"""Measures for drought & water scarcity risk reduction."""

MEASURE_TYPES = {
    "unsealing": {
        "label": "Entsiegelung",
        "risk_reduction": 0.12,
        "cost_per_m2": 45.0,
    },
    "tree_planting": {
        "label": "Baumpflanzungen",
        "risk_reduction": 0.15,
        "cost_per_m2": 30.0,
    },
    "rainwater_harvesting": {
        "label": "Regenwassernutzung",
        "risk_reduction": 0.18,
        "cost_per_m2": 55.0,
    },
    "greywater_system": {
        "label": "Brauchwassersysteme",
        "risk_reduction": 0.10,
        "cost_per_m2": 70.0,
    },
}
