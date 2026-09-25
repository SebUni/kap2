"""Tests für das Datenmodul CatRaRe (T-1165)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from shapely.geometry import Point, box  # noqa: E402

from app.data import catrare as c  # noqa: E402

DEUTSCHLAND = box(5.5, 47.0, 15.5, 55.5)


def test_ganz_deutschland_liefert_katalog():
    alle = c.ereignisse_in_flaeche(DEUTSCHLAND)
    assert len(alle) > 1000
    assert all({"id", "beginn", "lon", "lat"} <= set(e) for e in alle)
    assert min(e["beginn"] for e in alle)[:4] >= "2001"
    assert len({e["id"] for e in alle}) == len(alle)


def test_flaeche_ohne_ereignisse_ist_leer():
    assert c.ereignisse_in_flaeche(box(-10, -10, -9, -9)) == []


def test_leere_flaeche_ist_leer():
    assert c.ereignisse_in_flaeche(Point().buffer(0)) == []


def test_teilflaeche_ist_teilmenge():
    alle = c.ereignisse_in_flaeche(DEUTSCHLAND)
    sued = c.ereignisse_in_flaeche(box(5.5, 47.0, 15.5, 49.0))
    assert 0 < len(sued) < len(alle)
    assert all(47.0 <= e["lat"] <= 49.0 for e in sued)


def test_erstes_ereignis_hoechenschwand():
    e = c.ereignisse_in_flaeche(box(8.0, 47.5, 8.5, 48.0))[0]
    assert e["id"] == "T5_Eta_000001"
    assert e["beginn"].startswith("2001-01-01")
    assert abs(e["lon"] - 8.2056) < 1e-3 and abs(e["lat"] - 47.7101) < 1e-3


def test_rueckgabe_ist_kopie():
    e = c.ereignisse_in_flaeche(box(8.0, 47.5, 8.5, 48.0))[0]
    e["id"] = "x"
    assert c.ereignisse_in_flaeche(box(8.0, 47.5, 8.5, 48.0))[0]["id"] != "x"


def test_texte_gesetzt():
    assert "opendata.dwd.de" in c.QUELLE and "CC BY 4.0" in c.QUELLE
    assert "Schäden" in c.MODELLGRENZE and "2001" in c.MODELLGRENZE
