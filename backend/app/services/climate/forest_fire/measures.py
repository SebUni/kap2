"""Measures for forest fire risk reduction."""

MEASURE_TYPES = {
    "firebreak": {
        "label": "Waldbrandschneisen",
        "risk_reduction": 0.20,
        "cost_per_m2": 25.0,
    },
    "deciduous_conversion": {
        "label": "Laubwald-Umbau",
        "risk_reduction": 0.25,
        "cost_per_m2": 15.0,
    },
    "irrigation_system": {
        "label": "Bewässerungssysteme",
        "risk_reduction": 0.15,
        "cost_per_m2": 40.0,
    },
    "fire_pond": {
        "label": "Löschteiche",
        "risk_reduction": 0.12,
        "cost_per_m2": 90.0,
    },
}
