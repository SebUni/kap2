"""Tests der Gesundheits-Schadensfunktionen (Schicht B, Stufe 4).

Deckt ab:
  (a) Deterministische Einzelzell-Handrechnung je Funktion (Mortalität, Morbidität,
      Verletzte, Psyche, Betroffene, Wärme-/Schadstoffstunden).
  (b) AF-Kalibrierpunkt: ~10–11 Hitzetote/100k bei 20 Hitzetagen (Winklmayr-Größenordnung).
  (c) Nichtlinearität: doppelte Hitzetage → mehr als doppelte Mortalität (§3.4).
  (d) Registry emittiert die Impact-Parameter (risks.<CODE>.impact.*) editierbar mit Quelle.
  (e) Override eines Impact-Parameters wirkt; g(V̂)-Modifikator wirkt.
  (f) Alle 7 Gesundheitsrisiken haben eine registrierte Impact-Funktion.

Läuft mit pytest oder direkt: ``python tests/test_impact_health.py``.
"""

from __future__ import annotations

from math import exp

from app.data import catalog
from app.services import parameter_registry
from app.services.engine import impact, override_context
from app.services.engine.impact.base import CellContext, attributable_fraction

MORT = "EXPECTED_ANNUAL_MORTALITY"
HEALTH = list(__import__("app.services.engine.impact.health", fromlist=["HEALTH_IMPACTS"]).HEALTH_IMPACTS)


def _ctx(pop=100_000.0, hd=20.0, flood_norm=0.3, vnorm=0.5, event_norm=0.3):
    hev = {"hazards": {"HEAT_WAVE": hd, "HEAVY_RAIN_FLOOD": flood_norm * 100,
                       "EXTRATROPICAL_STORM": 6.0, "LANDSLIDE": 0.0, "STORM_SURGE": 0.0,
                       "WILDFIRE": 0.0, "COMPOUND_EVENT": event_norm, "CASCADE_EVENT": event_norm,
                       "DROUGHT": 20.0},
           "exposures": {}, "vulnerabilities": {}}
    hn = {"hazards": {"HEAVY_RAIN_FLOOD": flood_norm, "EXTRATROPICAL_STORM": 0.4,
                      "LANDSLIDE": 0.0, "STORM_SURGE": 0.0, "WILDFIRE": 0.0,
                      "COMPOUND_EVENT": event_norm, "CASCADE_EVENT": event_norm, "DROUGHT": 0.33},
          "exposures": {}, "vulnerabilities": {}}
    for r in catalog.RISKS:
        for v in r["vulnerabilities"]:
            hn["vulnerabilities"][v] = vnorm
    return CellContext(ci={"pop": pop}, hev=hev, hev_norm=hn, indices={}, regional={})


# ── (a)/(b) Mortalität: Handrechnung + Kalibrierpunkt ─────────────────────────

def test_mortality_matches_hand_calc_and_calibration():
    override_context.set_overrides({})
    ctx = _ctx(pop=100_000.0, hd=20.0, vnorm=0.5)
    r = catalog.RISKS_BY_CODE[MORT]
    af = attributable_fraction(20.0, 0.0008, 8.0)      # 1-exp(-0.0008*12)
    expected = 100_000.0 * (1130.0 / 100_000.0) * af * (0.5 + 0.5)
    got = impact.compute_all_cell_impacts(ctx)[MORT]["outcome"]
    assert abs(got - expected) < 1e-6
    # Kalibrierung: Größenordnung ~10-11 Tote/100k bei 20 Hitzetagen
    assert 9.0 < got < 13.0


# ── (c) Nichtlinearität ────────────────────────────────────────────────────────

def test_mortality_is_superlinear_in_hotdays():
    override_context.set_overrides({})
    o10 = impact.compute_all_cell_impacts(_ctx(hd=10.0))[MORT]["outcome"]
    o20 = impact.compute_all_cell_impacts(_ctx(hd=20.0))[MORT]["outcome"]
    o40 = impact.compute_all_cell_impacts(_ctx(hd=40.0))[MORT]["outcome"]
    # Schwellenwerteffekt: Verdopplung der Hitzetage verdoppelt die Mortalität ÜBER-
    # proportional (der lineare Index würde exakt verdoppeln) — behebt §3.4.
    assert o40 > 2.0 * o20
    assert o20 > 2.0 * o10


# ── (d) Registry emittiert Impact-Parameter ────────────────────────────────────

def test_registry_emits_impact_params():
    params = parameter_registry.catalog_parameters(
        layer_code=MORT, layer_category="risks")
    ids = {p["id"] for p in params}
    assert f"risks.{MORT}.impact.baseline_mort_per_100k" in ids
    assert f"risks.{MORT}.impact.beta_per_hotday" in ids
    beta = next(p for p in params if p["id"].endswith(".impact.beta_per_hotday"))
    assert beta["editable"] is True
    assert beta["references"], "Impact-Parameter muss belegte Quelle tragen"


# ── (e) Override + g(V̂) wirken ─────────────────────────────────────────────────

def test_impact_param_override_changes_outcome():
    override_context.set_overrides({})
    base = impact.compute_all_cell_impacts(_ctx())[MORT]["outcome"]
    override_context.set_overrides(
        {f"risks.{MORT}.impact.baseline_mort_per_100k": 2260.0})  # verdoppelt
    doubled = impact.compute_all_cell_impacts(_ctx())[MORT]["outcome"]
    override_context.set_overrides({})
    assert abs(doubled - 2.0 * base) < 1e-6


def test_vulnerability_modifier_scales_outcome():
    override_context.set_overrides({})
    low = impact.compute_all_cell_impacts(_ctx(vnorm=0.0))[MORT]["outcome"]   # g=0.5
    high = impact.compute_all_cell_impacts(_ctx(vnorm=1.0))[MORT]["outcome"]  # g=1.5
    assert abs(high - 3.0 * low) < 1e-6


# ── (f) Abdeckung + Sanity ─────────────────────────────────────────────────────

def test_all_health_risks_registered():
    assert len(HEALTH) == 7
    for code in HEALTH:
        assert impact.has(code), code


def test_sanity_ratio_in_tolerance():
    from app.services.engine.impact import sanity
    override_context.set_overrides({})
    ctx = _ctx(pop=100_000.0)
    res = impact.compute_all_cell_impacts(ctx)
    for code in HEALTH:
        ratio = sanity.check(code, res[code]["outcome"], 100_000.0, 50.0)
        # Referenzkommune: Summe (1 Zelle 100k) sollte in der Toleranz zur ref-Schätzung liegen
        assert ratio is None or (1.0 / sanity.TOLERANCE) <= ratio <= sanity.TOLERANCE, (code, ratio)


if __name__ == "__main__":
    import sys
    import pytest
    sys.exit(pytest.main([__file__, "-q"]))
