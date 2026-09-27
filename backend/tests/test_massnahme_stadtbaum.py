"""Katalogmaßnahme allergenarme Stadtbaumwahl rechnet im Zelllauf (T-1600-cto).

Vorhaben T-1483-cto Teilpaket #2, setzt auf der Zellfunktion ``health.stadtbaum_g_neu``
(T-1599-cto) auf. Wie S158 (Sperre aus Befund 124) rechnet die Maßnahme
``LOW_ALLERGEN_TREE_SELECTION`` NICHT als Faktor auf ein gespeichertes Ergebnis, sondern
frisch aus den in der Zelle gespeicherten Roheingaben (Muster
``measure_service._s158_cell_effect``).

Geprüft wird (Abnahmekriterium T-1600-cto):
(a) Katalogeintrag: ``effect_model`` 'stadtbaum', ``linked_risk_codes`` =
    [EXPECTED_ANNUAL_ALLERGY_DAYS]; ``test_no_flat_measure_on_allergy_days``
    (test_methodik_96_golden.py) lässt genau 's158' und 'stadtbaum' zu.
(b) Der Zweig liest nur ``config['anteil_ersetzt'] = a``. Je Zelle mit Deckungsgrad
    ``frac`` gilt ``dk_Birke = a·frac·canopy_birch_frac``,
    ``dk_unbek = a·frac·canopy_unknown_frac``. Ĝ′ entsteht über
    ``health.stadtbaum_g_neu``, der Faktor ist
    ``pollen_zelltage(Ĝ′)/pollen_zelltage(Ĝ)`` (± 1e-12). Kommunenbeispiel Zelle 3:
    B 2.500, Ĝ 0,30, k_Birke 0,30, Grün 0,30, Ḡ₀ 0,18125, a = 1/3, frac 1 ⇒ Ĝ′ 0,2536.
(c) Ḡ₀ ist der gespeicherte ``pollen_g_bar0`` der Zelle; der Zweig ruft
    ``inputs.kommunale_pollen_referenz`` nicht auf.
(d) Ohne ``anteil_ersetzt`` oder mit ``frac`` 0 ist der Faktor 1,0.
(e) Eine Überschreibung von ``birch_group_share_default`` ändert Ḡ₀ im Ausgangsstand
    (``kommunale_pollen_referenz``); die Maßnahme hat kein eigenes Feld für
    Gattungsangaben.
(f) Der Docstring von ``inputs.kommunale_pollen_referenz`` enthält „gilt im
    Ausgangsstand; mit einer Maßnahme sinkt die Summe“.

Divergenzen an den CMO (siehe Ergebnis-Notiz des Tickets und Katalog-Kommentar):
- Verteilungsregel (Bericht §5 Z. 1113–1115: Eingabe getrennt nach Kronen mit und
  ohne Gattungs-Tag) — das Produkt hat nur EINE Eingabe ``anteil_ersetzt``.
- Baumkataster: das Produkt nimmt Gattungsangaben nur kommunenweit über s_unbek auf
  (§5 Z. 990–992), kein zellscharfes Kataster.
- Kosten der Maßnahme: der Bericht beziffert sie nicht.

DB-frei: prüft die reine Zellfunktion der Maßnahmen-Engine
(``measure_service._stadtbaum_cell_factor``) und den Katalogeintrag.
"""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402
from app.services import measure_service  # noqa: E402
from app.services.engine import inputs as inputs_mod  # noqa: E402
from app.services.engine import override_context  # noqa: E402
from app.services.engine.impact import health  # noqa: E402

CODE = "LOW_ALLERGEN_TREE_SELECTION"
RISK = "EXPECTED_ANNUAL_ALLERGY_DAYS"


def setup_function(_fn=None) -> None:
    override_context.set_overrides({})


def teardown_function(_fn=None) -> None:
    override_context.set_overrides({})


def _mdef() -> dict:
    return catalog.MEASURES_BY_CODE[CODE]


def _zelle3() -> dict:
    """Zelle 3 des Kommunenbeispiels (Vorhaben T-1483-cto, Planung #cto): B 2.500,
    Ĝ 0,30, k_Birke 0,30, k_unbek 0 (kein Gattungs-Tag-Anteil), Grün 0,30, Ḡ₀ 0,18125."""
    return {
        "betroffene": 2500.0,
        "delta_birke": 0.8085,
        "delta_graeser": 1.0710,
        "pollen_g": 0.30,
        "pollen_g_bar0": 0.18125,
        "canopy_birch_frac": 0.30,
        "canopy_unknown_frac": 0.0,
        "green_frac": 0.30,
    }


# ── (a) Katalogeintrag ───────────────────────────────────────────────────────

def test_katalogeintrag_effect_model_und_linked_risk_codes():
    m = _mdef()
    assert m["effect_model"] == "stadtbaum"
    assert m.get("linked_risk_codes") == [RISK]


def test_no_flat_measure_erlaubt_genau_s158_und_stadtbaum():
    """Deckt sich mit test_methodik_96_golden.py::test_no_flat_measure_on_allergy_days:
    genau 's158' und 'stadtbaum' sind zugelassene Zelllaufmodelle auf #96."""
    verknuepft = [m for m in catalog.MEASURES if RISK in (m.get("linked_risk_codes") or [])]
    effect_models = {m.get("effect_model") for m in verknuepft}
    assert effect_models == {"s158", "stadtbaum"}


def test_measure_hat_kein_eigenes_gattungsfeld():
    """Die Maßnahme selbst trägt kein Feld für die Gattungsverteilung (s_unbek/Birke/
    unbekannt) — die Eingabe ist ausschließlich ``config['anteil_ersetzt']``, die
    Gattungsverteilung kommt aus den OSM-Kronentermen der Zelle und dem risikoweiten
    ``birch_group_share_default``."""
    m = _mdef()
    verboten = ("birch", "gattung", "s_unbek", "unbekannt")
    treffer = [k for k in m if any(v in k.lower() for v in verboten)]
    assert not treffer, f"Unerwartetes Gattungsfeld an der Maßnahme: {treffer}"


# ── (b) Rechenbeispiel Zelle 3 ────────────────────────────────────────────────

def test_stadtbaum_cell_factor_zelle3_ergibt_g_neu_02536():
    a, frac = 1.0 / 3.0, 1.0
    cell = _zelle3()

    # Ĝ′ unabhängig nachgerechnet: dk_Birke = a·frac·k_Birke, dk_unbek = a·frac·k_unbek.
    dk_birke = a * frac * cell["canopy_birch_frac"]
    dk_unbek = a * frac * cell["canopy_unknown_frac"]
    g_neu = health.stadtbaum_g_neu(
        cell["pollen_g"], cell["canopy_birch_frac"], cell["canopy_unknown_frac"],
        cell["green_frac"], dk_birke, dk_unbek, s_unbek=0.12)
    assert abs(g_neu - 0.2536) < 1e-12

    factor = measure_service._stadtbaum_cell_factor({"anteil_ersetzt": a}, frac, cell)

    tage_b0, tage_g0 = health.pollen_zelltage(
        cell["betroffene"], cell["delta_birke"], cell["delta_graeser"],
        cell["pollen_g"], cell["pollen_g_bar0"], 0.70)
    tage_b1, tage_g1 = health.pollen_zelltage(
        cell["betroffene"], cell["delta_birke"], cell["delta_graeser"],
        g_neu, cell["pollen_g_bar0"], 0.70)
    erwartet = (tage_b1 + tage_g1) / (tage_b0 + tage_g0)
    assert abs(factor - erwartet) < 1e-12
    assert 0.0 < factor < 1.0


def test_stadtbaum_cell_factor_respektiert_lambda_veg_override():
    """Der Faktor läuft über λ (Override ``lambda_veg``), wie der S158-Zweig."""
    a, frac = 1.0 / 3.0, 1.0
    cell = _zelle3()
    factor_default = measure_service._stadtbaum_cell_factor({"anteil_ersetzt": a}, frac, cell)
    with override_context.override_scope(
            {"risks.EXPECTED_ANNUAL_ALLERGY_DAYS.impact.lambda_veg": 0.0}):
        factor_neutral = measure_service._stadtbaum_cell_factor(
            {"anteil_ersetzt": a}, frac, cell)
    # λ = 0 → P̂ ≡ 1 in beiden Ständen → Faktor exakt 1,0 (keine Umverteilung ohne λ).
    assert abs(factor_neutral - 1.0) < 1e-12
    assert factor_default != factor_neutral


# ── (c) Ḡ₀ ist der gespeicherte pollen_g_bar0, keine erneute Referenzbildung ──

def test_stadtbaum_ruft_kommunale_pollen_referenz_nicht_auf(monkeypatch):
    def _boom(*_args, **_kwargs):
        raise AssertionError(
            "_stadtbaum_cell_factor darf inputs.kommunale_pollen_referenz nicht aufrufen "
            "— Ḡ₀ ist der gespeicherte pollen_g_bar0 der Zelle aus dem Ausgangsstand.")

    monkeypatch.setattr(inputs_mod, "kommunale_pollen_referenz", _boom)
    cell = _zelle3()
    factor = measure_service._stadtbaum_cell_factor({"anteil_ersetzt": 1.0 / 3.0}, 1.0, cell)
    assert abs(factor - 0.877144) < 1e-5  # bleibt grün trotz "explodierender" Referenzfunktion


# ── (d) ohne anteil_ersetzt bzw. ohne Deckung: Faktor 1,0 ────────────────────

def test_stadtbaum_faktor_eins_ohne_anteil_ersetzt_oder_deckung():
    cell = _zelle3()
    assert measure_service._stadtbaum_cell_factor(None, 1.0, cell) == 1.0
    assert measure_service._stadtbaum_cell_factor({}, 1.0, cell) == 1.0
    assert measure_service._stadtbaum_cell_factor({"anteil_ersetzt": 0.0}, 1.0, cell) == 1.0
    assert measure_service._stadtbaum_cell_factor({"anteil_ersetzt": 0.5}, 0.0, cell) == 1.0


def test_stadtbaum_faktor_eins_ohne_zell_rohdaten():
    """Alt-Zelle vor der Neuberechnung (T-1599-cto): fehlende Kronenterme/Roheingaben
    ergeben Faktor 1,0, keine pauschale Ersatzwirkung."""
    unvollstaendig = {"betroffene": 100.0, "delta_birke": 0.5, "delta_graeser": 0.5,
                      "pollen_g": 0.3, "pollen_g_bar0": 0.2}  # keine Kronenterme
    factor = measure_service._stadtbaum_cell_factor(
        {"anteil_ersetzt": 0.5}, 1.0, unvollstaendig)
    assert factor == 1.0


# ── (e) birch_group_share_default wirkt auf Ḡ₀ im Ausgangsstand, nicht an der Maßnahme ──

def _kommune_cells() -> list[dict]:
    bands = {"u20": 200.0, "a20_64": 600.0, "a65_74": 100.0, "a75_84": 60.0, "a85p": 40.0}
    return [
        {"pop_age_bands": bands, "canopy_birch_frac": 0.30, "canopy_unknown_frac": 0.20,
         "green_frac": 0.10},
        {"pop_age_bands": bands, "canopy_birch_frac": 0.05, "canopy_unknown_frac": 0.10,
         "green_frac": 0.50},
    ]


def test_birch_group_share_override_aendert_g_bar0_im_ausgangsstand():
    cells = _kommune_cells()
    g_bar0_default = inputs_mod.kommunale_pollen_referenz(cells)
    with override_context.override_scope(
            {"risks.EXPECTED_ANNUAL_ALLERGY_DAYS.impact.birch_group_share_default": 0.9}):
        g_bar0_override = inputs_mod.kommunale_pollen_referenz(cells)
    assert g_bar0_default is not None and g_bar0_override is not None
    assert abs(g_bar0_default - g_bar0_override) > 1e-6


# ── (f) Docstring kommunale_pollen_referenz ──────────────────────────────────

def test_docstring_kommunale_pollen_referenz_nennt_ausgangsstand():
    doc = inputs_mod.kommunale_pollen_referenz.__doc__ or ""
    normalisiert = re.sub(r"\s+", " ", doc)
    assert "gilt im Ausgangsstand; mit einer Maßnahme sinkt die Summe" in normalisiert


if __name__ == "__main__":
    import pytest

    sys.exit(pytest.main([__file__, "-q"]))
