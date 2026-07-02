"""Operator-Schritte für Herkunftsdiagramme (Zellwerte + Formeln)."""

from __future__ import annotations

from typing import Any

OperatorStep = dict[str, Any]

# ── Zell-Ebene: Berechnungsschritte vor Zwischenwert-Knoten ─────────────────

CELL_OPERATORS: dict[str, list[OperatorStep]] = {
    "bldg_count": [{
        "op_kind": "count",
        "label": "Gebäude zählen",
        "tooltip": "Zählt die Anzahl der Gebäude-Polygone in der Zelle (OSM building=*).",
    }],
    "energy_infra_count": [{
        "op_kind": "count",
        "label": "Infrastruktur zählen",
        "tooltip": "Zählt Energie-Infrastrukturobjekte in der Zelle (OSM).",
    }],
    "water_wastewater_count": [{
        "op_kind": "count",
        "label": "Wasser/Abwasser zählen",
        "tooltip": "Zählt Wasser- und Abwasseranlagen in der Zelle (OSM).",
    }],
    "communication_count": [{
        "op_kind": "count",
        "label": "Kommunikation zählen",
        "tooltip": "Zählt Kommunikationsinfrastruktur in der Zelle (OSM).",
    }],
    "bldg_cov": [{
        "op_kind": "coverage",
        "label": "Gebäudeflächen ermitteln",
        "tooltip": "Summiert Gebäudegrundrissflächen und teilt durch die Zellfläche (OSM).",
    }],
    "road_cov": [{
        "op_kind": "coverage",
        "label": "Straßenflächen ermitteln",
        "tooltip": "Summiert Straßenflächen und teilt durch die Zellfläche (OSM).",
    }],
    "imp_lu": [{
        "op_kind": "coverage",
        "label": "Versiegelung aus Landnutzung",
        "tooltip": "Versiegelungsanteil aus OSM-Landnutzungsklassen der Zelle.",
    }],
    "imp_frac": [
        {
            "op_kind": "scale_factor",
            "label": "×",
            "factor": 0.95,
            "tooltip": "Straßenanteil wird mit 0,95 gewichtet (Fahrbahn vs. Gesamtstraße).",
            "input_keys": ["road_cov"],
        },
        {
            "op_kind": "add",
            "label": "+",
            "tooltip": "Summe aus gewichtetem Straßen- und Gebäudeanteil, mit Landnutzungs-Fallback.",
            "input_keys": ["bldg_cov", "road_cov", "imp_lu"],
        },
        {
            "op_kind": "clamp",
            "label": "Begrenzen",
            "tooltip": "Minimum 2 %, Maximum aus Landnutzung und Detailwerten.",
        },
    ],
    "green_frac": [{
        "op_kind": "coverage",
        "label": "Grünflächen ermitteln",
        "tooltip": "Anteil Grünflächen (Wiesen, Parks, Gärten) in der Zelle (OSM).",
    }],
    "forest_frac": [{
        "op_kind": "coverage",
        "label": "Waldflächen ermitteln",
        "tooltip": "Waldanteil der Zelle (OSM natural=wood/forest).",
    }],
    "farmland_frac": [{
        "op_kind": "coverage",
        "label": "Ackerflächen ermitteln",
        "tooltip": "Acker- und landwirtschaftlicher Anteil (OSM).",
    }],
    "water_frac": [{
        "op_kind": "coverage",
        "label": "Wasserflächen ermitteln",
        "tooltip": "Wasserflächenanteil der Zelle (OSM).",
    }],
    "water_adj": [{
        "op_kind": "neighbor",
        "label": "Gewässernähe (Nachbarn)",
        "tooltip": "Maximaler Wasseranteil in den 8 Nachbarzellen (OSM).",
    }],
    "water_prox": [{
        "op_kind": "coverage",
        "label": "Gewässernähe ermitteln",
        "tooltip": "Gewässernähe als Score aus Distanz zum nächsten Gewässer (OSM).",
    }],
    "vent_score": [{
        "op_kind": "neighbor",
        "label": "Belüftung berechnen",
        "tooltip": "Frischluft-Anteil: offene/grüne Nachbarzellen / 8 Nachbarn (OSM).",
    }],
    "uhi_delta": [{
        "op_kind": "weighted_sum",
        "label": "UHI-Modell",
        "tooltip": (
            "Städtische Wärmeinsel ΔT (K): Versiegelung, Gebäude, Albedo, "
            "abzüglich Kühlung durch Grün, Wasser, Bäume und Straßenschlucht."
        ),
    }],
    "depression_factor": [{
        "op_kind": "add",
        "label": "+",
        "tooltip": "Senkenneigung: Versiegelung + Gewässernähe − Belüftung.",
    }],
    "depression_proxy": [{
        "op_kind": "add",
        "label": "+",
        "tooltip": "Senken-Proxy aus Versiegelung, Gewässernähe und Belüftung.",
    }],
    "pop_density": [{
        "op_kind": "divide",
        "label": "÷",
        "tooltip": "Bevölkerungsdichte = Einwohner (Zensus) ÷ Zellfläche (km²).",
        "input_keys": ["pop", "area_km2"],
    }],
    "pop": [{
        "op_kind": "formula",
        "label": "Einwohnerzahl in Zelle ermitteln",
        "tooltip": "Einwohnerzahl der Zelle, anteilig aus Zensus-Raster verteilt.",
    }],
    "area_km2": [{
        "op_kind": "formula",
        "label": "Zellgrundfläche ermitteln",
        "tooltip": "Zellgröße (m)² umgerechnet in km².",
    }],
    "area_ha": [{
        "op_kind": "divide",
        "label": "÷",
        "tooltip": "Zellgröße (m)² umgerechnet in Hektar.",
    }],
    "industrial": [{
        "op_kind": "max",
        "label": "max",
        "tooltip": "Industrieflächen-Proxy: max(0, Versiegelung − Gebäude − Straßen).",
    }],
    "slope_deg": [{
        "op_kind": "coverage",
        "label": "Hangneigung ermitteln",
        "tooltip": "Hangneigung aus Digitalem Geländemodell (DEM).",
    }],
    "twi_norm": [{
        "op_kind": "coverage",
        "label": "TWI berechnen",
        "tooltip": "Topographischer Feuchteindex (TWI) aus DEM, normiert.",
    }],
    "hot_days": [{
        "op_kind": "formula",
        "label": "Heiße Tage ermitteln",
        "tooltip": "Regionale Anzahl heißer Tage pro Jahr (DWD, Bundesland).",
    }],
    "healthcare_access_score": [{
        "op_kind": "coverage",
        "label": "Gesundheitszugang ermitteln",
        "tooltip": "Gesundheitszugang aus Distanz zu Ärzten/Krankenhäusern (OSM).",
    }],
}

# Direkte Quell-Zuordnung (kein Operator, nur Quelle → Zwischenwert)
CELL_DIRECT: dict[str, list[str]] = {
    "canopy_frac": ["osm"],
    "svf": ["osm"],
    "avg_height": ["osm"],
    "glacier_frac": ["osm"],
    "flow_accum": ["osm"],
    "mean_elevation_m": ["dem"],
    "snow_elevation_factor": ["dem"],
    "frost_days": ["dwd"],
    "heavy_rain_index": ["dwd"],
    "storm_days": ["dwd"],
    "mean_temp_rise": ["dwd"],
    "mean_temp": ["dwd"],
    "soil_moisture_decline": ["dwd"],
    "surface_water_heating": ["dwd"],
    "glacier_loss_rate": ["dwd"],
    "snow_decline_rate_pct": ["dwd"],
    "snow_days": ["dwd"],
    "sea_level_rise": ["bsh"],
}

# ── Formel-Ebene: explizite Schritte vor Indikator-Knoten ───────────────────

FORMULA_OPERATORS: dict[str, list[OperatorStep]] = {
    "HEAT_WAVE": [
        {
            "op_kind": "scaling",
            "label": "Skalierung",
            "factor": 1.5,
            "value": 1.5,
            "unit": "×",
            "parameter_id": "hazards.HEAT_WAVE.param.uhi_weight",
            "tooltip": "UHI-ΔT mit Gewichtungsfaktor skalieren.",
            "input_keys": ["uhi_delta"],
        },
        {
            "op_kind": "add",
            "label": "+",
            "tooltip": "Heiße Tage + skalierte UHI-ΔT.",
            "input_keys": ["hot_days", "uhi_delta"],
        },
        {"op_kind": "clamp", "label": "Begrenzen", "tooltip": "Ergebnis auf 0…40 begrenzt."},
    ],
    "HEAVY_RAIN_FLOOD": [
        {"op_kind": "multiply", "label": "×", "tooltip": "Starkregen × Versiegelung × TWI × Senke."},
        {"op_kind": "clamp", "label": "Begrenzen", "tooltip": "Ergebnis auf 0…100 begrenzt."},
    ],
    "SUPPLY_CHAIN_NODES": [
        {"op_kind": "scale_factor", "label": "×", "factor": 6, "tooltip": "Industriefläche × 6."},
        {"op_kind": "scale_factor", "label": "×", "factor": 0.004, "tooltip": "Gebäudeanzahl × 0,004."},
        {"op_kind": "add", "label": "+", "tooltip": "Summe der beiden Terme."},
    ],
    "POPULATION_DENSITY": [{
        "op_kind": "divide",
        "label": "÷",
        "tooltip": "Bevölkerungsdichte = Einwohner ÷ Zellfläche (km²).",
        "input_keys": ["pop", "area_km2"],
    }],
    "COMPOUND_EVENT": [{
        "op_kind": "max",
        "label": "Maximum",
        "tooltip": "Maximum aus normierten Hitze-, Dürre- und Starkregen-Indizes.",
    }],
}


def formula_operators_for(code: str, formula: str) -> list[OperatorStep]:
    """Explizite Schritte oder generischer Formel-Operator als Fallback."""
    if code in FORMULA_OPERATORS:
        return FORMULA_OPERATORS[code]
    return [{
        "op_kind": "formula",
        "label": "Formel",
        "tooltip": formula or f"Berechnung für {code}.",
    }]
