"""Bundesvergleich der Systembereiche (Konformitätszeile 10): Dienst und Route."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.api.deps import require_kommune_access
from app.data import catalog
from app.main import app
from app.services.systembereiche_bundesanalyse import bundesanalyse_vergleich


def test_fuenf_bereiche_in_katalogreihenfolge():
    r = bundesanalyse_vergleich()
    assert [b["systembereich"] for b in r["bereiche"]] == list(catalog.KWRA_SYSTEMBEREICHE)
    assert len(r["bereiche"]) == 5


def test_je_bereich_risiko_und_anpassung():
    for b in bundesanalyse_vergleich()["bereiche"]:
        assert b["risiko"]["risiko_ohne_anpassung"]
        assert set(b["anpassung"]) >= {"wirksamkeit", "anpassungsdauer", "grenzen"}


def test_schluesse_und_methodische_grenze():
    r = bundesanalyse_vergleich()
    assert len(r["schluesse"]) >= 1
    assert r["methodische_grenze"]["aussage"]
    assert r["methodische_grenze"]["fussnote"] == 30


def test_route_liefert_dasselbe():
    vorher = app.dependency_overrides.get(require_kommune_access)
    app.dependency_overrides[require_kommune_access] = lambda: None
    try:
        antwort = TestClient(app).get("/api/catalog/systembereiche/bundesanalyse")
    finally:
        if vorher is None:
            app.dependency_overrides.pop(require_kommune_access, None)
        else:
            app.dependency_overrides[require_kommune_access] = vorher
    assert antwort.status_code == 200, antwort.text
    assert antwort.json() == bundesanalyse_vergleich()


def test_route_ohne_anmeldung_401():
    antwort = TestClient(app).get("/api/catalog/systembereiche/bundesanalyse")
    assert antwort.status_code == 401
