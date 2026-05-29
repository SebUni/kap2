"""Drought & Water Scarcity assessor — Levels 1–2.

Level 1: OSM-based green deficit, water proximity, and sealed fraction.
Level 2: Adds DWD precipitation/evapotranspiration data.

risk_score = f(sealed × 0.3, green_deficit × 0.4, water_distance × 0.3)
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

# Climatic water balance proxy: annual precip minus PET (mm)
_WATER_BALANCE: dict[str, float] = {
    "Baden-Württemberg": -30, "Bayern": -10, "Berlin": -120,
    "Brandenburg": -130, "Bremen": -40, "Hamburg": -30,
    "Hessen": -40, "Mecklenburg-Vorpommern": -90,
    "Niedersachsen": -30, "Nordrhein-Westfalen": -20,
    "Rheinland-Pfalz": -50, "Saarland": -30,
    "Sachsen": -100, "Sachsen-Anhalt": -130,
    "Schleswig-Holstein": 10, "Thüringen": -70,
}


def _cell_worker(idx: int):
    from app.services.climate.heat.osm_data import compute_cell_landuse
    return idx, compute_cell_landuse(_w["cells"][idx]["geometry"], _w["lu"])


class DroughtAssessor(ClimateAssessor):
    climate_type = "drought"
    label = "Dürre & Wasserknappheit"
    max_level = 2

    def get_required_config(self) -> list[ConfigParamDef]:
        return [
            ConfigParamDef("drought", "sealed_weight", 0.3, "Gewichtung Versiegelung"),
            ConfigParamDef("drought", "green_deficit_weight", 0.4, "Gewichtung Gründefizit"),
            ConfigParamDef("drought", "water_distance_weight", 0.3, "Gewichtung Wasserentfernung"),
        ]

    def get_indicators(self) -> list[IndicatorDef]:
        return [
            IndicatorDef("green_deficit", "Gründefizit", "%", "1 − Grünanteil", 0, 100),
            IndicatorDef("sealed_fraction", "Versiegelung", "%", "Versiegelter Flächenanteil", 0, 100),
            IndicatorDef("water_distance", "Wasserentfernung", "score", "Entfernung zum nächsten Gewässer", 0, 10),
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

        # Water cell index
        water_cells: set[int] = set()
        rc_map: dict[tuple[int, int], int] = {}
        for i, cell in enumerate(grid_cells):
            rc_map[(cell["row"], cell["col"])] = i
            for feat in lu_data:
                if feat.get("natural") == "water" and cell["geometry"].intersects(feat["geometry"]):
                    water_cells.add(i)
                    break

        # Compute land-use
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
        wb = _WATER_BALANCE.get(bundesland, -70)
        # Negative water balance = higher drought risk; scale 0–1
        drought_factor = min(1.5, max(0.5, 1.0 + (-wb - 50) / 200.0))

        w_s = float(config_params.get("drought.sealed_weight", 0.3))
        w_g = float(config_params.get("drought.green_deficit_weight", 0.4))
        w_w = float(config_params.get("drought.water_distance_weight", 0.3))

        results: list[CellResult] = []
        for i, cell in enumerate(grid_cells):
            lu = cell_lu.get(i, {})
            green = lu.get("green_fraction", 0.0)
            imp = lu.get("impervious_fraction", 0.05)

            green_deficit = 1.0 - green
            sealed_score = min(10.0, imp * 10.0)
            gd_score = min(10.0, green_deficit * 10.0)

            # Water distance
            r, c = cell["row"], cell["col"]
            min_dist = 999
            for dr in range(-6, 7):
                for dc in range(-6, 7):
                    ni = rc_map.get((r + dr, c + dc))
                    if ni is not None and ni in water_cells:
                        min_dist = min(min_dist, max(abs(dr), abs(dc)))
            wd_score = min(10.0, min_dist * 1.5) if min_dist < 999 else 8.0

            raw = w_s * sealed_score + w_g * gd_score + w_w * wd_score
            if level >= 2:
                raw *= drought_factor
            rs = min(10.0, max(0.0, raw))

            indicators = {
                "green_deficit": round(green_deficit * 100, 1),
                "sealed_fraction": round(imp * 100, 1),
                "water_distance": round(wd_score, 2),
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
            factors["rcp45"][y] = 1.0 + 0.35 * t  # +35% drought risk by 2065
            factors["rcp85"][y] = 1.0 + 0.90 * t  # +90%
        return factors


_instance = DroughtAssessor()
registry.register(_instance)
