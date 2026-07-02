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
_infra_cache: dict[str, tuple[float, dict]] = {}                # bbox → (ts, infra dict)
_CACHE_TTL = 600  # 10 min – long enough for a full batch run

# OSM power way tags treated as line segments (weight 0.5 per cell intersection)
_POWER_LINE_TAGS = frozenset({"line", "cable", "minor_line", "busbar"})
_WATER_INFRA_TAGS = frozenset({"water_works", "wastewater_plant", "water_tower"})
_COMM_MAN_MADE_TAGS = frozenset({"mast", "communications_tower"})
_TRANSPORT_RAILWAY_TAGS = frozenset({"station", "halt"})
_HEALTHCARE_HOSPITAL_AMENITY = frozenset({"hospital"})
_HEALTHCARE_DOCTOR_AMENITY = frozenset({"clinic", "doctors"})
_HEALTHCARE_PHARMACY_AMENITY = frozenset({"pharmacy"})
_HEALTHCARE_HOSPITAL_HC = frozenset({"hospital"})
_HEALTHCARE_DOCTOR_HC = frozenset({"clinic", "doctor", "centre", "health_centre"})
_HEALTHCARE_PHARMACY_HC = frozenset({"pharmacy"})

HEALTHCARE_ROAD_FACTOR = 1.3
HEALTHCARE_MAX_DIST_M = 20_000.0

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
    "forestry": 0.02,
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
    "forestry": 0.12,
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
    "forest": 0.02,
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
    "forest": 0.12,
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


def prefetch_osm_data(
    grid_cells: list[dict],
    include_buildings: bool = False,
    include_infrastructure: bool = False,
):
    """Pre-fetch and cache OSM data for the given grid cells.

    Call this once before running multiple assessors on the same grid
    to avoid repeated Overpass API requests and 429 rate-limits.
    """
    log.info(
        "prefetch_osm_data: landuse (buildings=%s, infra=%s) for %d cells",
        include_buildings, include_infrastructure, len(grid_cells),
    )
    fetch_landuse(grid_cells)
    if include_buildings:
        fetch_buildings_and_roads(grid_cells)
    if include_infrastructure:
        fetch_infrastructure(grid_cells)


def clear_osm_cache():
    """Clear all cached OSM data."""
    with _cache_lock:
        _landuse_cache.clear()
        _buildings_cache.clear()
        _water_cache.clear()
        _infra_cache.clear()
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


def build_water_spatial_index(
    water_features: list[dict],
) -> tuple[Any, list[Any]] | None:
    """STRtree über Gewässer-Geometrien für schnelle Nächst-Nachbarsuche."""
    if not water_features:
        return None
    from shapely.strtree import STRtree

    geoms = [f["geometry"] for f in water_features]
    return STRtree(geoms), geoms


def compute_water_distance_m(
    cell_geom: Any,
    water_features: list[dict],
    cell_size_m: float,
    water_index: tuple[Any, list[Any]] | None = None,
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

    if water_index is not None:
        tree, geoms = water_index
        nearest_i = int(tree.nearest(cell_geom))
        feat_utm = shp_transform(to_utm, geoms[nearest_i])
        return float(cell_utm.distance(feat_utm))

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


def _healthcare_category(tags: dict) -> str | None:
    """Classify OSM healthcare feature as hospital, doctor, or pharmacy."""
    amenity = tags.get("amenity", "")
    hc = tags.get("healthcare", "")
    if amenity in _HEALTHCARE_PHARMACY_AMENITY or hc in _HEALTHCARE_PHARMACY_HC:
        return "pharmacy"
    if (
        amenity in _HEALTHCARE_HOSPITAL_AMENITY
        or hc in _HEALTHCARE_HOSPITAL_HC
        or tags.get("building") == "hospital"
    ):
        return "hospital"
    if amenity in _HEALTHCARE_DOCTOR_AMENITY or hc in _HEALTHCARE_DOCTOR_HC:
        return "doctor"
    return None


def build_healthcare_spatial_index(geoms: list) -> tuple[Any, list] | None:
    """STRtree over healthcare geometries for fast nearest-neighbour lookup."""
    if not geoms:
        return None
    from shapely.strtree import STRtree

    return STRtree(geoms), geoms


def build_healthcare_indexes(infra: dict) -> dict[str, tuple[Any, list] | None]:
    return {
        "hospital": build_healthcare_spatial_index(infra.get("healthcare_hospital", [])),
        "doctor": build_healthcare_spatial_index(infra.get("healthcare_doctor", [])),
        "pharmacy": build_healthcare_spatial_index(infra.get("healthcare_pharmacy", [])),
    }


def compute_nearest_distance_m(
    cell_geom: Any,
    geoms: list,
    spatial_index: tuple[Any, list] | None,
    fallback_m: float = HEALTHCARE_MAX_DIST_M,
) -> float:
    """Shortest straight-line distance (m) from cell to nearest geometry, × road factor."""
    if not geoms:
        return fallback_m

    import pyproj
    from shapely.ops import transform as shp_transform

    minx, miny, maxx, maxy = cell_geom.bounds
    lat = (miny + maxy) / 2.0
    utm_zone = int((cell_geom.centroid.x + 180) / 6) + 1
    utm_epsg = 32600 + utm_zone if lat >= 0 else 32700 + utm_zone

    to_utm = pyproj.Transformer.from_crs("EPSG:4326", f"EPSG:{utm_epsg}", always_xy=True).transform
    cell_utm = shp_transform(to_utm, cell_geom)

    if spatial_index is not None:
        tree, indexed_geoms = spatial_index
        nearest_i = int(tree.nearest(cell_geom))
        feat_utm = shp_transform(to_utm, indexed_geoms[nearest_i])
        raw_m = float(cell_utm.distance(feat_utm))
    else:
        raw_m = float("inf")
        for geom in geoms:
            feat_utm = shp_transform(to_utm, geom)
            raw_m = min(raw_m, float(cell_utm.distance(feat_utm)))

    if raw_m >= float("inf"):
        return fallback_m

    return min(fallback_m, raw_m * HEALTHCARE_ROAD_FACTOR)


def healthcare_proximity_score(dist_m: float, max_m: float = HEALTHCARE_MAX_DIST_M) -> float:
    """0..1 proximity score (1 = at facility, 0 = at or beyond max_m)."""
    d = min(max(0.0, dist_m), max_m)
    return max(0.0, 1.0 - d / max_m)


def healthcare_access_from_distances(dist_h: float, dist_d: float, dist_p: float) -> dict:
    """Weighted access score from effective distances (m, incl. road factor)."""
    prox_h = healthcare_proximity_score(dist_h)
    prox_d = healthcare_proximity_score(dist_d)
    prox_p = healthcare_proximity_score(dist_p)
    w_h = 0.50 * prox_h
    w_d = 0.35 * prox_d
    w_p = 0.15 * prox_p
    score = w_h + w_d + w_p
    return {
        "dist_hospital_m": round(dist_h, 1),
        "dist_doctor_m": round(dist_d, 1),
        "dist_pharmacy_m": round(dist_p, 1),
        "healthcare_weight_hospital": round(w_h, 4),
        "healthcare_weight_doctor": round(w_d, 4),
        "healthcare_weight_pharmacy": round(w_p, 4),
        "healthcare_access_score": round(score, 4),
    }


def compute_cell_healthcare_access(
    cell_geom: Any,
    infra: dict,
    healthcare_indexes: dict[str, tuple[Any, list] | None],
) -> dict:
    """Per-cell distances and composite healthcare access score."""
    dist_h = compute_nearest_distance_m(
        cell_geom, infra.get("healthcare_hospital", []), healthcare_indexes.get("hospital"),
    )
    dist_d = compute_nearest_distance_m(
        cell_geom, infra.get("healthcare_doctor", []), healthcare_indexes.get("doctor"),
    )
    dist_p = compute_nearest_distance_m(
        cell_geom, infra.get("healthcare_pharmacy", []), healthcare_indexes.get("pharmacy"),
    )
    return healthcare_access_from_distances(dist_h, dist_d, dist_p)


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
        elif nat in ("wood", "forest", "grassland", "scrub", "heath", "wetland"):
            green_area += frac
        elif lu in ("forest", "forestry", "meadow", "grass", "orchard", "vineyard",
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
    glacier_area = 0.0
    farmland_area = 0.0
    for label, area in landuse_areas.items():
        if label in ("forest", "wood", "forestry"):
            forest_area += area
        elif label in ("farmland", "orchard", "vineyard"):
            farmland_area += area

    # Gletscher separat (natural=glacier wird nicht in LANDUSE/NATURAL-Tabellen verarbeitet)
    for feat in landuse_features:
        if feat.get("natural") != "glacier":
            continue
        feat_geom = feat["geometry"]
        if not cell_geom.intersects(feat_geom):
            continue
        intersection = cell_geom.intersection(feat_geom)
        if intersection.area > 0 and cell_area > 0:
            glacier_area += intersection.area / cell_area

    return {
        "impervious_fraction": round(min(max(imp_final, 0.0), 1.0), 4),
        "albedo": round(alb_final, 4),
        "green_fraction": round(min(green_area, 1.0), 4),
        "water_fraction": round(min(water_area, 1.0), 4),
        "forest_fraction": round(min(forest_area, 1.0), 4),
        "glacier_fraction": round(min(glacier_area, 1.0), 4),
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


# ── Critical infrastructure (power, water/wastewater, communication) ───────────

def _empty_infra_features() -> dict:
    return {
        "energy_points": [],
        "energy_lines": [],
        "energy_areas": [],
        "water_points": [],
        "water_areas": [],
        "comm_points": [],
        "transport_points": [],
        "healthcare_hospital": [],
        "healthcare_doctor": [],
        "healthcare_pharmacy": [],
    }


def _add_healthcare_geometry(
    result: dict,
    tags: dict,
    geom: Any,
    seen: set,
    key: int | tuple[str, int],
) -> None:
    cat = _healthcare_category(tags)
    if cat is None or key in seen:
        return
    seen.add(key)
    result[f"healthcare_{cat}"].append(geom)


def fetch_infrastructure(grid_cells: list[dict]) -> dict:
    """Fetch OSM energy, water/wastewater, communication and healthcare infrastructure.

    Returns dict with keys: energy_points, energy_lines, energy_areas,
    water_points, water_areas, comm_points, healthcare_hospital,
    healthcare_doctor, healthcare_pharmacy.
    """
    bbox = _bbox_from_cells(grid_cells)

    with _cache_lock:
        cached = _infra_cache.get(bbox)
        if cached:
            ts, result = cached
            if _time.time() - ts < _CACHE_TTL:
                log.info("fetch_infrastructure: cache HIT for bbox=%s", bbox[:30])
                return result
            del _infra_cache[bbox]

    log.info("fetch_infrastructure: cache MISS — querying Overpass")

    query = f"""
    (
      node["power"]({bbox});
      way["power"]({bbox});
      node["man_made"~"water_works|wastewater_plant|water_tower"]({bbox});
      way["man_made"~"water_works|wastewater_plant"]({bbox});
      node["tower"="communication"]({bbox});
      node["man_made"~"mast|communications_tower"]({bbox});
      node["communication"]({bbox});
      node["railway"~"^(station|halt)$"]({bbox});
      node["public_transport"="station"]({bbox});
      node["amenity"="bus_station"]({bbox});
      node["amenity"~"hospital|clinic|doctors|pharmacy"]({bbox});
      way["amenity"~"hospital|clinic|doctors|pharmacy"]({bbox});
      node["healthcare"~"hospital|clinic|doctor|pharmacy|centre"]({bbox});
      way["healthcare"~"hospital|clinic|doctor|pharmacy|centre"]({bbox});
      way["building"="hospital"]({bbox});
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

    result = _empty_infra_features()
    comm_node_ids: set[int] = set()
    water_node_ids: set[int] = set()
    transport_node_ids: set[int] = set()
    healthcare_ids: set[int | tuple[str, int]] = set()

    from shapely.geometry import Point

    for el in elements:
        tags = el.get("tags", {})
        el_type = el.get("type")
        el_id = el.get("id")

        if el_type == "node" and "power" in tags:
            if el["id"] in nodes:
                lon, lat = nodes[el["id"]]
                result["energy_points"].append({"lon": lon, "lat": lat})

        elif el_type == "way" and "power" in tags:
            power_tag = tags.get("power", "")
            if power_tag in _POWER_LINE_TAGS:
                nds = el.get("nodes", [])
                coords = [nodes[n] for n in nds if n in nodes]
                if len(coords) >= 2:
                    result["energy_lines"].append({"geometry": LineString(coords)})
            else:
                geom = _element_to_polygon(el, nodes, elements)
                if geom is not None:
                    result["energy_areas"].append({"geometry": geom})
                else:
                    nds = el.get("nodes", [])
                    coords = [nodes[n] for n in nds if n in nodes]
                    if len(coords) >= 2:
                        result["energy_lines"].append({"geometry": LineString(coords)})

        elif el_type == "node":
            if el["id"] not in nodes:
                continue
            mm = tags.get("man_made", "")
            if mm in _WATER_INFRA_TAGS and el["id"] not in water_node_ids:
                water_node_ids.add(el["id"])
                lon, lat = nodes[el["id"]]
                result["water_points"].append({"lon": lon, "lat": lat})
            is_comm = (
                tags.get("tower") == "communication"
                or mm in _COMM_MAN_MADE_TAGS
                or "communication" in tags
            )
            if is_comm and el["id"] not in comm_node_ids:
                comm_node_ids.add(el["id"])
                lon, lat = nodes[el["id"]]
                result["comm_points"].append({"lon": lon, "lat": lat})
            is_transport = (
                tags.get("railway") in _TRANSPORT_RAILWAY_TAGS
                or tags.get("public_transport") == "station"
                or tags.get("amenity") == "bus_station"
            )
            if is_transport and el["id"] not in transport_node_ids:
                transport_node_ids.add(el["id"])
                lon, lat = nodes[el["id"]]
                result["transport_points"].append({"lon": lon, "lat": lat})
            _add_healthcare_geometry(
                result, tags, Point(nodes[el["id"]]), healthcare_ids, el_id,
            )

        elif el_type == "way":
            if tags.get("man_made") in _WATER_INFRA_TAGS:
                geom = _element_to_polygon(el, nodes, elements)
                if geom is not None:
                    result["water_areas"].append({"geometry": geom})
            cat = _healthcare_category(tags)
            if cat is not None and ("way", el_id) not in healthcare_ids:
                geom = _element_to_polygon(el, nodes, elements)
                if geom is not None:
                    _add_healthcare_geometry(result, tags, geom, healthcare_ids, ("way", el_id))
                else:
                    nds = el.get("nodes", [])
                    coords = [nodes[n] for n in nds if n in nodes]
                    if coords:
                        lon = sum(c[0] for c in coords) / len(coords)
                        lat = sum(c[1] for c in coords) / len(coords)
                        _add_healthcare_geometry(
                            result, tags, Point(lon, lat), healthcare_ids, ("way", el_id),
                        )

    log.info(
        "Fetched infrastructure from OSM: %d energy pts, %d lines, %d areas, "
        "%d water pts, %d water areas, %d comm pts, %d transport pts, "
        "%d hospital, %d doctor, %d pharmacy (%.2f MB)",
        len(result["energy_points"]), len(result["energy_lines"]),
        len(result["energy_areas"]), len(result["water_points"]),
        len(result["water_areas"]), len(result["comm_points"]),
        len(result["transport_points"]),
        len(result["healthcare_hospital"]), len(result["healthcare_doctor"]),
        len(result["healthcare_pharmacy"]),
        response_bytes / 1_048_576,
    )

    with _cache_lock:
        _infra_cache[bbox] = (_time.time(), result)

    return result


def compute_cell_infrastructure(cell_geom: Any, infra: dict) -> dict:
    """Count infrastructure features intersecting a single grid cell."""
    from shapely.geometry import Point

    if cell_geom is None or cell_geom.is_empty:
        return _empty_infra_metrics()

    energy = 0.0
    for pt in infra.get("energy_points", []):
        if cell_geom.contains(Point(pt["lon"], pt["lat"])):
            energy += 1.0
    for line in infra.get("energy_lines", []):
        if cell_geom.intersects(line["geometry"]):
            energy += 0.5
    for area in infra.get("energy_areas", []):
        if cell_geom.intersects(area["geometry"]):
            energy += 1.0

    water = 0
    for pt in infra.get("water_points", []):
        if cell_geom.contains(Point(pt["lon"], pt["lat"])):
            water += 1
    for area in infra.get("water_areas", []):
        if cell_geom.intersects(area["geometry"]):
            water += 1

    comm = 0
    for pt in infra.get("comm_points", []):
        if cell_geom.contains(Point(pt["lon"], pt["lat"])):
            comm += 1

    transport = 0
    for pt in infra.get("transport_points", []):
        if cell_geom.contains(Point(pt["lon"], pt["lat"])):
            transport += 1

    return {
        "energy_infra_count": round(energy, 2),
        "water_wastewater_count": water,
        "communication_count": comm,
        "transport_hub_count": transport,
    }


def _empty_infra_metrics() -> dict:
    return {
        "energy_infra_count": 0.0,
        "water_wastewater_count": 0,
        "communication_count": 0,
        "transport_hub_count": 0,
    }


# ── Helpers ───────────────────────────────────────────────────────────────────

def _ways_by_id(all_elements: list[dict]) -> dict[int, list[int]]:
    return {
        el["id"]: el.get("nodes", [])
        for el in all_elements
        if el.get("type") == "way"
    }


def _group_connected_ways(
    way_ids: list[int],
    ways_by_id: dict[int, list[int]],
) -> list[list[int]]:
    """Gruppiert Way-IDs, die Endpunkte teilen (für Multipolygon-Ringe)."""
    if not way_ids:
        return []
    id_set = set(way_ids)
    endpoint_map: dict[int, list[int]] = {}
    for wid in way_ids:
        nds = ways_by_id.get(wid, [])
        if len(nds) < 2:
            continue
        for n in (nds[0], nds[-1]):
            endpoint_map.setdefault(n, []).append(wid)

    visited: set[int] = set()
    groups: list[list[int]] = []
    for wid in way_ids:
        if wid in visited:
            continue
        stack = [wid]
        group: list[int] = []
        while stack:
            w = stack.pop()
            if w in visited:
                continue
            visited.add(w)
            group.append(w)
            nds = ways_by_id.get(w, [])
            if len(nds) >= 2:
                for n in (nds[0], nds[-1]):
                    for nb in endpoint_map.get(n, []):
                        if nb in id_set and nb not in visited:
                            stack.append(nb)
        if group:
            groups.append(group)
    return groups


def _stitch_ring_from_way_ids(
    way_ids: list[int],
    ways_by_id: dict[int, list[int]],
    nodes: dict[int, tuple[float, float]],
) -> list[tuple[float, float]] | None:
    """Stitcht OSM-Way-Segmente zu einem geschlossenen Koordinatenring."""
    segments: list[list[int]] = []
    for wid in way_ids:
        nds = ways_by_id.get(wid)
        if nds and len(nds) >= 2:
            segments.append(list(nds))
    if not segments:
        return None

    ring_nds = list(segments.pop(0))
    guard = len(segments) + 20
    while segments and guard > 0:
        guard -= 1
        end = ring_nds[-1]
        start = ring_nds[0]
        merged = False
        for i, seg in enumerate(segments):
            if seg[0] == end:
                ring_nds.extend(seg[1:])
                segments.pop(i)
                merged = True
                break
            if seg[-1] == end:
                ring_nds.extend(reversed(seg[:-1]))
                segments.pop(i)
                merged = True
                break
            if seg[-1] == start:
                ring_nds = seg + ring_nds[1:]
                segments.pop(i)
                merged = True
                break
            if seg[0] == start:
                ring_nds = list(reversed(seg)) + ring_nds[1:]
                segments.pop(i)
                merged = True
                break
        if not merged:
            break

    if ring_nds[0] != ring_nds[-1]:
        if len(ring_nds) >= 3:
            ring_nds.append(ring_nds[0])
        else:
            return None

    coords = [nodes[n] for n in ring_nds if n in nodes]
    return coords if len(coords) >= 4 else None


def _ring_to_polygon(coords: list[tuple[float, float]]) -> Polygon | None:
    try:
        poly = Polygon(coords)
        if poly.is_valid:
            return poly
        fixed = poly.buffer(0)
        return fixed if not fixed.is_empty else None
    except Exception:
        return None


def _relation_to_multipolygon(
    el: dict,
    nodes: dict[int, tuple[float, float]],
    all_elements: list[dict],
) -> Polygon | MultiPolygon | None:
    """Multipolygon-Relation: äußere Ringe stitchen, innere Löcher zuordnen."""
    ways_by_id = _ways_by_id(all_elements)
    outer_refs: list[int] = []
    inner_refs: list[int] = []
    for member in el.get("members", []):
        if member.get("type") != "way":
            continue
        ref = member.get("ref")
        if ref is None:
            continue
        role = member.get("role", "outer")
        if role == "inner":
            inner_refs.append(ref)
        else:
            outer_refs.append(ref)

    hole_rings: list[list[tuple[float, float]]] = []
    for ig in _group_connected_ways(inner_refs, ways_by_id):
        ring = _stitch_ring_from_way_ids(ig, ways_by_id, nodes)
        if ring:
            hole_rings.append(ring)

    polys: list[Polygon] = []
    for og in _group_connected_ways(outer_refs, ways_by_id):
        ring = _stitch_ring_from_way_ids(og, ways_by_id, nodes)
        if not ring:
            continue
        holes_here: list[list[tuple[float, float]]] = []
        if hole_rings:
            try:
                outer_tmp = Polygon(ring)
                for hole in hole_rings:
                    hp = Polygon(hole)
                    if outer_tmp.contains(hp.centroid):
                        holes_here.append(hole)
            except Exception:
                pass
        try:
            poly = Polygon(ring, holes_here) if holes_here else Polygon(ring)
            if poly.is_valid and not poly.is_empty:
                polys.append(poly)
            else:
                fixed = poly.buffer(0)
                if not fixed.is_empty:
                    polys.append(fixed)
        except Exception:
            pr = _ring_to_polygon(ring)
            if pr is not None:
                polys.append(pr)

    if not polys:
        return None
    if len(polys) == 1:
        return polys[0]
    return unary_union(polys)


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
            return _ring_to_polygon(coords)
        if len(coords) >= 3 and coords[0] == coords[-1]:
            return _ring_to_polygon(coords)
        return None

    if el["type"] == "relation":
        return _relation_to_multipolygon(el, nodes, all_elements)

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
