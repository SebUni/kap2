"""Measures for heavy rain & urban flooding risk reduction."""

MEASURE_TYPES = {
    "unsealing": {
        "label": "Entsiegelung",
        "risk_reduction": 0.15,
        "cost_per_m2": 45.0,
    },
    "retention_basin": {
        "label": "Retentionsflächen",
        "risk_reduction": 0.20,
        "cost_per_m2": 80.0,
    },
    "green_roof_rain": {
        "label": "Gründächer (Regenwasser)",
        "risk_reduction": 0.12,
        "cost_per_m2": 65.0,
    },
    "infiltration_trench": {
        "label": "Rigolen / Versickerungsmulden",
        "risk_reduction": 0.18,
        "cost_per_m2": 55.0,
    },
}
