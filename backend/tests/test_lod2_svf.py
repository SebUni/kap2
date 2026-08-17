"""Tests für das Horizontwinkel-SVF (Raster-Verfahren), ohne Netz."""

from __future__ import annotations

import os

import numpy as np
import pytest
from pyproj import Transformer
from shapely.geometry import Polygon, box
from shapely.ops import transform as shp_transform

from app.config import settings
from app.services.geodata.lod2 import svf as svf_mod
from app.services.geodata.lod2.svf import (
    _horizon_svf, _rasterize_heights, compute_svf_for_cells,
)

_TO_WGS = Transformer.from_crs("EPSG:25832", "EPSG:4326", always_xy=True)


def _utm_square_wgs84(x0: float, y0: float, size: float) -> Polygon:
    return shp_transform(_TO_WGS.transform, box(x0, y0, x0 + size, y0 + size))


def test_flaches_raster_svf_1():
    H = np.zeros((40, 40), dtype=np.float32)
    out = _horizon_svf(H, res_m=5.0, radius_m=100.0, n_dirs=16)
    assert float(out.min()) == pytest.approx(1.0)


def test_canyon_analytischer_wert():
    """Unendlicher Canyon W=20 m, H=10 m → SVF(Straßenmitte) = 1/√2 ≈ 0,707.

    Analytik: tanγ(φ) = (2H/W)·|cosφ| und ∫dφ/(1+cos²φ) = 2π/√2. Die
    Rasterdiskretisierung (5-m-Pixel, Wandabstand 10/15 m je Straßenpixel)
    weicht systematisch leicht ab — Toleranz ±0,08.
    """
    n = 60
    H = np.zeros((n, n), dtype=np.float32)
    street = (28, 32)               # 4 Spalten = 20 m Straße
    H[:, :street[0]] = 10.0
    H[:, street[1]:] = 10.0
    out = _horizon_svf(H, res_m=5.0, radius_m=100.0, n_dirs=16)
    mid = out[n // 2, street[0] + 1:street[1] - 1]   # innere Straßenpixel
    assert float(mid.mean()) == pytest.approx(0.7071, abs=0.08)


def test_innenhof_fast_geschlossen():
    n = 41
    H = np.full((n, n), 30.0, dtype=np.float32)
    H[n // 2, n // 2] = 0.0
    out = _horizon_svf(H, res_m=5.0, radius_m=100.0, n_dirs=16)
    assert float(out[n // 2, n // 2]) < 0.15


def test_hoehere_waende_kleineres_svf():
    def canyon(h):
        H = np.zeros((60, 60), dtype=np.float32)
        H[:, :28] = h
        H[:, 32:] = h
        return float(_horizon_svf(H, 5.0, 100.0, 16)[30, 29])

    assert canyon(20.0) < canyon(10.0) < 1.0


def test_rasterize_heights_setzt_gebaeudepixel():
    b = {"geometry": _utm_square_wgs84(350000, 5650000, 10.0), "height": 12.0}
    H, x0, y0 = _rasterize_heights(
        [b], bounds=(349990, 5649990, 350020, 5650020), res_m=5.0)
    assert H.shape == (6, 6)
    assert float(H.max()) == pytest.approx(12.0)
    # Pixelzentren 350002.5/350007.5 × 5650002.5/5650007.5 liegen im Gebäude
    assert float(H[2:4, 2:4].min()) == pytest.approx(12.0)
    assert float(H.sum()) == pytest.approx(4 * 12.0)


def test_compute_svf_for_cells_ende_zu_ende(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "LOD2_CACHE_DIR", str(tmp_path))
    svf_mod._ram_cache.clear()

    cell = {"geometry": _utm_square_wgs84(350000, 5650000, 100.0)}
    # Hochhausriegel 40×20 m, 30 m hoch, mitten in der Zelle
    bldg = {"geometry": _utm_square_wgs84(350030, 5650040, 30.0), "height": 30.0}

    out = compute_svf_for_cells([cell], [bldg], "lod2")
    assert len(out) == 1
    assert 0.0 < out[0] < 1.0
    disk = os.path.join(str(tmp_path), "svf")
    assert os.listdir(disk), "SVF-Disk-Cache wurde nicht geschrieben"

    # Zweiter Aufruf: identisches Ergebnis (RAM-/Disk-Cache)
    assert compute_svf_for_cells([cell], [bldg], "lod2") == out


def test_compute_svf_ohne_gebaeude_ist_1(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "LOD2_CACHE_DIR", str(tmp_path))
    cell = {"geometry": _utm_square_wgs84(350000, 5650000, 100.0)}
    assert compute_svf_for_cells([cell], [], "osm") == [1.0]
