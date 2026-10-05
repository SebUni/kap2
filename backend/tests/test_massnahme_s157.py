"""Hebel S157 — gekühlte Heimplätze (Bericht #95 §5, Beispiel-Block ``s157_berlin``).

Maßnahme ``COOLING_ROOMS_DRINKING_WATER`` ist aktiviert (T-1367) und wirkt mit
``ΔD_S157 = D_85+ · h_Heim · s_gek · (1 − g_S157)`` auf die Todesfälle 85+ der
Heimbewohner, bewertet mit L̄_85+ (YLL) × VOLY. s_gek ist der heutige gekühlte Anteil
der Kommune; ohne Eingabe gilt die Voreinstellung 0,11 (Block heat.s_gek, Befund 138).
S157 wirkt nur auf max(s_gek − 0,06; 0), den Anteil über dem Stand der Kalibrierjahre
(Block heat.s_gek_kalib, Befund 165, Log 50). Berlin (Kette) je vollen Anteil 24,99 Mio. €:
Voreinstellung 0,05 × 24,99 = 1,2 Mio. €, alle Heimplätze gekühlt 0,94 × 24,99 = 23,5 Mio. €.

Zusammen mit dem Hitzeaktionsplan (Befund 129) wirkt S157 auf den schon mit δ_HAP
gedämpften Heim-Exzess: Berlin zusammen 72,4 %, davon S157 je vollen Anteil 35,1
Todesfälle oder 23,5 Mio. € je Jahr.

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


def _benefit_eur(s_gek, delta_hap: float = 1.0, frac: float = 1.0) -> float:
    """Nutzen in € je Jahr; ``s_gek=None`` heißt: die Kommune gibt nichts ein."""
    override_context.set_overrides({})
    risk = catalog.RISKS_BY_CODE[MORT]
    mdef = catalog.MEASURES_BY_CODE[CODE]
    cell = _berlin_cell()
    factor = measure_service._measure_cell_factor(
        mdef, {} if s_gek is None else {"s_gek": s_gek}, MORT, frac, 1.0, cell, delta_hap)
    return risk_engine.cost_from_outcome(risk, cell["outcome"]) * (1.0 - factor)


def _s_zus_full() -> float:
    """Höchster zusätzlicher Anteil 1 − s_gek_kalib = 0,94 (Registry heat.s_gek_kalib)."""
    return 1.0 - measure_service._s157_param("s_gek_kalib", -1.0)


def _per_full_share(s_gek: float = 1.0, delta_hap: float = 1.0) -> float:
    """Nutzen je vollen Anteil über dem Stand der Kalibrierjahre (Bericht: 24,99 Mio. €)."""
    return _benefit_eur(s_gek, delta_hap) / _s_zus_full()


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


def test_kalib_from_registry_is_0_06():
    override_context.set_overrides({})
    assert measure_service._s157_param("s_gek_kalib", -1.0) == pytest.approx(0.06)
    assert measure_service._s157_param("s_gek", -1.0) == pytest.approx(0.11)
    assert _s_zus_full() == pytest.approx(0.94)


def test_berlin_per_full_share_is_25_0_mio_eur():
    """Beispiel-Block s157_berlin: je vollen Anteil 25,0 Mio. € (ungerundet 24,99)."""
    eur = _per_full_share()
    assert round(eur / 1e6, 1) == 25.0
    assert eur / 1e6 == pytest.approx(24.99, abs=0.01)


def test_berlin_all_care_home_places_cooled_is_23_5_mio_eur():
    """s_gek = 1: 0,94 × 24,99 = 23,5 Mio. € (Bericht #95 §5, Befund 165)."""
    eur = _benefit_eur(1.0)
    assert eur / 1e6 == pytest.approx(23.5, abs=0.05)
    assert eur / 1e6 == pytest.approx(0.94 * 24.99, abs=0.05)


def test_berlin_ten_points_above_kalib_is_one_tenth():
    """10 Prozentpunkte über dem Stand der Kalibrierjahre (s_gek = 0,16): ein Zehntel."""
    assert _benefit_eur(0.16) == pytest.approx(_per_full_share() / 10.0, rel=1e-9)


def test_without_input_default_0_11_gives_1_2_mio_eur():
    """Befund 138/172: ohne Eingabe s_gek = 0,11, 24,99 × 0,05 = 1,249, gerundet 1,2 Mio. €."""
    eur = _benefit_eur(None)
    assert eur / 1e6 == pytest.approx(1.2, abs=0.05)
    assert round(eur / 1e6, 1) == 1.2
    assert eur == pytest.approx(_benefit_eur(0.11), rel=1e-12)
    fields = measure_service._s157_summary_fields(catalog.MEASURES_BY_CODE[CODE], {})
    assert fields["s_gek"] == pytest.approx(0.11)
    assert fields["s_gek_is_default"] is True
    assert fields["s_gek_kalib"] == pytest.approx(0.06)
    assert fields["s157_estimate_note"] == "Abschätzung von KAP3"
    assert "benefit_display" not in fields
    assert "benefit_missing_input" not in fields


def test_with_input_marked_as_input():
    fields = measure_service._s157_summary_fields(
        catalog.MEASURES_BY_CODE[CODE], {"s_gek": 0.3})
    assert fields["s_gek"] == pytest.approx(0.3)
    assert fields["s_gek_is_default"] is False


def test_below_kalib_gives_zero():
    """s_gek = 0,05 liegt unter dem Stand der Kalibrierjahre 0,06: S157 wirkt nicht."""
    assert _benefit_eur(0.05) == 0.0
    assert _benefit_eur(0.06) == pytest.approx(0.0, abs=1e-6)


def test_coverage_frac_does_not_shrink_effect():
    """s_gek gilt für die ganze Kommune; der Deckungsgrad frac verkleinert die Wirkung nicht."""
    full = _benefit_eur(None, frac=1.0)
    assert full > 0.0
    for frac in (0.9, 0.5, 0.1):
        assert _benefit_eur(None, frac=frac) == pytest.approx(full, rel=1e-12)
        assert _benefit_eur(1.0, frac=frac) == pytest.approx(_benefit_eur(1.0), rel=1e-12)


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
    # Blockwert 0,2936 gerundet; gerechnet wird ungerundet wie im Beispiel s157_berlin
    assert round(g["value"], 4) == 0.2936 and g["evidence_class"] == "abgeschaetzt"
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
    assert _delta_hap_full() == pytest.approx(0.939, abs=1e-12)


def test_berlin_with_hap_combined_72_4_percent():
    """Zusammen fallen 1 − 0,939 × 0,2936 = 72,4 % des Heim-Exzesses weg (38,1 von 52,9)."""
    d_hap = _delta_hap_full()
    d_heim = D85_BERLIN * health.h_heim()
    s157 = health.s157_avoided_deaths(D85_BERLIN, 1.0, delta_hap=d_hap)
    gesamt = d_heim * (1.0 - d_hap) + s157
    assert gesamt / d_heim == pytest.approx(1.0 - d_hap * health.G_S157, rel=1e-12)
    assert round(100 * gesamt / d_heim, 1) == 72.4
    assert gesamt == pytest.approx(38.3, abs=0.05)
    # additiv gelesen wären es 76,7 % — das bucht 2,3 Todesfälle doppelt
    additiv = (1.0 - d_hap) + (1.0 - health.G_S157)
    assert round(100 * additiv, 1) == 76.7
    assert (additiv * d_heim - gesamt) == pytest.approx(2.3, abs=0.05)


def test_berlin_with_hap_s157_35_1_deaths_and_23_5_mio_eur():
    d_hap = _delta_hap_full()
    s157 = health.s157_avoided_deaths(D85_BERLIN, 1.0, delta_hap=d_hap)
    assert round(s157, 1) == 35.1
    # Bericht §5 „Berlin, voller Anteil“: je vollen Anteil über dem Stand der Kalibrierjahre
    eur = _per_full_share(1.0, d_hap)
    assert round(eur / 1e6, 1) == 23.5
    # Unterschied zur additiven Lesart 1,5 Mio. € (Beispiel-Block s157_berlin)
    assert (_per_full_share() - eur) / 1e6 == pytest.approx(1.5, abs=0.05)
    # bei δ_HAP = 0,852 rund 3,7 Mio. €
    assert (_per_full_share() - _per_full_share(1.0, 0.852)) / 1e6 == \
        pytest.approx(3.7, abs=0.05)


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


# ── Befund 146: h_Heim je Zelle aus share_care_home_85p (Bericht #95 §5, Log 45) ──

def test_h_heim_je_zelle_aus_heimanteil():
    """h_Heim,z = q_pfl,z · [1 + β(1 − q̄)] / [1 + β(q_pfl,z − q̄)], Rückfall 0,344."""
    # Beispielzelle des Berichts (§5): 0,5 × 2,31 / 1,541 = 0,75
    assert health.h_heim(q_pfl=0.5) == pytest.approx(0.75, abs=0.005)
    # Zelle im Mittel: dieselben 0,344 wie die Kommune
    assert health.h_heim(q_pfl=0.149) == pytest.approx(0.344, abs=0.0005)
    assert health.h_heim(q_pfl=0.149) == pytest.approx(health.h_heim(), rel=1e-12)
    # Zelle nur mit Heimbewohnern ab 85
    assert health.h_heim(q_pfl=1.0) == pytest.approx(1.0, abs=1e-9)
    # Ohne Zellwert gilt der Rückfall 0,344 (Block heat.h_heim)
    assert health.h_heim(q_pfl=None) == pytest.approx(0.344, abs=0.0005)
    assert health.h_heim() == pytest.approx(0.344, abs=0.0005)


def test_zellfaktoren_nutzen_heimanteil_der_zelle():
    """_s157_cell_factor und _vg_cell_factor rechnen mit h_Heim,z der Zelle."""
    override_context.set_overrides({})
    ohne_heim = {**_berlin_cell(), "deaths_a75_84": 71.4, "share_care_home_85p": 0.0}
    mit_heim = {**ohne_heim, "share_care_home_85p": 0.5}
    ohne_wert = {k: v for k, v in ohne_heim.items() if k != "share_care_home_85p"}

    s157 = [measure_service._s157_cell_factor(0.11, 1.0, c)
            for c in (ohne_heim, mit_heim, ohne_wert)]
    assert s157[0] != s157[1]
    assert s157[0] == pytest.approx(1.0)         # Zelle ohne Heim: keine Wirkung von S157
    assert s157[1] < s157[2] < 1.0               # Heimzelle stärker als der Rückfall 0,344
    # Wirkung skaliert mit h_Heim: 0,75 / 0,344
    assert (1.0 - s157[1]) / (1.0 - s157[2]) == pytest.approx(
        health.h_heim(q_pfl=0.5) / health.h_heim(), rel=1e-9)

    vg = [measure_service._vg_cell_factor(MORT, 1.0, c) for c in (ohne_heim, mit_heim, ohne_wert)]
    assert vg[0] != vg[1]
    assert vg[0] < vg[2] < vg[1] < 1.0           # Heimbewohner sind bei δ_VG herausgenommen


def test_heimanteil_kommt_aus_den_zell_eingaben():
    """Die Zellbewertung trägt share_care_home_85p unter data["inputs"], nicht im Risiko."""
    cell = _berlin_cell()
    merged = measure_service._with_cell_q_pfl(cell, {"share_care_home_85p": 0.5})
    assert merged["share_care_home_85p"] == 0.5 and "share_care_home_85p" not in cell
    assert measure_service._with_cell_q_pfl(cell, {"pop": 10.0}) is cell
    assert measure_service._with_cell_q_pfl(cell, None) is cell
