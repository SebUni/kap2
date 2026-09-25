"""Rauchtest der Route ``GET /api/kommune/{id}/systembereiche`` (Konformitätszeile 10).

Anmeldung (``require_kommune_access``) wird über ``app.dependency_overrides``
ersetzt; die Datenbank liefert der Testaufbau aus ``test_mandantentrennung.py``.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_kommune_access
from app.data import catalog
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


def test_unbekannte_kommune_404(client):
    antwort = client.get(f"/api/kommune/{UNBEKANNTE_KOMMUNE_ID}/systembereiche")
    assert antwort.status_code == 404, antwort.text


def test_fuenf_bereiche_in_katalogreihenfolge(client):
    antwort = client.get(f"/api/kommune/{KOMMUNE_A_ID}/systembereiche")
    assert antwort.status_code == 200, antwort.text
    bereiche = antwort.json()["bereiche"]
    assert len(bereiche) == 5
    assert [b["systembereich"] for b in bereiche] == list(catalog.KWRA_SYSTEMBEREICHE)


def test_leer_grund_je_leerem_bereich(client):
    bereiche = client.get(f"/api/kommune/{KOMMUNE_A_ID}/systembereiche").json()["bereiche"]
    for b in bereiche:
        if b["anzahl_klimawirkungen"] == 0:
            assert isinstance(b["leer_grund"], str) and b["leer_grund"].strip()
        else:
            assert b["leer_grund"] is None
    # Ohne Aggregat (Testkommune ohne Berechnung) sind alle fünf leer.
    assert all(b["anzahl_klimawirkungen"] == 0 for b in bereiche)
