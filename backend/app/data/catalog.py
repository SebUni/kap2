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
     "source": "DWD CDC / Copernicus C3S-CORDEX (regionalisiert)",
     "source_detail": "Normierungs-Obergrenze 3,0 °C entspricht der Spanne des projizierten "
        "mittleren Temperaturanstiegs in Deutschland bis Ende des Jahrhunderts unter mittleren "
        "bis hohen Emissionspfaden (DWD Nationaler Klimareport; IPCC AR6 WG1). Die angezeigten "
        "H-Werte stammen aus regionalem DWD-Mittel + lokalem UHI-Aufschlag; editierbar.",
     "source_refs": ["DWD_Klimareport", "IPCC_AR6_WG1"]},
    {"code": "SEA_LEVEL_RISE", "name": "Meeresspiegelanstieg",
     "unit": "mm/Jahr", "norm_min": 0.0, "norm_max": 10.0, "spatial": False, "coastal": True,
     "description": "Langfristiger Anstieg des mittleren Meeresspiegels an Küsten.",
     "proxy": "Regionaler Konstantwert; nur für Küstenkommunen aktiv.",
     "source": "Copernicus C3S / BSH",
     "source_detail": "Normierungsskala 0-10 mm/a: IPCC AR6 WG1 projiziert für hohe "
        "Emissionsszenarien globale Meeresspiegelanstiegsraten in dieser Größenordnung bis "
        "Ende des Jahrhunderts. Für Binnenkommunen inaktiv (nur Küste); editierbar.",
     "source_refs": ["IPCC_AR6_WG1"]},
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
     "source": "DWD CDC (Raster) + UHI-Modell (OSM)",
     "source_detail": "Normierungs-Obergrenze 40 heiße Tage/Jahr orientiert sich an der "
        "beobachteten und projizierten Zunahme heißer Tage (Tmax ≥ 30 °C) in Deutschland "
        "(DWD Nationaler Klimareport). Die Zell-Werte stammen aus dem DWD-CDC-Raster zzgl. "
        "UHI-Aufschlag; editierbar.",
     "source_refs": ["DWD_Klimareport"]},
    {"code": "COLD_EXTREME", "name": "Kälteextreme und Frostereignisse",
     "unit": "Tage/Jahr", "norm_min": 0.0, "norm_max": 40.0, "spatial": True,
     "description": "Extreme Kälte- und Frostereignisse (regional relevant).",
     "proxy": "DWD-CDC Frosttage-Raster (1 km, am Kommune-Zentroid), leicht reduziert in dicht bebauten (wärmeren) Zellen.",
     "source": "DWD CDC (Raster)"},
    {"code": "HEAVY_RAIN_FLOOD", "name": "Starkniederschlag und Fluten",
     "unit": "Index", "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Extreme Niederschläge inkl. Überflutungen und Sturzfluten.",
     "proxy": "Versiegelungsgrad (OSM) × TWI/Senkenlage (Terrarium-DEM, D8) × regionaler Starkregenindex.",
     "source": "DWD CDC + AWS Terrarium DEM",
     "source_detail": "Der Starkregen-/Überflutungsindex (0-100) kombiniert Versiegelung, "
        "Senkenlage und regionalen Starkregentrend. Die Zunahme von Starkniederschlägen in "
        "Deutschland ist im DWD Nationalen Klimareport dokumentiert; die Skala selbst ist eine "
        "dokumentierte Modellwahl (dimensionsloser Index), editierbar.",
     "source_refs": ["DWD_Klimareport"]},
    {"code": "DROUGHT", "name": "Dürren",
     "unit": "Tage/Jahr", "norm_min": 0.0, "norm_max": 60.0, "spatial": True,
     "description": "Meteorologische, hydrologische oder agrarische Dürreperioden.",
     "proxy": "Trockentage (Proxy aus DWD-CDC heißen Tagen am Zentroid) + erhöhte Empfindlichkeit auf versiegelten/landwirtschaftlichen Flächen.",
     "source": "DWD CDC (Raster, abgeleitet) / UBA",
     "source_detail": "Normierungs-Obergrenze 60 Trocken-/Dürretage orientiert sich an der "
        "beobachteten und projizierten Zunahme von Trockenperioden in Deutschland (DWD "
        "Nationaler Klimareport; UBA Klimawirkungs- und Risikoanalyse 2021, Handlungsfeld "
        "Boden/Landwirtschaft). Zell-Werte als Proxy abgeleitet; editierbar.",
     "source_refs": ["DWD_Klimareport", "UBA_KWRA_2021"]},
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
     "source": "Zensus 2022 (100m-Gitter, Destatis)",
     "source_detail": "Werte und Normierungsskala basieren auf dem Zensus 2022 (Destatis) im "
        "100-Meter-Gitter (Bevölkerungszahl, Altersanteile ≥65/<18 Jahre bzw. sozioökonomische "
        "Merkmale je Zelle). Die Referenzskala (norm_min/norm_max) ist eine dokumentierte "
        "Modellwahl auf Basis typischer Wertespannen dieser amtlichen Gitterdaten; editierbar.",
     "source_refs": ["Zensus_2022"]},
    {"code": "AGE_STRUCTURE", "name": "Altersstruktur (Ältere, Kinder)",
     "unit": "%", "norm_min": 0.0, "norm_max": 50.0, "spatial": True,
     "description": "Anteil altersbedingt vulnerabler Bevölkerungsgruppen.",
     "proxy": "Zensus-100m: Anteil ≥65 Jahre + Anteil <18 Jahre je Zelle.",
     "source": "Zensus 2022 (100m-Gitter, Destatis)",
     "source_detail": "Werte und Normierungsskala basieren auf dem Zensus 2022 (Destatis) im "
        "100-Meter-Gitter (Bevölkerungszahl, Altersanteile ≥65/<18 Jahre bzw. sozioökonomische "
        "Merkmale je Zelle). Die Referenzskala (norm_min/norm_max) ist eine dokumentierte "
        "Modellwahl auf Basis typischer Wertespannen dieser amtlichen Gitterdaten; editierbar.",
     "source_refs": ["Zensus_2022"]},
    {"code": "OUTDOOR_THERMAL_EXPOSURE", "name": "Aufenthalt im Freien (therm. Exposition)",
     "unit": "h/Tag", "norm_min": 0.0, "norm_max": 8.0, "spatial": True,
     "description": "Exposition der Bevölkerung durch Aufenthalt im Freien bei Hitze.",
     "proxy": "Proxy aus Anteil öffentlicher Freiflächen/Arbeitsplätze (OSM) + Bevölkerung.",
     "source": "OSM / Zensus (Proxy)"},
    {"code": "VULNERABLE_GROUPS_POPULATION", "name": "Vulnerable Gruppen (Personen)",
     "unit": "Pers.", "norm_min": 0.0, "norm_max": 2000.0, "spatial": True,
     "description": "Bevölkerungsgruppen mit erhöhter Schadenswahrscheinlichkeit.",
     "proxy": "Zensus-100m: Bevölkerung × (Anteil ≥65 + Anteil <18) je Zelle.",
     "source": "Zensus 2022 (100m-Gitter, Destatis)",
     "source_detail": "Werte und Normierungsskala basieren auf dem Zensus 2022 (Destatis) im "
        "100-Meter-Gitter (Bevölkerungszahl, Altersanteile ≥65/<18 Jahre bzw. sozioökonomische "
        "Merkmale je Zelle). Die Referenzskala (norm_min/norm_max) ist eine dokumentierte "
        "Modellwahl auf Basis typischer Wertespannen dieser amtlichen Gitterdaten; editierbar.",
     "source_refs": ["Zensus_2022"]},
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
     "source": "Zensus 2022 (100m-Gitter, Destatis)",
     "source_detail": "Werte und Normierungsskala basieren auf dem Zensus 2022 (Destatis) im "
        "100-Meter-Gitter (Bevölkerungszahl, Altersanteile ≥65/<18 Jahre bzw. sozioökonomische "
        "Merkmale je Zelle). Die Referenzskala (norm_min/norm_max) ist eine dokumentierte "
        "Modellwahl auf Basis typischer Wertespannen dieser amtlichen Gitterdaten; editierbar.",
     "source_refs": ["Zensus_2022"]},
    {"code": "INCOME_SOCIAL_RESILIENCE", "name": "Soziale Resilienz (invers)", "unit": "Index",
     "norm_min": 0.0, "norm_max": 100.0, "spatial": True,
     "description": "Sozioökonomische Resilienz (hoher Wert = geringe Resilienz).",
     "proxy": "Kombination aus Nettokaltmiete, Eigentümerquote und Wohnfläche je Bewohner (Zensus-100m).",
     "source": "Zensus 2022 (100m-Gitter, Destatis)",
     "source_detail": "Werte und Normierungsskala basieren auf dem Zensus 2022 (Destatis) im "
        "100-Meter-Gitter (Bevölkerungszahl, Altersanteile ≥65/<18 Jahre bzw. sozioökonomische "
        "Merkmale je Zelle). Die Referenzskala (norm_min/norm_max) ist eine dokumentierte "
        "Modellwahl auf Basis typischer Wertespannen dieser amtlichen Gitterdaten; editierbar.",
     "source_refs": ["Zensus_2022"]},
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


# ── Risiko-Quellenanreicherung (source_detail + IEEE-Referenzen) ──────────────────
# Zentral gepflegte Herleitungstexte + Bibliografie-Verweise je Risiko, sodass der
# (i)-Tooltip an JEDEM Referenzwert erklärt, wie der Wert zustande kommt und worauf er
# sich stützt. Ableitung erfolgt anhand des ``source``-Labels; reine Modellannahmen und
# Index=Outcome-Risiken erhalten einen ehrlichen Erklärtext OHNE (erfundene) Quelle.

def _enrich_risk_sources() -> None:
    def eur(v: float) -> str:
        return f"{int(round(v)):,}".replace(",", ".") + " €"

    def scale_word(s: str) -> str:
        return {"pop": "der Bevölkerung", "area": "der betroffenen Fläche",
                "flat": "pauschal (mengenunabhängig)"}.get(s, s)

    # Belastbar dokumentierte Einzelrisiken mit maßgeschneidertem Herleitungstext.
    BESPOKE: dict[str, tuple[str, list[str]]] = {
        "EXPECTED_ANNUAL_MORTALITY": (
            "Worst-Case-Anker 18/100.000 bei Index=100 ≈ 1,7× des bislang schlimmsten "
            "beobachteten Jahres (2018: ~8.700 Hitzetote ≈ 10,5/100.000; RKI-Methodik nach "
            "Winklmayr u. a. 2022, RKI-Sachstandsbericht Klimawandel & Gesundheit 2023). Die "
            "UBA-Klimawirkungs- und Risikoanalyse 2021 (Handlungsfeld Gesundheit) bestätigt die "
            "zunehmende Hitzemortalität. Eine typische Kommune mit P90-Index 20-40 ergibt "
            "3,6-7,2/100.000 (statistikkonform). Kostensatz 3,5 Mio € (VSL im gängigen "
            "EU/OECD-Band ~1-4 Mio) als Punktwert; editierbar.",
            ["RKI_Hitzemortalitaet", "UBA_KWRA_2021"]),
        "EXPECTED_BUILDING_DAMAGE_EUR": (
            "Nationale jährliche Gebäudeschäden (Hochwasser + Sturm/Hagel) ~3,5 Mrd €/a ÷ 832 "
            "(100.000-Einwohner-Einheiten in DE) ≈ 4,2 Mio €/100.000 → 4,5 Mio € bei Index=100. "
            "Größenordnung belegt durch Prognos/GWS/IÖW 2023 „Kosten durch Klimawandelfolgen in "
            "Deutschland“ (BMWK/BMUV): Ahrtal 2021 mit Anteil Bauwesen + Privathaushalte 20,9 "
            "von 40,5 Mrd €. Skaliert mit der Bevölkerung; editierbar.",
            ["Prognos_Klimaschaeden_2023"]),
        "EXPECTED_TRANSPORT_DAMAGE_EUR": (
            "Nationale jährliche Verkehrsinfrastruktur-Schäden ~1,5 Mrd €/a ÷ 832 ≈ 1,8 Mio "
            "€/100.000 bei Index=100. Größenordnung belegt durch Prognos/GWS/IÖW 2023 (BMWK/"
            "BMUV): Ahrtal 2021 mit Verkehrsanteil 6,8 von 40,5 Mrd € (~17 %). Skaliert mit "
            "der Bevölkerung; editierbar.",
            ["Prognos_Klimaschaeden_2023"]),
        "EXPECTED_AQUACULTURE_DAMAGE_EUR": (
            "Punktwert 200.000 € je ~50 km² Gewässerfläche bei Index=100 (Aquakultur ist in "
            "DE sehr klein). Für diese Einzelposition liegt keine belastbare Prognos-Zahl vor "
            "⇒ editierbare Modellannahme (nur Größenordnung), ohne eigene Quelle.",
            []),
    }

    for r in RISKS:
        if r.get("source_detail"):
            continue
        code, src = r["code"], r.get("source", "")
        rv = r.get("ref_value", 0.0)
        unit = r.get("outcome_unit", "")
        cost = r.get("cost_per_outcome_eur")
        if code in BESPOKE:
            detail, refs = BESPOKE[code]
        elif "UBA MK3.1" in src:  # Gesundheits-Outcomes (Kostensatz aus UBA-Methodenkonvention)
            detail = (
                f"Punktwert {rv:g} {unit} je Referenzkommune (100.000 Ew.) bei Index=100. Der "
                f"zugehörige Kostensatz ({eur(cost)}/Fall) ist an den Gesundheits-Kostensätzen "
                "der UBA-Methodenkonvention 3.1 (2020) orientiert. Für die Fallzahl selbst liegt "
                "keine belastbare nationale Pro-Kopf-Statistik vor ⇒ editierbare Modellannahme "
                "mit UBA MK3.1 als Kostensatz-Anker.")
            refs = ["UBA_Methodenkonvention_MK3.1"]
        elif "Belastungsstunden" in src:  # reine Belastungsindikatoren ohne Kostensatz
            detail = (
                f"Reiner Belastungsindikator ohne monetären Kostensatz (cost_per_outcome_eur=0). "
                f"Punktwert {rv:g} {unit} je Referenzkommune bei Index=100 als editierbare "
                "Modellannahme; keine belastbare Messreihe hinterlegt (unbelegt).")
            refs = []
        elif src.startswith("Prognos"):  # monetäre Schadens-/Verlustrisiken
            detail = (
                f"Schadensanker {eur(rv)} je Referenzeinheit bei Index=100. Die Größenordnung "
                "ist der Studie Prognos/GWS/IÖW 2023 „Kosten durch Klimawandelfolgen in "
                "Deutschland“ (BMWK/BMUV) entnommen, die die nationalen Schäden extremer "
                "Wetterereignisse (u. a. Dürre-/Hitzesommer 2018/2019, Flut 2021) systematisiert "
                f"und für Sektoren modelliert. Skaliert mit {scale_word(r.get('scale',''))}; "
                "editierbar.")
            refs = ["Prognos_Klimaschaeden_2023"]
        elif "BBK KRITIS" in src:  # KRITIS-Ausfallzeiten
            detail = (
                f"Ausfall-/Störungsanker {rv:g} {unit} je Referenzkommune bei Index=100. Mangels "
                "kommunaler Ausfallstatistik ist der Wert eine editierbare Modellannahme; "
                "Größenordnung und Systemabgrenzung sind an den KRITIS-Betrachtungen des BBK "
                "(Bundesamt für Bevölkerungsschutz und Katastrophenhilfe) angelehnt.")
            refs = ["BBK_KRITIS"]
        elif "Index=Outcome" in src:  # normierter Index IST der Outcome
            detail = (
                f"Index-Risiko: Der normierte Risiko-Index IST hier der Outcome (ref_value=100 "
                "per Konstruktion). Das ist eine bewusste, dokumentierte und editierbare "
                "Modellwahl (kein extern belegter Absolutkennwert); die inhaltliche "
                "Belastbarkeit stammt aus den zugrunde liegenden H/E/V-Komponenten.")
            refs = []
        elif "BfN" in src:  # ökologische Flächenrisiken
            detail = (
                f"Punktwert {rv:g} {unit} je Referenzkommune (Flächenbezug) bei Index=100 als "
                "editierbare Modellannahme. Ein belastbarer nationaler Pro-Fläche-Kennwert fehlt; "
                "die Größenordnung ist qualitativ am UBA-KWRA-2021-Handlungsfeld Biologische "
                "Vielfalt/Boden sowie an BfN-Befunden orientiert.")
            refs = ["UBA_KWRA_2021"]
        else:
            continue
        r["source_detail"] = detail
        if refs:
            r["source_refs"] = refs


_enrich_risk_sources()


# ── Quellenanreicherung Hazards/Expositionen/Sensitivitäten ──────────────────────
# Leitet je Indikator einen source_detail (Herkunft/Proxy + Bedeutung der Normierungs-
# skala) und – wo eine reale Datengrundlage im source-Label steckt – IEEE/Wayback-Verweise
# ab. Reine Annahme-/qualitative Werte bleiben ehrlich ohne Referenz. Bereits inline
# belegte Einträge (Kern-Hazards, Zensus) werden übersprungen.

def _enrich_hev_sources() -> None:
    # Schlüsselwort im source-Label -> (Bibliografie-Key, Anzeigename).
    KEYWORD_REFS: tuple[tuple[str, str, str], ...] = (
        ("OSM", "OSM_Data", "OpenStreetMap (ODbL)"),
        ("DWD", "DWD_CDC", "DWD Climate Data Center"),
        ("Copernicus", "Copernicus_C3S", "Copernicus C3S"),
        ("Sentinel", "Copernicus_C3S", "Copernicus C3S"),
        ("Zensus", "Zensus_2022", "Zensus 2022 (Destatis)"),
        ("INKAR", "BBSR_INKAR", "BBSR INKAR"),
        ("BBSR", "BBSR_INKAR", "BBSR INKAR"),
        ("UHI", "VDI3787_Stadtklima", "VDI 3787 Bl.1"),
        ("UBA", "UBA_KWRA_2021", "UBA KWRA 2021"),
    )

    for items in (HAZARDS, EXPOSURES, VULNERABILITIES):
        for m in items:
            if m.get("source_detail"):
                continue
            src = m.get("source", "")
            proxy = m.get("proxy", "").strip()
            unit = m.get("unit", "")
            nmin, nmax = m.get("norm_min", 0.0), m.get("norm_max", 0.0)

            refs: list[str] = []
            names: list[str] = []
            for kw, key, name in KEYWORD_REFS:
                if kw in src and key not in refs:
                    refs.append(key)
                    names.append(name)

            if refs:
                closing = f"Datengrundlage(n): {', '.join(names)}."
            else:
                closing = ("Mangels belastbarer Einzelquelle beruht der Wert auf einer "
                           "dokumentierten Modell-/Regionalannahme (unbelegt).")

            proxy_txt = f"Datengrundlage/Proxy: {proxy} " if proxy else ""
            if m.get("spatial", True):
                lead = f"Wert je 100-m-Zelle in {unit} (absolute Einheit). "
            else:
                lead = (f"Nicht räumlich aufgelöst: regionaler/nationaler Konstantwert "
                        f"in {unit}. ")
            scale_txt = (f"Die Referenzskala norm_min={nmin:g}…norm_max={nmax:g} {unit} dient "
                         "ausschließlich der Risiko-Normierung (0..1), nicht der Anzeige, und ist "
                         "eine dokumentierte, editierbare Modellwahl. ")
            m["source_detail"] = lead + proxy_txt + scale_txt + closing
            if refs:
                m["source_refs"] = refs


_enrich_hev_sources()


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
#
# Kostenmodell — symmetrisch CAPEX (einmalig) / OPEX (jährlich), je fix / Stück / Fläche.
# MECE: jeder Euro ist entweder einmalige Investition (CAPEX) oder wiederkehrende Betriebs-
# und Unterhaltskosten (OPEX); innerhalb beider Blöcke disjunkt nach Bezugsgröße (mengen-
# unabhängig / je Stück / je m²). Nicht anwendbar = None, NICHT 0.0 — 0.0 heißt "anwendbar,
# aber kostenlos" (z. B. planungsrechtliche Bauverbote).
#   capex_fixed          € einmalig, mengenunabhängig (Planung/Konzept/Einrichtung)
#   capex_per_unit       €/Stück      einmalig je Einheit (unit_label)
#   capex_per_m2         €/m²         einmalig je Polygonfläche
#   opex_fixed_year      €/a          wiederkehrend, mengenunabhängig (Betrieb/Koordination)
#   opex_per_unit_year   €/(Stück·a)  wiederkehrend je Einheit (Betrieb & Unterhalt)
#   opex_per_m2_year     €/(m²·a)     wiederkehrend je Fläche (Betrieb & Unterhalt)
#   unit_label           z. B. "Brunnen", "Station", "km"; None ⇒ keine Stück-Logik
#   unit_density_per_ha  Stück/ha Richtwert-Dichte (gesetzt wenn unit_label);
#                         Richtwert-Anzahl = max(1, round(density · Fläche_ha)),
#                         skaliert die Wirkung über u = min(1, Anzahl/Richtwert)
#   source / sources     Kurz-Key-Fallback bzw. per-Feld-Kurzquelle (Keys = Feldnamen
#                         inkl. default_reduction, unit_density_per_ha)
#   source_details       per-Feld-Langtext (Hover-Tooltip): woher der Wert stammt bzw. wie
#                         er hergeleitet/plausibilisiert wurde (Keys = Feldnamen)
# CAPEX  = capex_fixed + Anzahl × capex_per_unit + Fläche × capex_per_m2
# OPEX/a = opex_fixed_year + Anzahl × opex_per_unit_year + Fläche × opex_per_m2_year
# benefit_per_m2_year (Nutzen-Seite) bleibt unverändert vom Kostenmodell getrennt.
# default_reduction: unbelegte Modellannahme je Maßnahme (keine externe Kalibrierstudie
#   vorhanden); Kommune kann Wert über PUT /kommune/{id}/parameters mit eigener Quelle
#   überschreiben (source-Fallback: "Modellannahme (Maßnahmenwirkung, unbelegt)").
# Kostenquellen sind Stand dieser Migration überwiegend "Modellannahme (Maßnahmenkosten,
#   unbelegt)" bzw. für unit_density_per_ha "Modellannahme (Richtwert-Dichte, unbelegt)" —
#   der Recherche-Pass mit belastbaren Quellen je Maßnahme folgt in einem späteren Schritt.

MEASURES: list[dict] = [
    # Herleitung capex_per_unit: eine einzelne Ortsnetzstation kostet ~18.000-50.000 € (400-kVA-
    # Trafo bis eigene MS-Station inkl. Verkabelung; ront.info, ms-elektro), eine vollständige
    # Mittelspannungs-Netzverstärkung ~0,8-3 Mio € (Bayernwerk-Projekte). Der Wert 250.000 €/
    # "Station" steht für ein Verstärkungs-/Redundanzpaket je Netzknoten (Stationsausbau +
    # redundante Einspeisung + Kabelabschnitt), plausibilisiert zwischen Einzelstation und
    # Vollausbau (BNetzA/dena-Größenordnung).
    {"code": "GRID_REINFORCEMENT_REDUNDANCY", "name": "Netzverstärkung / Redundanzen",
     "description": "Erhöht Redundanz im Energienetz.", "measure_type": "structural",
     "effect_target": ["vulnerability"], "default_reduction": 0.30, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_ENERGY_OUTAGE_HOURS", "EXPECTED_CI_OUTAGE_HOURS"],
     "capex_fixed": 0.0, "capex_per_unit": 250000.0, "capex_per_m2": None,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": "Station", "unit_density_per_ha": 0.005,
     "source": "Verteilnetzbetreiber-Praxiswerte (ront.info / Bayernwerk) / BNetzA-Größenordnung",
     "sources": {"capex_per_unit": "Verteilnetz-Praxiswerte (Einzelstation bis MS-Ausbau)",
                 "unit_density_per_ha": "Modellannahme (Richtwert-Dichte, unbelegt)"},
     "source_refs": {"capex_per_unit": ["RONT_Ortsnetzstation"]},
     "source_details": {
        "capex_per_unit": "Eine einzelne Ortsnetzstation kostet ~18.000-50.000 € (400-kVA-Trafo "
            "bis eigene Mittelspannungsstation inkl. Verkabelung; ront.info, ms-elektro.gmbh); "
            "eine vollständige MS-Netzverstärkung liegt bei ~0,8-3 Mio € (Bayernwerk-Projekte). "
            "Der Punktwert 250.000 € je \"Station\" steht für ein Verstärkungs-/Redundanzpaket "
            "je Netzknoten (Stationsausbau + redundante Einspeisung + Kabelabschnitt), "
            "eingeordnet zwischen Einzelstation und Vollausbau (BNetzA/dena-Größenordnung).",
        "unit_density_per_ha": "Modellannahme mangels belastbarer Quelle: ~1 relevanter "
            "Netzknoten je 200 ha Versorgungsgebiet (0,005 Stationen/ha)."}},
    # Herleitung capex_per_unit: keine belastbare Einzelquelle für die hitzefeste Ertüchtigung/
    # Kühlung energiebezogener Anlagen (Transformatoren, Umspannwerke) — Modellannahme.
    # Größenordnung sechsstellig je Anlage (Zusatzkühlung/Redundanz); Punktwert 120.000 €.
    {"code": "HEAT_RESISTANT_PLANT_COOLING", "name": "Hitzefeste Anlagen / Kühlung",
     "description": "Technische Anpassung energiebezogener Anlagen an Hitze.", "measure_type": "structural",
     "effect_target": ["hazard"], "default_reduction": 0.20, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_ENERGY_INFRA_DAMAGE_EUR"],
     "capex_fixed": 0.0, "capex_per_unit": 120000.0, "capex_per_m2": None,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": "Anlage", "unit_density_per_ha": 0.003,
     "source": "Modellannahme (mangels belastbarer Quelle)",
     "sources": {"capex_per_unit": "Modellannahme (mangels belastbarer Quelle)",
                 "unit_density_per_ha": "Modellannahme (Richtwert-Dichte, unbelegt)"},
     "source_details": {
        "capex_per_unit": "Für die hitzefeste Ertüchtigung/Zusatzkühlung energiebezogener "
            "Anlagen (Transformatoren, Umspannwerke) war keine belastbare Einzelquelle "
            "auffindbar. Modellannahme in sechsstelliger Größenordnung je Anlage (Zusatz"
            "kühlung, thermische Absicherung, Redundanz) → Punktwert 120.000 €.",
        "unit_density_per_ha": "Modellannahme mangels belastbarer Quelle: ~1 hitzekritische "
            "Anlage je 330 ha (0,003 Anlagen/ha)."}},
    # Herleitung capex_per_m2: schlüsselfertige Aufdach-PV ~1.015-1.200 €/kWp (2026), Batterie-
    # speicher ~315-500 €/kWh (HTW-Stromspeicher-Inspektion 2025; 42watt). Bei ~6 m² Modul-
    # fläche je kWp entspricht das ~170-200 €/m² Modulfläche; über die Bruttodachfläche inkl.
    # Speicheranteil → Punktwert 150 €/m². opex_per_m2_year: ~1-2 % Betrieb/Versicherung.
    {"code": "DECENTRALIZED_ENERGY_PV_STORAGE", "name": "Dezentrale Energie (PV, Speicher)",
     "description": "Dezentrale Erzeugung und Speicher.", "measure_type": "structural",
     "effect_target": ["vulnerability"], "default_reduction": 0.25, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_ENERGY_OUTAGE_HOURS", "SYSTEMIC_DOMINO_RISK_INDEX"],
     "capex_fixed": 0.0, "capex_per_unit": None, "capex_per_m2": 150.0,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 2.0, "benefit_per_m2_year": 8.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "HTW-Stromspeicher-Inspektion 2025 / 42watt (PV + Speicher)",
     "sources": {"capex_per_m2": "HTW Berlin / 42watt (PV-Systempreis + Speicher)",
                 "opex_per_m2_year": "Modellannahme (Betrieb/Versicherung ~1-2 %)"},
     "source_refs": {"capex_per_m2": ["HTW_Stromspeicher_2025"]},
     "source_details": {
        "capex_per_m2": "Schlüsselfertige Aufdach-PV kostet ~1.015-1.200 €/kWp (Frühjahr 2026, "
            "historischer Tiefstand), Batteriespeicher ~315 €/kWh bzw. konservativ 500 €/kWh "
            "(HTW-Stromspeicher-Inspektion 2025, HTW Berlin; 42watt.de). Bei ~6 m² Modulfläche "
            "je kWp sind das ~170-200 €/m² Modulfläche; über die Bruttodachfläche inklusive "
            "Speicheranteil → Punktwert 150 €/m².",
        "opex_per_m2_year": "Modellannahme: ~1-2 % der Investition pro Jahr für Betrieb, "
            "Wartung, Wechselrichter-Rücklage und Versicherung → 2 €/m²/a."}},
    # Herleitung capex_per_m2/opex_per_m2_year: Mischmaßnahme Dach- + Fassadenbegrünung.
    # Extensives Gründach 40-70 €/m² Herstellung, Unterhalt 0,50-5 €/m²/a (BuGG-Marktreport;
    # 11880-dachdecker/co2online 2026); bodengebundene Fassadenbegrünung 15-35 €/m²
    # (co2online/gartenbau.org 2025). 55 €/m² Investition + 4 €/m²/a Unterhalt als Blend im
    # oberen Bereich (Gründach dominiert die Fläche).
    {"code": "GREEN_ROOFS_FACADES", "name": "Begrünte Dächer/Fassaden",
     "description": "Begrünung von Dächern und Fassaden.", "measure_type": "structural",
     "effect_target": ["hazard", "exposure"], "default_reduction": 0.18, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_THERMAL_STRESS_HOURS", "EXPECTED_BUILDING_DAMAGE_EUR"],
     "capex_fixed": 0.0, "capex_per_unit": None, "capex_per_m2": 55.0,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 4.0, "benefit_per_m2_year": 6.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "BuGG-Marktreport / Marktpreise Dach-/Fassadenbegrünung",
     "sources": {"capex_per_m2": "BuGG-Marktreport / Marktpreise Gründach + Fassade",
                 "opex_per_m2_year": "Marktpreise Gründach-/Fassadenpflege"},
     "source_refs": {"capex_per_m2": ["BuGG_Marktreport_2024", "co2online_Dachbegruenung"],
                     "opex_per_m2_year": ["BuGG_Marktreport_2024", "co2online_Dachbegruenung"]},
     "source_details": {
        "capex_per_m2": "Mischmaßnahme aus Dach- und Fassadenbegrünung. Extensives Gründach "
            "kostet 40-70 €/m² Herstellung (BuGG-Marktreport Gebäudegrün; 11880-dachdecker, "
            "co2online 2026), bodengebundene Fassadenbegrünung 15-35 €/m² (co2online, "
            "gartenbau.org 2025; wandgebundene Systeme ab 400 €/m² hier ausgeklammert). "
            "Punktwert 55 €/m² als flächengewichteter Blend im oberen Gründach-Bereich.",
        "opex_per_m2_year": "Unterhalt Gründach 0,50-5 €/m²/a (BuGG/co2online 2026), "
            "bodengebundene Fassade 5-50 €/m²/a bei fachgerechter Pflege. Punktwert 4 €/m²/a "
            "für den überwiegenden Gründachanteil zzgl. moderatem Fassadenpflegeaufwand."}},
    # Herleitung capex_per_m2: Objektschutz ist eigentlich objekt-/öffnungsbezogen, nicht
    # flächenbezogen — die BBK-Hochwasserschutzfibel (BMWSB 2022) beschreibt die Maßnahmen
    # qualitativ ohne €/m²-Kennwert. €/m² ist hier eine Modell-Abstraktion, plausibilisiert
    # anhand Einzelmaßnahmenkosten: Rückstauklappe fachkundig ~2.000-3.000 €, mobile
    # Kellerfenster-Schotts 800-1.200 €/Fenster (kostencheck/glaserei.org 2026), zzgl.
    # Abdichtung/Barrieren. Auf typische geschützte Gebäudegrundfläche umgelegt → 40 €/m².
    {"code": "FLOOD_PROTECTION_BUILDING", "name": "Hochwasserschutz (Gebäude)",
     "description": "Gebäudespezifischer Hochwasserschutz.", "measure_type": "structural",
     "effect_target": ["vulnerability"], "default_reduction": 0.35, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_BUILDING_DAMAGE_EUR"],
     "capex_fixed": 0.0, "capex_per_unit": None, "capex_per_m2": 40.0,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 1.0, "benefit_per_m2_year": 9.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "BBK-Hochwasserschutzfibel (qualitativ) / Modell-Umlage Objektschutz",
     "sources": {"capex_per_m2": "Modell-Umlage Objektschutz-Einzelmaßnahmen",
                 "opex_per_m2_year": "Modellannahme (Wartung/Funktionsprüfung)"},
     "source_refs": {"capex_per_m2": ["BBK_Hochwasserschutzfibel", "Kostencheck_Rueckstauklappe"]},
     "source_details": {
        "capex_per_m2": "Gebäude-Objektschutz ist objekt-/öffnungsbezogen, nicht flächen"
            "bezogen; die BBK-/BMWSB-Hochwasserschutzfibel (2022) beschreibt die Maßnahmen "
            "qualitativ ohne €/m²-Kennwert. Der €/m²-Wert ist daher eine Modell-Umlage, "
            "plausibilisiert anhand Einzelmaßnahmen: fachkundig eingebaute Rückstauklappe "
            "~2.000-3.000 €, mobile Kellerfenster-Schotts 800-1.200 €/Fenster (kostencheck.de, "
            "glaserei.org 2026) zzgl. Abdichtung und Barrieren. Auf die typische geschützte "
            "Gebäudegrundfläche umgelegt ergibt sich der Punktwert 40 €/m².",
        "opex_per_m2_year": "Modellannahme: 1 €/m²/a für jährliche Funktionsprüfung/"
            "Wartung von Rückstausicherungen und mobilen Schutzelementen sowie deren "
            "Ersatzbeschaffung über die Nutzungsdauer."}},
    # Herleitung capex_per_m2: Entsiegelung (Aufbruch + Entsorgung + Begrünung) ~25-40 €/m²
    # je nach aufzubrechendem Material (Sieker, bauindex-online 2026); kommunale
    # Förderprogramme setzen bis 40 €/m² an (Bremen), OÖ 30 €/m² pauschal → Punktwert 35 €/m².
    {"code": "DESEALING_SURFACE", "name": "Entsiegelung",
     "description": "Rückbau versiegelter Flächen.", "measure_type": "planning",
     "effect_target": ["hazard", "vulnerability"], "default_reduction": 0.30, "coverage_scaling": "linear",
     "linked_risk_codes": ["HYDROLOGICAL_STRESS_RISK_INDEX", "EXPECTED_BUILDING_DAMAGE_EUR"],
     "capex_fixed": 0.0, "capex_per_unit": None, "capex_per_m2": 35.0,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 0.5, "benefit_per_m2_year": 5.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "Sieker / kommunale Entsiegelungs-Förderprogramme",
     "sources": {"capex_per_m2": "Sieker / Entsiegelungs-Förderprogramme (Bremen, OÖ)",
                 "opex_per_m2_year": "Modellannahme (Pflege der begrünten Fläche)"},
     "source_refs": {"capex_per_m2": ["Bremen_Entsiegelung"]},
     "source_details": {
        "capex_per_m2": "Entsiegelung (Aufbruch der Versiegelung, Entsorgung, Bodenlockerung "
            "und Begrünung) kostet ~25-40 €/m² je nach aufzubrechendem Material (Sieker, "
            "bauindex-online 2026). Kommunale Förderprogramme setzen entsprechend an: Bremen "
            "bis 40 €/m², Oberösterreich 30 €/m² pauschal. Punktwert 35 €/m² im oberen "
            "Bereich der Spanne (befestigte Flächen mit Unterbau).",
        "opex_per_m2_year": "Modellannahme: 0,50 €/m²/a geringer Pflegeaufwand der neu "
            "begrünten/entsiegelten Fläche (extensive Grünpflege)."}},
    # Herleitung capex_per_m2: sonnenreflektierende Dachbeschichtung 10-30 €/m², Acryl-
    # beschichtung im Mittel ~18 €/m² (asphalt-shop/steelmonks 2026) → Punktwert 20 €/m².
    # opex_per_m2_year: Modellannahme (anteilige Nachbeschichtung ~alle 10-15 Jahre).
    {"code": "COOL_ROOFS", "name": "Helle Dächer",
     "description": "Hochreflektive Dachflächen.", "measure_type": "structural",
     "effect_target": ["hazard"], "default_reduction": 0.15, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_THERMAL_STRESS_HOURS"],
     "capex_fixed": 0.0, "capex_per_unit": None, "capex_per_m2": 20.0,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 1.0, "benefit_per_m2_year": 3.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "Marktpreise Dachbeschichtung / Modellannahme",
     "sources": {"capex_per_m2": "Marktpreise sonnenreflektierende Dachbeschichtung",
                 "opex_per_m2_year": "Modellannahme (anteilige Nachbeschichtung)"},
     "source_refs": {"capex_per_m2": ["Asphaltshop_Dachbeschichtung"]},
     "source_details": {
        "capex_per_m2": "Sonnenreflektierende (weiße) Dachbeschichtung kostet 10-30 €/m², eine "
            "Acrylbeschichtung im Mittel ~18 €/m² (asphalt-shop.de, steelmonks 2026). "
            "Punktwert 20 €/m² im Mittel der Marktspanne für die Beschichtung einer "
            "bestehenden Dachfläche (ohne Dacherneuerung).",
        "opex_per_m2_year": "Modellannahme mangels belastbarer Quelle: 1 €/m²/a bildet "
            "die anteilige Nachbeschichtung/Auffrischung ab (Beschichtung hält je nach "
            "Produkt ~10-15 Jahre, umgelegt auf die Jahre)."}},
    # Herleitung capex_per_m2: heller/hitzeresilienter Asphalt verursacht ~3-5 €/m² Mehrkosten
    # gegenüber Normalasphalt (45-60 €/m²), d. h. 20-50 % teurer (strasse-und-autobahn.de,
    # bauindex 2026). Der Wert 30 €/m² entspricht eher einer Deckschichterneuerung mit hellem
    # Belag als nur den Mehrkosten; plausibilisiert im Bereich Teilerneuerung.
    {"code": "HEAT_RESILIENT_PAVEMENT", "name": "Hitzeresiliente Beläge",
     "description": "Beläge mit höherer Hitzebeständigkeit.", "measure_type": "structural",
     "effect_target": ["vulnerability"], "default_reduction": 0.20, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_TRANSPORT_DAMAGE_EUR"],
     "capex_fixed": 0.0, "capex_per_unit": None, "capex_per_m2": 30.0,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 1.0, "benefit_per_m2_year": 3.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "strasse-und-autobahn.de / bauindex (heller Asphalt) / Modellannahme",
     "sources": {"capex_per_m2": "Marktdaten heller/hitzeresilienter Asphalt (Teilerneuerung)",
                 "opex_per_m2_year": "Modellannahme (Belagsunterhalt)"},
     "source_refs": {"capex_per_m2": ["Kirschbaum_HellerAsphalt"]},
     "source_details": {
        "capex_per_m2": "Heller/hitzeresilienter Asphalt verursacht ~3-5 €/m² Mehrkosten "
            "gegenüber Normalasphalt (45-60 €/m²), also 20-50 % Aufpreis (strasse-und-"
            "autobahn.de, bauindex-online 2026). Der Katalogwert 30 €/m² bildet nicht nur den "
            "Aufpreis, sondern eine Deckschichterneuerung mit hellem/resilientem Belag ab "
            "(Teilerneuerung der Fahrbahnoberfläche); plausibilisiert. Als reiner Aufpreis "
            "wären ~3-5 €/m² anzusetzen.",
        "opex_per_m2_year": "Modellannahme: 1 €/m²/a Belagsunterhalt (Risssanierung, "
            "anteilige Erneuerung der Deckschicht über die Nutzungsdauer)."}},
    # Herleitung capex_per_m2: Muldenversickerung 10-45 €/m², Mulden-Rigolen-System 60-85 €/m²
    # abflusswirksamer Fläche (DWA-A 138; baupreislexikon 2026) → Punktwert 45 €/m² an der
    # oberen Grenze reiner Mulden bzw. unterer Grenze kombinierter Systeme.
    # opex_per_m2_year: DWA-Betriebskennwert 0,50-0,75 €/m² abflusswirksamer Fläche;
    # bezogen auf die (deutlich kleinere) Anlagenfläche selbst höher → Punktwert 2 €/m²/a.
    {"code": "DRAINAGE_SWALES", "name": "Entwässerung (Mulden/Rigolen)",
     "description": "Oberflächenentwässerung und Rigolen.", "measure_type": "structural",
     "effect_target": ["hazard"], "default_reduction": 0.25, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_TRANSPORT_DISRUPTION_HOURS", "HYDROLOGICAL_STRESS_RISK_INDEX"],
     "capex_fixed": 0.0, "capex_per_unit": None, "capex_per_m2": 45.0,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 2.0, "benefit_per_m2_year": 4.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "DWA-A 138 / baupreislexikon (Mulden-Rigolen)",
     "sources": {"capex_per_m2": "DWA-A 138 / baupreislexikon (Mulden-Rigolen-Versickerung)",
                 "opex_per_m2_year": "DWA-A 138 (Betrieb), auf Anlagenfläche umgerechnet"},
     "source_refs": {"capex_per_m2": ["DWA_A138", "Baupreislexikon_Versickerung"],
                     "opex_per_m2_year": ["DWA_A138", "Baupreislexikon_Versickerung"]},
     "source_details": {
        "capex_per_m2": "Nach DWA-A 138 (baupreislexikon 2026) kostet eine reine "
            "Muldenversickerung 10-45 €/m² und ein kombiniertes Mulden-Rigolen-System 60-85 "
            "€/m² abflusswirksamer Fläche. Punktwert 45 €/m² liegt an der oberen Grenze der "
            "reinen Mulde bzw. am unteren Rand kombinierter Systeme.",
        "opex_per_m2_year": "Der DWA-Betriebskennwert liegt bei 0,50-0,75 €/m² "
            "abflusswirksamer (angeschlossener) Fläche. Bezogen auf die deutlich kleinere "
            "Anlagenfläche selbst (Mulde/Rigole) fällt der spezifische Unterhalt höher aus "
            "(Mahd, Entschlammung, Kontrolle) → Punktwert 2 €/m²/a."}},
    # Herleitung capex_per_unit: keine belastbare Standardquelle für die Ertüchtigung eines
    # kritischen Verkehrsknotens (Schutz vor Überflutung/Hitze/Ausfall) — Modellannahme in
    # niedriger sechsstelliger Größenordnung je Knoten → 80.000 €.
    {"code": "CRITICAL_NODE_PROTECTION", "name": "Schutz kritischer Knoten",
     "description": "Schutzmaßnahmen für Verkehrsknoten.", "measure_type": "structural",
     "effect_target": ["exposure"], "default_reduction": 0.25, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_TRANSPORT_DISRUPTION_HOURS"],
     "capex_fixed": 0.0, "capex_per_unit": 80000.0, "capex_per_m2": None,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": "Knoten", "unit_density_per_ha": 0.02,
     "source": "Modellannahme (mangels belastbarer Quelle)",
     "sources": {"capex_per_unit": "Modellannahme (mangels belastbarer Standardquelle)",
                 "unit_density_per_ha": "Modellannahme (Richtwert-Dichte, unbelegt)"},
     "source_details": {
        "capex_per_unit": "Für die Ertüchtigung eines kritischen Verkehrsknotens (Schutz vor "
            "Überflutung, Hitze, Ausfall; z. B. Pumpen, Redundanz, Ertüchtigung von Unter"
            "führungen) war keine belastbare Standardquelle auffindbar. Modellannahme in "
            "niedriger sechsstelliger Größenordnung je Knoten → 80.000 €.",
        "unit_density_per_ha": "Modellannahme mangels belastbarer Quelle: ~1 kritischer Knoten "
            "je 50 ha Siedlungs-/Verkehrsfläche (0,02 Knoten/ha)."}},
    # Herleitung capex_per_m2: Biotopverbund (Trittsteine, Hecken, Säume, Vernetzungsstrukturen)
    # hat keinen einheitlichen Flächenkennwert; günstige lineare Vernetzungselemente
    # (vgl. Hecken 5-20 €/lfm) auf die verbundene Fläche umgelegt → niedrige €/m². Punktwert
    # 8 €/m² als Modellannahme, plausibilisiert.
    {"code": "HABITAT_CONNECTIVITY", "name": "Biotopverbund",
     "description": "Vernetzung von Lebensräumen.", "measure_type": "planning",
     "effect_target": ["vulnerability"], "default_reduction": 0.20, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_BIODIVERSITY_LOSS", "ECOSYSTEM_FRAGMENTATION_RISK_INDEX"],
     "capex_fixed": 0.0, "capex_per_unit": None, "capex_per_m2": 8.0,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 0.5, "benefit_per_m2_year": 1.5,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "Modellannahme (mangels belastbarer Quelle)",
     "sources": {"capex_per_m2": "Modellannahme, an Vernetzungselement-Kosten (Hecken) angelehnt",
                 "opex_per_m2_year": "Modellannahme (extensive Biotoppflege)"},
     "source_details": {
        "capex_per_m2": "Der Biotopverbund bündelt lineare/punktuelle Vernetzungselemente "
            "(Trittsteinbiotope, Hecken, Säume, Kleingewässer) ohne einheitlichen Flächen"
            "kennwert. Günstige lineare Elemente (vgl. Hecken 5-20 €/lfm) auf die verbundene "
            "Fläche umgelegt ergeben niedrige €/m². Punktwert 8 €/m² als Modellannahme, "
            "plausibilisiert.",
        "opex_per_m2_year": "Modellannahme: 0,50 €/m²/a für extensive Biotoppflege "
            "(Mahd, Gehölzpflege)."}},
    # Herleitung capex_per_m2: Auenrenaturierung streut extrem nach Intensität. Extensive
    # Deichrückverlegung/Flächenrückgabe ~0,3-3 €/m² (WWF/BfN Mittlere Elbe: 6,5 Mio € auf
    # 2.300 ha ≈ 2.826 €/ha ≈ 0,28 €/m²); aktive/technische Renaturierung mit Erdbau und
    # Strukturanreicherung liegt bei ~5-20 €/m² (UBA: kleine Maßnahmen ~10 €/lfm bis techn.
    # Umbau 600+ €/lfm Gewässerlauf). Punktwert 12 €/m² für moderat-intensive Renaturierung
    # mit Erdbau; Modellannahme, plausibilisiert.
    {"code": "FLOODPLAIN_RENATURATION", "name": "Auenrenaturierung",
     "description": "Renaturierung von Auen und Flussauen.", "measure_type": "planning",
     "effect_target": ["hazard"], "default_reduction": 0.30, "coverage_scaling": "linear",
     "linked_risk_codes": ["HYDROLOGICAL_STRESS_RISK_INDEX", "EXPECTED_HABITAT_LOSS"],
     "capex_fixed": 0.0, "capex_per_unit": None, "capex_per_m2": 12.0,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 0.5, "benefit_per_m2_year": 3.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "BfN/WWF/UBA (Auenrenaturierung) / Modellannahme",
     "sources": {"capex_per_m2": "BfN/WWF Mittlere Elbe + UBA (Bandbreite Renaturierung)",
                 "opex_per_m2_year": "Modellannahme (extensive Auenpflege)"},
     "source_refs": {"capex_per_m2": ["UBA_Gewaesserrenaturierung"]},
     "source_details": {
        "capex_per_m2": "Auenrenaturierung streut stark nach Intensität. Extensive "
            "Deichrückverlegung/Flächenrückgabe kostet ~0,3-3 €/m² (BfN/WWF-Projekt Mittlere "
            "Elbe: 6,5 Mio € auf 2.300 ha ≈ 2.826 €/ha ≈ 0,28 €/m²). Aktive/technische "
            "Renaturierung mit Erdbau und Strukturanreicherung liegt bei ~5-20 €/m² (UBA: "
            "kleine Maßnahmen ~10 €/lfm, technischer Umbau 600+ €/lfm Gewässerlauf). Punktwert "
            "12 €/m² für moderat-intensive Renaturierung mit Erdbau; die Anwendung auf reine "
            "Flächenrückgabe würde deutlich niedriger liegen.",
        "opex_per_m2_year": "Modellannahme: 0,50 €/m²/a für extensive Auenpflege "
            "(Gehölzkontrolle, Monitoring); renaturierte Auen sind weitgehend selbsterhaltend."}},
    # Herleitung capex_per_m2: Hecken kosten 15-55 €/lfm komplett gepflanzt, Windschutzhecken
    # 5-20 €/lfm (gartenbau-kosten/kostencheck 2026). Als €/m² über die geschützte Feldfläche
    # ist das eine Modell-Umlage (Hecken belegen nur Ränder, Terrassen sind teurer) → 10 €/m²
    # als Mischwert; Modellannahme, plausibilisiert anhand Heckenpreisen.
    {"code": "EROSION_PROTECTION", "name": "Erosionsschutz (Hecken, Terrassen)",
     "description": "Baulicher und vegetativer Erosionsschutz.", "measure_type": "structural",
     "effect_target": ["hazard"], "default_reduction": 0.25, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_SOIL_DEGRADATION"],
     "capex_fixed": 0.0, "capex_per_unit": None, "capex_per_m2": 10.0,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 0.5, "benefit_per_m2_year": 2.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "Modellannahme (Umlage Heckenpreise, gartenbau-kosten)",
     "sources": {"capex_per_m2": "Modell-Umlage Heckenpreise (gartenbau-kosten/kostencheck)",
                 "opex_per_m2_year": "Modellannahme (Heckenpflege/Terrassenerhalt)"},
     "source_refs": {"capex_per_m2": ["Gartenbau_Hecke"]},
     "source_details": {
        "capex_per_m2": "Erosionsschutz bündelt lineare Elemente (Hecken 15-55 €/lfm komplett, "
            "Windschutzhecken 5-20 €/lfm; gartenbau-kosten.de, kostencheck.de 2026) und "
            "flächige (Terrassierung, teurer). Ein €/m² über die geschützte Feldfläche ist "
            "eine Modell-Umlage, da Hecken nur Feldränder belegen. Punktwert 10 €/m² als "
            "Mischwert; für reinen Heckenschutz großer Flächen tendenziell zu hoch.",
        "opex_per_m2_year": "Modellannahme: 0,50 €/m²/a für Heckenschnitt und "
            "Erhalt der Erosionsschutzstrukturen."}},
    # Herleitung capex_per_m2/maintenance: Humusaufbau erfolgt v. a. über Zwischenfrüchte/
    # Begrünung; Saatgut 20-60 €/ha, Prämien bis 220 €/ha (KTBL/LfL; ÖPUL) ≈ 0,002-0,022 €/m².
    # Punktwerte auf 0,02 €/m² (Etablierung, ~200 €/ha) bzw. 0,02 €/m²/a (laufende Begrünung,
    # ~200 €/ha/a) angepasst — Alt-Katalogwerte (2 bzw. 0,3 €/m²) lagen ~2 Größenordnungen zu hoch.
    {"code": "HUMUS_BUILDUP", "name": "Humusaufbau",
     "description": "Aufbau organischen Bodenanteils.", "measure_type": "behavioral",
     "effect_target": ["vulnerability"], "default_reduction": 0.15, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_AGRICULTURAL_DAMAGE_EUR", "EXPECTED_SOIL_DEGRADATION"],
     "capex_fixed": 0.0, "capex_per_unit": None, "capex_per_m2": 0.02,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 0.02, "benefit_per_m2_year": 1.5,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "KTBL/LfL (Zwischenfrucht-/Begrünungskosten)",
     "sources": {"capex_per_m2": "KTBL/LfL Zwischenfruchtkosten (Saatgut/Etablierung)",
                 "opex_per_m2_year": "KTBL/LfL (laufende Begrünungskosten)"},
     "source_refs": {"capex_per_m2": ["LfL_Pflanzenbau"],
                     "opex_per_m2_year": ["LfL_Pflanzenbau"]},
     "source_details": {
        "capex_per_m2": "Humusaufbau erfolgt überwiegend über Zwischenfrüchte/Begrünung: "
            "Saatgut 20-60 €/ha, mit Prämien/anspruchsvollen Mischungen bis 220 €/ha (KTBL/"
            "LfL-Daten; ÖPUL) ≈ 0,002-0,022 €/m². Punktwert 0,02 €/m² (~200 €/ha) für die "
            "Etablierung, im oberen Bereich der belegten Spanne. Der frühere Katalogwert "
            "2 €/m² (=20.000 €/ha) lag rund zwei Größenordnungen darüber und wurde gesenkt.",
        "opex_per_m2_year": "Laufende Begrünungskosten ~20-220 €/ha/a (KTBL/LfL) "
            "≈ 0,002-0,022 €/m²/a → Punktwert 0,02 €/m²/a (~200 €/ha/a)."}},
    # Herleitung capex_per_m2: trockenresistente Sorten verursachen im Wesentlichen nur einen
    # Saatgut-Mehrpreis (Saatgut gesamt ~50-200 €/ha; KTBL ≈ 0,005-0,02 €/m²). Punktwerte auf
    # 0,02 €/m² bzw. 0,02 €/m²/a gesenkt (obere Grenze der Saatgutspanne) — Alt-Katalogwerte
    # (1 bzw. 0,2 €/m²) lagen weit über jedem realen Sortenaufpreis.
    {"code": "DROUGHT_RESISTANT_VARIETIES", "name": "Trockenresistente Sorten",
     "description": "Anbau klimaresilienter Kulturen.", "measure_type": "behavioral",
     "effect_target": ["vulnerability"], "default_reduction": 0.18, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_AGRICULTURAL_DAMAGE_EUR"],
     "capex_fixed": 0.0, "capex_per_unit": None, "capex_per_m2": 0.02,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 0.02, "benefit_per_m2_year": 1.5,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "KTBL (Saatgutkosten)",
     "sources": {"capex_per_m2": "KTBL Saatgutkosten (Sortenaufpreis)",
                 "opex_per_m2_year": "KTBL (jährlicher Saatgut-/Sortenaufpreis)"},
     "source_refs": {"capex_per_m2": ["LfL_Pflanzenbau"],
                     "opex_per_m2_year": ["LfL_Pflanzenbau"]},
     "source_details": {
        "capex_per_m2": "Der Wechsel auf trockenresistente Sorten verursacht im Kern nur einen "
            "Saatgut-Mehrpreis; das gesamte Saatgut liegt je nach Kultur bei ~50-200 €/ha "
            "(KTBL) ≈ 0,005-0,02 €/m², der Aufpreis nur ein Bruchteil davon. Punktwert "
            "0,02 €/m² an der oberen Grenze der Saatgutspanne. Der frühere Katalogwert 1 €/m² "
            "(=10.000 €/ha) überstieg jeden realen Sortenaufpreis um Faktor ~50-100 und wurde "
            "gesenkt.",
        "opex_per_m2_year": "Jährlicher Saatgut-/Sortenaufpreis wenige €/ha bis "
            "~200 €/ha (KTBL) → Punktwert 0,02 €/m²/a."}},
    # Herleitung capex_per_m2: KTBL-Richtwert für neue Bewässerungssysteme ~5.000 €/ha
    # (Tröpfchen am teuersten, 18 €/mm/ha; profi.de/Thünen). Punktwert 0,5 €/m² (=5.000 €/ha)
    # = KTBL-Bewässerungsrichtwert; ein zusätzlicher Speicheranteil würde ihn erhöhen. Alt-
    # Katalogwert 5 €/m² (=50.000 €/ha) lag ~Faktor 10 darüber und wurde gesenkt.
    {"code": "WATER_STORAGE_EFFICIENT_IRRIGATION", "name": "Wasserspeicher / effiziente Bewässerung",
     "description": "Speicherung und effiziente Bewässerung.", "measure_type": "structural",
     "effect_target": ["exposure"], "default_reduction": 0.22, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_AGRICULTURAL_DAMAGE_EUR"],
     "capex_fixed": 0.0, "capex_per_unit": None, "capex_per_m2": 0.5,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 0.2, "benefit_per_m2_year": 2.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "KTBL (Feldbewässerung)",
     "sources": {"capex_per_m2": "KTBL-Investitionsrichtwert Bewässerung (~5.000 €/ha)",
                 "opex_per_m2_year": "KTBL (Betriebskosten Bewässerung)"},
     "source_refs": {"capex_per_m2": ["KTBL_Feldbewaesserung"],
                     "opex_per_m2_year": ["KTBL_Feldbewaesserung"]},
     "source_details": {
        "capex_per_m2": "Als Faustwert für neue Bewässerungssysteme nennt das KTBL ~5.000 €/ha "
            "Investition (Tröpfchenbewässerung am teuersten, 18 €/mm·ha; profi.de/Thünen). "
            "Punktwert 0,5 €/m² (=5.000 €/ha) entspricht diesem Richtwert; ein zusätzlicher "
            "Wasserspeicher/Speicherteich würde ihn erhöhen (~1-1,5 €/m²). Der frühere "
            "Katalogwert 5 €/m² (=50.000 €/ha) lag um Faktor 10 darüber und wurde gesenkt.",
        "opex_per_m2_year": "KTBL-Betriebskosten (Energie, Auf-/Abbau der Tropfschläuche) "
            "~0,05-0,27 €/m²/a je nach Wassergabe → Punktwert 0,2 €/m²/a."}},
    # Herleitung capex_per_m2: Waldumbau/Wiederbewaldung kostet je nach Baumart und Zaun
    # 3.000-20.000 €/ha, mit Vollzaun/intensiver Pflege bis 30.000 €/ha (Landesforsten RLP:
    # Douglasie ~7.600 €/ha, Eiche/Buche >20.000 €/ha; Ø ~12.700 €/ha) ≈ 0,3-3 €/m². Punktwert
    # 1,5 €/m² (=15.000 €/ha) nahe dem Durchschnitt inkl. Zaun — Alt-Katalogwert 4 €/m²
    # (=40.000 €/ha) lag oberhalb selbst intensiver Fälle und wurde gesenkt.
    {"code": "MIXED_FORESTS", "name": "Mischwälder",
     "description": "Waldumbau zu Mischbeständen.", "measure_type": "planning",
     "effect_target": ["vulnerability"], "default_reduction": 0.25, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_VEGETATION_DAMAGE"],
     "capex_fixed": 0.0, "capex_per_unit": None, "capex_per_m2": 1.5,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 0.1, "benefit_per_m2_year": 1.5,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "Landesforsten / AGDW (Waldumbaukosten)",
     "sources": {"capex_per_m2": "Landesforsten RLP / AGDW (Waldumbau €/ha)",
                 "opex_per_m2_year": "Landesforsten (Kulturpflege/Freischneiden)"},
     "source_refs": {"capex_per_m2": ["AGDW_Wiederbewaldung"],
                     "opex_per_m2_year": ["AGDW_Wiederbewaldung"]},
     "source_details": {
        "capex_per_m2": "Waldumbau/Wiederbewaldung kostet je nach Baumart und Wildschutzzaun "
            "3.000-20.000 €/ha, mit Vollzaun und intensiver Pflege bis 30.000 €/ha "
            "(Landesforsten Rheinland-Pfalz: Douglasie/Lärche ~7.600 €/ha, Roteiche/Tanne "
            "~12.500 €/ha, Buche/Eiche >20.000 €/ha; Ø ~12.700 €/ha) — also ~0,3-3 €/m². "
            "Punktwert 1,5 €/m² (=15.000 €/ha) nahe dem Durchschnitt inkl. Wildschutz. Der "
            "frühere Katalogwert 4 €/m² (=40.000 €/ha) lag oberhalb selbst intensiver Fälle "
            "und wurde gesenkt.",
        "opex_per_m2_year": "Kulturpflege (Freischneiden ~500 €/ha je Gang, ~2 Gänge "
            "in den ersten Jahren; Landesforsten) → Punktwert 0,10 €/m²/a."}},
    # Herleitung capex_per_m2: präventive Waldbrandmaßnahmen (Wundstreifen/Riegel, Löschwasser-
    # entnahmestellen, Monitoring) sind überwiegend punktuell/linear und je Fläche günstig;
    # kein belastbarer Flächen-Kennwert auffindbar. Punktwert 1 €/m² als Modellannahme, für
    # großflächige Anwendung tendenziell zu hoch.
    {"code": "WILDFIRE_PREVENTION", "name": "Brandprävention",
     "description": "Präventive Waldbrandmaßnahmen.", "measure_type": "organizational",
     "effect_target": ["hazard"], "default_reduction": 0.25, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_VEGETATION_DAMAGE"],
     "capex_fixed": 0.0, "capex_per_unit": None, "capex_per_m2": 1.0,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 0.3, "benefit_per_m2_year": 1.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "Modellannahme (mangels belastbarer Quelle)",
     "sources": {"capex_per_m2": "Modellannahme (mangels belastbarer Flächen-Quelle)",
                 "opex_per_m2_year": "Modellannahme (Unterhalt Wundstreifen/Monitoring)"},
     "source_details": {
        "capex_per_m2": "Präventive Waldbrandmaßnahmen (Wundstreifen/Brandriegel, Löschwasser"
            "entnahmestellen, Waldbrand-Monitoring) sind überwiegend punktuell bzw. linear "
            "angelegt und je Waldfläche günstig; ein belastbarer flächenbezogener Kennwert "
            "war nicht auffindbar. Punktwert 1 €/m² als Modellannahme — bei großflächiger "
            "Anwendung eher zu hoch.",
        "opex_per_m2_year": "Modellannahme: 0,30 €/m²/a für den Unterhalt der "
            "Wundstreifen und das laufende Monitoring."}},
    # Herleitung capex_fixed: Praxisrichtwert Erstellung Hitzeschutz-/Hitzeaktionsplan
    # Mittelstadt (~80.000 EW): 80.000-150.000 € zzgl. halbe Personalstelle
    # (klimastadtraum.de, Kommunalberatung; UBA-Projekt "HAP-DE" und Fulda-Arbeitshilfe
    # nennen selbst keine Kostenzahlen) → Punktwert 100.000 € (unterer Mittelwert).
    {"code": "HEAT_ACTION_PLANS", "name": "Hitzeaktionspläne",
     "description": "Kommunale Hitzeaktionspläne.", "measure_type": "organizational",
     "effect_target": ["vulnerability"], "default_reduction": 0.20, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_ANNUAL_MORTALITY", "EXPECTED_ANNUAL_MORBIDITY"],
     "capex_fixed": 100000.0, "capex_per_unit": None, "capex_per_m2": None,
     "opex_fixed_year": 20000.0, "opex_per_unit_year": None, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "klimastadtraum.de (Praxisrichtwert) / Modellannahme",
     "sources": {"opex_fixed_year": "Modellannahme (laufende Fortschreibung/Koordination)",
                 "capex_fixed": "klimastadtraum.de (Praxisrichtwert Hitzeaktionsplan)"},
     "source_details": {
        "opex_fixed_year":
            "Modellannahme für den laufenden Betrieb des Hitzeaktionsplans: jährliche Fortschreibung, Koordination der Warnkette und saisonaler Betrieb (Hitzetelefon). Entspricht grob der anteiligen halben Personalstelle, die klimastadtraum.de bereits für die Erstellung nennt. Punktwert 20.000 €/a (rund 20 % der einmaligen Erstellungskosten); editierbar.",
        "capex_fixed": "Praxisrichtwert für die Erstellung eines kommunalen "
        "Hitzeschutz-/Hitzeaktionsplans einer Mittelstadt (~80.000 EW): 80.000–150.000 € "
        "zzgl. rund einer halben Personalstelle (klimastadtraum.de, Kommunalberatung). Die "
        "einschlägigen Leitfäden (UBA-Projekt \"HAP-DE\", Fulda-Arbeitshilfe) beschreiben die "
        "Planerstellung, nennen aber selbst keine Kostenzahlen. Punktwert 100.000 € als "
        "unterer Mittelwert der Spanne."}},
    # Herleitung capex_per_unit: keine belastbare Primärquelle für "Kühlraum"-Herrichtung
    # als Gesamtpaket auffindbar (Modellannahme); plausibilisiert anhand Marktpreisen
    # gewerblicher Split-Klimaanlagen 1.500-5.000 € Gerät+Einbau (ADAC/Heizcenter 2026)
    # zzgl. Ausstattung/Trinkwasserstation/Beschilderung ~2.000-3.000 € → Punktwert 8.000 €
    # (Modellannahme, mangels belastbarer Quelle für die Gesamtmaßnahme).
    {"code": "COOLING_ROOMS_DRINKING_WATER", "name": "Kühle Räume / Kühlzentren",
     "description": "Öffentliche Kühl- und Trinkwasserinfrastruktur.", "measure_type": "structural",
     "effect_target": ["exposure"], "default_reduction": 0.18, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_THERMAL_STRESS_HOURS", "EXPECTED_ANNUAL_MORTALITY"],
     "capex_fixed": 0.0, "capex_per_unit": 8000.0, "capex_per_m2": None,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": "Raum",
     # Herleitung unit_density_per_ha: Modellannahme (mangels belastbarer Quelle) — an
     # HAP-Konzept "kühle Orte" angelehnt: ein fußläufig (~800 m Radius, ~20 ha Einzugs-
     # gebiet) erreichbarer Kühlraum je Quartier → Punktwert 0,05 Räume/ha (1 je 20 ha).
     "unit_density_per_ha": 0.05,
     "source": "Modellannahme (mangels belastbarer Quelle)",
     "sources": {"capex_per_unit": "Modellannahme (Marktpreise Klimatechnik)",
                 "unit_density_per_ha": "Modellannahme (HAP-Konzept \"kühle Orte\")"},
     "source_details": {
        "capex_per_unit": "Keine belastbare Primärquelle für die Herrichtung eines "
            "\"Kühlraums\" als Gesamtpaket auffindbar – daher Modellannahme. Plausibilisiert "
            "anhand Marktpreisen gewerblicher Split-Klimaanlagen 1.500–5.000 € (Gerät + "
            "Einbau, ADAC/Heizcenter 2026) zzgl. Ausstattung, Trinkwasserstation und "
            "Beschilderung ~2.000–3.000 €. Punktwert 8.000 € je hergerichtetem Raum.",
        "unit_density_per_ha": "Modellannahme mangels belastbarer Quelle, angelehnt an das "
            "Konzept fußläufig erreichbarer \"kühler Orte\" aus kommunalen Hitzeaktionsplänen: "
            "ein in ~800 m Radius (~20 ha Einzugsgebiet) erreichbarer Kühlraum je Quartier "
            "→ 0,05 Räume/ha (1 je 20 ha)."}},
    # Herleitung capex_fixed: kommunales Starkregen-/Hochwasser-Frühwarnsystem — Machbarkeits-
    # studie ~5.000 €, Messnetzkonzept bis ~100.000 € (LEADER-gefördert), laufender Betrieb
    # 30.000-40.000 €/a (kommunal.de/Hydrotec 2025); Großprojekt Landkreis Fulda >800.000 €.
    # Punktwert 60.000 € für Aufbau eines mittleren Systems (Konzept + Basis-Sensorik).
    {"code": "EARLY_WARNING_MEASURE", "name": "Frühwarnsysteme (Maßnahme)",
     "description": "Ausbau von Frühwarnsystemen.", "measure_type": "organizational",
     "effect_target": ["vulnerability"], "default_reduction": 0.25, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_ANNUAL_AFFECTED_EVACUATED", "EXPECTED_ANNUAL_INJURIES"],
     "capex_fixed": 60000.0, "capex_per_unit": None, "capex_per_m2": None,
     "opex_fixed_year": 35000.0, "opex_per_unit_year": None, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "kommunale Praxiswerte Frühwarnsystem (kommunal.de / Hydrotec)",
     "sources": {"opex_fixed_year": "kommunale Praxiswerte (laufender Betrieb Frühwarnsystem)",
                 "capex_fixed": "kommunale Praxiswerte Starkregen-/Hochwasser-Frühwarnsystem"},
     "source_refs": {"capex_fixed": ["Kommunal_Fruehwarnsystem"],
                     "opex_fixed_year": ["Kommunal_Fruehwarnsystem"]},
     "source_details": {
        "opex_fixed_year":
            "Laufender Betrieb (Wartung, Hosting, Softwarepflege) eines kommunalen Starkregen-/Hochwasser-Frühwarnsystems: 30.000–40.000 €/a (kommunal.de, Hydrotec 2025). Punktwert 35.000 €/a. Diese Betriebskosten waren im früheren Modell nicht abbildbar und sind jetzt als feste jährliche OPEX hinterlegt.",
        "capex_fixed": "Kommunales Starkregen-/Hochwasser-Frühwarnsystem: Machbarkeitsstudie "
            "~5.000 €, Messnetzkonzept bis ~100.000 € (LEADER-gefördert), laufender Betrieb "
            "(Wartung/Hosting/Entwicklung) 30.000-40.000 €/a (kommunal.de, Hydrotec 2025); als "
            "Großprojekt wurde das System im Landkreis Fulda mit >800.000 € gefördert. Punktwert "
            "60.000 € für den einmaligen Aufbau eines mittleren Systems (Konzept + Basis-"
            "Sensorik/Pegel); die jährlichen Betriebskosten sind separat unter opex_fixed_year "
            "abgebildet."}},
    # Herleitung capex_per_m2/opex_per_m2_year: kein einheitlicher Kennwert für
    # "Ausbau Stadtgrün" als Sammelmaßnahme auffindbar (Modellannahme, mangels belastbarer
    # Quelle) — Plausibilisierung anhand Institut für Stadtgrün/Fachsymposium 2013
    # (Unterhaltung 0,65-85 €/m²/a je nach Pflegeintensität: Rasen bis Wechselflor) und
    # Berliner Stadtbaumkampagne (~3.000 €/Baum inkl. 3 Jahre Pflege); 25 €/m² Investition
    # bzw. 3 €/m² Unterhalt liegen im plausiblen Bereich für Grünfläche mittlerer Dichte
    # (Baumbestand + Rasen/Strauchflächen, keine intensive Zierbepflanzung).
    {"code": "URBAN_GREEN", "name": "Stadtgrün",
     "description": "Ausbau städtischer Grünflächen.", "measure_type": "planning",
     "effect_target": ["hazard"], "default_reduction": 0.25, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_THERMAL_STRESS_HOURS"],
     "capex_fixed": 0.0, "capex_per_unit": None, "capex_per_m2": 25.0,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 3.0, "benefit_per_m2_year": 5.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "Modellannahme (mangels belastbarer Quelle für Sammelmaßnahme)",
     "sources": {"capex_per_m2": "Modellannahme (Institut für Stadtgrün / Berliner Stadtbaumkampagne)",
                 "opex_per_m2_year": "Institut für Stadtgrün (Semmler 2013)"},
     "source_refs": {"opex_per_m2_year": ["Semmler_Stadtgruen_2013"]},
     "source_details": {
        "capex_per_m2": "Kein einheitlicher €/m²-Kennwert für \"Ausbau Stadtgrün\" als "
            "Sammelmaßnahme auffindbar – daher Modellannahme. Plausibilisiert anhand Institut "
            "für Stadtgrün (Semmler, Fachsymposium 2013, Unterhaltung 0,65–85 €/m²/a je nach "
            "Pflegeintensität) und Berliner Stadtbaumkampagne (~3.000 €/Baum inkl. 3 Jahre "
            "Anwuchspflege). 25 €/m² Investition liegt im plausiblen Bereich für Grünfläche "
            "mittlerer Dichte (Baumbestand + Rasen/Strauchflächen, keine intensive "
            "Zierbepflanzung).",
        "opex_per_m2_year": "Modellannahme, plausibilisiert anhand Institut für "
            "Stadtgrün (Semmler 2013): Unterhaltung 0,65–85 €/m²/a je nach Pflegeintensität "
            "(extensiver Rasen bis Wechselflor). 3 €/m²/a entspricht mäßig intensiver Pflege "
            "einer Grünfläche mittlerer Dichte."}},
    # Herleitung capex_fixed: Erstellung kommunaler Evakuierungs-/Notfallpläne — der BBK
    # (Bundesamt für Bevölkerungsschutz und Katastrophenhilfe) liefert Rahmenempfehlungen/
    # Leitfäden, aber keine Kostenkennwerte. Modellannahme als einmaliges Planungs-/
    # Konzeptbudget (Analyse, Planwerk, Übungen) → 40.000 €.
    {"code": "EVACUATION_EMERGENCY_PLANS", "name": "Evakuierungs- & Notfallpläne",
     "description": "Bevölkerungsschutzpläne.", "measure_type": "organizational",
     "effect_target": ["vulnerability"], "default_reduction": 0.22, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_ANNUAL_AFFECTED_EVACUATED"],
     "capex_fixed": 40000.0, "capex_per_unit": None, "capex_per_m2": None,
     "opex_fixed_year": 8000.0, "opex_per_unit_year": None, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "BBK (Leitfäden, ohne Kostenkennwert) / Modellannahme",
     "sources": {"opex_fixed_year": "Modellannahme (Übungen/Aktualisierung)",
                 "capex_fixed": "Modellannahme (Planungsbudget; BBK-Leitfäden ohne Kostenangabe)"},
     "source_details": {
        "opex_fixed_year":
            "Modellannahme für den laufenden Unterhalt der Evakuierungs- und Notfallpläne: regelmäßige Übungen, Aktualisierung des Planwerks und Schulungen. Grob 20 % der einmaligen Erstellung → 8.000 €/a. BBK-Leitfäden nennen keine Kostenkennwerte; editierbar.",
        "capex_fixed": "Erstellung kommunaler Evakuierungs- und Notfallpläne. Der BBK (Bundesamt "
            "für Bevölkerungsschutz und Katastrophenhilfe) stellt Rahmenempfehlungen und "
            "Leitfäden bereit, nennt aber keine Kostenkennwerte. Modellannahme als einmaliges "
            "Planungs-/Konzeptbudget (Gefährdungsanalyse, Planwerk, Übungen) → 40.000 €. Für "
            "organisatorische Maßnahmen der erwartete, ehrliche Regelfall."}},
    # Herleitung: rein planungsrechtliche Maßnahme (Bauverbot/Rückhaltung in Gefahrenzonen über
    # Bauleitplanung); direkte Umsetzungskosten ≈ 0 €/m² (0,0 = anwendbar, aber kostenlos —
    # nicht "unbelegt"). Etwaige Entschädigungs-/Opportunitätskosten sind hier nicht abgebildet.
    {"code": "BUILDING_BANS_RISK_ZONES", "name": "Bauverbote in Risikozonen",
     "description": "Siedlungsrückhaltung in Gefahrenzonen.", "measure_type": "planning",
     "effect_target": ["exposure"], "default_reduction": 0.30, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_BUILDING_DAMAGE_EUR", "EXPECTED_ANNUAL_AFFECTED_EVACUATED"],
     "capex_fixed": 0.0, "capex_per_unit": None, "capex_per_m2": 0.0,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 0.0, "benefit_per_m2_year": 0.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "Planungsrechtliche Maßnahme (direkt kostenneutral)",
     "sources": {"capex_per_m2": "Planungsrechtlich – direkte Umsetzungskosten ≈ 0",
                 "opex_per_m2_year": "Planungsrechtlich – kein laufender Unterhalt"},
     "source_details": {
        "capex_per_m2": "Rein planungsrechtliche Maßnahme (Bauverbot bzw. Siedlungsrückhaltung "
            "in Gefahrenzonen über die Bauleitplanung). Die direkten Umsetzungskosten sind "
            "≈ 0 €/m² (der Wert 0,0 bedeutet \"anwendbar, aber kostenlos\", nicht \"unbelegt\"). "
            "Etwaige Entschädigungs- oder Opportunitätskosten unbebauter Flächen sind im Modell "
            "bewusst nicht abgebildet.",
        "opex_per_m2_year": "Planungsrechtliche Festsetzung ohne laufenden Unterhalt "
            "→ 0 €/m²/a."}},
    # Herleitung capex_per_m2: Freihaltung von Frischluftkorridoren ist überwiegend Planung/
    # Flächensicherung (Bebauungsverzicht, gelegentliche Gehölzpflege) ohne baulichen Aufwand;
    # kein Marktkennwert. Punktwert 2 €/m² als niedrige Modellannahme (Planungs-/Pflegeanteil).
    {"code": "FRESH_AIR_CORRIDORS", "name": "Frischluftschneisen",
     "description": "Freihaltung von Frischluftkorridoren.", "measure_type": "planning",
     "effect_target": ["hazard"], "default_reduction": 0.20, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_THERMAL_STRESS_HOURS"],
     "capex_fixed": 0.0, "capex_per_unit": None, "capex_per_m2": 2.0,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 0.5, "benefit_per_m2_year": 2.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "Modellannahme (Planungs-/Flächensicherung)",
     "sources": {"capex_per_m2": "Modellannahme (Planung/Flächensicherung, mangels Marktkennwert)",
                 "opex_per_m2_year": "Modellannahme (gelegentliche Gehölzpflege)"},
     "source_details": {
        "capex_per_m2": "Die Freihaltung von Frischluftkorridoren ist überwiegend Planung und "
            "Flächensicherung (Bebauungsverzicht, gelegentliche Gehölz-/Freihaltepflege) ohne "
            "baulichen Aufwand; ein Marktkennwert existiert nicht. Punktwert 2 €/m² als "
            "niedrige Modellannahme (Planungs- und geringer Pflegeanteil).",
        "opex_per_m2_year": "Modellannahme: 0,50 €/m²/a für gelegentliche Freihalte-/"
            "Gehölzpflege der Korridore."}},
    # Herleitung capex_per_m2: Schwammstadt ist ein Bündel (Entsiegelung 25-40 €/m² + Mulden-
    # Rigolen 60-85 €/m² + Baumrigolen/Retention), kein einzelner Kennwert. Plausibilisiert
    # als Mischwert im unteren Bereich der Kombinationsmaßnahmen (Hamburg RISA, DWA-A 138)
    # → Punktwert 40 €/m². Modellannahme für die Sammelmaßnahme.
    {"code": "SPONGE_CITY", "name": "Entsiegelung / Schwammstadt",
     "description": "Schwammstadt-Konzepte.", "measure_type": "planning",
     "effect_target": ["hazard"], "default_reduction": 0.30, "coverage_scaling": "linear",
     "linked_risk_codes": ["HYDROLOGICAL_STRESS_RISK_INDEX", "EXPECTED_BUILDING_DAMAGE_EUR"],
     "capex_fixed": 0.0, "capex_per_unit": None, "capex_per_m2": 40.0,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 2.0, "benefit_per_m2_year": 5.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "Modellannahme (Schwammstadt-Bündel), plausibilisiert anhand RISA / DWA-A 138",
     "sources": {"capex_per_m2": "Modellannahme, plausibilisiert anhand Entsiegelung + Mulden-Rigolen (RISA/DWA-A 138)",
                 "opex_per_m2_year": "Modellannahme (Pflege der blau-grünen Elemente)"},
     "source_details": {
        "capex_per_m2": "Die Schwammstadt ist kein Einzelbauteil, sondern ein Bündel aus "
            "Entsiegelung (25-40 €/m²), Mulden-Rigolen (60-85 €/m²), Baumrigolen und "
            "dezentraler Retention. Ein sauberer Einzelkennwert existiert nicht; der Wert ist "
            "als Mischwert im unteren Bereich der Kombinationsmaßnahmen plausibilisiert "
            "(Hamburg RISA – Regeninfrastrukturanpassung; DWA-A 138) → Punktwert 40 €/m². "
            "Modellannahme für die Sammelmaßnahme.",
        "opex_per_m2_year": "Modellannahme: 2 €/m²/a für die Pflege der blau-grünen "
            "Elemente (Mahd, Entschlammung, Vegetationskontrolle), analog Mulden-Rigolen."}},
    # Herleitung capex_per_m2: offene Retentionsflächen/Erdbecken kosten ~26-50 €/m³ nutzbaren
    # Rückhalts (Praxisbeispiele, agrarheute/Sieker 2026); bei flacher Bauweise (~1 m Tiefe)
    # entspricht das grob €/m² → Punktwert 30 €/m². opex_per_m2_year: Unterhalt offener
    # Erd-/Betonbecken ~0,50 €/m²/a (Sieker); Katalogwert 1,0 €/m²/a mit Puffer für Mahd/
    # Entschlammung.
    {"code": "RETENTION_STORAGE", "name": "Retentionsflächen / Speicher",
     "description": "Oberirdische Retention und Speicher.", "measure_type": "structural",
     "effect_target": ["hazard"], "default_reduction": 0.28, "coverage_scaling": "linear",
     "linked_risk_codes": ["HYDROLOGICAL_STRESS_RISK_INDEX"],
     "capex_fixed": 0.0, "capex_per_unit": None, "capex_per_m2": 30.0,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 1.0, "benefit_per_m2_year": 4.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "Praxiswerte Regenrückhaltebecken (Sieker / agrarheute)",
     "sources": {"capex_per_m2": "Praxiswerte offene Retentionsbecken (Sieker/agrarheute), auf Fläche umgerechnet",
                 "opex_per_m2_year": "Sieker (Unterhalt offener Becken), mit Puffer"},
     "source_refs": {"capex_per_m2": ["Agrarheute_Rueckhaltebecken"],
                     "opex_per_m2_year": ["Agrarheute_Rueckhaltebecken"]},
     "source_details": {
        "capex_per_m2": "Offene Retentionsflächen/Erdbecken kosten ~26-50 €/m³ nutzbaren "
            "Rückhaltevolumens (Praxisbeispiele 2005/2008 ~26-50 €/m³; agrarheute, Sieker "
            "2026; geschlossene Bauweise 230-370 €/m³ hier ausgeklammert). Bei flacher, "
            "offener Bauweise (~1 m Wassertiefe) entspricht 1 m³ ≈ 1 m² Fläche → Punktwert "
            "30 €/m².",
        "opex_per_m2_year": "Unterhalt offener Erd-/Betonbecken ~0,50 €/m²/a (Sieker). "
            "Katalogwert 1,0 €/m²/a mit Puffer für Mahd, Entschlammung und Auslaufkontrolle."}},
    # Herleitung capex_per_m2: großflächige, offene Polder/Hochwasserrückhaltung liegen am
    # unteren Ende der Retentionskostenspanne (viel Fläche, wenig Bauwerk) → Punktwert 25 €/m²,
    # abgeleitet aus den Regenrückhaltebecken-Praxiswerten (Sieker/agrarheute 2026).
    {"code": "RETENTION_POLDER_RESERVOIR", "name": "Retention / Polder / Rückhaltebecken",
     "description": "Großflächige Hochwasserretention.", "measure_type": "structural",
     "effect_target": ["hazard"], "default_reduction": 0.30, "coverage_scaling": "linear",
     "linked_risk_codes": ["HYDROLOGICAL_STRESS_RISK_INDEX", "EXPECTED_BUILDING_DAMAGE_EUR"],
     "capex_fixed": 0.0, "capex_per_unit": None, "capex_per_m2": 25.0,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 1.0, "benefit_per_m2_year": 4.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "Praxiswerte Rückhaltebecken (Sieker / agrarheute)",
     "sources": {"capex_per_m2": "Praxiswerte offene Polder/Rückhaltebecken (Sieker/agrarheute)",
                 "opex_per_m2_year": "Sieker (Unterhalt offener Becken)"},
     "source_refs": {"capex_per_m2": ["Agrarheute_Rueckhaltebecken"],
                     "opex_per_m2_year": ["Agrarheute_Rueckhaltebecken"]},
     "source_details": {
        "capex_per_m2": "Großflächige, offene Polder und Hochwasserrückhaltebecken liegen am "
            "unteren Ende der Retentionskostenspanne (überwiegend Erdbau/Fläche, wenig "
            "Bauwerk): Praxiswerte offener Becken ~26-50 €/m³ (Sieker, agrarheute 2026), bei "
            "flacher Ausformung → Punktwert 25 €/m².",
        "opex_per_m2_year": "Unterhalt offener Rückhaltebecken ~0,50-1,0 €/m²/a (Sieker) "
            "für Mahd der Böschungen und Kontrolle der Auslassbauwerke → 1,0 €/m²/a."}},
    # Herleitung capex_per_m2: Flächen-/Muldenversickerung 10-45 €/m² abflusswirksamer Fläche
    # (DWA-A 138; baupreislexikon 2026) → Punktwert 30 €/m² im mittleren Bereich.
    {"code": "INFILTRATION_AREAS", "name": "Versickerungsflächen",
     "description": "Flächenversickerung.", "measure_type": "structural",
     "effect_target": ["exposure"], "default_reduction": 0.25, "coverage_scaling": "linear",
     "linked_risk_codes": ["HYDROLOGICAL_STRESS_RISK_INDEX"],
     "capex_fixed": 0.0, "capex_per_unit": None, "capex_per_m2": 30.0,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 1.0, "benefit_per_m2_year": 3.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "DWA-A 138 / baupreislexikon (Flächenversickerung)",
     "sources": {"capex_per_m2": "DWA-A 138 / baupreislexikon (Mulden-/Flächenversickerung)",
                 "opex_per_m2_year": "DWA-A 138 (Betrieb), auf Anlagenfläche umgerechnet"},
     "source_refs": {"capex_per_m2": ["DWA_A138", "Baupreislexikon_Versickerung"],
                     "opex_per_m2_year": ["DWA_A138", "Baupreislexikon_Versickerung"]},
     "source_details": {
        "capex_per_m2": "Flächen- und Muldenversickerung kosten nach DWA-A 138 (baupreislexikon "
            "2026) 10-45 €/m² abflusswirksamer Fläche. Punktwert 30 €/m² im mittleren Bereich "
            "(einfache Sickermulde mit Oberbodenzone).",
        "opex_per_m2_year": "DWA-Betriebskennwert 0,50-0,75 €/m² abflusswirksamer "
            "Fläche; bezogen auf die Sickerfläche selbst → 1 €/m²/a (Mahd, Belüftung, "
            "Kontrolle der Sickerleistung)."}},
    # Herleitung capex_per_m2: DGM-basierte Abflusslenkung ist überwiegend Planung/geringfügige
    # Geländemodellierung (Bordsteine, Mulden, Wege als Notwasserwege) ohne einheitlichen
    # Baukennwert → Punktwert 8 €/m² als niedrige Modellannahme. Mangels belastbarer Quelle.
    {"code": "RUNOFF_ROUTING_DGM", "name": "Abflusslenkung (DGM-basiert)",
     "description": "Geländebasierte Abflusslenkung.", "measure_type": "planning",
     "effect_target": ["hazard"], "default_reduction": 0.20, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_BUILDING_DAMAGE_EUR"],
     "capex_fixed": 0.0, "capex_per_unit": None, "capex_per_m2": 8.0,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 0.5, "benefit_per_m2_year": 2.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "Modellannahme (mangels belastbarer Quelle)",
     "sources": {"capex_per_m2": "Modellannahme (mangels belastbarer Quelle)",
                 "opex_per_m2_year": "Modellannahme (mangels belastbarer Quelle)"},
     "source_details": {
        "capex_per_m2": "DGM-basierte Abflusslenkung ist überwiegend Planung und geringfügige "
            "Geländemodellierung (Bordsteinführung, flache Notwasserwege), für die kein "
            "einheitlicher Bau-Flächenkennwert vorliegt. 8 €/m² als niedrige Modellannahme "
            "(planungsdominiert), mangels belastbarer Quelle.",
        "opex_per_m2_year": "Modellannahme: 0,50 €/m²/a geringer Unterhalt der "
            "Geländeführung."}},
    # Herleitung capex_per_m2: künstliche Grundwasseranreicherung (Sickerbecken/-gräben) ohne
    # einheitlichen €/m²-Kennwert; an der unteren Versickerungskostenspanne (DWA-A 138)
    # orientiert → Punktwert 10 €/m². Überwiegend Modellannahme.
    {"code": "GROUNDWATER_RECHARGE", "name": "Grundwasseranreicherung",
     "description": "Künstliche Grundwasseranreicherung.", "measure_type": "structural",
     "effect_target": ["hazard"], "default_reduction": 0.20, "coverage_scaling": "linear",
     "linked_risk_codes": ["HYDROLOGICAL_STRESS_RISK_INDEX", "EXPECTED_WATER_SUPPLY_OUTAGE_HOURS"],
     "capex_fixed": 0.0, "capex_per_unit": None, "capex_per_m2": 10.0,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 0.5, "benefit_per_m2_year": 2.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "Modellannahme, an DWA-A 138 (Versickerung) orientiert",
     "sources": {"capex_per_m2": "Modellannahme, untere Versickerungskostenspanne (DWA-A 138)",
                 "opex_per_m2_year": "Modellannahme (mangels belastbarer Quelle)"},
     "source_details": {
        "capex_per_m2": "Für künstliche Grundwasseranreicherung (großflächige Sickerbecken/"
            "-gräben) liegt kein einheitlicher €/m²-Kennwert vor. Der Wert orientiert sich am "
            "unteren Ende der Versickerungskostenspanne nach DWA-A 138 (extensive, offene "
            "Sickerflächen) → Punktwert 10 €/m². Überwiegend Modellannahme.",
        "opex_per_m2_year": "Modellannahme: 0,50 €/m²/a für Erhalt der Sickerleistung "
            "(Belüftung/Kontrolle)."}},
    # Herleitung capex_per_unit: Rohrnetzsanierung offene Bauweise 80-150 €/lfm, grabenlose
    # Inliner-Verfahren (CIPP) 50-90 €/lfm (DVGW W 392 / energie|wasser-praxis). Ein
    # "Abschnitt" ≈ 1 km Leitung → 50-150 T€; Punktwert 90.000 € (Mittel, gemischtes Verfahren).
    {"code": "LEAKAGE_REDUCTION", "name": "Leckage-Reduktion",
     "description": "Reduktion von Wasserverlusten im Netz.", "measure_type": "structural",
     "effect_target": ["vulnerability"], "default_reduction": 0.22, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_WATER_SUPPLY_OUTAGE_HOURS"],
     "capex_fixed": 0.0, "capex_per_unit": 90000.0, "capex_per_m2": None,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": "Abschnitt",
     # Herleitung unit_density_per_ha: Modellannahme (Richtwert-Dichte) — sanierungs-
     # bedürftige Netzabschnitte je Fläche, ~1 Abschnitt (≈1 km) je 33 ha Siedlungsfläche.
     "unit_density_per_ha": 0.03,
     "source": "DVGW W 392 / energie|wasser-praxis (Netzsanierung)",
     "sources": {"capex_per_unit": "DVGW W 392 / energie|wasser-praxis (Rohrnetzsanierung €/lfm)",
                 "unit_density_per_ha": "Modellannahme (Richtwert-Dichte, unbelegt)"},
     "source_refs": {"capex_per_unit": ["DVGW_W392"]},
     "source_details": {
        "capex_per_unit": "Rohrnetzsanierung kostet in offener Bauweise (Rohrersatz) 80-150 "
            "€/lfm, im grabenlosen Inliner-Verfahren (CIPP) 50-90 €/lfm (DVGW W 392; "
            "energie|wasser-praxis 2019). Ein Sanierungs-\"Abschnitt\" entspricht rund 1 km "
            "Leitung → 50.000-150.000 €; Punktwert 90.000 € als Mittel eines gemischten "
            "Verfahrensmixes.",
        "unit_density_per_ha": "Modellannahme mangels belastbarer Quelle: rund ein sanierungs"
            "bedürftiger Netzabschnitt (≈1 km) je 33 ha Siedlungsfläche (0,03 Abschnitte/ha)."}},
    # Herleitung capex_per_unit: umfassende Deichsanierung/-verstärkung kostet nach Praxis-
    # projekten ~1,25-2,1 Mio €/km an Flussdeichen (Sachsen-Anhalt/Hessen 2024-2026,
    # volksstimme/rp-darmstadt) und ~4 Mio €/km an See-/Küstendeichen (NLWKN Generalplan
    # Küstenschutz: ~500 Mio € für ~125 km). Punktwert 1.250.000 €/km = konservativer unterer
    # Rand der belegten Flussdeich-Spanne (Alt-Katalogwert 300.000 €/km war Faktor 4-13 zu
    # niedrig und wurde angehoben).
    {"code": "LEVEE_REINFORCEMENT", "name": "Deichverstärkung / Barrieren",
     "description": "Küstenschutz und Deichbau.", "measure_type": "structural",
     "effect_target": ["hazard"], "default_reduction": 0.35, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_BUILDING_DAMAGE_EUR"],
     "capex_fixed": 0.0, "capex_per_unit": 1250000.0, "capex_per_m2": None,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": "km", "unit_density_per_ha": 0.01,
     "source": "NLWKN Generalplan Küstenschutz / Landesbetriebe (Deichsanierung)",
     "sources": {"capex_per_unit": "Praxisprojekte Flussdeich + NLWKN Generalplan Küstenschutz",
                 "unit_density_per_ha": "Modellannahme (Richtwert-Dichte, unbelegt)"},
     "source_refs": {"capex_per_unit": ["NLWKN_Generalplan_Kuestenschutz"]},
     "source_details": {
        "capex_per_unit": "Umfassende Deichsanierung/-verstärkung kostet nach Praxisprojekten "
            "~1,25-2,1 Mio €/km an Flussdeichen (Sachsen-Anhalt/Hessen 2024-2026: 3 Mio € für "
            "1,7 km, 1,5 Mio € für 0,7 km; volksstimme.de, rp-darmstadt.hessen.de) und ~4 Mio "
            "€/km an See-/Küstendeichen (NLWKN Generalplan Küstenschutz: ~500 Mio € für ~125 "
            "km Festlandküste). Punktwert 1.250.000 €/km als konservativer unterer Rand der "
            "Flussdeich-Spanne; für reine See-/Küstendeiche eher ~4 Mio €/km ansetzen. Der "
            "frühere Katalogwert 300.000 €/km lag um Faktor 4-13 darunter und wurde angehoben.",
        "unit_density_per_ha": "Modellannahme mangels belastbarer Quelle: ~0,01 km "
            "Schutzlinie je ha geschützter Fläche (1 km Deich schützt grob 100 ha Hinterland)."}},
    # Herleitung capex_per_unit: keine belastbare Einzelquelle für "Salzwasserbarriere" als
    # Standardanlage — Modellannahme. Kleine lokale Bauwerke gegen Salzwasserintrusion
    # (Sohlschwellen, Regelungswehre) liegen im niedrigen sechsstelligen Bereich, große
    # Sturmflutsperrwerke (z. B. Emssperrwerk) dagegen im dreistelligen Mio-Bereich und sind
    # hier NICHT gemeint. Punktwert 150.000 €/Anlage als lokale Kleinbarriere.
    {"code": "SALTWATER_BARRIERS", "name": "Salzwasserbarrieren",
     "description": "Barrieren gegen Salzwasserintrusion.", "measure_type": "structural",
     "effect_target": ["exposure"], "default_reduction": 0.25, "coverage_scaling": "saturating",
     "linked_risk_codes": ["HYDROLOGICAL_STRESS_RISK_INDEX"],
     "capex_fixed": 0.0, "capex_per_unit": 150000.0, "capex_per_m2": None,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": "Anlage", "unit_density_per_ha": 0.002,
     "source": "Modellannahme (mangels belastbarer Quelle)",
     "sources": {"capex_per_unit": "Modellannahme (lokale Kleinbarriere, mangels belastbarer Quelle)",
                 "unit_density_per_ha": "Modellannahme (Richtwert-Dichte, unbelegt)"},
     "source_details": {
        "capex_per_unit": "Keine belastbare Einzelquelle für eine \"Salzwasserbarriere\" als "
            "Standardanlage auffindbar – daher Modellannahme. Der Wert steht für lokale "
            "Kleinbauwerke gegen Salzwasserintrusion (Sohlschwellen, Regelungswehre) im "
            "niedrigen sechsstelligen Bereich. Große Sturmflutsperrwerke (z. B. Emssperrwerk, "
            "dreistelliger Mio-Bereich) sind hier ausdrücklich NICHT gemeint. Punktwert "
            "150.000 €/Anlage.",
        "unit_density_per_ha": "Modellannahme mangels belastbarer Quelle: ~1 Barriere je 500 "
            "ha exponierter Küsten-/Ästuarfläche (0,002 Anlagen/ha)."}},
    # Herleitung capex_fixed: organisatorisch-finanzielle Maßnahme (Risikoanalyse, Priorisierung
    # von Investitionsbudgets) ohne baulichen Anteil; kein Marktkennwert. Modellannahme in
    # Höhe eines Beratungs-/Konzeptbudgets → 30.000 €.
    {"code": "RISK_BASED_INVESTMENTS", "name": "Risikobasierte Investitionen",
     "description": "Finanzielle Steuerung nach Risiko.", "measure_type": "organizational",
     "effect_target": ["vulnerability"], "default_reduction": 0.15, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_TOTAL_DAMAGE_EAD_EUR"],
     "capex_fixed": 30000.0, "capex_per_unit": None, "capex_per_m2": None,
     "opex_fixed_year": 5000.0, "opex_per_unit_year": None, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "Modellannahme (Konzept-/Beratungsbudget)",
     "sources": {"opex_fixed_year": "Modellannahme (laufendes Controlling/Review)",
                 "capex_fixed": "Modellannahme (Beratungs-/Konzeptbudget, mangels Marktkennwert)"},
     "source_details": {
        "opex_fixed_year":
            "Modellannahme für die laufende Pflege der risikobasierten Investitionspriorisierung: jährliches Review und Controlling der Priorisierungsgrundlage. Punktwert 5.000 €/a. Rein organisatorisch, kein belastbarer Kostenkennwert; editierbar.",
        "capex_fixed": "Organisatorisch-finanzielle Maßnahme (Risikoanalyse, risikobasierte "
            "Priorisierung von Investitionsbudgets) ohne baulichen Anteil; hierfür existiert "
            "kein Marktkennwert. Modellannahme in Höhe eines einmaligen Beratungs-/Konzept"
            "budgets → 30.000 €. Für organisatorische Maßnahmen ist das der erwartete, "
            "ehrliche Regelfall."}},
    # Herleitung capex_fixed: Anreizprogramm (z. B. Förderung/Prämien für private Vorsorge);
    # kein einheitlicher Kennwert. Modellannahme in Höhe eines Programm-Aufsetzbudgets → 25.000 €.
    {"code": "PREVENTION_INCENTIVES", "name": "Präventionsanreize",
     "description": "Anreize für präventive Maßnahmen.", "measure_type": "organizational",
     "effect_target": ["exposure"], "default_reduction": 0.12, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_TOTAL_DAMAGE_EAD_EUR"],
     "capex_fixed": 25000.0, "capex_per_unit": None, "capex_per_m2": None,
     "opex_fixed_year": 6000.0, "opex_per_unit_year": None, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "Modellannahme (Programm-Aufsetzbudget)",
     "sources": {"opex_fixed_year": "Modellannahme (Programmverwaltung)",
                 "capex_fixed": "Modellannahme (Aufsetzen eines Anreiz-/Förderprogramms)"},
     "source_details": {
        "opex_fixed_year":
            "Modellannahme für die laufende Verwaltung des Präventions-Anreizprogramms (Antrags- und Auszahlungsbearbeitung, Öffentlichkeitsarbeit), ohne die ausgezahlten Fördermittel selbst. Punktwert 6.000 €/a; kein belastbarer Kostenkennwert; editierbar.",
        "capex_fixed": "Anreizprogramm (Förderung/Prämien für private Vorsorge); der reine "
            "Programm-Overhead (Konzeption, Verwaltung) ist gemeint, nicht die ausgezahlten "
            "Fördermittel. Kein einheitlicher Kennwert verfügbar → Modellannahme 25.000 € als "
            "Aufsetzbudget. Erwarteter, ehrlicher Regelfall für organisatorische Maßnahmen."}},
    # Herleitung capex_per_unit: betriebliche Kühlkonzepte (Prozess-/Gebäudekühlung in Industrie/
    # Gewerbe) sind stark anlagenspezifisch; keine belastbare Standard-Quelle. Modellannahme in
    # sechsstelliger Größenordnung je Anlage → 70.000 €.
    {"code": "INDUSTRIAL_COOLING_CONCEPTS", "name": "Kühlkonzepte (Industrie/Gewerbe)",
     "description": "Betriebliche Kühlkonzepte.", "measure_type": "structural",
     "effect_target": ["hazard"], "default_reduction": 0.18, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_INDIRECT_ECONOMIC_LOSS_EUR"],
     "capex_fixed": 0.0, "capex_per_unit": 70000.0, "capex_per_m2": None,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": "Anlage", "unit_density_per_ha": 0.02,
     "source": "Modellannahme (mangels belastbarer Quelle)",
     "sources": {"capex_per_unit": "Modellannahme (anlagenspezifisch, mangels Standard-Quelle)",
                 "unit_density_per_ha": "Modellannahme (Richtwert-Dichte, unbelegt)"},
     "source_details": {
        "capex_per_unit": "Betriebliche Kühlkonzepte (Prozess- und Gebäudekühlung in Industrie/"
            "Gewerbe) sind stark anlagen- und branchenspezifisch; eine belastbare Standard"
            "quelle war nicht auffindbar. Modellannahme in sechsstelliger Größenordnung je "
            "ertüchtigter Anlage → 70.000 €.",
        "unit_density_per_ha": "Modellannahme mangels belastbarer Quelle: ~1 kühlrelevante "
            "Anlage je 50 ha Industrie-/Gewerbefläche (0,02 Anlagen/ha)."}},
    # Herleitung capex_fixed: Lieferketten-Resilienz (Zweitlieferanten, Lager-/Redundanzkonzepte,
    # Notfallplanung) ist organisatorisch; kein Marktkennwert. Modellannahme als Konzept-/
    # Aufbaubudget → 40.000 €. Organisatorische Maßnahme: Modellannahme ist erwarteter Regelfall.
    {"code": "SUPPLY_CHAIN_RESILIENCE", "name": "Lieferketten-Resilienz",
     "description": "Resilienz in Lieferketten.", "measure_type": "organizational",
     "effect_target": ["vulnerability"], "default_reduction": 0.20, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_SUPPLY_CHAIN_DISRUPTION_HOURS"],
     "capex_fixed": 40000.0, "capex_per_unit": None, "capex_per_m2": None,
     "opex_fixed_year": 8000.0, "opex_per_unit_year": None, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "Modellannahme (Konzept-/Aufbaubudget)",
     "sources": {"opex_fixed_year": "Modellannahme (laufendes Monitoring)",
                 "capex_fixed": "Modellannahme (organisatorisch, mangels Marktkennwert)"},
     "source_details": {
        "opex_fixed_year":
            "Modellannahme für das laufende Monitoring der Lieferketten-Resilienz (Lieferantenbewertung, Notfallübungen, Aktualisierung der Redundanzkonzepte). Punktwert 8.000 €/a; rein organisatorisch, kein belastbarer Kostenkennwert; editierbar.",
        "capex_fixed": "Lieferketten-Resilienz (Aufbau von Zweitlieferanten, Lager-/Redundanz"
            "konzepten, betriebliche Notfallplanung) ist eine organisatorische Maßnahme ohne "
            "baulichen Anteil; kein Marktkennwert verfügbar. Modellannahme als einmaliges "
            "Konzept-/Aufbaubudget → 40.000 €. Für organisatorische Resilienzmaßnahmen ist die "
            "Modellannahme der erwartete, ehrliche Regelfall."}},
    # Herleitung capex_fixed: gezielte Schutzprogramme für vulnerable Gruppen (Hitzetelefon,
    # aufsuchende Betreuung, Aufklärung) sind organisatorisch; kein einheitlicher Kennwert.
    # Modellannahme als Programmbudget (Konzeption/Koordination) → 35.000 €.
    {"code": "VULNERABLE_GROUP_PROGRAMS", "name": "Schutzprogramme vulnerable Gruppen",
     "description": "Gezielte Programme für vulnerable Gruppen.", "measure_type": "organizational",
     "effect_target": ["vulnerability"], "default_reduction": 0.22, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_ANNUAL_MORTALITY", "SOCIAL_INEQUALITY_AMPLIFICATION_RISK_INDEX"],
     "capex_fixed": 35000.0, "capex_per_unit": None, "capex_per_m2": None,
     "opex_fixed_year": 10000.0, "opex_per_unit_year": None, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "Modellannahme (Programmbudget)",
     "sources": {"opex_fixed_year": "Modellannahme (laufender Programmbetrieb)",
                 "capex_fixed": "Modellannahme (organisatorisches Programmbudget)"},
     "source_details": {
        "opex_fixed_year":
            "Modellannahme für den laufenden Betrieb der Schutzprogramme für vulnerable Gruppen (aufsuchende Beratung, Netzwerkpflege) — überwiegend Personalaufwand, daher höherer Jahresanteil. Punktwert 10.000 €/a; kein belastbarer Kostenkennwert; editierbar.",
        "capex_fixed": "Gezielte Schutzprogramme für vulnerable Gruppen (z. B. Hitzetelefon, "
            "aufsuchende Betreuung, Aufklärung in Pflegeeinrichtungen) sind organisatorisch "
            "ohne baulichen Anteil; ein einheitlicher Kennwert existiert nicht. Modellannahme "
            "als einmaliges Programmbudget (Konzeption/Koordination) → 35.000 €."}},
    # Herleitung capex_fixed: angepasste Arbeitszeitmodelle bei Hitze verursachen im Kern nur
    # organisatorischen Aufwand (Dienstplanung, Betriebsvereinbarung); kein Marktkennwert.
    # Modellannahme als geringes Einführungs-/Konzeptbudget → 10.000 €.
    {"code": "HEAT_WORK_SCHEDULES", "name": "Arbeitszeitmodelle bei Hitze",
     "description": "Angepasste Arbeitszeiten bei Hitze.", "measure_type": "behavioral",
     "effect_target": ["exposure"], "default_reduction": 0.18, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_THERMAL_STRESS_HOURS"],
     "capex_fixed": 10000.0, "capex_per_unit": None, "capex_per_m2": None,
     "opex_fixed_year": 2000.0, "opex_per_unit_year": None, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "Modellannahme (Einführungs-/Konzeptbudget)",
     "sources": {"opex_fixed_year": "Modellannahme (Aktualisierung)",
                 "capex_fixed": "Modellannahme (organisatorischer Einführungsaufwand)"},
     "source_details": {
        "opex_fixed_year":
            "Modellannahme für die laufende Aktualisierung hitzeangepasster Arbeitszeitmodelle und Dienstpläne. Geringer organisatorischer Aufwand → 2.000 €/a; kein belastbarer Kostenkennwert; editierbar.",
        "capex_fixed": "Angepasste Arbeitszeitmodelle bei Hitze (z. B. Vorverlegung von "
            "Arbeitszeiten, längere Mittagspausen) verursachen im Kern nur organisatorischen "
            "Aufwand (Dienstplanung, Betriebsvereinbarung); ein Marktkennwert existiert nicht. "
            "Modellannahme als geringes einmaliges Einführungs-/Konzeptbudget → 10.000 €."}},
    # Herleitung capex_per_m2/opex_per_m2_year: keine belastbare €/m²-Quelle für die
    # Mischmaßnahme "Schatten/Wasser" auffindbar (Modellannahme, mangels belastbarer
    # Quelle) — Einzelkomponenten (Sonnensegel-Masten ~160-350 €/Stück, Sonnensegel ab
    # ~70 €/Stück, sonnensegel-guru.de 2026; Wasserspielplatz-Projekt Stuttgart Süd-
    # heimer Platz ~230.000 € Gesamtinvestition ohne Flächenangabe) bestätigen nur die
    # Größenordnung, ergeben aber keinen sauberen Flächen-Kennwert.
    {"code": "PUBLIC_SHADE_WATER", "name": "Schatten / Wasser im öffentlichen Raum",
     "description": "Öffentliche Beschattung und Wasserstellen.", "measure_type": "structural",
     "effect_target": ["hazard"], "default_reduction": 0.18, "coverage_scaling": "linear",
     "linked_risk_codes": ["EXPECTED_THERMAL_STRESS_HOURS"],
     "capex_fixed": 0.0, "capex_per_unit": None, "capex_per_m2": 35.0,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 2.0, "benefit_per_m2_year": 3.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "Modellannahme (mangels belastbarer Quelle)",
     "sources": {"capex_per_m2": "Modellannahme (Sonnensegel-/Wasserspielplatz-Projektkosten)",
                 "opex_per_m2_year": "Modellannahme (mangels belastbarer Quelle)"},
     "source_details": {
        "capex_per_m2": "Keine belastbare €/m²-Quelle für die Mischmaßnahme \"Schatten/Wasser\" "
            "auffindbar – daher Modellannahme. Die Einzelkomponenten (Sonnensegel-Masten "
            "~160–350 €/Stück, Sonnensegel ab ~70 €/Stück, sonnensegel-guru.de 2026; "
            "Wasserspielplatz Stuttgart Südheimer Platz ~230.000 € Gesamtinvestition ohne "
            "Flächenangabe) bestätigen nur die Größenordnung, ergeben aber keinen sauberen "
            "Flächenkennwert. Punktwert 35 €/m² als Größenordnungs-Schätzung.",
        "opex_per_m2_year": "Modellannahme mangels belastbarer Quelle; 2 €/m²/a als "
            "grober Unterhalt für Beschattungs-/Wasserelemente im öffentlichen Raum "
            "(Reinigung, Wartung, Winterlagerung von Segeln)."}},
    # Herleitung capex_fixed: adaptive Bewirtschaftung (Fangregeln, Schonzeiten, Monitoring) ist
    # rein organisatorisch; kein Marktkennwert. Modellannahme als Monitoring-/Konzeptbudget →
    # 20.000 €. Überwiegend Modellannahme ist im Fischerei-Cluster der erwartete Regelfall.
    {"code": "ADAPTIVE_FISHERIES_MANAGEMENT", "name": "Adaptive Fischereibewirtschaftung",
     "description": "Anpassung von Fangregeln, Schonzeiten und Monitoring.", "measure_type": "organizational",
     "effect_target": ["vulnerability"], "default_reduction": 0.20, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_FISHERIES_ECONOMIC_LOSS_EUR", "FISHERIES_STOCK_STRESS_RISK_INDEX"],
     "capex_fixed": 20000.0, "capex_per_unit": None, "capex_per_m2": None,
     "opex_fixed_year": 5000.0, "opex_per_unit_year": None, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "Modellannahme (Monitoring-/Konzeptbudget)",
     "sources": {"opex_fixed_year": "Modellannahme (Monitoring/Bestandsbewertung)",
                 "capex_fixed": "Modellannahme (organisatorisch, mangels Marktkennwert)"},
     "source_details": {
        "opex_fixed_year":
            "Modellannahme für das laufende Monitoring und die jährliche Bestandsbewertung im adaptiven Fischereimanagement. Punktwert 5.000 €/a; überwiegend Modellannahme (Cluster Fischerei); editierbar.",
        "capex_fixed": "Adaptive Fischereibewirtschaftung (Anpassung von Fangregeln, Schonzeiten "
            "und Bestandsmonitoring) ist eine rein organisatorische Maßnahme ohne baulichen "
            "Anteil; ein Marktkennwert existiert nicht. Modellannahme als einmaliges Monitoring-"
            "/Konzeptbudget → 20.000 €. Im Fischerei-Cluster ist die Modellannahme der "
            "erwartete, ehrliche Regelfall."}},
    # Herleitung capex_per_unit: Fischaufstiegsanlagen kosten je nach Bauart und Gewässergröße
    # stark unterschiedlich — ein Beispiel nennt ~600.000 € je Anlage, kompakte technische
    # Pässe (Denil/Schlitzpass) an kleinen Querbauwerken liegen deutlich darunter (Wikipedia/
    # LfU Bayern/BAW). Punktwert 200.000 €/Anlage als repräsentativer Mittelwert über kleine
    # bis größere Anlagen (Alt-Katalogwert 50.000 € bildete nur den kleinsten Pass ab).
    {"code": "FISH_PASSAGE_RESTORATION", "name": "Fischaufstieg / Gewässerdurchgängigkeit",
     "description": "Fischpässe und bauliche Durchgängigkeit.", "measure_type": "structural",
     "effect_target": ["exposure"], "default_reduction": 0.22, "coverage_scaling": "saturating",
     "linked_risk_codes": ["FISHERIES_STOCK_STRESS_RISK_INDEX", "LOW_WATER_FISHERIES_IMPACT_INDEX"],
     "capex_fixed": 0.0, "capex_per_unit": 200000.0, "capex_per_m2": None,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": "Anlage", "unit_density_per_ha": 0.01,
     "source": "LfU Bayern / BAW / Wikipedia (Fischaufstiegsanlagen)",
     "sources": {"capex_per_unit": "LfU Bayern / BAW / Wikipedia (Fischaufstiegsanlagen, breite Spanne)",
                 "unit_density_per_ha": "Modellannahme (Richtwert-Dichte, unbelegt)"},
     "source_refs": {"capex_per_unit": ["LfU_Bayern_Fischaufstieg"]},
     "source_details": {
        "capex_per_unit": "Fischaufstiegsanlagen streuen stark nach Bauart und Gewässergröße: "
            "ein dokumentiertes Beispiel liegt bei ~600.000 € je Anlage; kompakte technische "
            "Pässe (Denil-/Vertical-Slot-Pass) an kleinen Querbauwerken sind deutlich günstiger "
            "(Wikipedia, LfU Bayern-Beispielsammlung, BAW-Arbeitshilfe). Punktwert 200.000 €/"
            "Anlage als repräsentativer Mittelwert über kleine bis größere Anlagen. Der frühere "
            "Katalogwert 50.000 € bildete nur den kleinsten technischen Pass am niedrigen Wehr "
            "ab und wurde angehoben.",
        "unit_density_per_ha": "Modellannahme mangels belastbarer Quelle: ~1 Querbauwerk je "
            "100 ha Gewässer-/Auenfläche (0,01 Anlagen/ha)."}},
    # Herleitung capex_per_unit: keine belastbare Standardquelle für die Resilienz-Ertüchtigung
    # einer Aquakulturanlage (Sauerstoff-/Kühlungstechnik, Notstrom, Wasseraufbereitung) —
    # Modellannahme in sechsstelliger Größenordnung je Anlage → 60.000 €.
    {"code": "AQUACULTURE_RESILIENCE_SYSTEMS", "name": "Aquakultur-Resilienz",
     "description": "Technische und organisatorische Resilienz von Aquakulturanlagen.", "measure_type": "structural",
     "effect_target": ["vulnerability"], "default_reduction": 0.25, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_AQUACULTURE_DAMAGE_EUR", "FISHERIES_STOCK_STRESS_RISK_INDEX"],
     "capex_fixed": 0.0, "capex_per_unit": 60000.0, "capex_per_m2": None,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": "Anlage", "unit_density_per_ha": 0.01,
     "source": "Modellannahme (mangels belastbarer Quelle)",
     "sources": {"capex_per_unit": "Modellannahme (mangels belastbarer Standardquelle)",
                 "unit_density_per_ha": "Modellannahme (Richtwert-Dichte, unbelegt)"},
     "source_details": {
        "capex_per_unit": "Für die Resilienz-Ertüchtigung einer Aquakulturanlage (Sauerstoff-/"
            "Kühlungstechnik, Notstrom, Wasseraufbereitung, Redundanz) war keine belastbare "
            "Standardquelle auffindbar. Modellannahme in sechsstelliger Größenordnung je "
            "Anlage → 60.000 €.",
        "unit_density_per_ha": "Modellannahme mangels belastbarer Quelle: ~1 Aquakulturanlage "
            "je 100 ha Fischerei-/Gewässerfläche (0,01 Anlagen/ha)."}},
    # Herleitung capex_per_m2: Laichhabitat-/Gewässerrenaturierung liegt je nach Aufwand bei
    # ~10 €/lfm (kleine Maßnahmen) bis 600+ €/lfm (technischer Umbau) Gewässerlauf (UBA);
    # flächenbezogen für Kies-/Strukturanreicherung Größenordnung einstellige €/m². Punktwert
    # 10 €/m² für moderate Struktur-/Substratanreicherung; Modellannahme, plausibilisiert.
    {"code": "FISHERIES_SPAWNING_HABITAT_RESTORATION", "name": "Laichhabitat-Renaturierung",
     "description": "Renaturierung und Schutz von Laich- und Aufwuchsgebieten.", "measure_type": "planning",
     "effect_target": ["hazard"], "default_reduction": 0.22, "coverage_scaling": "linear",
     "linked_risk_codes": ["FISHERIES_STOCK_STRESS_RISK_INDEX", "LOW_WATER_FISHERIES_IMPACT_INDEX"],
     "capex_fixed": 0.0, "capex_per_unit": None, "capex_per_m2": 10.0,
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 0.5, "benefit_per_m2_year": 2.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "UBA (Gewässerrenaturierung) / Modellannahme",
     "sources": {"capex_per_m2": "UBA (Bandbreite Gewässerrenaturierung), auf Fläche umgelegt",
                 "opex_per_m2_year": "Modellannahme (extensive Gewässerpflege)"},
     "source_refs": {"capex_per_m2": ["UBA_Gewaesserrenaturierung"]},
     "source_details": {
        "capex_per_m2": "Laichhabitat- und Gewässerrenaturierung liegt nach UBA je nach Aufwand "
            "bei ~10 €/lfm (kleine Maßnahmen) bis 600+ €/lfm (technischer Umbau) Gewässerlauf. "
            "Flächenbezogen (Kies-/Substrat- und Strukturanreicherung von Laichbetten) ergibt "
            "sich eine einstellige €/m²-Größenordnung. Punktwert 10 €/m² für moderate Struktur"
            "anreicherung; Modellannahme, plausibilisiert.",
        "opex_per_m2_year": "Modellannahme: 0,50 €/m²/a für extensive Gewässerpflege "
            "(Substratkontrolle, Gehölzpflege); renaturierte Laichhabitate sind weitgehend "
            "selbsterhaltend."}},
    # Herleitung capex_fixed: organisatorischer Gewässerschutz (Gewässermonitoring, Uferrand-
    # streifen-/Einleiter-Management, Kooperationen) ohne einheitlichen Bau-Kennwert.
    # Modellannahme als Konzept-/Monitoringbudget → 25.000 €.
    {"code": "FISHERIES_WATER_QUALITY_PROTECTION", "name": "Gewässerschutz für Fischerei",
     "description": "Maßnahmen zur Sicherung der Gewässerqualität.", "measure_type": "organizational",
     "effect_target": ["vulnerability"], "default_reduction": 0.20, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_WATER_AIR_POLLUTION", "FISHERIES_STOCK_STRESS_RISK_INDEX"],
     "capex_fixed": 25000.0, "capex_per_unit": None, "capex_per_m2": None,
     "opex_fixed_year": 6000.0, "opex_per_unit_year": None, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "Modellannahme (Konzept-/Monitoringbudget)",
     "sources": {"opex_fixed_year": "Modellannahme (Gewässergüte-Monitoring)",
                 "capex_fixed": "Modellannahme (organisatorisch, mangels Marktkennwert)"},
     "source_details": {
        "opex_fixed_year":
            "Modellannahme für das laufende Gewässergüte-Monitoring (Probenahme, Laboranalytik) zum Schutz der Fischbestände. Punktwert 6.000 €/a; überwiegend Modellannahme; editierbar.",
        "capex_fixed": "Organisatorischer Gewässerschutz zugunsten der Fischerei (Gewässer"
            "monitoring, Uferrandstreifen- und Einleiter-Management, Kooperationen mit "
            "Landwirtschaft/Kommunen) ohne einheitlichen baulichen Kennwert. Modellannahme als "
            "einmaliges Konzept-/Monitoringbudget → 25.000 €."}},
    # Herleitung capex_per_unit: Berliner Wasserbetriebe: Errichtung inkl. Trinkwasser-
    # anschluss ~10-16 T€/Standort → Punktwert 14.000 €. Unabhängig bestätigt durch
    # Presseberichte (Berliner Zeitung/Tagesspiegel 2026): 12.000-15.000 €/Brunnen.
    # Herleitung opex_per_unit_year: Betrieb/Wartung/Beprobung ~2,5-5 T€/a → 3.500 €.
    # Presseberichte nennen ~4.500 €/a für Wartung/Beprobung (innerhalb der Spanne).
    {"code": "DRINKING_FOUNTAINS", "name": "Trinkbrunnen",
     "description": "Öffentliche Trinkwasserspender im Straßenraum.", "measure_type": "structural",
     "effect_target": ["exposure"], "default_reduction": 0.10, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_THERMAL_STRESS_HOURS", "EXPECTED_ANNUAL_MORTALITY"],
     "capex_fixed": 5000.0, "capex_per_unit": 14000.0, "capex_per_m2": None,
     "opex_fixed_year": None, "opex_per_unit_year": 3500.0, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": "Brunnen", "unit_density_per_ha": 0.5,
     "source": "Berliner Wasserbetriebe / Modellannahme",
     "sources": {"capex_fixed": "Modellannahme (Planung/Standortvorbereitung)",
                 "capex_per_unit": "Berliner Wasserbetriebe",
                 "opex_per_unit_year": "Berliner Wasserbetriebe"},
     "source_refs": {"capex_per_unit": ["BWB_Trinkbrunnen"],
                     "opex_per_unit_year": ["BWB_Trinkbrunnen"]},
     "source_details": {
        "capex_fixed": "Modellannahme für Planung/Standortvorbereitung je Trinkbrunnen-Programm "
            "(Standortsuche, Genehmigung, Tiefbauplanung), nicht direkt einer Quelle "
            "entnommen. 5.000 € pauschal als niedrige Konzeptkosten-Schätzung.",
        "capex_per_unit": "Berliner Wasserbetriebe: Errichtung eines öffentlichen Trinkbrunnens "
            "inkl. Trinkwasseranschluss ~10.000–16.000 €/Standort; unabhängig bestätigt durch "
            "Presseberichte (Berliner Zeitung/Tagesspiegel 2026: 12.000–15.000 €/Brunnen). "
            "Punktwert 14.000 € im oberen Mittel der Spanne.",
        "opex_per_unit_year": "Berliner Wasserbetriebe: Betrieb, Wartung und "
            "hygienische Beprobung ~2.500–5.000 €/a; Presseberichte 2026 nennen ~4.500 €/a. "
            "Punktwert 3.500 € im unteren Drittel der Spanne."}},
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
    "DRINKING_FOUNTAINS": ("health", "health"),
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

# ── Monetarisierung der Risiken ──────────────────────────────────────────────────
# Kernprinzip (Product-Owner-Vorgabe): Der Gesamtschaden ist die SUMME der monetär
# bewerteten Einzelrisiken. JEDES Risiko fließt monetär ein; ein nicht-monetärer
# Outcome (Tote, Fälle, Stunden, ha, Arten, Index) wird über einen eigenständigen,
# editierbaren Kostensatz ``cost_per_outcome_eur`` (€ je Outcome-Einheit) bewertet.
# Ein Risiko bleibt NUR dann unmonetarisiert (Kostensatz 0 → trägt 0 € bei), wenn
# eine Monetarisierung eine Doppelzählung wäre (reine Screening-Index-Risiken); das
# ist im jeweiligen ``cost_source_detail`` begründet.

# Reine Screening-/Index-Risiken: Outcome IST der HxVxE-Index. Sie werden bewusst
# NICHT monetarisiert (Kostensatz 0), weil ihr Schaden bereits über die konkreten
# Mortalitäts-/Morbiditäts-/Schadens-/Ausfallrisiken erfasst ist – eine eigene
# €-Bewertung wäre eine Doppelzählung (siehe docs/MODELL_KRITIK.md §6).
INDEX_ONLY_RISK_CODES: frozenset[str] = frozenset(
    r["code"] for r in RISKS if r.get("outcome_unit") == "Index"
)


def risk_is_monetary(risk: dict) -> bool:
    """True, wenn der ref_value bereits in €/Jahr vorliegt (cost_dimension monetary)."""
    return risk.get("cost_dimension") == "monetary"


def risk_default_cost_per_outcome(risk: dict) -> float:
    """Default-Kostensatz (€ je Outcome-Einheit) eines nicht-monetären Risikos."""
    return float(risk.get("cost_per_outcome_eur") or 0.0)


def risk_contributes_to_total(risk: dict) -> bool:
    """True, wenn das Risiko einen €-Beitrag zur Gesamtschadenssumme liefert.

    Monetäre Risiken tragen immer bei; nicht-monetäre nur, wenn ein positiver
    Kostensatz hinterlegt ist. Reine Index-Risiken (Kostensatz 0) sind damit
    automatisch von der Summe ausgenommen (dokumentierte Vermeidung von
    Doppelzählung).
    """
    if risk_is_monetary(risk):
        return True
    return risk_default_cost_per_outcome(risk) > 0.0


def cost_unit_label(outcome_unit: str) -> str:
    """Einheit des Kostensatz-Parameters: „€ je <Outcome-Einheit ohne /Jahr>“."""
    base = (outcome_unit or "").replace("/Jahr", "").strip()
    if not base or base == "€":
        return "€"
    if base == "Index":
        return "€ je Index-Punkt"
    return f"€ je {base}"

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
