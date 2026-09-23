"""Anpassungskapazität nach ISO 14091 (optionaler Analyseschritt): Daten und Textbausteine.

Checklistenzeile 18, Ticket T-0760, Vorhaben T-0448. Das Modul rechnet nichts und enthält
keine Zahl außer den Stufennummern 0 bis 3 (Vorgabe P1). Die Kommune oder das Beratungshaus
stuft jede der vier Komponenten selbst ein; die Gesamtstufe folgt der Engpassregel.
"""

from __future__ import annotations

KOMPONENTEN: tuple[dict[str, str], ...] = (
    {
        "code": "organisation",
        "label": "Organisationsbezogene Fähigkeit",
        "beschreibung": (
            "Zuständigkeiten, Personal, Fachwissen und Abstimmungswege, mit denen die "
            "Kommune Anpassung planen und umsetzen kann."
        ),
    },
    {
        "code": "technik",
        "label": "Technisches Vermögen",
        "beschreibung": (
            "Technische Infrastruktur, Daten sowie Warn- und Informationssysteme, die für "
            "Anpassung zur Verfügung stehen."
        ),
    },
    {
        "code": "finanzen",
        "label": "Finanzielle Fähigkeit",
        "beschreibung": (
            "Haushaltsmittel und Zugang zu Fördermitteln, mit denen Anpassungsmaßnahmen "
            "finanziert werden können."
        ),
    },
    {
        "code": "oekosystem",
        "label": "Fähigkeit des Ökosystems",
        "beschreibung": (
            "Natürliche Puffer- und Regulationsleistungen (z. B. Grünflächen, Gewässer, "
            "Böden), die Klimawirkungen abmildern."
        ),
    },
)

QUELLE_KOMPONENTEN = (
    "Umweltbundesamt (2022): Klimarisikoanalysen auf kommunaler Ebene – "
    "Handlungsempfehlungen zur Umsetzung der ISO 14091, Abschnitt 2.2.5, S. 28f.; "
    "ISO 14091:2021, Anhang G und H"
)

REIFEGRADE: tuple[dict[str, object], ...] = (
    {
        "stufe": 0,
        "label": "nicht vorhanden",
        "beschreibung": "Die Fähigkeit fehlt oder wird für Klimaanpassung nicht genutzt.",
    },
    {
        "stufe": 1,
        "label": "im Aufbau",
        "beschreibung": (
            "Erste Ansätze sind vorhanden, aber nicht verbindlich verankert oder für die "
            "bekannten Klimarisiken nicht ausreichend."
        ),
    },
    {
        "stufe": 2,
        "label": "etabliert",
        "beschreibung": (
            "Die Fähigkeit ist verbindlich verankert und reicht für die heute bekannten "
            "Klimarisiken aus."
        ),
    },
    {
        "stufe": 3,
        "label": "vorausschauend",
        "beschreibung": (
            "Die Fähigkeit wird regelmäßig überprüft und an die künftig erwarteten "
            "Klimaänderungen angepasst."
        ),
    },
)

HERLEITUNG_REIFEGRADE = (
    "Abschätzung von KAP3: Die vierstufige Skala ist eine Festlegung von KAP3, angelehnt "
    "an die in der Quelle genannten Reifegrade; sie ordnet nur und ist kein Messwert. Vier "
    "Stufen erlauben einer Kommune, jede Komponente ohne Statistikkenntnisse in einem "
    "Schritt einzuordnen."
)

REGEL_GESAMTSTUFE = (
    "Engpassregel: Die Gesamtstufe ist die niedrigste Stufe der vier Komponenten, weil die "
    "schwächste Fähigkeit begrenzt, wie viel Anpassung tatsächlich umgesetzt werden kann."
)

MINDERUNGSSAETZE: dict[int | None, str] = {
    0: "Mit der vorhandenen Anpassungskapazität lässt sich das Klimarisiko voraussichtlich kaum verringern.",
    1: "Mit der vorhandenen Anpassungskapazität lässt sich das Klimarisiko voraussichtlich nur in geringem Umfang verringern.",
    2: "Mit der vorhandenen Anpassungskapazität lässt sich das Klimarisiko voraussichtlich teilweise verringern.",
    3: "Mit der vorhandenen Anpassungskapazität lässt sich das Klimarisiko voraussichtlich weitgehend verringern.",
    None: "Die Anpassungskapazität ist nicht für alle vier Komponenten bewertet; eine Aussage, wie stark sich das Klimarisiko durch Anpassung verringern lässt, unterbleibt.",
}

OPTIONAL_SATZ = (
    "Die Analyse der Anpassungskapazität ist nach ISO 14091 ein optionaler Analyseschritt; "
    "sie ergänzt die Bewertung des Klimarisikos ohne (weitere) Anpassung und ersetzt sie nicht."
)
