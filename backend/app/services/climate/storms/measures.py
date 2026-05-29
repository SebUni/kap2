"""Measures for storm & extreme weather risk reduction."""

MEASURE_TYPES = {
    "windbreak_hedge": {
        "label": "Windschutzhecken",
        "risk_reduction": 0.15,
        "cost_per_m2": 15.0,
    },
    "building_reinforcement": {
        "label": "Gebäudeverstärkung",
        "risk_reduction": 0.20,
        "cost_per_m2": 85.0,
    },
    "storm_resistant_trees": {
        "label": "Sturmfeste Baumarten",
        "risk_reduction": 0.12,
        "cost_per_m2": 20.0,
    },
}
