"""Monetäre Schadensfunktionen (Schicht B, §6.2 — AAL-Struktur).

Kern je direktem Sektorschaden und Zelle:
    ``Schaden = Assetwert · max. Jahresverlustrate · Schadenskurve(Intensität) · g(V̂)``
Der **Assetwert** kommt aus den realen Zell-Rohgrößen (Gebäudefläche, KRITIS-
Anlagenklassen-Zählung, Agrar-/Wald-/Gewässerfläche) × editierbaren €-Parametern
statt aus dem abstrakten ``ref_value``. Die **Schadenskurve** ist konvex in der normierten Hazard-
Intensität der Zelle (``curves.damage_fraction``).

Folgekosten werden NICHT einzeln additiv gerechnet, sondern in
``compute_all_cell_impacts`` konsolidiert (siehe ``consolidate_indirect``):
- indirekte Verluste = ``k_indirekt · Σ direkte Sektorschäden`` (Zelle),
- Versorgungsengpass / Standortnachteil / verzögerte Schäden = 0 (in k_indirekt enthalten),
- Restaurierung = ``restaurierungsquote · Σ direkte Sektorschäden`` (nicht-additive Teilkennzahl).
"""

from __future__ import annotations

from app.data import catalog, infra_assets
from app.services.engine.impact.base import CellContext
from app.services.engine.impact.curves import damage_fraction

CELL_AREA_M2 = 10_000.0   # 100 m × 100 m
CELL_AREA_HA = 1.0
_FLOOR_HEIGHT_M_DEFAULT = 3.5   # Default der Geschosshöhe; editierbar als impact.floor_height_m


def _result(outcome: float) -> dict:
    outcome = max(0.0, outcome)
    return {"outcome": outcome, "cost_eur": outcome}   # monetär: € = Outcome


def _sector(ctx: CellContext, risk: dict, asset_value: float,
            hazard_codes: list[str], loss_default: float) -> dict:
    """Assetwert · Jahresverlustrate · konvexe Schadenskurve(Intensität) · g(V̂)."""
    loss_rate = ctx.p(risk["code"], "max_loss_rate", loss_default)
    exponent = ctx.pg("damage_exponent", 1.5)
    # Fixe Katalog-Referenzgrenzen (haz_intensity), damit Screening-Norm-Overrides die
    # absoluten Schäden nicht verändern (§3.3-Restlücke).
    intensity = max((ctx.haz_intensity(h) for h in hazard_codes), default=0.0)
    frac = damage_fraction(intensity, exponent)
    return _result(asset_value * loss_rate * frac * ctx.g(risk))


# ── Assetwert-Helfer (aus realen Zell-Rohgrößen × €-Parameter) ─────────────────

def _building_asset(ctx: CellContext) -> float:
    fh = ctx.pg("floor_height_m", _FLOOR_HEIGHT_M_DEFAULT)
    fh = fh if fh > 0 else _FLOOR_HEIGHT_M_DEFAULT
    floors = max(1.0, ctx.inp("avg_height", fh) / fh)
    floor_area = ctx.inp("bldg_cov") * CELL_AREA_M2 * floors
    return floor_area * ctx.pg("building_value_eur_m2", 2000.0)


def _class_asset(ctx: CellContext, classes_key: str, sector: str) -> float:
    """Assetwert = Σ Anzahl je Anlagenklasse × klassenspezifischer Ersatzwert.

    Nutzt die rohen Klassen-Zählungen (``*_classes``) statt der gewichteten
    Kritikalitätspunkte: ein Umspannwerk und ein Ortsnetztrafo haben andere
    Ersatzwerte als ein Sektor-Mittelwert je Stück abbilden könnte.
    """
    classes = ctx.ci.get(classes_key) or {}
    total = 0.0
    for cls, count in classes.items():
        spec = infra_assets.ASSET_CLASSES[sector].get(cls)
        if spec is None:
            continue
        value = ctx.pg(infra_assets.value_param_key(sector, cls), spec["value_eur"])
        total += float(count) * value
    return total


def _area_asset(ctx: CellContext, frac_key: str, value_ha: float) -> float:
    return ctx.inp(frac_key) * CELL_AREA_HA * value_ha


# ── Direkte Sektorschäden ──────────────────────────────────────────────────────

def building_damage(risk, ctx):
    return _sector(ctx, risk, _building_asset(ctx),
                   ["HEAVY_RAIN_FLOOD", "EXTRATROPICAL_STORM", "HEAT_WAVE"], 0.008)


def transport_damage(risk, ctx):
    asset = _class_asset(ctx, "transport_hub_classes", "transport")
    return _sector(ctx, risk, asset, ["HEAVY_RAIN_FLOOD", "HEAT_WAVE", "DROUGHT"], 0.02)


def energy_damage(risk, ctx):
    asset = _class_asset(ctx, "energy_infra_classes", "energy")
    return _sector(ctx, risk, asset, ["EXTRATROPICAL_STORM", "HEAVY_RAIN_FLOOD", "HEAT_WAVE"], 0.02)


def telecom_damage(risk, ctx):
    asset = _class_asset(ctx, "communication_classes", "comm")
    return _sector(ctx, risk, asset, ["EXTRATROPICAL_STORM", "HEAVY_RAIN_FLOOD"], 0.02)


def water_damage(risk, ctx):
    asset = _class_asset(ctx, "water_wastewater_classes", "water")
    return _sector(ctx, risk, asset, ["HEAVY_RAIN_FLOOD", "DROUGHT", "HEAT_WAVE"], 0.015)


def agricultural_damage(risk, ctx):
    asset = _area_asset(ctx, "farmland_frac", ctx.pg("agri_value_eur_ha", 12_000.0))
    return _sector(ctx, risk, asset, ["DROUGHT", "HEAT_WAVE", "HEAVY_RAIN_FLOOD"], 0.15)


def soil_damage(risk, ctx):
    asset = _area_asset(ctx, "farmland_frac", ctx.pg("soil_value_eur_ha", 30_000.0))
    return _sector(ctx, risk, asset, ["DROUGHT", "HEAVY_RAIN_FLOOD", "SOIL_SALINIZATION"], 0.01)


def ecosystem_service_loss(risk, ctx):
    area = (ctx.inp("forest_frac") + ctx.inp("green_frac")) * CELL_AREA_HA
    asset = area * ctx.pg("esl_value_eur_ha", 3000.0)
    return _sector(ctx, risk, asset, ["DROUGHT", "HEAVY_RAIN_FLOOD", "SEA_LEVEL_RISE"], 0.08)


def fisheries_loss(risk, ctx):
    asset = _area_asset(ctx, "water_frac", ctx.pg("fisheries_value_eur_ha", 5000.0))
    return _sector(ctx, risk, asset,
                   ["SURFACE_WATER_HEATING", "LOW_FLOW_NIEDRIGWASSER", "DROUGHT", "HEAT_WAVE"], 0.20)


def aquaculture_damage(risk, ctx):
    asset = _area_asset(ctx, "water_frac", ctx.pg("fisheries_value_eur_ha", 5000.0))
    return _sector(ctx, risk, asset,
                   ["SURFACE_WATER_HEATING", "LOW_FLOW_NIEDRIGWASSER", "HEAVY_RAIN_FLOOD"], 0.25)


# ── Klimamigration (eigenständig, nicht in k_indirekt) ─────────────────────────

def migration_costs(risk, ctx):
    ref = ctx.p(risk["code"], "cost_ref_per_100k", 400_000.0)
    driver = max(ctx.haz_intensity("SEA_LEVEL_RISE"), ctx.haz_intensity("HEAVY_RAIN_FLOOD"),
                 ctx.haz_intensity("DROUGHT"))
    outcome = (ctx.pop / 100_000.0) * ref * driver * ctx.g(risk)
    return _result(outcome)


MONETARY_IMPACTS = {
    "EXPECTED_BUILDING_DAMAGE_EUR": building_damage,
    "EXPECTED_TRANSPORT_DAMAGE_EUR": transport_damage,
    "EXPECTED_ENERGY_INFRA_DAMAGE_EUR": energy_damage,
    "EXPECTED_TELECOM_DAMAGE_EUR": telecom_damage,
    "EXPECTED_WATER_WASTEWATER_DAMAGE_EUR": water_damage,
    "EXPECTED_AGRICULTURAL_DAMAGE_EUR": agricultural_damage,
    "EXPECTED_SOIL_LOSS_DEGRADATION_EUR": soil_damage,
    "EXPECTED_ECOSYSTEM_SERVICE_LOSS": ecosystem_service_loss,
    "EXPECTED_FISHERIES_ECONOMIC_LOSS_EUR": fisheries_loss,
    "EXPECTED_AQUACULTURE_DAMAGE_EUR": aquaculture_damage,
    "EXPECTED_CLIMATE_MIGRATION_COSTS_EUR": migration_costs,
}


# ── Lineage-Spezifikation (Wirkungsdiagramm) ───────────────────────────────────
# Deklariert je Sektorschaden, was die Funktion oben rechnet (Assetwert · Verlustrate ·
# Schadenskurve(Intensität) · g(V̂)), damit ``lineage_graph`` den Schicht-B-Zweig exakt
# aus der tatsächlichen Rechnung baut. ``asset.kind``: building (Geschossfläche ×
# €/m²), class_count (Σ Anzahl je Anlagenklasse × Ersatzwert der Klasse, Parameter in
# ``value_params``), area (Flächenanteile × €/ha). Migration folgt dem
# Bevölkerungs-Muster (Bevölkerung · Referenzkosten · Intensität · g(V̂)) und liefert
# direkt €. Key-Gleichheit mit MONETARY_IMPACTS wird in tests/test_lineage_graph.py geprüft.

def _class_value_params(sector: str) -> list[str]:
    return [
        infra_assets.value_param_key(sector, cls)
        for cls in infra_assets.ASSET_CLASSES[sector]
    ]


LINEAGE_SPECS: dict[str, dict] = {
    "EXPECTED_BUILDING_DAMAGE_EUR": {
        "asset": {"kind": "building", "cell_keys": ["bldg_cov", "avg_height"],
                  "value_param": "building_value_eur_m2",
                  "label": "Gebäude-Assetwert (Zelle)"},
        "loss_param": "max_loss_rate",
        "driver": {"kind": "intensity",
                   "hazards": ["HEAVY_RAIN_FLOOD", "EXTRATROPICAL_STORM", "HEAT_WAVE"]},
    },
    "EXPECTED_TRANSPORT_DAMAGE_EUR": {
        "asset": {"kind": "class_count", "cell_keys": ["transport_hub_classes"],
                  "value_params": _class_value_params("transport"),
                  "label": "Verkehrs-Assetwert (Zelle)"},
        "loss_param": "max_loss_rate",
        "driver": {"kind": "intensity",
                   "hazards": ["HEAVY_RAIN_FLOOD", "HEAT_WAVE", "DROUGHT"]},
    },
    "EXPECTED_ENERGY_INFRA_DAMAGE_EUR": {
        "asset": {"kind": "class_count", "cell_keys": ["energy_infra_classes"],
                  "value_params": _class_value_params("energy"),
                  "label": "Energie-Assetwert (Zelle)"},
        "loss_param": "max_loss_rate",
        "driver": {"kind": "intensity",
                   "hazards": ["EXTRATROPICAL_STORM", "HEAVY_RAIN_FLOOD", "HEAT_WAVE"]},
    },
    "EXPECTED_TELECOM_DAMAGE_EUR": {
        "asset": {"kind": "class_count", "cell_keys": ["communication_classes"],
                  "value_params": _class_value_params("comm"),
                  "label": "Telekom-Assetwert (Zelle)"},
        "loss_param": "max_loss_rate",
        "driver": {"kind": "intensity",
                   "hazards": ["EXTRATROPICAL_STORM", "HEAVY_RAIN_FLOOD"]},
    },
    "EXPECTED_WATER_WASTEWATER_DAMAGE_EUR": {
        "asset": {"kind": "class_count", "cell_keys": ["water_wastewater_classes"],
                  "value_params": _class_value_params("water"),
                  "label": "Wasser-/Abwasser-Assetwert (Zelle)"},
        "loss_param": "max_loss_rate",
        "driver": {"kind": "intensity",
                   "hazards": ["HEAVY_RAIN_FLOOD", "DROUGHT", "HEAT_WAVE"]},
    },
    "EXPECTED_AGRICULTURAL_DAMAGE_EUR": {
        "asset": {"kind": "area", "cell_keys": ["farmland_frac"],
                  "value_param": "agri_value_eur_ha",
                  "label": "Agrar-Ertragswert (Zelle)"},
        "loss_param": "max_loss_rate",
        "driver": {"kind": "intensity",
                   "hazards": ["DROUGHT", "HEAT_WAVE", "HEAVY_RAIN_FLOOD"]},
    },
    "EXPECTED_SOIL_LOSS_DEGRADATION_EUR": {
        "asset": {"kind": "area", "cell_keys": ["farmland_frac"],
                  "value_param": "soil_value_eur_ha",
                  "label": "Bodenwert (Zelle)"},
        "loss_param": "max_loss_rate",
        "driver": {"kind": "intensity",
                   "hazards": ["DROUGHT", "HEAVY_RAIN_FLOOD", "SOIL_SALINIZATION"]},
    },
    "EXPECTED_ECOSYSTEM_SERVICE_LOSS": {
        "asset": {"kind": "area", "cell_keys": ["forest_frac", "green_frac"],
                  "value_param": "esl_value_eur_ha",
                  "label": "Ökosystemleistungswert (Zelle)"},
        "loss_param": "max_loss_rate",
        "driver": {"kind": "intensity",
                   "hazards": ["DROUGHT", "HEAVY_RAIN_FLOOD", "SEA_LEVEL_RISE"]},
    },
    "EXPECTED_FISHERIES_ECONOMIC_LOSS_EUR": {
        "asset": {"kind": "area", "cell_keys": ["water_frac"],
                  "value_param": "fisheries_value_eur_ha",
                  "label": "Fischereiwert (Zelle)"},
        "loss_param": "max_loss_rate",
        "driver": {"kind": "intensity",
                   "hazards": ["SURFACE_WATER_HEATING", "LOW_FLOW_NIEDRIGWASSER",
                                "DROUGHT", "HEAT_WAVE"]},
    },
    "EXPECTED_AQUACULTURE_DAMAGE_EUR": {
        "asset": {"kind": "area", "cell_keys": ["water_frac"],
                  "value_param": "fisheries_value_eur_ha",
                  "label": "Aquakulturwert (Zelle)"},
        "loss_param": "max_loss_rate",
        "driver": {"kind": "intensity",
                   "hazards": ["SURFACE_WATER_HEATING", "LOW_FLOW_NIEDRIGWASSER",
                                "HEAVY_RAIN_FLOOD"]},
    },
    "EXPECTED_CLIMATE_MIGRATION_COSTS_EUR": {
        "basis_pop": True,
        "rate_param": "cost_ref_per_100k",
        "driver": {"kind": "intensity",
                   "hazards": ["SEA_LEVEL_RISE", "HEAVY_RAIN_FLOOD", "DROUGHT"]},
    },
}


def consolidate_indirect(out: dict[str, dict], ctx: CellContext) -> None:
    """k_indirekt-Konsolidierung der Folgekosten (in-place, nach den Direktschäden)."""
    direct = sum(out[c]["cost_eur"] for c in catalog.DIRECT_SECTOR_RISK_CODES if c in out)
    k = ctx.pg("k_indirect", 0.25)
    r_share = ctx.pg("restoration_share", 0.15)

    if "EXPECTED_INDIRECT_ECONOMIC_LOSS_EUR" in out:
        out["EXPECTED_INDIRECT_ECONOMIC_LOSS_EUR"] = _result(k * direct)
    for code in catalog.CONSOLIDATED_INTO_INDIRECT_CODES:
        if code in out:
            out[code] = _result(0.0)   # in k_indirekt enthalten
    if "EXPECTED_RESTORATION_COSTS_EUR" in out:
        out["EXPECTED_RESTORATION_COSTS_EUR"] = _result(r_share * direct)   # nicht-additiv
