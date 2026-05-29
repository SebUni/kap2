"""Agriculture yield variability assessor — Levels 1–2.

Level 1: OSM-based agricultural fraction, irrigation access, exposure.
Level 2: Adds DWD frost/heat/drought/erosion data.

risk_score = f(ag_fraction × 0.3, no_irrigation × 0.3, heat_exposure × 0.2, storm_exp × 0.2)
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

# Late frost days per Bundesland (approximate)
_LATE_FROST: dict[str, float] = {
    "Baden-Württemberg": 3.5, "Bayern": 5.0, "Berlin": 2.5,
    "Brandenburg": 4.5, "Bremen": 2.0, "Hamburg": 2.0,
    "Hessen": 3.5, "Mecklenburg-Vorpommern": 4.0,
    "Niedersachsen": 3.0, "Nordrhein-Westfalen": 2.5,
    "Rheinland-Pfalz": 3.0, "Saarland": 3.0,
    "Sachsen": 4.5, "Sachsen-Anhalt": 4.0,
    "Schleswig-Holstein": 2.5, "Thüringen": 5.0,
}


def _cell_worker(idx: int):
    from app.services.climate.heat.osm_data import compute_cell_landuse
    return idx, compute_cell_landuse(_w["cells"][idx]["geometry"], _w["lu"])


class AgricultureAssessor(ClimateAssessor):
    climate_type = "agriculture"
    label = "Landwirtschaftliche Ertragsschwankungen"
    max_level = 2

    def get_required_config(self) -> list[ConfigParamDef]:
        return [
            ConfigParamDef("agriculture", "ag_fraction_weight", 0.3, "Gewichtung Agrarflächenanteil"),
            ConfigParamDef("agriculture", "irrigation_weight", 0.3, "Gewichtung fehlende Bewässerung"),
            ConfigParamDef("agriculture", "heat_weight", 0.2, "Gewichtung Hitzeexposition"),
            ConfigParamDef("agriculture", "storm_weight", 0.2, "Gewichtung Sturmexposition"),
        ]

    def get_indicators(self) -> list[IndicatorDef]:
        return [
            IndicatorDef("ag_fraction", "Agrarflächenanteil", "%", "Anteil landwirtschaftlicher Nutzfläche", 0, 100),
            IndicatorDef("irrigation_access", "Bewässerungszugang", "score", "Nähe zu Wasserquelle (0=nah, 10=fern)", 0, 10),
            IndicatorDef("heat_exposure", "Hitzeexposition", "score", "Offene Flächen → Hitzestress", 0, 10),
            IndicatorDef("storm_exposure", "Sturmexposition", "score", "Wind-Exposition offener Flächen", 0, 10),
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

        water_cells: set[int] = set()
        rc_map: dict[tuple[int, int], int] = {}
        for i, cell in enumerate(grid_cells):
            rc_map[(cell["row"], cell["col"])] = i
            for feat in lu_data:
                if feat.get("natural") == "water" and cell["geometry"].intersects(feat["geometry"]):
                    water_cells.add(i)
                    break

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
        frost = _LATE_FROST.get(bundesland, 3.5)
        frost_factor = frost / 3.5  # ≥1 = more frost risk

        results: list[CellResult] = []
        for i, cell in enumerate(grid_cells):
            lu = cell_lu.get(i, {})
            farmland = lu.get("farmland_fraction", 0.0)
            green = lu.get("green_fraction", 0.0)
            forest = lu.get("forest_fraction", 0.0)
            imp = lu.get("impervious_fraction", 0.05)

            # Agricultural fraction score
            ag_frac = farmland + max(0, green - forest) * 0.5

            # Hard gate: no agricultural risk without agriculture
            if ag_frac < 0.05:
                indicators = {
                    "ag_fraction": round(ag_frac * 100, 1),
                    "irrigation_access": 0.0,
                    "heat_exposure": 0.0,
                    "storm_exposure": 0.0,
                    "risk_score": 0.0,
                }
                results.append(CellResult(grid_cell_id=cell["id"], indicators=indicators, risk_score=0.0))
                continue

            ag_score = min(10.0, ag_frac * 12.0)

            # Irrigation access: distance to water (only for ag cells)
            r, c = cell["row"], cell["col"]
            min_dist = 999
            for dr in range(-6, 7):
                for dc in range(-6, 7):
                    ni = rc_map.get((r + dr, c + dc))
                    if ni is not None and ni in water_cells:
                        min_dist = min(min_dist, max(abs(dr), abs(dc)))
            irr_score = min(10.0, min_dist * 1.5) if min_dist < 999 else 8.0

            # Heat exposure: open, non-shaded agricultural cells are vulnerable
            shelter = forest + imp * 0.5  # trees and buildings provide some shelter
            heat_exp = min(10.0, max(0.0, (1.0 - shelter) * 10.0 * ag_frac))

            # Storm exposure: open flat farmland
            storm_exp = min(10.0, ag_frac * 8.0 * (1.0 - forest))

            w1 = float(config_params.get("agriculture.ag_fraction_weight", 0.3))
            w2 = float(config_params.get("agriculture.irrigation_weight", 0.3))
            w3 = float(config_params.get("agriculture.heat_weight", 0.2))
            w4 = float(config_params.get("agriculture.storm_weight", 0.2))

            raw = w1 * ag_score + w2 * irr_score + w3 * heat_exp + w4 * storm_exp
            if level >= 2:
                raw *= frost_factor
            rs = min(10.0, max(0.0, raw))

            indicators = {
                "ag_fraction": round(ag_frac * 100, 1),
                "irrigation_access": round(irr_score, 2),
                "heat_exposure": round(heat_exp, 2),
                "storm_exposure": round(storm_exp, 2),
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
            factors["rcp45"][y] = 1.0 + 0.25 * t
            factors["rcp85"][y] = 1.0 + 0.65 * t
        return factors


_instance = AgricultureAssessor()
registry.register(_instance)
