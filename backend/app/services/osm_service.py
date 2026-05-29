import logging
import httpx
from typing import Optional

from app.config import settings

logger = logging.getLogger(__name__)

# Overpass mirrors – tried in order if primary fails
_OVERPASS_URLS = [
    settings.OVERPASS_URL,
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
]


async def search_kommune(query: str, limit: int = 10) -> list[dict]:
    """Search for a municipality via OSM Nominatim."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{settings.NOMINATIM_URL}/search",
            params={
                "q": query,
                "format": "json",
                "addressdetails": 1,
                "limit": limit,
                "countrycodes": "de",
                "featuretype": "settlement",
                "polygon_geojson": 1,
            },
            headers={"User-Agent": settings.NOMINATIM_USER_AGENT},
            timeout=15.0,
        )
        resp.raise_for_status()
        results = resp.json()

    out = []
    for r in results:
        out.append({
            "name": r.get("name", r.get("display_name", "").split(",")[0]),
            "osm_id": str(r.get("osm_id", "")),
            "osm_type": r.get("osm_type", ""),
            "display_name": r.get("display_name", ""),
            "lat": float(r.get("lat", 0)),
            "lon": float(r.get("lon", 0)),
            "address": r.get("address", {}),
            "geojson": r.get("geojson"),
        })
    return out


async def fetch_kommune_boundary(osm_id: str, osm_type: str = "relation",
                                  nominatim_geojson: Optional[dict] = None) -> Optional[dict]:
    """Fetch municipality boundary as GeoJSON.

    1. Use pre-fetched Nominatim geometry if available.
    2. Fall back to Nominatim lookup with polygon_geojson=1.
    3. Fall back to Overpass API (with mirrors).
    """
    # ── 1. Use Nominatim geometry passed from search ──────────────────
    if nominatim_geojson:
        geojson = _normalize_to_multi(nominatim_geojson)
        if geojson:
            logger.info("Using Nominatim pre-fetched geometry for osm_id=%s", osm_id)
            return geojson

    # ── 2. Nominatim lookup ───────────────────────────────────────────
    try:
        geojson = await _fetch_via_nominatim(osm_id, osm_type)
        if geojson:
            logger.info("Got boundary via Nominatim lookup for osm_id=%s", osm_id)
            return geojson
    except Exception as e:
        logger.warning("Nominatim lookup failed for osm_id=%s: %s", osm_id, e)

    # ── 3. Overpass (try mirrors) ─────────────────────────────────────
    for url in _OVERPASS_URLS:
        try:
            geojson = await _fetch_via_overpass(osm_id, osm_type, url)
            if geojson:
                logger.info("Got boundary via Overpass (%s) for osm_id=%s", url, osm_id)
                return geojson
        except Exception as e:
            logger.warning("Overpass %s failed for osm_id=%s: %s", url, osm_id, e)

    return None


async def _fetch_via_nominatim(osm_id: str, osm_type: str = "relation") -> Optional[dict]:
    """Fetch boundary via Nominatim reverse/lookup with polygon_geojson."""
    osm_letter = {"relation": "R", "way": "W", "node": "N"}.get(osm_type, "R")
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{settings.NOMINATIM_URL}/lookup",
            params={
                "osm_ids": f"{osm_letter}{osm_id}",
                "format": "json",
                "polygon_geojson": 1,
            },
            headers={"User-Agent": settings.NOMINATIM_USER_AGENT},
            timeout=20.0,
        )
        resp.raise_for_status()
        data = resp.json()

    if not data:
        return None
    geojson = data[0].get("geojson")
    return _normalize_to_multi(geojson) if geojson else None


async def _fetch_via_overpass(osm_id: str, osm_type: str, overpass_url: str) -> Optional[dict]:
    """Fetch boundary from an Overpass API endpoint."""
    type_prefix = {"node": "node", "way": "way", "relation": "rel"}.get(osm_type, "rel")

    query = f"""
    [out:json][timeout:30];
    {type_prefix}({osm_id});
    out geom;
    """

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            overpass_url,
            data={"data": query},
            timeout=60.0,
        )
        resp.raise_for_status()
        data = resp.json()

    elements = data.get("elements", [])
    if not elements:
        return None

    element = elements[0]

    # Build GeoJSON from Overpass response
    if "members" in element:
        outer_coords = []
        for member in element.get("members", []):
            if member.get("role") == "outer" and "geometry" in member:
                ring = [(pt["lon"], pt["lat"]) for pt in member["geometry"]]
                outer_coords.append(ring)

        if not outer_coords:
            return None

        merged = _merge_rings(outer_coords)

        if len(merged) == 1:
            return {"type": "MultiPolygon", "coordinates": [[merged[0]]]}
        else:
            return {"type": "MultiPolygon", "coordinates": [[ring] for ring in merged]}

    elif "geometry" in element:
        coords = [(pt["lon"], pt["lat"]) for pt in element["geometry"]]
        return {"type": "MultiPolygon", "coordinates": [[[coords]]]}

    return None


def _normalize_to_multi(geojson: dict) -> Optional[dict]:
    """Ensure the geometry is a MultiPolygon."""
    gtype = geojson.get("type")
    coords = geojson.get("coordinates")
    if not gtype or not coords:
        return None
    if gtype == "MultiPolygon":
        return geojson
    if gtype == "Polygon":
        return {"type": "MultiPolygon", "coordinates": [coords]}
    # Ignore points / lines
    return None


def _merge_rings(rings: list[list]) -> list[list]:
    """Merge disconnected way segments into closed rings."""
    if not rings:
        return rings

    merged = []
    remaining = list(rings)

    while remaining:
        current = list(remaining.pop(0))

        changed = True
        while changed:
            changed = False
            for i, ring in enumerate(remaining):
                if not ring:
                    continue
                # Check if current's last point matches ring's first point
                if _points_close(current[-1], ring[0]):
                    current.extend(ring[1:])
                    remaining.pop(i)
                    changed = True
                    break
                # Check reverse
                elif _points_close(current[-1], ring[-1]):
                    current.extend(reversed(ring[:-1]))
                    remaining.pop(i)
                    changed = True
                    break
                elif _points_close(current[0], ring[-1]):
                    current = list(ring[:-1]) + current
                    remaining.pop(i)
                    changed = True
                    break
                elif _points_close(current[0], ring[0]):
                    current = list(reversed(ring[1:])) + current
                    remaining.pop(i)
                    changed = True
                    break

        # Close ring if not already closed
        if current and not _points_close(current[0], current[-1]):
            current.append(current[0])

        merged.append(current)

    return merged


def _points_close(a: tuple, b: tuple, tol: float = 1e-6) -> bool:
    return abs(a[0] - b[0]) < tol and abs(a[1] - b[1]) < tol
