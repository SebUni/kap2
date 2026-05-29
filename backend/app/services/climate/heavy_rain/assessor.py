"""Heavy Rain & Urban Flooding assessor — Levels 1–2.

Level 1: OSM land-use based estimation of imperviousness, drainage proximity,
          and topographic wetness (approximated from neighbour cell patterns).
Level 2: Adds DWD regional precipitation data for frequency scaling.

risk_score = f(imperviousness × 0.5, drainage_distance × 0.3, low_elevation × 0.2)
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


def _cell_worker(idx: int):
    from app.services.climate.heat.osm_data import compute_cell_landuse
    return idx, compute_cell_landuse(_w["cells"][idx]["geometry"], _w["lu"])


# Precipitation fallback per Bundesland (mm/year, heavy-rain-days/year)
_PRECIP_DATA: dict[str, dict[str, float]] = {
    "Baden-Württemberg":      {"annual_mm": 940, "heavy_rain_days": 8.5},
    "Bayern":                 {"annual_mm": 950, "heavy_rain_days": 8.0},
    "Berlin":                 {"annual_mm": 570, "heavy_rain_days": 5.5},
    "Brandenburg":            {"annual_mm": 560, "heavy_rain_days": 5.0},
    "Bremen":                 {"annual_mm": 720, "heavy_rain_days": 6.5},
    "Hamburg":                {"annual_mm": 770, "heavy_rain_days": 7.0},
    "Hessen":                 {"annual_mm": 780, "heavy_rain_days": 7.5},
    "Mecklenburg-Vorpommern": {"annual_mm": 600, "heavy_rain_days": 5.5},
    "Niedersachsen":          {"annual_mm": 730, "heavy_rain_days": 6.5},
    "Nordrhein-Westfalen":    {"annual_mm": 870, "heavy_rain_days": 8.0},
    "Rheinland-Pfalz":        {"annual_mm": 780, "heavy_rain_days": 7.5},
    "Saarland":               {"annual_mm": 830, "heavy_rain_days": 7.5},
    "Sachsen":                {"annual_mm": 680, "heavy_rain_days": 6.0},
    "Sachsen-Anhalt":         {"annual_mm": 560, "heavy_rain_days": 5.0},
    "Schleswig-Holstein":     {"annual_mm": 790, "heavy_rain_days": 7.0},
    "Thüringen":              {"annual_mm": 700, "heavy_rain_days": 6.5},
}


class HeavyRainAssessor(ClimateAssessor):
    climate_type = "heavy_rain"
    label = "Starkregen & urbane Überflutungen"
    max_level = 2

    def get_required_config(self) -> list[ConfigParamDef]:
        return [
            ConfigParamDef("heavy_rain", "impervious_weight", 0.5,
                           "Gewichtung Versiegelungsgrad"),
            ConfigParamDef("heavy_rain", "drainage_weight", 0.3,
                           "Gewichtung Entwässerungsnähe"),
            ConfigParamDef("heavy_rain", "topo_weight", 0.2,
                           "Gewichtung topographische Senke"),
        ]

    def get_indicators(self) -> list[IndicatorDef]:
        return [
            IndicatorDef("imperviousness", "Versiegelungsgrad", "%", "Anteil versiegelter Fläche", 0, 100),
            IndicatorDef("drainage_proximity", "Entwässerungsnähe", "score", "Nähe zu Gewässern/Kanälen (0-10)", 0, 10),
            IndicatorDef("topographic_wetness", "Topografische Feuchte", "score", "Senkenlage-Index", 0, 10),
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
            progress_callback(15.0, "Zellen berechnen", f"0/{len(grid_cells)}")

        _w = {"cells": grid_cells, "lu": lu_data}

        # Build water proximity index from OSM data
        water_cells = set()
        for i, cell in enumerate(grid_cells):
            for feat in lu_data:
                if feat.get("natural") == "water" and cell["geometry"].intersects(feat["geometry"]):
                    water_cells.add(i)
                    break

        # Map (row,col) → index for neighbour lookup
        rc_map: dict[tuple[int, int], int] = {}
        for i, c in enumerate(grid_cells):
            rc_map[(c["row"], c["col"])] = i

        # DWD regional factor for Level 2
        bundesland = config_params.get("_bundesland", "Sachsen")
        precip = _PRECIP_DATA.get(bundesland, {"annual_mm": 700, "heavy_rain_days": 6.0})
        regional_factor = precip["heavy_rain_days"] / 6.5  # normalise to national average

        # Compute land-use per cell using multiprocessing
        cell_lu: dict[int, dict] = {}
        total = len(grid_cells)
        with _MP.Pool(_N_WORKERS) as pool:
            for done_i, (idx, lu) in enumerate(pool.imap_unordered(_cell_worker, range(total), chunksize=_CHUNK)):
                cell_lu[idx] = lu
                if progress_callback and done_i % 200 == 0:
                    pct = 15.0 + 65.0 * done_i / total
                    progress_callback(pct, None, f"{done_i}/{total} Zellen")

        if progress_callback:
            progress_callback(82.0, "Risiko berechnen")

        results: list[CellResult] = []
        w_imp = float(config_params.get("heavy_rain.impervious_weight", 0.5))
        w_drain = float(config_params.get("heavy_rain.drainage_weight", 0.3))
        w_topo = float(config_params.get("heavy_rain.topo_weight", 0.2))

        for i, cell in enumerate(grid_cells):
            lu = cell_lu.get(i, {})
            imp_frac = lu.get("impervious_fraction", 0.05)
            water_frac = lu.get("water_fraction", 0.0)

            # Imperviousness score (0-10)
            imp_score = min(10.0, imp_frac * 10.0)

            # Drainage proximity: cells near water bodies drain better (lower risk)
            r, c = cell["row"], cell["col"]
            min_dist = 999
            for dr in range(-5, 6):
                for dc in range(-5, 6):
                    if (r + dr, c + dc) in rc_map and rc_map[(r + dr, c + dc)] in water_cells:
                        d = max(abs(dr), abs(dc))
                        min_dist = min(min_dist, d)
            drain_score = min(10.0, min_dist * 2.0) if min_dist < 999 else 8.0
            if water_frac > 0.3:
                drain_score = max(0.0, drain_score - 3.0)

            # Topographic wetness: approximate—high imperviousness neighbours = pooling risk
            nb_imp = []
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    ni = rc_map.get((r + dr, c + dc))
                    if ni is not None and ni in cell_lu:
                        nb_imp.append(cell_lu[ni].get("impervious_fraction", 0.05))
            avg_nb_imp = sum(nb_imp) / len(nb_imp) if nb_imp else 0.05
            topo_score = min(10.0, (imp_frac + avg_nb_imp) * 5.0)

            raw = w_imp * imp_score + w_drain * drain_score + w_topo * topo_score
            if level >= 2:
                raw *= regional_factor

            rs = min(10.0, max(0.0, raw))

            indicators = {
                "imperviousness": round(imp_frac * 100, 1),
                "drainage_proximity": round(drain_score, 2),
                "topographic_wetness": round(topo_score, 2),
                "risk_score": round(rs, 2),
            }
            results.append(CellResult(grid_cell_id=cell["id"], indicators=indicators, risk_score=rs))

        if progress_callback:
            progress_callback(98.0, "Ergebnisse speichern")

        return results

    def get_projection_factors(self, bundesland: str) -> dict:
        precip = _PRECIP_DATA.get(bundesland, {"heavy_rain_days": 6.0})
        base = precip["heavy_rain_days"]
        factors: dict[str, dict[int, float]] = {"rcp45": {}, "rcp85": {}}
        for y in range(2025, 2066):
            t = (y - 2025) / 40.0
            factors["rcp45"][y] = 1.0 + 0.25 * t  # +25% more heavy rain days by 2065
            factors["rcp85"][y] = 1.0 + 0.70 * t  # +70%
        return factors


_instance = HeavyRainAssessor()
registry.register(_instance)
