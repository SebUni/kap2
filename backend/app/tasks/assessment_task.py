"""Parent-Seite der Hintergrund-Bewertung: Warteschlange + Kind-Prozesse.

Assessments laufen NICHT mehr als Thread im API-Prozess, sondern als detachte
Kind-Prozesse (``app.tasks.assessment_worker``): Der API-Prozess bleibt klein,
und der Rechen-RAM geht mit dem Kind-Exit vollständig ans OS zurück.

Wahrheit über Läufe liegt in der DB (``ProjectStatus``: Status, ``worker_pid``
+ ``worker_start_ticks`` gegen PID-Reuse, ``abort_requested``, ``queued_at``).
Dieses Modul hält nur Popen-Handles zum Zombie-Reaping/Exit-Code-Lesen sowie
einen Scheduler-Thread, der Slots (``ASSESSMENT_MAX_CONCURRENT``) FIFO vergibt.
Damit überstehen Läufe Reload/Neustart des API-Prozesses: verwaiste Kinder
rechnen weiter und bleiben über PID+Ticks korrekt als „läuft" erkennbar.
"""

from __future__ import annotations

import logging
import os
import signal
import subprocess
import sys
import threading
import time
from datetime import datetime

from sqlalchemy.orm import Session

from app.config import settings
from app.db.database import SessionLocal
from app.models.models import AssessmentStatus, ProjectStatus
from app.tasks.memory_watchdog import pid_alive, proc_start_ticks

log = logging.getLogger(__name__)

TASK_KEY = "assessment"
LEVEL = 1

_BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_LOG_DIR = os.path.join(_BACKEND_DIR, "logs")

_SCHEDULER_TICK_S = 3.0
_ABORT_KILL_GRACE_S = 30.0

_lock = threading.RLock()
_procs: dict[int, subprocess.Popen] = {}          # kommune_id → Popen (nur Reaping)
_last_exit: dict[int, int] = {}                   # kommune_id → letzter Exit-Code
_kill_deadlines: dict[int, float] = {}            # kommune_id → SIGKILL-Frist nach Abort
_wake = threading.Event()
_scheduler_started = False


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


def is_row_alive(status: ProjectStatus) -> bool:
    """True, wenn der zur Status-Zeile gehörende Kind-Prozess lebt."""
    return pid_alive(status.worker_pid, status.worker_start_ticks)


def is_task_alive(db: Session, kommune_id: int) -> bool:
    status = (
        db.query(ProjectStatus)
        .filter(ProjectStatus.kommune_id == kommune_id, ProjectStatus.task_key == TASK_KEY)
        .first()
    )
    return bool(status and is_row_alive(status))


def _signal_pid(pid: int | None, sig: int) -> None:
    if not pid:
        return
    try:
        os.kill(pid, sig)
    except (ProcessLookupError, PermissionError):
        pass


def run_assessment_background(kommune_id: int) -> None:
    """Reiht die Kommune ein; der Scheduler startet, sobald ein Slot frei ist.

    Läuft für dieselbe Kommune bereits ein Prozess, wird er abgebrochen und die
    Kommune neu eingereiht (bisherige Neustart-Semantik). Die Status-Zeile
    gehört ab jetzt dem NEUEN Lauf — der alte Kind-Prozess erkennt das an
    Status ≠ RUNNING/fremder PID und schreibt kein ERROR mehr hinein.
    """
    db = SessionLocal()
    try:
        status = _get_status(db, kommune_id)
        restarting = is_row_alive(status)
        if restarting:
            _signal_pid(status.worker_pid, signal.SIGTERM)
            with _lock:
                _kill_deadlines[kommune_id] = time.monotonic() + _ABORT_KILL_GRACE_S
        status.status = AssessmentStatus.QUEUED
        status.queued_at = datetime.utcnow()
        status.progress_pct = 0.0
        status.message = (
            "Neustart angefordert – wartet auf freien Berechnungs-Slot …"
            if restarting else "Wartet auf freien Berechnungs-Slot …"
        )
        status.started_at = None
        status.finished_at = None
        status.step_history = []
        status.eta_seconds = None
        status.abort_requested = restarting  # Signal an den ALTEN Prozess
        db.commit()
    finally:
        db.close()
    ensure_scheduler_started()
    _wake.set()


def abort_assessment(db: Session, kommune_id: int) -> bool:
    """Bricht einen laufenden oder eingereihten Lauf ab. True = etwas abgebrochen."""
    status = (
        db.query(ProjectStatus)
        .filter(ProjectStatus.kommune_id == kommune_id, ProjectStatus.task_key == TASK_KEY)
        .first()
    )
    if not status:
        return False
    alive = is_row_alive(status)
    if status.status in (AssessmentStatus.RUNNING, AssessmentStatus.QUEUED) and alive:
        status.abort_requested = True
        db.commit()
        _signal_pid(status.worker_pid, signal.SIGTERM)
        with _lock:
            _kill_deadlines[kommune_id] = time.monotonic() + _ABORT_KILL_GRACE_S
        ensure_scheduler_started()
        _wake.set()
        return True
    if status.status in (AssessmentStatus.RUNNING, AssessmentStatus.QUEUED):
        # Kein lebender Prozess (Neustart/Standby/tot) → autoritativ beenden,
        # sonst bliebe der Lauf für immer als „läuft/wartet" hängen.
        status.status = AssessmentStatus.ERROR
        status.message = "Berechnung abgebrochen"
        status.finished_at = datetime.utcnow()
        status.queued_at = None
        status.worker_pid = None
        db.commit()
        return True
    return False


def ensure_scheduler_started() -> None:
    """Startet den Scheduler-Thread genau einmal (idempotent)."""
    global _scheduler_started
    with _lock:
        if _scheduler_started:
            return
        _scheduler_started = True
    thread = threading.Thread(target=_scheduler_loop, daemon=True, name="assessment-scheduler")
    thread.start()
    log.info("[TASK] Assessment-Scheduler gestartet (max_concurrent=%s)",
             settings.ASSESSMENT_MAX_CONCURRENT)


def recover_on_startup() -> None:
    """Nach API-Start: tote RUNNING-Zeilen heilen, Warteschlange wieder anwerfen.

    RUNNING-Zeilen mit LEBENDEM Prozess bleiben unangetastet — das sind
    verwaiste Kinder eines früheren API-Prozesses (z. B. ``--reload``), die
    weiterrechnen und ihren Status selbst pflegen.
    """
    try:
        db = SessionLocal()
        try:
            rows = (
                db.query(ProjectStatus)
                .filter(ProjectStatus.task_key == TASK_KEY,
                        ProjectStatus.status == AssessmentStatus.RUNNING)
                .all()
            )
            for row in rows:
                if not is_row_alive(row):
                    row.status = AssessmentStatus.ERROR
                    row.message = "Berechnung unterbrochen (Standby/Neustart) – bitte neu starten"
                    row.finished_at = datetime.utcnow()
                    row.worker_pid = None
            db.commit()
        finally:
            db.close()
    except Exception:
        log.exception("[TASK] recover_on_startup fehlgeschlagen")
    ensure_scheduler_started()
    _wake.set()


def _scheduler_loop() -> None:  # pragma: no cover - Endlosschleife; Logik in _scheduler_tick
    while True:
        _wake.wait(timeout=_SCHEDULER_TICK_S)
        _wake.clear()
        try:
            _scheduler_tick()
        except Exception:
            log.exception("[TASK] Scheduler-Tick fehlgeschlagen")


def _scheduler_tick() -> None:
    now = time.monotonic()
    with _lock:
        for kid, proc in list(_procs.items()):
            rc = proc.poll()
            if rc is None:
                continue
            _procs.pop(kid, None)
            _kill_deadlines.pop(kid, None)
            _last_exit[kid] = rc
            log.info("[TASK] Assessment-Kindprozess beendet kommune=%s exit=%s", kid, rc)
        deadlines = dict(_kill_deadlines)

    db = SessionLocal()
    try:
        rows = (
            db.query(ProjectStatus)
            .filter(ProjectStatus.task_key == TASK_KEY,
                    ProjectStatus.status.in_([AssessmentStatus.RUNNING, AssessmentStatus.QUEUED]))
            .all()
        )
        occupied = 0
        startable: list[ProjectStatus] = []
        for row in rows:
            alive = is_row_alive(row)
            if row.status == AssessmentStatus.RUNNING:
                if alive:
                    occupied += 1
                    if row.abort_requested:
                        deadline = deadlines.get(row.kommune_id)
                        if deadline is not None and now > deadline:
                            # Sanfter Abbruch greift nicht → ganze Prozessgruppe
                            # töten (Kind ist Session-Leader: pgid == pid).
                            log.warning("[TASK] SIGKILL für hängenden Lauf kommune=%s pid=%s",
                                        row.kommune_id, row.worker_pid)
                            try:
                                os.killpg(row.worker_pid, signal.SIGKILL)
                            except (ProcessLookupError, PermissionError):
                                pass
                else:
                    # Prozess starb, ohne seinen Status zu schreiben (SIGKILL/
                    # Kernel-OOM/Crash) → Zeile heilen, mit Exit-Code wenn bekannt.
                    rc = _last_exit.pop(row.kommune_id, None)
                    row.status = AssessmentStatus.ERROR
                    row.message = (
                        f"Berechnung unerwartet beendet (Exit {rc}, evtl. RAM/OOM)"
                        if rc is not None
                        else "Berechnung unterbrochen (Prozess beendet) – bitte neu starten"
                    )
                    row.finished_at = datetime.utcnow()
                    row.worker_pid = None
            else:  # QUEUED
                if alive:
                    # Neustart-Übergang: der ALTE Prozess wickelt noch ab und
                    # belegt den Slot; erst starten, wenn er weg ist.
                    occupied += 1
                else:
                    startable.append(row)

        startable.sort(key=lambda r: r.queued_at or datetime.min)
        slots = max(0, int(settings.ASSESSMENT_MAX_CONCURRENT) - occupied)
        for row in startable[:slots]:
            _spawn(row)
        db.commit()
    finally:
        db.close()


def _spawn(row: ProjectStatus) -> None:
    """Startet den Kind-Prozess und markiert die Zeile sofort als RUNNING.

    Das sofortige Setzen von PID/Ticks im Parent schließt das Fenster, in dem
    ein zweiter Scheduler-Tick dieselbe QUEUED-Zeile noch einmal starten könnte.
    """
    kid = row.kommune_id
    os.makedirs(_LOG_DIR, exist_ok=True)
    log_path = os.path.join(_LOG_DIR, f"worker-{kid}.log")
    with open(log_path, "ab") as log_fh:
        proc = subprocess.Popen(
            [sys.executable, "-m", "app.tasks.assessment_worker", str(kid)],
            cwd=_BACKEND_DIR,
            stdout=log_fh,
            stderr=subprocess.STDOUT,
            start_new_session=True,   # eigene Prozessgruppe: überlebt --reload; killpg möglich
            close_fds=True,
        )
    with _lock:
        _procs[kid] = proc
    row.status = AssessmentStatus.RUNNING
    row.message = "Berechnungsprozess gestartet …"
    row.progress_pct = 0.0
    row.started_at = datetime.utcnow()
    row.finished_at = None
    row.worker_pid = proc.pid
    row.worker_start_ticks = proc_start_ticks(proc.pid)
    row.abort_requested = False
    log.info("[TASK] Assessment-Kindprozess gestartet kommune=%s pid=%s (log: %s)",
             kid, proc.pid, log_path)
