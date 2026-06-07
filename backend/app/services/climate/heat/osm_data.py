"""Fetch and process OSM data for heat assessment levels 2 and 3.

Level 2: Land-use polygons per grid cell (residential, commercial, green, water, …).
Level 3: Individual building footprints, road surfaces, tree canopy.
"""

import logging
import threading
import time as _time
from typing import Any

import httpx
from shapely.geometry import shape, Polygon, MultiPolygon, LineString, mapping
from shapely.ops import unary_union

from app.config import settings

log = logging.getLogger(__name__)

OVERPASS_TIMEOUT = 120

# ── Thread-safe OSM data cache ────────────────────────────────────────────────
# Keyed by bbox string. Each entry is (timestamp, data).
# Cache is shared across assessors so identical Overpass queries are made once.

_cache_lock = threading.Lock()
_landuse_cache: dict[str, tuple[float, list[dict], int]] = {}  # bbox → (ts, features, bytes)
_buildings_cache: dict[str, tuple[float, dict]] = {}            # bbox → (ts, result_dict)
_water_cache: dict[str, tuple[float, list[dict]]] = {}          # bbox → (ts, water features)
_CACHE_TTL = 600  # 10 min – long enough for a full batch run

# ── Land-use categories and their properties ─────────────────────────────────

LANDUSE_IMPERVIOUS: dict[str, float] = {
    # OSM landuse tag → typical impervious fraction
    "residential": 0.55,
    "commercial": 0.85,
    "industrial": 0.90,
    "retail": 0.85,
    "construction": 0.60,
    "railway": 0.70,
    "farmland": 0.05,
    "farmyard": 0.40,
    "forest": 0.02,
    "meadow": 0.03,
    "grass": 0.03,
    "orchard": 0.05,
    "vineyard": 0.05,
    "cemetery": 0.25,
    "allotments": 0.15,
    "recreation_ground": 0.20,
    "village_green": 0.05,
}

LANDUSE_ALBEDO: dict[str, float] = {
    "residential": 0.20,
    "commercial": 0.18,
    "industrial": 0.15,
    "retail": 0.18,
    "construction": 0.22,
    "railway": 0.15,
    "farmland": 0.25,
    "farmyard": 0.22,
    "forest": 0.12,
    "meadow": 0.25,
    "grass": 0.25,
    "orchard": 0.18,
    "vineyard": 0.20,
    "cemetery": 0.22,
    "allotments": 0.22,
    "recreation_ground": 0.23,
    "village_green": 0.25,
}

NATURAL_IMPERVIOUS: dict[str, float] = {
    "wood": 0.02,
    "scrub": 0.05,
    "heath": 0.05,
    "grassland": 0.03,
    "water": 0.00,
    "wetland": 0.02,
    "bare_rock": 0.10,
    "sand": 0.05,
}

NATURAL_ALBEDO: dict[str, float] = {
    "wood": 0.12,
    "scrub": 0.18,
    "heath": 0.20,
    "grassland": 0.25,
    "water": 0.06,
    "wetland": 0.12,
    "bare_rock": 0.30,
    "sand": 0.35,
}


def _overpass_query(query_body: str, _retries: int = 5) -> dict:
    """Execute a synchronous Overpass API query with retry on transient errors.

    Handles 429 (rate-limit) by respecting the ``Retry-After`` header, and
    uses exponential back-off for 504 / timeout errors.  Returns the parsed
    JSON dict with an extra ``_response_bytes`` key for size tracking.
    """
    import time as _time
    full_query = f"[out:json][timeout:{OVERPASS_TIMEOUT}];\n{query_body}"
    for attempt in range(1, _retries + 1):
        try:
            with httpx.Client(timeout=OVERPASS_TIMEOUT + 10) as client:
                resp = client.post(
                    settings.OVERPASS_URL,
                    data={"data": full_query},
                    headers={
                        "User-Agent": settings.NOMINATIM_USER_AGENT,
                        "Accept": "application/json",
                    },
                )
                resp.raise_for_status()
                raw_bytes = len(resp.content)
                result = resp.json()
                result["_response_bytes"] = raw_bytes
                return result
        except httpx.HTTPStatusError as exc:
            if attempt < _retries:
                if exc.response.status_code == 429:
                    # Respect Retry-After header; default 30 s
                    retry_after = exc.response.headers.get("Retry-After")
                    wait = int(retry_after) if retry_after and retry_after.isdigit() else 30
                    wait = min(wait, 90)  # cap at 90 s
                else:
                    wait = 5 * attempt  # 5s, 10s, 15s …
                log.warning("Overpass query attempt %d/%d failed (HTTP %s), retrying in %ds",
                            attempt, _retries, exc.response.status_code, wait)
                _time.sleep(wait)
            else:
                raise
        except httpx.TimeoutException as exc:
            if attempt < _retries:
                wait = 5 * attempt
                log.warning("Overpass query attempt %d/%d timed out, retrying in %ds",
                            attempt, _retries, wait)
                _time.sleep(wait)
            else:
                raise


def _bbox_from_cells(grid_cells: list[dict]) -> str:
    """Compute a bounding box string (south,west,north,east) from grid cells."""
    from shapely.ops import unary_union as _union
    all_geoms = [c["geometry"] for c in grid_cells]
    combined = _union(all_geoms)
    minx, miny, maxx, maxy = combined.bounds
    return f"{miny},{minx},{maxy},{maxx}"


def prefetch_osm_data(grid_cells: list[dict], include_buildings: bool = False):
    """Pre-fetch and cache OSM data for the given grid cells.

    Call this once before running multiple assessors on the same grid
    to avoid repeated Overpass API requests and 429 rate-limits.
    """
    log.info("prefetch_osm_data: landuse (+ buildings=%s) for %d cells", include_buildings, len(grid_cells))
    fetch_landuse(grid_cells)
    if include_buildings:
        fetch_buildings_and_roads(grid_cells)


def clear_osm_cache():
    """Clear all cached OSM data."""
    with _cache_lock:
        _landuse_cache.clear()
        _buildings_cache.clear()
        _water_cache.clear()
    log.info("OSM data cache cleared")


# ── Level 2: Land-use data ────────────────────────────────────────────────────

def fetch_landuse(grid_cells: list[dict]) -> list[dict]:
    """Fetch OSM landuse and natural polygons covering the grid area.

    Returns tuple of (list of dicts, response_bytes).
    Uses thread-safe cache so concurrent assessors share the same data.
    """
    bbox = _bbox_from_cells(grid_cells)

    # ── Check cache ──────────────────────────────────────────────────────
    with _cache_lock:
        cached = _landuse_cache.get(bbox)
        if cached:
            ts, features, resp_bytes = cached
            if _time.time() - ts < _CACHE_TTL:
                log.info("fetch_landuse: cache HIT for bbox=%s (%d features)", bbox[:30], len(features))
                return features, resp_bytes
            else:
                del _landuse_cache[bbox]

    # ── Not cached — fetch from Overpass ─────────────────────────────────
    log.info("fetch_landuse: cache MISS for bbox=%s — querying Overpass", bbox[:30])

    query = f"""
    (
      way["landuse"]({bbox});
      relation["landuse"]({bbox});
      way["natural"]({bbox});
      relation["natural"]({bbox});
      way["leisure"="park"]({bbox});
      relation["leisure"="park"]({bbox});
    );
    out body;
    >;
    out skel qt;
    """

    data = _overpass_query(query)
    response_bytes = data.get("_response_bytes", 0)
    elements = data.get("elements", [])

    # Build node lookup
    nodes: dict[int, tuple[float, float]] = {}
    for el in elements:
        if el["type"] == "node":
            nodes[el["id"]] = (el["lon"], el["lat"])

    results = []
    for el in elements:
        tags = el.get("tags", {})
        landuse = tags.get("landuse", "")
        natural = tags.get("natural", "")
        leisure = tags.get("leisure", "")

        if not (landuse or natural or leisure):
            continue

        geom = _element_to_polygon(el, nodes, elements)
        if geom is None:
            continue

        results.append({
            "geometry": geom,
            "landuse": landuse,
            "natural": natural,
            "leisure": leisure,
        })

    log.info("Fetched %d land-use/natural features from OSM (%.2f MB)",
             len(results), response_bytes / 1_048_576)

    # ── Store in cache ───────────────────────────────────────────────────
    with _cache_lock:
        _landuse_cache[bbox] = (_time.time(), results, response_bytes)

    return results, response_bytes


def fetch_water_features(grid_cells: list[dict]) -> list[dict]:
    """Fetch OSM water polygons and waterways (rivers, streams, drains).

    Returns list of {geometry, kind} where kind is 'polygon' or 'line'.
    """
    bbox = _bbox_from_cells(grid_cells)

    with _cache_lock:
        cached = _water_cache.get(bbox)
        if cached and _time.time() - cached[0] < _CACHE_TTL:
            return cached[1]

    log.info("fetch_water_features: querying Overpass for bbox=%s", bbox[:30])

    query = f"""
    (
      way["natural"="water"]({bbox});
      relation["natural"="water"]({bbox});
      way["water"]({bbox});
      relation["water"]({bbox});
      way["waterway"]({bbox});
      relation["waterway"]({bbox});
    );
    out body;
    >;
    out skel qt;
    """

    data = _overpass_query(query)
    elements = data.get("elements", [])

    nodes: dict[int, tuple[float, float]] = {}
    for el in elements:
        if el["type"] == "node":
            nodes[el["id"]] = (el["lon"], el["lat"])

    results: list[dict] = []
    for el in elements:
        tags = el.get("tags", {})
        if not (tags.get("natural") == "water" or tags.get("water") or tags.get("waterway")):
            continue

        if el["type"] == "way":
            nds = el.get("nodes", [])
            coords = [nodes[n] for n in nds if n in nodes]
            if len(coords) < 2:
                continue
            waterway = tags.get("waterway", "")
            is_area = (
                tags.get("natural") == "water"
                or tags.get("water")
                or tags.get("area") == "yes"
                or (len(coords) >= 4 and coords[0] == coords[-1])
            )
            if is_area and len(coords) >= 4:
                try:
                    geom = Polygon(coords)
                    if not geom.is_valid:
                        geom = geom.buffer(0)
                    results.append({"geometry": geom, "kind": "polygon"})
                except Exception:
                    pass
            elif waterway or len(coords) >= 2:
                results.append({"geometry": LineString(coords), "kind": "line"})

        elif el["type"] == "relation":
            geom = _element_to_polygon(el, nodes, elements)
            if geom is not None:
                results.append({"geometry": geom, "kind": "polygon"})

    log.info("Fetched %d water features from OSM", len(results))

    with _cache_lock:
        _water_cache[bbox] = (_time.time(), results)

    return results


def compute_water_distance_m(
    cell_geom: Any,
    water_features: list[dict],
    cell_size_m: float,
) -> float:
    """Kürzeste Distanz (m) von der Zelle zum nächsten OSM-Gewässer."""
    if not water_features:
        return float(cell_size_m * 20)

    import pyproj
    from shapely.ops import transform as shp_transform

    minx, miny, maxx, maxy = cell_geom.bounds
    lat = (miny + maxy) / 2.0
    utm_zone = int((cell_geom.centroid.x + 180) / 6) + 1
    utm_epsg = 32600 + utm_zone if lat >= 0 else 32700 + utm_zone

    to_utm = pyproj.Transformer.from_crs("EPSG:4326", f"EPSG:{utm_epsg}", always_xy=True).transform
    cell_utm = shp_transform(to_utm, cell_geom)

    min_dist = float("inf")
    for feat in water_features:
        feat_utm = shp_transform(to_utm, feat["geometry"])
        d = cell_utm.distance(feat_utm)
        if d < min_dist:
            min_dist = d

    return min_dist if min_dist < float("inf") else float(cell_size_m * 20)


def water_proximity_score(dist_m: float, max_dist_m: float = 500.0) -> float:
    """0..1: 1 = direkt am Gewässer, 0 = weiter als max_dist_m entfernt."""
    if dist_m <= 0:
        return 1.0
    return max(0.0, 1.0 - dist_m / max_dist_m)


def compute_cell_landuse(
    cell_geom: Any,
    landuse_features: list[dict],
) -> dict:
    """Compute land-use composition for a single grid cell.

    Returns dict with:
        impervious_fraction, albedo, green_fraction, water_fraction,
        dominant_landuse, coverage_pct (how much of cell is covered by data).
    """
    cell_area = cell_geom.area
    if cell_area <= 0:
        return {"impervious_fraction": 0.05, "albedo": 0.23,
                "green_fraction": 0.0, "water_fraction": 0.0,
                "dominant_landuse": "unknown", "coverage_pct": 0.0}

    weighted_imp = 0.0
    weighted_albedo = 0.0
    total_covered = 0.0
    green_area = 0.0
    water_area = 0.0
    landuse_areas: dict[str, float] = {}

    for feat in landuse_features:
        feat_geom = feat["geometry"]
        if not cell_geom.intersects(feat_geom):
            continue

        intersection = cell_geom.intersection(feat_geom)
        int_area = intersection.area
        if int_area <= 0:
            continue

        lu = feat["landuse"]
        nat = feat["natural"]
        leisure = feat["leisure"]

        # Determine impervious fraction and albedo
        if lu and lu in LANDUSE_IMPERVIOUS:
            imp = LANDUSE_IMPERVIOUS[lu]
            alb = LANDUSE_ALBEDO.get(lu, 0.20)
            label = lu
        elif nat and nat in NATURAL_IMPERVIOUS:
            imp = NATURAL_IMPERVIOUS[nat]
            alb = NATURAL_ALBEDO.get(nat, 0.20)
            label = nat
        elif leisure == "park":
            imp = 0.10
            alb = 0.23
            label = "park"
        else:
            continue

        frac = int_area / cell_area
        weighted_imp += imp * frac
        weighted_albedo += alb * frac
        total_covered += frac
        landuse_areas[label] = landuse_areas.get(label, 0.0) + frac

        # Track green / water
        if nat == "water":
            water_area += frac
        elif nat in ("wood", "grassland", "scrub", "heath", "wetland"):
            green_area += frac
        elif lu in ("forest", "meadow", "grass", "orchard", "vineyard",
                     "allotments", "village_green"):
            green_area += frac
        elif leisure == "park":
            green_area += frac

    # Cap at 1.0
    total_covered = min(total_covered, 1.0)

    if total_covered > 0:
        imp_final = weighted_imp / total_covered
        alb_final = weighted_albedo / total_covered
    else:
        # No OSM data for this cell — assume unbuilt/rural fallback
        imp_final = 0.05
        alb_final = 0.23

    dominant = max(landuse_areas, key=landuse_areas.get) if landuse_areas else "unknown"

    # Detailed vegetation breakdown for Level 4
    forest_area = 0.0
    farmland_area = 0.0
    for label, area in landuse_areas.items():
        if label in ("forest", "wood"):
            forest_area += area
        elif label in ("farmland", "orchard", "vineyard"):
            farmland_area += area

    return {
        "impervious_fraction": round(min(max(imp_final, 0.0), 1.0), 4),
        "albedo": round(alb_final, 4),
        "green_fraction": round(min(green_area, 1.0), 4),
        "water_fraction": round(min(water_area, 1.0), 4),
        "forest_fraction": round(min(forest_area, 1.0), 4),
        "farmland_fraction": round(min(farmland_area, 1.0), 4),
        "dominant_landuse": dominant,
        "coverage_pct": round(total_covered * 100, 1),
    }


# ── Level 3: Buildings & detailed surfaces ────────────────────────────────────

def fetch_buildings_and_roads(grid_cells: list[dict]) -> dict:
    """Fetch building footprints, roads, and trees from OSM.

    Returns dict with keys: buildings, roads, trees – each a list of
    dicts with geometry and tags.  Uses thread-safe cache.
    """
    bbox = _bbox_from_cells(grid_cells)

    # ── Check cache ──────────────────────────────────────────────────────
    with _cache_lock:
        cached = _buildings_cache.get(bbox)
        if cached:
            ts, result = cached
            if _time.time() - ts < _CACHE_TTL:
                log.info("fetch_buildings_and_roads: cache HIT for bbox=%s", bbox[:30])
                return result
            else:
                del _buildings_cache[bbox]

    log.info("fetch_buildings_and_roads: cache MISS — querying Overpass")

    query = f"""
    (
      way["building"]({bbox});
      relation["building"]({bbox});
      way["highway"]({bbox});
      node["natural"="tree"]({bbox});
    );
    out body;
    >;
    out skel qt;
    """

    data = _overpass_query(query)
    response_bytes = data.get("_response_bytes", 0)
    elements = data.get("elements", [])

    nodes: dict[int, tuple[float, float]] = {}
    for el in elements:
        if el["type"] == "node":
            nodes[el["id"]] = (el["lon"], el["lat"])

    buildings = []
    roads = []
    trees = []

    for el in elements:
        tags = el.get("tags", {})

        if "building" in tags:
            geom = _element_to_polygon(el, nodes, elements)
            if geom is not None:
                levels = _parse_int(tags.get("building:levels"), 2)
                height = _parse_float(tags.get("height"), levels * 3.0)
                buildings.append({
                    "geometry": geom,
                    "levels": levels,
                    "height": height,
                    "building_type": tags.get("building", "yes"),
                })

        elif "highway" in tags and el["type"] == "way":
            nds = el.get("nodes", [])
            coords = [nodes[n] for n in nds if n in nodes]
            if len(coords) >= 2:
                from shapely.geometry import LineString
                line = LineString(coords)
                hw_type = tags.get("highway", "")
                width = _road_width(hw_type)
                roads.append({
                    "geometry": line,
                    "highway": hw_type,
                    "width_m": width,
                })

        elif tags.get("natural") == "tree" and el["type"] == "node":
            if el["id"] in nodes:
                trees.append({
                    "lon": nodes[el["id"]][0],
                    "lat": nodes[el["id"]][1],
                    "crown_diameter": _parse_float(
                        tags.get("diameter_crown"), 8.0
                    ),
                })

    log.info(
        "Fetched %d buildings, %d road segments, %d trees from OSM (%.2f MB)",
        len(buildings), len(roads), len(trees), response_bytes / 1_048_576,
    )
    result = {"buildings": buildings, "roads": roads, "trees": trees, "_response_bytes": response_bytes}

    # ── Store in cache ───────────────────────────────────────────────────
    with _cache_lock:
        _buildings_cache[bbox] = (_time.time(), result)

    return result


def compute_cell_buildings(
    cell_geom: Any,
    buildings: list[dict],
    roads: list[dict],
    trees: list[dict],
) -> dict:
    """Compute detailed building/surface metrics for a single grid cell.

    Returns dict with:
        building_density (buildings/km²),
        building_coverage (fraction of cell covered),
        avg_building_height (m),
        road_coverage (fraction),
        tree_count, tree_canopy_fraction,
        sky_view_factor (simplified 0–1).
    """
    cell_area = cell_geom.area  # in degree², used for fractions
    if cell_area <= 0:
        return _empty_building_metrics()

    # Buildings
    bldg_area = 0.0
    bldg_count = 0
    total_height = 0.0

    for b in buildings:
        bg = b["geometry"]
        if not cell_geom.intersects(bg):
            continue
        intersection = cell_geom.intersection(bg)
        ia = intersection.area
        if ia <= 0:
            continue
        bldg_area += ia
        bldg_count += 1
        total_height += b["height"]

    bldg_coverage = min(bldg_area / cell_area, 1.0) if cell_area > 0 else 0.0
    avg_height = (total_height / bldg_count) if bldg_count > 0 else 0.0

    # For building_density we need real-world area:
    # cell_geom is in EPSG:4326 so we approximate 1° ≈ 111 km at equator,
    # but the task already provides cell_size_m so caller should pass it.

    # Roads – buffer each line by half its width (in degrees, rough approx)
    road_area = 0.0
    DEGREE_PER_METER = 1.0 / 111_320.0  # rough
    for r in roads:
        rg = r["geometry"]
        if not cell_geom.intersects(rg):
            continue
        buf_deg = (r["width_m"] / 2.0) * DEGREE_PER_METER
        buffered = rg.buffer(buf_deg)
        intersection = cell_geom.intersection(buffered)
        road_area += intersection.area

    road_coverage = min(road_area / cell_area, 1.0) if cell_area > 0 else 0.0

    # Trees
    from shapely.geometry import Point
    tree_count = 0
    canopy_area = 0.0
    for t in trees:
        pt = Point(t["lon"], t["lat"])
        if cell_geom.contains(pt):
            tree_count += 1
            radius_deg = (t["crown_diameter"] / 2.0) * DEGREE_PER_METER
            canopy_area += 3.14159 * radius_deg ** 2

    canopy_fraction = min(canopy_area / cell_area, 1.0) if cell_area > 0 else 0.0

    # Simplified sky-view factor: 1 = open sky, 0 = fully enclosed
    # Decreases with building height and coverage
    svf = max(0.1, 1.0 - bldg_coverage * min(avg_height / 20.0, 1.0))

    return {
        "building_count": bldg_count,
        "building_coverage": round(bldg_coverage, 4),
        "avg_building_height": round(avg_height, 1),
        "road_coverage": round(road_coverage, 4),
        "tree_count": tree_count,
        "tree_canopy_fraction": round(canopy_fraction, 4),
        "sky_view_factor": round(svf, 3),
    }


def _empty_building_metrics() -> dict:
    return {
        "building_count": 0,
        "building_coverage": 0.0,
        "avg_building_height": 0.0,
        "road_coverage": 0.0,
        "tree_count": 0,
        "tree_canopy_fraction": 0.0,
        "sky_view_factor": 1.0,
    }


# ── Helpers ───────────────────────────────────────────────────────────────────

def _element_to_polygon(
    el: dict,
    nodes: dict[int, tuple[float, float]],
    all_elements: list[dict],
) -> Polygon | MultiPolygon | None:
    """Convert an OSM way/relation element to a Shapely polygon."""
    if el["type"] == "way":
        nds = el.get("nodes", [])
        coords = [nodes[n] for n in nds if n in nodes]
        if len(coords) >= 4:
            try:
                poly = Polygon(coords)
                if poly.is_valid:
                    return poly
                return poly.buffer(0)
            except Exception:
                return None

    elif el["type"] == "relation":
        outer_rings = []
        for member in el.get("members", []):
            if member.get("role") != "outer":
                continue
            ref = member.get("ref")
            # Find referenced way
            for sub in all_elements:
                if sub["type"] == "way" and sub["id"] == ref:
                    nds = sub.get("nodes", [])
                    coords = [nodes[n] for n in nds if n in nodes]
                    if len(coords) >= 4:
                        outer_rings.append(coords)
                    break
        if outer_rings:
            polys = []
            for ring in outer_rings:
                try:
                    p = Polygon(ring)
                    if p.is_valid:
                        polys.append(p)
                    else:
                        polys.append(p.buffer(0))
                except Exception:
                    continue
            if polys:
                return unary_union(polys)

    return None


def _road_width(highway_type: str) -> float:
    """Approximate road width in meters by highway type."""
    widths = {
        "motorway": 12.0, "trunk": 10.0, "primary": 8.0,
        "secondary": 7.0, "tertiary": 6.0, "residential": 5.5,
        "service": 3.5, "living_street": 4.0, "pedestrian": 3.0,
        "footway": 2.0, "cycleway": 2.0, "path": 1.5, "track": 3.0,
    }
    return widths.get(highway_type, 5.0)


def _parse_int(val: Any, default: int) -> int:
    if val is None:
        return default
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


def _parse_float(val: Any, default: float) -> float:
    if val is None:
        return default
    try:
        return float(str(val).replace(",", ".").rstrip("m "))
    except (ValueError, TypeError):
        return default
