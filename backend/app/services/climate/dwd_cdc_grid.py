"""DWD-CDC-Rasterdaten (grids_germany/annual): ortsaufgelöste Klimatreiber.

Greift die jährlichen 1-km-Raster des DWD Climate Data Center (offen, ohne
API-Schlüssel) am Kommune-/Zell-Zentroid ab und bildet ein robustes Klimamittel
der letzten N verfügbaren Jahre. Ersetzt die Bundesland-Konstanten aus
:data:`app.services.climate.dwd_data.FALLBACK_CLIMATE` für die Treiber
``hot_days`` (heiße Tage, Tmax ≥ 30 °C) und ``frost_days`` (Frosttage,
Tmin < 0 °C) — Report §B2.1.

Datenquelle je Jahr::

    {DWD_CDC_GRID_BASE}/{param}/grids_germany_annual_{param}_{YYYY}_17.asc.gz

Format: gzip-komprimiertes ESRI-ASCII-Grid (Header NCOLS/NROWS/XLLCORNER/
YLLCORNER/CELLSIZE/NODATA_VALUE + Werteblock). Projektion der
``grids_germany``-Raster: Gauß-Krüger Zone 3, **EPSG:31467**.

Robuster Fallback (inkar-Prinzip, siehe :mod:`app.services.inkar_loader`): fehlt
Netz, Datei, Projektion oder liegt der Zentroid außerhalb/auf NODATA, gibt jede
öffentliche Funktion ``None`` zurück; der Aufrufer nutzt dann den bisherigen
Bundesland-Proxy. Es wird nie eine Exception nach oben gereicht.
"""

from __future__ import annotations

import gzip
import json
import logging
import os
import threading
import time
from datetime import datetime

import httpx
import numpy as np
from pyproj import Transformer

from app.config import settings

log = logging.getLogger(__name__)

# ``grids_germany``-Raster liegen in Gauß-Krüger Zone 3 (EPSG:31467) vor.
_GRID_CRS = "EPSG:31467"

# DWD-Ordnername je Treiber (identisch zum Dateinamens-Baustein).
_PARAM_DIR: dict[str, str] = {"hot_days": "hot_days", "frost_days": "frost_days"}

# Mem-Caches: WGS84→GK3-Transformer, geparste Grids je (param, year),
# abgeleitete Zentroid-Werte je (param, gerundeter Zentroid).
_transformer: Transformer | None = None
_grid_cache: dict[tuple[str, int], tuple[dict, np.ndarray] | None] = {}
_value_cache: dict[str, tuple[float, float | None]] = {}
_cache_lock = threading.Lock()


def _get_transformer() -> Transformer:
    global _transformer
    if _transformer is None:
        with _cache_lock:
            if _transformer is None:
                _transformer = Transformer.from_crs(
                    "EPSG:4326", _GRID_CRS, always_xy=True
                )
    return _transformer


# ── Grid-Download (Disk-Cache) und -Parsing (Mem-Cache) ───────────────────────

def _grid_url(param: str, year: int) -> str:
    d = _PARAM_DIR[param]
    base = settings.DWD_CDC_GRID_BASE.rstrip("/")
    return f"{base}/{d}/grids_germany_annual_{d}_{year}_17.asc.gz"


def _raw_path(param: str, year: int) -> str:
    return os.path.join(settings.DWD_CDC_CACHE_DIR, f"{param}_{year}.asc.gz")


def _download_raw(param: str, year: int) -> bytes | None:
    """Rohes ``.asc.gz`` holen (Disk-Cache mit TTL). ``None`` bei 404/Netzfehler."""
    path = _raw_path(param, year)
    try:
        if (
            os.path.exists(path)
            and time.time() - os.path.getmtime(path) < settings.DWD_CDC_CACHE_TTL_S
        ):
            with open(path, "rb") as fh:
                return fh.read()
    except Exception:
        pass

    try:
        with httpx.Client(timeout=settings.DWD_CDC_TIMEOUT_S) as client:
            resp = client.get(_grid_url(param, year))
            if resp.status_code == 404:
                return None  # Jahr (noch) nicht veröffentlicht
            resp.raise_for_status()
            data = resp.content
    except Exception as exc:
        log.warning("DWD CDC Download %s %s fehlgeschlagen: %s", param, year, exc)
        return None

    try:
        os.makedirs(settings.DWD_CDC_CACHE_DIR, exist_ok=True)
        with open(path, "wb") as fh:
            fh.write(data)
    except Exception as exc:
        log.debug("DWD CDC Disk-Cache-Write übersprungen: %s", exc)
    return data


def _parse_grid(param: str, year: int) -> tuple[dict, np.ndarray] | None:
    """Geparstes Grid (Header-Dict, 2D-Array) je (param, year), Mem-Cache."""
    key = (param, year)
    with _cache_lock:
        if key in _grid_cache:
            return _grid_cache[key]

    result: tuple[dict, np.ndarray] | None = None
    raw = _download_raw(param, year)
    if raw is not None:
        try:
            lines = gzip.decompress(raw).decode("latin-1").splitlines()
            hdr: dict[str, float] = {}
            for i in range(6):
                k, v = lines[i].split()
                hdr[k.upper()] = float(v)
            nrows = int(hdr["NROWS"])
            arr = np.loadtxt(lines[6:6 + nrows])
            result = (hdr, arr)
        except Exception as exc:
            log.warning("DWD CDC Parsing %s %s fehlgeschlagen: %s", param, year, exc)
            result = None

    with _cache_lock:
        _grid_cache[key] = result
    return result


def _sample_year(param: str, year: int, lon: float, lat: float) -> float | None:
    """Rasterwert am Zentroid für ein Jahr. ``None`` bei NODATA/außerhalb/Fehler."""
    parsed = _parse_grid(param, year)
    if parsed is None:
        return None
    hdr, arr = parsed
    try:
        x, y = _get_transformer().transform(lon, lat)
        ncols, nrows = int(hdr["NCOLS"]), int(hdr["NROWS"])
        xll, yll, cs = hdr["XLLCORNER"], hdr["YLLCORNER"], hdr["CELLSIZE"]
        nodata = hdr["NODATA_VALUE"]
        col = int((x - xll) / cs)
        row = nrows - 1 - int((y - yll) / cs)  # Grid-Zeile 0 = Norden
        if not (0 <= row < nrows and 0 <= col < ncols):
            return None
        val = float(arr[row, col])
        return None if val == nodata else val
    except Exception as exc:
        log.warning("DWD CDC Sampling %s %s fehlgeschlagen: %s", param, year, exc)
        return None


# ── Klimatologie (Mittel der letzten N Jahre) mit Zentroid-Wert-Cache ─────────

def _value_cache_path(param: str, lon: float, lat: float) -> str:
    return os.path.join(settings.DWD_CDC_CACHE_DIR, f"val_{param}_{lon:.3f}_{lat:.3f}.json")


def sample_climatology(
    param: str, lon: float, lat: float, n_years: int | None = None
) -> float | None:
    """Mittelwert des Treibers ``param`` am Zentroid über die letzten N Jahre.

    Sucht rückwärts vom Vorjahr die jüngsten *verfügbaren* Jahresraster (das
    laufende Jahr ist beim DWD i. d. R. noch nicht publiziert) und mittelt bis zu
    ``n_years`` gültige Stichproben. Ergebnis wird je gerundetem Zentroid im Mem-
    und Disk-Cache gehalten. ``None``, wenn kein Jahr auswertbar ist.
    """
    if param not in _PARAM_DIR:
        return None
    n_years = n_years or settings.DWD_CDC_CLIMATOLOGY_YEARS
    lon_r, lat_r = round(lon, 3), round(lat, 3)
    ckey = f"{param}:{lon_r}:{lat_r}"

    with _cache_lock:
        cached = _value_cache.get(ckey)
        if cached and time.time() - cached[0] < settings.DWD_CDC_CACHE_TTL_S:
            return cached[1]

    vpath = _value_cache_path(param, lon_r, lat_r)
    try:
        if (
            os.path.exists(vpath)
            and time.time() - os.path.getmtime(vpath) < settings.DWD_CDC_CACHE_TTL_S
        ):
            with open(vpath, encoding="utf-8") as fh:
                val = json.load(fh).get("value")
            with _cache_lock:
                _value_cache[ckey] = (time.time(), val)
            return val
    except Exception:
        pass

    samples: list[float] = []
    consecutive_misses = 0
    year = datetime.utcnow().year - 1
    attempts, max_attempts = 0, n_years + 5
    while len(samples) < n_years and attempts < max_attempts and year > 1950:
        v = _sample_year(param, year, lon, lat)
        if v is not None:
            samples.append(v)
            consecutive_misses = 0
        else:
            consecutive_misses += 1
            # Quelle nicht erreichbar oder Zentroid außerhalb/NODATA: nicht alle
            # Jahre durchprobieren (Timeout-Schutz), wenn schon früh mehrere
            # Jahre in Folge fehlen und noch kein Wert vorliegt.
            if not samples and consecutive_misses >= 4:
                break
        year -= 1
        attempts += 1

    result = round(sum(samples) / len(samples), 1) if samples else None
    try:
        os.makedirs(settings.DWD_CDC_CACHE_DIR, exist_ok=True)
        with open(vpath, "w", encoding="utf-8") as fh:
            json.dump({"value": result, "n_years": len(samples)}, fh)
    except Exception as exc:
        log.debug("DWD CDC Wert-Cache-Write übersprungen: %s", exc)
    with _cache_lock:
        _value_cache[ckey] = (time.time(), result)
    return result


# ── Öffentliche Treiber-Getter ────────────────────────────────────────────────

def hot_days_at(lon: float, lat: float) -> float | None:
    """Mittlere heiße Tage/Jahr (Tmax ≥ 30 °C) am Zentroid (DWD-CDC-Klimatologie)."""
    return sample_climatology("hot_days", lon, lat)


def frost_days_at(lon: float, lat: float) -> float | None:
    """Mittlere Frosttage/Jahr (Tmin < 0 °C) am Zentroid (DWD-CDC-Klimatologie)."""
    return sample_climatology("frost_days", lon, lat)
