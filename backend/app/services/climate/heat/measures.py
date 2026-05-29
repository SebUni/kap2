"""Impact models for heat-related adaptation measures.

Each measure type has a function that computes:
- indicator_deltas: how indicators change in affected grid cells
- costs: investment and running costs
- savings: estimated savings from reduced heat effects

All handlers use:
- coverage_fraction: geometric intersection area / cell area (0..1)
- IST indicators from the best available assessment level
"""

from typing import Any


# ── Measure type catalog ───────────────────────────────────────────────────────

MEASURE_TYPES = {
    "drinking_fountain": {
        "label": "Trinkbrunnen",
        "params": [
            {"key": "count", "label": "Anzahl Brunnen", "type": "int", "default": 5},
            {"key": "spacing_m", "label": "Abstand (m)", "type": "float", "default": 200},
        ],
    },
    "green_roof": {
        "label": "Dachbegrünung",
        "params": [
            {"key": "coverage_pct", "label": "Begrünter Dachflächenanteil (%)", "type": "float", "default": 60},
        ],
    },
    "facade_greening": {
        "label": "Fassadenbegrünung",
        "params": [
            {"key": "coverage_pct", "label": "Begrünter Fassadenanteil (%)", "type": "float", "default": 30},
        ],
    },
    "tree_planting": {
        "label": "Baumpflanzung",
        "params": [
            {"key": "count", "label": "Anzahl Bäume", "type": "int", "default": 20},
            {"key": "shade_factor", "label": "Schattenfaktor pro Baum", "type": "float", "default": 0.03},
        ],
    },
    "unsealing": {
        "label": "Entsiegelung",
        "params": [
            {"key": "area_pct", "label": "Entsiegelungsanteil (%)", "type": "float", "default": 50},
        ],
    },
    "shade_structure": {
        "label": "Verschattungselemente",
        "params": [
            {"key": "coverage_pct", "label": "Beschatteter Flächenanteil (%)", "type": "float", "default": 30},
        ],
    },
}


def get_measure_catalog() -> dict:
    return MEASURE_TYPES


def calculate_measure_impact(
    measure_type: str,
    measure_config: dict,
    affected_cells: list[dict],
    global_config: dict[str, Any],
) -> list[dict]:
    """Calculate the impact of a measure on affected grid cells.

    Args:
        measure_type: Key from MEASURE_TYPES.
        measure_config: User-specified parameters for this measure instance.
        affected_cells: List of dicts with 'grid_cell_id', 'indicators',
            'cell_size_m', and 'coverage_fraction'.
        global_config: Global config params (category.key -> value).

    Returns:
        List of dicts with grid_cell_id, indicator_deltas, costs, savings.
    """
    handler = _HANDLERS.get(measure_type)
    if not handler:
        raise ValueError(f"Unknown measure type: {measure_type}")

    return handler(measure_config, affected_cells, global_config)


# ── Helpers ────────────────────────────────────────────────────────────────────

def _cell_frac(cell: dict) -> float:
    """Return the coverage fraction for this cell (0..1)."""
    return max(0.0, min(1.0, float(cell.get("coverage_fraction", 1.0))))


def _heat_context(indicators: dict) -> float:
    """Return a multiplier (0.2 .. 2.0) that amplifies effects in hot/urban areas.

    Uses IST indicators: higher UHI, higher impervious fraction, and higher
    heat stress all increase the effectiveness of cooling measures.
    A field (low impervious, low UHI) will see much less benefit than a dense
    inner-city area.
    """
    imp_frac = float(indicators.get("impervious_fraction", 0.3))
    uhi = float(indicators.get("uhi_delta", 0.0))
    stress = float(indicators.get("heat_stress_index", 3.0))

    # Weight: impervious surfaces → more heat to offset
    imp_weight = 0.3 + 1.7 * imp_frac  # 0.3 on field, 2.0 at 100% sealed
    # UHI bonus: stronger UHI → more room for improvement
    uhi_weight = max(0.5, min(1.5, 0.5 + uhi / 4.0))
    # Stress bonus
    stress_weight = max(0.5, min(1.5, stress / 5.0))

    combined = (imp_weight * 0.5 + uhi_weight * 0.25 + stress_weight * 0.25)
    return max(0.2, min(2.0, combined))


# ── Impact handlers ────────────────────────────────────────────────────────────

def _impact_drinking_fountain(config: dict, cells: list[dict], gconfig: dict) -> list[dict]:
    """Drinking fountains: minimal temperature effect, but health benefit.

    Effect scaled by coverage fraction and local heat stress.
    """
    count = int(config.get("count", 5))
    cost_per_unit = float(gconfig.get("costs.drinking_fountain_unit", 8000))
    annual_maintenance = float(gconfig.get("costs.drinking_fountain_annual", 500))

    total_cost = cost_per_unit * count
    total_maintenance = annual_maintenance * count

    # Total coverage weight for distributing costs/effects
    total_weight = sum(_cell_frac(c) for c in cells) or 1.0

    emergency_cost = float(gconfig.get("savings.emergency_call_cost", 500))
    calls_per_1000_pop = float(gconfig.get("savings.emergency_calls_per_1000_hot_day", 2.0))
    hot_days = float(gconfig.get("heat.hot_days_per_year", 20))
    reduction_factor = min(0.15, count * 0.02)

    results = []
    for cell in cells:
        frac = _cell_frac(cell)
        if frac <= 0:
            continue
        indicators = cell.get("indicators", {})
        ctx = _heat_context(indicators)
        w = frac / total_weight

        pop = float(indicators.get("estimated_affected_pop", 0))
        stress = float(indicators.get("heat_stress_index", 3.0))

        # Stress reduction: more fountain benefit in high-stress areas
        delta_stress = -0.2 * (count * w) * ctx * frac

        savings_annual = pop / 1000 * calls_per_1000_pop * hot_days * emergency_cost * reduction_factor * frac

        results.append({
            "grid_cell_id": cell["grid_cell_id"],
            "indicator_deltas": {
                "temperature_estimate": 0.0,
                "uhi_delta": 0.0,
                "heat_stress_index": round(delta_stress, 2),
            },
            "costs": {
                "investment": round(total_cost * w, 2),
                "annual_maintenance": round(total_maintenance * w, 2),
            },
            "savings": {
                "annual_health": round(savings_annual, 2),
            },
        })

    return results


def _impact_green_roof(config: dict, cells: list[dict], gconfig: dict) -> list[dict]:
    """Green roofs: increase albedo, reduce temperature.

    Effect depends on existing building/impervious fraction and coverage.
    """
    coverage = float(config.get("coverage_pct", 60)) / 100.0
    cost_per_m2 = float(gconfig.get("costs.green_roof_per_m2", 45))
    albedo_increase = 0.15 * coverage
    alpha = float(gconfig.get("heat.uhi_alpha", 6.0))

    results = []
    for cell in cells:
        frac = _cell_frac(cell)
        if frac <= 0:
            continue
        indicators = cell.get("indicators", {})
        imp_frac = float(indicators.get("impervious_fraction", 0.45))
        building_cov = float(indicators.get("building_coverage", imp_frac * 0.3))

        # Only rooftop surfaces get green roofs
        roof_fraction = building_cov
        # Temperature reduction from albedo change, scaled by coverage fraction
        delta_t = -alpha * albedo_increase * roof_fraction * frac
        delta_stress = delta_t * 1.5

        cell_area_m2 = cell.get("cell_size_m", 100) ** 2
        roof_area = cell_area_m2 * roof_fraction * coverage * frac
        investment = roof_area * cost_per_m2

        results.append({
            "grid_cell_id": cell["grid_cell_id"],
            "indicator_deltas": {
                "temperature_estimate": round(delta_t, 2),
                "uhi_delta": round(delta_t, 2),
                "heat_stress_index": round(delta_stress, 2),
            },
            "costs": {
                "investment": round(investment, 2),
                "annual_maintenance": round(investment * 0.02, 2),
            },
            "savings": {
                "annual_cooling": round(abs(delta_t) * cell_area_m2 * frac * 0.1, 2),
            },
        })

    return results


def _impact_tree_planting(config: dict, cells: list[dict], gconfig: dict) -> list[dict]:
    """Tree planting: shade and evapotranspiration reduce temperature.

    Effect depends on local heat context: trees in a hot urban area produce
    a much larger temperature reduction than on a field.
    """
    count = int(config.get("count", 20))
    shade_factor = float(config.get("shade_factor", 0.03))
    cost_per_tree = float(gconfig.get("costs.tree_planting_unit", 1200))
    annual_maintenance = float(gconfig.get("costs.tree_annual_maintenance", 80))

    total_shade = min(count * shade_factor, 0.6)

    # Distribute trees proportionally by coverage fraction
    total_weight = sum(_cell_frac(c) for c in cells) or 1.0

    results = []
    for cell in cells:
        frac = _cell_frac(cell)
        if frac <= 0:
            continue
        indicators = cell.get("indicators", {})
        ctx = _heat_context(indicators)
        w = frac / total_weight

        # Trees in urban area (high ctx) → up to ~3°C per cell fraction
        # Trees on a field (low ctx) → ~0.6°C
        delta_t = -total_shade * 3.0 * w * ctx
        delta_stress = delta_t * 1.5

        trees_in_cell = count * w
        delta_imp = -0.005 * trees_in_cell

        cell_area_m2 = cell.get("cell_size_m", 100) ** 2
        effective_area = cell_area_m2 * frac

        results.append({
            "grid_cell_id": cell["grid_cell_id"],
            "indicator_deltas": {
                "temperature_estimate": round(delta_t, 2),
                "uhi_delta": round(delta_t, 2),
                "heat_stress_index": round(delta_stress, 2),
                "impervious_fraction": round(delta_imp, 4),
            },
            "costs": {
                "investment": round(cost_per_tree * trees_in_cell, 2),
                "annual_maintenance": round(annual_maintenance * trees_in_cell, 2),
            },
            "savings": {
                "annual_cooling": round(abs(delta_t) * effective_area * 0.05, 2),
                "annual_health": round(abs(delta_t) * effective_area * 0.02, 2),
            },
        })

    return results


def _impact_unsealing(config: dict, cells: list[dict], gconfig: dict) -> list[dict]:
    """Unsealing: reduce impervious fraction, increase albedo effective.

    Can only unseal what is actually sealed — uses IST impervious_fraction.
    """
    area_pct = float(config.get("area_pct", 50)) / 100.0
    cost_per_m2 = float(gconfig.get("costs.unsealing_per_m2", 35))
    alpha = float(gconfig.get("heat.uhi_alpha", 6.0))

    results = []
    for cell in cells:
        frac = _cell_frac(cell)
        if frac <= 0:
            continue
        indicators = cell.get("indicators", {})
        imp_frac = float(indicators.get("impervious_fraction", 0.45))

        # Only the covered portion of the cell is affected
        reduction = imp_frac * area_pct * frac

        delta_t = -alpha * 0.2 * reduction
        delta_stress = delta_t * 1.5

        cell_area_m2 = cell.get("cell_size_m", 100) ** 2
        unseal_area = cell_area_m2 * imp_frac * area_pct * frac
        investment = unseal_area * cost_per_m2

        results.append({
            "grid_cell_id": cell["grid_cell_id"],
            "indicator_deltas": {
                "temperature_estimate": round(delta_t, 2),
                "uhi_delta": round(delta_t, 2),
                "heat_stress_index": round(delta_stress, 2),
                "impervious_fraction": round(-reduction, 4),
            },
            "costs": {
                "investment": round(investment, 2),
                "annual_maintenance": round(investment * 0.01, 2),
            },
            "savings": {
                "annual_cooling": round(abs(delta_t) * cell_area_m2 * frac * 0.05, 2),
            },
        })

    return results


def _impact_facade_greening(config: dict, cells: list[dict], gconfig: dict) -> list[dict]:
    """Facade greening: reduce building surface temperature.

    Effect depends on impervious/building fraction — no buildings → no facades.
    """
    coverage = float(config.get("coverage_pct", 30)) / 100.0
    cost_per_m2 = float(gconfig.get("costs.facade_greening_per_m2", 60))
    alpha = float(gconfig.get("heat.uhi_alpha", 6.0))

    results = []
    for cell in cells:
        frac = _cell_frac(cell)
        if frac <= 0:
            continue
        indicators = cell.get("indicators", {})
        imp_frac = float(indicators.get("impervious_fraction", 0.45))
        building_cov = float(indicators.get("building_coverage", imp_frac * 0.15))

        facade_fraction = building_cov
        delta_t = -alpha * 0.10 * facade_fraction * coverage * frac
        delta_stress = delta_t * 1.5

        cell_area_m2 = cell.get("cell_size_m", 100) ** 2
        facade_area = cell_area_m2 * facade_fraction * coverage * frac
        investment = facade_area * cost_per_m2

        results.append({
            "grid_cell_id": cell["grid_cell_id"],
            "indicator_deltas": {
                "temperature_estimate": round(delta_t, 2),
                "uhi_delta": round(delta_t, 2),
                "heat_stress_index": round(delta_stress, 2),
            },
            "costs": {
                "investment": round(investment, 2),
                "annual_maintenance": round(investment * 0.03, 2),
            },
            "savings": {
                "annual_cooling": round(abs(delta_t) * cell_area_m2 * frac * 0.08, 2),
            },
        })

    return results


def _impact_shade_structure(config: dict, cells: list[dict], gconfig: dict) -> list[dict]:
    """Shade structures: reduce direct heat exposure.

    Effect depends on local heat context — shading a cool park has little
    effect vs. shading a hot plaza.
    """
    coverage = float(config.get("coverage_pct", 30)) / 100.0
    cost_per_m2 = float(gconfig.get("costs.shade_structure_per_m2", 120))

    total_weight = sum(_cell_frac(c) for c in cells) or 1.0

    results = []
    for cell in cells:
        frac = _cell_frac(cell)
        if frac <= 0:
            continue
        indicators = cell.get("indicators", {})
        ctx = _heat_context(indicators)
        w = frac / total_weight

        delta_t = -2.5 * coverage * w * ctx
        delta_stress = delta_t * 1.5

        cell_area_m2 = cell.get("cell_size_m", 100) ** 2
        shade_area = cell_area_m2 * coverage * frac
        investment = shade_area * cost_per_m2

        results.append({
            "grid_cell_id": cell["grid_cell_id"],
            "indicator_deltas": {
                "temperature_estimate": round(delta_t, 2),
                "uhi_delta": round(delta_t, 2),
                "heat_stress_index": round(delta_stress, 2),
            },
            "costs": {
                "investment": round(investment, 2),
                "annual_maintenance": round(investment * 0.02, 2),
            },
            "savings": {
                "annual_health": round(abs(delta_t) * cell_area_m2 * frac * 0.03, 2),
            },
        })

    return results


_HANDLERS = {
    "drinking_fountain": _impact_drinking_fountain,
    "green_roof": _impact_green_roof,
    "facade_greening": _impact_facade_greening,
    "tree_planting": _impact_tree_planting,
    "unsealing": _impact_unsealing,
    "shade_structure": _impact_shade_structure,
}
