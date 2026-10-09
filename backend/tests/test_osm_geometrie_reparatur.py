"""Ungültige OSM-Geometrie (Schleife) darf die Zellanalyse nicht abbrechen (T-1980).

Der Test ruft dieselben Funktionen auf wie ``_cell_worker`` in
``app.services.engine.inputs`` (``compute_cell_composition``,
``compute_cell_buildings``). Die Reparatur läuft wie in ``gather_cell_inputs``
einmal vor dem Indexaufbau über ``repair_invalid_geometries``. Fehlt diese
Funktion (Stand vor T-1980), wird nichts repariert; so lässt sich die
Rot-Simulation auf dem alten Stand fahren.
"""

import pytest
from shapely.geometry import Polygon, box

from app.services.climate.heat import osm_data
from app.services.climate.heat.osm_data import (
    compute_cell_buildings,
    compute_cell_composition,
)

_repair = getattr(osm_data, "repair_invalid_geometries", lambda feats, key="geometry": 0)

CELL = box(0.1, 0.1, 0.9, 0.9)  # Fläche 0,64
LOOP = Polygon([(0, 0), (1, 1), (1, 0), (0, 1)])  # Schleife, Fläche in der Zelle 0,32


def _feats(**extra):
    return [{"geometry": LOOP, **extra}]


def test_schleife_ist_ungueltig():
    assert not LOOP.is_valid


def test_gebaeude_in_zellanalyse():
    bldgs = _feats(height=10.0)
    _repair(bldgs)
    bm = compute_cell_buildings(CELL, bldgs, [], [])
    assert bm["building_count"] == 1
    assert bm["building_coverage"] == pytest.approx(0.5, abs=1e-3)
    lu = compute_cell_composition(CELL, bldgs, [], [], [])
    assert lu["coverage_pct"] == pytest.approx(50.0, abs=0.1)


def test_landnutzung_in_zellanalyse():
    feats = _feats(landuse="forest")
    _repair(feats)
    lu = compute_cell_composition(CELL, [], [], [], feats)
    assert lu["coverage_pct"] == pytest.approx(50.0, abs=0.1)
    assert lu["forest_fraction"] > 0.4


def test_versiegelte_flaeche_in_zellanalyse():
    paved = _feats(kind="square")
    _repair(paved)
    lu = compute_cell_composition(CELL, [], [], paved, [])
    assert lu["coverage_pct"] == pytest.approx(50.0, abs=0.1)
    assert lu["impervious_fraction"] > 0.4


def test_reparatur_zaehlt_und_verwirft_nichts():
    feats = [{"geometry": LOOP}, {"geometry": box(0, 0, 1, 1)}]
    if not hasattr(osm_data, "repair_invalid_geometries"):
        pytest.fail("repair_invalid_geometries fehlt")
    assert osm_data.repair_invalid_geometries(feats) == 1
    assert len(feats) == 2
    assert all(f["geometry"].is_valid for f in feats)
    assert osm_data.repair_invalid_geometries(feats) == 0
