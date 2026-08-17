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

import logging
import os

from app.data import catalog
from app.services import file_cache

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
    file_cache.ensure_version_stamp(_cache_dir(kommune_id), catalog.MODEL_VERSION)


# ── Öffentliche API ──────────────────────────────────────────────────────────────

def load(kommune_id: int, apply_measures: bool) -> dict | None:
    """Zwischengespeichertes Aggregat oder ``None`` bei Miss/defektem Cache."""
    _ensure_model_version(kommune_id)
    return file_cache.read_gzip_json(_agg_path(kommune_id, apply_measures))


def store(kommune_id: int, apply_measures: bool, result: dict) -> None:
    """Aggregat atomar als gzip-JSON ablegen (best effort)."""
    _ensure_model_version(kommune_id)
    try:
        file_cache.write_gzip_json(_agg_path(kommune_id, apply_measures), result)
    except OSError as exc:
        log.debug("aggregate_cache store übersprungen kommune=%s: %s", kommune_id, exc)


def invalidate(kommune_id: int, *, only_with_measures: bool = False) -> None:
    """Verwirft den Aggregat-Cache der Kommune.

    ``only_with_measures=True`` löscht nur die „mit Maßnahmen"-Variante:
    Maßnahmen-Mutationen lassen das (teure) Basis-Aggregat unberührt.
    """
    if only_with_measures:
        try:
            os.unlink(_agg_path(kommune_id, apply_measures=True))
        except OSError:
            pass
        return
    file_cache.invalidate_dir(_cache_dir(kommune_id))
