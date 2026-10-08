# #98 — Räumliche Streuung von k_UV (Befund 449)

Teil von Anlage [73]. Erzeugt von `backend/scripts/kalibrierung/k_uv_raumstreuung.py`; die Kreiswerte stehen in `backend/data/kalibrierung/k_uv_raumstreuung.csv`. Grundlage ist die Festlegung der Gesamtschau zu T-1115 vom 27.09.2026 (»Räumliche Streuung von k_UV (Befund 449): Messung und Entscheidungsregel«). Punktmenge, Stabilitätsausschluss und Gewicht sind dieselben wie beim Bundeswert in `k_uv_herleitung.md`; die Leser der DWD-Raster sind aus `k_uv_herleitung.py` übernommen, dessen Anlage bleibt unverändert.

Gefragt ist, ob die Streuung des Rasterquotienten q = ΔGlobalstrahlung ÷ ΔSonnenscheindauer über die Gemeindepunkte ein räumliches Muster ist oder Schätzrauschen zweier Trends über 26 Jahre. Ein Wert je Kreis verschöbe die Reihenfolge der Kreise auch dann, wenn er nur Rauschen ist; wie stark, misst die Rangtreue. Dass der Bundeswert die Reihenfolge der Kommunen falsch darstellt (Aufgabe §8 E3, Zweig 3 der Festlegung), belegt aber nur ein beständiges Muster; das misst die Zeitstabilität.

**Abweichung vom Lauf vom 01.09.2026.** Die Gemeindepunkte kommen aus `backend/.cache/60_stichprobe/DE_VG250.gpkg`, Ebene `vg250_pk` (10.939 Punkte, Gebietsstand 2026); der Lauf liest nicht `backend/data/vg250/`, sondern diese Datei. Einwohner und 65+-Anteil je Gemeinde kommen aus `backend/data/kalibrierung/zensus2022_demografie_ab65.csv` über `zensus_loader.demografie_zeile_ab65` und `anteil_ab65_gemeinde` mit dem Anteil 2/7 der Gruppe 60–66, der Regel des Produkts (#95 §3.3). Sie ersetzen `backend/data/lite/zensus_gemeinde.json`, die der Lauf nicht liest. Deshalb weicht die Zahl der Punkte vom Lauf vom 01.09.2026 ab (dort 10.853 mit Einwohnerzahl). Ob der Bundeswert trotzdem derselbe ist, prüft Abschnitt 2.

## 1 Punktmengen-Kette

- **10.939** Gemeindepunkte in `vg250_pk`
- **10.743** davon mit eigener Gemeindezeile im Zensus 2022, also mit Einwohnerzahl und 65+-Anteil. Ohne Gewicht bleiben 196 Punkte. 195 davon haben nur eine Kreiszeile, und die nennt den 65+-Anteil, aber nicht die Einwohner der Gemeinde:
  - 190 gemeindefreie Gebiete.
  - Gröde (01054039): Der Zensus weist ».« aus (unbekannt oder geheim).
  - 4 Gemeinden, die nach dem Zensusstichtag 15.05.2022 neu gebildet wurden und deshalb keine eigene Zeile haben (Wirksamkeit laut VG250): Jahnatal (01.01.2023), Berga-Wünschendorf (01.01.2024), Uder (01.01.2024) und Obergeckler (01.01.2025).
  - Gar keine Zeile hat Hanau (06415000), seit 01.01.2026 kreisfreie Stadt; auch für seinen Kreis 06415 hat der Zensus keine Zeile.
- Umgekehrt haben 42 Gemeinden des Zensus mit zusammen 130.072 Einwohnern (0,16 %) keinen Punkt im Gebietsstand 2026:
  - Hanau, im Zensus 06435014 mit 93.632 Einwohnern (72 %), ist nicht aufgegangen, sondern hat den Schlüssel gewechselt: Die Stadt steht seit 01.01.2026 unter 06415000, dem Punkt ohne jede Zeile. VG250 trägt für den neuen Kreis 06415 und für den abgebenden Kreis 06435 (Main-Kinzig-Kreis) dieselbe Wirksamkeit.
  - 41 Gemeinden mit 36.440 Einwohnern sind in anderen Gemeinden aufgegangen: In jedem ihrer 14 Kreise trägt VG250 für mindestens eine Gemeinde eine Änderung mit Wirksamkeit nach dem Zensusstichtag.
- **10.630** davon mit auswertbaren Trendreihen in beiden Rastern (endlicher SSD- und Globalstrahlungstrend 1997–2022, SSD-Trend > 0, ΔSSD der Normalperioden > 0)
- **10.573** nach dem Stabilitätsausschluss (SSD-Trend ≥ 1 %/Dekade) — die Menge, über die alle folgenden Zahlen laufen. Sie liegen in **399** Kreisen und **16** Ländern.
  - VG250 führt im Gebietsstand 2026 401 Kreise. Es fehlen Flensburg (01001): sein einziger Punkt mit Gewicht hat einen SSD-Trend 1997–2022 von −0,79 %/Dekade und fällt an »SSD-Trend > 0« heraus; Hanau (06415): sein Punkt hat keine eigene Gemeindezeile im Zensus und damit kein Gewicht. Beide fehlen deshalb auch in den Kreiswerten, der Rangtreue und der Zeitstabilität.
  - 8 Punkte der Menge liegen in allen 26 Jahren des Globalstrahlungsrasters auf einer Zelle ohne Wert (NODATA), im Raster der Sonnenscheindauer in keinem: Kappeln, Arnis, Keppeshausen, Ralingen, Pruchten, Wolgast, Bärenstein und Ostritz. Ihr Globalstrahlungstrend ist damit 0 und ihr Punktquotient genau 0. Das drückt die Werte ihrer 7 Kreise: Jeder liegt um den Gewichtsanteil dieser Punkte im Kreis niedriger, als er ohne sie läge, hier um 0,01–12,5 %. Im Bundeswert tragen sie 0,03 % des Gewichts. Die Regel des Bundeswerts schließt sie nicht aus; nach der Festlegung bleiben sie deshalb in der Menge.

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

Zwischen dem 10. und 90. Perzentil liegen die Kreiswerte bei −38 … +43 % um q_Bund, zwischen dem 5. und 95. Perzentil bei −46 … +69 %. Zum Vergleich die Gemeindepunkte (`k_uv_herleitung.md`, Abschnitt 4): 5./95. Perzentil 0,3225/1,1671.

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

- **Rangtreue: 0,60** über 399 Kreise, von 401 im Gebietsstand 2026; die fehlenden nennt Abschnitt 1. Verglichen wird die Reihenfolge der Kreise nach dem Euro-Betrag je Einwohner, proportional zu Σ (Gewicht × q) ÷ Einwohner, einmal mit q_Bund für alle Kreise und einmal mit q je Kreis. Einwohner sind die der Punkte in der Menge aus Abschnitt 1.
- **Zeitstabilität: 0,12** über 398 Kreise. Verglichen wird q je Kreis aus den Trends 1997–2009 mit q je Kreis aus den Trends 2010–2022. q ist dabei jeweils der Quotient der gewichteten Kreistrends (Globalstrahlung ÷ Sonnenscheindauer), mit dem Gewicht aus Abschnitt 3. Einbezogen sind die Kreise mit positivem SSD-Trend in beiden Hälften; 1 Kreis fällt deshalb heraus (Freiburg im Breisgau).

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

## Eingangsdaten

Das Skript liest drei Eingänge, die nicht im Repository liegen (`backend/.cache/` und `backend/data/dwd_cdc/` stehen in `.gitignore`), und zwei, die im Repository liegen: die Zensus-Gemeindedatei und die Normalperioden-Raster `backend/data/kalibrierung/ssd_normalperioden.npz`. Alle Pfade gelten ab dem Wurzelverzeichnis des Repositorys. Die Abrufbefehle legen die Dateien dorthin, wo `k_uv_raumstreuung.py` sie erwartet; danach läuft `python backend/scripts/kalibrierung/k_uv_raumstreuung.py` ohne Zwischenstände aus einem Probeverzeichnis. Fehlt eine Datei, die das Skript braucht, bricht es mit »BLOCKIERT: Eingang fehlt« ab, statt eine Ersatzzahl zu schreiben.

### VG250 (GeoPackage)

- **Pfad:** `backend/.cache/60_stichprobe/DE_VG250.gpkg`, Ebene `vg250_pk` (Verwaltungspunkte), Gebietsstand 2026.
- **Herkunft:** Bundesamt für Kartographie und Geodäsie (BKG), Verwaltungsgebiete 1:250 000 (VG250), Ausgabe Stand 01.01., UTM32s-GeoPackage. Bezugsadresse: https://daten.gdz.bkg.bund.de/produkte/vg/vg250_ebenen_0101/2026/vg250_01-01.utm32s.gpkg.ebenen.zip (Katalogseite: https://gdz.bkg.bund.de/index.php/default/verwaltungsgebiete-1-250-000-ebenen-stand-01-01-vg250-ebenen-01-01.html).
- **Lizenz:** Datenlizenz Deutschland – Namensnennung – Version 2.0 (dl-de/by-2-0), Quelle: BKG.
- **Abrufbefehl** (aus dem Wurzelverzeichnis des Repositorys):

```
python3 -c "import io,os,urllib.request,zipfile;z=zipfile.ZipFile(io.BytesIO(urllib.request.urlopen('https://daten.gdz.bkg.bund.de/produkte/vg/vg250_ebenen_0101/2026/vg250_01-01.utm32s.gpkg.ebenen.zip',timeout=600).read()));n=[x for x in z.namelist() if x.endswith('DE_VG250.gpkg')][0];os.makedirs('backend/.cache/60_stichprobe',exist_ok=True);open('backend/.cache/60_stichprobe/DE_VG250.gpkg','wb').write(z.read(n))"
```

- **Gemessen am 07.10.2026:** Die so entpackte Datei hat SHA-256 `25dfeadf75c9d03939144a43e0a073b5311fdf2b72ae3097e31b3abda3edefcb`, ist byteweise die Datei, die auf dem Server unter diesem Pfad liegt, und hat 10.939 Punkte in `vg250_pk`.
- **Gebietsstand beachten:** Die Anlage [72] (`ssd_povw.md`) rechnet mit dem Stand 2025 (10.949 Punkte), diese Anlage mit dem Stand 2026. Die Adresse `…/aktuell/` zeigt am 07.10.2026 auf den Stand 2026, wechselt aber mit der nächsten Ausgabe; deshalb steht oben die Jahresadresse.

### Zensus-Gemeindedatei (CSV)

- **Pfad:** `backend/data/kalibrierung/zensus2022_demografie_ab65.csv` (liegt im Repository), Spalten `schluessel, ebene, insgesamt, g60_66, ab67` je Gemeinde und Kreis, Stichtag 15.05.2022. Sie ersetzt hier die Gemeindedatei `backend/data/lite/zensus_gemeinde.json`, die [72] liest; dieser Lauf liest sie nicht, sondern die Zensus-Datei im Repository (Abschnitt »Eingangsdaten« in `ssd_povw.md`).
- **Herkunft:** Statistische Ämter des Bundes und der Länder, Zensus 2022, Regionaltabelle »Demografie«, Blatt »CSV-Demografie«: https://www.destatis.de/static/DE/zensus/gitterdaten/Regionaltabelle_Demografie.xlsx (abgerufen am 26.09.2026, laut `zensus2022_demografie_ab65.md`).
- **Lizenz:** Datenlizenz Deutschland – Namensnennung – Version 2.0 (dl-de/by-2-0), © Statistische Ämter des Bundes und der Länder.
- **Abrufbefehl** (lädt die Tabelle von destatis.de und überschreibt die Datei an ihrem Pfad):

```
python3 backend/scripts/zensus_demografie_ab65.py
```

### DWD-Globalstrahlung (Jahresraster 1997–2022)

- **Pfad:** `backend/.cache/k_uv_raumstreuung/rad/<Jahr>.asc`, 26 Dateien (1997 bis 2022). Fehlt eine, lädt der Leser `_rad_grid` aus `k_uv_herleitung.py` sie beim Lauf selbst nach.
- **Herkunft:** Deutscher Wetterdienst (DWD), Climate Data Center, Raster der jährlichen Globalstrahlung (`radiation_global`, 1 km): https://opendata.dwd.de/climate_environment/CDC/grids_germany/annual/radiation_global/ (je Jahr `grids_germany_annual_radiation_global_<Jahr>.zip` mit einer `.asc`-Datei).
- **Lizenz:** Geodatennutzungsverordnung (GeoNutzV), Datenlizenz Deutschland – Zero – Version 2.0 (dl-de/zero-2-0), laut Quellenverzeichnis des Produkts (`DWD_CDC_Globalstrahlung_Raster`).
- **Abrufbefehl** (aus dem Wurzelverzeichnis des Repositorys):

```
python3 -c "import io,os,urllib.request,zipfile;D='backend/.cache/k_uv_raumstreuung/rad';B='https://opendata.dwd.de/climate_environment/CDC/grids_germany/annual/radiation_global/grids_germany_annual_radiation_global_';os.makedirs(D,exist_ok=True);[open(D+'/%d.asc'%j,'wb').write(zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(B+'%d.zip'%j,timeout=180).read())).read('grids_germany_annual_radiation_global_%d.asc'%j)) for j in range(1997,2023)]"
```

- **Gemessen am 07.10.2026:** Der Befehl legt 26 Dateien `1997.asc` bis `2022.asc` ab.

### DWD-Sonnenscheindauer (Jahresraster 1997–2022)

- **Pfad:** `backend/data/dwd_cdc/sunshine_duration_<Jahr>.asc.gz`, 26 Dateien (1997 bis 2022); der Disk-Cache des Produkts (`app.services.climate.dwd_cdc_grid`), der fehlende Jahre beim Lauf ebenfalls selbst nachlädt.
- **Herkunft:** Deutscher Wetterdienst (DWD), Climate Data Center, Raster der jährlichen Sonnenscheindauer (`sunshine_duration`, 1 km): https://opendata.dwd.de/climate_environment/CDC/grids_germany/annual/sunshine_duration/ (je Jahr `grids_germany_annual_sunshine_duration_<Jahr>17.asc.gz`).
- **Lizenz:** Geodatennutzungsverordnung (GeoNutzV), Datenlizenz Deutschland – Zero – Version 2.0 (dl-de/zero-2-0), laut Quellenverzeichnis des Produkts (`DWD_CDC_SSD_Raster`).
- **Abrufbefehl** (aus dem Wurzelverzeichnis des Repositorys):

```
python3 -c "import os,urllib.request;D='backend/data/dwd_cdc';B='https://opendata.dwd.de/climate_environment/CDC/grids_germany/annual/sunshine_duration/grids_germany_annual_sunshine_duration_';os.makedirs(D,exist_ok=True);[open(D+'/sunshine_duration_%d.asc.gz'%j,'wb').write(urllib.request.urlopen(B+'%d17.asc.gz'%j,timeout=180).read()) for j in range(1997,2023)]"
```

- **Gemessen am 07.10.2026:** Für 1997 und 2022 ist die abgerufene Datei byteweise die Datei, die auf dem Server im Disk-Cache liegt.

### Vorbehalt

Die Abrufe für VG250, Globalstrahlung und Sonnenscheindauer sind am 07.10.2026 mit gleichwertigem Code gegen die Adressen ausgeführt worden, mit Ausgabe in ein Probeverzeichnis statt an den Pfad (VG250 und Sonnenscheindauer mit Vergleich gegen die Dateien auf dem Server, Globalstrahlung mit Zählung der Dateien). Den Aufruf von `zensus_demografie_ab65.py` hat dieser Lauf nicht ausgeführt, weil er die Datei im Repository überschreiben würde. Die Anlage selbst lässt sich im Projekt-venv des Produkts (`scripts/testlauf.sh`) neu erzeugen; mit einem Python ohne `numpy` bricht das Skript an diesem Import ab. Am 07.10.2026 hat ein Lauf in diesem venv die Anlage `k_uv_raumstreuung.md` mit diesem Abschnitt geschrieben.
