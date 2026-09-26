"""Hebel S157 — gekühlte Heimplätze (Bericht #95 §5, Beispiel-Block ``s157_berlin``).

Maßnahme ``COOLING_ROOMS_DRINKING_WATER`` ist aktiviert (T-1367) und wirkt mit
``ΔD_S157 = D_85+ · h_Heim · s_gek · (1 − g_S157)`` auf die Todesfälle 85+ der
Heimbewohner, bewertet mit L̄_85+ (YLL) × VOLY. s_gek ist die Eingabe der Kommune;
ohne Eingabe entsteht kein Betrag (auch keine 0).

DB-frei: prüft die Rechenfunktion in ``health`` und den Zellfaktor der Maßnahmen-Engine
an einer Zelle mit den Berlin-Werten aus Kette 3.0 (D_85+ = 153,6; L̄_85+ = 4,16).
"""

from __future__ import annotations

import pytest

from app.data import catalog, catalog_parked
from app.services import measure_service, parameter_registry
from app.services.engine import risk_engine
from app.services.engine.impact import health

CODE = "COOLING_ROOMS_DRINKING_WATER"
MORT = "EXPECTED_ANNUAL_MORTALITY"
D85_BERLIN = 153.6       # Bericht #95 Kette 3.0, Ebene 6
L85 = 4.16               # Ebene 7


def _berlin_cell() -> dict:
    """Eine Zelle, die die Berliner Todesfälle 85+ trägt (YLL nur aus 85+ plus Rest)."""
    yll = D85_BERLIN * L85 + 1000.0   # übrige Bänder: beliebiger Sockel, bleibt unberührt
    return {"outcome": yll, "deaths_a85p": D85_BERLIN}


def _benefit_eur(s_gek) -> float | None:
    risk = catalog.RISKS_BY_CODE[MORT]
    mdef = catalog.MEASURES_BY_CODE[CODE]
    cell = _berlin_cell()
    factor = measure_service._measure_cell_factor(
        mdef, {} if s_gek is None else {"s_gek": s_gek}, MORT, 1.0, 1.0, cell)
    fields = measure_service._s157_summary_fields(
        mdef, {} if s_gek is None else {"s_gek": s_gek})
    if fields.get("benefit_display"):
        assert factor == 1.0
        return None
    return risk_engine.cost_from_outcome(risk, cell["outcome"]) * (1.0 - factor)


def test_measure_is_active_not_parked():
    assert CODE in catalog.MEASURES_BY_CODE
    assert CODE not in {m["code"] for m in catalog_parked._PARKED_MEASURES}
    m = catalog.MEASURES_BY_CODE[CODE]
    assert m["effect_model"] == "s157"
    assert m["linked_risk_codes"] == [MORT]
    assert m["default_reduction"] is None   # keine 0.18 auf die Exposition mehr


def test_h_heim_and_g_from_report():
    assert health.h_heim() == pytest.approx(0.344, abs=0.001)
    assert D85_BERLIN * health.h_heim() == pytest.approx(52.9, abs=0.05)
    assert health.s157_avoided_deaths(D85_BERLIN, 1.0) == pytest.approx(37.4, abs=0.05)


def test_berlin_all_care_home_places_cooled_is_25_0_mio_eur():
    eur = _benefit_eur(1.0)
    assert round(eur / 1e6, 1) == 25.0
    assert eur / 1e6 == pytest.approx(25.0, abs=0.05)


def test_berlin_ten_percent_is_one_tenth():
    assert _benefit_eur(0.1) == pytest.approx(_benefit_eur(1.0) / 10.0, rel=1e-9)


def test_without_input_no_amount():
    assert health.s157_avoided_deaths(D85_BERLIN, None) is None
    assert _benefit_eur(None) is None
    fields = measure_service._s157_summary_fields(catalog.MEASURES_BY_CODE[CODE], {})
    assert fields["s_gek"] is None
    assert fields["benefit_display"] == measure_service.S157_NO_INPUT_TEXT
    assert fields["benefit_missing_input"] == "s_gek"


def test_only_mortality_and_old_cells_unchanged():
    mdef = catalog.MEASURES_BY_CODE[CODE]
    cfg = {"s_gek": 1.0}
    assert measure_service._measure_cell_factor(
        mdef, cfg, "EXPECTED_ANNUAL_MORBIDITY", 1.0, 1.0, {"outcome": 10.0}) == 1.0
    # Zelle vor der Neuberechnung (ohne Teil-Ausweis D_85+): keine Wirkung
    assert measure_service._measure_cell_factor(
        mdef, cfg, MORT, 1.0, 1.0, {"outcome": 10.0}) == 1.0


def test_parameters_visible_in_registry():
    params = {p["id"]: p for p in parameter_registry.catalog_parameters(
        layer_code=MORT, layer_category="risks")}
    g = next(p for pid, p in params.items() if pid.endswith(".g_s157"))
    ror = next(p for pid, p in params.items() if pid.endswith(".ror_s157"))
    # Blockwert 0,29 gerundet; gerechnet wird ungerundet wie im Beispiel s157_berlin
    assert round(g["value"], 2) == 0.29 and g["evidence_class"] == "abgeschaetzt"
    assert g["value"] == pytest.approx(health.G_S157)
    assert ror["value"] == 0.93 and ror["evidence_class"] == "belegt"
