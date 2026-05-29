"""Heat / Urban Heat Island assessor — Levels 1–4.

Level 1: OSM land-use based estimation for realistic per-cell impervious
          fraction, albedo, green/water fractions and UHI delta.

Level 2: Same as Level 1 but adds DWD regional climate data for reference
          temperature (Bundesland-specific hot days / summer temps).

Level 3: Detailed building & surface analysis. Fetches individual building
          footprints, road network, and tree positions from OSM. Calculates
          building coverage, average height, road surface, tree canopy, and a
          simplified sky-view factor for refined UHI modeling.

Level 4: Full analysis including differentiated green cooling (forest vs
          grassland vs farmland), night-time UHI & tropical night risk,
          ventilation corridors, vulnerability index, and climate projections.

Key formulas:
- UHI intensity: ΔT = α × (1 − albedo) × impervious_fraction + β × bldg_factor
- Level 3+: − γ × green_cooling − δ × water_cooling + ε × (1 − SVF) × height_factor
- Level 4+: − ventilation_cooling + night_UHI_retention
- Heat stress index: 0–10 scale based on combined temperature and UHI delta
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

# ── Multiprocessing helpers ───────────────────────────────────────────────────
# Worker functions at module level so they are picklable / fork-inheritable.
# ``_w`` is populated in the parent before Pool creation; forked workers
# inherit it via copy-on-write on Linux.

_w: dict = {}
_N_WORKERS = min(os.cpu_count() or 4, 8)
_MP = multiprocessing.get_context("fork")
_CHUNK = 50


def _cell_lu(idx: int):
    """Worker: compute land-use for one grid cell (Level 1/2)."""
    from app.services.climate.heat.osm_data import compute_cell_landuse
    return idx, compute_cell_landuse(_w["cells"][idx]["geometry"], _w["lu"])


def _cell_lu_bm(idx: int):
    """Worker: compute land-use + building metrics for one cell (Level 3/4)."""
    from app.services.climate.heat.osm_data import compute_cell_landuse, compute_cell_buildings
    g = _w["cells"][idx]["geometry"]
    lu = compute_cell_landuse(g, _w["lu"])
    bm = compute_cell_buildings(g, _w["bldgs"], _w["roads"], _w["trees"])
    return idx, lu, bm


class HeatAssessor(ClimateAssessor):
    climate_type = "heat"
    label = "Hitzewellen & urbane Überhitzung"
    max_level = 4  # Levels 1-4 implemented

    def get_required_config(self) -> list[ConfigParamDef]:
        return [
            # Reference temperature
            ConfigParamDef("heat", "reference_temp_c", 25.0,
                           "Sommer-Referenztemperatur (°C) für die Region"),
            # Albedo
            ConfigParamDef("heat", "albedo_urban_mixed", 0.20,
                           "Mittlerer Albedo-Wert für gemischte Stadtflächen"),
            ConfigParamDef("heat", "albedo_green", 0.25,
                           "Albedo-Wert für Grünflächen"),
            ConfigParamDef("heat", "albedo_asphalt", 0.12,
                           "Albedo-Wert für Asphaltflächen"),
            ConfigParamDef("heat", "albedo_concrete", 0.30,
                           "Albedo-Wert für Betonflächen"),
            # Building density
            ConfigParamDef("heat", "building_density_per_km2", 75.0,
                           "Durchschnittliche Gebäudedichte (Gebäude/km²)"),
            # UHI formula coefficients
            ConfigParamDef("heat", "uhi_alpha", 6.0,
                           "UHI-Koeffizient α (Albedo & Versiegelung)"),
            ConfigParamDef("heat", "uhi_beta", 2.0,
                           "UHI-Koeffizient β (Gebäudedichte)"),
            # Population
            ConfigParamDef("heat", "population_density_per_km2", 230.0,
                           "Durchschnittliche Bevölkerungsdichte (Einw./km²)"),
            # Impervious fraction
            ConfigParamDef("heat", "impervious_fraction_default", 0.45,
                           "Geschätzter Versiegelungsgrad (0–1) städtisch"),
            # Kommune type factor (1.0 = average, >1 = more urban)
            ConfigParamDef("heat", "urbanity_factor", 1.0,
                           "Urbanitätsfaktor (0.5=ländlich, 1.0=mittel, 1.5=Großstadt)"),
            # Level 2/3/4 additional coefficients
            ConfigParamDef("heat", "green_cooling_gamma", 3.5,
                           "UHI-Koeffizient γ – Kühlwirkung durch Grünflächen (Level 2+)"),
            ConfigParamDef("heat", "water_cooling_delta", 2.0,
                           "UHI-Koeffizient δ – Kühlwirkung durch Gewässer (Level 2+)"),
            ConfigParamDef("heat", "canyon_epsilon", 1.5,
                           "UHI-Koeffizient ε – Straßenschlucht-Effekt (Level 3+)"),
            ConfigParamDef("heat", "tree_cooling_per_unit", 0.3,
                           "Kühleffekt pro Baum in °C (Level 3+)"),
            # Level 4 specific
            ConfigParamDef("heat", "forest_cooling_factor", 1.8,
                           "Verstärkter Kühleffekt von Wald vs. Gras (Level 4)"),
            ConfigParamDef("heat", "ventilation_cooling_max", 1.5,
                           "Max. Kühlwirkung durch Frischluftschneisen (°C, Level 4)"),
            ConfigParamDef("heat", "thermal_mass_factor", 0.6,
                           "Wärmespeicherung Gebäudemasse Nacht-UHI (Level 4)"),
        ]

    def get_indicators(self) -> list[IndicatorDef]:
        return [
            IndicatorDef("temperature_estimate", "Geschätzte Temperatur", "°C",
                         "Geschätzte Oberflächentemperatur bei Sommerhitze", 15.0, 50.0),
            IndicatorDef("uhi_delta", "UHI-Aufschlag", "K",
                         "Urban Heat Island Temperaturerhöhung über Referenz", 0.0, 15.0),
            IndicatorDef("heat_stress_index", "Hitzebelastungs-Index", "",
                         "Kombinierter Hitzebelastungs-Index (0=gering, 10=extrem)", 0.0, 10.0),
            IndicatorDef("impervious_fraction", "Versiegelungsgrad", "",
                         "Anteil versiegelter Fläche (0–1)", 0.0, 1.0),
            IndicatorDef("estimated_affected_pop", "Betroffene Bevölkerung", "Pers.",
                         "Geschätzte betroffene Einwohner in der Zelle", 0.0, 100000.0),
            # Level 2+ indicators
            IndicatorDef("green_fraction", "Grünflächenanteil", "",
                         "Anteil Grünflächen in der Zelle (Level 2+)", 0.0, 1.0),
            IndicatorDef("water_fraction", "Gewässeranteil", "",
                         "Anteil Wasserflächen in der Zelle (Level 2+)", 0.0, 1.0),
            IndicatorDef("albedo", "Albedo", "",
                         "Mittlerer Albedo-Wert der Zelloberfläche (Level 2+)", 0.0, 1.0),
            # Level 3 indicators
            IndicatorDef("building_coverage", "Gebäudebedeckung", "",
                         "Anteil der Zelle, der von Gebäuden bedeckt ist (Level 3)", 0.0, 1.0),
            IndicatorDef("avg_building_height", "Mittlere Gebäudehöhe", "m",
                         "Durchschnittliche Gebäudehöhe in der Zelle (Level 3)", 0.0, 100.0),
            IndicatorDef("tree_canopy_fraction", "Baumkronenanteil", "",
                         "Anteil der Baumkronenbedeckung (Level 3)", 0.0, 1.0),
            IndicatorDef("sky_view_factor", "Sky-View-Faktor", "",
                         "Himmelssichtfaktor – 1=offen, 0=verbaut (Level 3)", 0.0, 1.0),
            # Level 4 indicators
            IndicatorDef("night_uhi_delta", "Nacht-UHI-Aufschlag", "K",
                         "Nächtliche UHI-Intensität / Tropennacht-Risiko (Level 4)", 0.0, 10.0),
            IndicatorDef("night_temp_estimate", "Geschätzte Nachttemperatur", "°C",
                         "Tiefsttemperatur in Sommernächten (Level 4)", 10.0, 35.0),
            IndicatorDef("ventilation_cooling", "Belüftungs-Kühlung", "K",
                         "Kühleffekt durch Frischluftschneisen (Level 4)", 0.0, 5.0),
            IndicatorDef("vulnerability_index", "Vulnerabilitäts-Index", "",
                         "Kombination aus Hitzebelastung × Bevölkerungsexposition (Level 4)", 0.0, 10.0),
            IndicatorDef("tropical_night_risk", "Tropennacht-Risiko", "",
                         "Wahrscheinlichkeit für Tropennächte (Tmin≥20°C, Level 4)", 0.0, 1.0),
            IndicatorDef("forest_fraction", "Waldanteil", "",
                         "Anteil Waldfläche in der Zelle (Level 4)", 0.0, 1.0),
            IndicatorDef("farmland_fraction", "Ackerland-Anteil", "",
                         "Anteil landwirtschaftlicher Fläche (Level 4)", 0.0, 1.0),
        ]

    def assess(
        self,
        kommune_id: int,
        level: int,
        grid_cells: list[dict],
        config_params: dict[str, Any],
        progress_callback: Any = None,
    ) -> list[CellResult]:
        log.info("[HEAT] assess() called: kommune=%s level=%s cells=%d", kommune_id, level, len(grid_cells))
        if level == 1:
            return self._assess_level1(grid_cells, config_params, progress_callback)
        if level == 2:
            return self._assess_level2(grid_cells, config_params, progress_callback)
        if level == 3:
            return self._assess_level3(grid_cells, config_params, progress_callback)
        if level == 4:
            return self._assess_level4(grid_cells, config_params, progress_callback)
        raise NotImplementedError(f"Heat assessment level {level} not yet implemented")

    def _assess_level1(
        self,
        grid_cells: list[dict],
        config: dict[str, Any],
        progress_callback: Any = None,
    ) -> list[CellResult]:
        """Level 1: Uses OSM land-use data for realistic per-cell surface
        properties (impervious fraction, green/water fraction, albedo).
        Falls back to statistical estimation for cells with no OSM coverage.
        """
        from app.services.climate.heat.osm_data import fetch_landuse, compute_cell_landuse

        # Read config with defaults
        ref_temp = float(config.get("heat.reference_temp_c", 25.0))
        alpha = float(config.get("heat.uhi_alpha", 6.0))
        beta = float(config.get("heat.uhi_beta", 2.0))
        gamma = float(config.get("heat.green_cooling_gamma", 3.5))
        delta = float(config.get("heat.water_cooling_delta", 2.0))
        bldg_density = float(config.get("heat.building_density_per_km2", 75.0))
        pop_density = float(config.get("heat.population_density_per_km2", 230.0))
        urbanity = float(config.get("heat.urbanity_factor", 1.0))

        bldg_factor = min(bldg_density * urbanity / 100.0, 1.5)

        total = len(grid_cells)
        results = []

        if progress_callback:
            progress_callback(0.0, "Lade Konfiguration & statistische Basisdaten")

        # Fetch OSM land-use data for realistic impervious fractions
        if progress_callback:
            progress_callback(1.0, "Herunterladen OSM-Landnutzungsdaten")
        log.info("Level 1: Fetching OSM land-use data …")
        landuse_features, lu_bytes = fetch_landuse(grid_cells)
        lu_mb = lu_bytes / 1_048_576
        log.info("Level 1: Got %d land-use features", len(landuse_features))
        if progress_callback:
            progress_callback(10.0, f"Berechne Landnutzung parallel ({_N_WORKERS} Kerne) für {total} Zellen",
                              f"{len(landuse_features)} Landnutzungs-Features ({lu_mb:.1f} MB)")
        log.info("Level 1: parallel land-use with %d workers", _N_WORKERS)

        _w["lu"] = landuse_features
        _w["cells"] = grid_cells
        lu_map: list[dict | None] = [None] * total
        try:
            with _MP.Pool(_N_WORKERS) as pool:
                for done, (idx, lu) in enumerate(
                    pool.imap_unordered(_cell_lu, range(total), chunksize=_CHUNK)
                ):
                    lu_map[idx] = lu
                    if progress_callback and done % 200 == 0:
                        pct = 10.0 + (done + 1) / total * 80.0
                        progress_callback(pct)
        finally:
            _w.clear()

        if progress_callback:
            progress_callback(90.0, "Berechne UHI-Intensität & Hitzebelastung")

        for i, cell in enumerate(grid_cells):
            lu = lu_map[i]
            imp_frac = lu["impervious_fraction"]
            albedo = lu["albedo"]
            green_frac = lu["green_fraction"]
            water_frac = lu["water_fraction"]

            uhi_delta = (
                alpha * (1.0 - albedo) * imp_frac
                + beta * bldg_factor
                - gamma * green_frac
                - delta * water_frac
            )
            uhi_delta = max(0.0, uhi_delta)

            temp_estimate = ref_temp + uhi_delta
            heat_stress = min(10.0, uhi_delta * 1.5)

            cell_area_km2 = (cell.get("cell_size_m", 100) / 1000.0) ** 2
            pop_factor = 0.5 + imp_frac
            affected_pop = pop_density * urbanity * cell_area_km2 * pop_factor

            results.append(CellResult(
                grid_cell_id=cell["id"],
                indicators={
                    "temperature_estimate": round(temp_estimate, 1),
                    "uhi_delta": round(uhi_delta, 2),
                    "heat_stress_index": round(heat_stress, 1),
                    "impervious_fraction": round(imp_frac, 3),
                    "estimated_affected_pop": round(affected_pop, 0),
                    "green_fraction": round(green_frac, 3),
                    "water_fraction": round(water_frac, 3),
                    "albedo": round(albedo, 4),
                },
            ))

        if progress_callback:
            progress_callback(100.0, "Speichere Ergebnisse")

        return results

    # ── Level 2: OSM land-use based ────────────────────────────────────────────

    def _assess_level2(
        self,
        grid_cells: list[dict],
        config: dict[str, Any],
        progress_callback: Any = None,
    ) -> list[CellResult]:
        """Level 2: Uses real OSM land-use/natural data per grid cell.

        Fetches landuse polygons once for the whole area, then intersects
        each cell to derive impervious fraction, albedo, and green/water
        fractions. UHI formula is the same as Level 1, but with per-cell
        surface properties instead of uniform estimates.
        """
        from app.services.climate.heat.osm_data import fetch_landuse, compute_cell_landuse
        from app.services.climate.dwd_data import (
            fetch_dwd_reference_temp, fetch_hot_days, get_regional_climate,
        )

        # Use DWD data for reference temperature if bundesland is known
        bundesland = config.get("_bundesland", "")
        if bundesland:
            regional = get_regional_climate(bundesland)
            ref_temp = regional["summer_max_temp_avg"]
            hot_days = regional["hot_days_per_year"]
            log.info("Level 2: Using DWD data for %s – ref %.1f°C, %.0f hot days/yr",
                     bundesland, ref_temp, hot_days)
        else:
            ref_temp = float(config.get("heat.reference_temp_c", 25.0))
            hot_days = 10.0

        alpha = float(config.get("heat.uhi_alpha", 6.0))
        beta = float(config.get("heat.uhi_beta", 2.0))
        gamma = float(config.get("heat.green_cooling_gamma", 3.5))
        delta = float(config.get("heat.water_cooling_delta", 2.0))
        bldg_density = float(config.get("heat.building_density_per_km2", 75.0))
        pop_density = float(config.get("heat.population_density_per_km2", 230.0))
        urbanity = float(config.get("heat.urbanity_factor", 1.0))

        bldg_factor = min(bldg_density * urbanity / 100.0, 1.5)

        # Fetch OSM land-use data for the whole grid extent
        if progress_callback:
            progress_callback(1.0, "Lade DWD-Klimadaten für Region")
        if progress_callback:
            progress_callback(2.0, "Herunterladen OSM-Landnutzungsdaten")
        log.info("Level 2: Fetching OSM land-use data …")
        landuse_features, lu_bytes = fetch_landuse(grid_cells)
        lu_mb = lu_bytes / 1_048_576
        log.info("Level 2: Got %d land-use features", len(landuse_features))

        total = len(grid_cells)
        results: list[CellResult] = []

        # ── Parallel land-use computation ─────────────────────────────────
        if progress_callback:
            progress_callback(15.0, f"Berechne Landnutzung parallel ({_N_WORKERS} Kerne) für {total} Zellen",
                              f"{len(landuse_features)} Features ({lu_mb:.1f} MB)")
        log.info("Level 2: parallel land-use with %d workers", _N_WORKERS)

        _w["lu"] = landuse_features
        _w["cells"] = grid_cells
        lu_map: list[dict | None] = [None] * total
        try:
            with _MP.Pool(_N_WORKERS) as pool:
                for done, (idx, lu) in enumerate(
                    pool.imap_unordered(_cell_lu, range(total), chunksize=_CHUNK)
                ):
                    lu_map[idx] = lu
                    if progress_callback and done % 200 == 0:
                        pct = 15.0 + (done + 1) / total * 75.0
                        progress_callback(pct)
        finally:
            _w.clear()

        if progress_callback:
            progress_callback(90.0, "Berechne UHI & Hitzebelastungsindex")

        for i, cell in enumerate(grid_cells):
            lu = lu_map[i]
            imp_frac = lu["impervious_fraction"]
            albedo = lu["albedo"]
            green_frac = lu["green_fraction"]
            water_frac = lu["water_fraction"]

            uhi_delta = (
                alpha * (1.0 - albedo) * imp_frac
                + beta * bldg_factor
                - gamma * green_frac
                - delta * water_frac
            )
            uhi_delta = max(0.0, uhi_delta)

            temp_estimate = ref_temp + uhi_delta
            heat_stress = min(10.0, uhi_delta * 1.5)

            cell_area_km2 = (cell.get("cell_size_m", 100) / 1000.0) ** 2
            pop_factor = 0.5 + imp_frac
            affected_pop = pop_density * urbanity * cell_area_km2 * pop_factor

            rs = min(10.0, heat_stress)
            results.append(CellResult(
                grid_cell_id=cell["id"],
                indicators={
                    "temperature_estimate": round(temp_estimate, 1),
                    "uhi_delta": round(uhi_delta, 2),
                    "heat_stress_index": round(heat_stress, 1),
                    "impervious_fraction": round(imp_frac, 3),
                    "estimated_affected_pop": round(affected_pop, 0),
                    "green_fraction": round(green_frac, 3),
                    "water_fraction": round(water_frac, 3),
                    "albedo": round(albedo, 4),
                    "risk_score": round(rs, 2),
                },
                risk_score=round(rs, 2),
            ))

        if progress_callback:
            progress_callback(100.0, "Speichere Ergebnisse")

        return results

    # ── Level 3: Detailed building & surface analysis ──────────────────────────

    def _assess_level3(
        self,
        grid_cells: list[dict],
        config: dict[str, Any],
        progress_callback: Any = None,
    ) -> list[CellResult]:
        """Level 3: Uses OSM land-use *and* building/road/tree data.

        Builds on Level 2 land-use data but replaces the statistical
        building density with actual footprint analysis, adds road surface
        coverage, tree canopy cooling, and a simplified sky-view factor
        that models the street-canyon heat-trapping effect.
        """
        from app.services.climate.heat.osm_data import (
            fetch_landuse, compute_cell_landuse,
            fetch_buildings_and_roads, compute_cell_buildings,
        )
        from app.services.climate.dwd_data import (
            get_regional_climate, estimate_building_albedo,
        )

        # Use DWD data for reference temperature if bundesland is known
        bundesland = config.get("_bundesland", "")
        if bundesland:
            regional = get_regional_climate(bundesland)
            ref_temp = regional["summer_max_temp_avg"]
            hot_days = regional["hot_days_per_year"]
            log.info("Level 3: Using DWD data for %s – ref %.1f°C, %.0f hot days/yr",
                     bundesland, ref_temp, hot_days)
        else:
            ref_temp = float(config.get("heat.reference_temp_c", 25.0))
            hot_days = 10.0

        alpha = float(config.get("heat.uhi_alpha", 6.0))
        beta = float(config.get("heat.uhi_beta", 2.0))
        gamma = float(config.get("heat.green_cooling_gamma", 3.5))
        delta = float(config.get("heat.water_cooling_delta", 2.0))
        epsilon = float(config.get("heat.canyon_epsilon", 1.5))
        tree_cool = float(config.get("heat.tree_cooling_per_unit", 0.3))
        pop_density = float(config.get("heat.population_density_per_km2", 230.0))
        urbanity = float(config.get("heat.urbanity_factor", 1.0))

        # ── Phase 1: Fetch OSM data (sequential to avoid 429 rate-limit) ─
        if progress_callback:
            progress_callback(1.0, "Lade DWD-Klimadaten für Region")
        if progress_callback:
            progress_callback(2.0, "Herunterladen OSM-Landnutzungsdaten")
        log.info("Level 3: Fetching OSM land-use data …")
        landuse_features, lu_bytes = fetch_landuse(grid_cells)
        lu_mb = lu_bytes / 1_048_576
        log.info("Level 3: Got %d land-use features", len(landuse_features))

        if progress_callback:
            progress_callback(10.0, "Herunterladen OSM-Gebäude, Straßen & Bäume",
                              f"{len(landuse_features)} Landnutzungs-Features ({lu_mb:.1f} MB)")
        log.info("Level 3: Fetching OSM buildings/roads/trees …")
        osm_detail = fetch_buildings_and_roads(grid_cells)
        buildings = osm_detail["buildings"]
        roads = osm_detail["roads"]
        trees = osm_detail["trees"]
        bm_bytes = osm_detail.get("_response_bytes", 0)
        bm_mb = bm_bytes / 1_048_576
        log.info("Level 3: Got %d buildings, %d roads, %d trees",
                 len(buildings), len(roads), len(trees))

        if progress_callback:
            progress_callback(20.0, "Lade Zensus-Gebäudealter & Albedo-Daten",
                              f"{len(buildings)} Gebäude, {len(roads)} Straßen, {len(trees)} Bäume ({bm_mb:.1f} MB)")

        # Pre-compute Zensus-based building albedo by type
        _albedo_cache: dict[str, dict] = {}

        def _get_bldg_albedo(btype: str, levels: int) -> float:
            key = f"{btype}:{levels}"
            if key not in _albedo_cache:
                _albedo_cache[key] = estimate_building_albedo(btype, levels)
            return _albedo_cache[key]["effective_albedo"]

        # ── Phase 2: Parallel per-cell geometry analysis ──────────────────
        total = len(grid_cells)
        results: list[CellResult] = []

        if progress_callback:
            progress_callback(22.0, f"Analyse Oberflächen parallel ({_N_WORKERS} Kerne) für {total} Zellen")
        log.info("Level 3: parallel per-cell analysis with %d workers", _N_WORKERS)

        _w["lu"] = landuse_features
        _w["bldgs"] = buildings
        _w["roads"] = roads
        _w["trees"] = trees
        _w["cells"] = grid_cells
        lu_bm: list[tuple | None] = [None] * total
        try:
            with _MP.Pool(_N_WORKERS) as pool:
                for done, (idx, lu, bm) in enumerate(
                    pool.imap_unordered(_cell_lu_bm, range(total), chunksize=_CHUNK)
                ):
                    lu_bm[idx] = (lu, bm)
                    if progress_callback and done % 200 == 0:
                        pct = 22.0 + (done + 1) / total * 60.0
                        progress_callback(pct, "Zellanalyse", f"{done + 1}/{total}")
        finally:
            _w.clear()

        # ── Phase 3: UHI computation (serial, fast) ───────────────────────
        if progress_callback:
            progress_callback(85.0, "Berechne UHI-Intensität & Hitzebelastung")

        for i, cell in enumerate(grid_cells):
            lu, bm = lu_bm[i]
            cell_size_m = cell.get("cell_size_m", 100)

            imp_frac_lu = lu["impervious_fraction"]
            albedo_lu = lu["albedo"]
            green_frac = lu["green_fraction"]
            water_frac = lu["water_fraction"]

            bldg_cov = bm["building_coverage"]
            avg_height = bm["avg_building_height"]
            road_cov = bm["road_coverage"]
            canopy_frac = bm["tree_canopy_fraction"]
            svf = bm["sky_view_factor"]

            avg_levels = max(1, int(avg_height / 3.0))
            bldg_albedo = _get_bldg_albedo("residential", avg_levels)
            if bldg_cov > 0:
                albedo = bldg_cov * bldg_albedo + (1.0 - bldg_cov) * albedo_lu
            else:
                albedo = albedo_lu

            imp_frac_detail = bldg_cov + road_cov * 0.95
            if imp_frac_detail > 0.01:
                imp_frac = min(imp_frac_detail, 0.98)
            else:
                imp_frac = imp_frac_lu
            imp_frac = max(0.02, min(imp_frac, 0.98))

            height_factor = min(avg_height / 15.0, 2.0)
            bldg_factor = bldg_cov * height_factor

            uhi_base = alpha * (1.0 - albedo) * imp_frac + beta * bldg_factor
            uhi_cooling = gamma * green_frac + delta * water_frac + tree_cool * canopy_frac * 10.0
            uhi_canyon = epsilon * (1.0 - svf) * height_factor
            uhi_delta = max(0.0, uhi_base - uhi_cooling + uhi_canyon)

            temp_estimate = ref_temp + uhi_delta
            heat_stress = min(10.0, uhi_delta * 1.5)

            cell_area_km2 = (cell_size_m / 1000.0) ** 2
            pop_factor = 0.3 + bldg_cov * 2.0 + (1.0 - green_frac - water_frac) * 0.3
            affected_pop = pop_density * urbanity * cell_area_km2 * pop_factor

            rs = min(10.0, heat_stress)
            results.append(CellResult(
                grid_cell_id=cell["id"],
                indicators={
                    "temperature_estimate": round(temp_estimate, 1),
                    "uhi_delta": round(uhi_delta, 2),
                    "heat_stress_index": round(heat_stress, 1),
                    "impervious_fraction": round(imp_frac, 3),
                    "estimated_affected_pop": round(affected_pop, 0),
                    "green_fraction": round(green_frac, 3),
                    "water_fraction": round(water_frac, 3),
                    "albedo": round(albedo, 4),
                    "building_coverage": round(bldg_cov, 4),
                    "avg_building_height": round(avg_height, 1),
                    "tree_canopy_fraction": round(canopy_frac, 4),
                    "sky_view_factor": round(svf, 3),
                    "risk_score": round(rs, 2),
                },
                risk_score=round(rs, 2),
            ))

        if progress_callback:
            progress_callback(100.0, "Speichere Ergebnisse")

        return results

    # ── Level 4: Full analysis with night UHI, ventilation, vulnerability ──────

    def _assess_level4(
        self,
        grid_cells: list[dict],
        config: dict[str, Any],
        progress_callback: Any = None,
    ) -> list[CellResult]:
        """Level 4: Full heat assessment with all refinements.

        Builds on Level 3 data but adds:
        - Differentiated green cooling: forest cools more than grassland/farmland
        - Night-time UHI and tropical night risk (thermal mass retention)
        - Ventilation corridors: cells adjacent to open land get wind cooling
        - Vulnerability index combining heat stress with population exposure
        - Climate projection indicator based on DWD trend data
        """
        from app.services.climate.heat.osm_data import (
            fetch_landuse, compute_cell_landuse,
            fetch_buildings_and_roads, compute_cell_buildings,
        )
        from app.services.climate.dwd_data import (
            get_regional_climate, estimate_building_albedo,
        )

        # ── Config ────────────────────────────────────────────────────────
        bundesland = config.get("_bundesland", "")
        if bundesland:
            regional = get_regional_climate(bundesland)
            ref_temp = regional["summer_max_temp_avg"]
            hot_days = regional["hot_days_per_year"]
            tropical_nights = regional["tropical_nights_per_year"]
            mean_temp_annual = regional["mean_temp_annual"]
            log.info("Level 4: DWD data for %s – ref %.1f°C, %.0f hot days, %.1f tropical nights",
                     bundesland, ref_temp, hot_days, tropical_nights)
        else:
            ref_temp = float(config.get("heat.reference_temp_c", 25.0))
            hot_days = 10.0
            tropical_nights = 1.0
            mean_temp_annual = 9.8

        # Night reference: calibrated to DWD observed tropical nights.
        # Typical German summer DTR is ~10°C; additionally, if DWD reports
        # tropical nights > 0, we reduce the offset further so that the UHI
        # model can produce non-zero tropical risk for built-up cells.
        base_dtr = 10.0  # typical diurnal temperature range
        if tropical_nights > 0:
            # Shift night baseline up to be consistent with observed data
            # More tropical nights → warmer nights → smaller effective DTR
            dtr_adjustment = min(2.0, tropical_nights * 0.5)
            night_ref_temp = ref_temp - (base_dtr - dtr_adjustment)
        else:
            night_ref_temp = ref_temp - base_dtr
        log.info("Level 4: night_ref_temp = %.1f°C (DTR-based, tropical_nights=%.1f)",
                 night_ref_temp, tropical_nights)

        alpha = float(config.get("heat.uhi_alpha", 6.0))
        beta = float(config.get("heat.uhi_beta", 2.0))
        gamma = float(config.get("heat.green_cooling_gamma", 3.5))
        delta_w = float(config.get("heat.water_cooling_delta", 2.0))
        epsilon = float(config.get("heat.canyon_epsilon", 1.5))
        tree_cool = float(config.get("heat.tree_cooling_per_unit", 0.3))
        pop_density = float(config.get("heat.population_density_per_km2", 230.0))
        urbanity = float(config.get("heat.urbanity_factor", 1.0))
        forest_factor = float(config.get("heat.forest_cooling_factor", 1.8))
        vent_cool_max = float(config.get("heat.ventilation_cooling_max", 1.5))
        thermal_mass = float(config.get("heat.thermal_mass_factor", 0.6))

        # ── Phase 1: Fetch all data (sequential to avoid 429 rate-limit) ─
        if progress_callback:
            progress_callback(1.0, "Lade DWD-Klimadaten für Region")
        if progress_callback:
            progress_callback(2.0, "Herunterladen OSM-Landnutzungsdaten")
        log.info("Level 4: Fetching OSM land-use data …")
        landuse_features, lu_bytes = fetch_landuse(grid_cells)
        lu_mb = lu_bytes / 1_048_576
        log.info("Level 4: Got %d land-use features", len(landuse_features))

        if progress_callback:
            progress_callback(8.0, "Herunterladen OSM-Gebäude, Straßen & Bäume",
                              f"{len(landuse_features)} Landnutzungs-Features ({lu_mb:.1f} MB)")
        log.info("Level 4: Fetching OSM buildings/roads/trees …")
        osm_detail = fetch_buildings_and_roads(grid_cells)
        buildings = osm_detail["buildings"]
        roads = osm_detail["roads"]
        trees = osm_detail["trees"]
        bm_bytes = osm_detail.get("_response_bytes", 0)
        bm_mb = bm_bytes / 1_048_576
        log.info("Level 4: Got %d buildings, %d roads, %d trees",
                 len(buildings), len(roads), len(trees))

        if progress_callback:
            progress_callback(15.0, "Lade Zensus-Gebäudealter & Albedo-Daten",
                              f"{len(buildings)} Gebäude, {len(roads)} Straßen, {len(trees)} Bäume ({bm_mb:.1f} MB)")

        _albedo_cache: dict[str, dict] = {}

        def _get_bldg_albedo(btype: str, levels: int) -> float:
            key = f"{btype}:{levels}"
            if key not in _albedo_cache:
                _albedo_cache[key] = estimate_building_albedo(btype, levels)
            return _albedo_cache[key]["effective_albedo"]

        # ── Phase 2: Parallel per-cell geometry analysis ──────────────────
        if progress_callback:
            progress_callback(18.0, f"Analyse Oberflächen parallel ({_N_WORKERS} Kerne) für {len(grid_cells)} Zellen")
        log.info("Level 4: parallel per-cell analysis with %d workers", _N_WORKERS)

        total = len(grid_cells)
        cell_data: list[dict | None] = [None] * total

        _w["lu"] = landuse_features
        _w["bldgs"] = buildings
        _w["roads"] = roads
        _w["trees"] = trees
        _w["cells"] = grid_cells
        try:
            with _MP.Pool(_N_WORKERS) as pool:
                for done, (idx, lu, bm) in enumerate(
                    pool.imap_unordered(_cell_lu_bm, range(total), chunksize=_CHUNK)
                ):
                    cell_data[idx] = {"cell": grid_cells[idx], "lu": lu, "bm": bm}
                    if progress_callback and done % 200 == 0:
                        pct = 18.0 + (done + 1) / total * 22.0
                        progress_callback(pct, "Zellanalyse", f"{done + 1}/{total}")
        finally:
            _w.clear()

        # ── Phase 3: Compute ventilation index ───────────────────────────
        # Cells near open land (low impervious, high green) get wind cooling.
        # Build a grid index for neighbor lookup.
        if progress_callback:
            progress_callback(42.0, "Berechne Frischluftschneisen & Belüftungskorridore")

        row_col_index: dict[tuple[int, int], int] = {}
        for idx, cd in enumerate(cell_data):
            c = cd["cell"]
            row_col_index[(c["row"], c["col"])] = idx

        ventilation_scores: list[float] = []
        for idx, cd in enumerate(cell_data):
            c = cd["cell"]
            row, col = c["row"], c["col"]
            # Look at 8 neighbors
            open_neighbors = 0
            total_neighbors = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    ni = row_col_index.get((row + dr, col + dc))
                    if ni is None:
                        # Edge cell: treat as open land
                        open_neighbors += 1
                        total_neighbors += 1
                        continue
                    total_neighbors += 1
                    nb_lu = cell_data[ni]["lu"]
                    nb_bm = cell_data[ni]["bm"]
                    # Neighbor is "open" if low building coverage and high green/water/farm
                    nb_open = (nb_bm["building_coverage"] < 0.05
                               and nb_lu["green_fraction"] + nb_lu["water_fraction"]
                               + nb_lu.get("farmland_fraction", 0) > 0.3)
                    if nb_open:
                        open_neighbors += 1

            # Ventilation score: 0 (enclosed) to 1 (all neighbors are open)
            vent_score = open_neighbors / max(total_neighbors, 1)
            ventilation_scores.append(vent_score)

        # ── Phase 4: Main computation ────────────────────────────────────
        if progress_callback:
            progress_callback(50.0, f"Berechne UHI Tag/Nacht & Hitzebelastung für {total} Zellen")

        results: list[CellResult] = []

        for i, cd in enumerate(cell_data):
            cell = cd["cell"]
            lu = cd["lu"]
            bm = cd["bm"]
            cell_size_m = cell.get("cell_size_m", 100)

            imp_frac_lu = lu["impervious_fraction"]
            albedo_lu = lu["albedo"]
            green_frac = lu["green_fraction"]
            water_frac = lu["water_fraction"]
            forest_frac = lu.get("forest_fraction", 0.0)
            farmland_frac = lu.get("farmland_fraction", 0.0)

            bldg_cov = bm["building_coverage"]
            avg_height = bm["avg_building_height"]
            road_cov = bm["road_coverage"]
            canopy_frac = bm["tree_canopy_fraction"]
            svf = bm["sky_view_factor"]

            # ── Albedo refinement ─────────────────────────────────────────
            avg_levels = max(1, int(avg_height / 3.0))
            bldg_albedo = _get_bldg_albedo("residential", avg_levels)
            if bldg_cov > 0:
                albedo = bldg_cov * bldg_albedo + (1.0 - bldg_cov) * albedo_lu
            else:
                albedo = albedo_lu

            # ── Impervious fraction (data-driven, no blending) ────────────
            imp_frac_detail = bldg_cov + road_cov * 0.95
            if imp_frac_detail > 0.01:
                imp_frac = min(imp_frac_detail, 0.98)
            else:
                imp_frac = imp_frac_lu
            imp_frac = max(0.02, min(imp_frac, 0.98))

            # ── Building density factor ───────────────────────────────────
            height_factor = min(avg_height / 15.0, 2.0)
            bldg_factor = bldg_cov * height_factor

            # ── Differentiated green cooling ──────────────────────────────
            # Forest cools more than grassland; farmland cools less
            meadow_grass_frac = max(0.0, green_frac - forest_frac)
            green_cooling = (
                gamma * forest_frac * forest_factor  # forest: stronger
                + gamma * meadow_grass_frac           # grass/meadow: normal
                + gamma * farmland_frac * 0.5         # farmland: weaker
            )
            water_cooling = delta_w * water_frac
            tree_cooling = tree_cool * canopy_frac * 10.0

            # ── Ventilation cooling ───────────────────────────────────────
            vent_score = ventilation_scores[i]
            # Only applies meaningfully to built-up cells
            vent_cooling = vent_cool_max * vent_score * min(imp_frac * 2.0, 1.0)

            # ── Daytime UHI ───────────────────────────────────────────────
            uhi_canyon = epsilon * (1.0 - svf) * height_factor
            uhi_base = alpha * (1.0 - albedo) * imp_frac + beta * bldg_factor
            uhi_delta = max(0.0,
                            uhi_base
                            - green_cooling
                            - water_cooling
                            - tree_cooling
                            - vent_cooling
                            + uhi_canyon)

            temp_estimate = ref_temp + uhi_delta
            heat_stress = min(10.0, uhi_delta * 1.5)

            # ── Night-time UHI ────────────────────────────────────────────
            # At night, thermal mass of buildings retains heat; green areas
            # cool down faster. Canyon effect is stronger at night.
            night_thermal_retention = (
                thermal_mass * bldg_cov * (1.0 + height_factor)
                + 0.3 * imp_frac   # asphalt/concrete retains heat
            )
            night_green_cooling = (
                green_cooling * 0.5  # green cools at night but weaker
                + water_cooling * 0.8  # water has high heat capacity, cools well
            )
            night_canyon = epsilon * (1.0 - svf) * height_factor * 1.3  # stronger at night

            night_uhi_delta = max(0.0,
                                  night_thermal_retention
                                  - night_green_cooling
                                  + night_canyon * 0.5)
            night_temp_estimate = night_ref_temp + night_uhi_delta

            # Tropical night risk: probability that Tmin >= 20°C
            # Based on: regional baseline + night UHI
            if night_temp_estimate >= 20.0:
                tropical_risk = min(1.0, 0.5 + (night_temp_estimate - 20.0) * 0.15)
            elif night_temp_estimate >= 18.0:
                tropical_risk = (night_temp_estimate - 18.0) / 4.0  # ramp 18→20°C = 0→0.5
            else:
                tropical_risk = 0.0

            # ── Population & Vulnerability ────────────────────────────────
            cell_area_km2 = (cell_size_m / 1000.0) ** 2
            pop_factor = 0.3 + bldg_cov * 2.0 + (1.0 - green_frac - water_frac) * 0.3
            affected_pop = pop_density * urbanity * cell_area_km2 * pop_factor

            # Vulnerability index: heat stress × population density × night retention
            # Scale to 0–10
            pop_density_local = affected_pop / cell_area_km2 if cell_area_km2 > 0 else 0
            pop_norm = min(pop_density_local / 500.0, 1.0)  # normalize: 500/km² → 1.0
            night_norm = min(night_uhi_delta / 3.0, 1.0)    # normalize: 3K night UHI → 1.0
            vulnerability = min(10.0,
                                heat_stress * 0.4
                                + pop_norm * 10.0 * 0.3
                                + night_norm * 10.0 * 0.3)

            rs = min(10.0, vulnerability if vulnerability > 0 else heat_stress)
            results.append(CellResult(
                grid_cell_id=cell["id"],
                indicators={
                    "temperature_estimate": round(temp_estimate, 1),
                    "uhi_delta": round(uhi_delta, 2),
                    "heat_stress_index": round(heat_stress, 1),
                    "impervious_fraction": round(imp_frac, 3),
                    "estimated_affected_pop": round(affected_pop, 0),
                    "green_fraction": round(green_frac, 3),
                    "water_fraction": round(water_frac, 3),
                    "albedo": round(albedo, 4),
                    "building_coverage": round(bldg_cov, 4),
                    "avg_building_height": round(avg_height, 1),
                    "tree_canopy_fraction": round(canopy_frac, 4),
                    "sky_view_factor": round(svf, 3),
                    # Level 4 specifics
                    "night_uhi_delta": round(night_uhi_delta, 2),
                    "night_temp_estimate": round(night_temp_estimate, 1),
                    "ventilation_cooling": round(vent_cooling, 2),
                    "vulnerability_index": round(vulnerability, 1),
                    "tropical_night_risk": round(tropical_risk, 3),
                    "forest_fraction": round(forest_frac, 3),
                    "farmland_fraction": round(farmland_frac, 3),
                    "risk_score": round(rs, 2),
                },
                risk_score=round(rs, 2),
            ))

            if progress_callback and total > 0:
                pct = 50.0 + (i + 1) / total * 50.0
                if i + 1 == total:
                    progress_callback(pct, "Speichere Ergebnisse")
                elif i == total // 4:
                    progress_callback(pct, "Berechne differenzierte Grünkühlung")
                elif i == total // 2:
                    progress_callback(pct, "Berechne Nacht-UHI & Tropennacht-Risiko")
                elif i == int(total * 0.75):
                    progress_callback(pct, "Berechne Vulnerabilitätsindex")
                else:
                    progress_callback(pct)

        return results

    def get_projection_factors(self, bundesland: str) -> dict:
        """Scale heat risk by DWD hot-days projection trend."""
        from app.services.climate.dwd_data import (
            FALLBACK_CLIMATE,
            _HOT_DAYS_PROJECTION_RCP45,
            _HOT_DAYS_PROJECTION_RCP85,
        )
        base_hot = FALLBACK_CLIMATE.get(bundesland, {}).get("hot_days_avg", 10.5)
        factors: dict[str, dict[int, float]] = {"rcp45": {}, "rcp85": {}}
        for y in range(2025, 2066):
            rf45 = FALLBACK_CLIMATE.get(bundesland, {}).get("hot_days_avg", 10.5) / 10.5
            rf85 = rf45
            proj45 = _HOT_DAYS_PROJECTION_RCP45.get(y, 12.0) * rf45
            proj85 = _HOT_DAYS_PROJECTION_RCP85.get(y, 12.0) * rf85
            factors["rcp45"][y] = proj45 / base_hot if base_hot > 0 else 1.0
            factors["rcp85"][y] = proj85 / base_hot if base_hot > 0 else 1.0
        return factors


# Self-register on import
_instance = HeatAssessor()
registry.register(_instance)
