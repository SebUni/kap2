"""Tests für das Flächenkompositions-Schichtmodell (Versiegelung, 100%-Budget).

Kein Netz, kein DB — nur synthetische Shapely-Geometrien gegen
``compute_cell_composition`` und die Kompositionstabellen.
"""

from __future__ import annotations

from shapely.geometry import box

from app.services.climate.heat import osm_data as o


# ── Invariante: jede Tabellenzeile summiert exakt auf 100 % ───────────────────

def test_all_composition_rows_sum_to_100():
    tables = {
        "BUILDING_ROW": {"_": o.BUILDING_ROW},
        "FALLBACK_ROW": {"_": o.FALLBACK_ROW},
        "ROAD": o.ROAD_COMPOSITION,
        "PAVED": o.PAVED_COMPOSITION,
        "LANDUSE": o.LANDUSE_COMPOSITION,
        "NATURAL": o.NATURAL_COMPOSITION,
        "LEISURE": o.LEISURE_COMPOSITION,
    }
    violations = []
    for tbl_name, tbl in tables.items():
        for key, row in tbl.items():
            total = sum(row.values())
            if abs(total - 100) > 1e-9:
                violations.append((tbl_name, key, total))
    assert not violations, f"Zeilen ≠ 100 %: {violations}"


def test_composition_categories_only_known_keys():
    for tbl in (o.LANDUSE_COMPOSITION, o.NATURAL_COMPOSITION, o.LEISURE_COMPOSITION,
                o.ROAD_COMPOSITION, o.PAVED_COMPOSITION):
        for row in tbl.values():
            assert set(row).issubset(set(o._COMP_CATS))


# ── Fallback für unkartierte Restfläche ───────────────────────────────────────

def test_empty_cell_falls_back_to_5pct_sealed():
    r = o.compute_cell_composition(box(0, 0, 1, 1), [], [], [], [])
    assert r["impervious_fraction"] == 0.05
    assert r["open_fraction"] == 0.95
    assert r["green_fraction"] == 0.0
    assert r["coverage_pct"] == 0.0


def test_partial_coverage_rest_is_fallback():
    # Waldpolygon deckt die linke Hälfte, Rest ist unkartiert → Fallback.
    cell = box(0, 0, 1, 1)
    lu = [{"geometry": box(0, 0, 0.5, 1), "landuse": "forest",
           "natural": "", "leisure": "", "surface": None}]
    r = o.compute_cell_composition(cell, [], [], [], lu)
    # V = 0.5·0.01 (Wald) + 0.5·0.05 (Fallback) = 0.03
    assert abs(r["impervious_fraction"] - 0.03) < 1e-6
    assert r["coverage_pct"] == 50.0


# ── Überlagerung: höhere Schicht sticht ───────────────────────────────────────

def test_building_on_residential_blends_via_residual_row():
    # Gebäude (25 % der Zelle, 100 % V) auf residential (Rest-Zeile 30 V / 55 G).
    cell = box(0, 0, 1, 1)
    bldg = [{"geometry": box(0, 0, 0.5, 0.5)}]  # Fläche 0.25
    lu = [{"geometry": box(0, 0, 1, 1), "landuse": "residential",
           "natural": "", "leisure": "", "surface": None}]
    r = o.compute_cell_composition(cell, bldg, [], [], lu)
    assert abs(r["impervious_fraction"] - (0.25 + 0.75 * 0.30)) < 1e-6  # 0.475
    assert abs(r["green_fraction"] - (0.75 * 0.55)) < 1e-6             # 0.4125
    assert abs(sum(r["composition"].values()) - 1.0) < 1e-6


def test_specific_landuse_beats_broad():
    # Friedhof (spezifisch) überdeckt linke Hälfte, residential die ganze Zelle.
    cell = box(0, 0, 1, 1)
    lu = [
        {"geometry": box(0, 0, 1, 1), "landuse": "residential",
         "natural": "", "leisure": "", "surface": None},
        {"geometry": box(0, 0, 0.5, 1), "landuse": "cemetery",
         "natural": "", "leisure": "", "surface": None},
    ]
    r = o.compute_cell_composition(cell, [], [], [], lu)
    # links Friedhof (20 V), rechts residential (30 V) → 0.25
    assert abs(r["impervious_fraction"] - (0.5 * 0.20 + 0.5 * 0.30)) < 1e-6
    assert r["dominant_landuse"] in {"cemetery", "residential"}


def test_water_layer_beats_broad_landuse():
    cell = box(0, 0, 1, 1)
    lu = [
        {"geometry": box(0, 0, 1, 1), "landuse": "forest",
         "natural": "", "leisure": "", "surface": None},
        {"geometry": box(0, 0, 1, 0.5), "landuse": "",
         "natural": "water", "leisure": "", "surface": None},
    ]
    r = o.compute_cell_composition(cell, [], [], [], lu)
    assert abs(r["water_fraction"] - 0.5) < 1e-6
    assert abs(r["forest_fraction"] - 0.5 * 0.95) < 1e-6


# ── surface-Tag sticht den Tag-Default (innerhalb des Features) ────────────────

def test_paved_square_paving_stones_is_75pct():
    cell = box(0, 0, 1, 1)
    paved = [{"geometry": box(0, 0, 1, 1), "kind": "square", "surface": "paving_stones"}]
    r = o.compute_cell_composition(cell, [], [], paved, [])
    assert abs(r["impervious_fraction"] - 0.75) < 1e-6


def test_paved_square_sett_is_65pct():
    cell = box(0, 0, 1, 1)
    paved = [{"geometry": box(0, 0, 1, 1), "kind": "square", "surface": "sett"}]
    r = o.compute_cell_composition(cell, [], [], paved, [])
    assert abs(r["impervious_fraction"] - 0.65) < 1e-6


def test_surface_override_increasing_seal_eats_green_not_open():
    # Kunstrasen-/Asche-Belag (asphalt) auf einem pitch → praktisch voll versiegelt,
    # die Differenz muss aus dem Grünanteil kommen, nicht in negatives „offen".
    row = o._apply_surface(dict(o.LEISURE_COMPOSITION["pitch"]), "asphalt")
    assert abs(row.get("V", 0) - 95) < 1e-9
    assert all(v >= 0 for v in row.values())
    assert abs(sum(row.values()) - 100) < 1e-9


def test_surface_override_grass_moves_rest_to_green():
    row = o._apply_surface(dict(o.LEISURE_COMPOSITION["pitch"]), "grass")
    assert abs(row.get("V", 0) - 5) < 1e-9
    assert row.get("G", 0) >= 80
    assert abs(sum(row.values()) - 100) < 1e-9


def test_surface_variant_suffix_is_normalised():
    assert o._norm_surface("paving_stones:30") == "paving_stones"
    assert o._norm_surface("asphalt;concrete") == "asphalt"
    assert o._norm_surface("unknown_stuff") is None


def test_unknown_surface_leaves_row_unchanged():
    base = {"V": 80, "O": 20}
    assert o._apply_surface(dict(base), None) == base
    assert o._apply_surface(dict(base), "wat") == base


# ── Straßen: tracktype/surface statt Pauschal-95 % ────────────────────────────

def test_track_grade_reduces_sealing():
    assert o._road_row({"highway": "track", "tracktype": "grade1", "surface": None})["V"] == 80
    assert o._road_row({"highway": "track", "tracktype": "grade4", "surface": None})["V"] == 15
    # Feldweg ohne tracktype: klar unter dem alten 0,95-Straßenwert.
    assert o._road_row({"highway": "track", "surface": None})["V"] == 20


def test_paved_road_surface_downgrades_pedestrian():
    # Fußweg default 70; unbefestigt (ground) → 10.
    assert o._road_row({"highway": "footway", "surface": "ground"})["V"] == 10
    # Asphaltierter Fußweg → 95.
    assert o._road_row({"highway": "footway", "surface": "asphalt"})["V"] == 95


# ── Anker: Wohngebietszelle nahe der bisherigen Pauschale 0,55 ────────────────

def test_residential_cell_anchor_near_055():
    # 25 % Gebäude, ~7 % Straße (als Platz-Polygon emuliert), Rest residential.
    cell = box(0, 0, 1, 1)
    bldg = [{"geometry": box(0, 0, 0.5, 0.5)}]                     # 0.25
    paved = [{"geometry": box(0.5, 0.5, 0.77, 0.77 + 1e-9), "kind": "square",
              "surface": "asphalt"}]                              # ~0.07, 95 % V
    lu = [{"geometry": box(0, 0, 1, 1), "landuse": "residential",
           "natural": "", "leisure": "", "surface": None}]
    r = o.compute_cell_composition(cell, bldg, [], paved, lu)
    assert 0.50 <= r["impervious_fraction"] <= 0.58
