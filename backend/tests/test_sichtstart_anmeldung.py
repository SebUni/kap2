"""Lokale Anmeldung der Sichtprüfung (T-1771).

``get_current_user`` gibt ohne gültiges Login-Cookie einen nicht gespeicherten
Admin „Sichtprüfung (lokal)“ zurück — aber nur, wenn ``KAP2_SICHTSTART_ANMELDUNG``
genau ``1`` ist und der Client Loopback ist. Die Fälle (a) bis (d) laufen ohne
Datenbank: ``get_db`` ist durch einen Platzhalter ersetzt, der bei jedem Zugriff
fehlschlägt; ``/api/auth/me`` ohne Cookie und ``/api/kommune`` ohne Anmeldung
(401 vor jedem Datenbankzugriff) brauchen ihn nicht.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.api.deps import SICHTSTART_ENV
from app.db.database import get_db
from app.main import app


class _KeineDatenbank:
    def __getattr__(self, name):
        raise AssertionError(f"Datenbankzugriff in einem Test ohne Datenbank: {name}")


def _kein_db():
    yield _KeineDatenbank()


@pytest.fixture(autouse=True)
def _ohne_datenbank():
    alt = app.dependency_overrides.get(get_db)
    app.dependency_overrides[get_db] = _kein_db
    yield
    if alt is None:
        app.dependency_overrides.pop(get_db, None)
    else:
        app.dependency_overrides[get_db] = alt


@pytest.fixture(autouse=True)
def _variable_ungesetzt(monkeypatch):
    monkeypatch.delenv(SICHTSTART_ENV, raising=False)


def _mit_client(host: str):
    """ASGI-Hülle, die den Client des Scopes setzt (die Starlette-Fassung des
    Projekts kennt ``TestClient(client=…)`` nicht)."""
    async def asgi(scope, receive, send):
        if scope["type"] == "http":
            scope = {**scope, "client": (host, 50000)}
        await app(scope, receive, send)
    return asgi


def _client(host: str | None = None) -> TestClient:
    # Ohne Argument gilt die Vorgabe des TestClient: Client-Host „testclient“.
    if host is None:
        return TestClient(app)
    return TestClient(_mit_client(host))


def _nicht_angemeldet(client: TestClient) -> None:
    r = client.get("/api/auth/me")
    assert r.status_code == 200
    assert r.json() == {"authenticated": False}
    assert client.get("/api/kommune").status_code == 401


def test_a_ohne_variable_nicht_angemeldet():
    _nicht_angemeldet(_client())
    # Auch von Loopback aus, solange die Variable fehlt.
    _nicht_angemeldet(_client("127.0.0.1"))


@pytest.mark.parametrize("host", ["127.0.0.1", "::1"])
def test_b_variable_und_loopback_admin(monkeypatch, host):
    monkeypatch.setenv(SICHTSTART_ENV, "1")
    r = _client(host).get("/api/auth/me")
    assert r.status_code == 200
    body = r.json()
    assert body["authenticated"] is True
    assert body["user"]["role"] == "admin"
    assert body["user"]["display_name"] == "Sichtprüfung (lokal)"


def test_c_variable_aber_fremder_client(monkeypatch):
    monkeypatch.setenv(SICHTSTART_ENV, "1")
    _nicht_angemeldet(_client())  # Host „testclient“
    _nicht_angemeldet(_client("192.0.2.10"))


@pytest.mark.parametrize("wert", ["0", "", "true", "yes", "11", " 1", "1 "])
def test_d_anderer_wert_als_eins(monkeypatch, wert):
    monkeypatch.setenv(SICHTSTART_ENV, wert)
    _nicht_angemeldet(_client("127.0.0.1"))
    _nicht_angemeldet(_client())
