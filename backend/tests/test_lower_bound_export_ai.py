"""Untergrenzen-Hinweis dort, wo eine Euro-Summe das Haus verlässt (T-0481).

T-0440 hat den Hinweis in Dashboard und API eingebaut. Dieselbe Summe verlässt
das Haus an zwei weiteren Stellen: im Excel-Export (liegt dem Gutachter auf dem
Tisch) und im Kontext des KI-Assistenten (formuliert Sätze für den Nutzer).

Geprüft wird je Stelle ein Fall **mit** und ein Fall **ohne** unbelegte
Wirkungskategorie:
  (a) mit  → der wörtliche Qualifizierungstext aus ``lower_bound.lower_bound``
      steht in der Ausgabe, samt Anzahl der unbelegten Kategorien;
  (b) ohne → er erscheint nirgends.

Ohne Datenbank: Die Session wird durch ein Doppel ersetzt, das Aggregat über
``measure_service.get_risk_aggregate`` gesetzt.

Läuft mit pytest oder direkt: ``python tests/test_lower_bound_export_ai.py``.
"""

from __future__ import annotations

import pytest

import _stub_heavy_deps

# Muss vor dem Import der App-Module laufen (nur wirksam, wo die echten Pakete
# fehlen — im Deploy-Venv passiert nichts).
_stub_heavy_deps.install()

from app.data import catalog  # noqa: E402
from app.models.models import (  # noqa: E402
    AdaptationMeasure, ConfigParameter, Kommune, MeasureImpact,
)
from app.services import ai_context_service, export_service, measure_service  # noqa: E402
from app.services.engine import lower_bound  # noqa: E402

BELEGT = "EXPECTED_ANNUAL_MORTALITY"     # Kostensatz mit Quelle (VOLY, UBA MK 4.0)
UNBELEGT_CODE = "TEST_UNSOURCED_RISK_EXPORT"
KOMMUNE_ID = 1


# ── Doppel für die Datenbank-Session ──────────────────────────────────────────

class _FakeQuery:
    def __init__(self, rows):
        self._rows = list(rows)

    def filter(self, *a, **k):
        return self

    def limit(self, *a, **k):
        return self

    def all(self):
        return list(self._rows)

    def first(self):
        return self._rows[0] if self._rows else None


class _FakeDB:
    """Minimale Session: liefert je Modellklasse eine feste Zeilenliste."""

    def __init__(self, rows: dict):
        self._rows = rows

    def query(self, model, *a, **k):
        return _FakeQuery(self._rows.get(model, []))


@pytest.fixture
def unsourced_risk():
    """Wirkungskategorie mit unbelegtem Kostensatz (Sicherheitsnetz-Quelle)."""
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


def _aggregate(codes: list[str]) -> dict:
    """Risiko-Aggregat wie ``risk_engine.aggregate`` es ausgibt (nur Kostenblock)."""
    cost = {
        "total_eur": 1_234_567.0,
        "by_risk": [{"code": c, "name": c, "cost_eur": 1000.0,
                     "index": 40.0, "risk_class": "mittel"} for c in codes],
    }
    lb = lower_bound.lower_bound(codes)
    if lb is not None:
        cost["lower_bound"] = lb
    return {"cost": cost, "groups": {}}


def _erwarteter_text(codes: list[str]) -> str:
    lb = lower_bound.lower_bound(codes)
    assert lb is not None, "Testvoraussetzung: Fall mit unbelegter Kategorie"
    return lb["note"]


@pytest.fixture
def db():
    measure = AdaptationMeasure(
        id=1, kommune_id=KOMMUNE_ID, name="Testmaßnahme", measure_type="tree_planting",
        geometry=None, config={}, implementation_year=2027, description="",
        impact_summary={"capex_eur": 1000.0},
    )
    kommune = Kommune(id=KOMMUNE_ID, name="Testheim", osm_id="R1", population=5000,
                      area_km2=10.0)
    return _FakeDB({
        AdaptationMeasure: [measure],
        MeasureImpact: [],
        ConfigParameter: [],
        Kommune: [kommune],
    })


@pytest.fixture(autouse=True)
def _stub_measure_service(monkeypatch):
    monkeypatch.setattr(
        measure_service, "ensure_fresh_impact_summary",
        lambda db, m: {"capex_eur": 1000.0, "opex_annual_eur": 50.0,
                       "annual_benefit_eur": 4200.0, "count": 12},
    )


def _export_text(db, monkeypatch) -> str:
    """Der gesamte sichtbare Zelleninhalt des Maßnahmen-Exports.

    Die Mappe wird im Speicher mitgeschnitten, statt die erzeugten xlsx-Bytes
    wieder zu parsen — geprüft wird, was in die Zellen geschrieben wird.
    """
    erzeugt: list = []

    class _Recorder(_stub_heavy_deps._Workbook):
        def __init__(self):
            super().__init__()
            erzeugt.append(self)

    monkeypatch.setattr(export_service, "Workbook", _Recorder)
    export_service.export_measures_xlsx(db, KOMMUNE_ID)
    wb = erzeugt[0]
    return "\n".join(
        str(value or "")
        for ws in wb.worksheets for row in ws.rows for value in row
    )


# ── (1) Export ────────────────────────────────────────────────────────────────

def test_export_mit_unbelegter_kategorie_traegt_den_hinweis(db, monkeypatch,
                                                            unsourced_risk):
    codes = [BELEGT, UNBELEGT_CODE]
    monkeypatch.setattr(measure_service, "get_risk_aggregate",
                        lambda *a, **k: _aggregate(codes))
    text = _export_text(db, monkeypatch)
    assert _erwarteter_text(codes) in text
    assert "1 von 2 einfließenden Wirkungskategorien" in text


def test_export_ohne_unbelegte_kategorie_ohne_hinweis(db, monkeypatch):
    monkeypatch.setattr(measure_service, "get_risk_aggregate",
                        lambda *a, **k: _aggregate([BELEGT]))
    text = _export_text(db, monkeypatch)
    assert "konservative Untergrenze" not in text
    assert "ohne Beleg" not in text


# ── (2) Kontext des KI-Assistenten ────────────────────────────────────────────

def test_ai_kontext_mit_unbelegter_kategorie_traegt_den_hinweis(db, monkeypatch,
                                                                unsourced_risk):
    codes = [BELEGT, UNBELEGT_CODE]
    monkeypatch.setattr(measure_service, "get_risk_aggregate",
                        lambda *a, **k: _aggregate(codes))
    ctx = ai_context_service.build_context(db, KOMMUNE_ID)
    assert "ERWARTETER SCHADEN GESAMT" in ctx
    assert _erwarteter_text(codes) in ctx
    assert "1 von 2 einfließenden Wirkungskategorien" in ctx


def test_ai_kontext_ohne_unbelegte_kategorie_ohne_hinweis(db, monkeypatch):
    monkeypatch.setattr(measure_service, "get_risk_aggregate",
                        lambda *a, **k: _aggregate([BELEGT]))
    ctx = ai_context_service.build_context(db, KOMMUNE_ID)
    assert "ERWARTETER SCHADEN GESAMT" in ctx
    assert "konservative Untergrenze" not in ctx


# ── (3) Nutzergesetzter Kostensatz bleibt unbelegt und wird benannt ───────────

def test_override_wird_im_hinweis_benannt(unsourced_risk):
    lb = lower_bound.lower_bound([BELEGT, UNBELEGT_CODE])
    text = lower_bound.qualifier_text(lb, {UNBELEGT_CODE})
    assert text.startswith(lb["note"])          # wörtlich identischer Satzanfang
    assert "vom Nutzer gesetzt" in text


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-q"]))
