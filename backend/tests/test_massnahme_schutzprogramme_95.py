"""Hebel S152 — Schutzprogramme vulnerable Gruppen (Bericht #95 §5, Beispiel-Block
``schutzprogramme_berlin``, Blöcke ``heat.delta_vg`` und ``heat.delta_vg_morb``).

Maßnahme ``VULNERABLE_GROUP_PROGRAMS`` wirkt nicht mehr mit ``default_reduction`` 0.22
auf alle Bänder (Berlin rund 79,8 Mio. €), sondern mit

``ΔD_VG = [D_75–84 + D_85+ · (1 − h_Heim)] · (1 − δ_VG)``, δ_VG = 0,931,

bewertet mit L̄_a (YLL) × VOLY: Berlin 11,7 Mio. € je Jahr. Auf die Einweisungen
derselben Bänder δ_VG,morb = 1,0 (Band 0,931–1,069). Mit dem Hitzeaktionsplan zusammen
gilt ``max(δ_HAP × δ_VG; 0,794)`` (Kappung am Paketwert Deutschland, Befund 126).

DB-frei: prüft Rechenfunktionen in ``health`` und den Zellfaktor der Maßnahmen-Engine
an einer Zelle mit den Berlin-Werten aus Kette 3.0 (Ebene 6: D_75–84 = 71,4,
D_85+ = 153,6; Ebene 9: F_75–84 = 34,2, F_85+ = 21,0).
"""

from __future__ import annotations

import pytest

from app.data import catalog, sources
from app.services import measure_service, parameter_registry
from app.services.engine import impact, override_context, risk_engine, runner
from app.services.engine.impact import health
from app.services.engine.impact.base import CellContext

CODE = "VULNERABLE_GROUP_PROGRAMS"
HAP = "HEAT_ACTION_PLANS"
MORT = "EXPECTED_ANNUAL_MORTALITY"
MORB = "EXPECTED_ANNUAL_MORBIDITY"
D75_BERLIN, D85_BERLIN = 71.4, 153.6     # Bericht #95 Kette 3.0, Ebene 6
F75_BERLIN, F85_BERLIN = 34.2, 21.0      # Ebene 9 (Einweisungen)
EUR_JE_FALL = 7152.0                     # Kostensatz Einweisung (Bericht #95 §5)


@pytest.fixture(autouse=True)
def _keine_overrides():
    override_context.set_overrides({})
    yield
    override_context.set_overrides({})


def _berlin_mort_cell() -> dict:
    """Zelle mit den Berliner Todesfällen 75–84 und 85+ (übrige Bänder als Sockel)."""
    yll = (D75_BERLIN * health.AGE_LIFE_YEARS["a75_84"]
           + D85_BERLIN * health.AGE_LIFE_YEARS["a85p"] + 1000.0)
    return {"outcome": yll, "deaths_a75_84": D75_BERLIN, "deaths_a85p": D85_BERLIN}


def _berlin_morb_cell() -> dict:
    return {"outcome": F75_BERLIN + F85_BERLIN + 50.0,
            "cases_a75_84": F75_BERLIN, "cases_a85p": F85_BERLIN}


def _factor(code: str, cell: dict, delta_hap: float = 1.0, hap_cap: float = 1.0) -> float:
    return measure_service._measure_cell_factor(
        catalog.MEASURES_BY_CODE[CODE], {}, code, 1.0, 1.0, cell, delta_hap, hap_cap)


def _benefit_eur(delta_hap: float = 1.0) -> float:
    """Einzelnutzen Mortalität in € je Jahr (mit δ_HAP gedämpft und gekappt)."""
    cell = _berlin_mort_cell()
    base = risk_engine.cost_from_outcome(catalog.RISKS_BY_CODE[MORT], cell["outcome"])
    return base * (1.0 - _factor(MORT, cell, delta_hap, delta_hap))


def test_measure_uses_report_effect_model():
    m = catalog.MEASURES_BY_CODE[CODE]
    assert m["effect_model"] == "vg"
    assert m["default_reduction"] is None      # keine 0.22 auf alle Bänder mehr
    assert m["linked_risk_codes"] == [MORT, MORB]


def test_constants_from_report_blocks():
    assert health.DELTA_VG == 0.931
    assert health.DELTA_VG_MORB == 1.0
    assert health.VG_PAKET_DE == pytest.approx(0.794, abs=1e-12)
    # δ_VG = 1 − r × w = 1 − 0,20 × 24,4/97,3/0,728 (Block schutzprogramme_berlin)
    w = 24.372 / 97.3 / (4720 / 6483)
    assert 1.0 - 0.20 * w == pytest.approx(health.DELTA_VG, abs=0.0005)


def test_berlin_11_7_mio_eur():
    eur = _benefit_eur()
    assert round(eur / 1e6, 1) == 11.7
    assert eur / 1e6 == pytest.approx(11.7, abs=0.05)
    # 3,2 % des Jahresbetrags 362,9 Mio. € und rund 15 % der früheren 79,8 Mio. €
    assert eur / 1e6 / 362.9 == pytest.approx(0.032, abs=0.001)
    assert eur / 1e6 / 79.8 == pytest.approx(0.15, abs=0.005)


def test_berlin_yll_base_without_care_home_residents():
    """1.054 YLL (75–84 ganz, 85+ ohne Heimbewohner) = 169,5 Mio. €."""
    yll = health.vg_avoided(D75_BERLIN * health.AGE_LIFE_YEARS["a75_84"],
                            D85_BERLIN * health.AGE_LIFE_YEARS["a85p"], 0.0)
    assert yll == pytest.approx(1054, abs=1.5)
    assert yll * 160_800 / 1e6 == pytest.approx(169.5, abs=0.2)


def test_band_upper_end_is_package_value_34_9_mio_eur():
    override_context.set_overrides({f"risks.{MORT}.impact.delta_vg": 0.5})
    # δ_VG unter dem Paketwert wird auf 0,794 gekappt
    assert _benefit_eur() / 1e6 == pytest.approx(34.9, abs=0.1)
    override_context.set_overrides({f"risks.{MORT}.impact.delta_vg": 1.0})
    assert _benefit_eur() == 0.0


def test_kappung_0_794_with_heat_action_plan():
    # zentral 0,95 × 0,931 = 0,885, keine Kappung
    assert 0.95 * health.vg_effective_delta(health.DELTA_VG, 0.95) == \
        pytest.approx(0.885, abs=0.001)
    assert health.vg_effective_delta(health.DELTA_VG, 0.95) == health.DELTA_VG
    # δ_HAP 0,85: Produkt 0,791 < 0,794 — es gilt 0,794
    assert 0.85 * health.DELTA_VG < 0.794
    assert 0.85 * health.vg_effective_delta(health.DELTA_VG, 0.85) == \
        pytest.approx(0.794, abs=1e-12)
    # ohne Hitzeaktionsplan gilt δ_VG, nie unter 0,794
    assert health.vg_effective_delta(health.DELTA_VG, 1.0) == health.DELTA_VG
    assert health.vg_effective_delta(0.5, 1.0) == pytest.approx(0.794, abs=1e-12)


def test_kappung_in_cell_factor_berlin():
    """Beide Hebel nehmen zusammen auf 75+ ohne Heim höchstens 20,6 % weg."""
    cell = _berlin_mort_cell()
    base = risk_engine.cost_from_outcome(catalog.RISKS_BY_CODE[MORT], cell["outcome"])
    eur_7585 = health.vg_avoided(D75_BERLIN * health.AGE_LIFE_YEARS["a75_84"],
                                 D85_BERLIN * health.AGE_LIFE_YEARS["a85p"], 0.0) \
        * base / cell["outcome"]
    for d_hap, soll in ((0.95, 0.885), (0.85, 0.794)):
        einzel_hap = eur_7585 * (1.0 - d_hap)
        gesamt = einzel_hap + _benefit_eur(d_hap)
        assert gesamt / eur_7585 == pytest.approx(1.0 - soll, abs=0.001)


def test_sum_of_single_benefits_equals_aggregate_with_both():
    cell = _berlin_mort_cell()
    base = risk_engine.cost_from_outcome(catalog.RISKS_BY_CODE[MORT], cell["outcome"])
    for d_hap in (0.95, 0.85):
        # Aggregat „mit Maßnahmen“: Faktoren multipliziert, δ_VG dort nur gekappt
        aggregat = base * (1.0 - d_hap * _factor(MORT, cell, 1.0, d_hap))
        einzel = base * (1.0 - d_hap) + _benefit_eur(d_hap)
        assert einzel == pytest.approx(aggregat, rel=1e-9)


def test_care_home_residents_excluded():
    """Nur 85+ (ohne 75–84): Wirkung auf D_85+ × (1 − h_Heim), nicht auf D_85+."""
    cell = {"outcome": 1000.0, "deaths_a75_84": 0.0, "deaths_a85p": 100.0}
    f = _factor(MORT, cell)
    soll = 100.0 * (1.0 - health.h_heim()) * health.AGE_LIFE_YEARS["a85p"] * (1.0 - 0.931)
    assert (1.0 - f) * 1000.0 == pytest.approx(soll, rel=1e-9)


def test_morbidity_central_1_0_no_effect_band_0_02_mio_eur():
    cell = _berlin_morb_cell()
    assert _factor(MORB, cell) == 1.0
    f_75 = F75_BERLIN + F85_BERLIN * (1.0 - health.h_heim())
    assert f_75 == pytest.approx(48.0, abs=0.05)
    assert f_75 * EUR_JE_FALL / 1e6 == pytest.approx(0.34, abs=0.005)
    for m in (0.931, 1.069):
        override_context.set_overrides({f"risks.{MORB}.impact.delta_vg_morb": m})
        delta_cases = (1.0 - _factor(MORB, cell)) * cell["outcome"]
        assert abs(delta_cases * EUR_JE_FALL / 1e6) == pytest.approx(0.02, abs=0.005)
    # oben mehr Einweisungen (vorgezogen): Faktor über 1
    assert _factor(MORB, cell) > 1.0


def test_old_cells_without_band_values_unchanged():
    assert _factor(MORT, {"outcome": 10.0}) == 1.0
    assert _factor(MORB, {"outcome": 10.0}) == 1.0


def test_real_path_stores_band_values_and_measure_acts():
    pop = 100_000.0
    bands = {b: pop * 0.2186 * f for b, f in
             {"a65_74": 0.5003, "a75_84": 0.3555, "a85p": 0.1442}.items()}
    bands["u65"] = pop * (1.0 - 0.2186)
    ci = {"pop": pop, "summer_temp_cell": 19.0, "pop_age_bands": bands}
    hev = {"hazards": {"HEAT_WAVE": 20.0}, "exposures": {}, "vulnerabilities": {}}
    hn = {"hazards": {}, "exposures": {}, "vulnerabilities": {
        v: 0.5 for r in catalog.RISKS for v in r["vulnerabilities"]}}
    ctx = CellContext(ci=ci, hev=hev, hev_norm=hn, indices={MORT: 50.0, MORB: 50.0},
                      regional={"bundesland": "Nordrhein-Westfalen"})
    impacts = impact.compute_all_cell_impacts(ctx)
    stored = runner.build_cell_risks({MORT: 50.0, MORB: 50.0}, impacts)
    assert 0.0 < stored[MORT]["deaths_a75_84"] < stored[MORT]["deaths"]
    assert stored[MORB]["cases_a75_84"] > 0.0 and stored[MORB]["cases_a85p"] > 0.0
    assert 0.0 < _factor(MORT, stored[MORT]) < 1.0
    assert _factor(MORB, stored[MORB]) == 1.0


def test_parameters_visible_in_registry_with_resolvable_sources():
    mort = {p["id"]: p for p in parameter_registry.catalog_parameters(
        layer_code=MORT, layer_category="risks")}
    morb = {p["id"]: p for p in parameter_registry.catalog_parameters(
        layer_code=MORB, layer_category="risks")}
    dvg = next(p for pid, p in mort.items() if pid.endswith(".delta_vg"))
    dmorb = next(p for pid, p in morb.items() if pid.endswith(".delta_vg_morb"))
    assert dvg["value"] == health.DELTA_VG and dvg["evidence_class"] == "abgeschaetzt"
    assert dmorb["value"] == health.DELTA_VG_MORB and dmorb["evidence_class"] == "abgeschaetzt"
    from app.services.engine.impact.params import IMPACT_PARAM_SPECS
    for key in ("delta_vg", "delta_vg_morb"):
        spec = next(s for s in IMPACT_PARAM_SPECS if s["key"] == key)
        assert "Liotta_Rom_Hitze_2018" in spec["source_refs"]
        for ref in spec["source_refs"]:
            assert ref in sources.SOURCE_REFERENCES
        assert {"wert", "band", "sensitivitaet"} <= set(spec["evidence_derivation"])
