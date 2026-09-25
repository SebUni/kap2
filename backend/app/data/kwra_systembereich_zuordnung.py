"""KWRA-Systembereich je Klimawirkung (Konformitäts-Checkliste Zeile 10, Anforderung A1; T-1123).

Quelle: UBA/BMU, KWRA 2021, Teilbericht 6 (Integrierte Auswertung), Kap. 7
„Querbetrachtung der Systembereiche“ (S. 146–155). Übertragen aus der Arbeitsmappe
``docs/KWAR/KWRA-2021_Klimawirkungen.xlsx``, Blatt ``Klimawirkungen``, Spalte
„Systembereich“ (Spalte M), je KWRA-ID 1–102.

``SYSTEMBEREICH_JE_KWRA_ID`` ordnet jeder der 102 Klimawirkungen der KWRA genau einen
der fünf übergeordneten Systembereiche zu — damit auch den 49 Klimawirkungen der
Roadmap (``catalog.PLANNED_RISKS``), die bisher keinen Systembereich trugen. Die Werte
sind wörtlich die fünf Bezeichnungen aus ``catalog.KWRA_SYSTEMBEREICHE``; das Modul
importiert den Katalog bewusst nicht, damit der Katalog es seinerseits nutzen kann.
Der Test ``tests/test_kwra_systembereich_zuordnung.py`` gleicht die Zuordnung Zeile
für Zeile mit der Arbeitsmappe ab; eine Abweichung ist ein Befund, keine stille
Korrektur (CLAUDE.md, Eiserne Regel 2).

Beleg der Größenordnung: „Menschen und soziale Systeme“ umfasst neun Klimawirkungen
(TB 6, S. 151) — hier #87 und #95 bis #102.
"""

from __future__ import annotations

QUELLE = (
    "UBA/BMU, ›Klimawirkungs- und Risikoanalyse 2021 für Deutschland‹, Teilbericht 6 "
    "(Integrierte Auswertung), Kapitel 7 ›Querbetrachtung der Systembereiche‹, "
    "Dessau-Roßlau, 2021. Arbeitsmappe docs/KWAR/KWRA-2021_Klimawirkungen.xlsx, "
    "Blatt ›Klimawirkungen‹, Spalte ›Systembereich‹."
)

_NAT = "Natürliche Systeme und Ressourcen"
_NNW = "Naturnutzende Wirtschaftssysteme"
_INF = "Infrastrukturen und Gebäude"
_NFW = "Naturferne Wirtschaftssysteme"
_MEN = "Menschen und soziale Systeme"

SYSTEMBEREICH_JE_KWRA_ID: dict[int, str] = {
    # Handlungsfeld Biologische Vielfalt
    1: _NAT,  # Veränderung der Länge der Vegetationsperiode und Phänologie
    2: _NAT,  # Ausbreitung invasiver Arten
    3: _NAT,  # Verlust an genetischer Vielfalt
    4: _NAT,  # Verschiebung von Arealen und Rückgang der Bestände
    5: _NAT,  # Schäden an Küstenökosystemen
    6: _NAT,  # Schäden an Gebirgsökosystemen
    7: _NAT,  # Schäden an wassergebundenen Habitaten und Feuchtgebieten
    8: _NAT,  # Schäden an Wäldern
    9: _NNW,  # Ökosystemleistungen
    # Handlungsfeld Boden
    10: _NAT,  # Bodenerosion durch Wasser
    11: _NAT,  # Bodenerosion durch Wind
    12: _NAT,  # Rutschungen und Muren
    13: _NAT,  # Wassermangel im Boden
    14: _NAT,  # Sickerwasser
    15: _NAT,  # Vernässung
    16: _NAT,  # Bodenbiologie: Mikrobiologische Aktivität / Biodiversität / biologische Funktionalität
    17: _NAT,  # Bodenstoffhaushalt: Organische Bodensubstanz, Stickstoff- und Phosphorhaushalt, Stoffausträge
    18: _NAT,  # Bodenfunktionen: Filter- und Pufferfunktionen
    19: _NNW,  # Produktionsfunktionen
    # Handlungsfeld Landwirtschaft
    20: _NNW,  # Hitzestress bei und Leistung von Nutztieren
    21: _NNW,  # Abiotischer Stress (Pflanzen)
    22: _NNW,  # Verschiebung von Anbaugebieten
    23: _NNW,  # Agrophänologische Phasen und Wachstumsperiode
    24: _NNW,  # Stress durch Schädlinge und Krankheiten (Pflanzen)
    25: _NNW,  # Ertragsausfälle
    26: _NNW,  # Qualität der Ernteprodukte
    # Handlungsfeld Wald- und Forstwirtschaft
    27: _NNW,  # Hitze- und Trockenstress
    28: _NNW,  # Stress durch Schädlinge / Krankheiten
    29: _NNW,  # Schäden durch Windwurf
    30: _NNW,  # Waldbrandrisiko
    31: _NNW,  # Nutzfunktion: Holzertrag
    32: _NNW,  # Nutzfunktion: Erholung
    # Handlungsfeld Fischerei
    33: _NNW,  # Entkopplung von Nahrungsbeziehungen in der Ostsee
    34: _NNW,  # Verbreitung wärmeliebender Arten in der Nordsee
    35: _NNW,  # Verbreitung von Fischarten in Fließgewässern
    36: _NNW,  # Stress durch Schädlinge / Krankheiten
    37: _NNW,  # Schäden an Aquakulturen
    # Handlungsfeld Küsten- und Meeresschutz
    38: _NAT,  # Meerestemperatur und Eisbedeckung
    39: _NAT,  # Wasserqualität und Grundwasserversalzung
    40: _NAT,  # Meeresspiegelhöhe
    41: _NAT,  # Strömungen und Gezeitendynamik
    42: _NAT,  # Seegang
    43: _NAT,  # Sturmfluten
    44: _NAT,  # Naturräumliche Veränderungen an Küsten
    45: _INF,  # Höhere Belastung oder Versagen von Küstenschutzsystemen
    46: _INF,  # Beschädigung oder Zerstörung von Siedlung und Infrastruktur an der Küste
    47: _INF,  # Überlastung der Entwässerungseinrichtungen in überflutungsgefährdeten Gebieten
    # Handlungsfeld Wasserhaushalt, Wasserwirtschaft
    48: _NAT,  # Niedrigwasser
    49: _NAT,  # Hochwasser
    50: _INF,  # Belastung oder Versagen von Hochwasserschutzsystemen
    51: _NAT,  # Sturzfluten (Versagen von Entwässerungseinrichtungen und Überflutungsschutzsystemen)
    52: _INF,  # Einschränkungen der Funktionsfähigkeit von Kanalnetzen und Vorflutern und Kläranlagen
    53: _NAT,  # Gewässertemperatur und Eisbedeckung und biologische Wasserqualität
    54: _NAT,  # Chemische Wasserqualität
    55: _NAT,  # Grundwasserstand und Grundwasserqualität
    56: _NNW,  # Mangel an Bewässerungswasser
    57: _NNW,  # Trinkwasser
    58: _NNW,  # Produktionswasser
    # Handlungsfeld Bauwesen
    59: _INF,  # Schäden an Gebäuden aufgrund von Starkregen
    60: _INF,  # Schäden an Gebäuden aufgrund von Flusshochwasser
    61: _NNW,  # Vegetation in Siedlungen
    62: _INF,  # Stadtklima / Wärmeinseln
    63: _INF,  # Innenraumklima
    64: _NFW,  # Zeiten für Bautätigkeit
    # Handlungsfeld Energiewirtschaft
    65: _INF,  # Bedarf an Kühlenergie
    66: _INF,  # Bedarf an Heizenergie
    67: _INF,  # Unterbrechung der regionalen Lieferketten für Energieträger
    68: _NNW,  # Mangelndes Kühlwasser für thermische Kraftwerke
    69: _INF,  # Ertragsminderung / -zunahme bei Photovoltaikanlagen und bei Windenergieanlagen an Land und auf See
    70: _INF,  # Fehlende Zuverlässigkeit der Energieversorgung
    # Handlungsfeld Verkehr, Verkehrsinfrastruktur
    71: _NNW,  # Schiffbarkeit der Binnenschifffahrtsstraßen (Niedrigwasser)
    72: _NNW,  # Schiffbarkeit der Binnenschifffahrtsstraßen (Hochwasser)
    73: _NNW,  # Schiffbarkeit der Seeschifffahrtsstraßen
    74: _INF,  # Schäden / Hindernisse bei Straßen und Schienenwegen (Hochwasser)
    75: _INF,  # Schäden / Hindernisse bei Straßen und Schienenwegen (Gravitative Massenbewegungen)
    76: _INF,  # Schäden an Verkehrsleitsystemen, Oberleitungen und Stromversorgungsanlagen
    77: _INF,  # Schäden an Binnen- und Seeschifffahrtsstraßen, Häfen und maritimen Infrastrukturen
    # Handlungsfeld Industrie und Gewerbe
    78: _NFW,  # Beeinträchtigung der Versorgung mit Rohstoffen und Zwischenprodukten (international)
    79: _NFW,  # Bedingungen auf Absatzmärkten (international)
    80: _NFW,  # Wettbewerbsvorteil in innovativen Umwelttechnologien
    81: _INF,  # Beeinträchtigung des internationalen Warentransports
    82: _INF,  # Beeinträchtigung des Warenverkehrs über Wasserstraßen (Inland)
    83: _INF,  # Beeinträchtigung des landgestützten Warenverkehrs (Inland)
    84: _INF,  # Energieverbrauch und Beeinträchtigung bei der Energieversorgung
    85: _NNW,  # Wasserbedarf
    86: _INF,  # Freisetzung gefährlicher Stoffe
    87: _MEN,  # Leistungseinbußen von Beschäftigten
    88: _NFW,  # Beeinträchtigung von Produktionsprozessen
    89: _NFW,  # Aufwand für die betriebliche Planung
    # Handlungsfeld Tourismuswirtschaft
    90: _NNW,  # Einschränkungen touristischer Angebote: Auswirkungen fehlender Schneesicherheit auf den Wintertourismus
    91: _NNW,  # Einschränkungen touristischer Angebote: Auswirkungen von Hitze auf den Gesundheitstourismus
    92: _INF,  # Schäden an touristischen Infrastrukturen und Betriebsunterbrechungen
    93: _NFW,  # Verlagerung der Nachfrage
    94: _NFW,  # Wirtschaftliche Chancen und Risiken für die Tourismuswirtschaft
    # Handlungsfeld Menschliche Gesundheit
    95: _MEN,  # Hitzebelastung
    96: _MEN,  # Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft
    97: _MEN,  # Potenziell schädliche Mikroorganismen und Algen
    98: _MEN,  # UV-bedingte Gesundheitsschädigungen (insbesondere Hautkrebs)
    99: _MEN,  # Verbreitung und Abundanzveränderung von möglichen Vektoren
    100: _MEN,  # Atembeschwerden (aufgrund von Luftverunreinigungen)
    101: _MEN,  # Verletzungen und Todesfälle infolge von Extremereignissen
    102: _MEN,  # Auswirkungen auf das Gesundheitssystem
}


def systembereich_der_klimawirkung(kwra_id: int) -> str:
    """KWRA-Systembereich einer Klimawirkung (``KeyError`` bei unbekannter KWRA-ID)."""
    return SYSTEMBEREICH_JE_KWRA_ID[kwra_id]
