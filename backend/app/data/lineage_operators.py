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
    "transport_hub_count": [{
        "op_kind": "count",
        "label": "Verkehrsknoten zählen",
        "tooltip": "Zählt Verkehrsknoten (Bahnhof/Halt/ÖPNV-Station) in der Zelle (OSM).",
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
            "param_label": "Fahrbahnanteil an Straßenfläche",
            "tooltip": "Straßenanteil wird mit 0,95 gewichtet (Fahrbahn vs. Gesamtstraße).",
            "input_keys": ["road_cov"],
        },
        {
            "op_kind": "add",
            "label": "+",
            "tooltip": (
                "Summe aus gewichtetem Straßen- und Gebäudeanteil, mit Landnutzungs-"
                "Fallback; Ergebnis begrenzt auf mindestens 2 %."
            ),
            "input_keys": ["bldg_cov", "road_cov", "imp_lu"],
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
        "tooltip": ("Bevölkerungsdichte aus Zensus-Einwohnern und Zellfläche.\n"
        r"$$\text{Einwohner} / \text{Fläche}\ [\mathrm{km}^{2}]$$"),
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
        "label": "Maximum",
        "tooltip": ("Industrieflächen-Anteil aus den OSM-Flächenanteilen.\n"
        r"$$\max\bigl(0,\ \text{Versiegelung} - \text{Gebäude} - \text{Straßen}\bigr)$$"),
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
        "label": "Nähe-Score berechnen",
        "tooltip": (
            "Wandelt die Distanz zur nächsten Einrichtung (Krankenhaus/Arzt/Apotheke, "
            "OSM) in einen Nähe-Score 0…1 um (0 = weit entfernt, 1 = direkt benachbart)."
        ),
    }],
    # Ermittlungs-Operatoren für die CELL_DIRECT-Zwischenwerte: einheitlich hat
    # JEDER Quelle→Zwischenwert-Schritt einen Ableitungs-Operator.
    "canopy_frac": [{
        "op_kind": "coverage",
        "label": "Baumkronen ermitteln",
        "tooltip": "Baumkronenanteil aus OSM-Baumdaten der Zelle.",
    }],
    "svf": [{
        "op_kind": "formula",
        "label": "Himmelssicht berechnen",
        "tooltip": "Himmelsichtfaktor aus Gebäudehöhen und -anordnung (OSM).",
    }],
    "avg_height": [{
        "op_kind": "coverage",
        "label": "Gebäudehöhen mitteln",
        "tooltip": "Mittlere Gebäudehöhe über die OSM-Gebäude der Zelle.",
    }],
    "glacier_frac": [{
        "op_kind": "coverage",
        "label": "Gletscherflächen ermitteln",
        "tooltip": "Gletscheranteil der Zelle (OSM natural=glacier).",
    }],
    "flow_accum": [{
        "op_kind": "formula",
        "label": "Flussakkumulation berechnen",
        "tooltip": "Wasserfluss-Akkumulation aus dem Digitalen Geländemodell (DEM).",
    }],
    "mean_elevation_m": [{
        "op_kind": "coverage",
        "label": "Geländehöhe mitteln",
        "tooltip": "Mittlere Geländehöhe der Zelle aus dem DEM.",
    }],
    "snow_elevation_factor": [{
        "op_kind": "formula",
        "label": "Höhenfaktor berechnen",
        "tooltip": "Höhenmodulation für Schnee/Gletscher aus der Geländehöhe (DEM).",
    }],
    "frost_days": [{
        "op_kind": "formula",
        "label": "Frosttage ermitteln",
        "tooltip": "Regionale Frosttage pro Jahr (DWD CDC, am Gemeindezentroid).",
    }],
    "heavy_rain_index": [{
        "op_kind": "formula",
        "label": "Starkregenindex ermitteln",
        "tooltip": "Starkregenindex aus DWD-CDC-Rastern (Tage mit ≥ 20/30 mm Niederschlag).",
    }],
    "storm_days": [{
        "op_kind": "formula",
        "label": "Sturmtage ermitteln",
        "tooltip": "Sturmtage pro Jahr aus der regionalen Böenklimatologie.",
    }],
    "mean_temp_rise": [{
        "op_kind": "formula",
        "label": "Temperaturanstieg ermitteln",
        "tooltip": "Temperaturanstieg gegenüber der Referenzperiode (DWD, regional).",
    }],
    "mean_temp": [{
        "op_kind": "formula",
        "label": "Mitteltemperatur ermitteln",
        "tooltip": "Jahresmitteltemperatur (DWD, regional).",
    }],
    "soil_moisture_decline": [{
        "op_kind": "formula",
        "label": "Bodenfeuchte-Trend ermitteln",
        "tooltip": "Bodenfeuchte-Rückgang (DWD, regional).",
    }],
    "surface_water_heating": [{
        "op_kind": "formula",
        "label": "Gewässererwärmung ermitteln",
        "tooltip": "Erwärmungstrend der Oberflächengewässer (DWD, regional).",
    }],
    "glacier_loss_rate": [{
        "op_kind": "formula",
        "label": "Gletscherschwund ermitteln",
        "tooltip": "Gletscherschwund-Rate (Parameter/DWD, regional).",
    }],
    "snow_decline_rate_pct": [{
        "op_kind": "formula",
        "label": "Schneetrend ermitteln",
        "tooltip": "Trend des Schneedecken-Rückgangs (DWD, regional).",
    }],
    "snow_days": [{
        "op_kind": "formula",
        "label": "Schneedeckentage ermitteln",
        "tooltip": "Schneedeckentage pro Jahr (DWD, regional).",
    }],
    "sea_level_rise": [{
        "op_kind": "formula",
        "label": "Meeresspiegeltrend ermitteln",
        "tooltip": "Regionaler Meeresspiegelanstieg (BSH).",
    }],
    "area_m2": [{
        "op_kind": "formula",
        "label": "Zellfläche ermitteln",
        "tooltip": "Zellfläche in m² aus der Rastergeometrie (100 × 100 m).",
    }],
    "share_over_65": [{
        "op_kind": "coverage",
        "label": "Altersanteil ≥ 65 ermitteln",
        "tooltip": "Anteil der Bevölkerung ab 65 Jahren aus dem Zensus-Raster der Zelle.",
    }],
    "share_under_18": [{
        "op_kind": "coverage",
        "label": "Altersanteil < 18 ermitteln",
        "tooltip": "Anteil der Bevölkerung unter 18 Jahren aus dem Zensus-Raster der Zelle.",
    }],
    "living_area_per_person": [{
        "op_kind": "coverage",
        "label": "Wohnfläche ermitteln",
        "tooltip": "Wohnfläche je Person aus dem Zensus-Raster der Zelle.",
    }],
    "owner_share": [{
        "op_kind": "coverage",
        "label": "Eigentümerquote ermitteln",
        "tooltip": "Eigentümerquote der Wohnungen aus dem Zensus-Raster der Zelle.",
    }],
    "net_cold_rent": [{
        "op_kind": "coverage",
        "label": "Nettokaltmiete ermitteln",
        "tooltip": "Mittlere Nettokaltmiete aus dem Zensus-Raster der Zelle.",
    }],
    "building_age_mean": [{
        "op_kind": "coverage",
        "label": "Gebäudealter mitteln",
        "tooltip": "Mittleres Gebäudealter aus Zensus-/OSM-Gebäudedaten der Zelle.",
    }],
    "dist_hospital_m": [{
        "op_kind": "coverage",
        "label": "Distanz messen",
        "tooltip": "Distanz zum nächsten Krankenhaus in Metern (OSM).",
    }],
    "dist_doctor_m": [{
        "op_kind": "coverage",
        "label": "Distanz messen",
        "tooltip": "Distanz zur nächsten Arztpraxis/Klinik in Metern (OSM).",
    }],
    "dist_pharmacy_m": [{
        "op_kind": "coverage",
        "label": "Distanz messen",
        "tooltip": "Distanz zur nächsten Apotheke in Metern (OSM).",
    }],
    "dyke_prox": [{
        "op_kind": "coverage",
        "label": "Deichnähe ermitteln",
        "tooltip": (
            "Wandelt die Distanz zu Deich-/Küstenschutzanlagen (OSM) in einen "
            "Nähe-Score 0…1 um."
        ),
    }],
    "emergency_access_score": [{
        "op_kind": "coverage",
        "label": "Erreichbarkeit berechnen",
        "tooltip": (
            "Wandelt die Distanz zu Feuerwehr/Rettungsdiensten (OSM) in einen "
            "Erreichbarkeits-Score 0…1 um."
        ),
    }],
    "slope_factor": [{
        "op_kind": "formula",
        "label": "Hangfaktor berechnen",
        "tooltip": "Hangneigung (DEM) normiert, moduliert mit dem Belüftungsanteil (OSM).",
    }],
    "slope_proxy": [{
        "op_kind": "formula",
        "label": "Hangfaktor berechnen",
        "tooltip": "Hangneigung (DEM) normiert, moduliert mit dem Belüftungsanteil (OSM).",
    }],
}

# Direkte Quell-Zuordnung (Quelle je Zwischenwert; Ableitungs-Operator s. oben)
CELL_DIRECT: dict[str, list[str]] = {
    "canopy_frac": ["osm"],
    "svf": ["osm"],
    "avg_height": ["osm"],
    "glacier_frac": ["osm"],
    "flow_accum": ["dem"],
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
            # bewusst KEINE parameter_id: der Faktor ist in indicators.py fest
            # verdrahtet (Modellkonstante), ein Registry-Override wäre wirkungslos.
            # Er erscheint stattdessen als (nicht editierbarer) Parameterknoten.
            "param_label": "UHI-Gewichtung",
            "tooltip": "UHI-ΔT mit festem Gewichtungsfaktor 1,5 skalieren (Modellkonstante).",
            "input_keys": ["uhi_delta"],
        },
        {
            "op_kind": "add",
            "label": "+",
            "tooltip": ("Heiße Tage + skalierte UHI-ΔT; Ergebnis auf 0…40 begrenzt.\n"
                        r"$$\min\bigl(40,\ H_{\mathrm{Tage}} + 1{,}5 \cdot \Delta T_{\mathrm{UHI}}\bigr)$$"),
            "input_keys": ["hot_days", "uhi_delta"],
        },
    ],
    "HEAVY_RAIN_FLOOD": [
        {
            "op_kind": "multiply",
            "label": "×",
            "tooltip": ("Starkregen × Versiegelung × TWI × Senke; Ergebnis auf 0…100 begrenzt.\n"
                r"$$\min\bigl(100,\ \text{Starkregen} \cdot (0{,}4 + \text{Versiegelung}) \cdot \mathrm{TWI} \cdot \text{Senke}\bigr)$$"),
        },
    ],
    "SUPPLY_CHAIN_NODES": [
        {"op_kind": "scale_factor", "label": "×", "factor": 6,
         "param_label": "Gewichtung Industriefläche",
         "tooltip": "Industriefläche mit Faktor 6 gewichten (Modellkonstante)."},
        {"op_kind": "scale_factor", "label": "×", "factor": 0.004,
         "param_label": "Gewichtung Gebäudeanzahl",
         "tooltip": "Gebäudeanzahl mit Faktor 0,004 gewichten (Modellkonstante)."},
        {"op_kind": "add", "label": "+",
         "tooltip": ("Summe der beiden Terme.\n"
                     r"$$6 \cdot \text{Industrie} + 0{,}004 \cdot \text{Gebäude}$$")},
    ],
    "INFRA_CRITICALITY": [
        {"op_kind": "multiply", "label": "×", "tooltip": "Jeder KRITIS-Sektor mit seinem Gewicht (BBK) multipliziert."},
        {
            "op_kind": "add",
            "label": "+",
            "tooltip": (
                "Gewichtete Summe aus Energie, Wasser, IT/Kommunikation, Gesundheit "
                "und Verkehr; Ergebnis auf 0…100 begrenzt.\n"
                r"$$\min\Bigl(100,\ \sum_{i} w_{i} \cdot n_{i}\Bigr)$$"
            ),
        },
    ],
    "POPULATION_DENSITY": [{
        "op_kind": "divide",
        "label": "÷",
        "tooltip": ("Bevölkerungsdichte aus Einwohnern und Zellfläche.\n"
        r"$$\text{Einwohner} / \text{Fläche}\ [\mathrm{km}^{2}]$$"),
        "input_keys": ["pop", "area_km2"],
    }],
    "COMPOUND_EVENT": [{
        "op_kind": "max",
        "label": "Maximum",
        "tooltip": ("Maximum aus normierten Hitze-, Dürre- und Starkregen-Indizes.\n"
        r"$$\max\bigl(\hat{H}_{\text{Hitze}},\ \hat{H}_{\text{Dürre}},\ \hat{H}_{\text{Starkregen}}\bigr)$$"),
    }],
}


def formula_operators_for(code: str, formula: str) -> list[OperatorStep]:
    """Explizite Schritte oder generischer Formel-Operator als Fallback."""
    if code in FORMULA_OPERATORS:
        return FORMULA_OPERATORS[code]
    return [{
        "op_kind": "formula",
        "label": "Formel",
        # "Berechnung:"-Präfix, damit das Frontend die Formel als LaTeX rendert
        "tooltip": (
            f"Berechnung: {formula}" if formula else f"Berechnung für {code}."
        ),
    }]
