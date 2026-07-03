"""Fest verdrahteter Fachkatalog (einmalig portiert aus den KAP3-CSVs).

Dieser Katalog ist die EINZIGE Quelle der Wahrheit für klimatische Einflüsse (Hazards),
räumliche Expositionen, Sensitivitäten, Risiken und Maßnahmen. Es gibt bewusst keinen
Laufzeit-CSV-Parser und kein generisches Katalogsystem – die Inhalte sind als
Python-Konstanten hinterlegt (siehe Plan).

Konventionen
------------
* Klimatische Einflüsse/räumliche Expositionen/Sensitivitäten werden pro 100m-Zelle in ihrer
  ABSOLUTEN Einheit berechnet und angezeigt (``unit``).
* ``norm_min`` / ``norm_max`` definieren die Referenzskala, die AUSSCHLIESSLICH
  für die Risikoberechnung genutzt wird (Normalisierung auf 0..1). Sie hat keinen
  Einfluss auf die Darstellung der H/E/V-Werte.
* ``spatial=False`` markiert Indikatoren ohne lokalen räumlichen Proxy – diese
  bekommen einen regionalen/nationalen Konstantwert und werden in UI + Handbuch
  als „nicht räumlich aufgelöst" gekennzeichnet.
* Risiken werden über Wirkungsketten komponiert (siehe ``build_pathways`` und
  ``PATHWAY_WEIGHTS``; reproduziert die Logik aus ``risk_composition.csv`` +
  ``pathway_weight_defaults.csv`` deterministisch aus den H/E/V-Listen).
"""

from __future__ import annotations

# ── KWRA-Risikogruppen (max. 5) – für Spinnendiagramme & Risiko-Gruppierung ────

KWRA_GROUPS: list[dict] = [
    {"code": "heat", "challenge": "KWRA_CHALLENGE_HEAT",
     "label": "Hitze", "color": "#ef4444",
     "description": "Extreme Hitze, Gesundheit und urbane Überwärmung."},
    {"code": "drought", "challenge": "KWRA_CHALLENGE_DROUGHT_LOW_WATER",
     "label": "Trockenheit & Niedrigwasser", "color": "#f59e0b",
     "description": "Trockenheit, Niedrigwasser und sinkende Grundwasserstände."},
    {"code": "flood", "challenge": "KWRA_CHALLENGE_FLOOD",
     "label": "Hochwasser & Starkregen", "color": "#3b82f6",
     "description": "Hochwasser, Starkregen und Sturzfluten."},
    {"code": "gradual", "challenge": "KWRA_CHALLENGE_GRADUAL_CHANGE",
     "label": "Gradueller Wandel", "color": "#22c55e",
     "description": "Gradueller Temperatur-/Meeresspiegelanstieg, Ökosysteme."},
    {"code": "compound", "challenge": "KWRA_CHALLENGE_COMPOUND_SYSTEMIC",
     "label": "Verbund & Kaskaden", "color": "#8b5cf6",
     "description": "Verbund-, Kaskaden- und systemische Risiken."},
]

CHALLENGE_TO_GROUP = {g["challenge"]: g["code"] for g in KWRA_GROUPS}


# ── Klimatische Einflüsse (Hazards) ────────────────────────────────────────────
# unit = absolute Einheit; norm_* = Referenzskala nur für Risikoberechnung.
# spatial = ob lokal räumlich auflösbar; proxy/source = Tooltip + Handbuch.

HAZARDS: list[dict] = [
    {"code": "MEAN_TEMPERATURE_RISE", "name": "Anstieg der mittleren Lufttemperatur",
     "unit": "°C", "norm_min": 0.0, "norm_max": 3.0, "spatial": True,
     "description": "Langfristiger Trend steigender mittlerer Lufttemperaturen.",
     "proxy": "Regionaler DWD-Mittelwert (Bundesland) plus lokaler UHI-Aufschlag aus OSM-Landnutzung.",
     "source": "DWD CDC / Copernicus C3S-CORDEX (regionalisiert)"},
    {"code": "SEA_LEVEL_RISE", "name": "Meeresspiegelanstieg",
     "unit": "mm/Jahr", "norm_min": 0.0, "norm_max": 10.0, "spatial": False, "coastal": True,
     "description": "Langfristiger Anstieg des mittleren Meeresspiegels an Küsten.",
     "proxy": "Regionaler Konstantwert; nur für Küstenkommunen aktiv.",
     "source": "Copernicus C3S / BSH"},
    {"code": "OCEAN_WARMING", "name": "Ozeanerwärmung",
     "unit": "°C", "norm_min": 0.0, "norm_max": 3.0, "spatial": False, "coastal": True,
     "description": "Langfristige Erwärmung der Ozeanoberfläche und Wassermassen.",
     "proxy": "Regionaler Konstantwert; nur für Küstenkommunen.",
     "source": "Copernicus C3S"},
    {"code": "OCEAN_ACIDIFICATION", "name": "Ozeanversauerung",
     "unit": "ΔpH", "norm_min": 0.0, "norm_max": 0.5, "spatial": False, "coastal": True,
     "description": "Abnahme des pH-Werts der Ozeane durch CO2-Aufnahme.",
     "proxy": "Nationaler Konstantwert; nur Küstenkommunen.",
     "source": "Copernicus C3S"},
    {"code": "GLACIER_SNOW_LOSS", "name": "Gletscherschwund und Schneerückgang",
     "unit": "%/Jahr", "norm_min": 0.0, "norm_max": 5.0, "spatial": True,
     "description": "Rückgang von Gletschermassen und Schneedecke.",
     "proxy": "Gletscher (OSM natural=glacier) + relativer Schneedecken-Rückgang (DWD CDC snowcover_days-Trend), höhenmoduliert (DEM).",
     "source": "OSM + DWD CDC + Terrarium DEM"},
    {"code": "PERMAFROST_THAW", "name": "Permafrosttauung",
     "unit": "Index", "norm_min": 0.0, "norm_max": 1.0, "spatial": False,
     "description": "Auftauen dauerhaft gefrorener Böden in Permafrostregionen.",
     "proxy": "Konstantwert (in DE nur alpine Hochlagen).",
     "source": "Copernicus C3S"},
    {"code": "SOIL_MOISTURE_DECLINE", "name": "Abnahme der Bodenfeuchte / Aridität",
     "unit": "mm", "norm_min": 0.0, "norm_max": 80.0, "spatial": True,
     "description": "Langfristiger Trend abnehmender Bodenfeuchte und zunehmender Trockenheit.",
     "proxy": "Aus regionalem Trockenindex + Anteil unversiegelter/landwirtschaftlicher Fläche.",
     "source": "Sentinel/Copernicus (regionalisiert)"},
    {"code": "HEAT_WAVE", "name": "Hitzeextreme / Hitzewellen",
     "unit": "Tage/Jahr", "norm_min": 0.0, "norm_max": 40.0, "spatial": True,
     "description": "Akute oder anhaltende extreme Hitzeereignisse.",
     "proxy": "DWD-CDC heiße-Tage-Raster (1 km, am Kommune-Zentroid) + UHI-Modell (ΔT) pro 100m-Zelle aus OSM (siehe Handbuch).",
     "source": "DWD CDC (Raster) + UHI-Modell (OSM)"},
    {"code": "COLD_EXTREME", "name": "Kälteextreme und Frostereignisse",
     "unit": "Tage/Jahr", "norm_min": 0.0, "norm_max": 40.0, "spatial": True,
     "description": "Extreme Kälte- und Frostereignisse (regional relevant).",
     "proxy": "DWD-CDC Frosttage-Raster (1 km, am Kommune-Zentroid), leicht reduziert in dicht bebauten (wärmeren) Zellen.",
     "source": "DWD CDC (Raster)"},
    {"code": "HEAVY_RAIN_FLOOD", "name": "Starkniederschlag und Fluten",
     "unit": "Index", "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Extreme Niederschläge inkl. Überflutungen und Sturzfluten.",
     "proxy": "Versiegelungsgrad (OSM) × TWI/Senkenlage (Terrarium-DEM, D8) × regionaler Starkregenindex.",
     "source": "DWD CDC + AWS Terrarium DEM"},
    {"code": "DROUGHT", "name": "Dürren",
     "unit": "Tage/Jahr", "norm_min": 0.0, "norm_max": 60.0, "spatial": True,
     "description": "Meteorologische, hydrologische oder agrarische Dürreperioden.",
     "proxy": "Trockentage (Proxy aus DWD-CDC heißen Tagen am Zentroid) + erhöhte Empfindlichkeit auf versiegelten/landwirtschaftlichen Flächen.",
     "source": "DWD CDC (Raster, abgeleitet) / UBA"},
    {"code": "TROPICAL_CYCLONE", "name": "Tropische Wirbelstürme / Orkane",
     "unit": "Anzahl/Jahr", "norm_min": 0.0, "norm_max": 2.0, "spatial": False,
     "description": "Tropische Wirbelstürme und vergleichbare Zyklone.",
     "proxy": "Nationaler Konstantwert (in DE sehr niedrige Priorität).",
     "source": "Copernicus C3S"},
    {"code": "EXTRATROPICAL_STORM", "name": "Extratropische Stürme & Starkwind",
     "unit": "Anzahl/Jahr", "norm_min": 0.0, "norm_max": 12.0, "spatial": True,
     "description": "Extratropische Stürme mit starken Winden.",
     "proxy": "Regionaler Sturmtage-Wert, erhöht in exponierten (offenen/hohen) Lagen.",
     "source": "DWD CDC"},
    {"code": "STORM_SURGE", "name": "Sturmfluten und Küstenüberschwemmungen",
     "unit": "Anzahl/Jahr", "norm_min": 0.0, "norm_max": 6.0, "spatial": False, "coastal": True,
     "description": "Sturmfluten und damit verbundene Küstenüberschwemmungen.",
     "proxy": "Regionaler Konstantwert; nur Küstenkommunen.",
     "source": "BSH"},
    {"code": "WILDFIRE", "name": "Wald- und Vegetationsbrände",
     "unit": "Index", "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Wald- und Vegetationsbrände (Wildfires).",
     "proxy": "Wald-/Vegetationsanteil (OSM) × regionaler Trockenheitsindex.",
     "source": "Sentinel/Copernicus + DWD"},
    {"code": "LANDSLIDE", "name": "Hangrutschungen / Erdrutsche",
     "unit": "Index", "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Hang- und Erdrutsche, häufig nach Starkregen oder Entwaldung.",
     "proxy": "Hangneigung (Terrarium-DEM) × Starkregenindex.",
     "source": "AWS Terrarium DEM + DWD CDC"},
    {"code": "SALTWATER_INTRUSION", "name": "Salzwassereinbruch",
     "unit": "Index", "norm_min": 0.0, "norm_max": 1.0, "spatial": False, "coastal": True,
     "description": "Eindringen von Salzwasser in Küsten- und Grundwassersysteme.",
     "proxy": "Konstantwert; nur Küstenkommunen.",
     "source": "UBA / BfG"},
    {"code": "COASTAL_EROSION", "name": "Küstenerosion",
     "unit": "m/Jahr", "norm_min": 0.0, "norm_max": 5.0, "spatial": False, "coastal": True,
     "description": "Erosion und Rückgang von Küstenlinien.",
     "proxy": "Konstantwert; nur Küstenkommunen.",
     "source": "BSH"},
    {"code": "SOIL_SALINIZATION", "name": "Bodenversalzung",
     "unit": "Index", "norm_min": 0.0, "norm_max": 1.0, "spatial": True,
     "description": "Versalzung von Böden z. B. durch Meeresspiegelanstieg oder Bewässerungsfehler.",
     "proxy": "Basis Küste/Binnen × Senkenlage (DEM) × Ackeranteil (OSM) × Trockenheit (DWD) × Gewässernähe (Küste) bzw. Tieflage (Binnen).",
     "source": "OSM + Terrarium DEM + DWD CDC"},
    {"code": "COMPOUND_EVENT", "name": "Kombinierte/Compound-Events",
     "unit": "Index", "norm_min": 0.0, "norm_max": 1.0, "spatial": True,
     "description": "Überlagerung mehrerer klimatischer Einflüsse (z. B. Hitze + Dürre).",
     "proxy": "Maximum der normalisierten Bestandteile (Hitze, Dürre, Starkregen) – siehe model_parameters.",
     "source": "abgeleitet (max_of_constituent_hazards)"},
    {"code": "CASCADE_EVENT", "name": "Kaskadeneffekte",
     "unit": "Index", "norm_min": 0.0, "norm_max": 1.0, "spatial": False,
     "description": "Kettenreaktionen zwischen Systemen (z. B. Stromausfall → Wasser → Gesundheit).",
     "proxy": "Qualitativer Konstantwert; keine Rasterquelle.",
     "source": "qualitativ/systemisch"},
    {"code": "SURFACE_WATER_HEATING", "name": "Gewässererwärmung",
     "unit": "°C", "norm_min": 0.0, "norm_max": 5.0, "spatial": True,
     "description": "Anstieg der Oberflächentemperaturen in Fließ- und Stillgewässern.",
     "proxy": "Regionaler Wärmewert, erhöht nahe Wasserflächen (OSM) in warmen Regionen.",
     "source": "DWD / Sentinel"},
    {"code": "LOW_FLOW_NIEDRIGWASSER", "name": "Niedrigwasser / reduzierte Abflüsse",
     "unit": "Tage/Jahr", "norm_min": 0.0, "norm_max": 60.0, "spatial": True,
     "description": "Abflussarmut und Niedrigwasser in Fließgewässern.",
     "proxy": "Niedrigwassertage am nächsten Pegel (PEGELONLINE: Tage < MNW); Fallback Proxy aus heißen Tagen.",
     "source": "BfG / PEGELONLINE (WSV)"},
]


# ── Räumliche Expositionen ────────────────────────────────────────────────────

EXPOSURES: list[dict] = [
    {"code": "POPULATION_DENSITY", "name": "Bevölkerungsdichte",
     "unit": "Pers./km²", "norm_min": 0.0, "norm_max": 8000.0, "spatial": True,
     "description": "Räumliche Dichte der Bevölkerung.",
     "proxy": "Zensus-2022-100m-Gitter: Bevölkerungszahl je Zelle / Fläche.",
     "source": "Zensus 2022 (100m-Gitter, Destatis)"},
    {"code": "AGE_STRUCTURE", "name": "Altersstruktur (Ältere, Kinder)",
     "unit": "%", "norm_min": 0.0, "norm_max": 50.0, "spatial": True,
     "description": "Anteil altersbedingt vulnerabler Bevölkerungsgruppen.",
     "proxy": "Zensus-100m: Anteil ≥65 Jahre + Anteil <18 Jahre je Zelle.",
     "source": "Zensus 2022 (100m-Gitter, Destatis)"},
    {"code": "OUTDOOR_THERMAL_EXPOSURE", "name": "Aufenthalt im Freien (therm. Exposition)",
     "unit": "h/Tag", "norm_min": 0.0, "norm_max": 8.0, "spatial": True,
     "description": "Exposition der Bevölkerung durch Aufenthalt im Freien bei Hitze.",
     "proxy": "Proxy aus Anteil öffentlicher Freiflächen/Arbeitsplätze (OSM) + Bevölkerung.",
     "source": "OSM / Zensus (Proxy)"},
    {"code": "VULNERABLE_GROUPS_POPULATION", "name": "Vulnerable Gruppen (Personen)",
     "unit": "Pers.", "norm_min": 0.0, "norm_max": 2000.0, "spatial": True,
     "description": "Bevölkerungsgruppen mit erhöhter Schadenswahrscheinlichkeit.",
     "proxy": "Zensus-100m: Bevölkerung × (Anteil ≥65 + Anteil <18) je Zelle.",
     "source": "Zensus 2022 (100m-Gitter, Destatis)"},
    {"code": "BUILDING_STOCK", "name": "Gebäudebestand / Gebäudefläche",
     "unit": "m²", "norm_min": 0.0, "norm_max": 6000.0, "spatial": True,
     "description": "Gebäudebestand und bebaute Fläche.",
     "proxy": "OSM-Gebäudegrundflächen pro Zelle.",
     "source": "OSM"},
    {"code": "BUILDING_USE_TYPES", "name": "Nutzungstypen (Wohnen, Gewerbe, kritisch)",
     "unit": "Anzahl", "norm_min": 0.0, "norm_max": 200.0, "spatial": True,
     "description": "Nutzungsarten von Gebäuden inkl. kritischer Nutzungen.",
     "proxy": "Anzahl OSM-Gebäude mit Nutzungstag pro Zelle.",
     "source": "OSM"},
    {"code": "LOCATION_HAZARD_ZONES", "name": "Lage in Gefahrenzonen",
     "unit": "ha", "norm_min": 0.0, "norm_max": 1.0, "spatial": True,
     "description": "Gebäude/Siedlungen in klimarelevanten Gefahrenzonen (Hochwasser, Starkregen, Hitzeinseln).",
     "proxy": "Bebaute Fläche (OSM) in Senken-/UHI-Lage (Topografie + UHI).",
     "source": "OSM + Topografie"},
    {"code": "ENERGY_INFRASTRUCTURE", "name": "Energieanlagen",
     "unit": "Anzahl", "norm_min": 0.0, "norm_max": 20.0, "spatial": True,
     "description": "Energieinfrastruktur als exponiertes Sachgut.",
     "proxy": "OSM power=* (Umspannwerke, Leitungen, Anlagen) pro Zelle.",
     "source": "OSM"},
    {"code": "WATER_WASTEWATER_INFRA", "name": "Wasser/Abwasseranlagen",
     "unit": "Anzahl", "norm_min": 0.0, "norm_max": 20.0, "spatial": True,
     "description": "Wasser- und Abwasserinfrastruktur.",
     "proxy": "OSM man_made=water_works/wastewater_plant u. ä. pro Zelle.",
     "source": "OSM"},
    {"code": "TRANSPORT_HUBS", "name": "Verkehrsknotenpunkte",
     "unit": "Anzahl", "norm_min": 0.0, "norm_max": 20.0, "spatial": True,
     "description": "Verkehrsknoten und -kritikalität.",
     "proxy": "OSM Bahnhöfe/Haltestellen/ÖPNV-Stationen (Knoten) pro Zelle.",
     "source": "OSM"},
    {"code": "COMMUNICATION_INFRA", "name": "Kommunikationsinfrastruktur",
     "unit": "Anzahl", "norm_min": 0.0, "norm_max": 10.0, "spatial": True,
     "description": "Telekommunikations- und Kommunikationsanlagen.",
     "proxy": "OSM communication/tower=communication pro Zelle.",
     "source": "OSM"},
    {"code": "HEALTHCARE_INFRASTRUCTURE", "name": "Gesundheitsversorgung (Erreichbarkeit)",
     "unit": "Index", "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Nähe zu Krankenhaus, Arzt und Apotheke (höher = besserer Zugang).",
     "proxy": "100 · (0,5·prox(20km,KH) + 0,35·prox(20km,Arzt) + 0,15·prox(20km,Apo)); Luftlinie × 1,3.",
     "source": "OSM"},
    {"code": "INDUSTRIAL_COMMERCIAL_AREAS", "name": "Industrie- und Gewerbeflächen",
     "unit": "ha", "norm_min": 0.0, "norm_max": 1.0, "spatial": True,
     "description": "Industrie- und Gewerbeansiedlungen.",
     "proxy": "OSM landuse=industrial/commercial/retail-Flächenanteil pro Zelle.",
     "source": "OSM / Copernicus Land"},
    {"code": "AGRICULTURAL_LAND", "name": "Landwirtschaftliche Nutzflächen",
     "unit": "ha", "norm_min": 0.0, "norm_max": 1.0, "spatial": True,
     "description": "Landwirtschaftlich genutzte Flächen.",
     "proxy": "OSM landuse=farmland/orchard/vineyard-Anteil pro Zelle.",
     "source": "OSM / Copernicus Land"},
    {"code": "SUPPLY_CHAIN_NODES", "name": "Lieferkettenknoten (Logistik)",
     "unit": "Anzahl", "norm_min": 0.0, "norm_max": 10.0, "spatial": True,
     "description": "Logistik- und Versorgungsknoten der Wirtschaft.",
     "proxy": "OSM landuse=industrial + warehouse/logistics pro Zelle.",
     "source": "OSM"},
    {"code": "FOREST_AREA", "name": "Waldflächen",
     "unit": "ha", "norm_min": 0.0, "norm_max": 1.0, "spatial": True,
     "description": "Wald- und Forstflächen.",
     "proxy": "OSM landuse=forest / natural=wood-Anteil pro Zelle.",
     "source": "OSM / Copernicus Land"},
    {"code": "BIODIVERSITY_HOTSPOTS", "name": "Biodiversitäts-Hotspots",
     "unit": "ha", "norm_min": 0.0, "norm_max": 1.0, "spatial": True,
     "description": "Räume mit besonders hoher Biodiversität.",
     "proxy": "OSM Schutzgebiete (leisure=nature_reserve, boundary=protected_area) + Wald/Wasser.",
     "source": "OSM / Copernicus Land"},
    {"code": "EROSION_PRONE_SOILS", "name": "Erosionsgefährdete Flächen",
     "unit": "ha", "norm_min": 0.0, "norm_max": 1.0, "spatial": True,
     "description": "Erosionsanfällige Boden- und Landflächen.",
     "proxy": "Unbedeckte/landwirtschaftliche Flächen an Hängen (Topografie-Proxy).",
     "source": "ESDAC / BKG (Proxy)"},
    {"code": "COASTAL_RIPARIAN_ZONES", "name": "Küsten- und Uferzonen",
     "unit": "ha", "norm_min": 0.0, "norm_max": 1.0, "spatial": True,
     "description": "Küsten- und Flussuferbereiche.",
     "proxy": "Ufernähe (OSM water/waterway-Distanz) × TWI (Terrarium-DEM).",
     "source": "OSM + AWS Terrarium DEM"},
    {"code": "FLOODPLAINS", "name": "Überschwemmungsflächen",
     "unit": "ha", "norm_min": 0.0, "norm_max": 1.0, "spatial": True,
     "description": "Hochwasser- und Überschwemmungsflächen.",
     "proxy": "Senkentiefe/TWI (Terrarium-DEM) × Gewässernähe (OSM).",
     "source": "OSM + AWS Terrarium DEM"},
    {"code": "COASTAL_STORM_SURGE_EXPOSURE", "name": "Küstennähe / Sturmflutgefährdung",
     "unit": "ha", "norm_min": 0.0, "norm_max": 1.0, "spatial": False, "coastal": True,
     "description": "Küstennahe Exposition gegenüber Sturmflut.",
     "proxy": "Bebaute Fläche; nur Küstenkommunen.",
     "source": "OSM (Küste)"},
    {"code": "GROUNDWATER_DEPENDENT_ECOSYSTEMS", "name": "Grundwasserabhängige Ökosysteme",
     "unit": "ha", "norm_min": 0.0, "norm_max": 1.0, "spatial": True,
     "description": "Ökosysteme mit Abhängigkeit vom Grundwasser.",
     "proxy": "Feuchtgebiete/Wald nahe Gewässern (OSM natural=wetland + Wald).",
     "source": "OSM / UBA"},
    {"code": "FISHERIES_AQUACULTURE_AREAS", "name": "Fischerei-/Aquakulturbetriebe",
     "unit": "Anzahl", "norm_min": 0.0, "norm_max": 5.0, "spatial": True,
     "description": "Exposition von Fischerei und Aquakulturanlagen.",
     "proxy": "OSM Aquakultur/Fischerei + Wasserflächenanteil.",
     "source": "OSM / BMEL"},
    {"code": "FISH_SPAWNING_HABITATS", "name": "Laich- und Aufwuchsgebiete",
     "unit": "ha", "norm_min": 0.0, "norm_max": 1.0, "spatial": True,
     "description": "Räumlich relevante fischereiliche Lebensräume.",
     "proxy": "Wasserfläche + Gewässernähe (OSM water/waterway-Distanz).",
     "source": "OSM / LfU"},
]


# ── Sensitivitäten ──────────────────────────────────────────────────────────────
# Die meisten sind Index 0..100 (höher = verwundbarer). Anpassungskapazitäten
# (z. B. Frühwarnung, Redundanz) werden invertiert gespeichert, sodass ein hoher
# Wert immer „mehr Risiko" bedeutet.

VULNERABILITIES: list[dict] = [
    {"code": "BUILDING_STABILITY", "name": "Gebäudestabilität (invers)", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Physische Widerstandsfähigkeit von Gebäuden (hoher Wert = geringe Stabilität).",
     "proxy": "Aus Zensus-Gebäudealter (älter = anfälliger), moduliert über OSM-Gebäudehöhe.",
     "source": "Zensus 2022 / OSM"},
    {"code": "CRITICAL_INFRA_CONDITION", "name": "Zustand kritischer Infrastruktur", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": False,
     "description": "Technischer Zustand und Alter kritischer Infrastruktur.",
     "proxy": "Regionaler Annahmewert (kommunale Metadaten nicht zentral verfügbar).",
     "source": "Annahme (kommunal)"},
    {"code": "MATERIAL_HEAT_SENSITIVITY", "name": "Materialanfälligkeit (Hitze)", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Hitzeempfindlichkeit von Materialien (z. B. Asphalt).",
     "proxy": "Versiegelungs-/Straßenanteil (OSM) als Proxy für hitzeempfindliche Beläge.",
     "source": "OSM"},
    {"code": "VULNERABLE_GROUPS_SHARE", "name": "Anteil vulnerabler Gruppen", "unit": "%",
     "norm_min": 0.0, "norm_max": 50.0, "spatial": True,
     "description": "Anteil sozial vulnerabler Bevölkerungsgruppen.",
     "proxy": "Zensus-100m: Anteil ≥65 + Anteil <18 Jahre je Zelle.",
     "source": "Zensus 2022 (100m-Gitter, Destatis)"},
    {"code": "INCOME_SOCIAL_RESILIENCE", "name": "Soziale Resilienz (invers)", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Sozioökonomische Resilienz (hoher Wert = geringe Resilienz).",
     "proxy": "Kombination aus Nettokaltmiete, Eigentümerquote und Wohnfläche je Bewohner (Zensus-100m).",
     "source": "Zensus 2022 (100m-Gitter, Destatis)"},
    {"code": "HEALTHCARE_ACCESS", "name": "Zugang zu Gesundheitsdiensten (invers)", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Erreichbarkeit von Gesundheitsdiensten (hoher Wert = schlechter Zugang).",
     "proxy": "100 · (1 − (0,5·prox(KH) + 0,35·prox(Arzt) + 0,15·prox(Apo))); prox = 1 − min(dist,20km)/20km; dist = Luftlinie × 1,3.",
     "source": "OSM"},
    {"code": "WILDFIRE_SUSCEPTIBILITY", "name": "Waldbrandanfälligkeit", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Ökologische Anfälligkeit für Waldbrände.",
     "proxy": "Nadelwald-/Wald-/Trockenanteil (OSM + Trockenheit).", "source": "OSM / Sentinel"},
    {"code": "BIODIVERSITY_RESILIENCE", "name": "Biodiversitätsresilienz (invers)", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Widerstandsfähigkeit von Biodiversität (hoher Wert = geringe Resilienz).",
     "proxy": "Fragmentierung/geringer Grünanteil als Proxy.", "source": "OSM / Copernicus"},
    {"code": "SOIL_SENSITIVITY", "name": "Bodenempfindlichkeit", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Empfindlichkeit von Böden gegen Erosion und Versalzung.",
     "proxy": "Hangneigung + landwirtschaftlicher/unbedeckter Anteil.", "source": "ESDAC / BKG (Proxy)"},
    {"code": "SINGLE_SITE_DEPENDENCY", "name": "Abhängigkeit von Einzelstandorten", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Wirtschaftliche Konzentration auf einzelne Standorte.",
     "proxy": "Konzentration von Gewerbe-/Industriefläche pro Zelle.", "source": "OSM"},
    {"code": "SUPPLY_CHAIN_DEPENDENCY", "name": "Abhängigkeit von Lieferketten", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": False,
     "description": "Abhängigkeit von externen Lieferketten.", "proxy": "Regionaler Annahmewert.",
     "source": "Annahme"},
    {"code": "FINANCIAL_ADAPTATION_CAPACITY", "name": "Finanzielle Anpassungskapazität (invers)", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": False,
     "description": "Finanzielle Mittel für Anpassung (hoher Wert = geringe Kapazität).",
     "proxy": "Steuereinnahmekraft & Arbeitslosenquote je AGS (invertiert); Fallback neutral 50.",
     "source": "BBSR INKAR / Regionalstatistik"},
    {"code": "INFRA_CRITICALITY", "name": "Kritikalität von Infrastrukturen", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Systemkritikalität einzelner Infrastrukturen.",
     "proxy": "Gewichtete Dichte kritischer KRITIS-Assets (Energie, Wasser, IT/TK, Gesundheit, Verkehr) pro Zelle (OSM).",
     "source": "OSM"},
    {"code": "REDUNDANCY_BACKUP", "name": "Redundanzen / Backup (invers)", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": False,
     "description": "Vorhandene Redundanzen (hoher Wert = wenig Redundanz).",
     "proxy": "Regionaler Annahmewert.", "source": "Annahme"},
    {"code": "INFRA_DEPENDENCY_CHAIN", "name": "Infrastruktur-Abhängigkeiten", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": False,
     "description": "Funktionale Abhängigkeiten zwischen Infrastruktursystemen.",
     "proxy": "Regionaler Annahmewert.", "source": "Annahme"},
    {"code": "HEAT_SENSITIVITY", "name": "Hitzesensitivität", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Gesundheitliche Empfindlichkeit gegenüber Hitze.",
     "proxy": "Altersstruktur + UHI-Intensität + geringer Grünanteil pro Zelle.",
     "source": "Zensus + UHI-Modell"},
    {"code": "AIR_QUALITY_RISK", "name": "Luftqualitätsrisiko", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Vulnerabilität durch schlechte Luftqualität (oft hitzekoppelt).",
     "proxy": "Verkehrs-/Industriedichte + geringe Belüftung (OSM).", "source": "OSM / UBA"},
    {"code": "DISEASE_VECTOR_SUSCEPTIBILITY", "name": "Krankheitsanfälligkeit (Vektoren)", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Anfälligkeit für vektorübertragene Krankheiten.",
     "proxy": "Stehende Gewässer/Feuchtflächen + Wärme.", "source": "OSM / UBA (Proxy)"},
    {"code": "GROUNDWATER_DEPENDENCY", "name": "Grundwasserabhängigkeit", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Abhängigkeit von Grundwasserressourcen.",
     "proxy": "Anteil Landwirtschaft/Grünfläche pro Zelle.", "source": "OSM / UBA"},
    {"code": "WATER_STRESS_INDEX", "name": "Wasserstressindex", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Wasserstress durch Nachfrage und Verfügbarkeit.",
     "proxy": "Versiegelung + Bevölkerungsdichte + regionale Trockenheit.", "source": "UBA (Proxy)"},
    {"code": "IRRIGATION_DEPENDENCY", "name": "Bewässerungsabhängigkeit", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Abhängigkeit der Landwirtschaft von Bewässerung.",
     "proxy": "Landwirtschaftsanteil × regionale Trockenheit.", "source": "OSM / Copernicus"},
    {"code": "EROSION_SUSCEPTIBILITY", "name": "Erosionsanfälligkeit", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Anfälligkeit von Küsten und Hängen für Erosion.",
     "proxy": "Hangneigung + geringe Vegetationsbedeckung.", "source": "ESDAC / BKG (Proxy)"},
    {"code": "LEVEE_CONDITION", "name": "Deichzustand (invers)", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": True, "coastal": True,
     "description": "Baulicher Zustand von Deichen (hoher Wert = schlecht).",
     "proxy": "OSM man_made=dyke/embankment (Nähe) × Hochwasser-/Küstenexposition; Basis 50/30.",
     "source": "OSM"},
    {"code": "SALTWATER_INTRUSION_RISK", "name": "Salzwasserintrusionsrisiko", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": False, "coastal": True,
     "description": "Risiko salinen Grundwassers und Einbruchs.",
     "proxy": "Konstantwert; Küstenkommunen.", "source": "UBA"},
    {"code": "SEALING_DEGREE", "name": "Versiegelungsgrad", "unit": "%",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Grad der Bodenversiegelung in Siedlungen.",
     "proxy": "Direkt aus OSM-Versiegelungsmodell (Gebäude + Straßen + Landnutzung).", "source": "OSM"},
    {"code": "UHI_INTENSITY", "name": "Wärmeinselintensität", "unit": "K",
     "norm_min": 0.0, "norm_max": 8.0, "spatial": True,
     "description": "Intensität der städtischen Wärmeinsel (ΔT).",
     "proxy": "UHI-Modell ΔT pro 100m-Zelle (Versiegelung, Albedo, Grün/Wasser, Bebauung, Belüftung).",
     "source": "UHI-Modell (OSM)"},
    {"code": "GREEN_SPACE_SHARE", "name": "Grünflächenmangel (invers)", "unit": "%",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Mangel an Grünflächen (hoher Wert = wenig Grün).",
     "proxy": "100 − Grünflächenanteil (OSM) pro Zelle.", "source": "OSM"},
    {"code": "EARLY_WARNING_SYSTEMS", "name": "Frühwarnsysteme (invers)", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Vorhandensein/Qualität von Frühwarnsystemen (hoher Wert = fehlend).",
     "proxy": "OSM Feuerwehr/Rettung (Nähe, invertiert; Proxy), zur Neutrale gedämpft.",
     "source": "OSM"},
    {"code": "EMERGENCY_MANAGEMENT", "name": "Notfallmanagement (invers)", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Kapazität des Notfall-/Katastrophenmanagements (hoher Wert = gering).",
     "proxy": "Distanz zu OSM Feuerwehr/Rettung (invertiert).", "source": "OSM"},
    {"code": "PLANNING_IMPLEMENTATION_CAPACITY", "name": "Planungs-/Umsetzungskapazität (invers)", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": False,
     "description": "Governance-Kapazität (hoher Wert = gering).",
     "proxy": "Kommunale Finanzkraft (Steuereinnahmekraft je AGS, invertiert); Fallback neutral 50.",
     "source": "BBSR INKAR / Regionalstatistik"},
    {"code": "FISHERIES_TEMPERATURE_SENSITIVITY", "name": "Temp.-Empfindlichkeit Fischbestände", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Empfindlichkeit von Fischarten gegen Wärme/Niedrigwasser.",
     "proxy": "Gewässeranteil × regionale Gewässererwärmung.", "source": "LfU / DWD (Proxy)"},
    {"code": "AQUACULTURE_TECHNICAL_VULNERABILITY", "name": "Anfälligkeit Aquakultur", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": False,
     "description": "Technische Anfälligkeit von Aquakulturanlagen.",
     "proxy": "Regionaler Annahmewert.", "source": "BMEL (Annahme)"},
    {"code": "FISHERIES_MANAGEMENT_CAPACITY", "name": "Fischerei-Anpassungsfähigkeit (invers)", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": False,
     "description": "Kapazität für monitoringbasierte Anpassung (hoher Wert = gering).",
     "proxy": "Regionaler Annahmewert.", "source": "BMEL (Annahme)"},
]


# ── Risiken ──────────────────────────────────────────────────────────────────────
# group = KWRA-Gruppe (Code); cost_dimension ∈ {health, monetary, environment, operational}
# hazards/exposures/vulnerabilities = Listen (erste = primär).
# ref_value = Outcome-Wert bei Index=100 für eine Referenzkommune mit 100.000 Ew.
# scale = wie der Outcome mit der Kommune skaliert: pop | area | flat.
# Für cost_dimension=='monetary' ist ref_value in €/Jahr (Schadenkosten).

RISKS: list[dict] = [
    {"code": "EXPECTED_ANNUAL_MORTALITY", "name": "Erwartete jährliche Mortalität",
     "outcome_unit": "Todesfälle/Jahr", "group": "heat", "cost_dimension": "health",
     "hazards": ["HEAT_WAVE", "COLD_EXTREME", "COMPOUND_EVENT"],
     "exposures": ["POPULATION_DENSITY", "VULNERABLE_GROUPS_POPULATION", "AGE_STRUCTURE"],
     "vulnerabilities": ["HEAT_SENSITIVITY", "HEALTHCARE_ACCESS", "VULNERABLE_GROUPS_SHARE"],
     # Herleitung: Worst-Case-Anker 18/100k bei Index=100 ≈ 1,7× schlimmstes beobachtetes Jahr (2018: ~8.700 Tote = 10,5/100k; RKI/Winklmayr 2022). Typische Kommune P90-Index 20-40 ⇒ 3,6-7,2/100k (statistikkonform, UBA GE-I-2).
     # cost_per_outcome_eur: VSL-Punktwert 3,5 Mio € im gängigen EU/OECD-Band (~1-4 Mio); UBA MK3.1 nennt keinen einzelnen VSL-Wert (bewertet nur Luftschadstoff-/Lärmeffekte), daher Punktwert im Band statt exaktem UBA-Wert.
     "ref_value": 18.0, "scale": "pop", "cost_per_outcome_eur": 3500000.0, "source": "RKI 2022 / Winklmayr u.a. 2022 / UBA MK3.1 2020",
     "description": "Erwartete jährliche Mortalität durch klimatische Belastungen.",
     "priority": 1},
    {"code": "EXPECTED_ANNUAL_MORBIDITY", "name": "Erwartete jährliche Morbidität",
     "outcome_unit": "Fälle/Jahr", "group": "heat", "cost_dimension": "health",
     "hazards": ["HEAT_WAVE", "DROUGHT", "HEAVY_RAIN_FLOOD"],
     "exposures": ["POPULATION_DENSITY", "VULNERABLE_GROUPS_POPULATION"],
     "vulnerabilities": ["HEAT_SENSITIVITY", "DISEASE_VECTOR_SUSCEPTIBILITY", "HEALTHCARE_ACCESS"],
     # Modellannahme (Punktwert, editierbar): kalibriert gegen Größenordnung der UBA-MK3.1-Morbiditätskostensätze; keine belastbare nationale Pro-Kopf-Fallstatistik ⇒ als Annahme gekennzeichnet, nicht als Herleitung.
     "ref_value": 320.0, "scale": "pop", "cost_per_outcome_eur": 5000.0, "source": "UBA MK3.1 2020 / RKI JoHM",
     "description": "Erwartete jährliche Morbidität (Erkrankungen).", "priority": 1},
    {"code": "EXPECTED_ANNUAL_INJURIES", "name": "Erwartete jährliche Verletztenzahlen",
     "outcome_unit": "Verletzte/Jahr", "group": "flood", "cost_dimension": "health",
     "hazards": ["HEAVY_RAIN_FLOOD", "EXTRATROPICAL_STORM", "LANDSLIDE"],
     "exposures": ["POPULATION_DENSITY", "LOCATION_HAZARD_ZONES"],
     "vulnerabilities": ["EMERGENCY_MANAGEMENT", "EARLY_WARNING_SYSTEMS"],
     # Modellannahme (Punktwert, editierbar): Größenordnung Verletztenzahlen bei Extremereignissen (Sturm/Starkregen); keine belastbare nationale Pro-Kopf-Statistik ⇒ als Annahme gekennzeichnet.
     "ref_value": 45.0, "scale": "pop", "cost_per_outcome_eur": 12000.0, "source": "UBA MK3.1 2020 / RKI JoHM",
     "description": "Erwartete jährliche Verletztenzahlen durch Extremereignisse.", "priority": 2},
    {"code": "EXPECTED_ANNUAL_MENTAL_HEALTH", "name": "Psychische Belastungsfälle",
     "outcome_unit": "Fälle/Jahr", "group": "compound", "cost_dimension": "health",
     "hazards": ["HEAT_WAVE", "DROUGHT", "COMPOUND_EVENT", "CASCADE_EVENT"],
     "exposures": ["POPULATION_DENSITY", "VULNERABLE_GROUPS_POPULATION"],
     "vulnerabilities": ["INCOME_SOCIAL_RESILIENCE", "HEALTHCARE_ACCESS"],
     # Modellannahme (Punktwert, editierbar): Größenordnung psychischer Belastungsfälle nach Extremwetter; keine belastbare nationale Pro-Kopf-Statistik ⇒ als Annahme gekennzeichnet.
     "ref_value": 150.0, "scale": "pop", "cost_per_outcome_eur": 4000.0, "source": "UBA MK3.1 2020 / RKI JoHM",
     "description": "Erwartete jährliche Fälle psychischer Belastung.", "priority": 2},
    {"code": "EXPECTED_ANNUAL_AFFECTED_EVACUATED", "name": "Betroffene/Evakuierte Personen",
     "outcome_unit": "Personen/Jahr", "group": "flood", "cost_dimension": "health",
     "hazards": ["HEAVY_RAIN_FLOOD", "STORM_SURGE", "WILDFIRE"],
     "exposures": ["POPULATION_DENSITY", "LOCATION_HAZARD_ZONES", "COASTAL_STORM_SURGE_EXPOSURE"],
     "vulnerabilities": ["EMERGENCY_MANAGEMENT", "EARLY_WARNING_SYSTEMS"],
     # Modellannahme (Punktwert, editierbar): Größenordnung Evakuierten-/Betroffenenzahlen bei Hochwasser/Sturmflut; keine belastbare nationale Pro-Kopf-Statistik ⇒ als Annahme gekennzeichnet.
     "ref_value": 800.0, "scale": "pop", "cost_per_outcome_eur": 2500.0, "source": "UBA MK3.1 2020 / RKI JoHM",
     "description": "Erwartete jährliche Zahl betroffener oder evakuierter Personen.", "priority": 1},
    {"code": "EXPECTED_THERMAL_STRESS_HOURS", "name": "Stunden thermischer Belastung",
     "outcome_unit": "Stunden/Jahr", "group": "heat", "cost_dimension": "health",
     "hazards": ["HEAT_WAVE", "MEAN_TEMPERATURE_RISE"],
     "exposures": ["OUTDOOR_THERMAL_EXPOSURE", "POPULATION_DENSITY"],
     "vulnerabilities": ["HEAT_SENSITIVITY", "UHI_INTENSITY", "GREEN_SPACE_SHARE"],
     # Kein Kostensatz (cost_per_outcome_eur=0); reiner Belastungsindikator, Punktwert als Modellannahme.
     "ref_value": 400.0, "scale": "pop", "cost_per_outcome_eur": 0.0, "source": "Modellannahme (Belastungsstunden, unbelegt)",
     "description": "Erwartete jährliche Stunden thermischer Belastung.", "priority": 1},
    {"code": "EXPECTED_POLLUTANT_EXPOSURE_HOURS", "name": "Schadstoffexpositionsstunden",
     "outcome_unit": "Stunden/Jahr", "group": "heat", "cost_dimension": "health",
     "hazards": ["HEAT_WAVE", "MEAN_TEMPERATURE_RISE"],
     "exposures": ["POPULATION_DENSITY", "OUTDOOR_THERMAL_EXPOSURE"],
     "vulnerabilities": ["AIR_QUALITY_RISK", "HEAT_SENSITIVITY"],
     # Kein Kostensatz (cost_per_outcome_eur=0); reiner Belastungsindikator, Punktwert als Modellannahme.
     "ref_value": 250.0, "scale": "pop", "cost_per_outcome_eur": 0.0, "source": "Modellannahme (Belastungsstunden, unbelegt)",
     "description": "Erwartete jährliche Schadstoffexpositionsstunden.", "priority": 2},
    {"code": "EXPECTED_BUILDING_DAMAGE_EUR", "name": "Gebäudeschäden",
     "outcome_unit": "€/Jahr", "group": "flood", "cost_dimension": "monetary",
     "hazards": ["HEAT_WAVE", "HEAVY_RAIN_FLOOD", "EXTRATROPICAL_STORM"],
     "exposures": ["BUILDING_STOCK", "LOCATION_HAZARD_ZONES"],
     "vulnerabilities": ["BUILDING_STABILITY", "FINANCIAL_ADAPTATION_CAPACITY"],
     # Herleitung: nat. jährl. Gebäudeschäden (Hochwasser+Sturm/Hagel) ~3,5 Mrd €/J ÷ 832 (100k-Einw.-Einheiten DE) ≈ 4,2 Mio €/100k → 4,5 Mio bei Index=100. Prognos 2023: Ahr-Anteil Bauwesen+Privathaushalte 20,9 von 40,5 Mrd €.
     "ref_value": 4500000.0, "scale": "pop", "source": "Prognos/GWS/IÖW 2023", "description": "Erwartete jährliche Gebäudeschäden.", "priority": 1},
    {"code": "EXPECTED_TRANSPORT_DAMAGE_EUR", "name": "Schäden an Verkehrswegen",
     "outcome_unit": "€/Jahr", "group": "flood", "cost_dimension": "monetary",
     "hazards": ["HEAT_WAVE", "HEAVY_RAIN_FLOOD", "DROUGHT"],
     "exposures": ["TRANSPORT_HUBS", "LOCATION_HAZARD_ZONES"],
     "vulnerabilities": ["MATERIAL_HEAT_SENSITIVITY", "CRITICAL_INFRA_CONDITION"],
     # Herleitung: nat. jährl. Verkehrsinfrastruktur-Schäden ~1,5 Mrd €/J ÷ 832 ≈ 1,8 Mio €/100k bei Index=100. Prognos 2023: Ahr-Anteil Verkehr 6,8 von 40,5 Mrd € (~17%).
     "ref_value": 1800000.0, "scale": "pop", "source": "Prognos/GWS/IÖW 2023", "description": "Erwartete jährliche Schäden an Verkehrswegen.", "priority": 2},
    {"code": "EXPECTED_ENERGY_INFRA_DAMAGE_EUR", "name": "Schäden an Energieinfrastruktur",
     "outcome_unit": "€/Jahr", "group": "flood", "cost_dimension": "monetary",
     "hazards": ["HEAT_WAVE", "EXTRATROPICAL_STORM", "HEAVY_RAIN_FLOOD"],
     "exposures": ["ENERGY_INFRASTRUCTURE"],
     "vulnerabilities": ["CRITICAL_INFRA_CONDITION", "REDUNDANCY_BACKUP"],
     # Herleitung: nat. jährl. Energieinfrastruktur-Schäden ~0,75 Mrd €/J ÷ 832 ≈ 0,9 Mio €/100k bei Index=100. Prognos 2023 (Teilmenge Industrie/Infrastruktur der Extremwetterschäden).
     "ref_value": 900000.0, "scale": "pop", "source": "Prognos/GWS/IÖW 2023", "description": "Erwartete jährliche Schäden an Energieinfrastruktur.", "priority": 1},
    {"code": "EXPECTED_TELECOM_DAMAGE_EUR", "name": "Schäden an Telekommunikation",
     "outcome_unit": "€/Jahr", "group": "flood", "cost_dimension": "monetary",
     "hazards": ["EXTRATROPICAL_STORM", "HEAVY_RAIN_FLOOD"],
     "exposures": ["COMMUNICATION_INFRA"],
     "vulnerabilities": ["CRITICAL_INFRA_CONDITION", "REDUNDANCY_BACKUP"],
     # Herleitung: nat. jährl. Telekommunikationsschäden ~0,33 Mrd €/J ÷ 832 ≈ 0,4 Mio €/100k bei Index=100. Prognos 2023 (kleiner Infrastruktur-Teilbetrag).
     "ref_value": 400000.0, "scale": "pop", "source": "Prognos/GWS/IÖW 2023", "description": "Erwartete jährliche Schäden an Telekommunikationsinfrastruktur.", "priority": 2},
    {"code": "EXPECTED_WATER_WASTEWATER_DAMAGE_EUR", "name": "Schäden Wasser-/Abwasser",
     "outcome_unit": "€/Jahr", "group": "flood", "cost_dimension": "monetary",
     "hazards": ["HEAVY_RAIN_FLOOD", "DROUGHT", "HEAT_WAVE"],
     "exposures": ["WATER_WASTEWATER_INFRA"],
     "vulnerabilities": ["CRITICAL_INFRA_CONDITION", "GROUNDWATER_DEPENDENCY"],
     # Herleitung: nat. jährl. Wasser-/Abwasserschäden ~0,58 Mrd €/J ÷ 832 ≈ 0,7 Mio €/100k bei Index=100. Prognos 2023: Ahr-Anteil Wasser/Hochwasser-/Küstenschutz 2,5 von 40,5 Mrd € + Dürre-Wasserkosten.
     "ref_value": 700000.0, "scale": "pop", "source": "Prognos/GWS/IÖW 2023", "description": "Erwartete jährliche Schäden an Wasser-/Abwassersystemen.", "priority": 1},
    {"code": "EXPECTED_AGRICULTURAL_DAMAGE_EUR", "name": "Landwirtschaftliche Schäden",
     "outcome_unit": "€/Jahr", "group": "drought", "cost_dimension": "monetary",
     "hazards": ["DROUGHT", "HEAT_WAVE", "HEAVY_RAIN_FLOOD"],
     "exposures": ["AGRICULTURAL_LAND"],
     "vulnerabilities": ["IRRIGATION_DEPENDENCY", "WATER_STRESS_INDEX", "SOIL_SENSITIVITY"],
     # Herleitung: nat. landwirtschaftl. Klimaschaden ~3,9 Mrd €/J (Hitze/Dürre 2018/19: ~7,8 Mrd € über 2 J) ÷ Ackerland-Einheiten (~166.000 km²/50 = 3.320) ≈ 1,2 Mio €/50 km² Ackerland; auf 2,2 Mio bei Index=100 (Worst-Case-Dürrejahr) angehoben. scale=area an Nutzfläche der Kommune. Prognos 2023.
     "ref_value": 2200000.0, "scale": "area", "source": "Prognos/GWS/IÖW 2023", "description": "Erwartete jährliche landwirtschaftliche Schäden / Ernteverluste.", "priority": 1},
    {"code": "EXPECTED_TOTAL_DAMAGE_EAD_EUR", "name": "Gesamtschäden (EAD)",
     "outcome_unit": "€/Jahr", "group": "compound", "cost_dimension": "monetary",
     "hazards": ["HEAT_WAVE", "HEAVY_RAIN_FLOOD", "DROUGHT", "EXTRATROPICAL_STORM"],
     "exposures": ["BUILDING_STOCK", "ENERGY_INFRASTRUCTURE", "AGRICULTURAL_LAND"],
     "vulnerabilities": ["BUILDING_STABILITY", "FINANCIAL_ADAPTATION_CAPACITY", "CRITICAL_INFRA_CONDITION"],
     # Herleitung: nat. jährl. Gesamtschaden (EAD) ~8 Mrd €/J ÷ 832 ≈ 9,6 Mio €/100k → 10 Mio bei Index=100. Prognos 2023: seit 2000 ≥70 Mrd € Hochwasser + 35 Mrd € Hitze/Dürre 2018/19; Einzeljahr wie 2021 ~40 Mrd €.
     "ref_value": 10000000.0, "scale": "pop", "source": "Prognos/GWS/IÖW 2023", "description": "Erwartete jährliche Gesamtschäden (Expected Annual Damage).", "priority": 1},
    {"code": "EXPECTED_RESTORATION_COSTS_EUR", "name": "Wiederherstellungskosten",
     "outcome_unit": "€/Jahr", "group": "flood", "cost_dimension": "monetary",
     "hazards": ["HEAVY_RAIN_FLOOD", "EXTRATROPICAL_STORM", "WILDFIRE"],
     "exposures": ["BUILDING_STOCK", "FOREST_AREA", "ENERGY_INFRASTRUCTURE"],
     "vulnerabilities": ["FINANCIAL_ADAPTATION_CAPACITY", "PLANNING_IMPLEMENTATION_CAPACITY"],
     # Herleitung: Wiederherstellungskosten als Teilmenge des EAD ~1,25 Mrd €/J ÷ 832 ≈ 1,5 Mio €/100k bei Index=100 (Prognos 2023, Reparatur-/Wiederaufbauanteil der Sektorschäden).
     "ref_value": 1500000.0, "scale": "pop", "source": "Prognos/GWS/IÖW 2023", "description": "Erwartete jährliche Wiederherstellungskosten.", "priority": 2},
    {"code": "EXPECTED_SOIL_LOSS_DEGRADATION_EUR", "name": "Bodenverluste / -degradation (€)",
     "outcome_unit": "€/Jahr", "group": "drought", "cost_dimension": "monetary",
     "hazards": ["DROUGHT", "HEAVY_RAIN_FLOOD", "SOIL_SALINIZATION"],
     "exposures": ["EROSION_PRONE_SOILS", "AGRICULTURAL_LAND"],
     "vulnerabilities": ["SOIL_SENSITIVITY", "IRRIGATION_DEPENDENCY"],
     # Herleitung: Bodenverlust-/Erosionskosten ~2 Mrd €/J ÷ 3.320 Ackerland-Einheiten (50 km²) ≈ 0,6 Mio €/50 km² bei Index=100. scale=area an Nutzfläche der Kommune. Prognos 2023 (Teilbetrag Landwirtschaft/Boden).
     "ref_value": 600000.0, "scale": "area", "source": "Prognos/GWS/IÖW 2023", "description": "Erwartete jährliche Bodenverluste / Bodendegradation.", "priority": 2},
    {"code": "EXPECTED_CI_OUTAGE_HOURS", "name": "Ausfallzeiten kritischer Infrastruktur",
     "outcome_unit": "Stunden/Jahr", "group": "compound", "cost_dimension": "operational",
     "hazards": ["HEAVY_RAIN_FLOOD", "EXTRATROPICAL_STORM", "CASCADE_EVENT"],
     "exposures": ["ENERGY_INFRASTRUCTURE", "WATER_WASTEWATER_INFRA", "COMMUNICATION_INFRA"],
     "vulnerabilities": ["INFRA_CRITICALITY", "REDUNDANCY_BACKUP", "INFRA_DEPENDENCY_CHAIN"],
     # BBK/Betreiber-Kennzahlen zu KRITIS-Ausfallzeiten; ohne Rohdaten als Modellannahme markiert.
     "ref_value": 120.0, "scale": "flat", "source": "BBK KRITIS (Modellannahme)", "description": "Erwartete jährliche Ausfallzeiten kritischer Infrastrukturen.", "priority": 1},
    {"code": "EXPECTED_ENERGY_OUTAGE_HOURS", "name": "Ausfallstunden Energieversorgung",
     "outcome_unit": "Stunden/Jahr", "group": "compound", "cost_dimension": "operational",
     "hazards": ["EXTRATROPICAL_STORM", "HEAT_WAVE", "HEAVY_RAIN_FLOOD"],
     "exposures": ["ENERGY_INFRASTRUCTURE"],
     "vulnerabilities": ["CRITICAL_INFRA_CONDITION", "REDUNDANCY_BACKUP"],
     # BBK/Betreiber-Kennzahlen (Energieversorgung); ohne Rohdaten als Modellannahme markiert.
     "ref_value": 40.0, "scale": "flat", "source": "BBK KRITIS (Modellannahme)", "description": "Erwartete Ausfallstunden der Energieversorgung.", "priority": 1},
    {"code": "EXPECTED_WATER_SUPPLY_OUTAGE_HOURS", "name": "Ausfallstunden Wasserversorgung",
     "outcome_unit": "Stunden/Jahr", "group": "drought", "cost_dimension": "operational",
     "hazards": ["DROUGHT", "HEAVY_RAIN_FLOOD", "CASCADE_EVENT"],
     "exposures": ["WATER_WASTEWATER_INFRA"],
     "vulnerabilities": ["GROUNDWATER_DEPENDENCY", "WATER_STRESS_INDEX", "INFRA_DEPENDENCY_CHAIN"],
     # BBK/Betreiber-Kennzahlen (Wasserversorgung); ohne Rohdaten als Modellannahme markiert.
     "ref_value": 30.0, "scale": "flat", "source": "BBK KRITIS (Modellannahme)", "description": "Erwartete Ausfallstunden der Wasserversorgung.", "priority": 1},
    {"code": "EXPECTED_WASTEWATER_OUTAGE_HOURS", "name": "Ausfallstunden Abwasserentsorgung",
     "outcome_unit": "Stunden/Jahr", "group": "flood", "cost_dimension": "operational",
     "hazards": ["HEAVY_RAIN_FLOOD", "HEAT_WAVE"],
     "exposures": ["WATER_WASTEWATER_INFRA"],
     "vulnerabilities": ["CRITICAL_INFRA_CONDITION", "SEALING_DEGREE"],
     # BBK/Betreiber-Kennzahlen (Abwasserentsorgung); ohne Rohdaten als Modellannahme markiert.
     "ref_value": 25.0, "scale": "flat", "source": "BBK KRITIS (Modellannahme)", "description": "Erwartete Ausfallstunden der Abwasserentsorgung.", "priority": 2},
    {"code": "EXPECTED_COMMUNICATION_OUTAGE_HOURS", "name": "Ausfallzeiten Kommunikation",
     "outcome_unit": "Stunden/Jahr", "group": "flood", "cost_dimension": "operational",
     "hazards": ["EXTRATROPICAL_STORM", "HEAVY_RAIN_FLOOD"],
     "exposures": ["COMMUNICATION_INFRA"],
     "vulnerabilities": ["CRITICAL_INFRA_CONDITION", "REDUNDANCY_BACKUP"],
     # BBK/Betreiber-Kennzahlen (Kommunikation); ohne Rohdaten als Modellannahme markiert.
     "ref_value": 20.0, "scale": "flat", "source": "BBK KRITIS (Modellannahme)", "description": "Erwartete Ausfallzeiten der Kommunikationssysteme.", "priority": 2},
    {"code": "EXPECTED_TRANSPORT_DISRUPTION_HOURS", "name": "Verkehrsunterbrechungen",
     "outcome_unit": "Stunden/Jahr", "group": "flood", "cost_dimension": "operational",
     "hazards": ["HEAVY_RAIN_FLOOD", "HEAT_WAVE", "EXTRATROPICAL_STORM"],
     "exposures": ["TRANSPORT_HUBS"],
     "vulnerabilities": ["MATERIAL_HEAT_SENSITIVITY", "CRITICAL_INFRA_CONDITION"],
     # BBK/Betreiber-Kennzahlen (Verkehr); ohne Rohdaten als Modellannahme markiert.
     "ref_value": 60.0, "scale": "flat", "source": "BBK KRITIS (Modellannahme)", "description": "Erwartete Verkehrsunterbrechungen.", "priority": 2},
    {"code": "EXPECTED_SUPPLY_CHAIN_DISRUPTION_HOURS", "name": "Lieferkettenunterbrechungen",
     "outcome_unit": "Stunden/Jahr", "group": "compound", "cost_dimension": "operational",
     "hazards": ["HEAVY_RAIN_FLOOD", "DROUGHT", "CASCADE_EVENT"],
     "exposures": ["SUPPLY_CHAIN_NODES", "INDUSTRIAL_COMMERCIAL_AREAS"],
     "vulnerabilities": ["SUPPLY_CHAIN_DEPENDENCY", "SINGLE_SITE_DEPENDENCY"],
     # BBK/Betreiber-Kennzahlen (Lieferketten); ohne Rohdaten als Modellannahme markiert.
     "ref_value": 50.0, "scale": "flat", "source": "BBK KRITIS (Modellannahme)", "description": "Erwartete Unterbrechungen von Lieferketten.", "priority": 2},
    {"code": "EXPECTED_ADMIN_OUTAGE_HOURS", "name": "Administrative Ausfallzeiten",
     "outcome_unit": "Stunden/Jahr", "group": "compound", "cost_dimension": "operational",
     "hazards": ["CASCADE_EVENT", "HEAVY_RAIN_FLOOD"],
     "exposures": ["POPULATION_DENSITY"],
     "vulnerabilities": ["EMERGENCY_MANAGEMENT", "PLANNING_IMPLEMENTATION_CAPACITY"],
     # BBK/Betreiber-Kennzahlen (Verwaltung); ohne Rohdaten als Modellannahme markiert.
     "ref_value": 15.0, "scale": "flat", "source": "BBK KRITIS (Modellannahme)", "description": "Erwartete administrative Ausfallzeiten.", "priority": 3},
    {"code": "EXPECTED_FUNCTIONAL_FAILURE_DURATION", "name": "Dauer von Funktionsausfällen",
     "outcome_unit": "Stunden/Jahr", "group": "compound", "cost_dimension": "operational",
     "hazards": ["CASCADE_EVENT", "COMPOUND_EVENT"],
     "exposures": ["ENERGY_INFRASTRUCTURE", "WATER_WASTEWATER_INFRA"],
     "vulnerabilities": ["INFRA_DEPENDENCY_CHAIN", "INFRA_CRITICALITY"],
     # BBK/Betreiber-Kennzahlen (Funktionsausfälle); ohne Rohdaten als Modellannahme markiert.
     "ref_value": 35.0, "scale": "flat", "source": "BBK KRITIS (Modellannahme)", "description": "Erwartete Dauer von Funktionsausfällen.", "priority": 2},
    {"code": "MEDICAL_UNDERSUPPLY_RISK_INDEX", "name": "Risiko medizinischer Unterversorgung",
     "outcome_unit": "Index", "group": "compound", "cost_dimension": "health",
     "hazards": ["HEAT_WAVE", "CASCADE_EVENT", "DROUGHT"],
     "exposures": ["POPULATION_DENSITY", "VULNERABLE_GROUPS_POPULATION"],
     "vulnerabilities": ["HEALTHCARE_ACCESS", "INFRA_DEPENDENCY_CHAIN"],
     # Index-Risiko: Outcome = Index selbst bei ref=100 (bewusst, kein externer Anker).
     "ref_value": 100.0, "scale": "flat", "source": "Modellannahme (Index=Outcome, dokumentiert)", "description": "Risiko medizinischer Unterversorgung.", "priority": 1},
    {"code": "EXPECTED_BIODIVERSITY_LOSS", "name": "Biodiversitätsverlust",
     "outcome_unit": "Arten/Jahr", "group": "gradual", "cost_dimension": "environment",
     "hazards": ["MEAN_TEMPERATURE_RISE", "DROUGHT", "WILDFIRE"],
     "exposures": ["BIODIVERSITY_HOTSPOTS", "FOREST_AREA"],
     "vulnerabilities": ["BIODIVERSITY_RESILIENCE", "WILDFIRE_SUSCEPTIBILITY"],
     # Modellannahme (mangels flächendeckender Monitoring-Rohdaten): ~5 Arten/50 km² bei Index=100, an BfN/UBA-Naturschutz-Größenordnung gehängt; Punktwert, editierbar.
     "ref_value": 5.0, "scale": "area", "source": "BfN / UBA (Modellannahme)", "description": "Erwarteter jährlicher Biodiversitätsverlust.", "priority": 2},
    {"code": "EXPECTED_HABITAT_LOSS", "name": "Habitatverlust",
     "outcome_unit": "ha/Jahr", "group": "gradual", "cost_dimension": "environment",
     "hazards": ["DROUGHT", "WILDFIRE", "SEA_LEVEL_RISE"],
     "exposures": ["BIODIVERSITY_HOTSPOTS", "COASTAL_RIPARIAN_ZONES", "FOREST_AREA"],
     "vulnerabilities": ["BIODIVERSITY_RESILIENCE", "EROSION_SUSCEPTIBILITY"],
     # Modellannahme (mangels flächendeckender Monitoring-Rohdaten): ~8 ha/50 km² bei Index=100, an BfN/UBA-Habitatverlust-Größenordnung gehängt; Punktwert, editierbar.
     "ref_value": 8.0, "scale": "area", "source": "BfN / UBA (Modellannahme)", "description": "Erwarteter jährlicher Habitatverlust.", "priority": 2},
    {"code": "EXPECTED_SOIL_DEGRADATION", "name": "Bodenverschlechterung",
     "outcome_unit": "ha/Jahr", "group": "drought", "cost_dimension": "environment",
     "hazards": ["DROUGHT", "HEAVY_RAIN_FLOOD", "SOIL_SALINIZATION"],
     "exposures": ["EROSION_PRONE_SOILS", "AGRICULTURAL_LAND"],
     "vulnerabilities": ["SOIL_SENSITIVITY", "IRRIGATION_DEPENDENCY"],
     # Modellannahme (mangels flächendeckender Monitoring-Rohdaten): ~12 ha/50 km² bei Index=100, an BfN/UBA-Bodenmonitoring-Größenordnung gehängt; Punktwert, editierbar.
     "ref_value": 12.0, "scale": "area", "source": "BfN / UBA (Modellannahme)", "description": "Erwartete jährliche Bodenverschlechterung.", "priority": 2},
    {"code": "EXPECTED_VEGETATION_DAMAGE", "name": "Vegetationsschäden",
     "outcome_unit": "ha/Jahr", "group": "drought", "cost_dimension": "environment",
     "hazards": ["DROUGHT", "HEAT_WAVE", "WILDFIRE"],
     "exposures": ["FOREST_AREA", "AGRICULTURAL_LAND"],
     "vulnerabilities": ["WILDFIRE_SUSCEPTIBILITY", "WATER_STRESS_INDEX"],
     # Modellannahme (mangels flächendeckender Monitoring-Rohdaten): ~15 ha/50 km² bei Index=100, an BfN/UBA-Vegetationsmonitoring-Größenordnung gehängt; Punktwert, editierbar.
     "ref_value": 15.0, "scale": "area", "source": "BfN / UBA (Modellannahme)", "description": "Erwartete Vegetationsschäden.", "priority": 2},
    {"code": "HYDROLOGICAL_STRESS_RISK_INDEX", "name": "Risiko hydrologischer Belastungen",
     "outcome_unit": "Index", "group": "drought", "cost_dimension": "operational",
     "hazards": ["DROUGHT", "HEAVY_RAIN_FLOOD", "SOIL_MOISTURE_DECLINE"],
     "exposures": ["FLOODPLAINS", "GROUNDWATER_DEPENDENT_ECOSYSTEMS", "WATER_WASTEWATER_INFRA"],
     "vulnerabilities": ["WATER_STRESS_INDEX", "GROUNDWATER_DEPENDENCY"],
     # Index-Risiko: Outcome = Index selbst bei ref=100 (bewusst, kein externer Anker).
     "ref_value": 100.0, "scale": "flat", "source": "Modellannahme (Index=Outcome, dokumentiert)", "description": "Risiko hydrologischer Belastungen.", "priority": 1},
    {"code": "EXPECTED_WATER_AIR_POLLUTION", "name": "Gewässer-/Luftbelastung",
     "outcome_unit": "Index", "group": "drought", "cost_dimension": "environment",
     "hazards": ["HEAT_WAVE", "DROUGHT", "HEAVY_RAIN_FLOOD"],
     "exposures": ["POPULATION_DENSITY", "FLOODPLAINS"],
     "vulnerabilities": ["AIR_QUALITY_RISK", "WATER_STRESS_INDEX"],
     # Index-Risiko: Outcome = Index selbst bei ref=100 (bewusst, kein externer Anker).
     "ref_value": 100.0, "scale": "flat", "source": "Modellannahme (Index=Outcome, dokumentiert)", "description": "Erwartete jährliche Gewässer- oder Luftbelastung.", "priority": 2},
    {"code": "ECOSYSTEM_DEGRADATION_RISK_INDEX", "name": "Risiko Ökosystemdegradation",
     "outcome_unit": "Index", "group": "gradual", "cost_dimension": "environment",
     "hazards": ["MEAN_TEMPERATURE_RISE", "DROUGHT", "COMPOUND_EVENT"],
     "exposures": ["GROUNDWATER_DEPENDENT_ECOSYSTEMS", "FOREST_AREA"],
     "vulnerabilities": ["BIODIVERSITY_RESILIENCE", "SOIL_SENSITIVITY"],
     # Index-Risiko: Outcome = Index selbst bei ref=100 (bewusst, kein externer Anker).
     "ref_value": 100.0, "scale": "flat", "source": "Modellannahme (Index=Outcome, dokumentiert)", "description": "Risiko der Ökosystemdegradation.", "priority": 2},
    {"code": "ECOSYSTEM_FRAGMENTATION_RISK_INDEX", "name": "Risiko Ökosystemfragmentierung",
     "outcome_unit": "Index", "group": "gradual", "cost_dimension": "environment",
     "hazards": ["MEAN_TEMPERATURE_RISE", "WILDFIRE"],
     "exposures": ["FOREST_AREA", "BIODIVERSITY_HOTSPOTS"],
     "vulnerabilities": ["BIODIVERSITY_RESILIENCE", "GREEN_SPACE_SHARE"],
     # Index-Risiko: Outcome = Index selbst bei ref=100 (bewusst, kein externer Anker).
     "ref_value": 100.0, "scale": "flat", "source": "Modellannahme (Index=Outcome, dokumentiert)", "description": "Risiko der Ökosystemfragmentierung.", "priority": 3},
    {"code": "EXPECTED_ECOSYSTEM_SERVICE_LOSS", "name": "Verlust von Ökosystemleistungen",
     "outcome_unit": "€/Jahr", "group": "gradual", "cost_dimension": "monetary",
     "hazards": ["DROUGHT", "HEAVY_RAIN_FLOOD", "SEA_LEVEL_RISE"],
     "exposures": ["FOREST_AREA", "GROUNDWATER_DEPENDENT_ECOSYSTEMS", "FLOODPLAINS"],
     "vulnerabilities": ["BIODIVERSITY_RESILIENCE", "GREEN_SPACE_SHARE"],
     # Herleitung: Verlust an Ökosystemleistungen (Wald-/Gewässerfunktionen) ~5,7 Mrd €/J ÷ 7.152 Flächen-Einheiten (357.600 km²/50) ≈ 0,8 Mio €/50 km² bei Index=100. scale=area an Kommunefläche. Prognos 2023 (Kategorie Umwelt/Forst; Waldsterben 2018/19).
     "ref_value": 800000.0, "scale": "area", "source": "Prognos/GWS/IÖW 2023", "description": "Erwarteter Verlust von Ökosystemleistungen.", "priority": 2},
    {"code": "EXPECTED_INDIRECT_ECONOMIC_LOSS_EUR", "name": "Indirekte wirtschaftliche Verluste",
     "outcome_unit": "€/Jahr", "group": "compound", "cost_dimension": "monetary",
     "hazards": ["CASCADE_EVENT", "COMPOUND_EVENT", "DROUGHT"],
     "exposures": ["INDUSTRIAL_COMMERCIAL_AREAS", "SUPPLY_CHAIN_NODES"],
     "vulnerabilities": ["SUPPLY_CHAIN_DEPENDENCY", "FINANCIAL_ADAPTATION_CAPACITY"],
     # Herleitung: indirekte Folgeschäden (Lieferketten/Produktivität) ~1,0 Mrd €/J ÷ 832 ≈ 1,2 Mio €/100k bei Index=100. Prognos 2023: indirekter Anteil ~18% (Ahr 7,1 von 40,5 Mrd €).
     "ref_value": 1200000.0, "scale": "pop", "source": "Prognos/GWS/IÖW 2023", "description": "Erwartete indirekte wirtschaftliche Verluste.", "priority": 2},
    {"code": "EXPECTED_SUPPLY_SHORTAGE_COSTS_EUR", "name": "Kosten Versorgungsengpässe",
     "outcome_unit": "€/Jahr", "group": "drought", "cost_dimension": "monetary",
     "hazards": ["DROUGHT", "CASCADE_EVENT", "HEAT_WAVE"],
     "exposures": ["SUPPLY_CHAIN_NODES", "AGRICULTURAL_LAND"],
     "vulnerabilities": ["SUPPLY_CHAIN_DEPENDENCY", "WATER_STRESS_INDEX"],
     # Herleitung: Versorgungsengpass-Kosten (Dürre/Kaskaden) ~0,5 Mrd €/J ÷ 832 ≈ 0,6 Mio €/100k bei Index=100 (Prognos 2023, Teilbetrag indirekter wirtschaftlicher Folgen).
     "ref_value": 600000.0, "scale": "pop", "source": "Prognos/GWS/IÖW 2023", "description": "Erwartete Kosten durch Versorgungsengpässe.", "priority": 2},
    {"code": "EXPECTED_CLIMATE_MIGRATION_COSTS_EUR", "name": "Kosten klimabedingter Migration",
     "outcome_unit": "€/Jahr", "group": "compound", "cost_dimension": "monetary",
     "hazards": ["DROUGHT", "SEA_LEVEL_RISE", "HEAVY_RAIN_FLOOD"],
     "exposures": ["POPULATION_DENSITY", "COASTAL_STORM_SURGE_EXPOSURE"],
     "vulnerabilities": ["INCOME_SOCIAL_RESILIENCE", "FINANCIAL_ADAPTATION_CAPACITY"],
     # Herleitung: Kosten klimabedingter Verdrängung/Migration ~0,33 Mrd €/J ÷ 832 ≈ 0,4 Mio €/100k bei Index=100 (Prognos 2023, kleiner Teilbetrag; national gering, editierbar).
     "ref_value": 400000.0, "scale": "pop", "source": "Prognos/GWS/IÖW 2023", "description": "Erwartete Kosten klimabedingter Migration / Verdrängung.", "priority": 3},
    {"code": "EXPECTED_LOCATION_DISADVANTAGE_EUR", "name": "Wirtschaftliche Standortnachteile",
     "outcome_unit": "€/Jahr", "group": "compound", "cost_dimension": "monetary",
     "hazards": ["HEAT_WAVE", "DROUGHT", "HEAVY_RAIN_FLOOD"],
     "exposures": ["INDUSTRIAL_COMMERCIAL_AREAS", "LOCATION_HAZARD_ZONES"],
     "vulnerabilities": ["SINGLE_SITE_DEPENDENCY", "FINANCIAL_ADAPTATION_CAPACITY"],
     # Herleitung: wirtschaftliche Standortnachteile ~0,42 Mrd €/J ÷ 832 ≈ 0,5 Mio €/100k bei Index=100 (Prognos 2023, Teilbetrag indirekter Standort-/Wettbewerbsfolgen).
     "ref_value": 500000.0, "scale": "pop", "source": "Prognos/GWS/IÖW 2023", "description": "Erwartete wirtschaftliche Standortnachteile.", "priority": 3},
    {"code": "EXPECTED_DELAYED_DAMAGE_COSTS_EUR", "name": "Verzögerte Schadenswirkungen",
     "outcome_unit": "€/Jahr", "group": "compound", "cost_dimension": "monetary",
     "hazards": ["COMPOUND_EVENT", "CASCADE_EVENT"],
     "exposures": ["BUILDING_STOCK", "ENERGY_INFRASTRUCTURE"],
     "vulnerabilities": ["PLANNING_IMPLEMENTATION_CAPACITY", "FINANCIAL_ADAPTATION_CAPACITY"],
     # Herleitung: verzögerte Schadenswirkungen ~0,29 Mrd €/J ÷ 832 ≈ 0,35 Mio €/100k bei Index=100 (Prognos 2023, spät auftretender Teilbetrag der Sektorschäden).
     "ref_value": 350000.0, "scale": "pop", "source": "Prognos/GWS/IÖW 2023", "description": "Erwartete verzögerte Schadenswirkungen.", "priority": 3},
    {"code": "SYSTEMIC_DOMINO_RISK_INDEX", "name": "Risiko systemischer Dominoeffekte",
     "outcome_unit": "Index", "group": "compound", "cost_dimension": "operational",
     "hazards": ["CASCADE_EVENT", "COMPOUND_EVENT"],
     "exposures": ["ENERGY_INFRASTRUCTURE", "WATER_WASTEWATER_INFRA"],
     "vulnerabilities": ["INFRA_DEPENDENCY_CHAIN", "REDUNDANCY_BACKUP"],
     # Index-Risiko: Outcome = Index selbst bei ref=100 (bewusst, kein externer Anker).
     "ref_value": 100.0, "scale": "flat", "source": "Modellannahme (Index=Outcome, dokumentiert)", "description": "Risiko systemischer Dominoeffekte.", "priority": 1},
    {"code": "RESOURCE_CONFLICT_RISK_INDEX", "name": "Risiko von Ressourcenkonflikten",
     "outcome_unit": "Index", "group": "drought", "cost_dimension": "environment",
     "hazards": ["DROUGHT", "SOIL_MOISTURE_DECLINE"],
     "exposures": ["POPULATION_DENSITY", "AGRICULTURAL_LAND"],
     "vulnerabilities": ["WATER_STRESS_INDEX", "INCOME_SOCIAL_RESILIENCE"],
     # Index-Risiko: Outcome = Index selbst bei ref=100 (bewusst, kein externer Anker).
     "ref_value": 100.0, "scale": "flat", "source": "Modellannahme (Index=Outcome, dokumentiert)", "description": "Risiko von Ressourcenkonflikten.", "priority": 3},
    {"code": "SOCIAL_INEQUALITY_AMPLIFICATION_RISK_INDEX", "name": "Verstärkung sozialer Ungleichheiten",
     "outcome_unit": "Index", "group": "compound", "cost_dimension": "health",
     "hazards": ["HEAT_WAVE", "DROUGHT", "COMPOUND_EVENT"],
     "exposures": ["VULNERABLE_GROUPS_POPULATION", "POPULATION_DENSITY"],
     "vulnerabilities": ["VULNERABLE_GROUPS_SHARE", "INCOME_SOCIAL_RESILIENCE"],
     # Index-Risiko: Outcome = Index selbst bei ref=100 (bewusst, kein externer Anker).
     "ref_value": 100.0, "scale": "flat", "source": "Modellannahme (Index=Outcome, dokumentiert)", "description": "Risiko der Verstärkung sozialer Ungleichheiten.", "priority": 2},
    {"code": "ENVIRONMENTAL_FEEDBACK_RISK_INDEX", "name": "Risiko umweltbezogener Rückkopplungen",
     "outcome_unit": "Index", "group": "gradual", "cost_dimension": "environment",
     "hazards": ["COMPOUND_EVENT", "WILDFIRE", "DROUGHT"],
     "exposures": ["FOREST_AREA", "BIODIVERSITY_HOTSPOTS"],
     "vulnerabilities": ["BIODIVERSITY_RESILIENCE", "WILDFIRE_SUSCEPTIBILITY"],
     # Index-Risiko: Outcome = Index selbst bei ref=100 (bewusst, kein externer Anker).
     "ref_value": 100.0, "scale": "flat", "source": "Modellannahme (Index=Outcome, dokumentiert)", "description": "Risiko umweltbezogener Rückkopplungseffekte.", "priority": 3},
    {"code": "EXPECTED_FISHERIES_ECONOMIC_LOSS_EUR", "name": "Wirtschaftliche Verluste Fischerei",
     "outcome_unit": "€/Jahr", "group": "drought", "cost_dimension": "monetary",
     "hazards": ["SURFACE_WATER_HEATING", "LOW_FLOW_NIEDRIGWASSER", "DROUGHT", "HEAT_WAVE"],
     "exposures": ["FISHERIES_AQUACULTURE_AREAS"],
     "vulnerabilities": ["FISHERIES_TEMPERATURE_SENSITIVITY", "FISHERIES_MANAGEMENT_CAPACITY"],
     # Modellannahme (Punktwert, editierbar): Fischerei ist national klein; grober Anker ~0,3 Mio €/50 km² Gewässerfläche bei Index=100, an Gewässer-/Fischereianteil skaliert. Keine belastbare Prognos-Einzelposition ⇒ als Annahme gekennzeichnet.
     "ref_value": 300000.0, "scale": "area", "source": "Prognos/GWS/IÖW 2023", "description": "Erwartete jährliche wirtschaftliche Verluste in der Fischerei.", "priority": 2},
    {"code": "EXPECTED_AQUACULTURE_DAMAGE_EUR", "name": "Schäden in der Aquakultur",
     "outcome_unit": "€/Jahr", "group": "drought", "cost_dimension": "monetary",
     "hazards": ["SURFACE_WATER_HEATING", "LOW_FLOW_NIEDRIGWASSER", "HEAVY_RAIN_FLOOD"],
     "exposures": ["FISHERIES_AQUACULTURE_AREAS"],
     "vulnerabilities": ["AQUACULTURE_TECHNICAL_VULNERABILITY", "WATER_STRESS_INDEX"],
     # Modellannahme (Punktwert, editierbar): Aquakultur national sehr klein; grober Anker ~0,2 Mio €/50 km² Gewässerfläche bei Index=100. Keine belastbare Prognos-Einzelposition ⇒ als Annahme gekennzeichnet.
     "ref_value": 200000.0, "scale": "area", "source": "Prognos/GWS/IÖW 2023", "description": "Erwartete jährliche Schäden in der Aquakultur.", "priority": 2},
    {"code": "FISHERIES_STOCK_STRESS_RISK_INDEX", "name": "Risiko fischereilicher Bestandsbelastung",
     "outcome_unit": "Index", "group": "drought", "cost_dimension": "environment",
     "hazards": ["SURFACE_WATER_HEATING", "LOW_FLOW_NIEDRIGWASSER", "OCEAN_WARMING"],
     "exposures": ["FISH_SPAWNING_HABITATS", "FISHERIES_AQUACULTURE_AREAS"],
     "vulnerabilities": ["FISHERIES_TEMPERATURE_SENSITIVITY", "BIODIVERSITY_RESILIENCE"],
     # Index-Risiko: Outcome = Index selbst bei ref=100 (bewusst, kein externer Anker).
     "ref_value": 100.0, "scale": "flat", "source": "Modellannahme (Index=Outcome, dokumentiert)", "description": "Risiko fischereilicher Bestandsbelastung.", "priority": 2},
    {"code": "LOW_WATER_FISHERIES_IMPACT_INDEX", "name": "Fischereiliche Folgen von Niedrigwasser",
     "outcome_unit": "Index", "group": "drought", "cost_dimension": "environment",
     "hazards": ["LOW_FLOW_NIEDRIGWASSER", "DROUGHT"],
     "exposures": ["FISH_SPAWNING_HABITATS", "FISHERIES_AQUACULTURE_AREAS"],
     "vulnerabilities": ["FISHERIES_TEMPERATURE_SENSITIVITY", "GROUNDWATER_DEPENDENCY"],
     # Index-Risiko: Outcome = Index selbst bei ref=100 (bewusst, kein externer Anker).
     "ref_value": 100.0, "scale": "flat", "source": "Modellannahme (Index=Outcome, dokumentiert)", "description": "Risiko fischereilicher Folgen von Niedrigwasser.", "priority": 2},
]


# ── Pathway-Gewichte (aus pathway_weight_defaults.csv) ──────────────────────────
# Gewichte sind eine transparente Modellwahl (Rangfolge primär > parallel > alternativ >
# compound), keine externe Quelle; degressiv gestaffelt nach Pfadtyp-Nähe zum Primärpfad.
# Quelle: Modellwahl (Pfadgewichtung, dokumentiert) — siehe REVIEW_WIRKUNGSMECHANISMEN.md §5.

PATHWAY_WEIGHT_SOURCE = "Modellwahl (Pfadgewichtung, dokumentiert)"

PATHWAY_WEIGHTS: dict[str, float] = {
    "primary": 1.0,
    "aligned": 0.85,
    "alternate_hazard": 0.75,
    "alternate_exposure": 0.70,
    "alternate_vulnerability": 0.70,
    "compound_he": 0.65,
    "compound_hv": 0.60,
    "compound_ev": 0.55,
    "compound_multi": 0.50,
}


def build_pathways(risk: dict) -> list[dict]:
    """Reproduziert die Wirkungsketten aus risk_composition.csv deterministisch.

    Aus den (geordneten) H/E/V-Listen eines Risikos werden erzeugt:
    - primary:                 H0 × E0 × V0
    - aligned:                 Hi × Ei × Vi (gezippte weitere Indizes)
    - alternate_hazard:        Hi × E0 × V0
    - alternate_exposure:      H0 × Ei × V0
    - alternate_vulnerability: H0 × E0 × Vi
    - compound_he/hv/ev:       H1×E1×V0 / H1×E0×V1 / H0×E1×V1 (falls vorhanden)
    Gibt Liste von {hazard, exposure, vulnerability, pathway_type, weight} zurück.
    """
    H = risk["hazards"]
    E = risk["exposures"]
    V = risk["vulnerabilities"]
    if not H or not E or not V:
        return []

    pw = PATHWAY_WEIGHTS
    paths: list[dict] = []

    def add(h, e, v, ptype):
        paths.append({"hazard": h, "exposure": e, "vulnerability": v,
                      "pathway_type": ptype, "weight": pw[ptype]})

    add(H[0], E[0], V[0], "primary")

    # aligned: zip the further indices
    for i in range(1, min(len(H), len(E), len(V))):
        add(H[i], E[i], V[i], "aligned")

    for h in H[1:]:
        add(h, E[0], V[0], "alternate_hazard")
    for e in E[1:]:
        add(H[0], e, V[0], "alternate_exposure")
    for v in V[1:]:
        add(H[0], E[0], v, "alternate_vulnerability")

    if len(H) > 1 and len(E) > 1:
        add(H[1], E[1], V[0], "compound_he")
    if len(H) > 1 and len(V) > 1:
        add(H[1], E[0], V[1], "compound_hv")
    if len(E) > 1 and len(V) > 1:
        add(H[0], E[1], V[1], "compound_ev")

    return paths


# ── Maßnahmen ────────────────────────────────────────────────────────────────────
# effect_target: Liste aus {hazard, exposure, vulnerability} – worauf die Maßnahme wirkt.
# default_reduction: Reduktion der normalisierten Zielkomponente bei VOLLER Abdeckung
#   der Zelle (0..1). coverage_scaling: 'linear' oder 'saturating'.
# linked_risk_codes: Risiken, die neu berechnet werden.
# cost_per_m2 / maintenance_per_m2_year / benefit_per_m2_year in € (Polygonfläche),
#   alternativ cost_per_unit + Default-Anzahl. Quelle: KAP3-Vorschlag + Plausibilität
#   (siehe Handbuch; Recherche-Prompt für empirische Kalibrierung liegt vor).
# default_reduction: unbelegte Modellannahme je Maßnahme (keine externe Kalibrierstudie
#   vorhanden); Kommune kann Wert über PUT /kommune/{id}/parameters mit eigener Quelle
#   überschreiben (source-Fallback: "Modellannahme (Maßnahmenwirkung, unbelegt)").

MEASURES: list[dict] = [
    {"code": "GRID_REINFORCEMENT_REDUNDANCY", "name": "Netzverstärkung / Redundanzen",
     "description": "Erhöht Redundanz im Energienetz.", "measure_type": "structural",
     "effect_target": ["vulnerability"], "default_reduction": 0.30, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_ENERGY_OUTAGE_HOURS", "EXPECTED_CI_OUTAGE_HOURS"],
     "cost_per_m2": 0.0, "cost_per_unit": 250000.0, "maintenance_per_m2_year": 0.0, "benefit_per_m2_year": 0.0},
    {"code": "HEAT_RESISTANT_PLANT_COOLING", "name": "Hitzefeste Anlagen / Kühlung",
     "description": "Technische Anpassung energiebezogener Anlagen an Hitze.", "measure_type": "structural",
     "effect_target": ["hazard"], "default_reduction": 0.20, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_ENERGY_INFRA_DAMAGE_EUR"],
     "cost_per_m2": 0.0, "cost_per_unit": 120000.0, "maintenance_per_m2_year": 0.0, "benefit_per_m2_year": 0.0},
    {"code": "DECENTRALIZED_ENERGY_PV_STORAGE", "name": "Dezentrale Energie (PV, Speicher)",
     "description": "Dezentrale Erzeugung und Speicher.", "measure_type": "structural",
     "effect_target": ["vulnerability"], "default_reduction": 0.25, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_ENERGY_OUTAGE_HOURS", "SYSTEMIC_DOMINO_RISK_INDEX"],
     "cost_per_m2": 150.0, "cost_per_unit": 0.0, "maintenance_per_m2_year": 2.0, "benefit_per_m2_year": 8.0},
    {"code": "GREEN_ROOFS_FACADES", "name": "Begrünte Dächer/Fassaden",
     "description": "Begrünung von Dächern und Fassaden.", "measure_type": "structural",
     "effect_target": ["hazard", "exposure"], "default_reduction": 0.18, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_THERMAL_STRESS_HOURS", "EXPECTED_BUILDING_DAMAGE_EUR"],
     "cost_per_m2": 55.0, "cost_per_unit": 0.0, "maintenance_per_m2_year": 4.0, "benefit_per_m2_year": 6.0},
    {"code": "FLOOD_PROTECTION_BUILDING", "name": "Hochwasserschutz (Gebäude)",
     "description": "Gebäudespezifischer Hochwasserschutz.", "measure_type": "structural",
     "effect_target": ["vulnerability"], "default_reduction": 0.35, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_BUILDING_DAMAGE_EUR"],
     "cost_per_m2": 40.0, "cost_per_unit": 0.0, "maintenance_per_m2_year": 1.0, "benefit_per_m2_year": 9.0},
    {"code": "DESEALING_SURFACE", "name": "Entsiegelung",
     "description": "Rückbau versiegelter Flächen.", "measure_type": "planning",
     "effect_target": ["hazard", "vulnerability"], "default_reduction": 0.30, "coverage_scaling": "linear",
     "linked_risk_codes": ["HYDROLOGICAL_STRESS_RISK_INDEX", "EXPECTED_BUILDING_DAMAGE_EUR"],
     "cost_per_m2": 35.0, "cost_per_unit": 0.0, "maintenance_per_m2_year": 0.5, "benefit_per_m2_year": 5.0},
    {"code": "COOL_ROOFS", "name": "Helle Dächer",
     "description": "Hochreflektive Dachflächen.", "measure_type": "structural",
     "effect_target": ["hazard"], "default_reduction": 0.15, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_THERMAL_STRESS_HOURS"],
     "cost_per_m2": 20.0, "cost_per_unit": 0.0, "maintenance_per_m2_year": 1.0, "benefit_per_m2_year": 3.0},
    {"code": "HEAT_RESILIENT_PAVEMENT", "name": "Hitzeresiliente Beläge",
     "description": "Beläge mit höherer Hitzebeständigkeit.", "measure_type": "structural",
     "effect_target": ["vulnerability"], "default_reduction": 0.20, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_TRANSPORT_DAMAGE_EUR"],
     "cost_per_m2": 30.0, "cost_per_unit": 0.0, "maintenance_per_m2_year": 1.0, "benefit_per_m2_year": 3.0},
    {"code": "DRAINAGE_SWALES", "name": "Entwässerung (Mulden/Rigolen)",
     "description": "Oberflächenentwässerung und Rigolen.", "measure_type": "structural",
     "effect_target": ["hazard"], "default_reduction": 0.25, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_TRANSPORT_DISRUPTION_HOURS", "HYDROLOGICAL_STRESS_RISK_INDEX"],
     "cost_per_m2": 45.0, "cost_per_unit": 0.0, "maintenance_per_m2_year": 2.0, "benefit_per_m2_year": 4.0},
    {"code": "CRITICAL_NODE_PROTECTION", "name": "Schutz kritischer Knoten",
     "description": "Schutzmaßnahmen für Verkehrsknoten.", "measure_type": "structural",
     "effect_target": ["exposure"], "default_reduction": 0.25, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_TRANSPORT_DISRUPTION_HOURS"],
     "cost_per_m2": 0.0, "cost_per_unit": 80000.0, "maintenance_per_m2_year": 0.0, "benefit_per_m2_year": 0.0},
    {"code": "HABITAT_CONNECTIVITY", "name": "Biotopverbund",
     "description": "Vernetzung von Lebensräumen.", "measure_type": "planning",
     "effect_target": ["vulnerability"], "default_reduction": 0.20, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_BIODIVERSITY_LOSS", "ECOSYSTEM_FRAGMENTATION_RISK_INDEX"],
     "cost_per_m2": 8.0, "cost_per_unit": 0.0, "maintenance_per_m2_year": 0.5, "benefit_per_m2_year": 1.5},
    {"code": "FLOODPLAIN_RENATURATION", "name": "Auenrenaturierung",
     "description": "Renaturierung von Auen und Flussauen.", "measure_type": "planning",
     "effect_target": ["hazard"], "default_reduction": 0.30, "coverage_scaling": "linear",
     "linked_risk_codes": ["HYDROLOGICAL_STRESS_RISK_INDEX", "EXPECTED_HABITAT_LOSS"],
     "cost_per_m2": 12.0, "cost_per_unit": 0.0, "maintenance_per_m2_year": 0.5, "benefit_per_m2_year": 3.0},
    {"code": "EROSION_PROTECTION", "name": "Erosionsschutz (Hecken, Terrassen)",
     "description": "Baulicher und vegetativer Erosionsschutz.", "measure_type": "structural",
     "effect_target": ["hazard"], "default_reduction": 0.25, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_SOIL_DEGRADATION"],
     "cost_per_m2": 10.0, "cost_per_unit": 0.0, "maintenance_per_m2_year": 0.5, "benefit_per_m2_year": 2.0},
    {"code": "HUMUS_BUILDUP", "name": "Humusaufbau",
     "description": "Aufbau organischen Bodenanteils.", "measure_type": "behavioral",
     "effect_target": ["vulnerability"], "default_reduction": 0.15, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_AGRICULTURAL_DAMAGE_EUR", "EXPECTED_SOIL_DEGRADATION"],
     "cost_per_m2": 2.0, "cost_per_unit": 0.0, "maintenance_per_m2_year": 0.3, "benefit_per_m2_year": 1.5},
    {"code": "DROUGHT_RESISTANT_VARIETIES", "name": "Trockenresistente Sorten",
     "description": "Anbau klimaresilienter Kulturen.", "measure_type": "behavioral",
     "effect_target": ["vulnerability"], "default_reduction": 0.18, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_AGRICULTURAL_DAMAGE_EUR"],
     "cost_per_m2": 1.0, "cost_per_unit": 0.0, "maintenance_per_m2_year": 0.2, "benefit_per_m2_year": 1.5},
    {"code": "WATER_STORAGE_EFFICIENT_IRRIGATION", "name": "Wasserspeicher / effiziente Bewässerung",
     "description": "Speicherung und effiziente Bewässerung.", "measure_type": "structural",
     "effect_target": ["exposure"], "default_reduction": 0.22, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_AGRICULTURAL_DAMAGE_EUR"],
     "cost_per_m2": 5.0, "cost_per_unit": 0.0, "maintenance_per_m2_year": 0.5, "benefit_per_m2_year": 2.0},
    {"code": "MIXED_FORESTS", "name": "Mischwälder",
     "description": "Waldumbau zu Mischbeständen.", "measure_type": "planning",
     "effect_target": ["vulnerability"], "default_reduction": 0.25, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_VEGETATION_DAMAGE"],
     "cost_per_m2": 4.0, "cost_per_unit": 0.0, "maintenance_per_m2_year": 0.3, "benefit_per_m2_year": 1.5},
    {"code": "WILDFIRE_PREVENTION", "name": "Brandprävention",
     "description": "Präventive Waldbrandmaßnahmen.", "measure_type": "organizational",
     "effect_target": ["hazard"], "default_reduction": 0.25, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_VEGETATION_DAMAGE"],
     "cost_per_m2": 1.0, "cost_per_unit": 0.0, "maintenance_per_m2_year": 0.3, "benefit_per_m2_year": 1.0},
    {"code": "HEAT_ACTION_PLANS", "name": "Hitzeaktionspläne",
     "description": "Kommunale Hitzeaktionspläne.", "measure_type": "organizational",
     "effect_target": ["vulnerability"], "default_reduction": 0.20, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_ANNUAL_MORTALITY", "EXPECTED_ANNUAL_MORBIDITY"],
     "cost_per_m2": 0.0, "cost_per_unit": 50000.0, "maintenance_per_m2_year": 0.0, "benefit_per_m2_year": 0.0},
    {"code": "COOLING_ROOMS_DRINKING_WATER", "name": "Kühlräume / Trinkwasserpunkte",
     "description": "Öffentliche Kühl- und Trinkwasserinfrastruktur.", "measure_type": "structural",
     "effect_target": ["exposure"], "default_reduction": 0.18, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_THERMAL_STRESS_HOURS", "EXPECTED_ANNUAL_MORTALITY"],
     "cost_per_m2": 0.0, "cost_per_unit": 8000.0, "maintenance_per_m2_year": 0.0, "benefit_per_m2_year": 0.0},
    {"code": "EARLY_WARNING_MEASURE", "name": "Frühwarnsysteme (Maßnahme)",
     "description": "Ausbau von Frühwarnsystemen.", "measure_type": "organizational",
     "effect_target": ["vulnerability"], "default_reduction": 0.25, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_ANNUAL_AFFECTED_EVACUATED", "EXPECTED_ANNUAL_INJURIES"],
     "cost_per_m2": 0.0, "cost_per_unit": 60000.0, "maintenance_per_m2_year": 0.0, "benefit_per_m2_year": 0.0},
    {"code": "URBAN_GREEN", "name": "Stadtgrün",
     "description": "Ausbau städtischer Grünflächen.", "measure_type": "planning",
     "effect_target": ["hazard"], "default_reduction": 0.25, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_THERMAL_STRESS_HOURS"],
     "cost_per_m2": 25.0, "cost_per_unit": 0.0, "maintenance_per_m2_year": 3.0, "benefit_per_m2_year": 5.0},
    {"code": "EVACUATION_EMERGENCY_PLANS", "name": "Evakuierungs- & Notfallpläne",
     "description": "Bevölkerungsschutzpläne.", "measure_type": "organizational",
     "effect_target": ["vulnerability"], "default_reduction": 0.22, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_ANNUAL_AFFECTED_EVACUATED"],
     "cost_per_m2": 0.0, "cost_per_unit": 40000.0, "maintenance_per_m2_year": 0.0, "benefit_per_m2_year": 0.0},
    {"code": "BUILDING_BANS_RISK_ZONES", "name": "Bauverbote in Risikozonen",
     "description": "Siedlungsrückhaltung in Gefahrenzonen.", "measure_type": "planning",
     "effect_target": ["exposure"], "default_reduction": 0.30, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_BUILDING_DAMAGE_EUR", "EXPECTED_ANNUAL_AFFECTED_EVACUATED"],
     "cost_per_m2": 0.0, "cost_per_unit": 0.0, "maintenance_per_m2_year": 0.0, "benefit_per_m2_year": 0.0},
    {"code": "FRESH_AIR_CORRIDORS", "name": "Frischluftschneisen",
     "description": "Freihaltung von Frischluftkorridoren.", "measure_type": "planning",
     "effect_target": ["hazard"], "default_reduction": 0.20, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_THERMAL_STRESS_HOURS"],
     "cost_per_m2": 2.0, "cost_per_unit": 0.0, "maintenance_per_m2_year": 0.5, "benefit_per_m2_year": 2.0},
    {"code": "SPONGE_CITY", "name": "Entsiegelung / Schwammstadt",
     "description": "Schwammstadt-Konzepte.", "measure_type": "planning",
     "effect_target": ["hazard"], "default_reduction": 0.30, "coverage_scaling": "linear",
     "linked_risk_codes": ["HYDROLOGICAL_STRESS_RISK_INDEX", "EXPECTED_BUILDING_DAMAGE_EUR"],
     "cost_per_m2": 40.0, "cost_per_unit": 0.0, "maintenance_per_m2_year": 2.0, "benefit_per_m2_year": 5.0},
    {"code": "RETENTION_STORAGE", "name": "Retentionsflächen / Speicher",
     "description": "Oberirdische Retention und Speicher.", "measure_type": "structural",
     "effect_target": ["hazard"], "default_reduction": 0.28, "coverage_scaling": "linear",
     "linked_risk_codes": ["HYDROLOGICAL_STRESS_RISK_INDEX"],
     "cost_per_m2": 30.0, "cost_per_unit": 0.0, "maintenance_per_m2_year": 1.0, "benefit_per_m2_year": 4.0},
    {"code": "RETENTION_POLDER_RESERVOIR", "name": "Retention / Polder / Rückhaltebecken",
     "description": "Großflächige Hochwasserretention.", "measure_type": "structural",
     "effect_target": ["hazard"], "default_reduction": 0.30, "coverage_scaling": "linear",
     "linked_risk_codes": ["HYDROLOGICAL_STRESS_RISK_INDEX", "EXPECTED_BUILDING_DAMAGE_EUR"],
     "cost_per_m2": 25.0, "cost_per_unit": 0.0, "maintenance_per_m2_year": 1.0, "benefit_per_m2_year": 4.0},
    {"code": "INFILTRATION_AREAS", "name": "Versickerungsflächen",
     "description": "Flächenversickerung.", "measure_type": "structural",
     "effect_target": ["exposure"], "default_reduction": 0.25, "coverage_scaling": "linear",
     "linked_risk_codes": ["HYDROLOGICAL_STRESS_RISK_INDEX"],
     "cost_per_m2": 30.0, "cost_per_unit": 0.0, "maintenance_per_m2_year": 1.0, "benefit_per_m2_year": 3.0},
    {"code": "RUNOFF_ROUTING_DGM", "name": "Abflusslenkung (DGM-basiert)",
     "description": "Geländebasierte Abflusslenkung.", "measure_type": "planning",
     "effect_target": ["hazard"], "default_reduction": 0.20, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_BUILDING_DAMAGE_EUR"],
     "cost_per_m2": 8.0, "cost_per_unit": 0.0, "maintenance_per_m2_year": 0.5, "benefit_per_m2_year": 2.0},
    {"code": "GROUNDWATER_RECHARGE", "name": "Grundwasseranreicherung",
     "description": "Künstliche Grundwasseranreicherung.", "measure_type": "structural",
     "effect_target": ["hazard"], "default_reduction": 0.20, "coverage_scaling": "linear",
     "linked_risk_codes": ["HYDROLOGICAL_STRESS_RISK_INDEX", "EXPECTED_WATER_SUPPLY_OUTAGE_HOURS"],
     "cost_per_m2": 10.0, "cost_per_unit": 0.0, "maintenance_per_m2_year": 0.5, "benefit_per_m2_year": 2.0},
    {"code": "LEAKAGE_REDUCTION", "name": "Leckage-Reduktion",
     "description": "Reduktion von Wasserverlusten im Netz.", "measure_type": "structural",
     "effect_target": ["vulnerability"], "default_reduction": 0.22, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_WATER_SUPPLY_OUTAGE_HOURS"],
     "cost_per_m2": 0.0, "cost_per_unit": 90000.0, "maintenance_per_m2_year": 0.0, "benefit_per_m2_year": 0.0},
    {"code": "LEVEE_REINFORCEMENT", "name": "Deichverstärkung / Barrieren",
     "description": "Küstenschutz und Deichbau.", "measure_type": "structural",
     "effect_target": ["hazard"], "default_reduction": 0.35, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_BUILDING_DAMAGE_EUR"],
     "cost_per_m2": 0.0, "cost_per_unit": 300000.0, "maintenance_per_m2_year": 0.0, "benefit_per_m2_year": 0.0},
    {"code": "SALTWATER_BARRIERS", "name": "Salzwasserbarrieren",
     "description": "Barrieren gegen Salzwasserintrusion.", "measure_type": "structural",
     "effect_target": ["exposure"], "default_reduction": 0.25, "coverage_scaling": "saturating",
     "linked_risk_codes": ["HYDROLOGICAL_STRESS_RISK_INDEX"],
     "cost_per_m2": 0.0, "cost_per_unit": 150000.0, "maintenance_per_m2_year": 0.0, "benefit_per_m2_year": 0.0},
    {"code": "RISK_BASED_INVESTMENTS", "name": "Risikobasierte Investitionen",
     "description": "Finanzielle Steuerung nach Risiko.", "measure_type": "organizational",
     "effect_target": ["vulnerability"], "default_reduction": 0.15, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_TOTAL_DAMAGE_EAD_EUR"],
     "cost_per_m2": 0.0, "cost_per_unit": 30000.0, "maintenance_per_m2_year": 0.0, "benefit_per_m2_year": 0.0},
    {"code": "PREVENTION_INCENTIVES", "name": "Präventionsanreize",
     "description": "Anreize für präventive Maßnahmen.", "measure_type": "organizational",
     "effect_target": ["exposure"], "default_reduction": 0.12, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_TOTAL_DAMAGE_EAD_EUR"],
     "cost_per_m2": 0.0, "cost_per_unit": 25000.0, "maintenance_per_m2_year": 0.0, "benefit_per_m2_year": 0.0},
    {"code": "INDUSTRIAL_COOLING_CONCEPTS", "name": "Kühlkonzepte (Industrie/Gewerbe)",
     "description": "Betriebliche Kühlkonzepte.", "measure_type": "structural",
     "effect_target": ["hazard"], "default_reduction": 0.18, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_INDIRECT_ECONOMIC_LOSS_EUR"],
     "cost_per_m2": 0.0, "cost_per_unit": 70000.0, "maintenance_per_m2_year": 0.0, "benefit_per_m2_year": 0.0},
    {"code": "SUPPLY_CHAIN_RESILIENCE", "name": "Lieferketten-Resilienz",
     "description": "Resilienz in Lieferketten.", "measure_type": "organizational",
     "effect_target": ["vulnerability"], "default_reduction": 0.20, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_SUPPLY_CHAIN_DISRUPTION_HOURS"],
     "cost_per_m2": 0.0, "cost_per_unit": 40000.0, "maintenance_per_m2_year": 0.0, "benefit_per_m2_year": 0.0},
    {"code": "VULNERABLE_GROUP_PROGRAMS", "name": "Schutzprogramme vulnerable Gruppen",
     "description": "Gezielte Programme für vulnerable Gruppen.", "measure_type": "organizational",
     "effect_target": ["vulnerability"], "default_reduction": 0.22, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_ANNUAL_MORTALITY", "SOCIAL_INEQUALITY_AMPLIFICATION_RISK_INDEX"],
     "cost_per_m2": 0.0, "cost_per_unit": 35000.0, "maintenance_per_m2_year": 0.0, "benefit_per_m2_year": 0.0},
    {"code": "HEAT_WORK_SCHEDULES", "name": "Arbeitszeitmodelle bei Hitze",
     "description": "Angepasste Arbeitszeiten bei Hitze.", "measure_type": "behavioral",
     "effect_target": ["exposure"], "default_reduction": 0.18, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_THERMAL_STRESS_HOURS"],
     "cost_per_m2": 0.0, "cost_per_unit": 10000.0, "maintenance_per_m2_year": 0.0, "benefit_per_m2_year": 0.0},
    {"code": "PUBLIC_SHADE_WATER", "name": "Schatten / Wasser im öffentlichen Raum",
     "description": "Öffentliche Beschattung und Wasserstellen.", "measure_type": "structural",
     "effect_target": ["hazard"], "default_reduction": 0.18, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_THERMAL_STRESS_HOURS"],
     "cost_per_m2": 35.0, "cost_per_unit": 0.0, "maintenance_per_m2_year": 2.0, "benefit_per_m2_year": 3.0},
    {"code": "ADAPTIVE_FISHERIES_MANAGEMENT", "name": "Adaptive Fischereibewirtschaftung",
     "description": "Anpassung von Fangregeln, Schonzeiten und Monitoring.", "measure_type": "organizational",
     "effect_target": ["vulnerability"], "default_reduction": 0.20, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_FISHERIES_ECONOMIC_LOSS_EUR", "FISHERIES_STOCK_STRESS_RISK_INDEX"],
     "cost_per_m2": 0.0, "cost_per_unit": 20000.0, "maintenance_per_m2_year": 0.0, "benefit_per_m2_year": 0.0},
    {"code": "FISH_PASSAGE_RESTORATION", "name": "Fischaufstieg / Gewässerdurchgängigkeit",
     "description": "Fischpässe und bauliche Durchgängigkeit.", "measure_type": "structural",
     "effect_target": ["exposure"], "default_reduction": 0.22, "coverage_scaling": "saturating",
     "linked_risk_codes": ["FISHERIES_STOCK_STRESS_RISK_INDEX", "LOW_WATER_FISHERIES_IMPACT_INDEX"],
     "cost_per_m2": 0.0, "cost_per_unit": 50000.0, "maintenance_per_m2_year": 0.0, "benefit_per_m2_year": 0.0},
    {"code": "AQUACULTURE_RESILIENCE_SYSTEMS", "name": "Aquakultur-Resilienz",
     "description": "Technische und organisatorische Resilienz von Aquakulturanlagen.", "measure_type": "structural",
     "effect_target": ["vulnerability"], "default_reduction": 0.25, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_AQUACULTURE_DAMAGE_EUR", "FISHERIES_STOCK_STRESS_RISK_INDEX"],
     "cost_per_m2": 0.0, "cost_per_unit": 60000.0, "maintenance_per_m2_year": 0.0, "benefit_per_m2_year": 0.0},
    {"code": "FISHERIES_SPAWNING_HABITAT_RESTORATION", "name": "Laichhabitat-Renaturierung",
     "description": "Renaturierung und Schutz von Laich- und Aufwuchsgebieten.", "measure_type": "planning",
     "effect_target": ["hazard"], "default_reduction": 0.22, "coverage_scaling": "linear",
     "linked_risk_codes": ["FISHERIES_STOCK_STRESS_RISK_INDEX", "LOW_WATER_FISHERIES_IMPACT_INDEX"],
     "cost_per_m2": 10.0, "cost_per_unit": 0.0, "maintenance_per_m2_year": 0.5, "benefit_per_m2_year": 2.0},
    {"code": "FISHERIES_WATER_QUALITY_PROTECTION", "name": "Gewässerschutz für Fischerei",
     "description": "Maßnahmen zur Sicherung der Gewässerqualität.", "measure_type": "organizational",
     "effect_target": ["vulnerability"], "default_reduction": 0.20, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_WATER_AIR_POLLUTION", "FISHERIES_STOCK_STRESS_RISK_INDEX"],
     "cost_per_m2": 0.0, "cost_per_unit": 25000.0, "maintenance_per_m2_year": 0.0, "benefit_per_m2_year": 0.0},
]


# ── Kategorisierung (Karten-Layerspalte: Zwischenebene) ──────────────────────────
# Geordnete Kategorie-Definitionen + Zuordnung je Code. Die Felder werden unten in
# die H/E/V/Maßnahmen-Dicts injiziert, sodass /catalog sie automatisch mitliefert.

HAZARD_CATEGORIES: list[dict] = [
    {"code": "temp", "label": "Hitze & Temperatur"},
    {"code": "drought", "label": "Trockenheit & Wasserarmut"},
    {"code": "flood", "label": "Starkregen & Hochwasser"},
    {"code": "storm", "label": "Sturm & Wind"},
    {"code": "coast", "label": "Küste & Meer"},
    {"code": "soil", "label": "Boden & Kryosphäre"},
    {"code": "fire", "label": "Brände"},
    {"code": "compound", "label": "Verbund & Kaskade"},
]

EXPOSURE_CATEGORIES: list[dict] = [
    {"code": "people", "label": "Bevölkerung & Gesundheit"},
    {"code": "building", "label": "Gebäude & Siedlung"},
    {"code": "infra", "label": "Kritische Infrastruktur"},
    {"code": "economy", "label": "Wirtschaft"},
    {"code": "nature", "label": "Land & Natur"},
    {"code": "water", "label": "Wasser & Küste"},
]

VULNERABILITY_CATEGORIES: list[dict] = [
    {"code": "technical", "label": "Bauliche & technische"},
    {"code": "social", "label": "Soziale & Gesundheit"},
    {"code": "watersoil", "label": "Wasser & Boden"},
    {"code": "nature", "label": "Natur & Ökosysteme"},
    {"code": "economy", "label": "Wirtschaft"},
    {"code": "governance", "label": "Governance & Vorsorge"},
    {"code": "fisheries", "label": "Fischerei"},
]

# KAnG-Cluster mit Handlungsfeldern (Reihenfolge wie im Gesetz)
KANG_CLUSTERS: list[dict] = [
    {"code": "infrastructure", "label": "Infrastruktur", "fields": [
        {"code": "energy", "label": "Energieinfrastruktur"},
        {"code": "buildings", "label": "Gebäude"},
        {"code": "transport", "label": "Verkehr und Verkehrsinfrastruktur"},
    ]},
    {"code": "land", "label": "Land und Landnutzung", "fields": [
        {"code": "biodiversity", "label": "Biologische Vielfalt"},
        {"code": "soil", "label": "Boden"},
        {"code": "agriculture", "label": "Landwirtschaft"},
        {"code": "forestry", "label": "Wald und Forstwirtschaft"},
    ]},
    {"code": "health", "label": "Menschliche Gesundheit und Pflege", "fields": [
        {"code": "health", "label": "Gesundheit und Pflege"},
    ]},
    {"code": "urban", "label": "Stadtentwicklung, Raumplanung & Bevölkerungsschutz", "fields": [
        {"code": "civil_protection", "label": "Bevölkerungs- und Katastrophenschutz"},
        {"code": "spatial_planning", "label": "Raumplanung"},
        {"code": "urban_dev", "label": "Stadt- und Siedlungsentwicklung"},
    ]},
    {"code": "water", "label": "Wasser", "fields": [
        {"code": "fisheries", "label": "Fischerei"},
        {"code": "coastal", "label": "Küsten- und Meeresschutz"},
        {"code": "water_management", "label": "Wasserhaushalt und Wasserwirtschaft"},
    ]},
    {"code": "economy", "label": "Wirtschaft", "fields": [
        {"code": "finance", "label": "Finanzwirtschaft"},
        {"code": "industry", "label": "Industrie und Gewerbe"},
    ]},
    {"code": "crosscutting", "label": "Übergreifende Handlungsfelder", "fields": [
        {"code": "general", "label": "Übergreifend"},
    ]},
]

_HAZARD_CATEGORY_MAP: dict[str, str] = {
    "MEAN_TEMPERATURE_RISE": "temp", "HEAT_WAVE": "temp", "COLD_EXTREME": "temp",
    "SURFACE_WATER_HEATING": "temp", "OCEAN_WARMING": "temp",
    "DROUGHT": "drought", "SOIL_MOISTURE_DECLINE": "drought", "LOW_FLOW_NIEDRIGWASSER": "drought",
    "HEAVY_RAIN_FLOOD": "flood", "LANDSLIDE": "flood",
    "EXTRATROPICAL_STORM": "storm", "TROPICAL_CYCLONE": "storm",
    "SEA_LEVEL_RISE": "coast", "STORM_SURGE": "coast", "COASTAL_EROSION": "coast",
    "SALTWATER_INTRUSION": "coast", "OCEAN_ACIDIFICATION": "coast",
    "SOIL_SALINIZATION": "soil", "GLACIER_SNOW_LOSS": "soil", "PERMAFROST_THAW": "soil",
    "WILDFIRE": "fire",
    "COMPOUND_EVENT": "compound", "CASCADE_EVENT": "compound",
}

_EXPOSURE_CATEGORY_MAP: dict[str, str] = {
    "POPULATION_DENSITY": "people", "AGE_STRUCTURE": "people",
    "OUTDOOR_THERMAL_EXPOSURE": "people", "VULNERABLE_GROUPS_POPULATION": "people",
    "BUILDING_STOCK": "building", "BUILDING_USE_TYPES": "building", "LOCATION_HAZARD_ZONES": "building",
    "ENERGY_INFRASTRUCTURE": "infra", "WATER_WASTEWATER_INFRA": "infra",
    "TRANSPORT_HUBS": "infra", "COMMUNICATION_INFRA": "infra",
    "HEALTHCARE_INFRASTRUCTURE": "people",
    "INDUSTRIAL_COMMERCIAL_AREAS": "economy", "SUPPLY_CHAIN_NODES": "economy",
    "AGRICULTURAL_LAND": "nature", "FOREST_AREA": "nature",
    "BIODIVERSITY_HOTSPOTS": "nature", "EROSION_PRONE_SOILS": "nature",
    "COASTAL_RIPARIAN_ZONES": "water", "FLOODPLAINS": "water",
    "COASTAL_STORM_SURGE_EXPOSURE": "water", "GROUNDWATER_DEPENDENT_ECOSYSTEMS": "water",
    "FISHERIES_AQUACULTURE_AREAS": "water", "FISH_SPAWNING_HABITATS": "water",
}

_VULNERABILITY_CATEGORY_MAP: dict[str, str] = {
    "BUILDING_STABILITY": "technical", "CRITICAL_INFRA_CONDITION": "technical",
    "MATERIAL_HEAT_SENSITIVITY": "technical", "INFRA_CRITICALITY": "technical",
    "REDUNDANCY_BACKUP": "technical", "INFRA_DEPENDENCY_CHAIN": "technical",
    "SEALING_DEGREE": "technical", "UHI_INTENSITY": "technical", "GREEN_SPACE_SHARE": "technical",
    "VULNERABLE_GROUPS_SHARE": "social", "INCOME_SOCIAL_RESILIENCE": "social",
    "HEALTHCARE_ACCESS": "social", "HEAT_SENSITIVITY": "social",
    "AIR_QUALITY_RISK": "social", "DISEASE_VECTOR_SUSCEPTIBILITY": "social",
    "GROUNDWATER_DEPENDENCY": "watersoil", "WATER_STRESS_INDEX": "watersoil",
    "IRRIGATION_DEPENDENCY": "watersoil", "EROSION_SUSCEPTIBILITY": "watersoil",
    "SOIL_SENSITIVITY": "watersoil", "LEVEE_CONDITION": "watersoil",
    "SALTWATER_INTRUSION_RISK": "watersoil",
    "BIODIVERSITY_RESILIENCE": "nature", "WILDFIRE_SUSCEPTIBILITY": "nature",
    "SINGLE_SITE_DEPENDENCY": "economy", "SUPPLY_CHAIN_DEPENDENCY": "economy",
    "FINANCIAL_ADAPTATION_CAPACITY": "economy",
    "EARLY_WARNING_SYSTEMS": "governance", "EMERGENCY_MANAGEMENT": "governance",
    "PLANNING_IMPLEMENTATION_CAPACITY": "governance",
    "FISHERIES_TEMPERATURE_SENSITIVITY": "fisheries",
    "AQUACULTURE_TECHNICAL_VULNERABILITY": "fisheries",
    "FISHERIES_MANAGEMENT_CAPACITY": "fisheries",
}

# Maßnahme → (KAnG-Cluster, Handlungsfeld)
_MEASURE_KANG_MAP: dict[str, tuple[str, str]] = {
    "GRID_REINFORCEMENT_REDUNDANCY": ("infrastructure", "energy"),
    "HEAT_RESISTANT_PLANT_COOLING": ("infrastructure", "energy"),
    "DECENTRALIZED_ENERGY_PV_STORAGE": ("infrastructure", "energy"),
    "GREEN_ROOFS_FACADES": ("infrastructure", "buildings"),
    "FLOOD_PROTECTION_BUILDING": ("infrastructure", "buildings"),
    "COOL_ROOFS": ("infrastructure", "buildings"),
    "HEAT_RESILIENT_PAVEMENT": ("infrastructure", "transport"),
    "CRITICAL_NODE_PROTECTION": ("infrastructure", "transport"),
    "HABITAT_CONNECTIVITY": ("land", "biodiversity"),
    "EROSION_PROTECTION": ("land", "soil"),
    "HUMUS_BUILDUP": ("land", "soil"),
    "DROUGHT_RESISTANT_VARIETIES": ("land", "agriculture"),
    "WATER_STORAGE_EFFICIENT_IRRIGATION": ("land", "agriculture"),
    "MIXED_FORESTS": ("land", "forestry"),
    "WILDFIRE_PREVENTION": ("land", "forestry"),
    "HEAT_ACTION_PLANS": ("health", "health"),
    "COOLING_ROOMS_DRINKING_WATER": ("health", "health"),
    "EARLY_WARNING_MEASURE": ("urban", "civil_protection"),
    "EVACUATION_EMERGENCY_PLANS": ("urban", "civil_protection"),
    "BUILDING_BANS_RISK_ZONES": ("urban", "spatial_planning"),
    "FRESH_AIR_CORRIDORS": ("urban", "spatial_planning"),
    "URBAN_GREEN": ("urban", "urban_dev"),
    "SPONGE_CITY": ("urban", "urban_dev"),
    "DESEALING_SURFACE": ("urban", "urban_dev"),
    "PUBLIC_SHADE_WATER": ("urban", "urban_dev"),
    "ADAPTIVE_FISHERIES_MANAGEMENT": ("water", "fisheries"),
    "FISH_PASSAGE_RESTORATION": ("water", "fisheries"),
    "AQUACULTURE_RESILIENCE_SYSTEMS": ("water", "fisheries"),
    "FISHERIES_SPAWNING_HABITAT_RESTORATION": ("water", "fisheries"),
    "FISHERIES_WATER_QUALITY_PROTECTION": ("water", "fisheries"),
    "LEVEE_REINFORCEMENT": ("water", "coastal"),
    "SALTWATER_BARRIERS": ("water", "coastal"),
    "DRAINAGE_SWALES": ("water", "water_management"),
    "FLOODPLAIN_RENATURATION": ("water", "water_management"),
    "RETENTION_STORAGE": ("water", "water_management"),
    "RETENTION_POLDER_RESERVOIR": ("water", "water_management"),
    "INFILTRATION_AREAS": ("water", "water_management"),
    "RUNOFF_ROUTING_DGM": ("water", "water_management"),
    "GROUNDWATER_RECHARGE": ("water", "water_management"),
    "LEAKAGE_REDUCTION": ("water", "water_management"),
    "RISK_BASED_INVESTMENTS": ("economy", "finance"),
    "PREVENTION_INCENTIVES": ("economy", "finance"),
    "INDUSTRIAL_COOLING_CONCEPTS": ("economy", "industry"),
    "SUPPLY_CHAIN_RESILIENCE": ("economy", "industry"),
    "VULNERABLE_GROUP_PROGRAMS": ("crosscutting", "general"),
    "HEAT_WORK_SCHEDULES": ("crosscutting", "general"),
}

# Felder injizieren (in-place), damit /catalog die Kategorien automatisch ausgibt.
for _h in HAZARDS:
    _h["category"] = _HAZARD_CATEGORY_MAP.get(_h["code"], "compound")
for _e in EXPOSURES:
    _e["category"] = _EXPOSURE_CATEGORY_MAP.get(_e["code"], "people")
for _v in VULNERABILITIES:
    _v["category"] = _VULNERABILITY_CATEGORY_MAP.get(_v["code"], "technical")
for _m in MEASURES:
    _cluster, _field = _MEASURE_KANG_MAP.get(_m["code"], ("crosscutting", "general"))
    _m["kang_cluster"] = _cluster
    _m["kang_field"] = _field


from app.data.catalog_auxiliary import AUXILIARY, AUXILIARY_CATEGORIES, AUXILIARY_BY_CODE

# ── Lookups ──────────────────────────────────────────────────────────────────────

HAZARDS_BY_CODE = {h["code"]: h for h in HAZARDS}
EXPOSURES_BY_CODE = {e["code"]: e for e in EXPOSURES}
VULNERABILITIES_BY_CODE = {v["code"]: v for v in VULNERABILITIES}
RISKS_BY_CODE = {r["code"]: r for r in RISKS}
MEASURES_BY_CODE = {m["code"]: m for m in MEASURES}

INDICATOR_BY_CODE = {
    **HAZARDS_BY_CODE,
    **EXPOSURES_BY_CODE,
    **VULNERABILITIES_BY_CODE,
    **AUXILIARY_BY_CODE,
}


def normalize_value(code: str, value: float) -> float:
    """Normalisiert einen absoluten H/E/V-Wert auf 0..1 anhand der Referenzskala.

    Wird AUSSCHLIESSLICH für die Risikoberechnung verwendet.
    """
    meta = INDICATOR_BY_CODE.get(code)
    if not meta:
        return 0.0
    lo = float(meta.get("norm_min", 0.0))
    hi = float(meta.get("norm_max", 1.0))
    if hi <= lo:
        return 0.0
    x = (float(value) - lo) / (hi - lo)
    return max(0.0, min(1.0, x))


def group_label(code: str) -> str:
    for g in KWRA_GROUPS:
        if g["code"] == code:
            return g["label"]
    return code
