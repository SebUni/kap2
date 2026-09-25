# Befund-Ledger — Querverbindungsanalyse (KWRA 2021, Teilbericht 6)

Angelegt 23.09.2026 mit Befund 1 (Ticket T-0486). Gegenstand: `docs/QUERVERBINDUNGEN_KLIMAWIRKUNGEN.md`,
Datenmodul `backend/app/data/kwra_querverbindungen.py`, Arbeitsmappe `docs/KWAR/KWRA-2021_Klimawirkungen.xlsx`
(Blatt „Wirkbeziehungen"). Abweichungen in der Quelle werden hier fortgeschrieben, nie still korrigiert.

## Befund 1 — Zählung der Wirkbeziehungen: 262 gegen 257

Status: offen (Quelle nicht entscheidbar; Produkt bleibt unverändert). Herkunft: Prüfer T-0456,
offene Frage Q-20260920T114850Z-pruefer-348a2a-1.

**1. Eigene Nachzählung aus Tabelle 28** (Teilbericht 6, Kap. 7, S. 153; identisch übernommen in
Arbeitsmappe, Blatt „Wirkbeziehungen", Zeilen 18–22, Abschnitt „2. Querverbindungen zwischen den
Systembereichen"; Datenmodul `SYSTEMBEREICH_MATRIX`). Die Summenspalte der Quelle wurde mitgeprüft: alle fünf
Zeilensummen „ausgehend" stimmen mit der Nachzählung überein (80/35/30/0/12).

| Zeile (von) | Diagonale (innerhalb) | übrige vier Spalten (zwischen) |
|---|---|---|
| Natürliche Systeme und Ressourcen (Z. 18) | 24 | 50 + 13 + 9 + 8 = 80 |
| Naturnutzende Wirtschaftssysteme (Z. 19) | 44 | 6 + 13 + 8 + 8 = 35 |
| Infrastrukturen und Gebäude (Z. 20) | 26 | 3 + 3 + 13 + 11 = 30 |
| Naturferne Wirtschaftssysteme (Z. 21) | 5 | 0 |
| Menschen und soziale Systeme (Z. 22) | 6 | 0 + 4 + 1 + 7 = 12 |
| **Summe** | **24 + 44 + 26 + 5 + 6 = 105** | **80 + 35 + 30 + 0 + 12 = 157** |

Nachzählung: **157 zwischen Systembereichen + 105 innerhalb eines Systembereichs = 262**
(Quelle: PDF S. 153, Tabelle 28).

**2. Kennzahl der Arbeitsmappe:** **257** Querverbindungen insgesamt — Arbeitsmappe, Blatt
„Wirkbeziehungen", Zelle B6 (Zeile 6, Abschnitt „1. Kennzahlen (Teilbericht 6, Kapitel 3.4)"). Die Quelle nennt sie
an vier Stellen gleichlautend: Teilbericht 6, Kap. 3.4, S. 83 („Im Rahmen der Analyse wurden 257 Querverbindungen
identifiziert“); Teilbericht 6, Kernaussagen der Analyse der Querverbindungen, S. 88 („Insgesamt bestehen 257
Querverbindungen …“; Überschrift dort wörtlich „Kernaussagen der Analyse der Querverbindungen“); Teilbericht 6,
Zusammenfassung, S. 20 („Insgesamt wurden 257 Querverbindungen zwischen den 102 Klimawirkungen der 13
Handlungsfelder identifiziert“); Zusammenfassungsbericht der KWRA (`kwra2021_teilbericht_zusammenfassung_…pdf`),
S. 106, gleicher Wortlaut. Seitenzahlen nach der Seitenmarke des Textauszugs.

**3. Worin die Differenz von fünf besteht:** aus der Quelle nicht entscheidbar. Es fehlt die Kantenliste der 257
Querverbindungen (Einzelbeziehungen je Klimawirkung, von der KWRA in keinem der sechs Teilberichte veröffentlicht;
Abbildung 8, S. 83, zeigt nur das Chord-Diagramm auf Handlungsfeldebene) sowie eine Angabe des Teilberichts,
ob Tabelle 28 gleich abgegrenzt zählt wie Kap. 3.4. Durchgesehen für diese Aussage (Stand 23.09.2026): Teilbericht 6, Kap. 3.4 (S. 82–88), auf die
Stichworte „Liste“, „Anhang“ und „Tabelle“ durchsucht (keine Treffer, Text zu den 257 in Auszügen gelesen); Tabelle 28 (S. 153) und das Tabellenverzeichnis (S. 10) von
Teilbericht 6; über alle Teilberichte 1–6, den Zusammenfassungsbericht und den Anhang (`cc_20-2021_kwra2021_anhang.pdf`)
eine Volltextsuche nach „257“, „Querverbindung“ und „Wirkbeziehung“ (im Anhang keine Treffer; sein Inhaltsverzeichnis
nennt Anhänge A bis E — Expertenlisten, Szenarien, Indikator-Kennblätter —, keinen zu Wirkbeziehungen; die
Teilberichte 1–5 enthalten keinen Treffer für 257 in diesem Zusammenhang). Die Stichwortsuche ist Ergänzung; die
Aussage „keine Kantenliste veröffentlicht“ deckt sich mit dem Vermerk der Arbeitsmappe (Blatt „Wirkbeziehungen“,
Zeile 2; Blatt „Lesehinweise“, Zeile 40) und wird von dort **als übernommene Angabe** geführt, nicht als eigene
vollständige Durchsicht der Teilberichte 2–5 Seite für Seite. Belegt ist nur das Gegenteil einer naheliegenden Erklärung:
Kap. 3.4 nimmt die rein vorgelagerten Klimawirkungen in die 257 hinein (Fußnote 20, S. 82), Tabelle 28
schließt sie aus (Tabellenvermerk, S. 153). Das würde Tabelle 28 kleiner machen als 257, nicht größer — die
Abgrenzung erklärt die Differenz also nicht. Ob doppelt geführte Paare, gegenseitige Wechselwirkungen (S. 88:
Wirkung in beide Richtungen), Selbstbezüge oder Rundung die fünf ausmachen, lässt sich ohne die Kantenliste nicht
prüfen und wird hier nicht vermutet.

**4. Zahl im Produkt:** Das Produkt weist **257** aus (Datenmodul `querverbindungen_gesamt`, Dienst
`querverbindungen.py`, Frontend `RiskInteractionSection.tsx`, Analysedokument) — die Kennzahl der Quelle mit Fundstelle
S. 83/88. Die Systembereichs-Matrix wird mit ihren Tabellenwerten unverändert geführt; das Produkt summiert sie
nirgends zu 262 und stellt beide Zahlen nicht gegenüber. **Änderung nicht nötig:** 257 ist die zitierte Zahl der
amtlichen Vorlage, die Matrix ist eine Wiedergabe von Tabelle 28. Nachzählt ein Gutachter die Matrix, findet er hier
262 und die Erklärung, dass die Quelle selbst zwei verschieden abgegrenzte Zahlen enthält. Im Produkt wurde in diesem
Paket nichts geändert. Vorschlag für ein Folgepaket (nicht Teil von T-0486): Nachfrage beim UBA/adelphi nach der
Kantenliste bzw. ein Hinweis in der Produktanzeige, dass die Systembereichs-Matrix 262 Beziehungen summiert.

## Befund 2 — Arbeitsmappe führt nicht alle im Fließtext genannten Einzelbeziehungen

Status: im Produkt behoben, Arbeitsmappe unverändert (amtliche Quelldatei, Vorgabe des CEO im Vorhaben T-0870-ceo,
Nachtrag 24.09.2026). Herkunft: Gegenprobe Zeile 9 (T-0741-ceo), Anforderungen A1 und A3, Codebefund C2; umgesetzt
in T-0936-cto.

**Abweichung:** Das Blatt „Wirkbeziehungen“ der Arbeitsmappe, Abschnitt „3. Im Fließtext ausdrücklich benannte
Einzelbeziehungen“, führt 20 Beziehungen, alle in eine Richtung und mit dem Beleg „TB6 Kap. 3.4“ ohne Seite.
Teilbericht 6, Kap. 3.4 nennt im Fließtext weitere Beziehungen (S. 82–88 vollständig gelesen, Seitenzahl = gedruckte
Seite = PDF-Seite):

| Beziehung | Richtung | Seite |
|---|---|---|
| Wassermangel im Boden (#13) → Schäden in Wäldern (#8) | gerichtet | 82 |
| Schäden in Wäldern (#8) → Nutzfunktion: Holzertrag (#31) | gerichtet | 82 |
| Schäden in Wäldern (#8) → Nutzfunktion: Erholung (#32) | gerichtet | 82 |
| Gewässertemperatur und Eisbedeckung und biologische Wasserqualität (#53) ↔ Mangelndes Kühlwasser für thermische Kraftwerke (#68) | gegenseitig | 82, 85 |
| Bedarf an Kühlenergie (#65) ↔ Stadtklima/Wärmeinseln (#62) | gegenseitig | 85 |
| Hitzebelastung (#95) → Bedarf an Kühlenergie (#65) | gerichtet | 85–86 (Abb. 9) |
| Verschiebung von Arealen und Rückgang der Bestände (#4) ↔ Vegetation in Siedlungen (#61) | gegenseitig | 86 |

Die Unterscheidung „in eine Richtung führend“ gegen „gegenseitige Wechselwirkung“ trifft die Quelle selbst (S. 82,
S. 85: „Neben den bisher aufgeführten einseitigen Querverbindungen …“). Die IDs stammen aus dem Blatt
„Klimawirkungen“ der Arbeitsmappe.

**Produkt:** `BENANNTE_BEZIEHUNGEN` in `backend/app/data/kwra_querverbindungen.py` führt die sieben Beziehungen
zusätzlich (jetzt 27), jede mit dem Vermerk „nicht aus der Arbeitsmappe“ im Beleg. Alle 27 Einträge tragen das
Feld `richtung` („gerichtet“ oder „gegenseitig“) und die Seite im Beleg; bei den 20 übernommenen Einträgen ist nur
die Seite ergänzt, Wortlaut und Richtung sind die der Arbeitsmappe. Dieselbe Tabelle steht in
`docs/QUERVERBINDUNGEN_KLIMAWIRKUNGEN.md`, Abschnitt „Benannte Einzelbeziehungen“.
