"""Tests für den CityGML-Parser (LoD2): Footprints + Höhen, ohne Netz."""

from __future__ import annotations

import io

from pyproj import Transformer
from shapely.ops import transform as shp_transform

from app.services.geodata.lod2.citygml import parse_citygml

_TO_UTM = Transformer.from_crs("EPSG:4326", "EPSG:25832", always_xy=True)


def _utm_area(geom_wgs84) -> float:
    return shp_transform(_TO_UTM.transform, geom_wgs84).area


# Gebäude 1: measuredHeight + GroundSurface (10×10 m bei 350000/5650000).
# Gebäude 2: KEIN measuredHeight, keine GroundSurface — Höhe aus z-Ausdehnung
# (Wand 100→108 m), Footprint aus der konvexen Hülle (Dachfläche 10×10 m).
CITYGML_20 = """<?xml version="1.0" encoding="UTF-8"?>
<core:CityModel xmlns:core="http://www.opengis.net/citygml/2.0"
    xmlns:bldg="http://www.opengis.net/citygml/building/2.0"
    xmlns:gml="http://www.opengis.net/gml">
  <core:cityObjectMember>
    <bldg:Building gml:id="B1">
      <bldg:measuredHeight uom="m">12.5</bldg:measuredHeight>
      <bldg:boundedBy>
        <bldg:GroundSurface>
          <bldg:lod2MultiSurface><gml:MultiSurface><gml:surfaceMember>
            <gml:Polygon><gml:exterior><gml:LinearRing>
              <gml:posList>350000 5650000 100 350010 5650000 100 350010 5650010 100 350000 5650010 100 350000 5650000 100</gml:posList>
            </gml:LinearRing></gml:exterior></gml:Polygon>
          </gml:surfaceMember></gml:MultiSurface></bldg:lod2MultiSurface>
        </bldg:GroundSurface>
      </bldg:boundedBy>
    </bldg:Building>
  </core:cityObjectMember>
  <core:cityObjectMember>
    <bldg:Building gml:id="B2">
      <bldg:boundedBy>
        <bldg:RoofSurface>
          <bldg:lod2MultiSurface><gml:MultiSurface><gml:surfaceMember>
            <gml:Polygon><gml:exterior><gml:LinearRing>
              <gml:posList>350020 5650000 108 350030 5650000 108 350030 5650010 108 350020 5650010 108 350020 5650000 108</gml:posList>
            </gml:LinearRing></gml:exterior></gml:Polygon>
          </gml:surfaceMember></gml:MultiSurface></bldg:lod2MultiSurface>
        </bldg:RoofSurface>
      </bldg:boundedBy>
      <bldg:boundedBy>
        <bldg:WallSurface>
          <bldg:lod2MultiSurface><gml:MultiSurface><gml:surfaceMember>
            <gml:Polygon><gml:exterior><gml:LinearRing>
              <gml:posList>350020 5650000 100 350030 5650000 100 350030 5650000 108 350020 5650000 108 350020 5650000 100</gml:posList>
            </gml:LinearRing></gml:exterior></gml:Polygon>
          </gml:surfaceMember></gml:MultiSurface></bldg:lod2MultiSurface>
        </bldg:WallSurface>
      </bldg:boundedBy>
    </bldg:Building>
  </core:cityObjectMember>
</core:CityModel>
"""

# CityGML 1.0 (andere Namespace-URIs, z. B. Hamburg): Localname-Matching muss greifen.
CITYGML_10 = """<?xml version="1.0" encoding="UTF-8"?>
<core:CityModel xmlns:core="http://www.opengis.net/citygml/1.0"
    xmlns:bldg="http://www.opengis.net/citygml/building/1.0"
    xmlns:gml="http://www.opengis.net/gml">
  <core:cityObjectMember>
    <bldg:Building gml:id="H1">
      <bldg:measuredHeight uom="m">7.4</bldg:measuredHeight>
      <bldg:boundedBy>
        <bldg:GroundSurface>
          <bldg:lod2MultiSurface><gml:MultiSurface><gml:surfaceMember>
            <gml:Polygon><gml:exterior><gml:LinearRing>
              <gml:posList>565000 5930000 5 565008 5930000 5 565008 5930012 5 565000 5930012 5 565000 5930000 5</gml:posList>
            </gml:LinearRing></gml:exterior></gml:Polygon>
          </gml:surfaceMember></gml:MultiSurface></bldg:lod2MultiSurface>
        </bldg:GroundSurface>
      </bldg:boundedBy>
    </bldg:Building>
  </core:cityObjectMember>
</core:CityModel>
"""


def test_citygml20_measured_height_und_groundsurface():
    result = parse_citygml(io.BytesIO(CITYGML_20.encode()), "EPSG:25832")
    assert len(result) == 2
    heights = sorted(h for _, h in result)
    assert heights == [8.0, 12.5]

    by_height = {h: g for g, h in result}
    # B1: GroundSurface 10×10 m
    assert abs(_utm_area(by_height[12.5]) - 100.0) < 2.0
    # B2: konvexe Hülle der Dach-/Wandkoordinaten = 10×10 m
    assert abs(_utm_area(by_height[8.0]) - 100.0) < 2.0


def test_citygml20_footprint_liegt_in_wgs84():
    result = parse_citygml(io.BytesIO(CITYGML_20.encode()), "EPSG:25832")
    for geom, _ in result:
        w, s, e, n = geom.bounds
        # UTM32 350000/5650000 → grob 6,9° E / 51,0° N
        assert 5.0 < w < 8.0 and 50.0 < s < 52.0
        assert e - w < 0.01 and n - s < 0.01


def test_citygml10_namespace_variante():
    result = parse_citygml(io.BytesIO(CITYGML_10.encode()), "EPSG:25832")
    assert len(result) == 1
    geom, h = result[0]
    assert h == 7.4
    assert abs(_utm_area(geom) - 96.0) < 2.0  # 8×12 m


def test_gebaeude_ohne_hoehe_und_geometrie_wird_uebersprungen():
    xml = """<?xml version="1.0"?>
    <core:CityModel xmlns:core="http://www.opengis.net/citygml/2.0"
        xmlns:bldg="http://www.opengis.net/citygml/building/2.0">
      <core:cityObjectMember><bldg:Building/></core:cityObjectMember>
    </core:CityModel>"""
    assert parse_citygml(io.BytesIO(xml.encode()), "EPSG:25832") == []
