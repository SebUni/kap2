"""Formel- und Herkunftsregister für Karten-Tooltips.

Jeder H/E/V-Indikator und jedes Risiko hat ein Rezept mit Formeltext und
Eingabe-Deskriptoren. Pro Zelle werden die aufgelösten Eingabewerte an die
Frontend-Tooltip-Logik übergeben.
"""

from __future__ import annotations

from typing import Any

from app.data import catalog
from app.services.engine import tunables

EXTERN = "extern"
PARAM = "param"
COMPUTED = "computed"


def _fmt_de(n: float) -> str:
    """Ganzzahlen mit Tausenderpunkt (deutsch), sonst Komma-Dezimal."""
    if float(int(n)) == float(n):
        return f"{int(n):,}".replace(",", ".")
    return f"{n}".replace(".", ",")


def _i(
    key: str,
    label: str,
    prov: str,
    unit: str = "",
    source: str = "cell",
    value: Any = None,
    coastal_only: bool = False,
    coastal_split: tuple[Any, Any] | None = None,
    doc_source: str | None = None,
    overridable: bool = False,
    source_detail: str = "",
    source_refs: list[str] | None = None,
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
    if doc_source is not None:
        # Anzeigbare Herkunft für die Parameter-Registry (``source`` steuert die
        # Wertauflösung in ``_resolve_single`` und ist dafür reserviert).
        d["doc_source"] = doc_source
    if overridable:
        # Nur Inputs mit diesem Flag werden als editierbare Registry-Parameter emittiert.
        # Es darf ausschließlich dort gesetzt sein, wo indicators.py den Wert tatsächlich
        # per get_override liest — sonst entstünde ein wirkungsloser "toter" Parameter.
        d["overridable"] = True
    if source_detail:
        d["source_detail"] = source_detail
    if source_refs:
        d["source_refs"] = source_refs
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


# Gemeinsame Herleitung der KRITIS-Sektorgewichte (INFRA_CRITICALITY).
_KRITIS_W_DETAIL = (
    "Relative Priorisierung der KRITIS-Sektoren nach der BBK-Sektorenlogik (KRITIS-"
    "Dachgesetz/BBK-Sektorenübersicht): Die Zell-Kritikalität ist die gewichtete Summe der "
    "Kritikalitätspunkte je Sektor (anlagenklassen-gewichtete OSM-Zählung, siehe "
    "Exposure-Layer), gekappt bei 100. Die Gewichte (Skala ~1–10) sind eine "
    "dokumentierte Modellwahl auf Basis der BBK-Einstufung, keine amtliche Quantifizierung — "
    "das BBK publiziert Sektoren und Schutzziele, aber keine numerischen Gewichte; editierbar."
)


def _infra_weight_inputs(sector: str) -> list[dict]:
    """Override-fähige Klassengewicht-Parameter eines KRITIS-Sektors.

    Generiert aus der zentralen Taxonomie (app/data/infra_assets.py), damit
    Parameter-Registry und Zähl-Resolver (resolve_weights) nie divergieren.
    """
    from app.data import infra_assets

    return [
        _i(f"w_{cls}", f"Gewicht {spec['label']}", PARAM, "Punkte", "const",
           spec["weight"], overridable=True,
           source_refs=list(infra_assets.WEIGHT_SOURCE_REFS),
           source_detail=spec["source_detail"])
        for cls, spec in infra_assets.ASSET_CLASSES[sector].items()
    ]

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
        "formula": ("Gletscherschwund·Gletscheranteil + Schneerückgang·"
                    "(0,25 + 0,75·Höhenfaktor)·min(1; Schneetage/45)"),
        "inputs": [
            _i("glacier_loss_rate", "Gletscherschwund (DWD, regional)", EXTERN, "%/Jahr", "regional"),
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
        "formula": "Regional · (0,5 + 0,6·(Ackeranteil + Grünanteil))",
        "inputs": [
            _i("soil_moisture_decline", "Bodenfeuchte-Rückgang (regional)", EXTERN, "mm", "regional"),
            _i("farmland_frac", "Ackeranteil (OSM)", EXTERN, "", "cell"),
            _i("green_frac", "Grünanteil (OSM)", EXTERN, "", "cell"),
        ],
    },
    "HEAT_WAVE": {
        # Ohne obere Kappung: Die 40 war der Katalog-norm_max (Screening-Grenze) und
        # kappte zuvor auch die absoluten Schadenswerte heißer Stadtzellen (§3.3).
        "formula": "max(0 ; Heiße Tage + 1,5·UHI-ΔT)",
        "inputs": [
            _i("hot_days", "Heiße Tage/Jahr (DWD CDC, am Zentroid)", EXTERN, "Tage", "cell"),
            _i("uhi_delta", "UHI-ΔT (OSM-Modell)", COMPUTED, "K", "cell"),
            _i("uhi_weight", "UHI-Gewichtung", PARAM, "×", "const", 1.5),
        ],
    },
    "COLD_EXTREME": {
        "formula": "Frosttage · (1 − 0,3·min(UHI-ΔT/5 ; 1))",
        "inputs": [
            _i("frost_days", "Frosttage (DWD CDC, am Zentroid)", EXTERN, "Tage", "regional"),
            _i("uhi_delta", "UHI-ΔT (OSM-Modell)", COMPUTED, "K", "cell"),
        ],
    },
    "HEAVY_RAIN_FLOOD": {
        "formula": "clamp(Starkregen · (0,4 + Versiegelung) · (0,5 + 0,5·TWI) · (0,6 + Senke) ; 0…100)",
        "inputs": [
            _i("heavy_rain_index", "Starkregenindex (DWD)", EXTERN, "Index", "regional"),
            _i("imp_frac", "Versiegelungsgrad (OSM)", EXTERN, "", "cell"),
            _i("twi_norm", "TWI normiert (Terrarium-DEM)", EXTERN, "", "cell"),
            _i("depression_factor", "Senkentiefe (DEM)", COMPUTED, "", "cell"),
        ],
    },
    "DROUGHT": {
        "formula": "clamp(Trockentage · (0,6 + 0,7·(Ackeranteil + Grünanteil)) ; 0…60)",
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
        "formula": ("min(1; Basis(Küste 0,4/Binnen 0,05) · (0,35+0,65·Senke) · "
                    "(0,45+0,55·Acker) · (0,55+0,45·Trockenheit) · Küsten-/Höhenfaktor)"),
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
        "formula": "max(Hitze; Dürre; Starkregen) — jeweils normiert 0…1",
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
        "formula": "clamp(Niedrigwasser · (0,6 + 0,4·Trockenheit) · (1 + 0,3·Gewässernähe) ; 0…60)",
        "inputs": [
            _i("low_flow_days", "Niedrigwasser-Tage (PEGELONLINE, nächster Pegel)", EXTERN, "Tage", "regional"),
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
        "formula": "Fläche(ha) · Gebäudeanteil · max(Senke; min(UHI-ΔT/6; 1))",
        "inputs": [
            _i("area_ha", "Zellfläche", COMPUTED, "ha", "computed", "area_ha"),
            _i("bldg_cov", "Gebäudeanteil (OSM)", EXTERN, "", "cell"),
            _i("depression_factor", "Senkentiefe (DEM)", COMPUTED, "", "cell"),
            _i("uhi_delta", "UHI-ΔT (OSM)", COMPUTED, "K", "cell"),
        ],
    },
    "ENERGY_INFRASTRUCTURE": {
        "formula": "w_max + 0,5 · (Σ w(Anlagenklasse) · Anzahl − w_max); Leitungen je "
                   "kV-Klasse pro Zellquerung; Masten/Tragwerke = 0 (Bestandteil der Leitung)",
        "inputs": [
            _i("energy_infra_count", "Energie-Kritikalität (OSM, gewichtet)", EXTERN,
               "Punkte", "cell"),
            *_infra_weight_inputs("energy"),
        ],
    },
    "WATER_WASTEWATER_INFRA": {
        "formula": "w_max + 0,5 · (Σ w(Anlagenklasse) · Anzahl − w_max) "
                   "(Kläranlage/Wasserwerk/Pumpwerk/Speicher)",
        "inputs": [
            _i("water_wastewater_count", "Wasser/Abwasser-Kritikalität (OSM, gewichtet)",
               EXTERN, "Punkte", "cell"),
            *_infra_weight_inputs("water"),
        ],
    },
    "TRANSPORT_HUBS": {
        "formula": "w_max + 0,5 · (Σ w(Anlagenklasse) · Anzahl − w_max) "
                   "(Bahnhof/Halt/ÖPNV/Busbahnhof)",
        "inputs": [
            _i("transport_hub_count", "Verkehrsknoten-Kritikalität (OSM, gewichtet)",
               EXTERN, "Punkte", "cell"),
            *_infra_weight_inputs("transport"),
        ],
    },
    "COMMUNICATION_INFRA": {
        "formula": "w_max + 0,5 · (Σ w(Anlagenklasse) · Anzahl − w_max) "
                   "(RZ/Vermittlung/Funkturm/Mast)",
        "inputs": [
            _i("communication_count", "Kommunikations-Kritikalität (OSM, gewichtet)",
               EXTERN, "Punkte", "cell"),
            *_infra_weight_inputs("comm"),
        ],
    },
    "HEALTHCARE_INFRASTRUCTURE": {
        "formula": "100 · (0,5·Nähe(Krankenhaus) + 0,35·Nähe(Arzt) + 0,15·Nähe(Apotheke))",
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
        "formula": "Industrieanteil · 6 + Gebäudeanzahl · 0,004",
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
        "formula": "Fläche(ha) · Ackeranteil · Hangneigung",
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
        "formula": "Fläche(ha) · Senke · max(Gewässernähe; 0,3 bei Ufernähe, sonst 0,1)",
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
        "formula": "Fläche(ha) · (Waldanteil + Grünanteil) · (0,3 + Gewässernähe)",
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
        "formula": "Fläche(ha) · max(Wasseranteil; Gewässernähe·0,5)",
        "inputs": [
            _i("area_ha", "Zellfläche", COMPUTED, "ha", "computed", "area_ha"),
            _i("water_frac", "Wasseranteil (OSM)", EXTERN, "", "cell"),
            _i("water_prox", "Gewässernähe (OSM)", COMPUTED, "", "cell"),
        ],
    },
    # Vulnerabilities
    "BUILDING_STABILITY": {
        "formula": ("clamp(50 + 20·Gebäudeanteil + (10 wenn Höhe > 18 m) + "
                    "min(30; (heute−Baujahr)/100·30) ; 0…100)"),
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
        "formula": "100 · (1 − (0,5·Nähe(Krankenhaus) + 0,35·Nähe(Arzt) + 0,15·Nähe(Apotheke)))",
        "inputs": [
            _i("healthcare_access_score", "Erreichbarkeits-Score (OSM)", EXTERN, "", "cell"),
            _i("dist_hospital_m", "Distanz Krankenhaus × 1,3 (OSM)", EXTERN, "m", "cell"),
            _i("dist_doctor_m", "Distanz Arzt/Klinik × 1,3 (OSM)", EXTERN, "m", "cell"),
            _i("dist_pharmacy_m", "Distanz Apotheke × 1,3 (OSM)", EXTERN, "m", "cell"),
        ],
    },
    "WILDFIRE_SUSCEPTIBILITY": {
        "formula": "clamp(Waldanteil · 100 · (0,5 + Trockenheit/2) ; 0…100)",
        "inputs": [
            _i("forest_frac", "Waldanteil (OSM)", EXTERN, "", "cell"),
            _i("dry_index", "Trockenheitsindex (regional)", EXTERN, "", "regional"),
        ],
    },
    "BIODIVERSITY_RESILIENCE": {
        "formula": "clamp(100 − (Waldanteil + Grünanteil)·100·0,6 ; 0…100)",
        "inputs": [
            _i("forest_frac", "Waldanteil (OSM)", EXTERN, "", "cell"),
            _i("green_frac", "Grünanteil (OSM)", EXTERN, "", "cell"),
        ],
    },
    "SOIL_SENSITIVITY": {
        "formula": "clamp(60·Hangneigung + 40·Ackeranteil ; 0…100)",
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
        "formula": "INKAR-Sozioökonomie (Steuerkraft/Arbeitslosigkeit), invers; Fallback 50",
        "inputs": [
            _i("financial_adaptation", "Sozioökonomie-Index (BBSR INKAR)", EXTERN, "Index", "socio"),
            _i("__const", "Finanzielle Kapazität (invers, Fallback)", PARAM, "Index", "const", 50.0,
               doc_source="BBSR INKAR / Regionalstatistik (per AGS); "
                          "Fallback: Modellannahme (mangels lokaler Daten)",
               overridable=True, source_refs=["BBSR_INKAR"],
               source_detail="Vulnerabilität (invers: hoch = geringe Kapazität) aus BBSR-"
               "INKAR-Sozioökonomie je Gemeinde (Steuerkraft, Arbeitslosigkeit). Der Wert 50 "
               "ist der NEUTRALE Fallback der 0–100-Skala, wenn für die Kommune keine INKAR-"
               "Kennzahlen auflösbar sind (Skalenmitte = keine Aussage nach oben oder unten). "
               "Ein Override ersetzt in allen Zellen auch den INKAR-abgeleiteten Wert "
               "(Reihenfolge: Override > Ableitung > Fallback)."),
        ],
    },
    "INFRA_CRITICALITY": {
        "formula": "clamp(w_E·Energie + w_W·Wasser + w_K·Kommunikation + w_G·Gesundheit + w_V·Verkehr ; 0…100)",
        "inputs": [
            _i("energy_infra_count", "Energie-Kritikalität (OSM, gewichtet)", EXTERN, "Punkte", "cell"),
            _i("water_wastewater_count", "Wasser/Abwasser-Kritikalität (OSM, gewichtet)", EXTERN, "Punkte", "cell"),
            _i("communication_count", "Kommunikations-Kritikalität (OSM, gewichtet)", EXTERN, "Punkte", "cell"),
            _i("healthcare_access_score", "Gesundheits-Erreichbarkeit (OSM)", EXTERN, "", "cell"),
            _i("transport_hub_count", "Verkehrsknoten-Kritikalität (OSM, gewichtet)", EXTERN, "Punkte", "cell"),
            _i("w_energy", "Gewicht Energie (BBK-KRITIS)", PARAM, "", "const", 8.0,
               overridable=True, source_refs=["BBK_KRITIS"],
               source_detail=_KRITIS_W_DETAIL + " Energie: hohes Gewicht (8), da Strom-/"
               "Gasausfall unmittelbar alle anderen Sektoren kaskadiert (BBK-Leitszenario "
               "Stromausfall)."),
            _i("w_water", "Gewicht Wasser (BBK-KRITIS)", PARAM, "", "const", 8.0,
               overridable=True, source_refs=["BBK_KRITIS"],
               source_detail=_KRITIS_W_DETAIL + " Wasser/Abwasser: hohes Gewicht (8), "
               "lebensnotwendige Grundversorgung ohne kurzfristigen Ersatz."),
            _i("w_comm", "Gewicht IT/TK (BBK-KRITIS)", PARAM, "", "const", 6.0,
               overridable=True, source_refs=["BBK_KRITIS"],
               source_detail=_KRITIS_W_DETAIL + " IT/Telekommunikation: mittleres Gewicht (6), "
               "kritisch für Koordination/Warnung, aber mit Teil-Redundanzen (Mobilfunk/"
               "Festnetz/Behördenfunk)."),
            _i("w_health", "Gewicht Gesundheit (BBK-KRITIS)", PARAM, "", "const", 10.0,
               overridable=True, source_refs=["BBK_KRITIS"],
               source_detail=_KRITIS_W_DETAIL + " Gesundheit: höchstes Gewicht (10), direkter "
               "Lebensschutz (Krankenhäuser/Pflege) ohne Substitutionsmöglichkeit im Ereignisfall."),
            _i("w_transport", "Gewicht Verkehr (BBK-KRITIS)", PARAM, "", "const", 6.0,
               overridable=True, source_refs=["BBK_KRITIS"],
               source_detail=_KRITIS_W_DETAIL + " Transport/Verkehr: mittleres Gewicht (6), "
               "wichtig für Erreichbarkeit/Evakuierung, aber räumlich meist umfahrbar."),
        ],
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
        "formula": "clamp(Anteil Vulnerable + 6·UHI-ΔT + 20·(1−Grünanteil) ; 0…100)",
        "inputs": [
            _i("share_vulnerable", "Anteil vulnerable Gruppen (Zensus)", EXTERN, "%", "demo"),
            _i("uhi_delta", "UHI-ΔT (OSM)", COMPUTED, "K", "cell"),
            _i("green_frac", "Grünanteil (OSM)", EXTERN, "", "cell"),
        ],
    },
    "AIR_QUALITY_RISK": {
        "formula": "clamp(60·Versiegelung + 200·Straßenanteil ; 0…100)",
        "inputs": [
            _i("imp_frac", "Versiegelungsgrad (OSM)", EXTERN, "", "cell"),
            _i("road_cov", "Straßenanteil (OSM)", EXTERN, "", "cell"),
        ],
    },
    "DISEASE_VECTOR_SUSCEPTIBILITY": {
        "formula": "clamp(Wasseranteil · 100 · Mitteltemperatur/12 ; 0…100)",
        "inputs": [
            _i("water_frac", "Wasseranteil (OSM)", EXTERN, "", "cell"),
            _i("mean_temp", "Jahresmitteltemperatur (DWD)", EXTERN, "°C", "regional"),
        ],
    },
    "GROUNDWATER_DEPENDENCY": {
        "formula": "clamp((Ackeranteil + Grünanteil) · 50 ; 0…100)",
        "inputs": [
            _i("farmland_frac", "Ackeranteil (OSM)", EXTERN, "", "cell"),
            _i("green_frac", "Grünanteil (OSM)", EXTERN, "", "cell"),
        ],
    },
    "WATER_STRESS_INDEX": {
        "formula": "clamp(Versiegelung·40 + (Bevölkerungsdichte/4.000)·40 + Trockenheit·20 ; 0…100)",
        "inputs": [
            _i("imp_frac", "Versiegelungsgrad (OSM)", EXTERN, "", "cell"),
            _i("pop_density", "Bevölkerungsdichte", COMPUTED, "Pers./km²", "computed", "pop_density"),
            _i("dry_index", "Trockenheitsindex (regional)", EXTERN, "", "regional"),
        ],
    },
    "IRRIGATION_DEPENDENCY": {
        "formula": "clamp(Ackeranteil · 100 · (0,5 + Trockenheit/2) ; 0…100)",
        "inputs": [
            _i("farmland_frac", "Ackeranteil (OSM)", EXTERN, "", "cell"),
            _i("dry_index", "Trockenheitsindex (regional)", EXTERN, "", "regional"),
        ],
    },
    "EROSION_SUSCEPTIBILITY": {
        "formula": "clamp(Hangneigung · 100 · (1−Grünanteil) ; 0…100)",
        "inputs": [
            _i("slope_factor", "Hangneigung (DEM)", EXTERN, "", "cell"),
            _i("green_frac", "Grünanteil (OSM)", EXTERN, "", "cell"),
        ],
    },
    "LEVEE_CONDITION": {
        "formula": "Basis(Küste 50/Binnen 30) + 40·Exposition·(1−Deichnähe) − 25·Deichnähe",
        "inputs": [
            _i("dyke_prox", "Nähe Deich/Damm (OSM man_made=dyke/embankment)", EXTERN, "", "cell"),
            _i("water_prox", "Gewässernähe", EXTERN, "", "cell"),
            # value=30.0 (Binnen-Basis) statt None: der Registry-Parameter braucht einen
            # anzeigbaren Default; die Karten-Tooltips lösen weiterhin über coastal_split auf.
            _i("__const", "Deichzustand (invers, Basis-Fallback)", PARAM, "Index", "const", 30.0,
               coastal_split=(50.0, 30.0), doc_source="OSM man_made=dyke/embankment",
               overridable=True, source_refs=["OSM_Data"],
               source_detail="Basiswert des (inversen) Deichzustands-Index ohne lokale "
               "Deichdaten: 30 im Binnenland, 50 an der Küste (coastal_split; angezeigt wird "
               "die Binnen-Basis). Ortsaufgelöst wird der Wert aus OSM man_made=dyke/"
               "embankment und der Hochwasserexposition der Zelle moduliert (Basis + "
               "40·Exposition·(1−Deichnähe) − 25·Deichnähe). Ein Override ersetzt den Wert "
               "in ALLEN Zellen — auch die OSM-Ableitung und den Küstenaufschlag."),
        ],
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
        "formula": "clamp(100 − Grünanteil · 100 ; 0…100)",
        "inputs": [_i("green_frac", "Grünanteil (OSM)", EXTERN, "", "cell")],
    },
    "EARLY_WARNING_SYSTEMS": {
        "formula": "clamp(50 + (Katastrophenschutz − 50)·0,6 ; 0…100); Fallback 40",
        "inputs": [
            _i("emergency_access_score", "Nähe Feuerwehr/Rettung (OSM, Proxy)", EXTERN, "", "cell"),
            _i("__const", "Frühwarnsysteme (invers, Fallback)", PARAM, "Index", "const", 40.0,
               doc_source="OSM amenity=fire_station / emergency=* (Proxy)",
               overridable=True, source_refs=["OSM_Data"],
               source_detail="Vulnerabilität (invers: hoch = schwache Frühwarnung) aus dem "
               "OSM-Notfall-Proxy, zur Skalenmitte 50 gedämpft (Faktor 0,6), weil Feuerwehr-"
               "Nähe Frühwarnsysteme (Sirenen, Warn-Apps, Pegelmessnetze) nur schwach "
               "abbildet. Der Wert 40 ist der Fallback ohne OSM-Notfalldaten: leicht besser "
               "als neutral (50), da Deutschland flächendeckend über MoWaS/Cell Broadcast/"
               "Sirenen grundversorgt ist. Ein Override ersetzt den Wert in allen Zellen."),
        ],
    },
    "EMERGENCY_MANAGEMENT": {
        "formula": "clamp(100·(1 − Notfall-Erreichbarkeit) ; 0…100); Fallback 40",
        "inputs": [
            _i("emergency_access_score", "Nähe Feuerwehr/Rettung (OSM)", EXTERN, "", "cell"),
            _i("__const", "Katastrophenschutz (invers, Fallback)", PARAM, "Index", "const", 40.0,
               doc_source="OSM amenity=fire_station / emergency=*",
               overridable=True, source_refs=["OSM_Data"],
               source_detail="Vulnerabilität (invers: hoch = schwacher Katastrophenschutz) "
               "aus der OSM-Erreichbarkeit von Feuerwehr/Rettungsdiensten je Zelle "
               "(100·(1−Erreichbarkeit)). Der Wert 40 ist der Fallback ohne OSM-Notfall-"
               "daten: leicht besser als neutral (50) wegen des flächendeckenden deutschen "
               "Feuerwehrsystems (~95 % der Bevölkerung in <10 min Hilfsfrist erreichbar). "
               "Ein Override ersetzt den Wert in allen Zellen."),
        ],
    },
    "PLANNING_IMPLEMENTATION_CAPACITY": {
        "formula": "INKAR-Finanzkraft (Steuerkraft), invers; Fallback 50",
        "inputs": [
            _i("planning_capacity", "Finanzkraft-Index (BBSR INKAR)", EXTERN, "Index", "socio"),
            _i("__const", "Planungskapazität (invers, Fallback)", PARAM, "Index", "const", 50.0,
               doc_source="BBSR INKAR / Regionalstatistik (per AGS); "
                          "Fallback: Modellannahme (mangels lokaler Daten)",
               overridable=True, source_refs=["BBSR_INKAR"],
               source_detail="Vulnerabilität (invers: hoch = geringe Planungs-/Umsetzungs-"
               "kapazität) aus der BBSR-INKAR-Finanzkraft (Steuerkraft je Einwohner) der "
               "Gemeinde. Der Wert 50 ist der NEUTRALE Fallback der 0–100-Skala ohne "
               "auflösbare INKAR-Kennzahl (Skalenmitte = keine Aussage). Ein Override "
               "ersetzt in allen Zellen auch den INKAR-abgeleiteten Wert."),
        ],
    },
    "FISHERIES_TEMPERATURE_SENSITIVITY": {
        "formula": "clamp(Wasseranteil · 100 · Gewässererwärmung/3 ; 0…100)",
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
    meta = {
        k: v for k, v in inp.items()
        if k in ("key", "label", "prov", "unit", "source", "coastal_only", "overridable")
    }
    # Wert für die Anzeige/Lineage behalten: für Konstanten/HEV/Computed sowie für
    # jeden override-fähigen Formel-Parameter (dieser braucht seinen Default als
    # sichtbaren Fallback und damit die Lineage seine parameter_id verdrahten kann).
    keep_value = inp.get("source") in ("const", "hev", "computed") or inp.get("overridable")
    if keep_value and "value" in inp and inp["value"] is not None:
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
    if code in catalog.AUXILIARY_BY_CODE:
        # Sonstige-Ebenen: ehrlicher Berechnungstext statt des generischen
        # Katalog-Proxys "Direkt aus Datenquelle (siehe Quelle)".
        from app.data.lineage_operators import aux_formula_text
        proxy = aux_formula_text(code, m.get("source", ""))
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
    from app.data import sources

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
            # Begründung + Quelle der kuratierten Wirkungskette (Info-Fenster-Sektion)
            "justification": p.get("justification"),
            "justification_ref": p.get("justification_ref"),
            "justification_source": (
                sources.resolve([p["justification_ref"]])[0]
                if p.get("justification_ref") else None
            ),
            "cluster": p.get("cluster"),
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
    max_term = 0.0
    max_idx = -1
    for i, p in enumerate(catalog.build_pathways(risk)):
        h = float(Hn.get(p["hazard"], 0.0))
        e = float(En.get(p["exposure"], 0.0))
        v = float(Vn.get(p["vulnerability"], 0.0))
        w = float(p["weight"])
        term = w * h * e * v
        if term > max_term:
            max_term = term
            max_idx = i
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
            "is_max": False,
        })
    if max_idx >= 0:
        pathways[max_idx]["is_max"] = True
    index = round(100.0 * max_term, 2)
    return {
        "pathways": pathways,
        "max_term": round(max_term, 5),
        "index": index,
    }


def _outcome_factor_meta(risk: dict) -> list[dict]:
    """Statische Outcome-Faktoren (Referenz + Skalierung) für Tooltips."""
    from app.services.engine import impact

    scale = risk.get("scale", "pop")
    unit = risk.get("outcome_unit", "")
    ref = float(risk.get("ref_value", 0.0))
    is_monetary = risk.get("cost_dimension") == "monetary"
    has_impact = impact.has(risk["code"])
    if has_impact:
        # ref_value ist bei Risiken mit Schadensfunktion nur noch Kalibrier-/Sanity-Anker.
        ref_source = "Kalibrier-/Sanity-Anker (Schicht B, kein Rechenweg)"
        ref_label = "Referenzwert (Kalibrier-/Sanity-Anker)"
    else:
        ref_source = (
            "Schadenskosten-Schätzung (Risikokatalog)"
            if is_monetary
            else ("Referenz-Outcome bei Index 100 / "
                  f"{_fmt_de(tunables.effective_ref_population())} Ew. (Risikokatalog)")
        )
        ref_label = "Referenzwert (Index = 100)"
    factors: list[dict] = [{
        "key": "ref_value",
        "label": ref_label,
        "value": ref,
        "unit": unit,
        "source": ref_source,
        "prov": "param",
    }]
    if has_impact:
        # Bei Schadensfunktionen keine Index/Skalierungs-Faktoren als Rechenweg zeigen.
        return factors
    if scale == "pop":
        factors.append({
            "key": "scale_factor",
            "label": "Bevölkerungsfaktor",
            "formula": f"Einwohner_zelle / {_fmt_de(tunables.effective_ref_population())}",
            "source": "Zensus / OSM (räumlich aufgelöst)",
            "prov": "extern",
        })
    elif scale == "area":
        factors.append({
            "key": "scale_factor",
            "label": "Flächenfaktor",
            "formula": f"Zellfläche / {_fmt_de(tunables.effective_ref_area_km2())} km²",
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
    index_terms = " ,  ".join(p["formula"] for p in pathways)
    formula_index = (
        f"Index = 100 · max( {index_terms} )"
        if pathways
        else "Index = 0"
    )
    from app.services.engine import impact
    kind = impact.lineage_kind(risk)
    if kind == "health":
        outcome = (
            f"Outcome = Betroffene · Rate · Treiber(AF/Intensität) · g(V̂), Σ Zellen"
            f"  →  {unit};  € = Outcome × Kostensatz. Der Index bleibt Screening-Kennzahl."
        )
    elif kind == "environment":
        outcome = (
            f"Outcome = exponierte Fläche · Verlustrate · Intensität · g(V̂), Σ Zellen"
            f"  →  {unit};  € = Outcome × Kostensatz. Der Index bleibt Screening-Kennzahl."
        )
    elif kind == "monetary":
        outcome = (
            "€ = Assetwert · Verlustrate · Schadenskurve(Intensität) · g(V̂), Σ Zellen. "
            "Der Index bleibt Screening-Kennzahl."
        )
    elif kind == "indirect":
        outcome = "€ = k_indirekt · Σ direkte Sektorschäden (konsolidierte Folgekosten)."
    elif kind == "restoration":
        outcome = (
            "€ = Restaurierungsquote · Σ direkte Sektorschäden — Teilkennzahl, "
            "nicht additiv zur Gesamtsumme."
        )
    elif kind == "consolidated_zero":
        outcome = "0 € — in k_indirekt (Indirekte wirtschaftliche Verluste) konsolidiert."
    elif kind == "index_only":
        outcome = "Kein €-Outcome: reines Screening (Index), Doppelzählung vermieden."
    else:   # flat
        outcome = (
            f"Outcome = Referenz · (P90-Index/100), kommunenweit  →  {unit};  "
            f"€ = Outcome × Kostensatz × Einwohner/{_fmt_de(tunables.effective_ref_population())}."
        )
    return {
        "formula_index": formula_index,
        "formula_index_header": (
            "Index = 100 · max(w·Ĥ·Ê·V̂)   "
            "(stärkste Wirkungskette; Ĥ/Ê/V̂ normiert 0…1)"
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
    if source == "socio":
        return (regional.get("socioeconomic") or {}).get(key)
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
        from app.data.lineage_operators import aux_formula_text
        m = catalog.AUXILIARY_BY_CODE[code]
        return {
            "formula": aux_formula_text(code, m.get("source", "Quelle")),
            "inputs": [
                _i(code, m["name"], EXTERN, m.get("unit", ""), "auxiliary"),
            ],
        }
    return get_recipe(code)
