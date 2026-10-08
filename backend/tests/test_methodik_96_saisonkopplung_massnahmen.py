"""#96 Saisonkopplung c_Tag im Maßnahmen-Nutzen von S158 und Stadtbaum (T-1916-ceo, Bericht #96 §3.5).

Überschreibt eine Kommune f, p_B, p_G oder eine Saisonlänge, rechnet die Zelle
``cost_eur · POLLEN_D_SAISON_REF / d_Saison`` (T-1894-ceo). Die je Zelle gespeicherten Einsparungen
``s158_avoided_eur`` und ``stadtbaum_avoided_eur`` monetarisieren die vermiedenen Tage über
``risk_engine.cost_from_cell_entry`` und tragen damit denselben Faktor wie Zelle und Aggregat.
Maßstab ist der Wirkungsanteil (vermiedene Tage / Zell-Outcome) auf den Zellbetrag ``cost_eur``.
Berliner Golden-Zelle, ohne Datenbank. Sichtbar mit ``-s``.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest  # noqa: E402

import test_massnahme_s158_ausgabe as s158_ausgabe  # noqa: E402
import test_massnahme_stadtbaum_ausgabe as stadtbaum_ausgabe  # noqa: E402
from app.services import parameter_registry  # noqa: E402
from app.services.engine import impact, override_context  # noqa: E402
from app.services.engine.impact.base import CellContext  # noqa: E402
from test_methodik_96_golden_betraege import BERLIN, CODE, _zellbaender  # noqa: E402

P = f"risks.{CODE}.impact."
G_BAR0 = 0.18125            # Ĝ = Ḡ₀ ⇒ P̂ = 1: die Zelle ist die Golden-Zelle (2.474.857,71 €)
CANOPY_BIRKE = 0.078125     # Kronen für die Stadtbaumwahl (wie die Allee-Zelle)
GRUEN = 0.3


def _ctx() -> CellContext:
    b = {k: float(v) for k, v in _zellbaender(BERLIN).items()}
    b["u65"] = b["u20"] + b["a20_64"]
    return CellContext(
        ci={"pop": sum(b[k] for k in ("u20", "a20_64", "a65_74", "a75_84", "a85p")),
            "pop_age_bands": b, "canopy_birch_frac": CANOPY_BIRKE,
            "canopy_unknown_frac": 0.0, "green_frac": GRUEN},
        hev={"hazards": {"POLLEN_LOAD": G_BAR0}, "exposures": {}, "vulnerabilities": {}},
        hev_norm={"hazards": {}, "exposures": {}, "vulnerabilities": {}},
        indices={}, regional={"bundesland": "Berlin", "pollen_g_bar": G_BAR0})


def _messen(overrides: dict, monkeypatch) -> dict:
    """Zelle (cost_eur, outcome) und die gespeicherten Einsparungen beider Maßnahmen."""
    override_context.set_overrides(overrides)
    try:
        z = impact.compute_all_cell_impacts(_ctx())[CODE]
    finally:
        override_context.set_overrides({})
    cell = {"index": z["outcome"], "outcome": z["outcome"]}
    for k in ("betroffene", "delta_birke", "delta_graeser", "pollen_g", "pollen_g_bar0",
              "canopy_birch_frac", "canopy_unknown_frac", "green_frac"):
        cell[k] = z[k]
    monkeypatch.setattr(parameter_registry, "overrides_map", lambda *_a, **_k: dict(overrides))
    erg = {"zelle": z}
    for key, lauf in (
            ("s158", lambda: s158_ausgabe._run({1: cell}, {1: 1.0}, monkeypatch)),
            ("stadtbaum", lambda: stadtbaum_ausgabe._run_cells(
                {1: cell}, {"anteil_ersetzt": 1.0}, monkeypatch))):
        override_context.set_overrides(overrides)
        try:
            _, added = lauf()
        finally:
            override_context.set_overrides({})
        erg[key] = added[0].savings
    return erg


@pytest.mark.parametrize("name,ov", [
    ("Vorgabe", {}),
    ("f=0,5", {P + "f_symptomtage": 0.5}),
    ("p_B=0,3", {P + "p_sens_birke": 0.3}),
    ("p_G=0,4", {P + "p_sens_graeser": 0.4}),
    ("L_B=40", {P + "l_saison_birke": 40.0}),
    ("L_G=45", {P + "l_saison_graeser": 45.0}),
])
@pytest.mark.parametrize("massnahme", ["s158", "stadtbaum"])
def test_nutzen_gleich_zellbasis(name, ov, massnahme, monkeypatch):
    erg = _messen(ov, monkeypatch)
    z, sav = erg["zelle"], erg[massnahme]
    tage, eur = sav[f"{massnahme}_avoided_days"], sav[f"{massnahme}_avoided_eur"]
    zellbasis = z["cost_eur"] * tage / z["outcome"]
    print(f"{name} {massnahme}: avoided_eur = {eur:.2f} €, Zellbasis = {zellbasis:.2f} €")
    assert abs(eur - zellbasis) <= 1.0, f"{name} {massnahme}: {eur:.2f} ≠ {zellbasis:.2f}"


def test_vorgabe_unveraendert(monkeypatch):
    erg = _messen({}, monkeypatch)
    assert abs(erg["zelle"]["cost_eur"] - 2_474_857.71) <= 1.0
    assert abs(erg["s158"]["s158_avoided_eur"] - 55_684.30) <= 0.01
    assert abs(erg["stadtbaum"]["stadtbaum_avoided_eur"] - 195_462.56) <= 0.01
