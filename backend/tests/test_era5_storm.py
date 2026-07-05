"""Tests des ERA5-Sturmtage-Loaders (Stufe 5b).

Deckt ab:
  (a) Parsen eines gecachten ESRI-ASCII-Rasters (EPSG:4326) + Zentroid-Sampling.
  (b) NODATA / Punkt außerhalb → None.
  (c) Fehlt das Raster → None (Fallback auf den Konstantwert).
  (d) build_regional_context: storm_days aus ERA5 + Provenienz "era5"; ohne Raster
      Konstante 6.0 + Provenienz "regional_constant".

Kein Netz/CDS: es wird ein synthetisches Raster ins tmp-Cache-Verzeichnis geschrieben.
"""

from __future__ import annotations

import gzip
import os

import pytest

from app.services.climate import era5_storm


def _write_grid(cache_dir, rows, xll=5.0, yll=47.0, cs=1.0, nodata=-9999.0):
    ncols, nrows = len(rows[0]), len(rows)
    header = (f"NCOLS {ncols}\nNROWS {nrows}\nXLLCORNER {xll}\nYLLCORNER {yll}\n"
              f"CELLSIZE {cs}\nNODATA_VALUE {nodata}\n")
    body = "\n".join(" ".join(str(v) for v in r) for r in rows)
    os.makedirs(cache_dir, exist_ok=True)
    with gzip.open(os.path.join(cache_dir, "storm_days.asc.gz"), "wt", encoding="latin-1") as fh:
        fh.write(header + body)


@pytest.fixture
def storm_grid(monkeypatch, tmp_path):
    # 3×2-Raster (lon 5..8, lat 47..49), Nordzeile oben
    rows = [
        [10.0, 20.0, 30.0],   # Nordzeile (lat-Band 48..49)
        [4.0, 5.0, -9999.0],  # Südzeile (lat-Band 47..48); letzte Zelle NODATA
    ]
    monkeypatch.setattr(era5_storm.settings, "ERA5_STORM_CACHE_DIR", str(tmp_path))
    _write_grid(str(tmp_path), rows)
    era5_storm._reset_cache()
    yield
    era5_storm._reset_cache()


def test_sample_reads_correct_cell(storm_grid):
    # lon 5.5, lat 47.5 → col 0, Südzeile → 4.0
    assert era5_storm.storm_days_at(5.5, 47.5) == 4.0
    # lon 6.5, lat 48.5 → col 1, Nordzeile → 20.0
    assert era5_storm.storm_days_at(6.5, 48.5) == 20.0


def test_nodata_and_outside_is_none(storm_grid):
    assert era5_storm.storm_days_at(7.5, 47.5) is None   # NODATA-Zelle
    assert era5_storm.storm_days_at(99.0, 47.5) is None   # außerhalb


def test_missing_grid_is_none(monkeypatch, tmp_path):
    monkeypatch.setattr(era5_storm.settings, "ERA5_STORM_CACHE_DIR", str(tmp_path / "leer"))
    era5_storm._reset_cache()
    assert era5_storm.storm_days_at(6.5, 48.5) is None
    era5_storm._reset_cache()


def test_regional_context_uses_era5_when_available(monkeypatch):
    from app.services.engine import inputs
    from app.services.climate import dwd_cdc_grid, pegelonline
    monkeypatch.setattr(dwd_cdc_grid, "hot_days_at", lambda lon, lat: None)
    monkeypatch.setattr(dwd_cdc_grid, "frost_days_at", lambda lon, lat: None)
    monkeypatch.setattr(dwd_cdc_grid, "precip_days_ge20_at", lambda lon, lat: None)
    monkeypatch.setattr(dwd_cdc_grid, "precip_days_ge30_at", lambda lon, lat: None)
    monkeypatch.setattr(pegelonline, "low_flow_days_at", lambda lon, lat: None)

    monkeypatch.setattr(era5_storm, "storm_days_at", lambda lon, lat: 8.5)
    reg = inputs.build_regional_context("Bayern", False, centroid=(11.5, 48.1))
    assert reg["storm_days"] == 8.5
    assert reg["provenance"]["storm_days"] == "era5"

    monkeypatch.setattr(era5_storm, "storm_days_at", lambda lon, lat: None)
    reg2 = inputs.build_regional_context("Bayern", False, centroid=(11.5, 48.1))
    assert reg2["storm_days"] == 6.0
    assert reg2["provenance"]["storm_days"] == "regional_constant"


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-q"]))
