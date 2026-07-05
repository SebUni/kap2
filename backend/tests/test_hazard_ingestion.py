"""Tests zur echten Hazard-Datenanbindung (Stufe 2).

Deckt ab:
  (a) DWD-CDC-ASCII-Grid parsen + Zentroid-Sampling (Nord/Süd-Zeilenlogik).
  (b) NODATA und Punkt außerhalb des Rasters → ``None``.
  (c) Klimatologie (Mittel über Jahre) über synthetische Grids.
  (d) build_regional_context: heavy_rain_index aus echten Niederschlagsrastern +
      Provenienz-Kennzeichnung; Fallback auf den Proxy, wenn kein Raster vorliegt.

Kein Netzzugriff: die Downloads werden durch synthetische ``.asc.gz``-Bytes ersetzt.
"""

from __future__ import annotations

import gzip

import pytest

from app.services.climate import dwd_cdc_grid


def _asc_bytes(rows: list[list[float]], cellsize: float = 1000.0,
               xll: float = 0.0, yll: float = 0.0, nodata: float = -999.0) -> bytes:
    nrows = len(rows)
    ncols = len(rows[0])
    header = (
        f"NCOLS {ncols}\nNROWS {nrows}\nXLLCORNER {xll}\nYLLCORNER {yll}\n"
        f"CELLSIZE {cellsize}\nNODATA_VALUE {nodata}\n"
    )
    body = "\n".join(" ".join(str(v) for v in r) for r in rows)
    return gzip.compress((header + body).encode("latin-1"))


class _IdentityTransformer:
    """WGS84→GK3 durch Identität ersetzen: lon→x, lat→y (deterministisches Sampling)."""
    def transform(self, lon, lat):
        return lon, lat


@pytest.fixture
def synthetic_grid(monkeypatch, tmp_path):
    """Ein 3×2-Testraster für alle Jahre + isolierte Caches im tmp-Verzeichnis."""
    rows = [
        [10.0, 20.0, 30.0],   # Nordzeile (row 0)
        [40.0, 50.0, -999.0],  # Südzeile (row 1); letzte Zelle NODATA
    ]
    raw = _asc_bytes(rows)
    monkeypatch.setattr(dwd_cdc_grid, "_download_raw", lambda param, year: raw)
    monkeypatch.setattr(dwd_cdc_grid, "_get_transformer", _IdentityTransformer)
    monkeypatch.setattr(dwd_cdc_grid.settings, "DWD_CDC_CACHE_DIR", str(tmp_path))
    # Mem-Caches leeren, damit vorherige Läufe nicht durchschlagen
    dwd_cdc_grid._grid_cache.clear()
    dwd_cdc_grid._value_cache.clear()
    yield
    dwd_cdc_grid._grid_cache.clear()
    dwd_cdc_grid._value_cache.clear()


# ── (a) Parsen + Sampling ──────────────────────────────────────────────────────

def test_sample_year_reads_correct_cell(synthetic_grid):
    # x=500,y=500 → col 0, row 1 (Süden) → 40
    assert dwd_cdc_grid._sample_year("hot_days", 2020, 500.0, 500.0) == 40.0
    # x=1500,y=1500 → col 1, row 0 (Norden) → 20
    assert dwd_cdc_grid._sample_year("hot_days", 2020, 1500.0, 1500.0) == 20.0


# ── (b) NODATA + außerhalb ─────────────────────────────────────────────────────

def test_sample_year_nodata_is_none(synthetic_grid):
    # x=2500,y=500 → col 2, row 1 → NODATA -999 → None
    assert dwd_cdc_grid._sample_year("hot_days", 2020, 2500.0, 500.0) is None


def test_sample_year_out_of_range_is_none(synthetic_grid):
    assert dwd_cdc_grid._sample_year("hot_days", 2020, 99999.0, 500.0) is None


# ── (c) Klimatologie + neue Getter ─────────────────────────────────────────────

def test_climatology_averages_years(synthetic_grid):
    # Jedes Jahr liefert denselben Wert → Mittel == Wert
    assert dwd_cdc_grid.sample_climatology("precipGE20mm_days", 1500.0, 1500.0) == 20.0


def test_new_getters_route_to_params(synthetic_grid):
    assert dwd_cdc_grid.precip_days_ge20_at(500.0, 500.0) == 40.0
    assert dwd_cdc_grid.precip_days_ge30_at(500.0, 500.0) == 40.0
    assert dwd_cdc_grid.summer_days_at(500.0, 500.0) == 40.0


def test_unknown_param_is_none():
    assert dwd_cdc_grid.sample_climatology("does_not_exist", 1.0, 1.0) is None


# ── (d) build_regional_context: heavy_rain aus echten Rastern + Fallback ───────

def test_heavy_rain_index_from_real_precip_rasters(monkeypatch):
    from app.services.engine import inputs

    monkeypatch.setattr(dwd_cdc_grid, "hot_days_at", lambda lon, lat: None)
    monkeypatch.setattr(dwd_cdc_grid, "frost_days_at", lambda lon, lat: None)
    monkeypatch.setattr(dwd_cdc_grid, "precip_days_ge20_at", lambda lon, lat: 8.0)
    monkeypatch.setattr(dwd_cdc_grid, "precip_days_ge30_at", lambda lon, lat: 2.0)
    from app.services.climate import pegelonline
    monkeypatch.setattr(pegelonline, "low_flow_days_at", lambda lon, lat: None)

    reg = inputs.build_regional_context("Bayern", False, centroid=(11.5, 48.1))
    # index = min(100, 8·4 + 2·6) = 44
    assert reg["heavy_rain_index"] == 44.0
    assert reg["provenance"]["heavy_rain_index"] == "dwd_cdc_raster"


def test_heavy_rain_index_falls_back_to_proxy(monkeypatch):
    from app.services.engine import inputs

    monkeypatch.setattr(dwd_cdc_grid, "hot_days_at", lambda lon, lat: None)
    monkeypatch.setattr(dwd_cdc_grid, "frost_days_at", lambda lon, lat: None)
    monkeypatch.setattr(dwd_cdc_grid, "precip_days_ge20_at", lambda lon, lat: None)
    monkeypatch.setattr(dwd_cdc_grid, "precip_days_ge30_at", lambda lon, lat: None)
    from app.services.climate import pegelonline
    monkeypatch.setattr(pegelonline, "low_flow_days_at", lambda lon, lat: None)

    reg = inputs.build_regional_context("Bayern", False, centroid=(11.5, 48.1))
    assert reg["provenance"]["heavy_rain_index"] == "proxy_mean_temp"
    # Proxy-Formel: 40 + (mean_temp-9.5)*4  → jedenfalls ein endlicher Zahlenwert
    assert isinstance(reg["heavy_rain_index"], float)


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-q"]))
