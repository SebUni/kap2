"""Excel-Export: Blatt „Maßnahmen“ zeigt für Screening-Maßnahmen den Vermerk statt 0 € (T-0853).

Verwechslungssperre Klasse A/B (T-0838/T-0563): Eine Maßnahme, deren Wirkungen alle ohne
Euro-Schicht sind, trägt in „Nutzen/Jahr (€)“ den Vermerk ``catalog.NO_EURO_LAYER_TEXT``,
keine 0. Eine gemischte Maßnahme behält ihren Betrag; ihr Zusatz steht in derselben Zeile.
Ohne Datenbank: Session-Doppel; die Vermerkfelder kommen aus
``measure_service._benefit_euro_layer_fields`` (wie in ``ensure_fresh_impact_summary``).
"""

from __future__ import annotations

import io

import pytest

openpyxl = pytest.importorskip("openpyxl")
if not hasattr(openpyxl, "__version__"):  # Ersatzmodul statt echtem openpyxl
    pytest.skip("echtes openpyxl nötig, um die xlsx-Bytes zurückzulesen",
                allow_module_level=True)

from app.data import catalog  # noqa: E402
from app.models.models import (  # noqa: E402
    AdaptationMeasure, ConfigParameter, Kommune, MeasureImpact,
)
from app.services import export_service, measure_service  # noqa: E402

KLASSE_A_CODE = "EXPECTED_ANNUAL_MORTALITY"
KLASSE_B_CODE = "TEST_KLASSE_B_MASSNAHMEN"
VERMERK = "Screening ohne Euro-Bezifferung"
KOMMUNE_ID = 1

# Maßnahme-ID -> verknüpfte Wirkungen
VERKNUEPFT = {
    1: [KLASSE_B_CODE],                 # rein Screening
    2: [KLASSE_A_CODE],                 # nur Klasse A
    3: [KLASSE_A_CODE, KLASSE_B_CODE],  # gemischt
}


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
    def __init__(self, rows: dict):
        self._rows = rows

    def query(self, model, *a, **k):
        return _FakeQuery(self._rows.get(model, []))


def _klasse_b_eintrag() -> dict:
    return {
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


@pytest.fixture
def klasse_b(monkeypatch):
    risk = _klasse_b_eintrag()
    monkeypatch.setattr(catalog, "RISKS", list(catalog.RISKS) + [risk])
    monkeypatch.setitem(catalog.RISKS_BY_CODE, KLASSE_B_CODE, risk)
    return risk


@pytest.fixture
def zeilen(klasse_b, monkeypatch):
    massnahmen = [
        AdaptationMeasure(
            id=i, kommune_id=KOMMUNE_ID, name=f"Testmaßnahme {i}",
            measure_type="tree_planting", geometry=None, config={},
            implementation_year=2027, description="", impact_summary={})
        for i in VERKNUEPFT
    ]
    kommune = Kommune(id=KOMMUNE_ID, name="Testheim", osm_id="R1", population=5000,
                      area_km2=10.0)
    db = _FakeDB({AdaptationMeasure: massnahmen, MeasureImpact: [],
                  ConfigParameter: [], Kommune: [kommune]})
    cov = catalog.euro_coverage(catalog.RISKS)
    agg = {"cost": {"total_eur": 0.0, "by_risk": [],
                    "euro_coverage": {"covered": cov.covered, "total": cov.total,
                                      "text": cov.text}},
           "groups": {}}
    monkeypatch.setattr(measure_service, "get_risk_aggregate", lambda *a, **k: agg)

    def _summary(_db, m):
        rein = VERKNUEPFT[m.id] == [KLASSE_B_CODE]
        s = {"capex_eur": 1000.0, "opex_annual_eur": 50.0, "count": 12,
             "annual_benefit_eur": 0.0 if rein else 4200.0}
        s.update(measure_service._benefit_euro_layer_fields(VERKNUEPFT[m.id]))
        return s

    monkeypatch.setattr(measure_service, "ensure_fresh_impact_summary", _summary)
    data = export_service.export_measures_xlsx(db, KOMMUNE_ID)
    ws = openpyxl.load_workbook(io.BytesIO(data))["Maßnahmen"]
    kopf = {c.value: i for i, c in enumerate(ws[1])}
    return kopf, {r[0]: list(r) for r in ws.iter_rows(min_row=2, values_only=True)}


def test_reine_screening_massnahme_zeigt_vermerk_statt_null(zeilen):
    kopf, z = zeilen
    wert = z[1][kopf["Nutzen/Jahr (€)"]]
    assert wert == VERMERK
    assert wert not in (0, 0.0, "-", None)


def test_massnahme_mit_klasse_a_traegt_zahl(zeilen):
    kopf, z = zeilen
    wert = z[2][kopf["Nutzen/Jahr (€)"]]
    assert isinstance(wert, (int, float)) and abs(wert - 4200.0) < 1e-6


def test_gemischte_massnahme_behaelt_betrag_und_zusatz_in_derselben_zeile(zeilen):
    kopf, z = zeilen
    zeile = z[3]
    wert = zeile[kopf["Nutzen/Jahr (€)"]]
    assert isinstance(wert, (int, float)) and abs(wert - 4200.0) < 1e-6
    assert "ohne 1 Wirkung im Screening" in zeile[
        kopf["Hinweis zur Nutzen-Summe (Untergrenze)"]]
