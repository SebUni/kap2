"""Measures for sea level rise risk reduction."""

MEASURE_TYPES = {
    "levee_upgrade": {
        "label": "Deicherhöhung",
        "risk_reduction": 0.30,
        "cost_per_m2": 200.0,
    },
    "managed_retreat": {
        "label": "Rückbau / Rückzug",
        "risk_reduction": 0.40,
        "cost_per_m2": 50.0,
    },
    "salt_marsh": {
        "label": "Salzwiesen / natürlicher Küstenschutz",
        "risk_reduction": 0.15,
        "cost_per_m2": 30.0,
    },
    "storm_surge_barrier": {
        "label": "Sturmflutwehre",
        "risk_reduction": 0.35,
        "cost_per_m2": 350.0,
    },
}
