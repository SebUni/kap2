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
- ``ebenen``: Verwaltungsebenen, die an der Umsetzung beteiligt sind, aus ``gemeinde`` (die Kommune selbst, Stadt
  oder Gemeinde), ``kreis`` (Landkreis bzw. bei kreisfreien Städten die Stadt in ihrer Kreisfunktion) und ``land``
  (T-1193-ceo). Jede genannte Ebene ist in ``partner`` oder ``beleg`` begründet. Stellen des Bundes (etwa der
  Deutsche Wetterdienst) und Stellen außerhalb der Verwaltung zählen zu keiner der drei Ebenen;
- ``beleg``: entweder ``quelle`` mit ``seite`` oder ``abschaetzung`` mit ``herleitung`` (Vorgabe P1); weitere
  Quellen stehen in ``weitere_quellen`` (je ``quelle``, ``seite``, ``fundstelle``).

Die zitierten Quellen liegen mit Textabbild (``.txt``, Seitenmarken ``=== Seite n ===``) unter
``docs/quellen/hitzeaktionsplaene/``.

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
    "hap_handlungsempfehlungen_bf.pdf (PDF-Seite gleich gedruckter Seite; abgelegt unter "
    "docs/quellen/hitzeaktionsplaene/hap_handlungsempfehlungen_bf.pdf)"
)

_WD_OEGD = (
    "Deutscher Bundestag, Wissenschaftliche Dienste: Die Gesundheitsdienstgesetze der Länder, Ausarbeitung "
    "WD 9 – 3000 – 027/14, Abschluss der Arbeit 30.04.2014, "
    "https://www.bundestag.de/resource/blob/410444/a2f24acb7bdabf15da541c95d2946167/wd-9-027-14-pdf-data.pdf "
    "(PDF-Seite gleich gedruckter Seite; abgelegt unter "
    "docs/quellen/hitzeaktionsplaene/bundestag_wd9_3000_027_14_gesundheitsdienstgesetze.pdf)"
)

_PAKT_OEGD = (
    "Bund und Länder: Pakt für den Öffentlichen Gesundheitsdienst, beschlossen am 29.09.2020, "
    "Bundesministerium für Gesundheit, "
    "https://www.bundesgesundheitsministerium.de/fileadmin/Dateien/3_Downloads/O/OEGD/Pakt_fuer_den_OEGD.pdf "
    "(PDF-Seite gleich gedruckter Seite; abgelegt unter docs/quellen/hitzeaktionsplaene/bmg_pakt_oegd_2020.pdf)"
)

EBENEN_WERTE = ("gemeinde", "kreis", "land")

_GESUNDHEITSAMT = (
    "Gesundheitsamt (untere Gesundheitsbehörde): bei kreisangehörigen Gemeinden beim Landkreis, also außerhalb der "
    "eigenen Verwaltung; bei kreisfreien Städten bei der Stadt selbst"
)

_BELEG_GESUNDHEITSAMT = [
    {
        "quelle": _WD_OEGD,
        "seite": "7",
        "fundstelle": (
            "S. 7: „Viele Landesgesetze benennen die Träger des ÖGD (außerhalb der Stadtstaaten sind dies in der "
            "Regel das Land, die Landkreise sowie die kreisfreien Städte) und enthalten weitergehende "
            "organisatorische Vorgaben. So wird in vielen Gesetzen die Einrichtung eines „Gesundheitsamtes“ als "
            "untere Gesundheitsbehörde ausdrücklich vorgeschrieben.“"
        ),
    },
    {
        "quelle": _PAKT_OEGD,
        "seite": "1",
        "fundstelle": (
            "S. 1: „Die Beteiligten sind sich einig, dass für die Umsetzung des Paktes für den ÖGD die Mitwirkung "
            "der kreisfreien Städte und der Landkreise wesentlich ist. Dies gilt insbesondere für den Personalaufbau "
            "in den unteren Gesundheitsbehörden, …“"
        ),
    },
]

MASSNAHMEN_UMSETZUNG: dict[str, dict] = {
    "HEAT_ACTION_PLANS": {
        "umsetzung": "mit_partnern",
        "partner": [
            "Land: zentrale Koordinierungsstelle, etwa in einer Gesundheitsbehörde des Landes",
            _GESUNDHEITSAMT + "; bezieht den Hitzewarn-Newsletter des DWD",
            "Deutscher Wetterdienst (Hitzewarnsystem, Warnungen je Landkreis)",
            "Einrichtungen vor Ort: Pflegeeinrichtungen, Krankenhäuser, Rettungsdienste, Ärzteschaft",
        ],
        "ebenen": ["gemeinde", "kreis", "land"],
        "beleg": {
            "quelle": _BMU_HAP,
            "seite": "6, 11, 14, 15",
            "ebenen_begruendung": (
                "gemeinde: Umsetzung „auf kommunaler Ebene“ (S. 6), Kommunen als dezentrale Koordinierungsstellen "
                "(S. 11). kreis: Gesundheitsamt als untere Gesundheitsbehörde der Landkreise und kreisfreien Städte "
                "(S. 15 und weitere_quellen), Hitzewarnungen „landkreisbezogen“ (S. 14). land: zentrale "
                "Koordinierungsstelle „auf Landesebene“ und Gesundheitsministerien der Länder (S. 11, 15)."
            ),
            "weitere_quellen": _BELEG_GESUNDHEITSAMT,
            "fundstelle": (
                "S. 6: Die Empfehlungen „richten sich in erster Linie an die Länder. Die Umsetzung erfolgt im "
                "Wesentlichen in den einzelnen Ländern auf kommunaler Ebene.“ S. 11, Kernelement I: zentrale "
                "Koordinierungsstelle „auf Landesebene bspw. in einer Gesundheitsbehörde“; die Kommunen sind "
                "„dezentrale Koordinierungsstellen“ und binden Institutionen vor Ort ein (Feuerwehren, Not- und "
                "Rettungsdienste, Krankenhäuser, Ärzteschaft, Pflegeeinrichtungen u. a.). S. 14, Kernelement II: "
                "„Das Hitzewarnsystem wird vom Deutschen Wetterdienst (DWD) betrieben“; die Warnungen werden "
                "„landkreisbezogen herausgegeben“. S. 15: Den Hitzewarn-Newsletter des DWD sollen mindestens "
                "abonnieren: „Gesundheitsministerien der Länder“, „Gesundheitsämter der Kommunen“ sowie Verbände und "
                "Einrichtungen der gesundheitlichen und sozialen Versorgung."
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
            _GESUNDHEITSAMT + "; Beispiel: Hitzetelefon des Gesundheitsamtes der Region Kassel",
        ],
        "ebenen": ["gemeinde", "kreis"],
        "beleg": {
            "quelle": _BMU_HAP,
            "seite": "11, 15, 17, 20–21",
            "ebenen_begruendung": (
                "gemeinde: Die Mitwirkenden auf kommunaler Ebene legen die Zuständigkeiten vor Ort fest und planen "
                "die Maßnahmen zu den Kernelementen II bis VIII, darunter V „Besondere Beachtung von Risikogruppen“ "
                "(S. 11). kreis: Gesundheitsamt als untere Gesundheitsbehörde der Landkreise und kreisfreien Städte "
                "(weitere_quellen), mit eigenem Angebot für Risikogruppen (Hitzetelefon, S. 17)."
            ),
            "weitere_quellen": _BELEG_GESUNDHEITSAMT,
            "fundstelle": (
                "S. 11: Institutionen, die vor Ort Maßnahmen umsetzen können, u. a. Ärzteschaft, Apothekerschaft, "
                "ambulante und stationäre Pflegeeinrichtungen, Hilfsorganisationen, Behindertenhilfen und "
                "Heimaufsichten. S. 15: Den Hitzewarn-Newsletter sollen u. a. Pflegedienste und -einrichtungen "
                "sowie „Soziale Netzwerke und Nachbarschaftshilfen“ beziehen. S. 17: telefonische Beratung nach "
                "dem Hitzetelefon „Sonnenschirm“ des Gesundheitsamtes der Region Kassel; Weitergabe durch Ärztinnen "
                "und Ärzte und Apotheken. S. 20: Obdachlose „bedürfen in Extremsituationen oftmals "
                "einer individuellen Betreuung durch die Sozialdienste“. S. 21, Kernelement VI: Maßnahmenpläne für Alten- und Pflegeheime, Beispiel der "
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
        "ebenen": ["gemeinde"],
        "beleg": {
            "ebenen_begruendung": (
                "gemeinde: Die Kommune bindet ihre Messstationen an (siehe herleitung). Beide Partner gehören zu "
                "keiner der drei Ebenen: Der DWD ist eine Stelle des Bundes, der PID eine Stiftung. Kreis und Land "
                "stehen deshalb nicht in ebenen; auch das ist Teil der Abschätzung von KAP3."
            ),
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
