"""Tests der Gesundheits-Schadensfunktionen (Schicht B).

Deckt ab:
  (a) Deterministische Einzelzell-Handrechnung je Funktion.
  (b) Kalibrierung der Hitzemortalität gegen die nationale RKI-Jahresreihe.
  (c) **Altersverteilung** — der eigentliche Prüfstein der Altersschichtung: Die
      Gesamtzahl lässt sich über den Kalibrierfaktor immer treffen, die Verteilung
      über die Altersbänder nur, wenn die Wirkungskurven je Band stimmen.
  (d) Nichtlinearität/Schwellenwirkung der Expositions-Wirkungs-Kurve.
  (e) Unabhängige Gegenprobe des ΔT-Modells über den Wärmeinsel-Anteil.
  (f) Flutregime trennt Sturzflut von langsamem Anstieg um Größenordnungen.
  (g) Verletzte sind je Gefahr getrennt und ADDIEREN sich (früher: max()).
  (h) Registry, Overrides, Abdeckung, Sanity-Anker.

Läuft mit pytest oder direkt: ``python tests/test_impact_health.py``.
"""

from __future__ import annotations

from math import exp

from app.data import catalog, catalog_parked
from app.data import germany_health_reference as ghr
from app.services import parameter_registry
from app.services.engine import impact, override_context
from app.services.engine.impact import health as H
from app.services.engine.impact.base import CellContext

MORT = "EXPECTED_ANNUAL_MORTALITY"
MORT_FLOOD = "EXPECTED_ANNUAL_MORTALITY_FLOOD"
MORT_STORM = "EXPECTED_ANNUAL_MORTALITY_STORM"
INJ_FLOOD = "EXPECTED_ANNUAL_INJURIES"
INJ_STORM = "EXPECTED_ANNUAL_INJURIES_STORM"
INJ_SLIDE = "EXPECTED_ANNUAL_INJURIES_LANDSLIDE"
HEALTH = list(H.HEALTH_IMPACTS)

# M0-Verschlankung (docs/ROADMAP.md §5): Nur MORT/MORBIDITY sind aktiv; die übrigen
# 9 Gesundheits-Schadensfunktionen bleiben in der Registry (bewusst unangetastet)
# und werden hier mit den GEPARKTEN Risiko-Definitionen direkt aufgerufen —
# compute_all_cell_impacts dispatcht nur über catalog.RISKS.
_PARKED_BY_CODE = {r["code"]: r for r in catalog_parked._PARKED_RISKS}


def _risk(code: str) -> dict:
    return catalog.RISKS_BY_CODE.get(code) or _PARKED_BY_CODE[code]


def _outcome(code: str, ctx: CellContext) -> float:
    """Outcome einer (auch geparkten) Gesundheitsfunktion — Registry-Direktaufruf."""
    return H.HEALTH_IMPACTS[code](_risk(code), ctx)["outcome"]

# Bundesweite Altersstruktur (aus dem Zensus-100-m-Gitter aggregiert).
SHARE_65P = 0.2186
SENIOR_SPLIT = {"a65_74": 0.5003, "a75_84": 0.3555, "a85p": 0.1442}


def _bands(pop: float) -> dict[str, float]:
    out = {b: pop * SHARE_65P * f for b, f in SENIOR_SPLIT.items()}
    out["u65"] = pop * (1.0 - SHARE_65P)
    return out


def _abs(code: str, frac: float) -> float:
    """Absoluter Hazard-Wert, der über die Katalog-Referenzgrenzen auf ``frac``
    normiert. Geparkte Hazards fehlen in INDICATOR_BY_CODE — ``haz_intensity``
    fällt dann (wie die Engine selbst) auf die Grenzen 0..1 zurück."""
    m = catalog.INDICATOR_BY_CODE.get(code, {})
    lo = float(m.get("norm_min", 0.0))
    hi = float(m.get("norm_max", 1.0))
    return lo + frac * (hi - lo)


def _ctx(pop=100_000.0, summer_temp=19.0, hd=20.0, flood_norm=0.3, vnorm=0.5,
         event_norm=0.3, slope=0.2, depression=0.3, bundesland="Nordrhein-Westfalen",
         uhi_mean=0.0, **ci_extra):
    hn = {"hazards": {"HEAVY_RAIN_FLOOD": flood_norm, "EXTRATROPICAL_STORM": 0.4,
                      "LANDSLIDE": 0.1, "STORM_SURGE": 0.0, "WILDFIRE": 0.0,
                      "COMPOUND_EVENT": event_norm, "CASCADE_EVENT": event_norm,
                      "DROUGHT": 0.33},
          "exposures": {}, "vulnerabilities": {}}
    # Absolute Werte konsistent zu den (Fallback-)Grenzen von haz_intensity;
    # HEAT_WAVE bleibt absolut (Hitzetage), weil die Hitzefunktionen ctx.haz lesen.
    hev = {"hazards": {"HEAT_WAVE": hd,
                       **{c: _abs(c, f) for c, f in hn["hazards"].items()}},
           "exposures": {}, "vulnerabilities": {}}
    # Vulnerabilitäts-Normwerte auch für die geparkten Risiken setzen — deren
    # Funktionen (Flut/Sturm/…) lesen z. B. EARLY_WARNING_SYSTEMS weiter.
    for r in list(catalog.RISKS) + catalog_parked._PARKED_RISKS:
        for v in r["vulnerabilities"]:
            hn["vulnerabilities"][v] = vnorm
    ci = {"pop": pop, "summer_temp_cell": summer_temp, "pop_age_bands": _bands(pop),
          "slope_factor": slope, "depression_factor": depression,
          "uhi_delta_mean": uhi_mean, "canopy_frac": 0.1, "forest_frac": 0.05,
          "road_cov": 0.15}
    ci.update(ci_extra)
    return CellContext(ci=ci, hev=hev, hev_norm=hn, indices={},
                       regional={"bundesland": bundesland})


# ── (a) Handrechnung ───────────────────────────────────────────────────────────

def test_mortality_matches_hand_calc():
    """Rev. 7 (Bericht #95 §3.3/§3.5): YLL nativ, Todesfälle als Teil-Ausweis."""
    override_context.set_overrides({})
    ctx = _ctx(pop=100_000.0, summer_temp=19.0, vnorm=0.5)
    region = "mitte"
    thr, b85 = H.REGION_THRESHOLD[region], H.REGION_BETA_85P[region]
    temps = H.weekly_temperatures(19.0, region)
    exp_deaths, exp_yll = 0.0, 0.0
    for band in H.AGE_BANDS:
        pop_a = _bands(100_000.0)[band]
        m_a = ghr.BASELINE_MORTALITY_PER_100K[band]
        beta = b85 * H.AGE_BETA_FACTOR[band]
        exc = sum(exp(beta * max(0.0, t - thr)) - 1.0 for t in temps)
        # v_vers = 1 (keine Zellwerte für q_1P/q_pfl → Bundesmittel, §3.3)
        d_a = 0.581 * pop_a * (m_a / 100_000.0) * (1 / 52) * exc
        exp_deaths += d_a
        exp_yll += d_a * H.AGE_LIFE_YEARS[band]
    got = impact.compute_all_cell_impacts(ctx)[MORT]
    assert abs(got["outcome"] - exp_yll) < 1e-6
    assert abs(got["deaths"] - exp_deaths) < 1e-6
    # €-Bewertung: YLL × VOLY (160.800 €₂₀₂₄)
    assert abs(got["cost_eur"] - exp_yll * 160_800.0) < 1e-3


# ── (b) Nationale Kalibrierung gegen die RKI-Jahresreihe ──────────────────────

def test_heat_mortality_national_sum_in_rki_band():
    """Bundesweite Hochrechnung muss im Band der publizierten RKI-Jahre liegen.

    Bezugsgröße ist die bevölkerungsgewichtete Sommermitteltemperatur (19,01 °C,
    aus dem DWD-Monatsraster über 208.622 besiedelte 1-km-Zellen bestimmt) — NICHT
    das Flächenmittel von 18,55 °C: Menschen wohnen in den wärmeren Lagen, und die
    Wirkungskurve ist konvex.
    """
    override_context.set_overrides({})
    # Rev. 7: bevölkerungsgewichtetes DE-Sommermittel = Flächenmittel + 0,53 K
    # (gemessen, Bericht #95 §4 #t-povw) ≈ 19,08 °C. Geprüft wird der
    # Todesfälle-Teil-Ausweis (das RKI-Band ist in Todesfällen definiert).
    ctx = _ctx(pop=82_570_995.0, summer_temp=19.08, vnorm=0.5)
    total = impact.compute_all_cell_impacts(ctx)[MORT]["deaths"]
    lo, hi = ghr.heat_deaths_reference_band()
    assert lo <= total <= hi, (
        f"Bundessumme {total:.0f} liegt außerhalb des RKI-Bands {lo:.0f}–{hi:.0f}")


def test_heat_mortality_age_distribution_matches_rki():
    """Die modellierte Altersverteilung muss die publizierte RKI-Verteilung treffen.

    Das ist der Test, der die Altersschichtung trägt: Über den Kalibrierfaktor
    lässt sich jede Gesamtzahl erreichen, die Verteilung über die vier Bänder aber
    nur mit korrekten bandspezifischen Kurvensteigungen.
    """
    override_context.set_overrides({})
    region = "mitte"
    thr, b85 = H.REGION_THRESHOLD[region], H.REGION_BETA_85P[region]
    temps = H.weekly_temperatures(19.08, region)
    bands = _bands(82_570_995.0)
    per = {}
    for band in H.AGE_BANDS:
        beta = b85 * H.AGE_BETA_FACTOR[band]
        exc = sum(exp(beta * max(0.0, t - thr)) - 1.0 for t in temps)
        per[band] = bands[band] * (ghr.BASELINE_MORTALITY_PER_100K[band] / 1e5) * (1 / 52) * exc
    total = sum(per.values())
    # Toleranz ±5 Prozentpunkte — im Bericht #95 §4 vorab fixiert (Ist < 1 pp).
    for band, ref in ghr.HEAT_DEATH_AGE_SHARES.items():
        got = per[band] / total
        assert abs(got - ref) < 0.05, (
            f"{band}: Modell {got:.1%} vs. RKI {ref:.1%} — Abweichung > 5 Prozentpunkte")


# ── (c) Schwellenwirkung / Nichtlinearität ────────────────────────────────────

def test_mortality_is_superlinear_in_temperature():
    """Über der Wirkschwelle wächst die Mortalität überproportional mit der Temperatur."""
    override_context.set_overrides({})
    o = {t: impact.compute_all_cell_impacts(_ctx(summer_temp=t))[MORT]["outcome"]
         for t in (18.0, 19.0, 20.0, 21.0)}
    assert o[19.0] - o[18.0] < o[20.0] - o[19.0] < o[21.0] - o[20.0]


def test_mortality_below_threshold_is_small_but_nonzero():
    """Weit unter der Schwelle bleibt ein kleiner Rest — die heißesten Wochen der
    Verteilung überschreiten sie auch dann noch. Genau deshalb wird über die
    Verteilung integriert und nicht am Mittelwert ausgewertet."""
    override_context.set_overrides({})
    cold = impact.compute_all_cell_impacts(_ctx(summer_temp=14.0))[MORT]["outcome"]
    warm = impact.compute_all_cell_impacts(_ctx(summer_temp=20.0))[MORT]["outcome"]
    assert 0.0 <= cold < 0.05 * warm


# ── (d) Gegenprobe des ΔT-Modells über den Wärmeinsel-Anteil ──────────────────

def test_uhi_attributable_share_plausible():
    """Unabhängige Prüfung des ΔT-Modells, getrennt von der Wirkungskurve.

    Iungman u. a. 2023 rechnen 4,33 % [3,37; 5,27] **aller sommerlichen
    Sterbefälle** europäischer Städte der Wärmeinsel zu. Entscheidend ist der
    Nenner: nicht die hitzeattributablen Toten, sondern alle Sommertoten. Geprüft
    wird eine dichte Innenstadtzelle, für die ``compute_uhi_components`` einen
    24-h-Zuschlag von rund 1,5–2 K liefert.
    """
    override_context.set_overrides({})
    base_t, uhi = 19.08, 1.5
    # Der Iungman-Anteil ist in TODESFÄLLEN definiert — Teil-Ausweis nutzen.
    without = impact.compute_all_cell_impacts(_ctx(summer_temp=base_t))[MORT]["deaths"]
    with_uhi = impact.compute_all_cell_impacts(
        _ctx(summer_temp=base_t + uhi))[MORT]["deaths"]

    bands = _bands(100_000.0)
    summer_all = sum(bands[b] * ghr.BASELINE_MORTALITY_PER_100K[b] / 1e5
                     for b in H.AGE_BANDS) * (13 / 52)
    share = (with_uhi - without) / summer_all

    ref = ghr.UHI_ATTRIBUTABLE_SHARE_REFERENCE
    assert 0.5 * ref["min"] < share < 2.0 * ref["max"], (
        f"Der Wärmeinsel zurechenbarer Anteil {share:.2%} liegt außerhalb der "
        f"Größenordnung von Iungman u. a. 2023 ({ref['min']:.2%}–{ref['max']:.2%})")


# ── (e) Flutregime ────────────────────────────────────────────────────────────

def test_flood_regime_separates_flash_from_slow():
    """Sturzflut-Gelände und flache Aue müssen um Größenordnungen auseinanderliegen.

    Das ist der einzige Effekt, den das Flutmodell ohne Hydraulik belastbar
    abbildet — und der Unterschied, der Ahr 2021 von Elbe 2002 trennt.
    """
    override_context.set_overrides({})
    flat = _outcome(MORT_FLOOD, _ctx(slope=0.02, depression=0.1))
    steep = _outcome(MORT_FLOOD, _ctx(slope=1.0, depression=1.0))
    assert steep > 20 * flat, f"Regime-Spreizung zu gering: {steep:.4f} vs {flat:.4f}"


def test_flood_mortality_zero_without_hazard():
    override_context.set_overrides({})
    assert _outcome(MORT_FLOOD, _ctx(flood_norm=0.0)) == 0.0


def test_warning_reduces_flood_mortality():
    """Frühwarnung ist der Hebel, den eine Kommune bedienen kann — er muss wirken."""
    override_context.set_overrides({})
    poor = _outcome(MORT_FLOOD, _ctx(vnorm=1.0))
    good = _outcome(MORT_FLOOD, _ctx(vnorm=0.0))
    assert good < poor


# ── (f) Verletzte: getrennt und additiv ───────────────────────────────────────

def test_injuries_are_split_and_additive():
    """Verletzte aus Flut und Sturm addieren sich — früher lieferte ein max() nur
    die schlimmere der beiden Gefahren und unterschätzte Mehrgefahren-Kommunen."""
    override_context.set_overrides({})
    ctx = _ctx()
    flood, storm, slide = (_outcome(c, ctx) for c in (INJ_FLOOD, INJ_STORM, INJ_SLIDE))
    assert flood > 0 and storm > 0
    total = flood + storm + slide
    assert total > max(flood, storm, slide), "Summe muss über dem Maximum liegen"


def test_injury_channels_follow_their_own_hazard():
    override_context.set_overrides({})
    ctx = _ctx(flood_norm=0.0)
    assert _outcome(INJ_FLOOD, ctx) == 0.0
    assert _outcome(INJ_STORM, ctx) > 0.0, "Sturm darf nicht an der Flut hängen"


# ── (g) Registry / Overrides ──────────────────────────────────────────────────

def test_registry_emits_impact_params():
    params = parameter_registry.catalog_parameters(
        layer_code=MORT, layer_category="risks")
    ids = {p["id"] for p in params}
    for key in ("baseline_mort_a85p", "beta_85p_mitte", "threshold_mitte",
                "calibration", "beta_iso", "beta_pfl", "qbar_1p", "qbar_pfl",
                "life_years_a85p"):
        assert f"risks.{MORT}.impact.{key}" in ids, key
    beta = next(p for p in params if p["id"].endswith(".impact.beta_85p_mitte"))
    assert beta["editable"] is True
    assert beta["references"], "Impact-Parameter muss belegte Quelle tragen"


def test_call_site_defaults_match_registry_specs():
    """Registry-Spec und Call-Site-Default müssen denselben Wert tragen.

    ``ctx.p(code, key, default)`` liest den Default aus dem Funktionsaufruf, NICHT
    aus ``IMPACT_PARAM_SPECS`` — die Registry verdrahtet ihn nicht automatisch.
    Laufen beide auseinander, rechnet die Engine still mit einem anderen Wert als
    dem, den die Konfigurations-UI und der Parameter-Export anzeigen. Genau das ist
    beim Kalibrierfaktor der Hitzemortalität einmal passiert.
    """
    from app.services.engine.impact import params as pspec

    mismatches = []
    for spec in pspec.IMPACT_PARAM_SPECS:
        risk, key, value = spec["risk"], spec["key"], spec["value"]
        if risk not in H.HEALTH_IMPACTS:
            continue
        override_context.set_overrides({})
        without = _outcome(risk, _ctx())
        override_context.set_overrides({f"risks.{risk}.impact.{key}": value})
        with_spec = _outcome(risk, _ctx())
        if abs(without - with_spec) > 1e-9:
            mismatches.append(
                f"{risk}.{key}: Registry-Wert {value} ergibt {with_spec:.6f}, "
                f"Call-Site-Default ergibt {without:.6f}")
    override_context.set_overrides({})
    assert not mismatches, "Default-Drift zwischen Code und Registry:\n  " + "\n  ".join(mismatches)


def test_impact_param_override_changes_outcome():
    override_context.set_overrides({})
    base = impact.compute_all_cell_impacts(_ctx())[MORT]["outcome"]
    override_context.set_overrides({f"risks.{MORT}.impact.calibration": 1.162})
    doubled = impact.compute_all_cell_impacts(_ctx())[MORT]["outcome"]
    override_context.set_overrides({})
    assert abs(doubled - 2.0 * base) < 1e-6


def test_v_vers_modifier_bandwise_and_centered():
    """v_vers (Rev. 7, Bericht #95 §3.3): bandweise, mittelwertzentriert, nur D-Pfad.

    Golden-Werte aus dem Bericht (beispiel_95_or_uebersetzungen): 85+-Zelle ohne
    Heim ⇒ ×0,77; q_pfl = 0,30 ⇒ ×1,23. Ohne Zellwerte rechnet die Zelle mit dem
    Bundesmittel (Faktor exakt 1) — und der frühere pauschale g(V̂)-Ersatz über
    HEALTHCARE_ACCESS ist entfallen (vnorm darf die Mortalität nicht mehr ändern).
    """
    override_context.set_overrides({})
    base = impact.compute_all_cell_impacts(_ctx())[MORT]["outcome"]

    # (1) Zentrierung: Zellwerte exakt auf Bundesmittel ⇒ identisches Ergebnis.
    centered = impact.compute_all_cell_impacts(
        _ctx(share_single_65p=0.346, share_care_home_85p=0.149))[MORT]["outcome"]
    assert abs(centered - base) < 1e-9

    # (2) 85+-Zelle ohne Heim: nur das 85+-Band skaliert mit 1 + 1,54·(0−0,149) = 0,77.
    pop = 100_000.0
    only85 = {"u65": 0.0, "a65_74": 0.0, "a75_84": 0.0, "a85p": pop * 0.03}
    b0 = impact.compute_all_cell_impacts(
        _ctx(pop_age_bands=only85))[MORT]["outcome"]
    no_home = impact.compute_all_cell_impacts(
        _ctx(pop_age_bands=only85, share_care_home_85p=0.0))[MORT]["outcome"]
    many = impact.compute_all_cell_impacts(
        _ctx(pop_age_bands=only85, share_care_home_85p=0.30))[MORT]["outcome"]
    assert abs(no_home / b0 - (1 + 1.54 * (0.0 - 0.149))) < 0.005
    assert abs(many / b0 - (1 + 1.54 * (0.30 - 0.149))) < 0.005

    # (3) β_iso wirkt nicht auf u65 (Bandzuordnung 65+).
    only_u65 = {"u65": pop, "a65_74": 0.0, "a75_84": 0.0, "a85p": 0.0}
    u0 = impact.compute_all_cell_impacts(_ctx(pop_age_bands=only_u65))[MORT]["outcome"]
    u1 = impact.compute_all_cell_impacts(
        _ctx(pop_age_bands=only_u65, share_single_65p=0.9))[MORT]["outcome"]
    assert abs(u1 - u0) < 1e-9

    # (4) Kein pauschaler Versorgungsmodifikator mehr.
    low = impact.compute_all_cell_impacts(_ctx(vnorm=0.0))[MORT]["outcome"]
    high = impact.compute_all_cell_impacts(_ctx(vnorm=1.0))[MORT]["outcome"]
    assert abs(high - low) < 1e-9


def test_region_thresholds_differ():
    """Nord reagiert früher als Süd — bei gleicher Temperatur mehr Sterbefälle."""
    override_context.set_overrides({})
    nord = impact.compute_all_cell_impacts(
        _ctx(bundesland="Schleswig-Holstein"))[MORT]["outcome"]
    sued = impact.compute_all_cell_impacts(_ctx(bundesland="Bayern"))[MORT]["outcome"]
    assert nord > sued


# ── (h) Abdeckung + Sanity ────────────────────────────────────────────────────

def test_all_health_risks_registered():
    # 13 seit der #98-Integration (UV-YLL); davor 12 mit #96 (Symptomtage).
    assert len(HEALTH) == 13
    for code in HEALTH:
        assert impact.has(code), code


def test_sanity_ratio_in_tolerance():
    from app.services.engine.impact import sanity
    override_context.set_overrides({})
    ctx = _ctx(pop=100_000.0)
    for code in HEALTH:
        # sanity.check schaut nur in catalog.RISKS (für geparkte Codes: None) —
        # dieselbe Rechnung hier direkt über ref_estimate mit dem (ggf. geparkten)
        # Risiko-Dict, damit der 5×-Anker für alle 11 Funktionen geprüft bleibt.
        est = sanity.ref_estimate(_risk(code), 100_000.0, 50.0)
        ratio = None if est <= 0.0 else round(_outcome(code, ctx) / est, 3)
        assert ratio is None or (1.0 / sanity.TOLERANCE) <= ratio <= sanity.TOLERANCE, (code, ratio)


if __name__ == "__main__":
    import sys
    import pytest
    sys.exit(pytest.main([__file__, "-q"]))
