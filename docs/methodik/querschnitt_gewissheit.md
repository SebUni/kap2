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

## Folgegrößen

- **Gruppen der Charakterisierung (Konformitätszeile 7, `backend/app/services/charakterisierung.py`):** Sie setzen
  auf der Gesamtgewissheit der KWRA auf, die Kap. 6.2 „aus der Kombination der Gewissheit der Bewertung des
  Klimarisikos ohne Anpassung sowie der Gewissheit der Bewertung der Anpassungskapazität“ bildet (TB6 S. 141), deren
  erster Teil die Gewissheit nach Regel G ist und nicht die Quellenlage, weil die Gruppen „unter Unsicherheit“ fragen,
  wie sicher die Aussage über Risiko und Anpassung ist, und nicht, ob die Rechnung von KAP3 Quellen hat (zweiter Teil,
  Zeitscheibe und Schwellen folgen in Schritt 2).
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
  Tabelle 17, S. 80; Kap. 6.2, S. 141.
- **[Mappe]** `docs/KWAR/KWRA-2021_Klimawirkungen.xlsx`, Blatt „Klimawirkungen“, Zeile 97, Zellen A97, D97, S97, T97,
  AJ97; Kopfzellen S2, T2.
- **[Bericht 95]** `docs/methodik/95_hitzebelastung.md`, Abschnitt „Risiko ohne (weitere) Anpassung“, Absatz
  „Gewissheit der KWRA-Bewertung“; Kap. 6 „Szenario-Anwendung & Modellgrenzen“; Kap. 7 „Parameter-Blöcke“.
- **[Produkt]** `backend/app/services/gewissheit.py`, `charakterisierung.py`, `unsicherheits_zusammenschau.py`;
  `backend/app/api/routes/assessment.py`; `docs/KONFORMITAET_CHECKLISTE.md`, „Gegenprobe Zeile 8“.
