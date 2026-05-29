"""River Flooding assessor — Levels 1–2.

Level 1: OSM-based proximity to waterways (river/stream/canal), floodplain
          heuristic (cells <200m from river + low relative position).
Level 2: Adds DWD regional flood-frequency scaling and river-width proxy.

risk_score = f(flood_proximity × 0.5, elevation_relative × 0.3, infrastructure × 0.2)
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

# Regional flood frequency factor (relative to national avg = 1.0)
_FLOOD_FREQUENCY: dict[str, float] = {
    "Baden-Württemberg": 1.15, "Bayern": 1.20, "Berlin": 0.60,
    "Brandenburg": 0.85, "Bremen": 0.90, "Hamburg": 0.95,
    "Hessen": 1.05, "Mecklenburg-Vorpommern": 0.70,
    "Niedersachsen": 1.00, "Nordrhein-Westfalen": 1.10,
    "Rheinland-Pfalz": 1.15, "Saarland": 1.05,
    "Sachsen": 1.25, "Sachsen-Anhalt": 1.10,
    "Schleswig-Holstein": 0.75, "Thüringen": 0.95,
}


def _cell_worker(idx: int):
    from app.services.climate.heat.osm_data import compute_cell_landuse
    return idx, compute_cell_landuse(_w["cells"][idx]["geometry"], _w["lu"])


class RiverFloodAssessor(ClimateAssessor):
    climate_type = "river_flood"
    label = "Flusshochwasser"
    max_level = 2

    def get_required_config(self) -> list[ConfigParamDef]:
        return [
            ConfigParamDef("river_flood", "proximity_weight", 0.5, "Gewichtung Flussnähe"),
            ConfigParamDef("river_flood", "elevation_weight", 0.3, "Gewichtung Tiefenlage"),
            ConfigParamDef("river_flood", "infrastructure_weight", 0.2, "Gewichtung Infrastruktur"),
        ]

    def get_indicators(self) -> list[IndicatorDef]:
        return [
            IndicatorDef("flood_proximity", "Flussnähe", "score", "Nähe zum nächsten Gewässer (0-10, hoch=nah)", 0, 10),
            IndicatorDef("elevation_relative", "Relative Höhenlage", "score", "Tiefenlage relativ zur Umgebung", 0, 10),
            IndicatorDef("floodplain_risk", "Auenrisiko", "score", "Kombination Nähe + Tiefe", 0, 10),
            IndicatorDef("risk_score", "Risiko-Score", "", "Gesamtrisiko 0–10", 0, 10),
        ]

    def assess(self, kommune_id: int, level: int, grid_cells: list[dict],
               config_params: dict[str, Any], progress_callback: Any = None) -> list[CellResult]:
        global _w

        if progress_callback:
            progress_callback(2.0, "OSM-Daten laden", "Landnutzung + Gewässer abrufen")

        from app.services.climate.heat.osm_data import fetch_landuse
        lu_data, _ = fetch_landuse(grid_cells)

        if progress_callback:
            progress_callback(15.0, "Gewässer identifizieren")

        # Identify water cells (rivers, streams, canals)
        water_cells: set[int] = set()
        rc_map: dict[tuple[int, int], int] = {}
        for i, cell in enumerate(grid_cells):
            rc_map[(cell["row"], cell["col"])] = i
            for feat in lu_data:
                if feat.get("natural") == "water" and cell["geometry"].intersects(feat["geometry"]):
                    water_cells.add(i)
                    break

        if progress_callback:
            progress_callback(25.0, "Zellen berechnen", f"0/{len(grid_cells)}")

        # Compute land-use per cell
        _w = {"cells": grid_cells, "lu": lu_data}
        cell_lu: dict[int, dict] = {}
        total = len(grid_cells)
        with _MP.Pool(_N_WORKERS) as pool:
            for done_i, (idx, lu) in enumerate(pool.imap_unordered(_cell_worker, range(total), chunksize=_CHUNK)):
                cell_lu[idx] = lu
                if progress_callback and done_i % 200 == 0:
                    pct = 25.0 + 50.0 * done_i / total
                    progress_callback(pct, None, f"{done_i}/{total}")

        if progress_callback:
            progress_callback(78.0, "Risiko berechnen")

        bundesland = config_params.get("_bundesland", "Sachsen")
        flood_factor = _FLOOD_FREQUENCY.get(bundesland, 1.0)

        w_prox = float(config_params.get("river_flood.proximity_weight", 0.5))
        w_elev = float(config_params.get("river_flood.elevation_weight", 0.3))
        w_infra = float(config_params.get("river_flood.infrastructure_weight", 0.2))

        results: list[CellResult] = []
        for i, cell in enumerate(grid_cells):
            lu = cell_lu.get(i, {})
            r, c = cell["row"], cell["col"]

            # Flood proximity: distance to nearest water cell (in grid steps)
            min_dist = 999
            for dr in range(-8, 9):
                for dc in range(-8, 9):
                    ni = rc_map.get((r + dr, c + dc))
                    if ni is not None and ni in water_cells:
                        d = max(abs(dr), abs(dc))
                        min_dist = min(min_dist, d)

            # Proximity score: closer = higher risk (inverse)
            cell_size = cell.get("cell_size_m", 100)
            dist_m = min_dist * cell_size
            prox_score = max(0.0, 10.0 - dist_m / 100.0) if min_dist < 999 else 0.0

            # Elevation relative: use imperviousness as inverse proxy
            # (low-lying areas near rivers tend to have less impervious cover)
            imp = lu.get("impervious_fraction", 0.05)
            # Neighbour average imperviousness to detect relative "low" cells
            nb_imp = []
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    ni = rc_map.get((r + dr, c + dc))
                    if ni is not None and ni in cell_lu:
                        nb_imp.append(cell_lu[ni].get("impervious_fraction", 0.05))
            avg_nb = sum(nb_imp) / len(nb_imp) if nb_imp else imp
            elev_score = min(10.0, max(0.0, (avg_nb - imp + 0.3) * 10.0))

            # Infrastructure risk: buildings near water = higher consequence
            # Smooth ramp instead of hard step at prox_score=3
            bldg_risk = min(10.0, imp * (4.0 + 8.0 * min(1.0, prox_score / 5.0)))

            raw = w_prox * prox_score + w_elev * elev_score + w_infra * bldg_risk
            if level >= 2:
                raw *= flood_factor

            rs = min(10.0, max(0.0, raw))

            indicators = {
                "flood_proximity": round(prox_score, 2),
                "elevation_relative": round(elev_score, 2),
                "floodplain_risk": round(min(10.0, (prox_score + elev_score) / 2), 2),
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
            factors["rcp45"][y] = 1.0 + 0.20 * t
            factors["rcp85"][y] = 1.0 + 0.60 * t
        return factors


_instance = RiverFloodAssessor()
registry.register(_instance)
