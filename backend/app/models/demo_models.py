"""Demo-Kommune: anonyme Sitzungen + App-Einstellungen (Admin-konfiguriert).

Demo-Maßnahmen hängen über ``adaptation_measures.demo_session_id`` an einer
``DemoSession`` (ON DELETE CASCADE): läuft die Session ab (TTL-Sweep) oder
wird sie gelöscht, verschwinden ihre Maßnahmen mit. Produktpfade filtern
überall ``demo_session_id IS NULL`` — Demo-Daten verschmutzen nie Produkt-
Aggregate, -Exporte oder -Fingerprints.
"""
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, JSON, String

from app.db.database import Base


class DemoSession(Base):
    __tablename__ = "demo_sessions"

    id = Column(String(36), primary_key=True)  # UUID4
    created_at = Column(DateTime, default=datetime.utcnow)
    last_seen_at = Column(DateTime, default=datetime.utcnow, index=True)


class AppSetting(Base):
    """Key-Value-Einstellungen (JSON), z. B. Demo-Konfiguration."""
    __tablename__ = "app_settings"

    key = Column(String(100), primary_key=True)
    value = Column(JSON, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
