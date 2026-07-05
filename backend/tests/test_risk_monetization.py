"""Tests zur Monetarisierung der Risiken (Prompt 3).

Deckt ab:
  (a) Die Registry emittiert für JEDES nicht-monetäre Risiko einen
      Kostensatz-Parameter ``risks.<CODE>.cost_per_outcome``.
  (b) ``total_eur`` == Summe der Einzel-``cost_eur`` (ohne ausgenommene Risiken).
  (c) Der Parameter-Excel-Export enthält die neuen Kostensatz-Parameter.
  (d) Ein Override des Kostensatzes wirkt auf ``cost_eur``.

Läuft mit pytest oder direkt: ``python tests/test_risk_monetization.py``.
"""

from __future__ import annotations

from app.data import catalog
from app.services import parameter_registry
from app.services.engine import override_context, risk_engine


# ── (a) Registry emittiert Kostensatz je nicht-monetärem Risiko ────────────────

def test_registry_emits_cost_rate_for_every_non_monetary_risk():
    params = parameter_registry.catalog_parameters(layer_category="risks")
    cost_ids = {p["id"] for p in params if p["id"].endswith(".cost_per_outcome")}
    for r in catalog.RISKS:
        if catalog.risk_is_monetary(r):
            # Monetäre Risiken bekommen KEINEN Kostensatz (ref_value ist bereits €).
            assert f"risks.{r['code']}.cost_per_outcome" not in cost_ids
        else:
            assert f"risks.{r['code']}.cost_per_outcome" in cost_ids, r["code"]


def test_cost_rate_param_metadata():
    params = parameter_registry.catalog_parameters(
        layer_code="EXPECTED_ANNUAL_MORTALITY", layer_category="risks")
    cp = next(p for p in params if p["id"].endswith(".cost_per_outcome"))
    assert cp["unit"].startswith("€ je")
    assert cp["editable"] is True
    assert cp["value"] > 0.0


# ── (b) Gesamtschaden == Summe der Einzel-cost_eur ─────────────────────────────

def _synthetic_cells(n: int = 40, index: float = 50.0) -> list[dict]:
    cells = []
    for _ in range(n):
        risks = {r["code"]: {"index": index} for r in catalog.RISKS}
        cells.append({"risks": risks, "inputs": {"pop": 2500.0}})
    return cells


def test_total_eur_equals_sum_of_cost_eur():
    override_context.set_overrides({})
    agg = risk_engine.aggregate(_synthetic_cells(), total_pop=100000.0, area_km2=50.0)
    total = agg["cost"]["total_eur"]
    summed = round(sum(r["cost_eur"] for r in agg["risks"].values()), 2)
    assert abs(total - summed) < 0.01


def test_index_only_risks_are_excluded_from_total():
    override_context.set_overrides({})
    agg = risk_engine.aggregate(_synthetic_cells(), total_pop=100000.0, area_km2=50.0)
    for code in catalog.INDEX_ONLY_RISK_CODES:
        assert agg["risks"][code]["cost_eur"] == 0.0


# ── (c) Excel-Export enthält die Kostensatz-Parameter ──────────────────────────

def test_excel_export_contains_cost_rate_params():
    # Excel-Export nutzt catalog_parameters + merge_overrides; wir prüfen die
    # Parameterliste (kein DB-Zugriff nötig) auf Kostensatz-Einträge.
    params = parameter_registry.catalog_parameters()
    labels = {p["label"] for p in params if p["id"].endswith(".cost_per_outcome")}
    assert "Kostensatz (Monetarisierung)" in labels
    n_cost = sum(1 for p in params if p["id"].endswith(".cost_per_outcome"))
    n_non_monetary = sum(1 for r in catalog.RISKS if not catalog.risk_is_monetary(r))
    assert n_cost == n_non_monetary


# ── (d) Override eines Kostensatzes wirkt auf cost_eur ─────────────────────────

def test_cost_rate_override_changes_cost():
    mort = catalog.RISKS_BY_CODE["EXPECTED_ANNUAL_MORTALITY"]
    override_context.set_overrides({})
    base = risk_engine.estimate_outcome_and_cost(mort, 50.0, 100000.0, 10.0)
    override_context.set_overrides(
        {"risks.EXPECTED_ANNUAL_MORTALITY.cost_per_outcome": 1_000_000.0})
    changed = risk_engine.estimate_outcome_and_cost(mort, 50.0, 100000.0, 10.0)
    override_context.set_overrides({})
    assert changed["outcome"] == base["outcome"]
    assert changed["cost_eur"] != base["cost_eur"]
    assert abs(changed["cost_eur"] - changed["outcome"] * 1_000_000.0) < 0.01


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"ok: {name}")
