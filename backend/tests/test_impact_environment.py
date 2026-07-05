"""Tests der Umwelt-Schadensfunktionen (Schicht B §6.4) + Gesamt-Abdeckung.

Deckt ab:
  (a) Flächen- und Intensitätsskalierung (Fläche · Rate · Driver · g(V̂)).
  (b) Monetarisierung über den Kostensatz (€/ha bzw. €/Art).
  (c) area-Aggregation: die Umweltrisiken summieren über Zellen (aggregation="sum").
  (d) Vollständigkeit: JEDES nicht reine Index-Risiko hat jetzt eine Impact-Funktion.
  (e) Reine Index-Risiken bleiben ohne Funktion (Screening, 0 €).

Läuft mit pytest oder direkt: ``python tests/test_impact_environment.py``.
"""

from __future__ import annotations

from app.data import catalog
from app.services.engine import impact, override_context, risk_engine
from app.services.engine.impact.base import CellContext

HABITAT = "EXPECTED_HABITAT_LOSS"


def _abs(code: str, frac: float) -> float:
    """Absoluter Hazard-Wert, der über die Katalog-Referenzgrenzen auf ``frac`` normiert
    (Schicht B liest seit §8/B6-Umfeld die absolute Intensität via ``haz_intensity``)."""
    m = catalog.INDICATOR_BY_CODE.get(code, {})
    lo = float(m.get("norm_min", 0.0))
    hi = float(m.get("norm_max", 1.0))
    return lo + frac * (hi - lo)


def _ctx(forest=0.2, drought=0.4, vnorm=0.5):
    hn = {"hazards": {"DROUGHT": drought, "WILDFIRE": 0.2, "SEA_LEVEL_RISE": 0.0,
                      "MEAN_TEMPERATURE_RISE": 0.3, "HEAT_WAVE": 0.3, "HEAVY_RAIN_FLOOD": 0.3,
                      "SOIL_SALINIZATION": 0.0},
          "exposures": {}, "vulnerabilities": {}}
    hev = {"hazards": {c: _abs(c, f) for c, f in hn["hazards"].items()},
           "exposures": {}, "vulnerabilities": {}}
    for r in catalog.RISKS:
        for v in r["vulnerabilities"]:
            hn["vulnerabilities"][v] = vnorm
    ci = {"forest_frac": forest, "green_frac": 0.1, "water_frac": 0.05, "farmland_frac": 0.3}
    return CellContext(ci=ci, hev=hev, hev_norm=hn, indices={}, regional={})


def test_habitat_loss_scales_with_area():
    override_context.set_overrides({})
    low = impact.compute_all_cell_impacts(_ctx(forest=0.1))[HABITAT]["outcome"]
    high = impact.compute_all_cell_impacts(_ctx(forest=0.3))[HABITAT]["outcome"]
    assert high > low > 0.0


def test_habitat_loss_scales_with_intensity():
    override_context.set_overrides({})
    lo = impact.compute_all_cell_impacts(_ctx(drought=0.2))[HABITAT]["outcome"]
    hi = impact.compute_all_cell_impacts(_ctx(drought=0.8))[HABITAT]["outcome"]
    assert abs(hi - 4.0 * lo) < 1e-6   # linearer Driver: 0.8/0.2 = 4


def test_environment_is_monetized_via_cost_rate():
    override_context.set_overrides({})
    r = catalog.RISKS_BY_CODE[HABITAT]
    res = impact.compute_all_cell_impacts(_ctx())[HABITAT]
    rate = catalog.risk_default_cost_per_outcome(r)   # €/ha
    assert abs(res["cost_eur"] - res["outcome"] * rate) < 1e-6
    assert res["cost_eur"] > 0.0


def test_environment_risks_sum_over_cells():
    override_context.set_overrides({})
    def cell():
        imps = impact.compute_all_cell_impacts(_ctx())
        risks = {}
        for code, v in imps.items():
            e = {"index": 40.0}
            if round(v["outcome"], 4):
                e["outcome"] = round(v["outcome"], 4)
            if round(v["cost_eur"], 2):
                e["cost_eur"] = round(v["cost_eur"], 2)
            risks[code] = e
        return {"risks": risks, "inputs": {"pop": 100.0}}
    agg = risk_engine.aggregate([cell(), cell()], total_pop=200.0, area_km2=2.0)
    assert agg["risks"][HABITAT]["aggregation"] == "sum"
    # zwei identische Zellen → Summe ist doppelter Einzelwert
    single = impact.compute_all_cell_impacts(_ctx())[HABITAT]["outcome"]
    assert abs(agg["risks"][HABITAT]["outcome"] - 2.0 * round(single, 4)) < 0.01


# ── Gesamt-Abdeckung nach Stufe 5a ──────────────────────────────────────────────

def test_impact_coverage_matches_design():
    """Genau die Schadensrisiken haben eine Funktion; Folgekosten/operative/Index nicht.

    - Schadensfunktion: Gesundheit + direkte Sektorschäden + Migration + Umwelt.
    - Konsolidiert (keine Funktion): indirekte/Restaurierungs-Folgekosten (§3.7).
    - Legacy-P90 (keine Funktion): flat operative Ausfallstunden (§6.3, VoLL explizit).
    - Screening (keine Funktion): reine Index-Risiken.
    """
    from app.services.engine.impact.health import HEALTH_IMPACTS
    from app.services.engine.impact.monetary import MONETARY_IMPACTS
    from app.services.engine.impact.environment import ENVIRONMENT_IMPACTS
    expected = set(HEALTH_IMPACTS) | set(MONETARY_IMPACTS) | set(ENVIRONMENT_IMPACTS)

    for code in expected:
        assert impact.has(code), f"erwartete Funktion fehlt: {code}"

    # INDIRECT ist das Ziel der k_indirekt-Konsolidierung (per k·Σ gesetzt, keine Funktion).
    consolidated = (catalog.CONSOLIDATED_INTO_INDIRECT_CODES | catalog.NON_ADDITIVE_RISK_CODES
                    | {"EXPECTED_INDIRECT_ECONOMIC_LOSS_EUR"})
    operational_flat = {r["code"] for r in catalog.RISKS
                        if r["cost_dimension"] == "operational"
                        and r["code"] not in catalog.INDEX_ONLY_RISK_CODES}
    for code in consolidated | operational_flat | catalog.INDEX_ONLY_RISK_CODES:
        assert not impact.has(code), f"unerwartete Funktion: {code}"

    # Jedes Risiko ist genau in einer der vier Kategorien abgedeckt.
    covered = expected | consolidated | operational_flat | catalog.INDEX_ONLY_RISK_CODES
    all_codes = {r["code"] for r in catalog.RISKS}
    assert covered == all_codes, f"nicht zugeordnet: {all_codes - covered}"


if __name__ == "__main__":
    import sys
    import pytest
    sys.exit(pytest.main([__file__, "-q"]))
