"""KWRA-Rückkopplungen: gegenseitige Wechselwirkungen und der Kreislauf Hitzebelastung.

Quelle: UBA/BMU „Klimawirkungs- und Risikoanalyse 2021 für Deutschland" (KWRA 2021),
Teilbericht 6 (Integrierte Auswertung), Kapitel 3.4 „Analyse der Querverbindungen",
S. 82, 85 und 86 (Fließtext) sowie Abbildung 9 auf S. 86.

Teilbericht 6 nennt neben den einseitigen Querverbindungen genau drei gegenseitige
Wechselwirkungen (S. 85–86). Eine davon ist Teil des **einzigen Rückkopplungskreislaufs**
der Gesamtauswertung (S. 86, Abbildung 9): Hitzebelastung → Bedarf an Kühlenergie ↔
Stadtklima/Wärmeinseln → Hitzebelastung. Dieses Modul übernimmt diese Angaben wörtlich;
es ist keine eigene Netzanalyse.

  RUECKKOPPLUNGEN — je Eintrag:
    id        — feste Kennung des Eintrags
    art       — „wechselwirkung" (zwei Klimawirkungen beeinflussen sich gegenseitig)
                oder „kreislauf" (Rückkopplungskreislauf über mehrere Klimawirkungen)
    knoten    — beteiligte Klimawirkungen: kwra_id (Blatt „Klimawirkungen" der Arbeitsmappe
                docs/KWAR/KWRA-2021_Klimawirkungen.xlsx, Spalte „ID"), name, handlungsfeld
    kanten    — gerichtete Wirkbeziehungen (von_kwra_id → nach_kwra_id); eine gegenseitige
                Wirkung steht als zwei Kanten
    staerke   — „schwächer ausgeprägt", wo die Quelle das sagt, sonst None
    seiten    — Seiten in Teilbericht 6, auf denen der Eintrag belegt ist
    abbildung — Abbildung in Teilbericht 6, falls vorhanden
    beleg     — Kurzfassung der Textstelle
    quellen   — in Teilbericht 6 an der Stelle zitierte Literatur

Die Pfeilrichtungen des Kreislaufs sind eine ausgewiesene Ablesung aus Abbildung 9 (S. 86):
Pfeil Stadtklima/Wärmeinseln → Hitzebelastung, Pfeil Hitzebelastung → Bedarf an
Kühlenergie, Doppelpfeil Bedarf an Kühlenergie ↔ Stadtklima/Wärmeinseln. Der Fließtext
auf S. 85–86 beschreibt dieselben Richtungen.

Ob eine Klimawirkung im Katalog des Produkts steht, trägt dieses Modul bewusst nicht; das
ergibt sich aus ``app.data.catalog`` (Hitzebelastung #95 und Stadtklima #62 stehen dort,
Bedarf an Kühlenergie #65 nicht).
"""

from __future__ import annotations

QUELLE = (
    "UBA/BMU, ›Klimawirkungs- und Risikoanalyse 2021 für Deutschland‹, Teilbericht 6 "
    "(Integrierte Auswertung), Kapitel 3.4 ›Analyse der Querverbindungen‹, S. 82, 85–86 "
    "und Abbildung 9 (S. 86), Dessau-Roßlau, 2021. Kennungen der Klimawirkungen aus der "
    "Arbeitsmappe docs/KWAR/KWRA-2021_Klimawirkungen.xlsx, Blatt ›Klimawirkungen‹."
)

_HITZE = {"kwra_id": 95, "name": "Hitzebelastung",
          "handlungsfeld": "Menschliche Gesundheit"}
_KUEHLENERGIE = {"kwra_id": 65, "name": "Bedarf an Kühlenergie",
                 "handlungsfeld": "Energiewirtschaft"}
_STADTKLIMA = {"kwra_id": 62, "name": "Stadtklima/Wärmeinseln",
               "handlungsfeld": "Bauwesen"}

RUECKKOPPLUNGEN: list[dict] = [
    {
        "id": "RK-1",
        "art": "wechselwirkung",
        "knoten": [
            {"kwra_id": 53,
             "name": "Gewässertemperatur und Eisbedeckung und biologische Wasserqualität",
             "handlungsfeld": "Wasserhaushalt, Wasserwirtschaft"},
            {"kwra_id": 68, "name": "Mangelndes Kühlwasser für thermische Kraftwerke",
             "handlungsfeld": "Energiewirtschaft"},
        ],
        "kanten": [
            {"von_kwra_id": 53, "nach_kwra_id": 68},
            {"von_kwra_id": 68, "nach_kwra_id": 53},
        ],
        "staerke": None,
        "seiten": [82, 85],
        "abbildung": None,
        "beleg": (
            "Steigende Gewässertemperaturen schränken Entnahme und Einleitung von Kühlwasser "
            "ein; Einleitung und Entnahme durch thermische Kraftwerke können ihrerseits die "
            "Gewässertemperatur erhöhen (S. 82, wieder aufgegriffen S. 85)."
        ),
        "quellen": ["LAWA 2017"],
    },
    {
        "id": "RK-2",
        "art": "kreislauf",
        "knoten": [dict(_HITZE), dict(_KUEHLENERGIE), dict(_STADTKLIMA)],
        "kanten": [
            {"von_kwra_id": 62, "nach_kwra_id": 95},
            {"von_kwra_id": 95, "nach_kwra_id": 65},
            {"von_kwra_id": 65, "nach_kwra_id": 62},
            {"von_kwra_id": 62, "nach_kwra_id": 65},
        ],
        "staerke": None,
        "seiten": [85, 86],
        "abbildung": "Abbildung 9",
        "beleg": (
            "Ein wärmeres Stadtklima steigert den Bedarf an Kühlenergie; ein erhöhter "
            "Kühlenergieverbrauch, vor allem durch Klimaanlagen, erhöht die Temperatur im "
            "innerstädtischen Raum. Zusammen mit der Hitzebelastung, die dadurch verstärkt "
            "auftreten kann und sich wiederum auf den Bedarf an Kühlenergie auswirkt, bildet "
            "das einen Kreislauf. Er ist der einzige Rückkopplungskreislauf der "
            "Gesamtauswertung; Anpassung an ihn liegt neben dem Bund auch in der "
            "Verantwortlichkeit der Kommunen (S. 85–86, Abbildung 9)."
        ),
        "quellen": ["Salamanca et al. 2014", "IEA und OECD 2018"],
    },
    {
        "id": "RK-3",
        "art": "wechselwirkung",
        "knoten": [
            {"kwra_id": 4, "name": "Verschiebung von Arealen und Rückgang der Bestände",
             "handlungsfeld": "Biologische Vielfalt"},
            {"kwra_id": 61, "name": "Vegetation in Siedlungen",
             "handlungsfeld": "Bauwesen"},
        ],
        "kanten": [
            {"von_kwra_id": 61, "nach_kwra_id": 4},
            {"von_kwra_id": 4, "nach_kwra_id": 61},
        ],
        "staerke": "schwächer ausgeprägt",
        "seiten": [86],
        "abbildung": None,
        "beleg": (
            "Eine stark beeinträchtigte Stadtvegetation kann zum Rückgang der Bestände "
            "beitragen; Arealverschiebungen können Arten der Stadt- und Siedlungsvegetation "
            "ungünstigere Wachstumsbedingungen bringen (S. 86)."
        ),
        "quellen": ["LWG 2018", "Schönfeld 2019"],
    },
]

KREISLAUF: dict = next(e for e in RUECKKOPPLUNGEN if e["art"] == "kreislauf")
