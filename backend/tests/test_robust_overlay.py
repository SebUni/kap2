"""Verschneidung mit ungültigen OSM-Polygonen (TopologyException) kippt die Bewertung nicht."""
from shapely.geometry import Polygon, box

from app.services.climate.heat.osm_data import _robust_overlay


def test_bowtie_polygon_intersection_and_difference():
    bad = Polygon([(0, 0), (2, 2), (2, 0), (0, 2)])  # Schleife, ungültig
    cell = box(0, 0, 1, 1)
    assert abs(_robust_overlay("intersection", cell, bad).area - 0.5) < 1e-9
    assert abs(_robust_overlay("difference", cell, bad).area - 0.5) < 1e-9
