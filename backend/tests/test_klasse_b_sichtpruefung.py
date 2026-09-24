"""Sichtprüfung Verwechslungssperre Klasse A/B: die Punkte 1 bis 6 (Vorhaben T-0563).

Jeder Punkt wird an genau einer Testwirkung nachgewiesen, die nur im Test als
Klasse B markiert ist (``tests/klasse_b_testwirkung.py``; der Katalog bleibt
unverändert). Es gibt bewusst keinen Test, der verlangt, der Katalog enthalte keine
Klasse-B-Wirkung — der sperrte den ersten echten Eintrag.

1. by_risk: cost_eur None und Reihenfolge.
2. Dienste: kein Betrag in Gruppensumme, Maßnahmen-Nutzen und KI-Kontext, dort Vermerk.
3. Dashboard-Daten: has_euro_layer False, kein cost_eur; Block im Frontend.
4. GeoPackage: ``_outcome`` numerisch, fehlende Werte NULL.
5. Rundweg über echtes pyogrio mit dem Vermerk.
6. Excel: Vollständigkeit in der Zusammenfassung.
"""

from __future__ import annotations

import io
import re
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pyogrio
import pyogrio.raw
import pytest
from shapely.geometry import Polygon, box

import _stub_heavy_deps  # noqa: F401

from app.data import catalog
from app.models.models import (
    AdaptationMeasure, CellAssessment, ConfigParameter, GridCell, Kommune, MeasureImpact,
)
from app.services import (
    ai_context_service, export_service, geodata_export_service as gx, measure_service,
)
from app.services.engine import risk_engine

from tests.klasse_b_testwirkung import KLASSE_B_CODE, KLASSE_B_NAME, wirkung_einhaengen
from tests.test_klasse_b_excel import _FakeDB as _ExcelDB
from tests.test_klasse_b_geopackage import _FakeDB
from tests.test_klasse_b_massnahmen import _Session, _mdef, _zellen

RISK_RADAR = (Path(__file__).resolve().parents[2] / "frontend" / "src" / "components"
              / "dashboard" / "RiskRadarSection.tsx")


@pytest.fixture
def wirkung(monkeypatch):
    return wirkung_einhaengen(monkeypatch)


def _aggregate(mit_b: bool = True) -> dict:
    """Aggregat über den aktuellen Katalog; die Testwirkung trägt in beiden Zellen Werte."""
    risks = [r for r in catalog.RISKS if mit_b or r["code"] != KLASSE_B_CODE]
    werte = {r["code"]: {"index": 40.0, "outcome": 1.0,
                         "cost_eur": r["cost_per_outcome_eur"]} for r in risks}
    zellen = [{"risks": dict(werte), "inputs": {"pop": 250.0}} for _ in range(2)]
    return risk_engine.aggregate(zellen, total_pop=500.0, area_km2=2.0)


def _impact(monkeypatch) -> dict:
    monkeypatch.setattr(measure_service, "_coverage",
                        lambda db, m: ({1: 1.0, 2: 1.0}, 20000.0))
    monkeypatch.setattr(
        measure_service, "get_risk_aggregate",
        lambda db, kid, apply_measures=False, demo_session_id=None: {
            "risks": {KLASSE_B_CODE: {"cost_eur": 1_000_000.0}}})
    measure = SimpleNamespace(id=7, kommune_id=1, measure_type="TEST", config={},
                              impact_summary=None)
    db = _Session(_zellen([KLASSE_B_CODE]), SimpleNamespace(population=500, area_km2=2.0))
    return measure_service._compute_impact_scoped(db, measure, _mdef([KLASSE_B_CODE]), "fp")


# ── Punkt 1 ──────────────────────────────────────────────────────────────────

def test_punkt_1_by_risk_cost_eur_none_und_reihenfolge(wirkung):
    agg = _aggregate()
    by_risk = agg["cost"]["by_risk"]
    eintrag = [e for e in by_risk if e["code"] == KLASSE_B_CODE]
    assert len(eintrag) == 1
    assert eintrag[0]["cost_eur"] is None
    assert eintrag[0]["has_euro_layer"] is False
    assert eintrag[0]["cost_display"] == catalog.NO_EURO_LAYER_TEXT
    assert agg["risks"][KLASSE_B_CODE]["cost_eur"] is None
    # Klasse A vor Klasse B; Klasse A absteigend nach Betrag, B steht am Ende.
    flags = [e["has_euro_layer"] for e in by_risk]
    assert flags == sorted(flags, reverse=True)
    assert by_risk[-1]["code"] == KLASSE_B_CODE
    betraege = [e["cost_eur"] for e in by_risk if e["has_euro_layer"]]
    assert betraege == sorted(betraege, reverse=True)


# ── Punkt 2 ──────────────────────────────────────────────────────────────────

def test_punkt_2_dienste_ohne_betrag_mit_vermerk(wirkung, monkeypatch):
    mit, ohne = _aggregate(), _aggregate(mit_b=False)
    # Gruppensumme: Summe unverändert, Gruppe trägt keinen Euro-Betrag.
    assert mit["cost"]["total_eur"] == ohne["cost"]["total_eur"]
    gruppe = mit["groups"]["heat"]
    assert KLASSE_B_CODE in gruppe["risk_codes"]
    assert not [k for k in gruppe if "cost" in k or "eur" in k]

    # Maßnahmen-Nutzen: reine Klasse-B-Maßnahme zeigt den Vermerk, nicht 0.
    s = _impact(monkeypatch)
    assert s["annual_benefit_damage_eur"] == 0.0
    assert s["benefit_has_euro_layer"] is False
    assert s["benefit_display"] == catalog.NO_EURO_LAYER_TEXT

    # KI-Kontext: Risikozeile mit Vermerk und ohne Betrag, nicht in der Top-Liste.
    monkeypatch.setattr(ai_context_service.measure_service, "get_risk_aggregate",
                        lambda *a, **k: mit)
    monkeypatch.setattr(ai_context_service.lower_bound, "qualifier_text",
                        lambda *a, **k: "")
    monkeypatch.setattr(ai_context_service.lower_bound, "overridden_cost_rate_codes",
                        lambda *a, **k: [])
    zeilen = ai_context_service._risk_lines(None, 1)
    treffer = [z for z in zeilen if KLASSE_B_NAME in z]
    assert len(treffer) == 1
    assert catalog.NO_EURO_LAYER_TEXT in treffer[0]
    assert "€" not in treffer[0]
    i_top = zeilen.index("TOP-EINZELRISIKEN (Schaden/Jahr, Index, Klasse):")
    i_weitere = next(i for i, z in enumerate(zeilen) if z.startswith("WEITERE WIRKUNGEN"))
    assert i_top < i_weitere
    assert not any(KLASSE_B_NAME in z for z in zeilen[i_top:i_weitere])

    # KI-Kontext: Maßnahmenzeile trägt den Vermerk statt eines Nutzens von 0 €.
    class _M:
        name = "Testmaßnahme"
        measure_type = "test"
        impact_summary = {"capex_eur": 1000.0, "annual_benefit_eur": 0.0,
                          "benefit_has_euro_layer": s["benefit_has_euro_layer"],
                          "benefit_display": s["benefit_display"],
                          "benefit_note": s["benefit_note"]}

    class _Q:
        def filter(self, *a, **k):
            return self

        def limit(self, *a):
            return self

        def all(self):
            return [_M()]

    class _DB:
        def query(self, *a):
            return _Q()

    massnahme = next(z for z in ai_context_service._measure_lines(_DB(), 1)
                     if "Testmaßnahme" in z)
    assert catalog.NO_EURO_LAYER_TEXT in massnahme
    assert "Nutzen 0" not in massnahme


# ── Punkt 3 ──────────────────────────────────────────────────────────────────

def test_punkt_3_dashboard_daten_und_block(wirkung):
    eintrag = next(e for e in _aggregate()["cost"]["by_risk"] if e["code"] == KLASSE_B_CODE)
    assert eintrag["has_euro_layer"] is False
    assert eintrag["cost_eur"] is None
    assert eintrag["cost_display"] == catalog.NO_EURO_LAYER_TEXT
    quelle = re.sub(r"/\*.*?\*/", "", RISK_RADAR.read_text(encoding="utf-8"), flags=re.S)
    assert "Ohne Euro-Bezifferung (Screening)" in quelle


# ── GeoPackage-Grundlage (Punkte 4 und 5) ────────────────────────────────────

def _geopackage_db(echt: bool):
    klasse_a = next(r["code"] for r in catalog.RISKS if catalog.risk_has_euro_layer(r))
    daten = {"risks": {
        klasse_a: {"index": 30.0, "outcome": 2, "cost_eur": 5.0},
        KLASSE_B_CODE: {"index": 40.0, "outcome": 1.5, "cost_eur": 0.0},
    }}
    if echt:
        geoms = [box(13.0 + i * 0.001, 51.0, 13.001 + i * 0.001, 51.001) for i in range(3)]
        grenze = Polygon([(12.99, 50.99), (13.01, 50.99), (13.01, 51.01), (12.99, 51.01)])
    else:
        geoms = [object() for _ in range(3)]
        grenze = object()
    # Zelle ohne Wert zuerst: der Spaltentyp wird an col[0] bestimmt.
    zeilen = [
        (CellAssessment(data={}), GridCell(gitter_id="G0", x_3035=1.0, y_3035=1.0, geometry=geoms[0])),
        (CellAssessment(data=daten), GridCell(gitter_id="G1", x_3035=2.0, y_3035=1.0, geometry=geoms[1])),
        (CellAssessment(data=daten), GridCell(gitter_id="G2", x_3035=3.0, y_3035=1.0, geometry=geoms[2])),
    ]
    kommune = Kommune(id=1, name="K", bundesland="SN", area_km2=2.0, population=500,
                      boundary=grenze)
    return _FakeDB({Kommune: [kommune], CellAssessment: zeilen})


# ── Punkt 4 ──────────────────────────────────────────────────────────────────

def test_punkt_4_geopackage_outcome_zahl_fehlend_null(wirkung, monkeypatch, tmp_path):
    monkeypatch.setattr(gx, "assessment_is_done", lambda db, kid: True)
    monkeypatch.setattr(gx, "_build_output_path", lambda kid, eid: str(tmp_path / "t.gpkg"))
    monkeypatch.setattr(gx, "to_shape", lambda g: SimpleNamespace(geom_type="Polygon"))
    aufrufe: dict = {}
    monkeypatch.setattr(gx, "_write_layer",
                        lambda path, name, geoms, data, fields, **kw:
                        aufrufe.__setitem__(name, dict(zip(fields, data))))
    gx.build_geopackage(_geopackage_db(False), 1, 1)
    spalte = aufrufe["bewertung_100m"][f"{KLASSE_B_CODE}_outcome"]
    assert len(spalte) == 3
    assert spalte[0] is None  # Zelle ohne Wert: NULL, nie 0.0
    assert all(type(w) is float for w in spalte[1:])
    assert list(spalte[1:]) == [1.5, 1.5]
    assert not any(isinstance(w, str) for w in spalte)


# ── Punkt 5 ──────────────────────────────────────────────────────────────────

def test_punkt_5_rundweg_echtes_pyogrio_mit_vermerk(wirkung, monkeypatch, tmp_path):
    pfad = tmp_path / "rundweg.gpkg"
    monkeypatch.setattr(gx, "assessment_is_done", lambda db, kid: True)
    monkeypatch.setattr(gx, "_build_output_path", lambda kid, eid: str(pfad))
    monkeypatch.setattr(gx, "to_shape", lambda g: g)
    assert gx.build_geopackage(_geopackage_db(True), 1, 1) == str(pfad)
    meta, fids, _geom, werte = pyogrio.raw.read(str(pfad), layer="bewertung_100m",
                                                return_fids=True)
    spalten = dict(zip(meta["fields"], werte))
    vermerk = spalten[f"{KLASSE_B_CODE}_cost_eur"]
    assert len(vermerk) == 3
    assert all(w == catalog.NO_EURO_LAYER_TEXT for w in vermerk), list(vermerk)
    feld = f"{KLASSE_B_CODE}_outcome"
    assert np.issubdtype(spalten[feld].dtype, np.number)
    assert float(spalten[feld][1]) == 1.5
    # Die Zelle ohne Wert ist NULL (über den Filter ausgewiesen), nicht 0.0.
    _m, null_fids, _g, _s = pyogrio.raw.read(str(pfad), layer="bewertung_100m",
                                             return_fids=True, where=f'"{feld}" IS NULL')
    assert [int(f) for f in null_fids] == [int(fids[0])]


# ── Punkt 6 ──────────────────────────────────────────────────────────────────

def test_punkt_6_excel_vollstaendigkeit_in_zusammenfassung(wirkung, monkeypatch):
    openpyxl = pytest.importorskip("openpyxl")
    agg = _aggregate()
    measure = AdaptationMeasure(
        id=1, kommune_id=1, name="Testmaßnahme", measure_type="tree_planting",
        geometry=None, config={}, implementation_year=2027, description="",
        impact_summary={"capex_eur": 1000.0})
    kommune = Kommune(id=1, name="Testheim", osm_id="R1", population=5000, area_km2=10.0)
    db = _ExcelDB({AdaptationMeasure: [measure], MeasureImpact: [],
                   ConfigParameter: [], Kommune: [kommune]})
    monkeypatch.setattr(measure_service, "get_risk_aggregate", lambda *a, **k: agg)
    monkeypatch.setattr(
        measure_service, "ensure_fresh_impact_summary",
        lambda db, m: {"capex_eur": 1000.0, "opex_annual_eur": 50.0,
                       "annual_benefit_eur": 4200.0, "count": 12})
    wb = openpyxl.load_workbook(io.BytesIO(export_service.export_measures_xlsx(db, 1)))
    zeilen = [r for r in wb["Zusammenfassung"].iter_rows(values_only=True)
              if r[0] == "Vollständigkeit"]
    assert len(zeilen) == 1
    text = agg["cost"]["euro_coverage"]["text"]
    assert zeilen[0][1] == text
    assert "von" in text
