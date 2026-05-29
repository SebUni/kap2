"""Orchestrates measure impact calculation across climate assessors."""

import logging

from geoalchemy2 import functions as func
from geoalchemy2.shape import to_shape
from sqlalchemy import case, literal
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.models import (
    AdaptationMeasure, ClimateAssessment, GridCell, MeasureImpact, ClimateType,
)
from app.services.climate.heat.measures import calculate_measure_impact, get_measure_catalog

log = logging.getLogger(__name__)


def compute_impact(db: Session, measure_id: int) -> dict:
    """Compute impact of a measure on all overlapping grid cells.

    Returns summary of total deltas, costs, and savings.
    Uses area-proportional intersection fraction and best available IST data.
    """
    measure = db.query(AdaptationMeasure).filter(AdaptationMeasure.id == measure_id).first()
    if not measure:
        raise ValueError(f"Measure {measure_id} not found")

    # Find grid cells that intersect the measure geometry and compute
    # the coverage fraction (how much of each cell is covered by the measure polygon).
    # ST_Area operates on geography for accurate m² results.
    cell_area_expr = func.ST_Area(func.ST_Transform(GridCell.geometry, 3857))
    intersection_area_expr = func.ST_Area(
        func.ST_Transform(
            func.ST_Intersection(GridCell.geometry, measure.geometry),
            3857,
        )
    )
    # Avoid division by zero
    coverage_fraction_expr = case(
        (cell_area_expr > 0, intersection_area_expr / cell_area_expr),
        else_=literal(0.0),
    )

    overlapping = (
        db.query(GridCell, coverage_fraction_expr.label("coverage_fraction"))
        .filter(
            GridCell.kommune_id == measure.kommune_id,
            func.ST_Intersects(GridCell.geometry, measure.geometry),
        )
        .all()
    )

    if not overlapping:
        return {"message": "No grid cells overlap with this measure", "impacts": []}

    cell_ids = [row.GridCell.id for row in overlapping]
    coverage_map = {row.GridCell.id: float(row.coverage_fraction) for row in overlapping}
    cells_list = [row.GridCell for row in overlapping]

    # Get the BEST (highest-level) assessment data for each cell
    # so the IST situation is as detailed as possible.
    assessments = (
        db.query(ClimateAssessment)
        .filter(
            ClimateAssessment.grid_cell_id.in_(cell_ids),
            ClimateAssessment.climate_type == ClimateType.HEAT,
        )
        .order_by(ClimateAssessment.level.desc())
        .all()
    )
    # Keep only the highest-level assessment per cell
    assessment_map: dict[int, ClimateAssessment] = {}
    for a in assessments:
        if a.grid_cell_id not in assessment_map:
            assessment_map[a.grid_cell_id] = a

    # Build input for the measure impact calculator
    affected_cells = []
    total_affected_area_m2 = 0.0
    for cell in cells_list:
        a = assessment_map.get(cell.id)
        frac = coverage_map.get(cell.id, 0.0)
        cell_area_m2 = cell.cell_size_m ** 2
        total_affected_area_m2 += cell_area_m2 * frac
        affected_cells.append({
            "grid_cell_id": cell.id,
            "cell_size_m": cell.cell_size_m,
            "coverage_fraction": frac,
            "indicators": a.indicators if a else {},
        })

    # Load global config as flat dict
    from app.models.models import ConfigParameter
    params = db.query(ConfigParameter).filter(ConfigParameter.kommune_id == measure.kommune_id).all()
    gconfig = {f"{p.category}.{p.key}": p.value for p in params}

    # Calculate impact
    impacts = calculate_measure_impact(
        measure_type=measure.measure_type,
        measure_config=measure.config or {},
        affected_cells=affected_cells,
        global_config=gconfig,
    )

    # Filter impacts to only include grid cells that still exist in the DB,
    # protecting against race conditions when the grid is regenerated concurrently.
    valid_cell_ids = set(cell_ids)
    impacts = [imp for imp in impacts if imp["grid_cell_id"] in valid_cell_ids]

    # Delete old impacts for this measure
    db.query(MeasureImpact).filter(MeasureImpact.measure_id == measure_id).delete()

    # Save new impacts
    total_deltas: dict = {}
    total_costs: dict = {}
    total_savings: dict = {}

    for imp in impacts:
        db_impact = MeasureImpact(
            measure_id=measure_id,
            grid_cell_id=imp["grid_cell_id"],
            indicator_deltas=imp.get("indicator_deltas", {}),
            costs=imp.get("costs", {}),
            savings=imp.get("savings", {}),
        )
        db.add(db_impact)

        for k, v in imp.get("indicator_deltas", {}).items():
            total_deltas[k] = total_deltas.get(k, 0) + v
        for k, v in imp.get("costs", {}).items():
            total_costs[k] = total_costs.get(k, 0) + v
        for k, v in imp.get("savings", {}).items():
            total_savings[k] = total_savings.get(k, 0) + v

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        log.warning("Grid cells changed during impact calculation for measure %s – retrying", measure_id)
        # Grid was regenerated mid-flight. Re-query to get fresh cell IDs.
        return compute_impact(db, measure_id)

    return {
        "measure_id": measure_id,
        "affected_cells": len(impacts),
        "affected_area_m2": round(total_affected_area_m2, 1),
        "total_indicator_deltas": {k: round(v, 2) for k, v in total_deltas.items()},
        "total_costs": {k: round(v, 2) for k, v in total_costs.items()},
        "total_savings": {k: round(v, 2) for k, v in total_savings.items()},
    }
