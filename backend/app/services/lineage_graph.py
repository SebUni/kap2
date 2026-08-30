"""Baut Herkunfts-Graphen (Quellen → Zwischen → H/E/V → Risiko) für Info-Fenster."""

from __future__ import annotations

from typing import Any

from app.data import catalog
from app.data.lineage_operators import (
    AUX_LINEAGE,
    CELL_DIRECT,
    CELL_OPERATORS,
    aux_formula_text,
    formula_operators_for,
)
from app.data.pathway_descriptions import chain_label, get_pathway_description
from app.services.engine import formulas
from app.services.engine.formulas import risk_pathway_meta, risk_recipe
from app.services.engine.impact.environment import LINEAGE_SPECS as ENV_SPECS
from app.services.engine.impact.health import LINEAGE_SPECS as HEALTH_SPECS
from app.services.engine.impact.monetary import LINEAGE_SPECS as MONETARY_SPECS
from app.services.engine.impact.params import IMPACT_GLOBAL_SPECS, IMPACT_PARAM_SPECS

# Label/Einheit/Quelle der Schicht-B-Parameter für die Parameterknoten im Diagramm
_IMPACT_PARAM_BY_KEY: dict[tuple[str, str], dict] = {
    (s["risk"], s["key"]): s for s in IMPACT_PARAM_SPECS
}
_IMPACT_GLOBAL_BY_KEY: dict[str, dict] = {s["key"]: s for s in IMPACT_GLOBAL_SPECS}

# ── Kanonische Quellen ────────────────────────────────────────────────────────

SOURCE_IDS = {
    "osm": ("OSM", "OpenStreetMap"),
    "lod2": ("LoD2", "Amtliche 3D-Gebäudemodelle der Länder (LoD2, CityGML)"),
    "dwd": ("DWD", "Deutscher Wetterdienst (CDC-Klimaraster)"),
    "zensus": ("Zensus", "Zensus 2022 (100-m-Gitter, Destatis)"),
    "dem": ("DEM", "AWS Terrarium DEM (digitales Geländemodell)"),
    "bsh": ("BSH", "Bundesamt für Seeschifffahrt"),
    "pegelonline": ("PEGELONLINE", "Pegeldaten der Wasserstraßen- und Schifffahrtsverwaltung"),
    "era5": ("ERA5", "ECMWF-Reanalyse (Böenklimatologie)"),
    "inkar": ("INKAR", "BBSR INKAR / Regionalstatistik (sozioökonomische Kennzahlen je Gemeinde)"),
    "param": ("Parameter", "Modellannahme"),
    "computed": ("Berechnet", "Abgeleitet aus Zellgrößen"),
}

INTERMEDIATE_LABELS: dict[str, str] = {
    "imp_frac": "Versiegelungsgrad (Zelle)",
    "imp_lu": "Versiegelung (Landnutzung)",
    "bldg_cov": "Gebäudeanteil",
    "road_cov": "Straßenanteil",
    "green_frac": "Grünanteil",
    "forest_frac": "Waldanteil",
    "farmland_frac": "Ackeranteil",
    "water_frac": "Wasseranteil",
    "water_adj": "Gewässernähe (Nachbarschaft)",
    "water_prox": "Gewässernähe (Distanz)",
    "uhi_delta": "UHI-ΔT",
    "uhi_delta_night": "UHI-ΔT (Nacht)",
    "uhi_delta_mean": "UHI-ΔT (Tagesmittel)",
    "summer_temp_raster": "Sommertemperatur (DWD-Raster)",
    "summer_temp_uhi_dev": "Wärmeinsel-Abweichung",
    "summer_temp_lapse": "Höhenkorrektur",
    "summer_temp_cell": "Zell-Sommertemperatur",
    "summer_night_temp": "Sommer-Nachttemperatur",
    "pop_age_bands": "Bevölkerung je Altersband",
    "canopy_frac": "Baumkronenanteil",
    "svf": "Himmelssichtfaktor",
    "avg_height": "Mittlere Gebäudehöhe",
    "vent_score": "Belüftungsgrad",
    "slope_deg": "Hangneigung",
    "slope_factor": "Hangfaktor",
    "slope_proxy": "Hangfaktor (Proxy)",
    "mean_elevation_m": "Mittlere Höhe",
    "snow_elevation_factor": "Höhenfaktor Schnee",
    "depression_factor": "Senkenfaktor",
    "depression_proxy": "Senken-Proxy",
    "twi": "Feuchteindex (TWI)",
    "twi_norm": "Feuchteindex (TWI), normiert",
    "sink_depth_m": "Senkentiefe",
    "flow_accum": "Flussakkumulation",
    "water_dist_m": "Gewässerdistanz",
    "albedo": "Albedo",
    "building_count_zensus": "Gebäudeanzahl (Zensus)",
    "pop_over_65": "Einwohner ≥ 65",
    "pop_under_18": "Einwohner < 18",
    "drought_days": "Trockentage",
    "dry_index": "Trockenheitsindex",
    "low_flow_days": "Niedrigwasser-Tage",
    "pop": "Einwohner (Zelle)",
    "pop_density": "Bevölkerungsdichte",
    "area_km2": "Zellfläche",
    "area_ha": "Zellfläche (ha)",
    "industrial": "Industriefläche (abgeleitet)",
    "healthcare_access_score": "Gesundheitszugang",
    "transport_hub_count": "Verkehrsknoten",
    "hot_days": "Heiße Tage/Jahr",
    "frost_days": "Frosttage",
    "heavy_rain_index": "Starkregenindex",
    "storm_days": "Sturmtage",
    "mean_temp_rise": "Temperaturanstieg",
    "soil_moisture_decline": "Bodenfeuchte-Rückgang",
    "surface_water_heating": "Gewässererwärmung",
    "glacier_loss_rate": "Gletscherschwund",
    "glacier_frac": "Gletscheranteil",
    "snow_decline_rate_pct": "Schneedecken-Rückgang",
    "snow_days": "Schneedeckentage",
    "mean_temp": "Jahresmitteltemperatur",
    "sea_level_rise": "Meeresspiegelanstieg",
    "area_m2": "Zellfläche (m²)",
    "share_over_65": "Anteil ≥ 65 Jahre",
    "share_under_18": "Anteil < 18 Jahre",
    "share_vulnerable": "Anteil vulnerable Gruppen",
    "living_area_per_person": "Wohnfläche je Person",
    "owner_share": "Eigentümerquote",
    "net_cold_rent": "Nettokaltmiete",
    "building_age_mean": "Mittleres Gebäudealter",
    "dist_hospital_m": "Distanz Krankenhaus",
    "dist_doctor_m": "Distanz Arzt/Klinik",
    "dist_pharmacy_m": "Distanz Apotheke",
    "dyke_prox": "Deichnähe",
    "emergency_access_score": "Notfall-Erreichbarkeit",
    "bldg_count": "Gebäudeanzahl",
    "energy_infra_count": "Energie-Kritikalität (Punkte)",
    "water_wastewater_count": "Wasser-/Abwasser-Kritikalität (Punkte)",
    "communication_count": "Kommunikations-Kritikalität (Punkte)",
    "transport_hub_count": "Verkehrsknoten-Kritikalität (Punkte)",
    "energy_infra_classes": "Energieanlagen je Klasse (OSM)",
    "water_wastewater_classes": "Wasser-/Abwasseranlagen je Klasse (OSM)",
    "communication_classes": "Kommunikationsanlagen je Klasse (OSM)",
    "transport_hub_classes": "Verkehrsknoten je Klasse (OSM)",
}

# cell_key → (intermediate_keys, source_ids)
CELL_INPUT_LINEAGE: dict[str, tuple[list[str], list[str]]] = {
    "imp_frac": (["bldg_cov", "road_cov", "imp_lu"], ["osm"]),
    "imp_lu": ([], ["osm"]),
    "bldg_cov": ([], ["osm"]),
    "road_cov": ([], ["osm"]),
    "green_frac": ([], ["osm"]),
    "forest_frac": ([], ["osm"]),
    "farmland_frac": ([], ["osm"]),
    "water_frac": ([], ["osm"]),
    "water_adj": (["water_prox", "water_frac"], ["osm"]),
    "water_prox": (["water_dist_m"], []),
    "water_dist_m": ([], ["osm"]),
    "glacier_frac": ([], ["osm"]),
    "albedo": ([], ["osm"]),
    "canopy_frac": ([], ["osm"]),
    "svf": ([], ["lod2", "osm"]),
    "avg_height": ([], ["lod2", "osm"]),
    "bldg_count": ([], ["osm"]),
    "energy_infra_count": ([], ["osm"]),
    "water_wastewater_count": ([], ["osm"]),
    "communication_count": ([], ["osm"]),
    "transport_hub_count": ([], ["osm"]),
    "uhi_delta": (
        ["bldg_cov", "road_cov", "green_frac", "forest_frac", "water_frac", "canopy_frac", "svf"],
        ["osm", "param"],
    ),
    "uhi_delta_night": (["bldg_cov", "avg_height", "svf", "water_prox"], ["osm", "param"]),
    "uhi_delta_mean": (["uhi_delta", "uhi_delta_night", "vent_score"], ["param"]),
    "summer_temp_raster": ([], ["dwd"]),
    "summer_night_temp": ([], ["dwd"]),
    "summer_temp_uhi_dev": (["uhi_delta_mean"], []),
    "summer_temp_lapse": (["mean_elevation_m"], []),
    "summer_temp_cell": (
        ["summer_temp_raster", "summer_temp_uhi_dev", "summer_temp_lapse"], []),
    "pop_age_bands": (["pop", "share_over_65"], ["zensus"]),
    # Quellen fließen über die Teil-Zwischenwerte (slope_deg ← DEM, vent_score ← OSM)
    "slope_factor": (["slope_deg"], []),
    "slope_proxy": (["vent_score"], []),
    "slope_deg": ([], ["dem"]),
    "vent_score": ([], ["osm"]),
    "mean_elevation_m": ([], ["dem"]),
    "snow_elevation_factor": (["mean_elevation_m"], ["dem"]),
    "depression_factor": (["twi_norm", "sink_depth_m"], []),
    "depression_proxy": (["imp_frac", "water_adj", "vent_score"], ["osm", "dem"]),
    "twi": (["flow_accum", "slope_deg"], []),
    "twi_norm": (["twi"], []),
    "sink_depth_m": ([], ["dem"]),
    "flow_accum": ([], ["dem"]),
    "pop": ([], ["zensus"]),
    "pop_over_65": (["pop", "share_over_65"], []),
    "pop_under_18": (["pop", "share_under_18"], []),
    "building_count_zensus": ([], ["zensus"]),
    "pop_density": (["pop", "area_km2"], ["zensus", "computed"]),
    "area_km2": ([], []),
    "area_ha": ([], []),
    "industrial": (["bldg_cov", "road_cov", "imp_frac"], ["osm"]),
    "healthcare_access_score": (
        ["dist_hospital_m", "dist_doctor_m", "dist_pharmacy_m"], [],
    ),
    "hot_days": ([], ["dwd"]),
    "frost_days": ([], ["dwd"]),
    "heavy_rain_index": ([], ["dwd"]),
    "storm_days": ([], ["era5"]),
    "mean_temp_rise": (["mean_temp"], []),
    "mean_temp": ([], ["dwd"]),
    "soil_moisture_decline": (["hot_days"], []),
    "surface_water_heating": (["mean_temp"], []),
    "drought_days": (["hot_days"], []),
    "dry_index": (["hot_days"], []),
    "low_flow_days": ([], ["pegelonline"]),
    "glacier_loss_rate": ([], ["dwd"]),
    "snow_decline_rate_pct": ([], ["dwd"]),
    "snow_days": ([], ["dwd"]),
    "sea_level_rise": ([], ["bsh"]),
    "area_m2": ([], []),
    "share_over_65": ([], ["zensus"]),
    "share_under_18": ([], ["zensus"]),
    "share_vulnerable": (["share_over_65", "share_under_18"], []),
    "living_area_per_person": ([], ["zensus"]),
    "owner_share": ([], ["zensus"]),
    "net_cold_rent": ([], ["zensus"]),
    "building_age_mean": ([], ["zensus"]),
    "dist_hospital_m": ([], ["osm"]),
    "dist_doctor_m": ([], ["osm"]),
    "dist_pharmacy_m": ([], ["osm"]),
    "dyke_prox": ([], ["osm"]),
    "emergency_access_score": ([], ["osm"]),
}

# Kurzbeschreibung, wie Zwischenwerte aus Eingaben berechnet werden.
# Keine Quellenangaben in Tooltips — die Quelle steht sichtbar als Box im
# Diagramm (Nutzerwunsch).
INTERMEDIATE_TOOLTIPS: dict[str, str] = {
    "imp_frac": "Versiegelungsgrad = Gebäude- + Straßenanteil, ggf. mit Landnutzungs-Fallback.",
    "imp_lu": "Versiegelungsanteil aus den Landnutzungsklassen der Zelle.",
    "bldg_cov": "Anteil der Zellfläche, die von Gebäudegrundrissen bedeckt ist.",
    "road_cov": "Anteil der Zellfläche, der von Straßen bedeckt ist.",
    "green_frac": "Anteil Grünflächen — Wiesen, Parks, Gärten — in der Zelle.",
    "forest_frac": "Waldanteil der Zelle.",
    "farmland_frac": "Acker- und landwirtschaftlicher Anteil der Zelle.",
    "water_frac": "Wasserflächenanteil der Zelle.",
    "water_adj": ("Kombinierte Gewässernähe: Maximum aus Nachbar-Wasseranteil, "
                  "Gewässernähe-Score und Wasseranteil der Zelle."),
    "water_prox": ("Gewässernähe als Score 0…1 aus der Distanz zum nächsten "
                   "echten Gewässer: max(0; 1 − Distanz/500 m)."),
    "water_dist_m": "Entfernung zum nächsten echten Gewässer in Metern (ohne Gräben).",
    "canopy_frac": "Baumkronenanteil der Zelle.",
    "svf": ("Himmelssichtfaktor (Horizontwinkel-Verfahren) aus dem "
            "Gebäudehöhenraster; LoD2-Höhen wo verfügbar, sonst OSM."),
    "avg_height": ("Mittlere Gebäudehöhe der Zelle (flächengewichtet); "
                   "LoD2-Höhen wo verfügbar, sonst OSM-Heuristik."),
    "vent_score": "Frischluft-Anteil: offene/grüne Nachbarzellen / 8 Nachbarn.",
    "uhi_delta": (
        "Städtische Wärmeinsel ΔT in Kelvin: Aufheizung durch Versiegelung und "
        "Gebäude, abzüglich Kühlung durch Grün, Wasser, Bäume und Himmelssicht."
    ),
    "uhi_delta_night": (
        "Nächtliche Wärmeinsel: enge Straßenschluchten halten die Ausstrahlung "
        "zurück, die Gebäudemasse gibt gespeicherte Wärme ab; Gewässer dämpfen."
    ),
    "uhi_delta_mean": (
        "Wärmeinsel im 24-h-Mittel — die Größe, mit der die Expositions-Wirkungs-"
        "Kurve rechnet, denn diese läuft über die Wochenmitteltemperatur (Tag und "
        "Nacht). Zusätzlich durch den Luftaustausch mit dem Umland gedämpft."
    ),
    "summer_temp_raster": (
        "Sommermitteltemperatur Juni–August aus dem DWD-Monatsraster (1 km), am "
        "Zellmittelpunkt abgegriffen."
    ),
    "summer_night_temp": (
        "Mittlere sommerliche Tagesminimum-Temperatur (DWD-Monatsraster)."
    ),
    "summer_temp_uhi_dev": (
        "Abweichung der Wärmeinsel dieser Zelle vom Mittel ihrer 1-km-Rasterzelle. "
        "Mittelwerttreu, damit der im DWD-Raster bereits enthaltene Wärmeinsel-"
        "Anteil nicht doppelt gezählt wird."
    ),
    "summer_temp_lapse": (
        "Höhenkorrektur gegenüber der mittleren Höhe der 1-km-Rasterzelle "
        "(0,65 K je 100 Höhenmeter)."
    ),
    "summer_temp_cell": (
        "Sommermitteltemperatur der Zelle: Rasterwert plus Wärmeinsel-Abweichung "
        "plus Höhenkorrektur. Bezugsgröße der Expositions-Wirkungs-Kurve."
    ),
    "pop_age_bands": (
        "Bevölkerung je Altersband (<65, 65–74, 75–84, 85+). Menge der 65+ aus dem "
        "Zensus-Anteil, Binnenaufteilung aus den 5-Jahres-Gruppen."
    ),
    "slope_deg": "Hangneigung des Geländes in Grad.",
    "slope_factor": ("Hangneigung min-max-normiert über alle Zellen der Kommune "
                     "→ 0…1; ohne Geländemodell Fallback aus der Belüftung."),
    "slope_proxy": "Hangfaktor-Proxy ohne Geländemodell: 0,3 + 0,4 · (1 − Belüftung).",
    "mean_elevation_m": "Mittlere Geländehöhe der Zelle.",
    "snow_elevation_factor": "Höhenmodulation für Schnee/Gletscher aus der Geländehöhe.",
    "depression_factor": ("Senkenneigung: min(1; 0,55 · TWI normiert + 0,45 · "
                          "Senkentiefe normiert); ohne Geländemodell Fallback aus "
                          "Versiegelung, Gewässernähe und Belüftung."),
    "depression_proxy": "Senken-Proxy aus Versiegelung, Gewässernähe und Belüftung.",
    "twi": ("Topographischer Feuchteindex: TWI = ln(A / tan β) mit A = "
            "Flussakkumulation · Zellfläche und β = Hangneigung."),
    "twi_norm": "TWI min-max-normiert über alle Zellen der Kommune → 0…1.",
    "sink_depth_m": "Senkentiefe: max(0; mittlere Nachbarhöhe − Zellhöhe) in Metern.",
    "flow_accum": "Dem Geländegefälle folgend akkumulierter Wasserfluss (D8).",
    "albedo": "Flächengewichteter Albedo-Mittelwert der Landnutzungsklassen der Zelle.",
    "pop": "Einwohnerzahl der Zelle, direkt aus dem Zensus-100-m-Gitter.",
    "pop_over_65": "Einwohner ≥ 65 Jahre: Einwohner der Zelle · Anteil ≥ 65 / 100.",
    "pop_under_18": "Einwohner < 18 Jahre: Einwohner der Zelle · Anteil < 18 / 100.",
    "building_count_zensus": "Gebäudeanzahl der Zelle aus dem Zensus-Raster.",
    "pop_density": "Bevölkerungsdichte = Einwohner / Zellfläche in km².",
    "area_km2": "Zellfläche in km² aus der Zellgröße.",
    "area_ha": "Zellfläche in Hektar aus der Zellgröße.",
    "industrial": "Industrieflächen-Proxy aus Gebäude-, Straßen- und Versiegelungsanteil.",
    "healthcare_access_score": ("Gesundheitszugang 0…1: 0,50 · Nähe Krankenhaus + "
                                "0,35 · Nähe Arzt + 0,15 · Nähe Apotheke."),
    "hot_days": "Anzahl heißer Tage pro Jahr (DWD-CDC-Raster am Zentroid), regional.",
    "frost_days": "Anzahl Frosttage pro Jahr (DWD-CDC-Raster am Zentroid), regional.",
    "heavy_rain_index": "Starkregenindex aus DWD-CDC-Niederschlagsrastern, regional.",
    "storm_days": "Sturmtage pro Jahr aus der ERA5-Böenklimatologie, regional.",
    "mean_temp_rise": ("Temperaturanstieg gegenüber der Referenzperiode — Proxy "
                       "aus der Jahresmitteltemperatur, regional."),
    "mean_temp": "Jahresmitteltemperatur, regional.",
    "soil_moisture_decline": "Bodenfeuchte-Rückgang — Proxy aus heißen Tagen, regional.",
    "surface_water_heating": ("Gewässererwärmung — Proxy aus der "
                              "Jahresmitteltemperatur, regional."),
    "drought_days": "Trockentage — Proxy aus heißen Tagen (8 + 1,2 · heiße Tage), regional.",
    "dry_index": "Trockenheitsindex 0…1 — Proxy: min(1; heiße Tage / 25), regional.",
    "low_flow_days": "Tage unter mittlerem Niedrigwasser am nächsten Pegel, regional.",
    "glacier_loss_rate": "Gletscherschwund-Rate, regional.",
    "glacier_frac": "Gletscheranteil der Zelle.",
    "snow_decline_rate_pct": "Trend des Schneedecken-Rückgangs, regional.",
    "snow_days": "Schneedeckentage pro Jahr, regional.",
    "sea_level_rise": "Meeresspiegelanstieg, regional.",
    "area_m2": "Zellfläche in m² aus der Rastergeometrie: 100 × 100 m.",
    "share_over_65": "Anteil der Bevölkerung ab 65 Jahren in der Zelle.",
    "share_under_18": "Anteil der Bevölkerung unter 18 Jahren in der Zelle.",
    "share_vulnerable": ("Anteil vulnerabler Personen an der Zellbevölkerung: "
                         "Ältere ab 65 und Kinder unter 18, gedeckelt bei 100 %."),
    "living_area_per_person": "Wohnfläche je Person, direkt aus dem Zensus-Raster.",
    "owner_share": "Eigentümerquote, direkt aus dem Zensus-Raster.",
    "net_cold_rent": "Mittlere Nettokaltmiete je m², direkt aus dem Zensus-Raster.",
    "building_age_mean": ("Mittleres Baujahr aus den Zensus-Baujahrsklassen "
                          "(gebäudegewichtete Klassenmitten)."),
    "dist_hospital_m": "Distanz zum nächsten Krankenhaus in Metern.",
    "dist_doctor_m": "Distanz zur nächsten Arztpraxis/Klinik in Metern.",
    "dist_pharmacy_m": "Distanz zur nächsten Apotheke in Metern.",
    "dyke_prox": "Nähe-Score zu Deich-/Küstenschutzanlagen aus der Distanz.",
    "emergency_access_score": "Erreichbarkeit von Feuerwehr/Rettung als Score aus der Distanz.",
}

COMPUTED_TOOLTIPS: dict[str, str] = {
    "pop_density": "Einwohner geteilt durch Zellfläche in km².",
    "area_km2": "Zellgröße² umgerechnet in km².",
    "area_ha": "Zellgröße² umgerechnet in Hektar.",
    "industrial": "Kombination aus Gebäude-, Straßen- und Versiegelungsanteil.",
}

COMPUTED_RESOLVER_LINEAGE: dict[str, tuple[list[str], list[str]]] = {
    "industrial": (["bldg_cov", "road_cov", "imp_frac"], ["osm"]),
    "area_ha": ([], []),
    "area_km2": ([], []),
    "pop_density": (["pop", "area_km2"], ["zensus"]),
}

# Benannte Modellparameter, die als "param"-Quelle in CELL_INPUT_LINEAGE auftauchen
CELL_PARAM_LABELS: dict[str, tuple[str, str]] = {
    "uhi_delta": (
        "UHI-Koeffizienten (α…ε, τ)",
        "Übersetzen die dimensionslosen Flächenanteile in Kelvin — "
        "editierbar in der Konfiguration (uhi.*)",
    ),
    "uhi_delta_night": (
        "UHI-Nachtkoeffizienten (ε, ζ)",
        "Straßenschluchten- und Wärmespeicher-Beitrag der Nacht — "
        "editierbar in der Konfiguration (uhi.*)",
    ),
    "uhi_delta_mean": (
        "Tagesmittel- und Lüftungsfaktoren",
        "Nachtgewicht, Umrechnung auf das Tagesmittel und Dämpfung durch "
        "Durchlüftung — editierbar in der Konfiguration (uhi.*)",
    ),
}

COLLAPSE_GROUPS = [
    {"id": "sources", "label": "Quellen", "default_collapsed": False},
    {"id": "intermediates", "label": "Zwischenergebnisse", "default_collapsed": False},
    {"id": "indicators", "label": "H / E / V", "default_collapsed": False},
    {"id": "pathways", "label": "Wirkungsketten", "default_collapsed": False},
    {"id": "outcome", "label": "Ergebnis", "default_collapsed": False},
]


def _regional_source(label: str) -> str:
    ll = label.lower()
    if "zensus" in ll or "bevölkerung" in ll or "demo" in ll:
        return "zensus"
    if "bsh" in ll or "meeresspiegel" in ll:
        return "bsh"
    if "dwd" in ll or "wetter" in ll or "temperatur" in ll or "schnee" in ll or "regen" in ll:
        return "dwd"
    return "dwd"


# Quell-Label → kanonische Quell-ID (Reihenfolge = Priorität). Verhindert, dass
# benannte Quellen wie "AWS Terrarium DEM" als anonymer "Parameter"-Kasten enden.
_SOURCE_LABEL_PATTERNS: list[tuple[str, tuple[str, ...]]] = [
    ("osm", ("osm", "openstreetmap")),
    ("dwd", ("dwd", "wetterdienst")),
    ("zensus", ("zensus", "destatis")),
    ("dem", ("dem", "terrarium", "gelände")),
    ("lod2", ("lod2",)),
    ("bsh", ("bsh",)),
    ("pegelonline", ("pegelonline", "pegel")),
    ("era5", ("era5",)),
]


def _resolve_source_id(label: str) -> str:
    ll = label.lower()
    for sid, patterns in _SOURCE_LABEL_PATTERNS:
        if any(p in ll for p in patterns):
            return sid
    return "param"


class LineageBuilder:
    def __init__(self) -> None:
        self.nodes: dict[str, dict] = {}
        self.edges: list[dict] = []
        self._edge_keys: set[tuple[str, str, str | None]] = set()

    def add_node(
        self,
        node_id: str,
        ntype: str,
        label: str,
        *,
        column: int = 0,
        collapse_group: str = "intermediates",
        meta: dict | None = None,
    ) -> str:
        if node_id not in self.nodes:
            self.nodes[node_id] = {
                "id": node_id,
                "type": ntype,
                "label": label,
                "column": column,
                "collapse_group": collapse_group,
                "meta": meta or {},
            }
        return node_id

    def add_edge(
        self,
        source: str,
        target: str,
        *,
        label: str | None = None,
        parameter_id: str | None = None,
        meta: dict | None = None,
    ) -> None:
        key = (source, target, label)
        if key in self._edge_keys:
            return
        self._edge_keys.add(key)
        edge: dict[str, Any] = {
            "id": f"e:{source}:{target}:{len(self.edges)}",
            "source": source,
            "target": target,
            "label": label,
            "parameter_id": parameter_id,
        }
        if meta:
            edge["meta"] = meta
        self.edges.append(edge)

    def _wire_operator_chain(
        self,
        prefix: str,
        steps: list[dict],
        input_ids: list[str],
        target_id: str,
        *,
        cell_key_map: dict[str, str] | None = None,
    ) -> None:
        cell_key_map = dict(cell_key_map or {})
        step_outputs: dict[str, str] = dict(cell_key_map)
        last_op: str | None = None

        for i, step in enumerate(steps):
            op_id = f"op:{step['op_kind']}:{prefix}:{i}"
            _add_operator_compute(self, op_id, step)
            # Skalierungs-Konstanten ohne Registry-Parameter sind am Operator
            # nicht editierbar — der Faktor erscheint deshalb als benannter
            # (schreibgeschützter) Parameterknoten vor dem Operator.
            if (
                step.get("op_kind") in ("scaling", "scale_factor")
                and not step.get("parameter_id")
            ):
                factor = step.get("value", step.get("factor"))
                if factor is not None:
                    pnid = self.ensure_const_parameter(
                        f"const:{prefix}:{i}",
                        step.get("param_label") or "Skalierungsfaktor",
                        value=factor, unit=step.get("unit", "×"),
                        source="Modellkonstante (fest im Rechenmodell verdrahtet)",
                    )
                    self.add_edge(pnid, op_id)
            input_keys = step.get("input_keys")

            if input_keys:
                for ik in input_keys:
                    src_id = step_outputs.get(ik) or cell_key_map.get(ik) or f"int:{ik}"
                    self.add_edge(src_id, op_id)
                for ik in input_keys:
                    step_outputs[ik] = op_id
            elif i == 0:
                for pid in input_ids:
                    self.add_edge(pid, op_id)
            elif last_op:
                self.add_edge(last_op, op_id)

            last_op = op_id

        if last_op:
            self.add_edge(last_op, target_id)

    def ensure_source(self, src_key: str) -> str:
        nid = f"src:{src_key}"
        label, desc = SOURCE_IDS.get(src_key, (src_key.upper(), src_key))
        self.add_node(nid, "source", label, column=0, collapse_group="sources",
                      meta={"description": desc, "prov": "extern"})
        return nid

    def ensure_parameter(
        self,
        parameter_id: str,
        label: str,
        *,
        unit: str = "",
        source: str = "",
    ) -> str:
        nid = f"src:param:{parameter_id}"
        self.add_node(
            nid, "parameter", label, column=0, collapse_group="sources",
            meta={
                "parameter_id": parameter_id,
                "unit": unit,
                "description": source or "Modellannahme",
                "prov": "param",
            },
        )
        return nid

    def ensure_const_parameter(
        self,
        node_key: str,
        label: str,
        *,
        value: Any = None,
        unit: str = "",
        source: str = "",
        parameter_id: str | None = None,
    ) -> str:
        """Benannter Parameterknoten für Modellkonstanten.

        Zeigt Namen + Wert im Diagramm; editierbar nur, wenn eine
        ``parameter_id`` auf einen Registry-Parameter verweist (override-fähig).
        """
        nid = f"src:param:{node_key}"
        meta: dict[str, Any] = {
            "unit": unit,
            "description": source or "Modellannahme",
            "prov": "param",
        }
        if parameter_id:
            meta["parameter_id"] = parameter_id
        if value is not None:
            meta["value"] = value
        self.add_node(nid, "parameter", label, column=0, collapse_group="sources", meta=meta)
        return nid

    def expand_cell_key(self, key: str, *, _visited: set[str] | None = None) -> str:
        """Expandiert Zell-Schlüssel → Zwischenknoten → Quellen. Gibt Knoten-ID zurück."""
        if _visited is None:
            _visited = set()
        if key in _visited:
            return f"int:{key}"
        _visited.add(key)

        int_id = f"int:{key}"
        label = INTERMEDIATE_LABELS.get(key, key)
        self.add_node(int_id, "intermediate", label, column=1, collapse_group="intermediates",
                      meta={"cell_key": key})

        input_ids: list[str] = []
        cell_key_map: dict[str, str] = {}
        if key in CELL_DIRECT:
            for src in CELL_DIRECT[key]:
                input_ids.append(self.ensure_source(src))
        else:
            spec = CELL_INPUT_LINEAGE.get(key)
            if not spec:
                input_ids.append(self.ensure_source("osm"))
            else:
                intermediates, sources = spec
                for src in sources:
                    if src == "param":
                        p_label, p_desc = CELL_PARAM_LABELS.get(
                            key, ("Modellparameter", "Modellannahme"),
                        )
                        input_ids.append(self.ensure_const_parameter(
                            f"cell:{key}", p_label, source=p_desc,
                        ))
                    else:
                        input_ids.append(self.ensure_source(src))
                for sub in intermediates:
                    sub_id = self.expand_cell_key(sub, _visited=_visited)
                    cell_key_map[sub] = sub_id
                    input_ids.append(sub_id)

        steps = CELL_OPERATORS.get(key)
        if steps:
            self._wire_operator_chain(
                key, steps, input_ids, int_id, cell_key_map=cell_key_map,
            )
        else:
            for pid in input_ids:
                self.add_edge(pid, int_id)
        return int_id

    def ensure_indicator(self, code: str, category: str) -> str:
        """Indikator-Untergraph einmalig aufbauen und Knoten-ID zurückgeben."""
        ind_id = f"ind:{code}"
        if ind_id in self.nodes:
            return ind_id
        sub = build_indicator_lineage(code, category, include_norm=False)
        _merge_builder(self, sub)
        return ind_id

    def expand_computed(self, resolver_key: str, *, _visited: set[str] | None = None) -> str:
        spec = COMPUTED_RESOLVER_LINEAGE.get(resolver_key)
        if not spec:
            return self.ensure_source("computed")
        int_id = f"int:computed:{resolver_key}"
        label = INTERMEDIATE_LABELS.get(resolver_key, resolver_key)
        self.add_node(int_id, "intermediate", label, column=1, collapse_group="intermediates",
                      meta={"cell_key": resolver_key})
        intermediates, sources = spec
        input_ids: list[str] = []
        cell_key_map: dict[str, str] = {}
        for src in sources:
            input_ids.append(self.ensure_source(src))
        for sub in intermediates:
            sub_id = self.expand_cell_key(sub, _visited=_visited or set())
            cell_key_map[sub] = sub_id
            input_ids.append(sub_id)
        steps = CELL_OPERATORS.get(resolver_key)
        if steps:
            self._wire_operator_chain(
                f"computed:{resolver_key}", steps, input_ids, int_id,
                cell_key_map=cell_key_map,
            )
        else:
            for pid in input_ids:
                self.add_edge(pid, int_id)
        return int_id

    def expand_recipe_input_to_id(
        self,
        inp: dict,
        *,
        indicator_code: str | None = None,
        indicator_category: str | None = None,
    ) -> str:
        """Expandiert einen Rezept-Input und gibt die Blatt-Knoten-ID zurück."""
        prov = inp.get("prov", formulas.EXTERN)
        src_type = inp.get("source", "cell")
        key = inp.get("key", "")

        if src_type == "const" or prov == formulas.PARAM:
            # Jeder Formel-Parameter wird benannt (Label + Wert) angezeigt;
            # editierbar (parameter_id) nur, wenn override-fähig in der Registry.
            label = inp.get("label") or key or "Modellannahme"
            if key.startswith("__") or not key:
                return self.ensure_const_parameter(
                    f"const:{indicator_code or 'global'}:{label}", label,
                    value=inp.get("value"), unit=inp.get("unit", ""),
                    source=inp.get("doc_source") or "Modellannahme (Formelrezept)",
                )
            pid: str | None = None
            if inp.get("overridable"):
                pid = (
                    f"{indicator_category}.{indicator_code}.param.{key}"
                    if indicator_code and indicator_category
                    else key
                )
            return self.ensure_const_parameter(
                f"param:{indicator_category or ''}.{indicator_code or ''}.{key}", label,
                value=inp.get("value"), unit=inp.get("unit", ""),
                source=inp.get("doc_source") or "Modellannahme (Formelrezept)",
                parameter_id=pid,
            )

        if src_type == "regional":
            # Regionale Größen durch die Zellkey-Maschinerie routen — sonst
            # erscheint statt der echten Kette (z. B. low_flow_days ←
            # PEGELONLINE) nur eine per Label-Heuristik geratene Quellbox.
            if key in CELL_OPERATORS or key in CELL_INPUT_LINEAGE or key in CELL_DIRECT:
                return self.expand_cell_key(key)
            return self.ensure_source(_regional_source(inp.get("label", "")))

        if src_type == "socio":
            # BBSR-INKAR-Kennzahlen (Sozioökonomie je Gemeinde) — vorher
            # fiel dieser Zweig fälschlich auf die OSM-Quellbox durch.
            return self.ensure_source("inkar")

        if src_type == "demo":
            # Bekannte Zell-Schlüssel (z. B. share_vulnerable) als echte
            # Ableitungskette zeigen statt als anonyme Zensus-Direktquelle.
            if key in CELL_OPERATORS or key in CELL_INPUT_LINEAGE:
                return self.expand_cell_key(key)
            return self.ensure_source("zensus")

        if src_type == "computed":
            resolver = inp.get("value") or key
            return self.expand_computed(str(resolver))

        if src_type == "hev":
            ref_code = str(inp.get("value") or key).upper()
            if ref_code in catalog.HAZARDS_BY_CODE:
                cat = "hazards"
            elif ref_code in catalog.EXPOSURES_BY_CODE:
                cat = "exposures"
            elif ref_code in catalog.VULNERABILITIES_BY_CODE:
                cat = "vulnerabilities"
            else:
                cat = "hazards"
            return self.ensure_indicator(ref_code, cat)

        if src_type == "cell" or src_type == "auxiliary":
            cell_key = key if key and not key.startswith("__") else None
            if not cell_key:
                label = inp.get("label", "")
                for ck in CELL_INPUT_LINEAGE:
                    if ck in label.lower().replace(" ", "_"):
                        cell_key = ck
                        break
            if cell_key:
                return self.expand_cell_key(cell_key)
            return self.ensure_source("osm")

        return self.ensure_source("osm")

    def expand_recipe_input(self, inp: dict, target_id: str) -> None:
        sid = self.expand_recipe_input_to_id(inp)
        self.add_edge(sid, target_id)

    def build(self) -> dict:
        return {
            "nodes": list(self.nodes.values()),
            "edges": self.edges,
            "collapse_groups": COLLAPSE_GROUPS,
        }


def _indicator_node_type(category: str) -> str:
    if category == "hazards":
        return "hazard"
    if category == "exposures":
        return "exposure"
    if category == "vulnerabilities":
        return "vulnerability"
    return "intermediate"


def _incoming_labels(
    node_id: str,
    edges: list[dict],
    nodes_by_id: dict[str, dict],
) -> list[str]:
    """Fachliche Eingaben eines Knotens für die "Eingaben:"-Tooltip-Zeile.

    Quell-Boxen (OSM/DWD/…) werden nicht aufgezählt — sie stehen sichtbar im
    Diagramm und sind keine inhaltliche Erklärung. Vorgelagerte Operatoren
    sind Verkettung, keine Eingabe; ihre Labels sind ohnehin leer/symbolisch.
    """
    labels: list[str] = []
    for e in edges:
        if e["target"] != node_id:
            continue
        src = nodes_by_id.get(e["source"])
        if not src or src["type"] in ("source", "operator") or not src["label"]:
            continue
        if src["label"] not in labels:
            labels.append(src["label"])
    return labels


def _indicator_tooltip(code: str, unit: str) -> str:
    recipe = formulas.get_recipe(code)
    formula = recipe.get("formula", "")
    inputs = [
        inp.get("label", inp.get("key", ""))
        for inp in recipe.get("inputs", [])
        if inp.get("key") != "__source"
    ]
    lines = [f"Berechnung: {formula}" if formula else "Berechnung aus Eingabewerten"]
    if inputs:
        lines.append(f"Eingaben: {', '.join(inputs)}")
    if unit:
        lines.append(f"Einheit: {unit}")
    lo = catalog.INDICATOR_BY_CODE.get(code, {}).get("norm_min")
    hi = catalog.INDICATOR_BY_CODE.get(code, {}).get("norm_max")
    if lo is not None and hi is not None:
        lines.append(f"Normierung: Skala {lo}…{hi}")
    return "\n".join(lines)


# Tooltip-Titel: Symbol-/Kürzel-Labels der Operator-Pills ausgeschrieben.
# Regel: Kein unerklärtes Kürzel als alleiniger Titel — das Symbol bleibt in
# Klammern erhalten (Wiedererkennung zur Pill und zu den Formeln).
_SYMBOL_TITLES: dict[str, str] = {
    "+": "Addition",
    "×": "Multiplikation",
    "÷": "Division",
    "AF": "Attributable Fraktion (AF)",
    "g(V̂)": "Vulnerabilitäts-Modifikator g(V̂)",
    "Σ Zellen": "Summe über Zellen (Σ)",
    "Σ": "Summe (Σ)",
    "÷ Referenz": "Verhältnis zur Referenz",
    "P90": "90. Perzentil (P90)",
}

# Fallback-Titel je Operator-Klasse (wenn kein beschreibendes Label vorliegt)
_KIND_TITLES: dict[str, str] = {
    "add": "Addition",
    "multiply": "Multiplikation",
    "divide": "Division",
    "max": "Maximum",
    "min": "Minimum",
    "scale_factor": "Skalierung",
    "scaling": "Skalierung",
    "formula": "Formel",
    "count": "Zählung",
    "ratio": "Verhältnis",
    "neighbor": "Nachbarschaftsanalyse",
    "distance": "Distanzmessung",
    "distance_score": "Nähe-Score",
    "mean": "Mittelwert",
    "lookup": "Regionalwert",
    "constant": "Konstantwert",
    "derived_index": "Ableitung",
    "weighted_sum": "Gewichtete Summe",
    "sum_cells": "Summe über Zellen (Σ)",
    "p90": "90. Perzentil (P90)",
    "af": "Attributable Fraktion (AF)",
    "gv": "Vulnerabilitäts-Modifikator g(V̂)",
    "damage_curve": "Schadenskurve",
    "intensity": "Hazard-Intensität",
    "norm": "Normierung",
    "clamp": "Begrenzung",
    "coverage": "Anteil",
}


def _operator_title(kind: str, label: str) -> str:
    if label in _SYMBOL_TITLES:
        return _SYMBOL_TITLES[label]
    return label or _KIND_TITLES.get(kind, kind or "Operator")


def _fmt_de(val: Any) -> str:
    """Zahl deutsch formatiert, nie wissenschaftliche Notation (3.5e+06)."""
    try:
        f = float(val)
    except (TypeError, ValueError):
        return str(val)
    if f == int(f) and abs(f) >= 1000:
        return f"{int(f):,}".replace(",", ".")
    return f"{f:g}".replace(".", ",")


def _tooltip_for_node(
    node: dict,
    nodes_by_id: dict[str, dict],
    edges: list[dict],
) -> str:
    ntype = node["type"]
    meta = node.get("meta") or {}
    label = node["label"]
    nid = node["id"]
    incoming = _incoming_labels(nid, edges, nodes_by_id)

    if ntype == "source":
        desc = meta.get("description", "Externe Datenquelle")
        return f"{label}\n{desc}\nWird als Eingabe in nachfolgende Merkmale eingespeist."

    if ntype == "parameter":
        lines = [label, meta.get("description", "Modellannahme")]
        val = meta.get("value")
        if val is not None:
            lines.append(f"Wert: {_fmt_de(val)} {meta.get('unit', '')}".strip())
        return "\n".join(lines)

    if ntype == "intermediate":
        cell_key = meta.get("cell_key", "")
        if meta.get("note"):
            base = str(meta["note"])
        elif nid.startswith("int:computed:"):
            resolver = nid.split("int:computed:", 1)[-1]
            base = COMPUTED_TOOLTIPS.get(resolver, f"Berechneter Zwischenwert ({label}).")
        else:
            base = INTERMEDIATE_TOOLTIPS.get(cell_key, f"Zellbezogener Zwischenwert ({label}).")
        if incoming:
            return f"{base}\nEingaben: {', '.join(incoming)}"
        return base

    if ntype in ("hazard", "exposure", "vulnerability"):
        code = meta.get("code", "")
        if code:
            return _indicator_tooltip(code, meta.get("unit", ""))
        formula = meta.get("formula", "")
        if formula:
            lines = [f"Berechnung: {formula}"]
            if incoming:
                lines.append(f"Eingaben: {', '.join(incoming)}")
            return "\n".join(lines)

    if ntype == "pathway":
        chain = meta.get("chain_label", "")
        type_label = meta.get("type_label", "")
        weight = meta.get("weight")
        lines = [label]
        if chain:
            lines.append(f"Zusammensetzung: {chain}")
        if type_label:
            lines.append(f"Typ: {type_label}")
        weight_str = f"{weight:g}" if isinstance(weight, (int, float)) else "Gewicht"
        lines.append(
            f"Berechnung: {weight_str} · normierte Gefahr · Betroffenheit · Empfindlichkeit"
        )
        return "\n".join(lines)

    if ntype == "operator":
        kind = meta.get("op_kind", "")
        note = meta.get("note", "")
        label_op = meta.get("label", "")
        if kind == "multiplier":
            return _tooltip_for_node(
                {**node, "meta": {**meta, "op_kind": "scaling"}}, nodes_by_id, edges,
            )
        if kind == "scaling":
            val = meta.get("value")
            unit = meta.get("unit", "")
            scale = meta.get("scale", "pop")
            lines = [label_op or "Skalierung"]
            if note:
                lines.append(note)
            if val is not None:
                value_label = "Kostensatz" if scale == "cost" else "Referenzwert"
                lines.append(f"{value_label}: {_fmt_de(val)} {unit}".strip())
            if scale in _SCALE_FORMULAS:
                lines.append(f"Berechnung: {_SCALE_FORMULAS[scale]}")
            if incoming:
                lines.append(f"Eingaben: {', '.join(incoming)}")
            return "\n".join(lines)
        if kind == "norm":
            lo, hi = meta.get("norm_min"), meta.get("norm_max")
            unit = meta.get("unit", "")
            lines = [
                "Normierung",
                f"Untergrenze {lo} {unit} → normiert 0".strip(),
                f"Obergrenze {hi} {unit} → normiert 1".strip(),
            ]
            if incoming:
                lines.append(f"Eingaben: {', '.join(incoming)}")
            return "\n".join(lines)
        # Einheitliche Komposition für alle übrigen Operator-Klassen:
        # Titel (Kürzel ausgeschrieben) → Notiz/Formel → Eingaben.
        lines = [_operator_title(kind, label_op)]
        if note:
            lines.append(note)
        if incoming:
            lines.append(f"Eingaben: {', '.join(incoming)}")
        return "\n".join(lines)

    if ntype == "aggregation":
        short = meta.get("short", "stärkste Wirkungskette (Maximum)")
        formula = meta.get("formula", "")
        lines = [f"{label}: {short}"]
        if formula:
            lines.append(f"Berechnung: {formula}")
        if incoming:
            lines.append(f"Eingaben: {', '.join(incoming)}")
        return "\n".join(lines)

    if ntype in ("outcome", "norm"):
        if meta.get("is_norm"):
            lo, hi = meta.get("norm_min"), meta.get("norm_max")
            unit = meta.get("unit", "")
            return (
                f"Normiertes Ergebnis auf Skala {lo}…{hi} {unit}".strip()
                + (f"\nEingaben: {', '.join(incoming)}" if incoming else "")
            )
        formula = meta.get("formula", "")
        ref = meta.get("ref_value")
        unit = meta.get("unit", "")
        result_kind = meta.get("result_kind")
        lines = [label]
        if result_kind == "index":
            header = meta.get("formula_header", "")
            lines.append("Screening-Ergebnis (Schicht A), dimensionslos 0–100.")
            if header:
                lines.append(header)
        elif result_kind == "native":
            lines.append(f"Absolutes Ergebnis (Schicht B) in {unit}".strip() + ".")
        elif result_kind == "eur":
            lines.append("Monetäres Ergebnis (Schicht B) in €/Jahr.")
        elif result_kind == "raw":
            lines.append(
                (f"Kartenwert in {unit} — " if unit else "Kartenwert — ")
                + "Rohwert, nicht normiert."
            )
        if ref is not None:
            lines.append(f"Referenzfall: {_fmt_de(ref)} {unit}".strip())
        if formula:
            lines.append(f"Berechnung: {formula}")
        elif incoming and result_kind is None:
            lines.append(f"Eingaben: {', '.join(incoming)}")
        return "\n".join(lines)

    if incoming:
        return f"{label}\nEingaben: {', '.join(incoming)}"
    return label


def _add_operator_compute(
    b: "LineageBuilder",
    op_id: str,
    step: dict,
    *,
    collapse_group: str = "intermediates",
) -> str:
    meta: dict[str, Any] = {
        "op_kind": step["op_kind"],
        "label": step.get("label", ""),
        "note": step.get("note", ""),
    }
    for k, v in step.items():
        if k not in ("op_kind", "label", "note", "input_keys"):
            meta[k] = v
    b.add_node(op_id, "operator", "", column=0, collapse_group=collapse_group, meta=meta)
    return op_id


_SCALE_FORMULAS = {
    "pop": "Index/100 · Einwohner_zelle/100.000",
    "area": "Index/100 · Fläche/50 km²",
    "flat": "Outcome = Referenz · (P90-Index/100)",
}

_SCALE_SOURCES = {
    "pop": "Referenz-Outcome bei Index 100 / 100.000 Ew. (Risikokatalog)",
    "area": "Referenz-Outcome bei Index 100 / 50 km² (Risikokatalog)",
    "flat": "Referenz-Outcome bei P90-Index 100, kommunenweit (Risikokatalog)",
}


def _add_operator_scaling(
    b: "LineageBuilder",
    risk_code: str,
    ref: float,
    unit: str,
    scale: str = "pop",
) -> str:
    op_id = f"op:scaling:{risk_code}"
    b.add_node(
        op_id, "operator", "",
        column=0, collapse_group="outcome",
        meta={
            "op_kind": "scaling",
            "parameter_id": f"risks.{risk_code}.ref_value",
            "value": ref,
            "unit": unit,
            "scale": scale,
            "source": _SCALE_SOURCES.get(scale, _SCALE_SOURCES["flat"]),
            "note": "Skalierung des Indexes auf den Referenz-Outcome.",
        },
    )
    return op_id


def _add_operator_multiply(b: "LineageBuilder", op_id: str) -> str:
    b.add_node(
        op_id, "operator", "",
        column=0, collapse_group="pathways",
        meta={
            "op_kind": "multiply",
            "label": "×",
            "note": (
                "Gefahr × Betroffenheit × Empfindlichkeit (jeweils normiert 0…1; "
                "Normierungsgrenzen im Diagramm des jeweiligen Einflusses).\n"
                r"$$\hat{H} \cdot \hat{E} \cdot \hat{V}$$"
            ),
        },
    )
    return op_id


def _add_operator_max(b: "LineageBuilder") -> str:
    op_id = "op:max:index"
    b.add_node(
        op_id, "operator", "",
        column=0, collapse_group="outcome",
        meta={
            "op_kind": "max",
            "label": "Maximum",
            "note": (
                "Stärkste Wirkungskette (0–100): Die Kette mit dem höchsten gewichteten "
                "Produkt bestimmt den Index; die Kettenzahl beeinflusst ihn nicht.\n"
                r"$$\mathrm{Index} = 100 \cdot \max_{p}\,\bigl(w_{p} \cdot \hat{H} \cdot \hat{E} \cdot \hat{V}\bigr)$$"
            ),
        },
    )
    return op_id


def _add_operator_multiplier(
    b: "LineageBuilder",
    risk_code: str,
    ref: float,
    unit: str,
    scale: str = "pop",
) -> str:
    return _add_operator_scaling(b, risk_code, ref, unit, scale)


def _add_operator_norm(
    b: "LineageBuilder",
    code: str,
    category: str,
    lo: float,
    hi: float,
    unit: str,
    source: str = "",
) -> str:
    op_id = f"op:norm:{code}"
    b.add_node(
        op_id, "operator", "",
        column=0, collapse_group="outcome",
        meta={
            "op_kind": "norm",
            "norm_min": lo,
            "norm_max": hi,
            "unit": unit,
            "param_min_id": f"{category}.{code}.norm_min",
            "param_max_id": f"{category}.{code}.norm_max",
            "source": source or "Risikokatalog (Normierungsskala)",
        },
    )
    return op_id


def _add_operator_weight(
    b: "LineageBuilder",
    pathway_idx: int,
    pathway_type: str,
    weight: float,
) -> str:
    """Gewichte werden auf Kanten (Pfad → Maximum) gelegt."""
    return f"op:weight:{pathway_idx}"




def _assign_layout_rows(graph: dict) -> dict:
    """Horizontale Zeilen pro Zwischenwert-Kette (meta.layout_row)."""
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    row_by_int: dict[str, int] = {}
    row_cursor = 0
    for n in sorted(nodes, key=lambda x: x.get("label", "")):
        if n["type"] != "intermediate":
            continue
        ck = (n.get("meta") or {}).get("cell_key") or n["id"]
        if ck not in row_by_int:
            row_by_int[ck] = row_cursor
            row_cursor += 1

    node_row: dict[str, int] = {}
    for n in nodes:
        if n["type"] == "intermediate":
            ck = (n.get("meta") or {}).get("cell_key") or n["id"]
            node_row[n["id"]] = row_by_int.get(ck, 0)

    incoming: dict[str, list[str]] = {}
    outgoing: dict[str, list[str]] = {}
    for e in edges:
        incoming.setdefault(e["target"], []).append(e["source"])
        outgoing.setdefault(e["source"], []).append(e["target"])

    pipeline_types = {"source", "parameter", "intermediate", "operator"}

    def rows_of(node_ids: list[str]) -> list[int]:
        return [node_row[nid] for nid in node_ids if nid in node_row]

    for _ in range(len(nodes) + 2):
        changed = False
        for n in nodes:
            nid = n["id"]
            if nid in node_row or n["type"] not in pipeline_types:
                continue
            preds = rows_of(incoming.get(nid, []))
            if preds:
                if n["type"] == "operator" and len(preds) > 1:
                    node_row[nid] = max(preds)
                else:
                    node_row[nid] = preds[0]
                changed = True
        for n in nodes:
            nid = n["id"]
            if nid in node_row or n["type"] not in ("source", "parameter"):
                continue
            succ_rows = rows_of(outgoing.get(nid, []))
            if succ_rows:
                node_row[nid] = min(succ_rows)
                changed = True
        if not changed:
            break

    for _ in range(len(nodes) + 2):
        changed = False
        for e in edges:
            src, tgt = e["source"], e["target"]
            if tgt in node_row and src not in node_row:
                sn = next((n for n in nodes if n["id"] == src), None)
                if sn and sn["type"] in pipeline_types:
                    node_row[src] = node_row[tgt]
                    changed = True
            elif src in node_row and tgt not in node_row:
                tn = next((n for n in nodes if n["id"] == tgt), None)
                if tn and tn["type"] in pipeline_types:
                    node_row[tgt] = node_row[src]
                    changed = True
        if not changed:
            break

    for n in nodes:
        rid = node_row.get(n["id"])
        if rid is not None:
            n.setdefault("meta", {})["layout_row"] = rid

    return graph


def _assign_columns(graph: dict) -> dict:
    """Longest-Path-Layering: col(n) = max(col(pred)) + 1 (Quellen/Parameter = 0).

    Garantiert col(src) < col(tgt) für JEDE Kante (Pfeile strikt links→rechts);
    Ergebnisknoten ohne ausgehende Kante werden rechtsbündig auf die maximale
    Spalte gesetzt (Index-/€-Ergebnis nebeneinander am rechten Rand).
    """
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    cols: dict[str, int] = {n["id"]: 0 for n in nodes}
    for _ in range(len(nodes) + 4):
        changed = False
        for e in edges:
            src, tgt = e["source"], e["target"]
            if src in cols and tgt in cols:
                new_col = cols[src] + 1
                if new_col > cols[tgt]:
                    cols[tgt] = new_col
                    changed = True
        if not changed:
            break
    has_outgoing = {e["source"] for e in edges}
    max_col = max(cols.values(), default=0)
    for n in nodes:
        if n["type"] == "outcome" and n["id"] not in has_outgoing:
            cols[n["id"]] = max_col
        n["column"] = cols.get(n["id"], 0)
    return graph


def _finalize_graph(graph: dict) -> dict:
    graph = _assign_columns(graph)
    graph = _assign_layout_rows(graph)
    return _enrich_tooltips(graph)


def _enrich_tooltips(graph: dict) -> dict:
    """Einzige Schreibquelle für meta["tooltip"] — komponiert IMMER neu.

    Autorentexte liegen unter meta["note"]; Titel und die maschinelle
    "Eingaben:"-Zeile (aus den echten Kanten) kommen aus _tooltip_for_node.
    So kann die Eingaben-Legende nicht vergessen werden oder veralten.
    """
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    nodes_by_id = {n["id"]: n for n in nodes}
    for n in nodes:
        n.setdefault("meta", {})["tooltip"] = _tooltip_for_node(n, nodes_by_id, edges)
    return graph


def _find_result_ids(nodes: list[dict]) -> list[str]:
    """Alle Ergebnisknoten (Outcome); Fallback: rechtester Norm-Op/Norm-Knoten."""
    result_ids = [n["id"] for n in nodes if n["type"] == "outcome"]
    if result_ids:
        return result_ids
    norm_ops = [
        n for n in nodes
        if n["type"] == "operator" and (n.get("meta") or {}).get("op_kind") == "norm"
    ]
    if norm_ops:
        return [max(norm_ops, key=lambda n: n.get("column", 0))["id"]]
    norms = [n for n in nodes if n["type"] == "norm"]
    if norms:
        return [max(norms, key=lambda n: n.get("column", 0))["id"]]
    return []


def _prune_lineage(graph: dict) -> dict:
    """Entfernt Knoten, die auf keinem Pfad zu einem Ergebnisknoten liegen."""
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    result_ids = _find_result_ids(nodes)
    if not result_ids:
        return _finalize_graph(graph)

    rev: dict[str, list[str]] = {}
    for e in edges:
        rev.setdefault(e["target"], []).append(e["source"])

    reachable: set[str] = set()
    stack = list(result_ids)
    while stack:
        nid = stack.pop()
        if nid in reachable:
            continue
        reachable.add(nid)
        stack.extend(rev.get(nid, []))

    nodes2 = [n for n in nodes if n["id"] in reachable]
    ids = {n["id"] for n in nodes2}
    edges2 = [e for e in edges if e["source"] in ids and e["target"] in ids]
    return _finalize_graph({**graph, "nodes": nodes2, "edges": edges2})


def build_indicator_lineage(code: str, category: str, *, include_norm: bool = True) -> dict:
    """Quellen → Zwischen → Indikator → (optional) Normierung."""
    b = LineageBuilder()
    meta = catalog.INDICATOR_BY_CODE.get(code) or catalog.AUXILIARY_BY_CODE.get(code, {})
    name = meta.get("name", code)
    ntype = _indicator_node_type(category) if category != "auxiliary" else "intermediate"

    ind_id = f"ind:{code}"
    b.add_node(
        ind_id, ntype, name, column=2, collapse_group="indicators",
        meta={
            "code": code,
            "unit": meta.get("unit", ""),
            "formula": formulas.get_recipe(code).get("formula", ""),
            "norm_min": meta.get("norm_min"),
            "norm_max": meta.get("norm_max"),
        },
    )

    recipe = formulas.get_recipe(code)
    steps = formula_operators_for(code, recipe.get("formula", ""))
    input_ids: list[str] = []
    param_ids: list[str] = []
    cell_key_map: dict[str, str] = {}
    for inp in recipe.get("inputs", []):
        if inp.get("key") == "__source":
            input_ids.append(b.ensure_source(_resolve_source_id(inp.get("label", ""))))
            continue
        if inp.get("prov") == formulas.PARAM:
            # Trägt ein Operator-Schritt den Wert bereits sichtbar (z. B. Skalierung
            # ×1,5 bei HEAT_WAVE), keinen doppelten Parameterknoten erzeugen.
            val = inp.get("value")
            if val is not None and any(
                st.get("factor") == val or st.get("value") == val for st in steps
            ):
                continue
            pnid = b.expand_recipe_input_to_id(
                inp, indicator_code=code, indicator_category=category,
            )
            param_ids.append(pnid)
            input_ids.append(pnid)
            continue
        iid = b.expand_recipe_input_to_id(inp, indicator_code=code, indicator_category=category)
        key = inp.get("key", "")
        if key and not key.startswith("__"):
            cell_key_map[key] = iid
        input_ids.append(iid)

    if steps and input_ids:
        b._wire_operator_chain(
            f"ind:{code}", steps, input_ids, ind_id, cell_key_map=cell_key_map,
        )
        for i, step in enumerate(steps):
            pid = step.get("parameter_id")
            if pid and step.get("op_kind") in ("scaling", "multiplier"):
                param_nid = b.ensure_parameter(
                    pid,
                    step.get("label", "Skalierung"),
                    unit=step.get("unit", ""),
                    source="Modellannahme (Formelrezept)",
                )
                op_id = f"op:{step['op_kind']}:ind:{code}:{i}"
                b.add_edge(param_nid, op_id)
        # Parameterknoten, die die Verkettung über input_keys nicht angeschlossen
        # hat, explizit an den ersten Operator hängen (sonst hingen sie lose).
        first_op_id = f"op:{steps[0]['op_kind']}:ind:{code}:0"
        connected = {e["source"] for e in b.edges}
        for pnid in param_ids:
            if pnid not in connected:
                b.add_edge(pnid, first_op_id)
    else:
        for iid in input_ids:
            b.add_edge(iid, ind_id)

    if include_norm and meta.get("norm_min") is not None:
        lo, hi = meta.get("norm_min"), meta.get("norm_max")
        unit = meta.get("unit", "")
        op_id = _add_operator_norm(
            b, code, category, lo, hi, unit, meta.get("source", ""),
        )
        b.add_edge(ind_id, op_id)
        out_id = f"out:norm:{code}"
        b.add_node(
            out_id, "outcome", "Normierter Wert",
            column=0, collapse_group="outcome",
            meta={
                "result_kind": "index",
                "unit": "0–1",
                "formula": f"normiert({lo}…{hi} {unit}) → 0…1".strip(),
                "is_outcome": True,
            },
        )
        b.add_edge(op_id, out_id)

    return _prune_lineage(b.build())


def build_auxiliary_lineage(code: str) -> dict:
    """Sonstige-Ebene: echte Quellen → Zellwert-Kette → Rohwert-Ergebnis.

    Bewusst OHNE Normierungs-Schritt — die Karten zeigen für Sonstige-Ebenen
    Rohwerte; norm_min/norm_max dienen nur der Farbskala. Ebenen mit inhärent
    normiertem Kartenwert (z. B. TWI_NORMALIZED) erklären das in ihrem
    Ableitungsschritt.
    """
    meta = catalog.AUXILIARY_BY_CODE.get(code)
    if not meta:
        return {"nodes": [], "edges": [], "collapse_groups": COLLAPSE_GROUPS}

    b = LineageBuilder()
    out_id = f"out:aux:{code}"
    b.add_node(
        out_id, "outcome", meta.get("name", code),
        column=3, collapse_group="outcome",
        meta={
            "code": code,
            "unit": meta.get("unit", ""),
            "result_kind": "raw",
            "formula": aux_formula_text(code, meta.get("source", "")),
            "is_outcome": True,
        },
    )

    spec = AUX_LINEAGE.get(code)
    if not spec:
        # Sicherheitsnetz für neue Codes ohne Eintrag: benannte Quelle statt
        # anonymem Parameter-Kasten (Vollständigkeit erzwingt der Ratchet-Test).
        b.add_edge(b.ensure_source(_resolve_source_id(meta.get("source", ""))), out_id)
        return _prune_lineage(b.build())

    input_ids: list[str] = []
    cell_key_map: dict[str, str] = {}
    for key in spec["keys"]:
        iid = b.expand_cell_key(key)
        cell_key_map[key] = iid
        input_ids.append(iid)

    steps = spec.get("steps")
    if steps:
        b._wire_operator_chain(
            f"aux:{code}", steps, input_ids, out_id, cell_key_map=cell_key_map,
        )
    else:
        for iid in input_ids:
            b.add_edge(iid, out_id)

    return _prune_lineage(b.build())


def _merge_builder(target: LineageBuilder, other: dict) -> None:
    for n in other["nodes"]:
        target.add_node(
            n["id"], n["type"], n["label"],
            column=n.get("column", 0),
            collapse_group=n.get("collapse_group", "intermediates"),
            meta=n.get("meta"),
        )
    for e in other["edges"]:
        target.add_edge(
            e["source"], e["target"],
            label=e.get("label"),
            parameter_id=e.get("parameter_id"),
            meta=e.get("meta"),
        )


# ── Schicht B: Bausteine für den Impact-Zweig des Wirkungsdiagramms ─────────────

def _risk_lineage_kind(risk: dict) -> str:
    """Kategorisiert das Risiko nach seinem tatsächlichen Schicht-B-Rechenweg."""
    from app.services.engine import impact
    return impact.lineage_kind(risk)


def _impact_param_node(b: LineageBuilder, risk_code: str, key: str) -> str:
    spec = _IMPACT_PARAM_BY_KEY.get((risk_code, key), {})
    return b.ensure_parameter(
        f"risks.{risk_code}.impact.{key}",
        spec.get("label", key),
        unit=spec.get("unit", ""),
        source=spec.get("source", "Modellannahme (Schicht B)"),
    )


def _global_param_node(b: LineageBuilder, key: str) -> str:
    spec = _IMPACT_GLOBAL_BY_KEY.get(key, {})
    return b.ensure_parameter(
        f"impact.{key}",
        spec.get("label", key),
        unit=spec.get("unit", ""),
        source=spec.get("source", "Modellannahme (Schicht B)"),
    )


def _add_op(
    b: LineageBuilder,
    op_id: str,
    op_kind: str,
    label: str,
    note: str,
    *,
    collapse_group: str = "outcome",
) -> str:
    # Autorentext liegt unter "note"; der finale Tooltip (Titel + Notiz +
    # Eingaben) wird zentral in _enrich_tooltips/_tooltip_for_node komponiert.
    b.add_node(op_id, "operator", "", column=0, collapse_group=collapse_group,
               meta={"op_kind": op_kind, "label": label, "note": note})
    return op_id


def _add_intensity_op(
    b: LineageBuilder, code: str, hazards: list[str], *, op_id: str | None = None,
) -> str:
    op_id = op_id or f"op:intensity:{code}"
    _add_op(
        b, op_id, "intensity", "Intensität",
        "Normierte Hazard-Intensität (0–1) mit FIXEN Katalog-Referenzgrenzen — "
        "unabhängig von der editierbaren Screening-Normierung (§3.3). Bei mehreren "
        "Gefahren zählt die stärkste (Maximum).",
    )
    for h in hazards:
        b.add_edge(b.ensure_indicator(h, "hazards"), op_id)
    return op_id


def _add_af_op(b: LineageBuilder, code: str, driver: dict) -> str:
    op_id = f"op:af:{code}"
    _add_op(
        b, op_id, "af", "AF",
        "Attributable Fraktion: Anteil des Outcomes, der den Hitzetagen zuzurechnen "
        "ist (0…1). Unterhalb der Schwelle 0, oberhalb sättigend.\n"
        r"$$AF = 1 - e^{-\beta\,(H_{\mathrm{Tage}} - H_{0})_{+}}$$",
    )
    b.add_edge(b.ensure_indicator(driver["hazard"], "hazards"), op_id)
    for pkey in driver.get("params", []):
        b.add_edge(_impact_param_node(b, code, pkey), op_id)
    return op_id


def _add_driver_op(b: LineageBuilder, code: str, driver: dict) -> str:
    """Treiber-Operator des Schicht-B-Zweigs, exakt nach ``LINEAGE_SPECS``."""
    kind = driver["kind"]
    if kind == "intensity":
        return _add_intensity_op(b, code, driver["hazards"])
    if kind == "af":
        return _add_af_op(b, code, driver)
    if kind == "ratio":
        op_id = f"op:ratio:{code}"
        _add_op(
            b, op_id, "ratio", "÷ Referenz",
            "Linearer Treiber: Hitzetage der Zelle ÷ Referenz-Hitzetage.\n"
            r"$$\mathrm{Treiber} = H_{\mathrm{Tage}} / H_{\mathrm{Referenz}}$$",
        )
        b.add_edge(b.ensure_indicator(driver["hazard"], "hazards"), op_id)
        for pkey in driver.get("params", []):
            b.add_edge(_impact_param_node(b, code, pkey), op_id)
        return op_id
    if kind == "erf":
        op_id = f"op:erf:{code}"
        _add_op(
            b, op_id, "erf", "Wirkungskurve",
            "Expositions-Wirkungs-Kurve nach RKI/Winklmayr: relatives Sterberisiko über "
            "der Wochenmitteltemperatur, je Altersband und Region. Die Kurve wird über "
            "die 13 empirischen Wochenquantile des Sommers summiert (T_w = T̄ + q_w, "
            "Bericht #95 §3.2) — nicht am Mittelwert ausgewertet, denn das deutsche "
            "Sommermittel liegt unter der Wirkschwelle. Bewertung: YLL = Σ D_a · L̄_a "
            "(nativer Ausweis; Todesfälle als Teil-Ausweis).\n"
            r"$$\mathrm{Exzess} = \sum_{w=1}^{13} \left(e^{\beta_a\,(T_w - T_0)_{+}} - 1\right)$$",
        )
        b.add_edge(b.ensure_indicator(driver["hazard"], "hazards"), op_id)
        for pkey in driver.get("params", []):
            b.add_edge(_impact_param_node(b, code, pkey), op_id)
        return op_id
    if kind == "hd_linear":
        op_id = f"op:hdlinear:{code}"
        _add_op(
            b, op_id, "ratio", "HD-Term",
            "Zweiseitig linearer Hitzetage-Term um die Referenzlast, bei 0 gedeckelt "
            "(Bericht #95 §3.4): Zellen unter der Referenz reduzieren die Baseline "
            "anteilig — erwartungstreu um HD_ref, keine Doppelzählung des bereits in "
            "r_0 enthaltenen Referenzlast-Effekts.\n"
            r"$$\mathrm{Treiber} = \max\bigl(0,\; 1 + e_{HD}\,(\mathrm{HD} - "
            r"\mathrm{HD}_{ref})\bigr)$$",
        )
        b.add_edge(b.ensure_indicator(driver["hazard"], "hazards"), op_id)
        for pkey in driver.get("params", []):
            b.add_edge(_impact_param_node(b, code, pkey), op_id)
        return op_id
    if kind == "af_plus_event":
        af_id = _add_af_op(b, code, driver)
        ev_id = _add_intensity_op(
            b, code, driver["event_hazards"], op_id=f"op:eventintensity:{code}",
        )
        add_id = f"op:afevent:{code}"
        _add_op(
            b, add_id, "add", "+",
            "Treiber = AF + Ereignis-Anteil · Ereignisintensität (gedeckelt bei 1).",
        )
        b.add_edge(af_id, add_id)
        b.add_edge(ev_id, add_id)
        # Ereignis-Anteil als editierbarer Parameterknoten (risks.<code>.impact.<key>).
        share_param = driver.get("event_share_param")
        if share_param:
            b.add_edge(_impact_param_node(b, code, share_param), add_id)
        return add_id
    raise ValueError(f"Unbekannter Schicht-B-Treiber: {kind}")


def _add_modifier_op(b: LineageBuilder, code: str, mod: dict) -> str:
    """Zell-Modifikator, der von g(V̂) ABWEICHT (Schicht-B-Gesundheitskanäle).

    Für die Mortalitätskanäle ist g(V̂) sachlich falsch: Hitze rechnet mit dem
    Versorgungszugang, Flut mit Warnzeit×Alter, Sturm mit Bäumen×Straßen. Das
    Diagramm muss zeigen, was gerechnet wird — sonst behauptet es Eingänge
    (etwa HEAT_SENSITIVITY), die den Outcome gar nicht berühren.
    """
    op_id = f"op:modifier:{code}"
    _add_op(b, op_id, "gv", mod["label"], mod["note"])
    for vcode in mod.get("vulnerabilities", []):
        b.add_edge(b.ensure_indicator(vcode, "vulnerabilities"), op_id)
    for ckey in mod.get("cell_keys", []):
        b.add_edge(b.expand_cell_key(ckey), op_id)
    for pkey in mod.get("params", []):
        b.add_edge(_impact_param_node(b, code, pkey), op_id)
    return op_id


def _add_gv_op(b: LineageBuilder, risk: dict) -> str:
    op_id = f"op:gv:{risk['code']}"
    _add_op(
        b, op_id, "gv", "g(V̂)",
        "Vulnerabilitäts-Modifikator aus dem Mittel der normierten Sensitivitäten des "
        "Risikos: hebt/senkt den Zell-Outcome um Faktor 0,5…1,5.\n"
        r"$$g(\hat{V}) = 0{,}5 + \overline{\hat{V}}$$",
    )
    for vcode in risk.get("vulnerabilities", []):
        b.add_edge(b.ensure_indicator(vcode, "vulnerabilities"), op_id)
    return op_id


def _add_sum_cells_op(b: LineageBuilder, code: str) -> str:
    return _add_op(
        b, f"op:sumcells:{code}", "sum_cells", "Σ Zellen",
        "Summe der Zell-Outcomes über alle 100×100-m-Rasterzellen der Kommune (Schicht B).\n"
        r"$$O = \sum_{\mathrm{Zellen}} O_{z}$$",
    )


def _add_cost_op(b: LineageBuilder, risk: dict, *, extra_tooltip: str = "") -> str:
    code = risk["code"]
    rate = catalog.risk_default_cost_per_outcome(risk)
    unit = catalog.cost_unit_label(risk.get("outcome_unit", ""))
    src = risk.get("cost_source") or ""
    # Quelle NICHT in die Note: die Skalierungs-Komposition (_tooltip_for_node)
    # hängt sie aus meta["source"] an — sonst stünde sie doppelt im Tooltip.
    note = (
        "Monetarisierung des Outcomes über den editierbaren Kostensatz.\n"
        r"$$\text{€} = O \cdot \text{Kostensatz}$$"
    )
    if extra_tooltip:
        note += f"\n{extra_tooltip}"
    op_id = f"op:cost:{code}"
    b.add_node(
        op_id, "operator", "",
        column=0, collapse_group="outcome",
        meta={
            "op_kind": "scaling",
            "label": "Kostensatz",
            "parameter_id": f"risks.{code}.cost_per_outcome",
            "value": rate,
            "unit": unit,
            "scale": "cost",
            "source": src or "Kostensatz (Risikokatalog)",
            "note": note,
        },
    )
    return op_id


def _area_basis(b: LineageBuilder, code: str, keys: list[str], label: str) -> str:
    if len(keys) == 1:
        return b.expand_cell_key(keys[0])
    labels = [INTERMEDIATE_LABELS.get(k, k) for k in keys]
    area_id = f"int:area:{code}"
    b.add_node(
        area_id, "intermediate", label,
        column=1, collapse_group="intermediates",
        meta={"note": f"{label} = {' + '.join(labels)} (× 1 ha Zellfläche)."},
    )
    op_id = _add_op(
        b, f"op:addarea:{code}", "add", "+",
        f"Summe der Flächenanteile: {' + '.join(labels)}.",
        collapse_group="intermediates",
    )
    for k in keys:
        b.add_edge(b.expand_cell_key(k), op_id)
    b.add_edge(op_id, area_id)
    return area_id


def _asset_basis(b: LineageBuilder, code: str, asset: dict) -> str:
    kind = asset["kind"]
    label = asset.get("label", "Assetwert (Zelle)")
    if kind == "building":
        tip = ("Gebäude-Assetwert = Geschossfläche (Gebäudeanteil × Zellfläche × "
               "Geschosse aus mittlerer Höhe) × Gebäudewert je m².")
    elif kind == "class_count":
        tip = ("Assetwert = Σ Anzahl je Anlagenklasse in der Zelle × Ersatzwert "
               "der Klasse (editierbare impact-Parameter je Anlagenklasse).")
    else:
        tip = "Assetwert = Flächenanteil × 1 ha Zellfläche × Wert je ha."
    asset_id = f"int:asset:{code}"
    b.add_node(
        asset_id, "intermediate", label,
        column=1, collapse_group="intermediates",
        meta={"note": tip},
    )
    op_id = _add_op(b, f"op:asset:{code}", "multiply", "×", tip,
                    collapse_group="intermediates")
    for k in asset["cell_keys"]:
        b.add_edge(b.expand_cell_key(k), op_id)
    for p in asset.get("value_params", ([asset["value_param"]] if "value_param" in asset else [])):
        b.add_edge(_global_param_node(b, p), op_id)
    b.add_edge(op_id, asset_id)
    return asset_id


def _build_impact_branch(
    b: LineageBuilder, risk: dict, kind: str, idx_id: str,
) -> None:
    """Schicht-B-Zweig: Quellen → Schadensfunktion → (natives Ergebnis) → €."""
    code = risk["code"]
    unit = risk.get("outcome_unit", "")

    def add_eur(formula: str, *, non_additive: bool = False) -> str:
        meta: dict[str, Any] = {
            "result_kind": "eur",
            "unit": "€/Jahr",
            "formula": formula,
            "is_outcome": True,
            "cost_source": risk.get("cost_source", ""),
        }
        if non_additive:
            meta["non_additive"] = True
        b.add_node("out:eur", "outcome", "Monetärer Schaden",
                   column=0, collapse_group="outcome", meta=meta)
        return "out:eur"

    def add_native(formula: str) -> str:
        b.add_node(
            "out:native", "outcome", unit or "Outcome",
            column=0, collapse_group="outcome",
            meta={"result_kind": "native", "unit": unit, "formula": formula,
                  "is_outcome": True},
        )
        return "out:native"

    if kind == "index_only":
        return

    if kind in ("health", "environment"):
        mod_spec = None
        no_mod = False
        if kind == "health":
            spec = HEALTH_SPECS[code]
            mod_spec = spec.get("modifier")
            # no_modifier: der Kanal rechnet bewusst OHNE Zellmodifikator
            # (z. B. Hitze-Morbidität, Bericht #95 §3.4) — das Diagramm darf
            # dann kein g(V̂) erfinden.
            no_mod = bool(spec.get("no_modifier"))
            basis_label = spec.get("basis_label", "Bevölkerung")
            basis = b.expand_cell_key(spec.get("basis_key", "pop"))
            if no_mod:
                product = f"{basis_label} · Rate · Treiber"
                latex = (r"$$O_{z} = \text{" + basis_label + r"}_{z} \cdot "
                         r"\text{Rate} \cdot \text{Treiber}_{z}$$")
            else:
                mod_term = mod_spec["term"] if mod_spec else "g(V̂)"
                mod_latex = r"M_{z}" if mod_spec else r"g(\hat{V})"
                product = f"{basis_label} · Rate · Treiber · {mod_term}"
                latex = (r"$$O_{z} = \text{" + basis_label + r"}_{z} \cdot \text{Rate}"
                         r" \cdot \text{Treiber}_{z} \cdot " + mod_latex + "$$")
        else:
            spec = ENV_SPECS[code]
            basis = _area_basis(b, code, spec["area_keys"], "Exponierte Naturfläche (Zelle)")
            product = "exponierte Fläche · Verlustrate · Intensität · g(V̂)"
            latex = r"$$O_{z} = \text{Fläche}_{z} \cdot \text{Verlustrate} \cdot I_{z} \cdot g(\hat{V})$$"
        mul_id = _add_op(b, f"op:mulB:{code}", "multiply", "×",
                         f"Zell-Outcome = {product}.\n{latex}")
        b.add_edge(basis, mul_id)
        b.add_edge(_impact_param_node(b, code, spec["rate_param"]), mul_id)
        b.add_edge(_add_driver_op(b, code, spec["driver"]), mul_id)
        if not no_mod:
            b.add_edge(_add_modifier_op(b, code, mod_spec) if mod_spec
                       else _add_gv_op(b, risk), mul_id)
        sum_id = _add_sum_cells_op(b, code)
        b.add_edge(mul_id, sum_id)
        native_id = add_native(f"Outcome = {product}, Σ Zellen")
        b.add_edge(sum_id, native_id)
        cost_id = _add_cost_op(b, risk)
        b.add_edge(native_id, cost_id)
        b.add_edge(cost_id, add_eur("€ = Outcome × Kostensatz"))
        return

    if kind == "monetary":
        spec = MONETARY_SPECS[code]
        if spec.get("basis_pop"):
            # Klimamigration: Bevölkerungs-Muster, Outcome ist direkt €.
            mul_id = _add_op(
                b, f"op:mulB:{code}", "multiply", "×",
                "Zell-Kosten (€) = (Einwohner/100.000) · Referenzkosten · Intensität · g(V̂).\n"
                r"$$K_{z} = \frac{\text{Einwohner}_{z}}{100\,000} \cdot \text{Referenzkosten} \cdot I_{z} \cdot g(\hat{V})$$",
            )
            b.add_edge(b.expand_cell_key("pop"), mul_id)
            b.add_edge(_impact_param_node(b, code, spec["rate_param"]), mul_id)
            b.add_edge(_add_driver_op(b, code, spec["driver"]), mul_id)
            b.add_edge(_add_gv_op(b, risk), mul_id)
            sum_id = _add_sum_cells_op(b, code)
            b.add_edge(mul_id, sum_id)
            b.add_edge(sum_id, add_eur(
                "€ = (Einwohner/100.000) · Referenzkosten · Intensität · g(V̂), Σ Zellen"))
            return
        basis = _asset_basis(b, code, spec["asset"])
        damage_id = _add_op(
            b, f"op:damage:{code}", "damage_curve", "Schadenskurve",
            "Konvexe Schadenskurve: überproportionaler Schaden bei hoher Intensität.\n"
            r"$$s = I^{\,\gamma},\quad \gamma > 1$$",
        )
        b.add_edge(_add_intensity_op(b, code, spec["driver"]["hazards"]), damage_id)
        b.add_edge(_global_param_node(b, "damage_exponent"), damage_id)
        mul_id = _add_op(
            b, f"op:mulB:{code}", "multiply", "×",
            "Zell-Schaden (€) = Assetwert · max. Verlustrate · Schadenskurve(Intensität) · g(V̂).\n"
            r"$$S_{z} = A_{z} \cdot r_{\max} \cdot s(I_{z}) \cdot g(\hat{V})$$",
        )
        b.add_edge(basis, mul_id)
        b.add_edge(_impact_param_node(b, code, spec["loss_param"]), mul_id)
        b.add_edge(damage_id, mul_id)
        b.add_edge(_add_gv_op(b, risk), mul_id)
        sum_id = _add_sum_cells_op(b, code)
        b.add_edge(mul_id, sum_id)
        b.add_edge(sum_id, add_eur(
            "€ = Assetwert · Verlustrate · Schadenskurve(Intensität) · g(V̂), Σ Zellen"))
        return

    if kind in ("indirect", "restoration"):
        direct_id = "int:direct_sum"
        names = [
            catalog.RISKS_BY_CODE[c]["name"]
            for c in sorted(catalog.DIRECT_SECTOR_RISK_CODES)
        ]
        b.add_node(
            direct_id, "intermediate", "Direkte Sektorschäden (Σ €)",
            column=1, collapse_group="intermediates",
            meta={"note": "Summe der direkten Sektorschäden je Zelle (Schicht B): "
                          + ", ".join(names) + "."},
        )
        sum_direct_id = _add_op(
            b, f"op:sumdirect:{code}", "sum_cells", "Σ",
            "Summiert die €-Zellschäden der zehn direkten Sektorrisiken.",
            collapse_group="intermediates",
        )
        # Keine anonyme "Berechnet"-Box: die Eingaben sind die Schicht-B-
        # €-Zellschäden der zehn direkten Sektorrisiken (je eigenes
        # Wirkungsdiagramm) — benannt statt als generische Quelle.
        b.add_node(
            "src:direct_sectors", "source", "Sektorrisiken (Schicht B)",
            column=0, collapse_group="sources",
            meta={
                "description": ("€-Zellschäden der zehn direkten Sektorrisiken, "
                                "je mit eigenem Wirkungsdiagramm: "
                                + ", ".join(names)),
                "prov": "computed",
            },
        )
        b.add_edge("src:direct_sectors", sum_direct_id)
        b.add_edge(sum_direct_id, direct_id)
        if kind == "indirect":
            param = _global_param_node(b, "k_indirect")
            mul_id = _add_op(
                b, f"op:kfactor:{code}", "multiply", "×",
                "Indirekte Folgekosten = k_indirekt · Σ direkte Sektorschäden "
                "(konsolidiert Betriebsunterbrechung, Lieferketten, Standortnachteil, "
                "verzögerte Schäden).",
            )
            formula = "€ = k_indirekt · Σ direkte Sektorschäden"
            non_additive = False
        else:
            param = _global_param_node(b, "restoration_share")
            mul_id = _add_op(
                b, f"op:kfactor:{code}", "multiply", "×",
                "Restaurierungskosten = Restaurierungsquote · Σ direkte Sektorschäden. "
                "Teilkennzahl (Teilmenge der direkten Schäden) — nicht additiv zur "
                "Gesamtsumme.",
            )
            formula = "€ = Restaurierungsquote · Σ direkte Sektorschäden (nicht additiv)"
            non_additive = True
        b.add_edge(direct_id, mul_id)
        b.add_edge(param, mul_id)
        b.add_edge(mul_id, add_eur(formula, non_additive=non_additive))
        return

    if kind == "consolidated_zero":
        add_eur("0 € — in k_indirekt (Indirekte wirtschaftliche Verluste) konsolidiert, "
                "um Doppelzählung zu vermeiden (§3.7)")
        return

    # "flat": kommunenweiter Outcome aus dem P90-Index (estimate_outcome_and_cost).
    # Einziger Fall, in dem sich der €-Wert tatsächlich aus dem Index ableitet.
    p90_id = _add_op(
        b, f"op:p90:{code}", "p90", "P90",
        "90. Perzentil der Zell-Indizes → kommunenweiter Screening-Index (0–100).\n"
        r"$$P_{90}(\text{Zell-Indizes})$$",
    )
    b.add_edge(idx_id, p90_id)
    ref = float(risk.get("ref_value", 0.0))
    scale_id = _add_operator_scaling(b, code, ref, unit, "flat")
    b.add_edge(p90_id, scale_id)
    native_id = add_native("Outcome = Referenz · (P90-Index/100), kommunenweit")
    b.add_edge(scale_id, native_id)
    cost_id = _add_cost_op(
        b, risk,
        extra_tooltip="€-Bewertung skaliert mit Einwohner/100.000 (VoLL-Kalibrierung, §8/B6).",
    )
    b.add_edge(native_id, cost_id)
    b.add_edge(cost_id, add_eur("€ = Outcome × Kostensatz × Einwohner/100.000"))


def build_risk_lineage(code: str) -> dict:
    """Zwei-Schichten-Graph eines Risikos (Wirkungsdiagramm).

    Schicht A: Quellen → Zwischen → H/E/V → Wirkungsketten → Maximum → KWRA-Index.
    Schicht B: Quellen → Schadensfunktion → natives Ergebnis → Kostensatz → €
    (Struktur je Risikokategorie, siehe ``_risk_lineage_kind``).
    """
    risk = catalog.RISKS_BY_CODE[code]
    recipe = risk_recipe(risk)
    kind = _risk_lineage_kind(risk)
    b = LineageBuilder()

    # Schicht A: alle H/E/V der kuratierten Ketten (dedupliziert über ind:-IDs)
    hev_codes: set[tuple[str, str]] = set()
    for p in catalog.build_pathways(risk):
        hev_codes.add(("hazards", p["hazard"]))
        hev_codes.add(("exposures", p["exposure"]))
        hev_codes.add(("vulnerabilities", p["vulnerability"]))

    for cat, icode in hev_codes:
        sub = build_indicator_lineage(icode, cat, include_norm=False)
        _merge_builder(b, sub)

    pathways_meta = risk_pathway_meta(risk)
    idx_id = "out:index"
    b.add_node(
        idx_id, "outcome", "KWRA-Index",
        column=0, collapse_group="outcome",
        meta={
            "result_kind": "index",
            "unit": "0–100",
            "formula": recipe.get("formula_index", ""),
            "formula_header": recipe.get("formula_index_header", ""),
            "pathway_count": len(pathways_meta),
            "is_outcome": True,
        },
    )

    if pathways_meta:
        max_id = _add_operator_max(b)
        b.add_edge(max_id, idx_id)
        for i, p in enumerate(pathways_meta):
            h_id = f"ind:{p['hazard']}"
            e_id = f"ind:{p['exposure']}"
            v_id = f"ind:{p['vulnerability']}"
            mul_id = f"op:mul:path:{i}"
            path_id = f"pathway:{i}"
            title = get_pathway_description(
                code, p["hazard"], p["exposure"], p["vulnerability"],
                p["type"],
                p["hazard_name"], p["exposure_name"], p["vulnerability_name"],
            )
            _add_operator_multiply(b, mul_id)
            b.add_node(
                path_id, "pathway", title,
                column=3, collapse_group="pathways",
                meta={
                    "pathway_type": p["type"],
                    "type_label": p["type_label"],
                    "weight": p["weight"],
                    "chain_label": chain_label(p["hazard_name"], p["exposure_name"], p["vulnerability_name"]),
                    "hazard_name": p["hazard_name"],
                    "exposure_name": p["exposure_name"],
                    "vulnerability_name": p["vulnerability_name"],
                    "justification": p.get("justification"),
                    "justification_ref": p.get("justification_ref"),
                    "cluster": p.get("cluster"),
                },
            )
            b.add_edge(h_id, mul_id)
            b.add_edge(e_id, mul_id)
            b.add_edge(v_id, mul_id)
            b.add_edge(mul_id, path_id)
            b.add_edge(
                path_id, max_id,
                meta={
                    "op_kind": "weight",
                    "weight": p["weight"],
                    # bewusst KEINE parameter_id: Pfadgewichte sind beim Import fest
                    # eingelesene Modellkonstanten (risk_engine._PATHWAYS) — kein
                    # editierbarer Registry-Parameter (Override wäre wirkungslos).
                    "source": "Pfadgewicht (Modellkonstante, Risikokatalog)",
                },
            )

    # Schicht B: absoluter Outcome + € (bzw. nur Index bei Screening-Risiken)
    _build_impact_branch(b, risk, kind, idx_id)

    return _prune_lineage(b.build())


def build_measure_lineage(code: str) -> dict:
    m = catalog.MEASURES_BY_CODE.get(code)
    if not m:
        return {"nodes": [], "edges": [], "collapse_groups": COLLAPSE_GROUPS}
    b = LineageBuilder()
    mid = f"measure:{code}"
    b.add_node(mid, "pathway", m["name"], column=2, collapse_group="indicators",
               meta={"effect_target": m.get("effect_target", [])})
    for tgt in m.get("effect_target", []):
        b.add_node(f"src:effect:{tgt}", "source", f"Wirkung auf {tgt}",
                   column=0, collapse_group="sources")
        b.add_edge(f"src:effect:{tgt}", mid)
    for rcode in m.get("linked_risk_codes", [])[:3]:
        rname = catalog.RISKS_BY_CODE.get(rcode, {}).get("name", rcode)
        rid = f"risk:{rcode}"
        b.add_node(rid, "aggregation", rname, column=4, collapse_group="outcome")
        b.add_edge(mid, rid, label=f"−{m.get('default_reduction', 0)*100:.0f}%")
    return _finalize_graph(b.build())


def build_for_layer(code: str, category: str) -> dict:
    if category == "risks":
        return build_risk_lineage(code)
    if category == "measures":
        return build_measure_lineage(code)
    if category == "auxiliary":
        return build_auxiliary_lineage(code)
    if category in ("hazards", "exposures", "vulnerabilities"):
        return build_indicator_lineage(code, category)
    return {"nodes": [], "edges": [], "collapse_groups": COLLAPSE_GROUPS}
