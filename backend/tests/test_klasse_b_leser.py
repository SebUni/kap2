"""Verwechslungssperre Klasse A/B: Leser von ``cost_eur`` vertragen None (T-0879).

Die Inventur aller Fundstellen von ``cost_eur`` unter ``backend/app`` steht im
Ergebnis von T-0879. Je Stelle, die dort als **behoben** geführt ist, gibt es hier
genau eine Testfunktion ``test_leser_<modul>_<funktion>``. Sie durchläuft die Stelle
mit der Testwirkung aus ``tests/klasse_b_testwirkung.py`` (Katalog unverändert) und
einem echten Aggregat aus ``risk_engine.aggregate``, in dem ``cost_eur`` der
Klasse-B-Wirkung None ist.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_kommune_access
from app.data import catalog
from app.main import app
from app.services.engine import risk_engine

from tests.klasse_b_testwirkung import KLASSE_B_CODE, wirkung_einhaengen
from test_mandantentrennung import KOMMUNE_A_ID, aufbau  # noqa: F401  (Fixture)


@pytest.fixture
def wirkung(monkeypatch):
    return wirkung_einhaengen(monkeypatch)


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


def _aggregate() -> dict:
    """Aggregat über den aktuellen Katalog samt Testwirkung (zwei Zellen)."""
    werte = {r["code"]: {"index": 40.0, "outcome": 1.0,
                         "cost_eur": r["cost_per_outcome_eur"]} for r in catalog.RISKS}
    zellen = [{"risks": dict(werte), "inputs": {"pop": 250.0}} for _ in range(2)]
    return risk_engine.aggregate(zellen, total_pop=500.0, area_km2=2.0)


def test_leser_kommune_get_kommune_kang_nachweis(wirkung, client, monkeypatch):
    """KAnG-Nachweis: die Klasse-B-Wirkung erscheint ohne Betrag (None), nie mit 0 €,
    und geht in keine Feldsumme ein."""
    from app.api.routes import kommune as kommune_route

    agg = _aggregate()
    eintrag = next(e for e in agg["cost"]["by_risk"] if e["code"] == KLASSE_B_CODE)
    assert eintrag["cost_eur"] is None  # Voraussetzung: Sperre an der Quelle
    monkeypatch.setattr(kommune_route, "assessment_is_done", lambda *a, **k: True)
    monkeypatch.setattr(kommune_route, "get_risk_aggregate", lambda *a, **k: agg)
    monkeypatch.setattr(kommune_route, "kommune_measures_query",
                        lambda *a, **k: _LeereAbfrage())

    antwort = client.get(f"/api/kommune/{KOMMUNE_A_ID}/kang-nachweis")
    assert antwort.status_code == 200, antwort.text
    daten = antwort.json()

    # Die Testwirkung trägt kein ``kwra_field`` und landet deshalb unter
    # ``nicht_zugeordnet`` — dort mit None statt eines Betrags.
    b_zeilen = [r for r in daten["nicht_zugeordnet"]["risiken"] if r["code"] == KLASSE_B_CODE]
    assert b_zeilen == [{"code": KLASSE_B_CODE, "schaden_eur": None}]
    # In keinem Handlungsfeld zählt sie mit.
    for feld in daten["handlungsfelder"]:
        assert KLASSE_B_CODE not in feld["risiken"]


class _LeereAbfrage:
    """Maßnahmen-Abfrage ohne Treffer (die Test-DB kennt keine Maßnahmen)."""

    def options(self, *a, **k):
        return self

    def __iter__(self):
        return iter(())
