"""Hebel S158 — Pollen-Frühwarnung (Bericht #96 §5.1, Beispiel-Block ``beispiel_96_s158_wirkung``).

Sperre aus Befund 124 aufgehoben (T-1513-cto, Integrationsauflage Z. 1408–1415): Die
Maßnahme ``POLLEN_EARLY_WARNING`` wirkt im Zelllauf, nicht als pauschaler Faktor auf
gespeicherte Ergebnisse.

``ΔTage_vermieden,Zelle = A_Zelle · r_S158 · Σ_g t_warn,g · ΔTage_g,Zelle``

Die Gruppentage kommen über ``health.pollen_zelltage`` frisch aus den Roheingaben der
Zelle (``betroffene``, ``delta_birke``, ``delta_graeser``, ``pollen_g``,
``pollen_g_bar0``), nicht aus gespeicherten Summen ``tage_birke``/``tage_graeser`` —
so wirkt eine spätere Vegetationsmaßnahme (Stadtbaumwahl, T-1483-cto) multiplikativ
zusammen mit S158, statt von ihr überschrieben zu werden.

Geprüft wird (Abnahmekriterium T-1513-cto):
(a) ``POLLEN_EARLY_WARNING`` führt EXPECTED_ANNUAL_ALLERGY_DAYS in ``linked_risk_codes``
    und ``effect_model`` = 's158'.
(b) Eine Allee-Zelle (Betroffene 100, Berlin, Ĝ/Ḡ₀ = 2) mit voller Deckung ergibt
    7,19 ± 0,005 vermiedene Tage, mit Deckung 0 genau 0.
(c) Die Überschreibung ``t_warn_s158`` = 1,0 hebt die vermiedenen Tage auf das
    4/3-Fache (0,75 → 1,00).
(d) Eine Zelle ohne ``tage_birke``/``tage_graeser`` (bzw. ihre Roheingaben) behält den
    Faktor 1,0; es gibt keine pauschalen 0,03.

DB-frei: prüft die reine Rechenfunktion in ``health`` und den Zellfaktor der
Maßnahmen-Engine (``measure_service._s158_cell_factor``).
"""

from __future__ import annotations

import pytest

from app.data import catalog, catalog_parked
from app.services import measure_service
from app.services.engine import override_context
from app.services.engine.impact import health

CODE = "POLLEN_EARLY_WARNING"
RISK = "EXPECTED_ANNUAL_ALLERGY_DAYS"

# Berlin, Region Mitte (Bericht #96 §5.1 Z. 1200–1206 / §3.0 Ebenen 4–6).
DELTA_BIRKE = 0.8085
DELTA_GRAESER = 1.0710
R_S158 = 0.03      # Katalog default_reduction, Block pollen.r_s158
T_WARN = 0.75      # Registry-Parameter t_warn_s158, Block pollen.t_warn_s158
LAM = 0.70         # lambda_veg-Default


def setup_function(_fn=None) -> None:
    override_context.set_overrides({})


def teardown_function(_fn=None) -> None:
    override_context.set_overrides({})


def _mdef() -> dict:
    return catalog.MEASURES_BY_CODE[CODE]


def _allee_cell(betroffene: float = 100.0, g_verhaeltnis: float = 2.0,
               g_bar0: float = 0.2) -> dict:
    """Roheingaben einer Allee-Zelle mit Ĝ/Ḡ₀ = ``g_verhaeltnis`` (Bericht-Beispiel)."""
    return {
        "betroffene": betroffene,
        "delta_birke": DELTA_BIRKE,
        "delta_graeser": DELTA_GRAESER,
        "pollen_g": g_bar0 * g_verhaeltnis,
        "pollen_g_bar0": g_bar0,
    }


def _gruppentage(cell: dict) -> tuple[float, float]:
    return health.pollen_zelltage(
        cell["betroffene"], cell["delta_birke"], cell["delta_graeser"],
        cell["pollen_g"], cell["pollen_g_bar0"], lam=LAM)


# ── (a) Verknüpfung: Zelllauf-Modell statt Sperre ─────────────────────────────

def test_measure_is_active_linked_via_zelllauf_model():
    assert CODE in catalog.MEASURES_BY_CODE
    assert CODE not in {m["code"] for m in catalog_parked._PARKED_MEASURES}
    m = _mdef()
    assert m["effect_model"] == "s158"
    assert RISK in (m.get("linked_risk_codes") or [])
    assert not (m.get("qualitative_risk_codes") or [])
    assert m["default_reduction"] == pytest.approx(R_S158)


# ── (b) Allee-Zelle: 7,19 vermiedene Tage bei voller Deckung, 0 bei Deckung 0 ──

def test_allee_cell_full_coverage_7_19_avoided_days():
    cell = _allee_cell()
    tage_birke, tage_graeser = _gruppentage(cell)
    # P̂ = 1 + λ·(Ĝ/Ḡ₀ − 1) = 1 + 0,70·(2 − 1) = 1,7; Betroffene·δ·P̂ = 319,5 Tage (Bericht-Beispiel).
    assert (tage_birke + tage_graeser) == pytest.approx(319.5, abs=0.05)

    vermieden = health.s158_vermiedene_tage(
        tage_birke, tage_graeser, a_zelle=1.0, r=R_S158, t_warn_b=T_WARN, t_warn_g=T_WARN)
    assert vermieden == pytest.approx(7.19, abs=0.005)

    factor = measure_service._s158_cell_factor(_mdef(), 1.0, cell)
    total = tage_birke + tage_graeser
    assert factor == pytest.approx(1.0 - vermieden / total, rel=1e-9)


def test_allee_cell_zero_coverage_is_exactly_zero():
    cell = _allee_cell()
    tage_birke, tage_graeser = _gruppentage(cell)
    vermieden = health.s158_vermiedene_tage(
        tage_birke, tage_graeser, a_zelle=0.0, r=R_S158, t_warn_b=T_WARN, t_warn_g=T_WARN)
    assert vermieden == 0.0

    factor = measure_service._s158_cell_factor(_mdef(), 0.0, cell)
    assert factor == 1.0


# ── (c) Überschreibung t_warn_s158 = 1,0 hebt vermiedene Tage auf das 4/3-Fache ──

def test_t_warn_override_scales_avoided_days_by_four_thirds():
    cell = _allee_cell()
    tage_birke, tage_graeser = _gruppentage(cell)
    total = tage_birke + tage_graeser

    factor_basis = measure_service._s158_cell_factor(_mdef(), 1.0, cell)
    vermieden_basis = (1.0 - factor_basis) * total

    override_context.set_overrides({f"risks.{RISK}.impact.t_warn_s158": 1.0})
    try:
        factor_voll = measure_service._s158_cell_factor(_mdef(), 1.0, cell)
    finally:
        override_context.set_overrides({})
    vermieden_voll = (1.0 - factor_voll) * total

    assert vermieden_voll == pytest.approx(vermieden_basis * 4.0 / 3.0, rel=1e-9)
    # Gegenprobe direkt über die reine Funktion (ohne den Umweg über den Faktor).
    direkt_basis = health.s158_vermiedene_tage(
        tage_birke, tage_graeser, 1.0, R_S158, T_WARN, T_WARN)
    direkt_voll = health.s158_vermiedene_tage(
        tage_birke, tage_graeser, 1.0, R_S158, 1.0, 1.0)
    assert direkt_voll == pytest.approx(direkt_basis * 4.0 / 3.0, rel=1e-9)
    assert vermieden_basis == pytest.approx(direkt_basis, rel=1e-9)


# ── (c2) Überschreibung lambda_veg der Kommune wirkt auf den Zellfaktor (T-1592-ceo) ──

def test_lambda_veg_override_changes_avoided_days_not_factor():
    """λ aus der Parameterliste wirkt in der Zelle (T-1592-ceo).

    P̂ = 1 + λ·(Ĝ/Ḡ₀ − 1) skaliert beide Gruppentage gleich und kürzt sich im Faktor
    1 − vermieden/Σ Tage heraus; der Faktor hängt von λ deshalb nicht ab. Die
    vermiedenen Tage (zweite Rückgabe von ``_s158_cell_effect``) folgen λ.
    """
    cell = _allee_cell()
    factor_basis, tage_basis, _ = measure_service._s158_cell_effect(_mdef(), 1.0, cell)

    override_context.set_overrides({f"risks.{RISK}.impact.lambda_veg": 0.50})
    try:
        factor_050, tage_050, _ = measure_service._s158_cell_effect(_mdef(), 1.0, cell)
    finally:
        override_context.set_overrides({})

    assert tage_050 != pytest.approx(tage_basis, abs=1e-6)
    # Gegenprobe über die reine Funktion mit λ = 0,50: P̂ = 1 + 0,5·(2 − 1) = 1,5.
    tb, tg = health.pollen_zelltage(
        cell["betroffene"], cell["delta_birke"], cell["delta_graeser"],
        cell["pollen_g"], cell["pollen_g_bar0"], lam=0.50)
    vermieden = health.s158_vermiedene_tage(tb, tg, 1.0, R_S158, T_WARN, T_WARN)
    assert tage_050 == pytest.approx(vermieden, rel=1e-9)
    assert factor_050 == pytest.approx(factor_basis, rel=1e-9)


# ── (d) Zelle ohne Gruppentage/Roheingaben: Faktor 1,0, keine pauschalen 0,03 ────

def test_cell_without_group_day_inputs_keeps_factor_one():
    mdef = _mdef()
    # Alt-Zelle vor der Neuberechnung: kein delta_birke/delta_graeser/pollen_g/betroffene.
    factor = measure_service._s158_cell_factor(mdef, 1.0, {"outcome": 500.0})
    assert factor == 1.0
    assert factor != pytest.approx(1.0 - R_S158)

    # Auch bei nur teilweise vorhandenen Roheingaben keine Wirkung (kein Rückfall auf 0,03).
    teil = {"betroffene": 100.0, "delta_birke": DELTA_BIRKE}
    assert measure_service._s158_cell_factor(mdef, 1.0, teil) == 1.0


if __name__ == "__main__":
    import sys

    sys.exit(pytest.main([__file__, "-q"]))
