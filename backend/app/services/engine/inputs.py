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
from concurrent.futures import ThreadPoolExecutor, as_completed
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
_nw: dict = {}
_N_WORKERS = min(os.cpu_count() or 4, 8)
_MP = multiprocessing.get_context("fork")
_CHUNK = 50
_NEIGHBOR_OFFSETS = (
    (1, 0), (-1, 0), (0, 1), (0, -1),
    (1, 1), (1, -1), (-1, 1), (-1, -1),
)


def _cell_worker(idx: int):
    from app.services.climate.heat.osm_data import (
        compute_cell_landuse,
        compute_cell_buildings,
        compute_cell_infrastructure,
    )
    g = _w["cells"][idx]["geometry"]
    lu = compute_cell_landuse(g, _w["lu"])
    bm = compute_cell_buildings(g, _w["bldgs"], _w["roads"], _w["trees"])
    infra = compute_cell_infrastructure(g, _w["infra"])
    bm.update(infra)
    return idx, lu, bm


def _snow_elevation_factor(elev_m: float) -> float:
    """Höhenmodulation für Schneedeckentage: Flachland schwach, Hochlagen stark."""
    if elev_m <= 50:
        return 0.2
    return round(min(1.0, 0.2 + 0.8 * min(1.0, (elev_m - 50) / 1500.0)), 4)


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
    from app.services.engine.override_context import uhi_coefficients
    uhi = uhi_coefficients()
    green_cooling = uhi["gamma"] * forest * 1.8 + uhi["gamma"] * meadow + uhi["gamma"] * farmland * 0.5
    water_cooling = uhi["delta"] * water
    tree_cooling = UHI_TREE * canopy * 10.0
    canyon = UHI_EPSILON * (1.0 - svf) * height_factor

    uhi_base = uhi["alpha"] * (1.0 - albedo_lu) * imp + uhi["beta"] * bldg_factor
    delta = uhi_base - green_cooling - water_cooling - tree_cooling + canyon
    return max(0.0, round(delta, 3))


def _assemble_cell_input(
    cell: dict,
    lu: dict,
    bm: dict,
    lu_bm: list,
    coord_idx: dict[tuple[int, int], int],
    terrain: dict,
    water_features: list[dict],
    water_index: tuple[Any, list[Any]] | None,
    infra_features: dict,
    healthcare_indexes: dict[str, tuple[Any, list] | None],
    emergency_index: tuple[Any, list] | None,
    dyke_index: tuple[Any, list] | None,
    step: int,
) -> dict:
    from app.services.climate.heat.osm_data import (
        compute_water_distance_m,
        water_proximity_score,
        compute_cell_healthcare_access,
        compute_cell_emergency_access,
        compute_cell_dyke_proximity,
    )

    open_n = total_n = 0
    water_adj = 0.0
    r, c = cell["row"], cell["col"]
    x_mp = cell.get("x_3035", c * step)
    y_mp = cell.get("y_3035", r * step)
    for ox, oy in _NEIGHBOR_OFFSETS:
        ni = coord_idx.get((x_mp + ox * step, y_mp + oy * step))
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

    water_dist_m = compute_water_distance_m(
        cell["geometry"], water_features, cell_size_m, water_index,
    )
    water_prox = water_proximity_score(water_dist_m)
    water_adj_combined = max(water_adj, water_prox, lu["water_fraction"])

    depression_factor = terrain.get("depression_factor")
    slope_factor = terrain.get("slope_factor")
    if depression_factor is None:
        depression_factor = max(0.0, min(1.0, 0.5 * imp + 0.5 * water_adj_combined - 0.2 * vent_score))
    if slope_factor is None:
        slope_factor = max(0.0, min(1.0, 0.3 + 0.4 * (1.0 - vent_score)))

    hc = compute_cell_healthcare_access(
        cell["geometry"], infra_features, healthcare_indexes,
    )
    emergency_access_score = compute_cell_emergency_access(
        cell["geometry"], infra_features, emergency_index,
    )
    dyke_prox = compute_cell_dyke_proximity(
        cell["geometry"], infra_features, dyke_index,
    )

    return {
        "grid_cell_id": cell["id"],
        "gitter_id": cell.get("gitter_id"),
        "x_3035": x_mp,
        "y_3035": y_mp,
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
        "glacier_frac": lu.get("glacier_fraction", 0.0),
        "snow_elevation_factor": _snow_elevation_factor(terrain.get("mean_elevation_m", 0.0)),
        "farmland_frac": lu.get("farmland_fraction", 0.0),
        "bldg_cov": bm["building_coverage"],
        "bldg_count": bm.get("building_count", 0),
        "energy_infra_count": bm.get("energy_infra_count", 0.0),
        "water_wastewater_count": bm.get("water_wastewater_count", 0),
        "communication_count": bm.get("communication_count", 0),
        "transport_hub_count": bm.get("transport_hub_count", 0),
        "emergency_access_score": emergency_access_score,
        "dyke_prox": dyke_prox,
        "dist_hospital_m": hc["dist_hospital_m"],
        "dist_doctor_m": hc["dist_doctor_m"],
        "dist_pharmacy_m": hc["dist_pharmacy_m"],
        "healthcare_weight_hospital": hc["healthcare_weight_hospital"],
        "healthcare_weight_doctor": hc["healthcare_weight_doctor"],
        "healthcare_weight_pharmacy": hc["healthcare_weight_pharmacy"],
        "healthcare_access_score": hc["healthcare_access_score"],
        "avg_height": bm["avg_building_height"],
        "road_cov": bm["road_coverage"],
        "canopy_frac": bm["tree_canopy_fraction"],
        "svf": bm["sky_view_factor"],
        "vent_score": vent_score,
        "uhi_delta": uhi,
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
    }


def _neighbor_worker(idx: int):
    cell = _nw["cells"][idx]
    lu, bm = _nw["lu_bm"][idx]
    return idx, _assemble_cell_input(
        cell, lu, bm,
        _nw["lu_bm"], _nw["coord_idx"],
        _nw["terrain"].get(idx, {}),
        _nw["water_features"],
        _nw["water_index"],
        _nw["infra_features"],
        _nw["healthcare_indexes"],
        _nw["emergency_index"],
        _nw["dyke_index"],
        _nw["step"],
    )


def _fetch_osm_data_parallel(
    grid_cells: list[dict],
    progress_callback: Any = None,
) -> tuple[list, dict, list, dict]:
    """Lädt Landnutzung, Gebäude, Gewässer und Infrastruktur parallel."""
    from app.services.climate.heat.osm_data import (
        fetch_landuse, fetch_buildings_and_roads, fetch_water_features, fetch_infrastructure,
    )
    from app.services.engine.progress import OSM_LANDUSE, OSM_BUILDINGS, OSM_WATER, OSM_INFRA

    jobs = {
        "landuse": fetch_landuse,
        "buildings": fetch_buildings_and_roads,
        "water": fetch_water_features,
        "infra": fetch_infrastructure,
    }
    results: dict[str, Any] = {}

    with ThreadPoolExecutor(max_workers=4) as ex:
        futures = {ex.submit(fn, grid_cells): name for name, fn in jobs.items()}
        for fut in as_completed(futures):
            name = futures[fut]
            results[name] = fut.result()

    landuse_features, _ = results["landuse"]
    detail = results["buildings"]
    buildings, roads, trees = detail["buildings"], detail["roads"], detail["trees"]
    water_features = results["water"]
    infra_features = results["infra"]

    if progress_callback:
        progress_callback(OSM_LANDUSE[1], "OSM Landnutzung geladen")
        progress_callback(OSM_BUILDINGS[1], "OSM Gebäude, Straßen & Bäume geladen")
        progress_callback(OSM_WATER[1], "OSM Gewässer geladen")
        progress_callback(OSM_INFRA[1], "OSM-Daten geladen")

    return landuse_features, {"buildings": buildings, "roads": roads, "trees": trees}, water_features, infra_features


def build_regional_context(
    bundesland: str | None,
    is_coastal: bool,
    osm_id: str | None = None,
    centroid: tuple[float, float] | None = None,
) -> dict:
    """Regionale Klimawerte, Demografie und kommunale Sozioökonomie (INKAR).

    ``centroid`` = (lon, lat) in WGS84 (Kommune-Zentroid). Ist es gesetzt, werden
    die Treiber ``hot_days``/``frost_days`` (DWD-CDC-Raster) und ``low_flow_days``
    (PEGELONLINE, nächster Pegel) ortsaufgelöst abgegriffen (Report §B2). Fehlt
    der Zentroid oder eine Datenquelle, bleibt der bisherige Bundesland-Proxy
    erhalten (robuster Fallback, wirft nie).
    """
    from app.services.climate.dwd_data import get_regional_climate, get_snow_cover_climate
    from app.services.climate import dwd_cdc_grid, pegelonline, era5_storm
    from app.services.zensus_loader import demographic_shares
    from app.services.inkar_loader import socioeconomic_for_kommune

    bl = bundesland or "Nordrhein-Westfalen"
    regional_clim = get_regional_climate(bl)
    snow_clim = get_snow_cover_climate(bl)
    demo = demographic_shares()
    mean_temp = float(regional_clim["mean_temp_annual"])
    socioeconomic = socioeconomic_for_kommune(osm_id, bundesland)

    lon = lat = None
    if centroid is not None:
        lon, lat = float(centroid[0]), float(centroid[1])

    # hot_days: DWD-CDC-Raster (1 km) am Zentroid, sonst Bundesland-Mittel.
    hot_days = float(regional_clim["hot_days_per_year"])
    if lon is not None:
        real_hot = dwd_cdc_grid.hot_days_at(lon, lat)
        if real_hot is not None:
            hot_days = real_hot

    # frost_days: DWD-CDC-Raster am Zentroid, sonst Proxy aus Jahresmitteltemperatur.
    frost_days = round(max(0.0, 90.0 - mean_temp * 6.0), 1)
    if lon is not None:
        real_frost = dwd_cdc_grid.frost_days_at(lon, lat)
        if real_frost is not None:
            frost_days = real_frost

    # low_flow_days: nächster PEGELONLINE-Pegel (Tage < MNW), sonst Proxy aus hot_days.
    low_flow_days = round(10.0 + hot_days, 1)
    if lon is not None:
        real_lfd = pegelonline.low_flow_days_at(lon, lat)
        if real_lfd is not None:
            low_flow_days = real_lfd

    # storm_days: ERA5-Sturmtage-Raster am Zentroid (falls vom Betreiber erzeugt),
    # sonst regionaler Konstantwert (dokumentierter Fallback).
    storm_days = 6.0
    real_storm = era5_storm.storm_days_at(lon, lat) if lon is not None else None
    if real_storm is not None:
        storm_days = real_storm

    # Provenienz je Treiber protokollieren: echte Quelle vs. dokumentierter Proxy.
    provenance: dict[str, str] = {
        "hot_days": "dwd_cdc_raster" if (lon is not None and real_hot is not None) else "regional_constant",
        "frost_days": "dwd_cdc_raster" if (lon is not None and real_frost is not None) else "proxy_mean_temp",
        "low_flow_days": "pegelonline" if (lon is not None and real_lfd is not None) else "proxy_hot_days",
        "storm_days": "era5" if real_storm is not None else "regional_constant",
    }

    # heavy_rain_index (0–100): ECHTE Starkregen-Häufigkeit aus DWD-CDC-Rastern
    # (Tage/Jahr ≥ 20 mm und ≥ 30 mm) statt des früheren Mitteltemperatur-Proxys
    # (MODELL_KRITIK: heavy_rain aus mean_temp abgeleitet war fachlich unhaltbar).
    # Kalibrierung: DE-typisch ~8 Tage ≥20 mm + ~2 Tage ≥30 mm → Index ≈ 44 (nahe
    # dem bisherigen Baseline 40). Fallback: bisheriger Proxy.
    heavy_rain_index = round(40.0 + (mean_temp - 9.5) * 4.0, 1)
    provenance["heavy_rain_index"] = "proxy_mean_temp"
    if lon is not None:
        p20 = dwd_cdc_grid.precip_days_ge20_at(lon, lat)
        p30 = dwd_cdc_grid.precip_days_ge30_at(lon, lat)
        if p20 is not None:
            idx = p20 * 4.0 + (p30 * 6.0 if p30 is not None else p20 * 1.0)
            heavy_rain_index = round(min(100.0, idx), 1)
            provenance["heavy_rain_index"] = (
                "dwd_cdc_raster" if p30 is not None else "dwd_cdc_raster_ge20_only"
            )

    return {
        "bundesland": bundesland,
        "socioeconomic": socioeconomic,
        "hot_days": hot_days,
        "summer_temp": float(regional_clim["summer_max_temp_avg"]),
        "mean_temp": mean_temp,
        "tropical_nights": float(regional_clim["tropical_nights_per_year"]),
        "is_coastal": is_coastal,
        "drought_days": round(8.0 + hot_days * 1.2, 1),
        "dry_index": round(min(1.0, hot_days / 25.0), 3),
        "frost_days": frost_days,
        "storm_days": storm_days,
        "heavy_rain_index": heavy_rain_index,
        "mean_temp_rise": round(1.6 + (mean_temp - 9.5) * 0.1, 2),
        "soil_moisture_decline": round(20.0 + hot_days, 1),
        "low_flow_days": low_flow_days,
        "surface_water_heating": round(1.5 + (mean_temp - 9.5) * 0.2, 2),
        "sea_level_rise": 4.5 if is_coastal else 0.0,
        "glacier_loss_rate": 0.5,
        "snow_days": float(snow_clim["snow_days_per_year"]),
        "snow_decline_rate_pct": float(snow_clim["snow_decline_rate_pct"]),
        "demographics": demo,
        "provenance": provenance,
    }


def gather_cell_inputs(
    grid_cells: list[dict],
    bundesland: str | None,
    kommune_population: int | None,
    area_km2: float | None,
    is_coastal: bool,
    progress_callback: Any = None,
    osm_id: str | None = None,
    centroid: tuple[float, float] | None = None,
) -> tuple[list[dict], dict]:
    """Berechnet pro Zelle alle Rohgrößen. Gibt (cell_inputs, regional) zurück.

    ``cell_inputs`` ist an die Reihenfolge von ``grid_cells`` gekoppelt.
    ``centroid`` = (lon, lat) des Kommune-Zentroids für ortsaufgelöste Treiber.
    """
    from app.services.climate.heat.osm_data import (
        build_water_spatial_index,
        build_healthcare_indexes,
        build_emergency_spatial_index,
        build_dyke_spatial_index,
    )
    from app.services.terrain_service import compute_terrain_for_cells
    from app.services.zensus_loader import ensure_zensus_datasets, load_zensus_for_cells, apply_zensus_to_cell_inputs
    from app.services.engine.progress import (
        ZENSUS, OSM_LANDUSE, CELL_SURFACE, CELL_NEIGHBORS, ZENSUS_APPLY, lerp,
    )

    regional = build_regional_context(bundesland, is_coastal, osm_id, centroid)

    if progress_callback:
        progress_callback(ZENSUS[0], "Zensus-Daten prüfen/laden")
    ensure_zensus_datasets()
    if progress_callback:
        progress_callback(ZENSUS[1], "Zensus-Daten prüfen/laden")

    if progress_callback:
        progress_callback(OSM_LANDUSE[0], "Lade OSM-Daten parallel (4 Abfragen)")

    landuse_features, bldg_detail, water_features, infra_features = _fetch_osm_data_parallel(
        grid_cells, progress_callback,
    )
    buildings, roads, trees = bldg_detail["buildings"], bldg_detail["roads"], bldg_detail["trees"]

    total = len(grid_cells)
    lu_bm: list[tuple | None] = [None] * total

    terrain_by_idx = compute_terrain_for_cells(grid_cells, progress_callback)

    if progress_callback:
        progress_callback(CELL_SURFACE[0], f"Analyse Oberflächen ({_N_WORKERS} Kerne) für {total} Zellen")

    _w["lu"] = landuse_features
    _w["bldgs"] = buildings
    _w["roads"] = roads
    _w["trees"] = trees
    _w["infra"] = infra_features
    _w["cells"] = grid_cells
    try:
        with _MP.Pool(_N_WORKERS) as pool:
            for done, (idx, lu, bm) in enumerate(
                pool.imap_unordered(_cell_worker, range(total), chunksize=_CHUNK)
            ):
                lu_bm[idx] = (lu, bm)
                if progress_callback and (done % 100 == 0 or done + 1 == total):
                    pct = lerp(CELL_SURFACE[0], CELL_SURFACE[1], (done + 1) / total)
                    progress_callback(pct, "Zellanalyse", f"{done + 1}/{total}")
    finally:
        _w.clear()

    # Nachbarschaftsindex (Zensus-Gitter: ±100 m in EPSG:3035)
    if progress_callback:
        progress_callback(
            CELL_NEIGHBORS[0],
            f"Nachbarschaft & Zell-Eingaben ({_N_WORKERS} Kerne) für {total} Zellen",
        )

    coord_idx: dict[tuple[int, int], int] = {}
    step = 100
    for idx, cell in enumerate(grid_cells):
        x = cell.get("x_3035", cell.get("col", 0) * step)
        y = cell.get("y_3035", cell.get("row", 0) * step)
        coord_idx[(x, y)] = idx

    water_index = build_water_spatial_index(water_features)
    healthcare_indexes = build_healthcare_indexes(infra_features)
    emergency_index = build_emergency_spatial_index(infra_features)
    dyke_index = build_dyke_spatial_index(infra_features)
    cell_inputs: list[dict | None] = [None] * total

    _nw["cells"] = grid_cells
    _nw["lu_bm"] = lu_bm
    _nw["coord_idx"] = coord_idx
    _nw["terrain"] = terrain_by_idx
    _nw["water_index"] = water_index
    _nw["water_features"] = water_features
    _nw["infra_features"] = infra_features
    _nw["healthcare_indexes"] = healthcare_indexes
    _nw["emergency_index"] = emergency_index
    _nw["dyke_index"] = dyke_index
    _nw["step"] = step
    try:
        with _MP.Pool(_N_WORKERS) as pool:
            for done, (idx, ci) in enumerate(
                pool.imap_unordered(_neighbor_worker, range(total), chunksize=_CHUNK)
            ):
                cell_inputs[idx] = ci
                if progress_callback and (done % 200 == 0 or done + 1 == total):
                    pct = lerp(CELL_NEIGHBORS[0], CELL_NEIGHBORS[1], (done + 1) / total)
                    progress_callback(pct, "Nachbarschaft & Zell-Eingaben", f"{done + 1}/{total}")
    finally:
        _nw.clear()

    if progress_callback:
        progress_callback(ZENSUS_APPLY[0], "Zensus-Daten anwenden")
    zensus = load_zensus_for_cells(grid_cells)
    apply_zensus_to_cell_inputs(list(cell_inputs), grid_cells, zensus)
    if progress_callback:
        progress_callback(ZENSUS_APPLY[1], "Zensus-Daten anwenden")

    return list(cell_inputs), regional
