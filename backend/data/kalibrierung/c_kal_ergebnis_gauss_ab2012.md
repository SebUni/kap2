# c_kal — empirische Kalibrierung (Gauß-Quantile)

c_kal = **0.916** (Kleinste Quadrate durch Ursprung, 14 signifikante Jahre) · R² = 0.634 · 9/14 Jahre innerhalb des RKI-Prädiktionsintervalls

| Jahr | RKI [PI] | Modell roh | Modell × c_kal | Abw. % | im PI |
|---|---|---|---|---|---|
| 2012 | 1200 [100–2400] | 1248 | 1143 | -4.7 | ja |
| 2013 | 3500 [2400–4600] | 2271 | 2081 | -40.6 | nein |
| 2014 | 1400 [200–2400] | 1376 | 1260 | -10.0 | ja |
| 2015 | 7000 [5600–8100] | 3805 | 3486 | -50.2 | nein |
| 2016 | 1600 [100–2700] | 2474 | 2267 | +41.7 | ja |
| 2017 | 1400 [540–2150] | 2735 | 2506 | +79.0 | nein |
| 2018 | 8500 [7100–10100] | 7467 | 6841 | -19.5 | nein |
| 2019 | 6800 [5400–8300] | 7161 | 6560 | -3.5 | ja |
| 2020 | 3700 [2500–5000] | 3640 | 3334 | -9.9 | ja |
| 2021 | 1700 [700–2800] | 2903 | 2660 | +56.5 | ja |
| 2022 | 4500 [3100–6000] | 7054 | 6462 | +43.6 | nein |
| 2023 | 3100 [1300–4600] | 4318 | 3955 | +27.6 | ja |
| 2024 | 2800 [1200–4400] | 4083 | 3740 | +33.6 | ja |
| 2025 | 2500 [1200–3700] | 3741 | 3427 | +37.1 | ja |

## Bundesland-Verteilungsprüfung (Σ 2003, 2018, 2019, 2022, je 100.000 EW und Jahr)

| Bundesland | Region | RKI | Modell (c_kal) | Verh. | Modell (c_reg) | Verh. |
|---|---|---|---|---|---|---|
| Schleswig-Holstein | nord | 1.5 | 3.4 | 2.21 | 2.2 | 1.45 |
| Hamburg | nord | 2.6 | 5.2 | 2.03 | 3.4 | 1.33 |
| Mecklenburg-Vorpommern | nord | 5.4 | 7.5 | 1.39 | 4.9 | 0.91 |
| Bremen | nord | 5.7 | 5.7 | 1.0 | 3.7 | 0.66 |
| Bayern | sued | 5.8 | 2.9 | 0.5 | 5.3 | 0.91 |
| Niedersachsen | nord | 6.1 | 6.2 | 1.01 | 4.0 | 0.66 |
| Thüringen | mitte | 6.6 | 6.2 | 0.94 | 6.1 | 0.92 |
| Brandenburg | mitte | 7.7 | 12.3 | 1.6 | 12.1 | 1.57 |
| Sachsen | mitte | 8.3 | 9.1 | 1.11 | 9.0 | 1.09 |
| Sachsen-Anhalt | mitte | 8.9 | 11.7 | 1.32 | 11.5 | 1.3 |
| Berlin | mitte | 9.1 | 9.7 | 1.06 | 9.5 | 1.04 |
| Nordrhein-Westfalen | mitte | 9.4 | 5.9 | 0.63 | 5.8 | 0.62 |
| Baden-Württemberg | sued | 12.8 | 3.6 | 0.28 | 6.6 | 0.52 |
| Hessen | mitte | 14.4 | 6.4 | 0.45 | 6.3 | 0.44 |
| Saarland | mitte | 15.0 | 10.6 | 0.7 | 10.4 | 0.69 |
| Rheinland-Pfalz | mitte | 15.2 | 8.0 | 0.53 | 7.9 | 0.52 |

Regionale Kalibrierfaktoren c_reg (LS über Bundesland-Jahre 2012–2024): mitte = 0.900, nord = 0.601, sued = 1.683
