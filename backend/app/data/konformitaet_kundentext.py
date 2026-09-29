"""Kundensätze zu den Zeilen der Konformitäts-Checkliste, die nicht „erfüllt“ sind (T-1530).

Teil 2 des PDF-Ergebnisberichts zeigt bei „teilweise“ und „offen“ diesen Satz statt der Spalte
„Lücke“ aus ``docs/KONFORMITAET_CHECKLISTE.md``: Die Spalte „Lücke“ ist eine interne Arbeitsnotiz
(Pfade, Funktionsnamen, Ticketkennungen, Verweise auf die eigene Prüfung) und gehört nicht in ein
Kundenexemplar (Entscheidung des CEO, 27.09.2026). Jeder Kundensatz hier beschreibt aus Sicht einer
Kommune, was das Produkt zu dieser Anforderung heute leistet und was fehlt, und nennt dieselben
fehlenden Punkte wie die Spalte „Lücke“ — nur verständlich formuliert (A-0034).

Der Status je Zeile ist hier ausdrücklich mitgeführt: Ändert eine künftige Normprüfung den Status
einer Zeile der Checkliste, ohne dass jemand den Kundensatz nachzieht, bricht die Erzeugung von
Teil 2 ab (``konformitaet.py``, ``kundensatz``), statt einen veralteten Kundensatz stillschweigend
weiter zu zeigen.

Nur Zeilen mit Status „teilweise“ oder „offen“ stehen hier; „erfüllt“ zeigt in Teil 2 einen Strich.
"""

from __future__ import annotations

KUNDENTEXT: dict[int, tuple[str, str]] = {
    2: (
        "teilweise",
        "Nur bei einer der bewerteten Klimawirkungen weist der Bericht ausdrücklich aus, wie hoch "
        "das Risiko ohne zusätzliche Anpassung wäre; bei den übrigen Klimawirkungen fehlt dieser "
        "Vergleichswert bislang.",
    ),
    6: (
        "teilweise",
        "Die Reihenfolge, in der neue Klimawirkungen ins Produkt aufgenommen werden, ist nicht für "
        "jede Klimawirkung einzeln aus Risikohöhe und Zeitdruck hergeleitet, und ein Drittel der "
        "bundesweit besonders dringenden Klimawirkungen fehlt im heutigen Katalog noch.",
    ),
    7: (
        "teilweise",
        "Die Einordnung in die fünf Handlungsgruppen unterscheidet nicht zwischen bereits "
        "beschlossenen und weiteren möglichen Maßnahmen und rechnet keinen optimistischen und "
        "keinen pessimistischen Fall; die Gruppe „Innovation“ bedeutet im Produkt nur, dass keine "
        "ausreichend wirksame Maßnahme rechnerisch verknüpft ist, nicht dass wirklich alle "
        "Maßnahmen das Ziel verfehlen. Die Sicherheit der Einordnung berücksichtigt nicht, wie "
        "sicher die Anpassungsfähigkeit eingeschätzt ist, eine im amtlichen Vorbild vorgesehene "
        "Ausnahme für Aeroallergene fehlt, und es gibt weder eine gerechnete Empfindlichkeit der "
        "Einordnung noch einen Handlungsdruck je Gruppe; eingeordnet wird jede Klimawirkung, nicht "
        "nur die besonders dringenden. Dadurch landen die Aeroallergene und die UV-Schädigung in "
        "der strengsten Gruppe, obwohl das amtliche Vorbild sie milder einstuft, weil im Produkt "
        "noch keine wirksame Maßnahme für sie hinterlegt ist; diese Ursache nennt das Produkt an "
        "der Stelle nicht.",
    ),
    8: (
        "teilweise",
        "Die Skala für die Sicherheit der Einschätzung hat vier Stufen wie im amtlichen Vorbild, "
        "doch die Herleitung unterscheidet sich: Das Original bildet die Sicherheit je "
        "Zeitabschnitt aus fünf Bausteinen (Vorhandensein der Daten, Zuverlässigkeit der Daten, "
        "Verständnis der Wirkzusammenhänge, Plausibilität der Modellannahmen, Eindeutigkeit der "
        "Trends), das Produkt misst "
        "stattdessen nur, wie viele Rechenparameter belegt sind, ohne nach Zeitabschnitt zu "
        "unterscheiden. Das führt zu Widersprüchen zum amtlichen Vorbild: Bei der UV-Schädigung "
        "zeigt das Produkt hohe Sicherheit, wo die amtliche Einschätzung zum Jahrhundertende sehr "
        "geringe Sicherheit ausweist, und ein einzelner geschätzter Parameter senkt die Sicherheit "
        "bei der Hitzebelastung auf mittel. Es fehlen zudem eine Mittelung je Handlungsfeld und "
        "Themenbereich mit Angabe des Grades, der Vergleich zwischen den Zeitabschnitten, der "
        "Bezug zur Höhe des Risikos und ein Vergleich über mehrere Handlungsfelder hinweg, weil "
        "das Produkt bisher nur das Feld Gesundheit bearbeitet.",
    ),
    9: (
        "teilweise",
        "Das Produkt zeigt die Wechselwirkungen zwischen Klimawirkungen, die das amtliche Vorbild "
        "im Fließtext einzeln benennt, sowie deren Bündelung nach Handlungsfeldern, "
        "Themenbereichen und einen Rückkopplungskreislauf. Zwei Punkte fehlen: Von den insgesamt "
        "257 dort ausgewerteten Wechselwirkungen sind nur die im Fließtext einzeln genannten "
        "übernommen, weil die Quelle keine vollständige Liste veröffentlicht; und wie stark sich "
        "die Handlungsfelder gegenseitig beeinflussen, ist im Produkt nicht aus der amtlichen "
        "Abbildung abgelesen, sondern ausdrücklich als Grenze des Modells ausgewiesen.",
    ),
    10: (
        "teilweise",
        "Die fünf gesellschaftlichen Bereiche, in die das amtliche Vorbild alle Klimawirkungen "
        "einteilt, sind im Produkt hinterlegt, ein Vergleich zwischen ihnen findet aber nicht "
        "statt: Alle drei heute gerechneten Klimawirkungen liegen im selben Bereich, die übrigen "
        "vier Bereiche bleiben leer, und die geplanten weiteren Klimawirkungen tragen noch keinen "
        "Bereich. Die Risikohöhe wird anders verglichen als im amtlichen Vorbild vorgesehen, und "
        "die Anpassungsfähigkeit je Bereich — Wirkung bereits beschlossener und weiterer "
        "Maßnahmen, verbleibendes Risiko mit Anpassung, Zeitbedarf und Grenzen der Anpassung — "
        "wird ebenso wenig ermittelt wie die Sicherheit der Einschätzung, die maßgeblichen "
        "klimatischen Einflüsse je Bereich und die Zahl der besonders dringenden "
        "Handlungserfordernisse; die daraus abzuleitenden Schlüsse für die Anpassungsplanung "
        "fehlen entsprechend.",
    ),
    11: (
        "teilweise",
        "Diese gesetzliche Pflicht richtet sich an die Bundesregierung, eine bundesweite "
        "Klimarisikoanalyse zu erstellen und alle acht Jahre zu erneuern. Das Produkt liefert eine "
        "eigene, kommunenbezogene Risikoeinschätzung, ersetzt damit aber nicht die bundesweite "
        "Analyse und enthält keinen eingebauten Mechanismus, der eine Erneuerung im gesetzlich "
        "vorgesehenen Achtjahresrhythmus sicherstellt oder nachweist.",
    ),
    12: (
        "offen",
        "Diese gesetzliche Pflicht richtet sich an die Bundesregierung, alle vier Jahre eine "
        "bundesweite Anpassungsstrategie mit messbaren Zielen vorzulegen und fortzuschreiben. Das "
        "Produkt ist ein Werkzeug für Kommunen und Berater und bildet weder eine solche "
        "Bundesstrategie noch ihren Fortschreibungszyklus ab; diese Anforderung betrifft das "
        "Produkt nicht.",
    ),
    13: (
        "teilweise",
        "Das Produkt berücksichtigt Klimaanpassung bislang nur für das Handlungsfeld Gesundheit; "
        "die übrigen 16 Handlungsfelder stehen immer auf „nicht betroffen“, und keine Maßnahme "
        "wirkt über mehr als ein Handlungsfeld hinweg. Die im Gesetz ausdrücklich genannten "
        "Auswirkungen — Überflutung, Grundwasser und Trockenheit, Bodenerosion — sind im Produkt "
        "bisher nur vorgesehen, aber nicht gerechnet; ob eine Planung eine städtische Wärmeinsel "
        "verstärkt, wird nicht verglichen; bereits eingetretene und erst erwartete Auswirkungen "
        "werden nicht getrennt ausgewiesen, und ob Versickerungs-, Speicher- und "
        "Verdunstungsflächen erhalten bleiben, erfasst das Produkt nicht.",
    ),
    15: (
        "teilweise",
        "Wie bei der Einstufung dringender Handlungserfordernisse übernimmt das Produkt die "
        "Kategorie „sehr dringend“ nur punktuell in der Ausbaureihenfolge, ohne sie für jede "
        "Klimawirkung systematisch und vollständig aus einer eigenen Risikoanalyse herzuleiten; "
        "ein Teil der bundesweit als sehr dringend eingestuften Klimawirkungen fehlt im heutigen "
        "Katalog.",
    ),
    16: (
        "teilweise",
        "Die Bestandsaufnahme erfasst besonders betroffene Personengruppen und empfindliche "
        "Einrichtungen nur zum Teil: Bei vier von sieben Personengruppen sowie bei "
        "Kindertagesstätten und Schulen liegt kein Wert vor, nur ein Hinweis auf die Lücke; "
        "Naturschutzgebiete und Lieferketten fehlen ganz. Entwicklungen wie demografischer Wandel, "
        "Verstädterung, der Zustand natürlicher Systeme, vergangene Extremereignisse mit ihren "
        "Schäden sowie vorhandene kommunale Untersuchungen (etwa Hochwasser- und "
        "Starkregengefahrenkarten) erhebt das Produkt nicht, und es benennt keine dadurch "
        "betroffenen Handlungsfelder. Rahmenbedingungen und der bisherige Temperaturverlauf sind "
        "nur über das allgemeine Kommunenprofil verfügbar, und dieses liegt nur je Bundesland vor, "
        "nicht je Kommune.",
    ),
    17: (
        "offen",
        "Das Produkt unterstützt nicht dabei, interessierte Personen und Gruppen zu identifizieren "
        "oder einen Beteiligungsprozess zu planen und zu begleiten; es berechnet Klimarisiken, "
        "bietet aber keine Funktion für die Organisation eines solchen Beteiligungsverfahrens.",
    ),
    18: (
        "teilweise",
        "Die vier Bausteine der Anpassungsfähigkeit sind mit einer Selbsteinschätzung auf vier "
        "Stufen hinterlegt. Es fehlt aber die Verknüpfung mit dem bewerteten Klimarisiko zu einem "
        "verbleibenden Risiko mit Anpassung, ein Beleg, dass die Stufen den international "
        "vorgesehenen Reifegraden entsprechen, sowie Aussagen zu möglichen Anpassungsoptionen, zum "
        "Bedarf an weitergehender oder grundlegender Anpassung, zu Wechselwirkungen und "
        "Zielkonflikten zwischen Maßnahmen und zu den Grenzen der Anpassung; auch fehlt ein "
        "Vermerk, wer die Einschätzung vorgenommen hat und ob im Einvernehmen.",
    ),
    19: (
        "teilweise",
        "Das Produkt weist die Unsicherheit der zugrunde liegenden Daten je Handlungsfeld aus und "
        "verlangt ab einer bestimmten Schwelle vorsichtige Interpretation. Es vergleicht diese "
        "Unsicherheit aber nicht über mehrere Handlungsfelder hinweg, weil bisher nur das Feld "
        "Gesundheit bearbeitet ist, und stellt keine wechselseitigen Abhängigkeiten zwischen "
        "Handlungsfeldern oder zu Nachbarkommunen fest. Die Unsicherheit ist auch nicht mit "
        "einzelnen Handlungsmöglichkeiten verknüpft; eigene Leitfragen der Kommune, die "
        "Einbeziehung von Fachabteilungen, externer Expertise und benachbarter Kommunen sowie die "
        "Unterscheidung, ob eine Kommune eine Maßnahme allein umsetzen kann, fehlen. Geschlechter- "
        "und Diversitätsaspekte berücksichtigt das Produkt bislang nur über das Alter.",
    ),
    20: (
        "teilweise",
        "Für die breite Öffentlichkeit stellt das Produkt derzeit nichts bereit: Es gibt keine "
        "öffentlich zugängliche Karte, keine Broschüre und keinen Online-Auftritt mit den "
        "Ergebnissen einer Kommune oder Hinweisen zur eigenen Vorsorge. Die Kurzfassung für "
        "Entscheidungsträger nennt keine Dringlichkeit der Handlungserfordernisse, führt als "
        "Handlungsmöglichkeiten nur bereits geplante Maßnahmen auf, erklärt ihre Fachbegriffe "
        "nicht und enthält keine Karte. Einen ausführlichen Abschlussbericht mit Detailergebnissen "
        "je Kommune gibt es nicht; die Methodik-Berichte sind bundesweit gleich und gehen als "
        "Anlagen mit diesem Bericht, verzeichnet in Teil 9 (zur Hitzebelastung Anlage M95). "
        "Auf einzelne "
        "Zielgruppen zugeschnittene Kommunikationsziele, Beschlussvorlagen, Veranstaltungen und "
        "Kampagnen bietet das Produkt nicht.",
    ),
    21: (
        "teilweise",
        "Für Gesundheitsschäden rechnet das Produkt mit Schadenskosten, für Gebäudeschäden durch "
        "Flusshochwasser dagegen mit den Kosten der Wiederherstellung zum Neuwert. Das Produkt "
        "verwendet damit je nach Schadensart unterschiedliche Kostenkonzepte, statt durchgängig "
        "mit Schadenskosten zu rechnen, und weist diesen Wechsel des Kostenkonzepts nicht "
        "ausdrücklich als bewusste Abweichung aus.",
    ),
    22: (
        "teilweise",
        "Die Kostenprojektion weist zukünftige Kosten mit zwei Sätzen aus, wie gefordert. "
        "Abgezinst wird aber nur mit der reinen Zeitpräferenz; der zweite von der Methodenkonvention "
        "verlangte Bestandteil — die Veränderung relativer Preise über die Zeit — fehlt ohne "
        "Begründung und ohne ausgewiesene Abschätzung. Damit bleibt offen, ob für die bewerteten "
        "Gesundheitsschäden eigentlich ein höherer oder ein niedrigerer Satz gelten müsste. Der als "
        "„Barwert mit 0 Prozent“ bezeichnete Wert ist deshalb tatsächlich nur die unabgezinste "
        "Summe, und der als „Barwert mit 1 Prozent“ bezeichnete Wert ist nur ein zu 1 Prozent "
        "abgezinster Wert, nicht der von der Methodenkonvention verlangte vollständige Barwert. "
        "Risikoaversion geht in die Rechnung nicht ein.",
    ),
    25: (
        "teilweise",
        "Risiken, die absichtlich mit einem Kostensatz von null geführt werden, um "
        "Doppelzählungen zu vermeiden, sind im Produkt erklärt. Für Klimawirkungen, die "
        "methodisch schlicht noch nicht mit einem Kostensatz hinterlegt sind, gilt dagegen "
        "ebenfalls automatisch null, ohne dass das Produkt dies erläutert; und dass die daraus "
        "entstehende Gesamtsumme deshalb eine vorsichtige Untergrenze ist, weist das Produkt an "
        "dieser Stelle nicht aus.",
    ),
}
