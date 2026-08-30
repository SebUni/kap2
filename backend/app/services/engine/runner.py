"""Orchestriert einen vollständigen Assessment-Lauf für eine Kommune.

Ein einziger Pass berechnet pro 100m-Zelle: alle H/E/V (absolut), die
normalisierten Werte (intern) und alle Risiken (Index 0..100 + Outcome + Kosten).
Ergebnis ist eine Liste von Per-Zell-Daten-Dicts, die als ``CellAssessment.data``
gespeichert werden.
"""

from __future__ import annotations

import logging
from typing import Any

from app.services.engine.inputs import gather_cell_inputs
from app.services.engine.parallel import cow_pool, n_workers
from app.services.engine.indicators import compute_cell_hev
from app.services.engine.auxiliary import build_auxiliary
from app.services.engine import impact, risk_engine
from app.services.engine.impact.base import CellContext
from app.services.engine.progress import RISK_COMPOSE, FINALIZE, lerp

log = logging.getLogger(__name__)

COASTAL_BUNDESLAENDER = {
    "Schleswig-Holstein", "Mecklenburg-Vorpommern", "Niedersachsen",
    "Hamburg", "Bremen",
}

_rw: dict = {}
_CHUNK = 50


def _risk_worker(idx: int) -> tuple[int, dict]:
    ci = _rw["cell_inputs"][idx]
    regional = _rw["regional"]
    hev = compute_cell_hev(ci, regional)
    hev_norm = risk_engine.normalize_hev(hev)
    indices = risk_engine.cell_risk_indices(hev_norm)

    # Per-Zell-Outcome + Kosten je Risiko materialisieren (Schicht B): registrierte
    # Schadensfunktionen (Gesundheit ab Stufe 4) erhalten die volle CellContext, alle
    # übrigen rechnen den linearen Legacy-Weg. aggregate() summiert die Zell-Werte; der
    # GeoPackage-Export erhält gefüllte Spalten.
    ctx = CellContext(ci=ci, hev=hev, hev_norm=hev_norm, indices=indices, regional=regional)
    impacts = impact.compute_all_cell_impacts(ctx)
    risks: dict[str, dict] = {}
    for code, risk_idx in indices.items():
        imp = impacts.get(code, {})
        # Outcome/Kosten IMMER schreiben — auch echte 0-Werte. Ein FEHLENDER Schlüssel
        # bedeutet ausschließlich „Alt-Zelle vor Schicht B" und löst in aggregate()/
        # _cell_cost/get_layer den Legacy-Fallback (ref·Index/100·pop) aus. Würde ein
        # legitimer 0-Outcome (kühle Zelle unter der AF-Schwelle, Zelle ohne Asset/
        # Naturfläche) den Schlüssel weglassen, würde die Zelle fälschlich legacy-
        # nachgerechnet und erzeugte Phantomschaden (MODELL_KRITIK §8, Befund B1).
        # Outcome mit 6 Nachkommastellen: aggregate leitet die Kosten LIVE aus dem
        # gespeicherten Outcome × Kostensatz ab (§8/B2); bei großen Kostensätzen (VSL
        # 3,5 Mio €/Tod) würde eine gröbere Rundung kleiner Per-Zell-Outcomes den
        # €-Betrag spürbar verzerren.
        risks[code] = {
            "index": risk_idx,
            "outcome": round(imp.get("outcome", 0.0), 6),
            "cost_eur": round(imp.get("cost_eur", 0.0), 2),
        }
        # Teil-Ausweis unter der KWRA-Klammer (Bericht #95 §3.6): Hitzemortalität
        # rechnet nativ YLL und weist die Todesfälle zusätzlich aus.
        if "deaths" in imp:
            risks[code]["deaths"] = round(imp["deaths"], 6)

    data = {
        "hazards": hev["hazards"],
        "exposures": hev["exposures"],
        "vulnerabilities": hev["vulnerabilities"],
        "risks": risks,
        "auxiliary": build_auxiliary(ci, regional),
        "inputs": {
            k: (round(v, 4) if isinstance(v, float) else v)
            for k, v in ci.items()
            if k not in ("grid_cell_id", "row", "col")
        },
    }
    return idx, {"grid_cell_id": ci["grid_cell_id"], "data": data}


def run_full_assessment(
    grid_cells: list[dict],
    bundesland: str | None,
    kommune_population: int | None,
    area_km2: float | None,
    progress_callback: Any = None,
    parameter_overrides: dict[str, Any] | None = None,
    osm_id: str | None = None,
    centroid: tuple[float, float] | None = None,
) -> list[dict]:
    """Berechnet die komplette KAP3-Bewertung je Zelle.

    Gibt Liste von {grid_cell_id, data} zurück. ``centroid`` = (lon, lat) des
    Kommune-Zentroids für ortsaufgelöste regionale Treiber (Report §B2).
    """
    from app.services.engine.override_context import set_overrides

    set_overrides(parameter_overrides)
    is_coastal = (bundesland or "") in COASTAL_BUNDESLAENDER

    cell_inputs, regional = gather_cell_inputs(
        grid_cells, bundesland, kommune_population, area_km2, is_coastal, progress_callback,
        osm_id, centroid,
    )

    total = len(cell_inputs) or 1
    ordered: list[dict | None] = [None] * total

    if progress_callback:
        progress_callback(
            RISK_COMPOSE[0],
            f"Berechne klimatische Einflüsse, räumliche Expositionen & Sensitivitäten ({n_workers()} Kerne)",
        )

    _rw["cell_inputs"] = cell_inputs
    _rw["regional"] = regional
    try:
        with cow_pool() as pool:
            for done, (idx, result) in enumerate(
                pool.imap_unordered(_risk_worker, range(total), chunksize=_CHUNK)
            ):
                ordered[idx] = result
                if progress_callback and (done % 150 == 0 or done + 1 == total):
                    pct = lerp(RISK_COMPOSE[0], RISK_COMPOSE[1], (done + 1) / total)
                    progress_callback(pct, "Risikokomposition", f"{done + 1}/{total}")
    finally:
        _rw.clear()

    results = [r for r in ordered if r is not None]

    if progress_callback:
        progress_callback(FINALIZE[0], "Berechnung abschließen")

    return results
