# Querschnitt: Gewissheit einer Klimawirkung

Querschnittsdatei der Methodik, gültig für alle 102 Klimawirkungen der KWRA 2021 (TB6 S. 35). Werte bekommen zuerst
#95, #96 und #98 (A-0048); dieser Stand (Schritt 1, Ticket T-1172-methodik_manager, Vorhaben T-1117-cmo) rechnet
nur #95. Schritt 2 liest TB6 Kap. 6.2 (Zeitscheibe und Schwellen der Charakterisierung), Schritt 3 und 4 rechnen #96
und #98 nach.

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
der Rechnung“, erscheint nur als Zählung (etwa „8 von 19 Parametern mit Quelle“), ohne Stufe, und keine Folgegröße
setzt auf ihm auf.

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
derselben Zelle (Zeile 97 der Mappe). Heute stehen sie auf verschiedenen Stufen (mittel und hoch), obwohl es eine
Klimawirkung ist; das entfällt. Die Quellenlage zählt ebenfalls je Klimawirkung, über die Parameter-Blöcke des einen
Berichts, jeder Block einmal.

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
Tabelle 24 (S. 128–129) und Tabelle 27 (S. 142). PDF-Seite und gedruckte Seite stimmen auf S. 112–145 überein.

**Kurzfassung.** Die KWRA bildet die Charakterisierung für die Zeitscheibe Mitte des Jahrhunderts (2031–2060). Als
Gewissheit nimmt sie nicht die Gewissheit nach Regel G allein. Sie nimmt eine *Gesamtgewissheit*: den Mittelwert aus
der Gewissheit ohne Anpassung und der Gewissheit mit Anpassung, und „mittel“ gilt erst ab einem Mittelwert über 1,5.
Die beiden Schwellen des Produkts nennt die KWRA nicht als Zahl. Sie bleiben Abschätzungen von KAP3. Der Wert 0,5
bleibt, sein Band wird 0,33–0,5 statt 0,4–0,6. Der Wert 0,1 und sein Band 0,05–0,2 bleiben, mit einer Modellgrenze.

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
| Umsetzung (`SCHWELLE_UMSETZUNG`) | 0,5 | 0,33–0,5 (bisher 0,4–0,6) | Wert bestätigt, Band ersetzt | Abschätzung von KAP3 |
| Entwicklung (`SCHWELLE_ENTWICKLUNG`) | 0,1 | 0,05–0,2 | bestätigt, mit Modellgrenze | Abschätzung von KAP3 |

**Umsetzung 0,5: bestätigt.** Im pessimistischen Fall liegt das Risiko ohne Anpassung bei den sehr dringenden
Klimawirkungen meist auf „hoch“ (Tabelle 25, S. 138). Das Ziel „mittel“ (S. 141) verlangt dann eine Stufe Minderung,
also die Wirksamkeit „mittel“ = 0,5. Nachgerechnet an der Wirksamkeit der beschlossenen Maßnahmen, Mitte,
pessimistischer Fall (Mappe Spalte Y): Mit 0,5 trifft die Einordnung „Umsetzung“ bei allen 29 charakterisierten
Klimawirkungen Tabelle 27. Das sind drei Klimawirkungen in „Umsetzung“ (#96, Hochwasserschutzsysteme, Schiffbarkeit)
und 26 außerhalb.

**Band 0,33–0,5: ersetzt.** Das bisherige Band 0,4–0,6 reichte über 0,5 hinaus. Eine Schwelle über 0,5 verlangt mehr
als die eine Stufe, die Kap. 6.2 als Ziel setzt. Bei 0,6 fallen #96 und Schiffbarkeit aus „Umsetzung“ heraus (27
statt 29 Treffer), gegen Tabelle 27. Die untere Grenze 0,33 ist die zweite Lesart desselben Ziels. Liest man die drei
Risikostufen gering, mittel, hoch als 1, 2, 3, ist „hoch“ auf „mittel“ ein Drittel weniger. Diese Lesart behandelt eine
Rangskala wie Messwerte. Deshalb ist sie nur Bandgrenze und nicht Wert. Im ganzen Band 0,33–0,5 bleibt die Zuordnung
„Umsetzung“ gleich (29 von 29).

**Entwicklung 0,1: bestätigt, mit Modellgrenze.** Die Schwelle trennt im Produkt „kein nennenswerter Hebel“ von „ein
Hebel, der sich ausbauen lässt“. Auf der Wirksamkeitsskala liegt sie zwischen „gering“ (0, „würde … nicht
reduzieren“, S. 112) und „gering-mittel“ (0,25). Das ganze Band 0,05–0,2 liegt in dieser Lücke und ordnet
KWRA-Werte gleich ein. **Modellgrenze:** Die KWRA trennt „Entwicklung“ von „Innovation“ an einer anderen Frage. Sie
fragt, ob die *weiterreichenden* Maßnahmen das Ziel erreichen (S. 140–141, S. 143). Das Produkt kennt nur einen
Maßnahmenraum, den Katalog. An den beschlossenen Maßnahmen gemessen trifft 0,1 bei 15 von 26 Klimawirkungen die Gruppe
von Tabelle 27. Genauer geht es mit einer Zahl nicht: Jede Schwelle von 0,05 bis 0,2 gibt 15 Treffer. Jede Schwelle
über 0,25 gibt 12 Treffer, weil dann alle 26 Klimawirkungen in „Innovation“ fallen, auch #95 und #98, die Tabelle 27
unter „Entwicklung“ führt. Für M0 stimmt die Einordnung: #95 und #98 haben „gering-mittel“ (0,25), also „Entwicklung“;
#96 hat „mittel“ (0,5), also „Umsetzung“, wie Tabelle 27. Wie das Produkt „weiterreichend“ abbildet, gehört zur
Definition des Anpassungspotenzials (T-1111-ceo) und nicht hierher.

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
   Variante „unter Unsicherheit“ (S. 140). Deshalb ändert die Ausnahme keine Gruppe.

**Die Regel für das Produkt (übernommen, TB6 S. 141):** Die Charakterisierung zählt die Gewissheit als ausreichend,
wenn die Gesamtgewissheit zur Mitte über 1,5 liegt. Die Gesamtgewissheit ist der Mittelwert der Punkte (sehr gering 0,
gering 1, mittel 2, hoch 3) aus der Gewissheit nach Regel G, Wert Mitte (TB6 Tabelle 1, Mappe Spalte S), und der
Gewissheit der Bewertung der Klimarisiken mit Anpassung, Spalte „Mitte des Jahrhunderts“ (TB6 Tabelle 24, S. 128–129).
Die Mappe führt diese zweite Spalte nicht. Der Mittelwert ist die Regel der KWRA für eine Ja-Nein-Frage. Das Produkt
zeigt ihn nicht als Stufe.

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


# (2) Umsetzungsschwelle an der Wirksamkeit der beschlossenen Maßnahmen, Mitte pessimistisch (Mappe Spalte Y)
def umsetzung_treffer(schwelle):
    return sum((WIRKSAMKEIT[ws[f"Y{zeile[i]}"].value] >= schwelle) == (gr == "Umsetzung") for i, gr in gruppe.items())


print("Umsetzung, Treffer von 29 — 0,33:", umsetzung_treffer(0.33), "| 0,4:", umsetzung_treffer(0.4),
      "| 0,5:", umsetzung_treffer(0.5), "| 0,6:", umsetzung_treffer(0.6))
assert umsetzung_treffer(0.5) == 29 and umsetzung_treffer(0.6) == 27


# (2) Entwicklungsschwelle an derselben Spalte: trennt „Entwicklung“ von „Innovation“ nur zum Teil
def entwicklung_treffer(schwelle):
    return sum((WIRKSAMKEIT[ws[f"Y{zeile[i]}"].value] >= schwelle) == gr.startswith("Entwicklung")
               for i, gr in gruppe.items() if gr != "Umsetzung")


print("Entwicklung/Innovation, Treffer von 26 — 0,05:", entwicklung_treffer(0.05), "| 0,1:", entwicklung_treffer(0.1),
      "| 0,2:", entwicklung_treffer(0.2), "| 0,3:", entwicklung_treffer(0.3))
```

Ausgabe:

```
Treffer von 26 — Mitte/Mitte: 26 | Ende/Mitte: 19 | Mitte/2020–2031: 18
Treffer von 26 — Regel G allein: 18
Robust unter Unsicherheit (Mittelwert höchstens 1): [13, 19, 51, 55]
M0 Gesamtgewissheit Mitte: {95: 2.5, 96: 1.5, 98: 2.0} | ausreichend: {95: True, 96: False, 98: True}
Umsetzung, Treffer von 29 — 0,33: 29 | 0,4: 29 | 0,5: 29 | 0,6: 27
Entwicklung/Innovation, Treffer von 26 — 0,05: 15 | 0,1: 15 | 0,2: 15 | 0,3: 12
```

## Folgegrößen

- **Gruppen der Charakterisierung (Konformitätszeile 7, `backend/app/services/charakterisierung.py`):** Sie setzen
  auf der Gesamtgewissheit der KWRA auf, die Kap. 6.2 „aus der Kombination der Gewissheit der Bewertung des
  Klimarisikos ohne Anpassung sowie der Gewissheit der Bewertung der Anpassungskapazität“ bildet (TB6 S. 141), deren
  erster Teil die Gewissheit nach Regel G ist und nicht die Quellenlage, weil die Gruppen „unter Unsicherheit“ fragen,
  wie sicher die Aussage über Risiko und Anpassung ist, und nicht, ob die Rechnung von KAP3 Quellen hat. Nach Schritt 2
  gilt: Die Gruppen setzen auf der Gesamtgewissheit zur Mitte des Jahrhunderts auf, dem Mittelwert aus Regel G (Wert
  Mitte) und TB6 Tabelle 24 (Spalte Mitte). Ausreichend ist ein Mittelwert über 1,5. Ohne Wert in Tabelle 24 zählt die
  Gewissheit als nicht ausreichend. Einzelheiten und Schwellen stehen unter „Einordnung der Charakterisierung“. Grund:
  Kap. 6.2 bildet die Gesamtgewissheit so (TB6 S. 141). Die Gewissheit nach Regel G allein trifft Tabelle 27 nur
  18-mal von 26.
- **Hinweis zur vorsichtigen Interpretation (Zeile 19, `backend/app/services/unsicherheits_zusammenschau.py`):** Er
  setzt auf der Gewissheit nach Regel G auf, je Zeitscheibe, weil Kap. 3.3 genau diesen Zweck nennt, nämlich
  Klimawirkungen zu zeigen, „bei denen die ermittelten Klimarisiken noch hohen Unsicherheiten unterliegen und daher
  vorsichtig interpretiert werden sollten“ (TB6 S. 78), und das eine Aussage über das Klimarisiko ist, nicht über die
  Quellenlage der Rechnung.

## Rechenkette

Format nach Aufgabe §4, hier „Zelle → Stufe“ statt „Zahl × Faktor“, weil Regel G übernimmt und nicht rechnet. Es gibt
keinen Euro-Betrag am Ende: Die Gewissheit steht neben dem Betrag und ändert ihn nicht. Beispiel: #95 Hitzebelastung.

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
`docs/methodik/95_hitzebelastung.md` (Kap. 7). Gezählt: 19 Blöcke, davon 8 mit Kennzeichnung `quelle`,
8 `abschaetzung_kap3`, 3 `berechnet`. Das sind 8 von 19 = 42 % mit Quelle, mit den berechneten 11 von 19 = 58 %.
Nach der alten Regel stünde #95 damit auf „gering“ (42 % liegt unter 0,5) oder auf „mittel“ (58 %), je nachdem, wie
man „berechnet“ zählt, und die Registry kommt mit 25 von 26 und 8 von 8 Parametern zu „mittel“ und „hoch“. Die KWRA
sagt zur Mitte „hoch“. Das ist der Grund, warum die Zählung keine Gewissheit ist.

Beispiel-Block `rechenkette_gewissheit_95`, aus dem Stamm des Produkt-Repos ausführbar (am 25.09.2026 gelaufen,
Ausgabe darunter):

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
assert gewissheit(2085) == "mittel"

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
assert len(kz) == 19
assert zaehlung == {"abschaetzung_kap3": 8, "berechnet": 3, "quelle": 8}
assert round(8 / 19, 2) == 0.42 and round(11 / 19, 2) == 0.58

print("Mitte:", mitte, "| Ende:", ende, "| heutiges Klima:", HEUTIGES_KLIMA)
print("2025:", zeitreihe[2025], "| 2060:", zeitreihe[2060], "| 2061:", zeitreihe[2061], "| 2065:", zeitreihe[2065])
print("Quellenlage (nur Vergleich):", zaehlung)
```

Ausgabe:

```
Mitte: hoch | Ende: mittel | heutiges Klima: in der KWRA nicht ausgewiesen
2025: hoch | 2060: hoch | 2061: mittel | 2065: mittel
Quellenlage (nur Vergleich): {'abschaetzung_kap3': 8, 'berechnet': 3, 'quelle': 8}
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
Umsetzung 0,5 mit Band 0,33–0,5, Entwicklung 0,1 mit Band 0,05–0,2. Verworfen, je mit einem Satz:

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
17. **Eine Entwicklungsschwelle über 0,25** (bis 0,5, „weiterreichend erreicht das Ziel“) ist verworfen, weil das
    Produkt nur einen Maßnahmenraum kennt und dann alle 26 Klimawirkungen, auch #95 und #98, in „Innovation“ fielen
    (12 statt 15 Treffer).
18. **Regel G allein, wo Tabelle 24 keinen Wert hat**, ist verworfen, weil die Bedingung der KWRA beide Teile verlangt
    und Regel G allein die Gewissheit, wie gerechnet, zu oft als ausreichend zeigt.
19. **Den Mittelwert als Widerspruch zu Regel G** zu werten ist verworfen: Die Zeile „kein Mittelwert“ unter „Verhältnis
    zur KWRA-Einstufung“ und Punkt 5 gelten für die angezeigte Gewissheit einer Klimawirkung, und der Mittelwert hier
    ist die Regel der KWRA selbst (S. 141) für eine Ja-Nein-Frage, die das Produkt nicht als Stufe zeigt.

Änderungen an Abschnitten aus Schritt 1: Unter „Folgegrößen“ ist die Klammer „zweiter Teil, Zeitscheibe und Schwellen
folgen in Schritt 2“ durch das Ergebnis ersetzt, weil Schritt 2 sie beantwortet. Unter „Quellen“ sind die in Schritt 2
gelesenen Fundstellen ergänzt, damit jede Seitenangabe dieser Datei dort steht. Sonst ist nichts aus Schritt 1
geändert.

## Befunde an Berichte

Keine.

Verglichen am 25.09.2026: Bericht 95, Abschnitt „Risiko ohne (weitere) Anpassung“, Absatz „Gewissheit der
KWRA-Bewertung“, nennt Mitte **hoch** und Ende **mittel** mit Fundstelle Mappe Zeile 97, Spalten S und T, und TB6
Tabelle 1, S. 41; Quelle [68] nennt dieselbe Tabelle und Seite. Die Zellen S97 = „hoch“ und T97 = „mittel“ stimmen
damit überein, ebenso das Bild von TB6 Tabelle 1, S. 41. Der dort genannte Mittelwert 3,5 über beide Zeitscheiben
stimmt mit TB6 S. 78–79.

## Quellen

- **[TB6]** Umweltbundesamt (Hrsg.): Klimawirkungs- und Risikoanalyse 2021 für Deutschland, Teilbericht 6: Integrierte
  Auswertung – Klimarisiken, Handlungserfordernisse und Forschungsbedarfe. Reihe Climate Change, Dessau-Roßlau,
  Oktober 2021. Lokale Kopie `docs/KWAR/kwra2021_teilbericht_6_integrierte_auswertung_bf_211027_0.pdf`. Verwendet:
  Kap. 2.1, S. 35 mit Fußnote 3; Tabelle 1, S. 36–41 (Hitzebelastung S. 41); Kap. 3.3, S. 78–82 mit Fußnote 18;
  Tabelle 17, S. 80; Kap. 6.2, S. 141. Schritt 2: Kap. 5.1, S. 112–123; Kap. 5.2 mit Tabelle 24, S. 123–129
  (Tabelle 24 als Bild gelesen); Kap. 6.1 mit Tabelle 25, S. 136–140; Kap. 6.2, S. 140–145 mit Fußnoten 28 und 29 und
  Tabelle 27, S. 142 (als Bild gelesen).
- **[Mappe, Schritt 2]** Blatt „Klimawirkungen“, Spalten S, T, V und Y (Kopf Y2 „Wirksamkeit APA III – Mitte
  pessim.“) für die 29 Klimawirkungen aus Tabelle 27.
- **[Mappe]** `docs/KWAR/KWRA-2021_Klimawirkungen.xlsx`, Blatt „Klimawirkungen“, Zeile 97, Zellen A97, D97, S97, T97,
  AJ97; Kopfzellen S2, T2.
- **[Bericht 95]** `docs/methodik/95_hitzebelastung.md`, Abschnitt „Risiko ohne (weitere) Anpassung“, Absatz
  „Gewissheit der KWRA-Bewertung“; Kap. 6 „Szenario-Anwendung & Modellgrenzen“; Kap. 7 „Parameter-Blöcke“.
- **[Produkt]** `backend/app/services/gewissheit.py`, `charakterisierung.py`, `unsicherheits_zusammenschau.py`;
  `backend/app/api/routes/assessment.py`; `docs/KONFORMITAET_CHECKLISTE.md`, „Gegenprobe Zeile 8“.
