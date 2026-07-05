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
from app.services.engine import impact, override_context, risk_engine

# Repräsentative Risiken je Skalierung (dynamisch, robust gegen Katalog-Umbenennungen).
# Monetär gewählt, damit cost == outcome gilt (die Reconciliation-Handrechnungen bleiben
# vom Kostensatz unabhängig; die Live-Kostensatz-Wirkung testet _rate_override separat).
POP_RISK = next(r for r in catalog.RISKS
                if r.get("scale", "pop") == "pop" and catalog.risk_is_monetary(r))
AREA_RISK = next(r for r in catalog.RISKS
                 if r.get("scale", "pop") == "area" and catalog.risk_is_monetary(r))
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


# ── _cell_cost: live aus Outcome abgeleitet vs. Legacy-Fallback ─────────────

def test_cell_cost_derived_from_outcome_live():
    """Zellkosten werden LIVE aus dem Outcome × aktuellem Kostensatz abgeleitet, NICHT
    aus dem gespeicherten cost_eur (das hier bewusst abweicht) — so wirken Kostensatz-
    Overrides ohne Neuberechnung (§8/B2). Für monetäre Risiken gilt cost == outcome."""
    override_context.set_overrides({})
    r = {"index": 40.0, "outcome": 123.0, "cost_eur": 456.0}  # cost_eur wird ignoriert
    assert measure_service._cell_cost(POP_RISK, r, 800.0) == risk_engine.cost_from_outcome(
        POP_RISK, 123.0)


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


def test_cost_rate_override_is_live_without_recompute():
    """Kostensatz-Override (risks.*.cost_per_outcome) wirkt LIVE auf die Aggregatsumme,
    weil aggregate die Kosten aus dem gespeicherten Outcome × aktuellem Satz ableitet —
    das gespeicherte cost_eur (hier 999) wird ignoriert (§8/B2)."""
    health = next(r for r in catalog.RISKS
                  if r.get("scale", "pop") == "pop" and not catalog.risk_is_monetary(r)
                  and catalog.risk_contributes_to_total(r))
    code = health["code"]
    base_rate = catalog.risk_default_cost_per_outcome(health)
    cell = {"inputs": {"pop": 1000.0},
            "risks": {code: {"index": 50.0, "outcome": 2.0, "cost_eur": 999.0}}}

    override_context.set_overrides({})
    a0 = risk_engine.aggregate([copy.deepcopy(cell)], 1000.0, 10.0)
    assert a0["risks"][code]["cost_eur"] == pytest.approx(2.0 * base_rate, abs=0.01)

    override_context.set_overrides({f"risks.{code}.cost_per_outcome": base_rate * 2})
    a1 = risk_engine.aggregate([copy.deepcopy(cell)], 1000.0, 10.0)
    assert a1["risks"][code]["cost_eur"] == pytest.approx(2.0 * base_rate * 2, abs=0.01)
    override_context.set_overrides({})


def test_override_scope_resets_previous_state():
    """override_scope stellt den vorherigen Override-Stand wieder her (kein Cross-
    Kommune-Leak, §8/B2)."""
    override_context.set_overrides({"impact.k_indirect": 0.9})
    with override_context.override_scope({"impact.k_indirect": 0.1}):
        assert override_context.get_override("impact.k_indirect") == 0.1
    assert override_context.get_override("impact.k_indirect") == 0.9
    override_context.set_overrides({})


def test_folgekosten_reconsolidated_from_reduced_direct():
    """Nach Reduktion der direkten Sektorschäden werden indirekt/Restaurierung neu aus
    der NEUEN Direktsumme gebildet (§8/B3), nicht auf dem Vor-Maßnahmen-Stand belassen."""
    override_context.set_overrides({})
    direct_codes = sorted(catalog.DIRECT_SECTOR_RISK_CODES)[:2]
    risks = {c: {"index": 25.0, "outcome": 500.0, "cost_eur": 500.0} for c in direct_codes}
    risks["EXPECTED_INDIRECT_ECONOMIC_LOSS_EUR"] = {"index": 0.0, "outcome": 9999.0, "cost_eur": 9999.0}
    risks["EXPECTED_RESTORATION_COSTS_EUR"] = {"index": 0.0, "outcome": 8888.0, "cost_eur": 8888.0}

    measure_service._reconsolidate_cell_folgekosten(risks)

    direct_new = 500.0 * len(direct_codes)
    assert risks["EXPECTED_INDIRECT_ECONOMIC_LOSS_EUR"]["outcome"] == pytest.approx(
        measure_service._K_INDIRECT_DEFAULT * direct_new)
    assert risks["EXPECTED_RESTORATION_COSTS_EUR"]["outcome"] == pytest.approx(
        measure_service._RESTORATION_SHARE_DEFAULT * direct_new)


def test_measure_benefit_includes_folgekosten_reconciles():
    """Einzelmaßnahmen-Nutzen (direkte Reduktion × (1+k)) == Aggregat-Delta aus direkten
    Schäden + rekonsolidierten Folgekosten (§8/B3)."""
    override_context.set_overrides({})
    direct = "EXPECTED_TELECOM_DAMAGE_EUR"   # monetär, pop-skaliert, direkter Sektor
    rdirect = catalog.RISKS_BY_CODE[direct]
    IND = "EXPECTED_INDIRECT_ECONOMIC_LOSS_EUR"
    k = measure_service._K_INDIRECT_DEFAULT
    factor = 0.5

    def cell(dmg: float) -> dict:
        return {"inputs": {"pop": 1000.0},
                "risks": {direct: {"index": 40.0, "outcome": dmg, "cost_eur": dmg},
                          IND: {"index": 0.0, "outcome": k * dmg, "cost_eur": k * dmg}}}

    cells = [cell(1000.0), cell(2000.0), cell(3000.0)]
    covered = {0, 2}
    base = risk_engine.aggregate(copy.deepcopy(cells), 3000.0, 10.0)

    with_cells = []
    for i, c in enumerate(cells):
        nc = copy.deepcopy(c)
        if i in covered:
            r = nc["risks"][direct]
            r["outcome"] *= factor
            r["cost_eur"] *= factor
            measure_service._reconsolidate_cell_folgekosten(nc["risks"])
        with_cells.append(nc)
    withm = risk_engine.aggregate(with_cells, 3000.0, 10.0)

    delta_total = base["cost"]["total_eur"] - withm["cost"]["total_eur"]
    benefit = sum(
        measure_service._cell_cost(rdirect, cells[i]["risks"][direct], 1000.0)
        * (1.0 - factor) * (1.0 + k) for i in covered)
    assert benefit == pytest.approx(delta_total, abs=0.01)


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
