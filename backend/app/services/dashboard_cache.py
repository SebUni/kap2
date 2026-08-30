"""Datei-Cache für die Dashboard-Payloads je Kommune (gzip-JSON auf Platte).

Ergänzt ``layer_cache`` (Karten) und ``aggregate_cache`` (Roh-Aggregate) um die
fünf Dashboard-Endpoints: ``risk_summary``, ``cost_summary``,
``risk_histogram``, ``cost_projection``, ``profile``. Der Rebuild läuft im
Hintergrund (``artifact_rebuild`` bzw. der Assessment-Kind-Prozess); die
Endpoints liefern reines Datei-I/O mit ETag/304 — kein Voll-Scan der
``CellAssessment``-Blobs pro Request mehr.

Frische über einen FINGERPRINT des relevanten DB-Stands statt blindem Löschen:
``MODEL_VERSION`` + Zellen-Stand (max(calculated_at) + Anzahl) + Maßnahmen
(id, Typ, config, Jahr — Geometrie ist per Update unveränderbar) + alle
Parameter-Overrides + Kommune-Stammdaten; für ``profile``/``cost_projection``
zusätzlich ein Wochen-Bucket (extern bezogene DWD-/Finanzwerte altern so
kontrolliert). Gleiche Daten ⇒ gleicher Fingerprint ⇒ kein Rebuild und ein
stabiles ETag (304 ohne Datei-Zugriff).
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
from datetime import datetime
from typing import Iterable

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.data import catalog
from app.models.models import AdaptationMeasure, CellAssessment, ConfigParameter, Kommune
from app.services import file_cache

log = logging.getLogger(__name__)

ARTIFACTS: tuple[str, ...] = (
    "risk_summary", "cost_summary", "risk_histogram", "cost_projection", "profile",
)

# Artefakte mit extern bezogenen Werten (DWD-Raster, GENESIS-Finanzdaten):
# Wochen-Bucket im Fingerprint erzwingt einen frischen Build spätestens nach
# einer Woche, ohne dass eine Mutation nötig wäre.
_WEEKLY_ARTIFACTS = frozenset({"profile", "cost_projection"})

# Schema-Version des ``profile``-Payloads: bei Struktur-/Feldänderungen erhöhen,
# damit sich der ETag ändert und Browser NICHT per 304 den alten Body behalten
# (der Eingabe-Fingerprint allein erfasst extern bezogene Felder wie BIP/Haushalt
# nicht). v2: economy.estimated_municipal_eur / gdp_per_capita_eur + Haushalt-Chip.
# v3: LoD2-Gebäudehöhen + Horizontwinkel-SVF (Provenance-Felder building_height/svf).
# v4: Zell-Sommertemperatur aus den DWD-Monatsrastern + Wärmeinsel-Tagesmittel +
#     Zensus-Altersbänder — alles extern bezogene Felder, die der Eingabe-
#     Fingerprint nicht erfasst.
_PROFILE_SCHEMA_VERSION = 5

_CACHE_BASE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    ".cache",
    "dashboard",
)


def _cache_dir(kommune_id: int) -> str:
    return os.path.join(_CACHE_BASE, str(kommune_id))


def _artifact_path(kommune_id: int, name: str) -> str:
    return os.path.join(_cache_dir(kommune_id), f"{name}.json.gz")


# ── Fingerprint ────────────────────────────────────────────────────────────────

def fingerprint_payload(db: Session, kommune_id: int) -> dict:
    """Sammelt den rebuild-relevanten DB-Stand (Basis für Hash + Tests)."""
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    cells_max, cells_count = (
        db.query(func.max(CellAssessment.calculated_at), func.count(CellAssessment.id))
        .filter(CellAssessment.kommune_id == kommune_id)
        .one()
    )
    measures = [
        (m.id, m.measure_type, json.dumps(m.config or {}, sort_keys=True),
         m.implementation_year)
        for m in db.query(AdaptationMeasure)
        .filter(AdaptationMeasure.kommune_id == kommune_id)
        .order_by(AdaptationMeasure.id)
    ]
    params = [
        (p.parameter_id or f"{p.category}.{p.key}", json.dumps(p.value, sort_keys=True))
        for p in db.query(ConfigParameter)
        .filter(ConfigParameter.kommune_id == kommune_id)
        .order_by(ConfigParameter.category, ConfigParameter.key)
    ]
    return {
        "model_version": catalog.MODEL_VERSION,
        "cells": [str(cells_max), int(cells_count or 0)],
        "measures": measures,
        "params": params,
        "kommune": [
            kommune.population if kommune else None,
            kommune.area_km2 if kommune else None,
            kommune.bundesland if kommune else None,
            kommune.landkreis if kommune else None,
            kommune.osm_id if kommune else None,
        ],
    }


def fingerprint_hash(payload: dict, extra: object = None) -> str:
    """Deterministischer Hash über das Payload (reine Funktion, testbar)."""
    blob = json.dumps([payload, extra], sort_keys=True, default=str)
    return hashlib.sha1(blob.encode("utf-8")).hexdigest()


def fingerprint(db: Session, kommune_id: int, name: str) -> str:
    payload = fingerprint_payload(db, kommune_id)
    extra = None
    if name in _WEEKLY_ARTIFACTS:
        iso = datetime.utcnow().isocalendar()
        extra = f"week:{iso[0]}-{iso[1]}"
    if name == "profile":
        # Schema-Version + Budget-Store-Stand in den ETag ziehen, damit ein neuer
        # Bulk-Import (oder ein geändertes Profil-Schema) Browser-Caches invalidiert.
        extra = f"{extra or ''}|schema:{_PROFILE_SCHEMA_VERSION}|budget:{_budget_store_mtime()}"
    return fingerprint_hash(payload, extra)


def _budget_store_mtime() -> int:
    """mtime des Kommunalhaushalt-Bulk-Stores (0, wenn nicht vorhanden) — Teil des
    Profil-Fingerprints, damit ein Import den Chip in den Dashboards erneuert."""
    try:
        from app.services.finance_bulk import _STORE_PATH
        return int(os.path.getmtime(_STORE_PATH))
    except OSError:
        return 0


def etag_for(fp: str) -> str:
    return f'"da-{fp}"'


# ── Builder ────────────────────────────────────────────────────────────────────

def _build_risk_histogram(db: Session, kommune_id: int) -> dict:
    """Häufigkeitsverteilung der Risiko-Index-Höhen je Risiko (20 Bins à 5).

    Streamt die Zell-Blobs (``yield_per``) statt alle Zeilen zu materialisieren.
    """
    from app.services.measure_service import get_risk_aggregate

    n_bins = 20
    width = 5.0  # 0..100
    bin_labels = [f"{int(i * width)}-{int((i + 1) * width)}" for i in range(n_bins)]
    bin_centers = [round((i + 0.5) * width, 1) for i in range(n_bins)]

    counts: dict[str, list[int]] = {r["code"]: [0] * n_bins for r in catalog.RISKS}
    nonzero: dict[str, int] = {r["code"]: 0 for r in catalog.RISKS}
    total_cells = 0
    for (data,) in (
        db.query(CellAssessment.data)
        .filter(CellAssessment.kommune_id == kommune_id)
        .yield_per(500)
    ):
        total_cells += 1
        risks = (data or {}).get("risks", {})
        for code, r in risks.items():
            if code not in counts:
                continue
            idx = float(r.get("index", 0.0))
            b = min(n_bins - 1, max(0, int(idx // width)))
            counts[code][b] += 1
            if idx > 0.0:
                nonzero[code] += 1

    # Outcome/Index-Kennzahlen aus dem Aggregat (Basis, ohne Maßnahmen)
    agg = get_risk_aggregate(db, kommune_id, apply_measures=False)

    risks_out: dict[str, dict] = {}
    for risk in catalog.RISKS:
        code = risk["code"]
        a = agg["risks"].get(code, {})
        risks_out[code] = {
            "name": risk["name"],
            "group": risk["group"],
            "outcome_unit": risk["outcome_unit"],
            "cost_dimension": risk["cost_dimension"],
            "counts": counts[code],
            "nonzero_cells": nonzero[code],
            "p90_index": a.get("index", 0.0),
            "max_index": a.get("max_index", 0.0),
            "outcome": a.get("outcome", 0.0),
            "outcome_sum": a.get("outcome_sum", 0.0),
            "cost_eur": a.get("cost_eur", 0.0),
            # Schicht-B-Aggregationskennzahlen (Σ über Zellen vs. P90; Konzentration/Fläche)
            "aggregation": a.get("aggregation", "sum"),
            "top5_share": a.get("top5_share", 0.0),
            "area_km2_affected": a.get("area_km2_affected", 0.0),
            "share_above_threshold": a.get("share_above_threshold", 0.0),
            # Plausibilitätsanker (Σ/ref_value-Schätzung); Anzeige folgt in Prompt 7.
            "sanity_ratio": a.get("sanity_ratio"),
        }

    return {
        "total_cells": total_cells,
        "bin_labels": bin_labels,
        "bin_centers": bin_centers,
        "bin_width": width,
        "risks": risks_out,
    }


def _build(db: Session, kommune_id: int, name: str) -> dict | None:
    if name == "risk_summary":
        from app.services.measure_service import get_risk_aggregate
        return get_risk_aggregate(db, kommune_id, apply_measures=False)
    if name == "cost_summary":
        from app.services.measure_service import build_cost_summary
        return build_cost_summary(db, kommune_id)
    if name == "risk_histogram":
        return _build_risk_histogram(db, kommune_id)
    if name == "cost_projection":
        from app.services.cost_projection_service import project_costs
        kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
        if not kommune:
            return None
        return project_costs(db, kommune_id, kommune.bundesland or "Sachsen")
    if name == "profile":
        from app.services import finance_loader, kommune_profile_service
        kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
        if not kommune:
            return None
        finance = None
        try:
            finance = finance_loader.finance_for_kommune(kommune.osm_id, kommune.name)
        except Exception:
            log.exception("dashboard_cache: finance_loader fehlgeschlagen kommune=%s", kommune_id)
        return kommune_profile_service.build_profile(db, kommune, finance=finance)
    return None


# ── Öffentliche API ────────────────────────────────────────────────────────────

def artifact_file(db: Session, kommune_id: int, name: str) -> tuple[str, str] | None:
    """(Pfad, ETag) des frischen Artefakts; baut lazy bei Miss/Stale.

    ``None`` bei unbekanntem Namen oder wenn der Builder nichts liefert
    (z. B. Kommune fehlt).
    """
    if name not in ARTIFACTS:
        return None
    fp = fingerprint(db, kommune_id, name)
    path = _artifact_path(kommune_id, name)
    fp_path = path + ".fp"
    if os.path.exists(path) and file_cache.read_text(fp_path) == fp:
        return path, etag_for(fp)
    payload = _build(db, kommune_id, name)
    if payload is None:
        return None
    file_cache.write_gzip_json(path, payload)
    file_cache.write_text(fp_path, fp)
    log.info("[dashboard_cache] gebaut kommune=%s artefakt=%s", kommune_id, name)
    return path, etag_for(fp)


def current_etag(db: Session, kommune_id: int, name: str) -> str:
    return etag_for(fingerprint(db, kommune_id, name))


def rebuild(db: Session, kommune_id: int, names: Iterable[str] | None = None) -> None:
    """Baut (nur) veraltete Artefakte neu — Frische entscheidet der Fingerprint."""
    for name in (names or ARTIFACTS):
        if name not in ARTIFACTS:
            continue
        try:
            artifact_file(db, kommune_id, name)
        except Exception:
            log.exception("dashboard_cache rebuild fehlgeschlagen kommune=%s artefakt=%s",
                          kommune_id, name)


def invalidate(kommune_id: int) -> None:
    """Verwirft das Dashboard-Cache-Verzeichnis der Kommune komplett."""
    file_cache.invalidate_dir(_cache_dir(kommune_id))
