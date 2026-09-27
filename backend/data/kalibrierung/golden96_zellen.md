# Gepinnte Zelldaten für den Golden-Test der Beträge #96 (Berlin)

Datei: `golden96_zellen_11000000.csv.gz` (Berlin, 40.669 Zellen, 3.593.357 Einwohner; dieselben Zellen wie
`golden95_zellen_11000000.csv.gz`). Gebraucht von `backend/tests/test_methodik_96_golden_betraege.py`. Der Test
bindet den Jahresbetrag des Zelllaufs aus Bericht #96 (§3.0, Prüfblock `rechenkette_96`) an den Produktcode:
Berlin 4,58 Mio. € je Jahr mit der Ersatzregel #95 §3.3 (Preisstand 2024).

Die Anlage #95 trägt nur die 5er-Jahresgruppen ab 65. #96 teilt die Bevölkerung unter 65 je Zelle in u20 und
20–64 (§3.2) und braucht dafür alle 5er-Gruppen; deshalb eine eigene Anlage.

## Spalten

Je Zeile eine bewohnte 100-m-Zelle innerhalb der Gemeindegrenze:

| Spalte | Inhalt | Quelle |
|---|---|---|
| `gitter_id` | Kennung der Zelle im Zensus-Gitter (EPSG:3035) | [67] |
| `einwohner` | Einwohner (Datensatz „population“) | [67] |
| `anteil_ueber65` | Anteil 65+ in % (Datensatz „share_over_65“); leer oder 0 = geheimgehalten („–“) | [67] |
| `unter5` … `a90undaelter` | alle 19 5er-Jahresgruppen (Datensatz „age_groups“), Reihenfolge wie `zensus_loader.ALL_AGE_COLUMNS` | [67] |

Klimawerte und Vegetation fehlen bewusst: Berlin liegt in einer Region (δ in allen Zellen gleich), und der
Vegetationsfaktor P̂ mittelt im Ausgangsstand auf 1 (§3.0 Ebene 7). Die Summe über Berlin hängt von beidem
nicht ab.

Die letzte Zeile `__ausserhalb__` (Einwohner 0) trägt die Summen der 19 Gruppen aller Zellen im Rechteck um die
Gemeinde, die außerhalb der Grenze liegen. Der Loader bildet daraus die gebietsweiten Rückfälle für dünn besetzte
Zellen (`zensus_loader._area_senior_split`, `zensus_loader._area_u20_share`), wie im Zelllauf des Berichts.

## Quellen

- **[67]** Statistische Ämter des Bundes und der Länder, Zensus 2022, Gitterdaten 100 m, Stichtag 15.05.2022;
  Adressen und Einlese-Logik aus `backend/app/services/zensus_loader.py`.
- **[65]** BKG, Verwaltungsgebiete 1 : 250 000 (VG250), Ebene `vg250_gem`, GF = 4; Adresse aus
  `backend/app/config.py` (`VG250_GPKG_URL`), Stand `vg250_ebenen_0101`.

## Erzeugung

`backend/scripts/golden_96_zelldaten.py --gemeinde 11000000` (am 27.09.2026). Das Skript nutzt die Ladefunktionen
von `docs/methodik/anlagen/95_zellvergleich.py` (Gemeindegebiet, Punkt-in-Polygon mit den Zellmitten,
Zensus-Gitter) und Hilfsfunktionen aus `backend/scripts/golden_95_zelldaten.py`. Kontrollwerte aus §3.0:
40.669 Zellen und 3.593.357 Einwohner.

## Lizenz

Zensus 2022 und VG250: Datenlizenz Deutschland – Namensnennung – Version 2.0 (dl-de/by-2-0), © Statistische Ämter
des Bundes und der Länder bzw. © GeoBasis-DE / BKG.
