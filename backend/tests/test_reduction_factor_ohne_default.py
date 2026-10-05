"""``_reduction_factor`` bei Katalogmaßnahmen mit ``default_reduction`` = None (T-1723-cto).

Drei Katalogmaßnahmen tragen den Schlüssel ``default_reduction`` mit dem Wert None
(„nicht anwendbar“): VULNERABLE_GROUP_PROGRAMS (effect_model ``vg``),
LOW_ALLERGEN_TREE_SELECTION (``stadtbaum``) und COOLING_ROOMS_DRINKING_WATER
(``s157``). Ihre Wirkung rechnet je ein eigener Zweig; der Index-Faktor
``_reduction_factor`` darf sie nicht anfassen. Vorher stand dort
``float(mdef.get("default_reduction", 0.0))`` — bei vorhandenem Schlüssel mit None
wirft das einen TypeError, weil der Vorgabewert nur bei fehlendem Schlüssel greift.

Geprüft wird je Katalogmaßnahme mit ``default_reduction`` None:
(a) ``_reduction_factor`` wirft keinen TypeError und liefert genau 1,0 — für jede
    Deckung, mit und ohne Stückfaktor, linearer wie sättigender Skalierung;
(b) der Weg über ein verknüpftes Risiko (``_measure_cell_factor``) wirft ebenfalls
    keinen TypeError: einmal mit dem echten Maßnahmenzweig, einmal ohne
    ``effect_model`` — dann rechnet er über ``_reduction_factor`` und liefert 1,0;
(c) eine Maßnahme mit gesetztem ``default_reduction`` rechnet unverändert
    (``1 − r·Deckung`` bei einem Ziel).

DB-frei: reine Rechenfunktionen aus ``measure_service`` und der Katalog.
"""
from __future__ import annotations

import pytest

from app.data import catalog
from app.services import measure_service

_OHNE_DEFAULT = [m for m in catalog.MEASURES if m.get("default_reduction") is None]
_IDS = [m["code"] for m in _OHNE_DEFAULT]


def test_katalog_traegt_massnahmen_mit_default_reduction_none():
    # Der Schlüssel ist vorhanden (nicht fehlend) und hat den Wert None — genau der Fall,
    # den ``mdef.get("default_reduction", 0.0)`` nicht abfängt.
    assert _OHNE_DEFAULT, "keine Katalogmaßnahme mit default_reduction None"
    for m in _OHNE_DEFAULT:
        assert "default_reduction" in m


@pytest.mark.parametrize("mdef", _OHNE_DEFAULT, ids=_IDS)
@pytest.mark.parametrize("frac", [0.0, 0.3, 1.0])
@pytest.mark.parametrize("unit_factor", [1.0, 0.5])
def test_reduction_factor_none_ist_faktor_eins(mdef, frac, unit_factor):
    assert measure_service._reduction_factor(mdef, frac, unit_factor) == 1.0


@pytest.mark.parametrize("mdef", _OHNE_DEFAULT, ids=_IDS)
def test_reduction_factor_none_gilt_fuer_lineare_und_saettigende_skalierung(mdef):
    for scaling in ("linear", "saturating"):
        d = dict(mdef, coverage_scaling=scaling)
        assert measure_service._reduction_factor(d, 1.0) == 1.0


@pytest.mark.parametrize("mdef", _OHNE_DEFAULT, ids=_IDS)
def test_wirkung_ueber_verknuepftes_risiko_ohne_typeerror(mdef):
    linked = mdef.get("linked_risk_codes") or []
    assert linked, f"{mdef['code']} hat kein verknüpftes Risiko"
    for code in linked:
        # echter Zweig der Maßnahme (vg / s157 / stadtbaum), Zelle ohne Risikodaten
        faktor = measure_service._measure_cell_factor(mdef, None, code, 1.0, 1.0, {})
        assert faktor == 1.0, (mdef["code"], code)
        # ohne effect_model läuft derselbe Aufruf über ``_reduction_factor``
        generisch = {k: v for k, v in mdef.items() if k != "effect_model"}
        faktor = measure_service._measure_cell_factor(generisch, None, code, 1.0, 1.0, {})
        assert faktor == 1.0, (mdef["code"], code)


def test_reduction_factor_mit_default_reduction_rechnet_unveraendert():
    mdef = {"default_reduction": 0.2, "coverage_scaling": "linear", "effect_target": ["hazard"]}
    assert measure_service._reduction_factor(mdef, 0.5) == pytest.approx(1.0 - 0.2 * 0.5)
