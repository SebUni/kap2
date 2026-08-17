"""LoD2-Kacheln je bbox laden, parsen und kompakt cachen.

Ablauf je Anfrage (bbox im Overpass-Format ``s,w,n,e``, WGS84):
  1. Phase-1-Quelle fürs Bundesland? sonst None → OSM-Fallback.
  2. bbox → Kachelliste im Quell-CRS (km-Gitter mit Quell-Anker, +1 Kachel Rand).
  3. Kachel-URLs je nach Quellmechanismus (siehe sources.py):
     direktes URL-Muster / Kachel-Index (GeoJSON) / zweistufige Generierung
     (prepare-Endpunkt) / Stadt-Archive.
  4. Je Kachel: extrahierter Cache-Hit oder Download+Parse+Cache.
  5. LoD2 ersetzt OSM nur, wenn ≥ 90 % der Kacheln erfolgreich sind
     (HTTP 404 bzw. „nicht im Index" = leere Kachel zählt als Erfolg und wird
     als leer gecacht; Netzwerkfehler werden NICHT gecacht).

Cache-Layout (kompakt, gzip-JSON — Rohdaten-GML nur bei ``keep_raw=True``):
  data/lod2/extracted/{land_slug}/{e}_{n}.json.gz     (bzw. stadt_{i}.json.gz)
  data/lod2/extracted/{land_slug}/_index.json.gz      (Kachel-Index/ID-Map)
  → {"v": 1, "n": <Anzahl>, "b": [{"xy": [ring, …], "h": 7.4}, …]}
    (erster Ring = Außenring, weitere = Löcher; WGS84 lon/lat, 7 Nachkommastellen)
"""
from __future__ import annotations

import gzip
import io
import json
import logging
import math
import os
import re
import threading
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor
from xml.etree.ElementTree import ParseError as ET_ParseError

import httpx
from pyproj import Transformer
from shapely.geometry import MultiPolygon, Polygon

from app.config import settings
from .citygml import parse_citygml
from .sources import Lod2Source, source_for

log = logging.getLogger(__name__)

_download_lock = threading.Lock()
_CACHE_VERSION = 1
_MIN_TILE_SUCCESS = 0.9
_CITY_ARCHIVE_KEY = "stadt"  # Kachel-Schlüssel für Archiv-Quellen (+ _{i})
_INDEX_KEY = "_index"        # Cache-Schlüssel für Kachel-Indizes/ID-Maps
_index_ram: dict[str, dict[str, object]] = {}  # land → geparster Index
_index_lock = threading.Lock()  # 4 Download-Worker → Index nur einmal laden


def _land_slug(land: str) -> str:
    return (land.lower().replace(" ", "-").replace("ä", "ae")
            .replace("ö", "oe").replace("ü", "ue").replace("ß", "ss"))


def _extracted_path(land: str, key: str) -> str:
    return os.path.join(settings.LOD2_CACHE_DIR, "extracted",
                        _land_slug(land), f"{key}.json.gz")


def _tiles_for_bbox(bbox: str, src: Lod2Source) -> list[tuple[int, int]]:
    """bbox 's,w,n,e' (WGS84) → SW-Ecken (e_km, n_km) aller berührten Kacheln."""
    s, w, n, e = (float(v) for v in bbox.split(","))
    tr = Transformer.from_crs("EPSG:4326", src.crs, always_xy=True)
    xs, ys = [], []
    for lon, lat in ((w, s), (e, s), (w, n), (e, n)):
        x, y = tr.transform(lon, lat)
        xs.append(x)
        ys.append(y)
    step = src.tile_km
    ae, an = src.tile_anchor  # Rasteranker in km (BW: Ostwerte ungerade)

    def snap(v_m: float, anchor: int) -> int:
        return int(math.floor((v_m / 1000 - anchor) / step)) * step + anchor

    # +1 Kachel Rand, damit randständige Footprints nicht fehlen
    e0 = snap(min(xs), ae) - step
    e1 = snap(max(xs), ae) + step
    n0 = snap(min(ys), an) - step
    n1 = snap(max(ys), an) + step
    return [(ee, nn)
            for ee in range(e0, e1 + step, step)
            for nn in range(n0, n1 + step, step)]


def _rings_from_geom(geom) -> list[list[list[list[float]]]]:
    """(Multi)Polygon → Liste von Polygonen als [außen, loch, …]-Ringlisten."""
    polys = list(geom.geoms) if isinstance(geom, MultiPolygon) else [geom]
    out = []
    for p in polys:
        if p.is_empty or p.geom_type != "Polygon":
            continue
        rings = [[[round(x, 7), round(y, 7)] for x, y in p.exterior.coords]]
        for hole in p.interiors:
            rings.append([[round(x, 7), round(y, 7)] for x, y in hole.coords])
        out.append(rings)
    return out


def _geom_from_rings(rings: list) -> Polygon | MultiPolygon | None:
    polys = []
    for poly_rings in rings:
        if not poly_rings or len(poly_rings[0]) < 4:
            continue
        try:
            p = Polygon(poly_rings[0], poly_rings[1:])
            if not p.is_valid:
                p = p.buffer(0)
            if not p.is_empty:
                polys.append(p)
        except (ValueError, TypeError):
            continue
    if not polys:
        return None
    return polys[0] if len(polys) == 1 else MultiPolygon(polys)


def _write_extracted(path: str, buildings: list[tuple[object, float]]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    payload = {
        "v": _CACHE_VERSION,
        "n": len(buildings),
        "b": [{"xy": _rings_from_geom(g), "h": h} for g, h in buildings],
    }
    tmp = path + ".tmp"
    with gzip.open(tmp, "wt", encoding="utf-8") as fh:
        json.dump(payload, fh, separators=(",", ":"))
    os.replace(tmp, path)


def _read_extracted(path: str) -> list[dict] | None:
    try:
        with gzip.open(path, "rt", encoding="utf-8") as fh:
            payload = json.load(fh)
    except (OSError, ValueError):
        return None
    if payload.get("v") != _CACHE_VERSION:
        return None
    out = []
    for b in payload.get("b", []):
        geom = _geom_from_rings(b.get("xy", []))
        if geom is None:
            continue
        h = float(b.get("h", 0.0))
        out.append(_building_dict(geom, h))
    return out


def _building_dict(geom, height: float) -> dict:
    return {
        "geometry": geom,
        "height": height,
        "levels": max(1, round(height / 3.0)),
        "building_type": "lod2",
    }


def _parse_payload(content: bytes, src: Lod2Source) -> list[tuple[object, float]]:
    """Roh-Download (GML oder ZIP mit GML/XML-Dateien) → Gebäudeliste."""
    if src.archive in ("zip", "zip-city") or content[:2] == b"PK":
        buildings: list[tuple[object, float]] = []
        with zipfile.ZipFile(io.BytesIO(content)) as z:
            for name in z.namelist():
                if not name.lower().endswith((".gml", ".xml")):
                    continue
                with z.open(name) as fh:
                    buildings.extend(parse_citygml(fh, src.crs))
        return buildings
    return parse_citygml(io.BytesIO(content), src.crs)


def _download(urls: list[str], keep_raw: bool, raw_name: str,
              land: str) -> bytes | None:
    """Kandidaten-URLs durchprobieren. None = Kachel existiert nicht (404).

    Netzwerk-/Serverfehler werfen die letzte Exception weiter, damit der
    Aufrufer sie von "leere Kachel" unterscheiden kann.
    """
    last_exc: Exception | None = None
    for url in urls:
        for attempt in range(3):
            try:
                resp = httpx.get(
                    url, timeout=settings.LOD2_DOWNLOAD_TIMEOUT_S,
                    follow_redirects=True,
                )
                if resp.status_code == 404:
                    last_exc = None
                    break  # nächste Kandidaten-URL
                resp.raise_for_status()
                content = resp.content
                if keep_raw:
                    raw_dir = os.path.join(settings.LOD2_CACHE_DIR, "raw",
                                           _land_slug(land))
                    os.makedirs(raw_dir, exist_ok=True)
                    with open(os.path.join(raw_dir, raw_name), "wb") as fh:
                        fh.write(content)
                return content
            except httpx.HTTPError as exc:
                last_exc = exc
                if attempt < 2:
                    time.sleep(1.5 * (attempt + 1))
    if last_exc is not None:
        raise last_exc
    return None


def _resolve_city_archive_url(src: Lod2Source) -> str | None:
    """Ein-Archiv-Quellen (Hamburg): Resource-URL über CKAN-API auflösen."""
    try:
        resp = httpx.get(src.ckan_api, timeout=60, follow_redirects=True)
        resp.raise_for_status()
        data = resp.json()
        for res in data.get("result", {}).get("resources", []):
            fmt = (res.get("format") or "").lower()
            url = res.get("url") or ""
            if "gml" in fmt or "zip" in fmt or url.lower().endswith(
                    (".zip", ".gml")):
                return url
    except (httpx.HTTPError, ValueError) as exc:
        log.warning("LoD2 %s: CKAN-Auflösung fehlgeschlagen: %s", src.land, exc)
    return None


# ── Kachel-Index (NI, SH) und ID-Map (ST) ─────────────────────────────────────

def _index_cache_path(land: str) -> str:
    return _extracted_path(land, _INDEX_KEY)


def _parse_geojson_index(content: bytes, src: Lod2Source) -> dict[str, str]:
    """Index-GeoJSON → {"{e}_{n}": download_url}.

    Koordinaten aus ``index_coord_re`` auf die URL (SH) oder — falls leer —
    aus der Feature-Geometrie (NI; Index-CRS = Quell-CRS, Meter)."""
    data = json.loads(content)
    coord_re = re.compile(src.index_coord_re) if src.index_coord_re else None
    out: dict[str, str] = {}
    for feat in data.get("features", []):
        url = (feat.get("properties") or {}).get(src.index_url_prop)
        if not url:
            continue
        if coord_re is not None:
            m = coord_re.search(url)
            if not m:
                continue
            e_km, n_km = int(m.group(1)), int(m.group(2))
        else:
            try:
                ring = feat["geometry"]["coordinates"][0]
                e_km = int(round(min(p[0] for p in ring) / 1000))
                n_km = int(round(min(p[1] for p in ring) / 1000))
            except (KeyError, IndexError, TypeError, ValueError):
                continue
        out[f"{e_km}_{n_km}"] = url
    return out


def _parse_prepare_page(content: bytes, src: Lod2Source) -> dict[str, str]:
    """ST-Download-Seite → {"{e}_{n}": kachel_id} aus dem Inline-GeoJSON.

    Labels haben die Form ``32{E:3}{N:4}`` (zonenpräfixierter km-Index)."""
    html = content.decode("utf-8", errors="replace")
    out: dict[str, str] = {}
    for m in re.finditer(
            r'"id":\s*"(\d+)",\s*"label":\s*"32(\d{3})(\d{4})"', html):
        out[f"{int(m.group(2))}_{int(m.group(3))}"] = m.group(1)
    return out


def _ensure_index(src: Lod2Source) -> dict[str, str] | None:
    """Kachel-Index/ID-Map laden (RAM → Disk → Netz). None = Fetch-Fehler."""
    with _index_lock:
        return _ensure_index_locked(src)


def _ensure_index_locked(src: Lod2Source) -> dict[str, str] | None:
    cached = _index_ram.get(src.land)
    if cached is not None:
        return cached  # type: ignore[return-value]
    path = _index_cache_path(src.land)
    try:
        with gzip.open(path, "rt", encoding="utf-8") as fh:
            payload = json.load(fh)
        if payload.get("v") == _CACHE_VERSION and payload.get("map"):
            _index_ram[src.land] = payload["map"]
            return payload["map"]
    except (OSError, ValueError):
        pass

    url = src.index_url or src.prepare_page
    try:
        resp = httpx.get(url, timeout=settings.LOD2_DOWNLOAD_TIMEOUT_S,
                         follow_redirects=True)
        resp.raise_for_status()
        if src.index_url:
            mapping = _parse_geojson_index(resp.content, src)
        else:
            mapping = _parse_prepare_page(resp.content, src)
    except (httpx.HTTPError, ValueError) as exc:
        log.warning("LoD2 %s: Kachel-Index nicht ladbar: %s", src.land, exc)
        return None
    if not mapping:
        log.warning("LoD2 %s: Kachel-Index leer/unlesbar", src.land)
        return None
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with gzip.open(tmp, "wt", encoding="utf-8") as fh:
        json.dump({"v": _CACHE_VERSION, "map": mapping}, fh,
                  separators=(",", ":"))
    os.replace(tmp, path)
    _index_ram[src.land] = mapping
    log.info("LoD2 %s: Kachel-Index geladen (%d Einträge)",
             src.land, len(mapping))
    return mapping


def _tile_urls(src: Lod2Source, e_km: int, n_km: int) -> list[str] | None:
    """Download-URLs einer Kachel je nach Quellmechanismus.

    [] = Kachel existiert nicht (gültig leer); None = Adapter-Fehler."""
    key = f"{e_km}_{n_km}"
    if src.index_url:
        mapping = _ensure_index(src)
        if mapping is None:
            return None
        url = mapping.get(key)
        return [url] if url else []
    if src.prepare_page:
        mapping = _ensure_index(src)
        if mapping is None:
            return None
        item_id = mapping.get(key)
        if not item_id:
            return []
        try:
            resp = httpx.get(f"{src.prepare_endpoint}?items={item_id}&format=zip",
                             timeout=settings.LOD2_DOWNLOAD_TIMEOUT_S,
                             follow_redirects=True)
            resp.raise_for_status()
            url = resp.text.strip()
        except httpx.HTTPError as exc:
            log.warning("LoD2 %s Kachel %s: prepare fehlgeschlagen: %s",
                        src.land, key, exc)
            return None
        return [url] if url.startswith("http") else None
    return src.url_builder(e_km, n_km) or None


def _ensure_tile(src: Lod2Source, e_km: int, n_km: int,
                 keep_raw: bool = False) -> list[dict] | None:
    """Gebäude einer Kachel (Cache oder Download). None = Fetch-Fehler."""
    key = f"{e_km}_{n_km}"
    path = _extracted_path(src.land, key)
    cached = _read_extracted(path)
    if cached is not None:
        return cached
    urls = _tile_urls(src, e_km, n_km)
    if urls is None:
        return None
    if not urls:
        # nicht im Index = Kachel ohne Gebäude/außerhalb → als leer cachen
        _write_extracted(path, [])
        return []
    try:
        content = _download(urls, keep_raw, f"{key}.{src.archive}", src.land)
    except httpx.HTTPError as exc:
        log.warning("LoD2 %s Kachel %s: Download fehlgeschlagen: %s",
                    src.land, key, exc)
        return None
    if content is None:
        # 404 = Kachel ohne Gebäude/außerhalb der Abdeckung → als leer cachen
        _write_extracted(path, [])
        return []
    try:
        buildings = _parse_payload(content, src)
    except (ET_ParseError, zipfile.BadZipFile, ValueError) as exc:
        log.warning("LoD2 %s Kachel %s: Parse-Fehler: %s", src.land, key, exc)
        return None
    _write_extracted(path, buildings)
    return [_building_dict(g, h) for g, h in buildings]


def _ensure_city_archive(src: Lod2Source, keep_raw: bool) -> list[dict] | None:
    """Archiv-Quellen (HH, HB): Gesamtbestand einmalig laden, je Teil cachen."""
    if src.city_urls:
        urls = list(src.city_urls)
    else:
        resolved = _resolve_city_archive_url(src)
        if not resolved:
            return None
        urls = [resolved]

    all_buildings: list[dict] = []
    for i, url in enumerate(urls):
        part_key = _CITY_ARCHIVE_KEY if len(urls) == 1 else f"{_CITY_ARCHIVE_KEY}_{i}"
        path = _extracted_path(src.land, part_key)
        cached = _read_extracted(path)
        if cached is not None:
            all_buildings.extend(cached)
            continue
        try:
            content = _download([url], keep_raw, f"{part_key}.zip", src.land)
        except httpx.HTTPError as exc:
            log.warning("LoD2 %s: Archiv-Download fehlgeschlagen (%s): %s",
                        src.land, url, exc)
            return None
        if content is None:
            return None
        try:
            buildings = _parse_payload(content, src)
        except (ET_ParseError, zipfile.BadZipFile, ValueError) as exc:
            log.warning("LoD2 %s: Archiv-Parse-Fehler: %s", src.land, exc)
            return None
        _write_extracted(path, buildings)
        all_buildings.extend(_building_dict(g, h) for g, h in buildings)
    return all_buildings


def fetch_lod2_buildings(bbox: str, bundesland: str | None,
                         keep_raw: bool = False) -> list[dict] | None:
    """LoD2-Gebäude für eine bbox ('s,w,n,e', WGS84) oder None (→ OSM-Fallback).

    Rückgabe-Dicts sind kompatibel zum OSM-Gebäudeformat aus
    ``fetch_buildings_and_roads``: geometry (WGS84), height, levels,
    building_type ("lod2").
    """
    if not settings.LOD2_ENABLED:
        return None
    src = source_for(bundesland)
    if src is None:
        return None

    s, w, n, e = (float(v) for v in bbox.split(","))

    with _download_lock:
        if src.tile_km == 0:
            buildings = _ensure_city_archive(src, keep_raw)
            if buildings is None:
                return None
        else:
            tiles = _tiles_for_bbox(bbox, src)
            if len(tiles) > settings.LOD2_MAX_TILES:
                log.warning(
                    "LoD2 %s: %d Kacheln > LOD2_MAX_TILES=%d — OSM-Fallback",
                    src.land, len(tiles), settings.LOD2_MAX_TILES)
                return None
            results: list[list[dict] | None] = []
            with ThreadPoolExecutor(max_workers=4) as pool:
                results = list(pool.map(
                    lambda t: _ensure_tile(src, t[0], t[1], keep_raw), tiles))
            failed = sum(1 for r in results if r is None)
            if len(tiles) - failed < len(tiles) * _MIN_TILE_SUCCESS:
                log.warning(
                    "LoD2 %s: %d/%d Kacheln fehlgeschlagen — OSM-Fallback",
                    src.land, failed, len(tiles))
                return None
            if failed:
                log.warning("LoD2 %s: %d/%d Kacheln fehlgeschlagen (toleriert)",
                            src.land, failed, len(tiles))
            buildings = [b for r in results if r for b in r]

    # Auf bbox zuschneiden (Kacheln + Rand liefern mehr als angefragt;
    # Stadt-Archiv sowieso) — grober Envelope-Filter reicht hier.
    out = [b for b in buildings
           if b["geometry"].bounds[0] <= e and b["geometry"].bounds[2] >= w
           and b["geometry"].bounds[1] <= n and b["geometry"].bounds[3] >= s]
    log.info("LoD2 %s: %d Gebäude für bbox geladen (Quelle amtlich, %s)",
             src.land, len(out), src.license)
    return out
