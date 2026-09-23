"""Klasse B im KI-Kontext: Vermerk statt Betrag, nicht weggefiltert (T-0839)."""

from __future__ import annotations

import pytest

import _stub_heavy_deps  # noqa: F401

from app.data import catalog  # noqa: E402
from app.services import ai_context_service  # noqa: E402

KLASSE_A = "Testwirkung A"
KLASSE_B = "Testwirkung B (Screening)"


def _by_risk():
    return [
        {"code": "A", "name": KLASSE_A, "cost_eur": 5432.0, "index": 40.0,
         "risk_class": "mittel", "has_euro_layer": True, "cost_display": 5432.0},
        {"code": "B", "name": KLASSE_B, "cost_eur": None, "index": 55.0,
         "risk_class": "hoch", "has_euro_layer": False,
         "cost_display": catalog.NO_EURO_LAYER_TEXT},
    ]


@pytest.fixture
def lines(monkeypatch):
    agg = {"cost": {"total_eur": 5432.0, "by_risk": _by_risk()}, "groups": {}}
    monkeypatch.setattr(ai_context_service.measure_service, "get_risk_aggregate",
                        lambda *a, **k: agg)
    monkeypatch.setattr(ai_context_service.lower_bound, "qualifier_text",
                        lambda *a, **k: "")
    monkeypatch.setattr(ai_context_service.lower_bound, "overridden_cost_rate_codes",
                        lambda *a, **k: [])
    return ai_context_service._risk_lines(None, 1)


def test_klasse_b_steht_mit_vermerk_im_kontext(lines):
    zeile = next(z for z in lines if KLASSE_B in z)
    assert catalog.NO_EURO_LAYER_TEXT in zeile
    assert "€" not in zeile


def test_klasse_b_nicht_in_top_liste(lines):
    i_top = lines.index("TOP-EINZELRISIKEN (Schaden/Jahr, Index, Klasse):")
    assert KLASSE_A in lines[i_top + 1]
    assert KLASSE_B not in lines[i_top + 1]
    assert not lines[i_top + 2].startswith("- " + KLASSE_A)


def test_klasse_a_bleibt_mit_betrag(lines):
    zeile = next(z for z in lines if KLASSE_A in z)
    assert "€" in zeile
