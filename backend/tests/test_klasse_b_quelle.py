"""Verwechslungssperre Klasse A/B an der Quelle (T-0842): ``risks[code].cost_eur``.

Eine Klasse-B-Wirkung (``"euro_layer": False``) trägt in ``risks[code]`` keinen
Euro-Betrag (None); ``outcome`` bleibt erhalten. Klasse A ist unverändert.
"""

from __future__ import annotations

from app.data import catalog

from test_klasse_b_summen import KLASSE_B_CODE, _aggregate, _klasse_b_eintrag


def test_risks_cost_eur_klasse_b_none(monkeypatch):
    basis = list(catalog.RISKS)
    ohne = _aggregate(basis)
    eintrag = _klasse_b_eintrag()
    monkeypatch.setitem(catalog.RISKS_BY_CODE, KLASSE_B_CODE, eintrag)
    monkeypatch.setattr(catalog, "RISKS", basis + [eintrag])
    mit = _aggregate(basis + [eintrag])
    b = mit["risks"][KLASSE_B_CODE]
    assert b["cost_eur"] is None
    assert b["outcome"] > 0
    for r in basis:
        c = r["code"]
        assert mit["risks"][c]["cost_eur"] == ohne["risks"][c]["cost_eur"]
    assert mit["cost"]["total_eur"] == ohne["cost"]["total_eur"]
