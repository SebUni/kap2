# #98 — Herleitung von k_UV (Befunde 230/238/245/252/255/256)

Erzeugt von `backend/scripts/kalibrierung/k_uv_herleitung.py`. Fenster **1997–2022**, identisch zu Lorenz u. a. 2024.

## 1 Die Skalen unterscheiden sich metrikabhängig

Messzelle = DWD-Station **1117 Bochum**, an der die Quelle Globalstrahlung und Sonnenscheindauer misst (die UV-Dosis wird 10 km entfernt in Dortmund gemessen).

| Größe | Station (Lorenz, Tab. 4) | 1-km-Raster an der Messzelle | Raster ÷ Station |
|---|---|---|---|
| Globalstrahlung (GR_int) | 4.6 %/Dek. | 4.51 %/Dek. | **0.98** |
| Sonnenscheindauer (SunD) | 11.3 %/Dek. | 6.62 %/Dek. | **0.59** |

Das Raster gibt die **Globalstrahlung** nahezu exakt wieder, die **Sonnenscheindauer** nur zu rund 60 %. Eine direkte Paarung Stations-Zähler ÷ Raster-SSD-Nenner wäre deshalb ein Kategorienfehler (§3.9). Die Quelle nennt den physikalischen Grund: GR ist von AOD und Bewölkung bestimmt, SunD allein von Bewölkung — und die Rasterinterpolation glättet die Schwellenwert-Größe SunD stärker.

## 2 Die Brücke

$$ k_{UV} = \frac{\Delta Dosis}{\Delta Global}\bigg|_{Station} \times \frac{\Delta Global}{\Delta SSD}\bigg|_{Raster} $$

- **Stationsquotient = 4.9 ÷ 4.6 = 1.0652** — beide Werte publiziert (Tab. 2 bzw. Tab. 4). Das ist die quantitative Fassung der Abstract-Aussage 》Global radiation increases similarly to the UV data《.
- **Rasterquotient = 0.6683**, gewichtet mit ``Baseline-Fällen × ΔSSD_Normalperiode`` über 10.682 Gemeindepunkten, also mit genau der Größe, die das Produktionsmodell summiert (Befund 266/278; Kopfgewichtung ergäbe 0.6644, MM allein 0.6674, C44 allein 0.6689 — geführt wird das €-gewichtete Mittel bei einem MM-Anteil von 0.4316 — hergeleitet, nicht gesetzt (Befund 290) —, Restdifferenz < 0,2 % als Näherung gekennzeichnet). An der Messzelle allein: 0.6811. Mit dem SSD-**Trend** gewichtet ergäbe sich 0.6320 (+5.7%); die beiden SSD-Felder korrelieren nur mit r = 0.24, die Wahl des Gewichts ist also nicht neutral.
- **k_UV = 1.0652 × 0.6683 = 0.7119**

Der bevölkerungsgewichtete Bundeswert ist der richtige Bezug für die Bundessumme — dieselbe Logik, die Befund 223 für ΔSSD festgestellt hat.

## 3 Band aus den publizierten Standardfehlern

SE(Dosis) = 1.8 auf 4.9 = 36.7%; SE(Global) = 1.5 auf 4.6 = 32.6%. Unkorreliert fortgepflanzt: **±49.1%** (1 σ) ⇒ Band **0.3622–1.0616**.

Das ist die **konservative** Fassung: Beide Reihen sind bewölkungsgetrieben und damit positiv korreliert, die reale Unsicherheit des Quotienten ist kleiner. Bis Rev. 6 kam das Band aus Min/Max über acht handverlesene Städte — eine *räumliche* Streuung, fälschlich als Band der *Bundes*summe gebucht (Befunde 255/256).

## 4 Räumliche Streuung = Modellgrenze, nicht Bundesband

Verteilung über 10.682 Gemeindepunkte mit einem SSD-Trend ≥ 1 %/Dekade (darunter wird der Quotient numerisch instabil; 57 Punkte ausgenommen):

- 5. Perzentil: **0.3225**
- 10. Perzentil: **0.3693**
- Median: **0.6305**
- 90. Perzentil: **1.0046**
- 95. Perzentil: **1.1671**
- bevölkerungsgewichtet (Bundeswert): **0.6683**

Über die Gemeindepunkte streut der Rasterquotient erheblich. Das verschiebt **einzelne Kommunen** gegeneinander, nicht die Bundessumme — es gehört deshalb in die Modellgrenzen (wie die Binnenheterogenität des Bandes 20–64), nicht in das Sanity-Band.

## 5 Verworfene Ketten

- NRW-Gebietsmittel 5.81 %/Dek. ⇒ 0.8434 (bis Rev. 3): Punkt-Zähler gegen Landesflächenmittel (Befund 230).
- Raster-SSD an der Messzelle ⇒ 0.7405 (Rev. 4): Zähler weiter Station — halber Mismatch (Befund 238).
- Stationsquotient 0,867 aus 》roughly twice《 ⇒ 0,5782 (Rev. 5) bzw. 1,0 aus 》similarly《 ⇒ 0,6667 (Rev. 6): beides Ersatzkonstruktionen für eine Größe, die der Volltext beziffert (Befund 252).

## 6 Ozon im Messfenster (Befunde 246/258)

Tab. 4 weist für Bochum einen **signifikanten** sommerlichen Gesamtozon-Trend von **-0.9 %/Dekade** (Apr–Sept, CI −1,75…−0,03) aus. Das Messfenster liegt also **nicht** in einer Ozon-Erholung; die Ozonentwicklung wirkte dosiserhöhend. Richtung der Zeitinvarianz-Annahme damit: ΔDosis eher **überschätzt**.
