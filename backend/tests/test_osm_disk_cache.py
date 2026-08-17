"""Tests für den Overpass-Roh-JSON-Disk-Cache (kein Netz, kein DB)."""

from __future__ import annotations

import gzip
import os
import time

import pytest

from app.config import settings
from app.services.climate.heat import osm_data


@pytest.fixture()
def cache_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "OSM_CACHE_DIR", str(tmp_path))
    monkeypatch.setattr(settings, "OSM_CACHE_TTL_S", 3600)
    return tmp_path


@pytest.fixture()
def fake_overpass(monkeypatch):
    calls = {"n": 0}

    def _fake(query_body: str, _retries: int = 5) -> dict:
        calls["n"] += 1
        return {"elements": [{"type": "node", "id": 1, "lon": 12.3, "lat": 51.3}],
                "_response_bytes": 42}

    monkeypatch.setattr(osm_data, "_overpass_query", _fake)
    return calls


def test_roundtrip_second_call_hits_disk(cache_dir, fake_overpass):
    bbox = "51.0,12.0,51.5,12.5"
    d1 = osm_data._overpass_query_cached("landuse", bbox, "QUERY")
    d2 = osm_data._overpass_query_cached("landuse", bbox, "QUERY")
    assert fake_overpass["n"] == 1
    assert d1 == d2
    files = [f for f in os.listdir(cache_dir) if f.startswith("landuse_")]
    assert len(files) == 1 and files[0].endswith(".json.gz")


def test_key_separates_kind_and_bbox(cache_dir, fake_overpass):
    osm_data._overpass_query_cached("landuse", "1,2,3,4", "Q")
    osm_data._overpass_query_cached("water", "1,2,3,4", "Q")
    osm_data._overpass_query_cached("landuse", "5,6,7,8", "Q")
    assert fake_overpass["n"] == 3
    assert len(os.listdir(cache_dir)) == 3


def test_ttl_expiry_refetches(cache_dir, fake_overpass):
    bbox = "51.0,12.0,51.5,12.5"
    osm_data._overpass_query_cached("infra", bbox, "Q")
    path = os.path.join(cache_dir, os.listdir(cache_dir)[0])
    old = time.time() - settings.OSM_CACHE_TTL_S - 10
    os.utime(path, (old, old))
    osm_data._overpass_query_cached("infra", bbox, "Q")
    assert fake_overpass["n"] == 2


def test_corrupt_file_treated_as_miss(cache_dir, fake_overpass):
    bbox = "51.0,12.0,51.5,12.5"
    osm_data._overpass_query_cached("buildings", bbox, "Q")
    path = os.path.join(cache_dir, os.listdir(cache_dir)[0])
    with open(path, "wb") as fh:
        fh.write(b"kein gzip")
    data = osm_data._overpass_query_cached("buildings", bbox, "Q")
    assert fake_overpass["n"] == 2
    assert data["_response_bytes"] == 42
    # Danach wieder lesbar (frisch geschrieben)
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        assert "elements" in fh.read()
