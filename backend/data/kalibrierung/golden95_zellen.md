# Gepinnte Zelldaten für den Golden-Test der Beträge #95 (Berlin und Warmsen)

Dateien: `golden95_zellen_11000000.csv.gz` (Berlin, 40.669 Zellen, 3.593.357 Einwohner) und
`golden95_zellen_03256034.csv.gz` (Warmsen, Landkreis Nienburg (Weser), 529 Zellen, 3087 Einwohner).
Gebraucht von `backend/tests/test_methodik_95_golden_betraege.py`. Der Test bindet die Jahresbeträge des Zelllaufs
aus Bericht #95 (§3.0, Tabelle „Gemessene Wirkung“ in §3.3) an den Produktcode: Berlin 342,67 Mio. € und
707.318 Einwohner ab 65, Warmsen 173.099 € (Preisstand 2024).

## Spalten

Je Zeile eine bewohnte 100-m-Zelle innerhalb der Gemeindegrenze:

| Spalte | Inhalt | Quelle |
|---|---|---|
| `gitter_id` | Kennung der Zelle im Zensus-Gitter (EPSG:3035) | [67] |
| `einwohner` | Einwohner (Datensatz „population“) | [67] |
| `anteil_ueber65` | Anteil 65+ in % (Datensatz „share_over_65“); leer oder 0 = geheimgehalten („–“) | [67] |
| `a65bis69` … `a90undaelter` | die sechs 5er-Jahresgruppen ab 65 (Datensatz „age_groups“) | [67] |
| `t_sommer` | Sommermittel Juni–August in °C, 1-km-Raster, Mittel der Sommer 2016–2025 | [33] |
| `hitzetage` | Hitzetage je Jahr, 1-km-Raster, Mittel 2016–2025 | [33] |

Die letzte Zeile `__ausserhalb__` (Einwohner 0) trägt die Summen der sechs Gruppen ab 65 aller Zellen im Rechteck
um die Gemeinde, die außerhalb der Grenze liegen. Der Loader bildet daraus die gebietsweite Aufteilung der Menschen
ab 65 für dünn besetzte Zellen (`zensus_loader._area_senior_split`), wie im Zelllauf des Berichts.

## Quellen

- **[67]** Statistische Ämter des Bundes und der Länder, Zensus 2022, Gitterdaten 100 m, Stichtag 15.05.2022;
  Adressen und Einlese-Logik aus `backend/app/services/zensus_loader.py`.
- **[33]** Deutscher Wetterdienst, Climate Data Center, Raster 1 km: Monatsmittel der Lufttemperatur und Jahresraster
  `hot_days`; Adressen aus `backend/app/config.py` (`DWD_CDC_MONTHLY_BASE`, `DWD_CDC_GRID_BASE`).
- **[65]** BKG, Verwaltungsgebiete 1 : 250 000 (VG250), Ebene `vg250_gem`, GF = 4; Adresse aus
  `backend/app/config.py` (`VG250_GPKG_URL`), Stand `vg250_ebenen_0101`.

## Erzeugung

`backend/scripts/golden_95_zelldaten.py --gemeinde 11000000 --gemeinde 03256034` (am 26.09.2026). Das Skript
nutzt die Ladefunktionen von `docs/methodik/anlagen/95_zellvergleich.py`: Gemeindegebiet, Punkt-in-Polygon mit
den Zellmitten, Zensus-Gitter, DWD-Raster. Fehlt einer Zelle ein Rasterwert, gilt wie dort der Wert am Punkt der
Kette (bei beiden Gemeinden fehlt keiner). Kontrollwerte aus §3.0 (b) und §3.3: 40.669 Zellen und
3.593.357 Einwohner (Berlin), 3087 Einwohner (Warmsen).

## Lizenz

Zensus 2022 und VG250: Datenlizenz Deutschland – Namensnennung – Version 2.0 (dl-de/by-2-0), © Statistische Ämter
des Bundes und der Länder bzw. © GeoBasis-DE / BKG. DWD: Open Data des Deutschen Wetterdienstes, Quellenvermerk
„Deutscher Wetterdienst“.
