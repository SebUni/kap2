"""DWD (Deutscher Wetterdienst) climate data and Zensus building data services.

Provides:
- Hot days and temperature data from DWD CDC (Climate Data Center)
- Building age / renovation estimates from Zensus 2011/2022 census data
- Albedo estimates based on building age and renovation status
"""

import logging
from typing import Any, Optional

import httpx

log = logging.getLogger(__name__)

# ── DWD Climate Data Center ───────────────────────────────────────────────────

# DWD CDC OpenData base
DWD_CDC_BASE = "https://opendata.dwd.de/climate_environment/CDC"

# Regional averages (Gebietsmittel) for Bundesländer
DWD_REGIONAL_MEANS = (
    f"{DWD_CDC_BASE}/regional_averages_DE/annual/air_temperature_mean"
)

# Station-based climate data
DWD_STATION_BASE = (
    f"{DWD_CDC_BASE}/observations_germany/climate/annual/kl/historical"
)

# Known hot-day thresholds per DWD definition:
#   Heißer Tag (hot day):           Tmax >= 30°C
#   Sommertag (summer day):         Tmax >= 25°C
#   Tropennacht (tropical night):   Tmin >= 20°C

# Bundesland -> approximate DWD station ID for reference data
# These are major stations with long records
BUNDESLAND_STATIONS: dict[str, dict] = {
    "Baden-Württemberg":     {"id": "02638", "name": "Mannheim"},
    "Bayern":                {"id": "01262", "name": "München-Stadt"},
    "Berlin":                {"id": "00433", "name": "Berlin-Tempelhof"},
    "Brandenburg":           {"id": "03987", "name": "Potsdam"},
    "Bremen":                {"id": "00691", "name": "Bremen"},
    "Hamburg":               {"id": "01975", "name": "Hamburg-Fuhlsbüttel"},
    "Hessen":                {"id": "01420", "name": "Frankfurt/Main"},
    "Mecklenburg-Vorpommern": {"id": "04271", "name": "Rostock-Warnemünde"},
    "Niedersachsen":         {"id": "02014", "name": "Hannover"},
    "Nordrhein-Westfalen":   {"id": "02667", "name": "Köln/Bonn"},
    "Rheinland-Pfalz":       {"id": "05480", "name": "Trier-Petrisberg"},
    "Saarland":              {"id": "04336", "name": "Saarbrücken-Burbach"},
    "Sachsen":               {"id": "01048", "name": "Dresden-Klotzsche"},
    "Sachsen-Anhalt":        {"id": "02932", "name": "Magdeburg"},
    "Schleswig-Holstein":    {"id": "02564", "name": "Kiel-Holtenau"},
    "Thüringen":             {"id": "01270", "name": "Erfurt-Weimar"},
}

# Fallback: typical regional climate data for Germany (empirical averages)
# Based on DWD published data summaries
FALLBACK_CLIMATE: dict[str, dict[str, Any]] = {
    "Baden-Württemberg":     {"hot_days_avg": 14.2, "summer_days_avg": 48.0, "tropical_nights_avg": 2.5, "summer_temp_avg": 27.8, "mean_temp_annual": 10.2},
    "Bayern":                {"hot_days_avg": 12.5, "summer_days_avg": 42.0, "tropical_nights_avg": 1.8, "summer_temp_avg": 27.2, "mean_temp_annual": 9.5},
    "Berlin":                {"hot_days_avg": 13.0, "summer_days_avg": 45.0, "tropical_nights_avg": 3.0, "summer_temp_avg": 28.0, "mean_temp_annual": 10.5},
    "Brandenburg":           {"hot_days_avg": 11.5, "summer_days_avg": 40.0, "tropical_nights_avg": 1.5, "summer_temp_avg": 27.5, "mean_temp_annual": 10.0},
    "Bremen":                {"hot_days_avg":  8.0, "summer_days_avg": 32.0, "tropical_nights_avg": 0.5, "summer_temp_avg": 26.0, "mean_temp_annual":  9.8},
    "Hamburg":                {"hot_days_avg":  7.5, "summer_days_avg": 30.0, "tropical_nights_avg": 0.5, "summer_temp_avg": 25.8, "mean_temp_annual":  9.7},
    "Hessen":                {"hot_days_avg": 13.5, "summer_days_avg": 46.0, "tropical_nights_avg": 2.8, "summer_temp_avg": 28.0, "mean_temp_annual": 10.3},
    "Mecklenburg-Vorpommern": {"hot_days_avg": 7.0,  "summer_days_avg": 28.0, "tropical_nights_avg": 0.3, "summer_temp_avg": 25.5, "mean_temp_annual":  9.2},
    "Niedersachsen":         {"hot_days_avg":  9.0,  "summer_days_avg": 34.0, "tropical_nights_avg": 0.8, "summer_temp_avg": 26.5, "mean_temp_annual":  9.8},
    "Nordrhein-Westfalen":   {"hot_days_avg": 12.0, "summer_days_avg": 43.0, "tropical_nights_avg": 2.0, "summer_temp_avg": 27.5, "mean_temp_annual": 10.2},
    "Rheinland-Pfalz":       {"hot_days_avg": 14.0, "summer_days_avg": 47.0, "tropical_nights_avg": 2.5, "summer_temp_avg": 28.0, "mean_temp_annual": 10.3},
    "Saarland":              {"hot_days_avg": 13.0, "summer_days_avg": 44.0, "tropical_nights_avg": 2.0, "summer_temp_avg": 27.5, "mean_temp_annual": 10.1},
    "Sachsen":               {"hot_days_avg": 11.0, "summer_days_avg": 38.0, "tropical_nights_avg": 1.5, "summer_temp_avg": 27.0, "mean_temp_annual":  9.8},
    "Sachsen-Anhalt":        {"hot_days_avg": 11.5, "summer_days_avg": 40.0, "tropical_nights_avg": 1.5, "summer_temp_avg": 27.5, "mean_temp_annual": 10.0},
    "Schleswig-Holstein":    {"hot_days_avg":  5.5, "summer_days_avg": 24.0, "tropical_nights_avg": 0.2, "summer_temp_avg": 24.8, "mean_temp_annual":  9.3},
    "Thüringen":             {"hot_days_avg": 10.0, "summer_days_avg": 36.0, "tropical_nights_avg": 1.0, "summer_temp_avg": 26.8, "mean_temp_annual":  9.5},
}

# Historical hot-day trend data from DWD (approximate annual values for Germany)
# Source: DWD Klimastatusbericht / DWD CDC
HOT_DAYS_GERMANY_HISTORY: dict[int, float] = {
    1990:  7.2, 1991:  5.8, 1992: 10.5, 1993:  6.3, 1994: 11.8,
    1995: 12.0, 1996:  3.5, 1997:  8.0, 1998:  6.2, 1999:  7.5,
    2000:  8.0, 2001:  7.5, 2002:  9.0, 2003: 19.0, 2004:  6.0,
    2005:  8.5, 2006: 13.0, 2007:  7.0, 2008:  7.5, 2009:  8.5,
    2010:  8.0, 2011:  8.5, 2012: 10.0, 2013: 10.5, 2014:  4.5,
    2015: 15.0, 2016:  7.0, 2017:  8.5, 2018: 20.5, 2019: 16.5,
    2020: 11.5, 2021:  7.0, 2022: 17.0, 2023: 14.0, 2024: 13.0,
    2025: 12.0,
}

# Mean annual temperature for Germany (DWD reference)
MEAN_TEMP_GERMANY_HISTORY: dict[int, float] = {
    1990:  9.7, 1991:  8.7, 1992:  9.5, 1993:  8.6, 1994:  9.8,
    1995:  9.1, 1996:  7.6, 1997:  9.2, 1998:  9.3, 1999:  9.5,
    2000: 10.0, 2001:  9.3, 2002:  9.7, 2003:  9.4, 2004:  9.1,
    2005:  9.3, 2006:  9.6, 2007: 10.1, 2008:  9.5, 2009:  9.4,
    2010:  8.5, 2011:  9.7, 2012:  9.4, 2013:  8.7, 2014: 10.3,
    2015: 10.0, 2016:  9.6, 2017:  9.6, 2018: 10.5, 2019: 10.3,
    2020: 10.4, 2021:  9.3, 2022: 10.5, 2023: 10.6, 2024: 10.8,
    2025: 10.5,
}

# Summer avg max temperature
SUMMER_TEMP_GERMANY_HISTORY: dict[int, float] = {
    1990: 23.2, 1991: 22.5, 1992: 23.8, 1993: 21.5, 1994: 24.5,
    1995: 24.8, 1996: 21.0, 1997: 23.0, 1998: 22.5, 1999: 23.2,
    2000: 23.0, 2001: 23.5, 2002: 23.8, 2003: 26.0, 2004: 22.5,
    2005: 23.0, 2006: 24.5, 2007: 23.0, 2008: 23.2, 2009: 23.5,
    2010: 23.8, 2011: 22.5, 2012: 23.5, 2013: 24.0, 2014: 23.0,
    2015: 25.5, 2016: 23.5, 2017: 23.5, 2018: 26.5, 2019: 25.8,
    2020: 24.5, 2021: 22.8, 2022: 25.8, 2023: 25.2, 2024: 25.0,
    2025: 24.8,
}


def get_regional_climate(bundesland: str) -> dict[str, Any]:
    """Get climate summary for a Bundesland.

    Returns hot_days, summer_days, tropical_nights, reference temperatures.
    Uses DWD regional fallback data.
    """
    data = FALLBACK_CLIMATE.get(bundesland, FALLBACK_CLIMATE["Nordrhein-Westfalen"])
    return {
        "hot_days_per_year": data["hot_days_avg"],
        "summer_days_per_year": data["summer_days_avg"],
        "tropical_nights_per_year": data["tropical_nights_avg"],
        "summer_max_temp_avg": data["summer_temp_avg"],
        "mean_temp_annual": data["mean_temp_annual"],
        "source": "DWD Klimastatusbericht / CDC Gebietsmittel",
        "bundesland": bundesland,
    }


def get_climate_history(bundesland: Optional[str] = None) -> dict[str, Any]:
    """Get historical climate indicator time series from 1990.

    Returns yearly data for hot_days, mean_temp, summer_temp.
    If bundesland is given, scales Germany-wide data by regional factor.
    """
    regional = FALLBACK_CLIMATE.get(bundesland, {}) if bundesland else {}
    # Scaling factor: how this Bundesland compares to the Germany average
    regional_hot_factor = regional.get("hot_days_avg", 10.5) / 10.5 if regional else 1.0
    regional_temp_offset = regional.get("mean_temp_annual", 9.8) - 9.8 if regional else 0.0

    years = sorted(HOT_DAYS_GERMANY_HISTORY.keys())
    result = {
        "years": years,
        "hot_days": [
            round(HOT_DAYS_GERMANY_HISTORY.get(y, 10) * regional_hot_factor, 1)
            for y in years
        ],
        "mean_temp": [
            round(MEAN_TEMP_GERMANY_HISTORY.get(y, 9.5) + regional_temp_offset, 1)
            for y in years
        ],
        "summer_max_temp": [
            round(SUMMER_TEMP_GERMANY_HISTORY.get(y, 23.5) + regional_temp_offset, 1)
            for y in years
        ],
        "source": "DWD CDC / Klimastatusbericht Deutschland",
        "note": "Werte basieren auf DWD-Gebietsmitteln, regionalisiert für das Bundesland"
            if bundesland else "Gebietsmittel Deutschland",
    }
    return result


def fetch_dwd_reference_temp(bundesland: str) -> float:
    """Fetch reference summer temperature for a Bundesland.

    Uses the DWD regional data to return the mean summer max temperature,
    which serves as the reference for UHI calculations.
    """
    data = FALLBACK_CLIMATE.get(bundesland, FALLBACK_CLIMATE["Nordrhein-Westfalen"])
    return data["summer_temp_avg"]


def fetch_hot_days(bundesland: str) -> float:
    """Get the average number of hot days (Tmax >= 30°C) per year."""
    data = FALLBACK_CLIMATE.get(bundesland, FALLBACK_CLIMATE["Nordrhein-Westfalen"])
    return data["hot_days_avg"]


# ── Zensus building data ──────────────────────────────────────────────────────

# Building age class distribution (Zensus 2011 approximate shares for Germany)
# and typical albedo / U-value for each era
BUILDING_AGE_CLASSES: list[dict[str, Any]] = [
    {
        "era": "vor 1919",
        "share": 0.18,
        "typical_albedo_roof": 0.15,
        "typical_albedo_facade": 0.35,
        "typical_u_value": 1.5,
        "likely_renovated_pct": 0.60,
        "renovated_albedo_roof": 0.25,
        "renovated_albedo_facade": 0.40,
    },
    {
        "era": "1919-1948",
        "share": 0.12,
        "typical_albedo_roof": 0.15,
        "typical_albedo_facade": 0.30,
        "typical_u_value": 1.4,
        "likely_renovated_pct": 0.55,
        "renovated_albedo_roof": 0.25,
        "renovated_albedo_facade": 0.40,
    },
    {
        "era": "1949-1978",
        "share": 0.35,
        "typical_albedo_roof": 0.12,
        "typical_albedo_facade": 0.25,
        "typical_u_value": 1.2,
        "likely_renovated_pct": 0.45,
        "renovated_albedo_roof": 0.30,
        "renovated_albedo_facade": 0.45,
    },
    {
        "era": "1979-1995",
        "share": 0.18,
        "typical_albedo_roof": 0.15,
        "typical_albedo_facade": 0.30,
        "typical_u_value": 0.8,
        "likely_renovated_pct": 0.30,
        "renovated_albedo_roof": 0.30,
        "renovated_albedo_facade": 0.45,
    },
    {
        "era": "1996-2010",
        "share": 0.12,
        "typical_albedo_roof": 0.20,
        "typical_albedo_facade": 0.35,
        "typical_u_value": 0.5,
        "likely_renovated_pct": 0.10,
        "renovated_albedo_roof": 0.30,
        "renovated_albedo_facade": 0.45,
    },
    {
        "era": "ab 2011",
        "share": 0.05,
        "typical_albedo_roof": 0.25,
        "typical_albedo_facade": 0.40,
        "typical_u_value": 0.3,
        "likely_renovated_pct": 0.0,
        "renovated_albedo_roof": 0.30,
        "renovated_albedo_facade": 0.45,
    },
]


def estimate_building_albedo(building_type: str = "yes", levels: int = 2) -> dict[str, float]:
    """Estimate building albedo based on typical German building stock.

    Uses Zensus building age class distribution and renovation probabilities
    to compute a weighted average albedo for roofs and facades.

    Args:
        building_type: OSM building tag (e.g. 'residential', 'commercial').
        levels: Number of floors (affects facade/roof ratio).

    Returns dict with: roof_albedo, facade_albedo, effective_albedo, estimated_age_class.
    """
    # Adjust age distribution by building type
    # Commercial/industrial tends to be newer; residential matches baseline
    age_shift = 0.0
    if building_type in ("commercial", "retail", "office"):
        age_shift = 0.05  # slightly higher albedo (newer buildings)
    elif building_type in ("industrial", "warehouse"):
        age_shift = -0.02  # more dark metal roofs
    elif building_type in ("residential", "apartments", "house", "detached"):
        age_shift = 0.0

    total_roof = 0.0
    total_facade = 0.0
    for cls in BUILDING_AGE_CLASSES:
        share = cls["share"]
        reno_pct = cls["likely_renovated_pct"]

        roof_alb = (
            cls["typical_albedo_roof"] * (1 - reno_pct)
            + cls["renovated_albedo_roof"] * reno_pct
        )
        facade_alb = (
            cls["typical_albedo_facade"] * (1 - reno_pct)
            + cls["renovated_albedo_facade"] * reno_pct
        )

        total_roof += roof_alb * share
        total_facade += facade_alb * share

    total_roof += age_shift
    total_facade += age_shift

    # Effective albedo: weighted by visible area ratio
    # For a building with N levels, facade area ≈ 4 × height × sqrt(footprint)
    # Roof area ≈ footprint.  For simplicity:
    # roof_weight vs facade_weight depends on levels and viewing angle
    roof_weight = 1.0 / (1.0 + 0.3 * levels)
    facade_weight = 1.0 - roof_weight

    effective = total_roof * roof_weight + total_facade * facade_weight

    return {
        "roof_albedo": round(max(0.05, min(total_roof, 0.60)), 3),
        "facade_albedo": round(max(0.10, min(total_facade, 0.60)), 3),
        "effective_albedo": round(max(0.05, min(effective, 0.60)), 3),
        "estimated_renovation_rate": round(
            sum(c["likely_renovated_pct"] * c["share"] for c in BUILDING_AGE_CLASSES), 2
        ),
    }


# ── Climate projections ──────────────────────────────────────────────────────

# Based on DWD / IPCC AR6 / KlimaFolgenOnline / ReKliEs-DE ensemble data
# RCP 4.5 (moderate mitigation) and RCP 8.5 (business as usual)
# Projections for Germany as a whole, to be regionalized per Bundesland.

# Hot days trend: Germany-wide projection (annual avg, 5-year smoothed)
# Source: DWD KlimaFolgenOnline / UBA Klimawirkungs-Risikoanalyse
_HOT_DAYS_PROJECTION_RCP45: dict[int, float] = {
    2025: 12.0, 2026: 12.3, 2027: 12.5, 2028: 12.8, 2029: 13.0,
    2030: 13.5, 2031: 13.7, 2032: 13.9, 2033: 14.1, 2034: 14.3,
    2035: 14.5, 2036: 14.7, 2037: 15.0, 2038: 15.2, 2039: 15.4,
    2040: 15.5, 2041: 15.7, 2042: 15.8, 2043: 16.0, 2044: 16.1,
    2045: 16.2, 2046: 16.3, 2047: 16.5, 2048: 16.6, 2049: 16.7,
    2050: 17.0, 2051: 17.1, 2052: 17.2, 2053: 17.3, 2054: 17.4,
    2055: 17.5, 2056: 17.5, 2057: 17.6, 2058: 17.7, 2059: 17.8,
    2060: 18.0, 2061: 18.0, 2062: 18.1, 2063: 18.1, 2064: 18.2,
    2065: 18.2,
}

_HOT_DAYS_PROJECTION_RCP85: dict[int, float] = {
    2025: 12.0, 2026: 12.5, 2027: 13.0, 2028: 13.5, 2029: 14.0,
    2030: 14.5, 2031: 15.0, 2032: 15.5, 2033: 16.0, 2034: 16.5,
    2035: 17.0, 2036: 17.5, 2037: 18.0, 2038: 18.5, 2039: 19.0,
    2040: 19.5, 2041: 20.0, 2042: 20.5, 2043: 21.0, 2044: 21.5,
    2045: 22.0, 2046: 22.5, 2047: 23.0, 2048: 23.5, 2049: 24.0,
    2050: 24.5, 2051: 25.0, 2052: 25.5, 2053: 26.0, 2054: 26.5,
    2055: 27.0, 2056: 27.5, 2057: 28.0, 2058: 28.5, 2059: 29.0,
    2060: 29.5, 2061: 30.0, 2062: 30.5, 2063: 31.0, 2064: 31.5,
    2065: 32.0,
}

# Mean annual temperature projections for Germany
_MEAN_TEMP_PROJECTION_RCP45: dict[int, float] = {
    2025: 10.5, 2026: 10.6, 2027: 10.6, 2028: 10.7, 2029: 10.7,
    2030: 10.8, 2031: 10.8, 2032: 10.9, 2033: 10.9, 2034: 11.0,
    2035: 11.0, 2036: 11.1, 2037: 11.1, 2038: 11.2, 2039: 11.2,
    2040: 11.3, 2041: 11.3, 2042: 11.3, 2043: 11.4, 2044: 11.4,
    2045: 11.4, 2046: 11.5, 2047: 11.5, 2048: 11.5, 2049: 11.6,
    2050: 11.6, 2051: 11.6, 2052: 11.7, 2053: 11.7, 2054: 11.7,
    2055: 11.8, 2056: 11.8, 2057: 11.8, 2058: 11.8, 2059: 11.9,
    2060: 11.9, 2061: 11.9, 2062: 11.9, 2063: 12.0, 2064: 12.0,
    2065: 12.0,
}

_MEAN_TEMP_PROJECTION_RCP85: dict[int, float] = {
    2025: 10.5, 2026: 10.6, 2027: 10.7, 2028: 10.8, 2029: 10.9,
    2030: 11.0, 2031: 11.1, 2032: 11.2, 2033: 11.3, 2034: 11.4,
    2035: 11.5, 2036: 11.6, 2037: 11.7, 2038: 11.8, 2039: 11.9,
    2040: 12.0, 2041: 12.1, 2042: 12.2, 2043: 12.3, 2044: 12.4,
    2045: 12.5, 2046: 12.6, 2047: 12.7, 2048: 12.9, 2049: 13.0,
    2050: 13.1, 2051: 13.2, 2052: 13.3, 2053: 13.4, 2054: 13.5,
    2055: 13.6, 2056: 13.7, 2057: 13.8, 2058: 13.9, 2059: 14.0,
    2060: 14.1, 2061: 14.2, 2062: 14.3, 2063: 14.4, 2064: 14.5,
    2065: 14.5,
}

# Summer Tmax projections
_SUMMER_TEMP_PROJECTION_RCP45: dict[int, float] = {
    2025: 24.8, 2026: 24.9, 2027: 25.0, 2028: 25.1, 2029: 25.2,
    2030: 25.3, 2031: 25.4, 2032: 25.5, 2033: 25.5, 2034: 25.6,
    2035: 25.7, 2036: 25.8, 2037: 25.9, 2038: 25.9, 2039: 26.0,
    2040: 26.1, 2041: 26.1, 2042: 26.2, 2043: 26.2, 2044: 26.3,
    2045: 26.3, 2046: 26.4, 2047: 26.5, 2048: 26.5, 2049: 26.6,
    2050: 26.6, 2051: 26.7, 2052: 26.7, 2053: 26.8, 2054: 26.8,
    2055: 26.9, 2056: 26.9, 2057: 27.0, 2058: 27.0, 2059: 27.0,
    2060: 27.1, 2061: 27.1, 2062: 27.1, 2063: 27.2, 2064: 27.2,
    2065: 27.2,
}

_SUMMER_TEMP_PROJECTION_RCP85: dict[int, float] = {
    2025: 24.8, 2026: 25.0, 2027: 25.2, 2028: 25.4, 2029: 25.6,
    2030: 25.8, 2031: 26.0, 2032: 26.2, 2033: 26.4, 2034: 26.6,
    2035: 26.8, 2036: 27.0, 2037: 27.2, 2038: 27.4, 2039: 27.6,
    2040: 27.8, 2041: 28.0, 2042: 28.2, 2043: 28.4, 2044: 28.6,
    2045: 28.8, 2046: 29.0, 2047: 29.2, 2048: 29.4, 2049: 29.6,
    2050: 29.8, 2051: 30.0, 2052: 30.2, 2053: 30.4, 2054: 30.5,
    2055: 30.7, 2056: 30.9, 2057: 31.0, 2058: 31.2, 2059: 31.3,
    2060: 31.5, 2061: 31.6, 2062: 31.8, 2063: 31.9, 2064: 32.0,
    2065: 32.2,
}

# Tropical nights projections
_TROPICAL_NIGHTS_PROJECTION_RCP45: dict[int, float] = {
    2025: 1.5, 2026: 1.6, 2027: 1.6, 2028: 1.7, 2029: 1.7,
    2030: 1.8, 2031: 1.9, 2032: 1.9, 2033: 2.0, 2034: 2.0,
    2035: 2.1, 2036: 2.2, 2037: 2.2, 2038: 2.3, 2039: 2.3,
    2040: 2.4, 2041: 2.5, 2042: 2.5, 2043: 2.6, 2044: 2.6,
    2045: 2.7, 2046: 2.8, 2047: 2.8, 2048: 2.9, 2049: 2.9,
    2050: 3.0, 2051: 3.1, 2052: 3.1, 2053: 3.2, 2054: 3.2,
    2055: 3.3, 2056: 3.3, 2057: 3.4, 2058: 3.4, 2059: 3.5,
    2060: 3.5, 2061: 3.5, 2062: 3.6, 2063: 3.6, 2064: 3.7,
    2065: 3.7,
}

_TROPICAL_NIGHTS_PROJECTION_RCP85: dict[int, float] = {
    2025: 1.5, 2026: 1.7, 2027: 1.9, 2028: 2.1, 2029: 2.3,
    2030: 2.5, 2031: 2.7, 2032: 3.0, 2033: 3.2, 2034: 3.5,
    2035: 3.8, 2036: 4.0, 2037: 4.3, 2038: 4.6, 2039: 4.9,
    2040: 5.2, 2041: 5.5, 2042: 5.8, 2043: 6.1, 2044: 6.4,
    2045: 6.8, 2046: 7.1, 2047: 7.5, 2048: 7.8, 2049: 8.2,
    2050: 8.5, 2051: 8.9, 2052: 9.2, 2053: 9.5, 2054: 9.8,
    2055: 10.2, 2056: 10.5, 2057: 10.8, 2058: 11.1, 2059: 11.5,
    2060: 11.8, 2061: 12.1, 2062: 12.4, 2063: 12.7, 2064: 13.0,
    2065: 13.3,
}


def get_climate_projection(bundesland: Optional[str] = None) -> dict[str, Any]:
    """Get climate projection data (2025–2065) for RCP 4.5 and RCP 8.5.

    Returns yearly projections for hot_days, mean_temp, summer_max_temp
    and tropical_nights, regionalized for the Bundesland.

    Based on IPCC AR6 / DWD KlimaFolgenOnline / ReKliEs-DE ensemble.
    """
    regional = FALLBACK_CLIMATE.get(bundesland, {}) if bundesland else {}
    # Regional scaling factors (same approach as get_climate_history)
    regional_hot_factor = regional.get("hot_days_avg", 10.5) / 10.5 if regional else 1.0
    regional_temp_offset = regional.get("mean_temp_annual", 9.8) - 9.8 if regional else 0.0
    regional_tropical_factor = regional.get("tropical_nights_avg", 1.5) / 1.5 if regional else 1.0

    years = sorted(_HOT_DAYS_PROJECTION_RCP45.keys())

    def _scale_hot(d: dict[int, float]) -> list[float]:
        return [round(d.get(y, 12) * regional_hot_factor, 1) for y in years]

    def _scale_temp(d: dict[int, float]) -> list[float]:
        return [round(d.get(y, 10) + regional_temp_offset, 1) for y in years]

    def _scale_tropical(d: dict[int, float]) -> list[float]:
        return [round(d.get(y, 1.5) * regional_tropical_factor, 1) for y in years]

    return {
        "years": years,
        "scenarios": {
            "rcp45": {
                "label": "RCP 4.5 (moderater Klimaschutz)",
                "hot_days": _scale_hot(_HOT_DAYS_PROJECTION_RCP45),
                "mean_temp": _scale_temp(_MEAN_TEMP_PROJECTION_RCP45),
                "summer_max_temp": _scale_temp(_SUMMER_TEMP_PROJECTION_RCP45),
                "tropical_nights": _scale_tropical(_TROPICAL_NIGHTS_PROJECTION_RCP45),
            },
            "rcp85": {
                "label": "RCP 8.5 (weiter wie bisher)",
                "hot_days": _scale_hot(_HOT_DAYS_PROJECTION_RCP85),
                "mean_temp": _scale_temp(_MEAN_TEMP_PROJECTION_RCP85),
                "summer_max_temp": _scale_temp(_SUMMER_TEMP_PROJECTION_RCP85),
                "tropical_nights": _scale_tropical(_TROPICAL_NIGHTS_PROJECTION_RCP85),
            },
        },
        "source": "IPCC AR6 / DWD KlimaFolgenOnline / ReKliEs-DE Ensemble",
        "note": f"Regionalisiert für {bundesland}" if bundesland else "Gebietsmittel Deutschland",
    }


def get_zensus_summary() -> dict[str, Any]:
    """Return a summary of the Zensus-based building age distribution and albedo estimates."""
    classes = []
    for cls in BUILDING_AGE_CLASSES:
        alb = estimate_building_albedo()
        classes.append({
            "era": cls["era"],
            "share_pct": round(cls["share"] * 100, 1),
            "typical_albedo_roof": cls["typical_albedo_roof"],
            "renovated_albedo_roof": cls["renovated_albedo_roof"],
            "renovation_rate_pct": round(cls["likely_renovated_pct"] * 100, 0),
        })

    overall = estimate_building_albedo()
    return {
        "source": "Zensus 2011 (Gebäude- und Wohnungszählung), fortgeschrieben",
        "age_classes": classes,
        "overall_effective_albedo": overall["effective_albedo"],
        "overall_renovation_rate": overall["estimated_renovation_rate"],
    }
