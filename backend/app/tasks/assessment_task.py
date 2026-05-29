"""Background assessment tasks with status tracking and abort support."""

import logging
import threading
import traceback
from datetime import datetime

from geoalchemy2.shape import to_shape
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.models import (
    Kommune, GridCell, ClimateAssessment, ConfigParameter, ProjectStatus,
    ClimateType, AssessmentStatus,
)
from app.services.climate.registry import get_assessor, list_assessors

log = logging.getLogger(__name__)

# Track running threads so they can be aborted
_running_tasks: dict[str, threading.Event] = {}
_batch_lock = threading.Lock()  # serialise batch runs


def _task_key(kommune_id: int, climate_type: str, level: int) -> str:
    return f"{kommune_id}:{climate_type}:{level}"


def run_assessment_background(kommune_id: int, climate_type: str, level: int):
    """Start a background thread to run the climate assessment."""
    key = _task_key(kommune_id, climate_type, level)
    log.info("[TASK] run_assessment_background called: kommune=%s type=%s level=%s key=%s",
             kommune_id, climate_type, level, key)
    # Abort any already-running task for this combo
    if key in _running_tasks:
        log.info("[TASK] Aborting previous task for key=%s", key)
        _running_tasks[key].set()
    cancel_event = threading.Event()
    _running_tasks[key] = cancel_event

    thread = threading.Thread(
        target=_run_assessment,
        args=(kommune_id, climate_type, level, cancel_event),
        daemon=True,
    )
    thread.start()
    log.info("[TASK] Background thread started: %s (thread=%s)", key, thread.name)


def abort_assessment(kommune_id: int, climate_type: str, level: int) -> bool:
    """Abort a running assessment. Returns True if a task was found and signalled."""
    key = _task_key(kommune_id, climate_type, level)
    log.info("[TASK] abort_assessment called: key=%s, active_tasks=%s", key, list(_running_tasks.keys()))
    event = _running_tasks.get(key)
    if event:
        event.set()
        log.info("[TASK] Abort signal sent for key=%s", key)
        return True
    log.warning("[TASK] No running task found for key=%s", key)
    return False


def _run_assessment(
    kommune_id: int, climate_type_str: str, level: int,
    cancel_event: threading.Event,
):
    log.info("[TASK] _run_assessment ENTER: kommune=%s type=%s level=%s",
             kommune_id, climate_type_str, level)
    db: Session = SessionLocal()
    try:
        climate_type = ClimateType(climate_type_str)
        log.info("[TASK] ClimateType resolved: %s", climate_type)

        # Create or update project status
        status = (
            db.query(ProjectStatus)
            .filter(
                ProjectStatus.kommune_id == kommune_id,
                ProjectStatus.climate_type == climate_type,
                ProjectStatus.level == level,
            )
            .first()
        )
        if not status:
            log.info("[TASK] Creating new ProjectStatus row")
            status = ProjectStatus(
                kommune_id=kommune_id,
                climate_type=climate_type,
                level=level,
            )
            db.add(status)
        else:
            log.info("[TASK] Reusing existing ProjectStatus id=%s (was %s)", status.id, status.status)

        status.status = AssessmentStatus.RUNNING
        status.progress_pct = 0.0
        status.started_at = datetime.utcnow()
        status.finished_at = None
        status.message = "Berechnung gestartet..."
        status.step_history = []
        status.eta_seconds = None
        db.commit()
        log.info("[TASK] Status set to RUNNING, committed")

        # Get assessor
        assessor = get_assessor(climate_type_str)
        if not assessor:
            log.error("[TASK] No assessor found for type=%s", climate_type_str)
            status.status = AssessmentStatus.ERROR
            status.message = f"Kein Assessor für {climate_type_str} gefunden"
            status.finished_at = datetime.utcnow()
            db.commit()
            return
        log.info("[TASK] Assessor loaded: %s (max_level=%s)", assessor.label, assessor.max_level)

        # Load grid cells
        cells = db.query(GridCell).filter(GridCell.kommune_id == kommune_id).all()
        if not cells:
            log.error("[TASK] No grid cells found for kommune=%s", kommune_id)
            status.status = AssessmentStatus.ERROR
            status.message = "Keine Grid-Zellen gefunden. Bitte zuerst Grid generieren."
            status.finished_at = datetime.utcnow()
            db.commit()
            return
        log.info("[TASK] Loaded %d grid cells", len(cells))

        grid_cell_dicts = []
        for cell in cells:
            grid_cell_dicts.append({
                "id": cell.id,
                "row": cell.row_idx,
                "col": cell.col_idx,
                "cell_size_m": cell.cell_size_m,
                "geometry": to_shape(cell.geometry),
            })

        # Load config params as flat dict
        params = db.query(ConfigParameter).filter(
            ConfigParameter.kommune_id == kommune_id
        ).all()
        config_dict = {f"{p.category}.{p.key}": p.value for p in params}
        log.info("[TASK] Loaded %d config params: %s", len(params), list(config_dict.keys()))

        # Load kommune for bundesland info (used by DWD data)
        kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
        if kommune and kommune.bundesland:
            config_dict["_bundesland"] = kommune.bundesland
            log.info("[TASK] Bundesland: %s", kommune.bundesland)
        else:
            log.warning("[TASK] No bundesland set for kommune=%s", kommune_id)

        # Progress callback (also checks for abort)
        _last_committed_pct = [0.0]
        _last_phase = [""]
        _step_history: list[dict] = []
        _start_time = datetime.utcnow()

        def update_progress(pct: float, phase: str | None = None, detail: str | None = None):
            if cancel_event.is_set():
                log.info("[TASK] Cancel event detected at %.1f%%", pct)
                raise InterruptedError("Berechnung abgebrochen")
            status.progress_pct = round(pct, 1)

            now = datetime.utcnow()

            # ETA calculation
            elapsed = (now - _start_time).total_seconds()
            if pct > 0:
                eta = elapsed * (100.0 - pct) / pct
            else:
                eta = None
            status.eta_seconds = round(eta, 1) if eta is not None else None

            # Step history management: new phase = finish old step, start new one
            if phase and phase != _last_phase[0]:
                now_iso = now.isoformat()
                # Close previous step
                if _step_history:
                    _step_history[-1]["finished"] = now_iso
                    _step_history[-1]["pct_end"] = round(pct, 1)
                # Open new step
                _step_history.append({
                    "label": phase,
                    "detail": detail or "",
                    "started": now_iso,
                    "finished": None,
                    "pct_start": round(pct, 1),
                    "pct_end": None,
                })
                _last_phase[0] = phase
                status.step_history = list(_step_history)
            elif detail and _step_history:
                # Update detail of current step without changing phase
                _step_history[-1]["detail"] = detail
                status.step_history = list(_step_history)

            msg = _last_phase[0] or "Berechnung"
            status.message = f"{msg} ({round(pct, 0):.0f}%)"
            # Only commit to DB every ~2% or on phase change to avoid bottleneck
            if pct - _last_committed_pct[0] >= 2.0 or pct >= 100.0 or phase:
                db.commit()
                _last_committed_pct[0] = pct

        # Run assessment
        log.info("[TASK] Starting assessor.assess() for level=%s with %d cells", level, len(grid_cell_dicts))
        results = assessor.assess(
            kommune_id=kommune_id,
            level=level,
            grid_cells=grid_cell_dicts,
            config_params=config_dict,
            progress_callback=update_progress,
        )

        log.info("[TASK] assessor.assess() returned %d results", len(results))

        # Delete old assessments for this commune/type/level
        deleted = db.query(ClimateAssessment).filter(
            ClimateAssessment.kommune_id == kommune_id,
            ClimateAssessment.climate_type == climate_type,
            ClimateAssessment.level == level,
        ).delete()
        log.info("[TASK] Deleted %d old assessments", deleted)

        # Save results
        for r in results:
            db.add(ClimateAssessment(
                kommune_id=kommune_id,
                grid_cell_id=r.grid_cell_id,
                climate_type=climate_type,
                level=level,
                indicators=r.indicators,
                calculated_at=datetime.utcnow(),
            ))

        # ── Compute risk zones ─────────────────────────────────────────
        update_progress(95.0, "Risikogebiete berechnen", "Connected-Component-Analyse")
        try:
            from app.services.risk_zone_service import compute_risk_zones
            zones = compute_risk_zones(db, kommune_id, climate_type_str, level)
            log.info("[TASK] Computed %d risk zones", len(zones))
        except Exception as rz_err:
            log.warning("[TASK] Risk-zone computation failed (non-fatal): %s", rz_err)

        status.status = AssessmentStatus.DONE
        status.progress_pct = 100.0
        status.message = f"Fertig – {len(results)} Zellen berechnet"
        status.finished_at = datetime.utcnow()
        status.eta_seconds = 0.0
        # Close final step
        if _step_history:
            _step_history[-1]["finished"] = status.finished_at.isoformat()
            _step_history[-1]["pct_end"] = 100.0
        status.step_history = list(_step_history)
        db.commit()
        log.info("[TASK] ✓ Assessment DONE: %d cells saved", len(results))

    except InterruptedError:
        log.info("[TASK] Assessment interrupted (aborted by user)")
        status.status = AssessmentStatus.ERROR
        status.message = "Berechnung wurde abgebrochen"
        status.finished_at = datetime.utcnow()
        db.commit()
    except Exception as e:
        log.error("[TASK] Assessment FAILED with exception:\n%s", traceback.format_exc())
        status.status = AssessmentStatus.ERROR
        status.message = f"Fehler: {str(e)[:500]}"
        status.finished_at = datetime.utcnow()
        db.commit()
    finally:
        key = _task_key(kommune_id, climate_type_str, level)
        _running_tasks.pop(key, None)
        db.close()
        log.info("[TASK] _run_assessment EXIT: key=%s", key)


# ── Batch (all types) ─────────────────────────────────────────────────────────

def run_batch_assessment_background(kommune_id: int, level: int, types: list[str] | None = None):
    """Run all climate assessments sequentially in a single background thread.

    1. Pre-fetches OSM data once (cached for all subsequent assessors).
    2. Runs each assessor in order, reusing cached OSM data.
    """
    key = f"batch:{kommune_id}:{level}"
    if key in _running_tasks:
        _running_tasks[key].set()
    cancel_event = threading.Event()
    _running_tasks[key] = cancel_event

    thread = threading.Thread(
        target=_run_batch,
        args=(kommune_id, level, cancel_event, types),
        daemon=True,
    )
    thread.start()
    log.info("[BATCH] Background thread started for kommune=%s level=%s", kommune_id, level)


def _run_batch(
    kommune_id: int, level: int,
    cancel_event: threading.Event,
    types: list[str] | None,
):
    """Sequential batch runner — pre-fetches OSM, then runs each assessor."""
    from app.services.climate.heat.osm_data import prefetch_osm_data, clear_osm_cache

    db: Session = SessionLocal()
    try:
        # Determine which types to run
        if types:
            climate_types = types
        else:
            climate_types = [info["climate_type"] for info in list_assessors()]

        log.info("[BATCH] Starting batch for %d types: %s", len(climate_types), climate_types)

        # ── Load grid cells once (shared by all assessors) ───────────────
        cells = db.query(GridCell).filter(GridCell.kommune_id == kommune_id).all()
        if not cells:
            log.error("[BATCH] No grid cells for kommune=%s", kommune_id)
            return

        grid_cell_dicts = []
        for cell in cells:
            grid_cell_dicts.append({
                "id": cell.id,
                "row": cell.row_idx,
                "col": cell.col_idx,
                "cell_size_m": cell.cell_size_m,
                "geometry": to_shape(cell.geometry),
            })

        # ── Pre-fetch OSM data (single Overpass call, cached) ────────────
        log.info("[BATCH] Pre-fetching OSM landuse data for %d cells", len(grid_cell_dicts))
        include_buildings = level >= 3
        prefetch_osm_data(grid_cell_dicts, include_buildings=include_buildings)
        log.info("[BATCH] OSM data pre-fetched and cached")

        # ── Mark all types as RUNNING ────────────────────────────────────
        for ct_str in climate_types:
            try:
                ct = ClimateType(ct_str)
                ps = (
                    db.query(ProjectStatus)
                    .filter(
                        ProjectStatus.kommune_id == kommune_id,
                        ProjectStatus.climate_type == ct,
                        ProjectStatus.level == level,
                    )
                    .first()
                )
                if not ps:
                    ps = ProjectStatus(
                        kommune_id=kommune_id,
                        climate_type=ct,
                        level=level,
                    )
                    db.add(ps)
                ps.status = AssessmentStatus.PENDING
                ps.progress_pct = 0.0
                ps.message = f"Warte auf Berechnung (Batch)"
                ps.started_at = None
                ps.finished_at = None
                ps.step_history = []
                ps.eta_seconds = None
            except Exception:
                pass
        db.commit()

        # ── Run each assessor sequentially ───────────────────────────────
        for i, ct_str in enumerate(climate_types):
            if cancel_event.is_set():
                log.info("[BATCH] Cancelled before starting %s", ct_str)
                break
            log.info("[BATCH] Running assessor %d/%d: %s", i + 1, len(climate_types), ct_str)
            _run_assessment(kommune_id, ct_str, level, cancel_event)
            log.info("[BATCH] Completed %s", ct_str)

        # ── Clean up cache after batch ───────────────────────────────────
        clear_osm_cache()
        log.info("[BATCH] ✓ Batch complete for kommune=%s", kommune_id)

    except Exception:
        log.error("[BATCH] Batch failed:\n%s", traceback.format_exc())
    finally:
        key = f"batch:{kommune_id}:{level}"
        _running_tasks.pop(key, None)
        db.close()
