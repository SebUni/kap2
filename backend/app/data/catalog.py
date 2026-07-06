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
     "proxy": "Versiegelungsgrad (OSM) × TWI/Senkenlage (Terrarium-DEM, D8) × Starkregen-Häufigkeit (DWD-CDC-Raster: Tage/Jahr ≥ 20 mm und ≥ 30 mm).",
     "source": "DWD CDC (Starkregen-Raster) + AWS Terrarium DEM",
     "source_detail": "Der Starkregen-/Überflutungsindex (0-100) kombiniert Versiegelung, "
        "Senkenlage und die ortsaufgelöste Starkregen-Häufigkeit aus den DWD-CDC-Jahresrastern "
        "(Tage/Jahr mit ≥ 20 mm bzw. ≥ 30 mm Niederschlag, am Zentroid gemittelt). Kalibrierung: "
        "index = min(100, Tage≥20mm·4 + Tage≥30mm·6); DE-typisch ~8+2 Tage → ≈ 44. Fehlt das "
        "Raster, greift der frühere Proxy aus dem regionalen Temperatur-/Starkregentrend "
        "(dokumentiert). Die Zunahme von Starkniederschlägen ist im DWD Nationalen Klimareport "
        "belegt; die Index-Skala ist eine editierbare Modellwahl.",
     "source_refs": ["DWD_CDC_Starkregen", "DWD_Klimareport"]},
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
     "proxy": "Sturmtage/Jahr (ERA5-Böen ≥ 25 m/s am Zentroid, falls Raster vorhanden; sonst regionaler Konstantwert), erhöht in exponierten (offenen/hohen) Lagen.",
     "source": "ERA5 (Copernicus C3S) / DWD CDC",
     "source_detail": "Die Sturmtage stammen — falls der Betreiber das ERA5-Raster erzeugt hat "
        "(scripts/fetch_era5_storm.py, kostenloser CDS-Key) — aus der ERA5-Böenklimatologie "
        "(Tage/Jahr mit 10-m-Böe ≥ 25 m/s). Ohne dieses Raster bleibt ein dokumentierter "
        "regionaler Konstantwert (Provenienz storm_days in build_regional_context). ERA5 ist "
        "bundesweit einheitlich, kostenlos und kommerziell nutzbar (CC-BY 4.0).",
     "source_refs": ["ERA5_C3S", "DWD_CDC"]},
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
     # Kostensatz wird in _RISK_COST_RATES gesetzt (Arbeitsproduktivität, ohne klinische
     # Behandlung — die zählt „Erwartete jährliche Morbidität"; Abgrenzung dort/hier).
     "ref_value": 400.0, "scale": "pop", "source": "Modellannahme (Belastungsstunden, unbelegt)",
     "description": "Erwartete jährliche Stunden thermischer Belastung.", "priority": 1},
    {"code": "EXPECTED_POLLUTANT_EXPOSURE_HOURS", "name": "Schadstoffexpositionsstunden",
     "outcome_unit": "Stunden/Jahr", "group": "heat", "cost_dimension": "health",
     "hazards": ["HEAT_WAVE", "MEAN_TEMPERATURE_RISE"],
     "exposures": ["POPULATION_DENSITY", "OUTDOOR_THERMAL_EXPOSURE"],
     "vulnerabilities": ["AIR_QUALITY_RISK", "HEAT_SENSITIVITY"],
     # Kostensatz wird in _RISK_COST_RATES gesetzt (Produktivitäts-/Komfortverlust, ohne
     # klinische Behandlung — Abgrenzung zur Morbidität).
     "ref_value": 250.0, "scale": "pop", "source": "Modellannahme (Belastungsstunden, unbelegt)",
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
    # EXPECTED_TOTAL_DAMAGE_EAD_EUR (Gesamtschäden/EAD) wurde ENTFERNT: Der Gesamtschaden
    # ist kein eigenständiges HxVxE-Risiko mehr, sondern die SUMME der monetär bewerteten
    # Einzelrisiken (risk_engine.aggregate → cost.total_eur). Das eigene EAD-Risiko war per
    # Konstruktion ~die Summe der Sektorschäden und verdoppelte diese in total_eur (siehe
    # docs/MODELL_KRITIK.md §3.7). Maßnahmen, die früher auf EAD wirkten, sind auf die
    # konkreten Sektorschadens-Risiken umverdrahtet.
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


# ── Monetarisierung der Risiken (Helfer) ─────────────────────────────────────────
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


# Direkte Sektorschäden (Schicht B, §6.2): ihre Zell-Kosten bilden die Basis für den
# k_indirekt-Multiplikator (indirekte Folgekosten) und die Restaurierungs-Teilkennzahl.
DIRECT_SECTOR_RISK_CODES: frozenset[str] = frozenset({
    "EXPECTED_BUILDING_DAMAGE_EUR",
    "EXPECTED_TRANSPORT_DAMAGE_EUR",
    "EXPECTED_ENERGY_INFRA_DAMAGE_EUR",
    "EXPECTED_TELECOM_DAMAGE_EUR",
    "EXPECTED_WATER_WASTEWATER_DAMAGE_EUR",
    "EXPECTED_AGRICULTURAL_DAMAGE_EUR",
    "EXPECTED_SOIL_LOSS_DEGRADATION_EUR",
    "EXPECTED_ECOSYSTEM_SERVICE_LOSS",
    "EXPECTED_FISHERIES_ECONOMIC_LOSS_EUR",
    "EXPECTED_AQUACULTURE_DAMAGE_EUR",
})

# Folgekosten, die in den k_indirekt-Multiplikator konsolidiert werden (ihre eigene
# €-Bewertung wird 0 gesetzt, um die Doppelzählung aus MODELL_KRITIK §3.7 zu beenden).
CONSOLIDATED_INTO_INDIRECT_CODES: frozenset[str] = frozenset({
    "EXPECTED_SUPPLY_SHORTAGE_COSTS_EUR",
    "EXPECTED_LOCATION_DISADVANTAGE_EUR",
    "EXPECTED_DELAYED_DAMAGE_COSTS_EUR",
})

# Nicht additive Teilkennzahlen: eine Teilmenge bereits gezählter Schäden
# (Restaurierung = Anteil der direkten Sektorschäden). Werden ausgewiesen, aber NICHT
# in ``total_eur`` addiert (sonst Doppelzählung, §3.7).
NON_ADDITIVE_RISK_CODES: frozenset[str] = frozenset({
    "EXPECTED_RESTORATION_COSTS_EUR",
})


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
    if risk["code"] in NON_ADDITIVE_RISK_CODES:
        return False   # Teilkennzahl (z. B. Restaurierung) – nicht in die Summe
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
            "3,6-7,2/100.000 (statistikkonform). Die monetäre Bewertung erfolgt über den "
            "separaten, editierbaren Kostensatz-Parameter „Kostensatz (Monetarisierung)“ "
            "– nicht mehr über diesen Referenzwert.",
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


# ── Monetarisierungs-Kostensätze je Risiko (Quellen + Herleitung) ─────────────────
# Setzt für JEDES nicht-monetäre Risiko den Kostensatz ``cost_per_outcome_eur`` (€ je
# Outcome-Einheit) samt ``cost_source``/``cost_source_detail``/``cost_source_refs`` für
# den eigenständigen Registry-Parameter „Kostensatz (Monetarisierung)“. Damit fließt
# jedes Risiko monetär in den Gesamtschaden ein. Reine Screening-Index-Risiken bleiben
# bewusst bei 0 € (Vermeidung von Doppelzählung – im Detailtext begründet).
# Quellenprimat: OECD-VSL (Mortalität), UBA-Methodenkonvention 3.1 (Gesundheit/Umwelt),
# EWI-VoLL 2015 (Energie-/Ausfallkosten), BBK-KRITIS (Ausfallzeiten), Prognos 2023
# (indirekte/verkehrliche Folgen), TEEB-DE/BfN (Ökosystem-/Flächenwerte).

# CODE -> (Kostensatz €/Outcome, Kurz-Quelle, Referenz-Keys, Herleitungstext).
_RISK_COST_RATES: dict[str, tuple[float, str, list[str], str]] = {
    # ── Gesundheit: Personenschäden (Kostensatz je Fall/Person) ──
    "EXPECTED_ANNUAL_MORTALITY": (
        3_500_000.0, "OECD 2012 (VSL) / RKI 2023", ["OECD_VSL_2012", "RKI_Hitzemortalitaet"],
        "Wert eines statistischen Lebens (VSL) 3,5 Mio € je vorzeitigem Todesfall – "
        "Punktwert im international gebräuchlichen Band (OECD 2012: Meta-Analyse "
        "internationaler Zahlungsbereitschafts-Studien, EU/OECD-Zentralwerte ~1–4 Mio €). "
        "Editierbarer Kostensatz; ersetzt die frühere Prosa im Referenzwert-Tooltip."),
    "EXPECTED_ANNUAL_MORBIDITY": (
        5_000.0, "UBA MK3.1 2020", ["UBA_Methodenkonvention_MK3.1"],
        "Durchschnittliche Krankheitskosten 5.000 € je klimabedingtem Erkrankungsfall "
        "(ambulante/stationäre Behandlung + krankheitsbedingter Produktivitätsausfall), "
        "Größenordnung an den Gesundheits-Kostensätzen der UBA-Methodenkonvention 3.1 "
        "orientiert. Editierbar. Abgrenzung (§8/B4): erfasst die KLINISCHEN Fälle; die "
        "subklinische Produktivitätslast thermischer/Schadstoff-Belastung ist getrennt über "
        "die Belastungsstunden-Risiken bewertet — keine Doppelzählung."),
    "EXPECTED_ANNUAL_INJURIES": (
        12_000.0, "UBA MK3.1 2020", ["UBA_Methodenkonvention_MK3.1"],
        "12.000 € je Verletztem (Behandlung, Reha, temporärer Erwerbsausfall) als "
        "editierbarer Punktwert; Größenordnung an den Gesundheits-/Unfallkostensätzen der "
        "UBA-Methodenkonvention 3.1 orientiert."),
    "EXPECTED_ANNUAL_MENTAL_HEALTH": (
        4_000.0, "UBA MK3.1 2020", ["UBA_Methodenkonvention_MK3.1"],
        "4.000 € je psychischem Belastungsfall (Diagnostik, Therapie, Ausfallzeiten) als "
        "editierbarer Punktwert, an den Gesundheits-Kostensätzen der UBA-Methoden"
        "konvention 3.1 orientiert. Keine belastbare Einzelstatistik ⇒ Modellannahme."),
    "EXPECTED_ANNUAL_AFFECTED_EVACUATED": (
        2_500.0, "UBA MK3.1 / BBK", ["UBA_Methodenkonvention_MK3.1", "BBK_KRITIS"],
        "2.500 € je betroffener/evakuierter Person (Notunterbringung, Versorgung, "
        "Einsatz-/Betreuungskosten) als editierbarer Punktwert; Größenordnung an "
        "UBA MK3.1 und BBK-Bevölkerungsschutz-Kennzahlen orientiert."),
    "EXPECTED_THERMAL_STRESS_HOURS": (
        400.0, "UBA MK3.1 2020 (Modellannahme)", ["UBA_Methodenkonvention_MK3.1"],
        "400 € je aggregierter Belastungsstunde als editierbare Modellannahme — bewusst nur "
        "der ARBEITSPRODUKTIVITÄTS-/Komfortverlust thermischer Belastung, an den "
        "Produktivitätskosten-Ansätzen der UBA-Methodenkonvention 3.1 orientiert. Abgrenzung "
        "gegen Doppelzählung (§8/B4): Der klinische Behandlungs-/Krankheitsanteil ist im "
        "Risiko „Erwartete jährliche Morbidität“ (Kostensatz je Fall) erfasst und hier "
        "ausgeklammert — Belastungsstunden zählen nur die subklinische Produktivitätslast."),
    "EXPECTED_POLLUTANT_EXPOSURE_HOURS": (
        300.0, "UBA MK3.1 2020 (Modellannahme)", ["UBA_Methodenkonvention_MK3.1"],
        "300 € je aggregierter Schadstoff-Expositionsstunde als editierbare Modellannahme — "
        "bewusst nur der Produktivitäts-/Komfortverlust, an UBA-MK3.1-Luftschadstoff-"
        "Kostensätzen orientiert. Abgrenzung gegen Doppelzählung (§8/B4): Der klinische "
        "Anteil (Atemwegs-/Herz-Kreislauf-Behandlung) ist über die Morbidität erfasst und "
        "hier ausgeklammert."),
    # ── Operativ: Ausfallstunden (Kostensatz je Ausfallstunde, aggregiert) ──
    "EXPECTED_CI_OUTAGE_HOURS": (
        40_000.0, "BBK KRITIS / EWI-VoLL 2015", ["BBK_KRITIS", "EWI_VoLL_2015"],
        "40.000 € je aggregierter Ausfallstunde kritischer Infrastruktur (gemischtes "
        "Sektorportfolio) als editierbare Modellannahme; hergeleitet als konservativer "
        "Bruchteil des EWI-VoLL (nationale Stromausfallkosten ~430 Mio €/h) auf "
        "Kommunalebene, ergänzt um BBK-KRITIS-Systemabgrenzung. Bislang 0 € ⇒ jetzt bewertet."),
    "EXPECTED_ENERGY_OUTAGE_HOURS": (
        120_000.0, "EWI-VoLL 2015", ["EWI_VoLL_2015"],
        "120.000 € je Stromausfallstunde als editierbare Modellannahme, hergeleitet aus "
        "dem Value of Lost Load (EWI 2015: Haushalte ~11,92 €/kWh; nationale Ausfallkosten "
        "~430 Mio €/h) heruntergerechnet auf die Last einer ~100.000-Ew.-Kommune. "
        "Bislang 0 € ⇒ jetzt bewertet."),
    "EXPECTED_WATER_SUPPLY_OUTAGE_HOURS": (
        60_000.0, "BBK KRITIS (Modellannahme)", ["BBK_KRITIS"],
        "60.000 € je Ausfallstunde der Wasserversorgung (Ersatzversorgung, Gesundheits-/"
        "Betriebsfolgen) als editierbare Modellannahme, Systemabgrenzung an BBK-KRITIS "
        "angelehnt. Bislang 0 € ⇒ jetzt bewertet."),
    "EXPECTED_WASTEWATER_OUTAGE_HOURS": (
        25_000.0, "BBK KRITIS (Modellannahme)", ["BBK_KRITIS"],
        "25.000 € je Ausfallstunde der Abwasserentsorgung (Umwelt-/Hygienefolgen, "
        "Notbetrieb) als editierbare Modellannahme, an BBK-KRITIS angelehnt. "
        "Bislang 0 € ⇒ jetzt bewertet."),
    "EXPECTED_COMMUNICATION_OUTAGE_HOURS": (
        50_000.0, "BBK KRITIS (Modellannahme)", ["BBK_KRITIS"],
        "50.000 € je Ausfallstunde der Kommunikationsnetze (Wirtschafts-, Notruf- und "
        "Koordinationsfolgen) als editierbare Modellannahme, an BBK-KRITIS angelehnt. "
        "Bislang 0 € ⇒ jetzt bewertet."),
    "EXPECTED_TRANSPORT_DISRUPTION_HOURS": (
        30_000.0, "Prognos 2023 / BBK", ["Prognos_Klimaschaeden_2023", "BBK_KRITIS"],
        "30.000 € je Stunde Verkehrsunterbrechung (aggregierte Zeit-/Wertschöpfungskosten "
        "gestörter Personen- und Güterverkehre) als editierbare Modellannahme, "
        "Größenordnung an Prognos-2023-Folgekosten und BBK-KRITIS angelehnt. "
        "Bislang 0 € ⇒ jetzt bewertet."),
    "EXPECTED_SUPPLY_CHAIN_DISRUPTION_HOURS": (
        40_000.0, "Prognos 2023 (Modellannahme)", ["Prognos_Klimaschaeden_2023"],
        "40.000 € je Stunde Lieferkettenunterbrechung (Produktions-/Wertschöpfungsausfall) "
        "als editierbare Modellannahme, an den indirekten Wirtschaftsfolgen aus Prognos "
        "2023 orientiert. Bislang 0 € ⇒ jetzt bewertet."),
    "EXPECTED_ADMIN_OUTAGE_HOURS": (
        15_000.0, "BBK KRITIS (Modellannahme)", ["BBK_KRITIS"],
        "15.000 € je administrativer Ausfallstunde (verzögerte Verwaltungs-/Daseins"
        "vorsorge-Leistungen) als editierbare Modellannahme, an BBK-KRITIS angelehnt. "
        "Bislang 0 € ⇒ jetzt bewertet."),
    "EXPECTED_FUNCTIONAL_FAILURE_DURATION": (
        30_000.0, "BBK KRITIS (Modellannahme)", ["BBK_KRITIS"],
        "30.000 € je Stunde Funktionsausfall (kaskadierende System-/Versorgungsfolgen) als "
        "editierbare Modellannahme, an BBK-KRITIS-Kaskadenbetrachtungen angelehnt. "
        "Bislang 0 € ⇒ jetzt bewertet."),
    # ── Umwelt: physische Verluste (Kostensatz je Art / ha) ──
    "EXPECTED_BIODIVERSITY_LOSS": (
        500_000.0, "TEEB-DE / UBA KWRA 2021", ["TEEB_DE_Naturkapital", "UBA_KWRA_2021"],
        "500.000 € je verlorener Art (Wiederherstellungs-/Erhaltungsprogramm-Größenordnung) "
        "als editierbare Modellannahme, am Naturkapital-/Ökosystemleistungs-Bewertungsrahmen "
        "von TEEB-DE orientiert. Abgrenzung: bewertet den physischen Artverlust, nicht den "
        "laufenden Leistungsausfall (der über „Verlust von Ökosystemleistungen“ läuft) – "
        "keine Doppelzählung. Bislang 0 € ⇒ jetzt bewertet."),
    "EXPECTED_HABITAT_LOSS": (
        80_000.0, "TEEB-DE (Modellannahme)", ["TEEB_DE_Naturkapital"],
        "80.000 € je ha verlorenem Habitat (Renaturierungs-/Wiederherstellungskosten) als "
        "editierbare Modellannahme, an TEEB-DE-Bewertungen orientiert. Abgrenzung zum "
        "laufenden Ökosystemleistungs-Verlust (eigener monetärer Posten) im Sinne der "
        "Vermeidung von Doppelzählung. Bislang 0 € ⇒ jetzt bewertet."),
    "EXPECTED_SOIL_DEGRADATION": (
        10_000.0, "TEEB-DE / UBA MK3.1", ["TEEB_DE_Naturkapital", "UBA_Methodenkonvention_MK3.1"],
        "10.000 € je ha degradiertem Boden — bewusst nur der ÖKOLOGISCHE Bodenfunktionswert "
        "(Wasserhaushalt, Lebensraum, Kohlenstoffspeicher), an TEEB-DE/UBA MK3.1 orientiert. "
        "Abgrenzung gegen Doppelzählung (§8/B5): Der ökonomische Boden-/Ertragswert derselben "
        "Fläche ist über das monetäre Risiko „Bodenverluste / -degradation (€)“ "
        "(EXPECTED_SOIL_LOSS_DEGRADATION_EUR, Bodenwert je ha × Erosionsintensität) erfasst; "
        "dieses Umweltrisiko bewertet nur den davon getrennten Naturhaushaltsanteil. "
        "Editierbar."),
    "EXPECTED_VEGETATION_DAMAGE": (
        20_000.0, "TEEB-DE (Modellannahme)", ["TEEB_DE_Naturkapital"],
        "20.000 € je ha geschädigter Vegetation (Wiederbegrünungs-/Wiederherstellungs"
        "kosten) als editierbare Modellannahme, an TEEB-DE-Bewertungen orientiert. "
        "Bislang 0 € ⇒ jetzt bewertet."),
}

_INDEX_EXCLUSION_DETAIL = (
    "Bewusst NICHT monetarisiert (Kostensatz 0 €): Dieses Risiko ist ein reines "
    "Screening-Index-Risiko; sein Schadensgehalt ist bereits über die konkreten "
    "monetär bewerteten Risiken (Mortalität/Morbidität, Sektor-/Ausfall-/Flächen"
    "schäden) erfasst. Eine eigene €-Bewertung wäre eine Doppelzählung und ist "
    "deshalb aus der Gesamtschadenssumme ausgenommen (siehe docs/MODELL_KRITIK.md §6). "
    "Editierbar: Wird ein positiver Kostensatz gesetzt, fließt das Risiko additiv ein.")


def _enrich_risk_cost_sources() -> None:
    for r in RISKS:
        if risk_is_monetary(r):
            continue  # ref_value ist bereits €/Jahr → kein Kostensatz-Parameter
        code = r["code"]
        if code in _RISK_COST_RATES:
            rate, src, refs, detail = _RISK_COST_RATES[code]
            r["cost_per_outcome_eur"] = rate
            r["cost_source"] = src
            r["cost_source_detail"] = detail
            r["cost_source_refs"] = refs
        elif code in INDEX_ONLY_RISK_CODES:
            r["cost_per_outcome_eur"] = 0.0
            r["cost_source"] = "Bewusst nicht monetarisiert (Doppelzählung)"
            r["cost_source_detail"] = _INDEX_EXCLUSION_DETAIL
            r["cost_source_refs"] = ["UBA_KWRA_2021"]
        else:
            # Sicherheitsnetz: nicht-monetäres Risiko ohne Kostensatz-Eintrag.
            r.setdefault("cost_per_outcome_eur", 0.0)
            r["cost_source"] = r.get("cost_source") or "Modellannahme (Kostensatz, unbelegt)"
            r["cost_source_detail"] = r.get("cost_source_detail") or (
                "Für dieses Risiko ist noch kein belegter Kostensatz hinterlegt; "
                "Bewertung als editierbare Modellannahme.")


_enrich_risk_cost_sources()


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
    """Kuratierte Wirkungsketten eines Risikos (``pathway_curation.CURATED_PATHWAYS``).

    Jede Kette ist fachlich begründet und quellenbelegt (KWRA 2021 / GIZ Vulnerability
    Sourcebook); die frühere kartesische Erzeugung aus den H/E/V-Listen ist ersetzt
    (MODELL_KRITIK §3.5 — sinnlose Mischketten + pfadzahl-abhängige Verdünnung). Der
    Index ist das MAXIMUM der gewichteten Ketten (``risk_engine.cell_risk_indices``),
    nicht mehr der gewichtete Mittelwert.

    Gibt Liste von {hazard, exposure, vulnerability, pathway_type, weight, justification,
    justification_ref, cluster} zurück. Fällt für (theoretisch) unkuratierte Risiken auf
    die reine Primärkette H0×E0×V0 zurück, statt sinnlose Ketten zu erzeugen.
    """
    from app.data.pathway_curation import CURATED_PATHWAYS

    H = risk["hazards"]
    E = risk["exposures"]
    V = risk["vulnerabilities"]
    if not H or not E or not V:
        return []

    pw = PATHWAY_WEIGHTS
    spec = CURATED_PATHWAYS.get(risk["code"])
    if not spec:
        return [{
            "hazard": H[0], "exposure": E[0], "vulnerability": V[0],
            "pathway_type": "primary", "weight": pw["primary"],
            "justification": "Primärkette (keine Kuratierung hinterlegt).",
            "justification_ref": None, "cluster": None,
        }]

    cluster = spec.get("cluster")
    default_ref = spec.get("ref")
    paths: list[dict] = []
    for ch in spec["chains"]:
        h, e, v, ptype, note = ch[0], ch[1], ch[2], ch[3], ch[4]
        ref = ch[5] if len(ch) > 5 else default_ref
        paths.append({
            "hazard": h, "exposure": e, "vulnerability": v,
            "pathway_type": ptype, "weight": pw[ptype],
            "justification": note, "justification_ref": ref, "cluster": cluster,
        })
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
# default_reduction: je Maßnahme mit Wirkmechanismus-Herleitung dokumentiert (inline oder
#   zentral in _MEASURE_EFFECT_DOCS unten); wo Wirksamkeitsstudien existieren, darauf
#   kalibriert (z. B. Hitzeaktionspläne 0,25 nach Urban u. a. 2025). Kommune kann Werte
#   über PUT /kommune/{id}/parameters mit eigener Quelle überschreiben.
# Kostenquellen: recherchierte Kennwerte je Feld (sources/source_details/source_refs);
#   bewusste 0-Werte erklärt _enrich_measure_zero_cost_docs() maßnahmen­spezifisch.
#   Vollständigkeit („kein Parameter ohne Infokasten") erzwingt der Ratchet-Test
#   backend/tests/test_parameter_docs_complete.py.

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
     "opex_fixed_year": None, "opex_per_unit_year": 5000.0, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": "Station", "unit_density_per_ha": 0.005,
     "source": "Verteilnetzbetreiber-Praxiswerte (ront.info / Bayernwerk) / BNetzA-Größenordnung",
     "sources": {"capex_per_unit": "Verteilnetz-Praxiswerte (Einzelstation bis MS-Ausbau)",
                 "opex_per_unit_year": "VDI 2067 (Instandhaltungssätze elektrotechn. Anlagen)",
                 "default_reduction": "BNetzA-Versorgungsqualität (n-1-Redundanzprinzip)",
                 "benefit_per_m2_year": "Modellentscheidung (Nutzen über flat-Risiken, dokumentiert)",
                 "unit_density_per_ha": "Modellannahme (Richtwert-Dichte, unbelegt)"},
     "source_refs": {"capex_per_unit": ["RONT_Ortsnetzstation"],
                     "opex_per_unit_year": ["VDI_2067_Blatt1", "RONT_Ortsnetzstation"],
                     "default_reduction": ["BNetzA_SAIDI_2023"]},
     "source_details": {
        "default_reduction": "Wirkmechanismus: Redundante Einspeisung/Ringschluss (n-1-Prinzip) "
            "verhindert bzw. verkürzt Versorgungsunterbrechungen an den verstärkten Netzknoten — "
            "die hohe deutsche Versorgungszuverlässigkeit (SAIDI 2023: 12,8 min/a, BNetzA) beruht "
            "wesentlich auf Redundanz und Verkabelungsgrad der Netze. Für die abgedeckten Zellen "
            "wird eine Reduktion der Ausfallstunden-Risiken um 30 % angesetzt: konservativ-mittig, "
            "da vollständige n-1-Auslegung Einzelfehler nahezu eliminiert, Extremwetter aber auch "
            "redundante Systeme gleichzeitig treffen kann (Restrisiko). Keine externe "
            "Kalibrierstudie je Kommune — editierbare, dokumentierte Modellannahme im belegten "
            "Wirkprinzip.",
        "capex_per_unit": "Eine einzelne Ortsnetzstation kostet ~18.000-50.000 € (400-kVA-Trafo "
            "bis eigene Mittelspannungsstation inkl. Verkabelung; ront.info, ms-elektro.gmbh); "
            "eine vollständige MS-Netzverstärkung liegt bei ~0,8-3 Mio € (Bayernwerk-Projekte). "
            "Der Punktwert 250.000 € je \"Station\" steht für ein Verstärkungs-/Redundanzpaket "
            "je Netzknoten (Stationsausbau + redundante Einspeisung + Kabelabschnitt), "
            "eingeordnet zwischen Einzelstation und Vollausbau (BNetzA/dena-Größenordnung).",
        "opex_per_unit_year": "Betrieb/Instandhaltung der verstärkten Netzknoten: VDI 2067 "
            "setzt für elektrotechnische Anlagen Wartung + Instandsetzung von ~1-3 % der "
            "Investitionssumme pro Jahr an. 2 % von 250.000 € → 5.000 €/(Station·a) "
            "(Inspektion, Schalthandlungen, Trafo-/Kabelinstandhaltung).",
        "benefit_per_m2_year": "0 €/(m²·a) ist bewusst gesetzt: Der Nutzen der Netzverstärkung "
            "ist die Reduktion der Ausfallstunden-Risiken (EXPECTED_ENERGY_OUTAGE_HOURS, "
            "EXPECTED_CI_OUTAGE_HOURS). Diese sind kommunenweite (flat-skalierte) Risiken — ihr "
            "vermiedener Schaden wird als Differenz der kommunenweiten P90-Outcome-Kosten "
            "berechnet (measure_service, flat-Nutzen), nicht als €/m². Ein zusätzlicher "
            "Flächennutzen existiert nicht (kein Energieertrag o. Ä.).",
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
     "opex_fixed_year": None, "opex_per_unit_year": 6000.0, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": "Anlage", "unit_density_per_ha": 0.003,
     "source": "Modellannahme (mangels belastbarer Quelle)",
     "sources": {"capex_per_unit": "Modellannahme (mangels belastbarer Quelle)",
                 "opex_per_unit_year": "VDI 2067 (Wartungssätze Kälte-/RLT-Technik) + Energie",
                 "default_reduction": "Modellannahme (Derating-Mechanismus, dokumentiert)",
                 "unit_density_per_ha": "Modellannahme (Richtwert-Dichte, unbelegt)"},
     "source_refs": {"opex_per_unit_year": ["VDI_2067_Blatt1"]},
     "source_details": {
        "default_reduction": "Wirkmechanismus: Transformatoren, Umrichter und Schaltanlagen "
            "verlieren bei hohen Außentemperaturen Nennleistung (Derating) und altern "
            "beschleunigt; aktive Zusatzkühlung und hitzefeste Auslegung erhalten die "
            "Betriebsfähigkeit an Hitzetagen und senken hitzebedingte Anlagenschäden. Angesetzt: "
            "20 % Reduktion des hitzegetriebenen Energieinfrastruktur-Schadensrisikos in den "
            "abgedeckten Zellen — konservativ unterhalb der Netzverstärkung (0,30), da nur der "
            "Hitzepfad adressiert wird (Sturm/Flut unverändert). Keine externe Kalibrierstudie "
            "vorhanden — editierbare, dokumentierte Modellannahme.",
        "capex_per_unit": "Für die hitzefeste Ertüchtigung/Zusatzkühlung energiebezogener "
            "Anlagen (Transformatoren, Umspannwerke) war keine belastbare Einzelquelle "
            "auffindbar. Modellannahme in sechsstelliger Größenordnung je Anlage (Zusatz"
            "kühlung, thermische Absicherung, Redundanz) → Punktwert 120.000 €.",
        "opex_per_unit_year": "Kühl- und Klimatechnik verursacht laufende Kosten: VDI 2067 "
            "setzt für Kälte-/RLT-Anlagen Wartung + Instandsetzung von ~4-6 % der Investition "
            "pro Jahr an, hinzu kommt der Energieverbrauch der Zusatzkühlung an Hitzetagen. "
            "5 % von 120.000 € → 6.000 €/(Anlage·a) als Vollkosten-Punktwert (Wartung ~2-4 % "
            "+ Kühlenergie). Ohne diesen Posten wäre die Maßnahme unrealistisch betriebskostenfrei.",
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
                 "opex_per_m2_year": "Modellannahme (Betrieb/Versicherung ~1-2 %)",
                 "default_reduction": "HTW Berlin (Autarkiegrade PV-Speicher-Systeme)",
                 "benefit_per_m2_year": "HTW Berlin (PV-Ertrag/Eigenverbrauchswert)"},
     "source_refs": {"capex_per_m2": ["HTW_Stromspeicher_2025"],
                     "default_reduction": ["HTW_Stromspeicher_2025"],
                     "benefit_per_m2_year": ["HTW_Stromspeicher_2025"]},
     "source_details": {
        "default_reduction": "Wirkmechanismus: PV + Batteriespeicher (zunehmend mit Ersatzstrom-/"
            "Inselbetriebsfunktion) entkoppeln Verbraucher zeitweise vom Netz und dämpfen die "
            "Folgen von Versorgungsunterbrechungen sowie systemische Dominoeffekte. Typische "
            "PV-Speicher-Systeme erreichen Autarkiegrade von ~40-70 % (HTW-Stromspeicher-"
            "Inspektion); da Ersatzstromfähigkeit nicht in allen Systemen aktiv ist und Ausfälle "
            "auch nachts/im Winter auftreten, wird konservativ eine Reduktion der verknüpften "
            "Ausfall-/Domino-Risiken um 25 % in den abgedeckten Zellen angesetzt. Editierbare, "
            "dokumentierte Modellannahme auf belegter Autarkie-Basis.",
        "capex_per_m2": "Schlüsselfertige Aufdach-PV kostet ~1.015-1.200 €/kWp (Frühjahr 2026, "
            "historischer Tiefstand), Batteriespeicher ~315 €/kWh bzw. konservativ 500 €/kWh "
            "(HTW-Stromspeicher-Inspektion 2025, HTW Berlin; 42watt.de). Bei ~6 m² Modulfläche "
            "je kWp sind das ~170-200 €/m² Modulfläche; über die Bruttodachfläche inklusive "
            "Speicheranteil → Punktwert 150 €/m².",
        "opex_per_m2_year": "Modellannahme: ~1-2 % der Investition pro Jahr für Betrieb, "
            "Wartung, Wechselrichter-Rücklage und Versicherung → 2 €/m²/a.",
        "benefit_per_m2_year": "Direkter Energieertrag: ~1.000 kWh/kWp·a Ertrag bei ~6 m² "
            "Modulfläche je kWp ≈ 165 kWh/m² Modulfläche; bewertet mit Eigenverbrauchs-/"
            "Einspeisemix ~0,15-0,25 €/kWh wären das 25-40 €/m² MODULfläche. Der Parameter "
            "bezieht sich aber auf die gesamte Maßnahmenfläche (Bruttodach inkl. nicht belegter "
            "Anteile) und zieht die Betriebskosten nicht ab → konservativer Nettowert 8 €/(m²·a) "
            "(≈ 20-30 % effektiver Belegungs-/Nutzungsgrad; HTW-Ertrags-/Preisdaten)."}},
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
                 "opex_per_m2_year": "Modellannahme (anteilige Nachbeschichtung)",
                 "default_reduction": "Albedo-Wirkprinzip (VDI 3787, Modellannahme)",
                 "benefit_per_m2_year": "Modellannahme (eingesparte Kühlenergie)"},
     "source_refs": {"capex_per_m2": ["Asphaltshop_Dachbeschichtung"],
                     "default_reduction": ["VDI3787_Stadtklima"]},
     "source_details": {
        "default_reduction": "Wirkmechanismus: Hochreflektive Dächer senken die Dachoberflächen"
            "temperatur um bis zu ~30 K und reduzieren die Wärmeabgabe an Innenräume und "
            "Stadtluft (Albedo-Term des UHI-Modells, VDI 3787). Auf die Wärmebelastungsstunden "
            "der Zelle wirkt nur der Dachflächenanteil → 15 % Reduktion angesetzt, bewusst der "
            "niedrigste Wert der Hitzemaßnahmen (kein Schatten-/Verdunstungseffekt wie bei "
            "Begrünung). Editierbare, dokumentierte Modellannahme.",
        "capex_per_m2": "Sonnenreflektierende (weiße) Dachbeschichtung kostet 10-30 €/m², eine "
            "Acrylbeschichtung im Mittel ~18 €/m² (asphalt-shop.de, steelmonks 2026). "
            "Punktwert 20 €/m² im Mittel der Marktspanne für die Beschichtung einer "
            "bestehenden Dachfläche (ohne Dacherneuerung).",
        "opex_per_m2_year": "Modellannahme mangels belastbarer Quelle: 1 €/m²/a bildet "
            "die anteilige Nachbeschichtung/Auffrischung ab (Beschichtung hält je nach "
            "Produkt ~10-15 Jahre, umgelegt auf die Jahre).",
        "benefit_per_m2_year": "Direkter Zusatznutzen = eingesparte Kühlenergie der Räume "
            "unter dem Dach: kühlere Dachflächen senken den Kühlbedarf des obersten Geschosses "
            "um grob 5-15 kWh/m²·a; bei ~0,30 €/kWh sind das 1,50-4,50 €/m²·a → Punktwert "
            "3 €/(m²·a). Modellannahme (Größenordnung internationaler Cool-Roof-Programme), "
            "editierbar."}},
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
                 "opex_per_m2_year": "Modellannahme (Belagsunterhalt)",
                 "default_reduction": "Modellannahme (Hitzeschadens-Mechanik Fahrbahn)",
                 "benefit_per_m2_year": "Modellannahme (verlängerte Belagslebensdauer)"},
     "source_refs": {"capex_per_m2": ["Kirschbaum_HellerAsphalt"],
                     "default_reduction": ["Kirschbaum_HellerAsphalt"]},
     "source_details": {
        "default_reduction": "Wirkmechanismus: Hitzewellen verursachen Spurrinnen, Blow-ups "
            "und beschleunigte Belagsalterung; helle/hitzestabile Beläge bleiben bei hohen "
            "Oberflächentemperaturen formstabil (modifizierte Bindemittel, höhere Albedo — "
            "bis ~10-20 K kühlere Belagsoberfläche, Kirschbaum/FGSV-Umfeld). Angesetzt: 20 % "
            "Reduktion des hitze-/witterungsgetriebenen Verkehrsinfrastruktur-Schadens auf den "
            "erneuerten Flächen. Keine Kalibrierstudie — editierbare, dokumentierte Modellannahme.",
        "capex_per_m2": "Heller/hitzeresilienter Asphalt verursacht ~3-5 €/m² Mehrkosten "
            "gegenüber Normalasphalt (45-60 €/m²), also 20-50 % Aufpreis (strasse-und-"
            "autobahn.de, bauindex-online 2026). Der Katalogwert 30 €/m² bildet nicht nur den "
            "Aufpreis, sondern eine Deckschichterneuerung mit hellem/resilientem Belag ab "
            "(Teilerneuerung der Fahrbahnoberfläche); plausibilisiert. Als reiner Aufpreis "
            "wären ~3-5 €/m² anzusetzen.",
        "opex_per_m2_year": "Modellannahme: 1 €/m²/a Belagsunterhalt (Risssanierung, "
            "anteilige Erneuerung der Deckschicht über die Nutzungsdauer).",
        "benefit_per_m2_year": "Direkter Zusatznutzen = vermiedene vorgezogene Sanierung: "
            "hält die Deckschicht dank Hitzestabilität einige Jahre länger (z. B. 15 statt 12 "
            "Jahre bei ~45-60 €/m² Erneuerungskosten), entspricht das ~1-3 €/m²·a vermiedener "
            "Erneuerungsrücklage; zzgl. geringerer Flickkosten → Punktwert 3 €/(m²·a). "
            "Modellannahme, editierbar."}},
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
                 "opex_per_m2_year": "DWA-A 138 (Betrieb), auf Anlagenfläche umgerechnet",
                 "default_reduction": "DWA-A 138 (Bemessungsprinzip, Modellannahme)",
                 "benefit_per_m2_year": "Gesplittete Abwassergebühr (BWB-Größenordnung)"},
     "source_refs": {"capex_per_m2": ["DWA_A138", "Baupreislexikon_Versickerung"],
                     "opex_per_m2_year": ["DWA_A138", "Baupreislexikon_Versickerung"],
                     "default_reduction": ["DWA_A138"],
                     "benefit_per_m2_year": ["BWB_Niederschlagswasserentgelt"]},
     "source_details": {
        "default_reduction": "Wirkmechanismus: Mulden-/Rigolensysteme sind nach DWA-A 138 auf "
            "Bemessungsregen ausgelegt — sie nehmen den Oberflächenabfluss der angeschlossenen "
            "Flächen auf, bevor er Straßen/Unterführungen flutet. Bis zum Bemessungsereignis "
            "wird der Abfluss nahezu vollständig zurückgehalten, bei selteneren Extremen läuft "
            "das System über. Angesetzt: 25 % Reduktion der verkehrsbezogenen Ausfall-/"
            "hydrologischen Stressrisiken in den abgedeckten Zellen (Anlagen bedecken nur einen "
            "Teil der Zellfläche). Editierbare Modellannahme im DWA-Bemessungsprinzip.",
        "capex_per_m2": "Nach DWA-A 138 (baupreislexikon 2026) kostet eine reine "
            "Muldenversickerung 10-45 €/m² und ein kombiniertes Mulden-Rigolen-System 60-85 "
            "€/m² abflusswirksamer Fläche. Punktwert 45 €/m² liegt an der oberen Grenze der "
            "reinen Mulde bzw. am unteren Rand kombinierter Systeme.",
        "opex_per_m2_year": "Der DWA-Betriebskennwert liegt bei 0,50-0,75 €/m² "
            "abflusswirksamer (angeschlossener) Fläche. Bezogen auf die deutlich kleinere "
            "Anlagenfläche selbst (Mulde/Rigole) fällt der spezifische Unterhalt höher aus "
            "(Mahd, Entschlammung, Kontrolle) → Punktwert 2 €/m²/a.",
        "benefit_per_m2_year": "Direkter Zusatznutzen = eingespartes Niederschlagswasserentgelt "
            "der abgekoppelten Flächen (gesplittete Abwassergebühr): z. B. 1,84 €/m² "
            "versiegelte Fläche und Jahr in Berlin (BWB). Eine Mulde/Rigole entwässert das "
            "2-4-Fache ihrer eigenen Fläche → auf die Anlagenfläche bezogen ~4 €/(m²·a). "
            "Kommunal unterschiedlich, editierbar."}},
    # Herleitung capex_per_unit: keine belastbare Standardquelle für die Ertüchtigung eines
    # kritischen Verkehrsknotens (Schutz vor Überflutung/Hitze/Ausfall) — Modellannahme in
    # niedriger sechsstelliger Größenordnung je Knoten → 80.000 €.
    {"code": "CRITICAL_NODE_PROTECTION", "name": "Schutz kritischer Knoten",
     "description": "Schutzmaßnahmen für Verkehrsknoten.", "measure_type": "structural",
     "effect_target": ["exposure"], "default_reduction": 0.25, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_TRANSPORT_DISRUPTION_HOURS"],
     "capex_fixed": 0.0, "capex_per_unit": 80000.0, "capex_per_m2": None,
     "opex_fixed_year": None, "opex_per_unit_year": 1600.0, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": "Knoten", "unit_density_per_ha": 0.02,
     "source": "Modellannahme (mangels belastbarer Quelle)",
     "sources": {"capex_per_unit": "Modellannahme (mangels belastbarer Standardquelle)",
                 "opex_per_unit_year": "VDI 2067 (Instandhaltungssätze techn. Schutzeinrichtungen)",
                 "default_reduction": "BBK-Objektschutz-Prinzip (Größenordnung, Modellannahme)",
                 "unit_density_per_ha": "Modellannahme (Richtwert-Dichte, unbelegt)"},
     "source_refs": {"opex_per_unit_year": ["VDI_2067_Blatt1"],
                     "default_reduction": ["BBK_Hochwasserschutzfibel", "BBK_KRITIS"]},
     "source_details": {
        "default_reduction": "Wirkmechanismus: Objektschutz am kritischen Verkehrsknoten "
            "(Flutschotts/Pumpen an Unterführungen, hitzefeste Technik, Notstrom) hält den "
            "Knoten im Ereignisfall verfügbar. Die BBK-Hochwasserschutzfibel zeigt, dass "
            "konsequenter Objektschutz die Schäden am geschützten Objekt beim Bemessungs"
            "ereignis um einen Großteil (bis ~80 %) senkt; da je Zelle nur ein Teil der "
            "Verkehrsinfrastruktur aus geschützten Knoten besteht und Extremereignisse "
            "Schutzniveaus überschreiten können, werden 25 % Reduktion der Verkehrsausfall"
            "stunden in den abgedeckten Zellen angesetzt. Editierbare Modellannahme im "
            "belegten Wirkprinzip (BBK).",
        "capex_per_unit": "Für die Ertüchtigung eines kritischen Verkehrsknotens (Schutz vor "
            "Überflutung, Hitze, Ausfall; z. B. Pumpen, Redundanz, Ertüchtigung von Unter"
            "führungen) war keine belastbare Standardquelle auffindbar. Modellannahme in "
            "niedriger sechsstelliger Größenordnung je Knoten → 80.000 €.",
        "opex_per_unit_year": "Schutztechnik erfordert laufende Funktionsprüfung und "
            "Instandhaltung (Pumpen, Schotts, Notstrom-/USV-Batterien): VDI 2067 setzt für "
            "technische Anlagen ~1-3 % der Investition pro Jahr an. 2 % von 80.000 € → "
            "1.600 €/(Knoten·a).",
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
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 0.5, "benefit_per_m2_year": 0.02,
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
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 0.5, "benefit_per_m2_year": 0.03,
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
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 0.5, "benefit_per_m2_year": 0.02,
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
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 0.02, "benefit_per_m2_year": 0.02,
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
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 0.02, "benefit_per_m2_year": 0.02,
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
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 0.2, "benefit_per_m2_year": 0.05,
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
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 0.1, "benefit_per_m2_year": 0.02,
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
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 0.3, "benefit_per_m2_year": 0.01,
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
     # default_reduction 0,25: von 0,20 angehoben gemäß Urban u. a. 2025 (ERL) — europäische
     # Evaluationsstudie: Hitzeaktionspläne senken die hitzeattributable Übersterblichkeit
     # um 25,2 % (102 Städte, 14 Länder).
     "effect_target": ["vulnerability"], "default_reduction": 0.25, "coverage_scaling": "saturating",
     "linked_risk_codes": ["EXPECTED_ANNUAL_MORTALITY", "EXPECTED_ANNUAL_MORBIDITY"],
     "capex_fixed": 100000.0, "capex_per_unit": None, "capex_per_m2": None,
     "opex_fixed_year": 20000.0, "opex_per_unit_year": None, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": None, "unit_density_per_ha": None,
     "source": "klimastadtraum.de (Praxisrichtwert) / Modellannahme",
     "sources": {"opex_fixed_year": "Modellannahme (laufende Fortschreibung/Koordination)",
                 "capex_fixed": "klimastadtraum.de (Praxisrichtwert Hitzeaktionsplan)",
                 "default_reduction": "Urban u. a. 2025 (ERL): −25,2 % Hitzemortalität"},
     "source_refs": {"default_reduction": ["Urban_HHAP_Wirksamkeit_2025"]},
     "source_details": {
        "default_reduction": "Direkt kalibriert auf die europäische Evaluationsstudie von "
            "Urban u. a. 2025 (Environmental Research Letters): Die Einführung von Hitze"
            "präventions-/Hitzeaktionsplänen war über 102 Städte in 14 Ländern (1990-2019) mit "
            "einer Reduktion der hitzeattributablen Übersterblichkeit um 25,2 % (95 %-KI "
            "19,8-31,9 %) verbunden — das entspricht exakt den hier verknüpften Risiken "
            "(Hitzemortalität/-morbidität). Wert daher von zuvor 0,20 (unbelegte Annahme) auf "
            "0,25 angehoben; angesichts des breiten Konfidenzintervalls editierbar.",
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
     "opex_fixed_year": None, "opex_per_unit_year": 800.0, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": "Raum",
     # Herleitung unit_density_per_ha: Modellannahme (mangels belastbarer Quelle) — an
     # HAP-Konzept "kühle Orte" angelehnt: ein fußläufig (~800 m Radius, ~20 ha Einzugs-
     # gebiet) erreichbarer Kühlraum je Quartier → Punktwert 0,05 Räume/ha (1 je 20 ha).
     "unit_density_per_ha": 0.05,
     "source": "Modellannahme (mangels belastbarer Quelle)",
     "sources": {"capex_per_unit": "Modellannahme (Marktpreise Klimatechnik)",
                 "opex_per_unit_year": "VDI 2067 (Wartung Klimatechnik) + Saisonbetrieb",
                 "default_reduction": "Kühle-Orte-Prinzip der Hitzeaktionspläne (Modellannahme)",
                 "unit_density_per_ha": "Modellannahme (HAP-Konzept \"kühle Orte\")"},
     "source_refs": {"opex_per_unit_year": ["VDI_2067_Blatt1"],
                     "default_reduction": ["Urban_HHAP_Wirksamkeit_2025"]},
     "source_details": {
        "default_reduction": "Wirkmechanismus: Fußläufig erreichbare gekühlte Aufenthaltsorte "
            "mit Trinkwasser senken die individuelle Hitzeexposition besonders vulnerabler "
            "Personen und damit Wärmebelastungsstunden und Hitzemortalität im Einzugsgebiet. "
            "Kühle Orte sind ein Kernbaustein der Hitzeaktionspläne, deren Gesamtpaket europaweit "
            "−25,2 % Hitzemortalität erzielt (Urban u. a. 2025); als EINZELNER Baustein wird mit "
            "18 % ein Wert knapp darunter angesetzt. Editierbare, dokumentierte Modellannahme.",
        "capex_per_unit": "Keine belastbare Primärquelle für die Herrichtung eines "
            "\"Kühlraums\" als Gesamtpaket auffindbar – daher Modellannahme. Plausibilisiert "
            "anhand Marktpreisen gewerblicher Split-Klimaanlagen 1.500–5.000 € (Gerät + "
            "Einbau, ADAC/Heizcenter 2026) zzgl. Ausstattung, Trinkwasserstation und "
            "Beschilderung ~2.000–3.000 €. Punktwert 8.000 € je hergerichtetem Raum.",
        "opex_per_unit_year": "Klimatechnik läuft nicht kostenlos: VDI-2067-Wartungssätze für "
            "Klima-/Splitgeräte (~4-6 %/a der Investition) plus Strom im Saisonbetrieb und "
            "Reinigung/Aufsicht des Raums. 10 % von 8.000 € → 800 €/(Raum·a) als "
            "Vollkosten-Punktwert des Sommerbetriebs.",
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
                 "capex_fixed": "kommunale Praxiswerte Starkregen-/Hochwasser-Frühwarnsystem",
                 "default_reduction": "WMO Early Warnings for All (Wirksamkeits-Kennzahlen)"},
     "source_refs": {"capex_fixed": ["Kommunal_Fruehwarnsystem"],
                     "opex_fixed_year": ["Kommunal_Fruehwarnsystem"],
                     "default_reduction": ["WMO_EarlyWarnings"]},
     "source_details": {
        "default_reduction": "Kalibriert auf die WMO-Kennzahlen der Initiative \"Early "
            "Warnings for All\": Eine Warnung 24 Stunden vor dem Ereignis kann die Schäden um "
            "~30 % senken; Länder mit gut ausgebauten Frühwarnsystemen haben eine um mindestens "
            "Faktor 6 geringere Katastrophenmortalität. Für die verknüpften Betroffenen-/"
            "Verletztenrisiken werden 25 % angesetzt — leicht unterhalb der WMO-Schadenszahl, "
            "weil die Wirkung von der tatsächlichen Warnkette (Erreichbarkeit, Reaktion) "
            "abhängt. Editierbar.",
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
                 "opex_per_m2_year": "Institut für Stadtgrün (Semmler 2013)",
                 "default_reduction": "Stadtklima-Kühlwirkung Grünflächen (VDI 3787)",
                 "benefit_per_m2_year": "TEEB DE (Ökosystemleistungen Stadtgrün)"},
     "source_refs": {"opex_per_m2_year": ["Semmler_Stadtgruen_2013"],
                     "default_reduction": ["VDI3787_Stadtklima", "StewartOke_LCZ_2012"],
                     "benefit_per_m2_year": ["TEEB_DE_Naturkapital"]},
     "source_details": {
        "default_reduction": "Wirkmechanismus: Grünflächen kühlen über Verdunstung und "
            "Beschattung — Parkflächen sind nachts typischerweise 1-3 K (große Parks bis "
            "~5 K) kühler als das bebaute Umfeld (VDI 3787; Stewart & Oke LCZ) und senken "
            "damit die Wärmebelastungsstunden im Umfeld. Angesetzt: 25 % Reduktion der "
            "Wärmebelastungsstunden in den begrünten Zellen — höchster Wert der baulich-"
            "grünen Hitzemaßnahmen, da Stadtgrün Beschattung UND Verdunstung kombiniert. "
            "Editierbare Modellannahme im belegten Stadtklima-Wirkprinzip.",
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
            "einer Grünfläche mittlerer Dichte.",
        "benefit_per_m2_year": "Direkter Zusatznutzen über die vermiedenen Hitzeschäden hinaus: "
            "Stadtgrün liefert quantifizierbare Ökosystemleistungen (Regenwasserrückhalt → "
            "geringeres Niederschlagswasserentgelt, Luftreinhaltung, Erholungs-/Gesundheitswert; "
            "TEEB DE beziffert städtische Ökosystemleistungen auf einige €/m²·a). Punktwert "
            "5 €/(m²·a) als konservative Summe von Rückhalte- und Erholungsnutzen; editierbar."}},
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
                 "capex_fixed": "Modellannahme (Planungsbudget; BBK-Leitfäden ohne Kostenangabe)",
                 "default_reduction": "WMO/BBK (Evakuierungswirkung, Modellannahme)"},
     "source_refs": {"default_reduction": ["WMO_EarlyWarnings", "BBK_Hochwasserschutzfibel"]},
     "source_details": {
        "default_reduction": "Wirkmechanismus: Geübte Evakuierungs- und Notfallpläne verkürzen "
            "Reaktionszeiten und senken die Zahl unvorbereitet Betroffener — laut WMO wurden "
            "2015-2022 weltweit 2,1 Mrd. Menschen dank Frühwarnung/Planung vorsorglich evakuiert; "
            "geordnete Evakuierung ist der Kernhebel gegen Personenschäden. Angesetzt: 22 % "
            "Reduktion des Betroffenen-/Evakuiertenrisikos — unterhalb des Frühwarnsystems "
            "(0,25), da Pläne ohne technisches Warnsystem nur bei rechtzeitiger Alarmierung "
            "greifen. Editierbare, dokumentierte Modellannahme.",
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
                 "opex_per_m2_year": "Planungsrechtlich – kein laufender Unterhalt",
                 "default_reduction": "Expositionsvermeidung (BBK/ROG-Prinzip, Modellannahme)"},
     "source_refs": {"default_reduction": ["BBK_Hochwasserschutzfibel"]},
     "source_details": {
        "default_reduction": "Wirkmechanismus: Expositionsvermeidung ist die wirksamste Form "
            "der Anpassung — was in der Gefahrenzone nicht (mehr) gebaut wird, kann nicht "
            "beschädigt werden (Grundprinzip von Hochwasserschutzfibel und Raumordnung). Die "
            "Wirkung entfaltet sich aber nur für NEUE Bebauung; der Bestand in der Zone bleibt "
            "exponiert. Angesetzt: 30 % Reduktion von Gebäudeschadens- und Betroffenenrisiko in "
            "den festgesetzten Zellen über den Planungshorizont (Anteil verhinderter "
            "Neubau-/Nachverdichtungsexposition). Editierbare, dokumentierte Modellannahme.",
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
                 "opex_per_m2_year": "Modellannahme (gelegentliche Gehölzpflege)",
                 "default_reduction": "Kaltluft-/Belüftungswirkung (VDI 3787)",
                 "benefit_per_m2_year": "Modellannahme (Freiraum-Ökosystemleistung)"},
     "source_refs": {"default_reduction": ["VDI3787_Stadtklima"]},
     "source_details": {
        "default_reduction": "Wirkmechanismus: Freigehaltene Kaltluftbahnen führen nächtliche "
            "Kalt-/Frischluft aus dem Umland in überwärmte Quartiere — der zentrale Belüftungs"
            "mechanismus der Stadtklimatologie (VDI 3787 Bl. 1, Kaltlufthaushalt; im UHI-Modell "
            "der δ-Term). Angesetzt: 20 % Reduktion der Wärmebelastungsstunden in den "
            "durchlüfteten Zellen — wirkt v. a. nachts (Erholungsphasen), daher unterhalb von "
            "Stadtgrün (0,25). Editierbare Modellannahme im belegten Wirkprinzip.",
        "capex_per_m2": "Die Freihaltung von Frischluftkorridoren ist überwiegend Planung und "
            "Flächensicherung (Bebauungsverzicht, gelegentliche Gehölz-/Freihaltepflege) ohne "
            "baulichen Aufwand; ein Marktkennwert existiert nicht. Punktwert 2 €/m² als "
            "niedrige Modellannahme (Planungs- und geringer Pflegeanteil).",
        "opex_per_m2_year": "Modellannahme: 0,50 €/m²/a für gelegentliche Freihalte-/"
            "Gehölzpflege der Korridore.",
        "benefit_per_m2_year": "Direkter Zusatznutzen der freigehaltenen Flächen: extensive "
            "Grün-/Freiraumnutzung (Erholung, Regenwasserversickerung, Kaltluftproduktion) in "
            "der Größenordnung niedriger Ökosystemleistungswerte → 2 €/(m²·a) als konservative "
            "Modellannahme; editierbar."}},
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
     "opex_fixed_year": None, "opex_per_unit_year": 1800.0, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": "Abschnitt",
     # Herleitung unit_density_per_ha: Modellannahme (Richtwert-Dichte) — sanierungs-
     # bedürftige Netzabschnitte je Fläche, ~1 Abschnitt (≈1 km) je 33 ha Siedlungsfläche.
     "unit_density_per_ha": 0.03,
     "source": "DVGW W 392 / energie|wasser-praxis (Netzsanierung)",
     "sources": {"capex_per_unit": "DVGW W 392 / energie|wasser-praxis (Rohrnetzsanierung €/lfm)",
                 "opex_per_unit_year": "DVGW W 392 (Wasserverlust-Monitoring) / VDI 2067",
                 "default_reduction": "DVGW W 392 (Wasserverlustmanagement, Wirkprinzip)",
                 "unit_density_per_ha": "Modellannahme (Richtwert-Dichte, unbelegt)"},
     "source_refs": {"capex_per_unit": ["DVGW_W392"],
                     "opex_per_unit_year": ["DVGW_W392", "VDI_2067_Blatt1"],
                     "default_reduction": ["DVGW_W392"]},
     "source_details": {
        "default_reduction": "Wirkmechanismus: Leckageortung und Netzsanierung nach DVGW W 392 "
            "senken die realen Wasserverluste (in Deutschland im Schnitt ~5-7 % der Netzeinspei"
            "sung, regional deutlich mehr) und erhöhen Druckstabilität und Versorgungssicherheit "
            "in Trocken-/Spitzenlastphasen; zugleich sinkt die Rohrbruchrate sanierter Abschnitte "
            "deutlich. Angesetzt: 22 % Reduktion des Versorgungsausfall-Risikos in den abgedeckten "
            "Zellen — Modellannahme im Wirkprinzip des DVGW-Wasserverlustmanagements, ohne "
            "kommunale Kalibrierstudie; editierbar.",
        "capex_per_unit": "Rohrnetzsanierung kostet in offener Bauweise (Rohrersatz) 80-150 "
            "€/lfm, im grabenlosen Inliner-Verfahren (CIPP) 50-90 €/lfm (DVGW W 392; "
            "energie|wasser-praxis 2019). Ein Sanierungs-\"Abschnitt\" entspricht rund 1 km "
            "Leitung → 50.000-150.000 €; Punktwert 90.000 € als Mittel eines gemischten "
            "Verfahrensmixes.",
        "opex_per_unit_year": "Dauerhaftes Wasserverlustmanagement je sanierten Abschnitt: "
            "kontinuierliches Monitoring (Durchfluss-/Drucksensorik, Nachtmindestverbrauchs"
            "analyse nach DVGW W 392) plus anteilige Instandhaltung. VDI-2067-Größenordnung "
            "~2 % der Investition/Jahr → 1.800 €/(Abschnitt·a).",
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
     "opex_fixed_year": None, "opex_per_unit_year": 10000.0, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
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
     "opex_fixed_year": None, "opex_per_unit_year": 3000.0, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
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
     # Früher auf das (entfernte) Gesamtschaden-EAD-Risiko verdrahtet; jetzt auf die
     # direkten monetären Sektorschäden, die eine risikobasierte Investitionssteuerung
     # nachvollziehbar mindert.
     "linked_risk_codes": ["EXPECTED_BUILDING_DAMAGE_EUR", "EXPECTED_TRANSPORT_DAMAGE_EUR",
                           "EXPECTED_ENERGY_INFRA_DAMAGE_EUR"],
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
     # Früher auf das (entfernte) Gesamtschaden-EAD-Risiko verdrahtet; jetzt auf die
     # direkten monetären Sektorschäden, auf die private Vorsorgeanreize wirken.
     "linked_risk_codes": ["EXPECTED_BUILDING_DAMAGE_EUR", "EXPECTED_RESTORATION_COSTS_EUR"],
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
     "opex_fixed_year": None, "opex_per_unit_year": 3500.0, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
     "unit_label": "Anlage", "unit_density_per_ha": 0.02,
     "source": "Modellannahme (mangels belastbarer Quelle)",
     "sources": {"capex_per_unit": "Modellannahme (anlagenspezifisch, mangels Standard-Quelle)",
                 "opex_per_unit_year": "VDI 2067 (Wartungssätze Kältetechnik) + Energie",
                 "default_reduction": "Modellannahme (Hitze-Produktivitätsschutz, dokumentiert)",
                 "unit_density_per_ha": "Modellannahme (Richtwert-Dichte, unbelegt)"},
     "source_refs": {"opex_per_unit_year": ["VDI_2067_Blatt1"]},
     "source_details": {
        "default_reduction": "Wirkmechanismus: Hitzewellen verursachen indirekte wirtschaftliche "
            "Verluste durch Produktivitätseinbußen, Prozessunterbrechungen und Kühlketten"
            "probleme in Industrie/Gewerbe; betriebliche Kühlkonzepte halten Produktions- und "
            "Arbeitsbedingungen an Hitzetagen aufrecht. Angesetzt: 18 % Reduktion des "
            "verknüpften indirekten Verlustrisikos in den abgedeckten Zellen — bewusst unterhalb "
            "der technischen Anlagen-Ertüchtigung (0,20), da Kühlkonzepte nur den Hitzeanteil "
            "der (mehrfach getriebenen) indirekten Verluste adressieren. Keine Kalibrierstudie — "
            "editierbare, dokumentierte Modellannahme.",
        "capex_per_unit": "Betriebliche Kühlkonzepte (Prozess- und Gebäudekühlung in Industrie/"
            "Gewerbe) sind stark anlagen- und branchenspezifisch; eine belastbare Standard"
            "quelle war nicht auffindbar. Modellannahme in sechsstelliger Größenordnung je "
            "ertüchtigter Anlage → 70.000 €.",
        "opex_per_unit_year": "Kältetechnik ist betriebskostenintensiv: VDI 2067 setzt für "
            "Kälteanlagen Wartung + Instandsetzung von ~4-6 % der Investition pro Jahr an, "
            "zuzüglich Stromkosten der Kühlung in Hitzeperioden. 5 % von 70.000 € → "
            "3.500 €/(Anlage·a) als Vollkosten-Punktwert.",
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
                 "capex_fixed": "Modellannahme (organisatorisch, mangels Marktkennwert)",
                 "default_reduction": "Modellannahme (Redundanz-/Pufferprinzip, dokumentiert)"},
     "source_details": {
        "default_reduction": "Wirkmechanismus: Zweitlieferanten, Sicherheitsbestände und "
            "betriebliche Notfallpläne verkürzen klimabedingte Lieferunterbrechungen (Ausweich"
            "beschaffung statt Stillstand) und dämpfen deren Folgen. Angesetzt: 20 % Reduktion "
            "der Lieferketten-Unterbrechungsstunden im abgedeckten Gebiet — organisatorische "
            "Maßnahme mit begrenzter Reichweite (externe Störungen der Vorketten bleiben), "
            "daher unterhalb baulicher Redundanzmaßnahmen. Keine Kalibrierstudie — editierbare, "
            "dokumentierte Modellannahme.",
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
                 "capex_fixed": "Modellannahme (organisatorisches Programmbudget)",
                 "default_reduction": "Urban u. a. 2025 (HHAP-Kernbaustein) / RKI-Risikogruppen"},
     "source_refs": {"default_reduction": ["Urban_HHAP_Wirksamkeit_2025", "RKI_Hitzemortalitaet"]},
     "source_details": {
        "default_reduction": "Wirkmechanismus: Hitzemortalität konzentriert sich stark auf "
            "Risikogruppen (Hochaltrige, Pflegebedürftige, Vorerkrankte — RKI/Winklmayr); "
            "aufsuchende Programme (Hitzetelefon, Pflegeheim-Protokolle, Nachbarschaftshilfe) "
            "adressieren genau diese Gruppe und sind Kernbaustein wirksamer Hitzeaktionspläne "
            "(Gesamtpaket: −25,2 % Hitzemortalität, Urban u. a. 2025). Angesetzt: 22 % Reduktion "
            "des verknüpften Mortalitäts-/Ungleichheitsrisikos — nahe an der HHAP-Gesamtwirkung, "
            "da die Zielgruppe den Großteil der Übersterblichkeit trägt. Editierbar.",
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
                 "capex_fixed": "Modellannahme (organisatorischer Einführungsaufwand)",
                 "default_reduction": "Arbeitsschutz-Wirkprinzip (Expositionsverlagerung)"},
     "source_details": {
        "default_reduction": "Wirkmechanismus: Verlagerung von Arbeits-/Außenaktivitäten aus "
            "den heißesten Tagesstunden (Vorverlegung, Siesta-Modelle, Pausenregelungen nach "
            "Arbeitsschutzregel ASR A3.5) reduziert die individuelle Expositionszeit während "
            "der Belastungsspitzen — die Wärmebelastungsstunden sinken für die erfassten "
            "Beschäftigten, nicht aber die Stadttemperatur selbst. Angesetzt: 18 % Reduktion "
            "der Wärmebelastungsstunden im abgedeckten Gebiet (nur werktätige Teilpopulation, "
            "verhaltensabhängig). Editierbare, dokumentierte Modellannahme.",
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
                 "opex_per_m2_year": "Modellannahme (mangels belastbarer Quelle)",
                 "default_reduction": "Beschattungs-Wirkprinzip (UTCI/gefühlte Temperatur)",
                 "benefit_per_m2_year": "Modellannahme (Aufenthaltsqualität öffentl. Raum)"},
     "source_refs": {"default_reduction": ["VDI3787_Stadtklima"]},
     "source_details": {
        "default_reduction": "Wirkmechanismus: Beschattung senkt die Strahlungstemperatur "
            "(UTCI/gefühlte Temperatur im Schatten mehrere Kelvin unter besonnten Flächen, "
            "Stadtklimatologie/VDI 3787) und Wasserflächen kühlen lokal durch Verdunstung; "
            "Trink-/Abkühlmöglichkeiten senken die individuelle Belastung. Angesetzt: 18 % "
            "Reduktion der Wärmebelastungsstunden auf den ausgestatteten Flächen — punktuelle "
            "Wirkung an Aufenthaltsorten, daher unterhalb flächiger Begrünung (0,25). "
            "Editierbare, dokumentierte Modellannahme.",
        "capex_per_m2": "Keine belastbare €/m²-Quelle für die Mischmaßnahme \"Schatten/Wasser\" "
            "auffindbar – daher Modellannahme. Die Einzelkomponenten (Sonnensegel-Masten "
            "~160–350 €/Stück, Sonnensegel ab ~70 €/Stück, sonnensegel-guru.de 2026; "
            "Wasserspielplatz Stuttgart Südheimer Platz ~230.000 € Gesamtinvestition ohne "
            "Flächenangabe) bestätigen nur die Größenordnung, ergeben aber keinen sauberen "
            "Flächenkennwert. Punktwert 35 €/m² als Größenordnungs-Schätzung.",
        "opex_per_m2_year": "Modellannahme mangels belastbarer Quelle; 2 €/m²/a als "
            "grober Unterhalt für Beschattungs-/Wasserelemente im öffentlichen Raum "
            "(Reinigung, Wartung, Winterlagerung von Segeln).",
        "benefit_per_m2_year": "Direkter Zusatznutzen: nutzbarer öffentlicher Raum auch an "
            "Hitzetagen (Aufenthaltsqualität, Belebung/Einzelhandelsumfeld, Spielwert von "
            "Wasserelementen) in der Größenordnung niedriger Freiraum-Nutzwerte → 3 €/(m²·a) "
            "als konservative Modellannahme; editierbar."}},
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
     "opex_fixed_year": None, "opex_per_unit_year": 3000.0, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
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
     "opex_fixed_year": None, "opex_per_unit_year": 4000.0, "opex_per_m2_year": None, "benefit_per_m2_year": 0.0,
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
     "opex_fixed_year": None, "opex_per_unit_year": None, "opex_per_m2_year": 0.5, "benefit_per_m2_year": 0.02,
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
                 "opex_per_unit_year": "Berliner Wasserbetriebe",
                 "default_reduction": "Modellannahme (Einzelbaustein Hitzevorsorge)",
                 "unit_density_per_ha": "Modellannahme (Innenstadt-Versorgungsdichte)"},
     "source_refs": {"capex_per_unit": ["BWB_Trinkbrunnen"],
                     "opex_per_unit_year": ["BWB_Trinkbrunnen"],
                     "default_reduction": ["Urban_HHAP_Wirksamkeit_2025"]},
     "source_details": {
        "default_reduction": "Wirkmechanismus: Öffentlich zugängliches Trinkwasser beugt "
            "Dehydrierung vor — dem zentralen Pfad hitzebedingter Notfälle — und ist Standard"
            "empfehlung aller Hitzeaktionspläne. Als EINZELNER, punktueller Baustein wird mit "
            "10 % bewusst der niedrigste Wert aller Hitzemaßnahmen angesetzt (das HHAP-"
            "Gesamtpaket erreicht −25,2 %, Urban u. a. 2025; ein Brunnen allein leistet davon "
            "nur einen kleinen Teil). Editierbare, dokumentierte Modellannahme.",
        "unit_density_per_ha": "Modellannahme: 0,5 Brunnen/ha entspricht etwa einem Trink"
            "brunnen je 2 ha hochfrequentierter Innenstadt-/Aufenthaltsfläche (~140 m "
            "Abstandsraster) — Versorgungsdichte, wie sie Hitzeaktionspläne für Fußgänger"
            "bereiche anstreben; für Wohngebiete wäre die Dichte geringer zu wählen.",
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


def _fmt_eur_de(value: float) -> str:
    """1234567.0 → "1.234.567" (deutsches Tausenderformat, ohne Nachkommastellen)."""
    if value == int(value):
        return f"{int(value):,}".replace(",", ".")
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _enrich_measure_zero_cost_docs() -> None:
    """Herleitung für bewusste 0-Werte des Maßnahmen-Kostenmodells (je Maßnahme).

    Nutzeranforderung: Auch eine 0 braucht einen Infokasten, der erklärt, WARUM sie 0
    ist. Die Texte sind maßnahmen-spezifisch (nennen den tatsächlichen Kostenträger der
    Maßnahme) und werden nur gesetzt, wo noch keine handgeschriebene Herleitung existiert
    — individuelle ``source_details``-Einträge (z. B. Netzverstärkung) haben Vorrang.
    """
    for m in MEASURES:
        sources_map = m.setdefault("sources", {})
        details = m.setdefault("source_details", {})

        # capex_fixed == 0: Kosten skalieren vollständig über Stück-/Flächenkostensätze.
        if m.get("capex_fixed") == 0.0 and not details.get("capex_fixed"):
            unit_label = m.get("unit_label") or "Stück"
            carriers: list[str] = []
            if m.get("capex_per_unit"):
                carriers.append(
                    f"Stückkostensatz ({_fmt_eur_de(m['capex_per_unit'])} €/{unit_label})")
            if m.get("capex_per_m2"):
                carriers.append(
                    f"Flächenkostensatz ({_fmt_eur_de(m['capex_per_m2'])} €/m²)")
            if carriers:
                detail = (
                    "0 € ist bewusst gesetzt: Diese Maßnahme hat keinen investiven "
                    f"Sockelbetrag — die Investition skaliert vollständig über den "
                    f"{' und den '.join(carriers)} dieser Maßnahme; Planungs-/Nebenkosten "
                    "sind in diesen Einheitssätzen einkalkuliert. Ein zusätzlicher "
                    "Grundkosten-Betrag würde im MECE-Kostenmodell (CAPEX = fix + "
                    "Anzahl × Stücksatz + Fläche × Flächensatz) doppelt zählen. Editierbar, "
                    "falls die Kommune ein separates Planungs-/Grundbudget ansetzen will."
                )
            elif m.get("opex_fixed_year"):
                detail = (
                    "0 € ist bewusst gesetzt: Diese organisatorische Maßnahme erfordert "
                    "keine Bauinvestition; ihr Aufwand ist als laufende feste "
                    f"Betriebskosten ({_fmt_eur_de(m['opex_fixed_year'])} €/Jahr, "
                    "opex_fixed_year) modelliert. Editierbar, falls einmalige "
                    "Aufbaukosten (z. B. Erstkonzept) separat budgetiert werden."
                )
            else:
                detail = (
                    "0 € ist bewusst gesetzt: Die Maßnahme wirkt planungsrechtlich/"
                    "organisatorisch ohne modellierte Bauinvestition; der geringe "
                    "Verwaltungsaufwand ist nicht als eigener Kostenblock angesetzt. "
                    "Editierbar, falls die Kommune Umsetzungskosten budgetieren will."
                )
            details["capex_fixed"] = detail
            sources_map.setdefault(
                "capex_fixed", "Modellentscheidung (Kostenstruktur, dokumentiert)")

        # benefit_per_m2_year == 0: Hauptnutzen läuft über vermiedene Schäden (E3),
        # nicht über dieses Feld — sonst Doppelzählung.
        if m.get("benefit_per_m2_year") == 0.0 and not details.get("benefit_per_m2_year"):
            details["benefit_per_m2_year"] = (
                "0 €/(m²·a) ist bewusst gesetzt: Der Hauptnutzen der Maßnahme — vermiedene "
                "Klimaschäden — wird NICHT über dieses Feld gerechnet, sondern als "
                "Reduktion der Zellschadenskosten der verknüpften Risiken "
                "(Risikoreduktion × Zellkosten, measure_service). Dieses Feld bildet nur "
                "direkte marktfähige Zusatznutzen ab (z. B. Energieertrag, eingesparte "
                "Wasser-/Energiekosten). Für diese Maßnahme ist kein solcher "
                "flächenbezogener Zusatznutzen belegt — ein Wert > 0 ohne Beleg wäre eine "
                "Doppelzählung des Schadensnutzens."
            )
            sources_map.setdefault(
                "benefit_per_m2_year", "Modellentscheidung (Nutzen-Abgrenzung, dokumentiert)")


_enrich_measure_zero_cost_docs()


# ── Wirkungs-/Nutzen-Herleitungen je Maßnahme (Parameter-Vollerklärung) ─────────
# Je Eintrag: Feld → (Quellen-Kurzlabel, [Bibliografie-Keys], Herleitungstext).
# Zentrale Datenstruktur statt Inline-Edit je Maßnahme; Inline-``source_details``
# in den Maßnahmen-Dicts haben Vorrang (werden hier nicht überschrieben).
_MEASURE_EFFECT_DOCS: dict[str, dict[str, tuple[str, list[str], str]]] = {
    # ── Wasser/Starkregen ────────────────────────────────────────────────────────
    "DESEALING_SURFACE": {
        "default_reduction": ("Entsiegelungs-Wirkprinzip (Abflussbeiwert)", ["Bremen_Entsiegelung", "DWA_A138"],
            "Wirkmechanismus: Entsiegelung stellt die natürliche Versickerung wieder her — der "
            "Abflussbeiwert sinkt von ~0,9 (Asphalt/Beton) auf ~0,1-0,3 (begrünte Fläche), d. h. "
            "60-80 % des Oberflächenabflusses der entsiegelten Fläche entfallen (DWA-A-138-"
            "Kennwerte; Bremer Entsiegelungsprogramm). Zusätzlich kühlt die Fläche und speist "
            "Grundwasser. Angesetzt: 30 % Reduktion der verknüpften Überflutungs-/Hitzerisiken "
            "in den entsiegelten Zellen. Editierbare Modellannahme im belegten Wirkprinzip."),
        "benefit_per_m2_year": ("Gesplittete Abwassergebühr + Ökosystemleistung", ["BWB_Niederschlagswasserentgelt", "TEEB_DE_Naturkapital"],
            "Direkter Zusatznutzen: Entsiegelte Flächen entfallen aus dem Niederschlagswasser"
            "entgelt (z. B. 1,84 €/m²·a in Berlin, BWB) und erbringen Ökosystemleistungen "
            "(Versickerung, Kühlung, Grün; TEEB DE einige €/m²·a) → Punktwert 5 €/(m²·a). "
            "Kommunal unterschiedlich, editierbar."),
    },
    "SPONGE_CITY": {
        "default_reduction": ("Schwammstadt-Prinzip (RISA/DWA-Bemessung)", ["DWA_A138"],
            "Wirkmechanismus: Schwammstadt-Bündel (Entsiegelung, Mulden/Rigolen, Baumrigolen, "
            "Retentionsflächen) halten Niederschlag dezentral zurück und verdunsten ihn — "
            "bemessen nach DWA-A 138 nimmt das System Regen bis zum Bemessungsereignis nahezu "
            "vollständig auf und dämpft zugleich Hitze über Verdunstung. Angesetzt: 30 % "
            "Reduktion der verknüpften Überflutungs-/Gebäudeschadensrisiken in den umgestalteten "
            "Zellen (oberer Bereich der Flächenmaßnahmen, da Maßnahmenbündel). Editierbare "
            "Modellannahme im DWA-Bemessungsprinzip."),
        "benefit_per_m2_year": ("Gesplittete Abwassergebühr + Stadtgrün-Nutzen", ["BWB_Niederschlagswasserentgelt", "TEEB_DE_Naturkapital"],
            "Direkter Zusatznutzen: abgekoppelte Flächen sparen Niederschlagswasserentgelt "
            "(1,84 €/m²·a Berlin, BWB; bei Versickerung −50 bis −100 % der Gebühr) plus Grün-/"
            "Aufenthaltsnutzen der blau-grünen Elemente (TEEB DE) → 5 €/(m²·a); editierbar."),
    },
    "RETENTION_STORAGE": {
        "default_reduction": ("Retentions-Bemessung (DWA)", ["DWA_A138", "Agrarheute_Rueckhaltebecken"],
            "Wirkmechanismus: Rückhaltebecken/-flächen kappen die Abflussspitze — bis zur "
            "Bemessungsgröße wird der Scheitel vollständig zwischengespeichert und gedrosselt "
            "abgegeben (DWA-Regelwerk). Angesetzt: 28 % Reduktion der verknüpften Überflutungs"
            "risiken in den geschützten Zellen — knapp unter Mulden-Rigolen-Systemen, da "
            "zentrale Becken nur den kanalisierten Abfluss erfassen (wilder Abfluss bleibt). "
            "Editierbare Modellannahme im Bemessungsprinzip."),
        "benefit_per_m2_year": ("Gesplittete Abwassergebühr (angeschl. Flächen)", ["BWB_Niederschlagswasserentgelt"],
            "Direkter Zusatznutzen: Für die an die Retention angeschlossenen, abgekoppelten "
            "Flächen entfällt Niederschlagswasserentgelt (1,84 €/m²·a Berlin, BWB); auf die "
            "Beckenfläche bezogen (Einzugsfläche ≫ Beckenfläche) → 4 €/(m²·a). Editierbar."),
    },
    "RETENTION_POLDER_RESERVOIR": {
        "default_reduction": ("Polder-Scheitelkappung (Praxisnachweis)", ["Agrarheute_Rueckhaltebecken", "UBA_Gewaesserrenaturierung"],
            "Wirkmechanismus: Flutpolder und Speicherbecken kappen Hochwasserscheitel "
            "nachweislich — gesteuerte Polder senken den Scheitel des Bemessungshochwassers "
            "am Unterlieger messbar (Praxis der Länder-Hochwasserschutzprogramme). Angesetzt: "
            "30 % Reduktion der verknüpften Hochwasserrisiken in den geschützten Zellen; "
            "Extremereignisse jenseits des Poldervolumens bleiben (Restrisiko). Editierbare "
            "Modellannahme im belegten Wirkprinzip."),
        "benefit_per_m2_year": ("Modellannahme (Doppelnutzung Polderfläche)", [],
            "Direkter Zusatznutzen: Polder-/Speicherflächen sind außerhalb von Einstauereignissen "
            "land-/grünlandwirtschaftlich nutzbar und können Brauch-/Bewässerungswasser "
            "bereitstellen → 4 €/(m²·a) als konservative Doppelnutzungs-Annahme; editierbar."),
    },
    "INFILTRATION_AREAS": {
        "default_reduction": ("Versickerungs-Bemessung (DWA-A 138)", ["DWA_A138"],
            "Wirkmechanismus: Dezentrale Versickerungsflächen nehmen den Abfluss angeschlossener "
            "Flächen auf und führen ihn dem Grundwasser zu — nach DWA-A 138 auf das Bemessungs"
            "ereignis dimensioniert. Angesetzt: 25 % Reduktion der verknüpften Überflutungs-/"
            "hydrologischen Risiken in den abgedeckten Zellen (wie Mulden-Rigolen). Editierbare "
            "Modellannahme im DWA-Bemessungsprinzip."),
        "benefit_per_m2_year": ("Gesplittete Abwassergebühr", ["BWB_Niederschlagswasserentgelt"],
            "Direkter Zusatznutzen: abgekoppelte, versickernde Flächen sparen Niederschlags"
            "wasserentgelt (1,84 €/m²·a Berlin; ermäßigt −50 % bei bestimmten Versickerungs"
            "arten, BWB) → 3 €/(m²·a) bezogen auf die Anlagenfläche. Editierbar."),
    },
    "RUNOFF_ROUTING_DGM": {
        "default_reduction": ("Starkregen-Gefahrenkarten-Praxis (Notwasserwege)", ["DWA_A138"],
            "Wirkmechanismus: DGM-basierte Abflusslenkung (Notwasserwege, Bordsteine, "
            "Geländemodellierung) leitet den nicht mehr rückhaltbaren Extremabfluss gezielt "
            "über schadarme Korridore ab — Standardbaustein kommunaler Starkregen-Gefahren"
            "kartenkonzepte ergänzend zur DWA-Bemessung. Angesetzt: 20 % Reduktion der "
            "verknüpften Überflutungsrisiken (lenkt, speichert aber nicht). Editierbare, "
            "dokumentierte Modellannahme."),
        "benefit_per_m2_year": ("Modellannahme (multifunktionale Flächen)", [],
            "Direkter Zusatznutzen: Notwasserwege/multifunktionale Retentionsflächen sind im "
            "Normalfall als Straßenraum, Grün- oder Spielfläche nutzbar → 2 €/(m²·a) als "
            "konservative Mehrfachnutzungs-Annahme; editierbar."),
    },
    "GROUNDWATER_RECHARGE": {
        "default_reduction": ("Dargebotssicherung (DVGW-Wirkprinzip)", ["DVGW_W392"],
            "Wirkmechanismus: Gezielte Grundwasseranreicherung (Versickerung von Überschuss"
            "wasser, Uferfiltrat-Management) stützt das nutzbare Dargebot und die Grundwasser"
            "stände in Trockenperioden — der Puffer senkt hydrologischen Stress und Nutzungs"
            "konflikte in Dürrejahren. Angesetzt: 20 % Reduktion der verknüpften Wasser"
            "stressrisiken in den Anreicherungsgebieten. Editierbare, dokumentierte "
            "Modellannahme (Wirkung stark standortabhängig, Hydrogeologie)."),
        "benefit_per_m2_year": ("Modellannahme (gesichertes Rohwasser)", [],
            "Direkter Zusatznutzen: stabilere Rohwasserverfügbarkeit der Wasserversorgung "
            "(vermiedene Ersatzbeschaffung/Fernwasser in Dürrejahren) → 2 €/(m²·a) bezogen "
            "auf die Anreicherungsfläche; konservative Modellannahme, editierbar."),
    },
    # ── Gebäude/Begrünung ────────────────────────────────────────────────────────
    "GREEN_ROOFS_FACADES": {
        "default_reduction": ("BuGG (Retention/Kühlwirkung Gebäudegrün)", ["BuGG_Marktreport_2024", "co2online_Dachbegruenung"],
            "Wirkmechanismus: Extensive Gründächer halten 50-90 % des Jahresniederschlags "
            "zurück (BuGG) und senken die sommerliche Aufheizung des Gebäudes und der Umgebung "
            "(Verdunstung + Dämmwirkung; co2online). Auf die verknüpften Risiken (Wärme"
            "belastung, Gebäudeschäden) wirkt nur der begrünte Flächenanteil der Zelle → 18 % "
            "Reduktion angesetzt. Editierbare Modellannahme im belegten Wirkprinzip."),
        "benefit_per_m2_year": ("co2online/BuGG (Energie) + gespl. Abwassergebühr", ["co2online_Dachbegruenung", "BWB_Niederschlagswasserentgelt"],
            "Direkter Zusatznutzen: Dämm-/Kühlwirkung spart Heiz- und Kühlenergie (co2online: "
            "spürbare Reduktion des Energiebedarfs der obersten Geschosse, grob 2-5 €/m²·a) "
            "und Gründächer mindern das Niederschlagswasserentgelt (Berlin: −50 % von "
            "1,84 €/m²·a, BWB) zzgl. verlängerter Dachlebensdauer → Punktwert 6 €/(m²·a). "
            "Editierbar."),
    },
    "FLOOD_PROTECTION_BUILDING": {
        "default_reduction": ("BBK-Hochwasserschutzfibel (Objektschutz)", ["BBK_Hochwasserschutzfibel"],
            "Wirkmechanismus: Objektschutz am Gebäude (Rückstauklappen, druckdichte Fenster/"
            "Schotts, Abdichtung, angepasste Haustechnik) verhindert das Eindringen von Wasser "
            "bis zum Bemessungsniveau — die BBK-Hochwasserschutzfibel weist für konsequenten "
            "Objektschutz Schadensminderungen bis ~80 % am Einzelgebäude aus. Da je Zelle nur "
            "ein Teil der Gebäude nachgerüstet wird und Extremereignisse Schutzhöhen "
            "überschreiten, werden 35 % Reduktion des Gebäudeschadensrisikos angesetzt — "
            "höchster Wert der Gebäudemaßnahmen. Editierbar (BBK-Wirkprinzip)."),
        "benefit_per_m2_year": ("Modellannahme (Versicherbarkeit/Prämien)", [],
            "Direkter Zusatznutzen: Objektgeschützte Gebäude erreichen bessere Versicherbarkeit "
            "und niedrigere Elementarschaden-Prämien/Selbstbehalte (GDV-Zonierungslogik ZÜRS); "
            "grob 5-10 €/m² Wohnfläche·a Prämienvorteil in gefährdeten Lagen → Punktwert "
            "9 €/(m²·a) auf die geschützte Grundfläche. Modellannahme, editierbar."),
    },
    # ── Küste/Fluss/Boden ────────────────────────────────────────────────────────
    "LEVEE_REINFORCEMENT": {
        "default_reduction": ("NLWKN Generalplan (Bemessungsschutz)", ["NLWKN_Generalplan_Kuestenschutz"],
            "Wirkmechanismus: Deicherhöhung/-verstärkung stellt den Schutz auf das Bemessungs"
            "hochwasser (Küste: Bemessungswasserstand + Wellenauflauf, NLWKN-Generalplan) "
            "wieder her — hinter einem intakten Bemessungsdeich sinkt die Überflutungswahr"
            "scheinlichkeit drastisch. Angesetzt: 35 % Reduktion der verknüpften Hochwasser-/"
            "Sturmflutrisiken in den geschützten Zellen — bewusst nicht höher, weil Deiche "
            "binär versagen können (Versagensrisiko jenseits der Bemessung, Restrisiko-"
            "Prinzip). Editierbar."),
        "opex_per_unit_year": ("NLWKN/Länderpraxis (Deichunterhaltung)", ["NLWKN_Generalplan_Kuestenschutz", "VDI_2067_Blatt1"],
            "Deichunterhaltung ist Daueraufgabe (Mahd/Beweidung, Grasnarben-/Wühltierkontrolle, "
            "Deichschau, kleinere Instandsetzungen): Länderpraxis liegt in der Größenordnung "
            "5.000-15.000 €/km·a je nach Deichtyp. Punktwert 10.000 €/(km·a) ≈ 0,8 % der "
            "Investition — ohne diesen Posten wäre der Deich unrealistisch unterhaltsfrei."),
    },
    "SALTWATER_BARRIERS": {
        "default_reduction": ("Küstenschutz-Wirkprinzip (Sperrwerke/Siele)", ["NLWKN_Generalplan_Kuestenschutz"],
            "Wirkmechanismus: Sperrwerke, Siele und Rückschlagklappen blockieren das Eindringen "
            "von Salzwasser in Vorfluter und Entwässerungssysteme bei Sturmflut/hohen Tiden — "
            "Standardbausteine des Küstenschutzes (NLWKN). Angesetzt: 25 % Reduktion des "
            "Salzwasserintrusions-Risikos im geschützten Einzugsbereich; die schleichende "
            "Intrusion über Grundwasserleiter wird nur teilweise erfasst. Editierbare, "
            "dokumentierte Modellannahme."),
        "opex_per_unit_year": ("VDI 2067 (bewegl. Verschlussorgane)", ["VDI_2067_Blatt1", "NLWKN_Generalplan_Kuestenschutz"],
            "Bewegliche Verschlussorgane (Tore, Klappen, Antriebe) erfordern Wartung, Funktions"
            "proben und Korrosionsschutz: VDI-2067-Größenordnung ~2 % der Investition/Jahr → "
            "3.000 €/(Anlage·a) bei 150.000 € Investition."),
    },
    "EROSION_PROTECTION": {
        "default_reduction": ("LfL (konservierende Bodenbearbeitung/ABAG)", ["LfL_Pflanzenbau"],
            "Wirkmechanismus: Erosionsschutz (Begrünung, Zwischenfrüchte, konservierende "
            "Bearbeitung, Hangrinnen-Begrünung) senkt den Bodenabtrag über den Bedeckungs- und "
            "Bearbeitungsfaktor der Allgemeinen Bodenabtragsgleichung (ABAG) — konservierende "
            "Verfahren reduzieren den C-Faktor und damit den Abtrag um deutlich über 50 % "
            "(LfL-Pflanzenbau-Kennwerte). Angesetzt: 25 % Reduktion der verknüpften Erosions-/"
            "Bodenrisiken (nicht alle Flächen/Kulturen umstellbar). Editierbar."),
        "benefit_per_m2_year": ("Modellannahme (erhaltene Bodenfruchtbarkeit)", ["TEEB_DE_Naturkapital"],
            "Direkter Zusatznutzen: vermiedener Verlust an Bodenfruchtbarkeit und Nährstoffen "
            "(Oberboden-Neubildung dauert Jahrhunderte; TEEB DE bewertet Bodenfunktionen) "
            "0,02 €/(m²·a) = 200 €/ha·a als Werterhalt je Hektar Ackerfläche — von zuvor "
            "2 €/m² (= 20.000 €/ha, unplausibel) herabgesetzt; editierbar."),
    },
    "FLOODPLAIN_RENATURATION": {
        "default_reduction": ("UBA (Gewässer-/Auenrenaturierung)", ["UBA_Gewaesserrenaturierung"],
            "Wirkmechanismus: Reaktivierte Auen und rückverlegte Deiche geben dem Fluss "
            "Retentionsraum zurück — der Hochwasserscheitel wird gedämpft und verzögert "
            "(UBA-Renaturierungsleitfäden; Praxis der Aktionsprogramme an Elbe/Rhein). "
            "Angesetzt: 30 % Reduktion der verknüpften Hochwasserrisiken für die profitierenden "
            "Zellen; wirkt zusätzlich als Dürre-Puffer (Grundwasserstützung). Editierbare "
            "Modellannahme im belegten Wirkprinzip."),
        "benefit_per_m2_year": ("TEEB DE / UBA (Auen-Ökosystemleistungen)", ["TEEB_DE_Naturkapital", "UBA_Gewaesserrenaturierung"],
            "Direkter Zusatznutzen: intakte Auen liefern Ökosystemleistungen (Nährstoff"
            "rückhalt, Kohlenstoffspeicherung, Habitat/Erholung), die TEEB DE für Auen mit "
            "mehreren hundert €/ha·a bewertet. 0,03 €/(m²·a) = 300 €/ha·a entspricht dieser "
            "Spanne — von zuvor 3 €/m² (= 30.000 €/ha, unplausibel) herabgesetzt; editierbar."),
    },
    # ── Land-/Forstwirtschaft ────────────────────────────────────────────────────
    "MIXED_FORESTS": {
        "default_reduction": ("AGDW/Waldumbau (Mischbestands-Resilienz)", ["AGDW_Wiederbewaldung"],
            "Wirkmechanismus: Standortgerechte Mischbestände sind gegenüber Dürre, Sturmwurf, "
            "Borkenkäfer und Kronenfeuer deutlich widerstandsfähiger als Nadel-Reinbestände — "
            "der Kern der Wiederbewaldungs-/Waldumbauprogramme nach den Dürrejahren 2018-2020 "
            "(AGDW; Waldzustandserhebungen zeigen die höchsten Schäden in Fichten-Monokulturen). "
            "Angesetzt: 25 % Reduktion der verknüpften Wald-/Feuerrisiken auf den umgebauten "
            "Flächen über den Bestandszyklus. Editierbare Modellannahme."),
        "benefit_per_m2_year": ("Modellannahme (stabilere Erträge/Senke)", ["TEEB_DE_Naturkapital"],
            "Direkter Zusatznutzen: stabilere Holzerträge (geringere Kalamitätsverluste) und "
            "kontinuierliche Senken-/Ökosystemleistung des Waldes (TEEB DE bewertet Wald-"
            "Ökosystemleistungen mit mehreren hundert €/ha·a). 0,02 €/(m²·a) = 200 €/ha·a "
            "innerhalb der TEEB-Spanne — von zuvor 1,5 €/m² (= 15.000 €/ha, unplausibel) "
            "herabgesetzt; editierbar."),
    },
    "HUMUS_BUILDUP": {
        "default_reduction": ("LfL (Humus-Wasserspeicher)", ["LfL_Pflanzenbau"],
            "Wirkmechanismus: Humusaufbau (Zwischenfrüchte, Mulch, organische Düngung) erhöht "
            "die nutzbare Feldkapazität — je zusätzlichem Prozent Humus speichert der Boden "
            "grob 20-40 mm mehr pflanzenverfügbares Wasser (LfL-Kennwerte) und übersteht "
            "Trockenphasen länger. Angesetzt: 15 % Reduktion der verknüpften Dürre-/Boden"
            "risiken auf den aufgebauten Flächen — bewusst niedrig, da Humusaufbau Jahre "
            "braucht und langsam wirkt. Editierbar."),
        "benefit_per_m2_year": ("KTBL/LfL (Ertragsstabilität)", ["LfL_Pflanzenbau", "KTBL_Feldbewaesserung"],
            "Direkter Zusatznutzen: stabilere Erträge in Trockenjahren und eingesparte "
            "Düngung/Bewässerung (bessere Nährstoff- und Wasserhaltung; KTBL/LfL) → "
            "0,02 €/(m²·a) = 200 €/ha·a als Deckungsbeitrags-Vorteil in Trockenjahren — von "
            "zuvor 1,5 €/m² (= 15.000 €/ha, unplausibel) herabgesetzt; editierbar."),
    },
    "DROUGHT_RESISTANT_VARIETIES": {
        "default_reduction": ("LfL-Sortenversuche (Trockentoleranz)", ["LfL_Pflanzenbau"],
            "Wirkmechanismus: Trockentolerante Arten/Sorten (tiefwurzelnd, hitzetolerant, "
            "früh abreifend) halten die Ertragsbildung in Trockenjahren länger aufrecht — "
            "die LfL-Sortenversuche zeigen in Dürrejahren deutliche Ertragsunterschiede "
            "zwischen Sorten derselben Kultur. Angesetzt: 18 % Reduktion des dürregetriebenen "
            "Ertragsrisikos auf den umgestellten Flächen. Editierbare Modellannahme."),
        "benefit_per_m2_year": ("Modellannahme (Ertragsstabilität)", ["LfL_Pflanzenbau"],
            "Direkter Zusatznutzen: stabilere Erträge/Qualitäten in Trockenjahren ohne "
            "nennenswerte Mehrkosten des Saatguts. 0,02 €/(m²·a) = 200 €/ha·a als vorsichtiger "
            "Deckungsbeitrags-Vorteil im Feldmaßstab — von zuvor 1,5 €/m² (= 15.000 €/ha, "
            "unplausibel) herabgesetzt; editierbar."),
    },
    "WATER_STORAGE_EFFICIENT_IRRIGATION": {
        "default_reduction": ("KTBL (Tröpfchenbewässerung/Speicher)", ["KTBL_Feldbewaesserung"],
            "Wirkmechanismus: Effiziente Bewässerung (Tropf-/Mikrobewässerung spart gegenüber "
            "Beregnung 30-50 % Wasser, KTBL) kombiniert mit Speicherbecken überbrückt "
            "Trockenphasen und Entnahmeverbote — der Ertrag bleibt auch bei Niedrigwasser "
            "gesichert. Angesetzt: 22 % Reduktion des dürregetriebenen Ertragsrisikos auf den "
            "erschlossenen Flächen. Editierbare Modellannahme auf KTBL-Basis."),
        "benefit_per_m2_year": ("KTBL (Wasser-/Energieeinsparung)", ["KTBL_Feldbewaesserung"],
            "Direkter Zusatznutzen: 30-50 % geringerer Wasser- und Pumpenergieeinsatz "
            "gegenüber konventioneller Beregnung (KTBL: Bewässerung kostet mehrere hundert "
            "€/ha·a). 0,05 €/(m²·a) = 500 €/ha·a Einsparung bewässerungsintensiver Kulturen — "
            "von zuvor 2 €/m² (= 20.000 €/ha, unplausibel) herabgesetzt; editierbar."),
    },
    "WILDFIRE_PREVENTION": {
        "default_reduction": ("Waldbrandprävention (Länderpraxis)", ["AGDW_Wiederbewaldung"],
            "Wirkmechanismus: Waldbrandprävention (Brandschutzstreifen, Totholz-/Streu-"
            "Management, Löschwasserentnahmestellen, Früherkennung) senkt Zündwahrschein"
            "lichkeit und v. a. die Ausbreitungsgeschwindigkeit — kleingehaltene Brände "
            "statt Großfeuer (Waldbrandschutzkonzepte der Länder; Laub-/Mischwaldanteil "
            "wirkt zusätzlich brandhemmend, AGDW). Angesetzt: 25 % Reduktion des Waldbrand"
            "risikos in den gemanagten Zellen. Editierbare, dokumentierte Modellannahme."),
        "benefit_per_m2_year": ("Modellannahme (erhaltener Waldwert)", ["TEEB_DE_Naturkapital"],
            "Direkter Zusatznutzen: anteiliger Werterhalt von Holzvorrat und Waldfunktionen "
            "auch ohne Brandereignis (Versicherbarkeit, kontinuierliche Ökosystemleistung; "
            "TEEB DE). 0,01 €/(m²·a) = 100 €/ha·a — von zuvor 1 €/m² (= 10.000 €/ha, "
            "unplausibel) herabgesetzt; editierbar."),
    },
    "HABITAT_CONNECTIVITY": {
        "default_reduction": ("BfN-Biotopverbund-Prinzip", ["TEEB_DE_Naturkapital"],
            "Wirkmechanismus: Biotopverbund (Trittsteine, Korridore, Hecken) ermöglicht Arten "
            "das Ausweichen und Nachwandern bei Klimastress — fragmentierte Populationen "
            "sterben lokal aus, vernetzte können sich verschieben (Kernargument des bundes"
            "weiten Biotopverbunds nach § 21 BNatSchG). Angesetzt: 20 % Reduktion der "
            "verknüpften Biodiversitäts-/Fragmentierungsrisiken in den vernetzten Zellen. "
            "Editierbare, dokumentierte Modellannahme."),
        "benefit_per_m2_year": ("TEEB DE (Leistungen vernetzter Flächen)", ["TEEB_DE_Naturkapital"],
            "Direkter Zusatznutzen: Verbundstrukturen (Hecken, Säume) liefern Bestäubung, "
            "Schädlingsregulation, Windschutz und Erosionsminderung für angrenzende Nutz"
            "flächen (TEEB DE). 0,02 €/(m²·a) = 200 €/ha·a der Verbundfläche — von zuvor "
            "1,5 €/m² (= 15.000 €/ha, unplausibel) herabgesetzt; editierbar."),
    },
    # ── Fischerei/Aquakultur & Anreizprogramme ──────────────────────────────────
    "ADAPTIVE_FISHERIES_MANAGEMENT": {
        "default_reduction": ("Modellannahme (Befischungsdruck als Stellhebel)", [],
            "Wirkmechanismus: Unter Wärme-/Sauerstoffstress ist der Befischungsdruck der am "
            "schnellsten steuerbare Stressor — angepasste Fangquoten, Schonzeiten in Hitze"
            "phasen und Echtzeit-Monitoring senken die Gesamtbelastung der Bestände und "
            "sichern die Reproduktion. Angesetzt: 20 % Reduktion des Bestandsstress-/Ertrags"
            "risikos im bewirtschafteten Gebiet. Keine Kalibrierstudie — editierbare, "
            "dokumentierte Modellannahme."),
    },
    "AQUACULTURE_RESILIENCE_SYSTEMS": {
        "default_reduction": ("Modellannahme (Technik gegen O₂-/Hitzeverluste)", [],
            "Wirkmechanismus: Belüfter, Sauerstoffeintrag, Beschattung/Kühlung und Sensorik "
            "verhindern die typischen Sommerverluste in Teich-/Kreislaufanlagen (Sauerstoff"
            "mangel und Temperaturspitzen sind die Hauptschadensursachen der Aquakultur in "
            "Hitzejahren). Angesetzt: 25 % Reduktion des Aquakultur-Schadensrisikos in den "
            "ausgerüsteten Anlagenzellen. Editierbare, dokumentierte Modellannahme."),
        "opex_per_unit_year": ("VDI 2067 + Energie (Belüftung/Sensorik)", ["VDI_2067_Blatt1"],
            "Belüfter/Pumpen/Sensorik laufen im Sommer dauerhaft: Wartung nach VDI-2067-"
            "Größenordnung plus erheblicher Stromverbrauch → ~6-8 % der Investition/Jahr; "
            "Punktwert 4.000 €/(Anlage·a) bei 60.000 € Investition."),
    },
    "FISHERIES_SPAWNING_HABITAT_RESTORATION": {
        "default_reduction": ("UBA/LfU (Laichhabitat-Renaturierung)", ["UBA_Gewaesserrenaturierung", "LfU_Bayern_Fischaufstieg"],
            "Wirkmechanismus: Wiederhergestellte Kieslaichplätze, Flachwasser- und Beschattungs"
            "zonen erhöhen Reproduktionserfolg und bieten Temperatur-Refugien — Renaturierung "
            "ist der Kernhebel der WRRL-Programme für klimastabile Fischbestände (UBA/LfU). "
            "Angesetzt: 22 % Reduktion des Bestandsstressrisikos in den renaturierten "
            "Gewässerzellen. Editierbare Modellannahme im belegten Wirkprinzip."),
        "benefit_per_m2_year": ("TEEB/UBA (Gewässer-Ökosystemleistungen)", ["TEEB_DE_Naturkapital", "UBA_Gewaesserrenaturierung"],
            "Direkter Zusatznutzen: renaturierte Gewässerabschnitte liefern Selbstreinigung, "
            "Habitat- und Erholungsleistungen (TEEB DE/UBA). 0,02 €/(m²·a) = 200 €/ha·a der "
            "renaturierten Fläche — von zuvor 2 €/m² (= 20.000 €/ha, unplausibel) "
            "herabgesetzt; editierbar."),
    },
    "FISHERIES_WATER_QUALITY_PROTECTION": {
        "default_reduction": ("Modellannahme (O₂-Haushalt in Warmphasen)", ["UBA_Gewaesserrenaturierung"],
            "Wirkmechanismus: Warmes Wasser hält weniger Sauerstoff — Nährstoff- und "
            "Einleitungsmanagement (Uferrandstreifen, Kläranlagen-Feinsteuerung, Einleit"
            "stopps in Hitzephasen) senkt die Sauerstoffzehrung genau dann, wenn die Bestände "
            "am verwundbarsten sind. Angesetzt: 20 % Reduktion der verknüpften Gewässergüte-/"
            "Bestandsrisiken. Editierbare, dokumentierte Modellannahme."),
    },
    "FISH_PASSAGE_RESTORATION": {
        "default_reduction": ("LfU Bayern (Durchgängigkeit/Ausweichwanderung)", ["LfU_Bayern_Fischaufstieg"],
            "Wirkmechanismus: Durchgängige Gewässer ermöglichen Fischen die Ausweichwanderung "
            "in kühlere, sauerstoffreichere Ober-/Nebenläufe während Hitze- und Niedrigwasser"
            "phasen — ohne Durchgängigkeit kollabieren eingeschlossene Populationen in "
            "aufgeheizten Stauräumen (LfU-Praxishandbuch Fischaufstieg; WRRL-Kernmaßnahme). "
            "Angesetzt: 22 % Reduktion des Bestandsstressrisikos im wieder angebundenen "
            "Gewässersystem. Editierbare Modellannahme."),
        "opex_per_unit_year": ("LfU/VDI 2067 (Unterhaltung Fischaufstieg)", ["LfU_Bayern_Fischaufstieg", "VDI_2067_Blatt1"],
            "Fischaufstiegsanlagen brauchen laufende Unterhaltung (Geschwemmsel-Räumung, "
            "Kontrolle der Leitströmung, Funktionsmonitoring nach LfU-Handbuch): VDI-2067-"
            "Größenordnung ~1,5 % der Investition/Jahr → 3.000 €/(Anlage·a) bei 200.000 €."),
    },
    "PREVENTION_INCENTIVES": {
        "default_reduction": ("Modellannahme (Anreizprogramm, Teilnahmequote)", ["BBK_Hochwasserschutzfibel"],
            "Wirkmechanismus: Förder-/Prämienanreize aktivieren private Eigenvorsorge "
            "(Objektschutz, Elementarversicherung — Maßnahmen der BBK-Fibel), aber nur bei "
            "einem Teil der Eigentümer (Teilnahmequoten und Mitnahmeeffekte begrenzen die "
            "Wirkung). Angesetzt: 12 % Reduktion der verknüpften Gebäudeschadensrisiken — "
            "bewusst der niedrigste Wert aller Maßnahmen (indirekter Wirkpfad). Editierbare, "
            "dokumentierte Modellannahme."),
    },
    "RISK_BASED_INVESTMENTS": {
        "default_reduction": ("Modellannahme (risikobasierte Priorisierung)", [],
            "Wirkmechanismus: Risikobasierte Investitionsplanung lenkt begrenzte kommunale "
            "Mittel dorthin, wo je Euro die größte Schadensminderung entsteht (Priorisierung "
            "nach Risikokarten statt Gießkanne) — die Wirkung entsteht indirekt über besser "
            "platzierte Folgeinvestitionen. Angesetzt: 15 % Reduktion der verknüpften Risiken "
            "im priorisierten Gebiet. Keine Kalibrierstudie — editierbare, dokumentierte "
            "Modellannahme."),
    },
}


def _enrich_measure_effect_docs() -> None:
    """Verdrahtet die zentralen Wirkungs-/Nutzen-Herleitungen in die Maßnahmen-Dicts.

    Inline gepflegte ``sources``/``source_details``/``source_refs`` je Maßnahme haben
    Vorrang; hier wird nur ergänzt, was dort fehlt.
    """
    for m in MEASURES:
        fields = _MEASURE_EFFECT_DOCS.get(m["code"])
        if not fields:
            continue
        sources_map = m.setdefault("sources", {})
        details = m.setdefault("source_details", {})
        refs_map = m.setdefault("source_refs", {})
        for field, (label, refs, text) in fields.items():
            sources_map.setdefault(field, label)
            details.setdefault(field, text)
            if refs and field not in refs_map:
                refs_map[field] = refs


_enrich_measure_effect_docs()


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


# ── Modellversion ────────────────────────────────────────────────────────────────
# Wird bei strukturellen Modelländerungen (Risiko-Set, Kostensätze, Aggregation)
# erhöht. Der Layer-Cache stempelt seine Dateien mit dieser Version und invalidiert
# automatisch, wenn sich die Version ändert (siehe services/layer_cache.py).
MODEL_VERSION = "2026.07-schichtB-nachbesserung-n6"
