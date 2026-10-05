"""Zellfunktion Ĝ' der Stadtbaumwahl (Bericht #96 §5, Z. 975–989, 1115–1121).

Teilpaket #1 des Vorhabens T-1483-cto (Punkt (d), Spiegelstriche 2–4):

1. ``health.stadtbaum_g_neu`` zieht die Kronen-Ersatz-Senkung genau in dem Term ab,
   in dem die ersetzten Kronen im Ausgangsstand stehen (Kronen mit Gattungs-Tag der
   Birkengruppe voll, Kronen ohne Gattungs-Tag mit ``s_unbek``), niemals als anteilige
   Senkung von Ĝ.
2. Die Kappungsgrenze je Term (``dk ≤ k``) hält ``Ĝ' ≥ (1 − w_B) · Grün``.
3. Die Zellausgabe von ``allergy_symptom_days`` trägt die Kronenterme
   (``canopy_birch_frac``, ``canopy_unknown_frac``, ``green_frac``) gleich den
   Zelleingaben; ``runner.build_cell_risks`` speichert sie wie ``pollen_g``, ``outcome``
   und ``cost_eur`` bleiben unverändert (kein neuer Rechenpfad).

Die Maßnahme selbst (Ĝ' im Zelllauf einer Maßnahme, Ḡ₀-Festhaltung) ist NICHT Teil
dieses Pakets (#2 aus T-1483-cto).
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services.engine import impact, override_context  # noqa: E402
from app.services.engine.impact import health as H  # noqa: E402
from app.services.engine.impact.base import CellContext  # noqa: E402
from app.services.engine.indicators import POLLEN_G_WEIGHT_BIRKE  # noqa: E402
from app.services.engine.runner import build_cell_risks  # noqa: E402

CODE = "EXPECTED_ANNUAL_ALLERGY_DAYS"


# ── (a) Rechenbeispiel §5 (Allee-Zelle, Zellen 3/4 der Kommunentabelle) ──────────

def test_stadtbaum_g_neu_matches_report_example():
    """Ĝ' = Ĝ − w_B·dk_Birke, wie im Rechenbeispiel §5 Z. 1031 (Zellen 3 und 4)."""
    g_neu_3 = H.stadtbaum_g_neu(g_zelle=0.30, k_birke=0.30, k_unbek=0.0, gruen=0.30,
                                dk_birke=0.10, dk_unbek=0.0, s_unbek=0.12)
    assert abs(g_neu_3 - 0.2536) < 1e-12

    g_neu_4 = H.stadtbaum_g_neu(g_zelle=0.60, k_birke=0.60, k_unbek=0.0, gruen=0.60,
                                dk_birke=0.20, dk_unbek=0.0, s_unbek=0.12)
    assert abs(g_neu_4 - 0.5072) < 1e-12


# ── (b) Kronen ohne Gattungs-Tag: nur mit s_unbek, nie voll ──────────────────────

def test_stadtbaum_g_neu_unbekannte_kronen_nur_mit_s_unbek():
    """Ohne Gattungs-Tag zählt die Senkung nur mit s_unbek, nie mit w_B voll (§5 Befund 195)."""
    g_zelle = POLLEN_G_WEIGHT_BIRKE * 0.12 * 0.30  # w_B·s_unbek·k_unbek, Grün 0
    g_neu = H.stadtbaum_g_neu(g_zelle=g_zelle, k_birke=0.0, k_unbek=0.30, gruen=0.0,
                              dk_birke=0.0, dk_unbek=0.10, s_unbek=0.12)
    senkung = g_zelle - g_neu
    assert abs(senkung - 0.0056) < 1e-4
    # nie die volle w_B-Senkung, als trüge die Kronenfläche einen Gattungs-Tag
    assert abs(senkung - POLLEN_G_WEIGHT_BIRKE * 0.10) > 1e-3


# ── (c) Grenze: dk über k wird am Term gekappt ───────────────────────────────────

def test_stadtbaum_g_neu_kappt_dk_am_term():
    """dk_Birke > k_Birke wird am Term gekappt; Ĝ' = 0,536 × Grün, exakt."""
    g_neu = H.stadtbaum_g_neu(g_zelle=0.30, k_birke=0.30, k_unbek=0.0, gruen=0.30,
                              dk_birke=0.50, dk_unbek=0.0, s_unbek=0.12)
    erwartet = (1.0 - POLLEN_G_WEIGHT_BIRKE) * 0.30
    assert abs(erwartet - 0.1608) < 1e-9
    assert abs(g_neu - 0.1608) < 1e-12
    assert abs(g_neu - erwartet) < 1e-12


def test_stadtbaum_g_neu_haelt_die_gruen_grenze_auch_bei_unbek():
    """Dieselbe Kappung greift für dk_unbek, und der Boden gilt auch kombiniert."""
    k_birke, k_unbek, gruen, s_unbek = 0.10, 0.50, 0.20, 0.12
    g_zelle = POLLEN_G_WEIGHT_BIRKE * (k_birke + s_unbek * k_unbek) + (1.0 - POLLEN_G_WEIGHT_BIRKE) * gruen
    g_neu = H.stadtbaum_g_neu(g_zelle=g_zelle, k_birke=k_birke, k_unbek=k_unbek, gruen=gruen,
                              dk_birke=5.0, dk_unbek=5.0, s_unbek=s_unbek)
    boden = (1.0 - POLLEN_G_WEIGHT_BIRKE) * gruen
    assert abs(g_neu - boden) < 1e-9
    assert g_neu >= boden - 1e-12


def test_stadtbaum_g_neu_verlangt_keine_negativen_dk():
    """dk ≥ 0: negative Eingaben werden defensiv auf 0 gestutzt, keine Erhöhung von Ĝ."""
    g_ohne = H.stadtbaum_g_neu(g_zelle=0.30, k_birke=0.30, k_unbek=0.0, gruen=0.30,
                               dk_birke=0.0, dk_unbek=0.0, s_unbek=0.12)
    g_negativ = H.stadtbaum_g_neu(g_zelle=0.30, k_birke=0.30, k_unbek=0.0, gruen=0.30,
                                  dk_birke=-0.10, dk_unbek=0.0, s_unbek=0.12)
    assert abs(g_ohne - g_negativ) < 1e-12
    assert abs(g_ohne - 0.30) < 1e-12


# ── (d) Zellausgabe: Kronenterme gleich den Zelleingaben, outcome/cost_eur unverändert ──

def _ctx_mit_kronenterme(canopy_birch_frac: float, canopy_unknown_frac: float,
                          green_frac: float, pop: float = 1000.0) -> CellContext:
    from app.services.engine.indicators import pollen_load

    band_pop = {"u20": 15_583_456, "a20_64": 49_163_992, "a65_74": 9_569_640,
                "a75_84": 6_294_744, "a85p": 2_844_213}
    pop_de = sum(band_pop.values())
    ci = {"pop": pop, "pop_age_bands": {b: pop * n / pop_de for b, n in band_pop.items()},
          "canopy_birch_frac": canopy_birch_frac,
          "canopy_unknown_frac": canopy_unknown_frac, "green_frac": green_frac}
    g = pollen_load(ci)
    return CellContext(
        ci=ci, hev={"hazards": {"POLLEN_LOAD": g}, "exposures": {}, "vulnerabilities": {}},
        hev_norm={"hazards": {}, "exposures": {}, "vulnerabilities": {}},
        indices={}, regional={"bundesland": "Hessen", "pollen_g_bar": 0.18})


def test_zellausgabe_traegt_kronenterme_gleich_den_zelleingaben():
    override_context.set_overrides({})
    ctx = _ctx_mit_kronenterme(0.22, 0.05, 0.30)
    res = impact.compute_all_cell_impacts(ctx)[CODE]
    assert res["canopy_birch_frac"] == 0.22
    assert res["canopy_unknown_frac"] == 0.05
    assert res["green_frac"] == 0.30


def test_outcome_und_cost_eur_bleiben_bitgleich_zum_vorzustand():
    """Die neuen Ausgabefelder ändern den bestehenden Rechenweg nicht.

    Festwerte neu ermittelt (T-1714) auf main, Commit
    a823f5821e2802381dd148f49c2985d6985971af, nachdem a_attr auf 0,27 (Ü-13) stand
    (alt 0,50; Verhältnis 0,54 = 0,27 ÷ 0,50). Befehl: ``bash scripts/testlauf.sh
    <Messdatei> -q -s``, die ``impact.compute_all_cell_impacts`` auf dieselbe Zelle
    (``_ctx_mit_kronenterme(0.22, 0.05, 0.30)``) anwendet und ``outcome``, ``cost_eur``,
    ``betroffene`` samt ``float.hex`` ausgibt. Sie sind hier mit ``==``
    (Bit-Genauigkeit über ``float.hex``) gebunden — kein Toleranzband, weil das
    Abnahmekriterium Bitgleichheit verlangt, nicht Näherung. Nachvollzogen im Diff
    gegen origin/main: die Änderung fügt in ``allergy_symptom_days`` ausschließlich
    drei neue Ausgabefelder NACH der outcome/cost_eur-Berechnung an; die Rechenzeilen
    selbst (``tage``, ``_result``, Kostensatz-Kopplung) sind unverändert.
    """
    override_context.set_overrides({})
    ctx = _ctx_mit_kronenterme(0.22, 0.05, 0.30)
    res = impact.compute_all_cell_impacts(ctx)[CODE]

    # Neu ermittelt auf main a823f5821e2802381dd148f49c2985d6985971af (a_attr 0,27, Ü-13).
    assert res["outcome"].hex() == float.fromhex("0x1.227f70d4a4f73p+7").hex()
    assert res["outcome"] == 145.24890770448437
    assert res["cost_eur"].hex() == float.fromhex("0x1.c245887ccc7f2p+9").hex()
    assert res["cost_eur"] == 900.543227767803
    assert res["betroffene"] == 107.35117871928871


def test_runner_speichert_kronenterme_wie_pollen_g():
    override_context.set_overrides({})
    ctx = _ctx_mit_kronenterme(0.22, 0.05, 0.30)
    impacts = impact.compute_all_cell_impacts(ctx)
    risks = build_cell_risks({CODE: 50.0}, impacts)
    assert risks[CODE]["pollen_g"] == round(impacts[CODE]["pollen_g"], 6)
    assert risks[CODE]["canopy_birch_frac"] == round(impacts[CODE]["canopy_birch_frac"], 6)
    assert risks[CODE]["canopy_unknown_frac"] == round(impacts[CODE]["canopy_unknown_frac"], 6)
    assert risks[CODE]["green_frac"] == round(impacts[CODE]["green_frac"], 6)


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__, "-v"]))
