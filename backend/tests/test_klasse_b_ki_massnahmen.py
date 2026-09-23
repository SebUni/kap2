"""Klasse B in den Maßnahmenzeilen des KI-Kontexts: Vermerk statt 0 € (T-0841)."""

from __future__ import annotations

import _stub_heavy_deps  # noqa: F401

from app.data import catalog  # noqa: E402
from app.services import ai_context_service  # noqa: E402


class _M:
    def __init__(self, name, summary):
        self.name = name
        self.measure_type = "test"
        self.impact_summary = summary


class _Q:
    def __init__(self, items):
        self._i = items

    def filter(self, *a, **k):
        return self

    def limit(self, *a):
        return self

    def all(self):
        return self._i


class _DB:
    def __init__(self, items):
        self._i = items

    def query(self, *a):
        return _Q(self._i)


def _lines(summary):
    return ai_context_service._measure_lines(_DB([_M("M1", summary)]), 1)


def test_reine_klasse_b_massnahme_zeigt_vermerk_nicht_null():
    z = _lines({"capex_eur": 1000.0, "annual_benefit_eur": 0.0,
                "benefit_has_euro_layer": False,
                "benefit_display": catalog.NO_EURO_LAYER_TEXT})[1]
    assert f"Nutzen {catalog.NO_EURO_LAYER_TEXT}" in z
    assert "Nutzen 0" not in z
    assert "CAPEX" in z


def test_gemischte_massnahme_zeigt_betrag_mit_zusatz():
    z = _lines({"annual_benefit_eur": 500.0, "benefit_has_euro_layer": True,
                "benefit_note": "ohne 1 Wirkung im Screening"})[1]
    assert "€" in z and "ohne 1 Wirkung im Screening" in z


def test_altbestand_ohne_felder_zeigt_betrag():
    z = _lines({"annual_benefit_eur": 500.0})[1]
    assert "Nutzen" in z and "€" in z
