"""Zensus 2022 (100m) → Gemeinde-Aggregat (Bevölkerung, Altersanteile, Gebäude).

Speichersparend (Plan §4C): jede nationale 100m-CSV wird EINMAL gestreamt und
dabei auf die 1km-INSPIRE-Zelle gefaltet (~360k Zellen statt ~3M). Anschließend
wird jede 1km-Zelle über einen ``STRtree`` genau einer Gemeinde zugeordnet und
je AGS akkumuliert. Ergebnis wird als Checkpoint-JSON abgelegt und in
``gemeinden.demographics`` geschrieben.
"""
from __future__ import annotations

import csv
import json
import logging
import os

import numpy as np
from pyproj import Transformer
from shapely import STRtree
from shapely.geometry import Point
from sqlalchemy.orm import Session

from app.config import settings
from app.models.lite_models import Gemeinde
from app.services import zensus_loader as zl

log = logging.getLogger(__name__)

_CHECKPOINT = os.path.join(settings.LITE_DATA_DIR, "zensus_gemeinde.json")


def _km_key(x: int, y: int) -> tuple[int, int]:
    return (x // 1000, y // 1000)


def _stream_fold(key: str, bbox_3035, km: dict[tuple[int, int], dict]) -> None:
    """Streamt eine 100m-CSV und faltet Werte auf die 1km-Akkumulatoren ``km``."""
    path = zl.ensure_zensus_dataset(key)
    d = zl.ZENSUS_DATASETS[key]
    primary = d.value_columns[0]
    xmin, ymin, xmax, ymax = bbox_3035
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh, delimiter=";")
        for row in reader:
            x = zl._parse_int(row.get("x_mp_100m"))
            y = zl._parse_int(row.get("y_mp_100m"))
            if x is None or y is None:
                continue
            if not (xmin <= x <= xmax and ymin <= y <= ymax):
                continue
            cell = km.setdefault(_km_key(x, y), {})
            if key == "population":
                v = zl._parse_int(row.get(primary))
                if v:
                    cell["pop"] = cell.get("pop", 0) + v
            elif key in ("share_over_65", "share_under_18"):
                v = zl._parse_float(row.get(primary))
                if v is not None:
                    fld = "o65" if key == "share_over_65" else "u18"
                    cell[fld + "_sum"] = cell.get(fld + "_sum", 0.0) + v
                    cell[fld + "_n"] = cell.get(fld + "_n", 0) + 1
            elif key == "building_age":
                b = zl._parse_int(row.get("Insgesamt_Gebaeude"))
                yr = zl._mean_building_year(
                    {c: zl._parse_int(row.get(c)) for c in d.value_columns})
                if b:
                    cell["bld"] = cell.get("bld", 0) + b  # Gesamt (Exposition)
                    # Baujahr-Mittel nur über Gebäude MIT bekanntem Baujahr
                    # gewichten (sonst zögen geheimgehaltene Klassen es < 1900).
                    if yr is not None:
                        cell["bld_yr_w"] = cell.get("bld_yr_w", 0.0) + b * yr
                        cell["bld_yr_n"] = cell.get("bld_yr_n", 0) + b


def _target_bbox_3035(gemeinden: list[Gemeinde], margin_m: int = 2000):
    """3035-Bounding-Box über die Repräsentationspunkte + großzügiger Rand."""
    to_3035 = Transformer.from_crs("EPSG:4326", "EPSG:3035", always_xy=True)
    xs, ys = to_3035.transform(
        [g.rep_lon for g in gemeinden], [g.rep_lat for g in gemeinden])
    return (
        int(min(xs)) - 30000, int(min(ys)) - 30000,
        int(max(xs)) + 30000, int(max(ys)) + 30000,
    )


def aggregate(db: Session, gemeinden: list[Gemeinde], force: bool = False) -> dict[str, dict]:
    """Aggregiert Zensus je AGS. Nutzt Checkpoint, außer ``force``.

    Gibt ``{ags: {population, share_over_65, share_under_18, buildings,
    mean_building_year}}`` zurück und schreibt es in ``gemeinden.demographics``.
    """
    from shapely.geometry import shape
    from geoalchemy2.shape import to_shape

    if not force and os.path.exists(_CHECKPOINT):
        with open(_CHECKPOINT, encoding="utf-8") as fh:
            cached = json.load(fh)
        if all(g.ags in cached for g in gemeinden):
            _write_back(db, gemeinden, cached)
            return {g.ags: cached[g.ags] for g in gemeinden}

    bbox = _target_bbox_3035(gemeinden)
    km: dict[tuple[int, int], dict] = {}
    for key in ("population", "share_over_65", "share_under_18", "building_age"):
        _stream_fold(key, bbox, km)
        log.info("Zensus-Fold %s: %d 1km-Zellen", key, len(km))

    # 1km-Zellzentren (3035) → 4326, dann STRtree-Zuordnung zur Gemeinde.
    keys = list(km.keys())
    cx = np.array([k[0] * 1000 + 500 for k in keys], dtype=float)
    cy = np.array([k[1] * 1000 + 500 for k in keys], dtype=float)
    to_4326 = Transformer.from_crs("EPSG:3035", "EPSG:4326", always_xy=True)
    lons, lats = to_4326.transform(cx, cy)

    geoms = [to_shape(g.geometry) for g in gemeinden]
    tree = STRtree(geoms)
    agg: dict[str, dict] = {g.ags: {} for g in gemeinden}
    ags_list = [g.ags for g in gemeinden]

    for i, k in enumerate(keys):
        pt = Point(lons[i], lats[i])
        # Shapely 2: predicate(input, tree_geom) → pt.within(gemeinde_polygon)
        cand = tree.query(pt, predicate="within")
        if len(cand) == 0:
            continue
        ags = ags_list[int(cand[0])]
        a = agg[ags]
        cell = km[k]
        a["pop"] = a.get("pop", 0) + cell.get("pop", 0)
        a["o65_sum"] = a.get("o65_sum", 0.0) + cell.get("o65_sum", 0.0)
        a["o65_n"] = a.get("o65_n", 0) + cell.get("o65_n", 0)
        a["u18_sum"] = a.get("u18_sum", 0.0) + cell.get("u18_sum", 0.0)
        a["u18_n"] = a.get("u18_n", 0) + cell.get("u18_n", 0)
        a["bld"] = a.get("bld", 0) + cell.get("bld", 0)
        a["bld_yr_w"] = a.get("bld_yr_w", 0.0) + cell.get("bld_yr_w", 0.0)
        a["bld_yr_n"] = a.get("bld_yr_n", 0) + cell.get("bld_yr_n", 0)

    result: dict[str, dict] = {}
    for ags, a in agg.items():
        bld = a.get("bld", 0)
        bld_yr_n = a.get("bld_yr_n", 0)
        result[ags] = {
            "population": int(a.get("pop", 0)),
            "share_over_65": round(a["o65_sum"] / a["o65_n"], 3) if a.get("o65_n") else None,
            "share_under_18": round(a["u18_sum"] / a["u18_n"], 3) if a.get("u18_n") else None,
            "buildings": int(bld),
            "mean_building_year": round(a["bld_yr_w"] / bld_yr_n, 1) if bld_yr_n else None,
        }

    _merge_checkpoint(result)
    _write_back(db, gemeinden, result)
    return result


def _merge_checkpoint(result: dict[str, dict]) -> None:
    os.makedirs(settings.LITE_DATA_DIR, exist_ok=True)
    existing = {}
    if os.path.exists(_CHECKPOINT):
        try:
            with open(_CHECKPOINT, encoding="utf-8") as fh:
                existing = json.load(fh)
        except Exception:
            existing = {}
    existing.update(result)
    with open(_CHECKPOINT, "w", encoding="utf-8") as fh:
        json.dump(existing, fh)


def _write_back(db: Session, gemeinden: list[Gemeinde], result: dict[str, dict]) -> None:
    for g in gemeinden:
        demo = result.get(g.ags)
        if demo is None:
            continue
        g.demographics = demo
        # Bevölkerung aus Zensus-Summe (VG250 trägt keine EWZ).
        if demo.get("population"):
            g.population = demo["population"]
    db.commit()
