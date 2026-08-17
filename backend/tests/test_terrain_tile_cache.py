"""Tests für Terrain-Kachel-Disk-Cache, float32-Decode und RAM-LRU."""

from __future__ import annotations

import io
import os

import numpy as np
import pytest
from PIL import Image

from app.config import settings
from app.services import terrain_service


@pytest.fixture(autouse=True)
def clean_caches():
    terrain_service.clear_terrain_cache()
    yield
    terrain_service.clear_terrain_cache()


@pytest.fixture()
def tile_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "TERRAIN_TILE_CACHE_DIR", str(tmp_path))
    monkeypatch.setattr(settings, "TERRAIN_TILE_CACHE_TTL_S", 3600)
    return tmp_path


class _NoNet:
    def __init__(self, *a, **k):
        raise RuntimeError("Netzzugriff im Test verboten")


def _terrarium_png(elevation_m: float) -> tuple[bytes, np.ndarray]:
    """PNG mit konstanter Höhe im Terrarium-Encoding + erwartetes Array."""
    v = elevation_m + 32768.0
    r = int(v // 256)
    g = int(v % 256)
    b = int(round((v - int(v)) * 256))
    rgb = np.zeros((terrain_service.TILE_SIZE, terrain_service.TILE_SIZE, 3), dtype=np.uint8)
    rgb[:, :, 0] = r
    rgb[:, :, 1] = g
    rgb[:, :, 2] = b
    buf = io.BytesIO()
    Image.fromarray(rgb, "RGB").save(buf, format="PNG")
    expected = terrain_service._decode_terrarium(rgb.astype(np.float32).astype(np.uint8))
    return buf.getvalue(), expected


def test_decode_terrarium_is_float32_and_correct():
    rgb = np.zeros((2, 2, 3), dtype=np.uint8)
    rgb[:, :, 0] = 128  # 128*256 = 32768 → 0 m
    elev = terrain_service._decode_terrarium(rgb)
    assert elev.dtype == np.float32
    assert float(elev[0, 0]) == 0.0
    # Werte unter -500 m → NaN (Terrarium-NODATA-Konvention)
    rgb[:, :, 0] = 0
    rgb[:, :, 1] = 0
    assert np.isnan(terrain_service._decode_terrarium(rgb)).all()


def test_fetch_tile_reads_from_disk_without_network(tile_dir, monkeypatch):
    monkeypatch.setattr(terrain_service.httpx, "Client", _NoNet)
    png, _ = _terrarium_png(123.0)
    path = terrain_service._tile_disk_path(12, 100, 200)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(png)
    elev = terrain_service._fetch_tile(12, 100, 200)
    assert elev.dtype == np.float32
    assert abs(float(elev[0, 0]) - 123.0) < 0.01
    # Zweiter Zugriff: RAM-LRU (kein Disk-/Netz-Zugriff nötig)
    elev2 = terrain_service._fetch_tile(12, 100, 200)
    assert elev2 is elev


def test_failed_fetch_not_persisted(tile_dir, monkeypatch):
    monkeypatch.setattr(terrain_service.httpx, "Client", _NoNet)
    elev = terrain_service._fetch_tile(12, 1, 2)
    assert np.isnan(elev).all()
    assert not os.path.exists(terrain_service._tile_disk_path(12, 1, 2))


def test_ram_lru_evicts_oldest(monkeypatch):
    monkeypatch.setattr(terrain_service, "_TILE_LRU_MAX", 3)
    a = np.zeros((1, 1), dtype=np.float32)
    with terrain_service._cache_lock:
        for i in range(5):
            terrain_service._lru_put((1, i, 0), a)
        keys = list(terrain_service._tile_cache.keys())
    assert keys == [(1, 2, 0), (1, 3, 0), (1, 4, 0)]
