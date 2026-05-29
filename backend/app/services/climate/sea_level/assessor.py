"""Sea Level Rise assessor — Levels 1–2.

Level 1: OSM-based coast proximity check. Inland = 0 for all cells.
Level 2: Adds IPCC projection-based inundation thresholds.

risk_score = f(coast_distance, elevation_estimate, coastal_infrastructure)
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

# Coastal Bundesländer (have coastline or are at direct tidal influence)
_COASTAL_STATES = {
    "Schleswig-Holstein", "Mecklenburg-Vorpommern", "Niedersachsen",
    "Bremen", "Hamburg",
}


def _cell_worker(idx: int):
    from app.services.climate.heat.osm_data import compute_cell_landuse
    return idx, compute_cell_landuse(_w["cells"][idx]["geometry"], _w["lu"])


class SeaLevelAssessor(ClimateAssessor):
    climate_type = "sea_level"
    label = "Meeresspiegelanstieg"
    max_level = 2

    def get_required_config(self) -> list[ConfigParamDef]:
        return [
            ConfigParamDef("sea_level", "coast_distance_weight", 0.5, "Gewichtung Küstenentfernung"),
            ConfigParamDef("sea_level", "elevation_weight", 0.3, "Gewichtung Höhenlage"),
            ConfigParamDef("sea_level", "infrastructure_weight", 0.2, "Gewichtung Küsteninfrastruktur"),
        ]

    def get_indicators(self) -> list[IndicatorDef]:
        return [
            IndicatorDef("coast_distance", "Küstenentfernung", "score", "Entfernung zur Küste (0=nah, 10=fern)", 0, 10),
            IndicatorDef("elevation_estimate", "Höhenschätzung", "score", "Geschätzte Höhe ü.NN (Proxy)", 0, 10),
            IndicatorDef("coastal_infrastructure", "Küsteninfrastruktur", "score", "Bebaute Fläche nahe Küste", 0, 10),
            IndicatorDef("is_coastal", "Küstenlage", "bool", "Liegt die Kommune an der Küste?", 0, 1),
            IndicatorDef("risk_score", "Risiko-Score", "", "Gesamtrisiko 0–10", 0, 10),
        ]

    def assess(self, kommune_id: int, level: int, grid_cells: list[dict],
               config_params: dict[str, Any], progress_callback: Any = None) -> list[CellResult]:
        global _w

        bundesland = config_params.get("_bundesland", "Sachsen")
        is_coastal = bundesland in _COASTAL_STATES

        # For inland Bundesländer: all cells get risk_score 0
        if not is_coastal:
            if progress_callback:
                progress_callback(50.0, "Kein Küstenrisiko", "Binnenland-Kommune")
            results = []
            for cell in grid_cells:
                indicators = {
                    "coast_distance": 10.0,
                    "elevation_estimate": 10.0,
                    "coastal_infrastructure": 0.0,
                    "is_coastal": 0.0,
                    "risk_score": 0.0,
                }
                results.append(CellResult(grid_cell_id=cell["id"], indicators=indicators, risk_score=0.0))
            if progress_callback:
                progress_callback(98.0, "Ergebnisse speichern")
            return results

        if progress_callback:
            progress_callback(2.0, "OSM-Daten laden", "Landnutzung abrufen")

        from app.services.climate.heat.osm_data import fetch_landuse
        lu_data, _ = fetch_landuse(grid_cells)

        if progress_callback:
            progress_callback(15.0, "Zellen berechnen")

        _w = {"cells": grid_cells, "lu": lu_data}

        # Find water cells (ocean/sea proxy)
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

        w_cd = float(config_params.get("sea_level.coast_distance_weight", 0.5))
        w_el = float(config_params.get("sea_level.elevation_weight", 0.3))
        w_in = float(config_params.get("sea_level.infrastructure_weight", 0.2))

        results: list[CellResult] = []
        for i, cell in enumerate(grid_cells):
            lu = cell_lu.get(i, {})
            imp = lu.get("impervious_fraction", 0.05)
            r, c = cell["row"], cell["col"]

            # Coast distance (proxy: distance to water cells, assuming coastal water)
            min_dist = 999
            for dr in range(-10, 11):
                for dc in range(-10, 11):
                    ni = rc_map.get((r + dr, c + dc))
                    if ni is not None and ni in water_cells:
                        min_dist = min(min_dist, max(abs(dr), abs(dc)))

            cell_size = cell.get("cell_size_m", 100)
            dist_m = min_dist * cell_size
            coast_score = max(0.0, 10.0 - dist_m / 200.0) if min_dist < 999 else 0.0

            # Elevation estimate: lower cells (near water) = higher risk
            elev_score = max(0.0, coast_score * 0.8)

            # Coastal infrastructure: built-up areas near coast are most vulnerable
            infra_score = min(10.0, imp * 12.0) if coast_score > 2.0 else 0.0

            # Level 2: IPCC scenario scaling
            raw = w_cd * coast_score + w_el * elev_score + w_in * infra_score
            if level >= 2:
                # RCP 8.5 implies +0.6m by 2050 — increase risk for very low areas
                raw *= 1.15  # moderate additional risk from projected rise

            rs = min(10.0, max(0.0, raw))

            indicators = {
                "coast_distance": round(coast_score, 2),
                "elevation_estimate": round(elev_score, 2),
                "coastal_infrastructure": round(infra_score, 2),
                "is_coastal": 1.0,
                "risk_score": round(rs, 2),
            }
            results.append(CellResult(grid_cell_id=cell["id"], indicators=indicators, risk_score=rs))

        if progress_callback:
            progress_callback(98.0, "Ergebnisse speichern")

        return results

    def get_projection_factors(self, bundesland: str) -> dict:
        factors: dict[str, dict[int, float]] = {"rcp45": {}, "rcp85": {}}
        if bundesland not in _COASTAL_STATES:
            for y in range(2025, 2066):
                factors["rcp45"][y] = 1.0
                factors["rcp85"][y] = 1.0
            return factors
        for y in range(2025, 2066):
            t = (y - 2025) / 40.0
            factors["rcp45"][y] = 1.0 + 0.30 * t  # +0.3m equiv
            factors["rcp85"][y] = 1.0 + 0.80 * t  # +0.6m equiv
        return factors


_instance = SeaLevelAssessor()
registry.register(_instance)
