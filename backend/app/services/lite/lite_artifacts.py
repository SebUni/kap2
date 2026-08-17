"""Statische Artefakte der Deutschland-Karte: values.json, meta.json, GeoJSON.

Öffentliche Endpunkte liefern nur diese Dateien aus (billig). PMTiles via
tippecanoe ist optional; fehlt das Tool, werden GeoJSON-Dateien je Bundesland
geschrieben (Fallback, Plan §4G).
"""
from __future__ import annotations

import gzip
import json
import logging
import os

from sqlalchemy.orm import Session

from app.config import settings
from app.data import catalog
from app.data import sources
from app.models.lite_models import Gemeinde, GemeindeLiteResult
from app.services.lite.lite_scoring import LITE_RISK_CODES

log = logging.getLogger(__name__)


def _out(name: str) -> str:
    return os.path.join(settings.LITE_DATA_DIR, name)


def write_values(db: Session) -> str:
    """``values.json``: {ags: {RISK_CODE: index, ...}} — klein, gzip, ETag-fähig."""
    os.makedirs(settings.LITE_DATA_DIR, exist_ok=True)
    values: dict[str, dict[str, float]] = {}
    for r in db.query(GemeindeLiteResult).all():
        values.setdefault(r.ags, {})[r.risk_code] = r.index_value
    path = _out("values.json.gz")
    with gzip.open(path, "wt", encoding="utf-8") as fh:
        json.dump(values, fh, separators=(",", ":"))
    log.info("values.json.gz: %d Gemeinden", len(values))
    return path


def write_meta(db: Session) -> str:
    """``meta.json``: Risiko-Metadaten + Legenden für das Frontend."""
    risks = []
    for code in LITE_RISK_CODES:
        r = catalog.RISKS_BY_CODE[code]
        risks.append({
            "code": code,
            "name": r["name"],
            "group": r.get("group"),
            "unit": r.get("outcome_unit", ""),
            "description": r.get("description", ""),
            "source_refs": sources.resolve(r.get("source_refs")),
        })
    stand = db.query(Gemeinde.vg250_stand).first()
    meta = {
        "risks": risks,
        "gemeinde_count": db.query(Gemeinde).count(),
        "vg250_stand": stand[0] if stand else None,
        "choropleth_colors": ["#fef9c3", "#fde047", "#fb923c", "#ef4444", "#991b1b"],
    }
    path = _out("meta.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False)
    return path


def write_geojson(db: Session) -> list[str]:
    """Gemeinde-Polygone (vereinfacht) je Bundesland als gzip-GeoJSON (Fallback
    ohne tippecanoe). Eigenschaft ``ags`` je Feature für Feature-State-Färbung."""
    by_bl: dict[str, list] = {}
    for g in db.query(Gemeinde).all():
        if not g.geometry_simplified:
            continue
        feat = {
            "type": "Feature",
            "id": int(g.ags),
            "properties": {"ags": g.ags, "name": g.name, "bl": g.bundesland},
            "geometry": json.loads(g.geometry_simplified),
        }
        by_bl.setdefault(g.bundesland or "unbekannt", []).append(feat)
    os.makedirs(_out("geojson"), exist_ok=True)
    paths = []
    index = {}
    for bl, feats in by_bl.items():
        slug = bl.lower().replace(" ", "-").replace("ü", "ue").replace("ö", "oe").replace("ä", "ae")
        p = _out(f"geojson/{slug}.geojson.gz")
        with gzip.open(p, "wt", encoding="utf-8") as fh:
            json.dump({"type": "FeatureCollection", "features": feats}, fh, separators=(",", ":"))
        index[bl] = {"slug": slug, "count": len(feats)}
        paths.append(p)
    with open(_out("geojson/index.json"), "w", encoding="utf-8") as fh:
        json.dump(index, fh, ensure_ascii=False)
    log.info("GeoJSON: %d Bundesländer", len(paths))
    return paths


def write_all(db: Session) -> None:
    write_values(db)
    write_meta(db)
    write_geojson(db)
