"""Umsetzungsebene je Maßnahme: kann die Kommune sie allein umsetzen oder braucht sie Partner?

Anlass ist Anforderung A9 der Gegenprobe zur Konformitätszeile 19 (``docs/KONFORMITAET_CHECKLISTE.md``,
Abschnitt „Gegenprobe Zeile 19“; Ticket T-1132-cto, Vorhaben T-1010-ceo). Die UBA-Broschüre
„Klimarisikoanalysen auf kommunaler Ebene – Handlungsempfehlungen zur Umsetzung der ISO 14091“ (2022), S. 30,
verlangt zu erörtern, „welche Handlungsoptionen auf kommunaler Ebene bestehen und ggf. welche Optionen der
Zusammenarbeit mit Akteur*innen außerhalb der Kommune bedürfen“, unter Berücksichtigung der Aufteilung der
Verwaltungsverantwortung auf Stadt/Gemeinde, Landkreis und Bundesland.

Je Code aus ``catalog.MEASURES`` steht hier genau ein Eintrag:

- ``umsetzung``: ``kommune_allein`` oder ``mit_partnern``;
- ``partner``: Stellen außerhalb der Kommunalverwaltung, die für die Umsetzung gebraucht werden
  (leer genau dann, wenn die Kommune allein umsetzt);
- ``beleg``: entweder ``quelle`` mit ``seite`` oder ``abschaetzung`` mit ``herleitung`` (Vorgabe P1).

Die Broschüre selbst nennt keine Zuständigkeit je Maßnahme. Wer für die Pflicht zum Klimaanpassungskonzept
zuständig ist, steht je Land in ``kang_zustaendigkeit.py``; das betrifft das Konzept, nicht die einzelne
Maßnahme, und wird hier deshalb nicht übertragen.
"""

from __future__ import annotations

UMSETZUNG_WERTE = ("kommune_allein", "mit_partnern")

_BMU_HAP = (
    "Bund/Länder Ad-hoc AG „Gesundheitliche Anpassung an die Folgen des Klimawandels (GAK)“: "
    "Handlungsempfehlungen für die Erstellung von Hitzeaktionsplänen zum Schutz der menschlichen Gesundheit, "
    "Version 1.0, Stand 24.03.2017, Bundesministerium für Umwelt, Naturschutz, Bau und Reaktorsicherheit, "
    "https://www.bundesumweltministerium.de/fileadmin/Daten_BMU/Download_PDF/Klimaschutz/"
    "hap_handlungsempfehlungen_bf.pdf (PDF-Seite gleich gedruckter Seite)"
)

MASSNAHMEN_UMSETZUNG: dict[str, dict] = {
    "HEAT_ACTION_PLANS": {
        "umsetzung": "mit_partnern",
        "partner": [
            "Land: zentrale Koordinierungsstelle, etwa in einer Gesundheitsbehörde des Landes",
            "Deutscher Wetterdienst (Hitzewarnsystem, Warnungen je Landkreis)",
            "Einrichtungen vor Ort: Pflegeeinrichtungen, Krankenhäuser, Rettungsdienste, Ärzteschaft",
        ],
        "beleg": {
            "quelle": _BMU_HAP,
            "seite": "6, 11, 14",
            "fundstelle": (
                "S. 6: Die Empfehlungen „richten sich in erster Linie an die Länder. Die Umsetzung erfolgt im "
                "Wesentlichen in den einzelnen Ländern auf kommunaler Ebene.“ S. 11, Kernelement I: zentrale "
                "Koordinierungsstelle „auf Landesebene bspw. in einer Gesundheitsbehörde“; die Kommunen sind "
                "„dezentrale Koordinierungsstellen“ und binden Institutionen vor Ort ein (Feuerwehren, Not- und "
                "Rettungsdienste, Krankenhäuser, Ärzteschaft, Pflegeeinrichtungen u. a.). S. 14, Kernelement II: "
                "„Das Hitzewarnsystem wird vom Deutschen Wetterdienst (DWD) betrieben“; die Warnungen werden "
                "„landkreisbezogen herausgegeben“."
            ),
        },
    },
    "VULNERABLE_GROUP_PROGRAMS": {
        "umsetzung": "mit_partnern",
        "partner": [
            "ambulante und stationäre Pflegeeinrichtungen und Pflegedienste",
            "Hilfsorganisationen, Sozialdienste und Nachbarschaftshilfen",
            "Heimaufsicht",
            "Ärzteschaft und Apotheken",
        ],
        "beleg": {
            "quelle": _BMU_HAP,
            "seite": "11, 15, 17, 20–21",
            "fundstelle": (
                "S. 11: Institutionen, die vor Ort Maßnahmen umsetzen können, u. a. Ärzteschaft, Apothekerschaft, "
                "ambulante und stationäre Pflegeeinrichtungen, Hilfsorganisationen, Behindertenhilfen und "
                "Heimaufsichten. S. 15: Den Hitzewarn-Newsletter sollen u. a. Pflegedienste und -einrichtungen "
                "sowie „Soziale Netzwerke und Nachbarschaftshilfen“ beziehen. S. 17: telefonische Beratung nach "
                "dem Hitzetelefon „Sonnenschirm“ des Gesundheitsamtes der Region Kassel; Weitergabe durch Ärztinnen "
                "und Ärzte und Apotheken. S. 20: Obdachlose brauchen „eine individuelle Betreuung durch die "
                "Sozialdienste“. S. 21, Kernelement VI: Maßnahmenpläne für Alten- und Pflegeheime, Beispiel der "
                "hessischen Heimaufsicht."
            ),
        },
    },
    "POLLEN_EARLY_WARNING": {
        "umsetzung": "mit_partnern",
        "partner": [
            "Deutscher Wetterdienst (Pollenflug-Gefahrenindex)",
            "Stiftung Deutscher Polleninformationsdienst (PID, Pollenmessnetz)",
        ],
        "beleg": {
            "abschaetzung": True,
            "herleitung": (
                "Abschätzung von KAP3: Keine der ausgewerteten Quellen (UBA-Broschüre 2022, S. 29–30; "
                "Angaben source, sources und source_details in catalog.py; kang_zustaendigkeit.py) nennt, wer "
                "eine kommunale Pollen-Frühwarnung trägt. Die Maßnahme ist im Katalog und in Bericht #96 (§5.1, "
                "Registerzeile 96-S158-01) als Anbindung kommunaler Messstationen an das Frühwarnsystem von DWD und "
                "PID beschrieben; der Gefahrenindex, über den gewarnt wird, liegt also nicht bei der Kommune. "
                "Deshalb gilt die Maßnahme als nur mit diesen beiden Partnern umsetzbar. Die Einstufung ersetzt "
                "eine Quelle, die die Zuständigkeit ausdrücklich nennt, sobald eine gefunden ist."
            ),
        },
    },
}


def umsetzung_fuer(code: str) -> dict | None:
    """Eintrag für einen Maßnahmen-Code oder ``None``, wenn der Code fehlt."""
    return MASSNAHMEN_UMSETZUNG.get(code)
