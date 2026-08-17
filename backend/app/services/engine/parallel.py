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
"""

from __future__ import annotations

import gc
import multiprocessing
import os
from contextlib import contextmanager

from app.config import settings

_MP = multiprocessing.get_context("fork")


def n_workers() -> int:
    """Worker-Anzahl für die Rechen-Pools (Setting, sonst min(4, CPU))."""
    configured = int(getattr(settings, "ASSESSMENT_WORKERS", 0) or 0)
    if configured > 0:
        return configured
    return min(4, os.cpu_count() or 4)


def _worker_init() -> None:  # pragma: no cover - läuft im Fork-Kind
    gc.disable()
    try:
        from app.db.database import engine
        # Post-Fork-Härtung (SQLAlchemy-Doku): geerbte Verbindungen verwerfen,
        # ohne sie zu schließen (sie gehören dem Elternprozess).
        engine.dispose(close=False)
    except Exception:
        pass


@contextmanager
def cow_pool(processes: int | None = None):
    """Fork-Pool, der die COW-Seiten des Eltern-Heaps möglichst wenig anfasst."""
    gc.collect()
    gc.freeze()
    try:
        with _MP.Pool(processes or n_workers(), initializer=_worker_init) as pool:
            yield pool
    finally:
        gc.unfreeze()
