"""Diskontierung der Kostenprojektion (UBA Methodenkonvention 4.0, Kap. 2.2.3, S. 14–15).

Die Konvention verlangt eine Diskontrate aus zwei Teilen (S. 14): (1) die Zeitpräferenz und
(2) die relative Veränderung zwischen heutigen und künftigen Preisen. Die Reine
Zeitpräferenzrate (RZPR) ist ein Bestandteil der Diskontrate, nicht die Diskontrate selbst
(S. 10, S. 15). Das Produkt setzt deshalb an:

    Diskontrate = RZPR + Komponente der relativen Preise

Die RZPR wird mit 0 % und 1 % berichtet (S. 15). Die Komponente der relativen Preise ist eine
eigene, gekennzeichnete Größe. Bis die Methodik einen Wert festlegt, trägt sie den Wert
0 Prozentpunkte als Abschätzung von KAP3 (Vorgaben P1 und P2), mit Begründung und
Modellgrenzen.

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
RELATIVE_PRICE_COMPONENT: float = 0.0

RELATIVE_PRICE_COMPONENT_SPEC: dict = {
    "label": "Komponente der relativen Preise (Diskontrate)",
    "unit": "Prozentpunkte (als Dezimalzahl, 0,01 = 1 Pp.)",
    "source": "Abschätzung von KAP3 (UBA Methodenkonvention 4.0, Kap. 2.2.3, S. 14–15)",
    "source_detail": (
        "Die UBA Methodenkonvention 4.0 verlangt eine Diskontrate aus zwei Teilen: der "
        "Zeitpräferenz und der relativen Veränderung zwischen heutigen und künftigen Preisen "
        "(S. 14). Nach Ramsey kommt zur Reinen Zeitpräferenzrate das erwartete Konsumwachstum "
        "hinzu, gewichtet nach seiner Wirkung auf den Grenznutzen (S. 14–15). Eine Zahl für "
        "diese zweite Komponente gibt die Konvention nicht vor; es sei „nicht möglich, die "
        "genaue Diskontrate anzugeben“, weil das Konsumwachstum im GIVE-Modell eine abhängige "
        "Größe ist (S. 15). KAP3 führt sie deshalb als eigene Größe und "
        "setzt sie vorläufig mit 0 Prozentpunkten an, bis die Methodik einen Wert festlegt. "
        "Die Diskontrate ist damit RZPR + Komponente, heute also 0 % und 1 %."
    ),
    "evidence_class": "abgeschaetzt",
    "evidence_derivation": {
        "wert": (
            "0 Prozentpunkte (Punktwert, vorläufig). Abschätzung von KAP3: Die Konvention "
            "nennt für die Komponente keine Zahl (S. 15), und ihre Richtung hängt vom Gut ab. "
            "Für Konsumgüter mit sinkendem relativem Preis hebt sie die Diskontrate, für knapper "
            "werdende Umweltgüter senkt sie sie (S. 15). Für die bewerteten Gesundheitsschäden "
            "ist nicht belegt, welcher Effekt überwiegt. Der Wert 0 unterstellt, dass sich beide "
            "Effekte aufheben. Er ist der Wert, der im Produkt schon bisher wirkte, und gilt, bis "
            "die Methodik die Komponente festlegt."
        ),
        "band": (
            "Keine Bandbreite in Zahlen. Die Konvention legt nur die Richtung je Gut fest "
            "(S. 15): positiv bei Gütern, deren relativer Preis sinkt (Konsumgüter), negativ bei "
            "Gütern, deren relativer Preis steigt (knapper werdende Umweltgüter, bei weiterem "
            "Rückgang „eine noch niedrigere Diskontrate“). Welches Vorzeichen für "
            "Gesundheitsschäden gilt, ist offen."
        ),
        "sensitivitaet": (
            "Die Komponente wird zu jeder RZPR addiert. Ein positiver Wert erhöht die "
            "Diskontrate und senkt die Barwerte, umso stärker, je später ein Schaden eintritt; "
            "schon der Barwert zur RZPR 0 % liegt dann unter der unabgezinsten Summe. Ein "
            "negativer Wert senkt die Diskontrate und hebt die Barwerte; der Barwert zur RZPR "
            "0 % liegt dann über der unabgezinsten Summe. Bei 0 ist der Barwert zur RZPR 0 % "
            "gleich der unabgezinsten Summe."
        ),
    },
}

# Modellgrenzen der Diskontierung, je Satz mit Seite der UBA Methodenkonvention 4.0.
MODELLGRENZEN: list[str] = [
    "Die Richtung der Komponente der relativen Preise für die bewerteten Gesundheitsschäden ist "
    "offen: Sie hebt die Diskontrate für Güter mit sinkendem relativem Preis und senkt sie für "
    "knapper werdende Umweltgüter (UBA Methodenkonvention 4.0, S. 15).",
    "Risikoaversion geht nicht ein, obwohl die Diskontrate für politische Entscheidungen die "
    "höhere gesellschaftliche Risikoaversion berücksichtigen soll (UBA Methodenkonvention 4.0, "
    "S. 15).",
    "Der unvollständige Zusammenhang zwischen Finanzmärkten und dem Grenznutzen der Betroffenen "
    "ist nicht berücksichtigt, etwa wenn Betroffene keinen Zugang zu Finanzmärkten haben; die "
    "Konvention verlangt, dass die Diskontrate ihn berücksichtigt (UBA Methodenkonvention 4.0, "
    "S. 15).",
    "Die Diskontrate ist über den ganzen Horizont konstant; ein mit dem Konsumwachstum "
    "schwankender Satz, wie ihn das GIVE-Modell über die Monte-Carlo-Läufe ergibt, ist nicht "
    "abgebildet (UBA Methodenkonvention 4.0, S. 15).",
]
