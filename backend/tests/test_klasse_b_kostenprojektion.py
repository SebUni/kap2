"""Kostenprojektion: Klasse B wird in ``_group_costs`` ausgelassen, nicht als 0 gezählt.

Verwechslungssperre Klasse A/B (T-0825, Teilpaket T-0837). Die Wirkung legt ihren
Katalogeintrag selbst per monkeypatch an (Muster test_klasse_b_summen.py).
"""

from __future__ import annotations

from app.data import catalog
from app.services import cost_projection_service as cps

KLASSE_B_CODE = "TEST_KLASSE_B_SCREENING"


def _eintrag(group: str) -> dict:
    return {"code": KLASSE_B_CODE, "name": "Testwirkung Klasse B", "group": group,
            "euro_layer": False}


def _agg(*by_risk: dict) -> dict:
    return {"cost": {"by_risk": list(by_risk)}}


def _a_code_und_gruppe() -> tuple[str, str]:
    for r in catalog.RISKS:
        if catalog.risk_has_euro_layer(r) and r["code"] not in catalog.NON_ADDITIVE_RISK_CODES:
            return r["code"], r.get("group", "other")
    raise AssertionError("kein Klasse-A-Risiko im Katalog")


def test_klasse_b_wird_ausgelassen_gruppe_bleibt_unveraendert(monkeypatch):
    code, grp = _a_code_und_gruppe()
    monkeypatch.setitem(catalog.RISKS_BY_CODE, KLASSE_B_CODE, _eintrag(grp))
    ohne = cps._group_costs(_agg({"code": code, "cost_eur": 100.0}))
    mit = cps._group_costs(_agg(
        {"code": code, "cost_eur": 100.0},
        {"code": KLASSE_B_CODE, "cost_eur": None, "has_euro_layer": False},
    ))
    assert mit == ohne == {grp: 100.0}


def test_reine_klasse_b_gruppe_erscheint_nicht_als_null(monkeypatch):
    monkeypatch.setitem(catalog.RISKS_BY_CODE, KLASSE_B_CODE, _eintrag("testgruppe_b"))
    for kosten in (None, 500.0):  # None nach der Quellumstellung, 500 als Altbestand
        out = cps._group_costs(_agg({"code": KLASSE_B_CODE, "cost_eur": kosten}))
        assert "testgruppe_b" not in out
        assert out == {}
