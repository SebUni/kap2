"""Tests für die flächengewichtete Gebäudehöhen-Aggregation je Zelle."""

from __future__ import annotations

import pytest
from shapely.geometry import box

from app.services.climate.heat.osm_data import (
    _empty_building_metrics, compute_cell_buildings,
)


def test_hoehe_flaechengewichtet_statt_anzahlgewichtet():
    cell = box(0.0, 0.0, 0.001, 0.001)
    buildings = [
        # kleines Gebäude (Fläche a), 10 m
        {"geometry": box(0.0001, 0.0001, 0.0002, 0.0002), "height": 10.0},
        # großes Gebäude (Fläche 3a), 30 m
        {"geometry": box(0.0004, 0.0001, 0.0007, 0.0002), "height": 30.0},
    ]
    bm = compute_cell_buildings(cell, buildings, roads=[], trees=[])
    # flächengewichtet: (10·1 + 30·3) / 4 = 25; anzahlgewichtet wäre 20
    assert bm["avg_building_height"] == pytest.approx(25.0)
    assert bm["building_count"] == 2
    assert bm["building_coverage"] == pytest.approx(0.04, abs=0.001)


def test_teilweise_ueberlappendes_gebaeude_zaehlt_nur_anteilig():
    cell = box(0.0, 0.0, 0.001, 0.001)
    buildings = [
        # ragt zur Hälfte in die Zelle: nur der Schnitt wiegt
        {"geometry": box(-0.0001, 0.0, 0.0001, 0.0001), "height": 40.0},
        {"geometry": box(0.0004, 0.0, 0.0005, 0.0001), "height": 10.0},
    ]
    bm = compute_cell_buildings(cell, buildings, roads=[], trees=[])
    # Schnittflächen: je 1e-8 → Mittel (40+10)/2 = 25
    assert bm["avg_building_height"] == pytest.approx(25.0)


def test_leere_zelle_und_svf_platzhalter():
    cell = box(0.0, 0.0, 0.001, 0.001)
    bm = compute_cell_buildings(cell, buildings=[], roads=[], trees=[])
    assert bm["avg_building_height"] == 0.0
    # SVF ist nur noch Platzhalter (echtes SVF kommt aus dem Raster-Verfahren)
    assert bm["sky_view_factor"] == 1.0
    assert _empty_building_metrics()["sky_view_factor"] == 1.0
