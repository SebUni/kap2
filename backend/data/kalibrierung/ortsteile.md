# Gepinnte Ortsteilgrenzen der Beispielkommune Warmsen (OpenStreetMap)

Datei: `ortsteile_03256034.geojson` (Gemeinde Warmsen, Landkreis Nienburg (Weser), AGS 03256034). Gebraucht vom
PDF-Ergebnisbericht (Vorhaben T-1418-cto, Paket 5a); geprüft von
`backend/tests/test_ergebnisbericht_ortsteile_daten.py`, der die Datei ohne Netzzugriff liest.

Zahl der Flächen: **5** (Ebene 9: 0, Ebene 10: 5).

| Name | `admin_level` | `osm_relation` | `anteil_in_gemeinde` | Fläche |
|---|---|---|---|---|
| Bohnhorst | 10 | 2983143 | 0,9948 | 23,0 km² |
| Brünninghorstedt | 10 | 2991482 | 0,9909 | 4,22 km² |
| Großenvörde | 10 | 2991042 | 0,9980 | 14,4 km² |
| Sappelloh | 10 | 2991043 | 0,9998 | 16,1 km² |
| Warmsen | 10 | 2991044 | 0,9979 | 24,0 km² |

Zusammen 81,7 km². Beide Ebenen (9 und 10) werden gepinnt; welche der Bericht zeigt, entscheidet Paket 2. In Warmsen
trägt OpenStreetMap nur Ebene 10.

## Aufbau

Eine GeoJSON-FeatureCollection in EPSG:4326 (Länge, Breite; Koordinaten auf sieben Nachkommastellen gerundet).

Kopfangaben der FeatureCollection:

| Angabe | Inhalt |
|---|---|
| `stand_osm_base` | Stand der OSM-Daten: `osm3s.timestamp_osm_base` der Overpass-Antwort, hier `2026-09-27T11:19:06Z` |
| `abgerufen` | Datum des Abrufs, hier `2026-09-27` |
| `gemeinde` | AGS, Name und Stand der VG250-Gemeindegrenze, gegen die der Anteil gerechnet ist |
| `quelle`, `lizenz` | OpenStreetMap über Overpass API; ODbL 1.0, © OpenStreetMap-Mitwirkende |
| `mindestanteil_in_gemeinde` | Schwelle für die Übernahme einer Fläche (0,5) |

Eigenschaften je Fläche (Feature):

| Eigenschaft | Inhalt |
|---|---|
| `name` | Name der Relation (OSM-Tag `name`) |
| `admin_level` | 9 oder 10 (OSM-Tag `admin_level`) |
| `osm_relation` | Kennung der OSM-Relation (ganze Zahl), nachschlagbar unter `https://www.openstreetmap.org/relation/<Kennung>` |
| `anteil_in_gemeinde` | Anteil der Fläche, der in der VG250-Gemeindegrenze liegt (0 bis 1), gerechnet in EPSG:25832 |
| `flaeche_km2` | Fläche in km², gerechnet in EPSG:25832 |

Die Geometrie ist ein Polygon oder MultiPolygon, zusammengesetzt aus den äußeren und inneren Wegen der Relation.

## Quellen

- **OpenStreetMap**, Relationen `boundary=administrative` mit `admin_level` 9 oder 10, abgefragt über die
  Overpass API (Adresse aus `backend/app/config.py`, `OVERPASS_URL`). Stand der Daten `2026-09-27T11:19:06Z`,
  abgerufen am 27.09.2026.
- **[65]** BKG, Verwaltungsgebiete 1 : 250 000 (VG250), Ebene `vg250_gem`, GF = 4; Adresse aus
  `backend/app/config.py` (`VG250_GPKG_URL`), Stand `vg250_ebenen_0101`. Nur für die Auswahl: Übernommen werden
  Flächen, die zu mindestens 50 % in der Gemeindegrenze liegen.

## Erzeugung

`~/.venvs/kap2/bin/python backend/scripts/ortsteile_pinnen.py --gemeinde 03256034` (am 27.09.2026). Das Skript
fragt alle Relationen `boundary=administrative` mit `admin_level` 9 oder 10 im Rechteck um die Gemeindegrenze ab
(Rand 0,02 Grad, rund 2 km), setzt die Ringe mit `_merge_rings` aus `app/services/osm_service.py` zusammen, rechnet
den Anteil in der VG250-Gemeindegrenze (Loader `gemeindegebiet` aus `docs/methodik/anlagen/95_zellvergleich.py`,
wie in `golden_95_zelldaten.py`) und schreibt die Flächen ab 50 % Anteil. Findet OpenStreetMap keine Fläche,
entsteht eine leere FeatureCollection; eigene Grenzen werden nicht ergänzt.

## Lizenz

Die Ortsteilgrenzen stammen aus OpenStreetMap und stehen unter der Open Database License (ODbL 1.0).
Namensnennung: „© OpenStreetMap-Mitwirkende“. Die Datei ist eine abgeleitete Datenbank im Sinne der ODbL und steht
selbst unter der ODbL 1.0; wer sie weitergibt oder daraus Karten erzeugt, nennt OpenStreetMap als Quelle.
VG250: Datenlizenz Deutschland – Namensnennung – Version 2.0 (dl-de/by-2-0), © GeoBasis-DE / BKG.
