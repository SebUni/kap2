"""Tests zum Schicht-B-Framework (Stufe 3): Σ-über-Zellen-Aggregation.

Deckt ab:
  (a) total_eur == Summe der materialisierten Zell-Kosten (pop/area-Risiken).
  (b) Oschatz-Fall (§3.6): wenige Hotspot-Zellen → Summe ≠ P90-basierter Alt-Wert,
      und die Summe stimmt mit der Handrechnung überein.
  (c) Neue Aggregat-Felder: p90_index, outcome_sum, aggregation, top5_share,
      area_km2_affected, share_above_threshold.
  (d) flat-Risiken (Ausfallstunden/Index) bleiben P90-basiert (aggregation="p90").
  (e) Alt-Zelldaten ohne materialisierten outcome → identisches Ergebnis (Fallback).
  (f) compute_cell_impacts liefert für pop-Risiken mit Index>0 nicht-null Outcome/Kosten
      (GeoPackage-Export-Spalten sind damit gefüllt, nicht konstant 0).

Läuft mit pytest oder direkt: ``python tests/test_layer_b_framework.py``.
"""

from __future__ import annotations

from app.data import catalog
from app.services.engine import impact, override_context, risk_engine

MORT = "EXPECTED_ANNUAL_MORTALITY"   # pop-skaliert, monetär über VSL
OUTAGE = "EXPECTED_ENERGY_OUTAGE_HOURS"  # flat-skaliert (Stunden/Jahr)


def _cell(index: float, pop: float, materialize: bool = True) -> dict:
    risks: dict[str, dict] = {}
    for r in catalog.RISKS:
        entry = {"index": index}
        if materialize:
            imp = impact.compute_cell_impacts(r, index, pop)
            o, c = round(imp["outcome"], 4), round(imp["cost_eur"], 2)
            if o:
                entry["outcome"] = o
            if c:
                entry["cost_eur"] = c
        risks[r["code"]] = entry
    return {"risks": risks, "inputs": {"pop": pop}}


# ── (a) total_eur == Σ Zell-Kosten ─────────────────────────────────────────────

def test_total_eur_is_sum_of_cell_costs():
    override_context.set_overrides({})
    cells = [_cell(30.0, 100.0), _cell(70.0, 250.0), _cell(10.0, 50.0)]
    agg = risk_engine.aggregate(cells, total_pop=400.0, area_km2=5.0)

    # Für ein pop-Risiko: aggregierte Kosten == Summe der materialisierten Zell-Kosten.
    manual = sum(c["risks"][MORT].get("cost_eur", 0.0) for c in cells)
    assert abs(agg["risks"][MORT]["cost_eur"] - round(manual, 2)) < 0.01
    assert agg["risks"][MORT]["aggregation"] == "sum"

    # total_eur == Summe aller Einzel-cost_eur.
    summed = round(sum(r["cost_eur"] for r in agg["risks"].values()), 2)
    assert abs(agg["cost"]["total_eur"] - summed) < 0.01


# ── (b) Oschatz-Fall: Summe ≠ P90-Alt-Wert ─────────────────────────────────────

def test_oschatz_sum_differs_from_p90_estimate():
    override_context.set_overrides({})
    cells = [_cell(5.0, 10.0) for _ in range(9900)] + [_cell(80.0, 10.0) for _ in range(100)]
    total_pop = 100000.0
    agg = risk_engine.aggregate(cells, total_pop=total_pop, area_km2=50.0)

    rdef = catalog.RISKS_BY_CODE[MORT]
    # Handrechnung: Σ cell_outcome
    manual = sum(risk_engine.cell_outcome(rdef, c["risks"][MORT]["index"],
                                          c["inputs"]["pop"]) for c in cells)
    assert abs(agg["risks"][MORT]["outcome"] - round(manual, 2)) < 0.1

    # Alt-Weg (P90 × Gesamtbevölkerung) wäre deutlich niedriger (Hotspots verschwinden).
    p90_est = risk_engine.estimate_outcome_and_cost(
        rdef, agg["risks"][MORT]["p90_index"], total_pop, 50.0)["outcome"]
    assert agg["risks"][MORT]["outcome"] > p90_est * 1.1


# ── (c) neue Felder ────────────────────────────────────────────────────────────

def test_new_aggregate_fields_present():
    override_context.set_overrides({})
    cells = [_cell(80.0, 100.0)] + [_cell(5.0, 100.0) for _ in range(9)]
    agg = risk_engine.aggregate(cells, total_pop=1000.0, area_km2=10.0)
    r = agg["risks"][MORT]
    for key in ("p90_index", "outcome_sum", "aggregation", "top5_share",
                "area_km2_affected", "share_above_threshold"):
        assert key in r, key
    # 1 von 10 Zellen über der Schwelle (Index 80 ≥ 50) → 10 %.
    assert r["share_above_threshold"] == 0.1
    assert r["area_km2_affected"] == round(1 * risk_engine.CELL_AREA_KM2, 4)
    # Konzentration: die eine Hotspot-Zelle trägt den Großteil → top5_share hoch.
    assert r["top5_share"] > 0.5


# ── (d) flat-Risiken bleiben P90 ───────────────────────────────────────────────

def test_flat_risks_stay_p90():
    override_context.set_overrides({})
    cells = [_cell(40.0, 100.0) for _ in range(50)]
    agg = risk_engine.aggregate(cells, total_pop=5000.0, area_km2=5.0)
    assert agg["risks"][OUTAGE]["aggregation"] == "p90"
    assert agg["risks"][MORT]["aggregation"] == "sum"


# ── (e) Alt-Daten-Fallback ─────────────────────────────────────────────────────

def test_old_cells_without_outcome_fall_back():
    override_context.set_overrides({})
    mat = [_cell(60.0, 200.0), _cell(20.0, 80.0)]
    old = [_cell(60.0, 200.0, materialize=False), _cell(20.0, 80.0, materialize=False)]
    a_mat = risk_engine.aggregate(mat, total_pop=280.0, area_km2=3.0)
    a_old = risk_engine.aggregate(old, total_pop=280.0, area_km2=3.0)
    assert abs(a_mat["risks"][MORT]["cost_eur"] - a_old["risks"][MORT]["cost_eur"]) < 0.01
    assert abs(a_mat["risks"][MORT]["outcome"] - a_old["risks"][MORT]["outcome"]) < 0.01


# ── (f) Export-Spalten gefüllt ─────────────────────────────────────────────────

def test_compute_cell_impacts_nonzero_for_pop_risk():
    override_context.set_overrides({})
    rdef = catalog.RISKS_BY_CODE[MORT]
    imp = impact.compute_cell_impacts(rdef, 50.0, 500.0)
    assert imp["outcome"] > 0.0
    assert imp["cost_eur"] > 0.0
    assert not impact.has(MORT)  # Stufe 3: noch keine eigene Impact-Funktion registriert


if __name__ == "__main__":
    import sys
    import pytest
    sys.exit(pytest.main([__file__, "-q"]))
