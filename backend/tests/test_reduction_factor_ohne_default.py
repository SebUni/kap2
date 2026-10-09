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
    (``1 − r·Deckung`` bei einem Ziel);
(d) der Weg über ein verknüpftes **kommunenweites** (flat-skaliertes) Risiko — Zweig
    ``flat_linked`` in ``_compute_impact_scoped`` — wirft keinen TypeError, der Faktor
    ist dort 1,0 (flacher Nutzen genau 0); eine Kontrolle mit gesetztem
    ``default_reduction`` zeigt, dass der Zweig wirklich erreicht wird.

DB-frei: reine Rechenfunktionen aus ``measure_service``, der Katalog und eine Stub-Session.
"""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.data import catalog
from app.models.models import CellAssessment, Kommune, MeasureImpact
from app.services import measure_service

_OHNE_DEFAULT = [m for m in catalog.MEASURES if m.get("default_reduction") is None]
_IDS = [m["code"] for m in _OHNE_DEFAULT]
# T-1937-cto: SKIN_CANCER_EARLY_DETECTION (#98 S158) trägt default_reduction None UND kein
# verknüpftes Risiko (nur qualitativ, Vermerk statt Betrag; die Nutzenfelder entstehen
# nicht). Die Tests unten, die ein verknüpftes Risiko oder die Nutzenfelder voraussetzen,
# laufen deshalb nur über Maßnahmen mit Wirkungskanal; ihr Verhalten bindet
# test_massnahme_s158_uv_vermerk.py.
_OHNE_DEFAULT_MIT_RISIKO = [m for m in _OHNE_DEFAULT if m.get("linked_risk_codes")]
_IDS_MIT_RISIKO = [m["code"] for m in _OHNE_DEFAULT_MIT_RISIKO]


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


@pytest.mark.parametrize("mdef", _OHNE_DEFAULT_MIT_RISIKO, ids=_IDS_MIT_RISIKO)
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


# --- (d) Kommunenweites (flat) verknüpftes Risiko über ``_compute_impact_scoped`` ---------
# Zweig ``flat_linked`` (``flat_linked`` in ``_compute_impact_scoped``): dort ruft die große Nutzenrechnung
# ``_reduction_factor(mdef, …)`` direkt mit der Maßnahmendefinition auf. Das Muster (Stub-
# Session, Testrisiko in catalog.RISKS_BY_CODE, _coverage und get_risk_aggregate per
# monkeypatch) stammt aus test_klasse_b_direktnutzen.py — keine Datenbank nötig.

FLAT_CODE = "TEST_FLAT_OHNE_DEFAULT"
_N_ZELLEN = 10


def _flat_eintrag() -> dict:
    return {
        "code": FLAT_CODE, "name": "Testwirkung kommunenweit", "group": "infrastructure",
        "outcome_unit": "Stunden/Jahr", "ref_value": 100.0, "scale": "flat",
        "cost_per_outcome_eur": 1000.0, "cost_dimension": "economic",
        "cost_source": "Testquelle",
    }


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


@pytest.fixture
def flat_risiko(monkeypatch):
    e = _flat_eintrag()
    monkeypatch.setitem(catalog.RISKS_BY_CODE, e["code"], e)
    monkeypatch.setattr(catalog, "RISKS", list(catalog.RISKS) + [e])
    assert catalog.risk_contributes_to_total(e) and catalog.risk_has_euro_layer(e)


def _rechne_flat(monkeypatch, mdef: dict) -> dict:
    """Nutzen der Maßnahme ``mdef``, verknüpft mit dem kommunenweiten Testrisiko."""
    deckung = {cid: 1.0 for cid in range(1, _N_ZELLEN + 1)}
    monkeypatch.setattr(measure_service, "_coverage", lambda db, m: (dict(deckung), 20000.0))
    monkeypatch.setattr(
        measure_service, "get_risk_aggregate",
        lambda db, kid, apply_measures=False, demo_session_id=None: {"risks": {}})
    # Hitzeaktionspläne/Schutzprogramme-Zweige lesen Parameter-Overrides aus der Datenbank.
    monkeypatch.setattr(measure_service.parameter_registry, "load_db_overrides",
                        lambda db, kid: {})
    # Zellen mit gestuftem Index, damit eine echte Minderung das P90 bewegen würde.
    zellen = [SimpleNamespace(
        grid_cell_id=cid, kommune_id=1,
        data={"risks": {FLAT_CODE: {"index": 10.0 * cid, "outcome": 0.0, "cost_eur": 0.0}},
              "inputs": {"pop": 250.0}}) for cid in range(1, _N_ZELLEN + 1)]
    d = {**mdef, "linked_risk_codes": [FLAT_CODE], "custom_sources": {}}
    measure = SimpleNamespace(id=7, kommune_id=1, measure_type=mdef["code"], config={},
                              impact_summary=None, demo_session_id=None)
    db = _Session(zellen, SimpleNamespace(population=100000, area_km2=50.0))
    return measure_service._compute_impact_scoped(db, measure, d, "fp")


@pytest.mark.parametrize("mdef", _OHNE_DEFAULT_MIT_RISIKO, ids=_IDS_MIT_RISIKO)
def test_kommunenweites_risiko_ohne_typeerror_und_faktor_eins(monkeypatch, flat_risiko, mdef):
    # Kein TypeError, und weil der Faktor auf diesem Weg 1,0 ist, bewegt sich das P90
    # nicht: der flache Nutzen ist genau 0 (die Wirkung rechnet der eigene Zweig).
    s = _rechne_flat(monkeypatch, mdef)
    assert s["annual_benefit_flat_eur"] == 0.0, mdef["code"]
    assert s["annual_benefit_damage_eur"] == 0.0, mdef["code"]


def test_kommunenweites_risiko_kontrolle_mit_default_reduction_hat_nutzen(monkeypatch, flat_risiko):
    # Kontrolle: derselbe Aufbau mit gesetztem default_reduction bewegt das P90 — der Test
    # erreicht den flat-Zweig also wirklich und die 0 oben ist kein Leerlauf.
    basis = next(m for m in catalog.MEASURES if float(m.get("default_reduction") or 0) > 0
                 and not m.get("effect_model"))
    s = _rechne_flat(monkeypatch, basis)
    assert s["annual_benefit_flat_eur"] > 0.0
