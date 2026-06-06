import enum
from datetime import datetime

from geoalchemy2 import Geometry
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Enum, ForeignKey, JSON, Text,
    UniqueConstraint
)
from sqlalchemy.orm import relationship

from app.db.database import Base


# ── Enums ──────────────────────────────────────────────────────────────────────

class AssessmentStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    ERROR = "error"


class ExportStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    ERROR = "error"


# ── Kommune ────────────────────────────────────────────────────────────────────

class Kommune(Base):
    __tablename__ = "kommunen"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    bundesland = Column(String(100))
    osm_id = Column(String(50), unique=True)
    boundary = Column(Geometry("MULTIPOLYGON", srid=4326))
    area_km2 = Column(Float)
    population = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    grid_cells = relationship("GridCell", back_populates="kommune", cascade="all, delete-orphan")
    assessments = relationship("CellAssessment", back_populates="kommune", cascade="all, delete-orphan")
    config_params = relationship("ConfigParameter", back_populates="kommune", cascade="all, delete-orphan")
    measures = relationship("AdaptationMeasure", back_populates="kommune", cascade="all, delete-orphan")
    project_statuses = relationship("ProjectStatus", back_populates="kommune", cascade="all, delete-orphan")
    risk_zones = relationship("RiskZone", back_populates="kommune", cascade="all, delete-orphan")
    geo_exports = relationship("GeoExportJob", back_populates="kommune", cascade="all, delete-orphan")


# ── Grid ───────────────────────────────────────────────────────────────────────

class GridCell(Base):
    __tablename__ = "grid_cells"

    id = Column(Integer, primary_key=True, index=True)
    kommune_id = Column(Integer, ForeignKey("kommunen.id", ondelete="CASCADE"), nullable=False)
    geometry = Column(Geometry("POLYGON", srid=4326), nullable=False)
    row_idx = Column(Integer, nullable=False)
    col_idx = Column(Integer, nullable=False)
    cell_size_m = Column(Integer, default=100)

    kommune = relationship("Kommune", back_populates="grid_cells")
    assessments = relationship("CellAssessment", back_populates="grid_cell", cascade="all, delete-orphan")
    measure_impacts = relationship("MeasureImpact", back_populates="grid_cell", cascade="all, delete-orphan")


# ── Cell Assessment ──────────────────────────────────────────────────────────────
# Ein Datensatz pro Zelle. ``data`` enthält die komplette KAP3-Bewertung:
#   {
#     "hazards":          {CODE: absoluter Wert, ...},
#     "exposures":        {CODE: absoluter Wert, ...},
#     "vulnerabilities":  {CODE: absoluter Wert, ...},
#     "risks":            {CODE: {"index": 0-100, "outcome": float, "cost_eur": float}, ...},
#     "inputs":           {... Rohgrößen (Versiegelung, ΔT, Bevölkerung, ...) ...}
#   }

class CellAssessment(Base):
    __tablename__ = "cell_assessments"
    __table_args__ = (
        UniqueConstraint("kommune_id", "grid_cell_id", name="uq_cell_assessment"),
    )

    id = Column(Integer, primary_key=True, index=True)
    kommune_id = Column(Integer, ForeignKey("kommunen.id", ondelete="CASCADE"), nullable=False)
    grid_cell_id = Column(Integer, ForeignKey("grid_cells.id", ondelete="CASCADE"), nullable=False)
    data = Column(JSON, default=dict)
    calculated_at = Column(DateTime, default=datetime.utcnow)

    kommune = relationship("Kommune", back_populates="assessments")
    grid_cell = relationship("GridCell", back_populates="assessments")


# ── Config Parameters ──────────────────────────────────────────────────────────

class ConfigParameter(Base):
    __tablename__ = "config_parameters"
    __table_args__ = (
        UniqueConstraint("kommune_id", "category", "key", name="uq_config_kommune_cat_key"),
    )

    id = Column(Integer, primary_key=True, index=True)
    kommune_id = Column(Integer, ForeignKey("kommunen.id", ondelete="CASCADE"), nullable=False)
    category = Column(String(100), nullable=False)
    key = Column(String(100), nullable=False)
    value = Column(JSON, nullable=False)
    description = Column(Text)

    kommune = relationship("Kommune", back_populates="config_params")


# ── Adaptation Measures ────────────────────────────────────────────────────────

class AdaptationMeasure(Base):
    __tablename__ = "adaptation_measures"

    id = Column(Integer, primary_key=True, index=True)
    kommune_id = Column(Integer, ForeignKey("kommunen.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    measure_type = Column(String(100), nullable=False)
    geometry = Column(Geometry("POLYGON", srid=4326), nullable=False)
    config = Column(JSON, default=dict)
    implementation_year = Column(Integer)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    kommune = relationship("Kommune", back_populates="measures")
    impacts = relationship("MeasureImpact", back_populates="measure", cascade="all, delete-orphan")


# ── Measure Impact ─────────────────────────────────────────────────────────────

class MeasureImpact(Base):
    __tablename__ = "measure_impacts"

    id = Column(Integer, primary_key=True, index=True)
    measure_id = Column(Integer, ForeignKey("adaptation_measures.id", ondelete="CASCADE"), nullable=False)
    grid_cell_id = Column(Integer, ForeignKey("grid_cells.id", ondelete="CASCADE"), nullable=False)
    indicator_deltas = Column(JSON, default=dict)
    costs = Column(JSON, default=dict)
    savings = Column(JSON, default=dict)

    measure = relationship("AdaptationMeasure", back_populates="impacts")
    grid_cell = relationship("GridCell", back_populates="measure_impacts")


# ── Project Status ─────────────────────────────────────────────────────────────

class ProjectStatus(Base):
    __tablename__ = "project_statuses"
    __table_args__ = (
        UniqueConstraint("kommune_id", "task_key", "level",
                         name="uq_status_kommune_task_level"),
    )

    id = Column(Integer, primary_key=True, index=True)
    kommune_id = Column(Integer, ForeignKey("kommunen.id", ondelete="CASCADE"), nullable=False)
    task_key = Column(String(64), nullable=False, default="assessment")
    level = Column(Integer, nullable=False, default=1)
    progress_pct = Column(Float, default=0.0)
    status = Column(Enum(AssessmentStatus), default=AssessmentStatus.PENDING)
    message = Column(Text)
    started_at = Column(DateTime)
    finished_at = Column(DateTime)
    step_history = Column(JSON, default=list)   # [{label, detail, started, finished, pct_start, pct_end}]
    eta_seconds = Column(Float)                 # estimated seconds remaining

    kommune = relationship("Kommune", back_populates="project_statuses")


# ── Risk Zones ─────────────────────────────────────────────────────────────────

class RiskZone(Base):
    __tablename__ = "risk_zones"
    __table_args__ = (
        UniqueConstraint("kommune_id", "layer_code", "level", "zone_index",
                         name="uq_risk_zone_kommune_layer_level_idx"),
    )

    id = Column(Integer, primary_key=True, index=True)
    kommune_id = Column(Integer, ForeignKey("kommunen.id", ondelete="CASCADE"), nullable=False)
    layer_code = Column(String(64), nullable=False)
    level = Column(Integer, nullable=False, default=1)
    zone_index = Column(Integer, nullable=False)
    cell_count = Column(Integer, nullable=False, default=0)
    mean_risk = Column(Float, nullable=False, default=0.0)
    max_risk = Column(Float, nullable=False, default=0.0)
    area_m2 = Column(Float, nullable=False, default=0.0)
    centroid = Column(Geometry("POINT", srid=4326))
    calculated_at = Column(DateTime, default=datetime.utcnow)

    kommune = relationship("Kommune", back_populates="risk_zones")
    cells = relationship("RiskZoneCell", back_populates="risk_zone", cascade="all, delete-orphan")


class RiskZoneCell(Base):
    __tablename__ = "risk_zone_cells"

    id = Column(Integer, primary_key=True, index=True)
    risk_zone_id = Column(Integer, ForeignKey("risk_zones.id", ondelete="CASCADE"), nullable=False)
    grid_cell_id = Column(Integer, ForeignKey("grid_cells.id", ondelete="CASCADE"), nullable=False)
    risk_score = Column(Float, nullable=False, default=0.0)

    risk_zone = relationship("RiskZone", back_populates="cells")
    grid_cell = relationship("GridCell")


# ── Geo Export Jobs ────────────────────────────────────────────────────────────

class GeoExportJob(Base):
    __tablename__ = "geo_export_jobs"

    id = Column(Integer, primary_key=True, index=True)
    kommune_id = Column(Integer, ForeignKey("kommunen.id", ondelete="CASCADE"), nullable=False)
    export_type = Column(String(32), nullable=False, default="geodaten")
    status = Column(Enum(ExportStatus), default=ExportStatus.PENDING)
    file_path = Column(String(512))
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime)

    kommune = relationship("Kommune", back_populates="geo_exports")
