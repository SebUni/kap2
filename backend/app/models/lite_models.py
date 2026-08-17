"""Deutschland-Lite: Gemeinden, vorberechnete Grob-Risiken, Batch-Läufe.

Die kostenlose Deutschland-Karte (Plan §4) rechnet EINEN Wert je Gemeinde und
Risiko — kein 100m-Grid. Quelle der Geometrien: BKG VG250 (~11.000 Gemeinden).
Ergebnisse werden vom admin-getriggerten Batch materialisiert und öffentlich
nur als statische Artefakte / Einzelzeilen-Lookups ausgeliefert.
"""
from datetime import datetime

from geoalchemy2 import Geometry
from sqlalchemy import (
    Column, DateTime, Float, ForeignKey, Integer, JSON, String, Text,
    UniqueConstraint,
)

from app.db.database import Base


class Gemeinde(Base):
    __tablename__ = "gemeinden"

    ags = Column(String(8), primary_key=True)  # amtlicher Gemeindeschlüssel
    name = Column(String(255), nullable=False)
    bez = Column(String(80))                    # Bezeichnung (Stadt/Gemeinde …)
    bundesland = Column(String(100))
    population = Column(Integer)                 # EWZ (VG250) bzw. Zensus-Summe
    area_km2 = Column(Float)                     # KFL (VG250)
    geometry = Column(Geometry("MULTIPOLYGON", srid=4326))
    # Vereinfachte Geometrie (GeoJSON-Text) für Artefakt-Export ohne PostGIS.
    geometry_simplified = Column(Text)
    rep_lon = Column(Float)                      # Repräsentationspunkt (Sampling)
    rep_lat = Column(Float)
    demographics = Column(JSON)                  # Zensus-Aggregat je Gemeinde
    vg250_stand = Column(String(10))             # Datenstand VG250
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class GemeindeLiteResult(Base):
    __tablename__ = "gemeinde_lite_results"
    __table_args__ = (
        UniqueConstraint("ags", "risk_code", name="uq_gemeinde_risk"),
    )

    id = Column(Integer, primary_key=True, index=True)
    ags = Column(String(8), ForeignKey("gemeinden.ags", ondelete="CASCADE"),
                 nullable=False, index=True)
    risk_code = Column(String(64), nullable=False, index=True)
    raw_score = Column(Float)          # H×E×V vor nationaler Normierung
    index_value = Column(Float)        # 0–100 nach p5–p95-Normierung
    outcome_value = Column(Float)      # ref × (index/100) × Skalierung
    outcome_unit = Column(String(32))
    cost_eur = Column(Float)
    drivers = Column(JSON)             # Treiberwerte + source_refs (Transparenz)
    batch_id = Column(Integer, ForeignKey("lite_batch_runs.id", ondelete="SET NULL"))
    computed_at = Column(DateTime, default=datetime.utcnow)


class LiteBatchRun(Base):
    __tablename__ = "lite_batch_runs"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(16), nullable=False, default="pending")  # pending/running/done/error/aborted
    phase = Column(String(32))
    progress_pct = Column(Float, default=0.0)
    processed = Column(Integer, default=0)
    total = Column(Integer, default=0)
    message = Column(Text)
    error_count = Column(Integer, default=0)
    params = Column(JSON)              # {bundesland?, force_zensus?}
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
