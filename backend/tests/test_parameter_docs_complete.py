"""Vollständigkeits-Ratchet der Parameter-Dokumentation (Konfiguration-Infokästen).

Ziel (Nutzeranforderung): KEIN genutzter Parameter ohne Infokasten. Der Infokasten
erscheint im Frontend nur, wenn ``source_detail`` (Herleitung) ODER ``references``
(IEEE-Quellen) gefüllt sind (ParameterTable.tsx). Dieser Test friert den Rest-Bestand
undokumentierter Parameter als **Ratchet** ein:

- kein Parameter außerhalb von ``KNOWN_MISSING`` darf undokumentiert sein
  (Regressionen und undokumentierte NEUE Parameter schlagen sofort fehl),
- jeder Eintrag in ``KNOWN_MISSING`` muss noch undokumentiert sein
  (jede Doku-Batch MUSS die Liste hier mitschrumpfen — bis sie leer ist).

Zusätzlich abgesichert: die entfernten toten Parameter (Pfadgewichte + fest
verdrahtete Formel-Konstanten) bleiben draußen, die lebenden Formel-Parameter und
die neuen model/regional/uhi/impact-Stellschrauben sind vorhanden, dokumentiert
und tatsächlich verdrahtet (Override ändert die Rechnung).

Aufruf als Skript listet die offenen IDs (Futter für den Fortsetzungs-Prompt):
    python tests/test_parameter_docs_complete.py --list
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services import parameter_registry  # noqa: E402
from app.services.engine import override_context, tunables  # noqa: E402


# ── Ratchet-Bestand: LEER — alle anwendbaren Parameter dokumentiert ─────────────
KNOWN_MISSING: set[str] = set()

# Von der Registry-Emission ausgeschlossene tote Parameter (Override wirkungslos).
_REMOVED_DEAD_IDS = {
    "hazards.OCEAN_WARMING.param.__const",
    "hazards.OCEAN_ACIDIFICATION.param.__const",
    "hazards.GLACIER_SNOW_LOSS.param.glacier_loss_rate",
    "hazards.PERMAFROST_THAW.param.__const",
    "hazards.HEAT_WAVE.param.uhi_weight",
    "hazards.TROPICAL_CYCLONE.param.__const",
    "hazards.STORM_SURGE.param.__const",
    "hazards.SALTWATER_INTRUSION.param.__const",
    "hazards.COASTAL_EROSION.param.__const",
    "hazards.SOIL_SALINIZATION.param.__const",
    "hazards.CASCADE_EVENT.param.__const",
    "vulnerabilities.CRITICAL_INFRA_CONDITION.param.__const",
    "vulnerabilities.SUPPLY_CHAIN_DEPENDENCY.param.__const",
    "vulnerabilities.REDUNDANCY_BACKUP.param.__const",
    "vulnerabilities.INFRA_DEPENDENCY_CHAIN.param.__const",
    "vulnerabilities.SALTWATER_INTRUSION_RISK.param.__const",
    "vulnerabilities.AQUACULTURE_TECHNICAL_VULNERABILITY.param.__const",
    "vulnerabilities.FISHERIES_MANAGEMENT_CAPACITY.param.__const",
}

from app.data import infra_assets  # noqa: E402

# Lebende Formel-Parameter (indicators.py liest sie per get_override).
_LIVE_FORMULA_IDS = {
    "vulnerabilities.INFRA_CRITICALITY.param.w_energy",
    "vulnerabilities.INFRA_CRITICALITY.param.w_water",
    "vulnerabilities.INFRA_CRITICALITY.param.w_comm",
    "vulnerabilities.INFRA_CRITICALITY.param.w_health",
    "vulnerabilities.INFRA_CRITICALITY.param.w_transport",
    "vulnerabilities.EMERGENCY_MANAGEMENT.param.__const",
    "vulnerabilities.EARLY_WARNING_SYSTEMS.param.__const",
    "vulnerabilities.LEVEE_CONDITION.param.__const",
    "vulnerabilities.FINANCIAL_ADAPTATION_CAPACITY.param.__const",
    "vulnerabilities.PLANNING_IMPLEMENTATION_CAPACITY.param.__const",
}
# KRITIS-Klassengewichte der vier Infrastruktur-Layer (resolve_weights liest sie
# per get_override über "exposures.<CODE>.param.w_<cls>"; generiert aus der
# Taxonomie, damit der Ratchet automatisch jede neue Anlagenklasse erfasst).
# M0-Verschlankung: Die Infrastruktur-Expositionen sind geparkt; die Registry
# emittiert die Gewichte über den formulas.DETAILED-Kategorie-Fallback derzeit
# unter "vulnerabilities.<CODE>.param.w_<cls>" (parameter_registry.py, Zeile
# ~159: cat-Fallback für Codes außerhalb des aktiven Katalogs). Der Ratchet
# prüft deshalb kategorie-unabhängig je (Layer-Code, w_<cls>) auf Emission +
# Doku. ACHTUNG: Die Divergenz Emission (vulnerabilities.*) ⇄ Lesepfad
# (exposures.*, infra_assets.resolve_weights) ist als Befund gemeldet.
_LIVE_FORMULA_KEYS_BY_LAYER = {
    (infra_assets.SECTOR_EXPOSURE[sector], f"w_{cls}")
    for sector, classes in infra_assets.ASSET_CLASSES.items()
    for cls in classes
}

# Neue Stellschrauben aus Phase A (müssen vorhanden UND dokumentiert sein).
# M0-Verschlankung: "risks.EXPECTED_ANNUAL_MENTAL_HEALTH.impact.event_share"
# entfernt — das Risiko ist geparkt und per-Risiko-Impact-Parameter werden nur
# für aktive Risiken emittiert; kehrt mit Stage 1–4 zurück (docs/ROADMAP.md §5).
_NEW_PARAM_IDS = {
    "uhi.epsilon", "uhi.tree_cooling",
    "impact.floor_height_m",
    "model.ref_population", "model.ref_area_km2", "model.risk_threshold",
    "model.measure_coverage_saturation", "model.measure_reduction_cap",
    "regional.storm_days", "regional.sea_level_rise", "regional.glacier_loss_rate",
    "regional.heavy_rain_base", "regional.heavy_rain_slope", "regional.mean_temp_rise_base",
    "regional.dry_index_divisor", "regional.drought_base", "regional.drought_factor",
    "regional.share_over_65", "regional.share_under_18",
}


def _params() -> list[dict]:
    return parameter_registry.catalog_parameters()


def _undocumented() -> set[str]:
    return {
        p["id"] for p in _params()
        if p.get("applicable") is not False
        and not p.get("source_detail")
        and not p.get("references")
    }


# ── Ratchet ─────────────────────────────────────────────────────────────────────

def test_docs_ratchet_no_new_undocumented():
    """Kein anwendbarer Parameter außerhalb der bekannten Restliste ohne Infokasten."""
    extra = _undocumented() - KNOWN_MISSING
    assert not extra, (
        "Neue/undokumentierte Parameter ohne Herleitung+Quellen (source_detail/"
        f"references leer): {sorted(extra)}"
    )


def test_docs_ratchet_shrinks():
    """Jede dokumentierte Batch muss KNOWN_MISSING hier mitschrumpfen."""
    stale = KNOWN_MISSING - _undocumented()
    assert not stale, (
        "Bereits dokumentiert, bitte aus KNOWN_MISSING entfernen (Ratchet festziehen): "
        f"{sorted(stale)}"
    )


# ── Tote Parameter bleiben draußen, lebende drin ────────────────────────────────

def test_dead_parameters_removed():
    ids = {p["id"] for p in _params()}
    leftover_pathways = {i for i in ids if i.startswith("pathway_weights.")}
    assert not leftover_pathways, f"Pfadgewichte wieder emittiert: {sorted(leftover_pathways)}"
    dead = ids & _REMOVED_DEAD_IDS
    assert not dead, f"Tote Formel-Parameter wieder emittiert: {sorted(dead)}"


def test_live_formula_params_present_and_documented():
    params = _params()
    by_id = {p["id"]: p for p in params}
    for pid in sorted(_LIVE_FORMULA_IDS):
        p = by_id.get(pid)
        assert p is not None, f"Lebender Formel-Parameter fehlt: {pid}"
        assert p["editable"] is True, f"{pid} nicht editierbar"
        assert p["value"] is not None, f"{pid} ohne anzeigbaren Default (value=None)"
        assert p.get("source_detail") or p.get("references"), f"{pid} ohne Infokasten"
    # KRITIS-Klassengewichte kategorie-unabhängig je (Layer-Code, w_<cls>) — die
    # Emissionskategorie hängt in M0 am formulas-Fallback (siehe Kommentar oben).
    by_layer_key = {
        (p.get("layer_code"), p["id"].rsplit(".", 1)[-1]): p
        for p in params if ".param." in p["id"]
    }
    for code, key in sorted(_LIVE_FORMULA_KEYS_BY_LAYER):
        p = by_layer_key.get((code, key))
        assert p is not None, f"Klassengewicht fehlt in der Registry: {code}.param.{key}"
        assert p["editable"] is True, f"{code}.param.{key} nicht editierbar"
        assert p["value"] is not None, f"{code}.param.{key} ohne anzeigbaren Default"
        assert p.get("source_detail") or p.get("references"), \
            f"{code}.param.{key} ohne Infokasten"


def test_new_tunables_present_and_documented():
    by_id = {p["id"]: p for p in _params()}
    for pid in sorted(_NEW_PARAM_IDS):
        p = by_id.get(pid)
        assert p is not None, f"Neuer Parameter fehlt in der Registry: {pid}"
        assert p.get("source_detail"), f"{pid} ohne Herleitung (source_detail)"


def test_category_filter_returns_globals():
    """`?category=uhi/impact/model/regional` liefert die layer-losen Gruppen."""
    for cat, minimum in (("uhi", 6), ("impact", 12), ("model", 5), ("regional", 11)):
        got = parameter_registry.catalog_parameters(layer_category=cat)
        assert len(got) >= minimum, f"Kategorie-Filter {cat} liefert nur {len(got)}"
        assert all(p["layer_category"] == cat for p in got)


# ── Wiring: Overrides ändern die Rechnung wirklich ──────────────────────────────

def test_wiring_uhi_epsilon_and_tree_cooling():
    from app.services.engine.inputs import compute_uhi_delta

    lu = {"impervious_fraction": 0.6, "albedo": 0.15, "green_fraction": 0.1,
          "water_fraction": 0.0, "forest_fraction": 0.0, "farmland_fraction": 0.0}
    bm = {"building_coverage": 0.4, "avg_building_height": 15.0, "road_coverage": 0.2,
          "tree_canopy_fraction": 0.2, "sky_view_factor": 0.5}
    base = compute_uhi_delta(lu, bm)
    with override_context.override_scope({"uhi.tree_cooling": 3.0}):
        cooler = compute_uhi_delta(lu, bm)
    assert cooler < base, "uhi.tree_cooling-Override wirkungslos"
    with override_context.override_scope({"uhi.epsilon": 6.0}):
        hotter = compute_uhi_delta(lu, bm)
    assert hotter > base, "uhi.epsilon-Override wirkungslos"


def test_wiring_uhi_mean_components():
    """Die Parameter des 24-h-Wärmeinsel-Mittels müssen die Rechnung verändern.

    ``mean`` speist die Zelltemperatur und damit die Hitzemortalität; ``day``
    bleibt unverändert der Treiber von HEAT_WAVE/UHI_INTENSITY.
    """
    from app.services.engine.inputs import compute_uhi_components

    lu = {"impervious_fraction": 0.85, "albedo": 0.15, "green_fraction": 0.05,
          "water_fraction": 0.0, "forest_fraction": 0.0, "farmland_fraction": 0.0}
    bm = {"building_coverage": 0.45, "avg_building_height": 20.0, "road_coverage": 0.2,
          "tree_canopy_fraction": 0.05, "sky_view_factor": 0.4}
    base = compute_uhi_components(lu, bm, vent_score=0.5, water_prox=0.0)

    with override_context.override_scope({"uhi.mean_factor": 0.9}):
        assert compute_uhi_components(lu, bm, 0.5, 0.0)["mean"] > base["mean"], \
            "uhi.mean_factor-Override wirkungslos"
    with override_context.override_scope({"uhi.vent_ratio": 0.9}):
        assert compute_uhi_components(lu, bm, 0.5, 0.0)["mean"] < base["mean"], \
            "uhi.vent_ratio-Override wirkungslos (Durchlüftung muss dämpfen)"
    with override_context.override_scope({"uhi.zeta": 4.0}):
        assert compute_uhi_components(lu, bm, 0.5, 0.0)["night"] > base["night"], \
            "uhi.zeta-Override wirkungslos"
    with override_context.override_scope({"uhi.night_weight": 0.95}):
        assert compute_uhi_components(lu, bm, 0.5, 0.0)["mean"] != base["mean"], \
            "uhi.night_weight-Override wirkungslos"
    with override_context.override_scope({"uhi.delta_night": 5.0}):
        assert compute_uhi_components(lu, bm, 0.5, 1.0)["night"] < base["night"], \
            "uhi.delta_night-Override wirkungslos (Gewässer müssen kühlen)"

    # Durchlüftung darf das Tagesmaximum NICHT verändern — sonst verschöbe sich
    # HEAT_WAVE und mit ihm die Kalibrierung aller übrigen Hitzekanäle.
    calm = compute_uhi_components(lu, bm, vent_score=0.0, water_prox=0.0)
    assert calm["day"] == base["day"]
    assert calm["mean"] > base["mean"]


def test_wiring_measure_saturation_and_cap():
    from app.services.measure_service import _reduction_factor

    mdef = {"default_reduction": 0.4, "coverage_scaling": "saturating",
            "effect_target": ["hazard"]}
    base = _reduction_factor(mdef, fraction=0.5)
    with override_context.override_scope({"model.measure_coverage_saturation": 1.0}):
        weaker = _reduction_factor(mdef, fraction=0.5)
    assert weaker > base, "Sättigungs-Override wirkungslos (Faktor = verbleibender Anteil)"

    strong = {"default_reduction": 0.9, "coverage_scaling": "linear",
              "effect_target": ["hazard"]}
    with override_context.override_scope({"model.measure_reduction_cap": 0.5}):
        capped = _reduction_factor(strong, fraction=1.0)
    assert abs(capped - 0.5) < 1e-9, "Kappungs-Override wirkungslos"


def test_wiring_ref_population_in_engine_and_sanity():
    from app.services.engine import risk_engine
    from app.services.engine.impact import sanity

    risk = {"code": "X", "scale": "pop", "ref_value": 10.0}
    base = sanity.ref_estimate(risk, total_pop=100_000.0, area_km2=10.0)
    with override_context.override_scope({"model.ref_population": 50_000.0}):
        doubled = sanity.ref_estimate(risk, total_pop=100_000.0, area_km2=10.0)
        scale = risk_engine._scale_factor(risk, 100_000.0, 10.0)
    assert abs(doubled - 2 * base) < 1e-9, "Sanity nutzt die Referenzbevölkerung nicht"
    assert abs(scale - 2.0) < 1e-9, "Engine-Skalierung nutzt die Referenzbevölkerung nicht"


def test_wiring_regional_fallbacks():
    from app.services.engine.inputs import build_regional_context

    base = build_regional_context("Bayern", False, None, None)
    with override_context.override_scope({
        "regional.storm_days": 11.0,
        "regional.drought_base": 0.0,
        "regional.glacier_loss_rate": 2.5,
    }):
        tuned = build_regional_context("Bayern", False, None, None)
    if base["provenance"].get("storm_days") == "regional_constant":
        assert tuned["storm_days"] == 11.0, "regional.storm_days-Override wirkungslos"
    assert tuned["drought_days"] < base["drought_days"], "regional.drought_base wirkungslos"
    assert tuned["glacier_loss_rate"] == 2.5, "regional.glacier_loss_rate wirkungslos"


def test_wiring_risk_threshold():
    with override_context.override_scope({"model.risk_threshold": 80.0}):
        assert tunables.effective_risk_threshold() == 80.0
    assert tunables.effective_risk_threshold() == tunables.RISK_THRESHOLD_DEFAULT


# ── Skript-Modus: offene IDs listen (Fortsetzungs-Prompt) ───────────────────────

if __name__ == "__main__":
    if "--list" in sys.argv:
        open_ids = sorted(_undocumented())
        print(f"Undokumentierte anwendbare Parameter: {len(open_ids)}")
        for pid in open_ids:
            print(f"  {pid}")
        sys.exit(0)

    import traceback

    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except Exception:
            failed += 1
            print(f"FAIL {t.__name__}")
            traceback.print_exc()
    sys.exit(1 if failed else 0)
