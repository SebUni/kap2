"""Batch-Sampling der DWD-CDC-Raster für viele Punkte (Gemeinde-Zentroide).

Der Einzelpunkt-Pfad ``dwd_cdc_grid.sample_climatology`` schreibt je Punkt eine
Cache-Datei — für ~11.000 Gemeinden × 6 Parameter wären das zehntausende
Mini-Dateien. Hier wird stattdessen jedes Jahresraster GENAU EINMAL geparst
(via ``_parse_grid``, LRU-gecacht) und dann für alle Punkte im Speicher
indiziert. NODATA/außerhalb → Rückgabe ``None`` je Punkt (Aufrufer nutzt
Bundesland-Fallback).
"""
from __future__ import annotations

import logging
from datetime import datetime

import numpy as np

from app.config import settings
from app.services.climate import dwd_cdc_grid as g

log = logging.getLogger(__name__)


def _available_years(param: str, n_years: int) -> list[int]:
    """Jüngste verfügbare Jahresraster rückwärts sammeln (max. n_years)."""
    years: list[int] = []
    year = datetime.utcnow().year - 1
    misses = 0
    while len(years) < n_years and year > 1950 and misses < 6:
        parsed = g._parse_grid(param, year)
        if parsed is not None:
            years.append(year)
            misses = 0
        else:
            misses += 1
        year -= 1
    return years


def sample_many(
    param: str, points: list[tuple[float, float]], n_years: int | None = None
) -> list[float | None]:
    """Klimamittel (letzte N Jahre) des Treibers ``param`` je (lon, lat).

    Ein Wert je Punkt, gleiche Reihenfolge wie ``points``. ``None``, wenn für
    einen Punkt kein Jahr auswertbar ist (NODATA/außerhalb Deutschlands).
    """
    if param not in g._PARAM_DIR or not points:
        return [None] * len(points)
    n_years = n_years or settings.DWD_CDC_CLIMATOLOGY_YEARS
    years = _available_years(param, n_years)
    if not years:
        return [None] * len(points)

    transformer = g._get_transformer()
    # Punkte einmal ins Grid-CRS transformieren (vektorisata).
    lons = np.array([p[0] for p in points], dtype=float)
    lats = np.array([p[1] for p in points], dtype=float)
    xs, ys = transformer.transform(lons, lats)

    sums = np.zeros(len(points), dtype=float)
    counts = np.zeros(len(points), dtype=float)

    for year in years:
        parsed = g._parse_grid(param, year)
        if parsed is None:
            continue
        hdr, arr = parsed
        ncols, nrows = int(hdr["NCOLS"]), int(hdr["NROWS"])
        xll, yll, cs = hdr["XLLCORNER"], hdr["YLLCORNER"], hdr["CELLSIZE"]
        nodata = hdr["NODATA_VALUE"]
        cols = ((xs - xll) / cs).astype(int)
        rows = nrows - 1 - ((ys - yll) / cs).astype(int)
        inside = (rows >= 0) & (rows < nrows) & (cols >= 0) & (cols < ncols)
        idx = np.where(inside)[0]
        if idx.size == 0:
            continue
        vals = arr[rows[idx], cols[idx]]
        valid = vals != nodata
        vi = idx[valid]
        sums[vi] += vals[valid]
        counts[vi] += 1.0

    out: list[float | None] = []
    for i in range(len(points)):
        # native float (nicht np.float64) — sonst scheitert psycopg2/JSON.
        out.append(round(float(sums[i] / counts[i]), 2) if counts[i] > 0 else None)
    # Grids nach dem Batch aus dem LRU freigeben (RAM zurück ans OS).
    return out


def free_grid_cache() -> None:
    with g._cache_lock:
        g._grid_cache.clear()
