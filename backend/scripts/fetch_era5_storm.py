#!/usr/bin/env python3
"""Erzeugt das ERA5-Sturmtage-Raster für Deutschland (einmaliger Betreiber-Lauf).

ERA5 (ECMWF/Copernicus Climate Change Service) ist bundesweit einheitlich, kostenlos
und kommerziell nutzbar (seit 02.07.2025 CC-BY 4.0). Zugang: kostenloses CDS-Konto +
API-Key in ``~/.cdsapirc``.

Was das Skript tut:
  1. Lädt via ``cdsapi`` die tägliche 10-m-Böenspitze (``instantaneous_10m_wind_gust``,
     täglich max) über die Deutschland-Bounding-Box für die letzten N Jahre aus ERA5.
  2. Zählt je Rasterzelle die mittlere Anzahl Tage/Jahr mit Böe ≥ Schwelle (Default
     25 m/s) → Sturmtage-Klimatologie.
  3. Schreibt das Ergebnis als ESRI-ASCII-Grid (EPSG:4326) nach
     ``{ERA5_STORM_CACHE_DIR}/storm_days.asc.gz`` — genau das Format, das
     ``app.services.climate.era5_storm`` erwartet.

Voraussetzungen:  ``pip install cdsapi netCDF4``  und ein gültiger ``~/.cdsapirc``.
Aufruf:           ``python -m scripts.fetch_era5_storm``  (aus ``backend/``)

Ohne dieses Raster funktioniert die App normal weiter — ``storm_days`` bleibt dann der
dokumentierte regionale Konstantwert (siehe ``inputs.build_regional_context``).
"""

from __future__ import annotations

import datetime
import gzip
import os
import sys
import tempfile

# Deutschland-Bounding-Box (Nord, West, Süd, Ost) für die CDS-Anfrage.
_AREA = [55.5, 5.5, 47.0, 15.5]
_GRID = [0.25, 0.25]   # ERA5-Auflösung


def _years(n: int) -> list[str]:
    cur = datetime.date.today().year
    return [str(y) for y in range(cur - n, cur)]


def main() -> int:
    try:
        import cdsapi
        import netCDF4  # noqa: F401
        import numpy as np
    except ImportError as exc:
        print(f"Fehlt: {exc}. Bitte 'pip install cdsapi netCDF4' und ~/.cdsapirc einrichten.")
        return 2

    from app.config import settings

    threshold = settings.ERA5_STORM_GUST_THRESHOLD_MS
    n_years = settings.ERA5_STORM_CLIMATOLOGY_YEARS
    out_dir = settings.ERA5_STORM_CACHE_DIR
    os.makedirs(out_dir, exist_ok=True)

    client = cdsapi.Client()
    with tempfile.NamedTemporaryFile(suffix=".nc", delete=False) as tf:
        nc_path = tf.name
    print(f"Lade ERA5 (Böen, {n_years} Jahre) über DE … das kann dauern.")
    client.retrieve(
        "reanalysis-era5-single-levels",
        {
            "product_type": "reanalysis",
            "variable": "instantaneous_10m_wind_gust",
            "year": _years(n_years),
            "month": [f"{m:02d}" for m in range(1, 13)],
            "day": [f"{d:02d}" for d in range(1, 32)],
            "time": [f"{h:02d}:00" for h in range(0, 24, 3)],
            "area": _AREA,
            "grid": _GRID,
            "format": "netcdf",
        },
        nc_path,
    )

    import netCDF4
    ds = netCDF4.Dataset(nc_path)
    gust_name = next((v for v in ("i10fg", "fg10", "instantaneous_10m_wind_gust") if v in ds.variables), None)
    if gust_name is None:
        print(f"Böen-Variable nicht gefunden in {list(ds.variables)}")
        return 3
    gust = ds.variables[gust_name][:]                  # (time, lat, lon)
    lats = ds.variables["latitude"][:]
    lons = ds.variables["longitude"][:]
    times = ds.variables["time"]
    dates = netCDF4.num2date(times[:], times.units)

    # Tages-Maximum je Zelle, dann Anteil Sturmtage → Tage/Jahr.
    import numpy as np
    day_keys = np.array([(d.year, d.month, d.day) for d in dates])
    daily_max: dict[tuple, np.ndarray] = {}
    for i, key in enumerate(map(tuple, day_keys)):
        g = gust[i]
        daily_max[key] = np.maximum(daily_max[key], g) if key in daily_max else np.array(g)
    n_days = len(daily_max)
    storm = np.zeros_like(next(iter(daily_max.values())), dtype=float)
    for g in daily_max.values():
        storm += (g >= threshold)
    storm_days = storm / max(1, n_days) * 365.0        # Sturmtage/Jahr je Zelle

    _write_asc(out_dir, storm_days, lats, lons)
    ds.close()
    os.unlink(nc_path)
    print(f"Fertig: {os.path.join(out_dir, 'storm_days.asc.gz')} "
          f"(Schwelle {threshold} m/s, {n_years} Jahre).")
    return 0


def _write_asc(out_dir, arr, lats, lons) -> None:
    import numpy as np
    # Nach Norden-oben / Westen-links ordnen (ESRI-ASCII-Konvention).
    if lats[0] < lats[-1]:
        lats = lats[::-1]
        arr = arr[::-1, :]
    if lons[0] > lons[-1]:
        lons = lons[::-1]
        arr = arr[:, ::-1]
    cs = round(abs(float(lons[1] - lons[0])), 6)
    header = (
        f"NCOLS {arr.shape[1]}\nNROWS {arr.shape[0]}\n"
        f"XLLCORNER {float(lons.min()) - cs / 2:.6f}\n"
        f"YLLCORNER {float(lats.min()) - cs / 2:.6f}\n"
        f"CELLSIZE {cs}\nNODATA_VALUE -9999\n"
    )
    body = "\n".join(" ".join(f"{v:.2f}" for v in row) for row in arr)
    path = os.path.join(out_dir, "storm_days.asc.gz")
    with gzip.open(path, "wt", encoding="latin-1") as fh:
        fh.write(header + body)


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    raise SystemExit(main())
