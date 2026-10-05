"""Eingabe „Änderung des Kronenanteils“ im Maßnahmenformular mit ihrer Herkunft
nach P1 (T-1603-cto).

Vorhaben T-1483-cto Teilpaket #5. Es gibt kein neues Registry-Feld für die
Eingabe ``config['anteil_ersetzt']`` — ``test_measure_pricing.py`` bindet
9 Registry-Felder je Maßnahme (Muster wie s_gek/S157, MeasureSidebar.tsx). Der
Eingabetext liegt deshalb im neuen Katalogfeld ``config_input_help`` (nicht in
``source_details``, dessen Keys ``test_source_maps_keys_are_valid_field_names``
auf die numerischen Katalogfelder bindet — ``anteil_ersetzt`` ist keins davon).

Geprüft wird (Abnahmekriterium T-1603-cto):
(a) Die Katalogmaßnahme LOW_ALLERGEN_TREE_SELECTION trägt einen nutzersichtbaren
    Eingabetext für ``anteil_ersetzt`` mit den Phrasen „Änderung des
    Kronenanteils“, „OSM-Tags der gewählten Zellen“ und „Eingabe der Kommune“,
    und er sagt, dass Gattungen aus einem Baumkataster über den Ausgangsstand
    eingehen, nicht über die Maßnahme.
(b) Der API-Katalog (``GET /catalog``, ``app.data.catalog.MEASURES`` unverändert
    durchgereicht) liefert diesen Text aus.
(c) Werte außerhalb 0 < a ≤ 1 werden abgewiesen (``schemas.MeasureCreate`` /
    ``MeasureUpdate``, Feld ``config``).

DB-frei: prüft den Katalogeintrag und die reinen Pydantic-Schemas, keine
Session/kein Endpoint-Aufruf nötig.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from pydantic import ValidationError

from app.data import catalog  # noqa: E402
from app.schemas.schemas import MeasureCreate, MeasureUpdate  # noqa: E402

CODE = "LOW_ALLERGEN_TREE_SELECTION"


def _mdef() -> dict:
    return catalog.MEASURES_BY_CODE[CODE]


# ── (a) Eingabetext am Katalogeintrag ────────────────────────────────────────

def test_katalogeintrag_traegt_eingabetext_fuer_anteil_ersetzt():
    m = _mdef()
    help_map = m.get("config_input_help") or {}
    text = help_map.get("anteil_ersetzt")
    assert text, "LOW_ALLERGEN_TREE_SELECTION ohne config_input_help['anteil_ersetzt']"
    assert "Änderung des Kronenanteils" in text
    assert "OSM-Tags der gewählten Zellen" in text
    assert "Eingabe der Kommune" in text
    assert "Ausgangsstand" in text and "nicht über diese Maßnahme" in text


def test_eingabetext_kein_registry_feld():
    """Die Maßnahme bekommt keinen zusätzlichen Registry-Wert für anteil_ersetzt —
    nur den Hilfetext; die 9 Registry-Felder aus test_measure_pricing bleiben
    unberührt (kein neues Kosten-/Wirkungsfeld)."""
    m = _mdef()
    assert m.get("default_reduction") is None
    assert "anteil_ersetzt" not in m


# ── (b) API-Katalog liefert den Text aus ─────────────────────────────────────

def test_api_katalog_liefert_eingabetext():
    """GET /catalog liefert catalog.MEASURES unverändert (app/api/routes/catalog.py,
    Schlüssel 'measures') — der Katalogeintrag selbst ist also die API-Antwort."""
    treffer = [m for m in catalog.MEASURES if m["code"] == CODE]
    assert len(treffer) == 1
    text = treffer[0]["config_input_help"]["anteil_ersetzt"]
    assert "Änderung des Kronenanteils" in text


# ── (c) Wertebereich 0 < a ≤ 1 ────────────────────────────────────────────────

@pytest.mark.parametrize("wert", [0.0, -0.1, 1.5, 2.0])
def test_anteil_ersetzt_ausserhalb_bereich_wird_abgewiesen_bei_create(wert):
    with pytest.raises(ValidationError):
        MeasureCreate(
            name="Stadtbaumwahl", measure_type=CODE,
            geometry_geojson={"type": "Polygon", "coordinates": [[[0, 0], [0, 1], [1, 1], [0, 0]]]},
            config={"anteil_ersetzt": wert},
        )


@pytest.mark.parametrize("wert", [0.0, -0.1, 1.5, 2.0])
def test_anteil_ersetzt_ausserhalb_bereich_wird_abgewiesen_bei_update(wert):
    with pytest.raises(ValidationError):
        MeasureUpdate(config={"anteil_ersetzt": wert})


@pytest.mark.parametrize("wert", [0.0001, 1.0 / 3.0, 1.0])
def test_anteil_ersetzt_innerhalb_bereich_wird_angenommen(wert):
    m = MeasureUpdate(config={"anteil_ersetzt": wert})
    assert m.config["anteil_ersetzt"] == wert
    c = MeasureCreate(
        name="Stadtbaumwahl", measure_type=CODE,
        geometry_geojson={"type": "Polygon", "coordinates": [[[0, 0], [0, 1], [1, 1], [0, 0]]]},
        config={"anteil_ersetzt": wert},
    )
    assert c.config["anteil_ersetzt"] == wert


def test_anteil_ersetzt_ohne_eingabe_bleibt_zulaessig():
    """Ohne die Angabe (None/fehlend) entsteht keine Validierung — Faktor bleibt
    1,0 (measure_service._stadtbaum_cell_factor, unverändert von diesem Ticket)."""
    MeasureUpdate(config={})
    MeasureUpdate(config=None)
    MeasureUpdate(config={"anteil_ersetzt": None})


def test_anteil_ersetzt_ueber_eins_im_rechenweg_abgewiesen_oder_sichtbar_gekappt():
    """Ü-9 (Befund 251), Rechenweg: a > 1 ergibt keinen Betrag, sondern den Vermerk und
    ``benefit_missing_input`` = 'anteil_ersetzt'. Allee-Zelle nach Ü-13 (B 100, δ_B 0,43659,
    δ_G 0,57834, Ḡ₀ 0,18125, Ĝ 0,3625, Kronen 0,3625 mit Tag, Grün 0,3625): a = 1 ergibt
    65,93 Tage bei Deckungsgrad 1 und 32,96 Tage bei Deckungsgrad 0,5 (vorher, mit
    δ 1,8795, 122,09 und 61,05)."""
    from app.services import measure_service as ms

    cell = {
        "betroffene": 100.0, "delta_birke": 0.43659, "delta_graeser": 0.57834,
        "pollen_g": 0.3625, "pollen_g_bar0": 0.18125,
        "canopy_birch_frac": 0.3625, "canopy_unknown_frac": 0.0, "green_frac": 0.3625,
    }

    # a = 1: unverändert eine Zahl.
    _, tage_voll, grund = ms._stadtbaum_cell_effect({"anteil_ersetzt": 1.0}, 1.0, cell)
    assert grund is None
    assert tage_voll == pytest.approx(65.93, abs=0.01)
    _, tage_halb, grund = ms._stadtbaum_cell_effect({"anteil_ersetzt": 1.0}, 0.5, cell)
    assert grund is None
    assert tage_halb == pytest.approx(32.96, abs=0.01)

    # a > 1: kein Betrag, Grund 'anteil_ersetzt_bereich' (bei jedem Deckungsgrad).
    for a in (1.5, 2.0, 4.0):
        for frac in (1.0, 0.5):
            faktor, tage, grund = ms._stadtbaum_cell_effect({"anteil_ersetzt": a}, frac, cell)
            assert tage is None, (a, frac)
            assert faktor == 1.0
            assert grund == ms.STADTBAUM_ANTEIL_BEREICH_REASON

    # Der Vermerk der Kommune: kein Betrag, benefit_missing_input wie bei fehlender Eingabe.
    felder = ms._stadtbaum_summary_fields(
        _mdef(), 0.0, 0.0, ms.STADTBAUM_ANTEIL_BEREICH_REASON)
    assert felder["benefit_missing_input"] == "anteil_ersetzt"
    assert felder["benefit_display"] == (
        "kein Betrag: Anteil ersetzter Kronen (anteil_ersetzt) muss zwischen 0 und 1 liegen, "
        "Eingabe in der Maßnahme berichtigen")
    assert "stadtbaum_avoided_days_total" not in felder
    assert "stadtbaum_avoided_days_eur" not in felder


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
