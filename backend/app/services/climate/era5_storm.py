"""ERA5-Sturmtage (Copernicus CDS): ortsaufgelöster Treiber ``storm_days``.

Ersetzt die regionale Konstante ``storm_days = 6.0`` durch die tatsächliche
Sturmbö-Häufigkeit (Tage/Jahr mit 10-m-Böe ≥ Schwelle, Klimatologie der letzten N
Jahre) aus **ERA5** (ECMWF/Copernicus Climate Change Service). ERA5 ist bundesweit
einheitlich, kostenlos und kommerziell nutzbar (seit 02.07.2025 CC-BY 4.0); Zugang über
ein kostenloses CDS-Konto + API-Key.

Arbeitsteilung (wie DWD-CDC/PEGELONLINE):
- Der **Betreiber** erzeugt einmalig mit ``scripts/fetch_era5_storm.py`` (braucht
  ``cdsapi`` + ``~/.cdsapirc`` mit dem CDS-Key) ein Sturmtage-Raster über Deutschland
  und legt es als ``{ERA5_STORM_CACHE_DIR}/storm_days.asc[.gz]`` ab (ESRI-ASCII,
  **EPSG:4326**, Werte = Sturmtage/Jahr).
- Dieser **Loader** liest das gecachte Raster und greift den Zentroid-Wert ab. Fehlt
  Datei/Wert oder liegt der Punkt außerhalb, gibt ``storm_days_at`` ``None`` zurück →
  der Aufrufer nutzt den bisherigen Konstantwert. Es wird nie eine Exception geworfen.
"""

from __future__ import annotations

import gzip
import logging
import os
import threading

import numpy as np

from app.config import settings

log = logging.getLogger(__name__)

_grid_cache: tuple[dict, np.ndarray] | None | str = "unset"  # "unset" = noch nicht geladen
_cache_lock = threading.Lock()


def _grid_path() -> str | None:
    base = settings.ERA5_STORM_CACHE_DIR
    for name in ("storm_days.asc.gz", "storm_days.asc"):
        p = os.path.join(base, name)
        if os.path.exists(p):
            return p
    return None


def _read_bytes(path: str) -> str:
    if path.endswith(".gz"):
        with open(path, "rb") as fh:
            return gzip.decompress(fh.read()).decode("latin-1")
    with open(path, encoding="latin-1") as fh:
        return fh.read()


def _load_grid() -> tuple[dict, np.ndarray] | None:
    """Geparstes Sturmtage-Raster (Header-Dict, 2D-Array), Mem-Cache. ``None`` fehlend."""
    global _grid_cache
    with _cache_lock:
        if _grid_cache != "unset":
            return _grid_cache  # type: ignore[return-value]

    result: tuple[dict, np.ndarray] | None = None
    path = _grid_path()
    if path is not None:
        try:
            lines = _read_bytes(path).splitlines()
            hdr: dict[str, float] = {}
            for i in range(6):
                k, v = lines[i].split()
                hdr[k.upper()] = float(v)
            nrows = int(hdr["NROWS"])
            arr = np.loadtxt(lines[6:6 + nrows])
            result = (hdr, arr)
        except Exception as exc:  # pragma: no cover - defensiv
            log.warning("ERA5-Sturm-Raster %s nicht lesbar: %s", path, exc)
            result = None

    with _cache_lock:
        _grid_cache = result
    return result


def storm_days_at(lon: float, lat: float) -> float | None:
    """Sturmtage/Jahr am Zentroid aus dem ERA5-Raster (EPSG:4326). ``None`` = Fallback."""
    parsed = _load_grid()
    if parsed is None:
        return None
    hdr, arr = parsed
    try:
        ncols, nrows = int(hdr["NCOLS"]), int(hdr["NROWS"])
        xll, yll, cs = hdr["XLLCORNER"], hdr["YLLCORNER"], hdr["CELLSIZE"]
        nodata = hdr.get("NODATA_VALUE", -9999.0)
        col = int((lon - xll) / cs)
        row = nrows - 1 - int((lat - yll) / cs)   # Zeile 0 = Norden
        if not (0 <= row < nrows and 0 <= col < ncols):
            return None
        val = float(arr[row, col])
        return None if val == nodata else round(val, 1)
    except Exception as exc:  # pragma: no cover - defensiv
        log.warning("ERA5-Sturm-Sampling fehlgeschlagen: %s", exc)
        return None


def _reset_cache() -> None:
    """Nur für Tests: Mem-Cache leeren."""
    global _grid_cache
    with _cache_lock:
        _grid_cache = "unset"
