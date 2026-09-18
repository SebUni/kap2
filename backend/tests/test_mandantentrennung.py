"""Fundament der Mandantentrennungs-Prüfungen (T-0340, Teilpaket 1 aus T-0337).

Diese Datei bringt zwei Dinge mit, auf denen die eigentlichen vier
Trennungsprüfungen (Teilpaket 2) aufsetzen:

(a) Einen **in dieser Datei selbstständigen Testaufbau**: SQLite-Datenbank mit
    den Auth-Tabellen aus ``app/models/auth_models.py`` und schlank von Hand
    angelegten Tabellen ``kommunen`` und ``adaptation_measures``, zwei Kommunen
    A und B, ein angemeldeter Nutzer der Rolle ``user`` mit Zuordnung zu
    Kommune A, ein Nutzer der Rolle ``user`` ohne jede Zeile in
    ``user_kommunen``, ein Nutzer der Rolle ``admin`` sowie ``TestClient``s auf
    der App. In ``backend/tests`` gibt es keine gemeinsame ``conftest.py``;
    dieser Aufbau bleibt deshalb bewusst lokal und ändert nichts Gemeinsames.

    Warum die beiden Produkttabellen von Hand statt aus dem ORM: ``kommunen``
    und ``adaptation_measures`` tragen PostGIS-Geometriespalten, die auf SQLite
    weder anlegbar noch über das ORM beschreibbar sind. Die Geometriespalten
    sind hier als einfache Textspalten geführt und bleiben leer — für die
    Zugriffsprüfungen (``kommune_id``, ``demo_session_id``) reicht das.

(b) Eine Funktion, die die Prüfliste **zur Laufzeit aus der Routing-Tabelle der
    App** erzeugt (``kommunenbezogene_routen``): jede ``APIRoute``, die
    ``require_kommune_access`` als Router-Dependency trägt und einen Pfad- oder
    Abfrageparameter für die Kommune führt. So wächst die Prüfliste mit, wenn
    ein neuer Router an ``_PROTECTED`` gehängt wird (``app/main.py``), statt in
    einer Testdatei zu veralten.
"""

from __future__ import annotations

import secrets
from dataclasses import dataclass
from datetime import datetime

import pytest
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.deps import SESSION_COOKIE, require_kommune_access
from app.db.database import Base, get_db
from app.main import app
from app.models.auth_models import (
    ROLE_ADMIN,
    ROLE_USER,
    User,
    UserSession,
    user_kommunen,
)
from app.services import auth_service

# ─────────────────────────────────────────────────────────────────────────────
# (a) Testaufbau: Schema, Stammdaten, Prinzipale, Clients
# ─────────────────────────────────────────────────────────────────────────────

KOMMUNE_A_ID = 1
KOMMUNE_B_ID = 2
KOMMUNE_A_NAME = "Alpenstadt"
KOMMUNE_B_NAME = "Buchenheim"

# Schlanke Handanlage: nur die Spalten, die die Zugriffsprüfungen brauchen.
# Geometriespalten (PostGIS) als Text, damit ORM-Lesezugriffe NULL sehen.
_DDL_KOMMUNEN = """
CREATE TABLE kommunen (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    bundesland VARCHAR(100),
    landkreis VARCHAR(150),
    osm_id VARCHAR(50),
    boundary TEXT,
    area_km2 FLOAT,
    population INTEGER,
    created_at DATETIME
)
"""

_DDL_MEASURES = """
CREATE TABLE adaptation_measures (
    id INTEGER PRIMARY KEY,
    kommune_id INTEGER NOT NULL REFERENCES kommunen(id) ON DELETE CASCADE,
    demo_session_id VARCHAR(36),
    name VARCHAR(255) NOT NULL,
    measure_type VARCHAR(100) NOT NULL,
    geometry TEXT,
    config TEXT,
    impact_summary TEXT,
    implementation_year INTEGER,
    description TEXT,
    created_at DATETIME
)
"""


def _lege_schema_an(engine) -> None:
    """Produkttabellen von Hand, Auth-Tabellen aus dem ORM-Metadata."""
    with engine.begin() as conn:
        conn.execute(text(_DDL_KOMMUNEN))
        conn.execute(text(_DDL_MEASURES))
    Base.metadata.create_all(
        bind=engine,
        tables=[User.__table__, UserSession.__table__, user_kommunen],
    )


def _lege_kommunen_an(engine) -> None:
    with engine.begin() as conn:
        for kommune_id, name in (
            (KOMMUNE_A_ID, KOMMUNE_A_NAME),
            (KOMMUNE_B_ID, KOMMUNE_B_NAME),
        ):
            conn.execute(
                text("INSERT INTO kommunen (id, name, created_at) VALUES (:i, :n, :t)"),
                {"i": kommune_id, "n": name, "t": datetime.utcnow()},
            )


def _lege_nutzer_an(db, email: str, rolle: str) -> User:
    # Kennwort zur Laufzeit erzeugt: kein Literal im Quelltext.
    kennwort = secrets.token_urlsafe(12)
    nutzer = User(
        email=email,
        display_name=email.split("@")[0],
        role=rolle,
        is_active=True,
        created_at=datetime.utcnow(),
    )
    nutzer.password_hash = auth_service.hash_password(kennwort)
    db.add(nutzer)
    db.commit()
    db.refresh(nutzer)
    return nutzer


@dataclass
class Aufbau:
    """Alles, was die Trennungsprüfungen brauchen — in einem Objekt."""

    engine: object
    session_factory: object
    nutzer_a_id: int
    nutzer_ohne_id: int
    admin_id: int
    kommune_a_id: int = KOMMUNE_A_ID
    kommune_b_id: int = KOMMUNE_B_ID

    def sitzung(self):
        """Neue DB-Session auf der Testdatenbank."""
        return self.session_factory()

    def client_fuer(self, nutzer_id: int) -> TestClient:
        """TestClient mit gültigem Login-Cookie des genannten Nutzers."""
        client = TestClient(app)
        with self.sitzung() as db:
            nutzer = db.get(User, nutzer_id)
            anmeldung = auth_service.create_session(db, nutzer)
        client.cookies.set(SESSION_COOKIE, anmeldung)
        return client


@pytest.fixture(scope="module")
def aufbau():
    """SQLite-Datenbank, Stammdaten, drei Prinzipale, get_db-Override."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    _lege_schema_an(engine)
    _lege_kommunen_an(engine)
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    with session_factory() as db:
        nutzer_a = _lege_nutzer_an(db, "nutzer-a@example.test", ROLE_USER)
        nutzer_ohne = _lege_nutzer_an(db, "nutzer-ohne@example.test", ROLE_USER)
        admin = _lege_nutzer_an(db, "admin@example.test", ROLE_ADMIN)
        # Nur Nutzer A bekommt eine Zuordnung; nutzer_ohne bleibt ohne Zeile.
        db.execute(
            user_kommunen.insert().values(user_id=nutzer_a.id, kommune_id=KOMMUNE_A_ID)
        )
        db.commit()
        ids = (nutzer_a.id, nutzer_ohne.id, admin.id)

    def _get_db_override():
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    vorher = app.dependency_overrides.get(get_db)
    app.dependency_overrides[get_db] = _get_db_override
    try:
        yield Aufbau(engine, session_factory, *ids)
    finally:
        if vorher is None:
            app.dependency_overrides.pop(get_db, None)
        else:
            app.dependency_overrides[get_db] = vorher
        engine.dispose()


@pytest.fixture()
def client_a(aufbau) -> TestClient:
    """Angemeldeter Nutzer der Rolle ``user``, zugeordnet zu Kommune A."""
    return aufbau.client_fuer(aufbau.nutzer_a_id)


@pytest.fixture()
def client_ohne_kommune(aufbau) -> TestClient:
    """Angemeldeter Nutzer der Rolle ``user`` ohne jede Kommune-Zuordnung."""
    return aufbau.client_fuer(aufbau.nutzer_ohne_id)


@pytest.fixture()
def client_admin(aufbau) -> TestClient:
    """Angemeldeter Nutzer der Rolle ``admin``."""
    return aufbau.client_fuer(aufbau.admin_id)


@pytest.fixture()
def client_anonym(aufbau) -> TestClient:
    """TestClient ohne Login-Cookie."""
    return TestClient(app)


# ─────────────────────────────────────────────────────────────────────────────
# (b) Prüfliste zur Laufzeit aus der Routing-Tabelle
# ─────────────────────────────────────────────────────────────────────────────

# HEAD/OPTIONS erzeugt Starlette selbst; sie sind keine eigenen Prüffälle.
_NICHT_GEPRUEFTE_METHODEN = {"HEAD", "OPTIONS"}
# Ein Parameter gilt als Kommune-Parameter, wenn sein Name die Kommune nennt
# (heute durchgängig ``kommune_id``).
_KOMMUNE_MARKER = "kommune"


@dataclass(frozen=True)
class KommuneRoute:
    """Eine kommunenbezogene, durch ``require_kommune_access`` geschützte Route."""

    pfad: str
    name: str
    methoden: tuple[str, ...]
    pfad_parameter: tuple[str, ...]
    abfrage_parameter: tuple[str, ...]


def _traegt_kommune_guard(route: APIRoute) -> bool:
    """Trägt die Route ``require_kommune_access`` als Router-Dependency?"""
    return any(
        getattr(dep, "dependency", None) is require_kommune_access
        for dep in getattr(route, "dependencies", ()) or ()
    )


def _kommune_parameter(route: APIRoute) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """(Pfadparameter, Abfrageparameter), die die Kommune benennen."""
    pfad = tuple(sorted(
        name for name in getattr(route, "param_convertors", {})
        if _KOMMUNE_MARKER in name.lower()
    ))
    abfrage = tuple(sorted(
        p.name for p in route.dependant.query_params
        if _KOMMUNE_MARKER in p.name.lower()
    ))
    return pfad, abfrage


def kommunenbezogene_routen(anwendung=None) -> list[KommuneRoute]:
    """Prüfliste zur Laufzeit: alle kommunenbezogenen, geschützten Routen.

    Gelesen wird die Routing-Tabelle der App, nicht eine gepflegte Liste. Eine
    Route kommt in die Liste, wenn sie (1) eine ``APIRoute`` ist, (2)
    ``require_kommune_access`` als Router-Dependency trägt und (3) einen Pfad-
    oder Abfrageparameter für die Kommune führt.
    """
    anwendung = anwendung if anwendung is not None else app
    treffer: list[KommuneRoute] = []
    for route in anwendung.routes:
        if not isinstance(route, APIRoute):
            continue
        if not _traegt_kommune_guard(route):
            continue
        pfad_parameter, abfrage_parameter = _kommune_parameter(route)
        if not pfad_parameter and not abfrage_parameter:
            continue
        methoden = tuple(sorted(set(route.methods or ()) - _NICHT_GEPRUEFTE_METHODEN))
        if not methoden:
            continue
        treffer.append(KommuneRoute(
            pfad=route.path,
            name=route.name,
            methoden=methoden,
            pfad_parameter=pfad_parameter,
            abfrage_parameter=abfrage_parameter,
        ))
    return treffer


def route_methode_kombinationen(routen=None) -> list[tuple[KommuneRoute, str]]:
    """Prüffälle: jede Route einzeln je HTTP-Methode."""
    routen = routen if routen is not None else kommunenbezogene_routen()
    return [(route, methode) for route in routen for methode in route.methoden]


# ─────────────────────────────────────────────────────────────────────────────
# Tests
# ─────────────────────────────────────────────────────────────────────────────

def test_pruefliste_ist_nicht_leer():
    """Ohne Prüfliste prüft Teilpaket 2 nichts — dann muss es hier knallen."""
    routen = kommunenbezogene_routen()
    assert routen, (
        "Keine kommunenbezogene Route mit require_kommune_access gefunden — "
        "entweder hängt kein Router mehr an _PROTECTED (app/main.py) oder die "
        "Erkennung in kommunenbezogene_routen() passt nicht mehr zur App."
    )
    assert route_methode_kombinationen(routen), "Prüffälle ohne HTTP-Methode"


def test_aufbau_liefert_kommunen_und_prinzipale(aufbau, client_a, client_ohne_kommune,
                                                client_admin, client_anonym):
    """Der Testaufbau steht: zwei Kommunen, drei Prinzipale, lebende Sessions."""
    with aufbau.sitzung() as db:
        namen = [
            r.name for r in db.execute(
                text("SELECT name FROM kommunen ORDER BY id")
            ).all()
        ]
        assert namen == [KOMMUNE_A_NAME, KOMMUNE_B_NAME]

        zuordnungen = db.execute(user_kommunen.select()).all()
        assert [(r.user_id, r.kommune_id) for r in zuordnungen] == [
            (aufbau.nutzer_a_id, KOMMUNE_A_ID)
        ]

        assert db.get(User, aufbau.nutzer_a_id).role == ROLE_USER
        assert db.get(User, aufbau.nutzer_ohne_id).role == ROLE_USER
        assert db.get(User, aufbau.admin_id).is_admin is True
        assert db.query(UserSession).count() == 3  # drei angemeldete Clients

    assert client_anonym.cookies.get(SESSION_COOKIE) is None
    for client, nutzer_id in (
        (client_a, aufbau.nutzer_a_id),
        (client_ohne_kommune, aufbau.nutzer_ohne_id),
        (client_admin, aufbau.admin_id),
    ):
        assert client.cookies.get(SESSION_COOKIE)
        antwort = client.get("/api/auth/me")
        assert antwort.status_code == 200, antwort.text
        daten = antwort.json()
        assert daten["authenticated"] is True
        assert daten["user"]["id"] == nutzer_id
