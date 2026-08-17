"""Nutzer, Sessions und Kommune-Zuordnung (Login-Bereich + Admin).

Auth-Modell: DB-gestützte Session-Cookies (kein JWT) — Sessions sind sofort
revozierbar (Admin deaktiviert Nutzer → Session tot), kein Key-Management.
Das Session-Token selbst wird NIE gespeichert, nur sein SHA-256-Hash.
"""
from datetime import datetime

from sqlalchemy import (
    Boolean, Column, DateTime, ForeignKey, Integer, String, Table,
)
from sqlalchemy.orm import relationship

from app.db.database import Base

ROLE_ADMIN = "admin"
ROLE_USER = "user"

# Zuordnung Nutzer ↔ Kommune: normale Nutzer sehen nur zugeordnete Kommunen.
user_kommunen = Table(
    "user_kommunen",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("kommune_id", Integer, ForeignKey("kommunen.id", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    display_name = Column(String(255))
    # String statt Enum: kein PG-Enum-Migrationsaufwand für zwei Werte.
    role = Column(String(20), nullable=False, default=ROLE_USER)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login_at = Column(DateTime)

    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    kommunen = relationship("Kommune", secondary=user_kommunen)

    @property
    def is_admin(self) -> bool:
        return self.role == ROLE_ADMIN


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    token_hash = Column(String(64), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    last_seen_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="sessions")
