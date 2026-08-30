"""Gemeinsamer Eingabepass: berechnet pro 100m-Zelle alle Rohgrößen, die die
H/E/V-Calculatoren benötigen (OSM-Landnutzung, Gebäude/Straßen/Bäume, UHI-ΔT,
Belüftung, Bevölkerung, Gelände/DEM, Gewässernähe, regionale DWD-Werte).

Reuse: ``app.services.climate.heat.osm_data`` für die OSM-Extraktion und die
UHI-Formel aus dem Hitze-Assessor.
"""

from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from app.services.engine import tunables
from app.services.engine.parallel import cow_pool, n_workers

log = logging.getLogger(__name__)

# UHI-Koeffizienten: sämtlich override-fähig über override_context.uhi_coefficients()
# (Registry-IDs uhi.alpha…delta, uhi.epsilon, uhi.tree_cooling) — keine Modul-Literale.

_w: dict = {}
_nw: dict = {}
_CHUNK = 50
_NEIGHBOR_OFFSETS = (
    (1, 0), (-1, 0), (0, 1), (0, -1),
    (1, 1), (1, -1), (-1, 1), (-1, -1),
)


# Straßen werden in compute_cell_buildings um ihre halbe Breite gepuffert.
# Für die STRtree-Vorfilterung fragen wir die Zelle daher mit einem kleinen
# Sicherheitsrand (≈15 m in Grad) ab, damit knapp außerhalb liegende Straßen,
# die erst nach dem Puffern in die Zelle ragen, nicht verloren gehen.
_ROAD_QUERY_MARGIN_DEG = 15.0 / 111_320.0


def _build_geom_tree(geoms: list):
    """STRtree über eine Geometrie-Liste; ``None`` bei leerer Liste."""
    if not geoms:
        return None
    from shapely.strtree import STRtree
    return STRtree(geoms)


def _query_subset(tree, items: list, cell_geom, margin: float = 0.0) -> list:
    """Kandidaten (Bounding-Box-Überlappung mit der Zelle) via STRtree.

    Fällt auf die volle Liste zurück, falls kein Index vorhanden ist. Der
    ``intersects``/``contains``-Test in den compute_cell_*-Funktionen bleibt
    erhalten, d. h. die Vorfilterung ist eine reine Obermenge → identisches
    Ergebnis, nur ohne den O(Zellen×Features)-Volldurchlauf.
    """
    if tree is None:
        return items
    query_geom = cell_geom.buffer(margin) if margin else cell_geom
    return [items[i] for i in tree.query(query_geom)]


def _cell_worker(idx: int):
    from app.services.climate.heat.osm_data import (
        compute_cell_composition,
        compute_cell_buildings,
        compute_cell_infrastructure,
    )
    g = _w["cells"][idx]["geometry"]
    bldgs = _query_subset(_w["bldg_tree"], _w["bldgs"], g)
    roads = _query_subset(_w["road_tree"], _w["roads"], g, _ROAD_QUERY_MARGIN_DEG)
    paved = _query_subset(_w["paved_tree"], _w["paved"], g)
    # Flächenkomposition (Schichtmodell, 100%-Budget): Gebäude → Verkehr/Plätze →
    # Wasser → spezifische → großflächige Landnutzung → Fallback.
    lu = compute_cell_composition(
        g, bldgs, roads, paved, _query_subset(_w["lu_tree"], _w["lu"], g),
    )
    bm = compute_cell_buildings(
        g, bldgs, roads, _query_subset(_w["tree_tree"], _w["trees"], g),
    )
    infra = compute_cell_infrastructure(g, _w["infra"])
    bm.update(infra)
    return idx, lu, bm


# Klimatologischer Abstand sommerliches Tagesmaximum → Tagesmittel (K).
# Nur Rückfall, wenn das DWD-Monatsraster am Zentroid nicht auswertbar ist.
SUMMER_MAX_TO_MEAN_OFFSET_K = 6.3


def _snow_elevation_factor(elev_m: float) -> float:
    """Höhenmodulation für Schneedeckentage: Flachland schwach, Hochlagen stark."""
    if elev_m <= 50:
        return 0.2
    return round(min(1.0, 0.2 + 0.8 * min(1.0, (elev_m - 50) / 1500.0)), 4)


def _clamp_impervious(imp: float) -> float:
    """Versiegelungsgrad auf den physikalisch sinnvollen Bereich [0,02; 0,98] klemmen."""
    return max(0.02, min(float(imp), 0.98))


def compute_uhi_components(
    lu: dict, bm: dict, vent_score: float = 0.0, water_prox: float | None = None,
) -> dict[str, float]:
    """Wärmeinsel-ΔT als Tages-, Nacht- und Tagesmittelwert (K).

    ``day`` ist unverändert die bisherige KAP2/KAP3-Formel (Tagesmaximum) — sie
    speist weiterhin HEAT_WAVE, UHI_INTENSITY und HEAT_SENSITIVITY.

    ``night`` bildet die nächtliche Überwärmung ab: Straßenschluchten halten
    langwellige Ausstrahlung zurück (1 − SVF) und die Gebäudemasse gibt
    tagsüber gespeicherte Wärme ab. Gewässer in der Nähe dämpfen das.

    ``mean`` ist der 24-h-Mittelwert, den die Expositions-Wirkungs-Rechnung
    braucht: Die RKI-/Winklmayr-Kurven laufen über die **Wochenmitteltemperatur**
    (Tag und Nacht), nicht über das Tagesmaximum. Zusätzlich dämpft der
    Luftaustausch mit dem Umland (``vent_score``) die Wärmeinsel — bis hierher
    floss die Durchlüftung überhaupt nicht in den Hitzepfad ein.
    """
    from app.services.engine.override_context import uhi_coefficients
    uhi = uhi_coefficients()

    day = compute_uhi_delta(lu, bm)

    bldg_cov = bm["building_coverage"]
    height_factor = min(bm["avg_building_height"] / 15.0, 2.0)
    svf = bm["sky_view_factor"]
    # Gewässernähe wirkt über die Zellgrenze hinaus (Verdunstung/Wärmekapazität);
    # daher water_prox statt nur des Wasseranteils der Zelle selbst.
    wp = float(lu.get("water_fraction", 0.0) if water_prox is None else water_prox)

    night = (
        uhi["epsilon"] * (1.0 - svf) * height_factor
        + uhi["zeta"] * bldg_cov * height_factor
        - uhi["delta_night"] * wp
    )
    night = max(0.0, night)

    w_night = uhi["night_weight"]
    combined = (1.0 - w_night) * day + w_night * night
    damping = max(0.0, 1.0 - uhi["vent_ratio"] * max(0.0, min(1.0, vent_score)))
    mean = max(0.0, combined * uhi["mean_factor"] * damping)

    return {"day": round(day, 3), "night": round(night, 3), "mean": round(mean, 3)}


def compute_uhi_delta(lu: dict, bm: dict) -> float:
    """Tag-UHI ΔT (K) nach der KAP2/KAP3-Formel (siehe Handbuch)."""
    albedo_lu = lu["albedo"]
    green = lu["green_fraction"]
    water = lu["water_fraction"]
    forest = lu.get("forest_fraction", 0.0)
    farmland = lu.get("farmland_fraction", 0.0)

    bldg_cov = bm["building_coverage"]
    avg_h = bm["avg_building_height"]
    canopy = bm["tree_canopy_fraction"]
    svf = bm["sky_view_factor"]

    # Versiegelungsgrad kommt aus der Flächenkomposition (Schichtmodell); die
    # frühere ad-hoc-Ableitung aus Gebäude-/Straßendeckung entfällt.
    imp = _clamp_impervious(lu["impervious_fraction"])

    height_factor = min(avg_h / 15.0, 2.0)
    bldg_factor = bldg_cov * height_factor

    meadow = max(0.0, green - forest)
    from app.services.engine.override_context import uhi_coefficients
    uhi = uhi_coefficients()
    green_cooling = uhi["gamma"] * forest * 1.8 + uhi["gamma"] * meadow + uhi["gamma"] * farmland * 0.5
    water_cooling = uhi["delta"] * water
    tree_cooling = uhi["tree_cooling"] * canopy * 10.0
    canyon = uhi["epsilon"] * (1.0 - svf) * height_factor

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
    ditch_features: list[dict],
    ditch_index: tuple[Any, list[Any]] | None,
    infra_features: dict,
    healthcare_indexes: dict[str, tuple[Any, list] | None],
    emergency_index: tuple[Any, list] | None,
    dyke_index: tuple[Any, list] | None,
    step: int,
) -> dict:
    from app.services.climate.heat.osm_data import (
        compute_water_distance_m,
        water_proximity_score,
        compute_ditch_density_score,
        describe_cell_water_sources,
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
    # Versiegelungsgrad direkt aus der Flächenkomposition (Schichtmodell).
    imp = _clamp_impervious(lu["impervious_fraction"])

    cell_size_m = cell.get("cell_size_m", 100)
    area_m2 = float(cell_size_m) ** 2

    # Distanz/Nähe nur gegen echte Gewässer; Kleinstgräben liefern einen sehr
    # schwachen, über die Grabendichte der Zelle skalierten Zusatzbeitrag.
    water_dist_m = compute_water_distance_m(
        cell["geometry"], water_features, cell_size_m, water_index,
    )
    water_prox_real = water_proximity_score(water_dist_m)
    ditch_score = compute_ditch_density_score(
        cell["geometry"], ditch_features, cell_size_m, ditch_index,
    )
    water_prox = max(water_prox_real, ditch_score)
    water_adj_combined = max(water_adj, water_prox, lu["water_fraction"])

    # Wärmeinsel-Komponenten: ``uhi`` (Tagesmaximum) bleibt der bisherige Treiber
    # von HEAT_WAVE/UHI_INTENSITY; ``uhi_mean`` ist der 24-h-Mittelwert für die
    # Expositions-Wirkungs-Rechnung und berücksichtigt Durchlüftung + Gewässernähe.
    uhi_parts = compute_uhi_components(lu, bm, vent_score, water_prox)

    # Debug/Inspektor: welche konkreten OSM-Objekte begründen die Wasserannahme?
    water_src = (
        describe_cell_water_sources(
            cell["geometry"], water_features, cell_size_m, water_index)
        + describe_cell_water_sources(
            cell["geometry"], ditch_features, cell_size_m, ditch_index)
    )

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
        "water_src": water_src,
        "forest_frac": lu.get("forest_fraction", 0.0),
        "glacier_frac": lu.get("glacier_fraction", 0.0),
        "snow_elevation_factor": _snow_elevation_factor(terrain.get("mean_elevation_m", 0.0)),
        "farmland_frac": lu.get("farmland_fraction", 0.0),
        "bldg_cov": bm["building_coverage"],
        "bldg_count": bm.get("building_count", 0),
        "energy_infra_count": bm.get("energy_infra_count", 0.0),
        "water_wastewater_count": bm.get("water_wastewater_count", 0.0),
        "communication_count": bm.get("communication_count", 0.0),
        "transport_hub_count": bm.get("transport_hub_count", 0.0),
        # Rohe Klassen-Zählungen (Anlagenklasse → Anzahl) für den monetären
        # Pfad mit klassenspezifischen Ersatzwerten (impact/monetary.py).
        "energy_infra_classes": bm.get("energy_infra_classes", {}),
        "water_wastewater_classes": bm.get("water_wastewater_classes", {}),
        "communication_classes": bm.get("communication_classes", {}),
        "transport_hub_classes": bm.get("transport_hub_classes", {}),
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
        "uhi_delta_night": uhi_parts["night"],
        "uhi_delta_mean": uhi_parts["mean"],
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
        _nw["ditch_features"],
        _nw["ditch_index"],
        _nw["infra_features"],
        _nw["healthcare_indexes"],
        _nw["emergency_index"],
        _nw["dyke_index"],
        _nw["step"],
    )


def _fetch_osm_data_parallel(
    grid_cells: list[dict],
    progress_callback: Any = None,
    bundesland: str | None = None,
) -> tuple[list, dict, list, dict]:
    """Lädt Landnutzung, Gebäude, Gewässer und Infrastruktur parallel.

    ``bundesland`` steuert die LoD2-Quelle für Gebäudehöhen (amtliche
    3D-Modelle ersetzen die OSM-Höhenheuristik, wo angebunden).
    """
    from app.services.climate.heat.osm_data import (
        fetch_landuse, fetch_buildings_and_roads, fetch_water_features, fetch_infrastructure,
    )
    from app.services.engine.progress import OSM_LANDUSE, OSM_BUILDINGS, OSM_WATER, OSM_INFRA

    jobs = {
        "landuse": fetch_landuse,
        "buildings": lambda cells: fetch_buildings_and_roads(cells, bundesland),
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
    paved_areas = detail.get("paved_areas", [])
    water_features = results["water"]
    infra_features = results["infra"]

    if progress_callback:
        progress_callback(OSM_LANDUSE[1], "OSM Landnutzung geladen")
        progress_callback(OSM_BUILDINGS[1], "OSM Gebäude, Straßen & Bäume geladen")
        progress_callback(OSM_WATER[1], "OSM Gewässer geladen")
        progress_callback(OSM_INFRA[1], "OSM-Daten geladen")

    return (
        landuse_features,
        {"buildings": buildings, "roads": roads, "paved_areas": paved_areas,
         "trees": trees,
         "building_source": detail.get("building_source", "osm")},
        water_features,
        infra_features,
    )


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

    # Sommermitteltemperatur (Jun–Aug) am Zentroid — Bezugsgröße der Expositions-
    # Wirkungs-Kurven (Wochenmitteltemperatur). Rückfall: aus dem Bundesland-Mittel
    # der sommerlichen Tagesmaxima, vermindert um den klimatologischen Abstand
    # Tagesmaximum→Tagesmittel (DWD-Gebietsmittel: ~25 °C Maxima vs. ~18,5 °C Mittel).
    summer_temp_mean = round(
        float(regional_clim["summer_max_temp_avg"]) - SUMMER_MAX_TO_MEAN_OFFSET_K, 2)
    if lon is not None:
        real_smt = dwd_cdc_grid.summer_mean_temp_at(lon, lat)
        if real_smt is not None:
            summer_temp_mean = real_smt

    # low_flow_days: nächster PEGELONLINE-Pegel (Tage < MNW), sonst Proxy aus hot_days.
    low_flow_days = round(10.0 + hot_days, 1)
    if lon is not None:
        real_lfd = pegelonline.low_flow_days_at(lon, lat)
        if real_lfd is not None:
            low_flow_days = real_lfd

    # storm_days: ERA5-Sturmtage-Raster am Zentroid (falls vom Betreiber erzeugt),
    # sonst regionaler Konstantwert (dokumentierter, editierbarer Fallback).
    storm_days = tunables.regional_fallback("storm_days", 6.0)
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
    heavy_rain_index = round(
        tunables.regional_fallback("heavy_rain_base", 40.0)
        + (mean_temp - 9.5) * tunables.regional_fallback("heavy_rain_slope", 4.0), 1)
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
        "summer_temp_mean": summer_temp_mean,
        "mean_temp": mean_temp,
        "tropical_nights": float(regional_clim["tropical_nights_per_year"]),
        "is_coastal": is_coastal,
        "drought_days": round(
            tunables.regional_fallback("drought_base", 8.0)
            + hot_days * tunables.regional_fallback("drought_factor", 1.2), 1),
        "dry_index": round(
            min(1.0, hot_days / max(1.0, tunables.regional_fallback("dry_index_divisor", 25.0))), 3),
        "frost_days": frost_days,
        "storm_days": storm_days,
        "heavy_rain_index": heavy_rain_index,
        "mean_temp_rise": round(
            tunables.regional_fallback("mean_temp_rise_base", 1.6) + (mean_temp - 9.5) * 0.1, 2),
        "soil_moisture_decline": round(20.0 + hot_days, 1),
        "low_flow_days": low_flow_days,
        "surface_water_heating": round(1.5 + (mean_temp - 9.5) * 0.2, 2),
        "sea_level_rise": tunables.regional_fallback("sea_level_rise", 4.5) if is_coastal else 0.0,
        "glacier_loss_rate": tunables.regional_fallback("glacier_loss_rate", 0.5),
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
        grid_cells, progress_callback, bundesland,
    )
    buildings, roads, trees = bldg_detail["buildings"], bldg_detail["roads"], bldg_detail["trees"]
    paved_areas = bldg_detail.get("paved_areas", [])
    building_source = bldg_detail.get("building_source", "osm")

    # Provenienz: amtliche LoD2-Höhen vs. OSM-Heuristik (height/levels·3m/6m)
    regional["provenance"]["building_height"] = (
        f"lod2:{bundesland}" if building_source == "lod2" else "osm_heuristic"
    )
    regional["provenance"]["svf"] = f"horizon_raster_{building_source}"
    log.info("Gebäudehöhen-Quelle: %s (%d Gebäude)",
             regional["provenance"]["building_height"], len(buildings))

    total = len(grid_cells)
    lu_bm: list[tuple | None] = [None] * total

    terrain_by_idx = compute_terrain_for_cells(grid_cells, progress_callback)

    if progress_callback:
        progress_callback(CELL_SURFACE[0], f"Analyse Oberflächen ({n_workers()} Kerne) für {total} Zellen")

    # STRtree-Indizes einmalig im Elternprozess aufbauen; per fork werden sie
    # copy-on-write an die Worker vererbt (read-only Zugriff). Bäume sind
    # Punkt-Features (lon/lat) → als Points indizieren, passend zum
    # contains()-Test in compute_cell_buildings.
    from shapely.geometry import Point
    _w["lu"] = landuse_features
    _w["lu_tree"] = _build_geom_tree([f["geometry"] for f in landuse_features])
    _w["bldgs"] = buildings
    _w["bldg_tree"] = _build_geom_tree([b["geometry"] for b in buildings])
    _w["roads"] = roads
    _w["road_tree"] = _build_geom_tree([r["geometry"] for r in roads])
    _w["paved"] = paved_areas
    _w["paved_tree"] = _build_geom_tree([p["geometry"] for p in paved_areas])
    _w["trees"] = trees
    _w["tree_tree"] = _build_geom_tree([Point(t["lon"], t["lat"]) for t in trees])
    _w["infra"] = infra_features
    _w["cells"] = grid_cells
    try:
        with cow_pool() as pool:
            for done, (idx, lu, bm) in enumerate(
                pool.imap_unordered(_cell_worker, range(total), chunksize=_CHUNK)
            ):
                lu_bm[idx] = (lu, bm)
                if progress_callback and (done % 100 == 0 or done + 1 == total):
                    pct = lerp(CELL_SURFACE[0], CELL_SURFACE[1], (done + 1) / total)
                    progress_callback(pct, "Zellanalyse", f"{done + 1}/{total}")
    finally:
        _w.clear()

    # Echtes Horizontwinkel-SVF (Raster über die gesamte bbox, einmalig im
    # Elternprozess — Nachbargebäude AUSSERHALB der Zelle prägen das SVF,
    # deshalb ist es im Zell-Worker nicht berechenbar). Überschreibt den
    # Platzhalter aus compute_cell_buildings.
    from app.services.geodata.lod2.svf import compute_svf_for_cells
    try:
        svf_by_idx = compute_svf_for_cells(grid_cells, buildings, building_source)
    except Exception:  # noqa: BLE001 — SVF darf ein Assessment nie kippen
        log.exception("SVF-Rasterberechnung fehlgeschlagen — Zellen behalten 1.0")
        svf_by_idx = [1.0] * total
    for idx in range(total):
        pair = lu_bm[idx]
        if pair is not None:
            pair[1]["sky_view_factor"] = svf_by_idx[idx]

    # Nachbarschaftsindex (Zensus-Gitter: ±100 m in EPSG:3035)
    if progress_callback:
        progress_callback(
            CELL_NEIGHBORS[0],
            f"Nachbarschaft & Zell-Eingaben ({n_workers()} Kerne) für {total} Zellen",
        )

    coord_idx: dict[tuple[int, int], int] = {}
    step = 100
    for idx, cell in enumerate(grid_cells):
        x = cell.get("x_3035", cell.get("col", 0) * step)
        y = cell.get("y_3035", cell.get("row", 0) * step)
        coord_idx[(x, y)] = idx

    # Echte Gewässer von Kleinstgräben (ditch/drain) trennen: nur echte Gewässer
    # bestimmen Distanz/Nähe, Gräben fließen sehr schwach & dichteskaliert ein.
    real_water_features = [f for f in water_features if not f.get("minor")]
    ditch_features = [f for f in water_features if f.get("minor")]
    water_index = build_water_spatial_index(real_water_features)
    ditch_index = build_water_spatial_index(ditch_features)
    healthcare_indexes = build_healthcare_indexes(infra_features)
    emergency_index = build_emergency_spatial_index(infra_features)
    dyke_index = build_dyke_spatial_index(infra_features)
    cell_inputs: list[dict | None] = [None] * total

    _nw["cells"] = grid_cells
    _nw["lu_bm"] = lu_bm
    _nw["coord_idx"] = coord_idx
    _nw["terrain"] = terrain_by_idx
    _nw["water_index"] = water_index
    _nw["water_features"] = real_water_features
    _nw["ditch_index"] = ditch_index
    _nw["ditch_features"] = ditch_features
    _nw["infra_features"] = infra_features
    _nw["healthcare_indexes"] = healthcare_indexes
    _nw["emergency_index"] = emergency_index
    _nw["dyke_index"] = dyke_index
    _nw["step"] = step
    try:
        with cow_pool() as pool:
            for done, (idx, ci) in enumerate(
                pool.imap_unordered(_neighbor_worker, range(total), chunksize=_CHUNK)
            ):
                cell_inputs[idx] = ci
                if progress_callback and (done % 200 == 0 or done + 1 == total):
                    pct = lerp(CELL_NEIGHBORS[0], CELL_NEIGHBORS[1], (done + 1) / total)
                    progress_callback(pct, "Nachbarschaft & Zell-Eingaben", f"{done + 1}/{total}")
    finally:
        _nw.clear()

    apply_cell_temperature(list(cell_inputs), grid_cells, regional)

    if progress_callback:
        progress_callback(ZENSUS_APPLY[0], "Zensus-Daten anwenden")
    zensus = load_zensus_for_cells(grid_cells)
    apply_zensus_to_cell_inputs(list(cell_inputs), grid_cells, zensus)
    if progress_callback:
        progress_callback(ZENSUS_APPLY[1], "Zensus-Daten anwenden")

    # Heimbewohner-Anteil 85+ je Zelle (CARE_HOME_SHARE_85P) — braucht die
    # Zensus-Altersbänder, deshalb NACH apply_zensus_to_cell_inputs.
    apply_care_home_share(list(cell_inputs), grid_cells, infra_features)

    return list(cell_inputs), regional


def apply_care_home_share(
    cell_inputs: list[dict | None],
    grid_cells: list[dict],
    infra_features: dict,
) -> None:
    """Zellebene ``share_care_home_85p`` (Methodik #95 Rev. 8, §3.6, Log 35).

    Heimbewohner-Anteil an der 85+-Bevölkerung je Zelle aus OSM-Pflege-
    einrichtungen, **kommunen-erwartungstreu** auf das Bundesmittel q̄_pfl
    normiert (Registry ``risks.EXPECTED_ANNUAL_MORTALITY.impact.qbar_pfl``):

    - Einrichtungs-Gewicht w_z: Polygon-Grundfläche in m² (EPSG:3035,
      flächentreu), Punkt-Features und kleine Polygone mit Mindestgewicht
      400 m² (gekennzeichnete Setzung des Berichts).
    - Verteilt wird q̄·Σpop85 proportional w_z — **nur über Zellen mit
      pop_85+ > 0** (Heim-Gewichte in Zellen ohne erfasste 85+-Bevölkerung
      werden der Gewichtssumme entzogen, kein stiller Verlust an der Kappung);
      q_z = min(1, Bewohner_z/pop85_z), Kappung = kleiner dokumentierter
      Restfehler.
    - Kommune ohne OSM-Pflegeeinrichtung: Schlüssel bleibt ungesetzt → der
      v_vers-Modifikator rechnet mit q̄ (Faktor 1; OSM-Lücke nicht von
      „keine Heime" unterscheidbar — dokumentierter Fallback).
    """
    from pyproj import Transformer

    from app.services.engine import override_context

    care_homes = (infra_features or {}).get("care_home_geoms") or []
    if not care_homes:
        return

    # Zellzuordnung über Zellindex-Quantisierung int(v // 100): ``x_3035`` ist
    # der Zell-MITTELPUNKT (Ursprung + 50, grid_service) — die Quantisierung
    # bildet Mittelpunkt UND jeden Punkt innerhalb der Zelle auf denselben Key
    # ab und ist damit unabhängig von der Ecken-/Mittelpunkt-Konvention
    # (Ledger #95 Befund 93: ein Ursprungs-Key matchte nie).
    step = 100
    coord_idx: dict[tuple[int, int], int] = {}
    for idx, cell in enumerate(grid_cells):
        x = cell.get("x_3035", cell.get("col", 0) * step)
        y = cell.get("y_3035", cell.get("row", 0) * step)
        coord_idx[(int(float(x) // step), int(float(y) // step))] = idx

    def pop85(ci: dict | None) -> float:
        bands = (ci or {}).get("pop_age_bands")
        return float(bands.get("a85p") or 0.0) if isinstance(bands, dict) else 0.0

    MIN_WEIGHT_M2 = 400.0
    tr = Transformer.from_crs(4326, 3035, always_xy=True)
    weights: dict[int, float] = {}
    for feat in care_homes:
        geom = feat.get("geometry")
        if geom is None:
            continue
        try:
            from shapely.ops import transform as _shp_transform
            geom_m = _shp_transform(tr.transform, geom)
        except Exception:  # noqa: BLE001 — eine kaputte Geometrie kippt nichts
            continue
        w = max(float(getattr(geom_m, "area", 0.0)), MIN_WEIGHT_M2)
        c = geom_m.centroid
        key = (int(c.x // step), int(c.y // step))
        idx = coord_idx.get(key)
        if idx is None or cell_inputs[idx] is None:
            continue
        if pop85(cell_inputs[idx]) <= 0.0:
            # §3.6: Zellen ohne erfasste 85+-Bevölkerung nehmen nicht an der
            # Verteilung teil (Zensus-Geheimhaltung kleiner Besetzungen).
            continue
        weights[idx] = weights.get(idx, 0.0) + w

    total_w = sum(weights.values())
    total_p85 = sum(pop85(ci) for ci in cell_inputs)
    if total_w <= 0.0 or total_p85 <= 0.0:
        return

    qbar = float(override_context.get_override(
        "risks.EXPECTED_ANNUAL_MORTALITY.impact.qbar_pfl", 0.149) or 0.149)
    residents_total = qbar * total_p85
    for idx, ci in enumerate(cell_inputs):
        if ci is None:
            continue
        p85 = pop85(ci)
        if p85 <= 0.0:
            continue
        residents = residents_total * weights.get(idx, 0.0) / total_w
        ci["share_care_home_85p"] = round(min(1.0, residents / p85), 4)


# Trockenadiabatischer Temperaturgradient (K je Meter Höhenunterschied).
LAPSE_RATE_K_PER_M = 0.0065


def apply_cell_temperature(
    cell_inputs: list[dict], grid_cells: list[dict], regional: dict,
) -> None:
    """Setzt ``summer_temp_cell`` (und Bausteine) je Zelle — in-place.

    ``T_Zelle = T_Raster(1 km) + [ΔT_UHI − Mittel(ΔT_UHI je 1-km-Zelle)] + Höhenterm``

    Beide Zuschläge werden **mittelwerttreu innerhalb der 1-km-Rasterzelle**
    angesetzt: Das DWD-Raster wird aus Stationsdaten interpoliert und enthält die
    Wärmeinsel bereits teilweise (allerdings ohne Urbanisierungs-Prädiktor, also
    unzuverlässig). Würde man das volle ΔT_UHI aufaddieren, zählte man den
    erfassten Anteil doppelt. Indem nur die **Abweichung vom Rasterzellen-Mittel**
    addiert wird, bleibt der 1-km-Mittelwert exakt der gemessene und lediglich die
    Feinstruktur darunter kommt aus dem UHI-Modell. Analog beim Höhenterm.
    """
    from app.services.climate import dwd_cdc_grid

    cells = [ci for ci in cell_inputs if ci is not None]
    if not cells:
        return

    fallback = float(regional.get("summer_temp_mean") or 0.0)
    points: list[tuple[float, float]] = []
    for cell in grid_cells:
        c = cell["geometry"].centroid
        points.append((float(c.x), float(c.y)))

    try:
        grid = dwd_cdc_grid.climatology_grid("air_temp_mean", dwd_cdc_grid.SUMMER_MONTHS)
        sampled = dwd_cdc_grid.sample_grid_points(grid, points)
    except Exception:  # noqa: BLE001 — Rasterfehler darf kein Assessment kippen
        log.exception("Sommertemperatur-Raster nicht verfügbar — Bundesland-Mittel")
        grid, sampled = None, [None] * len(points)

    # 1-km-Rasterzelle je 100-m-Zelle (INSPIRE-Koordinaten ganzzahlig teilen).
    groups: dict[tuple[int, int], list[int]] = {}
    for idx, cell in enumerate(grid_cells):
        x = int(cell.get("x_3035", cell.get("col", 0) * 100))
        y = int(cell.get("y_3035", cell.get("row", 0) * 100))
        groups.setdefault((x // 1000, y // 1000), []).append(idx)

    n = len(cell_inputs)
    for _key, idxs in groups.items():
        valid = [i for i in idxs if i < n and cell_inputs[i] is not None]
        if not valid:
            continue
        uhi_vals = [float(cell_inputs[i].get("uhi_delta_mean") or 0.0) for i in valid]
        elev_vals = [float(cell_inputs[i].get("mean_elevation_m") or 0.0) for i in valid]
        uhi_mean = sum(uhi_vals) / len(uhi_vals)
        elev_mean = sum(elev_vals) / len(elev_vals)
        for i in valid:
            ci = cell_inputs[i]
            base = sampled[i] if i < len(sampled) and sampled[i] is not None else fallback
            uhi_dev = float(ci.get("uhi_delta_mean") or 0.0) - uhi_mean
            elev_dev = float(ci.get("mean_elevation_m") or 0.0) - elev_mean
            lapse = -LAPSE_RATE_K_PER_M * elev_dev
            ci["summer_temp_raster"] = round(float(base), 2)
            ci["summer_temp_uhi_dev"] = round(uhi_dev, 3)
            ci["summer_temp_lapse"] = round(lapse, 3)
            ci["summer_temp_cell"] = round(float(base) + uhi_dev + lapse, 2)
