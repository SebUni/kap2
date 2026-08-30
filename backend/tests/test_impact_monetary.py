"""Tests der monetären Schadensfunktionen + k_indirekt-Konsolidierung (Schicht B §6.2).

Deckt ab:
  (a) Sektorschaden skaliert mit Assetwert × Verlustrate × konvexer Schadenskurve × g(V̂).
  (b) Konvexität der Schadenskurve (doppelte Intensität → mehr als doppelter Schaden).
  (c) k_indirekt-Konsolidierung: INDIRECT = k·Σdirekt; SUPPLY/LOCATION/DELAYED = 0;
      RESTORATION = quote·Σdirekt und ist NICHT-additiv (nicht in total_eur).
  (d) Override von k_indirekt / Assetwert wirkt.
  (e) Registry emittiert globale (impact.*) und per-Risiko-Impact-Parameter.
  (f) aggregate: total_eur schließt die nicht-additive Restaurierung aus.

Läuft mit pytest oder direkt: ``python tests/test_impact_monetary.py``.
"""

from __future__ import annotations

import pytest

from app.data import catalog, catalog_parked
from app.services import parameter_registry
from app.services.engine import impact, override_context, risk_engine
from app.services.engine.impact.base import CellContext
from app.services.engine.impact.curves import damage_fraction

BUILD = "EXPECTED_BUILDING_DAMAGE_EUR"

# M0-Verschlankung (docs/ROADMAP.md §5): Die monetären Sektor-/Folgekosten-Risiken
# sind geparkt; ihre Schadensfunktionen bleiben in der Registry (bewusst
# unangetastet) und werden hier mit den geparkten Risiko-Dicts direkt aufgerufen —
# compute_all_cell_impacts dispatcht nur über catalog.RISKS.
_PARKED_BY_CODE = {r["code"]: r for r in catalog_parked._PARKED_RISKS}


def _risk(code: str) -> dict:
    return catalog.RISKS_BY_CODE.get(code) or _PARKED_BY_CODE[code]


def _compute(code: str, ctx: CellContext) -> dict:
    return impact.IMPACT_FUNCTIONS[code](_risk(code), ctx)


def _all_impacts(ctx: CellContext) -> dict[str, dict]:
    """Wie ``compute_all_cell_impacts`` für den Sektor-/Folgekosten-Ausschnitt,
    aber über die geparkten Definitionen (Registry-Direktaufruf + Konsolidierung)."""
    from app.services.engine.impact.monetary import consolidate_indirect

    codes = (set(catalog.DIRECT_SECTOR_RISK_CODES)
             | set(catalog.CONSOLIDATED_INTO_INDIRECT_CODES)
             | {"EXPECTED_INDIRECT_ECONOMIC_LOSS_EUR", "EXPECTED_RESTORATION_COSTS_EUR"})
    out: dict[str, dict] = {}
    for code in sorted(codes):
        fn = impact.IMPACT_FUNCTIONS.get(code)
        out[code] = fn(_risk(code), ctx) if fn else {"outcome": 0.0, "cost_eur": 0.0}
    consolidate_indirect(out, ctx)
    return out


def _abs(code: str, frac: float) -> float:
    """Absoluter Hazard-Wert, der über die Katalog-Referenzgrenzen auf ``frac`` normiert
    (Schicht B liest die absolute Intensität via ``haz_intensity``, §3.3-Entkopplung)."""
    m = catalog.INDICATOR_BY_CODE.get(code, {})
    lo = float(m.get("norm_min", 0.0))
    hi = float(m.get("norm_max", 1.0))
    return lo + frac * (hi - lo)


def _ctx(pop=250.0, flood=0.4, vnorm=0.5, bldg_cov=0.2, avg_height=7.0):
    hn = {"hazards": {"HEAVY_RAIN_FLOOD": flood, "EXTRATROPICAL_STORM": 0.3, "HEAT_WAVE": 0.3,
                      "DROUGHT": 0.3, "SEA_LEVEL_RISE": 0.0, "SURFACE_WATER_HEATING": 0.3,
                      "LOW_FLOW_NIEDRIGWASSER": 0.3, "SOIL_SALINIZATION": 0.0},
          "exposures": {}, "vulnerabilities": {}}
    hev = {"hazards": {c: _abs(c, f) for c, f in hn["hazards"].items()},
           "exposures": {}, "vulnerabilities": {}}
    for r in catalog.RISKS:
        for v in r["vulnerabilities"]:
            hn["vulnerabilities"][v] = vnorm
    ci = {"pop": pop, "bldg_cov": bldg_cov, "avg_height": avg_height, "area_m2": 10000,
          "transport_hub_count": 8.0, "energy_infra_count": 4.0, "communication_count": 2.0,
          "water_wastewater_count": 10.0,
          "transport_hub_classes": {"railway_station": 1},
          "energy_infra_classes": {"substation_distribution": 1},
          "communication_classes": {"mast": 1},
          "water_wastewater_classes": {"wastewater_plant": 1},
          "farmland_frac": 0.3, "forest_frac": 0.2,
          "green_frac": 0.2, "water_frac": 0.1}
    return CellContext(ci=ci, hev=hev, hev_norm=hn, indices={}, regional={})


# ── (a) Assetwert-Skalierung ────────────────────────────────────────────────────

def test_building_damage_scales_with_asset():
    override_context.set_overrides({})
    low = _compute(BUILD, _ctx(bldg_cov=0.1))["cost_eur"]
    high = _compute(BUILD, _ctx(bldg_cov=0.2))["cost_eur"]
    assert abs(high - 2.0 * low) < 1e-6   # doppelte Bebauung → doppelter Assetwert → doppelt


# ── §3.3-Entkopplung: Schadensfunktion ignoriert Screening-Norm-Overrides ──────

def test_haz_intensity_ignores_screening_norm_override():
    """haz_intensity nutzt FIXE Katalog-Referenzgrenzen; ein Screening-Norm-Override
    ändert nur die Index-Normierung (normalize_value), nicht die absolute Intensität —
    damit verschiebt ein Norm-Edit nicht mehr die absoluten Schäden (§3.3/§8).

    M0: geprüft am aktiven Hazard HEAT_WAVE (Grenzen 0..40) — normalize_value liefert
    für geparkte Hazards ohne Katalogeintrag konstant 0 und wäre kein Prüfstein mehr."""
    ctx = _ctx()   # HEAT_WAVE normiert 0,3 → absolut 12 Hitzetage (Grenzen 0..40)
    override_context.set_overrides({})
    base_int = ctx.haz_intensity("HEAT_WAVE")
    base_norm = override_context.normalize_value("HEAT_WAVE", ctx.haz("HEAT_WAVE"))
    override_context.set_overrides({"hazards.HEAT_WAVE.norm_max": 20.0})
    assert ctx.haz_intensity("HEAT_WAVE") == base_int                  # fixe Grenzen: unverändert
    assert override_context.normalize_value(
        "HEAT_WAVE", ctx.haz("HEAT_WAVE")) != base_norm                # Screening ändert sich
    override_context.set_overrides({})


# ── (b) Konvexe Schadenskurve ───────────────────────────────────────────────────

def test_damage_curve_is_convex():
    assert damage_fraction(0.5) < 0.5           # exponent 1.5 → unter der Diagonalen
    # Flut klar über dem Sturm/Hitze-Boden (0,3), damit sie den max()-Treiber stellt.
    o04 = _compute(BUILD, _ctx(flood=0.4))["cost_eur"]
    o08 = _compute(BUILD, _ctx(flood=0.8))["cost_eur"]
    assert o08 > 2.0 * o04                       # doppelte Intensität → mehr als doppelt


# ── (c) k_indirekt-Konsolidierung ───────────────────────────────────────────────

def test_indirect_consolidation():
    override_context.set_overrides({})
    res = _all_impacts(_ctx())
    direct = sum(res[c]["cost_eur"] for c in catalog.DIRECT_SECTOR_RISK_CODES)
    assert direct > 0.0
    assert abs(res["EXPECTED_INDIRECT_ECONOMIC_LOSS_EUR"]["cost_eur"] - 0.25 * direct) < 1e-6
    assert abs(res["EXPECTED_RESTORATION_COSTS_EUR"]["cost_eur"] - 0.15 * direct) < 1e-6
    for code in catalog.CONSOLIDATED_INTO_INDIRECT_CODES:
        assert res[code]["cost_eur"] == 0.0
    # Restaurierung ist nicht-additiv (geparkte Definition, reine Dict-Prüfung)
    assert not catalog.risk_contributes_to_total(_risk("EXPECTED_RESTORATION_COSTS_EUR"))


# ── (d) Override wirkt ──────────────────────────────────────────────────────────

def test_k_indirect_override():
    override_context.set_overrides({})
    base = _all_impacts(_ctx())
    direct = sum(base[c]["cost_eur"] for c in catalog.DIRECT_SECTOR_RISK_CODES)
    override_context.set_overrides({"impact.k_indirect": 0.5})
    res = _all_impacts(_ctx())
    override_context.set_overrides({})
    assert abs(res["EXPECTED_INDIRECT_ECONOMIC_LOSS_EUR"]["cost_eur"] - 0.5 * direct) < 1e-6


def test_asset_value_override():
    override_context.set_overrides({})
    base = _compute(BUILD, _ctx())["cost_eur"]
    override_context.set_overrides({"impact.building_value_eur_m2": 4000.0})
    doubled = _compute(BUILD, _ctx())["cost_eur"]
    override_context.set_overrides({})
    assert abs(doubled - 2.0 * base) < 1e-6


# ── (e) Registry-Emission ───────────────────────────────────────────────────────

def test_registry_emits_global_and_per_risk_impact_params():
    params = parameter_registry.catalog_parameters()
    ids = {p["id"] for p in params}
    assert "impact.k_indirect" in ids
    assert "impact.building_value_eur_m2" in ids
    # M0: per-Risiko-Impact-Parameter werden nur für AKTIVE Risiken emittiert —
    # geprüft am aktiven Hitzerisiko statt am geparkten Gebäudeschaden.
    assert "risks.EXPECTED_ANNUAL_MORTALITY.impact.calibration" in ids
    assert f"risks.{BUILD}.impact.max_loss_rate" not in ids  # geparkt ⇒ nicht emittiert
    k = next(p for p in params if p["id"] == "impact.k_indirect")
    assert k["editable"] is True and k["references"]


# ── (f) total_eur schließt Restaurierung aus ────────────────────────────────────

@pytest.mark.skip(reason="M0-Verschlankung: Restaurierungs-/Sektorschadens-Risiken "
                         "geparkt, aggregate braucht aktive Katalog-Mitgliedschaft; "
                         "kehrt mit Stage 1–4 zurück (docs/ROADMAP.md §5)")
def test_total_excludes_non_additive_restoration():
    override_context.set_overrides({})
    # Zwei Zellen mit materialisierten Schicht-B-Kosten
    def cell():
        ctx = _ctx()
        imps = impact.compute_all_cell_impacts(ctx)
        risks = {}
        for code, v in imps.items():
            e = {"index": 40.0}
            if round(v["outcome"], 4):
                e["outcome"] = round(v["outcome"], 4)
            if round(v["cost_eur"], 2):
                e["cost_eur"] = round(v["cost_eur"], 2)
            risks[code] = e
        return {"risks": risks, "inputs": {"pop": 250.0}}

    agg = risk_engine.aggregate([cell(), cell()], total_pop=500.0, area_km2=2.0)
    rest = agg["risks"]["EXPECTED_RESTORATION_COSTS_EUR"]["cost_eur"]
    assert rest > 0.0
    total = agg["cost"]["total_eur"]
    summed_all = sum(r["cost_eur"] for r in agg["risks"].values())
    assert abs((summed_all - rest) - total) < 0.01   # total = alles außer Restaurierung


if __name__ == "__main__":
    import sys
    import pytest
    sys.exit(pytest.main([__file__, "-q"]))
