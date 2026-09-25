"""T-1135-cto: Gender- und Diversitätsaspekte je Klimawirkung (Checkliste Zeile 19, A7).

Prüft ``app.data.diversitaet_aspekte``:
(a) genau ein Eintrag je Code aus ``catalog.RISKS``, verglichen zur Laufzeit,
(b) jede ``fundstelle`` (``app.modul:attribut``) lässt sich importieren und das
    Attribut existiert,
(c) jedes ``nicht_beruecksichtigt`` trägt eine ganzzahlige ``seite``.
"""

from __future__ import annotations

import importlib
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402
from app.data.diversitaet_aspekte import (  # noqa: E402
    DIVERSITAET_JE_KLIMAWIRKUNG,
    QUELLE,
)


def test_ein_eintrag_je_klimawirkung_des_katalogs():
    assert set(DIVERSITAET_JE_KLIMAWIRKUNG) == {r["code"] for r in catalog.RISKS}


def test_eintraege_haben_beide_listen():
    for code, eintrag in DIVERSITAET_JE_KLIMAWIRKUNG.items():
        assert isinstance(eintrag.get("beruecksichtigt"), list), code
        assert isinstance(eintrag.get("nicht_beruecksichtigt"), list), code
        for b in eintrag["beruecksichtigt"]:
            assert b.get("aspekt") and b.get("wie") and b.get("fundstelle"), (code, b)


def test_fundstellen_lassen_sich_laden():
    for code, eintrag in DIVERSITAET_JE_KLIMAWIRKUNG.items():
        for b in eintrag["beruecksichtigt"]:
            modul, sep, attribut = b["fundstelle"].partition(":")
            assert sep and modul.startswith("app.") and attribut, (code, b["fundstelle"])
            mod = importlib.import_module(modul)
            assert hasattr(mod, attribut), (code, b["fundstelle"])


def test_nicht_beruecksichtigt_hat_ganzzahlige_seite():
    for code, eintrag in DIVERSITAET_JE_KLIMAWIRKUNG.items():
        for n in eintrag["nicht_beruecksichtigt"]:
            assert n.get("aspekt") and n.get("quelle"), (code, n)
            assert isinstance(n.get("seite"), int) and not isinstance(n["seite"], bool), (code, n)


def test_quelle_vollstaendig():
    for feld in ("titel", "url", "abgerufen", "seite"):
        assert QUELLE.get(feld), feld
    assert QUELLE["url"].startswith("https://")
    assert isinstance(QUELLE["seite"], int)
