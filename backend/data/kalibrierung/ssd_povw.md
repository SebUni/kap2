# #98 — Bevölkerungsgewichtete SSD-Normalperiodenänderung (Befund 223)

Erzeugt von `backend/scripts/kalibrierung/ssd_povw.py`. Gewichtung auf der
**Gemeindepunkt-Ebene** (§3.4 ausdrücklich zulässig; kein 100-m-Vollraster-Lauf):
10.824 amtliche Gemeindepunkte (BKG VG250 `vg250_pk`, Gebietsstand 01.01.2025)
mit Zensus-2022-Gemeindebevölkerung; SSD über die **Produktfunktion**
`ssd_normalperioden.ssd_at` gelesen (Kalibriermodell = Produktionsmodell).

## 1 Nationale ΔSSD

| Aggregation | ΔSSD DE | Bezug |
|---|---|---|
| DWD-Gebietsmittel (**flächen**gewichtet, Anlage [69]) | **7.82 %** | bisheriger Berichtswert |
| Gemeindepunkte, ungewichtet | 7.76 % | Kontrolle: nahe am Flächenmittel |
| Gemeindepunkte, **bevölkerungsgewichtet** | **8.51 %** | wirksamer Wert des Produktionsmodells |

Korrektur gegenüber dem Flächenmittel: **+8.8%**.
Ursache: Die einwohnerstarken Länder (NRW, Hessen, Niedersachsen) haben
überdurchschnittliche Zuwächse, die dünn besiedelten Küsten- und
Nordostländer unterdurchschnittliche.

## 2 Je Region und Bundesland

| Gebiet | Gemeinden | Bevölkerung | ΔSSD bev.-gew. | ΔSSD Punktmittel |
|---|---|---|---|---|
| deutschland | 10.824 | 82.338.336 | **8.51 %** | 7.76 % |
| land:Baden-Württemberg | 1.097 | 11.033.438 | **8.42 %** | 8.25 % |
| land:Bayern | 2.167 | 13.006.330 | **7.21 %** | 7.09 % |
| land:Berlin | 1 | 3.586.909 | **7.17 %** | 7.17 % |
| land:Brandenburg | 412 | 2.515.450 | **6.96 %** | 6.77 % |
| land:Bremen | 2 | 684.981 | **8.29 %** | 8.43 % |
| land:Hamburg | 1 | 1.800.014 | **8.73 %** | 8.73 % |
| land:Hessen | 425 | 6.199.824 | **8.57 %** | 8.75 % |
| land:Mecklenburg-Vorpommern | 716 | 1.534.682 | **4.79 %** | 4.39 % |
| land:Niedersachsen | 950 | 7.918.440 | **9.09 %** | 9.00 % |
| land:Nordrhein-Westfalen | 395 | 17.809.211 | **9.63 %** | 9.29 % |
| land:Rheinland-Pfalz | 2.266 | 4.085.145 | **8.77 %** | 8.60 % |
| land:Saarland | 52 | 1.003.273 | **9.42 %** | 7.31 % |
| land:Sachsen | 417 | 4.022.361 | **10.55 %** | 9.30 % |
| land:Sachsen-Anhalt | 218 | 2.142.156 | **12.09 %** | 12.22 % |
| land:Schleswig-Holstein | 1.101 | 2.890.526 | **5.29 %** | 5.83 % |
| land:Thüringen | 604 | 2.105.596 | **7.85 %** | 8.05 % |
| region:mitte | 4.790 | 43.469.925 | **9.15 %** | 8.65 % |
| region:nord | 2.770 | 14.828.643 | **7.82 %** | 6.55 % |
| region:sued | 3.264 | 24.039.768 | **7.77 %** | 7.48 % |

## 3 Wirkung auf die Bundessummen (Basiswerte, L̄ nach Befund 224)

| Größe | flächengewichtet (Vergleich) | **bevölkerungsgewichtet (Basiswert)** | Δ |
|---|---|---|---|
| ΔDosis DE | 4.1752% | **4.5436%** | +8.8% |
| ΔF MM | 673 | **733** | +8.8% |
| ΔF C44 | 16.852 | **18.339** | +8.8% |
| YLL | 1.291 | **1.404** | +8.8% |
| € Mio | 311 | **339** | +8.8% |

Nicht zugeordnet: 96 Gemeindepunkte ohne Zensus-Bevölkerung, 29 ohne Rasterwert (beide gehen nicht in die Gewichtung ein).