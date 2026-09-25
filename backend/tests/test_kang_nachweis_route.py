"""Rauchtest der Route ``GET /api/kommune/{id}/kang-nachweis`` (T-1064, Checkliste Zeile 13).

Die Route liefert den Nachweis der fachübergreifenden Berücksichtigung nach
§ 8 Abs. 1 KAnG aus ``kang_beruecksichtigung.nachweis_fachuebergreifend``.
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


def test_kang_nachweis_unbekannte_kommune_404(client):
    antwort = client.get(f"/api/kommune/{UNBEKANNTE_KOMMUNE_ID}/kang-nachweis")
    assert antwort.status_code == 404
    assert antwort.json()["detail"] == "Kommune nicht gefunden"


def test_kang_nachweis_vorhandene_kommune(client, monkeypatch):
    """Die Testdatenbank kennt keine Statustabelle; wie im Systembereiche-Test
    gilt die Berechnung als nicht erfolgt (kein Aggregat, ``schaeden`` leer)."""
    from app.api.routes import kommune as kommune_route

    monkeypatch.setattr(kommune_route, "assessment_is_done", lambda *a, **k: False)
    antwort = client.get(f"/api/kommune/{KOMMUNE_A_ID}/kang-nachweis")
    assert antwort.status_code == 200, antwort.text
    daten = antwort.json()
    for schluessel in ("handlungsfelder", "zusammenfassung", "abgrenzung"):
        assert schluessel in daten, schluessel
    assert isinstance(daten["abgrenzung"], str)
    assert daten["abgrenzung"].strip()


def test_kang_nachweis_unbekannter_risikocode_kein_500(client, monkeypatch):
    """Ein Code, den der Katalog nicht kennt, landet in ``nicht_zugeordnet`` statt im 500."""
    from app.api.routes import kommune as kommune_route

    monkeypatch.setattr(kommune_route, "assessment_is_done", lambda *a, **k: True)
    monkeypatch.setattr(kommune_route, "get_risk_aggregate", lambda *a, **k: {
        "cost": {"by_risk": [{"code": "GIBT_ES_NICHT", "cost_eur": 1234.0}]}})
    antwort = client.get(f"/api/kommune/{KOMMUNE_A_ID}/kang-nachweis")
    assert antwort.status_code == 200, antwort.text
    daten = antwort.json()
    assert daten["nicht_zugeordnet"]["risiken"] == [
        {"code": "GIBT_ES_NICHT", "schaden_eur": 1234.0}
    ]
