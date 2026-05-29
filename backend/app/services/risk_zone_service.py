"""Risk-zone computation using connected-component analysis.

Identifies contiguous grid-cell clusters where risk_score ≥ threshold,
stores them as RiskZone rows, and provides aggregation / GeoJSON helpers.
"""

import logging
from collections import deque
from datetime import datetime

from geoalchemy2 import functions as func
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping
from sqlalchemy.orm import Session

from app.models.models import (
    ClimateAssessment, GridCell, RiskZone, RiskZoneCell, ClimateType,
)

log = logging.getLogger(__name__)

RISK_THRESHOLD = 4.0  # score ≥ this → "at risk"


# ── Public API ─────────────────────────────────────────────────────────────────

def compute_risk_zones(
    db: Session,
    kommune_id: int,
    climate_type: str,
    level: int,
    threshold: float = RISK_THRESHOLD,
) -> list[dict]:
    """Run connected-component analysis and persist RiskZone rows.

    Returns list of zone summary dicts.
    """
    ct = ClimateType(climate_type)

    # 1. Load assessments + grid cell positions
    rows = (
        db.query(ClimateAssessment, GridCell.row_idx, GridCell.col_idx, GridCell.cell_size_m)
        .join(GridCell, GridCell.id == ClimateAssessment.grid_cell_id)
        .filter(
            ClimateAssessment.kommune_id == kommune_id,
            ClimateAssessment.climate_type == ct,
            ClimateAssessment.level == level,
        )
        .all()
    )

    if not rows:
        log.info("No assessment data for risk zones (kommune=%s type=%s level=%s)",
                 kommune_id, climate_type, level)
        return []

    # 2. Extract risk_score per cell  (indicators dict must contain 'risk_score')
    cell_map: dict[int, dict] = {}   # cell_id -> {row, col, risk, cell_size_m}
    grid_idx: dict[tuple[int, int], int] = {}  # (row, col) -> cell_id

    for assessment, row_idx, col_idx, cell_size_m in rows:
        risk = float((assessment.indicators or {}).get("risk_score", 0.0))
        cell_id = assessment.grid_cell_id
        cell_map[cell_id] = {
            "row": row_idx, "col": col_idx,
            "risk": risk, "cell_size_m": cell_size_m,
        }
        grid_idx[(row_idx, col_idx)] = cell_id

    # 3. Filter cells above threshold
    at_risk_ids = {cid for cid, info in cell_map.items() if info["risk"] >= threshold}
    if not at_risk_ids:
        # Delete old zones, nothing to store
        _delete_old_zones(db, kommune_id, ct, level)
        db.flush()
        return []

    # 4. BFS connected-components (8-neighbourhood / Queen contiguity)
    visited: set[int] = set()
    components: list[list[int]] = []

    for seed_id in at_risk_ids:
        if seed_id in visited:
            continue
        component: list[int] = []
        queue: deque[int] = deque([seed_id])
        visited.add(seed_id)
        while queue:
            cid = queue.popleft()
            component.append(cid)
            info = cell_map[cid]
            r, c = info["row"], info["col"]
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    nb_id = grid_idx.get((r + dr, c + dc))
                    if nb_id is not None and nb_id in at_risk_ids and nb_id not in visited:
                        visited.add(nb_id)
                        queue.append(nb_id)
        components.append(component)

    # Sort components by size descending
    components.sort(key=len, reverse=True)

    # 5. Persist
    _delete_old_zones(db, kommune_id, ct, level)
    now = datetime.utcnow()

    result = []
    for zone_idx, comp in enumerate(components):
        risks = [cell_map[cid]["risk"] for cid in comp]
        mean_r = sum(risks) / len(risks)
        max_r = max(risks)
        area = sum(cell_map[cid]["cell_size_m"] ** 2 for cid in comp)

        zone = RiskZone(
            kommune_id=kommune_id,
            climate_type=ct,
            level=level,
            zone_index=zone_idx,
            cell_count=len(comp),
            mean_risk=round(mean_r, 2),
            max_risk=round(max_r, 2),
            area_m2=round(area, 0),
            calculated_at=now,
        )
        db.add(zone)
        db.flush()  # get zone.id

        for cid in comp:
            db.add(RiskZoneCell(
                risk_zone_id=zone.id,
                grid_cell_id=cid,
                risk_score=round(cell_map[cid]["risk"], 3),
            ))

        result.append({
            "zone_index": zone_idx,
            "cell_count": len(comp),
            "mean_risk": zone.mean_risk,
            "max_risk": zone.max_risk,
            "area_m2": zone.area_m2,
        })

    db.commit()
    log.info("Computed %d risk zones for kommune=%s type=%s level=%s (threshold=%.1f)",
             len(result), kommune_id, climate_type, level, threshold)
    return result


def get_risk_zones_geojson(db: Session, kommune_id: int, climate_type: str, level: int) -> dict:
    """Return risk zones as a GeoJSON FeatureCollection with merged polygons."""
    ct = ClimateType(climate_type)
    zones = (
        db.query(RiskZone)
        .filter(
            RiskZone.kommune_id == kommune_id,
            RiskZone.climate_type == ct,
            RiskZone.level == level,
        )
        .order_by(RiskZone.zone_index)
        .all()
    )

    features = []
    for zone in zones:
        # Merge cell geometries via ST_Union
        merged = (
            db.query(func.ST_AsGeoJSON(func.ST_Union(GridCell.geometry)))
            .join(RiskZoneCell, RiskZoneCell.grid_cell_id == GridCell.id)
            .filter(RiskZoneCell.risk_zone_id == zone.id)
            .scalar()
        )
        if not merged:
            continue
        import json
        geom = json.loads(merged)
        features.append({
            "type": "Feature",
            "geometry": geom,
            "properties": {
                "zone_index": zone.zone_index,
                "cell_count": zone.cell_count,
                "mean_risk": zone.mean_risk,
                "max_risk": zone.max_risk,
                "area_m2": zone.area_m2,
                "climate_type": climate_type,
            },
        })

    return {"type": "FeatureCollection", "features": features}


def get_risk_summary(db: Session, kommune_id: int) -> list[dict]:
    """Return a risk summary for all climate types that have data.

    Each entry: {climate_type, zone_count, total_area_m2, aggregated_risk, highest_zone_risk}.
    """
    from app.services.climate.registry import list_assessors

    all_types = [a["climate_type"] for a in list_assessors()]
    summaries = []

    for ct_str in all_types:
        ct = ClimateType(ct_str)
        zones = (
            db.query(RiskZone)
            .filter(RiskZone.kommune_id == kommune_id, RiskZone.climate_type == ct)
            .all()
        )
        if not zones:
            summaries.append({
                "climate_type": ct_str,
                "zone_count": 0,
                "total_area_m2": 0,
                "aggregated_risk": 0.0,
                "highest_zone_risk": 0.0,
            })
            continue

        total_area = sum(z.area_m2 for z in zones)
        weighted_sum = sum(z.area_m2 * z.mean_risk for z in zones)
        ari = weighted_sum / total_area if total_area > 0 else 0.0

        summaries.append({
            "climate_type": ct_str,
            "zone_count": len(zones),
            "total_area_m2": round(total_area, 0),
            "aggregated_risk": round(ari, 2),
            "highest_zone_risk": round(max(z.max_risk for z in zones), 2),
        })

    return summaries


def compute_aggregated_risk(db: Session, kommune_id: int, climate_type: str, level: int) -> float:
    """ARI = Σ(zone_area × zone_mean_risk) / Σ(zone_area) for zones with mean_risk ≥ threshold."""
    ct = ClimateType(climate_type)
    zones = (
        db.query(RiskZone)
        .filter(
            RiskZone.kommune_id == kommune_id,
            RiskZone.climate_type == ct,
            RiskZone.level == level,
        )
        .all()
    )
    if not zones:
        return 0.0
    total_area = sum(z.area_m2 for z in zones)
    if total_area == 0:
        return 0.0
    return sum(z.area_m2 * z.mean_risk for z in zones) / total_area


# ── Private ────────────────────────────────────────────────────────────────────

def _delete_old_zones(db: Session, kommune_id: int, ct: ClimateType, level: int):
    old = (
        db.query(RiskZone)
        .filter(
            RiskZone.kommune_id == kommune_id,
            RiskZone.climate_type == ct,
            RiskZone.level == level,
        )
        .all()
    )
    for z in old:
        db.delete(z)  # cascades to RiskZoneCell
    db.flush()
