"""Geländeanalyse aus AWS Terrarium-Höhentiles (Mapzen-Format).

Pro Rasterzelle: Mittelhöhe, Hangneigung, Senkentiefe, D8-Abflussakkumulation
und Topographic Wetness Index (TWI). Ergebnisse werden pro BBox gecacht.
"""

from __future__ import annotations

import io
import logging
import math
import threading
import time as _time
from typing import Any

import httpx
import numpy as np
from PIL import Image
from shapely.geometry import Point
from shapely.ops import unary_union

from app.config import settings

log = logging.getLogger(__name__)

TERRARIUM_URL = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"
TILE_SIZE = 256
_CACHE_TTL = 3600  # 1 h

_cache_lock = threading.Lock()
_tile_cache: dict[tuple[int, int, int], tuple[float, np.ndarray]] = {}
_dem_cache: dict[str, tuple[float, dict]] = {}

# D8-Nachbarn: (d_row, d_col, Distanzfaktor für Hang)
_D8 = (
    (-1, 0, 1.0), (1, 0, 1.0), (0, -1, 1.0), (0, 1, 1.0),
    (-1, -1, math.sqrt(2)), (-1, 1, math.sqrt(2)),
    (1, -1, math.sqrt(2)), (1, 1, math.sqrt(2)),
)


def _decode_terrarium(rgb: np.ndarray) -> np.ndarray:
    """RGB-Array (H×W×3) → Höhen in Metern."""
    r = rgb[:, :, 0].astype(np.float64)
    g = rgb[:, :, 1].astype(np.float64)
    b = rgb[:, :, 2].astype(np.float64)
    elev = (r * 256.0 + g + b / 256.0) - 32768.0
    elev[elev < -500.0] = np.nan
    return elev


def _lon_lat_to_tile(lon: float, lat: float, zoom: int) -> tuple[int, int]:
    n = 2 ** zoom
    x = int((lon + 180.0) / 360.0 * n)
    lat_rad = math.radians(lat)
    y = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return x, y


def _tile_bounds(zoom: int, x: int, y: int) -> tuple[float, float, float, float]:
    """West, south, east, north in WGS84."""
    n = 2 ** zoom
    west = x / n * 360.0 - 180.0
    east = (x + 1) / n * 360.0 - 180.0
    north = math.degrees(math.atan(math.sinh(math.pi * (1.0 - 2.0 * y / n))))
    south = math.degrees(math.atan(math.sinh(math.pi * (1.0 - 2.0 * (y + 1) / n))))
    return west, south, east, north


def _fetch_tile(zoom: int, x: int, y: int) -> np.ndarray:
    key = (zoom, x, y)
    with _cache_lock:
        cached = _tile_cache.get(key)
        if cached and _time.time() - cached[0] < _CACHE_TTL:
            return cached[1]

    url = TERRARIUM_URL.format(z=zoom, x=x, y=y)
    try:
        with httpx.Client(timeout=30.0) as client:
            resp = client.get(url, headers={"User-Agent": settings.NOMINATIM_USER_AGENT})
            resp.raise_for_status()
            img = Image.open(io.BytesIO(resp.content)).convert("RGB")
            elev = _decode_terrarium(np.array(img))
    except Exception as exc:
        log.warning("Terrarium tile %s failed: %s", url, exc)
        elev = np.full((TILE_SIZE, TILE_SIZE), np.nan)

    with _cache_lock:
        _tile_cache[key] = (_time.time(), elev)
    return elev


def _select_zoom(cell_size_m: float, lat: float) -> int:
    """Zoom-Stufe: mindestens ~4 Pixel je Zelle."""
    for z in range(15, 9, -1):
        mpp = 156543.03 * math.cos(math.radians(lat)) / (2 ** z)
        if mpp <= cell_size_m / 4.0:
            return z
    return 11


def _build_dem_mosaic(
    west: float, south: float, east: float, north: float, zoom: int,
) -> dict:
    """Stitch Terrarium-Tiles zu einem durchgängigen DEM-Raster."""
    x0, y0 = _lon_lat_to_tile(west, north, zoom)
    x1, y1 = _lon_lat_to_tile(east, south, zoom)
    xs = list(range(min(x0, x1), max(x0, x1) + 1))
    ys = list(range(min(y0, y1), max(y0, y1) + 1))

    rows = len(ys) * TILE_SIZE
    cols = len(xs) * TILE_SIZE
    mosaic = np.full((rows, cols), np.nan)

    for yi, ty in enumerate(ys):
        for xi, tx in enumerate(xs):
            tile = _fetch_tile(zoom, tx, ty)
            r0, c0 = yi * TILE_SIZE, xi * TILE_SIZE
            mosaic[r0:r0 + TILE_SIZE, c0:c0 + TILE_SIZE] = tile

    west_b, _, _, north_b = _tile_bounds(zoom, xs[0], ys[0])
    _, south_b, east_b, _ = _tile_bounds(zoom, xs[-1], ys[-1])

    return {
        "elev": mosaic,
        "west": west_b,
        "south": south_b,
        "east": east_b,
        "north": north_b,
        "zoom": zoom,
        "nrows": rows,
        "ncols": cols,
    }


def _elev_at(dem: dict, lon: float, lat: float) -> float:
    """Bilineare Interpolation im DEM-Mosaik."""
    west, south = dem["west"], dem["south"]
    east, north = dem["east"], dem["north"]
    nrows, ncols = dem["nrows"], dem["ncols"]
    if lon < west or lon > east or lat < south or lat > north:
        return float("nan")
    col_f = (lon - west) / (east - west) * (ncols - 1)
    row_f = (north - lat) / (north - south) * (nrows - 1)
    if not (0 <= row_f <= nrows - 1 and 0 <= col_f <= ncols - 1):
        return float("nan")
    r0, c0 = int(row_f), int(col_f)
    r1, c1 = min(r0 + 1, nrows - 1), min(c0 + 1, ncols - 1)
    dr, dc = row_f - r0, col_f - c0
    arr = dem["elev"]
    v00, v01 = arr[r0, c0], arr[r0, c1]
    v10, v11 = arr[r1, c0], arr[r1, c1]
    vals = [v for v in (v00, v01, v10, v11) if not np.isnan(v)]
    if not vals:
        return float("nan")
    if np.isnan(v00) or np.isnan(v01) or np.isnan(v10) or np.isnan(v11):
        return float(np.nanmean(vals))
    return float(
        v00 * (1 - dr) * (1 - dc)
        + v01 * (1 - dr) * dc
        + v10 * dr * (1 - dc)
        + v11 * dr * dc
    )


def _sample_cell_elevation(cell_geom: Any, dem: dict, n: int = 5) -> float:
    """Mittelhöhe über ein regelmäßiges Punktgitter in der Zelle."""
    minx, miny, maxx, maxy = cell_geom.bounds
    samples: list[float] = []
    for i in range(n):
        for j in range(n):
            x = minx + (maxx - minx) * (i + 0.5) / n
            y = miny + (maxy - miny) * (j + 0.5) / n
            pt = Point(x, y)
            if not cell_geom.contains(pt) and not cell_geom.intersects(pt):
                continue
            e = _elev_at(dem, x, y)
            if not math.isnan(e):
                samples.append(e)
    if not samples:
        cx, cy = cell_geom.centroid.x, cell_geom.centroid.y
        e = _elev_at(dem, cx, cy)
        return e if not math.isnan(e) else 0.0
    return float(np.mean(samples))


def _fill_nan_nearest(grid: np.ndarray) -> np.ndarray:
    """Füllt NaN-Lücken (außerhalb Gemeinde) mit Nachbar-Mittel für Hydrologie."""
    filled = grid.copy()
    mask = np.isnan(filled)
    if not mask.any():
        return filled
    for _ in range(10):
        new = filled.copy()
        rows, cols = filled.shape
        for i in range(rows):
            for j in range(cols):
                if not np.isnan(filled[i, j]):
                    continue
                vals = []
                for di in (-1, 0, 1):
                    for dj in (-1, 0, 1):
                        if di == 0 and dj == 0:
                            continue
                        ni, nj = i + di, j + dj
                        if 0 <= ni < rows and 0 <= nj < cols and not np.isnan(filled[ni, nj]):
                            vals.append(filled[ni, nj])
                if vals:
                    new[i, j] = float(np.mean(vals))
        filled = new
        if not np.isnan(filled).any():
            break
    global_mean = float(np.nanmean(grid))
    filled[np.isnan(filled)] = global_mean if not math.isnan(global_mean) else 0.0
    return filled


def _compute_slope_grid(elev: np.ndarray, cell_size_m: float) -> np.ndarray:
    """Hangneigung in Radiant (Horn-Operator)."""
    rows, cols = elev.shape
    slope = np.zeros((rows, cols))
    for i in range(rows):
        for j in range(cols):
            z = elev[i, j]
            z_w = elev[i, j - 1] if j > 0 else z
            z_e = elev[i, j + 1] if j < cols - 1 else z
            z_n = elev[i - 1, j] if i > 0 else z
            z_s = elev[i + 1, j] if i < rows - 1 else z
            dzdx = (z_e - z_w) / (2.0 * cell_size_m)
            dzdy = (z_s - z_n) / (2.0 * cell_size_m)
            slope[i, j] = math.atan(math.sqrt(dzdx * dzdx + dzdy * dzdy))
    return slope


def _compute_sink_depth(elev: np.ndarray) -> np.ndarray:
    """Senkentiefe: positiver Wert = Zelle liegt unter Nachbarn."""
    rows, cols = elev.shape
    sink = np.zeros((rows, cols))
    for i in range(rows):
        for j in range(cols):
            nb = []
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if di == 0 and dj == 0:
                        continue
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols:
                        nb.append(elev[ni, nj])
            if nb:
                sink[i, j] = max(0.0, float(np.mean(nb)) - elev[i, j])
    return sink


def _d8_flow_accumulation(elev: np.ndarray) -> np.ndarray:
    """D8-Abflussakkumulation (Einheiten: Anzahl upstream-Zellen)."""
    rows, cols = elev.shape
    acc = np.ones((rows, cols), dtype=np.float64)
    order = np.argsort(elev.ravel())[::-1]
    for flat_idx in order:
        i, j = divmod(int(flat_idx), cols)
        z = elev[i, j]
        best_drop = 0.0
        best: tuple[int, int] | None = None
        for di, dj, _ in _D8:
            ni, nj = i + di, j + dj
            if 0 <= ni < rows and 0 <= nj < cols:
                drop = z - elev[ni, nj]
                if drop > best_drop:
                    best_drop = drop
                    best = (ni, nj)
        if best is not None:
            acc[best[0], best[1]] += acc[i, j]
    return acc


def _compute_twi(flow_acc: np.ndarray, slope_rad: np.ndarray, cell_size_m: float) -> np.ndarray:
    """Topographic Wetness Index: ln(A / tan(β))."""
    a = np.maximum(flow_acc, 1.0) * (cell_size_m ** 2)
    tan_beta = np.maximum(np.tan(np.maximum(slope_rad, 0.001)), 0.001)
    return np.log(a / tan_beta)


def _normalize(arr: np.ndarray, valid_mask: np.ndarray) -> np.ndarray:
    vals = arr[valid_mask]
    if vals.size == 0:
        return np.zeros_like(arr)
    lo, hi = float(np.min(vals)), float(np.max(vals))
    if hi <= lo:
        return np.zeros_like(arr)
    out = (arr - lo) / (hi - lo)
    out[~valid_mask] = 0.0
    return np.clip(out, 0.0, 1.0)


def compute_terrain_for_cells(
    grid_cells: list[dict],
    progress_callback: Any = None,
) -> dict[int, dict]:
    """Berechnet Geländemetriken je Zellenindex (Position in ``grid_cells``).

    Returns ``{cell_index: {mean_elevation_m, slope_deg, slope_norm, sink_depth_m,
    sink_norm, flow_accum, twi, twi_norm, depression_factor, slope_factor}}``.
    """
    if not grid_cells:
        return {}

    cache_key = _bbox_key(grid_cells)
    with _cache_lock:
        cached = _dem_cache.get(cache_key)
        if cached and _time.time() - cached[0] < _CACHE_TTL:
            return cached[1]

    all_geoms = [c["geometry"] for c in grid_cells]
    combined = unary_union(all_geoms)
    west, south, east, north = combined.bounds
    lat_center = (south + north) / 2.0
    cell_size_m = float(grid_cells[0].get("cell_size_m", 100))
    zoom = _select_zoom(cell_size_m, lat_center)

    if progress_callback:
        progress_callback(12.0, "Lade Höhenmodell (Terrarium)")

    dem = _build_dem_mosaic(west, south, east, north, zoom)

    if progress_callback:
        progress_callback(18.0, "Berechne Zellhöhen")

    # Höhe je Zelle
    cell_elev: dict[tuple[int, int], float] = {}
    max_row = max(c["row"] for c in grid_cells)
    max_col = max(c["col"] for c in grid_cells)
    elev_grid = np.full((max_row + 1, max_col + 1), np.nan)
    valid = np.zeros((max_row + 1, max_col + 1), dtype=bool)

    for idx, cell in enumerate(grid_cells):
        r, c = cell["row"], cell["col"]
        e = _sample_cell_elevation(cell["geometry"], dem)
        cell_elev[(r, c)] = e
        elev_grid[r, c] = e
        valid[r, c] = True
        if progress_callback and idx % 500 == 0 and idx > 0:
            pct = 18.0 + idx / len(grid_cells) * 12.0
            progress_callback(pct, "Zellhöhen", f"{idx}/{len(grid_cells)}")

    if progress_callback:
        progress_callback(32.0, "Hydrologie (Hang, Senke, TWI)")

    elev_filled = _fill_nan_nearest(elev_grid)
    slope_rad = _compute_slope_grid(elev_filled, cell_size_m)
    sink_depth = _compute_sink_depth(elev_filled)
    flow_acc = _d8_flow_accumulation(elev_filled)
    twi = _compute_twi(flow_acc, slope_rad, cell_size_m)

    slope_norm_all = _normalize(np.degrees(slope_rad), valid)
    sink_norm_all = _normalize(sink_depth, valid)
    twi_norm_all = _normalize(twi, valid)

    results: dict[int, dict] = {}
    for idx, cell in enumerate(grid_cells):
        r, c = cell["row"], cell["col"]
        slope_deg = float(math.degrees(slope_rad[r, c]))
        s_norm = float(slope_norm_all[r, c])
        sk_m = float(sink_depth[r, c])
        sk_norm = float(sink_norm_all[r, c])
        t = float(twi[r, c])
        t_norm = float(twi_norm_all[r, c])
        # Senken-/Feuchte-Faktor: TWI + Senkentiefe (physikalisch)
        depression_factor = round(min(1.0, 0.55 * t_norm + 0.45 * sk_norm), 3)
        slope_factor = round(s_norm, 3)

        results[idx] = {
            "mean_elevation_m": round(cell_elev[(r, c)], 1),
            "slope_deg": round(slope_deg, 2),
            "slope_norm": slope_factor,
            "sink_depth_m": round(sk_m, 2),
            "sink_norm": sk_norm,
            "flow_accum": round(float(flow_acc[r, c]), 1),
            "twi": round(t, 3),
            "twi_norm": t_norm,
            "depression_factor": depression_factor,
            "slope_factor": slope_factor,
        }

    with _cache_lock:
        _dem_cache[cache_key] = (_time.time(), results)

    log.info(
        "Terrain: %d cells, zoom=%d, elev %.0f..%.0f m",
        len(results), zoom,
        float(np.nanmin(elev_grid)), float(np.nanmax(elev_grid)),
    )
    return results


def _bbox_key(grid_cells: list[dict]) -> str:
    combined = unary_union([c["geometry"] for c in grid_cells])
    b = combined.bounds
    cs = grid_cells[0].get("cell_size_m", 100)
    return f"{b[0]:.5f},{b[1]:.5f},{b[2]:.5f},{b[3]:.5f}:{cs}"


def clear_terrain_cache():
    with _cache_lock:
        _tile_cache.clear()
        _dem_cache.clear()
