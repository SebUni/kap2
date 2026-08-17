"""Hintergrund-Orchestrator: baut abgeleitete Artefakte nach Mutationen neu.

Ablauf: Mutations-Endpoints rufen ``invalidate_and_schedule()`` →
Debounce-Thread (koalesziert Änderungs-Bursts wie Multi-Parameter-Saves,
``DEBOUNCE_S``) → der eigentliche Rebuild läuft als kurzlebiger KIND-Prozess
(``python -m app.services.artifact_rebuild <kommune_id> …``): Er lädt alle
``CellAssessment``-Blobs, hält also kurzzeitig viel RAM und CPU — beides bleibt
so aus dem API-Prozess draußen (kein GIL-Stau, RAM geht mit Exit ans OS).
Rebuilds laufen strikt seriell (RAM-Budget), weitere Anforderungen sammeln
sich im Pending-Puffer.

Reihenfolge je Kommune in ``rebuild_now``: Aggregate (Basis + mit Maßnahmen →
``aggregate_cache``) → Dashboard-Artefakte (``dashboard_cache``) →
Karten-Layer-Dateien (``layer_cache.precompute``, nur bei ``layers=True`` —
Live-Parameter wie €-Sätze/ref_values backen in die Layer-Werte-Dateien).

Der Zeitplan ist bewusst in-process (bei Reload geht nur der Plan verloren,
nicht die Korrektheit): Die Serving-Pfade bauen bei Miss/Stale lazy nach.
"""

from __future__ import annotations

import logging
import os
import subprocess
import sys
import threading
import time
from typing import Iterable

log = logging.getLogger(__name__)

DEBOUNCE_S = 3.0
_TICK_S = 0.5
_CHILD_TIMEOUT_S = 1800  # Not-Deckel gegen hängende Rebuild-Kinder

_BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_LOG_DIR = os.path.join(_BACKEND_DIR, "logs")

_lock = threading.Lock()
# kommune_id → {"ts": letzte Anforderung, "layers": bool, "artifacts": set | None (= alle)}
_pending: dict[int, dict] = {}
_wake = threading.Event()
_worker_started = False


def ensure_worker_started() -> None:
    """Startet den Debounce-Thread genau einmal (idempotent)."""
    global _worker_started
    with _lock:
        if _worker_started:
            return
        _worker_started = True
    threading.Thread(target=_worker_loop, daemon=True, name="artifact-rebuild").start()
    log.info("[REBUILD] Debounce-Worker gestartet (%.1fs)", DEBOUNCE_S)


def schedule(kommune_id: int, *, layers: bool = False,
             artifacts: Iterable[str] | None = None) -> None:
    """Merkt einen Rebuild vor (entprellt); ``artifacts=None`` = alle."""
    with _lock:
        entry = _pending.setdefault(kommune_id, {"ts": 0.0, "layers": False, "artifacts": set()})
        entry["ts"] = time.monotonic()
        entry["layers"] = entry["layers"] or layers
        if artifacts is None:
            entry["artifacts"] = None
        elif entry["artifacts"] is not None:
            entry["artifacts"].update(artifacts)
    ensure_worker_started()
    _wake.set()


def invalidate_and_schedule(kommune_id: int, *, layers: bool = False,
                            artifacts: Iterable[str] | None = None,
                            only_with_measures: bool = False) -> None:
    """Invalidiert die betroffenen Datei-Caches und plant den Hintergrund-Rebuild.

    ``only_with_measures=True`` für Maßnahmen-Mutationen: das Basis-Aggregat
    hängt nicht von Maßnahmen ab und bleibt gültig (spart den teuersten Teil
    des Rebuilds). ``layers=True``, wenn Layer-Werte-Dateien betroffen sind
    (Live-Parameter). Das Dashboard-Cache braucht kein Invalidate — seine
    Frische entscheidet der Fingerprint.
    """
    from app.services import aggregate_cache, layer_cache

    aggregate_cache.invalidate(kommune_id, only_with_measures=only_with_measures)
    if layers:
        layer_cache.invalidate(kommune_id)
    schedule(kommune_id, layers=layers, artifacts=artifacts)


def rebuild_now(db, kommune_id: int, *, layers: bool = False,
                artifacts: Iterable[str] | None = None) -> None:
    """Synchroner Rebuild im AKTUELLEN Prozess.

    Gedacht für Prozesse, die ohnehin wegwerfbar sind: das Rebuild-Kind
    (``main``) und der Assessment-Kind-Prozess am Ende seines Laufs.
    Invalidiert selbst NICHTS — das erledigen die Mutationspunkte bzw. der
    Assessment-Worker vorab.
    """
    from app.services import dashboard_cache, layer_cache
    from app.services.measure_service import get_risk_aggregate

    t0 = time.monotonic()
    get_risk_aggregate(db, kommune_id, apply_measures=False)
    get_risk_aggregate(db, kommune_id, apply_measures=True)
    dashboard_cache.rebuild(db, kommune_id, artifacts)
    if layers:
        layer_cache.precompute(db, kommune_id)
    log.info("[REBUILD] kommune=%s fertig in %.1fs (layers=%s, artefakte=%s)",
             kommune_id, time.monotonic() - t0, layers,
             ",".join(sorted(artifacts)) if artifacts else "alle")


def _worker_loop() -> None:  # pragma: no cover - Endlosschleife; Kernlogik separat getestet
    while True:
        _wake.wait(timeout=_TICK_S)
        _wake.clear()
        for kommune_id, entry in pop_due(time.monotonic()):
            _run_rebuild_child(kommune_id, entry)


def pop_due(now: float) -> list[tuple[int, dict]]:
    """Entnimmt alle Einträge, deren Debounce-Fenster abgelaufen ist (testbar)."""
    due: list[tuple[int, dict]] = []
    with _lock:
        for kid, entry in list(_pending.items()):
            if now - entry["ts"] >= DEBOUNCE_S:
                due.append((kid, _pending.pop(kid)))
    return due


def _run_rebuild_child(kommune_id: int, entry: dict) -> None:
    """Führt EINEN Rebuild als Kind-Prozess aus (seriell, blockiert nur diesen Thread)."""
    args = [sys.executable, "-m", "app.services.artifact_rebuild", str(kommune_id)]
    if entry.get("layers"):
        args.append("--layers")
    artifacts = entry.get("artifacts")
    if artifacts:
        args += ["--artifacts", ",".join(sorted(artifacts))]
    os.makedirs(_LOG_DIR, exist_ok=True)
    log_path = os.path.join(_LOG_DIR, "artifact-rebuild.log")
    try:
        with open(log_path, "ab") as log_fh:
            proc = subprocess.Popen(
                args, cwd=_BACKEND_DIR, stdout=log_fh, stderr=subprocess.STDOUT,
            )
        try:
            rc = proc.wait(timeout=_CHILD_TIMEOUT_S)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
            log.error("[REBUILD] Kind für kommune=%s nach %ss gekillt", kommune_id, _CHILD_TIMEOUT_S)
            return
        if rc != 0:
            log.error("[REBUILD] Kind für kommune=%s endete mit Exit %s (log: %s)",
                      kommune_id, rc, log_path)
    except Exception:
        log.exception("[REBUILD] Kind-Start fehlgeschlagen kommune=%s", kommune_id)


def main(argv: list[str]) -> int:
    """Kind-Prozess-Entrypoint: ein Rebuild, dann Exit (RAM zurück ans OS)."""
    import argparse

    from app.log_config import setup_logging
    setup_logging()
    parser = argparse.ArgumentParser()
    parser.add_argument("kommune_id", type=int)
    parser.add_argument("--layers", action="store_true")
    parser.add_argument("--artifacts", default="")
    ns = parser.parse_args(argv)
    artifacts = [s for s in ns.artifacts.split(",") if s] or None

    from app.db.database import SessionLocal
    db = SessionLocal()
    try:
        rebuild_now(db, ns.kommune_id, layers=ns.layers, artifacts=artifacts)
        return 0
    except Exception:
        log.exception("[REBUILD] fehlgeschlagen kommune=%s", ns.kommune_id)
        return 1
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
