"""Excel-Export: Vollständigkeit im Blatt „Zusammenfassung“, Vermerk „nicht in der Gesamtsumme“."""

from __future__ import annotations

import io

import pytest

openpyxl = pytest.importorskip("openpyxl")
if not hasattr(openpyxl, "__version__"):
    pytest.skip("echtes openpyxl nötig", allow_module_level=True)

from app.data import catalog  # noqa: E402
from app.services import export_service, measure_service  # noqa: E402
from tests.test_klasse_b_excel import (  # noqa: E402,F401
    KLASSE_A_CODE, KOMMUNE_ID, _aggregate, db, klasse_b,
)

VERMERK = "nicht in der Gesamtsumme"


@pytest.fixture
def export(db, klasse_b, monkeypatch):
    agg = _aggregate()
    for code in sorted(catalog.NON_ADDITIVE_RISK_CODES):
        r = catalog.RISKS_BY_CODE.get(code, {})
        agg["cost"]["by_risk"].append({
            "code": code, "name": r.get("name", code), "cost_eur": 100.0, "index": 10.0,
            "risk_class": "gering",
            "has_euro_layer": True, "cost_display": 100.0,
        })
    monkeypatch.setattr(measure_service, "get_risk_aggregate", lambda *a, **k: agg)
    monkeypatch.setattr(
        measure_service, "ensure_fresh_impact_summary",
        lambda db, m: {"capex_eur": 1000.0, "opex_annual_eur": 50.0,
                       "annual_benefit_eur": 4200.0, "count": 12},
    )
    data = export_service.export_measures_xlsx(db, KOMMUNE_ID)
    return openpyxl.load_workbook(io.BytesIO(data)), agg


def _text(zeile) -> str:
    return " ".join(str(v) for v in zeile if v is not None)


def test_zusammenfassung_traegt_vollstaendigkeit(export):
    wb, agg = export
    zeilen = [r for r in wb["Zusammenfassung"].iter_rows(values_only=True)
              if r[0] == "Vollständigkeit"]
    assert len(zeilen) == 1
    assert zeilen[0][1] == agg["cost"]["euro_coverage"]["text"]


def test_nicht_additive_zeilen_tragen_vermerk(export):
    wb, _ = export
    zeilen = list(wb["Klimawirkungen"].iter_rows(min_row=2, values_only=True))
    na = [z for z in zeilen if z[0] in catalog.NON_ADDITIVE_RISK_CODES]
    assert na
    for z in na:
        assert VERMERK in _text(z)


def test_additive_klasse_a_ohne_vermerk(export):
    wb, _ = export
    zeilen = list(wb["Klimawirkungen"].iter_rows(min_row=2, values_only=True))
    a = [z for z in zeilen if z[0] == KLASSE_A_CODE]
    assert a
    for z in a:
        assert VERMERK not in _text(z)
