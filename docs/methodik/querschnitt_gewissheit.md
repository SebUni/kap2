# Querschnitt: Gewissheit einer Klimawirkung

Querschnittsdatei der Methodik, gültig für alle 102 Klimawirkungen der KWRA 2021 (TB6 S. 35). Werte bekommen zuerst
#95, #96 und #98 (A-0048; Vorhaben T-1117-cmo). Schritt 1 (Ticket T-1172-methodik_manager) rechnet #95. Schritt 2
(T-1173-methodik_manager) liest TB6 Kap. 6.2 (Zeitscheibe und Schwellen der Charakterisierung). Schritt 3
(T-1174-methodik_manager) rechnet #96 nach. Schritt 4 (T-1175-methodik_manager) rechnet #98 und schließt die Datei mit
der Übersicht am Ende ab.

Abkürzungen: **KWRA** = Klimawirkungs- und Risikoanalyse 2021 für Deutschland; **TB6** = deren Teilbericht 6
„Integrierte Auswertung“ (`docs/KWAR/kwra2021_teilbericht_6_integrierte_auswertung_bf_211027_0.pdf`; in Kap. 2 und
Kap. 3.3 stimmen PDF-Seite und gedruckte Seite überein); **Mappe** = `docs/KWAR/KWRA-2021_Klimawirkungen.xlsx`,
Blatt „Klimawirkungen“ (Zeile 2 Kopfzeile, Zeilen 3–104 die 102 Klimawirkungen).

## Festlegung

**Regel G (Gewissheit einer Klimawirkung).** Als Gewissheit einer Klimawirkung weist das Produkt die *Gewissheit der
Bewertung* der KWRA 2021 aus, unverändert übernommen, nicht nachgerechnet: je Klimawirkung ein Wert für die
Zeitscheibe Mitte des Jahrhunderts (2031–2060) und ein Wert für die Zeitscheibe Ende des Jahrhunderts (2071–2100), auf
der Skala sehr gering, gering, mittel, hoch, mit der Fundstelle TB6 Tabelle 1. Die Jahre des Produkts bekommen den
Wert nach der Zuordnungstabelle unten. Für das heutige Klima steht „in der KWRA nicht ausgewiesen“. Der Anteil der
Parameter mit Quelle, den `gewissheit.py` heute als Gewissheit ausgibt, ist keine Gewissheit: Er heißt „Quellenlage
der Rechnung“, erscheint nur als Zählung (etwa „10 von 30 Parametern mit Quelle“ bei #95, Stand 07.10.2026), ohne
Stufe, und keine Folgegröße setzt auf ihm auf.

### Herleitung und Fundstelle

- **Was die KWRA bestimmt hat.** „Die Gewissheit wurde für alle Klimawirkungen für die beiden Zeitscheiben Mitte des
  Jahrhunderts (2031 bis 2060) und Ende des Jahrhunderts (2071 bis 2100) bestimmt. Der Wertebereich umfasste eine
  vierstufige Skala von ‚sehr gering‘, ‚gering‘, ‚mittel‘ und ‚hoch‘.“ (TB6 Kap. 3.3, S. 78). Bewertet hat das
  Behördennetzwerk „Klimawandel und Anpassung“ (TB6 Kap. 2.1, S. 35).
- **Wo der Wert je Klimawirkung steht.** TB6 **Tabelle 1** „Klimarisiken der untersuchten Klimawirkungen nach
  Handlungsfeld“, S. 36–41, Spaltengruppe „Gewissheit der Bewertung“ mit den Spalten „Mitte des Jahrhunderts“ und
  „Ende des Jahrhunderts“; das Handlungsfeld „Menschliche Gesundheit“ mit #95, #96 und #98 steht auf S. 41 (als Bild
  gelesen am 25.09.2026). Die Mappe führt dieselben Werte in Spalte S „Gewissheit – Mitte“ und Spalte T „Gewissheit –
  Ende“, Quellvermerk in Spalte AJ „TB 6 Tab. 1“.
- **Nicht Tabelle 17.** Tabelle 17 (S. 80) zeigt *Mittelwerte je Handlungsfeld* und über alle Klimawirkungen, keinen
  Wert je Klimawirkung. Der Kopf von `backend/app/services/gewissheit.py` nennt dafür „Tabelle 17“; richtig ist
  Tabelle 1. Den Nachzug im Code macht der CTO mit der Umsetzung dieser Regel (T-1030-ceo), nicht diese Datei.
- **Warum übernommen und nicht gerechnet.** Die Gewissheit ist eine Bewertung durch Fachleute, keine Rechengröße; die
  KWRA nennt keine Formel, aus der sie folgt, und schlüsselt sie nicht nach Teilaspekten auf (S. 81). KAP3 kann sie
  deshalb nur mit Fundstelle übernehmen. Das Einzige, was KAP3 selbst festlegt, ist die Zuordnung der Jahre des
  Produkts zu den beiden Zeitscheiben (unten).

### Verhältnis zur KWRA-Einstufung

Die Gewissheit nach Regel G **ist** die KWRA-Einstufung, Zelle für Zelle. Damit enthält sie alles, was die KWRA
hineingelegt hat, und nichts darüber hinaus:

| Merkmal der KWRA-Einstufung | Fundstelle | In Regel G |
|---|---|---|
| Fünf Teilaspekte: „Vorhandensein von Daten, die Zuverlässigkeit der verwendeten Daten, Kenntnisse über Wirkzusammenhänge, Genauigkeit und Plausibilität von Modellannahmen, die Eindeutigkeit von Trends“ | TB6 S. 78 | enthalten, so gewichtet, wie das Behördennetzwerk sie gewichtet hat |
| Teilaspekte nicht einzeln bewertet; eine direkte Bewertung der Teilaspekte wird erst „für zukünftige KWRAs“ empfohlen | TB6 S. 81 | nicht aufgeschlüsselt; KAP3 erfindet keine Teilnoten |
| Je Zeitscheibe Mitte (2031–2060) und Ende (2071–2100) | TB6 S. 78 | je Zeitscheibe ein Wert |
| Keine Gewissheit für die Gegenwart (Tabelle 1 führt die Gewissheit nur für Mitte und Ende) | TB6 Tabelle 1, S. 36–41 | „in der KWRA nicht ausgewiesen“ |
| Eine Gewissheit je Zeitscheibe für beide Fälle, optimistisch und pessimistisch | TB6 Tabelle 1, S. 36–41 | gilt gleich für RCP 4.5 und RCP 8.5 des Produkts |
| Vierstufige Skala; Zahlen 1–4 nur für Mittelwerte, eine „künstliche Spezifizierung“ | TB6 S. 78, Fußnote 18 | Stufe als Wort, keine Zahl, kein Mittelwert |

### Zuordnung der Zeitscheiben

Das Produkt kennt zwei Zeiträume: den Euro-Betrag der M0-Berichte, ein Jahresbetrag „für ein Jahr im heutigen Klima
(Preisstand 2024)“ (Bericht 95, Kap. 6), und die Zeitreihe 2025–2065 für RCP 4.5 und RCP 8.5
(`backend/app/api/routes/assessment.py`, Routen `risk-projection` und `cost-projection`).

| Zeitraum im Produkt | KWRA-Zeitscheibe | Gewissheit nach Regel G | Art der Zuordnung |
|---|---|---|---|
| Heutiges Klima (Euro-Betrag M0) | Gegenwart, „die jüngere Vergangenheit“ (TB6 S. 35, Fußnote 3) | „in der KWRA nicht ausgewiesen“ | übernommen: Die KWRA hat keinen Wert |
| Zeitreihe 2025–2030 | keine; nächste Zeitscheibe ist Mitte | Wert Mitte | Zuordnung von KAP3, Begründung unten |
| Zeitreihe 2031–2060 | Mitte des Jahrhunderts (2031–2060) | Wert Mitte | übernommen, deckungsgleich |
| Zeitreihe 2061–2065 (Regel für 2061–2070) | keine; zwischen Mitte und Ende | die niedrigere der beiden Stufen | Zuordnung von KAP3, Begründung unten |
| 2071–2100 (heute nicht im Produkt) | Ende des Jahrhunderts (2071–2100) | Wert Ende | übernommen, deckungsgleich |

- **2025–2030 bekommen den Wert Mitte.** Die KWRA findet die Erkenntnislage „für die nahe Zukunft … vergleichsweise
  gut“ und die Bewertungen „für die nahe Zukunft robuster“ (TB6 S. 78 und S. 81); die Gewissheit fällt im Mittel von
  mittel zur Mitte auf gering zum Ende (S. 78). Die Stufe Mitte überschätzt die Jahre davor also nicht. Ließe man
  sie leer, fehlte der Zeitreihe am Anfang jeder Hinweis, obwohl die KWRA für diese Nähe eher sicherer ist.
- **2061–2070 bekommen die niedrigere Stufe.** Für diese Jahre sagt die KWRA nichts. Die einfachere Regel „nächste
  Zeitscheibe“ gäbe 2061–2065 die Stufe Mitte und würde bei fallender Gewissheit mehr Sicherheit zeigen, als die KWRA
  für den anschließenden Zeitraum stützt; bei #98 zeigte sie „mittel“, fünf Jahre bevor die KWRA „sehr gering“ nennt.
  Die niedrigere Stufe irrt, wenn überhaupt, zur Vorsicht.
- **Das heutige Klima bekommt keinen Wert.** Der M0-Betrag ist aus gemessenen Größen gerechnet; die Teilaspekte
  „Plausibilität von Modellannahmen“ und „Eindeutigkeit von Trends“ beziehen sich auf die Zukunft. Seine Unsicherheit
  zeigt der Bericht als Band je Parameter (Bericht 95, Kap. 7), nicht als Stufe.

### Ein Wert je Klimawirkung, nicht je Risikocode

Die KWRA bewertet je Klimawirkung (eine Zeile je Klimawirkung in Tabelle 1 und in der Mappe). Regel G gibt deshalb
**einen Wert je Klimawirkung und Zeitscheibe**, nicht je Risikocode des Produkts. #95 „Hitzebelastung“ hat im Produkt
zwei Codes, `EXPECTED_ANNUAL_MORTALITY` (Sterbefälle) und `EXPECTED_ANNUAL_MORBIDITY` (Krankenhauseinweisungen)
(`docs/KONFORMITAET_CHECKLISTE.md`, Abschnitt „Gegenprobe Zeile 8“). Beide Codes zeigen dieselbe Gewissheit aus
derselben Zelle (Zeile 97 der Mappe). Die Kennzahl in `gewissheit.py` zählt dagegen je Code. Am 25.09.2026 standen
die beiden Codes damit auf verschiedenen Stufen (mittel und hoch), obwohl es eine Klimawirkung ist. Gemessen am
07.10.2026 stehen beide auf „gering“ (Sterbefälle 17 von 38, Krankenhauseinweisungen 3 von 9), aber nur, weil zwei
getrennte Zählungen zufällig dieselbe Stufe ergeben. Nach Regel G entfällt die Stufe je Code. Die Quellenlage zählt
ebenfalls je Klimawirkung, über die Parameter-Blöcke des einen Berichts, jeder Block einmal.

### Was die Gewissheit über den Euro-Betrag von KAP3 aussagt und was nicht

**Sie sagt:** wie sicher sich die Fachleute der Bundesanalyse sind, dass das Klimarisiko dieser Klimawirkung in der
Zeitscheibe in der Stufe liegt, die sie ihm geben (TB6 Tabelle 1). Für die Jahre der Zeitreihe heißt das: wie gut der
Wirkzusammenhang, die Datenlage und der Trend belegt sind, auf denen jede Zukunftsrechnung für diese Klimawirkung
steht, also auch die von KAP3. „Hoch“ bei #95 zur Mitte heißt: Dass Hitze zur Mitte des Jahrhunderts ein
erhebliches Risiko für die Gesundheit ist, gilt als gut belegt.

**Sie sagt nicht:**

1. wie genau der Euro-Betrag von KAP3 ist; die Spanne des Betrags zeigen die Bänder je Parameter im Bericht
   (Kap. 7) und die Parameterliste nach P1, nicht die Stufe;
2. etwas über den Euro-Betrag im heutigen Klima (M0); dafür hat die KWRA keine Gewissheit bestimmt;
3. etwas über die einzelne Kommune; die KWRA bewertet für Deutschland;
4. ob die Parameter von KAP3 eine Quelle haben; das zeigt die Quellenlage als Zählung;
5. dass ein Betrag bei „sehr gering“ falsch, null oder zu hoch wäre; „sehr gering“ heißt, dass die Entwicklung
   bis dahin wenig verstanden ist, und der Betrag ist entsprechend vorsichtig zu lesen.

## Schwelle der Stufe „mittel“

**Nach Regel G gibt es keine Schwelle, die KAP3 setzt.** Die Stufe „mittel“ wird übernommen, nicht aus einer Zahl
gebildet: Wo „mittel“ beginnt, hat das Behördennetzwerk mit seiner Bewertung je Klimawirkung festgelegt (TB6 S. 78,
Tabelle 1). Herleitung damit: übernommen, Fundstelle TB6 Tabelle 1, S. 36–41.

- **`SCHWELLE_MITTEL` = 0,5 entfällt.** Diese Zahl (Abschätzung von KAP3 in `gewissheit.py`) trennte beim Anteil der
  Parameter mit Quelle „gering“ von „mittel“. Weil die Quellenlage nach Regel G keine Stufe mehr bekommt, braucht sie
  keine Schwelle. Eine Ersatzzahl gibt es nicht.
- **Die einzige Zahlenschwelle der KWRA für „mittel“** steht in Kap. 6.2: Die Gesamtgewissheit gilt „erst ab einem
  Mittelwert von über 1,5“ als „mittel“, auf der Skala 0 = sehr gering bis 3 = hoch (TB6 S. 141). Sie betrifft die
  Charakterisierung und gehört zu Schritt 2, nicht zur Gewissheit je Klimawirkung.

## Einordnung der Charakterisierung (KWRA TB6 Kap. 6.2)

Schritt 2, Ticket T-1173-methodik_manager. Gelesen am 25.09.2026, jeweils vollständig: TB6 Kap. 6 mit 6.1 und 6.2
(S. 136–145), dazu Kap. 5.1 (S. 112–123) und Kap. 5.2 (S. 123–129), weil Kap. 6.2 auf Kap. 5 aufbaut. Als Bild gelesen:
Tabelle 24 (S. 128–129) und Tabelle 27 (S. 142). PDF-Seite und gedruckte Seite stimmen auf S. 112–145 überein. In
Runde 1 kam TB1 Kap. 2.5 dazu (S. 91–94, PDF-Seiten 92–95, vollständig gelesen), auf das TB6 Fußnote 28 verweist.

**Kurzfassung.** Die KWRA bildet die Charakterisierung für die Zeitscheibe Mitte des Jahrhunderts (2031–2060). Als
Gewissheit nimmt sie nicht die Gewissheit nach Regel G allein. Sie nimmt eine *Gesamtgewissheit*: den Mittelwert aus
der Gewissheit ohne Anpassung und der Gewissheit mit Anpassung, und „mittel“ gilt erst ab einem Mittelwert über 1,5.
Wörtlich steht beides in der Methodik der KWRA (TB1 Kap. 2.5, S. 93). Die beiden Schwellen des Produkts nennt die KWRA
nicht als Zahl. Sie bleiben Abschätzungen von KAP3 und gelten nur, wenn der Eingang des Produkts die beschlossenen
Maßnahmen misst. Der Wert 0,5 bleibt, sein Band wird 0,33–0,5 statt 0,4–0,6. Der Wert 0,1 und sein Band 0,05–0,2
bleiben, gestützt von Kap. 6.2 sind sie nicht. Die Regel der KWRA für Entwicklung (0,5 an der weiterreichenden
Anpassung) geht als Übergabe an T-1111-ceo.

### Zeitscheibe der Charakterisierung

**Kap. 6.2 nennt die Zeitscheibe nicht wörtlich.** Auf S. 140–145 steht kein Jahr und keine Zeitscheibe. Die
Zeitscheibe folgt aus drei Stellen, auf die Kap. 6.2 selbst verweist:

1. Kap. 6.2 baut auf Kap. 5 auf: „Auf der Basis der Analyse der Anpassungskapazitäten (siehe Kapitel 5) lassen sich
   zu den identifizierten Klimawirkungen mit sehr dringenden Handlungserfordernissen ergänzende Aussagen treffen.“
   (S. 140). Gefragt wird, ob die Maßnahmen „im optimistischen und im pessimistischen Fall“ ausreichen (S. 140).
2. Kap. 5 bewertet die Anpassung nur bis zur Mitte des Jahrhunderts: „Die Einschätzung der Wirksamkeit der Anpassung
   wurde separat für den Zeitraum 2020 bis 2030 und für die Mitte des Jahrhunderts (2031 bis 2060) und dabei für den
   optimistischen und den pessimistischen Fall vorgenommen.“ (S. 112). In Tabelle 24 (S. 128–129) hat der Zeitraum
   2020–2030 nur eine Spalte, und zwar für die beschlossenen Maßnahmen, ohne optimistischen und pessimistischen Fall
   und ohne weiterreichende Anpassung. Beides gibt es nur für die „Mitte des Jahrhunderts“. Die Ziele von Kap. 6.2
   setzen genau diese beiden Fälle voraus (S. 141). Für das Ende des Jahrhunderts gibt es kein Klimarisiko mit
   Anpassung.
3. Die Gewissheit mit Anpassung steht in Tabelle 24 für „2020–2031“ und „Mitte des Jahrhunderts“. Mitte ist damit die
   einzige Zeitscheibe, für die es beide Teile der Gesamtgewissheit gibt: Tabelle 1 hat Mitte und Ende, Tabelle 24
   hat 2020–2031 und Mitte.

**Wörtlich belegt in Teilbericht 1.** Für die Gesamtgewissheit verweist Kap. 6.2 auf „Teilbericht 1, ‚Konzept und
Methodik‘“ (TB6 S. 141, Fußnote 28). Dort steht die Zeitscheibe ausdrücklich: „Die mittlere Gesamtgewissheit wurde
berechnet als Mittelwert der beiden Angaben für a) die Gewissheit der Bewertung der Bedeutung des Klimarisikos (also
ohne Einbeziehung von Anpassungskapazität) für die Mitte des Jahrhunderts und b) die Gewissheit der Einschätzung der
Anpassungskapazität für die Mitte des Jahrhunderts.“ (TB1 Kap. 2.5, S. 93, PDF-Seite 94). Dass es keine andere
Zeitscheibe gab, steht ebenfalls dort: Das Verfahren hat die Unsicherheit dadurch verringert, „dass die Einschätzung
der Anpassungskapazität nur für die Mitte des Jahrhunderts vorgenommen wurde und nicht für das Ende des Jahrhunderts“
(TB1 S. 91, PDF-Seite 92, Aufzählung unmittelbar vor Kap. 2.5). Der Satz oben bleibt richtig: Kap. 6.2 selbst nennt
die Zeitscheibe nicht.

**Nachgerechnet:** Mit der Gewissheit zur Mitte aus beiden Tabellen trifft die Gesamtgewissheit bei allen 26
Klimawirkungen außerhalb von „Umsetzung“ die Gruppe von Tabelle 27. Das heißt: 13 Klimawirkungen „unter
Unsicherheit“, 13 ohne. Mit Tabelle 1 Ende statt Mitte sind es nur 19 von 26 Treffern. Mit Tabelle 24 „2020–2031“
statt Mitte sind es 18 von 26 (Beispiel-Block unten).

**Zuordnung zur Zeitscheibe des Produkts.** Die Gruppe der Charakterisierung gilt für die Zeile „Zeitreihe 2031–2060“
der Zuordnungstabelle unter „Festlegung“ und ist mit ihr deckungsgleich: KWRA-Zeitscheibe Mitte, Gewissheit nach
Regel G mit dem Wert Mitte. Das Produkt führt je Klimawirkung eine Gruppe und kennzeichnet sie mit „Mitte des
Jahrhunderts (2031–2060)“. Sie wechselt nicht mit dem Jahr der Zeitreihe:

- **2025–2030 und 2061–2065** zeigen dieselbe Gruppe mit derselben Kennzeichnung. Die KWRA hat für diese Jahre keine
  eigene Charakterisierung. Sie hat nur für 2020–2030 eine Einschätzung der beschlossenen Maßnahmen, und daraus bildet
  Kap. 6.2 keine Gruppe.
- **Die Regel „niedrigere Stufe“ für 2061–2070 gilt hier nicht.** Sie mischte die Gewissheit ohne Anpassung zum Ende
  mit der Gewissheit mit Anpassung zur Mitte, und diese Kombination hat die KWRA nicht bewertet.
- **Heutiges Klima (Euro-Betrag M0):** Die Gruppe ist keine Aussage über das heutige Klima. Sie steht neben dem Betrag
  nur mit der Kennzeichnung „Mitte des Jahrhunderts (2031–2060)“.

### Die Schwellen der Einordnung

**Was Kap. 6.2 festlegt.** Kap. 6.2 misst nicht an einer Minderung in Prozent. Es misst an einem Restrisiko auf der
Stufenskala der KWRA: „im optimistischen Fall ein gering-mittleres Restrisiko nicht überschritten werden soll“ und
„im pessimistischen Fall ein mittleres Restrisiko durch die Umsetzung von Anpassungsmaßnahmen angestrebt wird“
(S. 141). Die Vorgabe ist „normativ“ und „beispielhaft“ (S. 141). Die Zuordnung „reagiert in hohem Maße sensitiv auf
Änderungen des akzeptierten Restrisikos“ (S. 143). Eine Schwelle als Zahl nennt Kap. 6.2 nicht. **Beide Schwellen
bleiben deshalb Abschätzungen von KAP3.** Ihre Begründung steht hier und nicht nur im Code (P1).

**Die Brücke von der Stufe zur Zahl** steht in Kap. 5.1, auf das Kap. 6.2 verweist: „Der Wert ‚gering‘ würde das
angenommene Klimarisiko ohne Anpassung nicht reduzieren, ‚gering-mittel‘ würde eine Reduzierung um eine halbe Stufe
bedeuten, ‚mittel‘ um eine Stufe und so weiter“ (S. 112). Die fünf Wirksamkeitsstufen gering, gering-mittel, mittel,
mittel-hoch und hoch mindern also um 0, ½, 1, 1½ und 2 Risikostufen. Zwei Stufen führen von „hoch“ bis „gering“ und
sind die größte Minderung, die die Skala ausdrücken kann. **Abschätzung von KAP3:** Diese Skala wird linear auf die
relative Minderung 0–1 des Produkts gelegt. Dann gilt: gering 0, gering-mittel 0,25, mittel 0,5, mittel-hoch 0,75,
hoch 1,0.

| Schwelle | Wert | Band | Urteil | Art |
|---|---|---|---|---|
| Umsetzung (`SCHWELLE_UMSETZUNG`) | 0,5 | 0,33–0,5 (bisher 0,4–0,6) | Wert beibehalten, Band ersetzt | Abschätzung von KAP3; gilt nur, wenn der Eingang die beschlossenen Maßnahmen misst |
| Entwicklung (`SCHWELLE_ENTWICKLUNG`) | 0,1 | 0,05–0,2 | beibehalten, von Kap. 6.2 nicht gestützt | Abschätzung von KAP3; gilt nur, wenn der Eingang die beschlossenen Maßnahmen misst |

**Welchen Maßnahmenraum die Schwellen voraussetzen.** Die KWRA stellt ihre zwei Fragen an zwei verschiedene
Maßnahmenräume. „Umsetzung“ fragt, ob die *beschlossenen* Maßnahmen das Ziel erreichen. „Entwicklung“ gegen
„Innovation“ fragt, ob die *weiterreichende* Anpassung es erreicht (S. 140–141, S. 143; TB1 S. 93). Die Mappe führt
beide Räume getrennt: Spalte Y „Wirksamkeit APA III – Mitte pessim.“ und Spalte AA „Wirksamkeit weiterr. – Mitte
pessim.“. Das Produkt hat einen Eingang, das Anpassungspotenzial aus dem Katalog. Welchem Raum er entspricht, legt
T-1111-ceo fest, nicht diese Datei. Hinweis dafür: Die beschlossenen Maßnahmen „liegen fast nur in der Zuständigkeit des
Bundes“, bei der weiterreichenden Anpassung „werden auch andere Akteure als diejenigen auf Bundesebene berücksichtigt“
(S. 112). Beide Schwellen dieser Datei gelten deshalb nur unter einer Bedingung: **Der Eingang des Produkts misst
dieselbe Frage wie die beschlossenen Maßnahmen.**

**Umsetzung 0,5: beibehalten, gemessen an den beschlossenen Maßnahmen.** Im pessimistischen Fall liegt das Risiko ohne
Anpassung bei den sehr dringenden Klimawirkungen meist auf „hoch“ (Tabelle 25, S. 138). Das Ziel „mittel“ (S. 141)
verlangt dann eine Stufe Minderung, also die Wirksamkeit „mittel“ = 0,5. Nachgerechnet an der Wirksamkeit der
**beschlossenen** Maßnahmen, Mitte, pessimistischer Fall (Mappe Spalte Y): Mit 0,5 trifft die Einordnung „Umsetzung“
bei allen 29 charakterisierten Klimawirkungen Tabelle 27. Das sind drei Klimawirkungen in „Umsetzung“ (#96,
Hochwasserschutzsysteme, Schiffbarkeit) und 26 außerhalb. An der weiterreichenden Anpassung (Spalte AA) gemessen
trifft dieselbe Schwelle nur 14 von 29. #95 und #98 haben dort „mittel“ (0,5) und stünden in „Umsetzung“, gegen
Tabelle 27. Die Gruppe „Umsetzung“ trägt im Produkt also nur, wenn sein Eingang die beschlossenen Maßnahmen misst.

**Band 0,33–0,5: ersetzt.** Das bisherige Band 0,4–0,6 reichte über 0,5 hinaus. Eine Schwelle über 0,5 verlangt mehr
als die eine Stufe, die Kap. 6.2 als Ziel setzt. Bei 0,6 fallen #96 und Schiffbarkeit aus „Umsetzung“ heraus (27
statt 29 Treffer), gegen Tabelle 27. Die untere Grenze 0,33 ist die zweite Lesart desselben Ziels. Liest man die drei
Risikostufen gering, mittel, hoch als 1, 2, 3, ist „hoch“ auf „mittel“ ein Drittel weniger. Diese Lesart behandelt eine
Rangskala wie Messwerte. Deshalb ist sie nur Bandgrenze und nicht Wert. Im ganzen Band 0,33–0,5 bleibt die Zuordnung
„Umsetzung“ gleich (29 von 29).

**Entwicklung 0,1: beibehalten als Abschätzung von KAP3, von Kap. 6.2 nicht gestützt.** Die Schwelle trennt im
Produkt „kein nennenswerter Hebel“ von „ein Hebel, der sich ausbauen lässt“. Auf der Wirksamkeitsskala liegt sie
zwischen „gering“ (0, „würde … nicht reduzieren“, S. 112) und „gering-mittel“ (0,25). Das ganze Band 0,05–0,2 liegt
in dieser Lücke und ordnet KWRA-Werte gleich ein. Das ist eine Setzung von KAP3. Die Frage der KWRA ist eine andere,
und an den beschlossenen Maßnahmen gemessen erklärt die Schwelle wenig: 0,1 an Spalte Y trifft 15 von 26
Klimawirkungen, und schon „alles ist Entwicklung“ träfe 14 von 26. Jede Schwelle über 0,25 an Spalte Y gibt 12
Treffer, weil dann alle 26 in „Innovation“ fallen, auch #95 und #98. Für M0 trifft 0,1 die Tabelle 27: #95 und #98
haben an Spalte Y „gering-mittel“ (0,25), also „Entwicklung“. #96 hat „mittel“ (0,5), also „Umsetzung“.

**Die Regel der KWRA für Entwicklung (Übergabe an T-1111-ceo).** Kap. 6.2 trennt „Entwicklung“ von „Innovation“
daran, ob die weiterreichende Anpassung das Ziel erreicht, also an der Wirksamkeit „mittel“ = 0,5 im weiterreichenden
Raum. Nachgerechnet an Spalte AA trifft diese Regel 25 von 26 Klimawirkungen der Tabelle 27. Der einzige Fehltreffer
ist ID 10 „Bodenerosion durch Wasser“. Dort steht in Spalte AA „mittel“, das Restrisiko nach weiterreichender
Anpassung bleibt aber „mittel-hoch“ (Tabelle 24, S. 128), und Tabelle 27 führt die Klimawirkung unter „Innovation
unter Unsicherheit“. Diese Regel ist nicht verworfen. Das Produkt kann sie erst anwenden, wenn sein Eingang einen
weiterreichenden Raum abbildet. Dann gilt auf diesem Raum 0,5 als Entwicklungsschwelle. Das entscheidet T-1111-ceo mit
der Definition des Anpassungspotenzials.

**Befund an der Quelle.** Der Text auf S. 142 nennt für „Umsetzung“ „vier Klimawirkungen aus unterschiedlichen
Handlungsfeldern“. Tabelle 27 auf derselben Seite zeigt drei. „Abiotischer Stress (Pflanzen)“ steht dort in
„Entwicklung“, und seine beschlossenen Maßnahmen lassen im pessimistischen Fall ein Restrisiko „hoch“ (Tabelle 24,
S. 128). Diese Datei rechnet mit der Tabelle.

### Wo Kap. 6.2 „mittel“ als ausreichende Gewissheit zählt

1. **Die Vorgabe (S. 141, dritter Spiegelstrich):** Die Ergebnisse beruhen auf der Vorgabe, dass „eine mittlere
   Gesamtgewissheit ausreicht, um nicht zu einer der beiden Gruppen ‚unter Unsicherheit‘ zu zählen“. Das ist die
   Stelle, die `charakterisierung.py` heute als „TB6 S. 141“ zitiert. Sie stimmt.
2. **Was „mittel“ dort heißt (S. 141):** „Den Skalenwerten der Einordung der Gewissheit (sehr gering, gering, mittel,
   hoch) wurden die Werte 0, 1, 2 und 3 zugeordnet. Erst ab einem Mittelwert von über 1,5 wurde die Gesamtgewissheit
   hier als ‚mittel‘ eingestuft.“
3. **Worauf sich „mittel“ bezieht (S. 141):** „Für die Betrachtung der Gewissheit wurde eine Gesamtgewissheit der
   Bewertungen abgeleitet, die sich aus der Kombination der Gewissheit der Bewertung des Klimarisikos ohne Anpassung
   sowie der Gewissheit der Bewertung der Anpassungskapazität ergibt.“ „Mittel“ gilt also für die Gesamtgewissheit.
   Die Gewissheit nach Regel G ist nur ihr erster Teil.
4. **Das Gegenstück in Gruppe III (S. 140):** Unter Unsicherheit fällt eine Klimawirkung, wenn „die Gewissheit bei der
   Bewertung des Restrisikos gering“ ist.
5. **Die Schwelle ist selbst gesetzt (S. 143):** Zählt schon ein Mittelwert „von über eins“, bleiben vier
   Klimawirkungen unter Unsicherheit. Werden die Gewissheiten „erst bei einer relativen hohen Gewissheit, das heißt ab
   mehr als 1,5, als ausreichend eingestuft“, „kommen … neun Klimawirkungen hinzu“. Nachgerechnet: dieselben vier
   Klimawirkungen (IDs 13, 19, 51, 55, wie auf S. 143 genannt) und neun weitere.
6. **Ausnahme (S. 141, Fußnote 28; S. 143, Fußnote 29):** „Ausnahmen in der Berechnung erfolgten bei Klimawirkungen,
   bei denen die beschlossenen Maßnahmen (APA III) ausschlaggebend für die Zuordnung waren“. Genannt sind #96 und
   „Belastung oder Versagen von Hochwasserschutzsystemen“. Beide stehen in „Umsetzung“, und „Umsetzung“ hat keine
   Variante „unter Unsicherheit“ (S. 140). Deshalb ändert die Ausnahme keine Gruppe. Worin die Ausnahme besteht, sagt
   die Methodik wörtlich. Die Gewissheit der Anpassungskapazität wurde „nur für die beschlossenen Maßnahmen und die
   weiterreichende Anpassung zusammen durchgeführt“. Deshalb wurden „alle Klimawirkungen, bei denen die beschlossenen
   Maßnahmen alleine ausreichten, die Zielwerte einzuhalten, nicht einer der Gruppen mit Unsicherheit zugeordnet“
   (TB1 Kap. 2.5, S. 93–94, PDF-Seiten 94–95). Das Produkt übernimmt diese Korrektur: „Umsetzung“ bekommt nie den
   Zusatz „unter Unsicherheit“, wie heute in `charakterisierung.py`.

**Die Regel für das Produkt (übernommen, TB6 S. 141; TB1 Kap. 2.5, S. 93–94):** Die Charakterisierung zählt die
Gewissheit als ausreichend, wenn die Gesamtgewissheit zur Mitte über 1,5 liegt („eine Gesamtgewissheit von > 1,5 als
‚mittel‘ eingestuft“, TB1 S. 93). Die Gesamtgewissheit ist der Mittelwert der Punkte (sehr gering 0, gering 1, mittel
2, hoch 3) aus zwei Teilen. Teil a) ist die Gewissheit nach Regel G, Wert Mitte (TB6 Tabelle 1, Mappe Spalte S). Teil
b) ist die Gewissheit der Einschätzung der Anpassungskapazität für die Mitte (TB1 S. 93). Ihr Wert je Klimawirkung
steht in TB6 Tabelle 24, S. 128–129, Spalte „Gewissheit der Bewertung (Klimarisiken mit Anpassung)“, „Mitte des
Jahrhunderts“. Dass diese Spalte Teil b) ist, bestätigt die Nachrechnung mit 26 von 26 Treffern. „Umsetzung“ bleibt
ohne Unsicherheitsvariante (Punkt 6). Die Mappe führt Teil b) nicht. Der Mittelwert ist die Regel der KWRA für eine
Ja-Nein-Frage, das Produkt zeigt ihn nicht als Stufe.

**Was die einfachere Rechnung verfälschen würde (§8 E3).** Die Gewissheit nach Regel G allein („mittel“ und „hoch“
reichen), wie `AUSREICHENDE_GEWISSHEIT` sie heute anwendet, trifft Tabelle 27 nur bei 18 von 26 Klimawirkungen. Acht
der 13 Klimawirkungen „unter Unsicherheit“ zeigte sie als hinreichend sicher. Bei M0 träfe es #96: Regel G gibt zur
Mitte „mittel“ (ausreichend), die Gesamtgewissheit ist (2 + 1) : 2 = 1,5 und damit nicht über 1,5, also nicht
ausreichend. Bei #95 ist sie (3 + 2) : 2 = 2,5 und bei #98 (2 + 2) : 2 = 2,0. Beide sind ausreichend.

**Ohne Wert in Tabelle 24.** Tabelle 24 hat einen Wert nur für die 33 Klimawirkungen, deren Anpassungskapazität die KWRA
analysiert hat (S. 112; Mappe Spalte V = „ja“). #95, #96 und #98 gehören dazu. Für alle übrigen Klimawirkungen gibt es
keine Gesamtgewissheit. **Abschätzung von KAP3:** Dann zählt die Gewissheit als nicht ausreichend, und die Gruppe
bekommt den Zusatz „unter Unsicherheit“, sofern sie nicht „Umsetzung“ ist. Begründung: Die Bedingung der KWRA verlangt
beide Teile. Mit Regel G allein wären 8 von 13 Fällen zu sicher dargestellt, wie oben gerechnet. Diese Setzung irrt
zur Vorsicht. Sie betrifft keine Klimawirkung von M0.

### Beispiel-Block

`einordnung_charakterisierung`, aus dem Stamm des Produkt-Repos ausführbar (am 25.09.2026 gelaufen, Ausgabe darunter).
Die Werte aus Tabelle 24 und Tabelle 27 stehen im Block, weil die Mappe sie nicht führt.

```python
# einordnung_charakterisierung — Kap. 6.2 an TB6 Tabelle 27 nachgerechnet
import openpyxl

PUNKTE = {"sehr gering": 0, "gering": 1, "mittel": 2, "hoch": 3}  # TB6 S. 141
# TB6 S. 112: je Stufe der Wirksamkeit eine halbe Risikostufe mehr Minderung; linear auf 0–1 (Abschätzung von KAP3)
WIRKSAMKEIT = {"gering": 0.0, "gering-mittel": 0.25, "mittel": 0.5, "mittel-hoch": 0.75, "hoch": 1.0}

ws = openpyxl.load_workbook("docs/KWAR/KWRA-2021_Klimawirkungen.xlsx", data_only=True)["Klimawirkungen"]
zeile = {ws.cell(r, 1).value: r for r in range(3, ws.max_row + 1)}
assert (ws["S2"].value, ws["T2"].value) == ("Gewissheit – Mitte", "Gewissheit – Ende")
assert ws["Y2"].value == "Wirksamkeit APA III – Mitte pessim."

# TB6 Tabelle 27, S. 142 (als Bild gelesen am 25.09.2026): KWRA-IDs je Gruppe
TAB27 = {
    "Umsetzung": (50, 71, 96),
    "Entwicklung": (21, 39, 44, 47, 53, 60, 62, 82, 95, 98),
    "Entwicklung unter Unsicherheit": (25, 7, 13, 11),
    "Innovation": (2, 35, 61),
    "Innovation unter Unsicherheit": (27, 28, 31, 30, 8, 10, 19, 55, 51),
}
gruppe = {i: g for g, ids in TAB27.items() for i in ids}
assert len(gruppe) == 29

# TB6 Tabelle 24, S. 128–129 (als Bild gelesen am 25.09.2026), „Gewissheit der Bewertung (Klimarisiken mit
# Anpassung)“, nicht in der Mappe. Erster Wert Spalte „Mitte des Jahrhunderts“, zweiter Spalte „2020–2031“.
g, m, h = "gering", "mittel", "hoch"
TAB24 = {
    2: (m, m), 7: (g, m), 8: (g, m), 10: (g, m), 11: (g, m), 13: (g, m), 19: (g, g), 21: (m, m), 25: (m, m),
    27: (g, m), 28: (g, m), 30: (g, m), 31: (g, m), 35: (g, m), 39: (m, m), 44: (m, m), 47: (m, h), 50: (g, m),
    51: (g, g), 53: (m, m), 55: (g, g), 60: (m, m), 61: (m, h), 62: (m, m), 71: (h, h), 82: (m, h), 95: (m, m),
    96: (g, g), 98: (m, m),
}


def gesamt(i, ohne="S", mit=0):
    """Gesamtgewissheit nach TB6 S. 141: Mittelwert der Punkte aus ohne und mit Anpassung."""
    return (PUNKTE[ws[f"{ohne}{zeile[i]}"].value] + PUNKTE[TAB24[i][mit]]) / 2


def treffer(ohne="S", mit=0, schwelle=1.5):
    """Wie viele der 26 Einträge außerhalb „Umsetzung“ bekommen die Unsicherheitsvariante wie Tabelle 27?"""
    return sum((gesamt(i, ohne, mit) > schwelle) == (not gr.endswith("Unsicherheit"))
               for i, gr in gruppe.items() if gr != "Umsetzung")


# (1) Zeitscheibe: nur Mitte und Mitte bilden Tabelle 27 nach
assert treffer("S", 0) == 26          # Tabelle 1 Mitte + Tabelle 24 Mitte
print("Treffer von 26 — Mitte/Mitte:", treffer("S", 0), "| Ende/Mitte:", treffer("T", 0),
      "| Mitte/2020–2031:", treffer("S", 1))

# (3) Gewissheit allein nach Regel G (Tabelle 1 Mitte, mittel und hoch reichen) statt Gesamtgewissheit
regel_g = sum((PUNKTE[ws[f"S{zeile[i]}"].value] >= 2) == (not gr.endswith("Unsicherheit"))
              for i, gr in gruppe.items() if gr != "Umsetzung")
print("Treffer von 26 — Regel G allein:", regel_g)

# (3) Empfindlichkeit S. 143: bei „über 1“ bleiben vier unter Unsicherheit, bei „über 1,5“ kommen neun hinzu
robust = sorted(i for i, gr in gruppe.items() if gr.endswith("Unsicherheit") and gesamt(i) <= 1)
assert robust == [13, 19, 51, 55]
assert sum(1 < gesamt(i) <= 1.5 for i, gr in gruppe.items() if gr.endswith("Unsicherheit")) == 9
print("Robust unter Unsicherheit (Mittelwert höchstens 1):", robust)

# M0: Gesamtgewissheit Mitte
m0 = {i: gesamt(i) for i in (95, 96, 98)}
assert m0 == {95: 2.5, 96: 1.5, 98: 2.0}
print("M0 Gesamtgewissheit Mitte:", m0, "| ausreichend:", {i: v > 1.5 for i, v in m0.items()})


# (2) Schwellen an der Wirksamkeit zur Mitte, pessimistischer Fall: Mappe Spalte Y = beschlossene Maßnahmen,
#     Spalte AA = weiterreichende Anpassung (die Frage, an der die KWRA Entwicklung von Innovation trennt)
assert ws["AA2"].value == "Wirksamkeit weiterr. – Mitte pessim."


def w(spalte, i):
    return WIRKSAMKEIT[ws[f"{spalte}{zeile[i]}"].value]


def umsetzung_treffer(schwelle, spalte="Y"):
    return sum((w(spalte, i) >= schwelle) == (gr == "Umsetzung") for i, gr in gruppe.items())


print("Umsetzung, Treffer von 29, an Y — 0,33:", umsetzung_treffer(0.33), "| 0,4:", umsetzung_treffer(0.4),
      "| 0,5:", umsetzung_treffer(0.5), "| 0,6:", umsetzung_treffer(0.6), "|| an AA — 0,5:", umsetzung_treffer(0.5, "AA"))
assert umsetzung_treffer(0.5) == 29 and umsetzung_treffer(0.6) == 27 and umsetzung_treffer(0.5, "AA") == 14
assert w("AA", 95) == w("AA", 98) == 0.5          # an AA gemessen stünden #95 und #98 in „Umsetzung“


def entwicklung_treffer(schwelle, spalte="Y"):
    return sum((w(spalte, i) >= schwelle) == gr.startswith("Entwicklung")
               for i, gr in gruppe.items() if gr != "Umsetzung")


alles_entwicklung = sum(gr.startswith("Entwicklung") for gr in gruppe.values())
fehl_aa = [i for i, gr in gruppe.items()
           if gr != "Umsetzung" and (w("AA", i) >= 0.5) != gr.startswith("Entwicklung")]
print("Entwicklung/Innovation, Treffer von 26, an Y — 0,05:", entwicklung_treffer(0.05), "| 0,1:",
      entwicklung_treffer(0.1), "| 0,2:", entwicklung_treffer(0.2), "| 0,3:", entwicklung_treffer(0.3),
      "| alles Entwicklung:", alles_entwicklung)
print("Entwicklung/Innovation, Treffer von 26, an AA — 0,5:", entwicklung_treffer(0.5, "AA"), "| Fehltreffer:", fehl_aa)
assert entwicklung_treffer(0.1) == 15 and alles_entwicklung == 14
assert entwicklung_treffer(0.5, "AA") == 25 and fehl_aa == [10]
```

Ausgabe:

```
Treffer von 26 — Mitte/Mitte: 26 | Ende/Mitte: 19 | Mitte/2020–2031: 18
Treffer von 26 — Regel G allein: 18
Robust unter Unsicherheit (Mittelwert höchstens 1): [13, 19, 51, 55]
M0 Gesamtgewissheit Mitte: {95: 2.5, 96: 1.5, 98: 2.0} | ausreichend: {95: True, 96: False, 98: True}
Umsetzung, Treffer von 29, an Y — 0,33: 29 | 0,4: 29 | 0,5: 29 | 0,6: 27 || an AA — 0,5: 14
Entwicklung/Innovation, Treffer von 26, an Y — 0,05: 15 | 0,1: 15 | 0,2: 15 | 0,3: 12 | alles Entwicklung: 14
Entwicklung/Innovation, Treffer von 26, an AA — 0,5: 25 | Fehltreffer: [10]
```

## Folgegrößen

- **Gruppen der Charakterisierung (Konformitätszeile 7, `backend/app/services/charakterisierung.py`):** Sie setzen
  auf der Gesamtgewissheit der KWRA auf, die Kap. 6.2 „aus der Kombination der Gewissheit der Bewertung des
  Klimarisikos ohne Anpassung sowie der Gewissheit der Bewertung der Anpassungskapazität“ bildet (TB6 S. 141), deren
  erster Teil die Gewissheit nach Regel G ist und nicht die Quellenlage, weil die Gruppen „unter Unsicherheit“ fragen,
  wie sicher die Aussage über Risiko und Anpassung ist, und nicht, ob die Rechnung von KAP3 Quellen hat. Nach Schritt 2
  gilt: Die Gruppen setzen auf der Gesamtgewissheit zur Mitte des Jahrhunderts auf, dem Mittelwert aus Regel G (Wert
  Mitte) und TB6 Tabelle 24 (Spalte Mitte). Ausreichend ist ein Mittelwert über 1,5. Ohne Wert in Tabelle 24 zählt die
  Gewissheit als nicht ausreichend. Die Schwellen 0,5 und 0,1 gelten nur, wenn der Eingang des Produkts die
  beschlossenen Maßnahmen misst; das klärt T-1111-ceo. Einzelheiten stehen unter „Einordnung der Charakterisierung“.
  Grund: Kap. 6.2 und TB1 Kap. 2.5 bilden die Gesamtgewissheit so (TB6 S. 141; TB1 S. 93). Die Gewissheit nach Regel G
  allein trifft Tabelle 27 nur 18-mal von 26.
- **Hinweis zur vorsichtigen Interpretation (Zeile 19, `backend/app/services/unsicherheits_zusammenschau.py`):** Er
  setzt auf der Gewissheit nach Regel G auf, je Zeitscheibe, weil Kap. 3.3 genau diesen Zweck nennt, nämlich
  Klimawirkungen zu zeigen, „bei denen die ermittelten Klimarisiken noch hohen Unsicherheiten unterliegen und daher
  vorsichtig interpretiert werden sollten“ (TB6 S. 78), und das eine Aussage über das Klimarisiko ist, nicht über die
  Quellenlage der Rechnung.

## Rechenkette

Format nach Aufgabe §4, hier „Zelle → Stufe“ statt „Zahl × Faktor“, weil Regel G übernimmt und nicht rechnet. Es gibt
keinen Euro-Betrag am Ende: Die Gewissheit steht neben dem Betrag und ändert ihn nicht. Beispiele: #95 Hitzebelastung
(Schritt 1), #96 Aeroallergene (Schritt 3) und #98 UV-Schädigungen (Schritt 4), die beiden letzten unten, alle in
denselben zehn Ebenen.

| Ebene | Rechenschritt | Wert (#95 Hitzebelastung) | Quelle |
|---|---|---|---|
| 1 | Risikocodes des Produkts → Klimawirkung der KWRA | `EXPECTED_ANNUAL_MORTALITY`, `EXPECTED_ANNUAL_MORBIDITY` → „Hitzebelastung“, KWRA-ID 95 | Bericht 95; Konformitätsliste, „Gegenprobe Zeile 8“ |
| 2 | KWRA-ID → Zeile der Mappe (Spalte A = 95) | Zeile 97; D97 = „Hitzebelastung“ | Mappe, Blatt „Klimawirkungen“, A97, D97 |
| 3 | Zelle S97 (Kopf S2 „Gewissheit – Mitte“) → Stufe Mitte | **hoch** | Mappe S97; gleichlautend TB6 Tabelle 1, S. 41 |
| 4 | Zelle T97 (Kopf T2 „Gewissheit – Ende“) → Stufe Ende | **mittel** | Mappe T97; gleichlautend TB6 Tabelle 1, S. 41 |
| 5 | Heutiges Klima (Euro-Betrag M0) → Gewissheit | „in der KWRA nicht ausgewiesen“ | TB6 Tabelle 1 (keine Spalte Gegenwart); Zuordnungstabelle |
| 6 | Jahre 2025–2060 der Zeitreihe → Stufe Mitte | hoch | Zuordnungstabelle; Ebene 3 |
| 7 | Jahre 2061–2065 der Zeitreihe → niedrigere Stufe von Mitte und Ende | niedrigere von hoch und mittel = mittel | Zuordnungstabelle; Ebenen 3 und 4 |
| 8 | Jahre 2071–2100 → Stufe Ende (heute nicht im Produkt) | mittel | Zuordnungstabelle; Ebene 4 |
| 9 | Beide Codes aus Ebene 1 → dieselbe Stufe je Zeitscheibe | Sterbefälle und Einweisungen: Mitte hoch, Ende mittel | Regel G, „Ein Wert je Klimawirkung“ |
| 10 | Stufe → Vorsichtshinweis (ab „gering“, `VORSICHT_STUFEN`) | Mitte hoch, Ende mittel: kein Hinweis für #95 | `unsicherheits_zusammenschau.py`; Folgegrößen |

Zum Vergleich, geht **nicht** in die Gewissheit ein: die Quellenlage aus dem Endstand der Parameter-Blöcke von
`docs/methodik/95_hitzebelastung.md` (Kap. 7; Stand Commit `b0f3ad9a` vom 06.10.2026, T-1791-ceo). Gezählt: 30 Blöcke,
davon 10 mit Kennzeichnung `quelle`, 17 `abschaetzung_kap3`, 3 `berechnet`. Das sind 10 von 30 = 33 % mit Quelle, mit
den berechneten 13 von 30 = 43 %. Nach der alten Regel (ab der Hälfte „mittel“, darunter „gering“) stünde #95 damit in
beiden Zählweisen auf „gering“ (beide Anteile unter 0,5). Die Registry des Produkts, nach derselben Regel gezählt, kommt
heute für die Sterbefälle mit 17 von 38 Parametern (45 %) und für die Krankenhauseinweisungen mit 3 von 9 (33 %)
ebenfalls zu „gering“. Die KWRA sagt zur Mitte „hoch“. Dieselbe Rechnung landet also in allen vier Zählweisen zwei
Stufen unter der KWRA. Am 27.09.2026 lag sie mit 23 Blöcken und 32 Registry-Parametern noch je nach Zählweise auf
„gering“ oder „mittel“. Die Stufe wandert mit der Zahl der Blöcke, nicht mit dem Wissen über Hitze. Das ist der Grund,
warum die Zählung keine Gewissheit ist.

Beispiel-Block `rechenkette_gewissheit_95`, aus dem Stamm des Produkt-Repos ausführbar (am 07.10.2026 gelaufen,
Ausgabe darunter). Er zählt die Blöcke in Bericht 95 und die Parameter der Registry selbst nach:

```python
# rechenkette_gewissheit_95 — Regel G an #95 nachgerechnet
import re
import openpyxl

STUFEN = ("sehr gering", "gering", "mittel", "hoch")  # TB6 S. 78, aufsteigend

ws = openpyxl.load_workbook("docs/KWAR/KWRA-2021_Klimawirkungen.xlsx", data_only=True)["Klimawirkungen"]

# Ebene 2: Zeile der Klimawirkung über die KWRA-ID in Spalte A
zeile = next(r for r in range(3, ws.max_row + 1) if ws.cell(r, 1).value == 95)
assert zeile == 97 and ws["D97"].value == "Hitzebelastung"

# Ebenen 3 und 4: Kopfzellen, Werte, Quellvermerk
assert (ws["S2"].value, ws["T2"].value) == ("Gewissheit – Mitte", "Gewissheit – Ende")
mitte, ende = ws["S97"].value, ws["T97"].value
assert (mitte, ende) == ("hoch", "mittel")
assert ws["AJ97"].value.startswith("TB 6 Tab. 1")


def gewissheit(jahr):
    """Ebenen 6 bis 8: Jahr der Zeitreihe → Stufe nach der Zuordnungstabelle."""
    if jahr <= 2060:
        return mitte
    if jahr <= 2070:
        return min(mitte, ende, key=STUFEN.index)
    return ende


HEUTIGES_KLIMA = "in der KWRA nicht ausgewiesen"  # Ebene 5
zeitreihe = {j: gewissheit(j) for j in range(2025, 2066)}  # Produkt: 2025–2065
assert all(zeitreihe[j] == "hoch" for j in range(2025, 2061))
assert all(zeitreihe[j] == "mittel" for j in range(2061, 2066))
assert all(gewissheit(j) == "mittel" for j in range(2071, 2101))

# Ebene 9: ein Wert je Klimawirkung, beide Codes von #95 gleich
codes = ("EXPECTED_ANNUAL_MORTALITY", "EXPECTED_ANNUAL_MORBIDITY")
je_code = {c: (mitte, ende) for c in codes}
assert set(je_code.values()) == {("hoch", "mittel")}

# Ebene 10: Vorsichtshinweis ab „gering“
VORSICHT_STUFEN = ("sehr gering", "gering")
assert mitte not in VORSICHT_STUFEN and ende not in VORSICHT_STUFEN

# Vergleich, geht nicht in die Gewissheit ein: Quellenlage aus dem Endstand der Parameter-Blöcke
text = open("docs/methodik/95_hitzebelastung.md", encoding="utf-8").read()
kap7 = text.split("## 7 Parameter-Blöcke", 1)[1].split("\n## ", 1)[0]
kz = re.findall(r"^\s*kennzeichnung:\s*(\w+)", kap7, flags=re.M)
zaehlung = {k: kz.count(k) for k in sorted(set(kz))}
assert len(kz) == len(re.findall(r"^parameter:", kap7, flags=re.M)) == 30
assert zaehlung == {"abschaetzung_kap3": 17, "berechnet": 3, "quelle": 10}
assert round(10 / 30, 2) == 0.33 and round(13 / 30, 2) == 0.43


def alte_regel(anteil):
    """Alte Kennzahl (backend/app/services/gewissheit.py): Stufe aus dem Anteil belegter Parameter."""
    return "sehr gering" if anteil == 0 else "gering" if anteil < 0.5 else "mittel" if anteil < 1 else "hoch"


assert (alte_regel(10 / 30), alte_regel(13 / 30)) == ("gering", "gering")

# Vergleich, Registry des Produkts nach derselben alten Regel (belegt oder berechnet zählt als belegt)
import sys
sys.path.insert(0, "backend")
from app.services import gewissheit as alt, parameter_registry  # noqa: E402

registry = {}
for c in codes:
    klassen = [p["evidence_class"] for p in alt._risiko_parameter(c)]
    registry[c] = (sum(k in parameter_registry.BELEGTE_KLASSEN for k in klassen), len(klassen))
assert registry == {"EXPECTED_ANNUAL_MORTALITY": (17, 38), "EXPECTED_ANNUAL_MORBIDITY": (3, 9)}
assert (alt.gewissheitsstufe(codes[0]), alt.gewissheitsstufe(codes[1])) == ("gering", "gering")
assert (alte_regel(17 / 38), alte_regel(3 / 9)) == ("gering", "gering")

print("Mitte:", mitte, "| Ende:", ende, "| heutiges Klima:", HEUTIGES_KLIMA)
print("2025:", zeitreihe[2025], "| 2060:", zeitreihe[2060], "| 2061:", zeitreihe[2061], "| 2065:", zeitreihe[2065])
print("Quellenlage Bericht (nur Vergleich):", zaehlung, "| Blöcke:", len(kz))
print("Registry belegt/alle (nur Vergleich):", registry)
```

Ausgabe:

```
Mitte: hoch | Ende: mittel | heutiges Klima: in der KWRA nicht ausgewiesen
2025: hoch | 2060: hoch | 2061: mittel | 2065: mittel
Quellenlage Bericht (nur Vergleich): {'abschaetzung_kap3': 17, 'berechnet': 3, 'quelle': 10} | Blöcke: 30
Registry belegt/alle (nur Vergleich): {'EXPECTED_ANNUAL_MORTALITY': (17, 38), 'EXPECTED_ANNUAL_MORBIDITY': (3, 9)}
```

### #96 Aeroallergene (Schritt 3)

Schritt 3, Ticket T-1174-methodik_manager. Gerechnet mit dem Endstand von Bericht 96 nach T-1114-cmo (Status
„fertig“; letzte Änderung am Bericht in Commit `f87bc789`, T-1427-methodik_manager). Dieselben zehn Ebenen wie #95,
Regel G unverändert.

| Ebene | Rechenschritt | Wert (#96 Aeroallergene) | Quelle |
|---|---|---|---|
| 1 | Risikocode des Produkts → Klimawirkung der KWRA | `EXPECTED_ANNUAL_ALLERGY_DAYS` → „Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft“, KWRA-ID 96 | Bericht 96; Konformitätsliste, „Gegenprobe Zeile 8“ |
| 2 | KWRA-ID → Zeile der Mappe (Spalte A = 96) | Zeile 98; D98 = „Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft“ | Mappe, Blatt „Klimawirkungen“, A98, D98 |
| 3 | Zelle S98 (Kopf S2 „Gewissheit – Mitte“) → Stufe Mitte | **mittel** | Mappe S98; gleichlautend TB6 Tabelle 1, S. 41 (als Bild gelesen am 26.09.2026) |
| 4 | Zelle T98 (Kopf T2 „Gewissheit – Ende“) → Stufe Ende | **mittel** | Mappe T98; gleichlautend TB6 Tabelle 1, S. 41 |
| 5 | Heutiges Klima (Euro-Betrag M0) → Gewissheit | „in der KWRA nicht ausgewiesen“ | TB6 Tabelle 1 (keine Spalte Gegenwart); Zuordnungstabelle |
| 6 | Jahre 2025–2060 der Zeitreihe → Stufe Mitte | mittel | Zuordnungstabelle; Ebene 3 |
| 7 | Jahre 2061–2065 der Zeitreihe → niedrigere Stufe von Mitte und Ende | niedrigere von mittel und mittel = mittel | Zuordnungstabelle; Ebenen 3 und 4 |
| 8 | Jahre 2071–2100 → Stufe Ende (heute nicht im Produkt) | mittel | Zuordnungstabelle; Ebene 4 |
| 9 | Alle Codes aus Ebene 1 → dieselbe Stufe je Zeitscheibe | ein Code, Allergietage: Mitte mittel, Ende mittel | Regel G, „Ein Wert je Klimawirkung“ |
| 10 | Stufe → Vorsichtshinweis (ab „gering“, `VORSICHT_STUFEN`) | Mitte mittel, Ende mittel: kein Hinweis für #96 | `unsicherheits_zusammenschau.py`; Folgegrößen |

Bei #96 sind Mitte und Ende gleich. Die Regel „niedrigere Stufe“ für 2061–2070 ändert deshalb nichts, und die ganze
Zeitreihe 2025–2065 zeigt „mittel“. Den Ausschlag geben allein die Zellen S98 und T98.

**Einordnung nach „Einordnung der Charakterisierung“ (Zeitscheibe Mitte).**

| Schritt | Rechnung | Ergebnis | Quelle |
|---|---|---|---|
| Teil a) der Gesamtgewissheit | Regel G, Wert Mitte = mittel | 2 Punkte | Mappe S98; TB6 S. 141 (Punkte) |
| Teil b) der Gesamtgewissheit | Gewissheit mit Anpassung, Mitte = gering | 1 Punkt | TB6 Tabelle 24, S. 128–129 (als Bild gelesen am 25.09.2026, Block `einordnung_charakterisierung`); Mappe V98 = „ja“ |
| Gesamtgewissheit | (2 + 1) : 2 | 1,5, nicht über 1,5: nicht ausreichend | TB6 S. 141; TB1 S. 93 |
| Gruppe | Wirksamkeit der beschlossenen Maßnahmen, Mitte, pessimistisch = mittel = 0,5; Schwelle Umsetzung 0,5 | „Umsetzung“, wie TB6 Tabelle 27, S. 142 | Mappe Y98; Schwelle als Abschätzung von KAP3 |
| Zusatz „unter Unsicherheit“ | „Umsetzung“ hat keine Variante unter Unsicherheit; #96 ist die Ausnahme aus Fußnote 28 und 29 | kein Zusatz, trotz Gesamtgewissheit 1,5 | TB6 S. 140, S. 141, S. 143; TB1 S. 93–94 |
| Kennzeichnung | eine Gruppe je Klimawirkung, gleich für alle Jahre der Zeitreihe und neben dem Betrag M0 | „Mitte des Jahrhunderts (2031–2060)“ | Abschnitt „Zuordnung zur Zeitscheibe des Produkts“ |

- **Die Bedingung an den Maßnahmenraum trifft #96 nicht.** Die weiterreichende Anpassung hat ebenfalls „mittel“ = 0,5
  (Mappe AA98). Die Gruppe „Umsetzung“ folgt also an Spalte Y wie an Spalte AA.
- **Was die einfachere Rechnung verfälschen würde (§8 E3).** In der Gruppe „Umsetzung“ unterscheiden sich Regel G
  allein und Gesamtgewissheit bei #96 nicht, weil „Umsetzung“ keinen Zusatz trägt. Sichtbar wird der Unterschied, sobald
  der Eingang des Produkts unter 0,5 liegt. Heute liegt er bei 0, weil keine Maßnahme im Rechenweg wirkt
  (Konformitätsliste, Zeile 7 und A10). Mit Regel G allein zeigt das Produkt dann „Innovation“ ohne Zusatz. Mit der
  Gesamtgewissheit zeigt es „Innovation unter Unsicherheit“ (0 liegt unter der Entwicklungsschwelle 0,1). Die Gruppe der
  KWRA, „Umsetzung“, erreicht das Produkt erst, wenn sein Eingang die beschlossenen Maßnahmen mit mindestens 0,5
  abbildet. Das entscheidet T-1111-ceo.

Zum Vergleich, geht **nicht** in die Gewissheit ein: die Quellenlage aus dem Endstand der Parameter-Blöcke von
`docs/methodik/96_aeroallergene.md` (Kap. 7; am 07.10.2026 nachgezogen auf den abgenommenen Stand, Commit `c0486100`
vom 30.09.2026, T-1640-methodik_manager). Gezählt: 14 Blöcke, davon 3 mit Kennzeichnung `quelle`
(`pollen.delta_s_region`, `pollen.p_ar`, `pollen.c_jahr_direkt`), 9 `abschaetzung_kap3` (`pollen.a_attr`,
`pollen.p_sens_gruppen`, `pollen.l_saison`, `pollen.f_symptomtage`, `pollen.lambda_veg`, `pollen.s_unbekannt`,
`pollen.r_s158`, `pollen.t_warn_s158`, `pollen.stadtbaum_kosten`) und 2 `berechnet` (`pollen.d_saison`,
`pollen.c_tag`). Das sind 3 von 14 = 21 % mit Quelle, mit den berechneten 5 von 14 = 36 %. Nach der alten Regel stünde
#96 in beiden Zählweisen auf „gering“ (unter 0,5). Die Registry kommt heute mit 15 von 24 Parametern (63 %) zu
„mittel“, nachgerechnet im Block; die Konformitätsliste („Gegenprobe Zeile 8“) nennt noch den älteren Stand 20 von 21.
Die KWRA sagt zur Mitte und zum Ende „mittel“. Dass Registry und KWRA hier gleich lauten, liegt an der Zerlegung: Aus
den Blöcken des Berichts ergibt dieselbe alte Regel „gering“. Drei der 14 Blöcke wirken nicht auf den Schadensbetrag:
`pollen.r_s158` und `pollen.t_warn_s158` nur im Maßnahmen-Modul, `pollen.stadtbaum_kosten` nur bei den Kosten einer
Maßnahme. Ohne sie wären es 3 von 11 = 27 %, ebenfalls unter 0,5. Regel G zählt jeden Block einmal, also 14.

Beispiel-Block `rechenkette_gewissheit_96`, aus dem Stamm des Produkt-Repos ausführbar (am 07.10.2026 gelaufen,
Ausgabe darunter):

```python
# rechenkette_gewissheit_96 — Regel G an #96 nachgerechnet, dieselben Ebenen wie #95
import re
import openpyxl

STUFEN = ("sehr gering", "gering", "mittel", "hoch")  # TB6 S. 78, aufsteigend
PUNKTE = {"sehr gering": 0, "gering": 1, "mittel": 2, "hoch": 3}  # TB6 S. 141
WIRKSAMKEIT = {"gering": 0.0, "gering-mittel": 0.25, "mittel": 0.5, "mittel-hoch": 0.75, "hoch": 1.0}  # S. 112

ws = openpyxl.load_workbook("docs/KWAR/KWRA-2021_Klimawirkungen.xlsx", data_only=True)["Klimawirkungen"]

# Ebene 2: Zeile der Klimawirkung über die KWRA-ID in Spalte A
zeile = next(r for r in range(3, ws.max_row + 1) if ws.cell(r, 1).value == 96)
assert zeile == 98
assert ws["D98"].value == "Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft"

# Ebenen 3 und 4: Kopfzellen, Werte, Quellvermerk
assert (ws["S2"].value, ws["T2"].value) == ("Gewissheit – Mitte", "Gewissheit – Ende")
mitte, ende = ws["S98"].value, ws["T98"].value
assert (mitte, ende) == ("mittel", "mittel")
assert ws["AJ98"].value.startswith("TB 6 Tab. 1")


def gewissheit(jahr):
    """Ebenen 6 bis 8: Jahr der Zeitreihe → Stufe nach der Zuordnungstabelle."""
    if jahr <= 2060:
        return mitte
    if jahr <= 2070:
        return min(mitte, ende, key=STUFEN.index)
    return ende


HEUTIGES_KLIMA = "in der KWRA nicht ausgewiesen"  # Ebene 5
zeitreihe = {j: gewissheit(j) for j in range(2025, 2066)}  # Produkt: 2025–2065
assert all(zeitreihe[j] == "mittel" for j in range(2025, 2066))
assert gewissheit(2085) == "mittel"

# Ebene 9: ein Wert je Klimawirkung; #96 hat einen Code
codes = ("EXPECTED_ANNUAL_ALLERGY_DAYS",)
je_code = {c: (mitte, ende) for c in codes}
assert set(je_code.values()) == {("mittel", "mittel")}

# Ebene 10: Vorsichtshinweis ab „gering“
VORSICHT_STUFEN = ("sehr gering", "gering")
assert mitte not in VORSICHT_STUFEN and ende not in VORSICHT_STUFEN

# Einordnung der Charakterisierung (Zeitscheibe Mitte): Gesamtgewissheit und Gruppe
TAB24_MITTE_96 = "gering"  # TB6 Tabelle 24, S. 128–129, „Gewissheit der Bewertung (Klimarisiken mit Anpassung)“, Mitte
gesamt = (PUNKTE[mitte] + PUNKTE[TAB24_MITTE_96]) / 2
assert gesamt == 1.5 and not gesamt > 1.5          # nicht ausreichend
assert ws["V98"].value == "ja"                       # Anpassungskapazität analysiert, Tabelle 24 hat einen Wert
assert ws["Y2"].value == "Wirksamkeit APA III – Mitte pessim."
assert ws["AA2"].value == "Wirksamkeit weiterr. – Mitte pessim."
w_y, w_aa = WIRKSAMKEIT[ws["Y98"].value], WIRKSAMKEIT[ws["AA98"].value]
assert w_y == w_aa == 0.5
SCHWELLE_UMSETZUNG = 0.5  # Abschätzung von KAP3, Band 0,33–0,5
gruppe = "Umsetzung" if w_y >= SCHWELLE_UMSETZUNG else "(nicht Umsetzung)"
assert gruppe == "Umsetzung"                         # wie TB6 Tabelle 27, S. 142; kein Zusatz (S. 140)

# Vergleich, geht nicht in die Gewissheit ein: Quellenlage aus dem Endstand der Parameter-Blöcke
text = open("docs/methodik/96_aeroallergene.md", encoding="utf-8").read()
kap7 = text.split("## 7 Parameter-Blöcke", 1)[1].split("\n## ", 1)[0]
kz = re.findall(r"^\s*kennzeichnung:\s*(\w+)", kap7, flags=re.M)
zaehlung = {k: kz.count(k) for k in sorted(set(kz))}
assert len(kz) == len(re.findall(r"^parameter:", kap7, flags=re.M)) == 14
assert zaehlung == {"abschaetzung_kap3": 9, "berechnet": 2, "quelle": 3}
assert round(3 / 14, 2) == 0.21 and round(5 / 14, 2) == 0.36 and round(3 / 11, 2) == 0.27

# Vergleich, Registry des Produkts nach der alten Regel (belegt oder berechnet zählt als belegt)
import sys
sys.path.insert(0, "backend")
from app.services import gewissheit as alt, parameter_registry  # noqa: E402

klassen = [p["evidence_class"] for p in alt._risiko_parameter(codes[0])]
registry = (sum(k in parameter_registry.BELEGTE_KLASSEN for k in klassen), len(klassen))
assert registry == (15, 24) and alt.gewissheitsstufe(codes[0]) == "mittel"

print("Mitte:", mitte, "| Ende:", ende, "| heutiges Klima:", HEUTIGES_KLIMA)
print("2025:", zeitreihe[2025], "| 2060:", zeitreihe[2060], "| 2061:", zeitreihe[2061], "| 2065:", zeitreihe[2065])
print("Gesamtgewissheit Mitte:", gesamt, "| ausreichend:", gesamt > 1.5, "| Gruppe:", gruppe,
      "| Wirksamkeit Y/AA:", w_y, w_aa)
print("Quellenlage (nur Vergleich):", zaehlung, "| Registry belegt/alle (nur Vergleich):", registry)
```

Ausgabe:

```
Mitte: mittel | Ende: mittel | heutiges Klima: in der KWRA nicht ausgewiesen
2025: mittel | 2060: mittel | 2061: mittel | 2065: mittel
Gesamtgewissheit Mitte: 1.5 | ausreichend: False | Gruppe: Umsetzung | Wirksamkeit Y/AA: 0.5 0.5
Quellenlage (nur Vergleich): {'abschaetzung_kap3': 9, 'berechnet': 2, 'quelle': 3} | Registry belegt/alle (nur Vergleich): (15, 24)
```

### #98 UV-Schädigungen (Schritt 4)

Schritt 4, Ticket T-1175-methodik_manager. Gerechnet mit dem Endstand von Bericht 98 nach T-1115-cmo (Status
„fertig“; Rev. 15 vom 05.10.2026, letzte Änderung am Bericht in Commit `5a59ef3b`, T-1728-methodik_manager).
Dieselben zehn Ebenen wie #95 und #96, Regel G unverändert.

| Ebene | Rechenschritt | Wert (#98 UV-Schädigungen) | Quelle |
|---|---|---|---|
| 1 | Risikocode des Produkts → Klimawirkung der KWRA | `EXPECTED_ANNUAL_UV_YLL` → „UV-bedingte Gesundheitsschädigungen (insbesondere Hautkrebs)“, KWRA-ID 98 | Bericht 98; Konformitätsliste, „Gegenprobe Zeile 8“ |
| 2 | KWRA-ID → Zeile der Mappe (Spalte A = 98) | Zeile 100; D100 = „UV-bedingte Gesundheitsschädigungen (insbesondere Hautkrebs)“ | Mappe, Blatt „Klimawirkungen“, A100, D100 |
| 3 | Zelle S100 (Kopf S2 „Gewissheit – Mitte“) → Stufe Mitte | **mittel** | Mappe S100; gleichlautend TB6 Tabelle 1, S. 41 (als Bild gelesen am 07.10.2026) |
| 4 | Zelle T100 (Kopf T2 „Gewissheit – Ende“) → Stufe Ende | **sehr gering** | Mappe T100; gleichlautend TB6 Tabelle 1, S. 41; TB6 S. 78 nennt „UV-bedingte Gesundheitsschädigungen“ unter den sieben Klimawirkungen mit „sehr gering“ zum Ende |
| 5 | Heutiges Klima (Euro-Betrag M0) → Gewissheit | „in der KWRA nicht ausgewiesen“ | TB6 Tabelle 1 (keine Spalte Gegenwart); Zuordnungstabelle |
| 6 | Jahre 2025–2060 der Zeitreihe → Stufe Mitte | mittel | Zuordnungstabelle; Ebene 3 |
| 7 | Jahre 2061–2065 der Zeitreihe → niedrigere Stufe von Mitte und Ende | niedrigere von mittel und sehr gering = sehr gering | Zuordnungstabelle; Ebenen 3 und 4 |
| 8 | Jahre 2071–2100 → Stufe Ende (heute nicht im Produkt) | sehr gering | Zuordnungstabelle; Ebene 4 |
| 9 | Alle Codes aus Ebene 1 → dieselbe Stufe je Zeitscheibe | ein Code, verlorene Lebensjahre: Mitte mittel, Ende sehr gering | Regel G, „Ein Wert je Klimawirkung“ |
| 10 | Stufe → Vorsichtshinweis (ab „gering“, `VORSICHT_STUFEN`) | Mitte mittel: kein Hinweis; Ende sehr gering: Hinweis, in der Zeitreihe ab 2061 | `unsicherheits_zusammenschau.py`; Folgegrößen |

Bei #98 liegen Mitte und Ende zwei Stufen auseinander. Hier wirkt die Regel „niedrigere Stufe“ für 2061–2070 zum
ersten Mal: Die Zeitreihe zeigt 2025–2060 „mittel“ und 2061–2065 „sehr gering“. Den Ausschlag geben die Zellen S100 und
T100.

**Wie Regel G das Auseinanderfallen von Produktstufe und KWRA-Stufe ausweist (§8 E3).** Die heutige Kennzahl des
Produkts (`gewissheit.gewissheitsstufe`) stand für #98 bis T-1820-cto auf „hoch“. Alle 30 Parameter der Registry galten
als belegt, gemessen am 07.10.2026 am Stand davor (Commit `22f532d3`). Seit T-1820-cto (Commit `c8aba66f`, 07.10.2026)
übernimmt die Registry die Kennzeichnung der Blöcke aus Kapitel 7 von Bericht 98 (`_UV_BLOECKE` und `_UV_KLASSE` in
`backend/app/services/engine/impact/params.py`). Seitdem zählt sie 22 von 30 Parametern als belegt oder berechnet
(73 %) und meldet „mittel“, im Block nachgerechnet. Die KWRA nennt zum Ende „sehr gering“: Die Kennzahl lag vorher drei
Stufen darüber, jetzt zwei. Regel G weist das Auseinanderfallen in beiden Fällen gleich aus. Als Gewissheit zeigt das
Produkt nicht mehr die Kennzahl, sondern je Zeitscheibe den Wert der KWRA: Mitte „mittel“, Ende „sehr gering“, je mit
Fundstelle Mappe S100 und T100 und TB6 Tabelle 1, S. 41. Die Zeitreihe zeigt ab 2061 „sehr gering“ mit dem Hinweis zur
vorsichtigen Interpretation. Die Quellenlage steht daneben nur als Zählung, „5 von 22 Parametern mit Quelle“, ohne
Stufe. So steht weder ein „hoch“ noch ein „mittel“ ohne Zeitbezug neben dem „sehr gering“.

**Das „mittel“ der Kennzahl trifft die KWRA zur Mitte nur zufällig.** Es folgt aus einem Anteil über der Hälfte, nicht
aus einer Bewertung der Gewissheit. An einem Tag ist es ohne neues Wissen über UV von „hoch“ auf „mittel“ gefallen,
allein weil die Parameter anders eingeteilt wurden. Aus den Blöcken des Berichts gezählt gibt dieselbe Regel je nach
Zählweise eine andere Stufe: „gering“, wenn nur die Parameter mit Quelle zählen (5 von 22 = 23 %), und „mittel“, wenn
wie in der Registry auch die berechneten zählen (11 von 22 = 50 %, genau auf der Hälfte). Und es hat keinen Zeitbezug:
Es stünde auch für 2071–2100, wo die KWRA „sehr gering“ nennt, und für 2061–2070. Zu diesen Jahren sagt die KWRA
nichts; dort setzt die Zuordnung von KAP3 („niedrigere Stufe“) „sehr gering“. Die einfachere Rechnung, die Kennzahl als
Gewissheit, stellt die Lage deshalb falsch dar: Ein Nutzer läse aus einer Stufe ohne Zeitbezug, die Gewissheit sei bis
2100 mindestens „mittel“. Die KWRA zählt genau diese Klimawirkung zu den sieben mit der geringsten Gewissheit zum Ende
(TB6 S. 78).

**Einordnung nach „Einordnung der Charakterisierung“ (Zeitscheibe Mitte).**

| Schritt | Rechnung | Ergebnis | Quelle |
|---|---|---|---|
| Teil a) der Gesamtgewissheit | Regel G, Wert Mitte = mittel | 2 Punkte | Mappe S100; TB6 S. 141 (Punkte) |
| Teil b) der Gesamtgewissheit | Gewissheit mit Anpassung, Mitte = mittel | 2 Punkte | TB6 Tabelle 24, S. 128–129 (als Bild gelesen am 25.09.2026, Block `einordnung_charakterisierung`); Mappe V100 = „ja“ |
| Gesamtgewissheit | (2 + 2) : 2 | 2,0, über 1,5: ausreichend | TB6 S. 141; TB1 S. 93 |
| Gruppe | Wirksamkeit der beschlossenen Maßnahmen, Mitte, pessimistisch = gering-mittel = 0,25; unter der Schwelle Umsetzung 0,5, ab der Schwelle Entwicklung 0,1 | „Entwicklung“, wie TB6 Tabelle 27, S. 142 | Mappe Y100; beide Schwellen Abschätzungen von KAP3 |
| Zusatz „unter Unsicherheit“ | Gesamtgewissheit ausreichend | kein Zusatz | TB6 S. 141 |
| Kennzeichnung | eine Gruppe je Klimawirkung, gleich für alle Jahre der Zeitreihe und neben dem Betrag M0 | „Mitte des Jahrhunderts (2031–2060)“ | Abschnitt „Zuordnung zur Zeitscheibe des Produkts“ |

- **Das „sehr gering“ zum Ende geht nicht in die Gruppe ein.** Die KWRA bildet die Charakterisierung nur zur Mitte
  (TB1 S. 93). Mit dem Ende statt der Mitte wäre die Gesamtgewissheit (0 + 2) : 2 = 1,0, also „Entwicklung unter
  Unsicherheit“, gegen Tabelle 27. Die Gruppe „Entwicklung“ ohne Zusatz steht deshalb neben der Gewissheit „sehr
  gering“ zum Ende. Das widerspricht sich nicht, solange die Gruppe die Kennzeichnung „Mitte des Jahrhunderts
  (2031–2060)“ trägt und das Ende mit eigenem Wert und Hinweis dasteht.
- **Die Bedingung an den Maßnahmenraum trifft #98.** Die weiterreichende Anpassung hat „mittel“ = 0,5 (Mappe AA100).
  Misst der Eingang des Produkts diesen Raum, gibt die Schwelle 0,5 „Umsetzung“, gegen Tabelle 27. An der Spalte Y
  gemessen folgt „Entwicklung“ wie in Tabelle 27. Das entscheidet T-1111-ceo.
- **Was die einfachere Rechnung verfälschen würde.** Regel G allein („mittel“ reicht) und die Gesamtgewissheit (2,0)
  geben bei #98 beide „ausreichend“. Der Unterschied liegt hier nicht im Zusatz, sondern im Eingang: Heute liegt er bei
  0, weil der Katalog für #98 keine Maßnahme führt (Konformitätsliste, Zeile 7). Das Produkt zeigt deshalb „Innovation“,
  nicht „Entwicklung“, mit beiden Regeln.

Die gebrauchte Quellenlage nach Regel G, gezählt aus dem Endstand der Parameter-Blöcke von
`docs/methodik/98_uv_schaedigungen.md` (Kap. 7): 22 Blöcke, davon 5 mit Kennzeichnung `quelle` (`uv.w_scc`,
`uv.i_raten_roh`, `uv.i_mm`, `uv.i_c44`, `uv.or_out`), 11 `abschaetzung_kap3` (`uv.a_attr`, `uv.c_fall`, `uv.voly`,
`uv.r_out_sensitivitaet`, `uv.s_komforttag`, `uv.phi_komfort`, `uv.qbar_out`, `uv.r_out_enabled`,
`uv.s155_dosisminderung`, `uv.s155_a_erk_mm`, `uv.s155_a_erk_c44`) und 6 `berechnet` (`uv.ssd_delta_region`,
`uv.k_uv`, `uv.baf`, `uv.lambda`, `uv.l_rest`, `uv.c_kal`). Angezeigt wird „5 von 22 Parametern mit Quelle“ (23 %).
Zum Vergleich, geht **nicht** in die Gewissheit ein: Mit den berechneten sind es 11 von 22 = 50 %. Nach der alten Regel
stünde #98 damit auf „gering“ (23 %) oder, genau auf der Hälfte, auf „mittel“ (50 %). Die Registry kommt heute mit 22
von 30 (73 %) auf „mittel“, bis T-1820-cto kam sie mit 30 von 30 auf „hoch“. Dieselbe alte Regel gibt also je nach
Zählweise heute zwei verschiedene Stufen (gering, mittel, mittel), vorher drei, und keine trifft das „sehr gering“ der
KWRA zum Ende. Dass die Registry trotz derselben Kennzeichnung auf 73 % statt 50 % kommt, liegt an der Zerlegung: Von
ihren 30 Parametern gehören 29 zu 16 Blöcken des Berichts, mehrere je Block (etwa fünf Altersgruppen bei `uv.i_mm` und
bei `uv.i_c44`), dazu kommt der Referenzwert des Index ohne Block. Die drei Blöcke `uv.s155_…` wirken nur im
Maßnahmen-Modul. Ohne sie wären es 5 von 19 = 26 %. Regel G zählt jeden Block einmal, also 22.

Beispiel-Block `rechenkette_gewissheit_98`, aus dem Stamm des Produkt-Repos ausführbar (am 07.10.2026 gelaufen,
Ausgabe darunter):

```python
# rechenkette_gewissheit_98 — Regel G an #98 nachgerechnet, dieselben Ebenen wie #95 und #96
import re
import sys
import openpyxl

STUFEN = ("sehr gering", "gering", "mittel", "hoch")  # TB6 S. 78, aufsteigend
PUNKTE = {"sehr gering": 0, "gering": 1, "mittel": 2, "hoch": 3}  # TB6 S. 141
WIRKSAMKEIT = {"gering": 0.0, "gering-mittel": 0.25, "mittel": 0.5, "mittel-hoch": 0.75, "hoch": 1.0}  # S. 112

ws = openpyxl.load_workbook("docs/KWAR/KWRA-2021_Klimawirkungen.xlsx", data_only=True)["Klimawirkungen"]

# Ebene 2: Zeile der Klimawirkung über die KWRA-ID in Spalte A
zeile = next(r for r in range(3, ws.max_row + 1) if ws.cell(r, 1).value == 98)
assert zeile == 100
assert ws["D100"].value == "UV-bedingte Gesundheitsschädigungen (insbesondere Hautkrebs)"

# Ebenen 3 und 4: Kopfzellen, Werte, Quellvermerk
assert (ws["S2"].value, ws["T2"].value) == ("Gewissheit – Mitte", "Gewissheit – Ende")
mitte, ende = ws["S100"].value, ws["T100"].value
assert (mitte, ende) == ("mittel", "sehr gering")
assert ws["AJ100"].value.startswith("TB 6 Tab. 1")


def gewissheit(jahr):
    """Ebenen 6 bis 8: Jahr der Zeitreihe → Stufe nach der Zuordnungstabelle."""
    if jahr <= 2060:
        return mitte
    if jahr <= 2070:
        return min(mitte, ende, key=STUFEN.index)
    return ende


HEUTIGES_KLIMA = "in der KWRA nicht ausgewiesen"  # Ebene 5
zeitreihe = {j: gewissheit(j) for j in range(2025, 2066)}  # Produkt: 2025–2065
assert all(zeitreihe[j] == "mittel" for j in range(2025, 2061))
assert all(zeitreihe[j] == "sehr gering" for j in range(2061, 2066))
assert all(gewissheit(j) == "sehr gering" for j in range(2071, 2101))

# Ebene 9: ein Wert je Klimawirkung; #98 hat einen Code
codes = ("EXPECTED_ANNUAL_UV_YLL",)
je_code = {c: (mitte, ende) for c in codes}
assert set(je_code.values()) == {("mittel", "sehr gering")}

# Ebene 10: Vorsichtshinweis ab „gering“ — zur Mitte nicht, zum Ende ja
VORSICHT_STUFEN = ("sehr gering", "gering")
assert mitte not in VORSICHT_STUFEN and ende in VORSICHT_STUFEN

# Einordnung der Charakterisierung (Zeitscheibe Mitte): Gesamtgewissheit und Gruppe
TAB24_MITTE_98 = "mittel"  # TB6 Tabelle 24, S. 128–129, „Gewissheit der Bewertung (Klimarisiken mit Anpassung)“, Mitte
gesamt = (PUNKTE[mitte] + PUNKTE[TAB24_MITTE_98]) / 2
assert gesamt == 2.0 and gesamt > 1.5                # ausreichend, kein Zusatz
assert (PUNKTE[ende] + PUNKTE[TAB24_MITTE_98]) / 2 == 1.0   # mit Ende statt Mitte: „unter Unsicherheit“
assert ws["V100"].value == "ja"                      # Anpassungskapazität analysiert, Tabelle 24 hat einen Wert
assert ws["Y2"].value == "Wirksamkeit APA III – Mitte pessim."
assert ws["AA2"].value == "Wirksamkeit weiterr. – Mitte pessim."
w_y, w_aa = WIRKSAMKEIT[ws["Y100"].value], WIRKSAMKEIT[ws["AA100"].value]
assert (w_y, w_aa) == (0.25, 0.5)
SCHWELLE_UMSETZUNG, SCHWELLE_ENTWICKLUNG = 0.5, 0.1  # Abschätzungen von KAP3, Bänder 0,33–0,5 und 0,05–0,2


def gruppe(w):
    return "Umsetzung" if w >= SCHWELLE_UMSETZUNG else "Entwicklung" if w >= SCHWELLE_ENTWICKLUNG else "Innovation"


assert gruppe(w_y) == "Entwicklung"                  # wie TB6 Tabelle 27, S. 142
assert gruppe(w_aa) == "Umsetzung"                   # an AA gemessen: gegen Tabelle 27
assert gruppe(0.0) == "Innovation"                   # heutiger Eingang des Produkts

# Gebrauchte Quellenlage: Endstand der Parameter-Blöcke, jeder Block einmal
text = open("docs/methodik/98_uv_schaedigungen.md", encoding="utf-8").read()
kap7 = text.split("## 7 Parameter-Blöcke", 1)[1].split("\n## ", 1)[0]
kz = re.findall(r"^\s*kennzeichnung:\s*(\w+)", kap7, flags=re.M)
zaehlung = {k: kz.count(k) for k in sorted(set(kz))}
assert len(kz) == len(re.findall(r"^parameter:", kap7, flags=re.M)) == 22
assert zaehlung == {"abschaetzung_kap3": 11, "berechnet": 6, "quelle": 5}
assert round(5 / 22, 2) == 0.23 and 11 / 22 == 0.5 and round(5 / 19, 2) == 0.26


def alte_regel(anteil):
    """Alte Kennzahl (backend/app/services/gewissheit.py): Stufe aus dem Anteil belegter Parameter."""
    return "sehr gering" if anteil == 0 else "gering" if anteil < 0.5 else "mittel" if anteil < 1 else "hoch"


# Vergleich, Registry des Produkts nach der alten Regel: seit T-1820-cto „mittel“
sys.path.insert(0, "backend")
from app.services import gewissheit as alt, parameter_registry  # noqa: E402

klassen = [p["evidence_class"] for p in alt._risiko_parameter(codes[0])]
registry = (sum(k in parameter_registry.BELEGTE_KLASSEN for k in klassen), len(klassen))
assert {k: klassen.count(k) for k in sorted(set(klassen))} == {"abgeschaetzt": 8, "belegt": 13, "berechnet": 9}
assert registry == (22, 30) and alt.gewissheitsstufe(codes[0]) == "mittel"
assert (alte_regel(5 / 22), alte_regel(11 / 22), alte_regel(22 / 30)) == ("gering", "mittel", "mittel")
assert STUFEN.index(alt.gewissheitsstufe(codes[0])) - STUFEN.index(ende) == 2   # heute zwei Stufen über dem Ende
# Stand vor T-1820-cto (Commit 22f532d3, gemessen am 07.10.2026): 30 von 30 belegt, also „hoch“, drei Stufen darüber
assert alte_regel(30 / 30) == "hoch" and STUFEN.index("hoch") - STUFEN.index(ende) == 3

print("Mitte:", mitte, "| Ende:", ende, "| heutiges Klima:", HEUTIGES_KLIMA)
print("2025:", zeitreihe[2025], "| 2060:", zeitreihe[2060], "| 2061:", zeitreihe[2061], "| 2065:", zeitreihe[2065])
print("Gesamtgewissheit Mitte:", gesamt, "| ausreichend:", gesamt > 1.5, "| Gruppe:", gruppe(w_y),
      "| Wirksamkeit Y/AA:", w_y, w_aa)
print("Quellenlage:", zaehlung, "| angezeigt:", f"{zaehlung['quelle']} von {len(kz)} Parametern mit Quelle")
print("Registry belegt/alle (nur Vergleich):", registry, "| Stufe heute:", alt.gewissheitsstufe(codes[0]))
```

Ausgabe:

```
Mitte: mittel | Ende: sehr gering | heutiges Klima: in der KWRA nicht ausgewiesen
2025: mittel | 2060: mittel | 2061: sehr gering | 2065: sehr gering
Gesamtgewissheit Mitte: 2.0 | ausreichend: True | Gruppe: Entwicklung | Wirksamkeit Y/AA: 0.25 0.5
Quellenlage: {'abschaetzung_kap3': 11, 'berechnet': 6, 'quelle': 5} | angezeigt: 5 von 22 Parametern mit Quelle
Registry belegt/alle (nur Vergleich): (22, 30) | Stufe heute: mittel
```

## Entscheidungslog

Gewählt ist Regel G. Verworfen, je mit einem Satz:

1. **Die heutige Kennzahl allein als Gewissheit** (Anteil der Parameter mit Quelle, Schnitt 0,5, je Risikocode, ohne
   Zeitbezug) ist verworfen, weil sie die Quellenlage der Rechnung misst statt der Gewissheit des Klimarisikos und die
   Lage falsch darstellt: #98 steht auf „hoch“, wo die KWRA zum Ende „sehr gering“ nennt, und #95 je nach Zählweise
   auf „gering“ oder „mittel“, wo die KWRA zur Mitte „hoch“ nennt.
2. **Der Vorschlag des CEO aus T-1030-ceo** (KWRA-Gewissheit mit Fundstelle, daneben die heutige Kennzahl als
   „Quellenlage“) ist in seinem ersten Teil gewählt und im zweiten Teil nur ohne Stufe übernommen, weil eine zweite
   Stufe auf derselben Skala neben der Gewissheit als zweite Gewissheit gelesen würde (bei #98 „hoch“ neben „sehr
   gering“) und ihr Anteil davon abhängt, wie fein die Parameter zerlegt sind (#95: 34 Parameter in der Registry, 19
   Blöcke im Bericht).
3. **Das Minimum aus KWRA-Stufe und Quellenlage-Stufe** ist verworfen, weil es zwei verschiedene Fragen vermischt und
   #95 zur Mitte allein wegen der Zählweise der eigenen Rechnung unter die Bewertung der KWRA drücken würde.
4. **Eine eigene Bewertung der fünf Teilaspekte durch KAP3** ist verworfen, weil die KWRA die Teilaspekte selbst nicht
   einzeln bewertet (TB6 S. 81) und eine Stufe von KAP3 ohne Quelle die Bewertung des Behördennetzwerks ersetzen
   würde.
5. **Ein Wert ohne Zeitbezug als Mittel beider Zeitscheiben** ist verworfen, weil die KWRA die Zahlen 1–4 selbst eine
   „künstliche Spezifizierung“ nennt (TB6 S. 78, Fußnote 18) und das Mittel den Abfall bei #98 von „mittel“ auf „sehr
   gering“ zu „gering“ glätten würde.
6. **Nur die Zeitscheibe Mitte**, weil die Zeitreihe des Produkts 2065 endet, ist verworfen, weil das Produkt dann
   das „sehr gering“ von #98 zum Ende verschwiege, das die KWRA eigens hervorhebt (TB6 S. 78).
7. **Die nächste Zeitscheibe für 2061–2070** ist verworfen, weil diese Jahre bei fallender Gewissheit dann die
   höhere Stufe Mitte trügen, die die KWRA für den anschließenden Zeitraum nicht mehr stützt.
8. **Den Wert Mitte auch für den Euro-Betrag im heutigen Klima** zu zeigen ist verworfen, weil die KWRA für die
   Gegenwart keine Gewissheit bestimmt hat (TB6 Tabelle 1) und das Produkt sonst eine Zukunftsbewertung an einen aus
   Messwerten gerechneten Betrag hängen würde.
9. **Eine Gewissheit je Risikocode** ist verworfen, weil die KWRA je Klimawirkung bewertet und eine Klimawirkung sonst
   zwei Stufen trüge, wie #95 heute mit „mittel“ und „hoch“.

Schritt 2 (T-1173-methodik_manager, TB6 Kap. 6.2). Gewählt: Zeitscheibe Mitte, Gesamtgewissheit nach TB6 S. 141,
Umsetzung 0,5 mit Band 0,33–0,5, Entwicklung 0,1 mit Band 0,05–0,2, beide nur gültig, wenn der Eingang des Produkts die
beschlossenen Maßnahmen misst. Verworfen, je mit einem Satz:

10. **Die Zeitscheibe Ende für die Charakterisierung** ist verworfen, weil die KWRA das Klimarisiko mit Anpassung nur
    bis 2060 bewertet hat (S. 112) und Tabelle 1 Ende mit Tabelle 24 Mitte nur 19 von 26 Gruppen trifft.
11. **Tabelle 24 „2020–2031“ statt Mitte** ist verworfen, weil Kap. 6.2 den optimistischen und pessimistischen Fall
    braucht (S. 141), den es für 2020–2030 nicht gibt, und die Spalte nur 18 von 26 Gruppen trifft.
12. **Eine Gruppe je Jahr der Zeitreihe** (etwa mit der Regel „niedrigere Stufe“ für 2061–2070) ist verworfen, weil die
    KWRA nur eine Charakterisierung zur Mitte gebildet hat und die Kombination Ende ohne Anpassung, Mitte mit Anpassung
    nicht bewertet ist.
13. **Die Gewissheit nach Regel G allein als Eingang der Charakterisierung** ist verworfen, weil „mittel“ in Kap. 6.2
    für die Gesamtgewissheit gilt (S. 141) und Regel G allein acht von 13 Klimawirkungen „unter Unsicherheit“, bei M0
    #96, als hinreichend sicher zeigen würde.
14. **Die Gewissheitsschwelle „über 1“** ist verworfen, weil Kap. 6.2 sie nur als Sensitivität nennt (S. 143) und
    neun Klimawirkungen ihren Hinweis „unter Unsicherheit“ verlören.
15. **Das Band 0,4–0,6 der Umsetzungsschwelle** ist ersetzt, weil Werte über 0,5 mehr als die eine Stufe verlangen, die
    Kap. 6.2 als Ziel setzt (S. 141), und bei 0,6 #96 und Schiffbarkeit gegen Tabelle 27 aus „Umsetzung“ fielen.
16. **Die Umsetzungsschwelle 0,33 als Wert** ist verworfen, weil sie die Rangskala gering, mittel, hoch wie Messwerte
    liest, während die KWRA Minderung auf der Wirksamkeitsskala beschreibt (S. 112); sie bleibt untere Bandgrenze.
17. **Eine Entwicklungsschwelle über 0,25 auf dem Eingang, der die beschlossenen Maßnahmen misst,** ist verworfen,
    weil dort alle 26 Klimawirkungen, auch #95 und #98, in „Innovation“ fielen (12 statt 15 Treffer an Spalte Y). Die
    Regel der KWRA, 0,5 an der weiterreichenden Anpassung (25 von 26 an Spalte AA), ist damit nicht verworfen, sondern
    als Übergabe an T-1111-ceo vermerkt, weil nur dort feststeht, ob der Eingang einen weiterreichenden Raum abbildet.
    (Runde 1: Die erste Fassung verwarf diese Regel an Spalte Y, also am falschen Maßnahmenraum.)
18. **Regel G allein, wo Tabelle 24 keinen Wert hat**, ist verworfen, weil die Bedingung der KWRA beide Teile verlangt
    und Regel G allein die Gewissheit, wie gerechnet, zu oft als ausreichend zeigt.
19. **Den Mittelwert als Widerspruch zu Regel G** zu werten ist verworfen: Die Zeile „kein Mittelwert“ unter „Verhältnis
    zur KWRA-Einstufung“ und Punkt 5 gelten für die angezeigte Gewissheit einer Klimawirkung, und der Mittelwert hier
    ist die Regel der KWRA selbst (S. 141) für eine Ja-Nein-Frage, die das Produkt nicht als Stufe zeigt.
20. **Die Schwellen ohne Bedingung an den Maßnahmenraum** zu übergeben ist verworfen (Runde 1), weil dieselbe Schwelle
    0,5 an der weiterreichenden Anpassung nur 14 von 29 Gruppen „Umsetzung“ trifft und #95 und #98 gegen Tabelle 27
    in „Umsetzung“ legte.
21. **Die Zeitscheibe nur aus Kap. 5 und Kap. 6.2 zu erschließen** ist ersetzt (Runde 1), weil TB1 Kap. 2.5, S. 93,
    auf das TB6 Fußnote 28 verweist, die Mitte des Jahrhunderts für beide Teile der Gesamtgewissheit wörtlich nennt.

Änderungen an Abschnitten aus Schritt 1: Unter „Folgegrößen“ ist die Klammer „zweiter Teil, Zeitscheibe und Schwellen
folgen in Schritt 2“ durch das Ergebnis ersetzt, weil Schritt 2 sie beantwortet. Unter „Quellen“ sind die in Schritt 2
gelesenen Fundstellen ergänzt, damit jede Seitenangabe dieser Datei dort steht. Sonst ist nichts aus Schritt 1
geändert.

Schritt 3 (T-1174-methodik_manager, #96). Regel G, Zuordnungstabelle und die Regel aus „Einordnung der
Charakterisierung“ sind **unverändert** angewendet. Sie passen an #96 ohne Änderung: ein Risikocode, eine Zeile der
Mappe, Mitte und Ende gleich, Tabelle 24 mit Wert, Gruppe „Umsetzung“ wie Tabelle 27. Keine weitere Option ist
verworfen. Änderungen an Abschnitten aus Schritt 1 und 2: Der Vorspann nennt die Schritte mit ihren Tickets, weil er
sonst „rechnet nur #95“ behauptete. Der Satz vor der Tabelle unter „Rechenkette“ nennt #96 als zweites Beispiel. Unter
„Befunde an Berichte“ steht das Ergebnis je Klimawirkung, unter „Quellen“ die Fundstellen von Schritt 3. Sonst ist
nichts aus Schritt 1 und 2 geändert.

Nachtrag 27.09.2026 (T-1478-methodik_manager): Bericht 95 hat jetzt 23 Parameter-Blöcke statt 19. Der Vergleich unter
„Rechenkette“ und der Block `rechenkette_gewissheit_95` sind darauf nachgezogen; der Block zählt jetzt auch die Registry
nach. Die Zahlen in Punkt 2 und 9 sind der Stand vom 25.09.2026. Die Entscheidungen bleiben unverändert.

Schritt 4 (T-1175-methodik_manager, #98). Regel G, Zuordnungstabelle und die Regel aus „Einordnung der
Charakterisierung“ sind **unverändert** angewendet. An #98 wirkt die Regel „niedrigere Stufe“ für 2061–2070 zum ersten
Mal (2061–2065 „sehr gering“ statt „mittel“), wie in der Begründung zur Zuordnungstabelle vorhergesagt. Verworfen, mit
einem Satz:

22. **Die Gewissheit Ende in die Gesamtgewissheit von #98 zu nehmen**, weil sie „sehr gering“ ist, ist verworfen,
    weil die KWRA die Charakterisierung nur zur Mitte bildet (TB1 S. 93) und (0 + 2) : 2 = 1,0 #98 gegen Tabelle 27 in
    „Entwicklung unter Unsicherheit“ legte; das Ende steht stattdessen mit eigenem Wert und Hinweis neben der Gruppe.

Nachtrag 07.10.2026 (T-1175-methodik_manager, Nachtrag des CEO vom 26.09.2026): Bericht 95 hat jetzt 30
Parameter-Blöcke statt 23 (Commit `b0f3ad9a`), Bericht 96 14 statt 13 (Commit `c0486100`). Beide Blöcke schlugen damit
fehl (`AssertionError` bei der Blockzahl). Vergleich und Block sind für #95 und #96 nachgezogen; der Block zu #96 zählt
jetzt auch die Registry nach. #96 ist mitgezogen, obwohl der Nachtrag des CEO nur #95 nennt: Sein Block schlug aus
demselben Grund fehl, die Übersicht am Ende braucht beide auf dem heutigen Stand, und ein zweites Paket auf dieser
Datei stieße mit diesem zusammen. Nach der alten Regel stehen heute beide Codes von #95 auf „gering“ (17 von 38, 3 von
9). Punkt 1 („gering“ oder „mittel“), Punkt 9 und der Satz „Heute stehen sie auf verschiedenen Stufen (mittel und
hoch)“ unter „Ein Wert je Klimawirkung“ sind deshalb der Stand vom 25.09.2026. Die Entscheidungen bleiben: Punkt 1
gilt verschärft, weil die Kennzahl jetzt in jeder Zählweise zwei Stufen unter der KWRA liegt. Punkt 9 gilt, weil zwei
Codes einer Klimawirkung je eigene Zählungen tragen und heute nur zufällig gleich lauten. **Die Einordnung von #95
ändert sich nicht** (Gesamtgewissheit 2,5, „Entwicklung“): Sie setzt auf Zellen der KWRA auf, nicht auf der Zählung.

Nachtrag Runde 1, 07.10.2026 (T-1820-cto): Seit Commit `c8aba66f` übernimmt die Registry für #98 die Kennzeichnung der
Blöcke aus Kapitel 7 von Bericht 98. Die alte Kennzahl meldet für #98 seitdem „mittel“ (22 von 30) statt „hoch“ (30
von 30, gemessen am Stand `22f532d3`). Die Angaben zu #98 in Punkt 1 („#98 steht auf ‚hoch‘“) und Punkt 2 („bei #98
‚hoch‘ neben ‚sehr gering‘“) sind deshalb der Stand bis T-1820-cto. Block, Text unter „#98 UV-Schädigungen“ und der
Hinweis unter „Befunde an Berichte“ sind nachgezogen. Die Entscheidungen bleiben. Punkt 1 bleibt, weil die Kennzahl
die Lage auch mit „mittel“ falsch darstellt: Sie hat keinen Zeitbezug und liegt zwei Stufen über dem „sehr gering“ zum
Ende. Gewechselt hat sie an einem Tag ohne neues Wissen, allein durch die Einteilung der Parameter. Punkt 2 bleibt,
weil eine zweite Stufe neben der Gewissheit weiterhin als zweite Gewissheit gelesen würde, jetzt „mittel“ neben „sehr
gering“. Ihr Anteil hängt von der Zerlegung ab: Registry 22 von 30 = 73 %, Blöcke des Berichts 11 von 22 = 50 %. An
Regel G, Zuordnungstabelle und Einordnung ändert sich nichts. Die Einordnung von #98 („Entwicklung“, 2,0) setzt auf
Zellen der KWRA und auf Tabelle 24 auf, nicht auf der Kennzahl.

Nachtrag Runde 2, 07.10.2026 (Urteil des Managers zu Runde 1): Unter „#98 UV-Schädigungen“ nennt der Absatz zum
zufälligen „mittel“ jetzt beide Zählweisen der Blöcke („gering“ mit 5 von 22, „mittel“ mit 11 von 22). Beim fehlenden
Zeitbezug trennt er 2071–2100, wo die KWRA „sehr gering“ nennt, von 2061–2070, wo die Zuordnung von KAP3 „sehr gering“
setzt. Zwei Angaben unter „Festlegung“ beschrieben im Präsens den Stand vom 25.09.2026 und tragen ihr Datum jetzt an
der Stelle selbst, nicht nur in den Nachträgen oben. In Regel G zeigt das Beispiel der Zählung jetzt den Stand vom
07.10.2026 („10 von 30 Parametern mit Quelle“ bei #95, vorher „8 von 19“), weil es nur die Form der Anzeige zeigt und
so mit der Übersicht am Ende übereinstimmt; „8 von 19“ mit Datum wäre ein überholtes Beispiel in der Regel geblieben.
Unter „Ein Wert je Klimawirkung“ steht der Satz „Heute stehen sie auf verschiedenen Stufen (mittel und hoch)“ jetzt als
Stand vom 25.09.2026, daneben der Stand vom 07.10.2026 (beide Codes „gering“). Regel G selbst ist unverändert: Das
Produkt zeigt als Gewissheit den Wert der KWRA je Zeitscheibe, und die Quellenlage erscheint nur als Zählung ohne
Stufe. Zuordnungstabelle und Einordnung sind ebenfalls unverändert.

Änderungen an Abschnitten aus Schritt 1 bis 3: Der Vorspann nennt Schritt 4 mit Ticket. Der Satz vor der Tabelle unter
„Rechenkette“ nennt #98 als drittes Beispiel. Vergleich und Block zu #95 und #96 sind auf den heutigen Stand
nachgezogen (oben). Unter „Festlegung“ tragen das Beispiel der Zählung in Regel G und der Satz zu den Stufen der beiden
Codes unter „Ein Wert je Klimawirkung“ ihr Datum an der Stelle selbst (Nachtrag Runde 2). Unter „Befunde an Berichte“
steht #98, unter „Quellen“ die Fundstellen von Schritt 4. Die Übersicht am Ende ist neu. Sonst ist nichts aus Schritt 1
bis 3 geändert.

## Befunde an Berichte

#95: keine. #96: keine. #98: keine.

Verglichen am 25.09.2026: Bericht 95, Abschnitt „Risiko ohne (weitere) Anpassung“, Absatz „Gewissheit der
KWRA-Bewertung“, nennt Mitte **hoch** und Ende **mittel** mit Fundstelle Mappe Zeile 97, Spalten S und T, und TB6
Tabelle 1, S. 41; Quelle [68] nennt dieselbe Tabelle und Seite. Die Zellen S97 = „hoch“ und T97 = „mittel“ stimmen
damit überein, ebenso das Bild von TB6 Tabelle 1, S. 41. Der dort genannte Mittelwert 3,5 über beide Zeitscheiben
stimmt mit TB6 S. 78–79.

Verglichen am 26.09.2026 (Schritt 3): Bericht 96 im Endstand, Kap. 1, Abschnitt „Risiko ohne (weitere) Anpassung“,
Aussage (c) „KWRA-Stufe ohne Anpassung und Gewissheit je Zeitscheibe“, nennt Mitte **mittel** (Zelle S98) und Ende
**mittel** (Zelle T98), Zeile 98, und für die Gegenwart „nicht ausgewiesen“. Die Zellen S98 = „mittel“ und
T98 = „mittel“ stimmen damit überein, ebenso das Bild von TB6 Tabelle 1, S. 41 (Zeile „Allergische Reaktionen durch
Aeroallergene pflanzlicher Herkunft“). Bericht 96 nennt als gleichlautende Fundstelle TB5 Tabelle 55, S. 179, nicht
TB6 Tabelle 1. Das ist keine Abweichung vom Wert. TB5 ist in diesem Schritt nicht nachgelesen worden.

Verglichen am 07.10.2026 (Schritt 4): Bericht 98 im Endstand (Rev. 15, Commit `5a59ef3b`), Kap. 1, Abschnitt „Risiko
ohne (weitere) Anpassung“, Aussage (d) „KWRA-Gewissheit je Zeitscheibe“, nennt Mitte **mittel** (Zeile 100, Spalte S)
und Ende **sehr gering** (Spalte T), für die Gegenwart „nicht ausgewiesen“. Die Zellen S100 = „mittel“ und T100 = „sehr
gering“ stimmen damit überein, ebenso das Bild von TB6 Tabelle 1, S. 41 (Zeile „UV-bedingte Gesundheitsschädigungen
(insb. Hautkrebs)“). Die Aussage (c) zur Einstufung ohne Anpassung (Gegenwart mittel; Mitte mittel und hoch; Ende
mittel und hoch; Spalten N–R) stimmt mit N100–R100 und mit demselben Bild überein. Die Fundstelle TB6 S. 78 für das
„sehr gering“ zum Ende stimmt mit dem Text dort.

Hinweis an Bericht 98, keine Abweichung von einer Zelle: Aussage (d) sagt, das Produkt führe #98 „bei der Quellenlage
auf ‚hoch‘“, weil jeder Parameter eine Quelle oder eine ausgewiesene Abschätzung mit Herleitung habe. Das beschrieb
die Registry bis T-1820-cto (30 von 30, „hoch“). Seit T-1820-cto (Commit `c8aba66f`, 07.10.2026) zählt die Registry
abgeschätzte Parameter nicht mehr als belegt, kommt auf 22 von 30 und meldet „mittel“. Der Satz beschreibt das Produkt
also nicht mehr. Nach Regel G trägt die Quellenlage ohnehin keine Stufe und lautet „5 von 22 Parametern mit Quelle“
(T-1030-ceo). Bericht 98 verweist für die Darstellung selbst auf die übergreifende Regel (T-1110). Der Nachzug in
Bericht 98 gehört nicht zu diesem Paket; Bericht 98 ist hier nicht geändert.

## Quellen

- **[TB6]** Umweltbundesamt (Hrsg.): Klimawirkungs- und Risikoanalyse 2021 für Deutschland, Teilbericht 6: Integrierte
  Auswertung – Klimarisiken, Handlungserfordernisse und Forschungsbedarfe. Reihe Climate Change, Dessau-Roßlau,
  Oktober 2021. Lokale Kopie `docs/KWAR/kwra2021_teilbericht_6_integrierte_auswertung_bf_211027_0.pdf`. Verwendet:
  Kap. 2.1, S. 35 mit Fußnote 3; Tabelle 1, S. 36–41 (Hitzebelastung S. 41); Kap. 3.3, S. 78–82 mit Fußnote 18;
  Tabelle 17, S. 80; Kap. 6.2, S. 141. Schritt 2: Kap. 5.1, S. 112–123; Kap. 5.2 mit Tabelle 24, S. 123–129
  (Tabelle 24 als Bild gelesen); Kap. 6.1 mit Tabelle 25, S. 136–140; Kap. 6.2, S. 140–145 mit Fußnoten 28 und 29 und
  Tabelle 27, S. 142 (als Bild gelesen).
- **[TB1]** Umweltbundesamt (Hrsg.): Klimawirkungs- und Risikoanalyse 2021 für Deutschland, Teilbericht 1: Grundlagen.
  Reihe Climate Change, Dessau-Roßlau, Oktober 2021. Lokale Kopie
  `docs/KWAR/kwra2021_teilbericht_1_grundlagen_bf_211027_0.pdf` (gedruckte Seite = PDF-Seite − 1). Verwendet
  (Schritt 2, Runde 1): Kap. 2.5 „Methodik zur Untersuchung von Handlungserfordernissen“, S. 91–94 (PDF-Seiten 92–95),
  vollständig gelesen, darin Gesamtgewissheit und Zeitscheibe S. 93, Korrektur für die beschlossenen Maßnahmen
  S. 93–94; Aufzählung unmittelbar vor Kap. 2.5, S. 91 (Anpassungskapazität nur für die Mitte).
- **[Mappe, Schritt 2]** Blatt „Klimawirkungen“, Spalten S, T, V, Y (Kopf Y2 „Wirksamkeit APA III – Mitte pessim.“)
  und AA (Kopf AA2 „Wirksamkeit weiterr. – Mitte pessim.“) für die 29 Klimawirkungen aus Tabelle 27.
- **[Mappe]** `docs/KWAR/KWRA-2021_Klimawirkungen.xlsx`, Blatt „Klimawirkungen“, Zeile 97, Zellen A97, D97, S97, T97,
  AJ97; Kopfzellen S2, T2.
- **[Bericht 95]** `docs/methodik/95_hitzebelastung.md`, Abschnitt „Risiko ohne (weitere) Anpassung“, Absatz
  „Gewissheit der KWRA-Bewertung“; Kap. 6 „Szenario-Anwendung & Modellgrenzen“; Kap. 7 „Parameter-Blöcke“.
- **[Schritt 3]** TB6 Tabelle 1, S. 41, Zeile „Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft“ (als
  Bild gelesen am 26.09.2026). Mappe, Blatt „Klimawirkungen“, Zeile 98, Zellen A98, D98, S98, T98, V98, Y98, AA98,
  AJ98. `docs/methodik/96_aeroallergene.md`, Kap. 1, Abschnitt „Risiko ohne (weitere) Anpassung“, Aussage (c);
  Kap. 7 „Parameter-Blöcke“. `docs/KONFORMITAET_CHECKLISTE.md`, Zeile 7 mit „Gegenprobe Zeile 7“ (A10) und „Gegenprobe
  Zeile 8“.
- **[Schritt 4]** TB6 Tabelle 1, S. 41, Zeile „UV-bedingte Gesundheitsschädigungen (insb. Hautkrebs)“ (als Bild
  gelesen am 07.10.2026); TB6 Kap. 3.3, S. 78 (die sieben Klimawirkungen mit „sehr gering“ zum Ende). Mappe, Blatt
  „Klimawirkungen“, Zeile 100, Zellen A100, D100, N100–T100, V100, Y100, AA100, AJ100.
  `docs/methodik/98_uv_schaedigungen.md` (Rev. 15, Commit `5a59ef3b`), Kap. 1, Abschnitt „Risiko ohne (weitere)
  Anpassung“, Aussagen (c) und (d); Kap. 7 „Parameter-Blöcke“. Für den Nachzug: `docs/methodik/95_hitzebelastung.md`
  Kap. 7 (Commit `b0f3ad9a`), `docs/methodik/96_aeroallergene.md` Kap. 7 (Commit `c0486100`). Für die Registry von
  #98 (Runde 1): `backend/app/services/engine/impact/params.py`, `_UV_BLOECKE` und `_UV_KLASSE` (T-1820-cto, Commit
  `c8aba66f`); Stand davor gemessen an `backend/app` aus Commit `22f532d3`.
- **[Produkt]** `backend/app/services/gewissheit.py`, `charakterisierung.py`, `unsicherheits_zusammenschau.py`;
  `backend/app/api/routes/assessment.py`; `docs/KONFORMITAET_CHECKLISTE.md`, „Gegenprobe Zeile 8“.

## Übersicht für die Übergabe

Stand 07.10.2026, Schritt 4. Pfad der Gewissheit: Mappe `docs/KWAR/KWRA-2021_Klimawirkungen.xlsx`, Blatt
„Klimawirkungen“, Spalte S (Mitte) und Spalte T (Ende) in der Zeile der Klimawirkung; Fundstelle TB6 Tabelle 1, S. 41.
Folgegrößen und Schwellen knapp, Einzelheiten in den genannten Abschnitten:

- **Gewissheit einer Klimawirkung:** Wert übernommen, keine Schwelle von KAP3; `SCHWELLE_MITTEL` = 0,5 entfällt
  („Festlegung“, „Schwelle der Stufe ‚mittel‘“).
- **Hinweis zur vorsichtigen Interpretation** (`unsicherheits_zusammenschau.py`): setzt auf der Gewissheit nach Regel G
  je Zeitscheibe auf; Hinweis bei „gering“ und „sehr gering“ (`VORSICHT_STUFEN`, im Code gesetzt, Zweck nach TB6
  S. 78) („Folgegrößen“).
- **Gruppe der Charakterisierung** (`charakterisierung.py`): setzt auf der Gesamtgewissheit zur Mitte auf, Mittelwert
  aus Regel G Mitte und TB6 Tabelle 24 Mitte. Ausreichend über 1,5 (übernommen, TB6 S. 141; TB1 S. 93). Ohne Wert in
  Tabelle 24 nicht ausreichend (Abschätzung von KAP3). Umsetzung 0,5, Band 0,33–0,5, und Entwicklung 0,1, Band
  0,05–0,2 (beide Abschätzungen von KAP3, gültig nur, wenn der Eingang die beschlossenen Maßnahmen misst; T-1111-ceo)
  („Einordnung der Charakterisierung“).
- **Quellenlage der Rechnung:** nur Zählung über die Parameter-Blöcke des Berichts, ohne Stufe; keine Folgegröße setzt
  auf ihr auf („Festlegung“).

| Klimawirkung (Zeile der Mappe) | Heutiges Klima (Betrag M0) | 2025–2060 (Mitte, Spalte S) | 2061–2070 (niedrigere Stufe) | 2071–2100 (Ende, Spalte T) | Hinweis zur vorsichtigen Interpretation | Gruppe der Charakterisierung (Mitte) | Quellenlage (Zählung, keine Stufe) |
|---|---|---|---|---|---|---|---|
| #95 Hitzebelastung (97) | in der KWRA nicht ausgewiesen | hoch | mittel | mittel | keiner | (3 + 2) : 2 = 2,5, ausreichend; „Entwicklung“ | 10 von 30 Parametern mit Quelle |
| #96 Aeroallergene (98) | in der KWRA nicht ausgewiesen | mittel | mittel | mittel | keiner | (2 + 1) : 2 = 1,5, nicht ausreichend; „Umsetzung“, ohne Zusatz | 3 von 14 Parametern mit Quelle |
| #98 UV-Schädigungen (100) | in der KWRA nicht ausgewiesen | mittel | sehr gering | sehr gering | ab 2061 und zum Ende | (2 + 2) : 2 = 2,0, ausreichend; „Entwicklung“ | 5 von 22 Parametern mit Quelle |
