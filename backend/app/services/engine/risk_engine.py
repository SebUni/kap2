"""Risiko-Kompositionsmotor.

Risiko = 100 · max_p(w_p · Ĥ_p · Ê_p · V̂_p) über die kuratierten Wirkungsketten
(``catalog.build_pathways``) → Index 0..100 (vergleichbare Metrik). Der Index ist
damit die stärkste einzelne Wirkungskette (Primärpfad w=1,0 dominiert, gedämpfte
Alternativpfade übernehmen nur, wenn sie deutlich stärker sind).

Warum Maximum statt gewichtetem Mittel: Beim Mittelwert hing die Index-Höhe von der
ANZAHL erzeugter Pfade ab (mehr Nebenpfade → stärkere Verdünnung des dominanten
Signals, MODELL_KRITIK §3.1/3.5). Das Maximum ist pfadanzahl-invariant und bildet die
tatsächlich treibende Kette ab. Kombiniert mit der Kuratierung der Pfade (nur fachlich
belegte Ketten, ``pathway_curation.py``) ersetzt das die frühere kartesische Erzeugung.

Kommune-Aggregation: 90.-Perzentil der Zell-Indizes je Risiko (statt Mittelwert),
damit belastete Zellen in Dashboard/Spinnendiagrammen sichtbar bleiben.
Kartenlayer: absolute Outcome-Werte pro Zelle via ``cell_outcome``.

Pathway-Gewichte: ``catalog.PATHWAY_WEIGHTS`` (degressiv je Pfadtyp; beim Import fest
eingelesene Modellkonstanten — bewusst KEINE Registry-Parameter, ein Override wäre
wegen ``_PATHWAYS`` wirkungslos). Compound/Cascade sind als Hazards mit
``max_of_constituent_hazards`` bzw. Konstantwert hinterlegt (siehe indicators.py).
"""

from __future__ import annotations

from app.data import catalog
from app.services.engine import override_context, tunables

CELL_AREA_KM2 = 0.01  # 100 m × 100 m Rasterzelle
AGGREGATION_PERCENTILE = 90.0

# Pathways je Risiko einmalig vorbauen
_PATHWAYS: dict[str, list[dict]] = {r["code"]: catalog.build_pathways(r) for r in catalog.RISKS}

# Expositions-Codes je Risiko (für das Expositions-Gate des Belastungs-P90):
# Zellen ohne relevante Exposition (unbewohnte Flur bei pop-skalierten Risiken,
# Zellen ohne Nutzfläche/Assets sonst) verdünnen das kommunale P90 sonst gegen 0.
_EXPOSURE_CODES: dict[str, set[str]] = {
    code: {p["exposure"] for p in paths} for code, paths in _PATHWAYS.items()
}


def normalize_hev(hev: dict) -> dict:
    """Normalisiert absolute H/E/V-Werte einer Zelle auf 0..1 (nur fürs Risiko)."""
    out = {"hazards": {}, "exposures": {}, "vulnerabilities": {}}
    for code, val in hev["hazards"].items():
        out["hazards"][code] = override_context.normalize_value(code, val)
    for code, val in hev["exposures"].items():
        out["exposures"][code] = override_context.normalize_value(code, val)
    for code, val in hev["vulnerabilities"].items():
        out["vulnerabilities"][code] = override_context.normalize_value(code, val)
    return out


def cell_risk_indices(hev_norm: dict) -> dict:
    """Berechnet für eine Zelle den Risiko-Index (0..100) je Risiko."""
    Hn = hev_norm["hazards"]
    En = hev_norm["exposures"]
    Vn = hev_norm["vulnerabilities"]
    result: dict[str, float] = {}
    for risk in catalog.RISKS:
        code = risk["code"]
        paths = _PATHWAYS[code]
        if not paths:
            result[code] = 0.0
            continue
        best = 0.0
        for p in paths:
            h = Hn.get(p["hazard"], 0.0)
            e = En.get(p["exposure"], 0.0)
            v = Vn.get(p["vulnerability"], 0.0)
            term = p["weight"] * h * e * v
            if term > best:
                best = term
        idx = 100.0 * best
        result[code] = round(min(100.0, idx), 2)
    return result


def _scale_factor(risk: dict, pop: float, area_km2: float) -> float:
    scale = risk.get("scale", "pop")
    if scale == "pop":
        return (pop or 0.0) / tunables.effective_ref_population()
    if scale == "area":
        return (area_km2 or 0.0) / tunables.effective_ref_area_km2()
    return 1.0  # flat (Index-Outcomes)


def cell_outcome(risk: dict, index: float, cell_pop: float,
                 cell_area_km2: float = CELL_AREA_KM2) -> float:
    """Absolute Outcome-Schätzung für eine einzelne Zelle (Kartenlayer)."""
    ref = override_context.effective_ref_value(risk["code"], float(risk.get("ref_value", 0.0)))
    factor = _scale_factor(risk, cell_pop, cell_area_km2)
    return ref * (index / 100.0) * factor


def cell_outcome_breakdown(risk: dict, index: float, cell_pop: float,
                           cell_area_km2: float = CELL_AREA_KM2) -> dict:
    """Zellbezogene Faktoren für Outcome = ref · (Index/100) · Skalierung (Tooltip)."""
    ref = override_context.effective_ref_value(risk["code"], float(risk.get("ref_value", 0.0)))
    factor = _scale_factor(risk, cell_pop, cell_area_km2)
    idx_frac = index / 100.0
    return {
        "ref_value": ref,
        "scale_factor": round(factor, 6),
        "index_fraction": round(idx_frac, 4),
        "cell_pop": round(cell_pop, 2),
        "cell_area_km2": cell_area_km2,
        "outcome": round(ref * idx_frac * factor, 4),
    }


def _percentile(values: list[float], pct: float = AGGREGATION_PERCENTILE) -> float:
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    k = (len(sorted_vals) - 1) * pct / 100.0
    f = int(k)
    c = min(f + 1, len(sorted_vals) - 1)
    if f == c:
        return sorted_vals[f]
    return sorted_vals[f] + (k - f) * (sorted_vals[c] - sorted_vals[f])


def cost_from_outcome(risk: dict, outcome: float) -> float:
    """Monetarisiert einen Outcome: monetäre Risiken 1:1 (€), sonst × Kostensatz."""
    if catalog.risk_is_monetary(risk):
        # ref_value liegt bereits in €/Jahr vor → Kostensatz implizit 1 €/€.
        return outcome
    rate = override_context.effective_cost_per_outcome(
        risk["code"], catalog.risk_default_cost_per_outcome(risk))
    return outcome * rate


def estimate_outcome_and_cost(risk: dict, agg_index: float, total_pop: float, area_km2: float) -> dict:
    """Outcome + Kosten für ein Risiko aus einem AGGREGIERTEN Index (P90).

    Nur noch für ``flat``-skalierte Risiken der primäre Rechenweg (kommunenweiter
    Einzelwert je Index, z. B. Ausfallstunden/Jahr, Index-Screening). pop-/area-
    skalierte Risiken werden in ``aggregate`` stattdessen als Summe der Zell-Outcomes
    gerechnet (Schicht B, §3.6).
    """
    factor = _scale_factor(risk, total_pop, area_km2)
    ref = override_context.effective_ref_value(risk["code"], float(risk.get("ref_value", 0.0)))
    outcome = ref * (agg_index / 100.0) * factor
    cost = cost_from_outcome(risk, outcome)
    # Flat-Risiken (Ausfallstunden): die STUNDEN sind kommunenweit (nicht pop-skaliert),
    # die €-Bewertung (VoLL/Kostensatz) ist aber auf die Last einer ~100.000-Ew.-Kommune
    # kalibriert und skaliert daher mit der Bevölkerung — sonst zahlt eine 5.000-Ew.-
    # Gemeinde denselben €-Ausfall wie eine Großstadt (MODELL_KRITIK §8, Befund B6).
    if risk.get("scale", "pop") not in ("pop", "area") and total_pop and total_pop > 0:
        cost *= total_pop / tunables.effective_ref_population()
    return {"outcome": round(outcome, 2), "cost_eur": round(cost, 2)}


def _cell_is_exposed(code: str, cell_pop: float, cell_exposures: dict | None) -> bool:
    """Expositions-Gate des Belastungs-P90: zählt die Zelle für dieses Risiko?

    pop-skalierte Risiken: nur bewohnte Zellen. area-/flat-Risiken: mindestens eine
    Pfad-Exposition > 0 (absolute Werte; der >0-Test ist einheitenunabhängig).
    Fallback für Zelldaten ohne ``exposures``-Key (adjustierte With-Measures-Daten,
    Alt-Bestände): pop-Gate bzw. kein Gate — nie strenger als die Datenlage erlaubt.
    """
    risk = catalog.RISKS_BY_CODE.get(code)
    if risk is not None and risk.get("scale", "pop") == "pop":
        return cell_pop > 0.0
    if cell_exposures is None:
        return True
    codes = _EXPOSURE_CODES.get(code)
    if not codes:
        return True
    return any(float(cell_exposures.get(e, 0.0) or 0.0) > 0.0 for e in codes)


def _top_share(weights: list[float], frac: float = 0.05) -> float:
    """Anteil der Summe, der auf die stärksten ``frac`` der Zellen entfällt (Konzentration)."""
    total = sum(weights)
    if total <= 0.0 or not weights:
        return 0.0
    k = max(1, int(len(weights) * frac))
    top = sorted(weights, reverse=True)[:k]
    return round(sum(top) / total, 4)


def aggregate(cell_data_list: list[dict], total_pop: float, area_km2: float) -> dict:
    """Aggregiert Risiken über alle Zellen (Schicht B: Summe statt P90 × Gesamtbev.).

    pop-/area-skalierte Risiken: ``outcome``/``cost_eur`` = **Summe der Zell-Outcomes**
    (jede Zelle mit ihrem Index, ihrer Bevölkerung und CELL_AREA_KM2). ``flat``-Risiken
    (kommunenweiter Einzelwert, z. B. Ausfallstunden, Index-Screening): P90-basiert wie
    bisher — eine Summe über Zellen wäre hier unsinnig.

    Je Risiko zusätzlich (auch für Prompt 7): ``p90_index`` (= ``index``, Screening),
    ``max_index``, ``outcome_sum``, ``aggregation`` (sum|p90), ``top5_share``
    (Konzentration: Anteil aus den stärksten 5 % Zellen), ``area_km2_affected`` und
    ``share_above_threshold`` (Zellen mit Index ≥ Risikozonen-Schwelle).

    Robuster Fallback für Alt-Zelldaten ohne materialisierten ``outcome`` (Kommune vor
    Neuberechnung): der Wert wird je Zelle über die Legacy-Impact-Funktion nachgerechnet.
    """
    from app.services.engine import impact  # lazy: Zyklus impact→risk_engine vermeiden
    from app.services.engine.impact import sanity  # lazy (impact/__init__ importiert risk_engine)

    # Live-Parameter model.risk_threshold (läuft innerhalb des Override-Scopes).
    _THR = tunables.effective_risk_threshold()

    n_cells = len(cell_data_list)
    indices_by_code: dict[str, list[float]] = {}
    exposed_indices_by_code: dict[str, list[float]] = {}  # nur expositionsrelevante Zellen
    sum_outcome: dict[str, float] = {}
    sum_cost: dict[str, float] = {}
    weights_by_code: dict[str, list[float]] = {}   # Zell-Beitrag (für top5_share)
    above_thr: dict[str, int] = {}

    for cd in cell_data_list:
        risks = cd.get("risks", {})
        cell_pop = float(cd.get("inputs", {}).get("pop", 0.0) or 0.0)
        cell_exposures = cd.get("exposures")
        for code, r in risks.items():
            idx = float(r.get("index", 0.0))
            indices_by_code.setdefault(code, []).append(idx)
            if _cell_is_exposed(code, cell_pop, cell_exposures):
                exposed_indices_by_code.setdefault(code, []).append(idx)
            if idx >= _THR:
                above_thr[code] = above_thr.get(code, 0) + 1
            risk = catalog.RISKS_BY_CODE.get(code)
            if risk is None or risk.get("scale", "pop") not in ("pop", "area"):
                continue
            o = r.get("outcome")
            if o is None:
                o = impact.compute_cell_impacts(risk, idx, cell_pop)["outcome"]
            else:
                o = float(o)
            # Kosten LIVE aus dem gespeicherten Outcome monetarisieren (statt das beim Lauf
            # materialisierte cost_eur zu summieren), damit Kostensatz-Overrides
            # (risks.*.cost_per_outcome) ohne Neuberechnung wirken (§8/B2). Monetäre
            # Risiken: cost == outcome; nicht-monetäre: outcome × effektiver Kostensatz.
            c = cost_from_outcome(risk, o)
            sum_outcome[code] = sum_outcome.get(code, 0.0) + o
            sum_cost[code] = sum_cost.get(code, 0.0) + c
            weights_by_code.setdefault(code, []).append(c if c else o)

    _class_bounds = tunables.risk_class_bounds()

    risk_out: dict[str, dict] = {}
    for risk in catalog.RISKS:
        code = risk["code"]
        vals = indices_by_code.get(code, [])
        p90_idx = round(_percentile(vals), 2)
        max_idx = round(max(vals) if vals else 0.0, 2)
        # Belastungs-P90: P90 nur über expositionsrelevante Zellen — unbewohnte/
        # nutzungsfreie Flur verdünnt die Anzeige-Leitgröße nicht mehr (§ Dashboard).
        exp_vals = exposed_indices_by_code.get(code, [])
        if exp_vals:
            exposed_p90 = round(_percentile(exp_vals), 2)
            exposure_share = round(len(exp_vals) / n_cells, 4) if n_cells else 0.0
            # Zusatz-Perzentile für die gestuften Radar-Bänder (Dashboard-Netzgrafik):
            # 0–P80 / P80–P85 / P85–P90 / P90–P95 / P95–Max. Über dieselbe exponierte
            # Zell-Verteilung, damit unbewohnte Flur die Stufen nicht verwässert.
            exposed_p80 = round(_percentile(exp_vals, 80.0), 2)
            exposed_p85 = round(_percentile(exp_vals, 85.0), 2)
            exposed_p95 = round(_percentile(exp_vals, 95.0), 2)
        else:
            exposed_p90 = p90_idx  # Gate matcht keine Zelle → ehrlicher Fallback
            exposure_share = 0.0
            exposed_p80 = exposed_p85 = exposed_p95 = exposed_p90
        if risk.get("scale", "pop") in ("pop", "area"):
            outcome = round(sum_outcome.get(code, 0.0), 2)
            cost = round(sum_cost.get(code, 0.0), 2)
            aggregation = "sum"
            top5 = _top_share(weights_by_code.get(code, []))
            # Plausibilitätsanker: Σ-über-Zellen-Outcome gegen die ref_value-Größenordnung
            # (loggt bei grober Abweichung, §6.6). Nur für Schicht-B-Summenrisiken sinnvoll.
            sanity_ratio = sanity.check(code, outcome, total_pop, area_km2)
        else:
            est = estimate_outcome_and_cost(risk, p90_idx, total_pop, area_km2)
            outcome, cost = est["outcome"], est["cost_eur"]
            aggregation = "p90"
            top5 = _top_share(vals)  # Konzentrations-Proxy aus der Index-Verteilung
            sanity_ratio = None  # flat: outcome == ref·P90/100 per Konstruktion (kein Anker)
        cnt = above_thr.get(code, 0)
        risk_out[code] = {
            "index": p90_idx,
            "p90_index": p90_idx,
            "exposed_p90_index": exposed_p90,
            "exposed_p80_index": exposed_p80,
            "exposed_p85_index": exposed_p85,
            "exposed_p95_index": exposed_p95,
            "exposure_share": exposure_share,
            "risk_class": tunables.classify_index(exposed_p90, _class_bounds),
            "max_index": max_idx,
            "outcome": outcome,
            "outcome_sum": outcome,
            "outcome_unit": risk["outcome_unit"],
            "cost_eur": cost,
            "cost_dimension": risk["cost_dimension"],
            "group": risk["group"],
            "name": risk["name"],
            "aggregation": aggregation,
            "top5_share": top5,
            "area_km2_affected": round(cnt * CELL_AREA_KM2, 4),
            "share_above_threshold": round(cnt / n_cells, 4) if n_cells else 0.0,
            "sanity_ratio": sanity_ratio,
        }

    # Gruppen-P90: Mittel der Einzelrisiko-P90-Indizes je KWRA-Gruppe;
    # exposed_index analog aus den Belastungs-P90-Werten (Anzeige-Leitgröße).
    groups: dict[str, dict] = {}
    for g in catalog.KWRA_GROUPS:
        codes = [r["code"] for r in catalog.RISKS if r["group"] == g["code"]]
        vals = [risk_out[c]["index"] for c in codes] if codes else [0.0]
        exp_vals_g = [risk_out[c]["exposed_p90_index"] for c in codes] if codes else [0.0]
        exposed_index = round(sum(exp_vals_g) / len(exp_vals_g), 2)
        # Gruppen-Bänder analog exposed_index: Mittel der jeweiligen Einzelrisiko-
        # Perzentile. Mittelwerte erhalten die Monotonie (P80 ≤ P85 ≤ P90 ≤ P95).
        _grp_mean = lambda key: round(
            sum(risk_out[c][key] for c in codes) / len(codes), 2) if codes else 0.0
        groups[g["code"]] = {
            "label": g["label"], "color": g["color"],
            "index": round(sum(vals) / len(vals), 2),
            "exposed_index": exposed_index,
            "exposed_p80_index": _grp_mean("exposed_p80_index"),
            "exposed_p85_index": _grp_mean("exposed_p85_index"),
            "exposed_p95_index": _grp_mean("exposed_p95_index"),
            "risk_class": tunables.classify_index(exposed_index, _class_bounds),
            "risk_codes": codes,
            "aggregation": f"P{int(AGGREGATION_PERCENTILE)}",
        }

    by_risk = sorted(
        [{"code": c, "name": r["name"], "cost_eur": r["cost_eur"],
          "outcome": r["outcome"], "outcome_unit": r["outcome_unit"],
          "cost_dimension": r["cost_dimension"], "index": r["index"],
          "exposed_p90_index": r["exposed_p90_index"], "risk_class": r["risk_class"],
          "aggregation": r["aggregation"], "top5_share": r["top5_share"]}
         for c, r in risk_out.items()],
        key=lambda x: x["cost_eur"], reverse=True,
    )
    # Nicht-additive Teilkennzahlen (z. B. Restaurierung = Anteil der Sektorschäden)
    # werden ausgewiesen, aber NICHT in die Summe addiert (Doppelzählung §3.7).
    total_cost = round(
        sum(r["cost_eur"] for r in by_risk
            if r["code"] not in catalog.NON_ADDITIVE_RISK_CODES),
        2,
    )

    return {
        "risks": risk_out,
        "groups": groups,
        "cost": {"total_eur": total_cost, "by_risk": by_risk},
        # Server-Wahrheit für die Frontend-Chips/Ringe: Grenzen + Labels der
        # Risikoklassen (abgeleitet aus model.risk_threshold, keine Hardcodes im UI).
        "classification": {
            "basis": "exposed_p90_index",
            "bounds": _class_bounds,
            "labels": tunables.RISK_CLASS_LABELS,
        },
    }
