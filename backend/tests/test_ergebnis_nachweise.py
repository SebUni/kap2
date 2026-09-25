"""Nachweisfelder zur Einbeziehung (ISO 14091 A6/A10), ohne Datenbankserver.

Die Tabelle ``kommunen`` nutzt Geometry (PostGIS) und wird deshalb für SQLite
von Hand angelegt; ``ergebnis_nachweise`` kommt aus dem ORM-Metadata.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta

import pytest
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base
from app.models.models import ErgebnisNachweis
from app.services.ergebnis_nachweise import (
    NACHWEIS_ARTEN,
    NICHT_ERFASST,
    nachweis_anlegen,
    nachweis_loeschen,
    nachweise,
)

KOMMUNE_ID = 1


@pytest.fixture()
def db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def _fk_an(dbapi_conn, _):
        dbapi_conn.execute("PRAGMA foreign_keys=ON")

    with engine.begin() as conn:
        conn.execute(text(
            "CREATE TABLE kommunen (id INTEGER PRIMARY KEY, name VARCHAR(255), created_at DATETIME)"
        ))
        conn.execute(
            text("INSERT INTO kommunen (id, name, created_at) VALUES (:i, :n, :t)"),
            {"i": KOMMUNE_ID, "n": "Beispielstadt", "t": datetime.utcnow()},
        )
    Base.metadata.create_all(bind=engine, tables=[ErgebnisNachweis.__table__])
    sitzung = sessionmaker(bind=engine)()
    try:
        yield sitzung
    finally:
        sitzung.close()
        engine.dispose()


def _nach_art(liste):
    return {zeile["art"]: zeile for zeile in liste}


def test_kommune_ohne_eintraege_viermal_nicht_erfasst(db):
    assert set(NACHWEIS_ARTEN) == {
        "fachabteilung", "externe_expertise", "angrenzende_kommune", "land",
    }
    liste = nachweise(db, KOMMUNE_ID)
    assert len(liste) == 4
    assert {zeile["art"] for zeile in liste} == set(NACHWEIS_ARTEN)
    for zeile in liste:
        assert zeile["status"] == NICHT_ERFASST == "nicht erfasst"
        assert zeile["eintraege"] == []
        assert zeile["bezeichnung"]


def test_eintrag_fachabteilung(db):
    tag = date(2026, 9, 1)
    nachweis_anlegen(
        db, KOMMUNE_ID, "fachabteilung", "Gesundheitsamt Landkreis Beispiel", tag,
        vermerk="Ergebnisse zu Hitze gelesen",
    )
    zeilen = _nach_art(nachweise(db, KOMMUNE_ID))

    fach = zeilen["fachabteilung"]
    assert fach["status"] is None
    assert len(fach["eintraege"]) == 1
    assert fach["eintraege"][0]["stelle"] == "Gesundheitsamt Landkreis Beispiel"
    assert fach["eintraege"][0]["datum"] == tag
    assert fach["eintraege"][0]["vermerk"] == "Ergebnisse zu Hitze gelesen"

    for art in ("externe_expertise", "angrenzende_kommune", "land"):
        assert zeilen[art]["status"] == "nicht erfasst"
        assert zeilen[art]["eintraege"] == []


def test_ungueltige_eingaben_loesen_value_error_aus(db):
    heute = date.today()
    with pytest.raises(ValueError):
        nachweis_anlegen(db, KOMMUNE_ID, "buergerschaft", "Stadtrat", heute)
    with pytest.raises(ValueError):
        nachweis_anlegen(db, KOMMUNE_ID, "land", "   ", heute)
    with pytest.raises(ValueError):
        nachweis_anlegen(
            db, KOMMUNE_ID, "land", "Landesamt für Umwelt", heute + timedelta(days=1)
        )
    assert db.query(ErgebnisNachweis).count() == 0


def test_loeschen(db):
    eintrag = nachweis_anlegen(
        db, KOMMUNE_ID, "land", "Landesamt für Umwelt", date(2026, 8, 15)
    )
    assert _nach_art(nachweise(db, KOMMUNE_ID))["land"]["status"] is None

    assert nachweis_loeschen(db, KOMMUNE_ID, eintrag.id) is True
    assert _nach_art(nachweise(db, KOMMUNE_ID))["land"]["status"] == "nicht erfasst"
    assert nachweis_loeschen(db, KOMMUNE_ID, eintrag.id) is False
