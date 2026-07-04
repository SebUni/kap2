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
from app.services.engine.progress import FINALIZE, MonotonicProgress
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
            "id": c.id,
            "gitter_id": c.gitter_id,
            "x_3035": c.x_3035,
            "y_3035": c.y_3035,
            "row": c.row_idx,
            "col": c.col_idx,
            "cell_size_m": c.cell_size_m,
            "geometry": to_shape(c.geometry),
        } for c in cells]

        kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
        bundesland = kommune.bundesland if kommune else None
        population = kommune.population if kommune else None
        area_km2 = kommune.area_km2 if kommune else None
        osm_id = kommune.osm_id if kommune else None

        # Kommune-Zentroid (lon, lat) für ortsaufgelöste regionale Treiber (§B2).
        centroid = None
        if kommune is not None and kommune.boundary is not None:
            try:
                c = to_shape(kommune.boundary).centroid
                centroid = (c.x, c.y)
            except Exception:
                centroid = None

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
            status.message = f"{round(pct):.0f}% – {_last_phase[0] or 'Berechnung'}"
            if pct - _last_pct[0] >= 1.0 or pct >= 100.0 or phase:
                db.commit()
                _last_pct[0] = pct

        progress = MonotonicProgress(update_progress)
        from app.services import parameter_registry
        from app.services.engine.override_context import set_overrides

        overrides = parameter_registry.overrides_map(
            parameter_registry.load_db_overrides(db, kommune_id)
        )
        set_overrides(overrides)
        results = run_full_assessment(
            grid_cell_dicts, bundesland, population, area_km2, progress, overrides, osm_id,
            centroid,
        )

        update_progress(FINALIZE[0], "Speichere Ergebnisse")
        db.query(CellAssessment).filter(CellAssessment.kommune_id == kommune_id).delete()
        now = datetime.utcnow()
        for r in results:
            db.add(CellAssessment(
                kommune_id=kommune_id, grid_cell_id=r["grid_cell_id"],
                data=r["data"], calculated_at=now,
            ))
        update_progress(FINALIZE[1], "Speichere Ergebnisse")

        status.status = AssessmentStatus.DONE
        status.progress_pct = 100.0
        status.finished_at = datetime.utcnow()
        finished_iso = status.finished_at.isoformat()
        status.message = f"100% – Abgeschlossen"
        status.eta_seconds = 0.0
        if _steps:
            _steps[-1]["finished"] = finished_iso
            _steps[-1]["pct_end"] = round(FINALIZE[1], 1)
        _steps.append({
            "label": "Abgeschlossen",
            "detail": f"{len(results)} Zellen berechnet",
            "started": finished_iso,
            "finished": finished_iso,
            "pct_start": 100.0,
            "pct_end": 100.0,
        })
        status.step_history = list(_steps)
        db.commit()
        log.info("[TASK] Assessment DONE: %d Zellen", len(results))

        # Karten-Layer-Cache neu bauen (fertige gzip-Dateien auf Platte)
        try:
            from app.services import layer_cache
            layer_cache.invalidate(kommune_id)
            layer_cache.precompute(db, kommune_id)
        except Exception:
            log.exception("[TASK] layer_cache precompute failed kommune=%s", kommune_id)

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
