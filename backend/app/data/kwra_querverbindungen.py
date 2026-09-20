"""KWRA-Querverbindungen (Wirkbeziehungen zwischen Klimawirkungen) — Teil 1.

Quelle: UBA/BMU „Klimawirkungs- und Risikoanalyse 2021 für Deutschland" (KWRA 2021),
Teilbericht 6 (Integrierte Auswertung), Kapitel 3.4 „Vernetzung der Klimawirkungen".
Arbeitsmappe: ``docs/KWAR/KWRA-2021_Klimawirkungen.xlsx``, Blatt ``Wirkbeziehungen``
(kuratierte Übertragung aus Teilbericht 6) und Blatt ``Klimawirkungen``, Spalte
„Netzrolle (TB 6 Kap. 3.4)".

Die KWRA nennt 257 Querverbindungen zwischen den 102 Klimawirkungen insgesamt, veröffent-
licht die Einzelkanten aber in keinem der sechs Teilberichte als vollständige Liste
(Abbildung 8 in Teilbericht 6 ist ein Chord-Diagramm auf Handlungsfeldebene, aus dem sich
keine exakten Kantenzahlen ablesen lassen). Dieses Modul enthält deshalb **nur, was
Teilbericht 6 ausdrücklich belegt**:

  NETZROLLEN            — die 25 Klimawirkungen, die TB 6 Kap. 3.4 ausdrücklich als
                           starke Sender ("stark ausgehend") oder starke Empfänger
                           ("stark eingehend") im Wirkungsnetz benennt.
  BENANNTE_BEZIEHUNGEN   — die im Fließtext von TB 6 Kap. 3.4 wörtlich genannten
                           Einzelbeziehungen (Auszug, nicht vollständig; 20 Einträge).
                           ``quelle_kwra_id``/``ziel_kwra_id`` sind gesetzt, wenn die
                           Quelle bzw. das Ziel eine einzelne, eindeutig identifizierbare
                           Klimawirkung ist (nicht bei Handlungsfeld-Ebene oder mehreren
                           Zielen); sonst ``None``.
  KENNZAHLEN             — Kennzahlen aus TB 6 Kap. 3.4 (Gesamtzahl, Durchschnitt, ...).
  SYSTEMBEREICH_MATRIX   — Querverbindungen zwischen den fünf Systembereichen
                           (TB 6, Tabelle 28). Rein vorgelagerte Klimawirkungen sind
                           darin nicht enthalten; die Diagonale zählt Wirkbeziehungen
                           innerhalb desselben Systembereichs, ``summe_ausgehend`` nur
                           die Beziehungen zu den vier anderen Systembereichen.

Eine vollständige Kantenliste aller 257 Querverbindungen ist keine KWRA-Angabe und
müsste eigenständig modelliert und als solche gekennzeichnet werden (siehe Vermerk am
Ende des Blatts ``Wirkbeziehungen``) — das ist nicht Gegenstand dieses Moduls (Teil 1).
"""

from __future__ import annotations

QUELLE = (
    "UBA/BMU, ›Klimawirkungs- und Risikoanalyse 2021 für Deutschland‹, Teilbericht 6 "
    "(Integrierte Auswertung), Kapitel 3.4 ›Vernetzung der Klimawirkungen‹, Dessau-Roßlau, "
    "2021. Arbeitsmappe docs/KWAR/KWRA-2021_Klimawirkungen.xlsx, Blätter "
    "›Klimawirkungen‹ (Spalte Netzrolle) und ›Wirkbeziehungen‹."
)

# ── Netzrollen: Klimawirkungen mit ausdrücklich benannter starker Netzrolle ──────
#
# Jeder Eintrag: kwra_id (1–102, siehe Blatt "Klimawirkungen" Spalte "ID"),
# name (Klimawirkung), handlungsfeld, rolle ("stark ausgehend" | "stark eingehend").
NETZROLLEN: list[dict] = [
    {"kwra_id": 1, "name": "Veränderung der Länge der Vegetationsperiode und Phänologie",
     "handlungsfeld": "Biologische Vielfalt", "rolle": "stark ausgehend"},
    {"kwra_id": 4, "name": "Verschiebung von Arealen und Rückgang der Bestände",
     "handlungsfeld": "Biologische Vielfalt", "rolle": "stark ausgehend"},
    {"kwra_id": 5, "name": "Schäden an Küstenökosystemen",
     "handlungsfeld": "Biologische Vielfalt", "rolle": "stark eingehend"},
    {"kwra_id": 12, "name": "Rutschungen und Muren",
     "handlungsfeld": "Boden", "rolle": "stark ausgehend"},
    {"kwra_id": 13, "name": "Wassermangel im Boden",
     "handlungsfeld": "Boden", "rolle": "stark ausgehend"},
    {"kwra_id": 14, "name": "Sickerwasser",
     "handlungsfeld": "Boden", "rolle": "stark ausgehend"},
    {"kwra_id": 15, "name": "Vernässung",
     "handlungsfeld": "Boden", "rolle": "stark ausgehend"},
    {"kwra_id": 25, "name": "Ertragsausfälle",
     "handlungsfeld": "Landwirtschaft", "rolle": "stark eingehend"},
    {"kwra_id": 26, "name": "Qualität der Ernteprodukte",
     "handlungsfeld": "Landwirtschaft", "rolle": "stark eingehend"},
    {"kwra_id": 31, "name": "Nutzfunktion: Holzertrag",
     "handlungsfeld": "Wald- und Forstwirtschaft", "rolle": "stark eingehend"},
    {"kwra_id": 38, "name": "Meerestemperatur und Eisbedeckung",
     "handlungsfeld": "Küsten- und Meeresschutz", "rolle": "stark ausgehend"},
    {"kwra_id": 39, "name": "Wasserqualität und Grundwasserversalzung",
     "handlungsfeld": "Küsten- und Meeresschutz", "rolle": "stark ausgehend"},
    {"kwra_id": 40, "name": "Meeresspiegelhöhe",
     "handlungsfeld": "Küsten- und Meeresschutz", "rolle": "stark ausgehend"},
    {"kwra_id": 43, "name": "Sturmfluten",
     "handlungsfeld": "Küsten- und Meeresschutz", "rolle": "stark ausgehend"},
    {"kwra_id": 48, "name": "Niedrigwasser",
     "handlungsfeld": "Wasserhaushalt, Wasserwirtschaft", "rolle": "stark ausgehend"},
    {"kwra_id": 49, "name": "Hochwasser",
     "handlungsfeld": "Wasserhaushalt, Wasserwirtschaft", "rolle": "stark ausgehend"},
    {"kwra_id": 53, "name": "Gewässertemperatur und Eisbedeckung und biologische Wasserqualität",
     "handlungsfeld": "Wasserhaushalt, Wasserwirtschaft", "rolle": "stark ausgehend"},
    {"kwra_id": 55, "name": "Grundwasserstand und Grundwasserqualität",
     "handlungsfeld": "Wasserhaushalt, Wasserwirtschaft", "rolle": "stark eingehend"},
    {"kwra_id": 73, "name": "Schiffbarkeit der Seeschifffahrtsstraßen",
     "handlungsfeld": "Verkehr, Verkehrsinfrastruktur", "rolle": "stark eingehend"},
    {"kwra_id": 82, "name": "Beeinträchtigung des Warenverkehrs über Wasserstraßen (Inland)",
     "handlungsfeld": "Industrie und Gewerbe", "rolle": "stark eingehend"},
    {"kwra_id": 92, "name": "Schäden an touristischen Infrastrukturen und Betriebsunterbrechungen",
     "handlungsfeld": "Tourismuswirtschaft", "rolle": "stark eingehend"},
    {"kwra_id": 95, "name": "Hitzebelastung",
     "handlungsfeld": "Menschliche Gesundheit", "rolle": "stark eingehend"},
    {"kwra_id": 96, "name": "Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft",
     "handlungsfeld": "Menschliche Gesundheit", "rolle": "stark eingehend"},
    {"kwra_id": 97, "name": "Potenziell schädliche Mikroorganismen und Algen",
     "handlungsfeld": "Menschliche Gesundheit", "rolle": "stark eingehend"},
    {"kwra_id": 101, "name": "Verletzungen und Todesfälle infolge von Extremereignissen",
     "handlungsfeld": "Menschliche Gesundheit", "rolle": "stark eingehend"},
]

# ── Im Fließtext ausdrücklich benannte Einzelbeziehungen (Auszug) ───────────────
#
# quelle/ziel: Wortlaut aus TB 6 Kap. 3.4. quelle_kwra_id/ziel_kwra_id sind gesetzt,
# wenn Quelle bzw. Ziel eine einzelne, eindeutig identifizierbare Klimawirkung ist
# (sonst None — z. B. bei Handlungsfeld-Ebene oder mehreren genannten Zielen).
BENANNTE_BEZIEHUNGEN: list[dict] = [
    {"quelle": "Hochwasser", "quelle_kwra_id": 49,
     "ziel": "zahlreiche Klimawirkungen in mehreren Handlungsfeldern", "ziel_kwra_id": None,
     "ebene": "Klimawirkung",
     "beleg": "TB6 Kap. 3.4: zentrale Klimawirkung, wirkt sich auf die meisten anderen aus"},
    {"quelle": "Gewässertemperatur und Eisbedeckung und biologische Wasserqualität",
     "quelle_kwra_id": 53,
     "ziel": "Potenziell schädliche Mikroorganismen und Algen", "ziel_kwra_id": 97,
     "ebene": "Klimawirkung", "beleg": "TB6 Kap. 3.4: fördert deren Entwicklung"},
    {"quelle": "Stadtklima / Wärmeinseln", "quelle_kwra_id": 62,
     "ziel": "Hitzebelastung", "ziel_kwra_id": 95,
     "ebene": "Klimawirkung",
     "beleg": "TB6 Kap. 3.4: zunehmender urbaner Wärmeinseleffekt erhöht die Hitzebelastung"},
    {"quelle": "Veränderung der Länge der Vegetationsperiode und Phänologie",
     "quelle_kwra_id": 1,
     "ziel": "Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft",
     "ziel_kwra_id": 96, "ebene": "Klimawirkung",
     "beleg": "TB6 Kap. 3.4: verlängerte Vegetationsperiode verstärkt Pollenreaktionen"},
    {"quelle": "Hochwasser", "quelle_kwra_id": 49,
     "ziel": "Verletzungen und Todesfälle infolge von Extremereignissen", "ziel_kwra_id": 101,
     "ebene": "Klimawirkung", "beleg": "TB6 Kap. 3.4"},
    {"quelle": "Sturzfluten (Versagen von Entwässerungseinrichtungen und "
               "Überflutungsschutzsystemen)", "quelle_kwra_id": 51,
     "ziel": "Verletzungen und Todesfälle infolge von Extremereignissen", "ziel_kwra_id": 101,
     "ebene": "Klimawirkung", "beleg": "TB6 Kap. 3.4"},
    {"quelle": "Niedrigwasser", "quelle_kwra_id": 48,
     "ziel": "Beeinträchtigung des Warenverkehrs über Wasserstraßen (Inland)",
     "ziel_kwra_id": 82, "ebene": "Klimawirkung",
     "beleg": "TB6 Kap. 3.4: niedrigwasserbedingte Einschränkungen im Warentransport"},
    {"quelle": "Hochwasser", "quelle_kwra_id": 49,
     "ziel": "Schäden / Hindernisse bei Straßen und Schienenwegen (Hochwasser)",
     "ziel_kwra_id": 74, "ebene": "Klimawirkung",
     "beleg": "TB6 Kap. 3.4: Beeinträchtigung der Verkehrswege"},
    {"quelle": "Boden (Handlungsfeld)", "quelle_kwra_id": None,
     "ziel": "Grundwasserstand und Grundwasserqualität", "ziel_kwra_id": 55,
     "ebene": "gemischt",
     "beleg": "TB6 Kap. 3.4: viele Klimawirkungen des Bodens wirken hierauf ein"},
    {"quelle": "Boden und Biologische Vielfalt (Handlungsfelder)", "quelle_kwra_id": None,
     "ziel": "Ertragsausfälle", "ziel_kwra_id": 25, "ebene": "gemischt",
     "beleg": "TB6 Kap. 3.4: landwirtschaftliche Ertragsausfälle werden von vielen "
              "Klimawirkungen dieser Handlungsfelder beeinflusst"},
    {"quelle": "Boden und Biologische Vielfalt (Handlungsfelder)", "quelle_kwra_id": None,
     "ziel": "Qualität der Ernteprodukte", "ziel_kwra_id": 26, "ebene": "gemischt",
     "beleg": "TB6 Kap. 3.4"},
    {"quelle": "Boden und Biologische Vielfalt (Handlungsfelder)", "quelle_kwra_id": None,
     "ziel": "Nutzfunktion: Holzertrag", "ziel_kwra_id": 31, "ebene": "gemischt",
     "beleg": "TB6 Kap. 3.4: weitere Auswirkungen auf Holzerträge in der Forstwirtschaft"},
    {"quelle": "Küsten- und Meeresschutz (Handlungsfeld)", "quelle_kwra_id": None,
     "ziel": "Schiffbarkeit der Seeschifffahrtsstraßen", "ziel_kwra_id": 73,
     "ebene": "gemischt", "beleg": "TB6 Kap. 3.4"},
    {"quelle": "Küsten- und Meeresschutz (Handlungsfeld)", "quelle_kwra_id": None,
     "ziel": "Schäden an touristischen Infrastrukturen und Betriebsunterbrechungen",
     "ziel_kwra_id": 92, "ebene": "gemischt", "beleg": "TB6 Kap. 3.4"},
    {"quelle": "Küsten- und Meeresschutz (Handlungsfeld)", "quelle_kwra_id": None,
     "ziel": "Schäden an Küstenökosystemen", "ziel_kwra_id": 5,
     "ebene": "gemischt", "beleg": "TB6 Kap. 3.4"},
    {"quelle": "Wasserhaushalt, Wasserwirtschaft (Handlungsfeld)", "quelle_kwra_id": None,
     "ziel": "Industrie und Gewerbe (Handlungsfeld)", "ziel_kwra_id": None,
     "ebene": "Handlungsfeld",
     "beleg": "TB6 Kap. 3.4: Einschränkungen der Wasserversorgung treffen die Produktion"},
    {"quelle": "Energiewirtschaft (Handlungsfeld)", "quelle_kwra_id": None,
     "ziel": "Industrie und Gewerbe (Handlungsfeld)", "ziel_kwra_id": None,
     "ebene": "Handlungsfeld",
     "beleg": "TB6 Kap. 3.4: Einschränkungen der Energieversorgung treffen die Produktion"},
    {"quelle": "Küsten- und Meeresschutz (Handlungsfeld)", "quelle_kwra_id": None,
     "ziel": "Tourismuswirtschaft (Handlungsfeld)", "ziel_kwra_id": None,
     "ebene": "Handlungsfeld",
     "beleg": "TB6 Kap. 3.4: viele eingehende Wirkungen beim Tourismus"},
    {"quelle": "Biologische Vielfalt (Handlungsfeld)", "quelle_kwra_id": None,
     "ziel": "Tourismuswirtschaft (Handlungsfeld)", "ziel_kwra_id": None,
     "ebene": "Handlungsfeld", "beleg": "TB6 Kap. 3.4"},
    {"quelle": "Wasserhaushalt, Wasserwirtschaft (Handlungsfeld)", "quelle_kwra_id": None,
     "ziel": "Tourismuswirtschaft (Handlungsfeld)", "ziel_kwra_id": None,
     "ebene": "Handlungsfeld", "beleg": "TB6 Kap. 3.4"},
]

# ── Kennzahlen (TB 6 Kap. 3.4) ───────────────────────────────────────────────────
KENNZAHLEN: dict[str, object] = {
    "querverbindungen_gesamt": 257,
    "durchschnitt_je_klimawirkung": "rund 2,5 ein- oder ausgehende Beziehungen",
    "klimawirkungen_mit_ausgehenden_beziehungen": "71 von 102",
    "klimawirkungen_mit_eingehenden_beziehungen": "62 von 102",
    "handlungsfeld_meiste_ausgehende_beziehungen": "Wasserhaushalt, Wasserwirtschaft",
    "handlungsfeld_meiste_eingehende_beziehungen": "Tourismuswirtschaft",
    "nur_ausgehende_beziehungen": "Küsten- und Meeresschutz",
    "nur_eingehende_beziehungen": "Tourismuswirtschaft",
}

# ── Querverbindungen zwischen den Systembereichen (TB 6, Tabelle 28) ────────────
#
# Rein vorgelagerte Klimawirkungen sind in dieser Matrix nicht enthalten. Die
# Diagonale zählt Wirkbeziehungen innerhalb desselben Systembereichs; die
# Summenspalte "summe_ausgehend" nur die Beziehungen zu den vier anderen
# Systembereichen.
SYSTEMBEREICH_MATRIX: dict[str, dict[str, int]] = {
    "Natürliche Systeme und Ressourcen": {
        "Natürliche Systeme und Ressourcen": 24,
        "Naturnutzende Wirtschaftssysteme": 50,
        "Infrastrukturen und Gebäude": 13,
        "Naturferne Wirtschaftssysteme": 9,
        "Menschen und soziale Systeme": 8,
        "summe_ausgehend": 80,
    },
    "Naturnutzende Wirtschaftssysteme": {
        "Natürliche Systeme und Ressourcen": 6,
        "Naturnutzende Wirtschaftssysteme": 44,
        "Infrastrukturen und Gebäude": 13,
        "Naturferne Wirtschaftssysteme": 8,
        "Menschen und soziale Systeme": 8,
        "summe_ausgehend": 35,
    },
    "Infrastrukturen und Gebäude": {
        "Natürliche Systeme und Ressourcen": 3,
        "Naturnutzende Wirtschaftssysteme": 3,
        "Infrastrukturen und Gebäude": 26,
        "Naturferne Wirtschaftssysteme": 13,
        "Menschen und soziale Systeme": 11,
        "summe_ausgehend": 30,
    },
    "Naturferne Wirtschaftssysteme": {
        "Natürliche Systeme und Ressourcen": 0,
        "Naturnutzende Wirtschaftssysteme": 0,
        "Infrastrukturen und Gebäude": 0,
        "Naturferne Wirtschaftssysteme": 5,
        "Menschen und soziale Systeme": 0,
        "summe_ausgehend": 0,
    },
    "Menschen und soziale Systeme": {
        "Natürliche Systeme und Ressourcen": 0,
        "Naturnutzende Wirtschaftssysteme": 4,
        "Infrastrukturen und Gebäude": 1,
        "Naturferne Wirtschaftssysteme": 7,
        "Menschen und soziale Systeme": 6,
        "summe_ausgehend": 12,
    },
}
