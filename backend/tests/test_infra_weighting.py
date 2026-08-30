"""Tests für die gewichtete KRITIS-Infrastruktur-Taxonomie (app/data/infra_assets).

Kernszenario: eine Zelle voller Strommasten darf nicht mehr wiegen als eine
Umspannwerk-Zelle oder eine Hochspannungs-Trassenzelle (Doppelzählungs-Fix).
"""
from app.data import infra_assets as ia
from app.services.engine import override_context


# ── Voltage-Parsing ───────────────────────────────────────────────────────────

def test_parse_voltage_single():
    assert ia.parse_voltage_kv({"voltage": "380000"}) == 380.0


def test_parse_voltage_multi_takes_max():
    assert ia.parse_voltage_kv({"voltage": "220000;110000"}) == 220.0


def test_parse_voltage_non_numeric_ignored():
    assert ia.parse_voltage_kv({"voltage": "medium"}) is None
    assert ia.parse_voltage_kv({"voltage": ""}) is None
    assert ia.parse_voltage_kv({}) is None


def test_parse_voltage_mixed_and_fallback_key():
    assert ia.parse_voltage_kv({"voltage": "medium;110000"}) == 110.0
    assert ia.parse_voltage_kv({"voltage:primary": "20000"}) == 20.0


# ── Klassifikation Energie ────────────────────────────────────────────────────

def test_power_supports_have_no_class():
    for val in ("tower", "pole", "portal", "catenary_mast", "insulator",
                "terminal", "switch", "busbar"):
        assert ia.classify_power_node({"power": val}) is None


def test_substation_classification():
    assert ia.classify_power_node(
        {"power": "substation", "substation": "transmission"}
    ) == "substation_transmission"
    assert ia.classify_power_node(
        {"power": "substation", "voltage": "110000"}
    ) == "substation_transmission"
    assert ia.classify_power_node({"power": "substation"}) == "substation_distribution"
    assert ia.classify_power_node(
        {"power": "substation", "substation": "minor_distribution"}
    ) == "substation_minor"
    assert ia.classify_power_node(
        {"power": "substation", "voltage": "10000"}
    ) == "substation_minor"


def test_generator_classification_filters_rooftop_solar():
    assert ia.classify_power_node(
        {"power": "generator", "generator:source": "solar"}
    ) is None
    assert ia.classify_power_node(
        {"power": "generator", "generator:source": "wind"}
    ) == "generator_wind"
    assert ia.classify_power_node(
        {"power": "generator", "generator:source": "biogas"}
    ) == "generator_other"


def test_line_classification_by_voltage():
    assert ia.classify_power_line({"power": "line", "voltage": "380000"}) == "line_ehv"
    assert ia.classify_power_line({"power": "line", "voltage": "110000"}) == "line_hv"
    # Ohne voltage-Tag ist power=line per OSM-Konvention Übertragungsnetz.
    assert ia.classify_power_line({"power": "line"}) == "line_hv"
    assert ia.classify_power_line({"power": "minor_line"}) == "line_mv"
    assert ia.classify_power_line({"power": "cable"}) == "line_mv"
    assert ia.classify_power_line({"power": "cable", "voltage": "220000"}) == "line_ehv"
    assert ia.classify_power_line({"power": "busbar"}) is None


# ── Klassifikation übrige Sektoren ────────────────────────────────────────────

def test_water_classification():
    assert ia.classify_water({"man_made": "wastewater_plant"}) == "wastewater_plant"
    assert ia.classify_water({"man_made": "pumping_station"}) == "pumping_station"
    assert ia.classify_water({"man_made": "storage_tank"}) == "reservoir"
    assert ia.classify_water({"man_made": "dyke"}) is None


def test_transport_priority_dedupes_multi_tagging():
    # Bahnhof mit zusätzlichem public_transport=station zählt nur als Bahnhof.
    assert ia.classify_transport(
        {"railway": "station", "public_transport": "station"}
    ) == "railway_station"
    assert ia.classify_transport({"railway": "halt"}) == "railway_halt"
    assert ia.classify_transport({"public_transport": "station"}) == "public_transport_station"
    assert ia.classify_transport({"amenity": "bus_station"}) == "bus_station"
    assert ia.classify_transport({"highway": "bus_stop"}) is None


def test_comm_classification():
    assert ia.classify_comm({"telecom": "data_center"}) == "data_center"
    assert ia.classify_comm({"building": "data_center"}) == "data_center"
    assert ia.classify_comm({"telecom": "exchange"}) == "exchange"
    assert ia.classify_comm({"man_made": "communications_tower"}) == "comm_tower"
    assert ia.classify_comm({"man_made": "mast"}) == "mast"
    assert ia.classify_comm({"tower:type": "communication"}) == "mast"
    assert ia.classify_comm({"communication:mobile_phone": "yes"}) == "antenna"
    assert ia.classify_comm({"man_made": "water_tower"}) is None


# ── Gewichte & Score ──────────────────────────────────────────────────────────

def test_weighted_score_regression_masts_vs_substation():
    """12 Masten (früher 12 Punkte) wiegen jetzt 0; Umspannwerk und Trasse dominieren."""
    weights = ia.resolve_weights("energy")
    mast_cell = ia.weighted_score({}, weights)  # Masten werden gar nicht klassifiziert
    line_cell = ia.weighted_score({"line_ehv": 1}, weights)
    substation_cell = ia.weighted_score({"substation_transmission": 1}, weights)
    assert mast_cell == 0.0
    assert 0 < line_cell < substation_cell


def test_resolve_weights_defaults_match_taxonomy():
    for sector, classes in ia.ASSET_CLASSES.items():
        weights = ia.resolve_weights(sector)
        for cls, spec in classes.items():
            assert weights[cls] == spec["weight"]


def test_resolve_weights_honors_override():
    pid = "exposures.ENERGY_INFRASTRUCTURE.param.w_substation_transmission"
    with override_context.override_scope({pid: 20.0}):
        assert ia.resolve_weights("energy")["substation_transmission"] == 20.0
    assert ia.resolve_weights("energy")["substation_transmission"] == 8.0  # Taxonomie-Default


# ── Zell-Zählung (compute_cell_infrastructure) ────────────────────────────────

def _square_cell():
    from shapely.geometry import Polygon
    return Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])


def test_compute_cell_weighted_scores_and_classes():
    from shapely.geometry import LineString
    from app.services.climate.heat.osm_data import compute_cell_infrastructure

    infra = {
        "energy_points": [
            {"lon": 0.5, "lat": 0.5, "cls": "substation_transmission"},
            {"lon": 5.0, "lat": 5.0, "cls": "plant"},  # außerhalb der Zelle
        ],
        "energy_lines": [
            {"geometry": LineString([(-1, 0.5), (2, 0.5)]), "cls": "line_ehv"},
        ],
        "energy_areas": [],
        "water_points": [{"lon": 0.2, "lat": 0.2, "cls": "water_works"}],
        "water_areas": [],
        "comm_points": [{"lon": 0.8, "lat": 0.8, "cls": "mast"}],
        "transport_points": [{"lon": 0.4, "lat": 0.6, "cls": "railway_halt"}],
    }
    m = compute_cell_infrastructure(_square_cell(), infra)
    # 8 (UW Übertragung, stärkstes Asset voll) + 0,5·6 (EHV-Querung, SATURATION_ALPHA)
    assert m["energy_infra_count"] == 11.0
    assert m["energy_infra_classes"] == {"substation_transmission": 1, "line_ehv": 1}
    assert m["water_wastewater_count"] == 10.0
    assert m["communication_count"] == 2.0
    assert m["transport_hub_count"] == 3.0
    assert m["transport_hub_classes"] == {"railway_halt": 1}


def test_compute_cell_weight_override_wiring():
    """Kommunale Gewichts-Overrides wirken bis in die Zell-Zählung durch."""
    from app.services.climate.heat.osm_data import compute_cell_infrastructure

    infra = {
        "energy_points": [{"lon": 0.5, "lat": 0.5, "cls": "substation_transmission"}],
        "energy_lines": [], "energy_areas": [],
        "water_points": [], "water_areas": [],
        "comm_points": [], "transport_points": [],
    }
    pid = "exposures.ENERGY_INFRASTRUCTURE.param.w_substation_transmission"
    with override_context.override_scope({pid: 3.0}):
        assert compute_cell_infrastructure(_square_cell(), infra)["energy_infra_count"] == 3.0
    assert compute_cell_infrastructure(_square_cell(), infra)["energy_infra_count"] == 8.0


def test_merge_energy_lines_joins_split_ways():
    """An Masten gesplittete Ways desselben Zugs zählen je Zelle nur einmal;
    getrennte Klassen und sich kreuzende Züge bleiben getrennt."""
    from shapely.geometry import LineString
    from app.services.climate.heat.osm_data import (
        _merge_energy_lines, compute_cell_infrastructure,
    )

    lines = [
        # Ein Leitungszug, an einem "Mast" bei x=0.5 in zwei Ways gesplittet.
        {"geometry": LineString([(-1, 0.5), (0.5, 0.5)]), "cls": "line_hv"},
        {"geometry": LineString([(0.5, 0.5), (2, 0.5)]), "cls": "line_hv"},
        # Kreuzender Zug anderer Klasse.
        {"geometry": LineString([(0.4, -1), (0.4, 2)]), "cls": "line_mv"},
    ]
    merged = _merge_energy_lines(lines)
    assert sorted(m["cls"] for m in merged) == ["line_hv", "line_mv"]

    infra = {"energy_points": [], "energy_lines": merged, "energy_areas": [],
             "water_points": [], "water_areas": [], "comm_points": [],
             "transport_points": []}
    m = compute_cell_infrastructure(_square_cell(), infra)
    assert m["energy_infra_classes"] == {"line_hv": 1, "line_mv": 1}
    # 3,0 (HV-Zug, stärkstes Asset voll) + 0,5·0,3 (MV-Zug, SATURATION_ALPHA)
    assert m["energy_infra_count"] == 3.15


# ── Monetär: klassenspezifische Ersatzwerte ───────────────────────────────────

def test_class_asset_values_and_override():
    from app.services.engine.impact.base import CellContext
    from app.services.engine.impact.monetary import _class_asset

    ctx = CellContext(
        ci={"energy_infra_classes": {"substation_transmission": 1, "line_mv": 2}},
        hev={}, hev_norm={}, indices={}, regional={},
    )
    assert _class_asset(ctx, "energy_infra_classes", "energy") == 5_000_000.0 + 2 * 20_000.0
    with override_context.override_scope(
        {"impact.energy_value_substation_transmission_eur": 1_000_000.0}
    ):
        assert _class_asset(ctx, "energy_infra_classes", "energy") == 1_000_000.0 + 40_000.0


def test_taxonomy_completeness():
    """Jede Klasse trägt Label, Gewicht, Ersatzwert und Infokasten-Doku."""
    for sector, classes in ia.ASSET_CLASSES.items():
        assert sector in ia.SECTOR_EXPOSURE
        assert sector in ia.SECTOR_CLASSES_KEY
        for cls, spec in classes.items():
            assert spec["label"], (sector, cls)
            assert spec["weight"] > 0, (sector, cls)
            assert spec["value_eur"] > 0, (sector, cls)
            assert len(spec["source_detail"]) > 30, (sector, cls)
