"""Gepinnte Ortsteilgrenzen der Beispielkommune Warmsen (T-1563-cto, Paket 5a von T-1418-cto).

Liest ohne Netzzugriff ``backend/data/kalibrierung/ortsteile_03256034.geojson`` und ``ortsteile.md`` und prüft
Aufbau, Kopfangaben, Eigenschaften je Fläche und die Beschreibung (Quelle, Lizenz, Stand, Befehl, Zahl der Flächen).
Erzeugt von ``backend/scripts/ortsteile_pinnen.py --gemeinde 03256034``.
"""
from __future__ import annotations

import json
import re
from datetime import date, datetime
from pathlib import Path

import pytest
from shapely.geometry import shape

DATEN = Path(__file__).resolve().parents[1] / "data" / "kalibrierung"
GEOJSON = DATEN / "ortsteile_03256034.geojson"
BESCHREIBUNG = DATEN / "ortsteile.md"


@pytest.fixture(scope="module")
def daten() -> dict:
    return json.loads(GEOJSON.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def text() -> str:
    return BESCHREIBUNG.read_text(encoding="utf-8")


def test_featurecollection_mit_kopfangaben(daten):
    assert daten["type"] == "FeatureCollection"
    assert isinstance(daten["features"], list)
    # Zeitstempel der Overpass-Antwort (osm3s.timestamp_osm_base), ISO 8601 in UTC
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", daten["stand_osm_base"])
    datetime.strptime(daten["stand_osm_base"], "%Y-%m-%dT%H:%M:%SZ")
    date.fromisoformat(daten["abgerufen"])
    # Kein abweichendes Koordinatensystem angegeben: nur fehlend oder CRS84/EPSG:4326
    crs = daten.get("crs")
    if crs is not None:
        assert crs["properties"]["name"] in ("urn:ogc:def:crs:OGC:1.3:CRS84", "EPSG:4326",
                                             "urn:ogc:def:crs:EPSG::4326")


def _koordinaten(geom: dict):
    polys = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
    for poly in polys:
        for ring in poly:
            yield from ring


def test_features(daten):
    for f in daten["features"]:
        assert f["type"] == "Feature"
        p = f["properties"]
        assert isinstance(p["name"], str) and p["name"].strip()
        assert p["admin_level"] in (9, 10)
        assert isinstance(p["osm_relation"], int) and not isinstance(p["osm_relation"], bool)
        assert p["osm_relation"] > 0
        assert 0.5 <= p["anteil_in_gemeinde"] <= 1.0
        geom = f["geometry"]
        assert geom["type"] in ("Polygon", "MultiPolygon")
        form = shape(geom)
        assert form.is_valid and not form.is_empty and form.area > 0
        for lon, lat, *_ in _koordinaten(geom):
            assert -180.0 <= lon <= 180.0 and -90.0 <= lat <= 90.0
        # Plausibel für Deutschland: Längen und Breiten nicht vertauscht, nicht projiziert
        minx, miny, maxx, maxy = form.bounds
        assert 5.5 <= minx and maxx <= 15.5 and 47.0 <= miny and maxy <= 55.5


def test_relationen_eindeutig(daten):
    ids = [f["properties"]["osm_relation"] for f in daten["features"]]
    assert len(ids) == len(set(ids))


def test_beschreibung(daten, text):
    assert "OpenStreetMap" in text
    assert "ODbL" in text
    assert daten["stand_osm_base"] in text
    assert daten["abgerufen"] in text
    assert "backend/scripts/ortsteile_pinnen.py --gemeinde 03256034" in text
    m = re.search(r"Zahl der Flächen: \*\*(\d+)\*\*", text)
    assert m, "ortsteile.md nennt die Zahl der Flächen nicht („Zahl der Flächen: **n**“)"
    assert int(m.group(1)) == len(daten["features"])
