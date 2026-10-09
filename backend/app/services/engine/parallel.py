"""Gemeinsame Fork-Pool-Konfiguration mit RAM-Schonung (Copy-on-Write).

Warum: Die Rechenphasen legen große, read-only Datenstrukturen (Shapely-
Geometrien, STRtrees, Zell-Dicts) in Modul-Globals und forken dann Worker.
Copy-on-Write sollte das billig teilen — aber CPythons Refcounting und der
GC beschreiben die Objekt-Header, wodurch die Seiten je Worker doch kopiert
werden. Gegenmaßnahmen hier:

- ``n_workers()``: Worker-Anzahl zentral, per ``ASSESSMENT_WORKERS``
  konfigurierbar; Default ``min(4, CPU)`` statt bisher ``min(8, CPU)`` —
  halbiert den COW-Peak bei ~20–30 % längerer Laufzeit.
- ``cow_pool()``: ``gc.freeze()`` vor dem Fork verschiebt alle bestehenden
  Objekte in die permanente GC-Generation, sodass GC-Läufe in den Workern
  deren Header nicht mehr anfassen; im Worker wird der GC ganz deaktiviert
  (kurzlebige Prozesse, kein Zyklen-Risiko) und die geerbte SQLAlchemy-
  Engine entsorgt (Worker nutzen die DB nie; geerbte Sockets wären UB).

Warum ``ProcessPoolExecutor`` statt ``multiprocessing.Pool`` (T-1953-cto): Stirbt ein
Kind von ``multiprocessing.Pool`` (``os._exit``, OOM-Killer, Signal), ersetzt der Pool
es und wartet mit ``imap_unordered`` unbegrenzt auf das verlorene Ergebnis — die
Bewertung bleibt scheinbar stehen. Der Executor erkennt den toten Worker und wirft
``BrokenProcessPool``; ``map_unordered`` macht daraus ``RechenWorkerBeendet`` mit
verständlicher Meldung. Der Assessment-Worker schreibt sie als Status ``error``.
"""

from __future__ import annotations

import gc
import multiprocessing
import os
import signal
from concurrent.futures import ProcessPoolExecutor, as_completed
from concurrent.futures.process import BrokenProcessPool
from contextlib import contextmanager
from typing import Any, Callable, Iterable, Iterator

from app.config import settings

_MP = multiprocessing.get_context("fork")


def n_workers() -> int:
    """Worker-Anzahl für die Rechen-Pools (Setting, sonst min(4, CPU))."""
    configured = int(getattr(settings, "ASSESSMENT_WORKERS", 0) or 0)
    if configured > 0:
        return configured
    return min(4, os.cpu_count() or 4)


def _worker_init() -> None:  # pragma: no cover - läuft im Fork-Kind
    # Der Elternprozess (assessment_worker) fängt SIGTERM ab und setzt nur ein Abbruch-
    # Flag; geerbt würde das Kind SIGTERM überleben und der Aufräumschritt nach einem
    # Fehler (``Process.terminate`` + ``join``) hinge. Im Kind gilt wieder das Standard-Ende.
    signal.signal(signal.SIGTERM, signal.SIG_DFL)
    gc.disable()
    try:
        from app.db.database import engine
        # Post-Fork-Härtung (SQLAlchemy-Doku): geerbte Verbindungen verwerfen,
        # ohne sie zu schließen (sie gehören dem Elternprozess).
        engine.dispose(close=False)
    except Exception:
        pass


class RechenWorkerBeendet(BrokenProcessPool):
    """Ein Prozess des Rechen-Pools wurde unerwartet beendet (kein Python-Fehler)."""


def _run_chunk(func: Callable[[Any], Any], items: list) -> list:  # pragma: no cover - Fork-Kind
    return [func(i) for i in items]


def _exitcodes(executor: ProcessPoolExecutor) -> list[int]:
    """Exit-Status der Worker, soweit lesbar (best effort; SIGTERM vom Aufräumen ausgenommen)."""
    codes: set[int] = set()
    try:
        for proc in list((getattr(executor, "_processes", None) or {}).values()):
            code = proc.exitcode
            if code is not None and code != -signal.SIGTERM:
                codes.add(code)
    except Exception:  # noqa: BLE001 - nur Diagnose
        pass
    return sorted(codes)


class RechenPool:
    """Schmale Hülle um den Executor: ``map_unordered`` statt ``imap_unordered``."""

    def __init__(self, executor: ProcessPoolExecutor):
        self._executor = executor

    def map_unordered(self, func: Callable[[Any], Any], iterable: Iterable,
                      chunksize: int = 1) -> Iterator[Any]:
        """Wie ``Pool.imap_unordered``: Ergebnisse in Fertigstellungs-Reihenfolge.

        Ein Python-Fehler im Worker wird unverändert weitergereicht. Stirbt ein Worker
        ohne Python-Fehler, endet der Aufruf mit ``RechenWorkerBeendet`` statt zu hängen.
        """
        items = list(iterable)
        size = max(1, int(chunksize))
        futures = [
            self._executor.submit(_run_chunk, func, items[start:start + size])
            for start in range(0, len(items), size)
        ]
        try:
            for fut in as_completed(futures):
                yield from fut.result()
        except BrokenProcessPool as exc:
            codes = _exitcodes(self._executor)
            status = f" (Exit-Status {', '.join(str(c) for c in codes)})" if codes else ""
            raise RechenWorkerBeendet(
                "Rechen-Worker unerwartet beendet" + status + " in Stufe "
                f"{getattr(func, '__name__', func)}: ein Prozess des Rechen-Pools endete, "
                "ohne ein Ergebnis zu liefern (z. B. Speichermangel oder Signal). "
                "Die Berechnung wurde abgebrochen."
            ) from exc
        finally:
            for fut in futures:
                fut.cancel()


def _stop(executor: ProcessPoolExecutor, hart: bool) -> None:
    """Executor beenden; nach einem Fehler laufende Worker beenden (wie ``Pool.terminate``)."""
    if hart:
        # Prozessliste vor ``shutdown`` sichern: der Executor setzt sie danach auf None.
        prozesse = list((getattr(executor, "_processes", None) or {}).values())
        executor.shutdown(wait=False, cancel_futures=True)
        for proc in prozesse:
            try:
                proc.terminate()
            except Exception:  # noqa: BLE001
                pass
    executor.shutdown(wait=True, cancel_futures=hart)


@contextmanager
def cow_pool(processes: int | None = None):
    """Fork-Pool, der die COW-Seiten des Eltern-Heaps möglichst wenig anfasst.

    Liefert einen ``RechenPool``; Ergebnisse über ``pool.map_unordered(...)``.
    """
    gc.collect()
    gc.freeze()
    executor = ProcessPoolExecutor(
        max_workers=processes or n_workers(), mp_context=_MP, initializer=_worker_init)
    ok = False
    try:
        yield RechenPool(executor)
        ok = True
    finally:
        try:
            _stop(executor, hart=not ok)
        finally:
            gc.unfreeze()
