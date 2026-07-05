"""Orchestriert einen vollständigen Assessment-Lauf für eine Kommune.

Ein einziger Pass berechnet pro 100m-Zelle: alle H/E/V (absolut), die
normalisierten Werte (intern) und alle Risiken (Index 0..100 + Outcome + Kosten).
Ergebnis ist eine Liste von Per-Zell-Daten-Dicts, die als ``CellAssessment.data``
gespeichert werden.
"""

from __future__ import annotations

import logging
import multiprocessing
import os
from typing import Any

from app.data import catalog
from app.services.engine.inputs import gather_cell_inputs
from app.services.engine.indicators import compute_cell_hev
from app.services.engine.auxiliary import build_auxiliary
from app.services.engine import impact, risk_engine
from app.services.engine.progress import RISK_COMPOSE, FINALIZE, lerp

log = logging.getLogger(__name__)

COASTAL_BUNDESLAENDER = {
    "Schleswig-Holstein", "Mecklenburg-Vorpommern", "Niedersachsen",
    "Hamburg", "Bremen",
}

_rw: dict = {}
_N_WORKERS = min(os.cpu_count() or 4, 8)
_MP = multiprocessing.get_context("fork")
_CHUNK = 50


def _risk_worker(idx: int) -> tuple[int, dict]:
    ci = _rw["cell_inputs"][idx]
    regional = _rw["regional"]
    hev = compute_cell_hev(ci, regional)
    hev_norm = risk_engine.normalize_hev(hev)
    indices = risk_engine.cell_risk_indices(hev_norm)

    # Per-Zell-Outcome + Kosten je Risiko materialisieren (Schicht B, Stufe 3): so wird
    # aggregate() zur reinen Summe und der GeoPackage-Export erhält gefüllte Spalten.
    # Null-Outcome/Kosten werden weggelassen (JSONB-Ersparnis); der Index bleibt immer.
    cell_pop = float(ci.get("pop", 0.0) or 0.0)
    risks: dict[str, dict] = {}
    for code, risk_idx in indices.items():
        rdef = catalog.RISKS_BY_CODE[code]
        imp = impact.compute_cell_impacts(rdef, risk_idx, cell_pop)
        entry = {"index": risk_idx}
        outcome = round(imp["outcome"], 4)
        cost = round(imp["cost_eur"], 2)
        if outcome:
            entry["outcome"] = outcome
        if cost:
            entry["cost_eur"] = cost
        risks[code] = entry

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
            f"Berechne klimatische Einflüsse, räumliche Expositionen & Sensitivitäten ({_N_WORKERS} Kerne)",
        )

    _rw["cell_inputs"] = cell_inputs
    _rw["regional"] = regional
    try:
        with _MP.Pool(_N_WORKERS) as pool:
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
