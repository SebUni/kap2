# #98 — Bevölkerungsgewichtete SSD-Normalperiodenänderung (Befund 223)

Erzeugt von `backend/scripts/kalibrierung/ssd_povw.py`. Gewichtung auf der
**Gemeindepunkt-Ebene** (§3.4 ausdrücklich zulässig; kein 100-m-Vollraster-Lauf):
10.824 amtliche Gemeindepunkte (BKG VG250 `vg250_pk`, Gebietsstand 01.01.2025)
mit Zensus-2022-Gemeindebevölkerung; SSD über die **Produktfunktion**
`ssd_normalperioden.ssd_at` gelesen (Kalibriermodell = Produktionsmodell).

**Punktmengen-Kette (Befund 396):** VG250 `vg250_pk` führt 10.949 amtliche Gemeindepunkte; davon 10.853 mit Zensus-2022-Einwohnerzahl (96 ohne) und davon 10.824 mit SSD-Rasterwert (29 ohne) — diese gehen in die Gewichtung ein.

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

## Eingangsdaten

Das Skript liest zwei Dateien, die nicht im Repository liegen (`backend/data/vg250/` und `backend/data/lite/` stehen in `.gitignore`), und die Normalperioden-Raster `backend/data/kalibrierung/ssd_normalperioden.npz`, die im Repository liegen. Alle Pfade gelten ab dem Wurzelverzeichnis des Repositorys. Die Abrufbefehle legen die Dateien dorthin, wo `ssd_povw.py` sie erwartet; danach läuft `python backend/scripts/kalibrierung/ssd_povw.py` ohne Zwischenstände aus einem Probeverzeichnis.

### VG250 (GeoPackage)

- **Pfad:** `backend/data/vg250/DE_VG250.gpkg`, Ebene `vg250_pk` (Verwaltungspunkte), Gebietsstand 01.01.2025.
- **Herkunft:** Bundesamt für Kartographie und Geodäsie (BKG), Verwaltungsgebiete 1:250 000 (VG250), Ausgabe Stand 01.01., UTM32s-GeoPackage. Bezugsadresse: https://daten.gdz.bkg.bund.de/produkte/vg/vg250_ebenen_0101/2025/vg250_01-01.utm32s.gpkg.ebenen.zip (Katalogseite: https://gdz.bkg.bund.de/index.php/default/verwaltungsgebiete-1-250-000-ebenen-stand-01-01-vg250-ebenen-01-01.html).
- **Lizenz:** Datenlizenz Deutschland – Namensnennung – Version 2.0 (dl-de/by-2-0), Quelle: BKG.
- **Abrufbefehl** (aus dem Wurzelverzeichnis des Repositorys):

```
python3 -c "import io,os,urllib.request,zipfile;z=zipfile.ZipFile(io.BytesIO(urllib.request.urlopen('https://daten.gdz.bkg.bund.de/produkte/vg/vg250_ebenen_0101/2025/vg250_01-01.utm32s.gpkg.ebenen.zip',timeout=600).read()));n=[x for x in z.namelist() if x.endswith('DE_VG250.gpkg')][0];os.makedirs('backend/data/vg250',exist_ok=True);open('backend/data/vg250/DE_VG250.gpkg','wb').write(z.read(n))"
```

- **Gemessen am 07.10.2026:** Die so entpackte Datei hat SHA-256 `f229550c80180a11de7d235d8387b96fe535bdf60cb633ff2532009362d784e9` und 10.949 Punkte in `vg250_pk`, wie im Kopf dieser Anlage.
- **Gebietsstand beachten:** Die Adresse `…/aktuell/` und der Standardabruf des Produkts (`vg250_loader.ensure_vg250`) liefern den jeweils neuesten Gebietsstand, am 07.10.2026 den Stand 2026 mit 10.939 Punkten. Für die Zahlen dieser Anlage gilt der Stand 2025.

### Zensus-Gemeindedatei (JSON)

- **Pfad:** `backend/data/lite/zensus_gemeinde.json`, ein Eintrag je Gemeindeschlüssel (AGS, 8 Stellen); das Skript liest daraus das Feld `population` (Einwohner, Zensus 2022, Stichtag 15.05.2022).
- **Herkunft:** keine amtliche Einzeldatei, sondern eine Ableitung des Produkts: Die Gitterdaten 100 m des Zensus 2022 (Statistische Ämter des Bundes und der Länder) werden auf die Gemeindeflächen der VG250 aufsummiert (`app.services.lite.zensus_gemeinde.aggregate`, Phase C des Lite-Batches). Bezugsadressen der Gitterdateien: https://www.destatis.de/static/DE/zensus/gitterdaten/Zensus2022_Bevoelkerungszahl.zip, dazu `Anteil_ab_65-jaehrige_in_Gitterzellen.zip`, `Anteil_unter_18-jaehrige_in_Gitterzellen.zip` und `Gebaeude_nach_Baujahr_in_Mikrozensus_Klassen.zip` im selben Verzeichnis (https://www.destatis.de/static/DE/zensus/gitterdaten/). Diese drei gehen in die Datei ein, nicht in diese Anlage.
- **Lizenz:** Datenlizenz Deutschland – Namensnennung – Version 2.0 (dl-de/by-2-0), © Statistische Ämter des Bundes und der Länder.
- **Abrufbefehl**, erst die Gitterdateien (legt die CSV unter `backend/data/zensus/extract/<Schlüssel>/` ab):

```
cd backend && python3 -c "from app.services import zensus_loader as zl;[zl.ensure_zensus_dataset(k) for k in ('population','share_over_65','share_under_18','building_age')]"
```

  dann die Aggregation, die die JSON-Datei an den oben genannten Pfad schreibt: als Administrator `POST /api/admin/lite-batch` mit dem Inhalt `{"bundesland": null, "force_zensus": true}`. Der Batch liest die VG250-Datei aus dem Abschnitt davor; sie muss deshalb vorher an ihrem Pfad liegen, sonst lädt er den neuesten Gebietsstand.
- **Grenze dieser Fassung:** Der Aggregationsschritt braucht die Datenbank des Produkts (PostGIS-Tabelle `gemeinden`) und die Gemeindedatei `backend/data/lite/zensus_gemeinde.json`. Ohne beide lässt er sich nicht ausführen; die beiden Befehle sind in diesem Lauf nicht ausgeführt worden. Die Anlage `ssd_povw.md` ist deshalb von Hand fortgeschrieben und nicht neu erzeugt; der Abschnitt steht in Skript und Anlage gleichlautend.