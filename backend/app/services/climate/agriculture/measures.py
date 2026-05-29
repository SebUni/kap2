"""Measures for agriculture yield variability risk reduction."""

MEASURE_TYPES = {
    "irrigation_system": {
        "label": "Bewässerungssysteme",
        "risk_reduction": 0.22,
        "cost_per_m2": 35.0,
    },
    "agroforestry": {
        "label": "Agroforstwirtschaft",
        "risk_reduction": 0.18,
        "cost_per_m2": 20.0,
    },
    "windbreak_hedge": {
        "label": "Windschutzhecken",
        "risk_reduction": 0.12,
        "cost_per_m2": 15.0,
    },
    "soil_protection": {
        "label": "Bodenschutzmaßnahmen",
        "risk_reduction": 0.15,
        "cost_per_m2": 25.0,
    },
}
