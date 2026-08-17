"""Gemeinsame Primitiven für die gzip-JSON-Datei-Caches unter ``backend/.cache``.

Genutzt von ``aggregate_cache``, ``layer_cache`` und ``dashboard_cache``.

Race-Härtung (behebt den beobachteten Crash ``FileNotFoundError:
.model_version.tmp``): ``invalidate()`` (rmtree) kann aus einem anderen Thread
ODER Prozess (Assessment-Kind) zwischen ``makedirs`` und dem tmp-Write laufen.
Schreiber legen das Verzeichnis dann einmalig neu an und versuchen es erneut —
danach gewinnt schlicht der letzte Schreiber; das Ergebnis bleibt korrekt, weil
alle Builder deterministisch aus dem DB-Stand bauen. Fehlt nach so einem Rennen
der Versions-Stempel, wird das Verzeichnis beim nächsten Zugriff regulär
invalidiert und lazy neu gebaut.
"""

from __future__ import annotations

import gzip
import json
import logging
import os
import shutil
import threading
import time

log = logging.getLogger(__name__)

_lock = threading.RLock()
_TMP_MAX_AGE_S = 3600  # verwaiste tmp-Dateien abgestürzter Schreiber


def _tmp_path(path: str) -> str:
    return f"{path}.tmp.{os.getpid()}.{threading.get_ident()}"


def write_gzip_json(path: str, obj: dict) -> None:
    """Atomar (tmp + os.replace); übersteht konkurrierendes ``invalidate``."""
    tmp = _tmp_path(path)
    try:
        for attempt in (1, 2):
            try:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with gzip.open(tmp, "wt", encoding="utf-8") as fh:
                    json.dump(obj, fh, separators=(",", ":"))
                os.replace(tmp, path)
                return
            except FileNotFoundError:
                if attempt == 2:
                    raise
    finally:
        try:
            if os.path.exists(tmp):
                os.unlink(tmp)
        except OSError:
            pass


def write_text(path: str, text: str) -> None:
    tmp = _tmp_path(path)
    try:
        for attempt in (1, 2):
            try:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(tmp, "w", encoding="utf-8") as fh:
                    fh.write(text)
                os.replace(tmp, path)
                return
            except FileNotFoundError:
                if attempt == 2:
                    raise
    finally:
        try:
            if os.path.exists(tmp):
                os.unlink(tmp)
        except OSError:
            pass


def read_gzip_json(path: str) -> dict | None:
    """Inhalt oder ``None`` bei Miss/defekter (halb geschriebener) Datei."""
    try:
        with gzip.open(path, "rt", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, EOFError, json.JSONDecodeError):
        return None


def read_text(path: str) -> str | None:
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read().strip()
    except OSError:
        return None


def cleanup_stale_tmp(cache_dir: str) -> None:
    """Verwaiste ``*.tmp*``-Dateien (> 1 h) entfernen."""
    try:
        names = os.listdir(cache_dir)
    except OSError:
        return
    now = time.time()
    for name in names:
        if ".tmp" not in name:
            continue
        p = os.path.join(cache_dir, name)
        try:
            if now - os.path.getmtime(p) > _TMP_MAX_AGE_S:
                os.unlink(p)
        except OSError:
            pass


def ensure_version_stamp(cache_dir: str, current: str, stamp_name: str = ".model_version") -> None:
    """Leert ``cache_dir``, wenn der Stempel nicht ``current`` ist, und stempelt neu.

    Threadsicher über das Modul-Lock; die Cross-Prozess-Race deckt der
    Retry in ``write_text`` ab.
    """
    with _lock:
        vpath = os.path.join(cache_dir, stamp_name)
        if read_text(vpath) == current:
            cleanup_stale_tmp(cache_dir)
            return
        shutil.rmtree(cache_dir, ignore_errors=True)
        write_text(vpath, current)


def invalidate_dir(cache_dir: str) -> None:
    with _lock:
        shutil.rmtree(cache_dir, ignore_errors=True)
