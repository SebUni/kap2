from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://kap2:kap2dev@localhost:5432/kap2"
    DEFAULT_GRID_SIZE_M: int = 100
    DEFAULT_SRID: int = 4326
    CALCULATION_SRID: int = 25832  # ETRS89 / UTM zone 32N (Germany)
    NOMINATIM_URL: str = "https://nominatim.openstreetmap.org"
    OVERPASS_URL: str = "https://overpass-api.de/api/interpreter"
    NOMINATIM_USER_AGENT: str = "kap2-climate-planner/1.0"

    class Config:
        env_file = ".env"


settings = Settings()
