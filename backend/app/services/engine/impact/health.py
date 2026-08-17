"""Gesundheits-Schadensfunktionen (Schicht B, Stufe 4 — MODELL_KRITIK §6.1).

Zwei verschiedene Bauarten, weil die Gefahren verschieden funktionieren:

**Hitze — chronisch und flächig.** Die Mortalität folgt der publizierten
Expositions-Wirkungs-Kurve des RKI (Winklmayr u. a. 2022): relatives Sterberisiko
über der **Wochenmitteltemperatur**, geschichtet nach vier Altersbändern und drei
Regionen mit eigenen Wirkschwellen (19,7/20,2/20,8 °C). Entscheidend ist, dass die
Kurve **über die Verteilung** der Sommerwochen integriert wird und nicht am
Mittelwert ausgewertet: Das deutsche Sommermittel liegt bei rund 18,5 °C und damit
*unter* der Wirkschwelle — am Mittelwert ausgewertet käme fast überall null heraus.
Die Todesfälle entstehen in den wenigen heißen Wochen.

**Flut und Sturm — selten, geclustert, tail-lastig.** Zu wenige Ereignisse für eine
gefittete Kurve; Struktur daher ``Exposition × bedingte Letalität``, wobei die
Letalität aus der Loss-of-Life-Literatur kommt und nur ein Skalierungsfaktor
kalibriert wird. Der wichtigste Unterscheider bei Flut ist das **Regime**
(Sturzflut vs. langsamer Anstieg) — Ahr 2021 (>180 Tote) gegen Elbe 2002 (~21) bei
weit größerer überfluteter Fläche.

Alle Raten/Koeffizienten sind editierbare Registry-Parameter
(``impact/params.py``); nationale Kalibrier- und Validierungsanker stehen in
``app/data/germany_health_reference.py``.

Registrierung am Modulende: die Funktionen werden in ``impact.IMPACT_FUNCTIONS``
eingetragen; ``compute_all_cell_impacts`` verteilt darauf, sonst auf
``legacy_cell_impact``.
"""

from __future__ import annotations

from math import exp, log, sqrt

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


# ── Expositions-Wirkungs-Kurve Hitze (RKI / Winklmayr u. a. 2022) ─────────────

# Regionszuschnitt exakt wie in Winklmayr u. a. 2022.
REGION_BY_BUNDESLAND: dict[str, str] = {
    "Bremen": "nord", "Hamburg": "nord", "Mecklenburg-Vorpommern": "nord",
    "Niedersachsen": "nord", "Schleswig-Holstein": "nord",
    "Berlin": "mitte", "Brandenburg": "mitte", "Nordrhein-Westfalen": "mitte",
    "Rheinland-Pfalz": "mitte", "Saarland": "mitte", "Hessen": "mitte",
    "Sachsen": "mitte", "Sachsen-Anhalt": "mitte", "Thüringen": "mitte",
    "Baden-Württemberg": "sued", "Bayern": "sued",
}

# Wirkschwellen der Wochenmitteltemperatur je Region (°C), Winklmayr Abb. 3.
REGION_THRESHOLD: dict[str, float] = {"nord": 19.7, "mitte": 20.2, "sued": 20.8}

# Steigung der Kurve für das Band 85+ je Region (1/K), aus den publizierten
# Expositions-Wirkungs-Kurven für 2012–2021: RR ≈ 1,4 (Nord) / 1,35 (Mitte) /
# 1,25 (Süd) bei 25 °C, bezogen auf die jeweilige Schwelle.
REGION_BETA_85P: dict[str, float] = {"nord": 0.0634, "mitte": 0.0625, "sued": 0.0531}

# Steigung der übrigen Altersbänder relativ zu 85+. NICHT frei gewählt, sondern
# aus der publizierten Altersverteilung der hitzebedingten Sterbefälle
# zurückgerechnet: Für kleine β·Δ gilt Todesfälle_a ∝ pop_a · m_a · β_a, also
# β_a ∝ Anteil_a / (pop_a · m_a). Mit den RKI-Anteilen 2026 (6,5/12,9/25,2/55,5 %),
# der Zensus-Altersstruktur und den altersspezifischen Basissterberaten ergeben
# sich die folgenden Faktoren (Herleitung in germany_health_reference.py).
AGE_BETA_FACTOR: dict[str, float] = {
    "u65": 0.404, "a65_74": 0.577, "a75_84": 0.620, "a85p": 1.0,
}

AGE_BANDS: tuple[str, ...] = ("u65", "a65_74", "a75_84", "a85p")


def region_for(bundesland: str | None) -> str:
    return REGION_BY_BUNDESLAND.get(bundesland or "", "mitte")


def _norm_quantile(p: float) -> float:
    """Standardnormal-Quantil (inverse CDF), Acklam-Approximation."""
    p = min(max(p, 1e-9), 1 - 1e-9)
    a = (-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00)
    b = (-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01)
    c = (-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00)
    d = (7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00)
    plow, phigh = 0.02425, 1 - 0.02425
    if p < plow:
        q = sqrt(-2 * log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
               ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p > phigh:
        q = sqrt(-2 * log(1 - p))
        return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
                ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    q = p - 0.5
    r = q * q
    return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / \
           (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)


def weekly_temperatures(mean_temp: float, sd: float, n_weeks: int) -> list[float]:
    """Wochenmitteltemperaturen der Sommerwochen als deterministische Quantile.

    Die Wochenmittel des Sommers streuen um das Sommermittel ``mean_temp``. Statt
    zu simulieren werden die ``n_weeks`` Quantile der Normalverteilung genommen —
    reproduzierbar, ohne Zufall, und die oberen Quantile bilden genau die heißen
    Wochen ab, aus denen die Sterbefälle stammen.
    """
    if n_weeks <= 0 or sd <= 0:
        return [mean_temp] * max(0, n_weeks)
    return [mean_temp + sd * _norm_quantile((k + 0.5) / n_weeks) for k in range(n_weeks)]


def heat_excess_weeks(mean_temp: float, sd: float, n_weeks: int, threshold: float) -> float:
    """Übertemperatur-Wochen (K·Wochen) über der Wirkschwelle."""
    return sum(max(0.0, t - threshold) for t in weekly_temperatures(mean_temp, sd, n_weeks))


def _healthcare_modifier(ctx: CellContext, code: str) -> float:
    """Nicht-demografischer Zellmodifikator (Versorgungszugang).

    Ersetzt für die Mortalität bewusst ``g(V̂)``: Mit expliziten Altersbändern
    zählte ``g`` die Demografie ein zweites und drittes Mal, weil sowohl
    ``HEAT_SENSITIVITY`` als auch ``VULNERABLE_GROUPS_SHARE`` den
    Verwundbaren-Anteil enthalten (REVIEW_BERECHNUNGSLOGIK V-E). Hier geht
    ausschließlich der Gesundheitszugang ein; die Demografie steckt genau einmal
    in ``pop_a``.
    """
    span = ctx.p(code, "healthcare_modifier_span", 0.5)
    v = float(ctx.hev_norm.get("vulnerabilities", {}).get("HEALTHCARE_ACCESS", 0.5) or 0.0)
    return max(0.0, 1.0 - span / 2.0 + span * v)


def cell_summer_temp(ctx: CellContext) -> float:
    """Sommermitteltemperatur der Zelle (°C) mit dokumentierten Rückfällen."""
    t = ctx.ci.get("summer_temp_cell")
    if t is not None:
        return float(t)
    t = ctx.regional.get("summer_temp_mean")
    if t is not None:
        # Ohne zellscharfes Raster wenigstens den Wärmeinsel-Zuschlag ansetzen.
        return float(t) + float(ctx.ci.get("uhi_delta_mean") or 0.0)
    from app.services.engine.inputs import SUMMER_MAX_TO_MEAN_OFFSET_K
    return float(ctx.regional.get("summer_temp", 24.0)) - SUMMER_MAX_TO_MEAN_OFFSET_K


def _age_bands(ctx: CellContext) -> dict[str, float]:
    """Bevölkerung je Altersband; Rückfall über den 65+-Anteil der Zelle."""
    bands = ctx.ci.get("pop_age_bands")
    if isinstance(bands, dict) and bands:
        return {b: float(bands.get(b) or 0.0) for b in AGE_BANDS}
    from app.services.zensus_loader import NATIONAL_SENIOR_SPLIT
    pop = ctx.pop
    share_o = ctx.ci.get("share_over_65")
    if share_o is None:
        share_o = ctx.regional.get("demographics", {}).get("share_over_65", 22.0)
    pop_65p = pop * float(share_o) / 100.0
    return {
        "u65": max(0.0, pop - pop_65p),
        **{b: pop_65p * f for b, f in NATIONAL_SENIOR_SPLIT.items()},
    }


# ── 1. Hitzemortalität ─────────────────────────────────────────────────────────

def mortality(risk: dict, ctx: CellContext) -> dict:
    """Hitzebedingte Sterbefälle je Zelle und Jahr.

    ``D = calib · h · Σ_Band pop_a · m_a/100k · (1/52) · Σ_Woche (RR_a(T_w) − 1)``
    """
    from app.data.germany_health_reference import BASELINE_MORTALITY_PER_100K

    code = risk["code"]
    region = region_for(ctx.regional.get("bundesland"))

    thr = ctx.p(code, f"threshold_{region}", REGION_THRESHOLD[region])
    beta85 = ctx.p(code, f"beta_85p_{region}", REGION_BETA_85P[region])
    sd = ctx.p(code, "weekly_temp_sd", 2.0)
    n_weeks = int(ctx.p(code, "summer_weeks", 13))
    # ACHTUNG: Der Default muss mit dem Registry-Spec in impact/params.py
    # übereinstimmen — die Registry verdrahtet ihn NICHT automatisch hierher.
    calib = ctx.p(code, "calibration", 1.44)

    temps = weekly_temperatures(cell_summer_temp(ctx), sd, n_weeks)
    bands = _age_bands(ctx)

    outcome = 0.0
    for band in AGE_BANDS:
        pop_a = bands.get(band, 0.0)
        if pop_a <= 0.0:
            continue
        m_a = ctx.p(code, f"baseline_mort_{band}", BASELINE_MORTALITY_PER_100K[band])
        beta_a = beta85 * ctx.p(code, f"beta_factor_{band}", AGE_BETA_FACTOR[band])
        excess = sum(exp(beta_a * max(0.0, t - thr)) - 1.0 for t in temps)
        outcome += pop_a * (m_a / 100_000.0) * (1.0 / 52.0) * excess

    return _result(risk, outcome * calib * _healthcare_modifier(ctx, code))


# ── 2. Hitzemorbidität ─────────────────────────────────────────────────────────

def morbidity(risk: dict, ctx: CellContext) -> dict:
    code = risk["code"]
    rate = ctx.p(code, "rate_per_100k", 8000.0)
    af = _heat_af(ctx, code, 0.0016, 8.0)
    outcome = ctx.pop * (rate / 100_000.0) * af * ctx.g(risk)
    return _result(risk, outcome)


# ── 3. Todesfälle durch Hochwasser/Sturzfluten ────────────────────────────────

def flood_regime(ctx: CellContext) -> float:
    """Sturzflut-Anteil der Zelle (0 = langsamer Anstieg, 1 = Sturzflut).

    Ohne Hydraulik (keine Tiefe, keine Fließgeschwindigkeit) ist das Gelände der
    einzige belastbare Unterscheider — und zugleich der wichtigste: Enge Steiltäler
    erzeugen schnelle, tödliche Fluten, flache Auen langsame. Genau das trennt
    Ahr 2021 von Elbe 2002.
    """
    slope = float(ctx.ci.get("slope_factor", ctx.ci.get("slope_proxy", 0.0)) or 0.0)
    depression = float(ctx.ci.get("depression_factor", ctx.ci.get("depression_proxy", 0.0)) or 0.0)
    return max(0.0, min(1.0, slope * (0.5 + 0.5 * depression)))


def _warning_modifier(ctx: CellContext, code: str) -> float:
    """Warnzeit/Notfallmanagement — der Hebel, den eine Kommune bedienen kann."""
    span = ctx.p(code, "warning_modifier_span", 0.6)
    vn = ctx.hev_norm.get("vulnerabilities", {})
    v = max(float(vn.get("EARLY_WARNING_SYSTEMS", 0.5) or 0.0),
            float(vn.get("EMERGENCY_MANAGEMENT", 0.5) or 0.0))
    return max(0.0, 1.0 - span / 2.0 + span * v)


def _elderly_share(ctx: CellContext) -> float:
    bands = _age_bands(ctx)
    total = sum(bands.values())
    return (total - bands.get("u65", 0.0)) / total if total > 0 else 0.0


def mortality_flood(risk: dict, ctx: CellContext) -> dict:
    code = risk["code"]
    intensity = ctx.haz_intensity("HEAVY_RAIN_FLOOD")
    if intensity <= 0.0 or ctx.pop <= 0.0:
        return _result(risk, 0.0)

    rate_flash = ctx.p(code, "fatality_rate_flash_per_100k", 9.0)
    rate_slow = ctx.p(code, "fatality_rate_slow_per_100k", 0.15)
    regime = flood_regime(ctx)
    rate = rate_slow + regime * (rate_flash - rate_slow)

    # Flutopfer sind überproportional alt und mobilitätseingeschränkt.
    age_span = ctx.p(code, "elderly_weight", 1.5)
    age_mod = 1.0 + age_span * (_elderly_share(ctx) - 0.22)

    outcome = (ctx.pop * (rate / 100_000.0) * intensity
               * _warning_modifier(ctx, code) * max(0.0, age_mod)
               * ctx.p(code, "calibration", 1.0))
    return _result(risk, outcome)


# ── 4. Todesfälle durch Stürme ────────────────────────────────────────────────

def mortality_storm(risk: dict, ctx: CellContext) -> dict:
    code = risk["code"]
    intensity = ctx.haz_intensity("EXTRATROPICAL_STORM")
    if intensity <= 0.0 or ctx.pop <= 0.0:
        return _result(risk, 0.0)

    rate = ctx.p(code, "fatality_rate_per_100k", 0.35)
    # Sturmtote fallen draußen und unterwegs: umstürzende Bäume an Straßen sind
    # der dominierende Mechanismus. Deshalb die Interaktion Kronen×Straße —
    # keine der beiden Größen allein bildet ihn ab.
    canopy = float(ctx.ci.get("canopy_frac", 0.0) or 0.0) + float(ctx.ci.get("forest_frac", 0.0) or 0.0)
    road = float(ctx.ci.get("road_cov", 0.0) or 0.0)
    tree_road = max(0.0, min(1.0, canopy * road * ctx.p(code, "tree_road_scale", 8.0)))

    bldg_vuln = float(ctx.hev_norm.get("vulnerabilities", {}).get("BUILDING_STABILITY", 0.5) or 0.0)

    w_base = ctx.p(code, "base_share", 0.4)
    w_tree = ctx.p(code, "tree_share", 0.4)
    w_bldg = ctx.p(code, "building_share", 0.2)
    exposure = w_base + w_tree * tree_road + w_bldg * bldg_vuln

    outcome = (ctx.pop * (rate / 100_000.0) * intensity * exposure
               * ctx.p(code, "calibration", 1.0))
    return _result(risk, outcome)


# ── 5. Verletzte — je Gefahr getrennt ─────────────────────────────────────────
# Bis Modellversion 6 lief das über EIN Risiko mit ``max()`` über drei Gefahren.
# Das war nicht nur unsauber, sondern falsch: Flut- und Sturmverletzte sind
# additive Ereignisse; eine Kommune, die beidem ausgesetzt ist, bekommt Verletzte
# aus beidem. Das Maximum behauptete, sie bekomme nur die schlimmere von beiden,
# und die ``alternate_hazard``-Ketten trugen zum absoluten Outcome gar nichts bei.
# Die Raten zählen ausschließlich **nicht-tödliche** Verletzte (die Todesfälle
# stehen in eigenen Kanälen), damit nichts doppelt bewertet wird.

def _injuries(risk: dict, ctx: CellContext, hazard: str, default_rate: float) -> dict:
    code = risk["code"]
    rate = ctx.p(code, "rate_per_100k", default_rate)
    outcome = ctx.pop * (rate / 100_000.0) * ctx.haz_intensity(hazard) * ctx.g(risk)
    return _result(risk, outcome)


def injuries_flood(risk: dict, ctx: CellContext) -> dict:
    return _injuries(risk, ctx, "HEAVY_RAIN_FLOOD", 90.0)


def injuries_storm(risk: dict, ctx: CellContext) -> dict:
    return _injuries(risk, ctx, "EXTRATROPICAL_STORM", 55.0)


def injuries_landslide(risk: dict, ctx: CellContext) -> dict:
    return _injuries(risk, ctx, "LANDSLIDE", 5.0)


# ── 6. Psychische Gesundheit ───────────────────────────────────────────────────

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


# ── 7. Betroffene / Evakuierte (Flut/Sturmflut/Feuer) ──────────────────────────

def affected_evacuated(risk: dict, ctx: CellContext) -> dict:
    code = risk["code"]
    rate = ctx.p(code, "rate_per_100k", 2500.0)
    driver = max(ctx.haz_intensity("HEAVY_RAIN_FLOOD"),
                 ctx.haz_intensity("STORM_SURGE"),
                 ctx.haz_intensity("WILDFIRE"))
    outcome = ctx.pop * (rate / 100_000.0) * driver * ctx.g(risk)
    return _result(risk, outcome)


# ── 8. Wärmebelastungsstunden ──────────────────────────────────────────────────

def thermal_stress_hours(risk: dict, ctx: CellContext) -> dict:
    code = risk["code"]
    hours_ref = ctx.p(code, "hours_ref_per_100k", 400.0)
    ref_hd = ctx.p(code, "reference_hotdays", 20.0)
    hd = ctx.haz("HEAT_WAVE")
    driver = hd / ref_hd if ref_hd > 0 else 0.0
    outcome = (ctx.pop / 100_000.0) * hours_ref * driver * ctx.g(risk)
    return _result(risk, outcome)


# ── 9. Schadstoff-Belastungsstunden ────────────────────────────────────────────

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
    "EXPECTED_ANNUAL_MORTALITY_FLOOD": mortality_flood,
    "EXPECTED_ANNUAL_MORTALITY_STORM": mortality_storm,
    "EXPECTED_ANNUAL_MORBIDITY": morbidity,
    "EXPECTED_ANNUAL_INJURIES": injuries_flood,
    "EXPECTED_ANNUAL_INJURIES_STORM": injuries_storm,
    "EXPECTED_ANNUAL_INJURIES_LANDSLIDE": injuries_landslide,
    "EXPECTED_ANNUAL_MENTAL_HEALTH": mental_health,
    "EXPECTED_ANNUAL_AFFECTED_EVACUATED": affected_evacuated,
    "EXPECTED_THERMAL_STRESS_HOURS": thermal_stress_hours,
    "EXPECTED_POLLUTANT_EXPOSURE_HOURS": pollutant_exposure_hours,
}


# ── Lineage-Spezifikation (Wirkungsdiagramm) ───────────────────────────────────
# Deklariert je Risiko, was die Funktion oben rechnet, damit ``lineage_graph`` den
# Schicht-B-Zweig des Wirkungsdiagramms exakt aus der tatsächlichen Rechnung baut.
# Muss die Funktionskörper spiegeln (Key-Gleichheit wird in
# tests/test_lineage_graph.py geprüft).
LINEAGE_SPECS: dict[str, dict] = {
    "EXPECTED_ANNUAL_MORTALITY": {
        "rate_param": "baseline_mort_a85p",
        # Basis ist NICHT die Gesamtbevölkerung: die Kurve läuft je Altersband.
        "basis_key": "pop_age_bands",
        "basis_label": "Bevölkerung je Altersband (Zelle)",
        "driver": {"kind": "erf", "hazard": "HEAT_WAVE",
                   "params": ["weekly_temp_sd", "summer_weeks", "calibration"]},
        # Kein g(V̂): mit expliziten Altersbändern zählte es die Demografie ein
        # zweites und drittes Mal (siehe ``_healthcare_modifier``).
        "modifier": {
            "term": "Versorgungs-Modifikator",
            "label": "Versorgungszugang",
            "vulnerabilities": ["HEALTHCARE_ACCESS"],
            "params": ["healthcare_modifier_span"],
            "note": ("Ersetzt hier bewusst g(V̂): Die Demografie steckt bereits in den "
                     "Altersbändern, ein Vulnerabilitätsmittel würde sie ein zweites und "
                     "drittes Mal zählen (HEAT_SENSITIVITY und VULNERABLE_GROUPS_SHARE "
                     "enthalten beide den Verwundbaren-Anteil). Es geht ausschließlich der "
                     "Gesundheitszugang ein.\n"
                     r"$$h = 1 - \tfrac{s}{2} + s\,\hat{V}_{\mathrm{Versorgung}}$$"),
        },
    },
    "EXPECTED_ANNUAL_MORTALITY_FLOOD": {
        "rate_param": "fatality_rate_flash_per_100k",
        "driver": {"kind": "intensity", "hazards": ["HEAVY_RAIN_FLOOD"]},
        "modifier": {
            "term": "Warnung · Altersgewicht",
            "label": "Warnzeit & Altersgewicht",
            "vulnerabilities": ["EARLY_WARNING_SYSTEMS", "EMERGENCY_MANAGEMENT"],
            "params": ["warning_modifier_span", "elderly_weight", "calibration"],
            "note": ("Kein g(V̂), sondern die beiden Größen, die bei Fluttoten tatsächlich "
                     "entscheiden: die Vorwarnzeit — am Ahr 2021 der ausschlaggebende "
                     "Faktor und der Hebel, den eine Kommune bedienen kann — und der "
                     "Altersüberhang der Opfer.\n"
                     r"$$m = \bigl(1 - \tfrac{s}{2} + s\,\hat{V}_{\mathrm{Warn}}\bigr)"
                     r"\cdot \bigl(1 + a\,(\text{Anteil}_{65+} - 0{,}22)\bigr)$$"),
        },
    },
    "EXPECTED_ANNUAL_MORTALITY_STORM": {
        "rate_param": "fatality_rate_per_100k",
        "driver": {"kind": "intensity", "hazards": ["EXTRATROPICAL_STORM"]},
        "modifier": {
            "term": "Expositionsterm",
            "label": "Bäume × Straßen, Bausubstanz",
            "vulnerabilities": ["BUILDING_STABILITY"],
            "params": ["tree_road_scale", "base_share", "tree_share", "building_share",
                       "calibration"],
            "cell_keys": ["canopy_frac", "forest_frac", "road_cov"],
            "note": ("Sturmtote fallen draußen und unterwegs, nicht in der Wohnung. "
                     "Umstürzende Bäume an Straßen sind der dominierende Mechanismus — "
                     "deshalb die INTERAKTION Kronen×Straße: keine der beiden Größen "
                     "allein bildet ihn ab.\n"
                     r"$$e = w_{0} + w_{B}\,(\text{Kronen}\cdot\text{Straße})"
                     r" + w_{G}\,\hat{V}_{\mathrm{Bausubstanz}}$$"),
        },
    },
    "EXPECTED_ANNUAL_MORBIDITY": {
        "rate_param": "rate_per_100k",
        "driver": {"kind": "af", "hazard": "HEAT_WAVE",
                   "params": ["beta_per_hotday", "hotday_threshold"]},
    },
    "EXPECTED_ANNUAL_INJURIES": {
        "rate_param": "rate_per_100k",
        "driver": {"kind": "intensity", "hazards": ["HEAVY_RAIN_FLOOD"]},
    },
    "EXPECTED_ANNUAL_INJURIES_STORM": {
        "rate_param": "rate_per_100k",
        "driver": {"kind": "intensity", "hazards": ["EXTRATROPICAL_STORM"]},
    },
    "EXPECTED_ANNUAL_INJURIES_LANDSLIDE": {
        "rate_param": "rate_per_100k",
        "driver": {"kind": "intensity", "hazards": ["LANDSLIDE"]},
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
