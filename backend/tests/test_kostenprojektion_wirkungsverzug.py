"""Hinweis zum Wirkungsverzug der Stadtbaumwahl in der Kostenprojektion (T-1724-cto).

Die Kostenprojektion rechnet Maßnahmen ab dem Umsetzungsjahr mit voller Wirkung.
Für die allergenarme Stadtbaumwahl (Bericht #96 §5) gilt das bei der Nachpflanzung
nicht: Der Nutzen je Jahr gilt erst mit voller Krone. ``project_costs`` führt dazu
das Feld ``hinweise_massnahmen`` (Liste von Texten, oberste Ebene des Ergebnisses);
``diskontierung.MODELLGRENZEN`` bleibt unberührt.

Läuft ohne Datenbank: Aggregat, Klimaprojektion, Szenariofaktoren und
Maßnahmenabfrage werden ersetzt, ``db`` bleibt ungenutzt.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.data import diskontierung
from app.services import cost_projection_service as cps
from app.services.measure_service import STADTBAUM_CODE

YEARS = list(range(2025, 2066))


class _FakeQuery:
    def __init__(self, measures):
        self._measures = measures

    def all(self):
        return self._measures


def _measure(mid, name, measure_type, year=2030):
    return SimpleNamespace(
        id=mid, name=name, measure_type=measure_type, implementation_year=year,
        impact_summary={"capex_eur": 1000.0, "opex_annual_eur": 10.0},
    )


def _fake_aggregate(db, kommune_id, apply_measures=False, demo_session_id=None):
    total = 800_000.0 if apply_measures else 1_000_000.0
    return {"cost": {"total_eur": total, "lower_bound": None,
                     "by_risk": [{"code": "TEST_RISK", "cost_eur": total}]}}


def _projektion(monkeypatch, measures):
    monkeypatch.setattr(cps, "get_risk_aggregate", _fake_aggregate)
    monkeypatch.setattr(cps, "get_climate_projection", lambda bl: {
        "years": YEARS,
        "scenarios": {"rcp45": {"label": "RCP4.5"}, "rcp85": {"label": "RCP8.5"}},
        "source": "Testdaten",
    })
    monkeypatch.setattr(cps, "scenario_factors",
                        lambda proj, scenario, group: [1.0] * len(YEARS))
    monkeypatch.setattr(cps, "kommune_measures_query",
                        lambda db, kommune_id, demo_session_id: _FakeQuery(measures))
    return cps.project_costs(db=None, kommune_id=1, bundesland="SN")


def test_mit_stadtbaumwahl_genau_ein_hinweis(monkeypatch):
    out = _projektion(monkeypatch, [
        _measure(1, "Allergenarme Stadtbaumwahl", STADTBAUM_CODE),
        _measure(2, "Entsiegelung", "DEPAVING"),
    ])
    hinweise = out["hinweise_massnahmen"]
    assert len(hinweise) == 1
    assert "Stadtbaumwahl" in hinweise[0]
    assert "Bericht #96 §5" in hinweise[0]


def test_mehrere_stadtbaumwahlen_bleiben_ein_hinweis(monkeypatch):
    out = _projektion(monkeypatch, [
        _measure(1, "Stadtbaumwahl Nord", STADTBAUM_CODE),
        _measure(2, "Stadtbaumwahl Süd", STADTBAUM_CODE, year=2035),
    ])
    assert len(out["hinweise_massnahmen"]) == 1


def test_ohne_stadtbaumwahl_leere_liste(monkeypatch):
    out = _projektion(monkeypatch, [_measure(2, "Entsiegelung", "DEPAVING")])
    assert out["hinweise_massnahmen"] == []


def test_ohne_massnahmen_leere_liste(monkeypatch):
    assert _projektion(monkeypatch, [])["hinweise_massnahmen"] == []


def test_modellgrenzen_bleiben_unberuehrt(monkeypatch):
    out = _projektion(monkeypatch, [_measure(1, "Stadtbaumwahl", STADTBAUM_CODE)])
    assert out["diskontierung"]["modellgrenzen"] == list(diskontierung.MODELLGRENZEN)
