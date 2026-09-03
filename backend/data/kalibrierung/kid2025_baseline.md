# #98 Baseline-Verankerung und Struktur-Validierung (KID 2025)

Erzeugt von `backend/scripts/kalibrierung/kid2025_baseline.py`. Anker = **Mittel 2021–2023**, weil die abgelesenen altersspezifischen Raten laut Abbildungstitel (Abb. 3.13.2 / 3.14.3) über genau diese drei Jahre gepoolt sind (Befund 220).

## 1 Anker-Zeitreihe und Normierungsskalare

| Größe | MM (C43) | C44 |
|---|---|---|
| Neuerkrankungen 2021 | 26.140 | 236.670 |
| 2022 | 27.040 | 243.430 |
| 2023 | 27.430 | 242.820 |
| Anker = Mittel 2021–2023 | **26.870** | **240.973** |
| Sterbefälle, Mittel | 3.081.0 | 1.261.7 |
| Modell-Rohfälle (Ablesekette × Bev. 31.12.2023) | 26.837 | 243.158 |
| c_kal = Anker ÷ Rohfälle | **1.0012** | **0.9910** |
| λ = Sterbefälle ÷ Neuerkrankungen | **0.11466** | **0.00524** |
| L̄ (sterbefallgewichtet, Sterbetafel 2022/2024) | **10.4569** J. | **5.4787** J. |

## 2 Struktur-Validierung: altersstandardisierte Rate (Befund 214)

Out-of-sample gegenüber c_kal: Die Normierung fittet die **rohe** Rate; die ASR gewichtet nach dem alten Europastandard und reagiert deshalb auf Fehler im Altersprofil, die die rohe Rate unberührt lassen.

**Toleranz hergeleitet** (Befund 229a, nicht mehr gesetzt): ±15 % je Einzelablesung; die Fehlerfortpflanzung des gewichteten Mittels ergibt im ungünstigsten der vier Reihen σ = ±5.07%. Abnahmetoleranz = **2σ = ±10.1%** — die bis Rev. 2 gesetzten ±10 % waren also sachlich richtig bemessen, nur unbelegt. Weil das Ist-Ergebnis mit 0.4σ weit darunter liegt, gilt zusätzlich die engere **Regressionsschranke ±3 %** (Golden-Test) gegen eine künftige Verschlechterung der Ablesekette.

| Entität | Geschlecht | ASR Modell | ASR amtlich (Mittel 2021–2023) | Abweichung | Verdikt |
|---|---|---|---|---|---|
| MM | frauen | 20.95 | 20.93 | +0.1% | bestanden |
| MM | maenner | 22.79 | 22.70 | +0.4% | bestanden |
| C44 | frauen | 144.28 | 141.87 | +1.7% | bestanden |
| C44 | maenner | 177.38 | 174.07 | +1.9% | bestanden |

Größte Abweichung **1.9%** — Toleranz ±10.1% eingehalten.

**Reichweite der Prüfungen (Befund 229b).** Die ASR oben prüft die **Ablesekette** (5-Jahres-Werte). Den Schritt Ablesewerte → **Bandraten**, an dem Befund 212 den Fehler hatte, prüft sie nicht — dafür ist die rohe Rate zuständig, und zwar aussagekräftig, weil sie gegen die *unnormierte* Ablesesumme läuft (c_kal wird erst danach gebildet; der 212er-Fehler erschien dort als +5,9 %). Beide Prüfungen zusammen decken Ableseprofil **und** Aggregation ab:

- MM: Bandraten × Bevölkerung = 26.837 gegen Ablesesumme-Anker 26.870 ⇒ -0.1% (rohe Rate 32.16 vs. 32.20 je 100.000)
- C44: Bandraten × Bevölkerung = 243.158 gegen Ablesesumme-Anker 240.973 ⇒ +0.9% (rohe Rate 291.36 vs. 288.74 je 100.000)

## 2b Binnenheterogenität des Bandes 20–64 (Befund 225)

Das Modell führt 20–64 als **eine** Rate. Innerhalb des Bandes variiert die abgelesene Evidenz um mehr als eine Größenordnung; eine Kommune mit überdurchschnittlich jungem oder altem 20–64-Anteil erhält deshalb eine systematisch falsche Bandrate. Stützrechnung mit der nationalen 5-Jahres-Struktur (reproduziert die Bandraten und validiert sich damit):

Nationaler 20–34-Anteil am Band: **30.8%**. Bandraten der Stützrechnung: MM 24.4 (Bericht 24.7) · C44 123.4 (Bericht 125.9).

| 20–34-Anteil am Band | I_MM,20–64 | Δ | I_C44,20–64 | Δ |
|---|---|---|---|---|
| 24% | 26.5 | +8.5% | 138.2 | +12.0% |
| 31% | 24.4 | +0.0% | 123.4 | +0.0% |
| 40% | 21.6 | -11.6% | 103.3 | -16.3% |

Das Band trägt 45% der MM- und 25% der C44-Baseline; über die angesetzte Kreis-Spannweite ergibt das **≈ ±4 %** auf die €-Summe einer Kommune, mit dem Vorzeichen an der Altersstruktur. Die Spannweite selbst ist eine **gekennzeichnete Abschätzung** (§3.9) — eine belegte kommunale Verteilung des 20–34-Anteils liegt nicht keyless vor. Bundessumme unberührt.

## 2c Kalibrier- vs. Produktionspopulation (Befund 226)

c_kal wird gegen die **Fortschreibung 31.12.2023** gerechnet (83.456.045 Personen); das Produkt wendet die Raten auf **Zensus-2022-Zellen** an (Gemeinde-Aggregat 82.459.764). Die Produktions-Baseline liegt damit um **-1.19%** unter dem Anker — Richtung: Unterschätzung, untergrenzenkonsistent. Dokumentierte Näherung (§3.9), **nicht** „exakt“; Ersetzungspfad: c_kal gegen die amtlichen Zensus-2022-Altersgruppen, sobald sie als Tabelle vorliegen.

## 3 Bundessummen (Basiswerte)

**ΔSSD bevölkerungsgewichtet** (Anlage `ssd_povw.csv`, Gemeindepunkt-Ebene, Befund 223): **8.51 %** gegen 7.82 % flächengewichtet (+8.8%) — das Produktionsmodell summiert bevölkerungsgewichtet über Zellen (§3.4).

ΔDosis DE = 0.0851 × 0.7119 × 0.75 = **0.04544** = 4.54 %

- ΔF: **733 MM + 18.339 C44 ≈ 19.072 Fälle/Jahr**
- YLL: **1.404/Jahr**
- €: **339 Mio €₂₀₂₄/Jahr** (Behandlung 113 + Mortalität 226)

- Inzidenzanteil: MM +2.73% · C44 +7.61%
- Behandlungs-€ / KKR C43+C44 (1.823 Mio €₂₀₂₃): 6.2%
- YLL-Anteil: 1.404 / 39.130 Gesamt-Hautkrebs-YLL = 3.6%

## 4 Bänder — je Achse separat, nicht kumuliert (Befunde 221/228)

Alle Zeilen der Berichts-Tabelle §4 werden hier erzeugt — auch die beiden zentrierten bzw. geparkten Achsen, die bis Rev. 2 nur im Bericht standen (Befund 228).

| Achse | Spanne | € Mio | Δ gegen Basiswert |
|---|---|---|---|
| Basiswert | — | 339 | +0.0% |
| k_UV × a_attr (untere Kombination) | 0,3622 × 0,50 | 115 | -66.1% |
| k_UV × a_attr × c_e oben (obere Kombination) | 1,0616 × 1,00 × c_e oben | 737 | +117.6% |
| VOLY | 136.400 / 165.600 € | 304 – 345 | -10.1% … +2.0% |
| a_attr | 0,50 / 1,00 | 226 – 452 | -33.3% … +33.3% |
| BAF_MM | 0,2 / 1,0 | 241 – 436 | -28.8% … +28.8% |
| w_SCC | 0,25 / 0,50 | 339 – 370 | +0.0% … +9.3% |
| r_out (geparkt, zentriert) | q_out ∈ [0; 0,21] | 339 | +0.0% |
| v_verh (geparkt) | φ ∈ [0; 0.25] | 339 – 377 | +0.0% … +11.3% |

## 5 Beispielzelle (1.000 EW im Bundesmix, Region Mitte)

ΔDosis Mitte = 4.89 % · ΔF = 0.0094 MM + 0.2364 C44 · YLL = 0.0181 · € = **4.365 €/Jahr**
