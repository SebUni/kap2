"""Verzeichnis vorhandener Untersuchungen (T-1166): Aufbau, Schlüssel, Pflichtfelder. Ohne Netzzugriff."""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import vorhandene_untersuchungen as v  # noqa: E402
from app.services.osm_service import BUNDESLAENDER  # noqa: E402

CODES = [
    "hochwassergefahrenkarten", "starkregengefahrenkarten", "klimaanalysekarten", "hitzeinseln",
    "feinstaub", "feuerwehreinsaetze", "catrare", "naturgefahrenreport", "klimareport", "kra_land", "kwra",
]


def test_codes_in_reihenfolge():
    assert [u["code"] for u in v.UNTERSUCHUNGEN] == CODES


def test_pflichtfelder_und_ebene():
    for u in v.UNTERSUCHUNGEN:
        assert u["bezeichnung"].strip() and u["wo_erhaeltlich"].strip()
        assert u["ebene"] in {"kommunal", "land", "bund"}


def test_ueberregionale_mit_url():
    for u in v.UNTERSUCHUNGEN:
        if u["ebene"] == "bund":
            assert re.search(r"https://\S+", u["wo_erhaeltlich"]), u["code"]
        if u["ebene"] == "land":
            assert "LANDESPORTALE" in u["wo_erhaeltlich"], u["code"]


def test_landesportale_schluessel_gleich_bundeslaender():
    assert set(v.LANDESPORTALE) == set(BUNDESLAENDER)
    assert len(v.LANDESPORTALE) == 16


def test_landesportale_nie_leer():
    for land, p in v.LANDESPORTALE.items():
        assert set(p) == {"hochwasser", "kra_land"}, land
        assert all(x.strip() for x in p.values()), land


def test_hochwasser_ist_url_und_kra_url_oder_satz_mit_datum():
    for land, p in v.LANDESPORTALE.items():
        assert p["hochwasser"].startswith("https://"), land
        kra = p["kra_land"]
        assert kra.startswith("https://") or re.search(r"\d{2}\.\d{2}\.\d{4}", kra), land


def test_nachbar_satz():
    assert "benachbarter" in v.NACHBAR_SATZ and "Kreises" in v.NACHBAR_SATZ and "Landes" in v.NACHBAR_SATZ
