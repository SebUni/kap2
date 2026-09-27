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

**Divergenz Bericht ↔ Code (kein stiller Fix, Befund an den CMO, s. Ticket-Ergebnis).** Der
Zelllauf des Berichts (Z. 1318, Z. 1366) rechnet auf 740.723 Zusatztagen (Preisstand 2024) und
weist 16.666 Tage / ≈ 103.300 € aus; der hier gebundene Produktcode liefert auf den gepinnten
Zelldaten 739.204,8 Zusatztage und damit 16.632 Tage / ≈ 103.119 €. Der Test bindet an den
gemessenen Code-Wert (T-1463-ceo/T-1431-ceo: dieselbe Ursache wie 4,59 gegen 4,58 Mio. € in
§3.0), nicht an die Berichtszahlen 16.666/103.300; die Toleranz des Prüfblocks gilt, bis der
Bericht für den Zelllauf eine eigene nennt.

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
    """Ebenen 1–5: 325.100/430.652 Tage, 566.814 gewarnt, 17.004 vermieden, ≈105.400 €."""
    tage_birke, tage_graeser = _kette_tage_birke_graeser()
    assert abs(tage_birke - 325_100) < 1, f"{tage_birke:.1f}"
    assert abs(tage_graeser - 430_652) < 1, f"{tage_graeser:.1f}"
    assert abs((tage_birke + tage_graeser) - 755_753) < 1

    gewarnt = T_WARN * tage_birke + T_WARN * tage_graeser
    assert abs(gewarnt - 566_814) < 1, f"{gewarnt:.1f}"

    vermieden = H.s158_vermiedene_tage(tage_birke, tage_graeser, 1, R_S158, T_WARN, T_WARN)
    assert abs(vermieden - 17_004) < 1, f"{vermieden:.1f}"

    euro = vermieden * _c_tag()
    assert abs(euro - 105_400) < 100, f"{euro:.1f} €"


def test_band_s158():
    """Bandenden (Aushang-Fall / aktivierte Warnkette): 1.889/75.575 Tage, ≈11.700/468.600 €."""
    tage_birke, tage_graeser = _kette_tage_birke_graeser()
    c_tag = _c_tag()

    unten = H.s158_vermiedene_tage(tage_birke, tage_graeser, 1, 0.005, 0.50, 0.50)
    assert abs(unten - 1_889) < 1, f"{unten:.1f}"
    assert abs(unten * c_tag - 11_700) < 50, f"{unten * c_tag:.1f} €"

    oben = H.s158_vermiedene_tage(tage_birke, tage_graeser, 1, 0.10, 1.00, 1.00)
    assert abs(oben - 75_575) < 1, f"{oben:.1f}"
    assert abs(oben * c_tag - 468_600) < 50, f"{oben * c_tag:.1f} €"


def test_t_warn_sensitivity():
    """Sensitivität t_warn (r fest bei 0,03): 11.336 Tage (0,50) und 22.673 Tage (1,00)."""
    tage_birke, tage_graeser = _kette_tage_birke_graeser()

    tw050 = H.s158_vermiedene_tage(tage_birke, tage_graeser, 1, R_S158, 0.50, 0.50)
    assert abs(tw050 - 11_336) < 1, f"{tw050:.1f}"

    tw100 = H.s158_vermiedene_tage(tage_birke, tage_graeser, 1, R_S158, 1.00, 1.00)
    assert abs(tw100 - 22_673) < 1, f"{tw100:.1f}"


# ── Allee-Zelle (§5.1, Z. 1320–1322) ─────────────────────────────────────────

def test_allee_zelle_s158():
    """100 Betroffene, P̂ = 1,7: 319,5 Zusatztage, 7,19 vermieden (≈45 €); A = 0 ⇒ 0."""
    _, _, roh = _tage_birke_graeser(_betraege.POP_KETTE)
    delta_birke, delta_graeser = roh["delta_birke"], roh["delta_graeser"]

    # P̂ = 1,7 über pollen_zelltage selbst (g_zelle/g_bar0 = 2, λ = 0,70 Kap.-7-Default).
    tage_birke, tage_graeser = H.pollen_zelltage(
        100, delta_birke, delta_graeser, g_zelle=2.0, g_bar0=1.0, lam=0.70)
    zelle = tage_birke + tage_graeser
    assert abs(zelle - 319.5) < 0.05, f"{zelle:.3f}"

    vermieden = H.s158_vermiedene_tage(tage_birke, tage_graeser, 1, R_S158, T_WARN, T_WARN)
    assert abs(vermieden - 7.19) < 0.005, f"{vermieden:.4f}"
    assert abs(vermieden * _c_tag() - 45) < 0.5, f"{vermieden * _c_tag():.2f} €"

    ausserhalb = H.s158_vermiedene_tage(tage_birke, tage_graeser, 0, R_S158, T_WARN, T_WARN)
    assert ausserhalb == 0.0


# ── Ersetzungspfad (§5.1, Z. 1379–1383) ──────────────────────────────────────

def test_ersetzungspfad_dwd_anteil():
    """t_warn_aus_dwd_anteil: m = 0,525 ⇒ 0,75; m = 0,80 (gedeckelt) ⇒ 1,0 (f = 0,70)."""
    assert abs(H.t_warn_aus_dwd_anteil(0.525, 0.70) - 0.75) < 1e-9
    assert H.t_warn_aus_dwd_anteil(0.80, 0.70) == 1.0


# ── Zelllauf Berlin auf den gepinnten Zelldaten (Z. 1317–1319, 1366) ─────────

def test_zelllauf_berlin_golden96():
    """A = 1: 16.632 vermiedene Tage, ≈103.119 €; Faktor 0,0225 auf die Summe (siehe Docstring)."""
    zellbaender = _betraege._zellbaender(_betraege.BERLIN)
    tage_birke, tage_graeser, _ = _tage_birke_graeser(zellbaender)
    summe = tage_birke + tage_graeser

    vermieden = H.s158_vermiedene_tage(tage_birke, tage_graeser, 1, R_S158, T_WARN, T_WARN)
    assert abs(vermieden - 16_632) < 1, f"{vermieden:.1f}"

    euro = vermieden * _c_tag()
    assert abs(euro - 103_119) < 50, f"{euro:.1f} €"

    faktor = R_S158 * T_WARN
    assert abs(faktor - 0.0225) < 1e-9
    assert abs(vermieden / summe - 0.0225) < 1e-9
    assert abs(faktor * summe - vermieden) < 1e-6


if __name__ == "__main__":
    import pytest

    sys.exit(pytest.main([__file__, "-q"]))
