"""Excel-Export: Blatt „Klimawirkungen“ mit einer Zeile je Klimawirkung (T-1476-cto).

Punkt 3 aus T-1461-ceo: Das Kostenblatt schreibt nicht mehr je Katalogzeile aus
``cost.by_risk`` eine Tabellenzeile, sondern je Klimawirkung
(``klimawirkungen(cost['by_risk'])`` aus ``app.services.klimawirkungen``, T-1470-cto).
Trägt eine Klimawirkung mehrere Katalogzeilen (hier #95 Hitzebelastung: Mortalität und
Erkrankungen), steht sie einmal mit dem Summenbetrag in der Tabelle; die Teilzeilen
folgen mit dem Vermerk „Teil von #<Nr>“ in „Euro-Bezifferung“, damit niemand die Spalte
selbst summiert und dabei doppelt zählt. Eine Klimawirkung mit genau einer Katalogzeile
(hier #96) bekommt keine Teilzeile.

Geprüft werden die echten xlsx-Bytes aus ``export_measures_xlsx``, mit openpyxl
zurückgelesen. Ohne Datenbank: Session-Doppel, Aggregat direkt gesetzt.
"""

from __future__ import annotations

import io

import pytest

openpyxl = pytest.importorskip("openpyxl")
if not hasattr(openpyxl, "__version__"):  # Ersatzmodul statt echtem openpyxl
    pytest.skip("echtes openpyxl nötig, um die xlsx-Bytes zurückzulesen",
                allow_module_level=True)


from app.data import catalog  # noqa: E402
from app.models.models import AdaptationMeasure, ConfigParameter, Kommune, MeasureImpact  # noqa: E402
from app.services import export_service, measure_service  # noqa: E402

# #95 Hitzebelastung: zwei Katalogzeilen (Mortalität, Erkrankungen).
MORTALITAET_CODE = "EXPECTED_ANNUAL_MORTALITY"
ERKRANKUNGEN_CODE = "EXPECTED_ANNUAL_MORBIDITY"
# #96 Aeroallergene: eine Katalogzeile.
ALLERGIE_CODE = "EXPECTED_ANNUAL_ALLERGY_DAYS"
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


def _by_risk_zeile(code: str, cost_eur: float) -> dict:
    risk = catalog.RISKS_BY_CODE[code]
    return {
        "code": code, "name": risk["name"], "cost_eur": cost_eur,
        "index": 40.0, "risk_class": "mittel",
        "has_euro_layer": True,
        "cost_display": cost_eur,
    }


def _aggregate() -> dict:
    """Kostenblock mit zwei #95-Zeilen (1000,0 €, 500,0 €) und einer #96-Zeile (200,0 €)."""
    by_risk = [
        _by_risk_zeile(MORTALITAET_CODE, 1000.0),
        _by_risk_zeile(ERKRANKUNGEN_CODE, 500.0),
        _by_risk_zeile(ALLERGIE_CODE, 200.0),
    ]
    total = sum(r["cost_eur"] for r in by_risk)
    cov = catalog.euro_coverage(catalog.RISKS)
    return {
        "cost": {
            "total_eur": total,
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
def export(db, monkeypatch):
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


def _zeilen(ws) -> tuple[dict, list]:
    kopf = [c.value for c in ws[1]]
    spalten = {name: i for i, name in enumerate(kopf)}
    zeilen = [list(r) for r in ws.iter_rows(min_row=2, values_only=True)]
    return spalten, zeilen


# (1) #95 steht genau einmal, mit dem Summenbetrag 1500,0 in „Schaden pro Jahr“.
def test_hitzebelastung_eine_zeile_mit_summe(export):
    wb, _ = export
    spalten, zeilen = _zeilen(wb["Klimawirkungen"])
    treffer = [z for z in zeilen if z[spalten["Klimawirkung"]] == "Hitzebelastung (#95)"]
    assert len(treffer) == 1, f"#95 nicht genau einmal: {zeilen}"
    assert treffer[0][spalten["Schaden pro Jahr"]] == 1500.0


# (2) Die beiden Katalogzeilen zu #95 folgen als Teilzeilen mit „Teil von #95“.
def test_hitzebelastung_teilzeilen_mit_vermerk(export):
    wb, _ = export
    spalten, zeilen = _zeilen(wb["Klimawirkungen"])
    codes = {MORTALITAET_CODE: 1000.0, ERKRANKUNGEN_CODE: 500.0}
    for code, betrag in codes.items():
        treffer = [z for z in zeilen if z[spalten["Code"]] == code]
        assert len(treffer) == 1, f"{code} nicht genau einmal: {zeilen}"
        zeile = treffer[0]
        assert zeile[spalten["Schaden pro Jahr"]] == betrag
        assert zeile[spalten["Euro-Bezifferung"]] == "Teil von #95"


# (3) #96 heißt mit amtlichem Namen und hat keine Teilzeile.
def test_allergie_eine_zeile_ohne_teilzeile(export):
    wb, _ = export
    spalten, zeilen = _zeilen(wb["Klimawirkungen"])
    name = "Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft (#96)"
    treffer = [z for z in zeilen if z[spalten["Klimawirkung"]] == name]
    assert len(treffer) == 1, f"#96 nicht gefunden: {zeilen}"
    assert treffer[0][spalten["Schaden pro Jahr"]] == 200.0
    assert not any(z[spalten["Euro-Bezifferung"]] == "Teil von #96" for z in zeilen)


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-q"]))
