"""Storms & Extreme Weather assessor — Levels 1–2.

Level 1: OSM-based wind exposure, building vulnerability, tree blowdown risk.
Level 2: Adds DWD storm frequency / max wind speed data.

risk_score = f(exposure × 0.4, building_vuln × 0.3, tree_risk × 0.3)
"""

import logging
import multiprocessing
import os
from typing import Any

from app.services.climate.base import (
    ClimateAssessor, CellResult, ConfigParamDef, IndicatorDef,
)
from app.services.climate import registry

log = logging.getLogger(__name__)

_w: dict = {}
_N_WORKERS = min(os.cpu_count() or 4, 8)
_MP = multiprocessing.get_context("fork")
_CHUNK = 50

# Storm frequency factor per Bundesland (relative to avg = 1.0)
_STORM_FREQ: dict[str, float] = {
    "Baden-Württemberg": 0.90, "Bayern": 0.85, "Berlin": 0.80,
    "Brandenburg": 0.85, "Bremen": 1.20, "Hamburg": 1.25,
    "Hessen": 1.00, "Mecklenburg-Vorpommern": 1.15,
    "Niedersachsen": 1.15, "Nordrhein-Westfalen": 1.10,
    "Rheinland-Pfalz": 0.95, "Saarland": 0.90,
    "Sachsen": 0.80, "Sachsen-Anhalt": 0.90,
    "Schleswig-Holstein": 1.35, "Thüringen": 0.85,
}


def _cell_worker(idx: int):
    from app.services.climate.heat.osm_data import compute_cell_landuse
    return idx, compute_cell_landuse(_w["cells"][idx]["geometry"], _w["lu"])


class StormsAssessor(ClimateAssessor):
    climate_type = "storms"
    label = "Stürme & Extremwetter"
    max_level = 2

    def get_required_config(self) -> list[ConfigParamDef]:
        return [
            ConfigParamDef("storms", "exposure_weight", 0.4, "Gewichtung Windexposition"),
            ConfigParamDef("storms", "building_weight", 0.3, "Gewichtung Gebäudevulnerabilität"),
            ConfigParamDef("storms", "tree_weight", 0.3, "Gewichtung Baumwurfrisiko"),
        ]

    def get_indicators(self) -> list[IndicatorDef]:
        return [
            IndicatorDef("wind_exposure", "Windexposition", "score", "Offene Fläche → Windbelastung", 0, 10),
            IndicatorDef("building_vulnerability", "Gebäudevulnerabilität", "score", "Verwundbarkeit der Bebauung", 0, 10),
            IndicatorDef("tree_blowdown_risk", "Baumwurfrisiko", "score", "Risiko durch Baumwurf", 0, 10),
            IndicatorDef("risk_score", "Risiko-Score", "", "Gesamtrisiko 0–10", 0, 10),
        ]

    def assess(self, kommune_id: int, level: int, grid_cells: list[dict],
               config_params: dict[str, Any], progress_callback: Any = None) -> list[CellResult]:
        global _w

        if progress_callback:
            progress_callback(2.0, "OSM-Daten laden", "Landnutzung abrufen")

        from app.services.climate.heat.osm_data import fetch_landuse
        lu_data, _ = fetch_landuse(grid_cells)

        if progress_callback:
            progress_callback(15.0, "Zellen berechnen")

        _w = {"cells": grid_cells, "lu": lu_data}
        rc_map: dict[tuple[int, int], int] = {}
        for i, cell in enumerate(grid_cells):
            rc_map[(cell["row"], cell["col"])] = i

        cell_lu: dict[int, dict] = {}
        total = len(grid_cells)
        with _MP.Pool(_N_WORKERS) as pool:
            for done_i, (idx, lu) in enumerate(pool.imap_unordered(_cell_worker, range(total), chunksize=_CHUNK)):
                cell_lu[idx] = lu
                if progress_callback and done_i % 200 == 0:
                    pct = 15.0 + 60.0 * done_i / total
                    progress_callback(pct, None, f"{done_i}/{total}")

        if progress_callback:
            progress_callback(78.0, "Risiko berechnen")

        bundesland = config_params.get("_bundesland", "Sachsen")
        storm_factor = _STORM_FREQ.get(bundesland, 1.0)

        w_exp = float(config_params.get("storms.exposure_weight", 0.4))
        w_bld = float(config_params.get("storms.building_weight", 0.3))
        w_tree = float(config_params.get("storms.tree_weight", 0.3))

        results: list[CellResult] = []
        for i, cell in enumerate(grid_cells):
            lu = cell_lu.get(i, {})
            imp = lu.get("impervious_fraction", 0.05)
            green = lu.get("green_fraction", 0.0)
            forest = lu.get("forest_fraction", 0.0)

            # Wind exposure: open areas with little shelter
            shelter = imp * 0.3 + forest * 0.5  # buildings and forest break wind
            exposure = min(10.0, max(0.0, (1.0 - shelter) * 10.0))

            # Building vulnerability: high impervious = more buildings at risk
            bldg_vuln = min(10.0, imp * 10.0)

            # Tree blowdown: more trees = more blowdown potential, especially conifers
            tree_risk = min(10.0, (forest + green * 0.3) * 12.0)

            # Edge effect: exposed tree lines near open areas
            r, c = cell["row"], cell["col"]
            if forest > 0.2:
                nb_open = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        ni = rc_map.get((r + dr, c + dc))
                        if ni is not None and ni in cell_lu:
                            if cell_lu[ni].get("forest_fraction", 0.0) < 0.1:
                                nb_open += 1
                if nb_open >= 3:  # forest edge
                    tree_risk = min(10.0, tree_risk * 1.5)

            raw = w_exp * exposure + w_bld * bldg_vuln + w_tree * tree_risk
            if level >= 2:
                raw *= storm_factor
            rs = min(10.0, max(0.0, raw))

            indicators = {
                "wind_exposure": round(exposure, 2),
                "building_vulnerability": round(bldg_vuln, 2),
                "tree_blowdown_risk": round(tree_risk, 2),
                "risk_score": round(rs, 2),
            }
            results.append(CellResult(grid_cell_id=cell["id"], indicators=indicators, risk_score=rs))

        if progress_callback:
            progress_callback(98.0, "Ergebnisse speichern")

        return results

    def get_projection_factors(self, bundesland: str) -> dict:
        factors: dict[str, dict[int, float]] = {"rcp45": {}, "rcp85": {}}
        for y in range(2025, 2066):
            t = (y - 2025) / 40.0
            factors["rcp45"][y] = 1.0 + 0.15 * t  # storms +15% by 2065
            factors["rcp85"][y] = 1.0 + 0.40 * t
        return factors


_instance = StormsAssessor()
registry.register(_instance)
