"""Formel- und Herkunftsregister für Karten-Tooltips.

Jeder H/E/V-Indikator und jedes Risiko hat ein Rezept mit Formeltext und
Eingabe-Deskriptoren. Pro Zelle werden die aufgelösten Eingabewerte an die
Frontend-Tooltip-Logik übergeben.
"""

from __future__ import annotations

from typing import Any

from app.data import catalog

EXTERN = "extern"
PARAM = "param"
COMPUTED = "computed"


def _i(
    key: str,
    label: str,
    prov: str,
    unit: str = "",
    source: str = "cell",
    value: Any = None,
    coastal_only: bool = False,
    coastal_split: tuple[Any, Any] | None = None,
) -> dict:
    d: dict = {
        "key": key,
        "label": label,
        "prov": prov,
        "unit": unit,
        "source": source,
        "value": value,
    }
    if coastal_only:
        d["coastal_only"] = True
    if coastal_split is not None:
        d["coastal_split"] = coastal_split
    return d


def _computed_industrial(ci: dict) -> float:
    return max(0.0, ci.get("imp_frac", 0.0) - ci.get("bldg_cov", 0.0) - ci.get("road_cov", 0.0))


def _computed_area_ha(ci: dict) -> float:
    return ci.get("area_m2", 10_000.0) / 10_000.0


def _computed_area_km2(ci: dict) -> float:
    return ci.get("area_m2", 10_000.0) / 1_000_000.0


def _computed_pop_density(ci: dict) -> float:
    area_km2 = _computed_area_km2(ci)
    return ci.get("pop", 0.0) / area_km2 if area_km2 > 0 else 0.0


_COMPUTED_RESOLVERS: dict[str, Any] = {
    "industrial": _computed_industrial,
    "area_ha": _computed_area_ha,
    "area_km2": _computed_area_km2,
    "pop_density": _computed_pop_density,
}


# ── Detaillierte Rezepte (abgeleitet aus indicators.py) ───────────────────────

DETAILED: dict[str, dict] = {
    # Hazards
    "MEAN_TEMPERATURE_RISE": {
        "formula": "Regionaler Anstieg + 0,08 · UHI-ΔT",
        "inputs": [
            _i("mean_temp_rise", "Temperaturanstieg (DWD, Bundesland)", EXTERN, "°C", "regional"),
            _i("uhi_delta", "UHI-ΔT (OSM-Modell)", COMPUTED, "K", "cell"),
        ],
    },
    "SEA_LEVEL_RISE": {
        "formula": "Regionaler Konstantwert (nur Küste)",
        "inputs": [_i("sea_level_rise", "Meeresspiegelanstieg (BSH)", EXTERN, "mm/Jahr", "regional")],
    },
    "OCEAN_WARMING": {
        "formula": "Konstantwert (nur Küste)",
        "inputs": [_i("__const", "Ozeanerwärmung", PARAM, "°C", "const", 1.2, coastal_only=True)],
    },
    "OCEAN_ACIDIFICATION": {
        "formula": "Konstantwert (nur Küste)",
        "inputs": [_i("__const", "Ozeanversauerung", PARAM, "ΔpH", "const", 0.1, coastal_only=True)],
    },
    "GLACIER_SNOW_LOSS": {
        "formula": "0,5·Gletscher + Schneerückgang(DWD) · Höhe · Schneetage",
        "inputs": [
            _i("glacier_loss_rate", "Gletscherschwund (Parameter)", PARAM, "%/Jahr", "regional"),
            _i("glacier_frac", "Gletscheranteil (OSM natural=glacier)", EXTERN, "", "cell"),
            _i("snow_decline_rate_pct", "Schneedecken-Rückgang (DWD-Trend)", EXTERN, "%/Jahr", "regional"),
            _i("snow_days", "Schneedeckentage (DWD, regional)", EXTERN, "Tage", "regional"),
            _i("snow_elevation_factor", "Höhenmodulation (DEM)", COMPUTED, "", "cell"),
        ],
    },
    "PERMAFROST_THAW": {
        "formula": "Konstantwert (DE: nur alpine Hochlagen)",
        "inputs": [_i("__const", "Permafrosttauung", PARAM, "Index", "const", 0.0)],
    },
    "SOIL_MOISTURE_DECLINE": {
        "formula": "clamp(Regional · (0,5 + 0,6·(Acker+Grün)) ; 0…80)",
        "inputs": [
            _i("soil_moisture_decline", "Bodenfeuchte-Rückgang (regional)", EXTERN, "mm", "regional"),
            _i("farmland_frac", "Ackeranteil (OSM)", EXTERN, "", "cell"),
            _i("green_frac", "Grünanteil (OSM)", EXTERN, "", "cell"),
        ],
    },
    "HEAT_WAVE": {
        "formula": "clamp(Heiße Tage + 1,5·UHI-ΔT ; 0…40)",
        "inputs": [
            _i("hot_days", "Heiße Tage/Jahr (DWD)", EXTERN, "Tage", "cell"),
            _i("uhi_delta", "UHI-ΔT (OSM-Modell)", COMPUTED, "K", "cell"),
            _i("uhi_weight", "UHI-Gewichtung", PARAM, "×", "const", 1.5),
        ],
    },
    "COLD_EXTREME": {
        "formula": "Frosttage · (1 − 0,3·min(UHI/5 ; 1))",
        "inputs": [
            _i("frost_days", "Frosttage (DWD)", EXTERN, "Tage", "regional"),
            _i("uhi_delta", "UHI-ΔT (OSM-Modell)", COMPUTED, "K", "cell"),
        ],
    },
    "HEAVY_RAIN_FLOOD": {
        "formula": "clamp(Starkregen · (0,4+Versieg.) · TWI · Senke ; 0…100)",
        "inputs": [
            _i("heavy_rain_index", "Starkregenindex (DWD)", EXTERN, "Index", "regional"),
            _i("imp_frac", "Versiegelungsgrad (OSM)", EXTERN, "", "cell"),
            _i("twi_norm", "TWI normiert (Terrarium-DEM)", EXTERN, "", "cell"),
            _i("depression_factor", "Senkentiefe (DEM)", COMPUTED, "", "cell"),
        ],
    },
    "DROUGHT": {
        "formula": "clamp(Trockentage · (0,6 + 0,7·(Acker+Grün)) ; 0…60)",
        "inputs": [
            _i("drought_days", "Trockentage (regional)", EXTERN, "Tage", "regional"),
            _i("farmland_frac", "Ackeranteil (OSM)", EXTERN, "", "cell"),
            _i("green_frac", "Grünanteil (OSM)", EXTERN, "", "cell"),
        ],
    },
    "TROPICAL_CYCLONE": {
        "formula": "Nationaler Konstantwert",
        "inputs": [_i("__const", "Tropische Wirbelstürme", PARAM, "Anzahl/Jahr", "const", 0.05)],
    },
    "EXTRATROPICAL_STORM": {
        "formula": "Sturmtage · (0,8 + 0,5·Frischluft-Anteil)",
        "inputs": [
            _i("storm_days", "Sturmtage (DWD)", EXTERN, "Anzahl", "regional"),
            _i("vent_score", "Frischluft-Anteil (8 Nachbarzellen, offen/grün)", COMPUTED, "", "cell"),
        ],
    },
    "STORM_SURGE": {
        "formula": "Konstantwert (nur Küste)",
        "inputs": [_i("__const", "Sturmflut", PARAM, "Anzahl/Jahr", "const", 2.0, coastal_only=True)],
    },
    "WILDFIRE": {
        "formula": "clamp(Waldanteil · 100 · (0,4 + Trockenheit) ; 0…100)",
        "inputs": [
            _i("forest_frac", "Waldanteil (OSM)", EXTERN, "", "cell"),
            _i("dry_index", "Trockenheitsindex (regional)", EXTERN, "", "regional"),
        ],
    },
    "LANDSLIDE": {
        "formula": "clamp(Hangneigung · 100 · Starkregen/100 ; 0…100)",
        "inputs": [
            _i("slope_factor", "Hangneigung (DEM)", EXTERN, "", "cell"),
            _i("heavy_rain_index", "Starkregenindex (DWD)", EXTERN, "Index", "regional"),
        ],
    },
    "SALTWATER_INTRUSION": {
        "formula": "Konstantwert (nur Küste)",
        "inputs": [_i("__const", "Salzwassereinbruch", PARAM, "Index", "const", 0.3, coastal_only=True)],
    },
    "COASTAL_EROSION": {
        "formula": "Konstantwert (nur Küste)",
        "inputs": [_i("__const", "Küstenerosion", PARAM, "m/Jahr", "const", 1.0, coastal_only=True)],
    },
    "SOIL_SALINIZATION": {
        "formula": "Basis(Küste/Binnen) · Senke · Acker · Trockenheit · (Gewässer|Höhe)",
        "inputs": [
            _i("__const", "Basis (Küste 0,4 / Binnen 0,05)", PARAM, "Index", "const", None, coastal_split=(0.4, 0.05)),
            _i("depression_factor", "Senkentiefe (DEM)", COMPUTED, "", "cell"),
            _i("farmland_frac", "Ackeranteil (OSM)", EXTERN, "", "cell"),
            _i("dry_index", "Trockenheitsindex (regional)", EXTERN, "", "regional"),
            _i("water_prox", "Gewässernähe (Küste, OSM)", EXTERN, "", "cell"),
            _i("mean_elevation_m", "Mittelhöhe (Binnen, DEM)", EXTERN, "m", "cell"),
        ],
    },
    "COMPOUND_EVENT": {
        "formula": "max(norm(Hitze), norm(Dürre), norm(Starkregen))",
        "inputs": [
            _i("heat_wave", "Hitzeextreme (berechnet)", COMPUTED, "Tage", "hev", "HEAT_WAVE"),
            _i("drought", "Dürren (berechnet)", COMPUTED, "Tage", "hev", "DROUGHT"),
            _i("heavy_rain", "Starkregen (berechnet)", COMPUTED, "Index", "hev", "HEAVY_RAIN_FLOOD"),
        ],
    },
    "CASCADE_EVENT": {
        "formula": "Qualitativer Konstantwert",
        "inputs": [_i("__const", "Kaskadeneffekte", PARAM, "Index", "const", 0.3)],
    },
    "SURFACE_WATER_HEATING": {
        "formula": "Regional · (0,5 + Wasseranteil)",
        "inputs": [
            _i("surface_water_heating", "Gewässererwärmung (DWD)", EXTERN, "°C", "regional"),
            _i("water_frac", "Wasseranteil (OSM)", EXTERN, "", "cell"),
        ],
    },
    "LOW_FLOW_NIEDRIGWASSER": {
        "formula": "clamp(Niedrigwasser · (0,6+0,4·Trocken) · (1+0,3·Gewässernähe) ; 0…60)",
        "inputs": [
            _i("low_flow_days", "Niedrigwasser-Tage (regional)", EXTERN, "Tage", "regional"),
            _i("dry_index", "Trockenheitsindex", EXTERN, "", "regional"),
            _i("water_prox", "Gewässernähe (OSM)", COMPUTED, "", "cell"),
        ],
    },
    # Exposures
    "POPULATION_DENSITY": {
        "formula": "Einwohner / Fläche (km²)",
        "inputs": [
            _i("pop", "Einwohner (Zensus 100m)", EXTERN, "Pers.", "cell"),
            _i("area_km2", "Zellfläche", COMPUTED, "km²", "computed", "area_km2"),
        ],
    },
    "AGE_STRUCTURE": {
        "formula": "Anteil ≥65 + Anteil <18 (Zensus je Zelle)",
        "inputs": [
            _i("share_over_65", "Anteil ≥65 Jahre (Zensus)", EXTERN, "%", "cell"),
            _i("share_under_18", "Anteil <18 Jahre (Zensus)", EXTERN, "%", "cell"),
        ],
    },
    "OUTDOOR_THERMAL_EXPOSURE": {
        "formula": "2 + 3 · Grünanteil",
        "inputs": [_i("green_frac", "Grünanteil (OSM)", EXTERN, "", "cell")],
    },
    "VULNERABLE_GROUPS_POPULATION": {
        "formula": "Einwohner · Anteil vulnerabler Gruppen / 100",
        "inputs": [
            _i("pop", "Einwohner (Zensus/OSM)", EXTERN, "Pers.", "cell"),
            _i("share_vulnerable", "Anteil vulnerable Gruppen (Zensus)", EXTERN, "%", "demo"),
        ],
    },
    "BUILDING_STOCK": {
        "formula": "Gebäudeanteil · Zellfläche",
        "inputs": [
            _i("bldg_cov", "Gebäudeanteil (OSM)", EXTERN, "", "cell"),
            _i("area_m2", "Zellfläche", COMPUTED, "m²", "cell"),
        ],
    },
    "BUILDING_USE_TYPES": {
        "formula": "Anzahl OSM-Gebäude",
        "inputs": [_i("bldg_count", "Gebäudeanzahl (OSM)", EXTERN, "Anzahl", "cell")],
    },
    "LOCATION_HAZARD_ZONES": {
        "formula": "Fläche(ha) · Gebäudeanteil · max(Senke, UHI/6)",
        "inputs": [
            _i("area_ha", "Zellfläche", COMPUTED, "ha", "computed", "area_ha"),
            _i("bldg_cov", "Gebäudeanteil (OSM)", EXTERN, "", "cell"),
            _i("depression_factor", "Senkentiefe (DEM)", COMPUTED, "", "cell"),
            _i("uhi_delta", "UHI-ΔT (OSM)", COMPUTED, "K", "cell"),
        ],
    },
    "ENERGY_INFRASTRUCTURE": {
        "formula": "Punkte(power=*) + 0,5 · Leitungssegmente(power=line/cable/…)",
        "inputs": [
            _i("energy_infra_count", "Energieinfrastruktur (OSM)", EXTERN, "Anzahl", "cell"),
        ],
    },
    "WATER_WASTEWATER_INFRA": {
        "formula": "Anzahl OSM Wasser-/Abwasseranlagen",
        "inputs": [
            _i("water_wastewater_count", "Wasser/Abwasser (OSM)", EXTERN, "Anzahl", "cell"),
        ],
    },
    "TRANSPORT_HUBS": {
        "formula": "Straßenanteil · 18",
        "inputs": [_i("road_cov", "Straßenanteil (OSM)", EXTERN, "", "cell")],
    },
    "COMMUNICATION_INFRA": {
        "formula": "Anzahl OSM Mobilfunk-/Kommunikationsmasten",
        "inputs": [
            _i("communication_count", "Kommunikationsinfrastruktur (OSM)", EXTERN, "Anzahl", "cell"),
        ],
    },
    "HEALTHCARE_INFRASTRUCTURE": {
        "formula": "100 · (0,5·prox(KH) + 0,35·prox(Arzt) + 0,15·prox(Apo))",
        "inputs": [
            _i("healthcare_access_score", "Erreichbarkeits-Score (OSM)", EXTERN, "", "cell"),
            _i("dist_hospital_m", "Distanz Krankenhaus (OSM)", EXTERN, "m", "cell"),
            _i("dist_doctor_m", "Distanz Arzt/Klinik (OSM)", EXTERN, "m", "cell"),
            _i("dist_pharmacy_m", "Distanz Apotheke (OSM)", EXTERN, "m", "cell"),
        ],
    },
    "INDUSTRIAL_COMMERCIAL_AREAS": {
        "formula": "Fläche(ha) · Industrieanteil",
        "inputs": [
            _i("area_ha", "Zellfläche", COMPUTED, "ha", "computed", "area_ha"),
            _i("industrial", "Industrie/Gewerbe (OSM)", COMPUTED, "", "computed", "industrial"),
        ],
    },
    "AGRICULTURAL_LAND": {
        "formula": "Fläche(ha) · Ackeranteil",
        "inputs": [
            _i("area_ha", "Zellfläche", COMPUTED, "ha", "computed", "area_ha"),
            _i("farmland_frac", "Ackeranteil (OSM)", EXTERN, "", "cell"),
        ],
    },
    "SUPPLY_CHAIN_NODES": {
        "formula": "Industrie · 6 + Gebäude · 0,004",
        "inputs": [
            _i("industrial", "Industrieanteil (OSM)", COMPUTED, "", "computed", "industrial"),
            _i("bldg_count", "Gebäudeanzahl (OSM)", EXTERN, "", "cell"),
        ],
    },
    "FOREST_AREA": {
        "formula": "Fläche(ha) · Waldanteil",
        "inputs": [
            _i("area_ha", "Zellfläche", COMPUTED, "ha", "computed", "area_ha"),
            _i("forest_frac", "Waldanteil (OSM)", EXTERN, "", "cell"),
        ],
    },
    "BIODIVERSITY_HOTSPOTS": {
        "formula": "Fläche(ha) · (Wald+Wasser) · 0,5",
        "inputs": [
            _i("area_ha", "Zellfläche", COMPUTED, "ha", "computed", "area_ha"),
            _i("forest_frac", "Waldanteil (OSM)", EXTERN, "", "cell"),
            _i("water_frac", "Wasseranteil (OSM)", EXTERN, "", "cell"),
        ],
    },
    "EROSION_PRONE_SOILS": {
        "formula": "Fläche(ha) · Acker · Hangneigung",
        "inputs": [
            _i("area_ha", "Zellfläche", COMPUTED, "ha", "computed", "area_ha"),
            _i("farmland_frac", "Ackeranteil (OSM)", EXTERN, "", "cell"),
            _i("slope_factor", "Hangneigung (DEM)", EXTERN, "", "cell"),
        ],
    },
    "COASTAL_RIPARIAN_ZONES": {
        "formula": "Fläche(ha) · Gewässernähe · (0,5+0,5·TWI)",
        "inputs": [
            _i("area_ha", "Zellfläche", COMPUTED, "ha", "computed", "area_ha"),
            _i("water_adj", "Gewässernähe (OSM+DEM)", COMPUTED, "", "cell"),
            _i("twi_norm", "TWI normiert (DEM)", EXTERN, "", "cell"),
        ],
    },
    "FLOODPLAINS": {
        "formula": "Fläche(ha) · Senke · Gewässernähe",
        "inputs": [
            _i("area_ha", "Zellfläche", COMPUTED, "ha", "computed", "area_ha"),
            _i("depression_factor", "Senkentiefe (DEM)", COMPUTED, "", "cell"),
            _i("water_prox", "Gewässernähe (OSM)", COMPUTED, "", "cell"),
        ],
    },
    "COASTAL_STORM_SURGE_EXPOSURE": {
        "formula": "Fläche(ha) · Gebäudeanteil (nur Küste)",
        "inputs": [
            _i("area_ha", "Zellfläche", COMPUTED, "ha", "computed", "area_ha"),
            _i("bldg_cov", "Gebäudeanteil (OSM)", EXTERN, "", "cell"),
        ],
    },
    "GROUNDWATER_DEPENDENT_ECOSYSTEMS": {
        "formula": "Fläche(ha) · (Wald+Grün) · (0,3+Gewässernähe)",
        "inputs": [
            _i("area_ha", "Zellfläche", COMPUTED, "ha", "computed", "area_ha"),
            _i("forest_frac", "Waldanteil (OSM)", EXTERN, "", "cell"),
            _i("green_frac", "Grünanteil (OSM)", EXTERN, "", "cell"),
            _i("water_adj", "Gewässernähe (OSM)", COMPUTED, "", "cell"),
        ],
    },
    "FISHERIES_AQUACULTURE_AREAS": {
        "formula": "Wasseranteil · 5",
        "inputs": [_i("water_frac", "Wasseranteil (OSM)", EXTERN, "", "cell")],
    },
    "FISH_SPAWNING_HABITATS": {
        "formula": "Fläche(ha) · max(Wasser, Gewässernähe·0,5)",
        "inputs": [
            _i("area_ha", "Zellfläche", COMPUTED, "ha", "computed", "area_ha"),
            _i("water_frac", "Wasseranteil (OSM)", EXTERN, "", "cell"),
            _i("water_prox", "Gewässernähe (OSM)", COMPUTED, "", "cell"),
        ],
    },
    # Vulnerabilities
    "BUILDING_STABILITY": {
        "formula": "clamp(50 + Gebäude·20 + (10 wenn H>18m) + Altersfaktor ; 0…100)",
        "inputs": [
            _i("bldg_cov", "Gebäudeanteil (OSM)", EXTERN, "", "cell"),
            _i("avg_height", "Ø Gebäudehöhe (OSM)", EXTERN, "m", "cell"),
            _i("building_age_mean", "Mittleres Baujahr (Zensus)", EXTERN, "Jahr", "cell"),
        ],
    },
    "CRITICAL_INFRA_CONDITION": {
        "formula": "Fester Annahmewert",
        "inputs": [_i("__const", "Zustand kritischer Infrastruktur", PARAM, "Index", "const", 50.0)],
    },
    "MATERIAL_HEAT_SENSITIVITY": {
        "formula": "clamp(Versiegelung · 100 ; 0…100)",
        "inputs": [_i("imp_frac", "Versiegelungsgrad (OSM)", EXTERN, "", "cell")],
    },
    "VULNERABLE_GROUPS_SHARE": {
        "formula": "Gemeindeanteil vulnerable Gruppen (Zensus)",
        "inputs": [_i("share_vulnerable", "Anteil vulnerable Gruppen", EXTERN, "%", "demo")],
    },
    "INCOME_SOCIAL_RESILIENCE": {
        "formula": "Index aus Nettokaltmiete, Eigentümerquote, Wohnfläche/Bewohner (Zensus)",
        "inputs": [
            _i("net_cold_rent", "Nettokaltmiete (Zensus)", EXTERN, "€/m²", "cell"),
            _i("owner_share", "Eigentümerquote (Zensus)", EXTERN, "%", "cell"),
            _i("living_area_per_person", "Wohnfläche je Bewohner (Zensus)", EXTERN, "m²", "cell"),
        ],
    },
    "HEALTHCARE_ACCESS": {
        "formula": "100 · (1 − (0,5·prox(KH) + 0,35·prox(Arzt) + 0,15·prox(Apo)))",
        "inputs": [
            _i("healthcare_access_score", "Erreichbarkeits-Score (OSM)", EXTERN, "", "cell"),
            _i("dist_hospital_m", "Distanz Krankenhaus × 1,3 (OSM)", EXTERN, "m", "cell"),
            _i("dist_doctor_m", "Distanz Arzt/Klinik × 1,3 (OSM)", EXTERN, "m", "cell"),
            _i("dist_pharmacy_m", "Distanz Apotheke × 1,3 (OSM)", EXTERN, "m", "cell"),
        ],
    },
    "WILDFIRE_SUSCEPTIBILITY": {
        "formula": "clamp(Wald · 100 · (0,5 + Trockenheit/2) ; 0…100)",
        "inputs": [
            _i("forest_frac", "Waldanteil (OSM)", EXTERN, "", "cell"),
            _i("dry_index", "Trockenheitsindex (regional)", EXTERN, "", "regional"),
        ],
    },
    "BIODIVERSITY_RESILIENCE": {
        "formula": "clamp(100 − (Wald+Grün)·100·0,6 ; 0…100)",
        "inputs": [
            _i("forest_frac", "Waldanteil (OSM)", EXTERN, "", "cell"),
            _i("green_frac", "Grünanteil (OSM)", EXTERN, "", "cell"),
        ],
    },
    "SOIL_SENSITIVITY": {
        "formula": "clamp(Hang·60 + Acker·40 ; 0…100)",
        "inputs": [
            _i("slope_factor", "Hangneigung (DEM)", EXTERN, "", "cell"),
            _i("farmland_frac", "Ackeranteil (OSM)", EXTERN, "", "cell"),
        ],
    },
    "SINGLE_SITE_DEPENDENCY": {
        "formula": "clamp(Industrieanteil · 200 ; 0…100)",
        "inputs": [_i("industrial", "Industrieanteil (OSM)", COMPUTED, "", "computed", "industrial")],
    },
    "SUPPLY_CHAIN_DEPENDENCY": {
        "formula": "Regionaler Annahmewert",
        "inputs": [_i("__const", "Lieferkettenabhängigkeit", PARAM, "Index", "const", 50.0)],
    },
    "FINANCIAL_ADAPTATION_CAPACITY": {
        "formula": "Regionaler Annahmewert",
        "inputs": [_i("__const", "Finanzielle Kapazität (invers)", PARAM, "Index", "const", 45.0)],
    },
    "INFRA_CRITICALITY": {
        "formula": "clamp(Gebäude · 0,3 ; 0…100)",
        "inputs": [_i("bldg_count", "Gebäudeanzahl (OSM)", EXTERN, "", "cell")],
    },
    "REDUNDANCY_BACKUP": {
        "formula": "Regionaler Annahmewert",
        "inputs": [_i("__const", "Redundanz (invers)", PARAM, "Index", "const", 50.0)],
    },
    "INFRA_DEPENDENCY_CHAIN": {
        "formula": "Regionaler Annahmewert",
        "inputs": [_i("__const", "Infrastrukturabhängigkeit", PARAM, "Index", "const", 50.0)],
    },
    "HEAT_SENSITIVITY": {
        "formula": "clamp(Vulnerable + UHI·6 + (1−Grün)·20 ; 0…100)",
        "inputs": [
            _i("share_vulnerable", "Anteil vulnerable Gruppen (Zensus)", EXTERN, "%", "demo"),
            _i("uhi_delta", "UHI-ΔT (OSM)", COMPUTED, "K", "cell"),
            _i("green_frac", "Grünanteil (OSM)", EXTERN, "", "cell"),
        ],
    },
    "AIR_QUALITY_RISK": {
        "formula": "clamp(Versiegelung·60 + Straße·200 ; 0…100)",
        "inputs": [
            _i("imp_frac", "Versiegelungsgrad (OSM)", EXTERN, "", "cell"),
            _i("road_cov", "Straßenanteil (OSM)", EXTERN, "", "cell"),
        ],
    },
    "DISEASE_VECTOR_SUSCEPTIBILITY": {
        "formula": "clamp(Wasser · 100 · Mitteltemp/12 ; 0…100)",
        "inputs": [
            _i("water_frac", "Wasseranteil (OSM)", EXTERN, "", "cell"),
            _i("mean_temp", "Jahresmitteltemperatur (DWD)", EXTERN, "°C", "regional"),
        ],
    },
    "GROUNDWATER_DEPENDENCY": {
        "formula": "clamp((Acker + Grün) · 50 ; 0…100)",
        "inputs": [
            _i("farmland_frac", "Ackeranteil (OSM)", EXTERN, "", "cell"),
            _i("green_frac", "Grünanteil (OSM)", EXTERN, "", "cell"),
        ],
    },
    "WATER_STRESS_INDEX": {
        "formula": "clamp(Versieg.·40 + Bev.dichte/4000·40 + Trocken·20 ; 0…100)",
        "inputs": [
            _i("imp_frac", "Versiegelungsgrad (OSM)", EXTERN, "", "cell"),
            _i("pop_density", "Bevölkerungsdichte", COMPUTED, "Pers./km²", "computed", "pop_density"),
            _i("dry_index", "Trockenheitsindex (regional)", EXTERN, "", "regional"),
        ],
    },
    "IRRIGATION_DEPENDENCY": {
        "formula": "clamp(Acker · 100 · (0,5 + Trockenheit/2) ; 0…100)",
        "inputs": [
            _i("farmland_frac", "Ackeranteil (OSM)", EXTERN, "", "cell"),
            _i("dry_index", "Trockenheitsindex (regional)", EXTERN, "", "regional"),
        ],
    },
    "EROSION_SUSCEPTIBILITY": {
        "formula": "clamp(Hang · 100 · (1−Grün) ; 0…100)",
        "inputs": [
            _i("slope_factor", "Hangneigung (DEM)", EXTERN, "", "cell"),
            _i("green_frac", "Grünanteil (OSM)", EXTERN, "", "cell"),
        ],
    },
    "LEVEE_CONDITION": {
        "formula": "Annahmewert (Küste 50 / sonst 30)",
        "inputs": [_i("__const", "Deichzustand (invers)", PARAM, "Index", "const", None, coastal_split=(50.0, 30.0))],
    },
    "SALTWATER_INTRUSION_RISK": {
        "formula": "Annahmewert (Küste 40 / sonst 10)",
        "inputs": [_i("__const", "Salzwasserintrusion", PARAM, "Index", "const", None, coastal_split=(40.0, 10.0))],
    },
    "SEALING_DEGREE": {
        "formula": "clamp(Versiegelung · 100 ; 0…100)",
        "inputs": [_i("imp_frac", "Versiegelungsgrad (OSM)", EXTERN, "", "cell")],
    },
    "UHI_INTENSITY": {
        "formula": "UHI-ΔT aus OSM-Landnutzung und Gebäuden",
        "inputs": [_i("uhi_delta", "UHI-ΔT (OSM-Modell)", COMPUTED, "K", "cell")],
    },
    "GREEN_SPACE_SHARE": {
        "formula": "clamp(100 − Grün · 100 ; 0…100)",
        "inputs": [_i("green_frac", "Grünanteil (OSM)", EXTERN, "", "cell")],
    },
    "EARLY_WARNING_SYSTEMS": {
        "formula": "Regionaler Annahmewert",
        "inputs": [_i("__const", "Frühwarnsysteme (invers)", PARAM, "Index", "const", 40.0)],
    },
    "EMERGENCY_MANAGEMENT": {
        "formula": "Regionaler Annahmewert",
        "inputs": [_i("__const", "Katastrophenschutz (invers)", PARAM, "Index", "const", 40.0)],
    },
    "PLANNING_IMPLEMENTATION_CAPACITY": {
        "formula": "Regionaler Annahmewert",
        "inputs": [_i("__const", "Planungskapazität (invers)", PARAM, "Index", "const", 45.0)],
    },
    "FISHERIES_TEMPERATURE_SENSITIVITY": {
        "formula": "clamp(Wasser · 100 · Gewässererwärmung/3 ; 0…100)",
        "inputs": [
            _i("water_frac", "Wasseranteil (OSM)", EXTERN, "", "cell"),
            _i("surface_water_heating", "Gewässererwärmung (DWD)", EXTERN, "°C", "regional"),
        ],
    },
    "AQUACULTURE_TECHNICAL_VULNERABILITY": {
        "formula": "Regionaler Annahmewert",
        "inputs": [_i("__const", "Aquakultur-Verwundbarkeit", PARAM, "Index", "const", 50.0)],
    },
    "FISHERIES_MANAGEMENT_CAPACITY": {
        "formula": "Regionaler Annahmewert",
        "inputs": [_i("__const", "Fischerei-Management (invers)", PARAM, "Index", "const", 45.0)],
    },
}


def _input_meta(inp: dict) -> dict:
    meta = {k: v for k, v in inp.items() if k in ("key", "label", "prov", "unit", "source", "coastal_only")}
    if inp.get("source") in ("const", "hev", "computed") and "value" in inp and inp["value"] is not None:
        meta["value"] = inp["value"]
    return meta


def get_recipe(code: str) -> dict:
    """Liefert {formula, inputs:[...]} für einen H/E/V-Code."""
    if code in DETAILED:
        recipe = DETAILED[code]
        return {
            "formula": recipe["formula"],
            "inputs": [_input_meta(inp) for inp in recipe["inputs"]],
        }
    m = catalog.INDICATOR_BY_CODE.get(code, {})
    spatial = m.get("spatial", False)
    proxy = m.get("proxy") or m.get("description") or "—"
    source = m.get("source")
    prov = EXTERN if spatial else PARAM
    label = "Datenquelle" if spatial else "Annahme (Parameter)"
    inputs = []
    if source:
        inputs.append({
            "key": "__source", "label": f"{label}: {source}",
            "prov": prov, "unit": "", "source": "const",
        })
    else:
        inputs.append({
            "key": "__source", "label": label,
            "prov": prov, "unit": "", "source": "const",
        })
    return {"formula": proxy, "inputs": inputs}


def _hev_meta(codes: list[str]) -> list[dict]:
    out = []
    for c in codes:
        m = catalog.INDICATOR_BY_CODE.get(c, {})
        out.append({
            "code": c,
            "name": m.get("name", c),
            "unit": m.get("unit", ""),
            "norm_min": m.get("norm_min"),
            "norm_max": m.get("norm_max"),
            "source": m.get("source"),
            "spatial": m.get("spatial", False),
        })
    return out


_PATHWAY_LABELS: dict[str, str] = {
    "primary": "Hauptwirkungskette",
    "aligned": "Parallele Wirkung",
    "alternate_hazard": "Alternative Gefahr",
    "alternate_exposure": "Alternative Betroffenheit",
    "alternate_vulnerability": "Alternative Empfindlichkeit",
    "compound_he": "Gefahr und Betroffenheit",
    "compound_hv": "Gefahr und Empfindlichkeit",
    "compound_ev": "Betroffenheit und Empfindlichkeit",
}


def _indicator_name(code: str) -> str:
    return catalog.INDICATOR_BY_CODE.get(code, {}).get("name", code)


def risk_pathway_meta(risk: dict) -> list[dict]:
    """Wirkungsketten mit benannten H/E/V-Faktoren für Tooltip-Formeln."""
    from app.data.pathway_descriptions import (
        chain_label,
        get_pathway_description,
    )

    risk_code = risk.get("code", "")
    out: list[dict] = []
    for p in catalog.build_pathways(risk):
        h_name = _indicator_name(p["hazard"])
        e_name = _indicator_name(p["exposure"])
        v_name = _indicator_name(p["vulnerability"])
        w = float(p["weight"])
        type_label = _PATHWAY_LABELS.get(p["pathway_type"], p["pathway_type"])
        cl = chain_label(h_name, e_name, v_name)
        chain_description = get_pathway_description(
            risk_code, p["hazard"], p["exposure"], p["vulnerability"],
            p["pathway_type"], h_name, e_name, v_name,
        )
        out.append({
            "type": p["pathway_type"],
            "type_label": type_label,
            "weight": w,
            "hazard": p["hazard"],
            "exposure": p["exposure"],
            "vulnerability": p["vulnerability"],
            "hazard_name": h_name,
            "exposure_name": e_name,
            "vulnerability_name": v_name,
            "chain_description": chain_description,
            "chain_label": cl,
            "formula": (
                f"{w:g}·Ĥ({h_name})·Ê({e_name})·V̂({v_name})"
            ),
        })
    return out


def risk_pathway_cell_breakdown(risk: dict, hev_norm: dict) -> dict:
    """Zellbezogene Terme je Wirkungskette (Ĥ,Ê,V̂ als 0…100 wie in der Tabelle)."""
    Hn = hev_norm["hazards"]
    En = hev_norm["exposures"]
    Vn = hev_norm["vulnerabilities"]
    pathways: list[dict] = []
    term_sum = 0.0
    weight_sum = 0.0
    for p in catalog.build_pathways(risk):
        h = float(Hn.get(p["hazard"], 0.0))
        e = float(En.get(p["exposure"], 0.0))
        v = float(Vn.get(p["vulnerability"], 0.0))
        w = float(p["weight"])
        term = w * h * e * v
        term_sum += term
        weight_sum += w
        pathways.append({
            "type": p["pathway_type"],
            "weight": w,
            "hazard": p["hazard"],
            "exposure": p["exposure"],
            "vulnerability": p["vulnerability"],
            "h_norm": round(h * 100.0, 2),
            "e_norm": round(e * 100.0, 2),
            "v_norm": round(v * 100.0, 2),
            "term": round(term, 5),
        })
    index = round(100.0 * term_sum / weight_sum, 2) if weight_sum else 0.0
    return {
        "pathways": pathways,
        "weight_sum": round(weight_sum, 2),
        "term_sum": round(term_sum, 5),
        "index": index,
    }


def _outcome_factor_meta(risk: dict) -> list[dict]:
    """Statische Outcome-Faktoren (Referenz + Skalierung) für Tooltips."""
    scale = risk.get("scale", "pop")
    unit = risk.get("outcome_unit", "")
    ref = float(risk.get("ref_value", 0.0))
    is_monetary = risk.get("cost_dimension") == "monetary"
    ref_source = (
        "Schadenskosten-Schätzung (Risikokatalog)"
        if is_monetary
        else "Referenz-Outcome bei Index 100 / 100.000 Ew. (Risikokatalog)"
    )
    factors: list[dict] = [{
        "key": "ref_value",
        "label": "Referenzwert (Index = 100)",
        "value": ref,
        "unit": unit,
        "source": ref_source,
        "prov": "param",
    }]
    if scale == "pop":
        factors.append({
            "key": "scale_factor",
            "label": "Bevölkerungsfaktor",
            "formula": "Einwohner_zelle / 100.000",
            "source": "Zensus / OSM (räumlich aufgelöst)",
            "prov": "extern",
        })
    elif scale == "area":
        factors.append({
            "key": "scale_factor",
            "label": "Flächenfaktor",
            "formula": "Zellfläche / 50 km²",
            "source": "Rastergeometrie (100 × 100 m)",
            "prov": "computed",
        })
    else:
        factors.append({
            "key": "scale_factor",
            "label": "Skalierung",
            "formula": "1 (keine Kommunal-Skalierung)",
            "source": "Modellannahme (flat)",
            "prov": "param",
        })
    return factors


def risk_recipe(risk: dict) -> dict:
    """Beschreibung der Risikokomposition für den Tooltip."""
    scale = risk.get("scale", "pop")
    unit = risk.get("outcome_unit", "")
    ref = float(risk.get("ref_value", 0.0))
    pathways = risk_pathway_meta(risk)
    weight_sum = round(sum(p["weight"] for p in pathways), 2) or 1.0
    index_terms = " + ".join(p["formula"] for p in pathways)
    formula_index = (
        f"Index = 100 · ({index_terms}) / {weight_sum:g}"
        if pathways
        else "Index = 0"
    )
    if scale == "pop":
        outcome = (
            f"Outcome = Referenz · (Index/100) · (Einwohner_zelle/100.000)"
            f"  →  {unit}"
        )
    elif scale == "area":
        outcome = (
            f"Outcome = Referenz · (Index/100) · (Zellfläche/50 km²)"
            f"  →  {unit}"
        )
    else:
        outcome = f"Outcome = Referenz · (Index/100)  →  {unit}"
    return {
        "formula_index": formula_index,
        "formula_index_header": (
            f"Index = 100 · Σ(w·Ĥ·Ê·V̂) / Σw   "
            f"(Σw = {weight_sum:g}, Ĥ/Ê/V̂ normiert 0…1)"
        ),
        "formula_outcome": outcome,
        "pathways": pathways,
        "weight_sum": weight_sum,
        "hazards": _hev_meta(risk.get("hazards", [])),
        "exposures": _hev_meta(risk.get("exposures", [])),
        "vulnerabilities": _hev_meta(risk.get("vulnerabilities", [])),
        "scale": scale,
        "ref_value": ref,
        "outcome_factors": _outcome_factor_meta(risk),
    }


def _resolve_single(inp: dict, ci: dict, regional: dict, hev: dict | None) -> Any:
    source = inp.get("source", "cell")
    key = inp.get("key", "")

    if source == "const":
        if inp.get("coastal_split"):
            coastal, inland = inp["coastal_split"]
            return coastal if regional.get("is_coastal") else inland
        val = inp.get("value")
        if inp.get("coastal_only") and not regional.get("is_coastal"):
            return 0.0
        return val
    if source == "regional":
        return regional.get(key)
    if source == "demo":
        return regional.get("demographics", {}).get(key)
    if source == "computed":
        resolver_key = inp.get("value") or key
        fn = _COMPUTED_RESOLVERS.get(resolver_key)
        return fn(ci) if fn else ci.get(key)
    if source == "hev" and hev:
        hev_code = inp.get("value") or key
        for cat in ("hazards", "exposures", "vulnerabilities"):
            if hev_code in hev.get(cat, {}):
                return hev[cat][hev_code]
        return None
    return ci.get(key)


def resolve_inputs(
    recipe: dict,
    ci: dict,
    regional: dict,
    hev: dict | None = None,
) -> list[dict]:
    """Löst Eingabewerte pro Zelle auf → [{v, prov}, ...]."""
    detailed_code_inputs = None
    out: list[dict] = []
    for i, inp in enumerate(recipe.get("inputs", [])):
        val = _resolve_single(inp, ci, regional, hev)
        prov = inp.get("prov", EXTERN)
        if isinstance(val, float):
            val = round(val, 4)
        out.append({"v": val, "prov": prov})
    return out


def risk_cell_breakdown(
    risk: dict,
    hev_abs: dict,
    hev_norm: dict,
) -> dict[str, list[list[float]]]:
    """Absolute + normierte Werte je H/E/V-Treiber für eine Zelle."""
    def pairs(codes: list[str], cat_abs: str, cat_norm: str) -> list[list[float]]:
        result = []
        for c in codes:
            abs_val = float(hev_abs.get(cat_abs, {}).get(c, 0.0))
            norm_val = float(hev_norm.get(cat_norm, {}).get(c, 0.0))
            result.append([round(abs_val, 3), round(norm_val * 100.0, 2)])
        return result

    return {
        "H": pairs(risk.get("hazards", []), "hazards", "hazards"),
        "E": pairs(risk.get("exposures", []), "exposures", "exposures"),
        "V": pairs(risk.get("vulnerabilities", []), "vulnerabilities", "vulnerabilities"),
    }


def recipe_for_layer(code: str, category: str) -> dict:
    if category == "risks":
        return risk_recipe(catalog.RISKS_BY_CODE[code])
    if category == "auxiliary":
        m = catalog.AUXILIARY_BY_CODE[code]
        return {
            "formula": f"Direkt aus {m.get('source', 'Quelle')}",
            "inputs": [
                _i(code, m["name"], EXTERN, m.get("unit", ""), "auxiliary"),
            ],
        }
    return get_recipe(code)
