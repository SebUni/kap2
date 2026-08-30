"""Grobes Gemeinde-Risiko-Scoring (Deutschland-Lite), pure Funktionen.

KEIN 100m-Engine: ein Wert je Gemeinde und Risiko aus deutschlandweit
verfügbaren Grobdaten (DWD-1km am Repräsentationspunkt, Zensus-Aggregat,
INKAR-Kreis). Ablauf (Plan §4):

1. ``raw = H_norm × E_norm × V_norm`` je Gemeinde (0..1-Komponenten).
2. Nationale p5–p95-Normierung je Risiko → ``index`` 0–100 (nutzt die volle
   Skala, macht die Choropleth informativ).
3. ``outcome = ref × (index/100) × Skalierung`` und ``cost`` exakt wie im
   Produkt (``risk_engine``): pop → pop/100000, area → area/50, flat → 1;
   monetäre Risiken sind bereits €, sonst × Kostensatz.

Jeder Wert trägt seine Treiber + Quellen-Keys im ``drivers``-JSON (Transparenz).
"""
from __future__ import annotations

from app.data import catalog
from app.data.germany_climate_reference import GERMANY_CLIMATE_REFERENCE

# Die 8 Lite-Risiken (aus den 14 Priorität-1-Risiken; Plan §3-Tabelle).
# M0-Verschlankung: geparkte Codes werden herausgefiltert, damit Admin-Batch
# und Scoring nicht auf fehlende Katalog-Einträge laufen; die Deutschland-
# Karte ist ohnehin offline (frontend FEATURES.deutschlandKarte). Mit der
# Re-Expansion (Stage 1+) wächst die Liste automatisch wieder mit.
LITE_RISK_CODES = [c for c in [
    "EXPECTED_ANNUAL_MORTALITY",
    "EXPECTED_ANNUAL_MORBIDITY",
    "EXPECTED_THERMAL_STRESS_HOURS",
    "EXPECTED_BUILDING_DAMAGE_EUR",
    "EXPECTED_WATER_WASTEWATER_DAMAGE_EUR",
    "EXPECTED_ANNUAL_AFFECTED_EVACUATED",
    "EXPECTED_AGRICULTURAL_DAMAGE_EUR",
    "HYDROLOGICAL_STRESS_RISK_INDEX",
] if c in catalog.RISKS_BY_CODE]

# Nationale Referenzen (für Treiber-Normierung + Anzeige).
_HOT_MEAN = GERMANY_CLIMATE_REFERENCE["hot_days"]["value"]          # 8.8
_SUMMER_MEAN = GERMANY_CLIMATE_REFERENCE["summer_days"]["value"]    # 43.5
_PRECIP_MEAN = GERMANY_CLIMATE_REFERENCE["precipitation_mm"]["value"]  # 791

_REF_POP = 100_000.0
_REF_AREA_KM2 = 50.0


def _norm(v: float | None, lo: float, hi: float) -> float:
    if v is None or hi <= lo:
        return 0.0
    return max(0.0, min(1.0, (v - lo) / (hi - lo)))


def _norm_inv(v: float | None, lo: float, hi: float) -> float:
    """Invertiert: niedrige Werte → hoch (z. B. altes Baujahr = verwundbar)."""
    if v is None:
        return 0.5
    return 1.0 - _norm(v, lo, hi)


def compute_raw(g: dict, dwd: dict, socio: dict | None = None) -> dict[str, dict]:
    """Roh-Scores + Treiber je Risiko für eine Gemeinde.

    ``g``: {population, area_km2, demographics{share_over_65, share_under_18,
    buildings, mean_building_year}}. ``dwd``: {hot_days, summer_days,
    precipGE20mm_days, precipGE30mm_days, precipitation}. ``socio``: INKAR-
    Indizes (0..100, optional).
    """
    demo = g.get("demographics") or {}
    pop = float(g.get("population") or 0.0)
    area = float(g.get("area_km2") or 1.0) or 1.0
    dens = pop / area  # Einw./km² (UHI-/Netz-Proxy)
    o65 = demo.get("share_over_65")
    u18 = demo.get("share_under_18")
    buildings = float(demo.get("buildings") or 0.0)
    byear = demo.get("mean_building_year")

    hot = dwd.get("hot_days")
    summer = dwd.get("summer_days")
    p20 = dwd.get("precipGE20mm_days")
    p30 = dwd.get("precipGE30mm_days")
    precip = dwd.get("precipitation")
    deficit = max(0.0, _PRECIP_MEAN - precip) if precip is not None else None

    # Normierte Komponenten (0..1)
    H_hot = _norm(hot, 2.0, 20.0)
    H_heat = _norm((hot or 0) + 0.3 * (summer or 0), 2.0, 32.0)
    H_p30 = _norm(p30, 0.0, 3.0)
    H_p20 = _norm(p20, 0.5, 6.0)
    H_dry = _norm(deficit, 0.0, 300.0) if deficit is not None else 0.4
    H_agrar = 0.6 * H_dry + 0.4 * _norm(summer, 25.0, 60.0)

    E_dens = _norm(dens, 50.0, 2000.0)
    E_build = _norm(buildings, 100.0, 30000.0)
    E_farmland = _norm(area - pop / 5000.0, 1.0, 200.0)  # Nicht-Siedlungsfläche

    V_old = _norm(o65, 0.12, 0.35)
    V_vuln = _norm((o65 or 0) + (u18 or 0), 0.25, 0.55)
    V_byear = _norm_inv(byear, 1950.0, 2010.0)
    V_socio = _norm(100.0 - (socio.get("financial", 50.0) if socio else 50.0), 0.0, 100.0)

    def entry(raw, drivers):
        return {"raw": round(max(0.0, raw), 6), "drivers": drivers}

    out: dict[str, dict] = {}
    out["EXPECTED_ANNUAL_MORTALITY"] = entry(
        H_hot * (0.5 + 0.5 * E_dens) * (0.4 + 0.6 * V_old),
        {"hot_days": hot, "population": int(pop), "share_over_65": o65,
         "source_refs": ["DWD_CDC", "Zensus2022", "UBA_KWRA"]})
    out["EXPECTED_ANNUAL_MORBIDITY"] = entry(
        H_hot * (0.5 + 0.5 * E_dens) * (0.4 + 0.6 * V_vuln),
        {"hot_days": hot, "population": int(pop), "share_vulnerable": round((o65 or 0) + (u18 or 0), 3),
         "source_refs": ["DWD_CDC", "Zensus2022", "UBA_KWRA"]})
    out["EXPECTED_THERMAL_STRESS_HOURS"] = entry(
        H_heat * (0.3 + 0.7 * E_dens) * (0.5 + 0.5 * V_old),
        {"hot_days": hot, "summer_days": summer, "pop_density": round(dens, 1),
         "source_refs": ["DWD_CDC", "Zensus2022"]})
    out["EXPECTED_BUILDING_DAMAGE_EUR"] = entry(
        H_p30 * (0.3 + 0.7 * E_build) * (0.5 + 0.5 * V_byear),
        {"precipGE30mm_days": p30, "buildings": int(buildings), "mean_building_year": byear,
         "source_refs": ["DWD_CDC", "Zensus2022"]})
    out["EXPECTED_WATER_WASTEWATER_DAMAGE_EUR"] = entry(
        H_p20 * (0.4 + 0.6 * E_dens) * (0.5 + 0.5 * V_socio),
        {"precipGE20mm_days": p20, "population": int(pop),
         "source_refs": ["DWD_CDC", "Zensus2022", "BBSR_INKAR"]})
    out["EXPECTED_ANNUAL_AFFECTED_EVACUATED"] = entry(
        H_p30 * (0.4 + 0.6 * E_dens) * (0.4 + 0.6 * V_vuln),
        {"precipGE30mm_days": p30, "population": int(pop),
         "source_refs": ["DWD_CDC", "Zensus2022"]})
    out["EXPECTED_AGRICULTURAL_DAMAGE_EUR"] = entry(
        H_agrar * (0.3 + 0.7 * E_farmland),
        {"precip_deficit_mm": round(deficit, 1) if deficit is not None else None,
         "summer_days": summer, "area_km2": area,
         "source_refs": ["DWD_CDC", "UFZ_Duerremonitor"]})
    out["HYDROLOGICAL_STRESS_RISK_INDEX"] = entry(
        H_dry * (0.6 + 0.4 * _norm(area, 5.0, 300.0)),
        {"precip_deficit_mm": round(deficit, 1) if deficit is not None else None, "area_km2": area,
         "source_refs": ["DWD_CDC", "BfG_PEGELONLINE"]})
    return out


def _percentile(sorted_vals: list[float], pct: float) -> float:
    if not sorted_vals:
        return 0.0
    k = (len(sorted_vals) - 1) * pct / 100.0
    f = int(k)
    c = min(f + 1, len(sorted_vals) - 1)
    if f == c:
        return sorted_vals[f]
    return sorted_vals[f] + (k - f) * (sorted_vals[c] - sorted_vals[f])


def normalize_index(raw_by_risk: dict[str, list[float]]) -> dict[str, tuple[float, float]]:
    """p5/p95 je Risiko über alle Gemeinden → (lo, hi) für die Index-Skalierung."""
    bounds: dict[str, tuple[float, float]] = {}
    for code, vals in raw_by_risk.items():
        sv = sorted(v for v in vals if v is not None)
        lo = _percentile(sv, 5.0)
        hi = _percentile(sv, 95.0)
        bounds[code] = (lo, hi if hi > lo else lo + 1e-6)
    return bounds


def raw_to_index(raw: float, bounds: tuple[float, float]) -> float:
    lo, hi = bounds
    return round(max(0.0, min(100.0, (raw - lo) / (hi - lo) * 100.0)), 1)


def outcome_and_cost(risk_code: str, index: float, pop: float, area_km2: float) -> tuple[float, float, str]:
    """(outcome, cost_eur, unit) — spiegelt ``risk_engine`` (scale/ref/Kostensatz)."""
    risk = catalog.RISKS_BY_CODE[risk_code]
    ref = float(risk.get("ref_value", 0.0))
    scale = risk.get("scale", "pop")
    if scale == "pop":
        factor = (pop or 0.0) / _REF_POP
    elif scale == "area":
        factor = (area_km2 or 0.0) / _REF_AREA_KM2
    else:
        factor = 1.0
    outcome = ref * (index / 100.0) * factor
    if catalog.risk_is_monetary(risk):
        cost = outcome
    else:
        cost = outcome * catalog.risk_default_cost_per_outcome(risk)
        # flat-Index-Risiken kommunenweit auf Bevölkerung skalieren (wie Engine)
        if scale not in ("pop", "area") and pop:
            cost *= pop / _REF_POP
    return round(outcome, 3), round(cost, 2), risk.get("outcome_unit", "")
