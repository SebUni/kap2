"""Echter Sky-View-Faktor per Horizontwinkel-Verfahren auf Gebäudehöhenraster.

Formel (Oke 1981; Zakšek, Oštir & Kokalj 2011, Remote Sens. 3(2):398–415):

    SVF = 1 − (1/N) · Σᵢ sin²(γᵢ),   γᵢ = max über Strahl i von atan(h/d)

mit N Azimutrichtungen (Default 16) und Suchradius R (Default 100 m) auf einem
Gebäudehöhenraster (Default 5 m, aus LoD2- oder OSM-Footprints+Höhen).
Beobachter auf Bodenniveau: reines Gebäude-Canyon-SVF ohne Gelände — genau die
Größe, die der UHI-Canyon-Term ``ε·(1−svf)·height_factor`` erwartet.

Je Analysezelle wird über die NICHT überbauten Pixel (Straßenniveau) gemittelt;
vollständig überbaute Zellen mitteln über alle Pixel. Zellen ohne Gebäude im
Umkreis erhalten 1,0 (freier Himmel).
"""
from __future__ import annotations

import gzip
import hashlib
import json
import logging
import math
import os
import threading
import time

import numpy as np
from pyproj import Transformer
from shapely import contains_xy
from shapely.geometry import MultiPolygon, Polygon

from app.config import settings

log = logging.getLogger(__name__)

_ram_lock = threading.Lock()
_ram_cache: dict[str, tuple[float, list[float]]] = {}  # Single-Entry, TTL
_RAM_TTL_S = 3600

_TO_UTM = Transformer.from_crs("EPSG:4326", f"EPSG:{settings.CALCULATION_SRID}",
                               always_xy=True)


def _cache_key(grid_cells: list[dict], buildings: list[dict],
               source: str) -> str:
    b0 = grid_cells[0]["geometry"].bounds if grid_cells else (0, 0, 0, 0)
    b1 = grid_cells[-1]["geometry"].bounds if grid_cells else (0, 0, 0, 0)
    raw = (f"{b0}|{b1}|{len(grid_cells)}|{source}|{len(buildings)}|"
           f"{settings.SVF_RESOLUTION_M}|{settings.SVF_RADIUS_M}|"
           f"{settings.SVF_DIRECTIONS}")
    return hashlib.sha1(raw.encode()).hexdigest()


def _disk_path(key: str) -> str:
    return os.path.join(settings.LOD2_CACHE_DIR, "svf", f"{key}.json.gz")


def _rasterize_heights(buildings: list[dict], bounds: tuple[float, float, float, float],
                       res_m: float) -> tuple[np.ndarray, float, float]:
    """Gebäude (WGS84-Geometrien + height) → Höhenraster in UTM.

    Rückgabe: (H[row, col], x0, y0) — Zeile 0 liegt bei y0 (Süden), d. h.
    row wächst nach Norden; x0/y0 sind die Koordinaten des Pixel-ZENTRUMS (0,0).
    """
    x0, y0, x1, y1 = bounds
    ncols = max(1, int(math.ceil((x1 - x0) / res_m)))
    nrows = max(1, int(math.ceil((y1 - y0) / res_m)))
    H = np.zeros((nrows, ncols), dtype=np.float32)

    for b in buildings:
        h = float(b.get("height", 0.0))
        if h <= 0:
            continue
        geom = b["geometry"]
        polys = list(geom.geoms) if isinstance(geom, MultiPolygon) else [geom]
        for poly in polys:
            if poly.is_empty or not hasattr(poly, "exterior"):
                continue
            xs, ys = poly.exterior.coords.xy
            ux, uy = _TO_UTM.transform(np.asarray(xs), np.asarray(ys))
            try:
                p_utm = Polygon(list(zip(ux, uy)))
            except (ValueError, TypeError):
                continue
            if p_utm.is_empty or not p_utm.is_valid:
                p_utm = p_utm.buffer(0)
                if p_utm.is_empty:
                    continue
            bx0, by0, bx1, by1 = p_utm.bounds
            c0 = max(0, int((bx0 - x0) / res_m))
            c1 = min(ncols - 1, int((bx1 - x0) / res_m))
            r0 = max(0, int((by0 - y0) / res_m))
            r1 = min(nrows - 1, int((by1 - y0) / res_m))
            if c1 < c0 or r1 < r0:
                continue
            px = x0 + (np.arange(c0, c1 + 1) + 0.5) * res_m
            py = y0 + (np.arange(r0, r1 + 1) + 0.5) * res_m
            PX, PY = np.meshgrid(px, py)
            mask = contains_xy(p_utm, PX, PY)
            if not mask.any():
                # Kleinstgebäude unterhalb Rasterauflösung: Zentrumspixel setzen
                cx, cy = p_utm.centroid.x, p_utm.centroid.y
                cc = int((cx - x0) / res_m)
                rr = int((cy - y0) / res_m)
                if 0 <= rr < nrows and 0 <= cc < ncols:
                    H[rr, cc] = max(H[rr, cc], h)
                continue
            win = H[r0:r1 + 1, c0:c1 + 1]
            win[mask] = np.maximum(win[mask], h)
    return H, x0, y0


def _shift(a: np.ndarray, dy: int, dx: int) -> np.ndarray:
    """Array um (dy, dx) verschieben, Ränder mit 0 auffüllen (kein Wraparound)."""
    out = np.zeros_like(a)
    src_r = slice(max(0, -dy), a.shape[0] - max(0, dy))
    src_c = slice(max(0, -dx), a.shape[1] - max(0, dx))
    dst_r = slice(max(0, dy), a.shape[0] - max(0, -dy))
    dst_c = slice(max(0, dx), a.shape[1] - max(0, -dx))
    out[dst_r, dst_c] = a[src_r, src_c]
    return out


def _horizon_svf(H: np.ndarray, res_m: float, radius_m: float,
                 n_dirs: int) -> np.ndarray:
    """SVF je Pixel: 1 − (1/N)·Σ sin²(max. Horizontwinkel je Richtung)."""
    n_steps = max(1, int(round(radius_m / res_m)))
    sum_sin2 = np.zeros_like(H, dtype=np.float32)
    for i in range(n_dirs):
        phi = 2.0 * math.pi * i / n_dirs
        cphi, sphi = math.cos(phi), math.sin(phi)
        tan_max = np.zeros_like(H, dtype=np.float32)
        for k in range(1, n_steps + 1):
            dx = int(round(k * cphi))
            dy = int(round(k * sphi))
            if dx == 0 and dy == 0:
                continue
            dist = math.hypot(dx, dy) * res_m
            # Höhe der Zelle in Richtung φ, Entfernung k — verschoben ZU uns:
            # Pixel (r,c) sieht H[r+dy, c+dx], also Shift um (-dy, -dx).
            shifted = _shift(H, -dy, -dx)
            np.maximum(tan_max, shifted / dist, out=tan_max)
        t2 = tan_max * tan_max
        sum_sin2 += t2 / (1.0 + t2)
    return 1.0 - sum_sin2 / float(n_dirs)


def compute_svf_for_cells(grid_cells: list[dict], buildings: list[dict],
                          building_source: str = "osm") -> list[float]:
    """SVF je Analysezelle (Reihenfolge = ``grid_cells``), Werte in [0, 1]."""
    if not grid_cells:
        return []
    if not buildings:
        return [1.0] * len(grid_cells)

    key = _cache_key(grid_cells, buildings, building_source)

    with _ram_lock:
        hit = _ram_cache.get(key)
        if hit and time.time() - hit[0] < _RAM_TTL_S:
            return list(hit[1])

    disk = _disk_path(key)
    try:
        with gzip.open(disk, "rt", encoding="utf-8") as fh:
            vals = json.load(fh)
        if isinstance(vals, list) and len(vals) == len(grid_cells):
            with _ram_lock:
                _ram_cache.clear()
                _ram_cache[key] = (time.time(), vals)
            return list(vals)
    except (OSError, ValueError):
        pass

    t0 = time.time()
    res_m = float(settings.SVF_RESOLUTION_M)
    radius = float(settings.SVF_RADIUS_M)

    # Gesamt-bbox aller Zellen in UTM + Suchradius-Puffer
    minx = miny = float("inf")
    maxx = maxy = float("-inf")
    cell_bounds_utm: list[tuple[float, float, float, float]] = []
    for cell in grid_cells:
        w, s, e, n = cell["geometry"].bounds
        ux, uy = _TO_UTM.transform(np.array([w, e]), np.array([s, n]))
        cb = (float(min(ux)), float(min(uy)), float(max(ux)), float(max(uy)))
        cell_bounds_utm.append(cb)
        minx, miny = min(minx, cb[0]), min(miny, cb[1])
        maxx, maxy = max(maxx, cb[2]), max(maxy, cb[3])
    bounds = (minx - radius, miny - radius, maxx + radius, maxy + radius)

    # Speichergrenze: Auflösung vergröbern statt scheitern
    while ((bounds[2] - bounds[0]) / res_m) * ((bounds[3] - bounds[1]) / res_m) \
            > settings.SVF_MAX_PIXELS:
        res_m *= 2.0
        log.warning("SVF: Raster > SVF_MAX_PIXELS — Auflösung vergröbert auf %.0f m",
                    res_m)

    H, x0, y0 = _rasterize_heights(buildings, bounds, res_m)
    svf_px = _horizon_svf(H, res_m, radius, int(settings.SVF_DIRECTIONS))

    out: list[float] = []
    nrows, ncols = H.shape
    for cb in cell_bounds_utm:
        c0 = max(0, int((cb[0] - x0) / res_m))
        c1 = min(ncols, int(math.ceil((cb[2] - x0) / res_m)))
        r0 = max(0, int((cb[1] - y0) / res_m))
        r1 = min(nrows, int(math.ceil((cb[3] - y0) / res_m)))
        if c1 <= c0 or r1 <= r0:
            out.append(1.0)
            continue
        win_svf = svf_px[r0:r1, c0:c1]
        win_h = H[r0:r1, c0:c1]
        street = win_h == 0.0
        vals = win_svf[street] if street.any() else win_svf
        out.append(round(float(vals.mean()), 3))

    log.info("SVF: %d Zellen, Raster %dx%d px @ %.0f m, Quelle %s, %.1f s",
             len(grid_cells), nrows, ncols, res_m, building_source,
             time.time() - t0)

    try:
        os.makedirs(os.path.dirname(disk), exist_ok=True)
        tmp = disk + ".tmp"
        with gzip.open(tmp, "wt", encoding="utf-8") as fh:
            json.dump(out, fh)
        os.replace(tmp, disk)
    except OSError as exc:
        log.warning("SVF: Disk-Cache nicht schreibbar: %s", exc)
    with _ram_lock:
        _ram_cache.clear()
        _ram_cache[key] = (time.time(), out)
    return out
