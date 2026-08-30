"""Fetch and process OSM data for heat assessment levels 2 and 3.

Level 2: Land-use polygons per grid cell (residential, commercial, green, water, …).
Level 3: Individual building footprints, road surfaces, tree canopy.
"""

import gzip
import hashlib
import json
import logging
import os
import threading
import time as _time
from typing import Any

import httpx
from shapely.geometry import shape, Point, Polygon, MultiPolygon, LineString, mapping
from shapely.ops import unary_union

from app.config import settings
from app.data import infra_assets

log = logging.getLogger(__name__)

OVERPASS_TIMEOUT = 120

# ── Thread-safe OSM data cache ────────────────────────────────────────────────
# Keyed by bbox string. Each entry is (timestamp, data).
# Cache is shared across assessors so identical Overpass queries are made once.
#
# RAM-Budget: je Cache-Art wird nur EIN Eintrag (die aktuelle bbox) gehalten —
# der einzige Zweck ist das Teilen innerhalb EINES Laufs (4 parallele Fetcher,
# mehrere Assessoren). Persistenz über Läufe/Neustarts hinweg übernimmt der
# Overpass-Disk-Cache (_overpass_query_cached, data/osm_cache/): Roh-JSON auf
# Platte statt Shapely-Geometrien im Speicher.

_cache_lock = threading.Lock()
_landuse_cache: dict[str, tuple[float, list[dict], int]] = {}  # bbox → (ts, features, bytes)
_buildings_cache: dict[str, tuple[float, dict]] = {}            # bbox → (ts, result_dict)
_water_cache: dict[str, tuple[float, list[dict]]] = {}          # bbox → (ts, water features)
_infra_cache: dict[str, tuple[float, dict]] = {}                # bbox → (ts, infra dict)
_CACHE_TTL = 600  # 10 min – long enough for a full batch run

# OSM power way tags treated as line geometries (class weight per cell
# intersection, see app/data/infra_assets.py)
_POWER_LINE_TAGS = frozenset({"line", "cable", "minor_line", "busbar"})
# Flugbetriebsflächen, die als versiegelte Fläche (paved_areas) zählen.
_AEROWAY_PAVED = frozenset({"apron", "runway", "taxiway", "helipad"})
# Wasser-/Kommunikations-/Verkehrs-Klassifikation: app/data/infra_assets.py
# Notfall-/Katastrophenschutz-Infrastruktur (Frühwarnung/Notfallmanagement-Proxy)
_EMERGENCY_TAGS = frozenset(
    {"ambulance_station", "water_rescue_station", "disaster_response", "lifeguard_base"}
)
# Hochwasserschutz-Bauwerke (Deichzustand-Proxy)
_DYKE_MAN_MADE_TAGS = frozenset({"dyke", "embankment"})
_HEALTHCARE_HOSPITAL_AMENITY = frozenset({"hospital"})
_HEALTHCARE_DOCTOR_AMENITY = frozenset({"clinic", "doctors"})
_HEALTHCARE_PHARMACY_AMENITY = frozenset({"pharmacy"})
_HEALTHCARE_HOSPITAL_HC = frozenset({"hospital"})
_HEALTHCARE_DOCTOR_HC = frozenset({"clinic", "doctor", "centre", "health_centre"})
_HEALTHCARE_PHARMACY_HC = frozenset({"pharmacy"})

HEALTHCARE_ROAD_FACTOR = 1.3
HEALTHCARE_MAX_DIST_M = 20_000.0

# Notfall-Erreichbarkeit: jenseits ~10 km gilt eine Zelle als schlecht versorgt.
EMERGENCY_MAX_DIST_M = 10_000.0
# Deich-Relevanz nur in unmittelbarer Nähe (Hochwasserschutz wirkt lokal).
DYKE_MAX_DIST_M = 1_000.0

# Kleinstgewässer (Entwässerungsgräben) dürfen die Gewässernähe NICHT wie ein echtes
# Gewässer auf 1 pinnen. Ackerland ist von ``waterway=ditch``/``drain`` durchzogen —
# ein einzelner querender Graben ist hydrologisch belanglos, ein dichtes Grabennetz
# nicht. Daher: sehr schwacher, über die Grabendichte der Zelle skalierter Beitrag.
_MINOR_WATERWAYS = frozenset({"ditch", "drain"})
# Ein die Zelle voll querender Graben (Dichte ≈ 1) liefert nur DITCH_DENSITY_WEIGHT;
# eine gestreifte Ecke entsprechend weniger, ein dichtes Grabennetz sättigt bei _CAP.
DITCH_DENSITY_WEIGHT = 0.05
DITCH_PROX_CAP = 0.2

# ── Flächenkomposition: Schichtmodell mit 100%-Budget ────────────────────────
#
# Jede Zelle wird vollständig auf sechs Kategorien aufgeteilt, deren Summe
# konstruktionsbedingt exakt 100 % ergibt:
#   V  = versiegelt (Gebäude, Asphalt, Pflaster …)
#   G  = grün (Wiese, Park, Garten, Grasland …)
#   W  = Wald (Baumbestand)
#   A  = Acker (landwirtschaftliche Nutzfläche)
#   Wa = Wasser (Gewässerflächen)
#   O  = offen/sonstiges (unversiegelter Boden ohne Vegetation, Fels, Sand …)
#
# Jede OSM-Tag-Zeile ist eine Komposition, die selbst auf 100 summiert (per
# Unit-Test erzwungen). Überlagerungen werden über eine feste Schichtreihenfolge
# (``precedence``) mit geometrischem Abzug aufgelöst — das konkretere Objekt
# „oben" sticht das großflächigere „unten" (siehe compute_cell_composition und
# docs/REVIEW_BERECHNUNGSLOGIK.md §IMPERVIOUS_FRACTION).
#
# Die Zeilen der urbanen Landnutzung (residential, industrial …) sind bewusst als
# RESIDUAL definiert: sie beschreiben die Fläche, die NACH Abzug der gemappten
# Gebäude und Straßen übrig bleibt (Einfahrten, Höfe, Gärten). Anker: residential
# 30 % V (Rest) + typ. Gebäudedeckung ~25 % + Straßen ~7 % ≈ 55 % — deckungsgleich
# mit der früheren Pauschale 0,55.

_COMP_CATS = ("V", "G", "W", "A", "Wa", "O")

# Meter→Grad (grobe Näherung, wie in compute_cell_buildings) für Straßenpuffer.
DEGREE_PER_METER = 1.0 / 111_320.0

# Precedence-Stufen (kleiner = höhere Schicht, wird zuerst zugewiesen).
_PREC_BUILDING = 10
_PREC_TRAFFIC = 20
_PREC_WATER = 30
_PREC_SPECIFIC = 40   # kleinflächige/spezifische Nutzung sticht großflächige
_PREC_BROAD = 50

BUILDING_ROW: dict[str, float] = {"V": 100}
FALLBACK_ROW: dict[str, float] = {"V": 5, "O": 95}
FALLBACK_ALBEDO = 0.23
BUILDING_ALBEDO = 0.15
PAVED_ALBEDO = 0.13
WATER_ALBEDO = 0.06
LEISURE_ALBEDO = 0.22

# surface → Versiegelungsanteil in % (angelehnt an Abflussbeiwert-Spannen
# DWA-A 138 / DIN 1986-100). Ein gepflasterter Platz ist eben NICHT 100 %
# versiegelt (Fugen versickern), aber auch nicht 0 %.
SURFACE_SEALING: dict[str, int] = {
    "asphalt": 95, "concrete": 95, "metal": 95, "paved": 85,
    "concrete:plates": 90, "concrete_plates": 90, "concrete:lanes": 80,
    "paving_stones": 75, "sett": 65, "cobblestone": 60, "bricks": 80,
    "unhewn_cobblestone": 55, "compacted": 50, "wood": 50,
    "fine_gravel": 45, "gravel": 35, "pebblestone": 35, "rock": 40,
    "unpaved": 30, "grass_paver": 25, "grass_pavers": 25,
    "ground": 10, "dirt": 10, "earth": 10, "mud": 10, "clay": 15,
    "grass": 5, "sand": 5, "woodchips": 5, "snow": 0, "ice": 0,
}
# surface-Werte, deren unversiegelter Rest als Grün (nicht „offen") zählt.
_GRASSY_SURFACES = frozenset({"grass", "grass_paver", "grass_pavers"})

# Straßen-Grundzeilen je highway-Typ (vor surface-Override). Nur V/O.
ROAD_COMPOSITION: dict[str, dict[str, float]] = {
    "motorway": {"V": 95, "O": 5}, "motorway_link": {"V": 95, "O": 5},
    "trunk": {"V": 95, "O": 5}, "trunk_link": {"V": 95, "O": 5},
    "primary": {"V": 95, "O": 5}, "primary_link": {"V": 95, "O": 5},
    "secondary": {"V": 95, "O": 5}, "secondary_link": {"V": 95, "O": 5},
    "tertiary": {"V": 95, "O": 5}, "tertiary_link": {"V": 95, "O": 5},
    "residential": {"V": 95, "O": 5}, "unclassified": {"V": 95, "O": 5},
    "service": {"V": 95, "O": 5}, "living_street": {"V": 90, "O": 10},
    "cycleway": {"V": 85, "O": 15}, "pedestrian": {"V": 80, "O": 20},
    "footway": {"V": 70, "O": 30}, "steps": {"V": 70, "O": 30},
    "bridleway": {"V": 10, "O": 90}, "path": {"V": 15, "O": 85},
    "track": {"V": 20, "O": 80},  # ohne tracktype; mit tracktype überschrieben
}
_ROAD_DEFAULT_ROW = {"V": 85, "O": 15}  # unbekannter highway-Typ (meist befestigt)
_TRACKTYPE_SEALING = {"grade1": 80, "grade2": 50, "grade3": 30, "grade4": 15, "grade5": 15}

# Flächenhafte Verkehrs-/Platzobjekte (paved_areas aus fetch_buildings_and_roads).
PAVED_COMPOSITION: dict[str, dict[str, float]] = {
    "square": {"V": 80, "O": 20},                 # highway=pedestrian/footway area, place=square
    "parking": {"V": 85, "G": 5, "O": 10},
    "aeroway": {"V": 95, "O": 5},
}

# Großflächige/spezifische Landnutzung. RESIDUAL-Zeilen (s. o.) für urbane Klassen.
LANDUSE_COMPOSITION: dict[str, dict[str, float]] = {
    "garages": {"V": 90, "O": 10},
    "depot": {"V": 80, "O": 20},
    "greenhouse_horticulture": {"V": 70, "G": 10, "A": 15, "O": 5},
    "industrial": {"V": 65, "G": 15, "O": 20},
    "port": {"V": 70, "G": 5, "Wa": 15, "O": 10},
    "commercial": {"V": 55, "G": 25, "O": 20},
    "retail": {"V": 55, "G": 25, "O": 20},
    "railway": {"V": 50, "G": 20, "O": 30},
    "construction": {"V": 50, "G": 10, "O": 40},
    "brownfield": {"V": 40, "G": 30, "O": 30},
    "landfill": {"V": 30, "G": 30, "O": 40},
    "religious": {"V": 35, "G": 45, "O": 20},
    "institutional": {"V": 35, "G": 45, "O": 20},
    "education": {"V": 35, "G": 45, "O": 20},
    "farmyard": {"V": 35, "G": 25, "A": 20, "O": 20},
    "residential": {"V": 30, "G": 55, "O": 15},
    "recreation_ground": {"V": 20, "G": 70, "O": 10},
    "quarry": {"V": 20, "G": 10, "O": 70},
    "cemetery": {"V": 20, "G": 70, "O": 10},
    "allotments": {"V": 15, "G": 80, "O": 5},
    "military": {"V": 10, "G": 40, "W": 30, "O": 20},
    "plant_nursery": {"V": 5, "G": 90, "O": 5},
    "orchard": {"V": 3, "G": 25, "A": 70, "O": 2},
    "vineyard": {"V": 3, "G": 25, "A": 70, "O": 2},
    "farmland": {"V": 2, "G": 3, "A": 95},
    "meadow": {"V": 2, "G": 95, "O": 3},
    "grass": {"V": 2, "G": 95, "O": 3},
    "village_green": {"V": 2, "G": 95, "O": 3},
    "greenfield": {"V": 2, "G": 95, "O": 3},
    "flowerbed": {"V": 2, "G": 95, "O": 3},
    "forest": {"V": 1, "G": 4, "W": 95},
    "forestry": {"V": 1, "G": 4, "W": 95},
    "meadow_orchard": {"V": 2, "G": 60, "A": 36, "O": 2},
}
# Landnutzungs-Tags, die (weil klein-/spezifisch) großflächige überstechen sollen.
_SPECIFIC_LANDUSE = frozenset({
    "garages", "depot", "greenhouse_horticulture", "cemetery", "allotments",
    "landfill", "quarry", "military", "religious", "institutional", "education",
    "plant_nursery", "orchard", "vineyard", "flowerbed", "brownfield",
    "construction", "port", "recreation_ground",
})

NATURAL_COMPOSITION: dict[str, dict[str, float]] = {
    "wood": {"V": 1, "G": 4, "W": 95},
    "forest": {"V": 1, "G": 4, "W": 95},
    "tree_row": {"V": 1, "G": 9, "W": 90},
    "scrub": {"V": 2, "G": 93, "O": 5},
    "heath": {"V": 2, "G": 93, "O": 5},
    "grassland": {"V": 2, "G": 95, "O": 3},
    "fell": {"V": 1, "G": 70, "O": 29},
    "grass": {"V": 2, "G": 95, "O": 3},
    "wetland": {"G": 70, "Wa": 20, "O": 10},
    "water": {"Wa": 100},
    "bare_rock": {"V": 10, "O": 90},
    "scree": {"V": 5, "O": 95},
    "shingle": {"V": 3, "O": 97},
    "sand": {"V": 2, "O": 98},
    "beach": {"V": 2, "O": 98},
    "mud": {"O": 100},
    "glacier": {"O": 100},
}

LEISURE_COMPOSITION: dict[str, dict[str, float]] = {
    "track": {"V": 65, "G": 25, "O": 10},          # Laufbahn
    "stadium": {"V": 60, "G": 30, "O": 10},
    "sports_centre": {"V": 50, "G": 40, "O": 10},
    "pitch": {"V": 40, "G": 50, "O": 10},          # surface-moduliert (Rasen vs. Asche/Kunst)
    "playground": {"V": 25, "G": 60, "O": 15},
    "park": {"V": 8, "G": 90, "O": 2},
    "garden": {"V": 5, "G": 90, "O": 5},
    "dog_park": {"V": 5, "G": 90, "O": 5},
    "recreation_ground": {"V": 20, "G": 70, "O": 10},
    "golf_course": {"V": 3, "G": 95, "Wa": 2},
    "nature_reserve": {"V": 1, "G": 60, "W": 30, "O": 9},
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


def _overpass_query_cached(kind: str, bbox: str, query_body: str) -> dict:
    """Overpass-Abfrage mit Platten-Cache für das Roh-JSON.

    Datei je (Abfrageart, bbox) unter ``OSM_CACHE_DIR`` (gzip, TTL
    ``OSM_CACHE_TTL_S``): Wiederholungsläufe derselben Kommune — auch nach
    Prozess-/Serverneustart — kommen ohne erneuten Download aus. Bewusst das
    Roh-JSON statt der geparsten Features: Shapely-Geometrien sind nicht
    JSON-serialisierbar, und das Parsen ist gegen den Download vernachlässigbar.
    """
    digest = hashlib.sha1(bbox.encode("utf-8")).hexdigest()[:16]
    path = os.path.join(settings.OSM_CACHE_DIR, f"{kind}_{digest}.json.gz")
    try:
        if (
            os.path.exists(path)
            and _time.time() - os.path.getmtime(path) < settings.OSM_CACHE_TTL_S
        ):
            with gzip.open(path, "rt", encoding="utf-8") as fh:
                data = json.load(fh)
            log.info("Overpass-Disk-Cache HIT: %s bbox=%s (%s)", kind, bbox[:30], path)
            return data
    except Exception as exc:
        log.warning("Overpass-Disk-Cache %s unlesbar (%s) — lade neu", path, exc)

    data = _overpass_query(query_body)
    try:
        os.makedirs(settings.OSM_CACHE_DIR, exist_ok=True)
        tmp = f"{path}.tmp.{os.getpid()}"
        with gzip.open(tmp, "wt", encoding="utf-8") as fh:
            json.dump(data, fh, separators=(",", ":"))
        os.replace(tmp, path)
    except Exception:
        log.exception("Overpass-Disk-Cache %s nicht schreibbar", path)
    return data


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
      way["leisure"~"park|garden|dog_park|pitch|track|stadium|sports_centre|playground|golf_course|nature_reserve|recreation_ground"]({bbox});
      relation["leisure"~"park|garden|dog_park|pitch|track|stadium|sports_centre|playground|golf_course|nature_reserve|recreation_ground"]({bbox});
    );
    out body;
    >;
    out skel qt;
    """

    data = _overpass_query_cached("landuse2", bbox, query)
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
            "surface": tags.get("surface"),
        })

    log.info("Fetched %d land-use/natural features from OSM (%.2f MB)",
             len(results), response_bytes / 1_048_576)

    # ── Store in cache (Single-Entry: nur die aktuelle bbox) ─────────────
    with _cache_lock:
        _landuse_cache.clear()
        _landuse_cache[bbox] = (_time.time(), results, response_bytes)

    return results, response_bytes


def _water_tag(tags: dict) -> str:
    """Kurzbeschreibung des OSM-Tags, das ein Feature zum Gewässer macht."""
    if tags.get("natural") == "water":
        return f"natural=water/{tags['water']}" if tags.get("water") else "natural=water"
    if tags.get("water"):
        return f"water={tags['water']}"
    if tags.get("waterway"):
        return f"waterway={tags['waterway']}"
    return "?"


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

    data = _overpass_query_cached("water", bbox, query)
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

        # Herkunft für den Inspektor: OSM-ID/-Typ + auslösendes Tag + Name.
        meta = {
            "osm_id": el.get("id"),
            "osm_type": el.get("type"),
            "tag": _water_tag(tags),
            "name": tags.get("name"),
        }

        if el["type"] == "way":
            nds = el.get("nodes", [])
            coords = [nodes[n] for n in nds if n in nodes]
            if len(coords) < 2:
                continue
            waterway = tags.get("waterway", "")
            minor = waterway in _MINOR_WATERWAYS
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
                    results.append({"geometry": geom, "kind": "polygon", "minor": minor, **meta})
                except Exception:
                    pass
            elif waterway or len(coords) >= 2:
                results.append({"geometry": LineString(coords), "kind": "line", "minor": minor, **meta})

        elif el["type"] == "relation":
            rel_type = tags.get("type", "")
            # Nur echte FLÄCHEN-Relationen polygonisieren. Eine ``type=waterway``-
            # Relation (Fluss/Bach aus vielen Segmenten, z. B. „Döllnitz“ rel/15077092)
            # ist KEINE Fläche — sonst stitcht _relation_to_multipolygon die Segmente
            # zu einem Riesenpolygon über den ganzen Lauf und pinnt water_prox flächig
            # auf 1. Solche Relationen als Linien führen.
            is_area_rel = rel_type == "multipolygon" or (
                (tags.get("natural") == "water" or tags.get("water"))
                and rel_type != "waterway"
            )
            if is_area_rel:
                geom = _element_to_polygon(el, nodes, elements)
                if geom is not None:
                    results.append({"geometry": geom, "kind": "polygon", "minor": False, **meta})
            else:
                minor = tags.get("waterway", "") in _MINOR_WATERWAYS
                for line in _relation_member_lines(el, nodes, elements):
                    results.append({"geometry": line, "kind": "line", "minor": minor, **meta})

    log.info("Fetched %d water features from OSM", len(results))

    with _cache_lock:
        _water_cache.clear()
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
        # STRtree.nearest() misst im Baum-CRS EPSG:4326 (Grad). Wegen der Anisotropie
        # zwischen Längen- und Breitengrad (bei 51° N: 1° lon ≈ 70 km, 1° lat ≈ 111 km)
        # ist das grad-nächste Gewässer NICHT immer das meter-nächste — der Score wäre
        # dann fälschlich zu niedrig. Daher: grad-nächstes nur als Startwert nehmen und
        # alle Features im metrischen Umkreis exakt in UTM nachmessen.
        import math
        nearest_i = int(tree.nearest(cell_geom))
        best = float(cell_utm.distance(shp_transform(to_utm, geoms[nearest_i])))
        # Meter → Grad großzügig über den kleineren m/Grad-Faktor (Längengrad) umrechnen,
        # damit der Suchradius den wahren Nächsten garantiert einschließt.
        m_per_deg_lon = max(1.0, 111_320.0 * math.cos(math.radians(lat)))
        pad_deg = (best + cell_size_m) / m_per_deg_lon
        try:
            candidates = tree.query(cell_geom.buffer(pad_deg))
        except Exception:
            candidates = [nearest_i]
        for i in candidates:
            d = float(cell_utm.distance(shp_transform(to_utm, geoms[int(i)])))
            if d < best:
                best = d
        return best

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


def compute_ditch_density_score(
    cell_geom: Any,
    ditch_features: list[dict],
    cell_size_m: float,
    ditch_index: tuple[Any, list[Any]] | None = None,
) -> float:
    """Sehr schwacher Gewässernähe-Beitrag von Kleinstgräben, über die Zelle skaliert.

    Kennzahl ist die Grabendichte = Gesamtlänge aller Gräben *innerhalb* der Zelle
    geteilt durch die Zellkantenlänge. Ein einzelner die Zelle querender Graben
    ergibt Dichte ≈ 1, eine nur gestreifte Ecke ≈ 0.1, ein dichtes Grabennetz > 1.
    Multipliziert mit ``DITCH_DENSITY_WEIGHT`` (sehr klein) und bei
    ``DITCH_PROX_CAP`` gedeckelt, damit Gräben nie wie ein echtes Gewässer wirken.
    """
    if not ditch_features:
        return 0.0

    import pyproj
    from shapely.ops import transform as shp_transform

    minx, miny, maxx, maxy = cell_geom.bounds
    lat = (miny + maxy) / 2.0
    utm_zone = int((cell_geom.centroid.x + 180) / 6) + 1
    utm_epsg = 32600 + utm_zone if lat >= 0 else 32700 + utm_zone
    to_utm = pyproj.Transformer.from_crs(
        "EPSG:4326", f"EPSG:{utm_epsg}", always_xy=True
    ).transform

    if ditch_index is not None:
        tree, geoms = ditch_index
        try:
            candidates = [geoms[int(i)] for i in tree.query(cell_geom)]
        except Exception:
            candidates = geoms
    else:
        candidates = [f["geometry"] for f in ditch_features]

    total_len_m = 0.0
    for g in candidates:
        clipped = cell_geom.intersection(g)
        if clipped.is_empty:
            continue
        # In Grad geclippt, zur Längenmessung nach UTM (Meter) projizieren.
        total_len_m += shp_transform(to_utm, clipped).length

    if total_len_m <= 0.0:
        return 0.0
    density = total_len_m / max(float(cell_size_m), 1.0)
    return min(DITCH_PROX_CAP, density * DITCH_DENSITY_WEIGHT)


def describe_cell_water_sources(
    cell_geom: Any,
    features: list[dict],
    cell_size_m: float,
    index: tuple[Any, list[Any]] | None = None,
    max_dist_m: float = 500.0,
    limit: int = 8,
) -> list[dict]:
    """Debug: welche OSM-Gewässer-Objekte begründen die Wasserannahme dieser Zelle?

    Liefert je Feature ``{osm_id, osm_type, tag, name, kind, minor, dist_m}`` —
    sortiert nach Distanz, nur Objekte in Reichweite (Schnitt mit der Zelle ⇒
    dist_m 0). Für den Inspektor gedacht, damit ein ``water_prox``-Ausreißer auf
    die konkrete OSM-ID zurückführbar ist.
    """
    if not features:
        return []

    import pyproj
    from shapely.ops import transform as shp_transform

    minx, miny, maxx, maxy = cell_geom.bounds
    lat = (miny + maxy) / 2.0
    utm_zone = int((cell_geom.centroid.x + 180) / 6) + 1
    utm_epsg = 32600 + utm_zone if lat >= 0 else 32700 + utm_zone
    to_utm = pyproj.Transformer.from_crs(
        "EPSG:4326", f"EPSG:{utm_epsg}", always_xy=True
    ).transform
    cell_utm = shp_transform(to_utm, cell_geom)

    if index is not None:
        _tree, _geoms = index
        try:
            cand_idx = [int(i) for i in _tree.query(cell_geom)]
        except Exception:
            cand_idx = list(range(len(features)))
    else:
        cand_idx = list(range(len(features)))

    out: list[dict] = []
    for i in cand_idx:
        if i >= len(features):
            continue
        feat = features[i]
        dist = float(cell_utm.distance(shp_transform(to_utm, feat["geometry"])))
        if dist > max_dist_m:
            continue
        out.append({
            "osm_id": feat.get("osm_id"),
            "osm_type": feat.get("osm_type"),
            "tag": feat.get("tag"),
            "name": feat.get("name"),
            "kind": feat.get("kind"),
            "minor": bool(feat.get("minor")),
            "dist_m": round(dist, 1),
        })
    out.sort(key=lambda d: d["dist_m"])
    return out[:limit]


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


def _is_emergency_feature(tags: dict) -> bool:
    """OSM-Feuerwehr/Rettungs-Infrastruktur (Notfallmanagement-/Frühwarn-Proxy)."""
    return tags.get("amenity") == "fire_station" or tags.get("emergency") in _EMERGENCY_TAGS


def build_emergency_spatial_index(infra: dict) -> tuple[Any, list] | None:
    geoms = [Point(pt["lon"], pt["lat"]) for pt in infra.get("emergency_points", [])]
    return build_healthcare_spatial_index(geoms)


def build_dyke_spatial_index(infra: dict) -> tuple[Any, list] | None:
    geoms = [d["geometry"] for d in infra.get("dyke_geoms", [])]
    return build_healthcare_spatial_index(geoms)


def compute_cell_emergency_access(
    cell_geom: Any,
    infra: dict,
    spatial_index: tuple[Any, list] | None,
) -> float | None:
    """0..1 Erreichbarkeit der nächsten Feuerwehr/Rettung (1 = direkt, 0 = ≥ max).

    ``None``, wenn im gesamten Gebiet keine Notfall-Infrastruktur gemappt ist
    (kein Datum ≠ schlecht versorgt → Indikator fällt dann auf Neutralwert).
    """
    geoms = [Point(pt["lon"], pt["lat"]) for pt in infra.get("emergency_points", [])]
    if not geoms:
        return None
    dist_m = compute_nearest_distance_m(
        cell_geom, geoms, spatial_index, fallback_m=EMERGENCY_MAX_DIST_M,
    )
    return round(healthcare_proximity_score(dist_m, EMERGENCY_MAX_DIST_M), 4)


def compute_cell_dyke_proximity(
    cell_geom: Any,
    infra: dict,
    spatial_index: tuple[Any, list] | None,
) -> float:
    """0..1 Nähe zum nächsten Deich/Damm (1 = direkt, 0 = ≥ max)."""
    geoms = [d["geometry"] for d in infra.get("dyke_geoms", [])]
    if not geoms:
        return 0.0
    dist_m = compute_nearest_distance_m(
        cell_geom, geoms, spatial_index, fallback_m=DYKE_MAX_DIST_M,
    )
    return round(water_proximity_score(dist_m, DYKE_MAX_DIST_M), 4)


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
        # STRtree.nearest() misst im Baum-CRS EPSG:4326 (Grad); wegen der Längen-/
        # Breitengrad-Anisotropie ist das grad-nächste Feature nicht immer das
        # meter-nächste. Grad-Nächstes daher nur als Startwert, dann alle Features im
        # metrischen Umkreis exakt in UTM nachmessen (analog compute_water_distance_m).
        import math
        nearest_i = int(tree.nearest(cell_geom))
        raw_m = float(cell_utm.distance(shp_transform(to_utm, indexed_geoms[nearest_i])))
        m_per_deg_lon = max(1.0, 111_320.0 * math.cos(math.radians(lat)))
        pad_deg = raw_m / m_per_deg_lon + (maxx - minx)
        try:
            candidates = tree.query(cell_geom.buffer(pad_deg))
        except Exception:
            candidates = [nearest_i]
        for i in candidates:
            d = float(cell_utm.distance(shp_transform(to_utm, indexed_geoms[int(i)])))
            if d < raw_m:
                raw_m = d
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


def _norm_surface(surface: str | None) -> str | None:
    """OSM ``surface``-Wert normalisieren (Varianten wie ``paving_stones:30`` → Basis)."""
    if not surface:
        return None
    s = str(surface).strip().lower()
    if s in SURFACE_SEALING:
        return s
    base = s.split(":")[0].split(";")[0]
    return base if base in SURFACE_SEALING else None


def _apply_surface(row: dict[str, float], surface: str | None) -> dict[str, float]:
    """surface-Tag sticht den V-Default der Zeile (Rest wandert nach O bzw. G).

    Robust gegen Über-/Unterschreitung: ist die Fläche versiegelter als der
    Default, wird die Differenz aus den größten Nicht-V-Kategorien abgezogen
    (z. B. Kunstrasen-Asche auf einem ``pitch`` frisst dessen Grün); ist sie
    weniger versiegelt, landet der Rest bei G (Rasengitter/Rasen) oder O.
    """
    surf = _norm_surface(surface)
    if surf is None:
        return row
    new_v = float(SURFACE_SEALING[surf])
    old_v = float(row.get("V", 0.0))
    out = dict(row)
    out["V"] = new_v
    diff = new_v - old_v
    if diff > 0:  # versiegelter → aus größten Nicht-V-Kategorien abziehen
        remaining = diff
        for cat in sorted((c for c in out if c != "V"), key=lambda c: -out[c]):
            take = min(remaining, out[cat])
            out[cat] -= take
            remaining -= take
            if remaining <= 1e-9:
                break
    elif diff < 0:  # unversiegelter → Rest nach G (grasig) bzw. O
        sink = "G" if surf in _GRASSY_SURFACES else "O"
        out[sink] = out.get(sink, 0.0) + (-diff)
    return {k: v for k, v in out.items() if v > 0}


def _road_row(road: dict) -> dict[str, float]:
    """Kompositionszeile einer Straße aus highway-Typ, tracktype und surface."""
    hw = road.get("highway", "")
    base = dict(ROAD_COMPOSITION.get(hw, _ROAD_DEFAULT_ROW))
    if hw == "track":
        tt = road.get("tracktype")
        if tt in _TRACKTYPE_SEALING:
            v = _TRACKTYPE_SEALING[tt]
            base = {"V": v, "O": 100 - v}
    return _apply_surface(base, road.get("surface"))


def _paved_row(paved: dict) -> dict[str, float]:
    """Kompositionszeile eines Flächen-Verkehrsobjekts (Platz/Parkplatz/Flugbetrieb)."""
    base = dict(PAVED_COMPOSITION.get(paved.get("kind", "square"), PAVED_COMPOSITION["square"]))
    return _apply_surface(base, paved.get("surface"))


def _landuse_item(feat: dict) -> tuple[int, dict[str, float], float, str, bool] | None:
    """(precedence, Kompositionszeile, Albedo, Label, is_glacier) für ein Landuse-Feature.

    ``None``, wenn kein bekannter Tag greift → die Fläche fällt an die
    Fallback-Zeile (bleibt also nicht stumm unbedeckt).
    """
    lu = feat.get("landuse") or ""
    nat = feat.get("natural") or ""
    leis = feat.get("leisure") or ""

    if nat == "water":
        return _PREC_WATER, dict(NATURAL_COMPOSITION["water"]), WATER_ALBEDO, "water", False
    if nat == "glacier":
        return _PREC_SPECIFIC, dict(NATURAL_COMPOSITION["glacier"]), 0.30, "glacier", True
    if leis in LEISURE_COMPOSITION:
        row = _apply_surface(dict(LEISURE_COMPOSITION[leis]), feat.get("surface"))
        return _PREC_SPECIFIC, row, LEISURE_ALBEDO, leis, False
    if lu in LANDUSE_COMPOSITION:
        prec = _PREC_SPECIFIC if lu in _SPECIFIC_LANDUSE else _PREC_BROAD
        return prec, dict(LANDUSE_COMPOSITION[lu]), LANDUSE_ALBEDO.get(lu, 0.20), lu, False
    if nat in NATURAL_COMPOSITION:
        return _PREC_BROAD, dict(NATURAL_COMPOSITION[nat]), NATURAL_ALBEDO.get(nat, 0.20), nat, False
    return None


def _empty_composition() -> dict:
    return {
        "impervious_fraction": 0.05, "albedo": FALLBACK_ALBEDO,
        "green_fraction": 0.0, "water_fraction": 0.0,
        "forest_fraction": 0.0, "glacier_fraction": 0.0, "farmland_fraction": 0.0,
        "open_fraction": 0.95,
        "composition": {"V": 0.05, "G": 0.0, "W": 0.0, "A": 0.0, "Wa": 0.0, "O": 0.95},
        "dominant_landuse": "unknown", "coverage_pct": 0.0,
    }


def compute_cell_composition(
    cell_geom: Any,
    buildings: list[dict],
    roads: list[dict],
    paved_areas: list[dict],
    landuse_features: list[dict],
) -> dict:
    """Vollständige Flächenkomposition einer Zelle (Schichtmodell, 100%-Budget).

    Die Zelle wird schichtweise (Gebäude → Verkehr/Plätze → Wasser → spezifische
    Nutzung → großflächige Landnutzung → Fallback) auf die sechs Kategorien
    V/G/W/A/Wa/O aufgeteilt. Höhere Schichten werden geometrisch von der Restfläche
    abgezogen (``difference``), sodass jedes Stück Zellfläche genau EINEM — dem
    konkretesten — Feature zugeordnet wird und die Summe exakt 100 % ergibt.

    Rückgabe-Keys sind mit der früheren ``compute_cell_landuse`` kompatibel
    (impervious_fraction, albedo, green_fraction, water_fraction, forest_fraction,
    glacier_fraction, farmland_fraction, dominant_landuse, coverage_pct) plus einer
    ``composition``-Aufschlüsselung für den Inspektor.
    """
    cell_area = cell_geom.area
    if cell_area <= 0:
        return _empty_composition()

    # (precedence, geom_area, geom, row, albedo, label, is_glacier)
    items: list[tuple[int, float, Any, dict[str, float], float, str, bool]] = []

    for b in buildings:
        g = b["geometry"]
        if cell_geom.intersects(g):
            items.append((_PREC_BUILDING, g.area, g, BUILDING_ROW, BUILDING_ALBEDO, "building", False))

    for r in roads:
        g = r["geometry"]
        buf = (float(r.get("width_m", 5.0)) / 2.0) * DEGREE_PER_METER
        pg = g.buffer(buf) if buf > 0 else g
        if cell_geom.intersects(pg):
            items.append((_PREC_TRAFFIC, pg.area, pg, _road_row(r), PAVED_ALBEDO, "road", False))

    for p in paved_areas:
        g = p["geometry"]
        if cell_geom.intersects(g):
            items.append((_PREC_TRAFFIC, g.area, g, _paved_row(p), PAVED_ALBEDO,
                          p.get("kind", "paved"), False))

    for feat in landuse_features:
        info = _landuse_item(feat)
        if info is None:
            continue
        prec, row, alb, label, is_gl = info
        g = feat["geometry"]
        if cell_geom.intersects(g):
            items.append((prec, g.area, g, row, alb, label, is_gl))

    # Schicht zuerst (precedence aufsteigend), innerhalb einer Schicht kleinere
    # Polygone zuerst → das spezifischere Objekt sticht das großflächigere.
    items.sort(key=lambda t: (t[0], t[1]))

    comp = {c: 0.0 for c in _COMP_CATS}
    albedo_acc = 0.0
    glacier_frac = 0.0
    forest_frac = 0.0
    farmland_frac = 0.0
    label_areas: dict[str, float] = {}

    remaining = cell_geom
    for _prec, _a, g, row, alb, label, is_gl in items:
        if remaining.is_empty:
            break
        try:
            clipped = remaining.intersection(g)
        except Exception:
            continue
        ia = clipped.area
        if ia <= 0:
            continue
        frac = ia / cell_area
        for cat, val in row.items():
            comp[cat] += (val / 100.0) * frac
        albedo_acc += alb * frac
        label_areas[label] = label_areas.get(label, 0.0) + frac
        forest_frac += (row.get("W", 0.0) / 100.0) * frac
        farmland_frac += (row.get("A", 0.0) / 100.0) * frac
        if is_gl:
            glacier_frac += frac
        try:
            remaining = remaining.difference(g)
        except Exception:
            try:
                remaining = remaining.difference(g.buffer(0))
            except Exception:
                pass

    # Fallback für die von keinem Feature bedeckte Restfläche.
    rem_frac = 0.0
    if not remaining.is_empty:
        rem_frac = max(0.0, min(1.0, remaining.area / cell_area))
    if rem_frac > 1e-9:
        for cat, val in FALLBACK_ROW.items():
            comp[cat] += (val / 100.0) * rem_frac
        albedo_acc += FALLBACK_ALBEDO * rem_frac
        label_areas["unknown"] = label_areas.get("unknown", 0.0) + rem_frac

    # Normierung gegen Rundungs-/Slivereffekte aus intersection/difference.
    total = sum(comp.values())
    if total > 0:
        for cat in comp:
            comp[cat] /= total
        albedo_final = albedo_acc / total
        forest_frac /= total
        farmland_frac /= total
        glacier_frac = min(glacier_frac / total, 1.0)
    else:
        return _empty_composition()

    green_frac = comp["G"] + comp["W"]  # Wald zählt (wie bisher) zum Grünanteil
    coverage = max(0.0, min(1.0, 1.0 - rem_frac))
    real_labels = {k: v for k, v in label_areas.items() if k != "unknown"}
    dominant = max(real_labels, key=real_labels.get) if real_labels else "unknown"

    return {
        "impervious_fraction": round(min(max(comp["V"], 0.0), 1.0), 4),
        "albedo": round(albedo_final, 4),
        "green_fraction": round(min(green_frac, 1.0), 4),
        "water_fraction": round(min(comp["Wa"], 1.0), 4),
        "forest_fraction": round(min(forest_frac, 1.0), 4),
        "glacier_fraction": round(min(glacier_frac, 1.0), 4),
        "farmland_fraction": round(min(farmland_frac, 1.0), 4),
        "open_fraction": round(min(max(comp["O"], 0.0), 1.0), 4),
        "composition": {c: round(comp[c], 4) for c in _COMP_CATS},
        "dominant_landuse": dominant,
        "coverage_pct": round(coverage * 100, 1),
    }


# ── Level 3: Buildings & detailed surfaces ────────────────────────────────────

def fetch_buildings_and_roads(grid_cells: list[dict],
                              bundesland: str | None = None) -> dict:
    """Fetch building footprints, roads, paved areas, and trees from OSM.

    Returns dict with keys: buildings, roads, paved_areas, trees – each a list of
    dicts with geometry and tags.  ``paved_areas`` sind flächenhafte Verkehrs-/
    Platzobjekte (gepflasterte Plätze, Parkplätze, Flugbetriebsflächen), die NICHT
    als Linie, sondern als Polygon in die Flächenkomposition eingehen.  Uses
    thread-safe cache.

    Ist für ``bundesland`` eine LoD2-Quelle angebunden (amtliche 3D-Gebäude-
    modelle, siehe services/geodata/lod2), ERSETZEN die LoD2-Footprints+Höhen
    das OSM-Gebäudeset vollständig (``building_source`` = "lod2"); sonst bleibt
    die OSM-Heuristik (height-Tag / levels·3 m / 6-m-Default) als Fallback.
    Der Single-Entry-Cache ist nur nach bbox geschlüsselt — das Bundesland ist
    je Kommune konstant, ein bbox-Wechsel invalidiert ohnehin.
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
      way["amenity"="parking"]({bbox});
      relation["amenity"="parking"]({bbox});
      way["aeroway"~"^(apron|runway|taxiway|helipad)$"]({bbox});
      node["natural"="tree"]({bbox});
    );
    out body;
    >;
    out skel qt;
    """

    data = _overpass_query_cached("buildings2", bbox, query)
    response_bytes = data.get("_response_bytes", 0)
    elements = data.get("elements", [])

    nodes: dict[int, tuple[float, float]] = {}
    for el in elements:
        if el["type"] == "node":
            nodes[el["id"]] = (el["lon"], el["lat"])

    from shapely.geometry import LineString
    buildings = []
    roads = []
    paved_areas = []
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
            if len(coords) < 2:
                continue
            # Gepflasterte Plätze (highway=pedestrian/footway + area=yes) sind
            # FLÄCHEN, nicht Linien — als Polygon führen, sonst zählt ein Marktplatz
            # nur als 3-m-Linienpuffer (≈ 0 % Versiegelung der Zelle).
            as_area = (
                tags.get("area") == "yes"
                and len(coords) >= 4
                and coords[0] == coords[-1]
            )
            area_geom = _ring_to_polygon(coords) if as_area else None
            if area_geom is not None:
                paved_areas.append({
                    "geometry": area_geom, "kind": "square",
                    "surface": tags.get("surface"),
                })
            else:
                hw_type = tags.get("highway", "")
                roads.append({
                    "geometry": LineString(coords),
                    "highway": hw_type,
                    "width_m": _road_width(hw_type),
                    "surface": tags.get("surface"),
                    "tracktype": tags.get("tracktype"),
                })

        elif tags.get("amenity") == "parking":
            # Unter-/überbaute Parkierung nicht als eigene versiegelte Fläche zählen
            # (unterirdisch versickert nicht, mehrgeschossig ist als building erfasst).
            if tags.get("parking") in ("underground", "rooftop", "multi-storey"):
                continue
            geom = _element_to_polygon(el, nodes, elements)
            if geom is not None:
                paved_areas.append({
                    "geometry": geom, "kind": "parking",
                    "surface": tags.get("surface"),
                })

        elif tags.get("aeroway") in _AEROWAY_PAVED and el["type"] == "way":
            geom = _element_to_polygon(el, nodes, elements)
            if geom is not None:
                paved_areas.append({
                    "geometry": geom, "kind": "aeroway",
                    "surface": tags.get("surface"),
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
        "Fetched %d buildings, %d road segments, %d paved areas, %d trees from OSM (%.2f MB)",
        len(buildings), len(roads), len(paved_areas), len(trees), response_bytes / 1_048_576,
    )
    result = {
        "buildings": buildings, "roads": roads, "paved_areas": paved_areas,
        "trees": trees, "_response_bytes": response_bytes,
        "building_source": "osm",
    }

    # ── LoD2-Overlay: amtliche Höhen+Footprints ersetzen OSM-Gebäude ─────
    try:
        from app.services.geodata.lod2.loader import fetch_lod2_buildings
        lod2 = fetch_lod2_buildings(bbox, bundesland)
    except Exception:  # noqa: BLE001 — LoD2 darf ein Assessment nie kippen
        log.exception("LoD2-Abruf fehlgeschlagen — OSM-Fallback")
        lod2 = None
    # None = keine LoD2-Abdeckung/Fehler; [] = Abdeckung ohne Gebäude (gültig)
    if lod2 is not None:
        result["buildings"] = lod2
        result["building_source"] = "lod2"
        log.info("LoD2: %d amtliche Gebäude ersetzen %d OSM-Gebäude (%s)",
                 len(lod2), len(buildings), bundesland)

    # ── Store in cache (Single-Entry: nur die aktuelle bbox) ─────────────
    with _cache_lock:
        _buildings_cache.clear()
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
        avg_building_height (m, flächengewichtet),
        road_coverage (fraction),
        tree_count, tree_canopy_fraction,
        sky_view_factor (Platzhalter 1.0 — wird nach dem Zell-Pool durch das
        Horizontwinkel-SVF aus services/geodata/lod2/svf.py überschrieben).
    """
    cell_area = cell_geom.area  # in degree², used for fractions
    if cell_area <= 0:
        return _empty_building_metrics()

    # Buildings — Höhe flächengewichtet (Gewicht = Grundriss∩Zelle), damit
    # eine Gartenhütte nicht gleich viel zählt wie ein Hochhaus.
    bldg_area = 0.0
    bldg_count = 0
    height_area = 0.0

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
        height_area += b["height"] * ia

    bldg_coverage = min(bldg_area / cell_area, 1.0) if cell_area > 0 else 0.0
    avg_height = (height_area / bldg_area) if bldg_area > 0 else 0.0

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

    return {
        "building_count": bldg_count,
        "building_coverage": round(bldg_coverage, 4),
        "avg_building_height": round(avg_height, 1),
        "road_coverage": round(road_coverage, 4),
        "tree_count": tree_count,
        "tree_canopy_fraction": round(canopy_fraction, 4),
        # Platzhalter: echtes Horizontwinkel-SVF wird in gather_cell_inputs
        # nach dem Zell-Pool je Zelle gesetzt (Raster-Verfahren, nicht je Zelle
        # isoliert berechenbar — Nachbargebäude außerhalb der Zelle zählen).
        "sky_view_factor": 1.0,
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
        "emergency_points": [],
        "dyke_geoms": [],
        "healthcare_hospital": [],
        "healthcare_doctor": [],
        "healthcare_pharmacy": [],
        # Pflegeeinrichtungen (Geometrie in lon/lat: Point oder Polygon) — Basis
        # der Zellebene CARE_HOME_SHARE_85P (Methodik #95 Rev. 8, §3.6).
        "care_home_geoms": [],
    }


def _is_care_home(tags: dict) -> bool:
    """OSM-Pflegeeinrichtung: amenity=nursing_home oder social_facility-Wohnformen."""
    return (tags.get("amenity") == "nursing_home"
            or tags.get("social_facility") in ("nursing_home", "assisted_living"))


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
      node["man_made"~"water_works|wastewater_plant|water_tower|pumping_station|reservoir_covered|storage_tank"]({bbox});
      way["man_made"~"water_works|wastewater_plant|water_tower|pumping_station|reservoir_covered|storage_tank"]({bbox});
      node["tower"="communication"]({bbox});
      node["man_made"~"mast|communications_tower|antenna"]({bbox});
      node["man_made"="tower"]["tower:type"="communication"]({bbox});
      node["tower:type"="communication"]({bbox});
      node["communication"]({bbox});
      node["communication:mobile_phone"]({bbox});
      node["communication:radio"]({bbox});
      node["telecom"~"data_centre|data_center|exchange"]({bbox});
      way["telecom"~"data_centre|data_center|exchange"]({bbox});
      way["building"="data_center"]({bbox});
      node["railway"~"^(station|halt)$"]({bbox});
      node["public_transport"="station"]({bbox});
      node["amenity"="bus_station"]({bbox});
      node["amenity"="fire_station"]({bbox});
      way["amenity"="fire_station"]({bbox});
      node["emergency"~"ambulance_station|water_rescue_station|disaster_response|lifeguard_base"]({bbox});
      way["emergency"~"ambulance_station|water_rescue_station|disaster_response|lifeguard_base"]({bbox});
      way["man_made"~"dyke|embankment"]({bbox});
      node["amenity"="nursing_home"]({bbox});
      way["amenity"="nursing_home"]({bbox});
      node["social_facility"~"nursing_home|assisted_living"]({bbox});
      way["social_facility"~"nursing_home|assisted_living"]({bbox});
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

    # Kind "infra3": + Pflegeeinrichtungen (nursing_home/assisted_living) für die
    # Zellebene CARE_HOME_SHARE_85P (Methodik #95 Rev. 8, §3.6); ältere
    # "infra"/"infra2"-Dateien altern per TTL weg.
    data = _overpass_query_cached("infra3", bbox, query)
    response_bytes = data.get("_response_bytes", 0)
    elements = data.get("elements", [])

    nodes: dict[int, tuple[float, float]] = {}
    for el in elements:
        if el["type"] == "node":
            nodes[el["id"]] = (el["lon"], el["lat"])

    result = _empty_infra_features()
    comm_node_ids: set[int | tuple[str, int]] = set()
    water_node_ids: set[int] = set()
    transport_node_ids: set[int] = set()
    emergency_ids: set[int | tuple[str, int]] = set()
    healthcare_ids: set[int | tuple[str, int]] = set()
    care_home_ids: set[int | tuple[str, int]] = set()

    for el in elements:
        tags = el.get("tags", {})
        el_type = el.get("type")
        el_id = el.get("id")

        if el_type == "node" and "power" in tags:
            # cls=None (Masten/Tragwerke, Dach-PV) zählt nicht — Doppelzählungs-Fix:
            # Tragwerke sind Bestandteil der je Zellquerung gezählten Leitung.
            cls = infra_assets.classify_power_node(tags)
            if cls is not None and el["id"] in nodes:
                lon, lat = nodes[el["id"]]
                result["energy_points"].append({"lon": lon, "lat": lat, "cls": cls})

        elif el_type == "way" and "power" in tags:
            power_tag = tags.get("power", "")
            if power_tag in _POWER_LINE_TAGS:
                cls = infra_assets.classify_power_line(tags)
                if cls is not None:
                    nds = el.get("nodes", [])
                    coords = [nodes[n] for n in nds if n in nodes]
                    if len(coords) >= 2:
                        result["energy_lines"].append(
                            {"geometry": LineString(coords), "cls": cls}
                        )
            else:
                cls = infra_assets.classify_power_area(tags)
                if cls is not None:
                    geom = _element_to_polygon(el, nodes, elements)
                    if geom is not None:
                        result["energy_areas"].append({"geometry": geom, "cls": cls})
                    else:
                        nds = el.get("nodes", [])
                        coords = [nodes[n] for n in nds if n in nodes]
                        if len(coords) >= 2:
                            result["energy_lines"].append(
                                {"geometry": LineString(coords), "cls": cls}
                            )

        elif el_type == "node":
            if el["id"] not in nodes:
                continue
            water_cls = infra_assets.classify_water(tags)
            if water_cls is not None and el["id"] not in water_node_ids:
                water_node_ids.add(el["id"])
                lon, lat = nodes[el["id"]]
                result["water_points"].append({"lon": lon, "lat": lat, "cls": water_cls})
            comm_cls = infra_assets.classify_comm(tags)
            if comm_cls is not None and el["id"] not in comm_node_ids:
                comm_node_ids.add(el["id"])
                lon, lat = nodes[el["id"]]
                result["comm_points"].append({"lon": lon, "lat": lat, "cls": comm_cls})
            transport_cls = infra_assets.classify_transport(tags)
            if transport_cls is not None and el["id"] not in transport_node_ids:
                transport_node_ids.add(el["id"])
                lon, lat = nodes[el["id"]]
                result["transport_points"].append(
                    {"lon": lon, "lat": lat, "cls": transport_cls}
                )
            if _is_emergency_feature(tags) and el["id"] not in emergency_ids:
                emergency_ids.add(el["id"])
                lon, lat = nodes[el["id"]]
                result["emergency_points"].append({"lon": lon, "lat": lat})
            _add_healthcare_geometry(
                result, tags, Point(nodes[el["id"]]), healthcare_ids, el_id,
            )
            if _is_care_home(tags) and el_id not in care_home_ids:
                care_home_ids.add(el_id)
                result["care_home_geoms"].append(
                    {"geometry": Point(nodes[el["id"]])}
                )

        elif el_type == "way":
            water_cls = infra_assets.classify_water(tags)
            if water_cls is not None:
                geom = _element_to_polygon(el, nodes, elements)
                if geom is not None:
                    result["water_areas"].append({"geometry": geom, "cls": water_cls})
            comm_cls = infra_assets.classify_comm(tags)
            if comm_cls is not None and ("way", el_id) not in comm_node_ids:
                # Rechenzentren/Vermittlungsstellen als Gebäude-Way → Zentroid-Punkt.
                comm_node_ids.add(("way", el_id))
                nds = el.get("nodes", [])
                coords = [nodes[n] for n in nds if n in nodes]
                if coords:
                    lon = sum(c[0] for c in coords) / len(coords)
                    lat = sum(c[1] for c in coords) / len(coords)
                    result["comm_points"].append({"lon": lon, "lat": lat, "cls": comm_cls})
            if tags.get("man_made") in _DYKE_MAN_MADE_TAGS:
                nds = el.get("nodes", [])
                coords = [nodes[n] for n in nds if n in nodes]
                if len(coords) >= 2:
                    result["dyke_geoms"].append({"geometry": LineString(coords)})
            if _is_emergency_feature(tags) and ("way", el_id) not in emergency_ids:
                emergency_ids.add(("way", el_id))
                nds = el.get("nodes", [])
                coords = [nodes[n] for n in nds if n in nodes]
                if coords:
                    lon = sum(c[0] for c in coords) / len(coords)
                    lat = sum(c[1] for c in coords) / len(coords)
                    result["emergency_points"].append({"lon": lon, "lat": lat})
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
            if _is_care_home(tags) and ("way", el_id) not in care_home_ids:
                geom = _element_to_polygon(el, nodes, elements)
                if geom is None:
                    nds = el.get("nodes", [])
                    coords = [nodes[n] for n in nds if n in nodes]
                    geom = (Point(sum(c[0] for c in coords) / len(coords),
                                  sum(c[1] for c in coords) / len(coords))
                            if coords else None)
                if geom is not None:
                    care_home_ids.add(("way", el_id))
                    result["care_home_geoms"].append({"geometry": geom})

    result["energy_lines"] = _merge_energy_lines(result["energy_lines"])

    log.info(
        "Fetched infrastructure from OSM: %d energy pts, %d lines, %d areas, "
        "%d water pts, %d water areas, %d comm pts, %d transport pts, "
        "%d emergency pts, %d dyke geoms, "
        "%d hospital, %d doctor, %d pharmacy, %d care homes (%.2f MB)",
        len(result["energy_points"]), len(result["energy_lines"]),
        len(result["energy_areas"]), len(result["water_points"]),
        len(result["water_areas"]), len(result["comm_points"]),
        len(result["transport_points"]),
        len(result["emergency_points"]), len(result["dyke_geoms"]),
        len(result["healthcare_hospital"]), len(result["healthcare_doctor"]),
        len(result["healthcare_pharmacy"]), len(result["care_home_geoms"]),
        response_bytes / 1_048_576,
    )

    with _cache_lock:
        _infra_cache.clear()
        _infra_cache[bbox] = (_time.time(), result)

    return result


def _merge_energy_lines(lines: list[dict]) -> list[dict]:
    """Leitungs-Ways je Klasse zu Strängen verschmelzen.

    OSM splittet Leitungszüge an Masten/Tag-Wechseln in viele Einzel-Ways —
    ohne Merge zählte derselbe Zug in einer Zelle mehrfach (v. a. am
    Umspannwerk-Sammelpunkt). ``linemerge`` verbindet nur Ketten an
    gemeinsamen Endpunkten (kein Noding): sich kreuzende oder am selben
    Portal endende getrennte Stromkreise bleiben getrennte Objekte.
    """
    if not lines:
        return lines
    from shapely.ops import linemerge

    by_cls: dict[str, list] = {}
    for ln in lines:
        by_cls.setdefault(ln["cls"], []).append(ln["geometry"])
    merged: list[dict] = []
    for cls, geoms in by_cls.items():
        m = linemerge(geoms) if len(geoms) > 1 else geoms[0]
        for g in getattr(m, "geoms", [m]):
            merged.append({"geometry": g, "cls": cls})
    return merged


def compute_cell_infrastructure(cell_geom: Any, infra: dict) -> dict:
    """Gewichtete KRITIS-Kritikalitätspunkte je Rasterzelle.

    Je Sektor werden die Vorkommen pro Anlagenklasse gezählt (Punkt-in-Zelle
    bzw. Linien-/Flächen-Intersect je +1) und mit den — kommunal
    override-fähigen — Klassengewichten aus app/data/infra_assets.py zu
    Punkten aggregiert. Die ``*_count``-Keys tragen die gewichteten Punkte,
    die ``*_classes``-Dicts die rohen Klassen-Zählungen (für den monetären
    Pfad mit klassenspezifischen Ersatzwerten).
    """
    from shapely.geometry import Point

    if cell_geom is None or cell_geom.is_empty:
        return _empty_infra_metrics()

    def _bump(counts: dict[str, int], cls: str | None) -> None:
        if cls is not None:
            counts[cls] = counts.get(cls, 0) + 1

    energy_counts: dict[str, int] = {}
    for pt in infra.get("energy_points", []):
        if cell_geom.contains(Point(pt["lon"], pt["lat"])):
            _bump(energy_counts, pt.get("cls"))
    for line in infra.get("energy_lines", []):
        if cell_geom.intersects(line["geometry"]):
            _bump(energy_counts, line.get("cls"))
    for area in infra.get("energy_areas", []):
        if cell_geom.intersects(area["geometry"]):
            # v2-Kandidat: Punkt-Features (Trafos) innerhalb bereits gezählter
            # Stationsflächen überspringen; bei Gewicht 0,5 tolerierbar.
            _bump(energy_counts, area.get("cls"))

    water_counts: dict[str, int] = {}
    for pt in infra.get("water_points", []):
        if cell_geom.contains(Point(pt["lon"], pt["lat"])):
            _bump(water_counts, pt.get("cls"))
    for area in infra.get("water_areas", []):
        if cell_geom.intersects(area["geometry"]):
            _bump(water_counts, area.get("cls"))

    comm_counts: dict[str, int] = {}
    for pt in infra.get("comm_points", []):
        if cell_geom.contains(Point(pt["lon"], pt["lat"])):
            _bump(comm_counts, pt.get("cls"))

    transport_counts: dict[str, int] = {}
    for pt in infra.get("transport_points", []):
        if cell_geom.contains(Point(pt["lon"], pt["lat"])):
            _bump(transport_counts, pt.get("cls"))

    def _score(sector: str, counts: dict[str, int]) -> float:
        return round(
            infra_assets.weighted_score(counts, infra_assets.resolve_weights(sector)), 2,
        )

    return {
        "energy_infra_count": _score("energy", energy_counts),
        "water_wastewater_count": _score("water", water_counts),
        "communication_count": _score("comm", comm_counts),
        "transport_hub_count": _score("transport", transport_counts),
        "energy_infra_classes": energy_counts,
        "water_wastewater_classes": water_counts,
        "communication_classes": comm_counts,
        "transport_hub_classes": transport_counts,
    }


def _empty_infra_metrics() -> dict:
    return {
        "energy_infra_count": 0.0,
        "water_wastewater_count": 0.0,
        "communication_count": 0.0,
        "transport_hub_count": 0.0,
        "energy_infra_classes": {},
        "water_wastewater_classes": {},
        "communication_classes": {},
        "transport_hub_classes": {},
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


def _relation_member_lines(
    el: dict,
    nodes: dict[int, tuple[float, float]],
    all_elements: list[dict],
) -> list[LineString]:
    """Mitglieds-Ways einer linearen Gewässer-Relation (``type=waterway``) als Linien.

    Anders als ``_relation_to_multipolygon`` werden die Segmente NICHT zu einem
    (bei Fluss-/Bach-Routen sinnlosen) Ring geschlossen, sondern einzeln als
    LineStrings geführt — so bleibt die Distanz zur Zelle korrekt linienbasiert
    statt über ein Riesenpolygon flächig auf 0 (⇒ Nähe 1) zu fallen.
    """
    ways_by_id = _ways_by_id(all_elements)
    lines: list[LineString] = []
    for member in el.get("members", []):
        if member.get("type") != "way":
            continue
        nds = ways_by_id.get(member.get("ref"))
        if not nds:
            continue
        coords = [nodes[n] for n in nds if n in nodes]
        if len(coords) >= 2:
            lines.append(LineString(coords))
    return lines


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
