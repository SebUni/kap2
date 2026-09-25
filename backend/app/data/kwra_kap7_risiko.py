"""Bereichsvergleich der Bundesanalyse — Risiko, Gewissheit, Dringlichkeit, Einflüsse.

Konformitäts-Checkliste Zeile 10, Anforderungen A2, A6, A7 und A9 (T-1124-cto, Vorhaben
T-0980-ceo).

Quelle: UBA/BMU, KWRA 2021, Teilbericht 6 (Integrierte Auswertung), Kap. 7
„Querbetrachtung der Systembereiche“, S. 146–154 (im Kapitel stimmen PDF-Seite und gedruckte
Seite überein). Datei: ``docs/KWAR/kwra2021_teilbericht_6_integrierte_auswertung_bf_211027_0.pdf``.

Das Modul **übernimmt** den Vergleich der fünf Systembereiche aus dem Text der Bundesanalyse,
es rechnet nichts neu. Je Bereich stehen vier Blöcke, jeder mit den Seiten, auf denen er steht:

- ``risiko_ohne_anpassung`` (A2): die Vergleichsaussage und die Zahl oder der Anteil der hoch
  bewerteten Klimawirkungen, so wie der Text sie nennt — mit Zeitscheibe und Fall. Nennt der
  Text keinen Fall, steht ``fall: None``. Die Angabe zum Ende des Jahrhunderts setzt im
  Text meist den Satz zur Mitte fort („und die Zahl kann … ansteigen“); sie trägt dann den
  Fall dieses Satzes. Eine eigene Auszählung aus der Arbeitsmappe ist eine
  fachliche Festlegung beim CMO (T-1144-ceo, F1) und steht hier nicht.
- ``gewissheit`` (A6): getrennt für das Klimarisiko ohne Anpassung und für die
  Anpassungskapazität; sagt der Text zu einem Teil nichts, steht ``None``.
- ``handlungserfordernisse`` (A7): Zahl der sehr dringenden und der dringenden
  Handlungserfordernisse.
- ``klimatische_einfluesse`` (A9): die maßgeblichen klimatischen Einflüsse, dazu die
  Einflüsse, die der Text als entlastend nennt.

Abbildung 24 (S. 152) zeigt dieselben Größen grafisch; sie ist in ``ABBILDUNG_24`` vermerkt.
Die Werte dieses Moduls stammen aus dem Fließtext, nicht aus der Grafik.
"""

from __future__ import annotations

QUELLE = (
    "UBA/BMU, ›Klimawirkungs- und Risikoanalyse 2021 für Deutschland‹, Teilbericht 6 "
    "(Integrierte Auswertung), Kapitel 7 ›Querbetrachtung der Systembereiche‹, S. 146–154, "
    "Dessau-Roßlau, 2021."
)

ABBILDUNG_24 = {
    "nummer": 24,
    "seite": 152,
    "titel": "Klimarisiken von betroffenen Systemen, Wirkbeziehungen und Dringlichkeit von Anpassung",
    "hinweis": "nur grafisch, Abb. 24, S. 152",
}

ZEITSCHEIBEN = ("gegenwart", "mitte", "ende")
FAELLE = ("optimistisch", "pessimistisch")

_NAT = "Natürliche Systeme und Ressourcen"
_NNW = "Naturnutzende Wirtschaftssysteme"
_INF = "Infrastrukturen und Gebäude"
_NFW = "Naturferne Wirtschaftssysteme"
_MEN = "Menschen und soziale Systeme"


def _hoch(zeitscheibe: str, fall: str | None, *, anzahl: int | None = None,
          anteil_prozent: int | None = None, wortlaut: str, seite: int) -> dict:
    """Eine Angabe des Textes zur Zahl oder zum Anteil hoch bewerteter Klimawirkungen."""
    return {
        "zeitscheibe": zeitscheibe,
        "fall": fall,
        "anzahl_hoch": anzahl,
        "anteil_prozent": anteil_prozent,
        "wortlaut": wortlaut,
        "seite": seite,
    }


BEREICHSVERGLEICH_RISIKO: dict[str, dict] = {
    _NAT: {
        "anzahl_klimawirkungen": 30,
        "risiko_ohne_anpassung": {
            "vergleich": "am stärksten betroffen; Klimarisiken am Ende des Jahrhunderts auf "
                         "gleicher Höhe wie bei „Menschen und soziale Systeme“, also relativ hoch",
            "hoch_bewertet": [
                _hoch("mitte", None, anteil_prozent=60, seite=146,
                      wortlaut="60 Prozent der untersuchten Klimawirkungen – werden bereits zur "
                               "Mitte des Jahrhunderts hohe Klimarisiken erwartet"),
                _hoch("ende", None, anteil_prozent=70, seite=146,
                      wortlaut="die Zahl steigt bis zum Ende des Jahrhunderts auf 70 Prozent"),
            ],
            "seiten": [146, 151, 153],
        },
        "gewissheit": {
            "risiko_ohne_anpassung": "tendenziell geringer als in den anderen Bereichen",
            "anpassungskapazitaet": "tendenziell geringer als in den anderen Bereichen",
            "seiten": [147],
        },
        "handlungserfordernisse": {"sehr_dringend": 11, "dringend": 5, "seiten": [147]},
        "klimatische_einfluesse": {
            "einfluesse": ["gradueller Temperaturanstieg", "Hitze", "Trockenheit",
                           "Starkwind (potentiell)"],
            "entlastend": [],
            "seiten": [146],
        },
    },
    _NNW: {
        "anzahl_klimawirkungen": 31,
        "risiko_ohne_anpassung": {
            "vergleich": "erkennbar geringer als bei den natürlichen Systemen und Ressourcen, "
                         "über alle Zeitscheiben und in beiden Fällen, aber keineswegs gering",
            "hoch_bewertet": [
                _hoch("mitte", "pessimistisch", anzahl=9, seite=148,
                      wortlaut="Neun Klimawirkungen, das heißt knapp ein Drittel, können zur "
                               "Mitte des Jahrhunderts im pessimistischen Fall ein hohes "
                               "Klimarisiko aufweisen"),
                _hoch("ende", "pessimistisch", anzahl=16, seite=148,
                      wortlaut="die Zahl kann bis zum Ende des Jahrhunderts auf 16, also gut "
                               "die Hälfte aller Klimawirkungen in diesem Bereich ansteigen"),
            ],
            "seiten": [147, 148],
        },
        "gewissheit": {
            "risiko_ohne_anpassung": "für die Gegenwart relativ hoch, sinkt für die Zukunft auf "
                                     "den Gesamtdurchschnitt aller Systembereiche",
            "anpassungskapazitaet": None,
            "seiten": [148],
        },
        "handlungserfordernisse": {"sehr_dringend": 10, "dringend": 6, "seiten": [148, 149]},
        "klimatische_einfluesse": {
            "einfluesse": ["Trockenheit", "Hitze (in Kombination mit Trockenheit)",
                           "gradueller Temperaturanstieg"],
            "entlastend": [],
            "seiten": [148],
        },
    },
    _INF: {
        "anzahl_klimawirkungen": 23,
        "risiko_ohne_anpassung": {
            "vergleich": "deutlich niedriger als der Durchschnitt aller Klimawirkungen, im "
                         "Schnitt etwa eine halbe Stufe niedriger als bei den natürlichen "
                         "Systemen und Ressourcen, über alle Zeitscheiben und beide Fälle",
            "hoch_bewertet": [
                _hoch("mitte", "pessimistisch", anzahl=6, seite=149,
                      wortlaut="Mitte des Jahrhunderts sind sechs Klimawirkungen im "
                               "pessimistischen Fall mit hoch bewertet, also etwa ein Viertel"),
                _hoch("ende", "pessimistisch", anzahl=8, seite=149,
                      wortlaut="Ende des Jahrhunderts dann acht, also etwa ein Drittel"),
            ],
            "seiten": [149],
        },
        "gewissheit": {
            "risiko_ohne_anpassung": None,
            "anpassungskapazitaet": "bei beschlossenen wie weiterreichenden Maßnahmen deutlich "
                                    "über den anderen Systembereichen",
            "seiten": [149],
        },
        "handlungserfordernisse": {"sehr_dringend": 7, "dringend": 7, "seiten": [150]},
        "klimatische_einfluesse": {
            "einfluesse": ["Starkregen", "Überschwemmungen und Überflutungen",
                           "Starkwind (potentiell, keine klaren Projektionen)",
                           "Meeresspiegelanstieg (in Verbindung mit Sturmfluten)"],
            "entlastend": ["weniger Frost", "weniger Schneefall",
                           "geringere Schnee- und Eislasten"],
            "seiten": [149],
        },
    },
    _NFW: {
        "anzahl_klimawirkungen": 7,
        "risiko_ohne_anpassung": {
            "vergleich": "noch deutlich niedriger als bei „Infrastrukturen und Gebäude“ und mit "
                         "Abstand die niedrigsten von allen Systembereichen, über alle "
                         "Zeitscheiben und beide Fälle",
            "hoch_bewertet": [
                _hoch("mitte", "pessimistisch", anzahl=1, seite=150,
                      wortlaut="Nur eine Klimawirkung scheint zur Mitte des Jahrhunderts bei "
                               "starkem Klimawandel mit einem hohen Risiko behaftet zu sein"),
                _hoch("ende", "pessimistisch", anzahl=2, seite=150,
                      wortlaut="und nur zwei zum Ende des Jahrhunderts"),
            ],
            "seiten": [150],
        },
        "gewissheit": {
            "risiko_ohne_anpassung": "relativ gering",
            "anpassungskapazitaet": None,
            "seiten": [150],
        },
        "handlungserfordernisse": {"sehr_dringend": 0, "dringend": 2, "seiten": [150]},
        "klimatische_einfluesse": {
            "einfluesse": ["gradueller Temperaturanstieg",
                           "Klimaextreme (zum Beispiel Hitze, Starkregen)"],
            "entlastend": ["geringeres Vorkommen von Frost", "verringerter Schneefall",
                           "geringere Schnee- und Eislasten",
                           "Anstieg der Durchschnittstemperaturen (partiell)"],
            "seiten": [150],
        },
    },
    _MEN: {
        "anzahl_klimawirkungen": 9,
        "risiko_ohne_anpassung": {
            "vergleich": "für die Gegenwart die höchsten Risiken von allen Systembereichen; zur "
                         "Mitte etwas unter dem Durchschnitt, am Ende auf gleicher Höhe wie bei "
                         "den natürlichen Systemen und Ressourcen, also relativ hoch",
            "hoch_bewertet": [
                _hoch("gegenwart", None, anzahl=1, seite=151,
                      wortlaut="Die Klimawirkung „Hitzebelastung“ ist die einzige aller "
                               "betrachteten Klimawirkungen, die schon in der Gegenwart mit "
                               "hoch bewertet wurde"),
                _hoch("mitte", "pessimistisch", seite=151,
                      wortlaut="Zur Mitte des Jahrhunderts können im Falle eines starken "
                               "Klimawandels ein Drittel der Klimawirkungen in dem Systembereich "
                               "mit hohem Klimarisiko behaftet sein"),
                _hoch("ende", "pessimistisch", seite=151,
                      wortlaut="Gegen Ende des Jahrhunderts kann die Zahl aber stark ansteigen "
                               "auf zwei Drittel"),
            ],
            "seiten": [151],
        },
        "gewissheit": {
            "risiko_ohne_anpassung": "für die Gegenwart und zur Mitte des Jahrhunderts recht "
                                     "hoch, am Ende im Durchschnitt aller Systembereiche",
            "anpassungskapazitaet": None,
            "seiten": [151],
        },
        "handlungserfordernisse": {"sehr_dringend": 3, "dringend": 3, "seiten": [151]},
        "klimatische_einfluesse": {
            "einfluesse": ["Hitze (mit Abstand wichtigster Einfluss)",
                           "Sturzfluten durch Starkregen", "Stürme", "UV-Strahlung",
                           "gradueller Temperaturanstieg (meist über natürliche Systeme)"],
            "entlastend": [],
            "seiten": [151],
        },
    },
}
