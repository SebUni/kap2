"""Rauchtest der Route ``GET /api/kommune/{id}/systembereiche`` (Konformitätszeile 10).

Anmeldung (``require_kommune_access``) wird über ``app.dependency_overrides``
ersetzt; die Datenbank liefert der Testaufbau aus ``test_mandantentrennung.py``.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.api.routes import kommune as kommune_routen
from app.api.deps import require_kommune_access
from app.data import catalog
from app.main import app

from test_mandantentrennung import KOMMUNE_A_ID, aufbau  # noqa: F401  (Fixture)

UNBEKANNTE_KOMMUNE_ID = 999999
MENSCHEN = "Menschen und soziale Systeme"


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


def test_fuenf_bereiche_in_katalogreihenfolge(client, monkeypatch):
    monkeypatch.setattr(kommune_routen, "assessment_is_done", lambda db, kid: False)
    antwort = client.get(f"/api/kommune/{KOMMUNE_A_ID}/systembereiche")
    assert antwort.status_code == 200, antwort.text
    bereiche = antwort.json()["bereiche"]
    assert len(bereiche) == 5
    assert [b["systembereich"] for b in bereiche] == list(catalog.KWRA_SYSTEMBEREICHE)


def _pruefe_leer_grund(bereiche):
    for b in bereiche:
        if b["anzahl_klimawirkungen"] == 0:
            assert isinstance(b["leer_grund"], str) and b["leer_grund"].strip()
        else:
            assert b["leer_grund"] is None


def test_ohne_berechnung_alle_fuenf_leer_mit_grund(client, monkeypatch):
    monkeypatch.setattr(kommune_routen, "assessment_is_done", lambda db, kid: False)

    def _nicht_aufrufen(*a, **k):
        raise AssertionError("Aggregat darf ohne Berechnung nicht geholt werden")

    monkeypatch.setattr(kommune_routen, "get_risk_aggregate", _nicht_aufrufen)
    bereiche = client.get(f"/api/kommune/{KOMMUNE_A_ID}/systembereiche").json()["bereiche"]
    assert len(bereiche) == 5
    assert all(b["anzahl_klimawirkungen"] == 0 for b in bereiche)
    assert all(b["schadenskosten_eur"] is None for b in bereiche)
    _pruefe_leer_grund(bereiche)


def test_mit_aggregat_vier_leer_einer_belegt(client, monkeypatch):
    code = next(c for c, b in catalog.RISK_SYSTEMBEREICH.items()
                if b == MENSCHEN and c not in catalog.NON_ADDITIVE_RISK_CODES)
    agg = {"cost": {"by_risk": [{"code": code, "cost_eur": 1000.0, "index": 40.0}]}}
    monkeypatch.setattr(kommune_routen, "assessment_is_done", lambda db, kid: True)
    monkeypatch.setattr(kommune_routen, "get_risk_aggregate", lambda *a, **k: agg)
    bereiche = client.get(f"/api/kommune/{KOMMUNE_A_ID}/systembereiche").json()["bereiche"]
    assert [b["systembereich"] for b in bereiche] == list(catalog.KWRA_SYSTEMBEREICHE)
    belegt = [b for b in bereiche if b["anzahl_klimawirkungen"] > 0]
    assert [b["systembereich"] for b in belegt] == [MENSCHEN]
    assert belegt[0]["leer_grund"] is None
    _pruefe_leer_grund(bereiche)
    assert sum(1 for b in bereiche if b["leer_grund"]) == 4
