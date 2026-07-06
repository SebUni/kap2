"""Maßnahmen-Engine (generalisiert für alle KAP3-Maßnahmen).

Eine Maßnahme reduziert ihre Zielkomponente(n) (``effect_target`` ∈ hazard/
exposure/vulnerability) in den abgedeckten Zellen, deckungs-skaliert. Da der
Risiko-Index multiplikativ in H·E·V ist, lässt sich die Wirkung auf die
verknüpften Risiken (``linked_risk_codes``) analytisch als Skalierung des Index
abbilden:

    factor = (1 - r_applied) ** n_targets
    neuer_Index = Basis-Index × factor

mit ``r_applied`` aus ``default_reduction`` und Deckungsgrad der Zelle.

Kosten je Maßnahme kommen aus den Katalog-Kostensätzen (CAPEX/OPEX). Der Nutzen ist
das **tatsächliche Delta der summierten Zellkosten** (E3): je abgedeckter Zelle und
verknüpftem Risiko ``Zellkosten · (1 − factor)``. Damit ist der ausgewiesene
Maßnahmen-Nutzen für pop-/area-skalierte Risiken exakt der Beitrag zur „Vermiedene
Schäden"-Kennzahl des Kommunen-Aggregats (dieselbe Σ-über-Zellen-Basis).
"""

from __future__ import annotations

import logging

from geoalchemy2 import functions as func
from sqlalchemy import case, literal
from sqlalchemy.orm import Session

from app.data import catalog, sources
from app.models.models import (
    AdaptationMeasure, CellAssessment, GridCell, MeasureImpact, Kommune,
)
from app.services import aggregate_cache, parameter_registry
from app.services.engine import impact, override_context, risk_engine, tunables

log = logging.getLogger(__name__)

# Defaults der Folgekosten-Konsolidierung (identisch zu impact/params.py IMPACT_GLOBAL_SPECS;
# override-fähig über impact.k_indirect / impact.restoration_share).
_K_INDIRECT_DEFAULT = 0.25
_RESTORATION_SHARE_DEFAULT = 0.15


def _reconsolidate_cell_folgekosten(risks: dict[str, dict]) -> None:
    """Bildet die Folgekosten einer Zelle aus ihren (ggf. maßnahmenbedingt reduzierten)
    direkten Sektorschäden neu — in-place, analog ``impact.consolidate_indirect`` (§8/B3).

    Ohne diesen Schritt bliebe nach Anwendung der Maßnahmen ``indirekt = k · Σ direkt``
    auf dem VOR-Maßnahmen-Stand stehen (die direkten Schäden sind reduziert, die daran
    gekoppelten Folgekosten aber nicht) — eine Inkonsistenz im Aggregat „mit Maßnahmen".
    Direkte Sektorschäden sind monetär (outcome == €), daher Summe über ``outcome``.
    """
    direct = sum(float(risks[c].get("outcome", 0.0))
                 for c in catalog.DIRECT_SECTOR_RISK_CODES if c in risks)
    k = float(override_context.get_override("impact.k_indirect", _K_INDIRECT_DEFAULT))
    r_share = float(override_context.get_override(
        "impact.restoration_share", _RESTORATION_SHARE_DEFAULT))
    for code, value in (("EXPECTED_INDIRECT_ECONOMIC_LOSS_EUR", k * direct),
                        ("EXPECTED_RESTORATION_COSTS_EUR", r_share * direct)):
        if code in risks:
            risks[code] = {"index": risks[code].get("index", 0.0),
                           "outcome": value, "cost_eur": value}
    # supply/location/delayed bleiben 0 (in k_indirekt enthalten) — nichts zu tun.


def _cell_cost(risk: dict, cell_risk: dict, cell_pop: float) -> float:
    """Zellkosten eines Risikos – identische Basis wie ``risk_engine.aggregate``.

    Kosten werden LIVE aus dem gespeicherten ``outcome`` × aktuellem Kostensatz
    abgeleitet (``cost_from_outcome``), NICHT aus dem materialisierten ``cost_eur``
    gelesen — so wirken Kostensatz-Overrides ohne Neuberechnung, und die Reconciliation
    (Maßnahmen-Nutzen == Aggregat-Delta) bleibt exakt, weil ``aggregate`` dieselbe
    Ableitung nutzt (§8/B2). Für Alt-Zelldaten ohne Outcome (Kommune vor Neuberechnung)
    den Outcome über den linearen Legacy-Weg nachrechnen.
    """
    o = cell_risk.get("outcome")
    if o is None:
        idx = float(cell_risk.get("index", 0.0))
        o = impact.compute_cell_impacts(risk, idx, cell_pop)["outcome"]
    return risk_engine.cost_from_outcome(risk, float(o))


def _coverage(db: Session, measure: AdaptationMeasure) -> tuple[dict[int, float], float]:
    """Deckungsgrad (0..1) je Zelle plus abgedeckte Gesamtfläche (m²).

    Die Fläche wird als Σ (cell_size_m² · frac) über alle schneidenden Zellen
    bestimmt; die 3857-Verzerrung kürzt sich im frac-Verhältnis heraus. Sie wird
    hier zentral berechnet, weil sowohl die Kosten- als auch die Wirkungs-
    skalierung (unit_factor) die Gesamtfläche vor der Zell-Schleife brauchen.
    """
    cell_area = func.ST_Area(func.ST_Transform(GridCell.geometry, 3857))
    inter = func.ST_Area(func.ST_Transform(
        func.ST_Intersection(GridCell.geometry, measure.geometry), 3857))
    frac = case((cell_area > 0, inter / cell_area), else_=literal(0.0))
    rows = (
        db.query(GridCell.id, GridCell.cell_size_m, frac.label("frac"))
        .filter(GridCell.kommune_id == measure.kommune_id,
                func.ST_Intersects(GridCell.geometry, measure.geometry))
        .all()
    )
    frac_map: dict[int, float] = {}
    covered_area_m2 = 0.0
    for r in rows:
        f = max(0.0, min(1.0, float(r.frac)))
        frac_map[r.id] = f
        size = float(r.cell_size_m or 100)
        covered_area_m2 += (size ** 2) * f
    return frac_map, covered_area_m2


def _reduction_factor(mdef: dict, fraction: float, unit_factor: float = 1.0) -> float:
    """Kombinierter Skalierungsfaktor (0..1) für den Risiko-Index einer Zelle.

    ``unit_factor`` (0..1) skaliert die Wirkung von Stück-Maßnahmen anhand der
    Anzahl gegenüber dem Richtwert (min(1, Anzahl/Richtwert)); für Flächen-
    maßnahmen ist er 1.0 und lässt die bisherige Rechnung unverändert.
    """
    base_r = float(mdef.get("default_reduction", 0.0))
    if mdef.get("coverage_scaling") == "saturating":
        r = base_r * min(1.0, fraction * tunables.effective_measure_saturation())
    else:
        r = base_r * fraction
    r = r * unit_factor
    r = max(0.0, min(tunables.effective_measure_reduction_cap(), r))
    n = max(1, len(mdef.get("effect_target", []) or []))
    return (1.0 - r) ** n


def _resolve_count(
    mdef: dict, config: dict | None, covered_area_m2: float
) -> tuple[int, bool, int]:
    """Stückzahl, Default-Flag und Richtwert-Anzahl einer Maßnahme.

    Flächenmaßnahmen (``unit_label`` is None) haben keine Stück-Logik ⇒
    (0, False, 0). Fehlt ``config["count"]``, greift die Richtwert-Anzahl aus der
    Dichte als Default (``is_default=True``), damit Bestandsmaßnahmen ohne
    Frontend-Eingabe weiter sinnvoll rechnen.
    """
    if mdef.get("unit_label") is None:
        return 0, False, 0
    density = float(mdef.get("unit_density_per_ha") or 0.0)
    recommended = max(1, round(density * covered_area_m2 / 10_000))
    raw = (config or {}).get("count")
    if raw is None:
        return recommended, True, recommended
    return max(0, int(round(float(raw)))), False, recommended


def _unit_effect_factor(count: int, recommended_count: int) -> float:
    """Wirkungs-Skalierung 0..1 aus Anzahl vs. Richtwert (1.0 ohne Stück-Logik)."""
    if recommended_count > 0:
        return min(1.0, count / recommended_count)
    return 1.0


# Kostenkomponenten je Block (CAPEX einmalig / OPEX jährlich). quantity_kind:
# fixed = mengenunabhängige Pauschale (Menge 1), unit = Stückzahl (Einheit = unit_label),
# area = Fläche (Einheit m²).
_CAPEX_COMPONENTS: tuple[tuple[str, str, str], ...] = (
    ("capex_fixed", "Grundkosten (Planung/Konzept)", "fixed"),
    ("capex_per_unit", "Investition je {unit}", "unit"),
    ("capex_per_m2", "Investition je m²", "area"),
)
_OPEX_COMPONENTS: tuple[tuple[str, str, str], ...] = (
    ("opex_fixed_year", "Feste Betriebskosten/Jahr", "fixed"),
    ("opex_per_unit_year", "Betrieb & Unterhalt je {unit}/Jahr", "unit"),
    ("opex_per_m2_year", "Betrieb & Unterhalt je m²/Jahr", "area"),
)


def _component_source(mdef: dict, field: str) -> tuple[str, str, bool]:
    """(Quelle, Herleitung/Detail, overridden) einer Kostenkomponente.

    ``source`` ist das kurze Inline-Label (z. B. "Berliner Wasserbetriebe"),
    ``detail`` die ausführliche Herleitung/Volltext-Quelle für den Hover-Tooltip:
    woher der Zahlenwert stammt bzw. – wenn er nicht direkt einer Quelle entnommen
    ist – wie er hergeleitet/plausibilisiert wurde. Ein kommunaler
    ``custom_source``-Override hat beim Kurz-Label Vorrang.
    """
    custom = (mdef.get("custom_sources") or {}).get(field)
    detail = (mdef.get("source_details") or {}).get(field) or ""
    if custom:
        return custom, detail, True
    source = (mdef.get("sources") or {}).get(field) or mdef.get("source") or ""
    return source, detail, False


def compute_costs(mdef: dict, count: int, area_m2: float) -> dict:
    """Kosten-Rohdaten (capex + opex) mit Komponenten-Breakdown.

    CAPEX  = capex_fixed + count·capex_per_unit + area·capex_per_m2,
    OPEX/a = opex_fixed_year + count·opex_per_unit_year + area·opex_per_m2_year.
    Nur Komponenten, deren Katalogfeld ``is not None`` ist, tauchen auf; ``0.0``
    gilt als anwendbar (z. B. kostenlose Bauverbote). Jede Komponente trägt
    Einzelpreis, Menge, Betrag und Quelle inkl. Override-Flag.
    """
    unit_label = mdef.get("unit_label") or "Einheit"

    def _block(specs: tuple[tuple[str, str, str], ...]) -> dict:
        components: list[dict] = []
        total = 0.0
        for field, label_tpl, kind in specs:
            unit_price = mdef.get(field)
            if unit_price is None:
                continue
            unit_price = float(unit_price)
            if kind == "unit":
                quantity, quantity_unit = count, unit_label
            elif kind == "area":
                quantity, quantity_unit = round(float(area_m2), 2), "m²"
            else:  # fixed
                quantity, quantity_unit = 1, "pauschal"
            amount = round(unit_price * quantity, 2)
            total += amount
            source, source_detail, overridden = _component_source(mdef, field)
            refs = sources.resolve((mdef.get("source_refs") or {}).get(field))
            components.append({
                "param": field,
                "label": label_tpl.format(unit=unit_label),
                "unit_price": unit_price,
                "quantity": quantity,
                "quantity_unit": quantity_unit,
                "amount_eur": amount,
                "source": source,
                "source_detail": source_detail,
                "references": refs,
                "overridden": overridden,
            })
        return {"total_eur": round(total, 2), "components": components}

    return {
        "capex": _block(_CAPEX_COMPONENTS),
        "opex": _block(_OPEX_COMPONENTS),
    }


def _measure_custom_sources(db_overrides: list[dict], measure_code: str) -> dict[str, str]:
    """Per-Feld ``custom_source``-Overrides einer Maßnahme (measures.<code>.<field>)."""
    prefix = f"measures.{measure_code}."
    out: dict[str, str] = {}
    for o in db_overrides:
        pid = o.get("parameter_id") or ""
        cs = o.get("custom_source")
        if cs and pid.startswith(prefix):
            out[pid[len(prefix):]] = cs
    return out


def compute_impact(db: Session, measure_id: int) -> dict:
    """Berechnet die Wirkung einer Maßnahme, speichert MeasureImpact und gibt
    eine Zusammenfassung (Index-Reduktion, Kosten, Nutzen) zurück."""
    measure = db.query(AdaptationMeasure).filter(AdaptationMeasure.id == measure_id).first()
    if not measure:
        raise ValueError(f"Maßnahme {measure_id} nicht gefunden")

    mdef = catalog.MEASURES_BY_CODE.get(measure.measure_type)
    if not mdef:
        raise ValueError(f"Unbekannter Maßnahmentyp: {measure.measure_type}")

    db_overrides = parameter_registry.load_db_overrides(db, measure.kommune_id)
    overrides = parameter_registry.overrides_map(db_overrides)
    mdef = parameter_registry.resolve_measure_def(mdef, overrides)
    mdef = {**mdef, "custom_sources": _measure_custom_sources(db_overrides, measure.measure_type)}

    # Kommune-Overrides für alle Live-Reads dieses Laufs installieren (k_indirekt,
    # Kostensätze in _cell_cost, Sättigung/Kappung in _reduction_factor): ohne Scope
    # läse dieser Request-Pfad die Overrides der zuletzt gerechneten Kommune
    # (Cross-Kommune-Leak, MODELL_KRITIK §8/B2).
    with override_context.override_scope(overrides):
        return _compute_impact_scoped(db, measure, mdef)


def _compute_impact_scoped(db: Session, measure: AdaptationMeasure, mdef: dict) -> dict:
    """Kern von ``compute_impact`` — läuft innerhalb des Override-Scopes der Kommune."""
    measure_id = measure.id
    coverage, covered_area_m2 = _coverage(db, measure)
    if not coverage:
        db.query(MeasureImpact).filter(MeasureImpact.measure_id == measure_id).delete()
        no_coverage = {"measure_id": measure_id, "affected_cells": 0, "message": "Keine überlappenden Zellen"}
        measure.impact_summary = no_coverage
        db.commit()
        return no_coverage

    # Anzahl/Wirkungsskalierung brauchen die Gesamtfläche vor der Zell-Schleife.
    count, count_is_default, recommended_count = _resolve_count(mdef, measure.config, covered_area_m2)
    unit_factor = _unit_effect_factor(count, recommended_count)

    linked = mdef.get("linked_risk_codes", [])
    cell_ids = list(coverage.keys())
    assessments = {
        ca.grid_cell_id: ca for ca in
        db.query(CellAssessment).filter(CellAssessment.grid_cell_id.in_(cell_ids)).all()
    }

    db.query(MeasureImpact).filter(MeasureImpact.measure_id == measure_id).delete()

    # Nutzen = tatsächliches Delta der summierten Zellkosten (E3): je abgedeckter Zelle
    # und verknüpftem Risiko  Zellkosten · (1 − factor). Für pop-/area-skalierte Risiken
    # ist das exakt der Beitrag dieser Maßnahme zu „Vermiedene Schäden" (Σ-über-Zellen im
    # Aggregat), weil dieselbe Zellkosten-Basis (``_cell_cost`` = Aggregat-Basis) und
    # derselbe multiplikative Zell-Faktor benutzt werden. Flache Ausfall-Risiken
    # (kommunenweiter P90-Einzelwert) sind nicht zell-additiv — ihr Nutzen wird unten
    # separat als Delta der kommunenweiten P90-Outcome-Kosten gerechnet.
    covered_base_index: dict[str, float] = {}
    covered_new_index: dict[str, float] = {}
    annual_benefit_damage = 0.0
    # Vermeidet eine Maßnahme direkte Sektorschäden, sinken auch die daran gekoppelten
    # Folgekosten (indirekt = k · Σ direkte Schäden). Dieser Anteil wird im Kommunen-
    # Aggregat „mit Maßnahmen" über die Rekonsolidierung (siehe _adjusted_cell_data)
    # mitreduziert; damit der Einzelmaßnahmen-Nutzen dazu passt, wird er hier ergänzt (§8/B3).
    k_indirect = float(override_context.get_override("impact.k_indirect", _K_INDIRECT_DEFAULT))

    for cid, frac in coverage.items():
        ca = assessments.get(cid)
        if not ca:
            continue
        factor = _reduction_factor(mdef, frac, unit_factor)
        data = ca.data or {}
        cell_pop = float(data.get("inputs", {}).get("pop", 0.0) or 0.0)
        cell_risks = data.get("risks", {})
        deltas = {}
        for code in linked:
            r = cell_risks.get(code, {})
            base_idx = float(r.get("index", 0.0))
            new_idx = base_idx * factor
            deltas[code] = round(new_idx - base_idx, 3)
            covered_base_index[code] = covered_base_index.get(code, 0.0) + base_idx
            covered_new_index[code] = covered_new_index.get(code, 0.0) + new_idx
            risk = catalog.RISKS_BY_CODE.get(code)
            if (risk and catalog.risk_contributes_to_total(risk)
                    and risk.get("scale", "pop") in ("pop", "area")):
                reduced = _cell_cost(risk, r, cell_pop) * (1.0 - factor)
                annual_benefit_damage += reduced
                # gekoppelte Folgekosten (nur direkte Sektorschäden treiben k_indirekt)
                if code in catalog.DIRECT_SECTOR_RISK_CODES:
                    annual_benefit_damage += k_indirect * reduced
        db.add(MeasureImpact(measure_id=measure_id, grid_cell_id=cid, indicator_deltas=deltas))

    # Flat-skalierte verknüpfte Risiken (z. B. Ausfallstunden bei Netzverstärkung):
    # Das Aggregat rechnet sie als kommunenweiten P90-Outcome — der Nutzen dieser
    # Maßnahme ist die Differenz der P90-Outcome-Kosten ohne/mit ihrem Zell-Faktor
    # (identische Logik wie ``_adjusted_cell_data``/``aggregate``, inkl. Pop-Skalierung
    # der flat-€-Bewertung). Vorher zeigten solche Maßnahmen hier 0 € Nutzen trotz
    # CAPEX. Deckt die Maßnahme zu wenige Zellen ab, um das P90 zu bewegen, bleibt der
    # Nutzen ehrlich 0 (konsistent: auch das Aggregat würde sich nicht ändern).
    annual_benefit_flat = 0.0
    flat_linked = [
        catalog.RISKS_BY_CODE[c] for c in linked
        if c in catalog.RISKS_BY_CODE
        and catalog.RISKS_BY_CODE[c].get("scale", "pop") not in ("pop", "area")
        and catalog.risk_contributes_to_total(catalog.RISKS_BY_CODE[c])
    ]
    if flat_linked:
        kommune = db.query(Kommune).filter(Kommune.id == measure.kommune_id).first()
        total_pop = float(kommune.population or 0) if kommune else 0.0
        kommune_area_km2 = float(kommune.area_km2 or 0) if kommune else 0.0
        all_rows = db.query(CellAssessment).filter(
            CellAssessment.kommune_id == measure.kommune_id).all()
        for risk in flat_linked:
            rcode = risk["code"]
            base_indices: list[float] = []
            adj_indices: list[float] = []
            for ca in all_rows:
                idx = float((ca.data or {}).get("risks", {}).get(rcode, {}).get("index", 0.0))
                base_indices.append(idx)
                frac = coverage.get(ca.grid_cell_id)
                if frac:
                    idx *= _reduction_factor(mdef, frac, unit_factor)
                adj_indices.append(idx)
            base_p90 = risk_engine._percentile(base_indices)
            adj_p90 = risk_engine._percentile(adj_indices)
            if adj_p90 >= base_p90:
                continue
            base_cost = risk_engine.estimate_outcome_and_cost(
                risk, base_p90, total_pop, kommune_area_km2)["cost_eur"]
            adj_cost = risk_engine.estimate_outcome_and_cost(
                risk, adj_p90, total_pop, kommune_area_km2)["cost_eur"]
            annual_benefit_flat += max(0.0, base_cost - adj_cost)

    # Kosten (CAPEX + OPEX, je fix/Stück/Fläche; None-Felder erzeugen keine Komponente)
    cost_breakdown = compute_costs(mdef, count, covered_area_m2)
    capex = cost_breakdown["capex"]["total_eur"]
    opex_annual = cost_breakdown["opex"]["total_eur"]
    annual_benefit_direct = float(mdef.get("benefit_per_m2_year") or 0.0) * covered_area_m2

    avg_reduction = 0.0
    if covered_base_index:
        tot_b = sum(covered_base_index.values())
        tot_n = sum(covered_new_index.values())
        avg_reduction = round((tot_b - tot_n) / tot_b * 100.0, 1) if tot_b > 0 else 0.0

    summary = {
        "measure_id": measure_id,
        "measure_type": measure.measure_type,
        "affected_cells": len(coverage),
        "affected_area_m2": round(covered_area_m2, 1),
        "linked_risk_codes": linked,
        "avg_index_reduction_pct": avg_reduction,
        "capex_eur": round(capex, 2),
        "opex_annual_eur": round(opex_annual, 2),
        "annual_benefit_eur": round(
            annual_benefit_direct + annual_benefit_damage + annual_benefit_flat, 2),
        # transparente Aufschlüsselung: flat-Anteil (kommunenweite P90-Risiken)
        "annual_benefit_flat_eur": round(annual_benefit_flat, 2),
        "count": count,
        "count_is_default": count_is_default,
        "recommended_count": recommended_count,
        "unit_label": mdef.get("unit_label"),
        "unit_factor": round(unit_factor, 4),
        "cost_breakdown": cost_breakdown,
    }

    # Persistiert am Maßnahmen-Objekt (bereits in der Session geladen) statt an
    # einer per Nachfrage-Query gesuchten MeasureImpact-Zelle - so unabhängig von
    # Flush-Reihenfolge/Autoflush-Konfiguration die einzige Quelle der Wahrheit
    # für Export/cost-summary, ohne dass diese neu rechnen müssen.
    measure.impact_summary = summary
    db.commit()

    return summary


def _adjusted_cell_data(db: Session, kommune_id: int, apply_measures: bool) -> list[dict]:
    """Liefert Per-Zell-Daten (ggf. mit angewandten Maßnahmen) für Aggregation."""
    assessments = db.query(CellAssessment).filter(
        CellAssessment.kommune_id == kommune_id).all()
    base = {ca.grid_cell_id: (ca.data or {}) for ca in assessments}

    if not apply_measures:
        return [dict(d) for d in base.values()]

    # Maßnahmen-Faktoren je Zelle/Risiko (multiplikativ kombiniert). Fläche, Anzahl
    # und unit_factor werden pro Maßnahme genauso bestimmt wie in compute_impact,
    # damit Dashboard ("mit Maßnahmen") und Sidebar nicht divergieren.
    factors: dict[int, dict[str, float]] = {}
    measures = db.query(AdaptationMeasure).filter(
        AdaptationMeasure.kommune_id == kommune_id).all()
    overrides = parameter_registry.overrides_map(
        parameter_registry.load_db_overrides(db, kommune_id)
    )
    for m in measures:
        mbase = catalog.MEASURES_BY_CODE.get(m.measure_type)
        if not mbase:
            continue
        mdef = parameter_registry.resolve_measure_def(mbase, overrides)
        frac_map, covered_area_m2 = _coverage(db, m)
        count, _, recommended = _resolve_count(mdef, m.config, covered_area_m2)
        unit_factor = _unit_effect_factor(count, recommended)
        for cid, frac in frac_map.items():
            factor = _reduction_factor(mdef, frac, unit_factor)
            cell_factors = factors.setdefault(cid, {})
            for code in mdef.get("linked_risk_codes", []):
                cell_factors[code] = cell_factors.get(code, 1.0) * factor

    out = []
    for cid, data in base.items():
        cell_pop = float(data.get("inputs", {}).get("pop", 0.0) or 0.0)
        new_data = {"risks": {}, "inputs": {"pop": cell_pop}}
        risks = data.get("risks", {})
        cell_factors = factors.get(cid, {})
        for code, r in risks.items():
            factor = cell_factors.get(code, 1.0)
            entry = {"index": float(r.get("index", 0.0)) * factor}
            # Der Maßnahmen-Faktor mindert den Screening-Index; die Schicht-B-Outcomes
            # hängen zwar an der Hazard-Intensität (nicht direkt am Index), werden hier
            # aber bewusst PROPORTIONAL zum Index-Faktor skaliert — die pragmatische
            # Brücke zwischen index-basierter Maßnahmenwirkung und der Kostenschicht
            # (bewusste Vereinfachung, keine „lineare Legacy-Rechnung"). aggregate()
            # summiert die Zell-Werte und leitet die Kosten live aus dem Outcome ab.
            if "outcome" in r:
                entry["outcome"] = float(r["outcome"]) * factor
            if "cost_eur" in r:
                entry["cost_eur"] = float(r["cost_eur"]) * factor
            new_data["risks"][code] = entry
        # Folgekosten (indirekt/Restaurierung) aus den NEUEN direkten Sektorschäden neu
        # bilden, sonst bliebe indirekt = k·Σ direkt VOR den Maßnahmen stehen (§8/B3).
        _reconsolidate_cell_folgekosten(new_data["risks"])
        out.append(new_data)
    return out


def _compute_risk_aggregate(db: Session, kommune_id: int, apply_measures: bool) -> dict:
    """Rechnet das Aggregat aus der DB (ohne Cache) — die eigentliche Arbeit."""
    kommune = db.query(Kommune).filter_by(id=kommune_id).first()
    total_pop = float(kommune.population or 0) if kommune else 0.0
    area_km2 = float(kommune.area_km2 or 0) if kommune else 0.0
    overrides = parameter_registry.overrides_map(
        parameter_registry.load_db_overrides(db, kommune_id))
    with override_context.override_scope(overrides):
        cell_data = _adjusted_cell_data(db, kommune_id, apply_measures)
        return risk_engine.aggregate(cell_data, total_pop, area_km2)


def get_risk_aggregate(db: Session, kommune_id: int, apply_measures: bool = False) -> dict:
    """Aggregiertes Risiko (mit/ohne Maßnahmen) inkl. Kosten — mit Datei-Cache.

    Das Aggregat lädt alle CellAssessment-Zeilen und aggregiert darüber; pro
    Dashboard-Load geschieht das mehrfach mit identischen Eingaben. Der
    ``aggregate_cache`` materialisiert das Ergebnis je ``(kommune_id,
    apply_measures)`` und wird an allen Mutationspunkten explizit invalidiert.

    Die Kommune-Overrides werden für die Dauer der Aggregation als aktiver Engine-Scope
    gesetzt (``override_scope``) — sonst läsen Kostensatz-/Legacy-Fallback-Pfade die
    Overrides der zuletzt gerechneten Kommune (Cross-Kommune-Leak, §8/B2). So wirken
    Kostensatz-Overrides zudem live auf die Aggregatsumme (``aggregate`` monetarisiert
    aus dem gespeicherten Outcome).
    """
    cached = aggregate_cache.load(kommune_id, apply_measures)
    if cached is not None:
        return cached
    result = _compute_risk_aggregate(db, kommune_id, apply_measures)
    aggregate_cache.store(kommune_id, apply_measures, result)
    return result
