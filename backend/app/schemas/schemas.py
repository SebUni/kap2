from datetime import datetime
from typing import Any, Optional, Union

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
    parameter_id: Optional[str] = None
    source: Optional[str] = None
    custom_source: Optional[str] = None

    model_config = {"from_attributes": True}


class ConfigParameterUpdate(BaseModel):
    category: str
    key: str
    value: Any
    description: Optional[str] = None


class ParameterUpdate(BaseModel):
    parameter_id: str
    value: Any
    custom_source: Optional[str] = None


# ── Parameters (Registry) ────────────────────────────────────────────────────────

class SourceReference(BaseModel):
    """Zitierfähiger Bibliografie-Eintrag (app.data.sources.SOURCE_REFERENCES)."""
    key: str = ""
    ieee: str = ""
    url: str = ""
    archive_url: str = ""
    accessed: str = ""


class ModelParameter(BaseModel):
    """Flaches Parameter-Dict aus parameter_registry._base_param()/catalog_parameters()."""
    id: str
    layer_code: str
    layer_category: str
    label: str
    value: Any
    default_value: Any
    unit: str = ""
    source: str = ""
    source_detail: str = ""
    references: list[SourceReference] = []
    prov: str = "param"
    editable: bool = True
    overridden: bool = False
    custom_source: Optional[str] = None
    applicable: Optional[bool] = None


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
    impact_summary: Optional[dict] = None
    """Zuletzt berechnetes compute_impact()-Ergebnis (None vor erster Berechnung)."""

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


# ── Measure cost breakdown (measure_service.compute_costs shape) ────────────────

class CostComponent(BaseModel):
    param: str
    label: str
    unit_price: float
    quantity: Union[int, float]
    quantity_unit: str
    amount_eur: float
    source: str
    source_detail: str = ""
    references: list[SourceReference] = []
    overridden: bool


class CostBlock(BaseModel):
    total_eur: float
    components: list[CostComponent]


class EffectScaling(BaseModel):
    unit_factor: float
    count: int
    recommended_count: int
    density_per_ha: Optional[float] = None
    source: str


class CostBreakdown(BaseModel):
    """capex/opex kommen 1:1 aus measure_service.compute_costs().

    capex = einmalige Investition (fix/Stück/Fläche), opex = jährliche Betriebs-
    und Unterhaltskosten (fix/Stück/Fläche). effect_scaling ist dort (noch) nicht
    enthalten - unit_factor/count/recommended_count/unit_label liegen als eigene
    Top-Level-Felder auf MeasureImpactSummary. effect_scaling bleibt daher
    optional/None und dokumentiert nur die im Beplanungsdokument gezeigte
    Ziel-Verschachtelung.
    """
    capex: CostBlock
    opex: CostBlock
    effect_scaling: Optional[EffectScaling] = None


class MeasureImpactSummary(BaseModel):
    """Dokumentiert measure_service.compute_impact()'s Response-Dict.

    Nicht als response_model verdrahtet - der Route-Handler gibt das dict
    unvalidiert zurück. Die meisten Felder sind optional, da der Early-Exit-
    Pfad (keine überlappenden Zellen) nur measure_id/affected_cells/message
    liefert.
    """
    measure_id: int
    measure_type: Optional[str] = None
    affected_cells: int
    affected_area_m2: Optional[float] = None
    linked_risk_codes: Optional[list[str]] = None
    avg_index_reduction_pct: Optional[float] = None
    capex_eur: Optional[float] = None
    opex_annual_eur: Optional[float] = None
    annual_benefit_eur: Optional[float] = None
    count: Optional[int] = None
    count_is_default: Optional[bool] = None
    recommended_count: Optional[int] = None
    unit_label: Optional[str] = None
    unit_factor: Optional[float] = None
    cost_breakdown: Optional[CostBreakdown] = None
    message: Optional[str] = None
