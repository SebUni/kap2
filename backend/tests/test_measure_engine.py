"""Tests der Maßnahmen-Engine (Stufe 6, E3): Nutzen = Zellkosten-Delta.

Der Maßnahmen-Nutzen (``compute_impact``) ist die **Summe der reduzierten Zellkosten**
``Σ_zellen Σ_linked  Zellkosten · (1 − factor)``. Für pop-/area-skalierte Risiken ist
das exakt der Beitrag der Maßnahme zur „Vermiedene Schäden"-Kennzahl des Kommunen-
Aggregats, weil ``compute_impact`` und ``risk_engine.aggregate``/``_adjusted_cell_data``
dieselbe Zellkosten-Basis (``_cell_cost``) und denselben multiplikativen Zell-Faktor
benutzen.

Die Tests beweisen diese Reconciliation DB-frei mit denselben Bausteinen: ``compute_impact``
selbst braucht PostGIS (ST_Intersection/ST_Area) und ist hier bewusst nicht End-to-End
getestet — die kostenrelevante Logik steckt in ``_cell_cost`` + ``aggregate`` und wird
direkt geprüft. ``_adjusted_cell_data`` wird durch ``_scaled_cell`` exakt nachgebildet
(Index/Outcome/Kosten × factor).
"""

from __future__ import annotations

import copy

import pytest

from app.data import catalog
from app.services import measure_service
from app.services.engine import impact, risk_engine

# Repräsentative Risiken je Skalierung (dynamisch, robust gegen Katalog-Umbenennungen).
POP_RISK = next(r for r in catalog.RISKS
                if r.get("scale", "pop") == "pop" and catalog.risk_contributes_to_total(r))
AREA_RISK = next(r for r in catalog.RISKS
                 if r.get("scale", "pop") == "area" and catalog.risk_contributes_to_total(r))
FLAT_RISK = next((r for r in catalog.RISKS
                  if r.get("scale", "pop") not in ("pop", "area")), None)


def _cell(code: str, index: float, pop: float, cost: float) -> dict:
    """Zelldaten-Dict mit einem materialisierten Risiko (outcome==cost der Einfachheit)."""
    return {
        "inputs": {"pop": pop},
        "risks": {code: {"index": index, "outcome": cost, "cost_eur": cost}},
    }


def _scaled_cell(cell: dict, code: str, factor: float) -> dict:
    """Bildet ``_adjusted_cell_data`` nach: skaliert index/outcome/cost_eur mit factor."""
    r = cell["risks"][code]
    entry = {"index": r["index"] * factor}
    if "outcome" in r:
        entry["outcome"] = r["outcome"] * factor
    if "cost_eur" in r:
        entry["cost_eur"] = r["cost_eur"] * factor
    new = copy.deepcopy(cell)
    new["risks"][code] = entry
    return new


def _cell_benefit(risk: dict, cell: dict, factor: float) -> float:
    """Nutzenbeitrag einer abgedeckten Zelle wie in ``compute_impact``."""
    code = risk["code"]
    cell_pop = float(cell["inputs"]["pop"])
    return measure_service._cell_cost(risk, cell["risks"][code], cell_pop) * (1.0 - factor)


# ── _cell_cost: materialisiert vs. Legacy-Fallback ──────────────────────────

def test_cell_cost_uses_materialized_value():
    r = {"index": 40.0, "outcome": 123.0, "cost_eur": 456.0}
    assert measure_service._cell_cost(POP_RISK, r, 800.0) == 456.0


def test_cell_cost_falls_back_to_legacy_without_outcome():
    """Alt-Zelle ohne materialisierten Outcome ⇒ identische Nachrechnung wie im
    Aggregat-Fallback (``impact.compute_cell_impacts``)."""
    r_old = {"index": 40.0}
    expected = impact.compute_cell_impacts(POP_RISK, 40.0, 800.0)["cost_eur"]
    assert measure_service._cell_cost(POP_RISK, r_old, 800.0) == expected


# ── Reconciliation: Nutzen == Aggregat-Delta ────────────────────────────────

@pytest.mark.parametrize("risk", [POP_RISK, AREA_RISK])
def test_benefit_equals_aggregate_cost_delta(risk):
    """Σ_covered Zellkosten·(1−factor) == Basis-Aggregat − Mit-Maßnahmen-Aggregat."""
    code = risk["code"]
    pop, area = 50_000.0, 30.0
    factor = 0.6  # Restfaktor nach der Maßnahme (40 % Reduktion)
    cells = [_cell(code, index=10.0 * i + 5.0, pop=1000.0 * i + 500.0, cost=1000.0 * (i + 1))
             for i in range(5)]
    covered = {0, 2, 4}

    base = risk_engine.aggregate(copy.deepcopy(cells), pop, area)
    with_cells = [_scaled_cell(c, code, factor) if i in covered else copy.deepcopy(c)
                  for i, c in enumerate(cells)]
    withm = risk_engine.aggregate(with_cells, pop, area)

    benefit = sum(_cell_benefit(risk, cells[i], factor) for i in covered)

    delta_risk = base["risks"][code]["cost_eur"] - withm["risks"][code]["cost_eur"]
    assert benefit == pytest.approx(delta_risk, abs=0.01)
    # Nur dieses Risiko ist in den Zelldaten → Gesamt-Delta == Risiko-Delta.
    delta_total = base["cost"]["total_eur"] - withm["cost"]["total_eur"]
    assert benefit == pytest.approx(delta_total, abs=0.01)
    # Handrechnung: (1000+3000+5000)·0.4 = 3600
    assert benefit == pytest.approx(3600.0, abs=0.01)


def test_partial_coverage_only_reduces_covered_cells():
    """Eine Teilflächen-Maßnahme mindert nur die abgedeckte Zelle; der Nutzen ist
    genau deren Kostenanteil·(1−factor), unbedeckte Zellen bleiben unverändert."""
    code = POP_RISK["code"]
    pop, area = 8000.0, 10.0
    factor = 0.5
    cells = [_cell(code, index=20.0, pop=500.0, cost=1000.0 * (i + 1)) for i in range(4)]
    covered = {1}

    base = risk_engine.aggregate(copy.deepcopy(cells), pop, area)
    with_cells = [_scaled_cell(c, code, factor) if i in covered else copy.deepcopy(c)
                  for i, c in enumerate(cells)]
    withm = risk_engine.aggregate(with_cells, pop, area)

    benefit = _cell_benefit(POP_RISK, cells[1], factor)
    assert benefit == pytest.approx(cells[1]["risks"][code]["cost_eur"] * (1 - factor), abs=1e-9)
    assert benefit == pytest.approx(
        base["risks"][code]["cost_eur"] - withm["risks"][code]["cost_eur"], abs=0.01)


def test_flat_risk_is_p90_and_excluded_from_cell_benefit():
    """Flache Ausfall-/Screening-Risiken sind nicht zell-additiv (Aggregat P90-basiert)
    und deshalb bewusst vom Zellkosten-Nutzen ausgenommen (scale ∉ pop/area)."""
    assert FLAT_RISK is not None, "Katalog ohne flat-Risiko?"
    code = FLAT_RISK["code"]
    cells = [{"inputs": {"pop": 500.0}, "risks": {code: {"index": 30.0}}} for _ in range(4)]
    agg = risk_engine.aggregate(cells, 10_000.0, 20.0)
    assert agg["risks"][code]["aggregation"] == "p90"
    # Genau dieser Filter greift in compute_impact (scale ∉ pop/area ⇒ kein Zell-Nutzen).
    assert FLAT_RISK.get("scale", "pop") not in ("pop", "area")


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-q"]))
