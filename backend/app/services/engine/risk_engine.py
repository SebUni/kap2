"""Risiko-Kompositionsmotor.

Risiko = Σ(w · H_n · E_n · V_n) über die Wirkungsketten (``catalog.build_pathways``)
mit normalisierten Pathway-Gewichten → Index 0..100 (vergleichbare Metrik).
Zusätzlich werden Outcome-Schätzung (outcome_unit) und – wo monetär – Schadens-
kosten (€/Jahr) abgeleitet.

Aggregationsregel: ``weighted_sum_pathways`` mit ``NORMALIZE_PATHWAY_WEIGHTS``
(siehe model_parameters.csv). Compound/Cascade sind als Hazards mit
``max_of_constituent_hazards`` bzw. Konstantwert hinterlegt (siehe indicators.py).
"""

from __future__ import annotations

from app.data import catalog

# Pathways je Risiko einmalig vorbauen
_PATHWAYS: dict[str, list[dict]] = {r["code"]: catalog.build_pathways(r) for r in catalog.RISKS}
_WEIGHT_SUM: dict[str, float] = {
    code: (sum(p["weight"] for p in paths) or 1.0) for code, paths in _PATHWAYS.items()
}


def normalize_hev(hev: dict) -> dict:
    """Normalisiert absolute H/E/V-Werte einer Zelle auf 0..1 (nur fürs Risiko)."""
    out = {"hazards": {}, "exposures": {}, "vulnerabilities": {}}
    for code, val in hev["hazards"].items():
        out["hazards"][code] = catalog.normalize_value(code, val)
    for code, val in hev["exposures"].items():
        out["exposures"][code] = catalog.normalize_value(code, val)
    for code, val in hev["vulnerabilities"].items():
        out["vulnerabilities"][code] = catalog.normalize_value(code, val)
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
        acc = 0.0
        for p in paths:
            h = Hn.get(p["hazard"], 0.0)
            e = En.get(p["exposure"], 0.0)
            v = Vn.get(p["vulnerability"], 0.0)
            acc += p["weight"] * h * e * v
        idx = 100.0 * acc / _WEIGHT_SUM[code]
        result[code] = round(min(100.0, idx), 2)
    return result


def _scale_factor(risk: dict, total_pop: float, area_km2: float) -> float:
    scale = risk.get("scale", "pop")
    if scale == "pop":
        return (total_pop or 0.0) / 100_000.0
    if scale == "area":
        return (area_km2 or 0.0) / 50.0
    return 1.0  # flat (Index-Outcomes)


def estimate_outcome_and_cost(risk: dict, mean_index: float, total_pop: float, area_km2: float) -> dict:
    """Outcome-Schätzung + monetäre Kosten für ein Risiko."""
    factor = _scale_factor(risk, total_pop, area_km2)
    ref = float(risk.get("ref_value", 0.0))
    outcome = ref * (mean_index / 100.0) * factor
    cost_eur = 0.0
    dim = risk.get("cost_dimension")
    if dim == "monetary":
        cost_eur = outcome
    elif risk.get("cost_per_outcome_eur"):
        cost_eur = outcome * float(risk["cost_per_outcome_eur"])
    return {"outcome": round(outcome, 2), "cost_eur": round(cost_eur, 2)}


def aggregate(cell_data_list: list[dict], total_pop: float, area_km2: float) -> dict:
    """Aggregiert Risiken über alle Zellen.

    Gibt zurück:
      {
        "risks": {CODE: {index, max_index, outcome, cost_eur}},
        "groups": {GROUP: {index, label}},
        "cost": {total_eur, by_risk: [...]},
      }
    """
    n = len(cell_data_list) or 1
    sums: dict[str, float] = {}
    maxs: dict[str, float] = {}
    for cd in cell_data_list:
        risks = cd.get("risks", {})
        for code, r in risks.items():
            idx = float(r.get("index", 0.0))
            sums[code] = sums.get(code, 0.0) + idx
            if idx > maxs.get(code, 0.0):
                maxs[code] = idx

    risk_out: dict[str, dict] = {}
    for risk in catalog.RISKS:
        code = risk["code"]
        mean_idx = round(sums.get(code, 0.0) / n, 2)
        est = estimate_outcome_and_cost(risk, mean_idx, total_pop, area_km2)
        risk_out[code] = {
            "index": mean_idx,
            "max_index": round(maxs.get(code, 0.0), 2),
            "outcome": est["outcome"],
            "outcome_unit": risk["outcome_unit"],
            "cost_eur": est["cost_eur"],
            "cost_dimension": risk["cost_dimension"],
            "group": risk["group"],
            "name": risk["name"],
        }

    # Gruppen-Mittel (übergreifende Metrik)
    groups: dict[str, dict] = {}
    for g in catalog.KWRA_GROUPS:
        codes = [r["code"] for r in catalog.RISKS if r["group"] == g["code"]]
        vals = [risk_out[c]["index"] for c in codes] if codes else [0.0]
        groups[g["code"]] = {
            "label": g["label"], "color": g["color"],
            "index": round(sum(vals) / len(vals), 2),
            "risk_codes": codes,
        }

    by_risk = sorted(
        [{"code": c, "name": r["name"], "cost_eur": r["cost_eur"],
          "outcome": r["outcome"], "outcome_unit": r["outcome_unit"],
          "cost_dimension": r["cost_dimension"], "index": r["index"]}
         for c, r in risk_out.items()],
        key=lambda x: x["cost_eur"], reverse=True,
    )
    total_cost = round(sum(r["cost_eur"] for r in by_risk), 2)

    return {
        "risks": risk_out,
        "groups": groups,
        "cost": {"total_eur": total_cost, "by_risk": by_risk},
    }
