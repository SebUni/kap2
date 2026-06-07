"""Löscht abgeleitete Geodaten (Grid, Assessments, Risikozonen) für eine oder alle Kommunen."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.models import (
    CellAssessment,
    GridCell,
    MeasureImpact,
    RiskZone,
    RiskZoneCell,
)


def reset_kommune_grid_data(db: Session, kommune_id: int) -> dict:
    """Entfernt Grid und alle davon abhängigen Bewertungen für eine Kommune."""
    mi = (
        db.query(MeasureImpact)
        .filter(MeasureImpact.grid_cell_id.in_(
            db.query(GridCell.id).filter(GridCell.kommune_id == kommune_id)
        ))
        .delete(synchronize_session=False)
    )
    rzc = (
        db.query(RiskZoneCell)
        .filter(RiskZoneCell.risk_zone_id.in_(
            db.query(RiskZone.id).filter(RiskZone.kommune_id == kommune_id)
        ))
        .delete(synchronize_session=False)
    )
    rz = db.query(RiskZone).filter(RiskZone.kommune_id == kommune_id).delete(synchronize_session=False)
    ca = db.query(CellAssessment).filter(CellAssessment.kommune_id == kommune_id).delete(synchronize_session=False)
    gc = db.query(GridCell).filter(GridCell.kommune_id == kommune_id).delete(synchronize_session=False)
    db.commit()
    return {
        "kommune_id": kommune_id,
        "deleted_grid_cells": gc,
        "deleted_assessments": ca,
        "deleted_risk_zones": rz,
        "deleted_risk_zone_cells": rzc,
        "deleted_measure_impacts": mi,
    }


def reset_all_grid_data(db: Session) -> dict:
    db.query(MeasureImpact).delete(synchronize_session=False)
    db.query(RiskZoneCell).delete(synchronize_session=False)
    db.query(RiskZone).delete(synchronize_session=False)
    db.query(CellAssessment).delete(synchronize_session=False)
    gc = db.query(GridCell).delete(synchronize_session=False)
    db.commit()
    return {"deleted_grid_cells": gc, "scope": "all"}
