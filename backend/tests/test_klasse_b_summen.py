"""Summe zählt nur Wirkungen mit Euro-Schicht; das Aggregat trägt Abdeckung und Anzeigewert.

Verwechslungssperre Klasse A/B (T-0358, Teilpaket T-0514): Ein Klasse-B-Eintrag
(``"euro_layer": False``) mit Zellwerten Index > 0 wird ins Aggregat eingehängt.
Geprüft wird gegen einen Lauf ohne diesen Eintrag:

(1) ``cost['total_eur']`` bleibt bitgleich;
(2) der Eintrag steht trotzdem in ``cost['by_risk']`` mit ``has_euro_layer`` False
    und ``cost_display`` == ``catalog.NO_EURO_LAYER_TEXT``;
(3) ``cost['euro_coverage']['total']`` steigt um genau 1, ``covered`` bleibt;
(4) der Code des Eintrags kommt in ``cost.get('lower_bound')`` nicht vor.
"""

from __future__ import annotations

import pytest

from app.data import catalog
from app.services.engine import lower_bound, risk_engine

KLASSE_B_CODE = "TEST_KLASSE_B_SCREENING"


def _klasse_b_eintrag(**abweichung) -> dict:
    """Klasse-B-Testeintrag mit einem Kostensatz > 0 — ohne die Ausnahme in der
    Summenbildung würde er also einen Betrag in die Summe tragen."""
    risk = {
        "code": KLASSE_B_CODE,
        "name": "Testwirkung Klasse B (Screening)",
        "group": "health",
        "outcome_unit": "Fälle/Jahr",
        "ref_value": 10.0,
        "scale": "pop",
        "cost_per_outcome_eur": 1000.0,
        "cost_dimension": "health",
        "cost_source": "Testquelle",
        "euro_layer": False,
    }
    risk.update(abweichung)
    return risk


def _cells(risks: list[dict]) -> list[dict]:
    """Zwei bewohnte Zellen mit Index > 0 für jede übergebene Wirkung."""
    werte = {r["code"]: {"index": 40.0, "outcome": 1.0, "cost_eur": 100.0}
             for r in risks}
    return [{"risks": dict(werte), "inputs": {"pop": 250.0}},
            {"risks": dict(werte), "inputs": {"pop": 250.0}}]


def _aggregate(risks: list[dict]) -> dict:
    return risk_engine.aggregate(_cells(risks), total_pop=500.0, area_km2=2.0)


@pytest.fixture(params=["belegter_kostensatz", "unbelegter_kostensatz"])
def mit_und_ohne(request, monkeypatch):
    """Liefert (Aggregat ohne, Aggregat mit Klasse-B-Eintrag).

    Zwei Varianten: mit belegtem Kostensatz > 0 (würde die Summe erhöhen) und mit
    unbelegtem Kostensatz 0 € (würde ohne Ausnahme im Untergrenzen-Block stehen).
    """
    basis = list(catalog.RISKS)
    ohne = _aggregate(basis)

    if request.param == "belegter_kostensatz":
        eintrag = _klasse_b_eintrag()
    else:
        eintrag = _klasse_b_eintrag(cost_per_outcome_eur=0.0,
                                    cost_source=lower_bound.UNSOURCED_COST_SOURCE)
    monkeypatch.setitem(catalog.RISKS_BY_CODE, KLASSE_B_CODE, eintrag)
    monkeypatch.setattr(catalog, "RISKS", basis + [eintrag])
    mit = _aggregate(basis + [eintrag])
    return ohne, mit


def test_summe_bitgleich_ohne_klasse_b(mit_und_ohne):
    ohne, mit = mit_und_ohne
    assert mit["cost"]["total_eur"] == ohne["cost"]["total_eur"]
    assert repr(mit["cost"]["total_eur"]) == repr(ohne["cost"]["total_eur"])


def test_klasse_b_steht_in_by_risk_mit_anzeigewert(mit_und_ohne):
    _, mit = mit_und_ohne
    eintraege = [r for r in mit["cost"]["by_risk"] if r["code"] == KLASSE_B_CODE]
    assert len(eintraege) == 1
    eintrag = eintraege[0]
    assert eintrag["has_euro_layer"] is False
    assert eintrag["cost_display"] == catalog.NO_EURO_LAYER_TEXT
    # Der Eintrag hatte tatsächlich Zellwerte mit Index > 0.
    assert eintrag["index"] > 0


def test_euro_coverage_total_plus_eins_covered_gleich(mit_und_ohne):
    ohne, mit = mit_und_ohne
    assert mit["cost"]["euro_coverage"]["total"] == ohne["cost"]["euro_coverage"]["total"] + 1
    assert mit["cost"]["euro_coverage"]["covered"] == ohne["cost"]["euro_coverage"]["covered"]


def test_klasse_b_nicht_im_untergrenzen_block(mit_und_ohne):
    _, mit = mit_und_ohne
    lb = mit["cost"].get("lower_bound")
    assert KLASSE_B_CODE not in repr(lb)
