"""Gender- und Diversitätsaspekte je Klimawirkung (Konformitäts-Checkliste Zeile 19, A7).

UBA-Broschüre „Klimarisikoanalysen auf kommunaler Ebene“, Abschnitt 2.2.6, S. 30:
„Zudem ist empfehlenswert, Gender- und Diversitätsaspekte zu berücksichtigen.“

Das Modul beschreibt den Stand des Codes, es ändert keine Rechnung (T-1135-cto):

- ``beruecksichtigt``: Merkmale von Personengruppen, die heute in die Rechnung der
  Klimawirkung eingehen. ``fundstelle`` zeigt im Format ``app.modul:attribut`` auf die
  Stelle im Code, nicht auf den Methodik-Bericht (die Berichte zu M0 werden nach A-0048
  neu gefasst).
- ``nicht_beruecksichtigt``: nur Aspekte, die S. 30 der Broschüre oder eine dort
  verwiesene Quelle nennt. Der Satz auf S. 30 trägt keine Fußnote und nennt keine
  einzelnen Merkmale; die einzige Fußnote der Seite (35, „Kapitel 7 der ISO 14091“)
  gehört zu Abschnitt 2.3 (Kommunikation). Genannt sind damit nur „Gender“ und
  „Diversitätsaspekte“ allgemein. Das Wort „Gender“ kommt in der Broschüre nur auf S. 30 vor.

Gelesen: S. 29–31 im Text (Abschnitt 2.2.6 vollständig, Beginn 2.3), ergänzend eine
Stichwortsuche über S. 1–40. PDF:
https://www.uba.de/system/files/medien/479/publikationen/2022_uba-fachbroschuere_kra_auf_kommunaler_ebene.pdf

Nachführung: Wird eine Methodik von M0 neu ins Produkt gebracht (``cto-integration``),
zieht die Integration diese Liste mit nach (Vorgabe in T-1010-ceo).
"""

from __future__ import annotations

QUELLE: dict = {
    "titel": "Klimarisikoanalysen auf kommunaler Ebene – Handlungsempfehlungen zur "
             "Umsetzung der ISO 14091 (Umweltbundesamt, 2022)",
    "url": "https://www.umweltbundesamt.de/publikationen/klimarisikoanalysen-auf-kommunaler-ebene",
    "abgerufen": "2026-09-25",
    "seite": 30,
}

_BROSCHUERE = "UBA, Klimarisikoanalysen auf kommunaler Ebene (2022), Abschnitt 2.2.6"

_DIVERSITAET_ALLGEMEIN = {
    "aspekt": "Diversitätsaspekte über Alter und Lebenslage hinaus: S. 30 nennt keine "
              "einzelnen Merkmale, im Code geht kein weiteres ein.",
    "quelle": _BROSCHUERE,
    "seite": 30,
}

_H = "app.services.engine.impact.health"

DIVERSITAET_JE_KLIMAWIRKUNG: dict[str, dict] = {
    # #95 Hitzebelastung — Mortalität
    "EXPECTED_ANNUAL_MORTALITY": {
        "beruecksichtigt": [
            {"aspekt": "Alter",
             "wie": "Die Rechnung läuft in vier Altersbändern (unter 65, 65–74, 75–84, "
                    "85 und älter) mit je eigener Steigung der Hitzekurve und eigener "
                    "Grundsterblichkeit, angewandt auf die Bevölkerung des Bandes in der "
                    "Zelle (Zensus 2022).",
             "fundstelle": f"{_H}:AGE_BETA_FACTOR"},
            {"aspekt": "Geschlecht",
             "wie": "Geschlecht geht nur in die verlorenen Lebensjahre je Sterbefall "
                    "ein; Frauen und Männer sind bis 84 Jahre mit dem Bevölkerungsanteil, "
                    "ab 85 Jahren mit den Sterbefällen 2023 gemittelt.",
             "fundstelle": f"{_H}:AGE_LIFE_YEARS"},
            {"aspekt": "Leben im Pflegeheim (85 und älter)",
             "wie": "Der Anteil der Heimbewohner ab 85 Jahren je Zelle (OSM-"
                    "Pflegeeinrichtungen, auf das Bundesmittel 14,9 % bezogen) hebt oder "
                    "senkt das Sterberisiko im Band 85 und älter.",
             "fundstelle": "app.services.engine.inputs:apply_care_home_share"},
            {"aspekt": "Alleinleben (65 und älter)",
             "wie": "Der Alleinleben-Faktor steht in der Formel, rechnet aber in jeder "
                    "Zelle mit dem Bundesmittel 34,6 % und wirkt deshalb örtlich nicht, "
                    "weil es keine offene Zellquelle gibt.",
             "fundstelle": f"{_H}:_v_vers"},
        ],
        "nicht_beruecksichtigt": [
            {"aspekt": "Gender: Der Geschlechteranteil der Kommune und ein nach "
                       "Geschlecht unterschiedliches Hitzesterberisiko gehen nicht ein.",
             "quelle": _BROSCHUERE, "seite": 30},
            _DIVERSITAET_ALLGEMEIN,
        ],
    },
    # #95 Hitzebelastung — Erkrankungen
    "EXPECTED_ANNUAL_MORBIDITY": {
        "beruecksichtigt": [
            {"aspekt": "Alter",
             "wie": "Die Krankenhauseinweisungen werden je Altersband (unter 65, 65–74, "
                    "75–84, 85 und älter) mit eigener Grundrate aus der Bevölkerung der "
                    "Zelle gerechnet.",
             "fundstelle": f"{_H}:AGE_MORBIDITY_R0"},
        ],
        "nicht_beruecksichtigt": [
            {"aspekt": "Gender: Die Einweisungsraten gelten für beide Geschlechter "
                       "zusammen; Geschlecht geht nicht ein.",
             "quelle": _BROSCHUERE, "seite": 30},
            _DIVERSITAET_ALLGEMEIN,
        ],
    },
    # #96 Aeroallergene
    "EXPECTED_ANNUAL_ALLERGY_DAYS": {
        "beruecksichtigt": [
            {"aspekt": "Alter",
             "wie": "Die Zahl der Betroffenen ergibt sich aus fünf Altersbändern der "
                    "Zelle, je mit eigener Häufigkeit des Heuschnupfens (DEGS1, KiGGS).",
             "fundstelle": f"{_H}:POLLEN_PREVALENCE"},
        ],
        "nicht_beruecksichtigt": [
            {"aspekt": "Gender: Die Häufigkeit des Heuschnupfens gilt je Altersband für "
                       "beide Geschlechter zusammen; Geschlecht geht nicht ein.",
             "quelle": _BROSCHUERE, "seite": 30},
            _DIVERSITAET_ALLGEMEIN,
        ],
    },
    # #98 UV-Schädigungen
    "EXPECTED_ANNUAL_UV_YLL": {
        "beruecksichtigt": [
            {"aspekt": "Alter",
             "wie": "Die Hautkrebsfälle werden je Altersband der Zelle mit eigener "
                    "Neuerkrankungsrate für Melanom und hellen Hautkrebs gerechnet.",
             "fundstelle": f"{_H}:UV_INCIDENCE_C44"},
            {"aspekt": "Geschlecht (Neuerkrankungen)",
             "wie": "Die Neuerkrankungsraten je Altersband sind aus den Raten für Frauen "
                    "und Männer mit dem bundesweiten Bevölkerungsanteil zusammengesetzt.",
             "fundstelle": f"{_H}:UV_INCIDENCE_MM"},
            {"aspekt": "Geschlecht (verlorene Lebensjahre)",
             "wie": "Die Restlebenserwartung je Sterbefall an Melanom und hellem "
                    "Hautkrebs (l_rest_mm, l_rest_c44) ist über Frauen und Männer mit den "
                    "Sterbefällen 2021–2023 gemittelt.",
             "fundstelle": "app.services.engine.impact.params:IMPACT_PARAM_SPECS"},
        ],
        "nicht_beruecksichtigt": [
            {"aspekt": "Gender: Der Geschlechteranteil der Kommune geht nicht ein; "
                       "die Rechnung nutzt nur das bundesweite Verhältnis.",
             "quelle": _BROSCHUERE, "seite": 30},
            _DIVERSITAET_ALLGEMEIN,
        ],
    },
}
