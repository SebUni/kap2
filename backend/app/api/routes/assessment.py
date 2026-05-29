import logging
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import (
    Kommune, ClimateAssessment, GridCell, ProjectStatus, ClimateType,
    AssessmentStatus,
)
from app.schemas.schemas import AssessmentRequest, AssessmentStatusOut
from app.tasks.assessment_task import run_assessment_background, abort_assessment, run_batch_assessment_background
from app.services.climate.registry import list_assessors

log = logging.getLogger(__name__)
router = APIRouter()


@router.get("/climate-types")
def get_climate_types():
    """List all available climate assessor types."""
    return list_assessors()


@router.post("/kommune/{kommune_id}/assess")
def start_assessment(
    kommune_id: int,
    req: AssessmentRequest,
    db: Session = Depends(get_db),
):
    """Start a climate assessment calculation in the background."""
    log.info("[ROUTE] POST /kommune/%s/assess  type=%s level=%s", kommune_id, req.climate_type, req.level)
    # Check kommune and grid exist
    cell_count = db.query(GridCell).filter(GridCell.kommune_id == kommune_id).count()
    log.info("[ROUTE] Grid cells for kommune %s: %d", kommune_id, cell_count)
    if cell_count == 0:
        raise HTTPException(400, "Keine Grid-Zellen vorhanden. Bitte zuerst Grid generieren.")

    # Immediately set status to RUNNING/0% so the frontend sees it right away
    # (before the background thread even starts)
    ct = ClimateType(req.climate_type)
    ps = (
        db.query(ProjectStatus)
        .filter(
            ProjectStatus.kommune_id == kommune_id,
            ProjectStatus.climate_type == ct,
            ProjectStatus.level == req.level,
        )
        .first()
    )
    if ps:
        ps.status = AssessmentStatus.RUNNING
        ps.progress_pct = 0.0
        ps.message = "Berechnung wird vorbereitet …"
        ps.started_at = datetime.utcnow()
        ps.finished_at = None
    else:
        ps = ProjectStatus(
            kommune_id=kommune_id,
            climate_type=ct,
            level=req.level,
            status=AssessmentStatus.RUNNING,
            progress_pct=0.0,
            message="Berechnung wird vorbereitet …",
            started_at=datetime.utcnow(),
        )
        db.add(ps)
    db.commit()

    # Kick off background task
    run_assessment_background(kommune_id, req.climate_type, req.level)

    return {
        "message": "Berechnung gestartet",
        "kommune_id": kommune_id,
        "climate_type": req.climate_type,
        "level": req.level,
    }


@router.post("/kommune/{kommune_id}/assess/batch")
def start_batch_assessment(
    kommune_id: int,
    level: int = 4,
    db: Session = Depends(get_db),
):
    """Start all climate assessments sequentially with shared OSM data.

    Pre-fetches OSM data once, then runs each assessor in order.
    """
    cell_count = db.query(GridCell).filter(GridCell.kommune_id == kommune_id).count()
    if cell_count == 0:
        raise HTTPException(400, "Keine Grid-Zellen vorhanden. Bitte zuerst Grid generieren.")

    run_batch_assessment_background(kommune_id, level)

    return {
        "message": "Batch-Berechnung gestartet",
        "kommune_id": kommune_id,
        "level": level,
    }


@router.post("/kommune/{kommune_id}/assess/abort")
def abort_running_assessment(
    kommune_id: int,
    req: AssessmentRequest,
    db: Session = Depends(get_db),
):
    """Abort a running climate assessment."""
    aborted = abort_assessment(kommune_id, req.climate_type, req.level)
    if aborted:
        # Update status in DB
        status = (
            db.query(ProjectStatus)
            .filter(
                ProjectStatus.kommune_id == kommune_id,
                ProjectStatus.climate_type == ClimateType(req.climate_type),
                ProjectStatus.level == req.level,
            )
            .first()
        )
        if status:
            status.status = AssessmentStatus.ERROR
            status.message = "Berechnung abgebrochen"
            db.commit()
        return {"message": "Berechnung wird abgebrochen", "aborted": True}
    return {"message": "Keine laufende Berechnung gefunden", "aborted": False}


@router.get("/kommune/{kommune_id}/status")
def get_status(kommune_id: int, db: Session = Depends(get_db)):
    """Get the calculation status for a municipality."""
    statuses = (
        db.query(ProjectStatus)
        .filter(ProjectStatus.kommune_id == kommune_id)
        .all()
    )
    return [
        {
            "climate_type": s.climate_type.value if s.climate_type else None,
            "level": s.level,
            "progress_pct": s.progress_pct,
            "status": s.status.value if s.status else None,
            "message": s.message,
            "started_at": s.started_at.isoformat() if s.started_at else None,
            "finished_at": s.finished_at.isoformat() if s.finished_at else None,
            "step_history": s.step_history or [],
            "eta_seconds": s.eta_seconds,
        }
        for s in statuses
    ]


@router.get("/kommune/{kommune_id}/assessment/{climate_type}")
def get_assessment(
    kommune_id: int,
    climate_type: str,
    level: int = 1,
    db: Session = Depends(get_db),
):
    """Get assessment results as GeoJSON FeatureCollection."""
    try:
        ct = ClimateType(climate_type)
    except ValueError:
        raise HTTPException(400, f"Unbekannter Klimatyp: {climate_type}")

    assessments = (
        db.query(ClimateAssessment, GridCell)
        .join(GridCell, ClimateAssessment.grid_cell_id == GridCell.id)
        .filter(
            ClimateAssessment.kommune_id == kommune_id,
            ClimateAssessment.climate_type == ct,
            ClimateAssessment.level == level,
        )
        .all()
    )

    features = []
    for assessment, cell in assessments:
        shape = to_shape(cell.geometry)
        features.append({
            "type": "Feature",
            "properties": {
                "grid_cell_id": cell.id,
                "row": cell.row_idx,
                "col": cell.col_idx,
                **assessment.indicators,
            },
            "geometry": mapping(shape),
        })

    return {
        "type": "FeatureCollection",
        "features": features,
    }


@router.get("/kommune/{kommune_id}/climate-history")
def get_climate_history(kommune_id: int, db: Session = Depends(get_db)):
    """Get historical climate indicator time series (from ~1990) for this municipality's region."""
    from app.services.climate.dwd_data import get_climate_history as _get_history

    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")

    bundesland = kommune.bundesland or None
    return _get_history(bundesland)


@router.get("/kommune/{kommune_id}/regional-climate")
def get_regional_climate(kommune_id: int, db: Session = Depends(get_db)):
    """Get current regional climate summary (hot days, temperatures) from DWD data."""
    from app.services.climate.dwd_data import get_regional_climate as _get_regional

    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")

    bundesland = kommune.bundesland or "Nordrhein-Westfalen"
    return _get_regional(bundesland)


@router.get("/kommune/{kommune_id}/climate-projection")
def get_climate_projection_route(kommune_id: int, db: Session = Depends(get_db)):
    """Get climate projection data (2025–2065) for RCP 4.5 and RCP 8.5."""
    from app.services.climate.dwd_data import get_climate_projection

    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")

    bundesland = kommune.bundesland or None
    return get_climate_projection(bundesland)


# ── Risk Zone endpoints ───────────────────────────────────────────────────────

@router.get("/kommune/{kommune_id}/risk-zones/{climate_type}")
def get_risk_zones(
    kommune_id: int,
    climate_type: str,
    level: int = 1,
    db: Session = Depends(get_db),
):
    """Get risk zones as GeoJSON FeatureCollection for a specific climate type."""
    from app.services.risk_zone_service import get_risk_zones_geojson
    try:
        ClimateType(climate_type)
    except ValueError:
        raise HTTPException(400, f"Unbekannter Klimatyp: {climate_type}")
    return get_risk_zones_geojson(db, kommune_id, climate_type, level)


@router.get("/kommune/{kommune_id}/risk-summary")
def get_risk_summary_route(kommune_id: int, db: Session = Depends(get_db)):
    """Get aggregated risk summary for all climate types."""
    from app.services.risk_zone_service import get_risk_summary
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")
    return get_risk_summary(db, kommune_id)


@router.get("/kommune/{kommune_id}/risk-projection/{climate_type}")
def get_risk_projection(
    kommune_id: int,
    climate_type: str,
    level: int = 1,
    db: Session = Depends(get_db),
):
    """Get risk zone projections (2025-2065) for a specific climate type."""
    from app.services.projection_service import project_risk_zones
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")
    try:
        ClimateType(climate_type)
    except ValueError:
        raise HTTPException(400, f"Unbekannter Klimatyp: {climate_type}")
    bundesland = kommune.bundesland or "Sachsen"
    return project_risk_zones(db, kommune_id, climate_type, level, bundesland)
