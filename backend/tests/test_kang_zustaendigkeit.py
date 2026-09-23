"""Deckung von app/data/kang_zustaendigkeit.py mit docs/KANG_ZUSTAENDIGKEIT_LAENDER.md (T-0751)."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))

from app.data.kang_zustaendigkeit import ZUSTAENDIGKEIT, zustaendigkeit_fuer  # noqa: E402
from app.services.osm_service import BUNDESLAENDER  # noqa: E402
from test_kang_zustaendigkeit_doku import _datenzeilen  # noqa: E402

SCHLUESSEL = {"bundesland", "rechtsgrundlage", "fundstelle", "zustaendige_stelle", "pflicht", "stand"}


def test_schluessel_gleich_bundeslaender():
    assert set(ZUSTAENDIGKEIT) == set(BUNDESLAENDER)


def test_werte_gleich_dokument():
    zeilen = {z[0]: z for z in _datenzeilen()}
    for land, eintrag in ZUSTAENDIGKEIT.items():
        _, rg, fs, stelle, pflicht, stand = zeilen[land]
        assert eintrag["rechtsgrundlage"] == rg, land
        assert eintrag["fundstelle"] == fs, land
        assert eintrag["zustaendige_stelle"] == stelle, land
        assert eintrag["pflicht"] == pflicht, land
        assert eintrag["stand"] == stand, land


def test_zustaendigkeit_fuer_bekannt():
    r = zustaendigkeit_fuer("Niedersachsen")
    assert set(r) == SCHLUESSEL
    assert r["bundesland"] == "Niedersachsen" and r["pflicht"] == "ja"


def test_zustaendigkeit_fuer_unbekannt():
    for wert in (None, "Atlantis"):
        r = zustaendigkeit_fuer(wert)
        assert set(r) == SCHLUESSEL
        assert r["pflicht"] == "unbekannt"
