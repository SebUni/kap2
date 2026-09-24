"""Reine Screening-Maßnahme mit direktem Zusatznutzen zeigt den Betrag mit Zusatz (T-0872).

Der direkte Zusatznutzen (``benefit_per_m2_year``) ist ein eigener, belegter Parameter
und kein Klasse-B-Schadensbetrag. Geprüft wird am echten ``_compute_impact_scoped``
mit Testwirkungen nach dem Muster ``_klasse_b_eintrag``:

(1) direkter Nutzen > 0: ``benefit_display`` None, Zusatz „ohne 1 Wirkung im Screening“,
    ``benefit_has_euro_layer`` False, kein Schadensnutzen;
(2) direkter Nutzen 0: Vermerktext wie bisher.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.data import catalog
from app.models.models import CellAssessment, Kommune, MeasureImpact
from app.services import measure_service

KLASSE_B_CODE = "TEST_KLASSE_B_DIREKT"


def _klasse_b_eintrag(code: str) -> dict:
    return {
        "code": code, "name": f"Testwirkung {code}", "group": "health",
        "outcome_unit": "Fälle/Jahr", "ref_value": 10.0, "scale": "pop",
        "cost_per_outcome_eur": 1000.0, "cost_dimension": "health",
        "cost_source": "Testquelle", "euro_layer": False,
    }


@pytest.fixture
def klasse_b(monkeypatch):
    e = _klasse_b_eintrag(KLASSE_B_CODE)
    monkeypatch.setitem(catalog.RISKS_BY_CODE, e["code"], e)
    monkeypatch.setattr(catalog, "RISKS", list(catalog.RISKS) + [e])


class _Query:
    def __init__(self, rows):
        self._rows = list(rows)

    def filter(self, *a, **k):
        return self

    filter_by = filter

    def all(self):
        return list(self._rows)

    def first(self):
        return self._rows[0] if self._rows else None

    def delete(self):
        return 0


class _Session:
    def __init__(self, cells, kommune):
        self._rows = {CellAssessment: cells, Kommune: [kommune], MeasureImpact: []}

    def query(self, model):
        return _Query(self._rows.get(model, []))

    def add(self, obj):
        pass

    def commit(self):
        pass


def _rechne(monkeypatch, direkt: float) -> dict:
    monkeypatch.setattr(measure_service, "_coverage",
                        lambda db, m: ({1: 1.0, 2: 1.0}, 20000.0))
    monkeypatch.setattr(
        measure_service, "get_risk_aggregate",
        lambda db, kid, apply_measures=False, demo_session_id=None: {"risks": {}})
    zellen = [SimpleNamespace(
        grid_cell_id=cid, kommune_id=1,
        data={"risks": {KLASSE_B_CODE: {"index": 40.0, "outcome": 2.0, "cost_eur": 2000.0}},
              "inputs": {"pop": 250.0}}) for cid in (1, 2)]
    basis = next(m for m in catalog.MEASURES if float(m.get("default_reduction") or 0) > 0)
    mdef = {**basis, "linked_risk_codes": [KLASSE_B_CODE], "custom_sources": {},
            "benefit_per_m2_year": direkt}
    measure = SimpleNamespace(id=7, kommune_id=1, measure_type="TEST", config={},
                              impact_summary=None)
    db = _Session(zellen, SimpleNamespace(population=500, area_km2=2.0))
    return measure_service._compute_impact_scoped(db, measure, mdef, "fp")


def test_direkter_nutzen_groesser_null_betrag_gilt_mit_zusatz(monkeypatch, klasse_b):
    s = _rechne(monkeypatch, 2.0)
    assert s["annual_benefit_direct_eur"] > 0.0
    assert s["annual_benefit_damage_eur"] == 0.0
    assert s["benefit_display"] is None
    assert s["benefit_note"] == "ohne 1 Wirkung im Screening"
    assert s["benefit_has_euro_layer"] is False
    assert s["benefit_screening_risk_codes"] == [KLASSE_B_CODE]


def test_direkter_nutzen_null_vermerktext(monkeypatch, klasse_b):
    s = _rechne(monkeypatch, 0.0)
    assert s["annual_benefit_direct_eur"] == 0.0
    assert s["benefit_display"] == catalog.NO_EURO_LAYER_TEXT
    assert s["benefit_note"] is None
    assert s["benefit_has_euro_layer"] is False
