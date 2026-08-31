"""Golden-Tests der Methodik #96 (Aeroallergene, Bericht Rev. 1).

Prüfklassen wie bei #95 (Integrations-Kontrakt, AUFGABE §7 / integriere-risiko §4):

1. **Beispiel-Blöcke** des Berichts laufen als Test — Bericht und Repo können
   nicht divergieren, ohne dass CI rot wird.
2. **Registry ⇄ Bericht**: die maschinenlesbaren Kap.-7-Werte müssen exakt den
   Registry-Specs/Katalogwerten entsprechen (kein stiller Code-Fix).
3. **Sanity-/Struktur-Anker aus Kap. 4**: Bundessumme Symptomtage und €,
   impliziter Klimaanteil, Verteilschlüssel-Lackmustest.
4. **Zellrechnung**: Handrechnung der Schadensfunktion inkl. P̂-Zentrierung.
"""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402
from app.services.engine import impact, override_context  # noqa: E402
from app.services.engine.impact import health as H  # noqa: E402
from app.services.engine.impact.base import CellContext  # noqa: E402

REPORT = os.path.join(os.path.dirname(__file__), "..", "..",
                      "docs", "methodik", "96_aeroallergene.md")
CODE = "EXPECTED_ANNUAL_ALLERGY_DAYS"


def _spec(key: str) -> dict:
    from app.services.engine.impact.params import IMPACT_PARAM_SPECS
    for s in IMPACT_PARAM_SPECS:
        if s["risk"] == CODE and s["key"] == key:
            return s
    raise AssertionError(f"Registry-Spec fehlt: {CODE}.{key}")


# ── 1. Beispiel-Blöcke des Berichts ───────────────────────────────────────────

def test_report_example_blocks_green():
    with open(os.path.abspath(REPORT), encoding="utf-8") as fh:
        blocks = re.findall(r"```python test: (\S+)\n(.*?)```", fh.read(), re.S)
    assert len(blocks) >= 7, "Bericht #96 muss mindestens 7 Beispiel-Blöcke tragen"
    for name, code in blocks:
        try:
            exec(compile(code, f"96:{name}", "exec"), {})  # noqa: S102
        except Exception as e:  # pragma: no cover
            raise AssertionError(f"Beispiel-Block {name} rot: {e}") from e


# ── 2. Registry/Katalog ⇄ Bericht (Kap. 7) ───────────────────────────────────

def test_registry_matches_report_parameters():
    """Kap.-7-Werte des Berichts == Registry-Specs (Divergenz = Ledger-Fall)."""
    for key, val in (("delta_s_birke_nord", 3.96), ("delta_s_birke_mitte", 4.20),
                     ("delta_s_birke_sued", 5.94), ("delta_s_graeser_nord", 4.78),
                     ("delta_s_graeser_mitte", 4.08), ("delta_s_graeser_sued", 3.70)):
        assert _spec(key)["value"] == val, key
    assert _spec("a_attr")["value"] == 0.50
    for key, val in (("p_ar_u20", 0.088), ("p_ar_a20_64", 0.132),
                     ("p_ar_a65_74", 0.067), ("p_ar_a75_84", 0.050),
                     ("p_ar_a85p", 0.050)):
        assert _spec(key)["value"] == val, key
    assert _spec("p_sens_birke")["value"] == 0.55
    assert _spec("p_sens_graeser")["value"] == 0.75
    assert _spec("f_symptomtage")["value"] == 0.70
    assert _spec("lambda_veg")["value"] == 0.70
    # Produktionskonstanten spiegeln die Specs (Call-Site-Defaults).
    assert H.POLLEN_PREVALENCE == {"u20": 0.088, "a20_64": 0.132, "a65_74": 0.067,
                                   "a75_84": 0.050, "a85p": 0.050}
    assert H.POLLEN_DELTA_S_BIRKE == {"nord": 3.96, "mitte": 4.20, "sued": 5.94}
    assert H.POLLEN_DELTA_S_GRAESER == {"nord": 4.78, "mitte": 4.08, "sued": 3.70}


def test_cost_rate_chain_matches_report():
    """§3.5-Kette: c_Tag = c_Jahr/d_Saison — testgebunden an den Katalog-Kostensatz."""
    risk = catalog.RISKS_BY_CODE[CODE]
    c_jahr = 210.3 * 119.3 / 94.0                       # TOTALL €2014 → €2024
    d_saison = 0.70 * (0.55 * 30 + 0.75 * 60)           # f · (p_B·L_B + p_G·L_G)
    assert abs(c_jahr - 266.90) < 0.05
    assert abs(d_saison - 43.05) < 1e-9
    assert abs(catalog.risk_default_cost_per_outcome(risk) - c_jahr / d_saison) < 0.01
    # Native Ergebnisgröße (§3.6): genau eine je Code.
    assert risk["outcome_unit"] == "Symptomtage/Jahr"


def test_veg_weight_derives_from_delta_contributions():
    """w_B = p_B·ΔS_B,DE / (p_B·ΔS_B,DE + p_G·ΔS_G,DE) — Herleitung der Ĝ-Gewichte."""
    w_b = 0.55 * 4.79 / (0.55 * 4.79 + 0.75 * 4.06)
    assert abs(_spec("veg_weight_birke")["value"] - w_b) < 0.001


# ── 3. Sanity-/Struktur-Anker (Bericht Kap. 4) ───────────────────────────────

# Bundes-Altersmix (Bevölkerung 31.12.2023, §3.2-Bandsummen).
_BAND_POP = {"u20": 15_583_456, "a20_64": 49_163_992, "a65_74": 9_569_640,
             "a75_84": 6_294_744, "a85p": 2_844_213}
_POP_DE = sum(_BAND_POP.values())


def _ctx(pop: float, bundesland: str = "Nordrhein-Westfalen",
         g_cell: float | None = None) -> CellContext:
    bands = {b: pop * n / _POP_DE for b, n in _BAND_POP.items()}
    bands["u65"] = bands["u20"] + bands["a20_64"]
    g = 0.1775 if g_cell is None else g_cell
    return CellContext(
        ci={"pop": pop, "pop_age_bands": bands},
        hev={"hazards": {"POLLEN_LOAD": g}, "exposures": {}, "vulnerabilities": {}},
        hev_norm={"hazards": {}, "exposures": {}, "vulnerabilities": {}},
        indices={}, regional={"bundesland": bundesland})


def test_national_sum_matches_report_sanity_band():
    """Kap. 4: ~17,8 Mio Symptomtage und ~110 Mio €₂₀₂₄/Jahr (Bundessumme)."""
    override_context.set_overrides({})
    # Region Mitte trägt die DE-nahen ΔS-Werte; für die Bundessumme rechnet der
    # Bericht mit den DE-Mittelwerten — hier über den Δ-Term direkt geprüft.
    res = impact.compute_all_cell_impacts(_ctx(float(_POP_DE)))[CODE]
    betroffene = res["betroffene"]
    assert abs(betroffene / 1e6 - 8.96) < 0.02, betroffene
    # Mitte: δ = 0,70·(0,55·4,20 + 0,75·4,08)·0,50 = 1,880 Tage
    assert abs(res["outcome"] / betroffene - 1.880) < 0.002
    tage_de = betroffene * 1.988                        # DE-gewichtetes δ
    assert abs(tage_de / 1e6 - 17.8) < 0.1
    assert abs(tage_de * 6.20 / 1e6 - 110) < 2


def test_implied_climate_share_in_published_band():
    """Impliziter Klimaanteil δ/d_Saison = 4,6 % ∈ [3 %, 20 %] (Kap. 4)."""
    delta_de = 0.70 * (0.55 * 4.79 + 0.75 * 4.06) * 0.50
    share = delta_de / (0.70 * (0.55 * 30 + 0.75 * 60))
    assert abs(share * 100 - 4.62) < 0.05
    assert 0.03 <= share <= 0.20


def test_cell_hand_calculation_and_p_hat_centering():
    """Zell-Handrechnung (§3.3) + P̂-Zentrierung: Ĝ = Ḡ ⇒ P̂ = 1."""
    override_context.set_overrides({})
    res = impact.compute_all_cell_impacts(_ctx(1000.0, "Hessen"))[CODE]
    # Betroffene = 1000 × gewichtete Bundesprävalenz 10,74 %
    assert abs(res["betroffene"] - 107.4) < 0.1
    # Region Mitte, P̂ = 1 (Ĝ = Ḡ): ΔTage ≈ 201,9; € ≈ 1.252
    assert abs(res["outcome"] - 201.9) < 0.5
    assert abs(res["cost_eur"] - 201.9 * 6.20) < 5

    # P̂ skaliert linear mit λ: Ĝ = 1,5·Ḡ ⇒ P̂ = 1 + 0,7·0,5 = 1,35
    rich = impact.compute_all_cell_impacts(
        _ctx(1000.0, "Hessen", g_cell=0.1775 * 1.5))[CODE]
    assert abs(rich["outcome"] / res["outcome"] - 1.35) < 1e-6
    # … und wirkt in BEIDEN Pfaden identisch (nativ ⇄ €, Rev.-5-Befund 12).
    assert abs(rich["cost_eur"] / res["cost_eur"] - 1.35) < 1e-6


def test_lackmus_no_population_no_days():
    """§3.1-Verteilschlüssel-Test: Zelle ohne Bevölkerung → 0 Symptomtage."""
    override_context.set_overrides({})
    empty = CellContext(
        ci={"pop": 0.0, "pop_age_bands": {b: 0.0 for b in H.POLLEN_AGE_BANDS}},
        hev={"hazards": {"POLLEN_LOAD": 0.3}, "exposures": {}, "vulnerabilities": {}},
        hev_norm={"hazards": {}, "exposures": {}, "vulnerabilities": {}},
        indices={}, regional={"bundesland": "Bayern"})
    assert impact.compute_all_cell_impacts(empty)[CODE]["outcome"] == 0.0


def test_f_cancels_in_euro_path():
    """§3.5: f wirkt auf ΔTage, kürzt sich aber im €-Pfad (c_Tag = c_Jahr/d_Saison)."""
    override_context.set_overrides({})
    base = impact.compute_all_cell_impacts(_ctx(1000.0, "Hessen"))[CODE]["outcome"]
    override_context.set_overrides({f"risks.{CODE}.impact.f_symptomtage": 0.85})
    higher = impact.compute_all_cell_impacts(_ctx(1000.0, "Hessen"))[CODE]["outcome"]
    override_context.set_overrides({})
    # Native Größe skaliert mit f …
    assert abs(higher / base - 0.85 / 0.70) < 1e-9
    # … der €-Wert je Betroffenem bleibt gleich, weil d_Saison dasselbe f trägt.
    c_tag = lambda f: 266.90 / (f * (0.55 * 30 + 0.75 * 60))  # noqa: E731
    assert abs(higher * c_tag(0.85) - base * c_tag(0.70)) < 1e-6


# ── 4. Ebene POLLEN_LOAD (§3.3-Spezifikation, Integrationsumfang) ────────────

def test_pollen_load_layer_weights_and_unknown_share():
    """Ĝ = w_B·(getaggte + Anteil·ungetaggte Kronen) + (1−w_B)·Grünanteil."""
    from app.services.engine.indicators import pollen_load

    override_context.set_overrides({})
    ci = {"canopy_birch_frac": 0.02, "canopy_unknown_frac": 0.10, "green_frac": 0.30}
    w_b, share = 0.463, 0.12
    assert abs(pollen_load(ci) - (w_b * (0.02 + share * 0.10)
                                  + (1 - w_b) * 0.30)) < 1e-9
    # Zelle ohne Vegetation → 0
    assert pollen_load({}) == 0.0
    # Der Gattungsanteil ungetaggter Kronen ist editierbar (Registry-Wiring).
    override_context.set_overrides(
        {f"risks.{CODE}.impact.birch_group_share_default": 1.0})
    assert abs(pollen_load(ci) - (w_b * 0.12 + (1 - w_b) * 0.30)) < 1e-9
    override_context.set_overrides({})


def test_u20_band_is_available_and_consistent():
    """Band u20 (§3.2, neu angelegt): u65 = u20 + 20–64 bleibt erhalten."""
    from app.services.zensus_loader import (
        NATIONAL_U20_SHARE_OF_U65, U20_COLUMNS, _u20_share_of_u65,
    )

    assert U20_COLUMNS == ("unter5", "a5bis9", "a10bis14", "a15bis19")
    assert abs(NATIONAL_U20_SHARE_OF_U65 - 15_583_456 / 64_747_448) < 0.0005
    # Zellwerte aus den 5-Jahres-Gruppen; Rückfall bei leerer Zelle.
    parsed = {"unter5": 10, "a5bis9": 10, "a10bis14": 10, "a15bis19": 10,
              "a20bis24": 60}
    assert abs(_u20_share_of_u65(parsed, 0.24) - 40 / 100) < 1e-9
    assert _u20_share_of_u65({}, 0.24) == 0.24


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-q"]))
