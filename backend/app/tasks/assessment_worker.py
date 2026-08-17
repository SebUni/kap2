"""Assessment-Kind-Prozess: ein Lauf je Aufruf, dann Prozessende (RAM → OS).

Gestartet vom API-Prozess (app.tasks.assessment_task) als
``python -m app.tasks.assessment_worker <kommune_id>`` — detached in eigener
Session/Prozessgruppe. Fortschritt, Abbruch und Ergebnisse laufen ausschließlich
über die Datenbank (ProjectStatus/CellAssessment) und Cache-Dateien: Der
API-Prozess hält nichts im RAM, übersteht Reload/Neustart, und der komplette
Rechen-Speicher (OSM-Geometrien, Fork-Worker, Allocator-Arenen) geht mit dem
Prozessende vollständig ans Betriebssystem zurück.

Exit-Codes: 0 = ok, 1 = Fehler, 2 = Usage, 3 = abgebrochen (Nutzer/Neustart),
70 = RAM-Limit (sanfter Abbruch durch den Watchdog).
"""

from __future__ import annotations

import logging
import os
import signal
import sys
import threading
import traceback
from datetime import datetime

log = logging.getLogger(__name__)

EXIT_OK = 0
EXIT_FAILED = 1
EXIT_USAGE = 2
EXIT_ABORTED = 3
EXIT_RSS_LIMIT = 70


def _apply_rlimit_backstop() -> None:
    """Optionaler Not-Backstop über RLIMIT_AS (default aus).

    Vorsicht: begrenzt den VIRTUELLEN Adressraum, der bei numpy/GEOS weit über
    dem realen RSS liegt — deshalb nur als dokumentierte Notbremse gedacht.
    """
    from app.config import settings

    mb = int(getattr(settings, "ASSESSMENT_RLIMIT_AS_MB", 0) or 0)
    if mb <= 0:
        return
    try:
        import resource

        limit = mb * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
        log.info("[WORKER] RLIMIT_AS-Backstop aktiv: %d MB", mb)
    except Exception:
        log.exception("[WORKER] RLIMIT_AS konnte nicht gesetzt werden")


def worker_main(kommune_id: int) -> int:
    from geoalchemy2.shape import to_shape

    from app.config import settings
    from app.db.database import SessionLocal
    from app.models.models import (
        AssessmentStatus, CellAssessment, GridCell, Kommune, ProjectStatus,
    )
    from app.services.engine.progress import FINALIZE, MonotonicProgress
    from app.services.engine.runner import run_full_assessment
    from app.tasks.assessment_task import LEVEL, TASK_KEY
    from app.tasks.memory_watchdog import RssWatchdog, proc_start_ticks

    _apply_rlimit_backstop()

    db = SessionLocal()
    cancel = threading.Event()
    # Abbruchgrund + Exit-Code setzt der jeweilige Auslöser (Nutzer/RAM/SIGTERM);
    # der erste Auslöser gewinnt.
    state = {"msg": "Berechnung wurde abgebrochen", "exit": EXIT_ABORTED}

    def _request_cancel(msg: str, exit_code: int) -> None:
        if not cancel.is_set():
            state["msg"] = msg
            state["exit"] = exit_code
        cancel.set()

    signal.signal(
        signal.SIGTERM,
        lambda *_: _request_cancel("Berechnung wurde abgebrochen", EXIT_ABORTED),
    )

    status: ProjectStatus | None = None
    watchdog: RssWatchdog | None = None

    def _owns_row() -> bool:
        """Gehört die Status-Zeile noch diesem Lauf? (Parent kann re-queuen.)"""
        try:
            db.rollback()
            db.refresh(status)
        except Exception:
            return False
        return (
            status.status == AssessmentStatus.RUNNING
            and status.worker_pid == os.getpid()
        )

    try:
        status = (
            db.query(ProjectStatus)
            .filter(ProjectStatus.kommune_id == kommune_id,
                    ProjectStatus.task_key == TASK_KEY)
            .first()
        )
        if not status:
            status = ProjectStatus(kommune_id=kommune_id, task_key=TASK_KEY, level=LEVEL)
            db.add(status)
        status.status = AssessmentStatus.RUNNING
        status.progress_pct = 0.0
        status.started_at = datetime.utcnow()
        status.finished_at = None
        status.message = "Berechnung gestartet..."
        status.step_history = []
        status.eta_seconds = None
        status.worker_pid = os.getpid()
        status.worker_start_ticks = proc_start_ticks(os.getpid())
        status.abort_requested = False
        db.commit()

        def _on_breach(mb: float) -> None:
            _request_cancel(
                f"Abbruch: RAM-Limit erreicht ({mb:.0f} MB > "
                f"ASSESSMENT_MAX_RSS_MB={settings.ASSESSMENT_MAX_RSS_MB}) — "
                "Limit erhöhen oder Grid verkleinern",
                EXIT_RSS_LIMIT,
            )

        def _on_escalate(mb: float) -> None:
            # Der sanfte Abbruch greift nicht (Worker hängt in einem C-Call):
            # Status mit eigener Session festschreiben, dann die gesamte
            # Prozessgruppe (inkl. Fork-Worker) hart beenden.
            try:
                edb = SessionLocal()
                try:
                    row = (
                        edb.query(ProjectStatus)
                        .filter(ProjectStatus.kommune_id == kommune_id,
                                ProjectStatus.task_key == TASK_KEY)
                        .first()
                    )
                    if row is not None and row.status == AssessmentStatus.RUNNING:
                        row.status = AssessmentStatus.ERROR
                        row.message = (
                            f"Abbruch (hart): RAM-Limit überschritten ({mb:.0f} MB > "
                            f"{settings.ASSESSMENT_MAX_RSS_MB} MB) und Prozess reagierte nicht"
                        )
                        row.finished_at = datetime.utcnow()
                        row.worker_pid = None
                        edb.commit()
                finally:
                    edb.close()
            finally:
                os.killpg(os.getpgrp(), signal.SIGKILL)

        watchdog = RssWatchdog(
            os.getpid(),
            float(settings.ASSESSMENT_MAX_RSS_MB),
            _on_breach,
            interval_s=float(settings.ASSESSMENT_WATCHDOG_INTERVAL_S),
            on_escalate=_on_escalate,
        )
        watchdog.start()

        cells = db.query(GridCell).filter(GridCell.kommune_id == kommune_id).all()
        if not cells:
            status.status = AssessmentStatus.ERROR
            status.message = "Keine Grid-Zellen gefunden. Bitte zuerst Grid generieren."
            status.finished_at = datetime.utcnow()
            status.worker_pid = None
            db.commit()
            return EXIT_FAILED

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
            if cancel.is_set():
                raise InterruptedError(state["msg"])
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
                # Abbruch-Flag frisch aus der DB (Spaltenabfrage umgeht die
                # Identity-Map, die den alten Wert festhalten würde).
                flag = (
                    db.query(ProjectStatus.abort_requested)
                    .filter(ProjectStatus.id == status.id)
                    .scalar()
                )
                if flag:
                    _request_cancel("Berechnung wurde abgebrochen", EXIT_ABORTED)
                    raise InterruptedError(state["msg"])

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

        # Kommunen-Bevölkerung als Zensus-Summe der Zellen persistieren
        # (korrekter als der nie gesetzte Anlage-Wert; Basis fürs Kommunen-Profil)
        pop_sum = sum(
            float((r["data"].get("inputs") or {}).get("pop", 0.0) or 0.0)
            for r in results
        )
        if kommune is not None and pop_sum > 0:
            kommune.population = int(round(pop_sum))

        status.status = AssessmentStatus.DONE
        status.progress_pct = 100.0
        status.finished_at = datetime.utcnow()
        finished_iso = status.finished_at.isoformat()
        status.message = "100% – Abgeschlossen"
        status.eta_seconds = 0.0
        status.worker_pid = None
        status.recalc_recommended = False
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
        log.info("[WORKER] Assessment DONE: %d Zellen (kommune=%s)", len(results), kommune_id)

        # Abgeleitete Artefakte (Karten-Layer + Dashboard-Payloads) noch in
        # diesem Wegwerf-Prozess vorbauen: Der erste Dashboard-/Karten-Aufruf
        # ist danach reines Datei-Lesen, und die schwere Serialisierung belastet
        # nie den API-Prozess.
        try:
            from app.services import aggregate_cache, artifact_rebuild, layer_cache
            aggregate_cache.invalidate(kommune_id)
            layer_cache.invalidate(kommune_id)
            artifact_rebuild.rebuild_now(db, kommune_id, layers=True)
        except Exception:
            log.exception("[WORKER] Artefakt-Precompute fehlgeschlagen kommune=%s", kommune_id)

        return EXIT_OK

    except InterruptedError:
        if status is not None and _owns_row():
            # Bei „Neustart angefordert" hat der Parent die Zeile bereits auf
            # QUEUED gesetzt — die gehört dann dem nächsten Lauf.
            status.status = AssessmentStatus.ERROR
            status.message = state["msg"]
            status.finished_at = datetime.utcnow()
            status.worker_pid = None
            db.commit()
        return state["exit"]
    except Exception as e:
        log.error("[WORKER] Assessment FAILED:\n%s", traceback.format_exc())
        if status is not None and _owns_row():
            status.status = AssessmentStatus.ERROR
            status.message = f"Fehler: {str(e)[:500]}"
            status.finished_at = datetime.utcnow()
            status.worker_pid = None
            db.commit()
        return EXIT_FAILED
    finally:
        if watchdog is not None:
            watchdog.stop()
        try:
            # Gürtel & Hosenträger: Prozessende räumt ohnehin auf, aber falls
            # worker_main je in-process aufgerufen wird, bleiben keine
            # Stadt-Geometrien im Speicher zurück.
            from app.services.climate.heat.osm_data import clear_osm_cache
            from app.services.terrain_service import clear_terrain_cache
            from app.services.zensus_loader import clear_bbox_cache
            clear_osm_cache()
            clear_terrain_cache()
            clear_bbox_cache()
        except Exception:
            pass
        db.close()


def main(argv: list[str]) -> int:
    from app.log_config import setup_logging

    setup_logging()
    if len(argv) != 1:
        print("usage: python -m app.tasks.assessment_worker <kommune_id>", file=sys.stderr)
        return EXIT_USAGE
    try:
        kommune_id = int(argv[0])
    except ValueError:
        print("kommune_id muss eine Zahl sein", file=sys.stderr)
        return EXIT_USAGE
    log.info("[WORKER] Start kommune=%s pid=%s", kommune_id, os.getpid())
    code = worker_main(kommune_id)
    log.info("[WORKER] Ende kommune=%s exit=%s", kommune_id, code)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
