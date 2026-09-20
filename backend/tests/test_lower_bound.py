"""Untergrenzen-Kennzeichnung von Euro-Summen (UBA MK 4.0, Anforderung 25).

Deckt ab:
  (a) ``lower_bound.lower_bound`` ist None, solange jede einfließende
      Wirkungskategorie einen belegten Kostensatz trägt.
  (b) Bei mindestens einer Kategorie mit unbelegtem Kostensatz ist das Feld
      gesetzt, trägt die Zahl der unbelegten Kategorien und begründet die Summe
      wörtlich als „konservative Untergrenze".
  (c) ``risk_engine.aggregate`` hängt den Block an die ausgewiesene Euro-Summe
      (``cost.lower_bound``) — und nur dann, wenn es etwas zu melden gibt.

Läuft mit pytest oder direkt: ``python tests/test_lower_bound.py``.
"""

from __future__ import annotations

import pytest

from app.data import catalog
from app.services.engine import lower_bound, risk_engine

BELEGT = "EXPECTED_ANNUAL_MORTALITY"     # Kostensatz mit Quelle (VOLY, UBA MK 4.0)
UNBELEGT_CODE = "TEST_UNSOURCED_RISK"


@pytest.fixture
def unsourced_risk():
    """Registriert eine Wirkungskategorie mit unbelegtem Kostensatz (Sicherheitsnetz)."""
    risk = {
        "code": UNBELEGT_CODE,
        "name": "Testrisiko ohne belegten Kostensatz",
        "group": "health",
        "outcome_unit": "Fälle/Jahr",
        "ref_value": 10.0,
        "scale": "pop",
        "cost_per_outcome_eur": 0.0,
        "cost_dimension": "health",
        "cost_source": lower_bound.UNSOURCED_COST_SOURCE,
    }
    catalog.RISKS_BY_CODE[UNBELEGT_CODE] = risk
    try:
        yield risk
    finally:
        catalog.RISKS_BY_CODE.pop(UNBELEGT_CODE, None)


def test_alle_kostensaetze_belegt_kein_feld():
    """Ohne unbelegte Kategorie gibt es keinen Untergrenzen-Block."""
    belegte = [r["code"] for r in catalog.RISKS
               if not lower_bound.cost_rate_is_unsourced(r)]
    assert belegte, "Testvoraussetzung: mindestens ein belegtes Risiko im Katalog"
    assert lower_bound.lower_bound(belegte) is None


def test_unbelegte_kategorie_setzt_feld_mit_zaehlwert(unsourced_risk):
    lb = lower_bound.lower_bound([BELEGT, UNBELEGT_CODE])
    assert lb is not None
    assert lb["unsourced_categories"] == 1
    assert lb["total_categories"] == 2
    assert [c["code"] for c in lb["categories"]] == [UNBELEGT_CODE]
    assert "konservative Untergrenze" in lb["note"]


def test_mehrere_unbelegte_kategorien_werden_gezaehlt(unsourced_risk):
    zweites = dict(unsourced_risk, code=UNBELEGT_CODE + "_2",
                   name="Zweites Testrisiko ohne Kostensatz")
    catalog.RISKS_BY_CODE[zweites["code"]] = zweites
    try:
        lb = lower_bound.lower_bound([BELEGT, UNBELEGT_CODE, zweites["code"]])
        assert lb["unsourced_categories"] == 2
        assert "konservative Untergrenze" in lb["note"]
    finally:
        catalog.RISKS_BY_CODE.pop(zweites["code"], None)


def _cells() -> list[dict]:
    """Zwei Zellen mit je einem Wert für alle Katalogrisiken."""
    risks = {r["code"]: {"index": 40.0, "outcome": 1.0, "cost_eur": 100.0}
             for r in catalog.RISKS}
    cell = {"risks": risks, "inputs": {"pop": 250.0}}
    return [dict(cell), dict(cell)]


def test_aggregate_ohne_unbelegte_kategorie_ohne_feld():
    agg = risk_engine.aggregate(_cells(), total_pop=500.0, area_km2=2.0)
    assert agg["cost"]["total_eur"] >= 0.0
    assert "lower_bound" not in agg["cost"]


def test_aggregate_mit_unbelegter_kategorie_setzt_feld(unsourced_risk, monkeypatch):
    monkeypatch.setattr(catalog, "RISKS", catalog.RISKS + [unsourced_risk])
    agg = risk_engine.aggregate(_cells(), total_pop=500.0, area_km2=2.0)
    lb = agg["cost"]["lower_bound"]
    assert lb["unsourced_categories"] == 1
    assert "konservative Untergrenze" in lb["note"]


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-q"]))
