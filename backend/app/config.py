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

    class Config:
        env_file = ".env"


settings = Settings()
