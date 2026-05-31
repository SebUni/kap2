"""Hintergrund-Assessment (ein Lauf je Kommune) mit Status-Tracking & Abbruch."""

import logging
import threading
import traceback
from datetime import datetime

from geoalchemy2.shape import to_shape
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.models import (
    Kommune, GridCell, CellAssessment, ProjectStatus, AssessmentStatus,
)
from app.services.engine.runner import run_full_assessment

log = logging.getLogger(__name__)

TASK_KEY = "assessment"
LEVEL = 1

_running_tasks: dict[int, threading.Event] = {}


def run_assessment_background(kommune_id: int):
    """Startet einen Hintergrund-Thread für die vollständige Bewertung."""
    if kommune_id in _running_tasks:
        _running_tasks[kommune_id].set()
    cancel_event = threading.Event()
    _running_tasks[kommune_id] = cancel_event
    thread = threading.Thread(
        target=_run_assessment, args=(kommune_id, cancel_event), daemon=True,
    )
    thread.start()
    log.info("[TASK] Assessment-Thread gestartet für kommune=%s", kommune_id)


def abort_assessment(kommune_id: int) -> bool:
    event = _running_tasks.get(kommune_id)
    if event:
        event.set()
        return True
    return False


def _get_status(db: Session, kommune_id: int) -> ProjectStatus:
    status = (
        db.query(ProjectStatus)
        .filter(ProjectStatus.kommune_id == kommune_id, ProjectStatus.task_key == TASK_KEY)
        .first()
    )
    if not status:
        status = ProjectStatus(kommune_id=kommune_id, task_key=TASK_KEY, level=LEVEL)
        db.add(status)
    return status


def _run_assessment(kommune_id: int, cancel_event: threading.Event):
    db: Session = SessionLocal()
    status = None
    try:
        status = _get_status(db, kommune_id)
        status.status = AssessmentStatus.RUNNING
        status.progress_pct = 0.0
        status.started_at = datetime.utcnow()
        status.finished_at = None
        status.message = "Berechnung gestartet..."
        status.step_history = []
        status.eta_seconds = None
        db.commit()

        cells = db.query(GridCell).filter(GridCell.kommune_id == kommune_id).all()
        if not cells:
            status.status = AssessmentStatus.ERROR
            status.message = "Keine Grid-Zellen gefunden. Bitte zuerst Grid generieren."
            status.finished_at = datetime.utcnow()
            db.commit()
            return

        grid_cell_dicts = [{
            "id": c.id, "row": c.row_idx, "col": c.col_idx,
            "cell_size_m": c.cell_size_m, "geometry": to_shape(c.geometry),
        } for c in cells]

        kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
        bundesland = kommune.bundesland if kommune else None
        population = kommune.population if kommune else None
        area_km2 = kommune.area_km2 if kommune else None

        _last_pct = [0.0]
        _last_phase = [""]
        _steps: list[dict] = []
        _start = datetime.utcnow()

        def update_progress(pct: float, phase: str | None = None, detail: str | None = None):
            if cancel_event.is_set():
                raise InterruptedError("Berechnung abgebrochen")
            status.progress_pct = round(pct, 1)
            now = datetime.utcnow()
            elapsed = (now - _start).total_seconds()
            status.eta_seconds = round(elapsed * (100.0 - pct) / pct, 1) if pct > 0 else None
            if phase and phase != _last_phase[0]:
                iso = now.isoformat()
                if _steps:
                    _steps[-1]["finished"] = iso
                    _steps[-1]["pct_end"] = round(pct, 1)
                _steps.append({"label": phase, "detail": detail or "", "started": iso,
                               "finished": None, "pct_start": round(pct, 1), "pct_end": None})
                _last_phase[0] = phase
                status.step_history = list(_steps)
            elif detail and _steps:
                _steps[-1]["detail"] = detail
                status.step_history = list(_steps)
            status.message = f"{_last_phase[0] or 'Berechnung'} ({round(pct):.0f}%)"
            if pct - _last_pct[0] >= 2.0 or pct >= 100.0 or phase:
                db.commit()
                _last_pct[0] = pct

        results = run_full_assessment(
            grid_cell_dicts, bundesland, population, area_km2, update_progress,
        )

        db.query(CellAssessment).filter(CellAssessment.kommune_id == kommune_id).delete()
        now = datetime.utcnow()
        for r in results:
            db.add(CellAssessment(
                kommune_id=kommune_id, grid_cell_id=r["grid_cell_id"],
                data=r["data"], calculated_at=now,
            ))

        status.status = AssessmentStatus.DONE
        status.progress_pct = 100.0
        status.message = f"Fertig – {len(results)} Zellen berechnet"
        status.finished_at = datetime.utcnow()
        status.eta_seconds = 0.0
        if _steps:
            _steps[-1]["finished"] = status.finished_at.isoformat()
            _steps[-1]["pct_end"] = 100.0
        status.step_history = list(_steps)
        db.commit()
        log.info("[TASK] Assessment DONE: %d Zellen", len(results))

    except InterruptedError:
        if status:
            status.status = AssessmentStatus.ERROR
            status.message = "Berechnung wurde abgebrochen"
            status.finished_at = datetime.utcnow()
            db.commit()
    except Exception as e:
        log.error("[TASK] Assessment FAILED:\n%s", traceback.format_exc())
        if status:
            status.status = AssessmentStatus.ERROR
            status.message = f"Fehler: {str(e)[:500]}"
            status.finished_at = datetime.utcnow()
            db.commit()
    finally:
        _running_tasks.pop(kommune_id, None)
        db.close()
