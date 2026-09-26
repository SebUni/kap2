"""Hebel S157 — gekühlte Heimplätze (Bericht #95 §5, Beispiel-Block ``s157_berlin``).

Maßnahme ``COOLING_ROOMS_DRINKING_WATER`` ist aktiviert (T-1367) und wirkt mit
``ΔD_S157 = D_85+ · h_Heim · s_gek · (1 − g_S157)`` auf die Todesfälle 85+ der
Heimbewohner, bewertet mit L̄_85+ (YLL) × VOLY. s_gek ist die Eingabe der Kommune;
ohne Eingabe entsteht kein Betrag (auch keine 0).

Zusammen mit dem Hitzeaktionsplan (Befund 129) wirkt S157 auf den schon mit δ_HAP
gedämpften Heim-Exzess: Berlin zusammen 72,1 %, davon S157 35,5 Todesfälle oder
23,7 Mio. € je Jahr.

DB-frei: prüft die Rechenfunktion in ``health`` und den Zellfaktor der Maßnahmen-Engine
an einer Zelle mit den Berlin-Werten aus Kette 3.0 (D_85+ = 153,6; L̄_85+ = 4,16).
"""

from __future__ import annotations

import pytest

from app.data import catalog, catalog_parked
from app.services import measure_service, parameter_registry
from app.services.engine import impact, override_context, risk_engine, runner
from app.services.engine.impact import health
from app.services.engine.impact.base import CellContext

CODE = "COOLING_ROOMS_DRINKING_WATER"
MORT = "EXPECTED_ANNUAL_MORTALITY"
D85_BERLIN = 153.6       # Bericht #95 Kette 3.0, Ebene 6
L85 = 4.16               # Ebene 7


def _berlin_cell() -> dict:
    """Eine Zelle, die die Berliner Todesfälle 85+ trägt (YLL nur aus 85+ plus Rest)."""
    yll = D85_BERLIN * L85 + 1000.0   # übrige Bänder: beliebiger Sockel, bleibt unberührt
    return {"outcome": yll, "deaths_a85p": D85_BERLIN}


def _benefit_eur(s_gek, delta_hap: float = 1.0) -> float | None:
    risk = catalog.RISKS_BY_CODE[MORT]
    mdef = catalog.MEASURES_BY_CODE[CODE]
    cell = _berlin_cell()
    factor = measure_service._measure_cell_factor(
        mdef, {} if s_gek is None else {"s_gek": s_gek}, MORT, 1.0, 1.0, cell, delta_hap)
    fields = measure_service._s157_summary_fields(
        mdef, {} if s_gek is None else {"s_gek": s_gek})
    if fields.get("benefit_display"):
        assert factor == 1.0
        return None
    return risk_engine.cost_from_outcome(risk, cell["outcome"]) * (1.0 - factor)


def test_measure_is_active_not_parked():
    assert CODE in catalog.MEASURES_BY_CODE
    assert CODE not in {m["code"] for m in catalog_parked._PARKED_MEASURES}
    m = catalog.MEASURES_BY_CODE[CODE]
    assert m["effect_model"] == "s157"
    assert m["linked_risk_codes"] == [MORT]
    assert m["default_reduction"] is None   # keine 0.18 auf die Exposition mehr


def test_h_heim_and_g_from_report():
    assert health.h_heim() == pytest.approx(0.344, abs=0.001)
    assert D85_BERLIN * health.h_heim() == pytest.approx(52.9, abs=0.05)
    assert health.s157_avoided_deaths(D85_BERLIN, 1.0) == pytest.approx(37.4, abs=0.05)


def test_berlin_all_care_home_places_cooled_is_25_0_mio_eur():
    eur = _benefit_eur(1.0)
    assert round(eur / 1e6, 1) == 25.0
    assert eur / 1e6 == pytest.approx(25.0, abs=0.05)


def test_berlin_ten_percent_is_one_tenth():
    assert _benefit_eur(0.1) == pytest.approx(_benefit_eur(1.0) / 10.0, rel=1e-9)


def test_without_input_no_amount():
    assert health.s157_avoided_deaths(D85_BERLIN, None) is None
    assert _benefit_eur(None) is None
    fields = measure_service._s157_summary_fields(catalog.MEASURES_BY_CODE[CODE], {})
    assert fields["s_gek"] is None
    assert fields["benefit_display"] == measure_service.S157_NO_INPUT_TEXT
    assert fields["benefit_missing_input"] == "s_gek"


def test_only_mortality_and_old_cells_unchanged():
    mdef = catalog.MEASURES_BY_CODE[CODE]
    cfg = {"s_gek": 1.0}
    assert measure_service._measure_cell_factor(
        mdef, cfg, "EXPECTED_ANNUAL_MORBIDITY", 1.0, 1.0, {"outcome": 10.0}) == 1.0
    # Zelle vor der Neuberechnung (ohne Teil-Ausweis D_85+): keine Wirkung
    assert measure_service._measure_cell_factor(
        mdef, cfg, MORT, 1.0, 1.0, {"outcome": 10.0}) == 1.0


def test_real_path_stores_deaths_a85p_and_measure_acts():
    """Zelle über den echten Weg: Schadensfunktion → gespeichertes risks-Dict (runner)."""
    override_context.set_overrides({})
    pop = 100_000.0
    bands = {b: pop * 0.2186 * f for b, f in
             {"a65_74": 0.5003, "a75_84": 0.3555, "a85p": 0.1442}.items()}
    bands["u65"] = pop * (1.0 - 0.2186)
    ci = {"pop": pop, "summer_temp_cell": 19.0, "pop_age_bands": bands}
    hev = {"hazards": {"HEAT_WAVE": 20.0}, "exposures": {}, "vulnerabilities": {}}
    hn = {"hazards": {}, "exposures": {}, "vulnerabilities": {
        v: 0.5 for r in catalog.RISKS for v in r["vulnerabilities"]}}
    ctx = CellContext(ci=ci, hev=hev, hev_norm=hn, indices={MORT: 50.0},
                      regional={"bundesland": "Nordrhein-Westfalen"})
    impacts = impact.compute_all_cell_impacts(ctx)
    stored = runner.build_cell_risks({MORT: 50.0}, impacts)[MORT]
    assert stored["deaths_a85p"] > 0.0
    assert stored["deaths_a85p"] < stored["deaths"]
    factor = measure_service._measure_cell_factor(
        catalog.MEASURES_BY_CODE[CODE], {"s_gek": 1.0}, MORT, 1.0, 1.0, stored)
    assert 0.0 < factor < 1.0


def test_parameters_visible_in_registry():
    params = {p["id"]: p for p in parameter_registry.catalog_parameters(
        layer_code=MORT, layer_category="risks")}
    g = next(p for pid, p in params.items() if pid.endswith(".g_s157"))
    ror = next(p for pid, p in params.items() if pid.endswith(".ror_s157"))
    # Blockwert 0,29 gerundet; gerechnet wird ungerundet wie im Beispiel s157_berlin
    assert round(g["value"], 2) == 0.29 and g["evidence_class"] == "abgeschaetzt"
    assert g["value"] == pytest.approx(health.G_S157)
    assert ror["value"] == 0.93 and ror["evidence_class"] == "belegt"


# ── Befund 129: S157 zusammen mit dem Hitzeaktionsplan — Faktoren multiplizieren ──

HAP = measure_service.S157_HAP_CODE


def _delta_hap_full() -> float:
    """δ_HAP des Produkts bei voller Deckung (Hitzeaktionsplan für die ganze Kommune)."""
    override_context.set_overrides({})
    return measure_service._reduction_factor(catalog.MEASURES_BY_CODE[HAP], 1.0, 1.0)


def test_hap_factor_is_report_delta_hap():
    assert HAP in catalog.MEASURES_BY_CODE
    assert MORT in catalog.MEASURES_BY_CODE[HAP]["linked_risk_codes"]
    assert _delta_hap_full() == pytest.approx(0.95, abs=1e-12)


def test_berlin_with_hap_combined_72_1_percent():
    """Zusammen fallen 1 − 0,95 × 0,294 = 72,1 % des Heim-Exzesses weg (38,1 von 52,9)."""
    d_hap = _delta_hap_full()
    d_heim = D85_BERLIN * health.h_heim()
    s157 = health.s157_avoided_deaths(D85_BERLIN, 1.0, delta_hap=d_hap)
    gesamt = d_heim * (1.0 - d_hap) + s157
    assert gesamt / d_heim == pytest.approx(1.0 - d_hap * health.G_S157, rel=1e-12)
    assert round(100 * gesamt / d_heim, 1) == 72.1
    assert gesamt == pytest.approx(38.1, abs=0.05)
    # additiv gelesen wären es 75,6 % — das bucht 1,9 Todesfälle doppelt
    additiv = (1.0 - d_hap) + (1.0 - health.G_S157)
    assert round(100 * additiv, 1) == 75.6
    assert (additiv * d_heim - gesamt) == pytest.approx(1.9, abs=0.05)


def test_berlin_with_hap_s157_35_5_deaths_and_23_7_mio_eur():
    d_hap = _delta_hap_full()
    s157 = health.s157_avoided_deaths(D85_BERLIN, 1.0, delta_hap=d_hap)
    assert round(s157, 1) == 35.5
    eur = _benefit_eur(1.0, d_hap)
    assert round(eur / 1e6, 1) == 23.7
    # Unterschied zur additiven Lesart 1,25 Mio. € (Beispiel-Block s157_berlin)
    assert (_benefit_eur(1.0) - eur) / 1e6 == pytest.approx(1.25, abs=0.05)
    # bei δ_HAP = 0,85 rund 3,75 Mio. €
    assert (_benefit_eur(1.0) - _benefit_eur(1.0, 0.85)) / 1e6 == pytest.approx(3.75, abs=0.05)


def test_sum_of_single_benefits_equals_aggregate_with_both():
    """Einzelnutzen HAP + Einzelnutzen S157 (mit δ_HAP) = Minderung im Aggregat."""
    override_context.set_overrides({})
    risk = catalog.RISKS_BY_CODE[MORT]
    cell = _berlin_cell()
    base = risk_engine.cost_from_outcome(risk, cell["outcome"])
    f_hap = measure_service._measure_cell_factor(
        catalog.MEASURES_BY_CODE[HAP], {}, MORT, 1.0, 1.0, cell)
    # Aggregat „mit Maßnahmen“: Faktoren je Zelle multipliziert, S157 dort ohne δ_HAP
    f_s157_agg = measure_service._measure_cell_factor(
        catalog.MEASURES_BY_CODE[CODE], {"s_gek": 1.0}, MORT, 1.0, 1.0, cell)
    aggregat = base * (1.0 - f_hap * f_s157_agg)
    einzel = base * (1.0 - f_hap) + _benefit_eur(1.0, f_hap)
    assert einzel == pytest.approx(aggregat, rel=1e-9)


def test_without_hap_unchanged():
    assert health.s157_avoided_deaths(D85_BERLIN, 1.0, delta_hap=1.0) == \
        health.s157_avoided_deaths(D85_BERLIN, 1.0)
    assert health.s157_avoided_deaths(D85_BERLIN, None, delta_hap=0.95) is None
