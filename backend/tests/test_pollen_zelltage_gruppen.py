"""Zellfunktion ``health.pollen_zelltage`` und Zusatztage je Pollengruppe (T-1512-cto).

Integrationsauflage S158 Punkt 1 (Bericht #96 §5.1 Z. 1406 f.; Formel Z. 1255
ΔTage_g,Zelle = B·δ_g·P̂, δ_B/δ_G Z. 1200–1206). Architekturentscheidung des CTO
(T-1482-cto): genau eine reine Zellfunktion ``pollen_zelltage`` in
``impact/health.py``; ``allergy_symptom_days`` rechnet über sie und legt die
Tage und die Eingaben in der Zellausgabe ab. Das Maßnahmen-Modul (S158,
Paket 2) ruft dieselbe Funktion später mit festgehaltenem Ḡ₀ auf.

Geprüft wird:
(a) Schlüssel der Zellausgabe und tage_birke + tage_graeser = outcome.
(b) δ_B = 0,43659 und δ_G = 0,57834 (Berlin, Region Mitte, Bericht §5.1 Z. 1200–1206).
(c) ``pollen_zelltage`` mit 402.103 Betroffenen und P̂ = 1 (Ḡ₀ = Ĝ) ergibt
    175.554 und 232.552 Tage (§3.0-Rechenkette, Toleranz ± 1).
(d) Ein erneuter Aufruf von ``pollen_zelltage`` mit den gespeicherten Eingaben
    ergibt dieselben Tage (± 1e-9) — die Funktion ist rein und deterministisch.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services.engine import impact, override_context  # noqa: E402
from app.services.engine.impact import health as H  # noqa: E402
from app.services.engine.impact.base import CellContext  # noqa: E402

CODE = "EXPECTED_ANNUAL_ALLERGY_DAYS"

# Berlin-Rechenkette (Ebenen 1–10, test_methodik_96_golden_betraege.py::KETTE_BETROFFENE).
KETTE_BETROFFENE = 402_103
DELTA_BIRKE = 0.43659
DELTA_GRAESER = 0.57834
TAGE_BIRKE = 175_554
TAGE_GRAESER = 232_552
TOL = 1.0


def _berlin_ctx(g_cell: float = 0.18, g_bar0: float | None = 0.18) -> CellContext:
    """Zelle mit dem Bundes-Altersmix, so skaliert, dass ``betroffene`` = 402.103.

    Region Mitte (Berlin), Standardprävalenzen (Bericht Kap. 7) ergeben δ_R = 1,01493
    Tage/Betroffener und die Prävalenzen POLLEN_PREVALENCE aus dem Produkt. Die
    Bevölkerung wird über die Bundesbänder so skaliert, dass die gewichtete
    Prävalenzsumme exakt KETTE_BETROFFENE ergibt.
    """
    band_pop = {"u20": 15_583_456, "a20_64": 49_163_992, "a65_74": 9_569_640,
                "a75_84": 6_294_744, "a85p": 2_844_213}
    pop_de = sum(band_pop.values())
    gewichtete_praevalenz = sum(
        (n / pop_de) * H.POLLEN_PREVALENCE[b] for b, n in band_pop.items())
    skala = KETTE_BETROFFENE / (pop_de * gewichtete_praevalenz)
    bands = {b: n * skala for b, n in band_pop.items()}
    bands["u65"] = bands["u20"] + bands["a20_64"]
    pop = sum(band_pop.values()) * skala
    regional = {"bundesland": "Berlin"}
    if g_bar0 is not None:
        regional["pollen_g_bar"] = g_bar0
    return CellContext(
        ci={"pop": pop, "pop_age_bands": bands},
        hev={"hazards": {"POLLEN_LOAD": g_cell}, "exposures": {}, "vulnerabilities": {}},
        hev_norm={"hazards": {}, "exposures": {}, "vulnerabilities": {}},
        indices={}, regional=regional)


def test_zellausgabe_schluessel_und_summe():
    """(a) Die Zellausgabe trägt die geforderten Schlüssel; Summe = outcome."""
    override_context.set_overrides({})
    res = impact.compute_all_cell_impacts(_berlin_ctx())[CODE]
    for key in ("tage_birke", "tage_graeser", "delta_birke", "delta_graeser",
               "pollen_g", "pollen_g_bar0"):
        assert key in res, key
    assert abs((res["tage_birke"] + res["tage_graeser"]) / res["outcome"] - 1.0) < 1e-12


def test_delta_je_gruppe_berlin():
    """(b) δ_B = 0,43659 und δ_G = 0,57834 (Region Mitte, §5.1 Z. 1200–1206)."""
    override_context.set_overrides({})
    res = impact.compute_all_cell_impacts(_berlin_ctx())[CODE]
    assert abs(res["delta_birke"] - DELTA_BIRKE) < 1e-9
    assert abs(res["delta_graeser"] - DELTA_GRAESER) < 1e-9


def test_pollen_zelltage_berlin_betroffene():
    """(c) pollen_zelltage(402.103, δ_B, δ_G, ·, ·, ·) mit P̂ = 1 ergibt 175.554/232.552 Tage."""
    tage_birke, tage_graeser = H.pollen_zelltage(
        KETTE_BETROFFENE, DELTA_BIRKE, DELTA_GRAESER,
        g_zelle=0.18, g_bar0=0.18, lam=0.70)
    assert abs(tage_birke - TAGE_BIRKE) < TOL, tage_birke
    assert abs(tage_graeser - TAGE_GRAESER) < TOL, tage_graeser


def test_pollen_zelltage_ist_rein_und_deterministisch():
    """(d) Erneuter Aufruf mit den gespeicherten Eingaben ergibt dieselben Tage."""
    override_context.set_overrides({})
    res = impact.compute_all_cell_impacts(_berlin_ctx())[CODE]
    eingaben = dict(
        betroffene=res["betroffene"], delta_b=res["delta_birke"],
        delta_g=res["delta_graeser"], g_zelle=res["pollen_g"],
        g_bar0=res["pollen_g_bar0"], lam=0.70)
    wieder_birke, wieder_graeser = H.pollen_zelltage(**eingaben)
    assert abs(wieder_birke - res["tage_birke"]) < 1e-9
    assert abs(wieder_graeser - res["tage_graeser"]) < 1e-9


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__, "-v"]))
