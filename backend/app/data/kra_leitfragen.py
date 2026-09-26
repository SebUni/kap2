"""Leitfragen der UBA-Broschüre und die Stelle im Produkt, die sie beantwortet (Checkliste Zeile 19, A1).

UBA-Broschüre „Klimarisikoanalysen auf kommunaler Ebene“, Abschnitt 2.2.6, S. 29: Die Interpretation
soll „Antworten auf die zu Beginn formulierten Leitfragen … liefern“. Die Leitfragen formuliert die
Broschüre in Abschnitt 2.1.1 „Ziele und Ergebnisse definieren“ (S. 11, zwei Beispiele) und in
Abschnitt 2.2.2 „Wirkungsketten erstellen“ (S. 25, drei Beispiele „für jedes Handlungsfeld“).
Seitenzahlen sind die gedruckten Seiten; in dieser Broschüre stimmen sie mit den PDF-Seiten überein.

``beantwortet_durch`` zeigt im Format ``app.modul:attribut`` auf die Stelle im Code, die die Frage
für die Kommune beantwortet, oder lautet genau „nicht beantwortet“. ``begruendung`` sagt in einem
Satz, warum. Das Modul ändert keine Rechnung (T-1139-cto, Vorhaben T-1010-ceo).

Gelesen: S. 5 (Inhaltsverzeichnis), S. 10–12 (Abschnitt 2.1.1 vollständig mit Fußnoten 5 und 6
und Abbildung 2, Beginn 2.1.2), S. 24–25 (Abschnitt 2.2.2 vollständig, Beginn 2.2.3), S. 29–30
(Abschnitt 2.2.6 vollständig, Beginn 2.3); ergänzend eine Stichwortsuche nach „Leitfrage“ und „?“
über S. 1–40. Die Fußnoten 5 und 6 verweisen auf Kapitel 5 der ISO 14091, die nicht vorliegt
(T-0531-ceo); Abbildung 2 enthält keine Leitfrage.
"""

from __future__ import annotations

QUELLE: dict = {
    "titel": "Klimarisikoanalysen auf kommunaler Ebene – Handlungsempfehlungen zur "
             "Umsetzung der ISO 14091 (Umweltbundesamt, 2022)",
    "url": "https://www.umweltbundesamt.de/publikationen/klimarisikoanalysen-auf-kommunaler-ebene",
    "pdf": "https://www.uba.de/system/files/medien/479/publikationen/"
           "2022_uba-fachbroschuere_kra_auf_kommunaler_ebene.pdf",
    "abgerufen": "2026-09-26",
}

NICHT_BEANTWORTET = "nicht beantwortet"

LEITFRAGEN: list[dict] = [
    {
        "nr": 1,
        "wortlaut": "Wie wirkt sich der Klimawandel zukünftig auf meine Kommune aus?",
        "seite": 11,
        "beantwortet_durch": "app.services.cost_projection_service:project_costs",
        "begruendung": "Die Kosten-Projektion schreibt die erwarteten Jahresschäden der Kommune mit "
                       "dem regionalisierten DWD-Klimasignal je Szenario bis 2065 fort, je "
                       "Klimawirkungsgruppe und mit und ohne Maßnahmen.",
    },
    {
        "nr": 2,
        "wortlaut": "In welchen Bereichen ist dringendes Handeln erforderlich?",
        "seite": 11,
        "beantwortet_durch": NICHT_BEANTWORTET,
        "begruendung": "Das Produkt reiht die Bereiche der Kommune nach Risikohöhe und "
                       "Schadenskosten (app.services.systembereiche:systembereich_auswertung), "
                       "schätzt aber keine Dringlichkeit für die Kommune ein, die die Broschüre "
                       "auf S. 30 zusätzlich zur Risikohöhe verlangt; die Dringlichkeit aus "
                       "app.data.kwra_kap7_risiko gilt für Deutschland, nicht für die Kommune.",
    },
    {
        "nr": 3,
        "wortlaut": "Wie haben sich klimatische Veränderungen ausgewirkt?",
        "seite": 25,
        "beantwortet_durch": NICHT_BEANTWORTET,
        "begruendung": "Das Produkt führt vergangene Starkregenereignisse (app.data.catrare), aber "
                       "keine Folgen vergangener Veränderungen; die Größe „Vergangene "
                       "Schadensereignisse durch Wetterextreme“ der Bestandsaufnahme trägt einen "
                       "Lückensatz statt eines Werts.",
    },
    {
        "nr": 4,
        "wortlaut": "Welche Auswirkungen (primär und sekundär) gibt es?",
        "seite": 25,
        "beantwortet_durch": "app.services.handlungsfeld_abhaengigkeiten:abhaengigkeiten_der_kommune",
        "begruendung": "Die Funktion nennt je gerechneter Klimawirkung der Kommune (primär) die in "
                       "der KWRA 2021 benannten Beziehungen zu weiteren Klimawirkungen und "
                       "Handlungsfeldern (sekundär), ohne deren Stärke zu beziffern.",
    },
    {
        "nr": 5,
        "wortlaut": "Wer oder was ist besonders betroffen?",
        "seite": 25,
        "beantwortet_durch": "app.services.bestandsaufnahme_service:bestandsaufnahme_fuer_kommune",
        "begruendung": "Die Bestandsaufnahme weist für die Kommune vulnerable Personengruppen "
                       "(Anteile unter 18 und ab 65 Jahren) und klimasensible Strukturen "
                       "(KRITIS-Sektoren) aus, wie die Broschüre sie auf S. 12 nennt; "
                       "Krankenhäuser und Pflegeeinrichtungen bleiben ohne Wert, solange die "
                       "gespeicherten Zellen die Zählung nicht tragen.",
    },
]
