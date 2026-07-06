"""Gesundheits-Schadensfunktionen (Schicht B, Stufe 4 — MODELL_KRITIK §6.1).

Kernmuster: ``Outcome = Betroffene · Rate · Treiber · g(V̂)`` je Zelle, Summe über
Zellen in ``risk_engine.aggregate``. Der Treiber ist für hitzegetriebene Risiken die
**nichtlineare attributable Fraktion** ``AF(Hitzetage)`` (fixt §3.4), für ereignis-
getriebene Risiken (Flut/Sturm) die normierte Hazard-Intensität. Alle Raten/Koeffizienten
sind editierbare Registry-Parameter (``impact/params.py``), kalibriert auf publizierte
Größenordnungen (RKI/Winklmayr 2022; UBA MK3.1; GDV; Destatis).

Registrierung am Modulende: die Funktionen werden in ``impact.IMPACT_FUNCTIONS``
eingetragen; ``compute_all_cell_impacts`` verteilt darauf, sonst auf ``legacy_cell_impact``.
"""

from __future__ import annotations

from app.services.engine import risk_engine
from app.services.engine.impact.base import CellContext, attributable_fraction


def _result(risk: dict, outcome: float) -> dict:
    outcome = max(0.0, outcome)
    return {"outcome": outcome, "cost_eur": risk_engine.cost_from_outcome(risk, outcome)}


def _heat_af(ctx: CellContext, code: str, beta_default: float, thr_default: float) -> float:
    """Attributable Fraktion aus den Zell-Hitzetagen (HEAT_WAVE absolut)."""
    hd = ctx.haz("HEAT_WAVE")
    beta = ctx.p(code, "beta_per_hotday", beta_default)
    thr = ctx.p(code, "hotday_threshold", thr_default)
    return attributable_fraction(hd, beta, thr)


# ── 1. Hitzemortalität ─────────────────────────────────────────────────────────

def mortality(risk: dict, ctx: CellContext) -> dict:
    code = risk["code"]
    baseline = ctx.p(code, "baseline_mort_per_100k", 1130.0)
    af = _heat_af(ctx, code, 0.0008, 8.0)
    outcome = ctx.pop * (baseline / 100_000.0) * af * ctx.g(risk)
    return _result(risk, outcome)


# ── 2. Hitzemorbidität ─────────────────────────────────────────────────────────

def morbidity(risk: dict, ctx: CellContext) -> dict:
    code = risk["code"]
    rate = ctx.p(code, "rate_per_100k", 8000.0)
    af = _heat_af(ctx, code, 0.0016, 8.0)
    outcome = ctx.pop * (rate / 100_000.0) * af * ctx.g(risk)
    return _result(risk, outcome)


# ── 3. Verletzte (Flut/Sturm/Hangrutsch) ──────────────────────────────────────

def injuries(risk: dict, ctx: CellContext) -> dict:
    code = risk["code"]
    rate = ctx.p(code, "rate_per_100k", 150.0)
    # Ereignisgetrieben: Intensität des stärksten relevanten Hazards (fixe Katalog-
    # Referenzgrenzen, entkoppelt von Screening-Norm-Overrides — §3.3-Restlücke).
    driver = max(ctx.haz_intensity("HEAVY_RAIN_FLOOD"),
                 ctx.haz_intensity("EXTRATROPICAL_STORM"),
                 ctx.haz_intensity("LANDSLIDE"))
    outcome = ctx.pop * (rate / 100_000.0) * driver * ctx.g(risk)
    return _result(risk, outcome)


# ── 4. Psychische Gesundheit ───────────────────────────────────────────────────

def mental_health(risk: dict, ctx: CellContext) -> dict:
    code = risk["code"]
    rate = ctx.p(code, "rate_per_100k", 1500.0)
    af = _heat_af(ctx, code, 0.0012, 10.0)
    # zusätzlicher Ereignisanteil (Extremereignisse/Kaskaden/Dürre); fixe Katalog-
    # Referenzgrenzen (haz_intensity, §3.3-Restlücke).
    event = max(ctx.haz_intensity("COMPOUND_EVENT"), ctx.haz_intensity("CASCADE_EVENT"),
                ctx.haz_intensity("DROUGHT"))
    driver = min(1.0, af + ctx.p(code, "event_share", 0.3) * event)
    outcome = ctx.pop * (rate / 100_000.0) * driver * ctx.g(risk)
    return _result(risk, outcome)


# ── 5. Betroffene / Evakuierte (Flut/Sturmflut/Feuer) ──────────────────────────

def affected_evacuated(risk: dict, ctx: CellContext) -> dict:
    code = risk["code"]
    rate = ctx.p(code, "rate_per_100k", 2500.0)
    driver = max(ctx.haz_intensity("HEAVY_RAIN_FLOOD"),
                 ctx.haz_intensity("STORM_SURGE"),
                 ctx.haz_intensity("WILDFIRE"))
    outcome = ctx.pop * (rate / 100_000.0) * driver * ctx.g(risk)
    return _result(risk, outcome)


# ── 6. Wärmebelastungsstunden ──────────────────────────────────────────────────

def thermal_stress_hours(risk: dict, ctx: CellContext) -> dict:
    code = risk["code"]
    hours_ref = ctx.p(code, "hours_ref_per_100k", 400.0)
    ref_hd = ctx.p(code, "reference_hotdays", 20.0)
    hd = ctx.haz("HEAT_WAVE")
    driver = hd / ref_hd if ref_hd > 0 else 0.0
    outcome = (ctx.pop / 100_000.0) * hours_ref * driver * ctx.g(risk)
    return _result(risk, outcome)


# ── 7. Schadstoff-Belastungsstunden ────────────────────────────────────────────

def pollutant_exposure_hours(risk: dict, ctx: CellContext) -> dict:
    code = risk["code"]
    hours_ref = ctx.p(code, "hours_ref_per_100k", 250.0)
    ref_hd = ctx.p(code, "reference_hotdays", 20.0)
    hd = ctx.haz("HEAT_WAVE")   # bodennahes Ozon/Feinstaub korreliert mit Hitze
    driver = hd / ref_hd if ref_hd > 0 else 0.0
    outcome = (ctx.pop / 100_000.0) * hours_ref * driver * ctx.g(risk)
    return _result(risk, outcome)


HEALTH_IMPACTS = {
    "EXPECTED_ANNUAL_MORTALITY": mortality,
    "EXPECTED_ANNUAL_MORBIDITY": morbidity,
    "EXPECTED_ANNUAL_INJURIES": injuries,
    "EXPECTED_ANNUAL_MENTAL_HEALTH": mental_health,
    "EXPECTED_ANNUAL_AFFECTED_EVACUATED": affected_evacuated,
    "EXPECTED_THERMAL_STRESS_HOURS": thermal_stress_hours,
    "EXPECTED_POLLUTANT_EXPOSURE_HOURS": pollutant_exposure_hours,
}


# ── Lineage-Spezifikation (Wirkungsdiagramm) ───────────────────────────────────
# Deklariert je Risiko, was die Funktion oben rechnet (Bevölkerung · Rate · Treiber ·
# g(V̂)), damit ``lineage_graph`` den Schicht-B-Zweig des Wirkungsdiagramms exakt aus
# der tatsächlichen Rechnung baut. Muss die Funktionskörper spiegeln
# (Key-Gleichheit wird in tests/test_lineage_graph.py geprüft).
LINEAGE_SPECS: dict[str, dict] = {
    "EXPECTED_ANNUAL_MORTALITY": {
        "rate_param": "baseline_mort_per_100k",
        "driver": {"kind": "af", "hazard": "HEAT_WAVE",
                   "params": ["beta_per_hotday", "hotday_threshold"]},
    },
    "EXPECTED_ANNUAL_MORBIDITY": {
        "rate_param": "rate_per_100k",
        "driver": {"kind": "af", "hazard": "HEAT_WAVE",
                   "params": ["beta_per_hotday", "hotday_threshold"]},
    },
    "EXPECTED_ANNUAL_INJURIES": {
        "rate_param": "rate_per_100k",
        "driver": {"kind": "intensity",
                   "hazards": ["HEAVY_RAIN_FLOOD", "EXTRATROPICAL_STORM", "LANDSLIDE"]},
    },
    "EXPECTED_ANNUAL_MENTAL_HEALTH": {
        "rate_param": "rate_per_100k",
        "driver": {"kind": "af_plus_event", "hazard": "HEAT_WAVE",
                   "params": ["beta_per_hotday", "hotday_threshold"],
                   "event_hazards": ["COMPOUND_EVENT", "CASCADE_EVENT", "DROUGHT"],
                   # editierbarer Registry-Parameter (risks.….impact.event_share)
                   "event_share_param": "event_share"},
    },
    "EXPECTED_ANNUAL_AFFECTED_EVACUATED": {
        "rate_param": "rate_per_100k",
        "driver": {"kind": "intensity",
                   "hazards": ["HEAVY_RAIN_FLOOD", "STORM_SURGE", "WILDFIRE"]},
    },
    "EXPECTED_THERMAL_STRESS_HOURS": {
        "rate_param": "hours_ref_per_100k",
        "driver": {"kind": "ratio", "hazard": "HEAT_WAVE",
                   "params": ["reference_hotdays"]},
    },
    "EXPECTED_POLLUTANT_EXPOSURE_HOURS": {
        "rate_param": "hours_ref_per_100k",
        "driver": {"kind": "ratio", "hazard": "HEAT_WAVE",
                   "params": ["reference_hotdays"]},
    },
}
