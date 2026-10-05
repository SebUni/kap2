"""Golden-Test des Prüfblocks ``beispiel_96_s158_wirkung`` (Bericht #96 §5.1, Z. 1335–1401)
an den Produktfunktionen — nicht am Beispiel-Block selbst (der läuft bereits über
``test_report_example_blocks_green`` in ``test_methodik_96_golden.py``).

Vorhabens-Kriterium (ii), T-1514-cto: bindet ``health.pollen_zelltage``,
``health.s158_vermiedene_tage``, ``health.t_warn_aus_dwd_anteil`` sowie die Zellausgabe von
``allergy_symptom_days`` (``tage_birke``, ``tage_graeser``, ``delta_birke``, ``delta_graeser``,
über ``impact.compute_all_cell_impacts``) an die im Prüfblock genannten Zahlenwerte.

**Zelllauf Berlin (ii, Kette).** Wie ``test_methodik_96_golden_betraege.py`` werden die Bänder
der Kette (§3.0, 402.103 Betroffene, region Mitte) vor dem Aufruf zu einer Zelle summiert (ohne
kommunale Ĝ-Referenz bleibt P̂ = 1 in beiden Pfaden identisch — linear, siehe dortige Begründung);
der Produktcode liefert dabei ``tage_birke``/``tage_graeser`` getrennt, die S158 braucht (Bericht
Integrationsauflage Punkt 1, Z. 1406).

**Zelllauf Berlin auf den gepinnten Zelldaten (golden96_zellen_11000000.csv.gz, ii).** Die
gepinnten Zellen tragen kein Ĝ (keine Kronendaten in der Anlage), P̂ ist deshalb 1 — wie im
Golden-Pfad von ``test_methodik_96_golden_betraege.py``. Anlage und Einlesen (``_zellen``,
``_zellbaender``) werden aus dieser Datei übernommen, nicht dupliziert oder verändert. Symptomtage
sind linear in der Bevölkerung je Band bei gleichem P̂; die Zellbänder werden deshalb vor dem
S158-Aufruf summiert (wie dort), statt 40.669 Einzelzellen zu durchlaufen — Ergebnis ist exakt
dasselbe wie eine Summe über getrennte Zellaufrufe mit p_hat ≡ 1.

**Zelllauf des Berichts ↔ Code.** Der Zelllauf des Berichts (§5.1) rechnet auf 399.171
Zusatztagen (Preisstand 2024) und weist 8.981 Tage / ≈ 55.700 € aus; der hier gebundene
Produktcode liefert auf den gepinnten Zelldaten 399.170,6 Zusatztage und damit 8.981 Tage /
≈ 55.684 € (2,47 Mio. € je Jahr, §3.0). Der Test bindet an den gemessenen Code-Wert
(T-1463-ceo/T-1431-ceo); die Toleranz des Prüfblocks gilt.

**Nicht gebunden.** ``e_Tag``, ``q_reich`` und ``q_handel`` sind keine Produktparameter (nur
``r_s158`` = ihr Produkt und ``t_warn_s158`` sind Registry-/Katalogwerte, s. Bericht Kap. 7); ihr
Anteil im Prüfblock (Herleitung ``r_roh``, Sensitivitäts-Spannen von ``e_Tag``) bleibt deshalb
außen vor.
"""

from __future__ import annotations

import os
import sys
from importlib import import_module

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402
from app.services.engine import impact, override_context  # noqa: E402
from app.services.engine.impact import health as H  # noqa: E402

_betraege = import_module("test_methodik_96_golden_betraege")

CODE = "EXPECTED_ANNUAL_ALLERGY_DAYS"
R_S158 = 0.03            # Kap. 7 pollen.r_s158 (Katalog default_reduction POLLEN_EARLY_WARNING)
T_WARN = 0.75            # Kap. 7 pollen.t_warn_s158


def _c_tag() -> float:
    return catalog.risk_default_cost_per_outcome(catalog.RISKS_BY_CODE[CODE])


def _tage_birke_graeser(bands: dict[str, float]) -> tuple[float, float, dict]:
    """(ΔTage Birke, ΔTage Gräser, Roheingaben) aus der Zellausgabe von ``allergy_symptom_days``."""
    override_context.set_overrides({})
    ctx = _betraege._ctx(bands)
    out = impact.compute_all_cell_impacts(ctx)[CODE]
    return out["tage_birke"], out["tage_graeser"], out


def _kette_tage_birke_graeser() -> tuple[float, float]:
    """ΔTage je Gruppe für die Beispielkommune Berlin, B = 402.103 (Bericht, gerundet wie im
    Prüfblock Z. 1352), δ_B/δ_G aus der Zellausgabe von ``allergy_symptom_days`` (Region Mitte,
    dieselbe Kette wie ``test_kette_berlin`` in ``test_methodik_96_golden_betraege.py``).
    Gebunden über ``health.pollen_zelltage`` (ohne Ĝ-Referenz ⇒ P̂ = 1, wie im Bericht).
    """
    _, _, roh = _tage_birke_graeser(_betraege.POP_KETTE)
    return H.pollen_zelltage(
        402_103, roh["delta_birke"], roh["delta_graeser"], g_zelle=0.0, g_bar0=None, lam=0.70)


# ── Kette Berlin (§5.1, Z. 1309–1316) ────────────────────────────────────────

def test_kette_berlin_s158():
    """Ebenen 1–5: 175.554/232.552 Tage, 306.080 gewarnt, 9.182 vermieden, ≈56.900 €."""
    tage_birke, tage_graeser = _kette_tage_birke_graeser()
    assert abs(tage_birke - 175_554) < 1, f"{tage_birke:.1f}"
    assert abs(tage_graeser - 232_552) < 1, f"{tage_graeser:.1f}"
    assert abs((tage_birke + tage_graeser) - 408_106) < 1

    gewarnt = T_WARN * tage_birke + T_WARN * tage_graeser
    assert abs(gewarnt - 306_080) < 1, f"{gewarnt:.1f}"

    vermieden = H.s158_vermiedene_tage(tage_birke, tage_graeser, 1, R_S158, T_WARN, T_WARN)
    assert abs(vermieden - 9_182) < 1, f"{vermieden:.1f}"

    euro = vermieden * _c_tag()
    assert abs(euro - 56_900) < 100, f"{euro:.1f} €"


def test_band_s158():
    """Bandenden (Aushang-Fall / aktivierte Warnkette): 1.020/40.811 Tage, ≈6.300/253.000 €."""
    tage_birke, tage_graeser = _kette_tage_birke_graeser()
    c_tag = _c_tag()

    unten = H.s158_vermiedene_tage(tage_birke, tage_graeser, 1, 0.005, 0.50, 0.50)
    assert abs(unten - 1_020) < 1, f"{unten:.1f}"
    assert abs(unten * c_tag - 6_300) < 50, f"{unten * c_tag:.1f} €"

    oben = H.s158_vermiedene_tage(tage_birke, tage_graeser, 1, 0.10, 1.00, 1.00)
    assert abs(oben - 40_811) < 1, f"{oben:.1f}"
    assert abs(oben * c_tag - 253_000) < 50, f"{oben * c_tag:.1f} €"


def test_t_warn_sensitivity():
    """Sensitivität t_warn (r fest bei 0,03): 6.122 Tage (0,50) und 12.243 Tage (1,00)."""
    tage_birke, tage_graeser = _kette_tage_birke_graeser()

    tw050 = H.s158_vermiedene_tage(tage_birke, tage_graeser, 1, R_S158, 0.50, 0.50)
    assert abs(tw050 - 6_122) < 1, f"{tw050:.1f}"

    tw100 = H.s158_vermiedene_tage(tage_birke, tage_graeser, 1, R_S158, 1.00, 1.00)
    assert abs(tw100 - 12_243) < 1, f"{tw100:.1f}"


# ── Allee-Zelle (§5.1, Z. 1320–1322) ─────────────────────────────────────────

def test_allee_zelle_s158():
    """100 Betroffene, P̂ = 1,7: 172,5 Zusatztage, 3,88 vermieden (≈24 €); A = 0 ⇒ 0."""
    _, _, roh = _tage_birke_graeser(_betraege.POP_KETTE)
    delta_birke, delta_graeser = roh["delta_birke"], roh["delta_graeser"]

    # P̂ = 1,7 über pollen_zelltage selbst (g_zelle/g_bar0 = 2, λ = 0,70 Kap.-7-Default).
    tage_birke, tage_graeser = H.pollen_zelltage(
        100, delta_birke, delta_graeser, g_zelle=2.0, g_bar0=1.0, lam=0.70)
    zelle = tage_birke + tage_graeser
    assert abs(zelle - 172.5) < 0.05, f"{zelle:.3f}"

    vermieden = H.s158_vermiedene_tage(tage_birke, tage_graeser, 1, R_S158, T_WARN, T_WARN)
    assert abs(vermieden - 3.88) < 0.005, f"{vermieden:.4f}"
    assert abs(vermieden * _c_tag() - 24) < 0.5, f"{vermieden * _c_tag():.2f} €"

    ausserhalb = H.s158_vermiedene_tage(tage_birke, tage_graeser, 0, R_S158, T_WARN, T_WARN)
    assert ausserhalb == 0.0


# ── Ersetzungspfad (§5.1, Z. 1379–1383) ──────────────────────────────────────

def test_ersetzungspfad_dwd_anteil():
    """t_warn_aus_dwd_anteil: m = 0,525 ⇒ 0,75; m = 0,80 (gedeckelt) ⇒ 1,0 (f = 0,70)."""
    assert abs(H.t_warn_aus_dwd_anteil(0.525, 0.70) - 0.75) < 1e-9
    assert H.t_warn_aus_dwd_anteil(0.80, 0.70) == 1.0


# ── Zelllauf Berlin auf den gepinnten Zelldaten (Z. 1317–1319, 1366) ─────────

def test_zelllauf_berlin_golden96():
    """A = 1: 8.981 vermiedene Tage, ≈55.684 €; Faktor 0,0225 auf die Summe (siehe Docstring)."""
    zellbaender = _betraege._zellbaender(_betraege.BERLIN)
    tage_birke, tage_graeser, _ = _tage_birke_graeser(zellbaender)
    summe = tage_birke + tage_graeser

    vermieden = H.s158_vermiedene_tage(tage_birke, tage_graeser, 1, R_S158, T_WARN, T_WARN)
    assert abs(vermieden - 8_981) < 1, f"{vermieden:.1f}"

    euro = vermieden * _c_tag()
    assert abs(euro - 55_684) < 50, f"{euro:.1f} €"

    faktor = R_S158 * T_WARN
    assert abs(faktor - 0.0225) < 1e-9
    assert abs(vermieden / summe - 0.0225) < 1e-9
    assert abs(faktor * summe - vermieden) < 1e-6


if __name__ == "__main__":
    import pytest

    sys.exit(pytest.main([__file__, "-q"]))
