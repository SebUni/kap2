"""KWRA-Querbezüge zwischen den 13 Handlungsfeldern — ausgewiesene Ablesung.

Quelle: UBA/BMU „Klimawirkungs- und Risikoanalyse 2021 für Deutschland" (KWRA 2021),
Teilbericht 6 (Integrierte Auswertung), Kapitel 3.4 „Analyse der Querverbindungen",
Abbildung 8 „Querverbindungen zwischen den Handlungsfeldern" (S. 83), dazu der Fließtext
auf S. 84 und S. 85.

Die KWRA veröffentlicht die Anzahlen je Handlungsfeld **nicht als Tabelle**, sondern nur als
Chord-Diagramm mit Skalen. Die Zahlen in ``HANDLUNGSFELDER`` sind deshalb eine **ausgewiesene
Ablesung** von KAP3 (Vorgabe P1), keine Tabellenwerte der Quelle. Wie abgelesen wurde und wie
genau, steht in ``ABLESUNG``. Nur die Rangaussagen (meiste ausgehende, meiste eingehende,
nur ausgehende, nur eingehende Beziehungen) sind wörtlich im Text der Quelle belegt; die
Ablesung ist so festgelegt, dass sie diesen Aussagen nicht widerspricht.
"""

from __future__ import annotations

QUELLE = (
    "UBA/BMU, ›Klimawirkungs- und Risikoanalyse 2021 für Deutschland‹, Teilbericht 6 "
    "(Integrierte Auswertung), Kapitel 3.4 ›Analyse der Querverbindungen‹, Abbildung 8 "
    "›Querverbindungen zwischen den Handlungsfeldern‹, S. 83; Fließtext S. 84–85. "
    "Dessau-Roßlau, 2021. Datei docs/KWAR/kwra2021_teilbericht_6_integrierte_auswertung_bf_211027_0.pdf."
)

ABLESUNG = (
    "Ausgewiesene Ablesung von KAP3 aus Abbildung 8 „Querverbindungen zwischen den "
    "Handlungsfeldern“, KWRA 2021, Teilbericht 6, Kap. 3.4, S. 83 — keine Tabelle der Quelle. "
    "Vorgehen: (1) Die Länge jedes Handlungsfeld-Bogens an seiner Skala abgelesen; sie ist die "
    "Summe aus ein- und ausgehenden Querbezügen des Handlungsfelds (Genauigkeit etwa ±3). "
    "(2) Die Aufteilung in aus- und eingehend nach den Balken am Bogen und nach dem Anteil der "
    "Verbindungen in der Farbe des Handlungsfelds abgelesen (Genauigkeit etwa ±5). "
    "(3) Die Aufteilung so abgestimmt, dass die Summe aller ausgehenden gleich der Summe aller "
    "eingehenden Querbezüge ist und dass die Rangaussagen des Fließtexts gelten: meiste "
    "ausgehende Wirkungen „Wasserhaushalt, Wasserwirtschaft“ (S. 84), am meisten beeinflusst "
    "„Tourismuswirtschaft“ (S. 85), nur ausgehend „Küsten- und Meeresschutz“ und nur eingehend "
    "„Tourismuswirtschaft“ (Hinweistext zu Abbildung 8, S. 83). "
    "Modellgrenze: Die Summe der Ablesung (251) liegt unter den 257 Querverbindungen der Quelle. "
    "Mögliche Ursachen sind die Ablesegenauigkeit oder Beziehungen innerhalb desselben "
    "Handlungsfelds, die die Abbildung nicht zeigt (Ursache in der Quelle nicht belegt). Die "
    "Verbindungen von Handlungsfeld zu Handlungsfeld (Dicke der Bänder) sind nicht als Zahl "
    "abgelesen."
)

# Genauigkeit der Ablesung (Anzahl Querbezüge, plus/minus)
GENAUIGKEIT_SUMME = 3
GENAUIGKEIT_AUFTEILUNG = 5

# Je Handlungsfeld: name, ausgehend, eingehend (abgelesen, siehe ABLESUNG).
# Reihenfolge wie in Abbildung 8 im Uhrzeigersinn, beginnend oben.
HANDLUNGSFELDER: list[dict] = [
    {"name": "Wasserhaushalt, Wasserwirtschaft", "ausgehend": 60, "eingehend": 12},
    {"name": "Wald- und Forstwirtschaft", "ausgehend": 6, "eingehend": 17},
    {"name": "Verkehr und Verkehrsinfrastruktur", "ausgehend": 12, "eingehend": 21},
    {"name": "Tourismuswirtschaft", "ausgehend": 0, "eingehend": 43},
    {"name": "Menschliche Gesundheit", "ausgehend": 10, "eingehend": 32},
    {"name": "Landwirtschaft", "ausgehend": 3, "eingehend": 30},
    {"name": "Küsten- und Meeresschutz", "ausgehend": 44, "eingehend": 0},
    {"name": "Industrie und Gewerbe", "ausgehend": 7, "eingehend": 35},
    {"name": "Fischerei", "ausgehend": 2, "eingehend": 10},
    {"name": "Energiewirtschaft", "ausgehend": 13, "eingehend": 19},
    {"name": "Boden", "ausgehend": 38, "eingehend": 6},
    {"name": "Biologische Vielfalt", "ausgehend": 38, "eingehend": 17},
    {"name": "Bauwesen", "ausgehend": 18, "eingehend": 9},
]


def summe(eintrag: dict) -> int:
    """Summe aus aus- und eingehenden Querbezügen (Bogenlänge in Abbildung 8)."""
    return eintrag["ausgehend"] + eintrag["eingehend"]


def meiste_ausgehende() -> str:
    return max(HANDLUNGSFELDER, key=lambda e: e["ausgehend"])["name"]


def meiste_eingehende() -> str:
    return max(HANDLUNGSFELDER, key=lambda e: e["eingehend"])["name"]
