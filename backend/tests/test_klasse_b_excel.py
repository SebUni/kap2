"""Excel-Export: Blatt „Klimawirkungen“ mit Screening-Vermerk und Vollständigkeit (T-0516).

Verwechslungssperre Klasse A/B (T-0358): Eine Wirkung ohne Euro-Schicht
(Katalogeintrag ``"euro_layer": False``) darf im Excel-Export in der Spalte
„Schaden pro Jahr“ keine 0 zeigen — ein Gutachter läse sie als „kein Schaden“.
Dort steht wörtlich ``catalog.NO_EURO_LAYER_TEXT``. Außerdem trägt das Blatt die
Vollständigkeitsanzeige ``cost['euro_coverage']['text']`` des Aggregats.

Geprüft werden die echten xlsx-Bytes aus ``export_measures_xlsx``, mit openpyxl
zurückgelesen. Ohne Datenbank: Session-Doppel, Aggregat über
``measure_service.get_risk_aggregate`` gesetzt.
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
KLASSE_B_CODE = "TEST_KLASSE_B_EXCEL"
VERMERK = "Screening ohne Euro-Bezifferung"
KOMMUNE_ID = 1


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
    """Hängt eine Klasse-B-Wirkung in den Katalog ein (RISKS und RISKS_BY_CODE)."""
    risk = _klasse_b_eintrag()
    monkeypatch.setattr(catalog, "RISKS", list(catalog.RISKS) + [risk])
    monkeypatch.setitem(catalog.RISKS_BY_CODE, KLASSE_B_CODE, risk)
    return risk


def _aggregate() -> dict:
    """Kostenblock wie ``risk_engine.aggregate`` ihn ausgibt, mit einer Klasse-B-Zeile."""
    by_risk = []
    for code, cost_eur in ((KLASSE_A_CODE, 5432.1), (KLASSE_B_CODE, 0.0)):
        risk = catalog.RISKS_BY_CODE[code]
        has_euro = catalog.risk_has_euro_layer(risk)
        by_risk.append({
            "code": code, "name": risk["name"], "cost_eur": cost_eur,
            "index": 40.0, "risk_class": "mittel",
            "has_euro_layer": has_euro,
            "cost_display": cost_eur if has_euro else catalog.NO_EURO_LAYER_TEXT,
        })
    cov = catalog.euro_coverage(catalog.RISKS)
    return {
        "cost": {
            "total_eur": 5432.1,
            "by_risk": by_risk,
            "euro_coverage": {"covered": cov.covered, "total": cov.total,
                              "text": cov.text},
        },
        "groups": {},
    }


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


@pytest.fixture
def export(db, klasse_b, monkeypatch):
    """Exportiert und liest die xlsx-Bytes mit openpyxl zurück; liefert (Mappe, Aggregat)."""
    agg = _aggregate()
    monkeypatch.setattr(measure_service, "get_risk_aggregate", lambda *a, **k: agg)
    monkeypatch.setattr(
        measure_service, "ensure_fresh_impact_summary",
        lambda db, m: {"capex_eur": 1000.0, "opex_annual_eur": 50.0,
                       "annual_benefit_eur": 4200.0, "count": 12},
    )
    data = export_service.export_measures_xlsx(db, KOMMUNE_ID)
    wb = openpyxl.load_workbook(io.BytesIO(data))
    return wb, agg


def _klasse_b_zeile(ws) -> tuple[dict, list]:
    kopf = [c.value for c in ws[1]]
    zeilen = [list(r) for r in ws.iter_rows(min_row=2, values_only=True)]
    treffer = [z for z in zeilen if KLASSE_B_CODE in z]
    assert len(treffer) == 1, f"Klasse-B-Zeile nicht eindeutig gefunden: {zeilen}"
    return {name: i for i, name in enumerate(kopf)}, treffer[0]


# (1) Blatt vorhanden
def test_blatt_klimawirkungen_vorhanden(export):
    wb, _ = export
    assert "Klimawirkungen" in wb.sheetnames


# (2) Klasse B trägt den Vermerk, nie 0 / 0.0 / "-" / None
def test_klasse_b_zeigt_vermerk_statt_zahl(export):
    wb, _ = export
    spalten, zeile = _klasse_b_zeile(wb["Klimawirkungen"])
    assert "Schaden pro Jahr" in spalten
    wert = zeile[spalten["Schaden pro Jahr"]]
    assert wert == VERMERK
    assert catalog.NO_EURO_LAYER_TEXT == VERMERK
    assert wert not in (0, 0.0, "-", None)


# Gegenprobe: Klasse A behält ihren Eurobetrag als Zahl
def test_klasse_a_behaelt_eurobetrag(export):
    wb, _ = export
    ws = wb["Klimawirkungen"]
    spalten = {c.value: i for i, c in enumerate(ws[1])}
    zeile = next(r for r in ws.iter_rows(min_row=2, values_only=True)
                 if KLASSE_A_CODE in r)
    wert = zeile[spalten["Schaden pro Jahr"]]
    assert isinstance(wert, (int, float)) and abs(wert - 5432.1) < 1e-6


# (3) Vollständigkeitsanzeige wörtlich aus dem Aggregat
def test_vollstaendigkeit_woertlich_aus_aggregat(export):
    wb, agg = export
    text = agg["cost"]["euro_coverage"]["text"]
    ws = wb["Klimawirkungen"]
    zellen = [v for r in ws.iter_rows(values_only=True) for v in r]
    assert text in zellen
    assert "von" in text and "Klimawirkungen in Euro beziffert" in text


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
