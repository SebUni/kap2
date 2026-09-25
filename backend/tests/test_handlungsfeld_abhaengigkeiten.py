"""Tests für die Abhängigkeiten der gerechneten Klimawirkungen über Handlungsfelder (A4)."""

from pathlib import Path

import pytest

from app.data import catalog
from app.data import kwra_querverbindungen as kq
from app.services.handlungsfeld_abhaengigkeiten import abhaengigkeiten_der_kommune

MODUL = (Path(__file__).resolve().parents[1] / "app" / "services"
         / "handlungsfeld_abhaengigkeiten.py")


def test_je_kwra_id_genau_ein_eintrag_aus_risks():
    ergebnis = abhaengigkeiten_der_kommune()
    ids = [e["kwra_id"] for e in ergebnis]
    assert len(ids) == len(set(ids))
    assert set(ids) == {r["kwra_id"] for r in catalog.RISKS}


def test_beziehungen_passen_zu_benannte_beziehungen():
    for eintrag in abhaengigkeiten_der_kommune():
        kid = eintrag["kwra_id"]
        for b in eintrag["beziehungen"]:
            quelle = kq.BENANNTE_BEZIEHUNGEN[b["beziehung_nr"]]
            paar = {quelle["quelle_kwra_id"], quelle["ziel_kwra_id"]}
            assert kid in paar
            if quelle["quelle_kwra_id"] == kid:
                assert b["partner_kwra_id"] == quelle["ziel_kwra_id"]
                assert b["partner_name"] == quelle["ziel"]
            else:
                assert quelle["ziel_kwra_id"] == kid
                assert b["partner_kwra_id"] == quelle["quelle_kwra_id"]
                assert b["partner_name"] == quelle["quelle"]
            for feld in ("beziehung_nr", "partner_kwra_id", "partner_name",
                         "partner_handlungsfeld", "partner_gerechnet",
                         "anderes_handlungsfeld"):
                assert feld in b
            # „gegenseitig“ gilt in beide Richtungen
            if quelle["richtung"] == "gegenseitig":
                assert b["wirkt_auf_partner"] and b["partner_wirkt_ein"]


def test_zahl_der_beziehungen_je_kwra_id():
    for eintrag in abhaengigkeiten_der_kommune():
        kid = eintrag["kwra_id"]
        erwartet = sum(
            1 for b in kq.BENANNTE_BEZIEHUNGEN
            if b.get("quelle_kwra_id") == kid or b.get("ziel_kwra_id") == kid
        )
        assert len(eintrag["beziehungen"]) == erwartet


def test_andere_handlungsfelder_aus_beziehungen():
    for eintrag in abhaengigkeiten_der_kommune():
        erwartet = sorted({
            b["partner_handlungsfeld"] for b in eintrag["beziehungen"]
            if b["partner_handlungsfeld"] is not None
            and b["partner_handlungsfeld"] != eintrag["handlungsfeld"]
        })
        assert eintrag["andere_handlungsfelder"] == erwartet
        assert eintrag["handlungsfeld"] not in eintrag["andere_handlungsfelder"]


def test_keine_gewichtung():
    for eintrag in abhaengigkeiten_der_kommune():
        for b in eintrag["beziehungen"]:
            assert not {"gewicht", "gewichtung", "staerke", "stärke"} & set(b)


def test_teilmenge_der_codes_und_partner_gerechnet():
    ergebnis = abhaengigkeiten_der_kommune(["EXPECTED_ANNUAL_ALLERGY_DAYS"])
    assert [e["kwra_id"] for e in ergebnis] == [96]
    for b in ergebnis[0]["beziehungen"]:
        assert b["partner_gerechnet"] is False


def test_unbekannter_code():
    with pytest.raises(ValueError):
        abhaengigkeiten_der_kommune(["GIBT_ES_NICHT"])


def test_keine_eigene_beziehungsliste():
    text = MODUL.read_text(encoding="utf-8")
    assert text.count('quelle_kwra_id":') == 0
