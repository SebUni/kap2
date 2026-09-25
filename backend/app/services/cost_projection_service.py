"""Kosten-Projektion 2025–2065: erwartete Jahresschäden mit und ohne Maßnahmen.

Skaliert die heutigen aggregierten Schadenskosten (``get_risk_aggregate``) mit
demselben regionalisierten DWD-Klimasignal wie die Risiko-Index-Projektion
(``projection_service.scenario_factors``) und preist auf dem Maßnahmenpfad die
Maßnahmenkosten ein: OPEX jährlich ab Umsetzungsjahr, CAPEX einmalig im
Umsetzungsjahr. Die kumulierten Kosten werden zusätzlich als Barwerte
ausgewiesen, abgezinst mit einer Diskontrate von 0 % und 1 %. Diese ist hier
gleich der Reinen Zeitpräferenzrate gesetzt (UBA Methodenkonvention 4.0,
Kap. 2.2.3); die Komponente der relativen Preise ist nicht angesetzt. Bewusste,
im Response dokumentierte Vereinfachung — Maßnahmenwirkung zeitkonstant.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from app.data import catalog
from app.services.climate.dwd_data import get_climate_projection
from app.services.measure_service import get_risk_aggregate, kommune_measures_query
from app.services.projection_service import scenario_factors

# Diskontraten von 0 % und 1 %, hier gleich der Reinen Zeitpräferenzrate (RZPR)
# der UBA Methodenkonvention 4.0, Kap. 2.2.3 gesetzt; die Komponente der
# relativen Preise ist nicht angesetzt. Mindestens zwei Werte berichten, um die
# Sensitivität gegenüber der Zeitpräferenz zu zeigen.
PURE_TIME_PREFERENCE_RATES: tuple[float, ...] = (0.0, 0.01)


def _group_costs(agg: dict) -> dict[str, float]:
    """Schadenskosten je KWRA-Gruppe (nicht-additive Sammelrisiken ausgeschlossen,
    damit die Gruppensumme der ausgewiesenen Gesamtsumme entspricht).

    Klasse-B-Wirkungen (Screening ohne Euro-Bezifferung, ``euro_layer: False``)
    werden ausgelassen, nicht als 0 gezählt: Sie tragen keinen Euro-Betrag, und
    eine Gruppe, die nur aus Klasse B besteht, erscheint nicht mit 0 €."""
    out: dict[str, float] = {}
    for r in agg["cost"]["by_risk"]:
        code = r["code"]
        if code in catalog.NON_ADDITIVE_RISK_CODES:
            continue
        spec = catalog.RISKS_BY_CODE.get(code)
        if (r.get("has_euro_layer") is False
                or (spec is not None and not catalog.risk_has_euro_layer(spec))):
            continue
        grp = catalog.RISKS_BY_CODE.get(code, {}).get("group", "other")
        out[grp] = out.get(grp, 0.0) + float(r["cost_eur"] or 0.0)
    return {g: round(v, 2) for g, v in out.items()}


def project_costs(db: Session, kommune_id: int, bundesland: str,
                  demo_session_id: str | None = None) -> dict:
    base = get_risk_aggregate(db, kommune_id, apply_measures=False)
    withm = get_risk_aggregate(db, kommune_id, apply_measures=True,
                               demo_session_id=demo_session_id)

    total_base = float(base["cost"]["total_eur"] or 0.0)
    total_with = float(withm["cost"]["total_eur"] or 0.0)

    proj = get_climate_projection(bundesland)
    years: list[int] = proj["years"]
    horizon_start, horizon_end = years[0], years[-1]

    # ── Maßnahmen: Kostenzeitpunkte bestimmen ─────────────────────────────
    default_impl_year = datetime.utcnow().year + 1
    measures = kommune_measures_query(db, kommune_id, demo_session_id).all()
    warnings: list[str] = []
    measure_rows: list[dict] = []
    for m in measures:
        summary = m.impact_summary or {}
        if not summary:
            warnings.append(
                f"Maßnahme „{m.name}“ ohne berechnete Wirkung — geht mit 0 € ein"
            )
        impl = m.implementation_year or default_impl_year
        if impl < horizon_start:
            impl = horizon_start  # Vergangenheit auf Projektionsstart clampen
        if impl > horizon_end:
            warnings.append(
                f"Maßnahme „{m.name}“ liegt mit Umsetzungsjahr {impl} außerhalb "
                f"des Projektionshorizonts (bis {horizon_end})"
            )
        measure_rows.append({
            "id": m.id,
            "name": m.name,
            "implementation_year": impl,
            "capex_eur": round(float(summary.get("capex_eur", 0.0) or 0.0), 2),
            "opex_annual_eur": round(float(summary.get("opex_annual_eur", 0.0) or 0.0), 2),
        })

    opex_by_year = [
        sum(r["opex_annual_eur"] for r in measure_rows if r["implementation_year"] <= y)
        for y in years
    ]
    capex_by_year = [
        sum(r["capex_eur"] for r in measure_rows if r["implementation_year"] == y)
        for y in years
    ]

    def _cumulative(series: list[float]) -> list[float]:
        out, running = [], 0.0
        for v in series:
            running += v
            out.append(round(running, 2))
        return out

    def _discounted(series: list[float]) -> dict[str, list[float]]:
        """Kumulierte Kosten als Barwerte je Diskontrate (UBA MK 4.0, Kap. 2.2.3):
        mindestens 0 % und 1 %, abgezinst auf das Basisjahr ``years[0]`` mit dem
        Faktor 1/(1+r)^(Jahr − Basisjahr). Die Diskontrate ist hier gleich der
        Reinen Zeitpräferenzrate gesetzt; die Komponente der relativen Preise
        ist nicht angesetzt."""
        out: dict[str, list[float]] = {}
        for rate in PURE_TIME_PREFERENCE_RATES:
            running, row = 0.0, []
            for year, value in zip(years, series):
                running += value / ((1.0 + rate) ** (year - years[0]))
                row.append(round(running, 2))
            out[str(rate)] = row
        return out

    def _scenario_block(scenario: str) -> dict:
        # Gefahrengruppen-spezifisch fortschreiben statt EINEN Gesamtwert linear zu
        # skalieren: Der Hitzeanteil folgt der konvexen Expositions-Wirkungs-Kurve,
        # die übrigen Gruppen dem Hitzetage-Trend. Vorher trug der Hitzetrend auch
        # Flut- und Sturmschäden — und die Konvexität fiel ganz unter den Tisch.
        groups_base = _group_costs(base)
        groups_with = _group_costs(withm)
        factors = {g: scenario_factors(proj, scenario, g) for g in set(groups_base) | set(groups_with)}
        n_years = len(years)

        def _series(group_costs: dict[str, float], total: float) -> list[float]:
            covered = sum(group_costs.values())
            # Nicht gruppierbarer Rest (nicht-additive Sammelrisiken) folgt dem
            # übergreifenden Klimasignal.
            rest = total - covered
            rest_f = scenario_factors(proj, scenario, None)
            out = []
            for i in range(n_years):
                v = rest * rest_f[i]
                for g, c in group_costs.items():
                    v += c * factors[g][i]
                out.append(round(v, 2))
            return out

        damages_no = _series(groups_base, total_base)
        damages_with = _series(groups_with, total_with)
        annual_with = [
            round(d + o + c, 2)
            for d, o, c in zip(damages_with, opex_by_year, capex_by_year)
        ]
        return {
            "label": proj["scenarios"][scenario].get("label", scenario),
            "no_measures": {
                "annual": damages_no,
                "cumulative": _cumulative(damages_no),
                "discounted": _discounted(damages_no),
            },
            "with_measures": {
                "annual": annual_with,
                "cumulative": _cumulative(annual_with),
                "discounted": _discounted(annual_with),
                "components": {
                    "damages": damages_with,
                    "opex": [round(v, 2) for v in opex_by_year],
                    "capex": [round(v, 2) for v in capex_by_year],
                },
            },
        }

    # Untergrenzen-Kennzeichnung (UBA MK 4.0, Anforderung 25): Die projizierten
    # Summen schreiben dieselben Wirkungskategorien fort wie die Basissumme — fehlt
    # dort ein belegter Kostensatz, sind auch die Projektionswerte Untergrenzen.
    lb = base["cost"].get("lower_bound")

    out = {
        "years": years,
        "base_year_damages_eur": round(total_base, 2),
        "has_measures": bool(measure_rows),
        "scenarios": {
            "rcp45": _scenario_block("rcp45"),
            "rcp85": _scenario_block("rcp85"),
        },
        "by_group_base": _group_costs(base),
        "measures": measure_rows,
        "assumptions": [
            "Skalierung der heutigen Schadenskosten mit dem regionalisierten "
            "DWD-Hitzetage-Trend (gleiches Klimasignal wie die Risiko-Projektion)",
            "CAPEX einmalig im Umsetzungsjahr (Default: Folgejahr); die "
            "kumulierten Kosten werden zusätzlich als Barwerte ausgewiesen, "
            "abgezinst mit einer Diskontrate von 0 % und 1 %, die hier gleich der "
            "Reinen Zeitpräferenzrate gesetzt ist; die Komponente der relativen "
            "Preise ist nicht angesetzt (Feld „discounted“, abgezinst "
            f"auf das Basisjahr {years[0]})",
            "Maßnahmenwirkung zeitkonstant über den Horizont; OPEX ab Umsetzungsjahr",
        ],
        "warnings": warnings,
        "source": proj.get("source"),
    }
    if lb is not None:
        out["lower_bound"] = lb
    return out
