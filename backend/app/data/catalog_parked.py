"""Geparkte Katalog-Einträge (M0-Verschlankung, docs/ROADMAP.md §5).

Diese Einträge sind NICHT Teil des aktiven Katalogs: keine Index-Maps, keine
Engine, keine Ratchets, kein /catalog-Payload. Sie kehren mit den Roadmap-
Stufen M1–M4 zurück (Stage-Zuordnung in catalog.PLANNED_RISKS) und werden dabei
gegen die KWRA-1:1-Struktur (kwra_id, Schadensbaum-Wirkungsketten) überarbeitet.
Quelle der Verschiebung: automatischer AST-Split vom 18.08.2026.
"""

_PARKED_HAZARDS: list[dict] = [
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

_PARKED_EXPOSURES: list[dict] = [
    {"code": "OUTDOOR_THERMAL_EXPOSURE", "name": "Aufenthalt im Freien (therm. Exposition)",
     "unit": "h/Tag", "norm_min": 0.0, "norm_max": 8.0, "spatial": True,
     "description": "Exposition der Bevölkerung durch Aufenthalt im Freien bei Hitze.",
     "proxy": "Proxy aus Anteil öffentlicher Freiflächen/Arbeitsplätze (OSM) + Bevölkerung.",
     "source": "OSM / Zensus (Proxy)"},
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
     "unit": "Punkte", "norm_min": 0.0, "norm_max": 15.0, "spatial": True,
     "description": "Energieinfrastruktur als exponiertes Sachgut (Kritikalitätspunkte).",
     "proxy": "OSM power=*, gewichtet nach Anlagenklasse und Spannungsebene (Umspannwerk/"
              "Kraftwerk hoch, Leitung je kV-Klasse pro Zellquerung); Masten/Tragwerke "
              "zählen nicht (Bestandteil der Leitung). Sättigung je Zelle: stärkstes "
              "Asset voll, Restsumme zu 50 %.",
     "source": "OSM"},
    {"code": "WATER_WASTEWATER_INFRA", "name": "Wasser/Abwasseranlagen",
     "unit": "Punkte", "norm_min": 0.0, "norm_max": 15.0, "spatial": True,
     "description": "Wasser- und Abwasserinfrastruktur (Kritikalitätspunkte).",
     "proxy": "OSM man_made=water_works/wastewater_plant/pumping_station u. ä., "
              "gewichtet nach Anlagenklasse (Kläranlage/Wasserwerk hoch).",
     "source": "OSM"},
    {"code": "TRANSPORT_HUBS", "name": "Verkehrsknotenpunkte",
     "unit": "Punkte", "norm_min": 0.0, "norm_max": 12.0, "spatial": True,
     "description": "Verkehrsknoten und -kritikalität (Kritikalitätspunkte).",
     "proxy": "OSM Bahnhöfe/Haltestellen/ÖPNV-Stationen, gewichtet nach Knotenklasse "
              "(Bahnhof hoch, Haltepunkt niedriger).",
     "source": "OSM"},
    {"code": "COMMUNICATION_INFRA", "name": "Kommunikationsinfrastruktur",
     "unit": "Punkte", "norm_min": 0.0, "norm_max": 12.0, "spatial": True,
     "description": "Telekommunikations- und Kommunikationsanlagen (Kritikalitätspunkte).",
     "proxy": "OSM telecom/tower=communication/man_made=mast, gewichtet nach Anlagenklasse "
              "(Rechenzentrum/Vermittlung hoch, Mast/Antenne niedriger).",
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

_PARKED_VULNERABILITIES: list[dict] = [
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

_PARKED_RISKS: list[dict] = [
    {"code": "EXPECTED_ANNUAL_MORTALITY_FLOOD", "name": "Erwartete Mortalität (Flut)",
     "outcome_unit": "Todesfälle/Jahr", "group": "flood", "cost_dimension": "health",
     "hazards": ["HEAVY_RAIN_FLOOD"],
     "exposures": ["POPULATION_DENSITY", "LOCATION_HAZARD_ZONES"],
     "vulnerabilities": ["EARLY_WARNING_SYSTEMS", "EMERGENCY_MANAGEMENT"],
     # Anker: annualisiertes Mittel der kuratierten Ereignisliste (~6 Tote/Jahr bundesweit
     # = ~0,007/100k). ref_value ist der Wert bei Index=100, also der Ereignisfall.
     "ref_value": 0.6, "scale": "pop", "cost_per_outcome_eur": 3500000.0,
     "source": "Jonkman 2008 / CEDIM 2021 / Destatis ICD-10 X38",
     "description": "Todesfälle durch Hochwasser und Sturzfluten (Ertrinken). Der "
                    "Geländetyp entscheidet: Sturzfluten in engen Steiltälern sind um "
                    "Größenordnungen tödlicher als langsam steigende Auenhochwasser.",
     "priority": 2},
    {"code": "EXPECTED_ANNUAL_MORTALITY_STORM", "name": "Erwartete Mortalität (Sturm)",
     "outcome_unit": "Todesfälle/Jahr", "group": "flood", "cost_dimension": "health",
     "hazards": ["EXTRATROPICAL_STORM"],
     "exposures": ["POPULATION_DENSITY", "LOCATION_HAZARD_ZONES"],
     "vulnerabilities": ["BUILDING_STABILITY", "EARLY_WARNING_SYSTEMS"],
     "ref_value": 0.15, "scale": "pop", "cost_per_outcome_eur": 3500000.0,
     "source": "DWD-Sturmereignisse / Destatis ICD-10 X37",
     "description": "Sturmbedingte Todesfälle — überwiegend durch umstürzende Bäume, "
                    "fliegende Trümmer und Bauteilversagen; die Opfer fallen draußen und "
                    "unterwegs, nicht in der Wohnung.",
     "priority": 2},
    {"code": "EXPECTED_ANNUAL_INJURIES", "name": "Erwartete Verletzte (Flut)",
     "outcome_unit": "Verletzte/Jahr", "group": "flood", "cost_dimension": "health",
     # Vorher lief EIN Risiko mit max() über Flut/Sturm/Hangrutsch. Verletzte aus
     # verschiedenen Gefahren sind additiv, nicht alternativ — daher aufgetrennt.
     "hazards": ["HEAVY_RAIN_FLOOD"],
     "exposures": ["POPULATION_DENSITY", "LOCATION_HAZARD_ZONES"],
     "vulnerabilities": ["EMERGENCY_MANAGEMENT", "EARLY_WARNING_SYSTEMS"],
     "ref_value": 30.0, "scale": "pop", "cost_per_outcome_eur": 12000.0,
     "source": "Destatis ICD-10 X38 / BBK",
     "description": "Nicht-tödlich Verletzte durch Hochwasser und Starkregen, "
                    "einschließlich der Verletzungen bei den Aufräumarbeiten.",
     "priority": 2},
    {"code": "EXPECTED_ANNUAL_INJURIES_STORM", "name": "Erwartete Verletzte (Sturm)",
     "outcome_unit": "Verletzte/Jahr", "group": "flood", "cost_dimension": "health",
     "hazards": ["EXTRATROPICAL_STORM"],
     "exposures": ["POPULATION_DENSITY", "LOCATION_HAZARD_ZONES"],
     "vulnerabilities": ["BUILDING_STABILITY", "EARLY_WARNING_SYSTEMS"],
     "ref_value": 18.0, "scale": "pop", "cost_per_outcome_eur": 12000.0,
     "source": "Destatis ICD-10 X37/X33 / DWD",
     "description": "Nicht-tödlich Verletzte durch Stürme (Baumsturz, Trümmer, "
                    "Dachreparaturen nach dem Ereignis).",
     "priority": 2},
    {"code": "EXPECTED_ANNUAL_INJURIES_LANDSLIDE", "name": "Erwartete Verletzte (Hangrutsch)",
     "outcome_unit": "Verletzte/Jahr", "group": "flood", "cost_dimension": "health",
     "hazards": ["LANDSLIDE"],
     "exposures": ["POPULATION_DENSITY", "LOCATION_HAZARD_ZONES"],
     "vulnerabilities": ["EMERGENCY_MANAGEMENT", "EARLY_WARNING_SYSTEMS"],
     "ref_value": 1.5, "scale": "pop", "cost_per_outcome_eur": 12000.0,
     "source": "Destatis ICD-10 X36",
     "description": "Nicht-tödlich Verletzte durch Hangrutschungen. Außerhalb steilen "
                    "Geländes nahe null.",
     "priority": 3},
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
     # Behandlung — die zählt „Erwartete Morbidität (Hitze)"; Abgrenzung dort/hier).
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

_PARKED_MEASURES: list[dict] = [
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
    {"code": "EARLY_WARNING_MEASURE", "name": "Frühwarnsysteme (Maßnahme)",
     "description": "Ausbau von Frühwarnsystemen.", "measure_type": "organizational",
     "effect_target": ["vulnerability"], "default_reduction": 0.25, "coverage_scaling": "saturating",
     # Frühwarnung wirkt auf alle ereignisgetriebenen Personenschäden — seit der
     # Auftrennung der Verletzten nach Gefahr sind das mehrere Kanäle. Die
     # Todesfall-Kanäle sind der wichtigste Hebel: An der Ahr 2021 war das
     # Warnversagen ausschlaggebend.
     "linked_risk_codes": ["EXPECTED_ANNUAL_AFFECTED_EVACUATED",
                           "EXPECTED_ANNUAL_INJURIES", "EXPECTED_ANNUAL_INJURIES_STORM",
                           "EXPECTED_ANNUAL_INJURIES_LANDSLIDE",
                           "EXPECTED_ANNUAL_MORTALITY_FLOOD",
                           "EXPECTED_ANNUAL_MORTALITY_STORM"],
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

