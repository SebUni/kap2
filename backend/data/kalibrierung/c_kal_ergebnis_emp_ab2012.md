# c_kal — empirische Kalibrierung (empirische Wochenquantile)

c_kal = **0.890** (Kleinste Quadrate durch Ursprung, 14 signifikante Jahre) · R² = 0.633 · 9/14 Jahre innerhalb des RKI-Prädiktionsintervalls

| Jahr | RKI [PI] | Modell roh | Modell × c_kal | Abw. % | im PI |
|---|---|---|---|---|---|
| 2012 | 1200 [100–2400] | 1266 | 1127 | -6.1 | ja |
| 2013 | 3500 [2400–4600] | 2328 | 2071 | -40.8 | nein |
| 2014 | 1400 [200–2400] | 1399 | 1245 | -11.1 | ja |
| 2015 | 7000 [5600–8100] | 3935 | 3501 | -50.0 | nein |
| 2016 | 1600 [100–2700] | 2545 | 2265 | +41.6 | ja |
| 2017 | 1400 [540–2150] | 2821 | 2510 | +79.3 | nein |
| 2018 | 8500 [7100–10100] | 7676 | 6830 | -19.6 | nein |
| 2019 | 6800 [5400–8300] | 7343 | 6533 | -3.9 | ja |
| 2020 | 3700 [2500–5000] | 3741 | 3328 | -10.0 | ja |
| 2021 | 1700 [700–2800] | 2971 | 2644 | +55.5 | ja |
| 2022 | 4500 [3100–6000] | 7278 | 6476 | +43.9 | nein |
| 2023 | 3100 [1300–4600] | 4461 | 3969 | +28.0 | ja |
| 2024 | 2800 [1200–4400] | 4224 | 3759 | +34.2 | ja |
| 2025 | 2500 [1200–3700] | 3864 | 3439 | +37.5 | ja |

## Bundesland-Verteilungsprüfung (Σ 2003, 2018, 2019, 2022, je 100.000 EW und Jahr)

| Bundesland | Region | RKI | Modell (c_kal) | Verh. | Modell (c_reg) | Verh. |
|---|---|---|---|---|---|---|
| Schleswig-Holstein | nord | 1.5 | 3.4 | 2.21 | 2.2 | 1.46 |
| Hamburg | nord | 2.6 | 5.2 | 2.01 | 3.4 | 1.33 |
| Mecklenburg-Vorpommern | nord | 5.4 | 7.4 | 1.38 | 4.9 | 0.91 |
| Bremen | nord | 5.7 | 5.7 | 0.99 | 3.7 | 0.66 |
| Bayern | sued | 5.8 | 2.9 | 0.5 | 5.4 | 0.92 |
| Niedersachsen | nord | 6.1 | 6.1 | 1.0 | 4.0 | 0.66 |
| Thüringen | mitte | 6.6 | 6.3 | 0.94 | 6.1 | 0.92 |
| Brandenburg | mitte | 7.7 | 12.2 | 1.58 | 12.0 | 1.55 |
| Sachsen | mitte | 8.3 | 9.1 | 1.11 | 9.0 | 1.08 |
| Sachsen-Anhalt | mitte | 8.9 | 11.6 | 1.31 | 11.4 | 1.29 |
| Berlin | mitte | 9.1 | 9.6 | 1.05 | 9.4 | 1.03 |
| Nordrhein-Westfalen | mitte | 9.4 | 5.9 | 0.63 | 5.8 | 0.62 |
| Baden-Württemberg | sued | 12.8 | 3.7 | 0.28 | 6.7 | 0.52 |
| Hessen | mitte | 14.4 | 6.4 | 0.45 | 6.3 | 0.44 |
| Saarland | mitte | 15.0 | 10.5 | 0.7 | 10.3 | 0.69 |
| Rheinland-Pfalz | mitte | 15.2 | 8.0 | 0.53 | 7.8 | 0.52 |

Regionale Kalibrierfaktoren c_reg (LS über Bundesland-Jahre 2012–2024): mitte = 0.872, nord = 0.588, sued = 1.634
