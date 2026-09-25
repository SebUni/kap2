"""KWRA-Schlüsse für die Anpassungsplanung und methodische Grenze des Vergleichs — aus Kap. 7.

Quelle: UBA/BMU „Klimawirkungs- und Risikoanalyse 2021 für Deutschland" (KWRA 2021),
Teilbericht 6 (Integrierte Auswertung), Kapitel 7 „Querbetrachtung der Systembereiche",
Schlussabschnitt S. 153–154 mit Tabelle 28 (S. 153) und Fußnote 30 (S. 153).

Konformitätsliste Zeile 10:

- A10 — ``SCHLUESSE_ANPASSUNGSPLANUNG``: die Schlussfolgerungen, die die Bundesanalyse aus dem
  Vergleich der Systembereiche für die Anpassungsplanung zieht, in der Reihenfolge des Textes;
- A11 — ``METHODISCHE_GRENZE``: die methodische Grenze des Vergleichs (Fußnote 30).

Das Modul **übernimmt** die Aussagen der Quelle, es rechnet nichts. Jeder Eintrag hat
``schluss`` (Kennung), ``titel``, ``aussage`` (Wiedergabe mit Zitaten aus dem Text) und
``seiten`` (Druckseiten des Berichts). Die Quelle zieht das besondere Handlungserfordernis
ausdrücklich für den ganzen Systembereich „Natürliche Systeme und Ressourcen“, nicht für einzelne
Klimawirkungen aus Kaskadeneffekten; das steht im Feld ``geltungsbereich``.
"""

from __future__ import annotations

QUELLE = (
    "UBA/BMU, ›Klimawirkungs- und Risikoanalyse 2021 für Deutschland‹, Teilbericht 6 "
    "(Integrierte Auswertung), Kapitel 7 ›Querbetrachtung der Systembereiche‹, S. 153–154; "
    "Tabelle 28 und Fußnote 30, S. 153. Dessau-Roßlau, 2021. "
    "Datei docs/KWAR/kwra2021_teilbericht_6_integrierte_auswertung_bf_211027_0.pdf."
)

SCHLUESSE_ANPASSUNGSPLANUNG: list[dict] = [
    {
        "schluss": "staerker_betroffen_langsamer_weniger_wirksam",
        "titel": "Natürliche Systeme: stärker betroffen, langsamer und weniger wirksam angepasst",
        "aussage": (
            "Der Systembereich „Natürliche Systeme und Ressourcen“ ist „grundsätzlich stärker vom "
            "Klimawandel betroffen als die anderen Systembereiche. Gleichzeitig ist hier die "
            "Anpassungsdauer tendenziell deutlich höher und es kommt hinzu, dass die Wirksamkeit "
            "von Anpassungsmaßnahmen vergleichsweise gering ist.“ Diese Lage „ist in sich schon "
            "ungünstig. Besonderer Beachtung bedarf sie aufgrund der Verflechtungen der einzelnen "
            "Systeme.“ (S. 153)"
        ),
        "seiten": [153],
    },
    {
        "schluss": "vorgelagert_mehr_als_die_haelfte",
        "titel": "Natürliche Systeme wirken auf die anderen Bereiche ein",
        "aussage": (
            "Klimawirkungen aus dem Systembereich „Natürliche Systeme und Ressourcen“ „haben viel "
            "häufiger ausgehende Wirkbeziehungen, das heißt, sie sind vorgelagert und wirken auf "
            "nachgelagerte Klimawirkungen in anderen Systembereichen ein. Mehr als die Hälfte aller "
            "ausgehenden Wirkbeziehungen entfallen auf diesen Systembereich (Tabelle 28).“ Laut "
            "Tabelle 28 sind das 80 von 157 ausgehenden Wirkbeziehungen zu den jeweils vier anderen "
            "Bereichen. Die Wirkungen zeigen sich teils unmittelbar, teils „erst mit Verzögerungen, "
            "gegebenenfalls erst viele Jahre später“ (S. 153)."
        ),
        "ausgehend_natuerliche_systeme": 80,
        "ausgehend_summe": 157,
        "seiten": [153],
    },
    {
        "schluss": "blick_auf_vorgelagerte_klimawirkungen",
        "titel": "Blick auf vorgelagerte Klimawirkungen und die natürlichen Systeme richten",
        "aussage": (
            "„Der Blick [sollte] verstärkt auf vorgelagerte Klimawirkungen gerichtet werden […] "
            "und hier insbesondere auf den Systembereich der ‚Natürlichen Systeme und "
            "Ressourcen‘, von dem aus die meisten Klimawirkungen ausgehen.“ Gelingt es, dort die "
            "Auswirkungen einzugrenzen, kann das „für sehr viele Klimawirkungen in anderen "
            "Systembereichen positive Effekte haben“. Gelingt dort keine wirksame Anpassung, „so "
            "wird dies Rückwirkungen auf alle anderen Systembereiche“ haben — naturnutzende "
            "Wirtschaftssysteme, Infrastrukturen und Gebäude, naturferne Wirtschaftssysteme und "
            "„letztlich ‚Menschen und soziale Systeme‘“ (S. 154)."
        ),
        "seiten": [154],
    },
    {
        "schluss": "sensitivitaetsfaktoren_land_und_wasser",
        "titel": "Sensitivitätsfaktoren natürlicher Ressourcen stützen den Schluss",
        "aussage": (
            "Die Untersuchung der Sensitivitätsfaktoren (Kap. 3.2) stützt die Aussage: „gerade "
            "Faktoren, die natürliche Ressourcen betreffen, wie Landnutzung oder Wassernutzung“, "
            "sind „besonders häufig in verschiedenen Handlungsfeldern und bei vielen "
            "Klimawirkungen wichtig für die Empfindlichkeit der betroffenen Systeme“. Ihr Schutz "
            "„wirkt sich also in vielfacher Hinsicht positiv aus“ (S. 154)."
        ),
        "seiten": [154],
    },
    {
        "schluss": "zielkonflikte_wasser_land_raumplanung",
        "titel": "Zielkonflikte bei Wasser- und Landnutzung vorbeugend eingrenzen",
        "aussage": (
            "Es scheint wichtig, „vorbeugend zukünftige Zielkonflikte, insbesondere bei der "
            "Nutzung von Wasserressourcen wie auch bei der Nutzung von Landressourcen, "
            "einzugrenzen“. Beide Ressourcen werden künftig verstärkt beansprucht; „Hier wird der "
            "Raumplanung künftig eine noch gewichtigere Rolle zukommen.“ (S. 154)"
        ),
        "seiten": [154],
    },
    {
        "schluss": "besonderes_handlungserfordernis",
        "titel": "Besonderes Handlungserfordernis bei den natürlichen Systemen",
        "aussage": (
            "Verstärkend zu Kapitel 6 besteht „ein besonderes Handlungserfordernis im Bereich der "
            "‚Natürlichen Systeme und Ressourcen‘“. Die Methodik der KWRA 2021 erlaubt es nicht, "
            "„für einzelne Klimawirkungen Handlungserfordernisse aus Kaskadeneffekten heraus "
            "abzuleiten“ (nicht evaluiert wurde, wie genau und wie stark Klimawirkungen aufeinander "
            "einwirken und ob Verzögerungen eintreten); „für den gesamten Systembereich“ lässt sich "
            "aber schließen, dass Klimaanpassung dort „eine besonders große und wichtige Rolle "
            "spielt“ (S. 154)."
        ),
        "geltungsbereich": (
            "ganzer Systembereich „Natürliche Systeme und Ressourcen“, nicht einzelne "
            "Klimawirkungen aus Kaskadeneffekten"
        ),
        "seiten": [154],
    },
    {
        "schluss": "autonome_anpassungsfaehigkeit_entlastung",
        "titel": "Autonome Anpassungsfähigkeit stärken, Systeme entlasten",
        "aussage": (
            "Die Möglichkeiten erfolgreicher Klimaanpassung sind in diesem Bereich „besonders "
            "eingeschränkt“. „Neben Klimaschutz scheint daher die hauptsächliche "
            "Einwirkungsmöglichkeit darin zu bestehen, die autonome Anpassungsfähigkeit sowie die "
            "Funktionsfähigkeiten der Systeme zu stärken und deren Einschränkungen zu reduzieren“; "
            "dafür bedarf es „einer grundsätzlichen Entlastung dieser Systeme von aktueller "
            "Übernutzung und Überbeanspruchung durch den Menschen“ (S. 154)."
        ),
        "seiten": [154],
    },
]

METHODISCHE_GRENZE: dict = {
    "titel": "Methodische Grenze des Vergleichs",
    "aussage": (
        "„Bei der Bewertung der Klimarisiken konnte schon systematisch kein Bezug darauf genommen "
        "werden, inwiefern die Anpassung an den Klimawandel bei den vorgelagerten Klimawirkungen "
        "erfolgreich sein wird oder nicht.“ (S. 153) „Es besteht vor diesem Hintergrund das "
        "Risiko, dass für nachgelagerte Klimawirkungen das Bild verzerrt wurde in der Erwartung, "
        "dass sich nur geringe Effekte aus den vorgelagerten Klimawirkungen durchschlagen "
        "würden.“ Und obwohl die KWRA 2021 Wirkbeziehungen wesentlich systematischer erfasst hat "
        "als die VA 2015, „kann nicht davon ausgegangen werden, dass alle Wirkbeziehungen "
        "tatsächlich berücksichtigt wurden“ (S. 153–154)."
    ),
    "fussnote": 30,
    "fussnote_text": (
        "„Die Einschätzung der Anpassungskapazitäten erfolgte (aus methodischen Gründen) zeitlich "
        "erst nach der Bewertung der Klimarisiken ohne Anpassung (siehe Teilbericht 1, ‚Konzept "
        "und Methodik‘).“ (Fn. 30, S. 153)"
    ),
    "folgen": [
        "Das Bild für nachgelagerte Klimawirkungen kann verzerrt sein (S. 154).",
        "Nicht alle Wirkbeziehungen sind erfasst (S. 154).",
    ],
    "seiten": [153, 154],
}
