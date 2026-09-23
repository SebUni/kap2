"""by_risk: Klasse B trägt cost_eur None, Rangfolge A nach Betrag, B nach Name.

Verwechslungssperre 2/1: Der Betrag einer Klasse-B-Wirkung verschwindet an der
Quelle; eine Rangfolge nach dem unterdrückten Betrag würde ihn verraten.
"""

from __future__ import annotations

import pytest

from app.data import catalog
from app.services.engine import risk_engine

A_CODES = ["TEST_A_KLEIN", "TEST_A_GROSS"]
B_CODES = ["TEST_B_ZULU", "TEST_B_ALPHA"]


def _risk(code: str, name: str, euro_layer: bool, kosten: float) -> dict:
    return {
        "code": code, "name": name, "group": "health",
        "outcome_unit": "Fälle/Jahr", "ref_value": 10.0, "scale": "pop",
        "cost_per_outcome_eur": kosten, "cost_dimension": "health",
        "cost_source": "Testquelle", "euro_layer": euro_layer,
    }


def _eintraege() -> tuple[list[dict], list[dict]]:
    a = [_risk("TEST_A_KLEIN", "Wirkung A klein", True, 1000.0),
         _risk("TEST_A_GROSS", "Wirkung A gross", True, 5000.0)]
    # Betragsreihenfolge der Klasse B widerspricht der Namensreihenfolge
    # (Zulu teurer als Alpha).
    b = [_risk("TEST_B_ZULU", "Wirkung B Zulu", False, 9000.0),
         _risk("TEST_B_ALPHA", "Wirkung B Alpha", False, 100.0)]
    return a, b


def _cells(risks: list[dict]) -> list[dict]:
    werte = {r["code"]: {"index": 40.0, "outcome": 1.0,
                         "cost_eur": r["cost_per_outcome_eur"]}
             for r in risks}
    return [{"risks": dict(werte), "inputs": {"pop": 250.0}},
            {"risks": dict(werte), "inputs": {"pop": 250.0}}]


def _aggregate(risks: list[dict]) -> dict:
    return risk_engine.aggregate(_cells(risks), total_pop=500.0, area_km2=2.0)


@pytest.fixture
def lauf(monkeypatch):
    """(Aggregat mit A und B, Aggregat nur mit A) über denselben Katalog."""
    basis = list(catalog.RISKS)
    a, b = _eintraege()
    for r in a:
        monkeypatch.setitem(catalog.RISKS_BY_CODE, r["code"], r)
    monkeypatch.setattr(catalog, "RISKS", basis + a)
    ohne_b = _aggregate(basis + a)
    for r in b:
        monkeypatch.setitem(catalog.RISKS_BY_CODE, r["code"], r)
    monkeypatch.setattr(catalog, "RISKS", basis + a + b)
    return _aggregate(basis + a + b), ohne_b


def test_klasse_b_ohne_betrag_mit_anzeigetext(lauf):
    mit, _ = lauf
    eintraege = [e for e in mit["cost"]["by_risk"] if e["code"] in B_CODES]
    assert len(eintraege) == 2
    for e in eintraege:
        assert e["cost_eur"] is None
        assert e["cost_display"] == catalog.NO_EURO_LAYER_TEXT


def test_klasse_a_steht_vor_klasse_b(lauf):
    mit, _ = lauf
    flags = [e["has_euro_layer"] for e in mit["cost"]["by_risk"]]
    assert flags == sorted(flags, reverse=True)
    assert True in flags and False in flags


def test_reihenfolge_a_nach_betrag_b_nach_name(lauf):
    mit, _ = lauf
    by_risk = mit["cost"]["by_risk"]
    a = [e for e in by_risk if e["code"] in A_CODES]
    assert [e["code"] for e in a] == ["TEST_A_GROSS", "TEST_A_KLEIN"]
    assert a[0]["cost_eur"] > a[1]["cost_eur"]
    b = [e for e in by_risk if e["code"] in B_CODES]
    assert [e["code"] for e in b] == ["TEST_B_ALPHA", "TEST_B_ZULU"]


def test_summe_gleich_aggregat_ohne_klasse_b(lauf):
    mit, ohne = lauf
    assert mit["cost"]["total_eur"] == ohne["cost"]["total_eur"]
