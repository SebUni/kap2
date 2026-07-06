"""Datei-Cache für das aggregierte Risiko-/Kostenergebnis je Kommune.

``get_risk_aggregate`` lädt sämtliche ``CellAssessment``-Zeilen (tausende fette
JSON-Blobs) und lässt die Engine darüber aggregieren — pro Dashboard-Aufruf
geschieht das mehrfach (risk-summary, cost-summary, risk-histogram-Kontext,
cost-projection nutzen dasselbe Aggregat mit/ohne Maßnahmen). Dieser Cache
materialisiert das Ergebnis je ``(kommune_id, apply_measures)`` einmal als
gzip-JSON und liefert es danach als reines I/O — analog zu ``layer_cache``.

Invalidiert wird explizit an allen Mutationspunkten (neue Berechnung, Maßnahmen-,
Config-/Parameter-Änderung, Reset, Grid-Neubau) sowie automatisch bei einer
Änderung von ``catalog.MODEL_VERSION`` (Kostensätze/Modelllogik).
"""

from __future__ import annotations

import gzip
import json
import logging
import os
import shutil

from app.data import catalog

log = logging.getLogger(__name__)

_CACHE_BASE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    ".cache",
    "aggregates",
)


# ── Pfade ──────────────────────────────────────────────────────────────────────

def _cache_dir(kommune_id: int) -> str:
    return os.path.join(_CACHE_BASE, str(kommune_id))


def _agg_path(kommune_id: int, apply_measures: bool) -> str:
    variant = "withmeasures" if apply_measures else "base"
    return os.path.join(_cache_dir(kommune_id), f"aggregate_{variant}.json.gz")


def _version_path(kommune_id: int) -> str:
    return os.path.join(_cache_dir(kommune_id), ".model_version")


def _ensure_model_version(kommune_id: int) -> None:
    """Leert den Cache, wenn er unter einer alten Modellversion gebaut wurde."""
    vpath = _version_path(kommune_id)
    current = catalog.MODEL_VERSION
    stored = None
    if os.path.exists(vpath):
        try:
            with open(vpath, encoding="utf-8") as fh:
                stored = fh.read().strip()
        except OSError:
            stored = None
    if stored == current:
        return
    invalidate(kommune_id)
    os.makedirs(_cache_dir(kommune_id), exist_ok=True)
    tmp = vpath + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(current)
    os.replace(tmp, vpath)


# ── Öffentliche API ──────────────────────────────────────────────────────────────

def load(kommune_id: int, apply_measures: bool) -> dict | None:
    """Zwischengespeichertes Aggregat oder ``None`` bei Miss/defektem Cache."""
    _ensure_model_version(kommune_id)
    path = _agg_path(kommune_id, apply_measures)
    if not os.path.exists(path):
        return None
    try:
        with gzip.open(path, "rt", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        # Defekte/halb geschriebene Datei: als Miss behandeln, wird neu gebaut.
        return None


def store(kommune_id: int, apply_measures: bool, result: dict) -> None:
    """Aggregat atomar als gzip-JSON ablegen (best effort)."""
    _ensure_model_version(kommune_id)
    path = _agg_path(kommune_id, apply_measures)
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = path + ".tmp"
        with gzip.open(tmp, "wt", encoding="utf-8") as fh:
            json.dump(result, fh, separators=(",", ":"))
        os.replace(tmp, path)
    except OSError as exc:
        log.debug("aggregate_cache store übersprungen kommune=%s: %s", kommune_id, exc)


def invalidate(kommune_id: int) -> None:
    """Verwirft das Aggregat-Cache-Verzeichnis der Kommune (beide Varianten)."""
    shutil.rmtree(_cache_dir(kommune_id), ignore_errors=True)
