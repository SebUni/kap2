"""Tests für die LoD2-Quellmechanismen: Anker-Snapping, Index-, Prepare-Adapter."""

from __future__ import annotations

import json

import pytest

from app.config import settings
from app.services.geodata.lod2 import loader
from app.services.geodata.lod2.loader import (
    _parse_geojson_index, _parse_prepare_page, _tile_urls, _tiles_for_bbox,
)
from app.services.geodata.lod2.sources import LOD2_SOURCES, source_for


@pytest.fixture(autouse=True)
def _iso_cache(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "LOD2_CACHE_DIR", str(tmp_path))
    loader._index_ram.clear()
    yield
    loader._index_ram.clear()


def test_alle_relevanten_laender_phase_1():
    phase1 = {land for land, s in LOD2_SOURCES.items() if s.phase == 1}
    assert phase1 == {
        "Nordrhein-Westfalen", "Bayern", "Brandenburg", "Hamburg",
        "Thüringen", "Rheinland-Pfalz", "Mecklenburg-Vorpommern", "Berlin",
        "Sachsen", "Baden-Württemberg", "Niedersachsen", "Schleswig-Holstein",
        "Sachsen-Anhalt", "Bremen",
    }
    assert source_for("Hessen") is None
    assert source_for("Saarland") is None


def test_bw_anker_snapping_ungerade_ostwerte():
    """BW rastert 2 km auf UNGERADE Ostwerte (verifiziert: 509/511/513)."""
    src = LOD2_SOURCES["Baden-Württemberg"]
    # Stuttgart-Zentrum (~UTM32 513/5403)
    tiles = _tiles_for_bbox("48.77,9.17,48.78,9.19", src)
    assert tiles, "keine Kacheln aufgelöst"
    for e, n in tiles:
        assert e % 2 == 1, f"Ostwert {e} muss ungerade sein"
        assert n % 2 == 0, f"Nordwert {n} muss gerade sein"


def test_gerade_anker_bei_2km_quellen():
    src = LOD2_SOURCES["Thüringen"]
    tiles = _tiles_for_bbox("50.97,11.02,50.99,11.04", src)  # Erfurt
    for e, n in tiles:
        assert e % 2 == 0 and n % 2 == 0


def test_geojson_index_ni_koordinaten_aus_geometrie():
    src = LOD2_SOURCES["Niedersachsen"]
    content = json.dumps({
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {
                "tile_id": "23425822",
                "CityGML": "https://lod2.example/LOD2_23425822_2.gml",
            },
            "geometry": {"type": "Polygon", "coordinates": [[
                [341935.5, 5822002.1], [343998.0, 5821935.9],
                [344063.7, 5823998.0], [342002.1, 5824064.1],
                [341935.5, 5822002.1],
            ]]},
        }],
    }).encode()
    mapping = _parse_geojson_index(content, src)
    assert mapping == {"342_5822": "https://lod2.example/LOD2_23425822_2.gml"}


def test_geojson_index_sh_koordinaten_aus_dateiname():
    src = LOD2_SOURCES["Schleswig-Holstein"]
    content = json.dumps({
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {"data_link": (
                "https://geodaten.schleswig-holstein.de/x/massen.php"
                "?file=LoD2_32_426_6004_1_SH.xml&id=4&km=32420_6000")},
            "geometry": {"type": "Polygon", "coordinates": [[[0, 0]]]},
        }],
    }).encode()
    mapping = _parse_geojson_index(content, src)
    assert mapping == {
        "426_6004": ("https://geodaten.schleswig-holstein.de/x/massen.php"
                     "?file=LoD2_32_426_6004_1_SH.xml&id=4&km=32420_6000")
    }


def test_prepare_page_st_label_zu_id():
    src = LOD2_SOURCES["Sachsen-Anhalt"]
    html = ('... {"properties": {"id": "689732","label": "327245648"}} '
            '{"properties": {"id": "689733","label": "327265648"}} ...').encode()
    mapping = _parse_prepare_page(html, src)
    assert mapping == {"724_5648": "689732", "726_5648": "689733"}


def test_tile_urls_index_fehlend_ist_leere_kachel(monkeypatch):
    src = LOD2_SOURCES["Niedersachsen"]
    monkeypatch.setattr(loader, "_ensure_index",
                        lambda s: {"342_5822": "https://x/le.gml"})
    assert _tile_urls(src, 342, 5822) == ["https://x/le.gml"]
    assert _tile_urls(src, 400, 5900) == []          # nicht im Index → leer
    monkeypatch.setattr(loader, "_ensure_index", lambda s: None)
    assert _tile_urls(src, 342, 5822) is None        # Indexfehler → Fallback


def test_tile_urls_prepare_ruft_endpoint(monkeypatch):
    src = LOD2_SOURCES["Sachsen-Anhalt"]
    monkeypatch.setattr(loader, "_ensure_index", lambda s: {"724_5648": "689732"})

    class _Resp:
        status_code = 200
        text = ("https://www.lvermgeo.sachsen-anhalt.de/de/mod/4,1965,501/"
                "ajax/1/download/?file=mapdownloader-abc.zip")

        def raise_for_status(self):
            pass

    seen = {}

    def fake_get(url, **kwargs):
        seen["url"] = url
        return _Resp()

    monkeypatch.setattr(loader.httpx, "get", fake_get)
    urls = _tile_urls(src, 724, 5648)
    assert urls == [_Resp.text]
    assert "items=689732" in seen["url"] and "format=zip" in seen["url"]
    # Kachel außerhalb der ID-Map → gültig leer
    assert _tile_urls(src, 100, 5000) == []


def test_direkte_url_muster_der_neuen_laender():
    fixtures = {
        "Thüringen": (644, 5648, "LoD2_32_644_5648_2_TH.zip"),
        "Rheinland-Pfalz": (446, 5536, "LoD2_32_446_5536_2_RP.gml"),
        "Mecklenburg-Vorpommern": (262, 5948, "lod2_33_262_5948_2_gml.zip"),
        "Berlin": (391, 5819, "LoD2_391_5819.zip"),
        "Sachsen": (410, 5656, "lod2_33410_5656_2_sn_citygml.zip"),
        "Baden-Württemberg": (509, 5400, "LoD2_32_509_5400_2_bw.zip"),
    }
    for land, (e, n, fname) in fixtures.items():
        urls = LOD2_SOURCES[land].url_builder(e, n)
        assert urls and fname in urls[0], f"{land}: {urls}"


def test_bremen_stadtarchive_konfiguriert():
    src = LOD2_SOURCES["Bremen"]
    assert src.tile_km == 0 and len(src.city_urls) == 2
    assert all(u.endswith(".zip") for u in src.city_urls)
