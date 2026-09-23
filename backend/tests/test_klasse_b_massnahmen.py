"""Maßnahmen-Nutzen und Deckel ohne Klasse-B-Betrag, Vermerk statt 0 (T-0838).

Verwechslungssperre Klasse A/B, Teilpaket 2 der Planung T-0825: ``measure_service``
rechnete für eine Klasse-B-Wirkung (``"euro_layer": False``) mit Kostensatz > 0 einen
Euro-Nutzen und einen Deckel aus genau dem Betrag, den die Sperre unterdrücken soll,
weil ``catalog.risk_contributes_to_total`` die Euro-Schicht nicht prüft.

Geprüft wird DB-frei am echten ``_compute_impact_scoped`` (Session als Stub, Deckung
und Basis-Aggregat per monkeypatch), mit selbst angelegten Testwirkungen nach dem
Muster ``_klasse_b_eintrag`` aus ``test_klasse_b_summen.py`` — der echte Katalog
führt heute keine Klasse-B-Wirkung:

(1) Zell-Nutzen: eine reine Klasse-B-Maßnahme hat ``annual_benefit_damage_eur`` 0,
    ``benefit_has_euro_layer`` False und ``benefit_display`` ==
    ``catalog.NO_EURO_LAYER_TEXT`` (Vermerk statt 0);
(2) flat-Nutzen: eine flat-skalierte Klasse-B-Wirkung liefert keinen flat-Nutzen;
(3) Deckel: ein Klasse-B-Betrag im Basis-Aggregat hebt den Deckel nicht an;
(4) gemischte Maßnahme: Nutzen nur aus Klasse A, Zusatz „ohne 1 Wirkung im Screening“;
(5) reine Klasse-A-Maßnahme: keine Vermerkfelder gesetzt, Nutzen unverändert > 0.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.data import catalog
from app.models.models import CellAssessment, Kommune, MeasureImpact
from app.services import measure_service

KLASSE_A_CODE = "TEST_KLASSE_A_WIRKUNG"
KLASSE_B_CODE = "TEST_KLASSE_B_SCREENING"
KLASSE_B_FLAT_CODE = "TEST_KLASSE_B_FLAT"


def _eintrag(code: str, **abweichung) -> dict:
    """Nicht-monetäre pop-Testwirkung mit belegtem Kostensatz > 0 — sie trägt also
    zur Gesamtsumme bei (``risk_contributes_to_total`` True)."""
    risk = {
        "code": code,
        "name": f"Testwirkung {code}",
        "group": "health",
        "outcome_unit": "Fälle/Jahr",
        "ref_value": 10.0,
        "scale": "pop",
        "cost_per_outcome_eur": 1000.0,
        "cost_dimension": "health",
        "cost_source": "Testquelle",
    }
    risk.update(abweichung)
    return risk


@pytest.fixture
def testwirkungen(monkeypatch):
    eintraege = [
        _eintrag(KLASSE_A_CODE),
        _eintrag(KLASSE_B_CODE, euro_layer=False),
        _eintrag(KLASSE_B_FLAT_CODE, euro_layer=False, scale="flat"),
    ]
    for e in eintraege:
        monkeypatch.setitem(catalog.RISKS_BY_CODE, e["code"], e)
    monkeypatch.setattr(catalog, "RISKS", list(catalog.RISKS) + eintraege)
    for e in eintraege:
        assert catalog.risk_contributes_to_total(e)  # ohne Sperre gäbe es einen Betrag
    return {e["code"]: e for e in eintraege}


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
    """Stub-Session: liefert Zellen/Kommune aus Listen, schreibt nichts."""

    def __init__(self, cells, kommune):
        self._rows = {CellAssessment: cells, Kommune: [kommune], MeasureImpact: []}

    def query(self, model):
        return _Query(self._rows.get(model, []))

    def add(self, obj):
        pass

    def commit(self):
        pass


def _zellen(codes: list[str]) -> list:
    werte = {c: {"index": 40.0, "outcome": 2.0, "cost_eur": 2000.0} for c in codes}
    return [SimpleNamespace(grid_cell_id=cid, kommune_id=1,
                            data={"risks": {c: dict(v) for c, v in werte.items()},
                                  "inputs": {"pop": 250.0}})
            for cid in (1, 2)]


def _mdef(linked: list[str]) -> dict:
    basis = next(m for m in catalog.MEASURES if float(m.get("default_reduction") or 0) > 0)
    return {**basis, "linked_risk_codes": linked, "custom_sources": {},
            "benefit_per_m2_year": 0.0}


def _rechne(monkeypatch, linked: list[str], basis_kosten: dict[str, float]) -> dict:
    monkeypatch.setattr(measure_service, "_coverage",
                        lambda db, m: ({1: 1.0, 2: 1.0}, 20000.0))
    monkeypatch.setattr(
        measure_service, "get_risk_aggregate",
        lambda db, kid, apply_measures=False, demo_session_id=None: {
            "risks": {c: {"cost_eur": v} for c, v in basis_kosten.items()}})
    measure = SimpleNamespace(id=7, kommune_id=1, measure_type="TEST", config={},
                              impact_summary=None)
    db = _Session(_zellen(linked), SimpleNamespace(population=500, area_km2=2.0))
    return measure_service._compute_impact_scoped(db, measure, _mdef(linked), "fp")


def test_reine_klasse_b_massnahme_vermerk_statt_null(monkeypatch, testwirkungen):
    s = _rechne(monkeypatch, [KLASSE_B_CODE], {KLASSE_B_CODE: 1_000_000.0})
    assert s["annual_benefit_damage_eur"] == 0.0
    assert s["benefit_capped"] is False
    assert s["benefit_has_euro_layer"] is False
    assert s["benefit_display"] == catalog.NO_EURO_LAYER_TEXT
    assert s["benefit_note"] is None
    assert s["benefit_screening_risk_codes"] == [KLASSE_B_CODE]


def test_flat_klasse_b_ohne_flat_nutzen(monkeypatch, testwirkungen):
    s = _rechne(monkeypatch, [KLASSE_B_FLAT_CODE], {})
    assert s["annual_benefit_flat_eur"] == 0.0
    assert s["benefit_has_euro_layer"] is False
    assert s["benefit_display"] == catalog.NO_EURO_LAYER_TEXT


def test_deckel_ohne_klasse_b_betrag(monkeypatch, testwirkungen):
    # Klasse A hat im Basis-Aggregat nur 1 €, Klasse B eine Million: der Deckel darf
    # nur aus Klasse A kommen, der Nutzen wird also auf 1 € gekappt.
    s = _rechne(monkeypatch, [KLASSE_A_CODE, KLASSE_B_CODE],
                {KLASSE_A_CODE: 1.0, KLASSE_B_CODE: 1_000_000.0})
    assert s["benefit_capped"] is True
    assert s["annual_benefit_damage_eur"] == 1.0
    assert measure_service._benefit_cap(
        [KLASSE_A_CODE, KLASSE_B_CODE],
        {KLASSE_A_CODE: {"cost_eur": 1.0}, KLASSE_B_CODE: {"cost_eur": 1_000_000.0}},
        0.25) == 1.0


def test_gemischte_massnahme_nur_klasse_a_mit_zusatz(monkeypatch, testwirkungen):
    gross = {KLASSE_A_CODE: 1e9, KLASSE_B_CODE: 1e9}
    nur_a = _rechne(monkeypatch, [KLASSE_A_CODE], gross)
    gemischt = _rechne(monkeypatch, [KLASSE_A_CODE, KLASSE_B_CODE], gross)
    assert nur_a["annual_benefit_damage_eur"] > 0.0
    assert gemischt["annual_benefit_damage_eur"] == nur_a["annual_benefit_damage_eur"]
    assert gemischt["annual_benefit_eur"] == nur_a["annual_benefit_eur"]
    assert gemischt["benefit_has_euro_layer"] is True
    assert gemischt["benefit_display"] is None
    assert gemischt["benefit_note"] == "ohne 1 Wirkung im Screening"
    assert gemischt["benefit_screening_risk_codes"] == [KLASSE_B_CODE]


def test_zusatz_zaehlt_mehrere_screening_wirkungen(testwirkungen):
    felder = measure_service._benefit_euro_layer_fields(
        [KLASSE_A_CODE, KLASSE_B_CODE, KLASSE_B_FLAT_CODE])
    assert felder["benefit_note"] == "ohne 2 Wirkungen im Screening"
    assert felder["benefit_has_euro_layer"] is True


def test_reine_klasse_a_massnahme_ohne_vermerk(monkeypatch, testwirkungen):
    s = _rechne(monkeypatch, [KLASSE_A_CODE], {KLASSE_A_CODE: 1e9})
    assert s["annual_benefit_damage_eur"] > 0.0
    assert s["benefit_has_euro_layer"] is True
    assert s["benefit_display"] is None
    assert s["benefit_note"] is None
    assert s["benefit_screening_risk_codes"] == []


def test_echter_katalog_ohne_vermerk():
    """Im echten Katalog trägt keine Wirkung ``euro_layer: False`` — jede Maßnahme
    bleibt Klasse A, die Änderung ist für echte Daten neutral."""
    for m in catalog.MEASURES:
        felder = measure_service._benefit_euro_layer_fields(m.get("linked_risk_codes", []))
        assert felder["benefit_has_euro_layer"] is True
        assert felder["benefit_display"] is None
        assert felder["benefit_note"] is None
