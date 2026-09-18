# Konformitäts-Checkliste: KAP2 gegen KWRA 2021

Interne Arbeitsgrundlage. Kein Konformitätsclaim nach außen ohne Freigabe des Aufsichtsrats.

Diese Checkliste stellt Anforderungen aus der Klimawirkungs- und Risikoanalyse 2021 für
Deutschland (Quelle: KWRA 2021, Fundstelle-Datei
`kwra2021_teilbericht_1_grundlagen_bf_211027_0.pdf`) den entsprechenden Umsetzungen im
Produkt gegenüber. Sie entsteht paketweise (T-0344); dieses Paket trägt die Zeilen 1–5.
Zeilen 6–25 sind eigene, spätere Pakete und werden hier nicht vorweggenommen.

## Tabelle

| Nr | Anforderung | Quelle | Fundstelle | Status | Beleg im Produkt | Lücke |
|---|---|---|---|---|---|---|
| 1 | Das Klimarisiko ist über Klimawirkungsketten herzuleiten, die klimatischen Einfluss, Sensitivität und räumliche Exposition als benannte, unterscheidbare Komponenten abbilden. | KWRA 2021 | kwra2021_teilbericht_1_grundlagen_bf_211027_0.pdf, Kap. 2.1.4.1 | erfüllt | docs/methodik/95_hitzebelastung.md, docs/methodik/61_vegetation_in_siedlungen.md | — |
| 2 | Das Klimarisiko ist ausdrücklich als "Risiko ohne (weitere) Anpassung" auszuweisen und von einem Zustand "mit Anpassung" begrifflich zu unterscheiden. | KWRA 2021 | kwra2021_teilbericht_1_grundlagen_bf_211027_0.pdf, Kap. 2.1.4.1 | teilweise | docs/methodik/61_vegetation_in_siedlungen.md | Nur der Methodik-Bericht zu Vegetation in Siedlungen weist einen Vergleichswert "ohne Anpassung" explizit in KWRA-Terminologie aus. Für die übrigen vorliegenden Methodik-Berichte fehlt ein systematischer, unter diesem Begriff geführter Ausweis; die Aufgabenbeschreibung (docs/AUFGABE_METHODIK_SCHADENSRECHNUNG.md) definiert die Unterscheidung "ohne Anpassung"/"mit Anpassung" bislang nicht als eigenen Pflichtabschnitt. |
| 3 | Für jeden in die Bewertung eingehenden Parameter beziehungsweise Faktor ist die zugrunde gelegte Quelle offenzulegen und zu dokumentieren; ist keine Quelle vorhanden, ist die Abschätzung als solche kenntlich zu machen. | KWRA 2021 | kwra2021_teilbericht_1_grundlagen_bf_211027_0.pdf, Kap. 2.1.3 (S. 42, Tabelle 3) und Kap. 1.3 (S. 34) | erfüllt | docs/evidenz/register.md, docs/methodik/95_hitzebelastung.md | — |
| 4 | Sensitivität (Anfälligkeit eines Systems gegenüber einem klimatischen Einfluss) und räumliche Exposition (Vorhandensein potenziell betroffener Systemelemente) sind begrifflich und methodisch getrennt zu führen, nicht zu vermischen. | KWRA 2021 | kwra2021_teilbericht_1_grundlagen_bf_211027_0.pdf, Kap. 2.1.4.1 (S. 44) | erfüllt | docs/methodik/95_hitzebelastung.md | — |
| 5 | Die Analyse muss ihre methodischen Grenzen und ihren Anwendungsbereich explizit benennen, insbesondere dass sie keine detailliertere lokale oder sektorale Risikoanalyse ersetzt. | KWRA 2021 | kwra2021_teilbericht_1_grundlagen_bf_211027_0.pdf, Kap. 1.4 (S. 35) | erfüllt | docs/methodik/95_hitzebelastung.md, docs/methodik/60_gebaeudeschaeden_flusshochwasser.md | — |

## Ergebnis

Fünf Anforderungen (Zeilen 1–5) aus Kapitel 1 und 2 des Teilberichts 1 wurden erfasst: vier als
`erfüllt`, eine (Zeile 2, Trennung "Klimarisiko ohne/mit Anpassung") als `teilweise`, weil nur ein
vorliegender Methodik-Bericht diese KWRA-Unterscheidung ausdrücklich verwendet. Keine Lücke
wurde behoben, kein Produktcode wurde angefasst — das war nicht Aufgabe dieses Pakets.

Prüflauf der genannten Belegpfade (`ls -d` je Pfad):

```
$ ls -d docs/methodik/95_hitzebelastung.md
docs/methodik/95_hitzebelastung.md
$ ls -d docs/methodik/61_vegetation_in_siedlungen.md
docs/methodik/61_vegetation_in_siedlungen.md
$ ls -d docs/evidenz/register.md
docs/evidenz/register.md
$ ls -d docs/methodik/60_gebaeudeschaeden_flusshochwasser.md
docs/methodik/60_gebaeudeschaeden_flusshochwasser.md
```

Kein Pfad wurde als `No such file` gemeldet; alle vier zitierten Belegpfade existieren im
Produkt-Repo.

Für das Inhaltsverzeichnis wurden die Seiten 1–10 des PDFs gelesen, für die Kapitelinhalte die
Seiten 33–48 (Kapitel 1 und 2.1). Insgesamt 26 PDF-Seiten, innerhalb des Rahmens von höchstens
40 Seiten.
