# Lokale Daten

## Zensus 2022 (100-m-Gitter)

Für Bevölkerungs- und Wohnindikatoren werden CSV-Extracts und Index-Dateien unter
`zensus/` erwartet. Sie sind nicht im Repository (zu groß).

Nach dem Klonen im Backend-Verzeichnis:

```bash
python -m app.cli zensus-download
```

Optional nur bestimmte Datensätze:

```bash
python -m app.cli zensus-download --keys population share_over_65
```

Die Dateien landen in `backend/data/zensus/extract/` und `backend/data/zensus/index/`.

## Klima-/Hazard-Raster (Schicht B)

Die Schadensfunktionen (Schicht B, `MODELL_KRITIK.md` §5–6) speisen sich aus bundesweit
einheitlichen, gecachten Rastern. **Alle Loader haben einen Fallback:** fehlt eine Datei,
liefern sie `None` und die App fällt auf den bisherigen regionalen Proxy zurück
(Provenienz in `build_regional_context["provenance"]`). Die App läuft also ohne diese
Daten — sie erhöhen nur die Ortsauflösung.

| Verzeichnis | Quelle | Inhalt | Lizenz |
|---|---|---|---|
| `dwd_cdc/` | DWD Climate Data Center (CDC) | Jahresraster Hitze-/Frosttage, Starkregentage ≥ 20/30 mm, Sommertage (ESRI-ASCII, EPSG:31467) | GeoNutzV / DL-DE→Zero-2.0 (frei, auch kommerziell) |
| `era5_storm/` | ERA5 / Copernicus C3S | Sturmtage/Jahr (10-m-Böe ≥ 25 m/s), EPSG:4326 (`storm_days.asc.gz`) | CC-BY 4.0 (frei, kommerziell; Nennung C3S/ECMWF) |
| `pegelonline/` | WSV PEGELONLINE | Niedrigwasser-Kennzahlen (bestehend) | DL-DE→Zero-2.0 |
| `inkar/` | BBSR INKAR | regionale Struktur-Indikatoren (bestehend) | frei mit Nennung |
| `osm_cache/` | OSM Overpass API | Roh-JSON der Overpass-Antworten je (Abfrageart, bbox), gzip; TTL `OSM_CACHE_TTL_S` (30 d). Wiederholungsläufe derselben Kommune laden nichts neu. | ODbL |
| `terrain_tiles/` | AWS Terrarium (Mapzen) | DEM-Kacheln `{z}/{x}/{y}.png`; TTL `TERRAIN_TILE_CACHE_TTL_S` (1 Jahr, quasi statisch) | Mapzen/AWS Open Data |

Beide neuen Verzeichnisse sind reine Caches: Sie können jederzeit gelöscht werden
(werden beim nächsten Lauf neu befüllt) und gehören nicht ins Repository.
Die abgeleiteten **Serving-Artefakte** (Karten-Layer, Dashboard-Payloads,
Aggregate) liegen getrennt unter `backend/.cache/{layers,dashboard,aggregates}/`
— Details in `docs/BETRIEB.md`.

**ERA5-Sturmraster erzeugen** (einmaliger Betreiber-Lauf, kostenloser CDS-Account nötig):

```bash
pip install cdsapi netCDF4          # optionale Zusatzpakete (s. requirements.txt)
python scripts/fetch_era5_storm.py  # schreibt data/era5_storm/storm_days.asc.gz
```

Der CDS-API-Key gehört in `~/.cdsapirc` (nicht ins Repo).

**Kommunalfinanzen-Chip aktualisieren** (Dashboard-Kopf „Kommunaler Haushalt"): Die
Regionalstatistik-Statistik 71717 (Auszahlungen der kommunalen Kernhaushalte) ist für
den GENESIS-Direkt-Dialog zu groß und wird über den Job/Batch-Pfad als komplette
Bundestabelle gezogen (Minuten, ~mehrere 100 MB). Der Importer extrahiert die Kennzahl
`AUSZ001` je Berichtsgemeinde und legt einen kompakten Lookup unter
`data/inkar/budget_71717.json.gz` ab (Match über Kreis + Gemeindename, weil der
GENESIS-Regionalcode nicht der amtliche AGS ist). Der Chip liest nur diesen Store.

```bash
python -m scripts.import_finance_budget   # oder: python -m app.cli finance-budget-import
```

**Selbstheilend:** Der neue Stand wird validiert (Mindestabdeckung + Anker-Kommunen)
und nur bei Erfolg atomar übernommen; scheitert Download/Parsing/Validierung, bleibt
der zuletzt gültige Store erhalten (Exit-Code 1). Voraussetzung:
`REGIONALSTATISTIK_USERNAME`/`…_PASSWORD` in `.env` und `REGIONALSTATISTIK_BUDGET_ENABLED=True`.
Server-seitige Zeitsteuerung (jährliche Daten → monatlich reicht), z. B. crontab:

```cron
30 3 5 * * cd /opt/lampp/htdocs/kap2/backend && /pfad/python -m scripts.import_finance_budget >> data/inkar/budget_import.log 2>&1
```

Die intensitätsbasierten
Datensätze **JRC River Flood Hazard Maps** (Hochwassertiefe je Wiederkehrperiode) und
**UFZ-Dürremonitor SMI** bleiben spätere Verfeinerungen (brauchen `rasterio`/`netCDF4`
+ GB-Downloads); bis dahin treibt die normierte Hazard-Intensität die Schadenskurven.
