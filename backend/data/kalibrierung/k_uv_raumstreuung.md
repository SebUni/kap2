# #98 — Räumliche Streuung von k_UV (Befund 449)

Teil von Anlage [73]. Erzeugt von `backend/scripts/kalibrierung/k_uv_raumstreuung.py`; die Kreiswerte stehen in `backend/data/kalibrierung/k_uv_raumstreuung.csv`. Grundlage ist die Festlegung der Gesamtschau zu T-1115 vom 27.09.2026 (»Räumliche Streuung von k_UV (Befund 449): Messung und Entscheidungsregel«). Punktmenge, Stabilitätsausschluss und Gewicht sind dieselben wie beim Bundeswert in `k_uv_herleitung.md`; die Leser der DWD-Raster sind aus `k_uv_herleitung.py` übernommen, dessen Anlage bleibt unverändert.

Gefragt ist, ob die Streuung des Rasterquotienten q = ΔGlobalstrahlung ÷ ΔSonnenscheindauer über die Gemeindepunkte ein räumliches Muster ist oder Schätzrauschen zweier Trends über 26 Jahre. Nur ein beständiges Muster könnte die Reihenfolge der Kommunen verändern, wenn das Modell statt des Bundeswerts einen Wert je Kreis nähme.

**Abweichung vom Lauf vom 01.09.2026.** Die Gemeindepunkte kommen aus `backend/.cache/60_stichprobe/DE_VG250.gpkg`, Ebene `vg250_pk` (10.939 Punkte, Gebietsstand 2026); `backend/data/vg250/` gibt es auf dem Server nicht. Einwohner und 65+-Anteil je Gemeinde kommen aus `backend/data/kalibrierung/zensus2022_demografie_ab65.csv` über `zensus_loader.demografie_zeile_ab65` und `anteil_ab65_gemeinde` mit dem Anteil 2/7 der Gruppe 60–66, der Regel des Produkts (#95 §3.3). Sie ersetzen `backend/data/lite/zensus_gemeinde.json`, das auf dem Server fehlt. Deshalb weicht die Zahl der Punkte vom Lauf vom 01.09.2026 ab (dort 10.853 mit Einwohnerzahl). Ob der Bundeswert trotzdem derselbe ist, prüft Abschnitt 2.

## 1 Punktmengen-Kette

- **10.939** Gemeindepunkte in `vg250_pk`
- **10.743** davon mit eigener Gemeindezeile im Zensus 2022, also mit Einwohnerzahl und 65+-Anteil. Ohne Gewicht bleiben 196 Punkte: 195 mit nur einer Kreiszeile, davon 190 gemeindefreie Gebiete; 1 ohne jede Zeile. Die Kreiszeile nennt den 65+-Anteil, aber nicht die Einwohner der Gemeinde. Umgekehrt haben Gemeinden des Zensus mit zusammen 130.072 Einwohnern (0,16 %) keinen Punkt im Gebietsstand 2026, weil sie seit 2022 in anderen Gemeinden aufgegangen sind.
- **10.630** davon mit auswertbaren Trendreihen in beiden Rastern (endlicher SSD- und Globalstrahlungstrend 1997–2022, SSD-Trend > 0, ΔSSD der Normalperioden > 0)
- **10.573** nach dem Stabilitätsausschluss (SSD-Trend ≥ 1 %/Dekade) — die Menge, über die alle folgenden Zahlen laufen. Sie liegen in **399** Kreisen und **16** Ländern. 8 dieser Punkte liegen in mindestens einem Jahr auf einer Rasterzelle ohne Wert (NODATA); die Regel des Bundeswerts schließt sie nicht aus, sie bleiben deshalb in der Menge.

## 2 Reproduktion des Bundeswerts

q_Bund = 0,4316 × 0,6664 (MM) + 0,5684 × 0,6676 (C44) = **0,6671**. Die Anlage `k_uv_herleitung.md` nennt 0,6683; die Abweichung ist −0,0012 und liegt innerhalb der Toleranz von 0,003. Die folgenden Zahlen gelten damit.

## 3 Kreis- und Landeswerte

q je Kreis (AGS Stellen 1–5) und je Land ist das gewichtete Mittel der Punktquotienten, mit demselben Gewicht wie der Bundeswert: Baseline-Fälle × ΔSSD der Normalperioden, als €-gewichtetes Mittel aus MM und C44. Über alle Punkte ergibt dieses Mittel genau q_Bund.

Perzentile der 399 Kreiswerte, ungewichtet über die Kreise (lineare Interpolation):

| Perzentil | q je Kreis | relativ zu q_Bund |
|---|---|---|
| 5. | 0,3598 | −46 % |
| 10. | 0,4127 | −38 % |
| 50. (Median) | 0,6553 | −2 % |
| 90. | 0,9536 | +43 % |
| 95. | 1,1260 | +69 % |

Zwischen dem 10. und 90. Perzentil liegen die Kreiswerte bei −38 % … +43 % um q_Bund, zwischen dem 5. und 95. Perzentil bei −46 % … +69 %. Zum Vergleich die Gemeindepunkte (`k_uv_herleitung.md`, Abschnitt 4): 5./95. Perzentil 0,3225/1,1671.

Die 16 Landeswerte:

| Land | Punkte | q je Land | relativ zu q_Bund |
|---|---|---|---|
| Schleswig-Holstein | 998 | 0,9920 | +49 % |
| Hamburg | 1 | 0,8760 | +31 % |
| Niedersachsen | 934 | 0,7024 | +5 % |
| Bremen | 2 | 0,5987 | −10 % |
| Nordrhein-Westfalen | 395 | 0,6197 | −7 % |
| Hessen | 420 | 0,6318 | −5 % |
| Rheinland-Pfalz | 2.297 | 0,4897 | −27 % |
| Baden-Württemberg | 1.088 | 0,4800 | −28 % |
| Bayern | 2.041 | 0,6816 | +2 % |
| Saarland | 52 | 0,6351 | −5 % |
| Berlin | 1 | 0,9324 | +40 % |
| Brandenburg | 412 | 0,8326 | +25 % |
| Mecklenburg-Vorpommern | 716 | 0,9821 | +47 % |
| Sachsen | 416 | 0,7568 | +13 % |
| Sachsen-Anhalt | 218 | 0,7982 | +20 % |
| Thüringen | 582 | 0,7861 | +18 % |

## 4 Rangtreue und Zeitstabilität

Die Rangkorrelation nach Spearman vergleicht zwei Reihenfolgen derselben Kreise: 1 heißt gleiche Reihenfolge, 0 kein Zusammenhang, −1 umgekehrte Reihenfolge.

- **Rangtreue: 0,60** über 399 Kreise. Verglichen wird die Reihenfolge der Kreise nach dem Euro-Betrag je Einwohner, proportional zu Σ (Gewicht × q) ÷ Einwohner, einmal mit q_Bund für alle Kreise und einmal mit q je Kreis. Einwohner sind die der Punkte in der Menge aus Abschnitt 1.
- **Zeitstabilität: 0,12** über 398 Kreise. Verglichen wird q je Kreis aus den Trends 1997–2009 mit q je Kreis aus den Trends 2010–2022. q ist dabei jeweils der Quotient der gewichteten Kreistrends (Globalstrahlung ÷ Sonnenscheindauer), mit dem Gewicht aus Abschnitt 3. Einbezogen sind die Kreise mit positivem SSD-Trend in beiden Hälften; 1 Kreis fällt deshalb heraus.

## 5 Entscheidungsregel und Schwellen

Zweig 1 gilt bei Rangtreue ≥ 0,90: Der Bundeswert bleibt, denn die Vereinfachung ändert die Reihenfolge der Kreise nicht wesentlich. Zweig 2 gilt bei Rangtreue < 0,90 und Zeitstabilität < 0,50: Der Bundeswert bleibt, weil die Kreiswerte über die Zeit nicht stabil und damit nicht belegt sind. Zweig 3 gilt bei Rangtreue < 0,90 und Zeitstabilität ≥ 0,50: Die Vereinfachung stellt die Reihenfolge der Kommunen falsch dar (E3), und k_UV wird regional, als eigener Methodik-Schritt.

Die Schwellen 0,90 und 0,50 sind Setzungen von KAP3 (Festlegung vom 27.09.2026). Angewandt wird die Regel auf die Werte, wie sie hier auf zwei Stellen gerundet stehen. Mit anderen Schwellen gälte:

| Schwelle Rangtreue | Zeitstabilität 0,40 | Zeitstabilität 0,50 | Zeitstabilität 0,60 |
|---|---|---|---|
| 0,85 | Zweig 2 | Zweig 2 | Zweig 2 |
| 0,90 | Zweig 2 | Zweig 2 | Zweig 2 |
| 0,95 | Zweig 2 | Zweig 2 | Zweig 2 |

Es gilt **Zweig 2**. Es entscheidet das Ergebnis der Regel; eine Prüfung wendet sie an und entscheidet sie nicht neu.

## 6 Ergebnis

Reproduktion: q_Bund = 0,6671

Rangtreue: Rangkorrelation = 0,60

Zeitstabilität: Rangkorrelation = 0,12

Zweig: 2
