"""Golden-Test der Rechenbeispiele Stadtbaumwahl (Bericht #96 §5, Z. 999–1035) an den
Produktfunktionen — nicht am Beispiel-Block selbst (der läuft bereits über
``test_report_example_blocks_green`` in ``test_methodik_96_golden.py``).

Vorhabens-Kriterium (i), T-1601-cto: bindet ``health.stadtbaum_g_neu``,
``health.pollen_zelltage`` und den Zweig ``'stadtbaum'`` in ``measure_service``
(``measure_service._stadtbaum_cell_factor``) an die im Bericht genannten Zahlenwerte —
δ_R = 1,01493 (Ebene 6, wie im S158-Golden-Test), λ = 0,7 und c_Tag = 6,20 € aus dem Katalog
(Kap. 7 ``pollen.lambda_veg``/``pollen.c_tag``, wie in ``test_methodik_96_s158_golden.py``).

**Allee-Zelle (§5, Z. 999–1006).** B = 100, Ḡ₀ = 0,18125, Kronenanteil mit Gattungs-Tag
Birkengruppe = Grünanteil = 0,3625 ⇒ Ĝ = 0,464 × 0,3625 + 0,536 × 0,3625 = 0,3625 (Gewichte
summieren zu 1, deshalb Ĝ = k_Birke = Grün, wie im Bericht). ``anteil_ersetzt`` =
0,078125 / 0,3625 (die Pflanzung senkt den Kronenanteil um 0,2 × Ḡ₀ / 0,464 = 0,078125 Pp.,
§5 Z. 1000–1004), ``frac`` = 1.

**Kommune (§5, Z. 1016–1035; Toleranzen des Prüfblocks ``beispiel_96_stadtbaum_kommunensumme``,
Z. 1058–1100).** Vier Zellen wie im Prüfblock (B = 1.000/4.000/2.500/500, Ĝ = 0/0,10/0,30/0,60,
``pollen_g_bar0`` = 0,18125 in allen Zellen, unverändert durch die Maßnahme). In den Zellen 3
und 4 wird ``anteil_ersetzt`` = 1/3 mit ``frac`` = 1 über ``measure_service`` gerechnet; Zellen 1
und 2 bleiben ohne Deckung (``frac`` = 0) unverändert.

δ_B/δ_G werden hier — anders als im S158-Golden-Test — nicht getrennt gebraucht: Der Bericht
rechnet die Beispiele mit der kombinierten Größe δ_R (Ebene 6). Gebunden wird deshalb über
``health.pollen_zelltage(betroffene, delta_r, 0.0, …)``; die Summe beider Rückgabewerte ist
bitgleich zu ``betroffene · delta_r · P̂`` (§5.1 Formel, dieselbe Linearität wie im S158-Test),
unabhängig davon, wie δ_R auf ``delta_b``/``delta_g`` verteilt wird — der Zweig ``'stadtbaum'``
in ``measure_service`` prüft dieselbe Invarianz zusätzlich über ``_stadtbaum_cell_factor``, der
ausschließlich mit dem Verhältnis der Summen rechnet.

Keine Divergenz Bericht ↔ Code: alle Zielwerte des Tickets binden ohne Toleranzverschiebung.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402
from app.services import measure_service  # noqa: E402
from app.services.engine import override_context  # noqa: E402
from app.services.engine.impact import health as H  # noqa: E402

CODE = "EXPECTED_ANNUAL_ALLERGY_DAYS"
DELTA_R = 1.01493       # Ebene 6 des Berichts (wie test_methodik_96_s158_golden.py)
LAM = 0.70               # Kap. 7 pollen.lambda_veg


def setup_function(_fn=None) -> None:
    override_context.set_overrides({})


def teardown_function(_fn=None) -> None:
    override_context.set_overrides({})


def _c_tag() -> float:
    return catalog.risk_default_cost_per_outcome(catalog.RISKS_BY_CODE[CODE])


def _tage(betroffene: float, g_zelle: float, g_bar0: float, lam: float = LAM) -> float:
    """Summe beider Pollengruppen aus ``health.pollen_zelltage`` (δ_R kombiniert, delta_g = 0)."""
    tage_b, tage_g = H.pollen_zelltage(betroffene, DELTA_R, 0.0, g_zelle, g_bar0, lam)
    return tage_b + tage_g


# ── Allee-Zelle (§5, Z. 999–1006) ────────────────────────────────────────────

def test_allee_zelle_stadtbaum():
    """100 Betroffene: 172,5 → 158,3 Tage, Senkung 14,2 Tage / ≈88 € je Jahr;
    Band λ 0,3 → 6,1 Tage, λ 1,0 → 20,3 Tage."""
    b_zelle, g_bar0 = 100.0, 0.18125
    k_birke = gruen = 0.3625
    g_vor = 0.464 * k_birke + 0.536 * gruen
    assert abs(g_vor - 0.3625) < 1e-12
    assert abs(g_vor / g_bar0 - 2.0) < 1e-9

    a = 0.078125 / 0.3625
    dk_birke = a * 1.0 * k_birke
    assert abs(dk_birke - 0.078125) < 1e-9
    g_neu = H.stadtbaum_g_neu(g_vor, k_birke, 0.0, gruen, dk_birke, 0.0, s_unbek=0.12)
    assert abs(g_neu / g_bar0 - 1.8) < 1e-6

    tage_vor = _tage(b_zelle, g_vor, g_bar0)
    tage_nach = _tage(b_zelle, g_neu, g_bar0)
    assert abs(tage_vor - 172.5) < 0.05, f"{tage_vor:.3f}"
    assert abs(tage_nach - 158.3) < 0.05, f"{tage_nach:.3f}"

    senkung = tage_vor - tage_nach
    assert abs(senkung - 14.2) < 0.05, f"{senkung:.3f}"
    assert abs(senkung * _c_tag() - 88) < 0.5, f"{senkung * _c_tag():.2f} €"

    # Zweig 'stadtbaum' in measure_service: derselbe Faktor über die Zellfunktion.
    cell_risk = {
        "betroffene": b_zelle, "delta_birke": DELTA_R, "delta_graeser": 0.0,
        "pollen_g": g_vor, "pollen_g_bar0": g_bar0,
        "canopy_birch_frac": k_birke, "canopy_unknown_frac": 0.0, "green_frac": gruen,
    }
    factor = measure_service._stadtbaum_cell_factor({"anteil_ersetzt": a}, 1.0, cell_risk)
    assert abs(tage_vor * factor - tage_nach) < 1e-9

    # Band über λ (§5, Z. 1005–1006).
    tage_vor_03 = _tage(b_zelle, g_vor, g_bar0, lam=0.3)
    tage_nach_03 = _tage(b_zelle, g_neu, g_bar0, lam=0.3)
    assert abs((tage_vor_03 - tage_nach_03) - 6.1) < 0.05

    tage_vor_10 = _tage(b_zelle, g_vor, g_bar0, lam=1.0)
    tage_nach_10 = _tage(b_zelle, g_neu, g_bar0, lam=1.0)
    assert abs((tage_vor_10 - tage_nach_10) - 20.3) < 0.05


# ── Kommune (§5, Z. 1016–1035) ────────────────────────────────────────────────

def _kommune_zellen() -> list[dict]:
    """Vier Zellen wie im Prüfblock ``beispiel_96_stadtbaum_kommunensumme`` (Z. 1058–1100)."""
    B = [1_000.0, 4_000.0, 2_500.0, 500.0]
    G = [0.00, 0.10, 0.30, 0.60]
    krone = [0.00, 0.00, 0.30, 0.60]
    gruen = [0.00, 0.00, 0.30, 0.60]
    g_bar0 = 0.18125
    zellen = []
    for b, g, k, gr in zip(B, G, krone, gruen):
        zellen.append({
            "betroffene": b, "delta_birke": DELTA_R, "delta_graeser": 0.0,
            "pollen_g": g, "pollen_g_bar0": g_bar0,
            "canopy_birch_frac": k, "canopy_unknown_frac": 0.0, "green_frac": gr,
        })
    return zellen


def test_kommune_stadtbaum_kommunensumme():
    """Σ B·P̂′ = 7.372,8; 8.119,4 → 7.482,9 Tage; Senkung 636,6 Tage (Anteil 0,078);
    ≈3.950 € je Jahr; Zellen 1 und 2 unverändert."""
    zellen = _kommune_zellen()
    a = 1.0 / 3.0

    g_bar0 = zellen[0]["pollen_g_bar0"]
    assert all(abs(z["pollen_g_bar0"] - 0.18125) < 1e-12 for z in zellen)

    tage_vor_je_zelle = [_tage(z["betroffene"], z["pollen_g"], z["pollen_g_bar0"]) for z in zellen]
    tage_vor = sum(tage_vor_je_zelle)
    assert abs(tage_vor - 8_119.4) < 0.5, f"{tage_vor:.2f}"

    # frac: Zellen 1/2 ohne Deckung (unverändert), Zellen 3/4 vollständig gedeckt.
    fracs = [0.0, 0.0, 1.0, 1.0]
    factors = [
        measure_service._stadtbaum_cell_factor({"anteil_ersetzt": a}, frac, z)
        for frac, z in zip(fracs, zellen)
    ]
    assert factors[0] == 1.0 and factors[1] == 1.0

    tage_nach_je_zelle = [t * f for t, f in zip(tage_vor_je_zelle, factors)]
    assert abs(tage_nach_je_zelle[0] - tage_vor_je_zelle[0]) < 1e-9
    assert abs(tage_nach_je_zelle[1] - tage_vor_je_zelle[1]) < 1e-9

    tage_nach = sum(tage_nach_je_zelle)
    assert abs(tage_nach - 7_482.9) < 0.1, f"{tage_nach:.2f}"

    # Kontrolle über Σ B·P̂′ direkt (Ĝ′ je Zelle über health.stadtbaum_g_neu).
    g_neu_je_zelle = []
    for z in zellen:
        dk_birke = a * (1.0 if z["canopy_birch_frac"] > 0 else 0.0) * z["canopy_birch_frac"]
        g_neu = H.stadtbaum_g_neu(
            z["pollen_g"], z["canopy_birch_frac"], z["canopy_unknown_frac"], z["green_frac"],
            dk_birke, 0.0, s_unbek=0.12)
        g_neu_je_zelle.append(g_neu)
    assert abs(g_neu_je_zelle[2] - 0.2536) < 1e-12
    assert abs(g_neu_je_zelle[3] - 0.5072) < 1e-12
    p_hat_nach = [1.0 + LAM * (g / g_bar0 - 1.0) for g in g_neu_je_zelle]
    summe_b_phat_nach = sum(z["betroffene"] * p for z, p in zip(zellen, p_hat_nach))
    assert abs(summe_b_phat_nach - 7_372.8) < 0.01, f"{summe_b_phat_nach:.2f}"

    senkung = tage_vor - tage_nach
    assert abs(senkung - 636.6) < 0.1, f"{senkung:.2f}"
    assert abs(senkung / tage_vor - 0.078) < 0.001

    euro = senkung * _c_tag()
    assert abs(euro - 3_950) < 5, f"{euro:.2f} €"


if __name__ == "__main__":
    import pytest

    sys.exit(pytest.main([__file__, "-q"]))
