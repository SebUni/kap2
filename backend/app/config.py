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
    # Auth: HTTP-Header username/password ODER token; data/table via POST,
    # regionalkey filtert auf den AGS. Ohne (gültige) Zugangsdaten wird die
    # Ableitung übersprungen (neutraler Fallback 50).
    REGIONALSTATISTIK_API_BASE: str = "https://www.regionalstatistik.de/genesisws/rest/2020"
    REGIONALSTATISTIK_USERNAME: str = ""
    REGIONALSTATISTIK_PASSWORD: str = ""
    REGIONALSTATISTIK_TOKEN: str = ""  # Alternative zu username/password (API-Kennung)
    # GENESIS-Tabellencodes (überschreibbar, falls sich die Tabellen ändern).
    REGIONALSTATISTIK_TABLE_TAX: str = "71231-01-03-4"          # Realsteuervergleich, €/Einwohner
    REGIONALSTATISTIK_TABLE_UNEMPLOYMENT: str = "13211-02-05-4"  # Arbeitslosenquote, %
    REGIONALSTATISTIK_CACHE_DIR: str = os.path.join(_BACKEND_ROOT, "data", "inkar")
    REGIONALSTATISTIK_TIMEOUT_S: int = 30
    REGIONALSTATISTIK_CACHE_TTL_S: int = 30 * 24 * 3600  # 30 Tage (jährliche Daten)

    # ── DWD CDC Rasterdaten (heiße Tage / Frosttage) — offene, keyless Grids ──
    # Jährliche 1-km-ESRI-ASCII-Grids (Gauß-Krüger 3 / EPSG:31467), am Kommune-
    # Zentroid abgegriffen und über die letzten N Jahre gemittelt (Report §B2.1).
    DWD_CDC_GRID_BASE: str = (
        "https://opendata.dwd.de/climate_environment/CDC/grids_germany/annual"
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

    class Config:
        env_file = ".env"


settings = Settings()
