"""DWD-CDC-Rasterdaten (grids_germany/annual): ortsaufgelöste Klimatreiber.

Greift die jährlichen 1-km-Raster des DWD Climate Data Center (offen, ohne
API-Schlüssel) am Kommune-/Zell-Zentroid ab und bildet ein robustes Klimamittel
der letzten N verfügbaren Jahre. Ersetzt die Bundesland-Konstanten bzw. Proxys
für die Treiber ``hot_days`` (heiße Tage, Tmax ≥ 30 °C), ``frost_days``
(Frosttage, Tmin < 0 °C) — Report §B2.1 — sowie ``precipGE20mm_days`` /
``precipGE30mm_days`` (Starkregen-Häufigkeit, Basis des ``heavy_rain_index``,
Stufe 2) und ``summer_days`` (Sommertage, Tmax ≥ 25 °C).

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
from collections import OrderedDict
from datetime import datetime

import httpx
import numpy as np
from pyproj import Transformer

from app.config import settings

log = logging.getLogger(__name__)

# ``grids_germany``-Raster liegen in Gauß-Krüger Zone 3 (EPSG:31467) vor.
_GRID_CRS = "EPSG:31467"

# DWD-Ordnername je Treiber (identisch zum Dateinamens-Baustein). Die meisten
# Raster nutzen das Standard-Dateinamensmuster
# ``grids_germany_annual_{dir}_{YYYY}_17.asc.gz`` (verifiziert für hot_days,
# frost_days, precipGE20mm_days, precipGE30mm_days, summer_days). Raster mit
# abweichendem Muster ``..._{YYYY}17.asc.gz`` (ohne Unterstrich, z. B.
# precipitation, drought_index) stehen zusätzlich in ``_PARAM_NO_UNDERSCORE``.
_PARAM_DIR: dict[str, str] = {
    "hot_days": "hot_days",
    "frost_days": "frost_days",
    "precipGE20mm_days": "precipGE20mm_days",
    "precipGE30mm_days": "precipGE30mm_days",
    "summer_days": "summer_days",
    "precipitation": "precipitation",
}

# Parameter mit Dateinamensmuster ``..._{YYYY}17.asc.gz`` (verifiziert per
# Verzeichnis-Listing opendata.dwd.de, 2026-07-05).
_PARAM_NO_UNDERSCORE: frozenset[str] = frozenset({"precipitation"})

# ── Monatsraster (Lufttemperatur) ─────────────────────────────────────────────
# Andere Ablage als die Jahresraster: ``monthly/<dir>/<MM_Mon>/
# grids_germany_monthly_<stem>_<YYYY><MM>.asc.gz``. Header-Aufbau ist identisch
# (6 Zeilen, GK3, 1 km), daher greift ``_parse_grid`` unverändert.
# ACHTUNG: Die Werte stehen in **1/10 °C** (verifiziert 2026-08-02 an
# air_temp_mean 2024-07: Gebietsmittel 188 → 18,8 °C). Ohne ``_MONTHLY_SCALE``
# wären alle Temperaturen um den Faktor 10 zu hoch.
_MONTHLY_PARAM: dict[str, tuple[str, str]] = {
    "air_temp_mean": ("air_temperature_mean", "air_temp_mean"),
    "air_temp_min": ("air_temperature_min", "air_temp_min"),
    "air_temp_max": ("air_temperature_max", "air_temp_max"),
}
_MONTHLY_SCALE = 0.1
_MONTH_DIR = {
    1: "01_Jan", 2: "02_Feb", 3: "03_Mar", 4: "04_Apr", 5: "05_May", 6: "06_Jun",
    7: "07_Jul", 8: "08_Aug", 9: "09_Sep", 10: "10_Oct", 11: "11_Nov", 12: "12_Dec",
}
# Sommerhalbjahr-Kernmonate für die Hitze-Expositionsrechnung (Juni–August).
SUMMER_MONTHS: tuple[int, ...] = (6, 7, 8)


def _split_monthly(param: str) -> tuple[str, int] | None:
    """``"air_temp_mean_07"`` → ``("air_temp_mean", 7)``; ``None`` für Jahresraster."""
    base, _, mm = param.rpartition("_")
    if base in _MONTHLY_PARAM and mm.isdigit():
        return base, int(mm)
    return None

# Mem-Caches: WGS84→GK3-Transformer, geparste Grids je (param, year),
# abgeleitete Zentroid-Werte je (param, gerundeter Zentroid).
# Grid-Cache als kleines LRU: ein Deutschland-Raster ≈ 4-5 MB; ohne Deckel
# sammelten sich hier ~Parameter×Klimatologie-Jahre ≈ hunderte MB an.
_GRID_LRU_MAX = 6
_transformer: Transformer | None = None
_grid_cache: "OrderedDict[tuple[str, int], tuple[dict, np.ndarray] | None]" = OrderedDict()
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
    monthly = _split_monthly(param)
    if monthly is not None:
        base_param, month = monthly
        d, stem = _MONTHLY_PARAM[base_param]
        base = settings.DWD_CDC_MONTHLY_BASE.rstrip("/")
        return (f"{base}/{d}/{_MONTH_DIR[month]}/"
                f"grids_germany_monthly_{stem}_{year}{month:02d}.asc.gz")
    d = _PARAM_DIR[param]
    base = settings.DWD_CDC_GRID_BASE.rstrip("/")
    suffix = f"{year}17.asc.gz" if param in _PARAM_NO_UNDERSCORE else f"{year}_17.asc.gz"
    return f"{base}/{d}/grids_germany_annual_{d}_{suffix}"


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
            _grid_cache.move_to_end(key)
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
        _grid_cache.move_to_end(key)
        while len(_grid_cache) > _GRID_LRU_MAX:
            _grid_cache.popitem(last=False)
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
        if val == nodata:
            return None
        # Monatsraster liefern 1/10 °C — hier auf °C bringen.
        return val * _MONTHLY_SCALE if _split_monthly(param) is not None else val
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
    if param not in _PARAM_DIR and _split_monthly(param) is None:
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


def precip_days_ge20_at(lon: float, lat: float) -> float | None:
    """Mittlere Tage/Jahr mit Niederschlag ≥ 20 mm am Zentroid (Starkregen-Signal)."""
    return sample_climatology("precipGE20mm_days", lon, lat)


def precip_days_ge30_at(lon: float, lat: float) -> float | None:
    """Mittlere Tage/Jahr mit Niederschlag ≥ 30 mm am Zentroid (Starkregen-Extreme)."""
    return sample_climatology("precipGE30mm_days", lon, lat)


def summer_days_at(lon: float, lat: float) -> float | None:
    """Mittlere Sommertage/Jahr (Tmax ≥ 25 °C) am Zentroid (DWD-CDC-Klimatologie)."""
    return sample_climatology("summer_days", lon, lat)


def precipitation_at(lon: float, lat: float) -> float | None:
    """Mittlere Jahresniederschlagssumme (mm) am Zentroid (DWD-CDC-Klimatologie)."""
    return sample_climatology("precipitation", lon, lat)


# ── Klimatologie-Grid (für zellscharfes Sampling) ─────────────────────────────
# ``sample_climatology`` cacht je *Zentroid*; bei 100-m-Zellen entstünden
# tausende Cache-Einträge, die jeweils erneut über alle Jahresraster liefen.
# Für flächige Auswertung wird das Klimatologie-Mittel daher **einmal** als
# Array gebaut und anschließend vektorisiert abgetastet.

_clim_grid_cache: "OrderedDict[tuple[str, tuple[int, ...], int], tuple[dict, np.ndarray] | None]" = OrderedDict()


def climatology_grid(
    param: str, months: tuple[int, ...] | None = None, n_years: int | None = None,
) -> tuple[dict, np.ndarray] | None:
    """Über Monate und die letzten N Jahre gemitteltes Raster (Header, Array).

    ``months=None`` → Jahresraster (``param`` aus ``_PARAM_DIR``). Sonst werden
    die Monatsraster ``param_MM`` gemittelt. NODATA-Zellen bleiben ``np.nan``.
    """
    months = tuple(months or ())
    n_years = n_years or settings.DWD_CDC_CLIMATOLOGY_YEARS
    key = (param, months, n_years)
    with _cache_lock:
        if key in _clim_grid_cache:
            _clim_grid_cache.move_to_end(key)
            return _clim_grid_cache[key]

    param_keys = [f"{param}_{m:02d}" for m in months] if months else [param]
    total: np.ndarray | None = None
    count: np.ndarray | None = None
    header: dict | None = None

    for pk in param_keys:
        collected = 0
        year = datetime.utcnow().year - 1
        attempts, max_attempts = 0, n_years + 5
        while collected < n_years and attempts < max_attempts and year > 1950:
            parsed = _parse_grid(pk, year)
            year -= 1
            attempts += 1
            if parsed is None:
                continue
            hdr, arr = parsed
            vals = np.where(arr == hdr["NODATA_VALUE"], np.nan, arr.astype(float))
            if _split_monthly(pk) is not None:
                vals = vals * _MONTHLY_SCALE
            if total is None:
                header = hdr
                total = np.zeros_like(vals)
                count = np.zeros_like(vals)
            elif vals.shape != total.shape:
                log.warning("DWD CDC Klimatologie %s: abweichende Rastergröße %s",
                            pk, vals.shape)
                continue
            valid = ~np.isnan(vals)
            total[valid] += vals[valid]
            count[valid] += 1
            collected += 1

    result: tuple[dict, np.ndarray] | None = None
    if total is not None and count is not None and header is not None:
        with np.errstate(invalid="ignore"):
            mean = np.where(count > 0, total / np.maximum(count, 1), np.nan)
        result = (header, mean)

    with _cache_lock:
        _clim_grid_cache[key] = result
        _clim_grid_cache.move_to_end(key)
        while len(_clim_grid_cache) > 4:
            _clim_grid_cache.popitem(last=False)
    return result


def sample_grid_points(
    grid: tuple[dict, np.ndarray] | None, points: list[tuple[float, float]],
) -> list[float | None]:
    """Rasterwerte für viele (lon, lat)-Punkte; ``None`` außerhalb/NODATA."""
    if grid is None:
        return [None] * len(points)
    hdr, arr = grid
    ncols, nrows = int(hdr["NCOLS"]), int(hdr["NROWS"])
    xll, yll, cs = hdr["XLLCORNER"], hdr["YLLCORNER"], hdr["CELLSIZE"]
    out: list[float | None] = []
    if not points:
        return out
    tr = _get_transformer()
    lons = [p[0] for p in points]
    lats = [p[1] for p in points]
    xs, ys = tr.transform(lons, lats)
    for x, y in zip(xs, ys):
        col = int((x - xll) / cs)
        row = nrows - 1 - int((y - yll) / cs)
        if not (0 <= row < nrows and 0 <= col < ncols):
            out.append(None)
            continue
        val = float(arr[row, col])
        out.append(None if np.isnan(val) else val)
    return out


def summer_mean_temp_at(lon: float, lat: float) -> float | None:
    """Mittlere Sommer-Lufttemperatur (Jun–Aug, °C) am Punkt."""
    vals = [sample_climatology(f"air_temp_mean_{m:02d}", lon, lat) for m in SUMMER_MONTHS]
    ok = [v for v in vals if v is not None]
    return round(sum(ok) / len(ok), 2) if ok else None


def summer_night_temp_at(lon: float, lat: float) -> float | None:
    """Mittlere Sommer-Nachttemperatur (Tmin Jun–Aug, °C) am Punkt."""
    vals = [sample_climatology(f"air_temp_min_{m:02d}", lon, lat) for m in SUMMER_MONTHS]
    ok = [v for v in vals if v is not None]
    return round(sum(ok) / len(ok), 2) if ok else None
