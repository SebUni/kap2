"""Rauchtest der Konformitäts-Schnittstellen (T-0900-ceo).

Ruft vier Routen wirklich auf (``TestClient`` gegen ``app.main.app``), damit sie
nicht nur auf Syntax geprüft sind:

- ``GET /api/catalog/charakterisierungsgruppen``
- ``GET /api/catalog/querverbindungen``
- ``GET /api/kommune/{id}/kang-zustaendigkeit``
- ``GET /api/kommune/{id}/unsicherheits-zusammenschau``

Anmeldung (``require_kommune_access``) wird über ``app.dependency_overrides``
ersetzt; die Datenbank (SQLite mit Kommunen A/B) liefert der Testaufbau aus
``test_mandantentrennung.py``. Eine echte Datenbank ist nicht nötig.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_kommune_access
from app.main import app

from test_mandantentrennung import KOMMUNE_A_ID, aufbau  # noqa: F401  (Fixture)

UNBEKANNTE_KOMMUNE_ID = 999999


@pytest.fixture()
def client(aufbau):  # noqa: F811
    """Client ohne Anmeldung: der Kommune-Guard ist überschrieben."""
    vorher = app.dependency_overrides.get(require_kommune_access)
    app.dependency_overrides[require_kommune_access] = lambda: None
    try:
        yield TestClient(app)
    finally:
        if vorher is None:
            app.dependency_overrides.pop(require_kommune_access, None)
        else:
            app.dependency_overrides[require_kommune_access] = vorher


def test_charakterisierungsgruppen_liefert_nicht_leeres_json(client):
    antwort = client.get("/api/catalog/charakterisierungsgruppen")
    assert antwort.status_code == 200, antwort.text
    daten = antwort.json()
    assert daten


def test_querverbindungen_hat_klimawirkungen(client):
    antwort = client.get("/api/catalog/querverbindungen")
    assert antwort.status_code == 200, antwort.text
    assert "klimawirkungen" in antwort.json()


def test_kang_zustaendigkeit_vorhandene_kommune(client):
    antwort = client.get(f"/api/kommune/{KOMMUNE_A_ID}/kang-zustaendigkeit")
    assert antwort.status_code == 200, antwort.text


def test_kang_zustaendigkeit_unbekannte_kommune_404(client):
    antwort = client.get(f"/api/kommune/{UNBEKANNTE_KOMMUNE_ID}/kang-zustaendigkeit")
    assert antwort.status_code == 404


def test_unsicherheits_zusammenschau_vorhandene_kommune(client):
    antwort = client.get(f"/api/kommune/{KOMMUNE_A_ID}/unsicherheits-zusammenschau")
    assert antwort.status_code == 200, antwort.text
    daten = antwort.json()
    for schluessel in ("handlungsfelder", "handlungsfelder_vorsicht", "hinweis"):
        assert schluessel in daten, schluessel


def test_unsicherheits_zusammenschau_unbekannte_kommune_404(client):
    antwort = client.get(f"/api/kommune/{UNBEKANNTE_KOMMUNE_ID}/unsicherheits-zusammenschau")
    assert antwort.status_code == 404
