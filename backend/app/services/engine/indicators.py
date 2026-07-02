"""Berechnet pro Zelle alle klimatischen Einflüsse (Hazards), räumlichen Expositionen und
Sensitivitäten in ABSOLUTEN Einheiten aus den Rohgrößen (``inputs.py``).

Wo kein lokaler räumlicher Proxy existiert (catalog: ``spatial=False``), wird ein
regionaler/nationaler Konstantwert gesetzt. Alle Annahmen sind im Handbuch und in
den (i)-Tooltips dokumentiert.
"""

from __future__ import annotations

from app.data import catalog


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def _building_stability(ci: dict) -> float:
    bldg_cov = ci.get("bldg_cov", 0.0)
    avg_h = ci.get("avg_height", 0.0)
    base = 50.0 + bldg_cov * 20.0 + (10.0 if avg_h > 18 else 0.0)
    age = ci.get("building_age_mean")
    if age is not None:
        base += min(30.0, max(0.0, (2024.0 - float(age)) / 100.0 * 30.0))
    return round(_clamp(base, 0, 100), 1)


def _income_resilience(ci: dict) -> float:
    """Hoher Index = geringe soziale Resilienz (invers)."""
    scores: list[float] = []
    rent = ci.get("net_cold_rent")
    if rent is not None:
        scores.append(_clamp(float(rent) / 18.0 * 100.0, 0, 100))
    owner = ci.get("owner_share")
    if owner is not None:
        scores.append(_clamp(100.0 - float(owner), 0, 100))
    la = ci.get("living_area_per_person")
    if la is not None:
        scores.append(_clamp(100.0 - min(float(la) / 60.0 * 100.0, 100.0), 0, 100))
    if not scores:
        return 45.0
    return round(sum(scores) / len(scores), 1)


def _healthcare_access(ci: dict) -> float:
    """Inverser Zugangsindex: geringere Erreichbarkeit = höhere Verwundbarkeit."""
    score = float(ci.get("healthcare_access_score") or 0)
    return round(_clamp(100.0 * (1.0 - score), 0, 100), 1)


def compute_cell_hev(ci: dict, regional: dict) -> dict:
    """Gibt {"hazards":{}, "exposures":{}, "vulnerabilities":{}} für eine Zelle."""
    area_ha = ci["area_m2"] / 10_000.0
    area_km2 = ci["area_m2"] / 1_000_000.0
    pop = ci.get("pop", 0.0)
    pop_density = pop / area_km2 if area_km2 > 0 else 0.0

    imp = ci["imp_frac"]
    green = ci["green_frac"]
    water = ci["water_frac"]
    forest = ci["forest_frac"]
    farmland = ci["farmland_frac"]
    bldg_cov = ci["bldg_cov"]
    bldg_count = ci.get("bldg_count", 0)
    avg_h = ci["avg_height"]
    road_cov = ci["road_cov"]
    uhi = ci["uhi_delta"]
    vent = ci["vent_score"]
    glacier_frac = ci.get("glacier_frac", 0.0)
    snow_elev = ci.get("snow_elevation_factor", 0.2)
    depression = ci.get("depression_factor", ci["depression_proxy"])
    slope = ci.get("slope_factor", ci["slope_proxy"])
    water_adj = ci.get("water_adj", 0.0)
    water_prox = ci.get("water_prox", water_adj)
    twi_norm = ci.get("twi_norm", depression)
    elev_m = float(ci.get("mean_elevation_m", 0.0))

    coastal = regional["is_coastal"]
    dry = regional["dry_index"]
    share_old = float(ci.get("share_over_65") if ci.get("share_over_65") is not None
                    else regional["demographics"].get("share_over_65", 22.0))
    share_young = float(ci.get("share_under_18") if ci.get("share_under_18") is not None
                      else regional["demographics"].get("share_under_18", 18.0))
    share_vuln = float(ci.get("share_vulnerable") if ci.get("share_vulnerable") is not None
                       else min(100.0, share_old + share_young))

    industrial = max(0.0, imp - bldg_cov - road_cov)  # grober Industrie/Gewerbe-Proxy

    # ── Hazards (absolute Einheit) ─────────────────────────────────────────────
    H = {
        "MEAN_TEMPERATURE_RISE": round(regional["mean_temp_rise"] + uhi * 0.08, 2),
        "SEA_LEVEL_RISE": regional["sea_level_rise"] if coastal else 0.0,
        "OCEAN_WARMING": 1.2 if coastal else 0.0,
        "OCEAN_ACIDIFICATION": 0.1 if coastal else 0.0,
        "GLACIER_SNOW_LOSS": round(
            regional["glacier_loss_rate"] * glacier_frac
            + regional["snow_decline_rate_pct"]
            * (0.25 + 0.75 * snow_elev)
            * min(1.0, regional.get("snow_days", 20) / 45.0),
            3,
        ),
        "PERMAFROST_THAW": 0.0,
        "SOIL_MOISTURE_DECLINE": round(regional["soil_moisture_decline"] * (0.5 + 0.6 * (farmland + green)), 1),
        "HEAT_WAVE": round(_clamp(regional["hot_days"] + uhi * 1.5, 0, 40), 1),
        "COLD_EXTREME": round(regional["frost_days"] * (1.0 - 0.3 * min(uhi / 5.0, 1.0)), 1),
        "HEAVY_RAIN_FLOOD": round(
            _clamp(regional["heavy_rain_index"] * (0.4 + imp) * (0.5 + 0.5 * twi_norm) * (0.6 + depression), 0, 100), 1
        ),
        "DROUGHT": round(_clamp(regional["drought_days"] * (0.6 + 0.7 * (farmland + green)), 0, 60), 1),
        "TROPICAL_CYCLONE": 0.05,
        "EXTRATROPICAL_STORM": round(regional["storm_days"] * (0.8 + 0.5 * vent), 1),
        "STORM_SURGE": 2.0 if coastal else 0.0,
        "WILDFIRE": round(_clamp(forest * 100.0 * (0.4 + dry), 0, 100), 1),
        "LANDSLIDE": round(_clamp(slope * 100.0 * (regional["heavy_rain_index"] / 100.0), 0, 100), 1),
        "SALTWATER_INTRUSION": 0.3 if coastal else 0.0,
        "COASTAL_EROSION": 1.0 if coastal else 0.0,
        "SOIL_SALINIZATION": round(min(1.0, (
            (0.4 if coastal else 0.05)
            * (0.35 + 0.65 * depression)
            * (0.45 + 0.55 * farmland)
            * (0.55 + 0.45 * dry)
            * (
                (0.5 + 0.5 * max(water_prox, water_adj)) if coastal
                else (0.55 + 0.45 * max(0.0, min(1.0, 1.0 - elev_m / 80.0)))
            )
        )), 3),
        "SURFACE_WATER_HEATING": round(regional["surface_water_heating"] * (0.5 + water), 2),
        "LOW_FLOW_NIEDRIGWASSER": round(
            _clamp(regional["low_flow_days"] * (0.6 + 0.4 * dry) * (1.0 + 0.3 * water_prox), 0, 60), 1
        ),
        "CASCADE_EVENT": 0.3,
    }
    # Compound = max der normalisierten Bestandteile (model_parameters: max_of_constituent)
    comp = max(
        catalog.normalize_value("HEAT_WAVE", H["HEAT_WAVE"]),
        catalog.normalize_value("DROUGHT", H["DROUGHT"]),
        catalog.normalize_value("HEAVY_RAIN_FLOOD", H["HEAVY_RAIN_FLOOD"]),
    )
    H["COMPOUND_EVENT"] = round(comp, 3)

    # ── Exposures (absolute Einheit) ───────────────────────────────────────────
    E = {
        "POPULATION_DENSITY": round(pop_density, 1),
        "AGE_STRUCTURE": round(share_old + share_young, 1),
        "OUTDOOR_THERMAL_EXPOSURE": round(2.0 + 3.0 * green, 2),
        "VULNERABLE_GROUPS_POPULATION": round(pop * share_vuln / 100.0, 1),
        "BUILDING_STOCK": round(bldg_cov * ci["area_m2"], 0),
        "BUILDING_USE_TYPES": float(bldg_count),
        "LOCATION_HAZARD_ZONES": round(area_ha * bldg_cov * max(depression, min(uhi / 6.0, 1.0)), 4),
        "ENERGY_INFRASTRUCTURE": round(float(ci.get("energy_infra_count") or 0), 2),
        "WATER_WASTEWATER_INFRA": round(float(ci.get("water_wastewater_count") or 0), 2),
        "TRANSPORT_HUBS": round(road_cov * 18.0, 2),
        "COMMUNICATION_INFRA": round(float(ci.get("communication_count") or 0), 2),
        "HEALTHCARE_INFRASTRUCTURE": round(
            float(ci.get("healthcare_access_score") or 0) * 100.0, 1,
        ),
        "INDUSTRIAL_COMMERCIAL_AREAS": round(area_ha * industrial, 4),
        "AGRICULTURAL_LAND": round(area_ha * farmland, 4),
        "SUPPLY_CHAIN_NODES": round(industrial * 6.0 + bldg_count * 0.004, 2),
        "FOREST_AREA": round(area_ha * forest, 4),
        "BIODIVERSITY_HOTSPOTS": round(area_ha * (forest + water) * 0.5, 4),
        "EROSION_PRONE_SOILS": round(area_ha * farmland * slope, 4),
        "COASTAL_RIPARIAN_ZONES": round(area_ha * max(water_adj, water_prox) * (0.5 + 0.5 * twi_norm), 4),
        "FLOODPLAINS": round(area_ha * depression * max(water_prox, 0.3 if water_adj > 0 else 0.1), 4),
        "COASTAL_STORM_SURGE_EXPOSURE": round(area_ha * bldg_cov, 4) if coastal else 0.0,
        "GROUNDWATER_DEPENDENT_ECOSYSTEMS": round(area_ha * (forest + green) * (0.3 + water_adj), 4),
        "FISHERIES_AQUACULTURE_AREAS": round(water * 5.0, 2),
        "FISH_SPAWNING_HABITATS": round(area_ha * max(water, water_prox * 0.5), 4),
    }

    # ── Vulnerabilities (Index 0..100 bzw. natürliche Einheit) ─────────────────
    V = {
        "BUILDING_STABILITY": _building_stability(ci),
        "CRITICAL_INFRA_CONDITION": 50.0,
        "MATERIAL_HEAT_SENSITIVITY": round(_clamp(imp * 100.0, 0, 100), 1),
        "VULNERABLE_GROUPS_SHARE": round(share_vuln, 1),
        "INCOME_SOCIAL_RESILIENCE": _income_resilience(ci),
        "HEALTHCARE_ACCESS": _healthcare_access(ci),
        "WILDFIRE_SUSCEPTIBILITY": round(_clamp(forest * 100.0 * (0.5 + dry / 2.0), 0, 100), 1),
        "BIODIVERSITY_RESILIENCE": round(_clamp(100.0 - (forest + green) * 100.0 * 0.6, 0, 100), 1),
        "SOIL_SENSITIVITY": round(_clamp(slope * 60.0 + farmland * 40.0, 0, 100), 1),
        "SINGLE_SITE_DEPENDENCY": round(_clamp(industrial * 200.0, 0, 100), 1),
        "SUPPLY_CHAIN_DEPENDENCY": 50.0,
        "FINANCIAL_ADAPTATION_CAPACITY": 45.0,
        "INFRA_CRITICALITY": round(_clamp(bldg_count * 0.3, 0, 100), 1),
        "REDUNDANCY_BACKUP": 50.0,
        "INFRA_DEPENDENCY_CHAIN": 50.0,
        "HEAT_SENSITIVITY": round(_clamp(share_vuln + uhi * 6.0 + (1.0 - green) * 20.0, 0, 100), 1),
        "AIR_QUALITY_RISK": round(_clamp(imp * 60.0 + road_cov * 200.0, 0, 100), 1),
        "DISEASE_VECTOR_SUSCEPTIBILITY": round(_clamp(water * 100.0 * (regional["mean_temp"] / 12.0), 0, 100), 1),
        "GROUNDWATER_DEPENDENCY": round(_clamp((farmland + green) * 50.0, 0, 100), 1),
        "WATER_STRESS_INDEX": round(_clamp(imp * 40.0 + min(pop_density / 4000.0, 1.0) * 40.0 + dry * 20.0, 0, 100), 1),
        "IRRIGATION_DEPENDENCY": round(_clamp(farmland * 100.0 * (0.5 + dry / 2.0), 0, 100), 1),
        "EROSION_SUSCEPTIBILITY": round(_clamp(slope * 100.0 * (1.0 - green), 0, 100), 1),
        "LEVEE_CONDITION": 50.0 if coastal else 30.0,
        "SALTWATER_INTRUSION_RISK": 40.0 if coastal else 10.0,
        "SEALING_DEGREE": round(_clamp(imp * 100.0, 0, 100), 1),
        "UHI_INTENSITY": round(uhi, 2),
        "GREEN_SPACE_SHARE": round(_clamp(100.0 - green * 100.0, 0, 100), 1),
        "EARLY_WARNING_SYSTEMS": 40.0,
        "EMERGENCY_MANAGEMENT": 40.0,
        "PLANNING_IMPLEMENTATION_CAPACITY": 45.0,
        "FISHERIES_TEMPERATURE_SENSITIVITY": round(_clamp(water * 100.0 * (regional["surface_water_heating"] / 3.0), 0, 100), 1),
        "AQUACULTURE_TECHNICAL_VULNERABILITY": 50.0,
        "FISHERIES_MANAGEMENT_CAPACITY": 45.0,
    }

    # Sicherstellen, dass jeder Katalog-Code vorhanden ist (Default 0)
    for h in catalog.HAZARDS:
        H.setdefault(h["code"], 0.0)
    for e in catalog.EXPOSURES:
        E.setdefault(e["code"], 0.0)
    for v in catalog.VULNERABILITIES:
        V.setdefault(v["code"], 0.0)

    return {"hazards": H, "exposures": E, "vulnerabilities": V}
