"""Sonnenscheindauer der Klimanormalperioden je Zellstandort (Methodik #98 §3.2).

Das UV-Modell braucht pro Zelle zwei Werte: das SSD-Mittel 1961–1990 und
1991–2020. Beide stammen aus den DWD-CDC-Jahresrastern (1 km, ab 1961 verfügbar
— bei der Integration am 31.08.2026 verifiziert), sind aber **vorgemittelt** in
der Anlage ``backend/data/kalibrierung/ssd_normalperioden.npz`` abgelegt
(Skript ``scripts/kalibrierung/dwd_ssd_normalperioden.py``). So lädt kein
Assessment 60 Jahresraster nach — die Ressourcen-Regel (§3.4) bleibt gewahrt und
der Datenstand ist gepinnt.

Fallback-Kette (Bericht §3.6):
1. Zellwert aus dem Normalperioden-Raster (Regelfall),
2. Bundesland-Gebietsmittel aus ``ssd_trend_region.csv`` (wenn die Position
   außerhalb des Rasters liegt oder die Anlage fehlt),
3. Deutschland-Gebietsmittel.
"""
from __future__ import annotations

import csv
import logging
import os
import threading

log = logging.getLogger(__name__)

_DATA = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data",
                     "kalibrierung")
_NPZ = os.path.abspath(os.path.join(_DATA, "ssd_normalperioden.npz"))
_CSV = os.path.abspath(os.path.join(_DATA, "ssd_trend_region.csv"))

# Rasterdaten liegen in Gauß-Krüger 3 (wie alle grids_germany-Raster).
_GRID_CRS = "EPSG:31467"

_lock = threading.Lock()
_grid: dict | None = None
_region_means: dict[str, tuple[float, float]] | None = None
_transformer = None


def _load_grid() -> dict | None:
    """Normalperioden-Mittelraster laden (einmalig, danach im Speicher)."""
    global _grid
    if _grid is not None:
        return _grid or None
    with _lock:
        if _grid is not None:
            return _grid or None
        try:
            import numpy as np

            with np.load(_NPZ) as z:
                _grid = {
                    "ref": z["ref"], "neu": z["neu"],
                    "ncols": int(z["ncols"]), "nrows": int(z["nrows"]),
                    "xll": float(z["xllcorner"]), "yll": float(z["yllcorner"]),
                    "cell": float(z["cellsize"]), "nodata": float(z["nodata"]),
                }
        except Exception as exc:  # noqa: BLE001 — Anlage fehlt → Gebietsmittel
            log.warning("SSD-Normalperioden-Anlage nicht ladbar (%s) — "
                        "Gebietsmittel-Fallback (Bericht #98 §3.6)", exc)
            _grid = {}
    return _grid or None


def _load_region_means() -> dict[str, tuple[float, float]]:
    """Gebietsmittel je Bundesland/Region aus der CSV-Anlage (Fallback)."""
    global _region_means
    if _region_means is not None:
        return _region_means
    with _lock:
        out: dict[str, tuple[float, float]] = {}
        try:
            with open(_CSV, newline="", encoding="utf-8") as fh:
                for row in csv.DictReader(fh):
                    out[row["gebiet"].strip().lower()] = (
                        float(row["ssd_ref_1961_1990"]),
                        float(row["ssd_neu_1991_2020"]),
                    )
        except OSError as exc:
            log.warning("ssd_trend_region.csv nicht lesbar: %s", exc)
        _region_means = out
    return _region_means


def _to_gk3(lon: float, lat: float) -> tuple[float, float]:
    global _transformer
    if _transformer is None:
        from pyproj import Transformer

        _transformer = Transformer.from_crs("EPSG:4326", _GRID_CRS, always_xy=True)
    return _transformer.transform(lon, lat)


def ssd_at(lon: float, lat: float) -> tuple[float, float] | None:
    """(SSD 1961–1990, SSD 1991–2020) in h/Jahr am Punkt; ``None`` außerhalb."""
    grid = _load_grid()
    if grid is None:
        return None
    try:
        x, y = _to_gk3(lon, lat)
    except Exception:  # noqa: BLE001
        return None
    col = int((x - grid["xll"]) // grid["cell"])
    row = int(grid["nrows"] - 1 - (y - grid["yll"]) // grid["cell"])
    if not (0 <= col < grid["ncols"] and 0 <= row < grid["nrows"]):
        return None
    ref = float(grid["ref"][row, col])
    neu = float(grid["neu"][row, col])
    if ref == grid["nodata"] or neu == grid["nodata"] or ref <= 0:
        return None
    return ref, neu


def ssd_for_cells_3035(xs: list[float], ys: list[float]
                       ) -> list[tuple[float, float] | None]:
    """Zellweise (SSD_ref, SSD_neu) für EPSG:3035-Koordinaten — vektorisiert.

    Der Assessment-Lauf hat die Zellmittelpunkte bereits in EPSG:3035; ein
    Einzeltransform je Zelle wäre bei 10⁴–10⁵ Zellen unnötig teuer. ``None``
    steht für „außerhalb des Rasters/nodata" — dann greift der
    Bundesland-Fallback (Bericht #98 §3.6).
    """
    if not xs:
        return []
    grid = _load_grid()
    if grid is None:
        return [None] * len(xs)
    import numpy as np
    from pyproj import Transformer

    tr = Transformer.from_crs("EPSG:3035", _GRID_CRS, always_xy=True)
    gx, gy = tr.transform(np.asarray(xs, dtype="float64"),
                          np.asarray(ys, dtype="float64"))
    col = ((gx - grid["xll"]) // grid["cell"]).astype("int64")
    row = (grid["nrows"] - 1 - (gy - grid["yll"]) // grid["cell"]).astype("int64")
    ok = ((col >= 0) & (col < grid["ncols"])
          & (row >= 0) & (row < grid["nrows"]))
    col_c = np.clip(col, 0, grid["ncols"] - 1)
    row_c = np.clip(row, 0, grid["nrows"] - 1)
    ref = grid["ref"][row_c, col_c].astype("float64")
    neu = grid["neu"][row_c, col_c].astype("float64")
    ok &= (ref != grid["nodata"]) & (neu != grid["nodata"]) & (ref > 0)
    return [(float(r), float(n)) if o else None
            for o, r, n in zip(ok.tolist(), ref.tolist(), neu.tolist())]


# Die DWD-Gebietsmittel fassen kleine Länder zusammen (Zeilenschlüssel der
# Anlage ``ssd_trend_region.csv``, Präfix ``land:``).
_LAND_KEY: dict[str, str] = {
    "baden-württemberg": "land:baden-wuerttemberg",
    "bayern": "land:bayern",
    "berlin": "land:brandenburg/berlin",
    "brandenburg": "land:brandenburg/berlin",
    "bremen": "land:niedersachsen/hamburg/bremen",
    "hamburg": "land:niedersachsen/hamburg/bremen",
    "hessen": "land:hessen",
    "mecklenburg-vorpommern": "land:mecklenburg-vorpommern",
    "niedersachsen": "land:niedersachsen/hamburg/bremen",
    "nordrhein-westfalen": "land:nordrhein-westfalen",
    "rheinland-pfalz": "land:rheinland-pfalz",
    "saarland": "land:saarland",
    "sachsen": "land:sachsen",
    "sachsen-anhalt": "land:thueringen/sachsen-anhalt",
    "schleswig-holstein": "land:schleswig-holstein",
    "thüringen": "land:thueringen/sachsen-anhalt",
}


def ssd_for_bundesland(bundesland: str | None) -> tuple[float, float]:
    """Gebietsmittel des Bundeslands (Fallback); sonst Deutschland-Mittel."""
    means = _load_region_means()
    key = (bundesland or "").strip().lower()
    for candidate in (_LAND_KEY.get(key), key, f"land:{key}"):
        if candidate and candidate in means:
            return means[candidate]
    return means.get("deutschland", (1544.0, 1664.8))


def relative_change(lon: float | None, lat: float | None,
                    bundesland: str | None = None) -> float:
    """Relative SSD-Änderung (Anteil, nicht %) zwischen den Normalperioden.

    Zellwert aus dem Raster, sonst Bundesland-Gebietsmittel (Bericht §3.6).
    """
    pair = ssd_at(lon, lat) if lon is not None and lat is not None else None
    if pair is None:
        pair = ssd_for_bundesland(bundesland)
    ref, neu = pair
    return (neu - ref) / ref if ref > 0 else 0.0
