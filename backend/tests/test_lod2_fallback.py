"""Tests für LoD2-Loader: Fallback-Regeln, Kachel-Cache, Quellen-Ersetzung."""

from __future__ import annotations

import gzip
import json
import os

import pytest
from pyproj import Transformer
from shapely.geometry import box
from shapely.ops import transform as shp_transform

from app.config import settings
from app.services.geodata.lod2 import loader
from app.services.geodata.lod2.loader import fetch_lod2_buildings
from app.services.geodata.lod2.sources import LOD2_SOURCES

_TO_WGS = Transformer.from_crs("EPSG:25832", "EPSG:4326", always_xy=True)


def _bbox_around_utm(x: float, y: float, half_m: float) -> str:
    """WGS84-bbox 's,w,n,e' um einen UTM32-Punkt."""
    g = shp_transform(_TO_WGS.transform,
                      box(x - half_m, y - half_m, x + half_m, y + half_m))
    w, s, e, n = g.bounds
    return f"{s},{w},{n},{e}"


def _citygml_at(x: float, y: float) -> bytes:
    """Minimal-CityGML: ein Gebäude 10×10 m, 12 m hoch, bei (x, y) UTM32."""
    return f"""<?xml version="1.0"?>
    <core:CityModel xmlns:core="http://www.opengis.net/citygml/2.0"
        xmlns:bldg="http://www.opengis.net/citygml/building/2.0"
        xmlns:gml="http://www.opengis.net/gml">
      <core:cityObjectMember><bldg:Building gml:id="T1">
        <bldg:measuredHeight uom="m">12.0</bldg:measuredHeight>
        <bldg:boundedBy><bldg:GroundSurface>
          <bldg:lod2MultiSurface><gml:MultiSurface><gml:surfaceMember>
            <gml:Polygon><gml:exterior><gml:LinearRing>
              <gml:posList>{x} {y} 100 {x + 10} {y} 100 {x + 10} {y + 10} 100 {x} {y + 10} 100 {x} {y} 100</gml:posList>
            </gml:LinearRing></gml:exterior></gml:Polygon>
          </gml:surfaceMember></gml:MultiSurface></bldg:lod2MultiSurface>
        </bldg:GroundSurface></bldg:boundedBy>
      </bldg:Building></core:cityObjectMember>
    </core:CityModel>""".encode()


class _Resp:
    def __init__(self, status_code: int, content: bytes = b""):
        self.status_code = status_code
        self.content = content

    def raise_for_status(self):
        if self.status_code >= 400:
            import httpx
            raise httpx.HTTPStatusError("err", request=None, response=None)


@pytest.fixture()
def lod2_cache(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "LOD2_CACHE_DIR", str(tmp_path))
    monkeypatch.setattr(settings, "LOD2_ENABLED", True)
    return tmp_path


def test_disabled_ergibt_none(lod2_cache, monkeypatch):
    monkeypatch.setattr(settings, "LOD2_ENABLED", False)
    assert fetch_lod2_buildings("51.0,6.9,51.01,6.91",
                                "Nordrhein-Westfalen") is None


def test_unbekanntes_und_phase2_land_ergibt_none(lod2_cache):
    assert fetch_lod2_buildings("51.0,6.9,51.01,6.91", "Atlantis") is None
    assert fetch_lod2_buildings("51.0,6.9,51.01,6.91", None) is None
    assert LOD2_SOURCES["Hessen"].phase == 2
    assert fetch_lod2_buildings("50.1,8.6,50.11,8.61", "Hessen") is None


def test_max_tiles_guard_ergibt_none(lod2_cache, monkeypatch):
    monkeypatch.setattr(settings, "LOD2_MAX_TILES", 4)
    # ~10×10 km → weit über 4 NRW-1-km-Kacheln; kein Netzzugriff nötig
    assert fetch_lod2_buildings(
        _bbox_around_utm(350000, 5650000, 5000), "Nordrhein-Westfalen") is None


def test_404_wird_als_leere_kachel_gecacht(lod2_cache, monkeypatch):
    calls: list[str] = []  # list.append ist unter dem GIL threadsicher

    def fake_get(url, **kwargs):
        calls.append(url)
        return _Resp(404)

    monkeypatch.setattr(loader.httpx, "get", fake_get)
    bbox = _bbox_around_utm(350500, 5650500, 200)

    out = fetch_lod2_buildings(bbox, "Nordrhein-Westfalen")
    assert out == []  # Abdeckung ohne Gebäude ist gültig (ersetzt OSM)
    first_calls = len(calls)
    assert first_calls > 0

    cache_dir = os.path.join(str(lod2_cache), "extracted", "nordrhein-westfalen")
    files = os.listdir(cache_dir)
    assert files
    with gzip.open(os.path.join(cache_dir, files[0]), "rt") as fh:
        payload = json.load(fh)
    assert payload["n"] == 0

    # Zweiter Aufruf: komplett aus dem Cache, kein weiterer HTTP-Call
    assert fetch_lod2_buildings(bbox, "Nordrhein-Westfalen") == []
    assert len(calls) == first_calls


def test_happy_path_und_cache_wiederverwendung(lod2_cache, monkeypatch):
    def fake_get(url, **kwargs):
        return _Resp(200, _citygml_at(350495, 5650495))

    monkeypatch.setattr(loader.httpx, "get", fake_get)
    bbox = _bbox_around_utm(350500, 5650500, 200)

    out = fetch_lod2_buildings(bbox, "Nordrhein-Westfalen")
    assert out is not None and len(out) > 0
    b = out[0]
    assert b["building_type"] == "lod2"
    assert b["height"] == pytest.approx(12.0)
    assert b["levels"] == 4
    # WGS84-Geometrie in plausibler Gegend (Rheinland)
    w, s, e, n = b["geometry"].bounds
    assert 5.0 < w < 8.0 and 50.0 < s < 52.0

    # Zweiter Aufruf ohne Netz (Cache): identische Anzahl
    def boom(url, **kwargs):
        raise AssertionError("HTTP-Call trotz Cache")

    monkeypatch.setattr(loader.httpx, "get", boom)
    again = fetch_lod2_buildings(bbox, "Nordrhein-Westfalen")
    assert again is not None and len(again) == len(out)


def test_netzwerkfehler_ergibt_none_und_cached_nicht(lod2_cache, monkeypatch):
    import httpx

    def fake_get(url, **kwargs):
        raise httpx.ConnectError("offline")

    monkeypatch.setattr(loader.httpx, "get", fake_get)
    monkeypatch.setattr(loader.time, "sleep", lambda s: None)
    bbox = _bbox_around_utm(350500, 5650500, 200)

    assert fetch_lod2_buildings(bbox, "Nordrhein-Westfalen") is None
    cache_dir = os.path.join(str(lod2_cache), "extracted", "nordrhein-westfalen")
    assert not os.path.isdir(cache_dir) or not os.listdir(cache_dir)


def test_fetch_buildings_and_roads_setzt_building_source(monkeypatch):
    from app.services.climate.heat import osm_data

    monkeypatch.setattr(
        osm_data, "_overpass_query_cached",
        lambda kind, bbox, query: {"elements": [], "_response_bytes": 0})
    osm_data._buildings_cache.clear()

    cells = [{"geometry": box(6.9, 51.0, 6.905, 51.005)}]

    # Fall 1: LoD2 aus → OSM-Quelle
    monkeypatch.setattr(settings, "LOD2_ENABLED", False)
    res = osm_data.fetch_buildings_and_roads(cells, "Nordrhein-Westfalen")
    assert res["building_source"] == "osm"

    # Fall 2: LoD2 liefert → ersetzt Gebäudeset
    osm_data._buildings_cache.clear()
    monkeypatch.setattr(settings, "LOD2_ENABLED", True)
    fake = [{"geometry": box(6.901, 51.001, 6.9012, 51.0012),
             "height": 15.0, "levels": 5, "building_type": "lod2"}]
    monkeypatch.setattr(
        "app.services.geodata.lod2.loader.fetch_lod2_buildings",
        lambda bbox, bundesland, keep_raw=False: fake)
    res = osm_data.fetch_buildings_and_roads(cells, "Nordrhein-Westfalen")
    assert res["building_source"] == "lod2"
    assert res["buildings"] == fake
    osm_data._buildings_cache.clear()
