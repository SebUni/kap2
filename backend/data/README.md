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

**ERA5-Sturmraster erzeugen** (einmaliger Betreiber-Lauf, kostenloser CDS-Account nötig):

```bash
pip install cdsapi netCDF4          # optionale Zusatzpakete (s. requirements.txt)
python scripts/fetch_era5_storm.py  # schreibt data/era5_storm/storm_days.asc.gz
```

Der CDS-API-Key gehört in `~/.cdsapirc` (nicht ins Repo). Die intensitätsbasierten
Datensätze **JRC River Flood Hazard Maps** (Hochwassertiefe je Wiederkehrperiode) und
**UFZ-Dürremonitor SMI** bleiben spätere Verfeinerungen (brauchen `rasterio`/`netCDF4`
+ GB-Downloads); bis dahin treibt die normierte Hazard-Intensität die Schadenskurven.
