"""Gemeinsamer Eingabepass: berechnet pro 100m-Zelle alle Rohgrößen, die die
H/E/V-Calculatoren benötigen (OSM-Landnutzung, Gebäude/Straßen/Bäume, UHI-ΔT,
Belüftung, Bevölkerung, Gelände/DEM, Gewässernähe, regionale DWD-Werte).

Reuse: ``app.services.climate.heat.osm_data`` für die OSM-Extraktion und die
UHI-Formel aus dem Hitze-Assessor.
"""

from __future__ import annotations

import logging
import multiprocessing
import os
from typing import Any

log = logging.getLogger(__name__)

# UHI-Standardkoeffizienten (identisch zum Hitze-Assessor)
UHI_ALPHA = 6.0
UHI_BETA = 2.0
UHI_GAMMA = 3.5
UHI_DELTA = 2.0
UHI_EPSILON = 1.5
UHI_TREE = 0.3

_w: dict = {}
_N_WORKERS = min(os.cpu_count() or 4, 8)
_MP = multiprocessing.get_context("fork")
_CHUNK = 50


def _cell_worker(idx: int):
    from app.services.climate.heat.osm_data import compute_cell_landuse, compute_cell_buildings
    g = _w["cells"][idx]["geometry"]
    lu = compute_cell_landuse(g, _w["lu"])
    bm = compute_cell_buildings(g, _w["bldgs"], _w["roads"], _w["trees"])
    return idx, lu, bm


def compute_uhi_delta(lu: dict, bm: dict) -> float:
    """Tag-UHI ΔT (K) nach der KAP2/KAP3-Formel (siehe Handbuch)."""
    imp_lu = lu["impervious_fraction"]
    albedo_lu = lu["albedo"]
    green = lu["green_fraction"]
    water = lu["water_fraction"]
    forest = lu.get("forest_fraction", 0.0)
    farmland = lu.get("farmland_fraction", 0.0)

    bldg_cov = bm["building_coverage"]
    avg_h = bm["avg_building_height"]
    road_cov = bm["road_coverage"]
    canopy = bm["tree_canopy_fraction"]
    svf = bm["sky_view_factor"]

    imp_detail = bldg_cov + road_cov * 0.95
    imp = min(imp_detail, 0.98) if imp_detail > 0.01 else imp_lu
    imp = max(0.02, min(imp, 0.98))

    height_factor = min(avg_h / 15.0, 2.0)
    bldg_factor = bldg_cov * height_factor

    meadow = max(0.0, green - forest)
    green_cooling = UHI_GAMMA * forest * 1.8 + UHI_GAMMA * meadow + UHI_GAMMA * farmland * 0.5
    water_cooling = UHI_DELTA * water
    tree_cooling = UHI_TREE * canopy * 10.0
    canyon = UHI_EPSILON * (1.0 - svf) * height_factor

    uhi_base = UHI_ALPHA * (1.0 - albedo_lu) * imp + UHI_BETA * bldg_factor
    delta = uhi_base - green_cooling - water_cooling - tree_cooling + canyon
    return max(0.0, round(delta, 3))


def gather_cell_inputs(
    grid_cells: list[dict],
    bundesland: str | None,
    kommune_population: int | None,
    area_km2: float | None,
    is_coastal: bool,
    progress_callback: Any = None,
) -> tuple[list[dict], dict]:
    """Berechnet pro Zelle alle Rohgrößen. Gibt (cell_inputs, regional) zurück.

    ``cell_inputs`` ist an die Reihenfolge von ``grid_cells`` gekoppelt.
    """
    from app.services.climate.heat.osm_data import (
        fetch_landuse, fetch_buildings_and_roads, fetch_water_features,
        compute_water_distance_m, water_proximity_score,
    )
    from app.services.climate.dwd_data import get_regional_climate
    from app.services.terrain_service import compute_terrain_for_cells
    from app.services.zensus_service import distribute_population, demographic_shares

    regional_clim = get_regional_climate(bundesland or "Nordrhein-Westfalen")
    demo = demographic_shares()

    # Regionale Treiber-Werte (Konstanten / nicht räumlich aufgelöst)
    hot_days = float(regional_clim["hot_days_per_year"])
    mean_temp = float(regional_clim["mean_temp_annual"])
    # einfache Ableitungen für regionale Hazards
    regional = {
        "bundesland": bundesland,
        "hot_days": hot_days,
        "summer_temp": float(regional_clim["summer_max_temp_avg"]),
        "mean_temp": mean_temp,
        "tropical_nights": float(regional_clim["tropical_nights_per_year"]),
        "is_coastal": is_coastal,
        # dürre/trockenheit grob aus Hitze-Niveau
        "drought_days": round(8.0 + hot_days * 1.2, 1),
        "dry_index": round(min(1.0, hot_days / 25.0), 3),
        "frost_days": round(max(0.0, 90.0 - mean_temp * 6.0), 1),
        "storm_days": 6.0,
        "heavy_rain_index": round(40.0 + (mean_temp - 9.5) * 4.0, 1),
        "mean_temp_rise": round(1.6 + (mean_temp - 9.5) * 0.1, 2),
        "soil_moisture_decline": round(20.0 + hot_days, 1),
        "low_flow_days": round(10.0 + hot_days, 1),
        "surface_water_heating": round(1.5 + (mean_temp - 9.5) * 0.2, 2),
        "sea_level_rise": 4.5 if is_coastal else 0.0,
        "demographics": demo,
    }

    if progress_callback:
        progress_callback(2.0, "Herunterladen OSM-Landnutzung")
    landuse_features, _ = fetch_landuse(grid_cells)
    if progress_callback:
        progress_callback(8.0, "Herunterladen OSM-Gebäude, Straßen & Bäume")
    detail = fetch_buildings_and_roads(grid_cells)
    buildings, roads, trees = detail["buildings"], detail["roads"], detail["trees"]

    total = len(grid_cells)
    lu_bm: list[tuple | None] = [None] * total

    if progress_callback:
        progress_callback(10.0, "Lade OSM-Gewässer")
    water_features = fetch_water_features(grid_cells)

    terrain_by_idx = compute_terrain_for_cells(grid_cells, progress_callback)

    if progress_callback:
        progress_callback(15.0, f"Analyse Oberflächen ({_N_WORKERS} Kerne) für {total} Zellen")

    _w["lu"] = landuse_features
    _w["bldgs"] = buildings
    _w["roads"] = roads
    _w["trees"] = trees
    _w["cells"] = grid_cells
    try:
        with _MP.Pool(_N_WORKERS) as pool:
            for done, (idx, lu, bm) in enumerate(
                pool.imap_unordered(_cell_worker, range(total), chunksize=_CHUNK)
            ):
                lu_bm[idx] = (lu, bm)
                if progress_callback and done % 200 == 0:
                    pct = 15.0 + (done + 1) / total * 35.0
                    progress_callback(pct, "Zellanalyse", f"{done + 1}/{total}")
    finally:
        _w.clear()

    # Belüftungsindex (Nachbarschaft)
    row_col: dict[tuple[int, int], int] = {}
    for idx, cell in enumerate(grid_cells):
        row_col[(cell["row"], cell["col"])] = idx

    cell_inputs: list[dict] = []
    for idx, cell in enumerate(grid_cells):
        lu, bm = lu_bm[idx]
        # Belüftung + Wassernähe aus Nachbarn
        open_n = total_n = 0
        water_adj = 0.0
        r, c = cell["row"], cell["col"]
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                ni = row_col.get((r + dr, c + dc))
                if ni is None:
                    open_n += 1
                    total_n += 1
                    continue
                total_n += 1
                nlu, nbm = lu_bm[ni]
                if (nbm["building_coverage"] < 0.05
                        and nlu["green_fraction"] + nlu["water_fraction"]
                        + nlu.get("farmland_fraction", 0.0) > 0.3):
                    open_n += 1
                water_adj = max(water_adj, nlu["water_fraction"])
        vent_score = open_n / max(total_n, 1)

        uhi = compute_uhi_delta(lu, bm)
        imp_detail = bm["building_coverage"] + bm["road_coverage"] * 0.95
        imp = max(0.02, min(imp_detail if imp_detail > 0.01 else lu["impervious_fraction"], 0.98))

        cell_size_m = cell.get("cell_size_m", 100)
        area_m2 = float(cell_size_m) ** 2

        terrain = terrain_by_idx.get(idx, {})
        water_dist_m = compute_water_distance_m(cell["geometry"], water_features, cell_size_m)
        water_prox = water_proximity_score(water_dist_m)
        # Kombiniert OSM-Flächenanteil, Nachbar-Wasser und Distanz zu Fließgewässern
        water_adj_combined = max(water_adj, water_prox, lu["water_fraction"])

        depression_factor = terrain.get("depression_factor")
        slope_factor = terrain.get("slope_factor")
        if depression_factor is None:
            depression_factor = max(0.0, min(1.0, 0.5 * imp + 0.5 * water_adj_combined - 0.2 * vent_score))
        if slope_factor is None:
            slope_factor = max(0.0, min(1.0, 0.3 + 0.4 * (1.0 - vent_score)))

        cell_inputs.append({
            "grid_cell_id": cell["id"],
            "row": r, "col": c,
            "area_m2": area_m2,
            "imp_frac": imp,
            "albedo": lu["albedo"],
            "green_frac": lu["green_fraction"],
            "water_frac": max(lu["water_fraction"], water_adj * 0.5, water_prox * 0.3),
            "water_adj": round(water_adj_combined, 3),
            "water_dist_m": round(water_dist_m, 1),
            "water_prox": round(water_prox, 3),
            "forest_frac": lu.get("forest_fraction", 0.0),
            "farmland_frac": lu.get("farmland_fraction", 0.0),
            "bldg_cov": bm["building_coverage"],
            "bldg_count": bm.get("building_count", 0),
            "avg_height": bm["avg_building_height"],
            "road_cov": bm["road_coverage"],
            "canopy_frac": bm["tree_canopy_fraction"],
            "svf": bm["sky_view_factor"],
            "vent_score": vent_score,
            "uhi_delta": uhi,
            # Gelände aus Terrarium-DEM (TWI + Senkentiefe / Hangneigung)
            "mean_elevation_m": terrain.get("mean_elevation_m", 0.0),
            "slope_deg": terrain.get("slope_deg", 0.0),
            "sink_depth_m": terrain.get("sink_depth_m", 0.0),
            "twi": terrain.get("twi", 0.0),
            "twi_norm": terrain.get("twi_norm", 0.0),
            "flow_accum": terrain.get("flow_accum", 1.0),
            "depression_proxy": depression_factor,
            "slope_proxy": slope_factor,
            "depression_factor": depression_factor,
            "slope_factor": slope_factor,
            "pop": 0.0,
        })

    # Bevölkerung verteilen (Zensus / Proxy)
    distribute_population(cell_inputs, kommune_population, area_km2)

    return cell_inputs, regional
