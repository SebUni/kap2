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

Fixture ``_zelle3``: δ 0,8085 / 1,0710 ist der Stand vor Ü-13 (a_attr 0,50) und bleibt
als Testeingabe. Der geprüfte Faktor ist ein Verhältnis und ändert sich nicht, wenn beide
δ gemeinsam skaliert werden (0,8085 / 1,0710 = 0,43659 / 0,57834 ≈ 0,7549).

DB-frei: prüft die reine Zellfunktion der Maßnahmen-Engine
(``measure_service._stadtbaum_cell_factor``) und den Katalogeintrag.
"""

from __future__ import annotations

import os
import re
import sys

import pytest

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
    Ĝ 0,30, k_Birke 0,30, k_unbek 0 (kein Gattungs-Tag-Anteil), Grün 0,30, Ḡ₀ 0,18125.

    Vermerk zu δ: δ_Birke 0,8085 / δ_Gräser 1,0710 ist der Stand vor Ü-13 (a_attr 0,50)
    und bleibt als Testeingabe. Der geprüfte Faktor ist ein Verhältnis; er ändert sich
    nicht, wenn beide δ gemeinsam skaliert werden (0,8085 / 1,0710 = 0,43659 / 0,57834
    ≈ 0,7549). Die Werte der Fixture bleiben deshalb unverändert."""
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


# ── (g) s_unbek der Maßnahme ist der des Ausgangslaufs (Ü-10, Befund 252) ─────────────

S_UNBEK_ALLEE_KRONE = 0.3625


def _allee_zelle_ohne_tag(**extra) -> dict:
    """Allee-Zelle nach Ü-13 ohne Gattungs-Tag: Kronenanteil 0,3625 nur in
    ``canopy_unknown_frac``, Grün 0,3625, 100 Betroffene, Ḡ₀ 0,18125. Ĝ im Ausgangslauf mit
    s_unbek 0,12: 0,464·(0,12·0,3625) + 0,536·0,3625 = 0,21448."""
    zelle = {
        "index": 172.5, "outcome": 172.5,
        "betroffene": 100.0, "delta_birke": 0.43659, "delta_graeser": 0.57834,
        "pollen_g": 0.21448, "pollen_g_bar0": 0.18125,
        "canopy_birch_frac": 0.0, "canopy_unknown_frac": S_UNBEK_ALLEE_KRONE,
        "green_frac": S_UNBEK_ALLEE_KRONE,
    }
    zelle.update(extra)
    return zelle


_A_ALLEE = 0.078125 / S_UNBEK_ALLEE_KRONE
_OVERRIDE_S_UNBEK = "risks.EXPECTED_ANNUAL_ALLERGY_DAYS.impact.birch_group_share_default"


def _summary_mit_overrides(zelle: dict, overrides: dict, monkeypatch) -> dict:
    """impact_summary der Stadtbaumwahl über ``compute_impact`` (DB-frei, Doppel aus
    test_massnahme_stadtbaum_ausgabe); die vermiedenen Tage der Zelle (auf drei Stellen
    gerundet, das Kommunenfeld rundet auf eine) stehen zusätzlich unter ``_zelltage``."""
    from app.services import parameter_registry
    from test_massnahme_stadtbaum_ausgabe import _run

    monkeypatch.setattr(parameter_registry, "overrides_map", lambda *_a, **_k: dict(overrides))
    summary, added = _run(zelle, {"anteil_ersetzt": _A_ALLEE}, monkeypatch)
    zeile = next(o for o in added if o.measure_id == 1)
    return {**summary, "_zelltage": (zeile.savings or {}).get("stadtbaum_avoided_days")}


def test_s_unbek_der_massnahme_aus_dem_ausgangslauf(monkeypatch):
    """Ausgangslauf mit s_unbek 0,12 (Zellfeld ``pollen_s_unbek``); die spätere
    Überschreibung 0,25 ändert die Senkung nicht (1,71 statt 3,55 vermiedene Tage), das
    impact_summary sagt, dass sie erst mit einem neuen Zelllauf gilt. Ohne Überschreibung
    ebenfalls 1,71 Tage und kein Hinweis."""
    zelle = _allee_zelle_ohne_tag(pollen_s_unbek=0.12)

    # Ohne Überschreibung: 1,71 Tage, kein Hinweis.
    ohne = _summary_mit_overrides(zelle, {}, monkeypatch)
    assert ohne["_zelltage"] == pytest.approx(1.71, abs=0.01)
    assert "stadtbaum_s_unbek_hinweis" not in ohne

    # Überschreibung 0,25 nach dem Lauf: weiter 1,71 Tage, nicht 3,55; Hinweis im Summary.
    mit = _summary_mit_overrides(zelle, {_OVERRIDE_S_UNBEK: 0.25}, monkeypatch)
    assert mit["_zelltage"] == pytest.approx(1.71, abs=0.01)
    assert abs(mit["_zelltage"] - 3.55) > 1.0
    assert mit["stadtbaum_avoided_days_total"] == pytest.approx(1.7, abs=0.05)
    hinweis = mit["stadtbaum_s_unbek_hinweis"]
    assert "0,25" in hinweis and "0,12" in hinweis
    assert "neuen Zelllauf" in hinweis

    # Zellebene: Faktor und Tage hängen nicht an der Überschreibung.
    a = {"anteil_ersetzt": _A_ALLEE}
    f_ohne, t_ohne, _ = measure_service._stadtbaum_cell_effect(a, 1.0, zelle)
    with override_context.override_scope({_OVERRIDE_S_UNBEK: 0.25}):
        f_mit, t_mit, _ = measure_service._stadtbaum_cell_effect(a, 1.0, zelle)
    assert f_ohne == f_mit and t_ohne == t_mit


def test_s_unbek_ausgangslauf_ohne_feld_rechnet_mit_heutigem_wert_und_sagt_es(monkeypatch):
    """Gespeicherter Lauf vor dieser Änderung (kein ``pollen_s_unbek``): die Senkung rechnet
    mit dem Wert von heute, das impact_summary verlangt den neuen Ausgangslauf — keine
    stille Zahl."""
    zelle = _allee_zelle_ohne_tag()
    assert "pollen_s_unbek" not in zelle

    summary = _summary_mit_overrides(zelle, {_OVERRIDE_S_UNBEK: 0.25}, monkeypatch)
    assert summary["_zelltage"] == pytest.approx(3.55, abs=0.01)
    hinweis = summary["stadtbaum_s_unbek_hinweis"]
    assert "Rechnen Sie den Ausgangslauf neu" in hinweis and "0,25" in hinweis
    assert "älter" in hinweis and "Kronen ohne Gattung" in hinweis and "Änderung" not in hinweis

    ohne = _summary_mit_overrides(zelle, {}, monkeypatch)
    assert ohne["_zelltage"] == pytest.approx(1.71, abs=0.01)
    assert "Rechnen Sie den Ausgangslauf neu" in ohne["stadtbaum_s_unbek_hinweis"]


def test_zelle_legt_s_unbek_des_laufs_ab():
    """``runner.build_cell_risks`` legt neben ``pollen_g_bar0`` den s_unbek des Laufs ab
    (Override der Kommune oder Vorgabe 0,12); Risiken ohne Pollenrechnung tragen das Feld
    nicht."""
    from app.services.engine import runner

    impacts = {RISK: {"outcome": 1.0, "cost_eur": 6.2, "pollen_g": 0.21448,
                      "pollen_g_bar0": 0.18125},
               "OTHER": {"outcome": 1.0, "cost_eur": 1.0}}
    indices = {RISK: 50.0, "OTHER": 10.0}

    risks = runner.build_cell_risks(indices, impacts)
    assert risks[RISK]["pollen_s_unbek"] == 0.12
    assert "pollen_s_unbek" not in risks["OTHER"]

    with override_context.override_scope({_OVERRIDE_S_UNBEK: 0.0}):
        assert runner.build_cell_risks(indices, impacts)[RISK]["pollen_s_unbek"] == 0.0
    with override_context.override_scope({_OVERRIDE_S_UNBEK: 0.25}):
        assert runner.build_cell_risks(indices, impacts)[RISK]["pollen_s_unbek"] == 0.25


if __name__ == "__main__":

    sys.exit(pytest.main([__file__, "-q"]))
