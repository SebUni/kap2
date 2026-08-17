"""Streaming-CityGML-Parser: Gebäude-Footprints + Höhen aus LoD2-Kacheln.

Kacheln sind 50–500 MB XML — deshalb ``ElementTree.iterparse`` mit Element-
Clearing nach jedem Gebäude (Speicher bleibt flach) statt DOM/lxml.

Namespace-Varianz: Die Länder liefern CityGML 1.0 (u. a. Hamburg) und 2.0 mit
unterschiedlichen Namespace-URIs — Matching daher über den Localname.

Höhe je Gebäude: ``bldg:measuredHeight``; fehlt sie, Fallback auf die
z-Ausdehnung (max−min) aller Koordinaten des Gebäudes; ohne beides wird das
Gebäude übersprungen. ``BuildingPart``s werden dem übergeordneten ``Building``
zugeschlagen (Footprint-Union, Höhe = Maximum der Teile).

Footprint: Union der ``bldg:GroundSurface``-Polygone; ohne GroundSurface die
2D-Hülle (convex hull) der Koordinatenwolke des Gebäudes.
"""
from __future__ import annotations

import logging
import xml.etree.ElementTree as ET
from typing import IO

from pyproj import Transformer
from shapely.geometry import MultiPoint, Polygon
from shapely.ops import transform as shp_transform, unary_union

log = logging.getLogger(__name__)

_TRANSFORMERS: dict[str, Transformer] = {}


def _transformer(crs: str) -> Transformer:
    tr = _TRANSFORMERS.get(crs)
    if tr is None:
        tr = Transformer.from_crs(crs, "EPSG:4326", always_xy=True)
        _TRANSFORMERS[crs] = tr
    return tr


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _parse_poslist(text: str) -> list[tuple[float, float, float]]:
    """gml:posList/pos-Text → [(x, y, z), …]; 2D-Listen bekommen z=0."""
    vals = text.split()
    if not vals:
        return []
    try:
        nums = [float(v) for v in vals]
    except ValueError:
        return []
    # LoD2-Geometrien sind 3D; falls die Länge nicht durch 3 teilbar ist,
    # als 2D interpretieren (defensiv, kommt bei Envelope-Ecken vor).
    if len(nums) % 3 == 0:
        return [(nums[i], nums[i + 1], nums[i + 2]) for i in range(0, len(nums), 3)]
    if len(nums) % 2 == 0:
        return [(nums[i], nums[i + 1], 0.0) for i in range(0, len(nums), 2)]
    return []


class _BuildingAccu:
    """Sammelt Geometrie/Höhe eines Buildings inkl. seiner BuildingParts."""

    __slots__ = ("measured_heights", "ground_rings", "all_coords",
                 "in_ground_surface")

    def __init__(self) -> None:
        self.measured_heights: list[float] = []
        self.ground_rings: list[list[tuple[float, float]]] = []
        self.all_coords: list[tuple[float, float, float]] = []
        self.in_ground_surface = 0

    def footprint(self) -> Polygon | None:
        polys = []
        for ring in self.ground_rings:
            if len(ring) >= 4:
                try:
                    p = Polygon(ring)
                    if p.is_valid and p.area > 0:
                        polys.append(p)
                    elif not p.is_valid:
                        p = p.buffer(0)
                        if not p.is_empty:
                            polys.append(p)
                except (ValueError, TypeError):
                    continue
        if polys:
            merged = unary_union(polys)
            if merged.geom_type == "MultiPolygon":
                # Teilgebäude können disjunkt sein — größtes Teil reicht nicht,
                # konvexe Hülle überzeichnet: nimm die Union als Hülle je Teil
                # zusammengefasst über die Gesamthülle der Ringe.
                merged = merged.convex_hull if merged.is_empty else merged
            if not merged.is_empty:
                return merged
        if len(self.all_coords) >= 3:
            hull = MultiPoint([(x, y) for x, y, _ in self.all_coords]).convex_hull
            if hull.geom_type == "Polygon" and hull.area > 0:
                return hull
        return None

    def height(self) -> float | None:
        if self.measured_heights:
            return max(self.measured_heights)
        zs = [z for _, _, z in self.all_coords]
        if len(zs) >= 2:
            dz = max(zs) - min(zs)
            if dz > 0.5:  # < 0.5 m ist kein plausibles Gebäude
                return dz
        return None


def parse_citygml(fileobj: IO[bytes], crs: str) -> list[tuple[object, float]]:
    """Parst eine CityGML-Datei → [(footprint_wgs84, hoehe_m), …].

    ``footprint_wgs84`` ist ein shapely-(Multi)Polygon in EPSG:4326.
    """
    tr = _transformer(crs)
    out: list[tuple[object, float]] = []
    accu: _BuildingAccu | None = None
    depth_in_building = 0
    skipped = 0

    for event, elem in ET.iterparse(fileobj, events=("start", "end")):
        name = _local(elem.tag)

        if event == "start":
            if name == "Building":
                accu = _BuildingAccu()
                depth_in_building = 1
            elif accu is not None:
                depth_in_building += 1
                if name == "GroundSurface":
                    accu.in_ground_surface += 1
            continue

        # event == "end"
        if accu is not None:
            if name == "measuredHeight" and elem.text:
                try:
                    accu.measured_heights.append(float(elem.text))
                except ValueError:
                    pass
            elif name in ("posList", "pos") and elem.text:
                coords = _parse_poslist(elem.text)
                accu.all_coords.extend(coords)
                if accu.in_ground_surface > 0 and name == "posList":
                    ring = [(x, y) for x, y, _ in coords]
                    if len(ring) >= 4:
                        accu.ground_rings.append(ring)
            elif name == "GroundSurface":
                accu.in_ground_surface -= 1

            depth_in_building -= 1
            if name == "Building" or depth_in_building <= 0:
                fp = accu.footprint()
                h = accu.height()
                if fp is not None and h is not None:
                    try:
                        fp_wgs = shp_transform(tr.transform, fp)
                        out.append((fp_wgs, round(h, 2)))
                    except Exception:  # noqa: BLE001 — defekte Einzelgeometrie
                        skipped += 1
                else:
                    skipped += 1
                accu = None
                depth_in_building = 0
                elem.clear()
        else:
            # außerhalb von Buildings: Speicher freigeben
            elem.clear()

    if skipped:
        log.debug("parse_citygml: %d Gebäude ohne Footprint/Höhe übersprungen",
                  skipped)
    return out
