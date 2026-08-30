# Rev.-6-Kalibrierlauf #95 — Ergebnisse

f_a-Rückrechnung (Befund 32, lineare Näherung): u65 = 0.357, a65_74 = 0.588, a75_84 = 0.631, a85p = 1.0
- **fenster_2012_2024**: c_kal = 0.905 · R² = 0.640 · 8/13 Jahre im RKI-PI
- **vollreihe_1992_2024**: c_kal = 1.042 · R² = 0.563 · 16/26 Jahre im RKI-PI
- **vollreihe_inkl2025**: c_kal = 1.029 · R² = 0.555 · 17/27 Jahre im RKI-PI

## Holdout (Befund 19): Fit 1992–2015 → c = 1.300; Prüfung 2016–2024:
| Jahr | RKI | Modell×c | Abw. % | im PI |
|---|---|---|---|---|
| 2016 | 1600 | 3304 | +106.5 | nein |
| 2017 | 1400 | 3660 | +161.5 | nein |
| 2018 | 8500 | 9963 | +17.2 | ja |
| 2019 | 6800 | 9531 | +40.2 | nein |
| 2020 | 3700 | 4855 | +31.2 | ja |
| 2021 | 1700 | 3856 | +126.8 | nein |
| 2022 | 4500 | 9446 | +109.9 | nein |
| 2023 | 3100 | 5790 | +86.8 | nein |
| 2024 | 2800 | 5483 | +95.8 | nein |
→ 2/9 Prüfjahre im RKI-Prädiktionsintervall (out-of-sample).

## Regionale c_reg (RKI-4-Zuschnitt), Signifikanzfilter BL-PI-Untergrenze > 0:
- **fenster_2012_2024**: norden = 0.841, osten = 0.879, sueden = 1.995, westen = 1.064
- **vollreihe_1992_2024**: norden = 0.886, osten = 1.101, sueden = 1.907, westen = 1.235

## Verteilungsprüfung (Σ (2018, 2019, 2022), c_reg Fenster): Verhältnis Modell/RKI je Land:
- Baden-Württemberg (sueden): 1.09
- Bayern (sueden): 1.99
- Berlin (osten): 1.28
- Brandenburg (osten): 1.93
- Bremen (norden): 1.15
- Hamburg (norden): 2.57
- Hessen (westen): 0.86
- Mecklenburg-Vorpommern (norden): 1.64
- Niedersachsen (norden): 1.24
- Nordrhein-Westfalen (westen): 1.08
- Rheinland-Pfalz (westen): 1.08
- Saarland (westen): 1.46
- Sachsen (osten): 1.36
- Sachsen-Anhalt (osten): 1.7
- Schleswig-Holstein (norden): 2.35
- Thüringen (osten): 1.31
→ **8/16 Länder im Band 0,75–1,35**

## Altersverteilungs-Ist (Befund 20, Fenster 2012–2024):
| Band | Modell % | RKI % |
|---|---|---|
| u65 | 6.2 | 6.5 |
| a65_74 | 12.7 | 12.9 |
| a75_84 | 24.8 | 25.2 |
| a85p | 56.3 | 55.5 |

## Unabhängiger Anker: Berlin 2018, Band 85+: Modell (c_reg Osten) = 232 je 100.000 (RKI-Referenz 260–320 [14]); national c = 0.905

## Befund-1-Bias-Band (Beispieljahre, Verhältnis Modellsumme):
- 2018: +0,2 K → ×1.123 · +0,4 K → ×1.256 · UHI-Streuung σ=0,5 K (mittelwerttreu) → ×1.030
- 2022: +0,2 K → ×1.127 · +0,4 K → ×1.263 · UHI-Streuung σ=0,5 K (mittelwerttreu) → ×1.031
- 2003: +0,2 K → ×1.113 · +0,4 K → ×1.238 · UHI-Streuung σ=0,5 K (mittelwerttreu) → ×1.025
