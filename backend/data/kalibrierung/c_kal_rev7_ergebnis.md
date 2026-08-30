# Rev.-7-Kalibrierlauf #95 — bevölkerungsgewichtete Temperaturen

Gemeinden mit Zensus-Bevölkerung: **10853** · Daten-Pins: zensus_gemeinde.json sha256:124fd7a7a15b · DE_VG250.gpkg sha256:f229550c8018

## Temperatur-Offsets (bevölkerungsgewichtet − Flächenmittel, Ø 1992–2024):
- Baden-Württemberg: +0.84 K
- Bayern: +0.57 K
- Berlin: +0.85 K
- Brandenburg: +0.20 K
- Bremen: +0.07 K
- Hamburg: +0.15 K
- Hessen: +1.05 K
- Mecklenburg-Vorpommern: +0.01 K
- Niedersachsen: +0.16 K
- Nordrhein-Westfalen: +0.50 K
- Rheinland-Pfalz: +0.73 K
- Saarland: +0.24 K
- Sachsen: +0.43 K
- Sachsen-Anhalt: +0.19 K
- Schleswig-Holstein: +0.11 K
- Thüringen: +0.29 K
- **Deutschland (bevölkerungsgewichtet): +0.53 K** (Rev.-6-Abschätzung war +0,2…+0,4 K)

## Lauf A — Basis Rev. 7 (bevölkerungsgewichtete Reihen, ERF unverändert):
- **fenster_2012_2024**: c_kal = 0.661 · R² = 0.649 · 8/13 Jahre im RKI-PI
- **vollreihe_1992_2024**: c_kal = 0.754 · R² = 0.592 · 13/26 Jahre im RKI-PI
- **vollreihe_inkl2025**: c_kal = 0.744 · R² = 0.583 · 13/27 Jahre im RKI-PI
- Holdout: Fit 1992–2015 → c = 0.913; Prüfung 2016–2024: 2/9 im PI (Abw. +9…+178 %)
- c_reg-Diagnose (Fenster): norden = 0.748, osten = 0.660, sueden = 1.225, westen = 0.769
- **Prüfstein (nationaler Skalar c = 0.661): 10/16 Länder im Band 0,75–1,35** · mit c_reg-Diagnosefaktoren: 9/16
- Altersverteilungs-Ist: 6.2 / 12.7 / 24.8 / 56.3 % (RKI 6,5/12,9/25,2/55,5; Toleranz ±5 pp)
- Berlin 2018, 85+ (nationaler Skalar): 251 je 100.000 (RKI-Referenz 260–320)
- Rest-Bias UHI-Konvexität 2018: ×1.023 (σ = 0,5 K, mittelwerttreu — verbleibende dokumentierte Näherung)
- Rest-Bias UHI-Konvexität 2022: ×1.024 (σ = 0,5 K, mittelwerttreu — verbleibende dokumentierte Näherung)

## Lauf B — regionale ERF-Nachschätzung (β-Skalar je N/M/S; Fit OHNE Validierungsjahre 2018/2019/2022 — Holdout):
- Fit-Set (signifikante Land-Jahre 2012–2024 ohne 2018/19/22): nord = 0, mitte = 12, sued = 7
- Zielfunktionsprofil s_nord: 0.7:1.38 · 0.8:1.38 · 0.9:1.38 · 1.0:1.38 · 1.1:1.38 · 1.2:1.38 · 1.3:1.38
- Zielfunktionsprofil s_mitte: 0.7:2.44 · 0.8:1.76 · 0.9:1.46 · 1.0:1.38 · 1.1:1.46 · 1.2:1.62 · 1.3:1.85
- Zielfunktionsprofil s_sued: 1.35:1.66 · 1.45:1.51 · 1.55:1.42 · 1.65:1.38 · 1.75:1.41 · 1.85:1.48 · 1.95:1.60
- Identifikation: s_Nord flach (nicht identifizierbar, bleibt 1,0); s_Mitte-Optimum = 1,0 (bleibt 1,0); nachgeschätzt nur s_Süd (diagnostizierte Schieflage, klar identifiziert)
- Nachschätzung (Fit ohne Hitzejahre): s_Nord = 1.00 · s_Mitte = 1.00 · s_Süd = 1.65 ⇒ β_85+ = 0.0634 / 0.0625 / 0.0876 K⁻¹
- Voll-Holdout-Sensitivität (Befund 78): Niveau-Skalar ohne 2018/19/22 gefittet → c = 0.567; Prüfstein damit **12/16** (vollständig out-of-sample)
- c_kal-Band-Stütze (Befund 80): s_Süd = 1.45 → c = 0.604
- c_kal-Band-Stütze (Befund 80): s_Süd = 1.85 → c = 0.559
- **fenster_2012_2024**: c_kal = 0.581 · R² = 0.650 · 8/13 Jahre im RKI-PI
- **vollreihe_1992_2024**: c_kal = 0.660 · R² = 0.589 · 16/26 Jahre im RKI-PI
- **vollreihe_inkl2025**: c_kal = 0.651 · R² = 0.580 · 16/27 Jahre im RKI-PI
- Holdout: Fit 1992–2015 → c = 0.792; Prüfung 2016–2024: 2/9 im PI (Abw. +7…+185 %)
- c_reg-Diagnose (Fenster): norden = 0.748, osten = 0.660, sueden = 0.716, westen = 0.769
- **Prüfstein (nationaler Skalar c = 0.581): 12/16 Länder im Band 0,75–1,35** · mit c_reg-Diagnosefaktoren: 9/16
- Altersverteilungs-Ist: 6.3 / 12.6 / 24.7 / 56.4 % (RKI 6,5/12,9/25,2/55,5; Toleranz ±5 pp)
- Berlin 2018, 85+ (nationaler Skalar): 221 je 100.000 (RKI-Referenz 260–320)

## Ergebnis: Prüfstein (nationaler Skalar) = **12/16** (Anforderung ≥ 11/16) — BESTANDEN; ERF-Skalare {'nord': 1.0, 'mitte': 1.0, 'sued': 1.65}
