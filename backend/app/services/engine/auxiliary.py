"""Befüllt ``cell_assessments.data['auxiliary']`` — alle Sonstige-Layer-Werte."""

from __future__ import annotations

from typing import Any

from app.data import catalog


def _computed_industrial(ci: dict) -> float:
    return max(0.0, ci.get("imp_frac", 0.0) - ci.get("bldg_cov", 0.0) - ci.get("road_cov", 0.0))


def _norm_index(value: float | None, lo: float, hi: float, invert: bool = False) -> float | None:
    if value is None:
        return None
    if hi <= lo:
        return 50.0
    t = max(0.0, min(1.0, (value - lo) / (hi - lo)))
    if invert:
        t = 1.0 - t
    return round(t * 100.0, 1)


def _age_band(ci: dict, band: str) -> float | None:
    bands = ci.get("pop_age_bands")
    if not isinstance(bands, dict):
        return None
    v = bands.get(band)
    return round(float(v), 2) if v is not None else None


def _cell_temp(ci: dict, regional: dict) -> float | None:
    t = ci.get("summer_temp_cell")
    if t is not None:
        return float(t)
    base = regional.get("summer_temp_mean")
    return float(base) + float(ci.get("uhi_delta_mean") or 0.0) if base is not None else None


def _heat_excess_weeks(ci: dict, regional: dict) -> float | None:
    """Übertemperatur-Wochen über der regionalen Wirkschwelle (K·Wochen)."""
    from app.services.engine.impact import health
    t = _cell_temp(ci, regional)
    if t is None:
        return None
    region = health.region_for(regional.get("bundesland"))
    return round(health.heat_excess_weeks(
        t, region, health.REGION_THRESHOLD[region]), 3)


def _heat_relative_risk(ci: dict, regional: dict) -> float | None:
    """Bevölkerungsgewichtetes relatives Sterberisiko der Zelle (Faktor ≥ 1)."""
    from math import exp

    from app.services.engine.impact import health
    t = _cell_temp(ci, regional)
    if t is None:
        return None
    region = health.region_for(regional.get("bundesland"))
    thr = health.REGION_THRESHOLD[region]
    beta85 = health.REGION_BETA_85P[region]
    temps = health.weekly_temperatures(t, region)

    bands = ci.get("pop_age_bands")
    if not isinstance(bands, dict) or not sum(float(v or 0.0) for v in bands.values()):
        bands = {b: 1.0 for b in health.AGE_BANDS}
    total = sum(float(bands.get(b) or 0.0) for b in health.AGE_BANDS)
    if total <= 0:
        return None

    acc = 0.0
    for band in health.AGE_BANDS:
        beta = beta85 * health.AGE_BETA_FACTOR[band]
        rr = sum(exp(beta * max(0.0, x - thr)) for x in temps) / len(temps)
        acc += float(bands.get(band) or 0.0) * rr
    return round(acc / total, 4)


def _flood_regime(ci: dict) -> float:
    """Sturzflut-Anteil aus Hangneigung und Senkenlage (0 = Aue, 1 = Sturzflut)."""
    slope = float(ci.get("slope_factor", ci.get("slope_proxy", 0.0)) or 0.0)
    depression = float(ci.get("depression_factor", ci.get("depression_proxy", 0.0)) or 0.0)
    return round(max(0.0, min(1.0, slope * (0.5 + 0.5 * depression))), 4)


def build_auxiliary(ci: dict, regional: dict) -> dict[str, float | None]:
    """Map cell inputs + regional context to AUXILIARY catalog codes."""
    pop = float(ci.get("pop") or 0.0)
    share_o = ci.get("share_over_65")
    share_u = ci.get("share_under_18")

    aux: dict[str, Any] = {
        # Zensus
        "POPULATION_COUNT": round(pop, 2) if pop else 0.0,
        "SHARE_OVER_65": share_o,
        "SHARE_UNDER_18": share_u,
        "POPULATION_OVER_65": round(ci.get("pop_over_65") or 0.0, 2),
        "POPULATION_UNDER_18": round(ci.get("pop_under_18") or 0.0, 2),
        "LIVING_AREA_PER_PERSON": ci.get("living_area_per_person"),
        "NET_COLD_RENT": ci.get("net_cold_rent"),
        "OWNER_SHARE": ci.get("owner_share"),
        "BUILDING_COUNT_ZENSUS": ci.get("building_count_zensus"),
        "BUILDING_AGE_MEAN": ci.get("building_age_mean"),
        # OSM
        "IMPERVIOUS_FRACTION": round(ci.get("imp_frac", 0.0), 4),
        "GREEN_FRACTION": round(ci.get("green_frac", 0.0), 4),
        "WATER_FRACTION": round(ci.get("water_frac", 0.0), 4),
        "FOREST_FRACTION": round(ci.get("forest_frac", 0.0), 4),
        "FARMLAND_FRACTION": round(ci.get("farmland_frac", 0.0), 4),
        "BUILDING_COVERAGE": round(ci.get("bldg_cov", 0.0), 4),
        "BUILDING_COUNT": float(ci.get("bldg_count") or 0),
        "ENERGY_INFRA_COUNT": float(ci.get("energy_infra_count") or 0),
        "WATER_WASTEWATER_COUNT": float(ci.get("water_wastewater_count") or 0),
        "COMMUNICATION_INFRA_COUNT": float(ci.get("communication_count") or 0),
        "HOSPITAL_DISTANCE_M": float(ci.get("dist_hospital_m") or 0),
        "DOCTOR_DISTANCE_M": float(ci.get("dist_doctor_m") or 0),
        "PHARMACY_DISTANCE_M": float(ci.get("dist_pharmacy_m") or 0),
        "HEALTHCARE_ACCESS_GRID": round(float(ci.get("healthcare_access_score") or 0) * 100.0, 1),
        "HEALTHCARE_INDEX_HOSPITAL": float(ci.get("healthcare_weight_hospital") or 0),
        "HEALTHCARE_INDEX_DOCTOR": float(ci.get("healthcare_weight_doctor") or 0),
        "HEALTHCARE_INDEX_PHARMACY": float(ci.get("healthcare_weight_pharmacy") or 0),
        "HEALTHCARE_ACCESS_SCORE": float(ci.get("healthcare_access_score") or 0),
        "HEALTHCARE_ACCESS_INDEX": round(
            100.0 * (1.0 - float(ci.get("healthcare_access_score") or 0)), 1,
        ),
        "AVG_BUILDING_HEIGHT": round(ci.get("avg_height", 0.0), 2),
        "ROAD_COVERAGE": round(ci.get("road_cov", 0.0), 4),
        "TREE_CANOPY": round(ci.get("canopy_frac", 0.0), 4),
        "SKY_VIEW_FACTOR": round(ci.get("svf", 0.0), 4),
        "SURFACE_ALBEDO": round(ci.get("albedo", 0.0), 4),
        "INDUSTRIAL_FRACTION": round(_computed_industrial(ci), 4),
        "VENTILATION_SCORE": round(ci.get("vent_score", 0.0), 4),
        # Terrain
        "MEAN_ELEVATION": ci.get("mean_elevation_m"),
        "SLOPE_DEGREES": ci.get("slope_deg"),
        "SINK_DEPTH": ci.get("sink_depth_m"),
        "TWI": ci.get("twi"),
        "TWI_NORMALIZED": ci.get("twi_norm"),
        "DEPRESSION_FACTOR": ci.get("depression_factor"),
        "SLOPE_FACTOR": ci.get("slope_factor"),
        "FLOW_ACCUMULATION": ci.get("flow_accum"),
        # Water
        "WATER_DISTANCE": ci.get("water_dist_m"),
        "WATER_PROXIMITY": ci.get("water_prox"),
        "WATER_ADJACENCY": ci.get("water_adj"),
        # Regional (DWD) — same value per kommune, stored per cell for export
        "HOT_DAYS": regional.get("hot_days"),
        "FROST_DAYS": regional.get("frost_days"),
        "MEAN_ANNUAL_TEMP": regional.get("mean_temp"),
        "DROUGHT_DAYS": regional.get("drought_days"),
        "DRYNESS_INDEX": regional.get("dry_index"),
        "STORM_DAYS": regional.get("storm_days"),
        "HEAVY_RAIN_INDEX": regional.get("heavy_rain_index"),
        "TEMPERATURE_RISE": regional.get("mean_temp_rise"),
        "SOIL_MOISTURE_DECLINE": regional.get("soil_moisture_decline"),
        "LOW_FLOW_DAYS": regional.get("low_flow_days"),
        "SURFACE_WATER_HEATING_REGIONAL": regional.get("surface_water_heating"),
        "SEA_LEVEL_RISE": regional.get("sea_level_rise"),
        # Hitzemodell: die Zwischenschritte der Sterbefall-Rechnung, damit die
        # Kette Temperatur → Wärmeinsel → Zelltemperatur → Übertemperatur →
        # Altersbänder als eigene Karten prüfbar ist.
        "SUMMER_MEAN_TEMP": ci.get("summer_temp_raster"),
        "SUMMER_NIGHT_TEMP": ci.get("summer_night_temp"),
        "UHI_DELTA_DAY": ci.get("uhi_delta"),
        "UHI_DELTA_MEAN": ci.get("uhi_delta_mean"),
        "CELL_SUMMER_TEMP": ci.get("summer_temp_cell"),
        "HEAT_EXCESS_WEEKS": _heat_excess_weeks(ci, regional),
        "HEAT_RELATIVE_RISK": _heat_relative_risk(ci, regional),
        "FLOOD_REGIME": _flood_regime(ci),
        "POPULATION_65_74": _age_band(ci, "a65_74"),
        "POPULATION_75_84": _age_band(ci, "a75_84"),
        "POPULATION_85_PLUS": _age_band(ci, "a85p"),
        # None = Kommune ohne OSM-Pflegeeinrichtungen (v_vers rechnet dann mit
        # dem Bundesmittel q̄ — Faktor 1; Methodik #95 §3.6).
        "CARE_HOME_SHARE_85P": ci.get("share_care_home_85p"),
    }

    for code in catalog.AUXILIARY_BY_CODE:
        if code not in aux:
            aux[code] = None

    rounded: dict[str, float | None] = {}
    for k, v in aux.items():
        if v is None:
            rounded[k] = None
        elif isinstance(v, float):
            rounded[k] = round(v, 4)
        else:
            rounded[k] = float(v)
    return rounded
