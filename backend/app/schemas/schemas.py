from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


# ── Kommune ────────────────────────────────────────────────────────────────────

class KommuneSearch(BaseModel):
    name: str
    osm_id: str
    display_name: str
    lat: float
    lon: float


class KommuneCreate(BaseModel):
    osm_id: str
    name: str
    osm_type: str = "relation"
    geojson: Optional[dict] = None


class KommuneOut(BaseModel):
    id: int
    name: str
    bundesland: Optional[str] = None
    osm_id: Optional[str] = None
    area_km2: Optional[float] = None
    population: Optional[int] = None
    created_at: datetime
    boundary_geojson: Optional[dict] = None

    model_config = {"from_attributes": True}


# ── Grid ───────────────────────────────────────────────────────────────────────

class GridCellOut(BaseModel):
    id: int
    gitter_id: str
    x_3035: int
    y_3035: int
    row_idx: int
    col_idx: int
    cell_size_m: int

    model_config = {"from_attributes": True}


class GridGenerateRequest(BaseModel):
    cell_size_m: int = 100
    force: bool = False


# ── Assessment ─────────────────────────────────────────────────────────────────

class AssessmentRequest(BaseModel):
    climate_type: str = "heat"
    level: int = 1


class AssessmentStatusOut(BaseModel):
    climate_type: str
    level: int
    progress_pct: float
    status: str
    message: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    step_history: list[dict] = []
    eta_seconds: Optional[float] = None


# ── Config ─────────────────────────────────────────────────────────────────────

class ConfigParameterOut(BaseModel):
    id: int
    category: str
    key: str
    value: Any
    description: Optional[str] = None

    model_config = {"from_attributes": True}


class ConfigParameterUpdate(BaseModel):
    category: str
    key: str
    value: Any
    description: Optional[str] = None


# ── Measures ───────────────────────────────────────────────────────────────────

class MeasureCreate(BaseModel):
    name: str
    measure_type: str
    geometry_geojson: dict
    config: dict = {}
    implementation_year: Optional[int] = None
    description: Optional[str] = None


class MeasureUpdate(BaseModel):
    name: Optional[str] = None
    measure_type: Optional[str] = None
    config: Optional[dict] = None
    implementation_year: Optional[int] = None
    description: Optional[str] = None


class MeasureOut(BaseModel):
    id: int
    name: str
    measure_type: str
    geometry_geojson: Optional[dict] = None
    config: dict
    implementation_year: Optional[int] = None
    description: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class MeasureImpactOut(BaseModel):
    id: int
    measure_id: int
    grid_cell_id: int
    indicator_deltas: dict
    costs: dict
    savings: dict

    model_config = {"from_attributes": True}


class MeasureWithImpactOut(BaseModel):
    measure: MeasureOut
    total_indicator_deltas: dict
    total_costs: dict
    total_savings: dict
