"""Ü-11 (Befund 253): Kosten der Stadtbaumwahl je ersetztem Baum nach Fall.

Bericht #96 §5, Absatz „Kosten der Stadtbaumwahl“, Kap. 7.1 Block ``pollen.stadtbaum_kosten``
(Abschätzung von KAP3, Preisstand 2024): 60 € je Baum bei ohnehin fälliger Nachpflanzung
(Mehrkosten der Artenwahl), 4.436 € je Baum bei vorgezogenem Ersatz (Pflanzung mit
Anwuchspflege 3.636 € plus Fällung 800 €). Die Kommune wählt den Fall in
``config['ersatzfall']``; ohne Fall entsteht kein CAPEX und keine Kosten-Nutzen-Kennzahl, das
``impact_summary`` zeigt beide Beträge nebeneinander (``capex_je_fall``). Eine stille Vorgabe
gibt es nicht. Die Zahl der Bäume ist Pflichteingabe (``count_pflicht``).

Allee-Zelle (Block ``beispiel_96_stadtbaum_kosten``): 16 Bäume → 960 € (Nachpflanzung) und
70.976 € (vorgezogen). Die Wirkung hängt weder vom Fall noch von der Stückzahl ab; die Zelle
rechnet mit den Werten nach Ü-13 aus Bericht §5, Block ``beispiel_96_stadtbaum_allee``
(δ_B 0,43659, δ_G 0,57834, Ausgangsstand 172,538 Tage → 14,2 Tage und 88 € je Jahr). Die
Werte stehen hier fest und werden nicht aus der Registry gelesen.

DB-frei (Session-Doppel wie ``test_massnahme_stadtbaum_ausgabe.py``).
"""

from __future__ import annotations

import pytest

from app.data import catalog
from app.models.models import AdaptationMeasure, CellAssessment, ConfigParameter, Kommune
from app.schemas.schemas import MeasureCreate, _validate_config_value_ranges
from app.services import measure_service, parameter_registry

CODE = "LOW_ALLERGEN_TREE_SELECTION"
RISK = "EXPECTED_ANNUAL_ALLERGY_DAYS"
KOMMUNE_ID = 1
CELL_ID = 42
BAEUME = 16

# Allee-Zelle nach Ü-13 (Bericht §5, Block beispiel_96_stadtbaum_allee).
AUSGANGSSTAND_TAGE = 172.538
DELTA_BIRKE = 0.43659
DELTA_GRAESER = 0.57834


class _Q:
    def __init__(self, rows):
        self._rows = list(rows)

    def filter(self, *a, **k):
        return self

    def all(self):
        return list(self._rows)

    def first(self):
        return self._rows[0] if self._rows else None

    def delete(self):
        return 0

    def scalar(self):
        return None


class _DB:
    def __init__(self, rows):
        self._rows = rows
        self.added: list = []

    def query(self, model, *a, **k):
        return _Q(self._rows.get(model, []))

    def add(self, obj):
        self.added.append(obj)

    def commit(self):
        pass


def _allee_cell() -> dict:
    return {
        "index": AUSGANGSSTAND_TAGE, "outcome": AUSGANGSSTAND_TAGE,
        "betroffene": 100.0, "delta_birke": DELTA_BIRKE, "delta_graeser": DELTA_GRAESER,
        "pollen_g": 0.3625, "pollen_g_bar0": 0.18125,
        "canopy_birch_frac": 0.078125, "canopy_unknown_frac": 0.0, "green_frac": 0.3,
    }


def _run(config: dict, monkeypatch) -> dict:
    measure = AdaptationMeasure(
        id=1, kommune_id=KOMMUNE_ID, name="Stadtbaumwahl Kosten", measure_type=CODE,
        geometry=None, config=config, implementation_year=2027, description="",
        impact_summary={})
    kommune = Kommune(id=KOMMUNE_ID, name="Testheim", osm_id="R-STADTBAUM-K",
                      population=10_000, area_km2=5.0)
    zelle = CellAssessment(id=CELL_ID, kommune_id=KOMMUNE_ID, grid_cell_id=CELL_ID,
                           data={"risks": {RISK: _allee_cell()}, "inputs": {"pop": 100.0}})
    db = _DB({AdaptationMeasure: [measure], CellAssessment: [zelle],
              ConfigParameter: [], Kommune: [kommune]})
    monkeypatch.setattr(measure_service, "_coverage", lambda _db, _m: ({CELL_ID: 1.0}, 1000.0))
    monkeypatch.setattr(measure_service, "_params_fingerprint",
                        lambda *a, **k: "fp-test-stadtbaum-kosten")
    monkeypatch.setattr(parameter_registry, "load_db_overrides", lambda *a, **k: [])
    monkeypatch.setattr(measure_service, "get_risk_aggregate",
                        lambda *a, **k: {"risks": {RISK: {"cost_eur": 1_000_000_000.0}}})
    return measure_service.compute_impact(db, measure.id)


def _capex_komponenten(summary: dict) -> list[dict]:
    return summary["cost_breakdown"]["capex"]["components"]


def test_kosten_je_baum_nach_fall(monkeypatch):
    # Parameter der Registry (Ü-11 (a)).
    params = {p["id"]: p for p in parameter_registry.catalog_parameters(
        layer_code=CODE, layer_category="measures")}
    assert params[f"measures.{CODE}.capex_per_unit_nachpflanzung"]["value"] == pytest.approx(
        60.0, abs=1e-9)
    assert params[f"measures.{CODE}.capex_per_unit_vorgezogen"]["value"] == pytest.approx(
        4436.0, abs=1e-9)
    assert catalog.MEASURES_BY_CODE[CODE]["capex_per_unit"] is None

    # Mit Fall: CAPEX = Zahl der Bäume × Wert des Falls (Block beispiel_96_stadtbaum_kosten).
    soll = {"nachpflanzung": 960.0, "vorgezogen": 70_976.0}
    for fall, betrag in soll.items():
        summary = _run({"anteil_ersetzt": 1.0, "count": BAEUME, "ersatzfall": fall}, monkeypatch)
        assert summary["capex_eur"] == pytest.approx(betrag, abs=0.01)
        (komp,) = _capex_komponenten(summary)
        assert komp["param"] == "capex_per_unit" and komp["quantity"] == BAEUME
        assert komp["quantity_unit"] == "Baum" and komp["source"]
        assert summary["ersatzfall"] == fall
        assert "capex_je_fall" not in summary and "kosten_vermerk" not in summary
        assert summary["opex_annual_eur"] == 0.0
    nach = _run({"anteil_ersetzt": 1.0, "count": BAEUME, "ersatzfall": "nachpflanzung"},
                monkeypatch)
    assert nach["stadtbaum_kosten_hinweis"] == (
        "Der Nutzen je Jahr gilt erst mit voller Krone der sonst gepflanzten Bäume; "
        "Amortisation am Punktwert nach rund 24 Jahren (Bericht #96 §5)")

    # Ohne Fall: kein CAPEX, keine Komponente, keine Kosten-Nutzen-Kennzahl, beide Beträge.
    ohne = _run({"anteil_ersetzt": 1.0, "count": BAEUME}, monkeypatch)
    assert ohne["capex_eur"] == 0.0
    assert _capex_komponenten(ohne) == []
    assert ohne["kosten_nutzen_kennzahl_offen"] is True
    assert ohne["capex_je_fall"]["nachpflanzung"] == pytest.approx(960.0, abs=0.01)
    assert ohne["capex_je_fall"]["vorgezogen"] == pytest.approx(70_976.0, abs=0.01)
    assert ohne["kosten_vermerk"] == measure_service.STADTBAUM_FALL_WAEHLEN_TEXT
    assert ohne["ersatzfall"] is None


def test_ohne_stueckzahl_vermerk_statt_betrag(monkeypatch):
    summary = _run({"anteil_ersetzt": 1.0, "ersatzfall": "vorgezogen"}, monkeypatch)
    assert summary["kosten_vermerk"] == "Zahl der ersetzten Bäume eingeben"
    assert summary["capex_eur"] == 0.0 and _capex_komponenten(summary) == []
    assert "capex_je_fall" not in summary
    assert summary["count"] == 0 and summary["recommended_count"] == 0
    assert summary["count_is_default"] is False
    assert measure_service._resolve_count(
        catalog.MEASURES_BY_CODE[CODE], {}, 1_000_000.0) == (0, False, 0)


def test_anderer_ersatzfall_wird_abgewiesen():
    for gut in ("nachpflanzung", "vorgezogen"):
        assert _validate_config_value_ranges({"ersatzfall": gut}) == {"ersatzfall": gut}
    for schlecht in ("", "Nachpflanzung", "beide", 1, True):
        with pytest.raises(ValueError):
            _validate_config_value_ranges({"ersatzfall": schlecht})
    with pytest.raises(ValueError):
        MeasureCreate(name="x", measure_type=CODE, geometry_geojson={},
                      config={"ersatzfall": "irgendwas"})


@pytest.mark.parametrize("config_zusatz", [
    {},
    {"count": 1},
    {"count": BAEUME},
    {"count": 500},
    {"count": BAEUME, "ersatzfall": "nachpflanzung"},
    {"count": BAEUME, "ersatzfall": "vorgezogen"},
    {"count": 500, "ersatzfall": "vorgezogen"},
    {"ersatzfall": "nachpflanzung"},
])
def test_allee_zelle_unabhaengig_von_fall_und_stueckzahl(monkeypatch, config_zusatz):
    summary = _run({"anteil_ersetzt": 1.0, **config_zusatz}, monkeypatch)
    assert summary["stadtbaum_avoided_days_total"] == pytest.approx(14.2, abs=0.05)
    assert summary["stadtbaum_avoided_days_eur"] == pytest.approx(88, abs=0.5)


if __name__ == "__main__":
    import sys

    sys.exit(pytest.main([__file__, "-q"]))
