"""KWRA-Querverbindungen (Wirkbeziehungen zwischen Klimawirkungen) — Teil 1.

Quelle: UBA/BMU „Klimawirkungs- und Risikoanalyse 2021 für Deutschland" (KWRA 2021),
Teilbericht 6 (Integrierte Auswertung), Kapitel 3.4 „Analyse der Querverbindungen".
Arbeitsmappe: ``docs/KWAR/KWRA-2021_Klimawirkungen.xlsx``, Blatt ``Wirkbeziehungen``
(kuratierte Übertragung aus Teilbericht 6) und Blatt ``Klimawirkungen``, Spalte
„Netzrolle (TB 6 Kap. 3.4)".

Die KWRA nennt 257 Querverbindungen zwischen den 102 Klimawirkungen insgesamt, veröffent-
licht die Einzelkanten aber in keinem der sechs Teilberichte als vollständige Liste
(Abbildung 8 in Teilbericht 6 ist ein Chord-Diagramm auf Handlungsfeldebene, aus dem sich
keine exakten Kantenzahlen ablesen lassen). Dieses Modul enthält deshalb **nur, was
Teilbericht 6 ausdrücklich belegt**:

  NETZROLLEN            — die 27 Klimawirkungen, die TB 6 Kap. 3.4 ausdrücklich als
                           starke Sender ("stark ausgehend") oder starke Empfänger
                           ("stark eingehend") im Wirkungsnetz benennt; ``rollen``
                           mehrwertig (Sender und Empfänger zugleich, Fn. 21, S. 84),
                           ``zentral`` für die ausdrücklich zentralen Klimawirkungen,
                           ``auswertungen`` trennt Gesamtbetrachtung („gesamt“) und
                           Auswertung der hoch bewerteten Klimawirkungen („hochrisiko“,
                           S. 86–87).
  HOCHRISIKO_BEFUNDE    — die Aussagen der gesonderten Auswertung der hoch bewerteten
                           Klimawirkungen (S. 86–88), je mit Seitenangabe.
  AUSSAGEN              — Annahme der Auswertung (S. 82), Einordnung nach Clustern und
                           Systembereichen (S. 84–85, 88) und mögliche Kaskadeneffekte
                           (S. 84, 87, 88), je im Wortlaut mit Seite.
  BENANNTE_BEZIEHUNGEN   — die im Fließtext von TB 6 Kap. 3.4 wörtlich genannten
                           Einzelbeziehungen (Auszug, nicht vollständig; 27 Einträge,
                           je mit ``richtung`` „gerichtet“ oder „gegenseitig“ und
                           Seitenangabe im ``beleg``; 7 davon aus dem Fließtext
                           ergänzt, nicht aus der Arbeitsmappe).
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
    "(Integrierte Auswertung), Kapitel 3.4 ›Analyse der Querverbindungen‹, Dessau-Roßlau, "
    "2021. Arbeitsmappe docs/KWAR/KWRA-2021_Klimawirkungen.xlsx, Blätter "
    "›Klimawirkungen‹ (Spalte Netzrolle) und ›Wirkbeziehungen‹."
)

# ── Netzrollen: Klimawirkungen mit ausdrücklich benannter starker Netzrolle ──────
#
# Jeder Eintrag: kwra_id (1–102, siehe Blatt "Klimawirkungen" Spalte "ID"),
# name (Klimawirkung), handlungsfeld, rolle ("stark ausgehend" | "stark eingehend"),
# rollen, zentral und — wo rollen zwei Werte hat oder zentral True ist — beleg_rolle.
#
# rolle:   Hauptrolle aus der Arbeitsmappe (Spalte „Netzrolle“), einwertig; bleibt für
#          bestehende Leser unverändert.
# rollen:  alle Rollen, die TB 6 Kap. 3.4 der Klimawirkung zuschreibt. Eine Klimawirkung
#          kann Sender und Empfänger zugleich sein (Fn. 21, S. 84); ausdrücklich belegt
#          ist das für #4 (S. 87, 88). Die zweite Rolle stammt aus dem Fließtext, nicht aus
#          der Arbeitsmappe.
# zentral: True, wo TB 6 Kap. 3.4 die Klimawirkung ausdrücklich „zentral“ nennt —
#          #49 Hochwasser in der Gesamtbetrachtung (S. 84, 88), #4 unter den hoch
#          bewerteten Klimawirkungen (S. 87, 88).
# beleg_rolle: Seite und Wortlaut für die zweite Rolle bzw. die Kennzeichnung „zentral“.
# auswertungen: in welcher Auswertung von TB 6 Kap. 3.4 die Netzrolle belegt ist —
#          „gesamt“ (Gesamtbetrachtung aller 102 Klimawirkungen, S. 82–86) und/oder
#          „hochrisiko“ (gesonderte Betrachtung der als hoch bewerteten Klimawirkungen,
#          Zeitscheiben Gegenwart, Mitte und Ende des Jahrhunderts, S. 86–87, Kernaussage
#          S. 88). Die Arbeitsmappe trennt beide Auswertungen nicht; wo ein Eintrag ganz oder
#          teilweise aus der Hochrisiko-Auswertung stammt, steht die Seite in beleg_auswertung.
#          #7 und #8 stehen nur im Fließtext S. 87, nicht in der Arbeitsmappe.
NETZROLLEN: list[dict] = [
    {"kwra_id": 1, "name": "Veränderung der Länge der Vegetationsperiode und Phänologie",
     "handlungsfeld": "Biologische Vielfalt", "rolle": "stark ausgehend",
     "rollen": ["stark ausgehend"], "zentral": False,
     "auswertungen": ["gesamt"]},
    {"kwra_id": 4, "name": "Verschiebung von Arealen und Rückgang der Bestände",
     "handlungsfeld": "Biologische Vielfalt", "rolle": "stark ausgehend",
     "rollen": ["stark ausgehend", "stark eingehend"], "zentral": True,
     "auswertungen": ["gesamt", "hochrisiko"],
     "beleg_auswertung": "TB6 Kap. 3.4: stark ausgehend in der Gesamtauswertung (S. 84); stark "
                         "eingehend und zentral in der Auswertung der hoch bewerteten "
                         "Klimawirkungen (S. 87, Kernaussage S. 88).",
     "beleg_rolle": "TB6 Kap. 3.4, S. 84, 87, 88 (Fn. 21 S. 84): viele ausgehende "
                    "Wirkbeziehungen (S. 84) und unter den hoch bewerteten Klimawirkungen "
                    "zugleich von vielen anderen beeinflusst (S. 87); nimmt dort „eine zentrale "
                    "Position mit vielen ausgehenden und eingehenden Wirkbeziehungen“ ein (S. 88). "
                    "Zentral bezogen auf die hoch bewerteten Klimawirkungen, nicht auf die "
                    "Gesamtbetrachtung."},
    {"kwra_id": 5, "name": "Schäden an Küstenökosystemen",
     "handlungsfeld": "Biologische Vielfalt", "rolle": "stark eingehend",
     "rollen": ["stark eingehend"], "zentral": False,
     "auswertungen": ["gesamt", "hochrisiko"],
     "beleg_auswertung": "TB6 Kap. 3.4: in der Gesamtauswertung als Ziel der Klimawirkungen des "
                         "Küsten- und Meeresschutzes genannt (S. 84); in der Auswertung der hoch "
                         "bewerteten Klimawirkungen ausdrücklich mit „besonders viele[n] "
                         "eingehende[n] Wirkbeziehungen“ (S. 87)."},
    {"kwra_id": 7, "name": "Schäden an Feuchtgebieten und wassergebundenen Habitaten",
     "handlungsfeld": "Biologische Vielfalt", "rolle": "stark eingehend",
     "rollen": ["stark eingehend"], "zentral": False,
     "auswertungen": ["hochrisiko"],
     "beleg_auswertung": "TB6 Kap. 3.4, S. 87 (nicht aus der Arbeitsmappe): unter den hoch "
                         "bewerteten Klimawirkungen „besonders viele eingehende "
                         "Wirkbeziehungen“. Name wie im Fließtext S. 87; die Arbeitsmappe führt "
                         "#7 als „Schäden an wassergebundenen Habitaten und Feuchtgebieten“."},
    {"kwra_id": 8, "name": "Schäden an Wäldern",
     "handlungsfeld": "Biologische Vielfalt", "rolle": "stark eingehend",
     "rollen": ["stark eingehend"], "zentral": False,
     "auswertungen": ["hochrisiko"],
     "beleg_auswertung": "TB6 Kap. 3.4, S. 87 (nicht aus der Arbeitsmappe): unter den hoch "
                         "bewerteten Klimawirkungen „besonders viele eingehende "
                         "Wirkbeziehungen“."},
    {"kwra_id": 12, "name": "Rutschungen und Muren",
     "handlungsfeld": "Boden", "rolle": "stark ausgehend",
     "rollen": ["stark ausgehend"], "zentral": False,
     "auswertungen": ["gesamt"]},
    {"kwra_id": 13, "name": "Wassermangel im Boden",
     "handlungsfeld": "Boden", "rolle": "stark ausgehend",
     "rollen": ["stark ausgehend"], "zentral": False,
     "auswertungen": ["gesamt"]},
    {"kwra_id": 14, "name": "Sickerwasser",
     "handlungsfeld": "Boden", "rolle": "stark ausgehend",
     "rollen": ["stark ausgehend"], "zentral": False,
     "auswertungen": ["gesamt"]},
    {"kwra_id": 15, "name": "Vernässung",
     "handlungsfeld": "Boden", "rolle": "stark ausgehend",
     "rollen": ["stark ausgehend"], "zentral": False,
     "auswertungen": ["gesamt"]},
    {"kwra_id": 25, "name": "Ertragsausfälle",
     "handlungsfeld": "Landwirtschaft", "rolle": "stark eingehend",
     "rollen": ["stark eingehend"], "zentral": False,
     "auswertungen": ["gesamt"]},
    {"kwra_id": 26, "name": "Qualität der Ernteprodukte",
     "handlungsfeld": "Landwirtschaft", "rolle": "stark eingehend",
     "rollen": ["stark eingehend"], "zentral": False,
     "auswertungen": ["gesamt"]},
    {"kwra_id": 31, "name": "Nutzfunktion: Holzertrag",
     "handlungsfeld": "Wald- und Forstwirtschaft", "rolle": "stark eingehend",
     "rollen": ["stark eingehend"], "zentral": False,
     "auswertungen": ["gesamt"]},
    {"kwra_id": 38, "name": "Meerestemperatur und Eisbedeckung",
     "handlungsfeld": "Küsten- und Meeresschutz", "rolle": "stark ausgehend",
     "rollen": ["stark ausgehend"], "zentral": False,
     "auswertungen": ["gesamt"]},
    {"kwra_id": 39, "name": "Wasserqualität und Grundwasserversalzung",
     "handlungsfeld": "Küsten- und Meeresschutz", "rolle": "stark ausgehend",
     "rollen": ["stark ausgehend"], "zentral": False,
     "auswertungen": ["gesamt"]},
    {"kwra_id": 40, "name": "Meeresspiegelhöhe",
     "handlungsfeld": "Küsten- und Meeresschutz", "rolle": "stark ausgehend",
     "rollen": ["stark ausgehend"], "zentral": False,
     "auswertungen": ["gesamt"]},
    {"kwra_id": 43, "name": "Sturmfluten",
     "handlungsfeld": "Küsten- und Meeresschutz", "rolle": "stark ausgehend",
     "rollen": ["stark ausgehend"], "zentral": False,
     "auswertungen": ["gesamt"]},
    {"kwra_id": 48, "name": "Niedrigwasser",
     "handlungsfeld": "Wasserhaushalt, Wasserwirtschaft", "rolle": "stark ausgehend",
     "rollen": ["stark ausgehend"], "zentral": False,
     "auswertungen": ["gesamt"]},
    {"kwra_id": 49, "name": "Hochwasser",
     "handlungsfeld": "Wasserhaushalt, Wasserwirtschaft", "rolle": "stark ausgehend",
     "rollen": ["stark ausgehend"], "zentral": True,
     "auswertungen": ["gesamt"],
     "beleg_rolle": "TB6 Kap. 3.4, S. 84, 88: „Eine zentrale Bedeutung in der Gesamtbetrachtung "
                    "aller Handlungsfelder hat die vorgelagerte Klimawirkung ›Hochwasser‹, die "
                    "sich auf die meisten anderen Klimawirkungen auswirkt“ (S. 84); weist „die "
                    "meisten ausgehenden Wirkbeziehungen“ auf (S. 88)."},
    {"kwra_id": 53, "name": "Gewässertemperatur und Eisbedeckung und biologische Wasserqualität",
     "handlungsfeld": "Wasserhaushalt, Wasserwirtschaft", "rolle": "stark ausgehend",
     "rollen": ["stark ausgehend"], "zentral": False,
     "auswertungen": ["gesamt"]},
    {"kwra_id": 55, "name": "Grundwasserstand und Grundwasserqualität",
     "handlungsfeld": "Wasserhaushalt, Wasserwirtschaft", "rolle": "stark eingehend",
     "rollen": ["stark eingehend"], "zentral": False,
     "auswertungen": ["gesamt"]},
    {"kwra_id": 73, "name": "Schiffbarkeit der Seeschifffahrtsstraßen",
     "handlungsfeld": "Verkehr, Verkehrsinfrastruktur", "rolle": "stark eingehend",
     "rollen": ["stark eingehend"], "zentral": False,
     "auswertungen": ["gesamt"]},
    {"kwra_id": 82, "name": "Beeinträchtigung des Warenverkehrs über Wasserstraßen (Inland)",
     "handlungsfeld": "Industrie und Gewerbe", "rolle": "stark eingehend",
     "rollen": ["stark eingehend"], "zentral": False,
     "auswertungen": ["gesamt"]},
    {"kwra_id": 92, "name": "Schäden an touristischen Infrastrukturen und Betriebsunterbrechungen",
     "handlungsfeld": "Tourismuswirtschaft", "rolle": "stark eingehend",
     "rollen": ["stark eingehend"], "zentral": False,
     "auswertungen": ["gesamt"]},
    {"kwra_id": 95, "name": "Hitzebelastung",
     "handlungsfeld": "Menschliche Gesundheit", "rolle": "stark eingehend",
     "rollen": ["stark eingehend"], "zentral": False,
     "auswertungen": ["gesamt"]},
    {"kwra_id": 96, "name": "Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft",
     "handlungsfeld": "Menschliche Gesundheit", "rolle": "stark eingehend",
     "rollen": ["stark eingehend"], "zentral": False,
     "auswertungen": ["gesamt"]},
    {"kwra_id": 97, "name": "Potenziell schädliche Mikroorganismen und Algen",
     "handlungsfeld": "Menschliche Gesundheit", "rolle": "stark eingehend",
     "rollen": ["stark eingehend"], "zentral": False,
     "auswertungen": ["gesamt"]},
    {"kwra_id": 101, "name": "Verletzungen und Todesfälle infolge von Extremereignissen",
     "handlungsfeld": "Menschliche Gesundheit", "rolle": "stark eingehend",
     "rollen": ["stark eingehend"], "zentral": False,
     "auswertungen": ["gesamt"]},
]

# ── Auswertung der hoch bewerteten Klimawirkungen (TB 6 Kap. 3.4, S. 86–88) ──────
#
# TB 6 betrachtet „in einem weiteren Analyseschritt“ nur die Querverbindungen der als hoch
# bewerteten Klimawirkungen (Zeitscheiben Gegenwart, Mitte und Ende des Jahrhunderts,
# S. 86). Die Aussagen dieser Auswertung stehen hier gesondert, damit sie nicht mit der
# Gesamtbetrachtung vermischt werden. Die Einzel-Klimawirkungen mit Netzrolle aus dieser
# Auswertung tragen in NETZROLLEN „hochrisiko“ in ``auswertungen``.
# Jeder Eintrag: ebene („Handlungsfeld“ | „Klimawirkung“ | „Cluster“ | „Auswertung“), name, kwra_ids
# (Klimawirkungen, auf die sich die Aussage bezieht; leer auf Handlungsfeld-/Clusterebene),
# aussage (nah am Wortlaut), seiten (gedruckte Seiten in TB 6).
HOCHRISIKO_BEFUNDE: list[dict] = [
    {"ebene": "Handlungsfeld", "name": "Biologische Vielfalt", "kwra_ids": [],
     "aussage": "Weist in der Auswertung der hoch bewerteten Klimawirkungen die höchste "
                "Gesamtzahl an Querverbindungen auf (Summe aus eingehenden und ausgehenden "
                "Wirkbeziehungen) und wird am häufigsten von anderen hoch bewerteten "
                "Klimawirkungen beeinflusst; die vielen eingehenden Wirkbeziehungen weisen auf "
                "die vielfache Gefährdung durch den Klimawandel hin.",
     "seiten": [86, 87, 88]},
    {"ebene": "Klimawirkung", "name": "Besonders viele eingehende Wirkbeziehungen",
     "kwra_ids": [5, 7, 8, 4],
     "aussage": "Besonders viele eingehende Wirkbeziehungen bei „Schäden an "
                "Küstenökosystemen“, „Schäden an Feuchtgebieten und wassergebundenen "
                "Habitaten“, „Schäden an Wäldern“ und „Verschiebung von Arealen und Rückgang "
                "der Bestände“.",
     "seiten": [87]},
    {"ebene": "Klimawirkung", "name": "Verschiebung von Arealen und Rückgang der Bestände",
     "kwra_ids": [4],
     "aussage": "Wird von vielen anderen Klimawirkungen beeinflusst und wirkt zugleich auf die "
                "Handlungsfelder Landwirtschaft, Wald- und Forstwirtschaft, Fischerei, "
                "Bauwesen und Menschliche Gesundheit; nimmt eine zentrale Position innerhalb "
                "der hoch bewerteten Klimawirkungen ein.",
     "seiten": [87, 88]},
    {"ebene": "Handlungsfeld", "name": "Küsten- und Meeresschutz; Wasserhaushalt, Wasserwirtschaft",
     "kwra_ids": [],
     "aussage": "Wichtige Einflussfaktoren kommen insbesondere aus den vorgelagerten "
                "Klimawirkungen dieser beiden Handlungsfelder.",
     "seiten": [87]},
    {"ebene": "Cluster", "name": "Land und Wasser", "kwra_ids": [],
     "aussage": "Bei Betrachtung der hohen Klimarisiken ergibt sich eine engere Verflechtung "
                "der Cluster Land und Wasser.",
     "seiten": [87]},
    {"ebene": "Auswertung", "name": "Unterschied zur Gesamtbetrachtung", "kwra_ids": [],
     "aussage": "Unterschiede zur Gesamtbetrachtung ergaben sich vor allem für die "
                "eingehenden Wirkbeziehungen.",
     "seiten": [86]},
]

# ── Übernommene Aussagen der Auswertung (TB 6 Kap. 3.4, S. 82–88) ────────────────
#
# Aussagen von Kap. 3.4, die keine Netzrolle und keine Einzelbeziehung sind, aber sagen, wie die
# Auswertung zu lesen ist: die Annahme, auf der sie beruht (S. 82), die Einordnung der Ergebnisse
# nach Clustern und Systembereichen (S. 84–85, Kernaussagen S. 88) und die möglichen
# Kaskadeneffekte (S. 84, 87, Kernaussage S. 88).
# Jeder Eintrag: titel, wortlaut (wörtlich aus TB 6, Auslassungen mit „…“), seite (gedruckte
# Seite der Hauptstelle, = PDF-Seite), seiten (alle Stellen, an denen die Aussage steht), beleg.
AUSSAGEN: dict[str, dict] = {
    "annahme": {
        "titel": "Annahme der Auswertung",
        "wortlaut": "Die Auswertung basiert auf der Annahme, dass negative Auswirkungen des "
                    "Klimawandels auf eine Klimawirkung auch negative Folgen für die ihr "
                    "nachgelagerten Wirkungen haben.",
        "seite": 82,
        "seiten": [82],
        "beleg": "TB6 Kap. 3.4, S. 82, letzter Satz vor Fußnote 20.",
    },
    "einordnung_cluster": {
        "titel": "Einordnung nach Clustern und Systembereichen",
        "wortlaut": "Alle Handlungsfelder mit verhältnismäßig vielen ausgehenden "
                    "Wirkbeziehungen sind Teil der Cluster Wasser und Land … fast alle "
                    "Klimawirkungen mit den meisten ausgehenden Wirkbeziehungen zählen zu den "
                    "natürlichen Systemen und Ressourcen. … Alle genannten Handlungsfelder mit "
                    "einer hohen Anzahl an eingehenden Wirkungen gehören bis auf die "
                    "Landwirtschaft zu den Clustern Wirtschaft und Gesundheit. Ausgehende "
                    "Wirkungen finden sich also vor allem in Bezug auf natürliche Systeme und "
                    "Ressourcen, während eingehende Wirkungen naturnutzende "
                    "Wirtschaftssysteme, Infrastrukturen und Gebäude sowie Menschen und soziale "
                    "Systeme betreffen.",
        "seite": 85,
        "seiten": [84, 85, 88],
        "beleg": "TB6 Kap. 3.4, S. 84 (Cluster Wasser und Land), S. 85 (natürliche Systeme und "
                 "Ressourcen; Cluster Wirtschaft und Gesundheit; Systembereiche), Kernaussagen "
                 "S. 88 (zweiter und dritter Punkt).",
    },
    "kaskadeneffekte": {
        "titel": "Mögliche Kaskadeneffekte",
        "wortlaut": "Die Handlungsfelder mit verhältnismäßig vielen ausgehenden "
                    "Wirkbeziehungen sind Teil der Cluster Wasser und Land, welche zukünftig "
                    "besonders stark vom Klimawandel betroffen sein werden. Dies kann unter "
                    "Umständen Kaskadeneffekte bei einer Vielzahl der mit ihnen verknüpften "
                    "Klimawirkungen und Handlungsfelder in den Clustern Wirtschaft, "
                    "Infrastruktur und Gesundheit auslösen.",
        "seite": 88,
        "seiten": [84, 87, 88],
        "beleg": "TB6 Kap. 3.4, Kernaussagen S. 88 (vierter Punkt); gleichlautend S. 84, dort "
                 "ergänzt: viele Wirkbeziehungen innerhalb des Clusters Land (Boden, Biologische "
                 "Vielfalt, Landwirtschaft) „könnte“ den Effekt verstärken; S. 87: schon die "
                 "VA 2015 stellte einen „kaskadenartigen Effekt“ der Cluster Land und Wasser auf "
                 "die Cluster Wirtschaft, Gesundheit und Infrastruktur fest.",
    },
}

# ── Im Fließtext ausdrücklich benannte Einzelbeziehungen (Auszug) ───────────────
#
# quelle/ziel: Wortlaut aus TB 6 Kap. 3.4. quelle_kwra_id/ziel_kwra_id sind gesetzt,
# wenn Quelle bzw. Ziel eine einzelne, eindeutig identifizierbare Klimawirkung ist
# (sonst None — z. B. bei Handlungsfeld-Ebene oder mehreren genannten Zielen).
# richtung: "gerichtet" (quelle wirkt auf ziel) oder "gegenseitig" (Wechselwirkung in
# beide Richtungen, TB 6 S. 82 und 85–86; quelle/ziel sind dann nur die Lesereihenfolge).
# beleg: Kapitel und Seite in TB 6 (Seitenzahl = gedruckte Seite = PDF-Seite).
BENANNTE_BEZIEHUNGEN: list[dict] = [
    {"quelle": "Hochwasser", "quelle_kwra_id": 49,
     "ziel": "zahlreiche Klimawirkungen in mehreren Handlungsfeldern", "ziel_kwra_id": None,
     "ebene": "Klimawirkung",
     "richtung": "gerichtet",
     "beleg": "TB6 Kap. 3.4, S. 84, 88: zentrale Klimawirkung, wirkt sich auf die meisten anderen aus"},
    {"quelle": "Gewässertemperatur und Eisbedeckung und biologische Wasserqualität",
     "quelle_kwra_id": 53,
     "ziel": "Potenziell schädliche Mikroorganismen und Algen", "ziel_kwra_id": 97,
     "ebene": "Klimawirkung", "richtung": "gerichtet",
     "beleg": "TB6 Kap. 3.4, S. 84: fördert deren Entwicklung"},
    {"quelle": "Stadtklima / Wärmeinseln", "quelle_kwra_id": 62,
     "ziel": "Hitzebelastung", "ziel_kwra_id": 95,
     "ebene": "Klimawirkung",
     "richtung": "gerichtet",
     "beleg": "TB6 Kap. 3.4, S. 85: zunehmender urbaner Wärmeinseleffekt erhöht die Hitzebelastung"},
    {"quelle": "Veränderung der Länge der Vegetationsperiode und Phänologie",
     "quelle_kwra_id": 1,
     "ziel": "Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft",
     "ziel_kwra_id": 96, "ebene": "Klimawirkung",
     "richtung": "gerichtet",
     "beleg": "TB6 Kap. 3.4, S. 85: verlängerte Vegetationsperiode verstärkt Pollenreaktionen"},
    {"quelle": "Hochwasser", "quelle_kwra_id": 49,
     "ziel": "Verletzungen und Todesfälle infolge von Extremereignissen", "ziel_kwra_id": 101,
     "ebene": "Klimawirkung", "richtung": "gerichtet",
     "beleg": "TB6 Kap. 3.4, S. 85"},
    {"quelle": "Sturzfluten (Versagen von Entwässerungseinrichtungen und "
               "Überflutungsschutzsystemen)", "quelle_kwra_id": 51,
     "ziel": "Verletzungen und Todesfälle infolge von Extremereignissen", "ziel_kwra_id": 101,
     "ebene": "Klimawirkung", "richtung": "gerichtet",
     "beleg": "TB6 Kap. 3.4, S. 85"},
    {"quelle": "Niedrigwasser", "quelle_kwra_id": 48,
     "ziel": "Beeinträchtigung des Warenverkehrs über Wasserstraßen (Inland)",
     "ziel_kwra_id": 82, "ebene": "Klimawirkung",
     "richtung": "gerichtet",
     "beleg": "TB6 Kap. 3.4, S. 84, 85: niedrigwasserbedingte Einschränkungen im Warentransport"},
    {"quelle": "Hochwasser", "quelle_kwra_id": 49,
     "ziel": "Schäden / Hindernisse bei Straßen und Schienenwegen (Hochwasser)",
     "ziel_kwra_id": 74, "ebene": "Klimawirkung",
     "richtung": "gerichtet",
     "beleg": "TB6 Kap. 3.4, S. 84: Beeinträchtigung der Verkehrswege"},
    {"quelle": "Boden (Handlungsfeld)", "quelle_kwra_id": None,
     "ziel": "Grundwasserstand und Grundwasserqualität", "ziel_kwra_id": 55,
     "ebene": "gemischt",
     "richtung": "gerichtet",
     "beleg": "TB6 Kap. 3.4, S. 84: viele Klimawirkungen des Bodens wirken hierauf ein"},
    {"quelle": "Boden und Biologische Vielfalt (Handlungsfelder)", "quelle_kwra_id": None,
     "ziel": "Ertragsausfälle", "ziel_kwra_id": 25, "ebene": "gemischt",
     "richtung": "gerichtet",
     "beleg": "TB6 Kap. 3.4, S. 84, 85: landwirtschaftliche Ertragsausfälle werden von vielen "
              "Klimawirkungen dieser Handlungsfelder beeinflusst"},
    {"quelle": "Boden und Biologische Vielfalt (Handlungsfelder)", "quelle_kwra_id": None,
     "ziel": "Qualität der Ernteprodukte", "ziel_kwra_id": 26, "ebene": "gemischt",
     "richtung": "gerichtet",
     "beleg": "TB6 Kap. 3.4, S. 84"},
    {"quelle": "Boden und Biologische Vielfalt (Handlungsfelder)", "quelle_kwra_id": None,
     "ziel": "Nutzfunktion: Holzertrag", "ziel_kwra_id": 31, "ebene": "gemischt",
     "richtung": "gerichtet",
     "beleg": "TB6 Kap. 3.4, S. 84: weitere Auswirkungen auf Holzerträge in der Forstwirtschaft"},
    {"quelle": "Küsten- und Meeresschutz (Handlungsfeld)", "quelle_kwra_id": None,
     "ziel": "Schiffbarkeit der Seeschifffahrtsstraßen", "ziel_kwra_id": 73,
     "ebene": "gemischt", "richtung": "gerichtet",
     "beleg": "TB6 Kap. 3.4, S. 84"},
    {"quelle": "Küsten- und Meeresschutz (Handlungsfeld)", "quelle_kwra_id": None,
     "ziel": "Schäden an touristischen Infrastrukturen und Betriebsunterbrechungen",
     "ziel_kwra_id": 92, "ebene": "gemischt", "richtung": "gerichtet",
     "beleg": "TB6 Kap. 3.4, S. 84"},
    {"quelle": "Küsten- und Meeresschutz (Handlungsfeld)", "quelle_kwra_id": None,
     "ziel": "Schäden an Küstenökosystemen", "ziel_kwra_id": 5,
     "ebene": "gemischt", "richtung": "gerichtet",
     "beleg": "TB6 Kap. 3.4, S. 84"},
    {"quelle": "Wasserhaushalt, Wasserwirtschaft (Handlungsfeld)", "quelle_kwra_id": None,
     "ziel": "Industrie und Gewerbe (Handlungsfeld)", "ziel_kwra_id": None,
     "ebene": "Handlungsfeld",
     "richtung": "gerichtet",
     "beleg": "TB6 Kap. 3.4, S. 85: Einschränkungen der Wasserversorgung treffen die Produktion"},
    {"quelle": "Energiewirtschaft (Handlungsfeld)", "quelle_kwra_id": None,
     "ziel": "Industrie und Gewerbe (Handlungsfeld)", "ziel_kwra_id": None,
     "ebene": "Handlungsfeld",
     "richtung": "gerichtet",
     "beleg": "TB6 Kap. 3.4, S. 85: Einschränkungen der Energieversorgung treffen die Produktion"},
    {"quelle": "Küsten- und Meeresschutz (Handlungsfeld)", "quelle_kwra_id": None,
     "ziel": "Tourismuswirtschaft (Handlungsfeld)", "ziel_kwra_id": None,
     "ebene": "Handlungsfeld",
     "richtung": "gerichtet",
     "beleg": "TB6 Kap. 3.4, S. 84, 85: viele eingehende Wirkungen beim Tourismus"},
    {"quelle": "Biologische Vielfalt (Handlungsfeld)", "quelle_kwra_id": None,
     "ziel": "Tourismuswirtschaft (Handlungsfeld)", "ziel_kwra_id": None,
     "ebene": "Handlungsfeld", "richtung": "gerichtet",
     "beleg": "TB6 Kap. 3.4, S. 85"},
    {"quelle": "Wasserhaushalt, Wasserwirtschaft (Handlungsfeld)", "quelle_kwra_id": None,
     "ziel": "Tourismuswirtschaft (Handlungsfeld)", "ziel_kwra_id": None,
     "ebene": "Handlungsfeld", "richtung": "gerichtet",
     "beleg": "TB6 Kap. 3.4, S. 85"},
    # Ab hier: im Fließtext genannt, nicht aus der Arbeitsmappe (Blatt „Wirkbeziehungen“
    # führt diese Beziehungen nicht; Befund 2 in reviews/BEFUNDE_QUERVERBINDUNGEN.md).
    {"quelle": "Wassermangel im Boden", "quelle_kwra_id": 13,
     "ziel": "Schäden in Wäldern", "ziel_kwra_id": 8,
     "ebene": "Klimawirkung", "richtung": "gerichtet",
     "beleg": "TB6 Kap. 3.4, S. 82 (nicht aus der Arbeitsmappe): verstärkter Wassermangel im "
              "Boden kann zu trockenheitsbedingten Schäden in Wäldern führen"},
    {"quelle": "Schäden in Wäldern", "quelle_kwra_id": 8,
     "ziel": "Nutzfunktion: Holzertrag", "ziel_kwra_id": 31,
     "ebene": "Klimawirkung", "richtung": "gerichtet",
     "beleg": "TB6 Kap. 3.4, S. 82 (nicht aus der Arbeitsmappe): Schäden in Wäldern wirken "
              "auf die Nutzfunktion Holzertrag"},
    {"quelle": "Schäden in Wäldern", "quelle_kwra_id": 8,
     "ziel": "Nutzfunktion: Erholung", "ziel_kwra_id": 32,
     "ebene": "Klimawirkung", "richtung": "gerichtet",
     "beleg": "TB6 Kap. 3.4, S. 82 (nicht aus der Arbeitsmappe): Schäden in Wäldern wirken "
              "auf die Nutzfunktion Erholung"},
    {"quelle": "Gewässertemperatur und Eisbedeckung und biologische Wasserqualität",
     "quelle_kwra_id": 53,
     "ziel": "Mangelndes Kühlwasser für thermische Kraftwerke", "ziel_kwra_id": 68,
     "ebene": "Klimawirkung", "richtung": "gegenseitig",
     "beleg": "TB6 Kap. 3.4, S. 82, 85 (nicht aus der Arbeitsmappe): steigende "
              "Gewässertemperatur schränkt Entnahme und Einleitung von Kühlwasser ein; "
              "eingeleitetes Kühlwasser erhöht die Gewässertemperatur"},
    {"quelle": "Bedarf an Kühlenergie", "quelle_kwra_id": 65,
     "ziel": "Stadtklima/Wärmeinseln", "ziel_kwra_id": 62,
     "ebene": "Klimawirkung", "richtung": "gegenseitig",
     "beleg": "TB6 Kap. 3.4, S. 85, Abb. 9 S. 86 (nicht aus der Arbeitsmappe): wärmeres "
              "Stadtklima steigert den Bedarf an Kühlenergie; Kühlenergieverbrauch erhöht die "
              "Temperatur im innerstädtischen Raum"},
    {"quelle": "Hitzebelastung", "quelle_kwra_id": 95,
     "ziel": "Bedarf an Kühlenergie", "ziel_kwra_id": 65,
     "ebene": "Klimawirkung", "richtung": "gerichtet",
     "beleg": "TB6 Kap. 3.4, S. 85–86, Abb. 9 S. 86 (nicht aus der Arbeitsmappe): "
              "Hitzebelastung wirkt auf den Bedarf an Kühlenergie; schließt den einzigen "
              "Rückkopplungskreislauf der Gesamtauswertung"},
    {"quelle": "Verschiebung von Arealen und Rückgang der Bestände", "quelle_kwra_id": 4,
     "ziel": "Vegetation in Siedlungen", "ziel_kwra_id": 61,
     "ebene": "Klimawirkung", "richtung": "gegenseitig",
     "beleg": "TB6 Kap. 3.4, S. 86 (nicht aus der Arbeitsmappe): etwas schwächer ausgeprägte "
              "Wechselwirkung zwischen Stadtvegetation und Rückgang der Bestände"},
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
