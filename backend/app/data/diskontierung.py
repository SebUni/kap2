"""Diskontierung der Kostenprojektion (UBA Methodenkonvention 4.0, Kap. 2.2.3, S. 14–15).

Die Konvention verlangt eine Diskontrate aus zwei Teilen (S. 14): (1) die Zeitpräferenz und
(2) die relative Veränderung zwischen heutigen und künftigen Preisen. Die Reine
Zeitpräferenzrate (RZPR) ist ein Bestandteil der Diskontrate, nicht die Diskontrate selbst
(S. 10, S. 15). Das Produkt setzt deshalb an:

    Diskontrate = RZPR + Komponente der relativen Preise

Die RZPR wird mit 0 % und 1 % berichtet (S. 15). Die Komponente der relativen Preise ist eine
eigene, gekennzeichnete Größe. Sie beträgt 0,1 Prozentpunkte (Band 0–0,7 Pp.) als Abschätzung
von KAP3 (Vorgaben P1 und P2), gerechnet aus drei Quellenwerten, mit Begründung und
Modellgrenzen. Quelle: docs/methodik/querschnitt_diskontrate.md, Regel D. Sie gilt für die
Gesundheitsschäden von M0 (#95, #96, #98); übrige Schäden und Maßnahmenkosten werden mit der
RZPR allein abgezinst.

Eigenes Datenmodul ohne Importe aus ``app.services``, damit die Parameter-Registry die
Konstanten lesen kann, ohne einen Importzirkel über ``measure_service`` zu erzeugen.
"""

from __future__ import annotations

# Reine Zeitpräferenzrate (RZPR), UBA Methodenkonvention 4.0, Kap. 2.2.3, S. 15: Die Ergebnisse
# werden für eine RZPR von 0 % und 1 % dargestellt. Mindestens zwei Werte berichten, um die
# Sensitivität gegenüber der Zeitpräferenz zu zeigen.
PURE_TIME_PREFERENCE_RATES: tuple[float, ...] = (0.0, 0.01)

# Komponente der relativen Preise (Aspekt 2 der Diskontrate, S. 14), als Dezimalzahl
# (0,01 = 1 Prozentpunkt). Abschätzung von KAP3, siehe RELATIVE_PRICE_COMPONENT_SPEC.
RELATIVE_PRICE_COMPONENT: float = 0.001

# Schadensarten, für die die Komponente gilt: die Gesundheitsschäden von M0, das sind die
# KWRA-Klimawirkungen #95 Hitzebelastung, #96 Aeroallergene und #98 UV-Schädigungen. Quelle:
# docs/methodik/querschnitt_diskontrate.md, Abschnitt „Geltung für die Schadensarten von M0“
# (Befund C5). Für andere Schadensarten und für Maßnahmenkosten setzt die Quelle keinen Wert
# (Anweisung A-0048); sie werden nur mit der RZPR abgezinst. Maßgeblich ist das Feld ``kwra_id``
# des Katalogeintrags eines Risikos.
RELATIVE_PRICE_COMPONENT_KWRA_IDS: tuple[int, ...] = (95, 96, 98)

RELATIVE_PRICE_COMPONENT_SPEC: dict = {
    "label": "Komponente der relativen Preise (Diskontrate)",
    "unit": "Prozentpunkte (als Dezimalzahl, 0,01 = 1 Pp.)",
    "source": (
        "Abschätzung von KAP3 aus drei Quellenwerten (UBA Methodenkonvention 4.0, Kap. 2.2.3, "
        "S. 14–16 und S. 22; Sachverständigenrat; 2024 Ageing Report, Country fiche Germany; "
        "World Bank, World Development Indicators; Green Book; OECD)"
    ),
    "source_detail": (
        "Die UBA Methodenkonvention 4.0 verlangt eine Diskontrate aus zwei Teilen: der "
        "Zeitpräferenz und der relativen Veränderung zwischen heutigen und künftigen Preisen "
        "(S. 14). Nach Ramsey kommt zur Reinen Zeitpräferenzrate das erwartete Konsumwachstum "
        "hinzu, gewichtet nach seiner Wirkung auf den Grenznutzen (S. 14–15). Eine Zahl für "
        "diese zweite Komponente gibt die Konvention nicht vor; es sei „nicht möglich, die "
        "genaue Diskontrate anzugeben“, weil das Konsumwachstum im GIVE-Modell eine abhängige "
        "Größe ist (S. 15). KAP3 rechnet sie deshalb aus drei Quellenwerten: "
        "Veränderung der relativen Preise = Konsumwachstum je Kopf × (Elastizität des "
        "Grenznutzens − Einkommenselastizität des Schadenswerts). "
        "Wir zinsen künftige Gesundheitsschäden mit 0,1 % und 1,1 % ab: RZPR 0 % bzw. 1 % "
        "plus 0,1 Prozentpunkte für steigende relative Preise. Die Komponente gilt für die "
        "Gesundheitsschäden von M0 (#95, #96, #98); übrige Schäden und Maßnahmenkosten werden "
        "mit der RZPR allein abgezinst."
    ),
    "evidence_class": "abgeschaetzt",
    "evidence_derivation": {
        "wert": (
            "0,1 Prozentpunkte, positives Vorzeichen (Abschätzung von KAP3). Gerechnet aus drei "
            "Quellenwerten: Konsumwachstum je Kopf 0,7 % je Jahr (Band 0,4–1,1 %; Potenzialwachstum "
            "2023–2070 im Mittel 0,7 % je Jahr, Sachverständigenrat, S. 15, bei nahezu gleicher "
            "Bevölkerung 2022–2070, 2024 Ageing Report, Country fiche Germany, Tabelle 2; Untergrenze "
            "0,4 %: Potenzialwachstum der 2020er Jahre, Sachverständigenrat, S. 15; Obergrenze "
            "1,1 %: BIP je Kopf Deutschlands 1991–2024, im Mittel 1,06 % je Jahr, World Bank, "
            "World Development Indicators, NY.GDP.PCAP.KD, Preise von 2015); Elastizität des "
            "Grenznutzens 1,0 (Band 1,0–1,5; Green Book §2.13, Spanne §2.12; Rechenbeispiel der "
            "UBA Methodenkonvention 4.0, S. 16, entspricht 1); Einkommenselastizität des "
            "Schadenswerts 0,85 (Band 0,85–1,0; UBA Methodenkonvention 4.0, S. 22; Obergrenze nach "
            "OECD Tabelle 0.1, S. 15, und Green Book §2.16). Rechnung: Wohlstandseffekt "
            "0,7 % × 1,0 = +0,7 Pp. hebt die Rate; Preiseffekt 0,7 % × 0,85 = −0,595 Pp. senkt "
            "sie; Summe 0,105 Pp., gerundet 0,1 Pp. (auf eine Stelle, weil das Konsumwachstum "
            "nur eine hat). Die Kostensätze werden real nicht fortgeschrieben (Preisanpassung nur "
            "mit dem Verbraucherpreisindex, S. 9); der steigende Wert der Gesundheit gehört "
            "deshalb in die Diskontrate."
        ),
        "band": (
            "0–0,7 Pp. Untergrenze 0, wenn beide Elastizitäten 1,0 sind und sich die Effekte "
            "aufheben (Green Book §2.16, OECD). Obergrenze 1,1 % × (1,5 − 0,85) = 0,715 Pp., "
            "gerundet 0,7 Pp., aus den jeweils ungünstigsten Werten der drei Bestandteile. "
            "Das Vorzeichen für Gesundheitsschäden ist positiv."
        ),
        "sensitivitaet": (
            "Wirkung auf den Barwert bei gleichbleibendem Jahresbetrag über 2025–2065 und zur "
            "RZPR 0 %: Die Summe der Abzinsfaktoren ist 41,0 bei 0 Pp., 40,19 beim Wert 0,1 Pp. "
            "und 35,78 bei 0,7 Pp. Gegenüber dem Wert liegt der Barwert an der Untergrenze um "
            "2,0 % höher und an der Obergrenze um 11 % niedriger, also +2,0 % bis −11 %. "
            "Jede Abweichung um 0,1 Pp. ändert ihn um rund 2 %. Ein positiver Wert senkt die "
            "Barwerte, umso stärker, je später ein Schaden eintritt; schon der Barwert zur "
            "RZPR 0 % liegt unter der unabgezinsten Summe."
        ),
    },
}

# Modellgrenzen der Diskontierung, je Satz mit Seite der UBA Methodenkonvention 4.0.
MODELLGRENZEN: list[str] = [
    "Die Richtung der Komponente der relativen Preise ist für die bewerteten Gesundheitsschäden "
    "positiv, mit 0,1 Pp. (Band 0–0,7 Pp.): Sie hebt die Diskontrate für Güter mit sinkendem "
    "relativem Preis und senkt sie für knapper werdende Umweltgüter (UBA Methodenkonvention "
    "4.0, S. 15).",
    "Die Anforderung, die gesellschaftliche Risikoaversion zu berücksichtigen, geht über die "
    "RZPR von 0 % ein, die langfristige Ziele wie Generationengerechtigkeit abbildet und immer "
    "neben der RZPR von 1 % ausgewiesen wird; die Risikoaversion bleibt ohne eigene Zahl, weil "
    "die Konvention sie weder beziffert noch einen Rechenweg nennt und der Abschlag nach der "
    "Green Book den Barwert nur um 0,02 % bis 0,17 % höbe (UBA Methodenkonvention 4.0, S. 15).",
    "Der unvollständige Zusammenhang zwischen Finanzmärkten und dem Grenznutzen der Betroffenen "
    "geht über die Bauweise der Rate ein, ohne eigene Zahl: Kein Bestandteil kommt vom "
    "Finanzmarkt, und das Wachstum ist das des Konsums je Kopf, nicht das des Kapitals "
    "(UBA Methodenkonvention 4.0, S. 15).",
    "Die Diskontrate ist über den ganzen Horizont konstant; ein mit dem Konsumwachstum "
    "schwankender Satz, wie ihn das GIVE-Modell über die Monte-Carlo-Läufe ergibt, ist nicht "
    "abgebildet (UBA Methodenkonvention 4.0, S. 15).",
    "Behandlungskosten bekommen denselben Wert wie die immateriellen Schäden, als Abschätzung "
    "von KAP3: Die Konvention nennt die Elastizität 0,85 nur für die Zahlungsbereitschaft "
    "(S. 22) und für Behandlungskosten weder eine Elastizität noch eine Richtung; jede "
    "Abweichung um 0,1 Pp. ändert den Barwert um rund 2 % (UBA Methodenkonvention 4.0, S. 22).",
    "Der Barwert gilt nur über die Jahre 2025–2065, die 41 Jahre der Klimaprojektion; Schäden "
    "nach 2065 gehen nicht ein, der Barwert ist also nicht der aller künftigen Schäden "
    "(UBA Methodenkonvention 4.0, S. 14).",
]
