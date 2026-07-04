"""Datei-Cache fuer Karten-Layer (gzip-JSON auf Platte).

Trennt die statische Zellgeometrie von den je Layer wechselnden Werten. Beide
werden als fertige gzip-Dateien geschrieben und danach reines I/O gestreamt
(kaum RAM, kein DB-Rebuild pro Layer-Klick).

- ``geometry.json.gz``  : FeatureCollection nur mit grid_cell_id + Geometrie.
- ``layer_<code>.json.gz``: pro Zelle value/index + Inspektor-Detailfelder
  (ohne Geometrie) plus ``meta`` (min/max/label/unit/recipe).

Fehlt eine Datei (erster Zugriff, nach Neustart, nach Invalidierung), wird sie
einmalig aus der DB gebaut und geschrieben (Lazy-Build).
"""

from __future__ import annotations

import gzip
import json
import logging
import os
import shutil

from geoalchemy2.shape import to_shape
from shapely.geometry import mapping
from sqlalchemy.orm import Session

from app.data import catalog
from app.models.models import CellAssessment, GridCell, Kommune
from app.services.engine import formulas, risk_engine
from app.services.engine.inputs import build_regional_context
from app.services.engine.runner import COASTAL_BUNDESLAENDER

log = logging.getLogger(__name__)

_CACHE_BASE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    ".cache",
    "layers",
)


# ── Pfade ──────────────────────────────────────────────────────────────────────

def _cache_dir(kommune_id: int) -> str:
    return os.path.join(_CACHE_BASE, str(kommune_id))


def _geometry_path(kommune_id: int) -> str:
    return os.path.join(_cache_dir(kommune_id), "geometry.json.gz")


def _values_path(kommune_id: int, code: str) -> str:
    return os.path.join(_cache_dir(kommune_id), f"layer_{code}.json.gz")


def layer_category(code: str) -> str | None:
    if code in catalog.HAZARDS_BY_CODE:
        return "hazards"
    if code in catalog.EXPOSURES_BY_CODE:
        return "exposures"
    if code in catalog.VULNERABILITIES_BY_CODE:
        return "vulnerabilities"
    if code in catalog.AUXILIARY_BY_CODE:
        return "auxiliary"
    if code in catalog.RISKS_BY_CODE:
        return "risks"
    return None


# ── Schreiben ──────────────────────────────────────────────────────────────────

def _write_gzip_json(path: str, obj: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with gzip.open(tmp, "wt", encoding="utf-8") as fh:
        json.dump(obj, fh, separators=(",", ":"))
    os.replace(tmp, path)


# ── Builder ────────────────────────────────────────────────────────────────────

def _build_geometry_package(db: Session, kommune_id: int) -> dict:
    cells = db.query(GridCell).filter(GridCell.kommune_id == kommune_id).all()
    features = []
    for cell in cells:
        features.append({
            "type": "Feature",
            "properties": {
                "grid_cell_id": cell.id,
                "gitter_id": cell.gitter_id,
                "row": cell.row_idx,
                "col": cell.col_idx,
            },
            "geometry": mapping(to_shape(cell.geometry)),
        })
    return {"type": "FeatureCollection", "features": features}


def _regional_for(kommune: Kommune) -> dict:
    is_coastal = (kommune.bundesland or "") in COASTAL_BUNDESLAENDER
    centroid = None
    if kommune.boundary is not None:
        try:
            c = to_shape(kommune.boundary).centroid
            centroid = (c.x, c.y)
        except Exception:
            centroid = None
    return build_regional_context(
        kommune.bundesland, is_coastal, kommune.osm_id, centroid,
    )


def _build_values_package(rows, regional: dict, code: str, category: str) -> dict:
    """Baut das Werte-Paket (ohne Geometrie) aus vorgeladenen CellAssessment-Zeilen."""
    recipe = formulas.recipe_for_layer(code, category)
    cells_out: list[dict] = []
    vmin, vmax = None, None

    for ca in rows:
        data = ca.data or {}
        props: dict = {"grid_cell_id": ca.grid_cell_id}
        if category == "risks":
            rdef = catalog.RISKS_BY_CODE[code]
            idx = float(data.get("risks", {}).get(code, {}).get("index", 0.0))
            cell_pop = float(data.get("inputs", {}).get("pop", 0.0))
            value = risk_engine.cell_outcome(rdef, idx, cell_pop)
            hev_abs = {
                "hazards": data.get("hazards", {}),
                "exposures": data.get("exposures", {}),
                "vulnerabilities": data.get("vulnerabilities", {}),
            }
            hev_norm = risk_engine.normalize_hev(hev_abs)
            breakdown = formulas.risk_cell_breakdown(rdef, hev_abs, hev_norm)
            props["index"] = round(idx, 2)
            props["H"] = breakdown["H"]
            props["E"] = breakdown["E"]
            props["V"] = breakdown["V"]
            props["outcome"] = risk_engine.cell_outcome_breakdown(rdef, idx, cell_pop)
            props["pathways"] = formulas.risk_pathway_cell_breakdown(rdef, hev_norm)
        else:
            raw = data.get(category, {}).get(code)
            if raw is None:
                continue
            value = float(raw)
            ci = data.get("inputs", {})
            props["inputs"] = formulas.resolve_inputs(recipe, ci, regional, data)
        vmin = value if vmin is None else min(vmin, value)
        vmax = value if vmax is None else max(vmax, value)
        props["value"] = round(value, 3)
        cells_out.append(props)

    meta = {"code": code, "category": category, "min": vmin or 0.0, "max": vmax or 0.0, "recipe": recipe}
    if category == "risks":
        r = catalog.RISKS_BY_CODE[code]
        meta.update({"label": r["name"], "unit": r["outcome_unit"]})
    else:
        m = catalog.INDICATOR_BY_CODE[code]
        meta.update({"label": m["name"], "unit": m["unit"]})

    return {"cells": cells_out, "meta": meta}


# ── Oeffentliche API: Datei-Zugriff mit Lazy-Build ───────────────────────────────

def geometry_file(db: Session, kommune_id: int) -> str | None:
    """Pfad zur gzip-Geometriedatei; baut sie bei Bedarf. None, wenn keine Zellen."""
    path = _geometry_path(kommune_id)
    if os.path.exists(path):
        return path
    pkg = _build_geometry_package(db, kommune_id)
    if not pkg["features"]:
        return None
    _write_gzip_json(path, pkg)
    return path


def values_file(db: Session, kommune_id: int, code: str) -> str | None:
    """Pfad zur gzip-Werte-Datei; baut sie bei Bedarf. None bei unbekanntem Code."""
    category = layer_category(code)
    if not category:
        return None
    path = _values_path(kommune_id, code)
    if os.path.exists(path):
        return path
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        return None
    rows = db.query(CellAssessment).filter(CellAssessment.kommune_id == kommune_id).all()
    regional = _regional_for(kommune)
    pkg = _build_values_package(rows, regional, code, category)
    _write_gzip_json(path, pkg)
    return path


def precompute(db: Session, kommune_id: int) -> None:
    """Schreibt Geometrie + alle Layer-Werte-Dateien in einem Rutsch (nach Berechnung)."""
    try:
        kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
        if not kommune:
            return
        geom = _build_geometry_package(db, kommune_id)
        if not geom["features"]:
            return
        _write_gzip_json(_geometry_path(kommune_id), geom)

        rows = db.query(CellAssessment).filter(CellAssessment.kommune_id == kommune_id).all()
        if not rows:
            return
        regional = _regional_for(kommune)
        codes = list(catalog.INDICATOR_BY_CODE.keys()) + list(catalog.RISKS_BY_CODE.keys())
        for code in codes:
            category = layer_category(code)
            if not category:
                continue
            try:
                pkg = _build_values_package(rows, regional, code, category)
                _write_gzip_json(_values_path(kommune_id, code), pkg)
            except Exception:
                log.exception("layer_cache precompute failed kommune=%s code=%s", kommune_id, code)
        log.info("[layer_cache] precompute done kommune=%s (%d codes)", kommune_id, len(codes))
    except Exception:
        log.exception("layer_cache precompute failed kommune=%s", kommune_id)


def invalidate(kommune_id: int) -> None:
    """Loescht das Cache-Verzeichnis der Kommune."""
    shutil.rmtree(_cache_dir(kommune_id), ignore_errors=True)
