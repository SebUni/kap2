"""Umwelt-Schadensfunktionen (Schicht B, §6.4 — physischer Flächen-/Artenverlust).

Kern je Zelle: ``Verlust = exponierte Naturfläche · Verlustrate(Hazard) · g(V̂)``, Summe
über Zellen. Die exponierte Fläche kommt aus den realen Landnutzungsanteilen der Zelle
(Wald-/Grün-/Agrarfläche × 1 ha Zellfläche); die Verlustrate skaliert linear mit der
normierten Hazard-Intensität (gradueller Prozess). Monetarisiert wird über den bereits
vorhandenen, editierbaren Kostensatz je Risiko (€/ha bzw. €/Art) —
``risk_engine.cost_from_outcome``.

Die reinen Index-/Screening-Umweltrisiken (Ökosystem-Degradation/-Fragmentierung,
Wasser-/Luftverschmutzung, Rückkopplung, Fischereibestandsstress …) bleiben bewusst ohne
eigene Funktion (Kostensatz 0, dokumentierte Doppelzählungs-Vermeidung, §6.4).
"""

from __future__ import annotations

from app.services.engine import risk_engine
from app.services.engine.impact.base import CellContext

CELL_AREA_HA = 1.0   # 100 m × 100 m


def _result(risk: dict, outcome: float) -> dict:
    outcome = max(0.0, outcome)
    return {"outcome": outcome, "cost_eur": risk_engine.cost_from_outcome(risk, outcome)}


def _driver(ctx: CellContext, hazard_codes: list[str]) -> float:
    # Fixe Katalog-Referenzgrenzen (haz_intensity): Screening-Norm-Overrides ändern die
    # absoluten Flächen-/Artenverluste nicht (§3.3-Restlücke).
    return max((ctx.haz_intensity(h) for h in hazard_codes), default=0.0)


# ── Biodiversitätsverlust (Arten/Jahr) ─────────────────────────────────────────

def biodiversity_loss(risk, ctx):
    area = (ctx.inp("forest_frac") + ctx.inp("green_frac")) * CELL_AREA_HA
    rate = ctx.p(risk["code"], "species_loss_per_ha", 0.0006)   # Arten je ha·a bei voller Intensität
    driver = _driver(ctx, ["MEAN_TEMPERATURE_RISE", "DROUGHT", "WILDFIRE"])
    return _result(risk, area * rate * driver * ctx.g(risk))


# ── Habitatverlust (ha/Jahr) ────────────────────────────────────────────────────

def habitat_loss(risk, ctx):
    area = (ctx.inp("forest_frac") + ctx.inp("green_frac") + ctx.inp("water_frac")) * CELL_AREA_HA
    rate = ctx.p(risk["code"], "loss_rate", 0.02)
    driver = _driver(ctx, ["DROUGHT", "WILDFIRE", "SEA_LEVEL_RISE"])
    return _result(risk, area * rate * driver * ctx.g(risk))


# ── Bodendegradation (ha/Jahr) ──────────────────────────────────────────────────

def soil_degradation(risk, ctx):
    area = ctx.inp("farmland_frac") * CELL_AREA_HA
    rate = ctx.p(risk["code"], "loss_rate", 0.03)
    driver = _driver(ctx, ["DROUGHT", "HEAVY_RAIN_FLOOD", "SOIL_SALINIZATION"])
    return _result(risk, area * rate * driver * ctx.g(risk))


# ── Vegetationsschaden (ha/Jahr) ────────────────────────────────────────────────

def vegetation_damage(risk, ctx):
    area = (ctx.inp("forest_frac") + ctx.inp("farmland_frac")) * CELL_AREA_HA
    rate = ctx.p(risk["code"], "loss_rate", 0.05)
    driver = _driver(ctx, ["DROUGHT", "HEAT_WAVE", "WILDFIRE"])
    return _result(risk, area * rate * driver * ctx.g(risk))


ENVIRONMENT_IMPACTS = {
    "EXPECTED_BIODIVERSITY_LOSS": biodiversity_loss,
    "EXPECTED_HABITAT_LOSS": habitat_loss,
    "EXPECTED_SOIL_DEGRADATION": soil_degradation,
    "EXPECTED_VEGETATION_DAMAGE": vegetation_damage,
}
