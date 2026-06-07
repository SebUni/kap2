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
from app.services.engine.indicators import compute_cell_hev
from app.services.engine.auxiliary import build_auxiliary
from app.services.engine import risk_engine
from app.services.engine.progress import RISK_COMPOSE, FINALIZE, lerp

log = logging.getLogger(__name__)

COASTAL_BUNDESLAENDER = {
    "Schleswig-Holstein", "Mecklenburg-Vorpommern", "Niedersachsen",
    "Hamburg", "Bremen",
}


def run_full_assessment(
    grid_cells: list[dict],
    bundesland: str | None,
    kommune_population: int | None,
    area_km2: float | None,
    progress_callback: Any = None,
) -> list[dict]:
    """Berechnet die komplette KAP3-Bewertung je Zelle.

    Gibt Liste von {grid_cell_id, data} zurück.
    """
    is_coastal = (bundesland or "") in COASTAL_BUNDESLAENDER

    cell_inputs, regional = gather_cell_inputs(
        grid_cells, bundesland, kommune_population, area_km2, is_coastal, progress_callback,
    )

    total = len(cell_inputs) or 1
    results: list[dict] = []

    if progress_callback:
        progress_callback(RISK_COMPOSE[0], "Berechne Klimatreiber, Expositionen & Verwundbarkeiten")

    for i, ci in enumerate(cell_inputs):
        hev = compute_cell_hev(ci, regional)
        hev_norm = risk_engine.normalize_hev(hev)
        indices = risk_engine.cell_risk_indices(hev_norm)
        risks = {code: {"index": idx} for code, idx in indices.items()}

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
        results.append({"grid_cell_id": ci["grid_cell_id"], "data": data})

        if progress_callback and (i % 150 == 0 or i + 1 == total):
            pct = lerp(RISK_COMPOSE[0], RISK_COMPOSE[1], (i + 1) / total)
            progress_callback(pct, "Risikokomposition", f"{i + 1}/{total}")

    if progress_callback:
        progress_callback(FINALIZE[0], "Berechnung abschließen")

    return results
