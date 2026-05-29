"""Risk zone projection service (2025–2065).

Scales current risk_scores by assessor-specific climate factors
and recomputes connected components for each projected year.
"""

import logging
from collections import deque

from sqlalchemy.orm import Session

from app.models.models import ClimateAssessment, GridCell, ClimateType
from app.services.climate.registry import get_assessor

log = logging.getLogger(__name__)

RISK_THRESHOLD = 4.0


def project_risk_zones(
    db: Session,
    kommune_id: int,
    climate_type: str,
    level: int,
    bundesland: str,
    years: range | None = None,
) -> list[dict]:
    """Project risk zones into the future by scaling current scores.

    Returns list of {year, rcp45: {...}, rcp85: {...}} dicts.
    """
    if years is None:
        years = range(2025, 2066)

    ct = ClimateType(climate_type)
    assessor = get_assessor(climate_type)
    if not assessor:
        return []

    factors = assessor.get_projection_factors(bundesland)

    # Load current assessments
    rows = (
        db.query(ClimateAssessment, GridCell.row_idx, GridCell.col_idx)
        .join(GridCell, GridCell.id == ClimateAssessment.grid_cell_id)
        .filter(
            ClimateAssessment.kommune_id == kommune_id,
            ClimateAssessment.climate_type == ct,
            ClimateAssessment.level == level,
        )
        .all()
    )

    if not rows:
        return []

    # Build base data
    cells: list[dict] = []
    grid_idx: dict[tuple[int, int], int] = {}
    for i, (assessment, row_idx, col_idx) in enumerate(rows):
        risk = float((assessment.indicators or {}).get("risk_score", 0.0))
        cells.append({"row": row_idx, "col": col_idx, "base_risk": risk})
        grid_idx[(row_idx, col_idx)] = i

    result = []
    for year in years:
        entry = {"year": year}
        for scenario in ("rcp45", "rcp85"):
            factor = factors.get(scenario, {}).get(year, 1.0)
            # Scale risk scores
            scaled = [min(10.0, c["base_risk"] * factor) for c in cells]

            # Quick connected-component count
            at_risk = {i for i, s in enumerate(scaled) if s >= RISK_THRESHOLD}
            visited: set[int] = set()
            zone_count = 0
            risks_in_zones: list[float] = []
            zone_sizes: list[int] = []

            for seed in at_risk:
                if seed in visited:
                    continue
                zone_count += 1
                queue: deque[int] = deque([seed])
                visited.add(seed)
                comp_risks: list[float] = []
                while queue:
                    ci = queue.popleft()
                    comp_risks.append(scaled[ci])
                    r, c = cells[ci]["row"], cells[ci]["col"]
                    for dr in (-1, 0, 1):
                        for dc in (-1, 0, 1):
                            if dr == 0 and dc == 0:
                                continue
                            ni = grid_idx.get((r + dr, c + dc))
                            if ni is not None and ni in at_risk and ni not in visited:
                                visited.add(ni)
                                queue.append(ni)
                risks_in_zones.extend(comp_risks)
                zone_sizes.append(len(comp_risks))

            mean_sev = sum(risks_in_zones) / len(risks_in_zones) if risks_in_zones else 0.0
            max_sev = max(risks_in_zones) if risks_in_zones else 0.0
            total_cells = sum(zone_sizes)

            entry[scenario] = {
                "zone_count": zone_count,
                "mean_severity": round(mean_sev, 2),
                "max_severity": round(max_sev, 2),
                "total_cells_at_risk": total_cells,
            }
        result.append(entry)

    return result
