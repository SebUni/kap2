"""Umsetzungsebene je Maßnahme (app/data/massnahmen_umsetzung.py, T-1132-cto, A9 der Gegenprobe Zeile 19)."""

from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402
from app.data.massnahmen_umsetzung import MASSNAHMEN_UMSETZUNG  # noqa: E402

CODES = sorted(MASSNAHMEN_UMSETZUNG)


def test_genau_ein_eintrag_je_katalogcode():
    katalog_codes = [m["code"] for m in catalog.MEASURES]
    assert len(katalog_codes) == len(set(katalog_codes))
    assert set(MASSNAHMEN_UMSETZUNG) == {m["code"] for m in catalog.MEASURES}


@pytest.mark.parametrize("code", CODES)
def test_schluessel(code):
    eintrag = MASSNAHMEN_UMSETZUNG[code]
    assert {"umsetzung", "partner", "beleg"} <= set(eintrag)


@pytest.mark.parametrize("code", CODES)
def test_umsetzung_und_partner(code):
    eintrag = MASSNAHMEN_UMSETZUNG[code]
    assert eintrag["umsetzung"] in ("kommune_allein", "mit_partnern")
    partner = eintrag["partner"]
    assert isinstance(partner, list)
    assert all(isinstance(p, str) and p.strip() for p in partner)
    assert bool(partner) == (eintrag["umsetzung"] == "mit_partnern")


@pytest.mark.parametrize("code", CODES)
def test_beleg_quelle_mit_seite_oder_abschaetzung(code):
    beleg = MASSNAHMEN_UMSETZUNG[code]["beleg"]
    assert isinstance(beleg, dict)
    hat_quelle = bool(str(beleg.get("quelle", "")).strip()) and bool(str(beleg.get("seite", "")).strip())
    hat_abschaetzung = bool(beleg.get("abschaetzung"))
    assert hat_quelle or hat_abschaetzung
    if hat_abschaetzung:
        herleitung = str(beleg.get("herleitung", "")).strip()
        # mindestens ein Satz: Text mit Satzschlusszeichen
        assert len(herleitung.split()) >= 3
        assert herleitung[-1] in ".!?"
