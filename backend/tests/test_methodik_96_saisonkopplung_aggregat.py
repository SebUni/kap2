"""#96 Saisonkopplung c_Tag im Aggregat (T-1894-ceo, Bericht #96 §3.5, health.py Z. 769–771).

Überschreibt eine Kommune f, p_B, p_G oder eine Saisonlänge, rechnet die Zelle
``cost_eur · POLLEN_D_SAISON_REF / d_Saison``. Das Aggregat monetarisiert den gespeicherten
Outcome über ``risk_engine.cost_from_cell_entry`` und muss denselben Faktor tragen.
Berliner Golden-Zelle, ohne Datenbank. Sichtbar mit ``-s``.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest  # noqa: E402

from app.services.engine import impact, override_context, risk_engine  # noqa: E402
from test_methodik_96_endpunkt_berlin import _aggregat_zellen  # noqa: E402
from test_methodik_96_golden_betraege import BERLIN, CODE, _ctx, _zellbaender  # noqa: E402

P = f"risks.{CODE}.impact."


def _messen(overrides: dict) -> tuple[float, float]:
    """(Zelle cost_eur, Aggregat-Zeile kwra_id 96) mit denselben Überschreibungen."""
    override_context.set_overrides(overrides)
    try:
        zelle = impact.compute_all_cell_impacts(_ctx(_zellbaender(BERLIN)))[CODE]
        zellen, pop = _aggregat_zellen(BERLIN)       # setzt die Overrides zurück
        zellen[0]["risks"][CODE]["outcome"] = zelle["outcome"]
        override_context.set_overrides(overrides)
        by = risk_engine.aggregate(zellen, pop, 891.0)["cost"]["by_risk"]
    finally:
        override_context.set_overrides({})
    zeilen = [e for e in by if e.get("kwra_id") == 96]
    assert len(zeilen) == 1
    return zelle["cost_eur"], zeilen[0]["cost_eur"]


@pytest.mark.parametrize("name,ov", [
    ("Vorgabe", {}),
    ("f=0,5", {P + "f_symptomtage": 0.5}),
    ("p_B=0,3", {P + "p_sens_birke": 0.3}),
    ("p_G=0,4", {P + "p_sens_graeser": 0.4}),
    ("L_B=40", {P + "l_saison_birke": 40.0}),
    ("L_G=45", {P + "l_saison_graeser": 45.0}),
])
def test_zelle_gleich_aggregat(name, ov):
    zelle, aggregat = _messen(ov)
    print(f"{name}: Zelle cost_eur = {zelle:.2f} €, Aggregat kwra_id 96 = {aggregat:.2f} €")
    assert abs(zelle - aggregat) <= 1.0, f"{name}: Zelle {zelle:.2f} ≠ Aggregat {aggregat:.2f}"


def test_vorgabe_unveraendert():
    zelle, aggregat = _messen({})
    assert abs(zelle - 2_474_857.71) <= 1.0
    assert abs(aggregat - 2_474_857.71) <= 1.0
