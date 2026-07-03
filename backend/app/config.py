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
    # Ohne Zugangsdaten wird die Ableitung übersprungen (neutraler Fallback 50).
    REGIONALSTATISTIK_API_BASE: str = "https://www.regionalstatistik.de/genesis/api/rest/2020"
    REGIONALSTATISTIK_USERNAME: str = ""
    REGIONALSTATISTIK_PASSWORD: str = ""
    # GENESIS-Tabellencodes (überschreibbar, falls sich die Tabellen ändern).
    REGIONALSTATISTIK_TABLE_TAX: str = "71231-01-03-4"          # Realsteuervergleich, €/Einwohner
    REGIONALSTATISTIK_TABLE_UNEMPLOYMENT: str = "13211-02-05-4"  # Arbeitslosenquote, %
    REGIONALSTATISTIK_CACHE_DIR: str = os.path.join(_BACKEND_ROOT, "data", "inkar")
    REGIONALSTATISTIK_TIMEOUT_S: int = 30
    REGIONALSTATISTIK_CACHE_TTL_S: int = 30 * 24 * 3600  # 30 Tage (jährliche Daten)

    class Config:
        env_file = ".env"


settings = Settings()
