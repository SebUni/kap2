import os

from pydantic_settings import BaseSettings

_BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://kap2:kap2dev@localhost:5432/kap2"
    DEFAULT_GRID_SIZE_M: int = 100
    DEFAULT_SRID: int = 4326
    CALCULATION_SRID: int = 25832  # ETRS89 / UTM zone 32N (Germany)
    ZENSUS_SRID: int = 3035  # ETRS89-LAEA (Destatis INSPIRE 100m grid)
    ZENSUS_DATA_DIR: str = os.path.join(_BACKEND_ROOT, "data", "zensus")
    ZENSUS_AUTO_DOWNLOAD: bool = True
    ZENSUS_FORCE_REFRESH: bool = False
    ZENSUS_DOWNLOAD_TIMEOUT_S: int = 600
    ZENSUS_USER_AGENT: str = "kap2-climate-planner/1.0 (zensus-autoload)"
    NOMINATIM_URL: str = "https://nominatim.openstreetmap.org"
    OVERPASS_URL: str = "https://overpass-api.de/api/interpreter"
    NOMINATIM_USER_AGENT: str = "kap2-climate-planner/1.0"

    # ── BBSR INKAR / Regionalstatistik (GENESIS-Online REST) ──────────────────
    # Kommunale Sozioökonomie (Steuereinnahmekraft, Arbeitslosenquote) je AGS.
    # Auth: HTTP-Header (Kennung/Passwort ODER Token im ``username``-Feld, latin-1);
    # Datenabruf über data/tablefile (ffcsv, gezippt), regionalkey filtert auf den
    # AGS. Ohne (gültige) Zugangsdaten wird die Ableitung übersprungen (Fallback 50).
    REGIONALSTATISTIK_API_BASE: str = "https://www.regionalstatistik.de/genesisws/rest/2020"
    REGIONALSTATISTIK_USERNAME: str = ""
    REGIONALSTATISTIK_PASSWORD: str = ""
    REGIONALSTATISTIK_TOKEN: str = ""  # Alternative: API-Token (dann ins username-Feld, pw leer)
    # GENESIS-Tabellencodes (überschreibbar, falls sich die Tabellen ändern).
    REGIONALSTATISTIK_TABLE_TAX: str = "71231-01-03-4"          # Realsteuervergleich, €/Einwohner
    REGIONALSTATISTIK_TABLE_UNEMPLOYMENT: str = "13211-02-05-4"  # Arbeitslosenquote, %
    # Dashboard-Kopf (finance_loader): BIP liegt amtlich nur auf KREISebene vor
    # (Statistik VGR der Länder = 82000; Tabelle hat je Kreis/Jahr mehrere
    # Kennzahlen, BIP802 = BIP insgesamt in Tsd. EUR). Die kommunalen Auszahlungen
    # (Kernhaushalte, Statistik 71717) liegen auf GEMEINDEebene vor, sind aber für
    # den Direkt-Dialog zu groß → Abruf über den Job/Batch-Pfad (job=true →
    # catalogue/jobs → data/resultfile). Codes/Kennzahlen sind Settings, weil sich
    # die GENESIS-Zuschnitte ändern — bei Fehlern (JSON-Error im Log) im Katalog
    # (/catalogue/tables2statistic?name=82000 bzw. 71717) nachschlagen.
    REGIONALSTATISTIK_TABLE_GDP: str = "82000-01-01-4"          # BIP, Kreise (VGR der Länder)
    REGIONALSTATISTIK_GDP_VARIABLE: str = "BIP802"             # Kennzahl: BIP insgesamt (Tsd. EUR)
    REGIONALSTATISTIK_GDP_PC_VARIABLE: str = "BIP804"         # Kennzahl: BIP je Einwohner (EUR) — für die Kommunen-Schätzung
    # Kommunaler-Haushalt-Chip (Auszahlungen insg., Kennzahl AUSZ001, EUR):
    # Statistik 71717 ist für den Direkt-Dialog zu groß → periodischer Bulk-Import
    # (finance_bulk / scripts.import_finance_budget, Betreiber-Cron) in einen
    # lokalen Store; der Chip liest nur diesen (netzfrei). Match über Kreis+Name,
    # weil der GENESIS-Regionalcode NICHT der amtliche AGS ist (Verbandsschlüssel,
    # z. B. Oschatz AGS 14730230 → GENESIS F1473002300). Ist der Store leer (Cron
    # noch nicht gelaufen), bleibt der Chip einfach aus.
    REGIONALSTATISTIK_BUDGET_ENABLED: bool = True
    REGIONALSTATISTIK_TABLE_BUDGET: str = "71717-Z-03"         # Auszahlungen (Übersicht), Gemeinden
    REGIONALSTATISTIK_BUDGET_VARIABLE: str = "AUSZ001"        # Auszahlungen insgesamt (bereinigt), EUR
    REGIONALSTATISTIK_BUDGET_AVG_YEARS: int = 5                 # Ø über die letzten N verfügbaren Jahre
    REGIONALSTATISTIK_CACHE_DIR: str = os.path.join(_BACKEND_ROOT, "data", "inkar")
    REGIONALSTATISTIK_TIMEOUT_S: int = 45
    # Job/Batch-Abruf der Gemeindefinanzen (finance_bulk, Betreiber-Cron): großzügige
    # Fristen, weil der RS-Server träge ist und die Ergebnistabelle groß wird.
    REGIONALSTATISTIK_JOB_POLL_S: int = 15
    REGIONALSTATISTIK_JOB_MAX_WAIT_S: int = 900       # bis zu 15 min auf „Fertig" warten
    REGIONALSTATISTIK_JOB_DOWNLOAD_S: int = 600       # bis zu 10 min für den Ergebnis-Download
    REGIONALSTATISTIK_JOB_SUBMIT_S: int = 180         # Timeout je Submit-Versuch (Server hängt sporadisch)
    REGIONALSTATISTIK_JOB_SUBMIT_TRIES: int = 4       # Submit-Wiederholungen
    REGIONALSTATISTIK_CACHE_TTL_S: int = 30 * 24 * 3600  # 30 Tage (jährliche Daten)

    # ── DWD CDC Rasterdaten (heiße Tage / Frosttage) — offene, keyless Grids ──
    # Jährliche 1-km-ESRI-ASCII-Grids (Gauß-Krüger 3 / EPSG:31467), am Kommune-
    # Zentroid abgegriffen und über die letzten N Jahre gemittelt (Report §B2.1).
    DWD_CDC_GRID_BASE: str = (
        "https://opendata.dwd.de/climate_environment/CDC/grids_germany/annual"
    )
    # Monatsraster (Lufttemperatur) — gleiche 1-km-ESRI-ASCII-Struktur wie die
    # Jahresraster, aber eigener Pfad und Dateinamensmuster. Werte in 1/10 °C.
    DWD_CDC_MONTHLY_BASE: str = (
        "https://opendata.dwd.de/climate_environment/CDC/grids_germany/monthly"
    )
    DWD_CDC_CACHE_DIR: str = os.path.join(_BACKEND_ROOT, "data", "dwd_cdc")
    DWD_CDC_TIMEOUT_S: int = 30
    DWD_CDC_CACHE_TTL_S: int = 30 * 24 * 3600   # 30 Tage (jährliche Grids)
    DWD_CDC_CLIMATOLOGY_YEARS: int = 10         # Mittel der letzten N verfügbaren Jahre

    # ── BfG / PEGELONLINE (WSV) — Niedrigwasser nächster Pegel, keyless REST ──
    # Report §B2.6: low_flow_days aus dem nächstgelegenen Pegel (Tage < MNW).
    PEGELONLINE_API_BASE: str = (
        "https://www.pegelonline.wsv.de/webservices/rest-api/v2"
    )
    PEGELONLINE_CACHE_DIR: str = os.path.join(_BACKEND_ROOT, "data", "pegelonline")
    PEGELONLINE_TIMEOUT_S: int = 30
    PEGELONLINE_CACHE_TTL_S: int = 30 * 24 * 3600
    PEGELONLINE_MAX_DISTANCE_KM: float = 50.0   # nur Pegel innerhalb dieser Distanz

    # ── ERA5 / Copernicus CDS — Sturmtage (Böen ≥ Schwelle) am Zentroid ──────────
    # Loader liest ein gecachtes Sturmtage-Raster (EPSG:4326, ESRI-ASCII), das der
    # Betreiber einmalig mit ``scripts/fetch_era5_storm.py`` + kostenlosem CDS-Key
    # erzeugt (ERA5 ist kostenlos, seit 02.07.2025 CC-BY 4.0). Fehlt die Datei, bleibt
    # der bisherige regionale Konstantwert (robuster Fallback).
    ERA5_STORM_CACHE_DIR: str = os.path.join(_BACKEND_ROOT, "data", "era5_storm")
    ERA5_STORM_GUST_THRESHOLD_MS: float = 25.0   # Böen-Schwelle für einen „Sturmtag"
    ERA5_STORM_CLIMATOLOGY_YEARS: int = 10

    # ── Assessment-Ausführung (Kind-Prozess, RAM-Budget) ─────────────────────
    # Die Voll-Bewertung läuft in einem eigenen, kurzlebigen Prozess
    # (app/tasks/assessment_worker.py): RAM geht bei Exit vollständig ans OS
    # zurück, der API-Prozess bleibt dauerhaft klein. Defaults sind für eine
    # 16-GB-Maschine ausgelegt; für 24-GB-Server (Strato XXL) z. B.
    # ASSESSMENT_MAX_RSS_MB=9000, ASSESSMENT_WORKERS=6 (siehe docs/BETRIEB.md).
    ASSESSMENT_WORKERS: int = 0                  # 0 = auto: min(4, CPU-Kerne)
    ASSESSMENT_MAX_CONCURRENT: int = 1           # parallele Assessment-Kindprozesse
    ASSESSMENT_MAX_RSS_MB: int = 5000            # PSS-Limit des Kind-Prozessbaums
    ASSESSMENT_WATCHDOG_INTERVAL_S: float = 3.0
    ASSESSMENT_RLIMIT_AS_MB: int = 0             # 0 = aus (nur Not-Backstop; VA ≫ RSS)

    # ── OSM/Overpass-Rohdaten-Cache (Platte) ─────────────────────────────────
    # Roh-JSON der Overpass-Antworten je (Abfrageart, bbox) — Wiederholungs-
    # läufe derselben Kommune kommen ohne erneuten Download aus.
    OSM_CACHE_DIR: str = os.path.join(_BACKEND_ROOT, "data", "osm_cache")
    OSM_CACHE_TTL_S: int = 30 * 24 * 3600        # 30 Tage

    # ── Terrain-Kachel-Cache (Platte) — Terrarium-DEM ist quasi statisch ─────
    TERRAIN_TILE_CACHE_DIR: str = os.path.join(_BACKEND_ROOT, "data", "terrain_tiles")
    TERRAIN_TILE_CACHE_TTL_S: int = 365 * 24 * 3600

    # ── Deutschland-Lite (kostenlose Gemeinde-Grobkarte) ─────────────────────
    # BKG VG250 (Verwaltungsgebiete 1:250.000, dl-de/by-2-0): Gemeindegeometrien
    # + Attribute (AGS, Einwohner, Fläche). Einmalig geladen, Cache auf Platte.
    VG250_GPKG_URL: str = (
        "https://daten.gdz.bkg.bund.de/produkte/vg/vg250_ebenen_0101/aktuell/"
        "vg250_01-01.utm32s.gpkg.ebenen.zip"
    )
    LITE_DATA_DIR: str = os.path.join(_BACKEND_ROOT, "data", "lite")
    VG250_CACHE_DIR: str = os.path.join(_BACKEND_ROOT, "data", "vg250")
    LITE_DOWNLOAD_TIMEOUT_S: int = 600

    # ── M0-Verschlankung (docs/ROADMAP.md §5): Nicht-Kern-Bereiche offline ───
    # Frontend-Pendant: frontend/src/config/features.ts. Demo kehrt mit
    # Stage 2 zurück, Studie mit M3½, SEO-/Lite-Seiten mit der Re-Expansion.
    # Admin-Router (Demo-Konfiguration, Lite-Batch) bleiben bewusst erreichbar.
    DEMO_ENABLED: bool = False                   # /api/demo/* (Router-Mount)
    STUDY_ENABLED: bool = False                  # /api/public/lite/studie*, study-highlights
    LITE_PAGES_ENABLED: bool = False             # SEO-Gemeindeseiten, sitemap.xml, robots.txt

    # ── LoD2-Gebäudemodelle (amtliche 3D-Modelle der Länder, CityGML) ────────
    # Gebäudehöhen (bldg:measuredHeight) + Footprints ersetzen die OSM-Höhen-
    # heuristik, wo ein Land als Phase-1-Quelle angebunden ist (sources.py in
    # services/geodata/lod2). Kacheln werden pro bbox geladen und KOMPAKT
    # (nur Ringe + Höhe, gzip-JSON) gecacht — Rohdaten-GML nur auf Wunsch (CLI).
    LOD2_ENABLED: bool = True
    LOD2_CACHE_DIR: str = os.path.join(_BACKEND_ROOT, "data", "lod2")
    LOD2_DOWNLOAD_TIMEOUT_S: int = 300
    LOD2_MAX_TILES: int = 400                    # Kachel-Obergrenze je bbox-Anfrage

    # ── Sky-View-Faktor (Horizontwinkel-Verfahren auf Gebäudehöhenraster) ────
    SVF_RESOLUTION_M: float = 5.0
    SVF_RADIUS_M: float = 100.0
    SVF_DIRECTIONS: int = 16
    SVF_MAX_PIXELS: int = 60_000_000             # darüber: Auflösung vergröbern

    # ── KI-Assistent (Mistral AI, La Plateforme — EU-Hosting) ────────────────
    # Der API-Schlüssel wird primär serverseitig in der DB (AppSetting 'ai_api_key')
    # über den Einstellungs-Dialog hinterlegt. Diese Env-Variable ist ein optionaler
    # Ops-Override (Muster wie REGIONALSTATISTIK_TOKEN): ist sie gesetzt, hat sie
    # Vorrang vor dem DB-Wert. Leer = ausschließlich DB-Wert wird verwendet.
    MISTRAL_API_KEY: str = ""
    MISTRAL_TIMEOUT_S: int = 120

    class Config:
        env_file = ".env"


settings = Settings()
