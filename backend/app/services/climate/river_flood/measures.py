"""Measures for river flooding risk reduction."""

MEASURE_TYPES = {
    "levee": {
        "label": "Deiche",
        "risk_reduction": 0.30,
        "cost_per_m2": 120.0,
    },
    "retention_area": {
        "label": "Retentionsflächen",
        "risk_reduction": 0.25,
        "cost_per_m2": 60.0,
    },
    "flood_wall": {
        "label": "Hochwasserschutzwände",
        "risk_reduction": 0.22,
        "cost_per_m2": 150.0,
    },
    "catchment_unsealing": {
        "label": "Entsiegelung im Einzugsgebiet",
        "risk_reduction": 0.12,
        "cost_per_m2": 40.0,
    },
}
