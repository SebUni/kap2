"""Öffentliche Deutschland-Karte: billige Endpunkte (statische Artefakte +
Einzelzeilen-Lookups). Keine On-Demand-Berechnung."""
import gzip
import json
import os

from fastapi import APIRouter, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi import Depends

from app.config import settings
from app.data import catalog, sources
from app.db.database import get_db
from app.models.lite_models import Gemeinde, GemeindeLiteResult

router = APIRouter()


def _artifact(name: str) -> str:
    return os.path.join(settings.LITE_DATA_DIR, name)


@router.get("/meta")
def lite_meta():
    path = _artifact("meta.json")
    if not os.path.exists(path):
        raise HTTPException(404, "Deutschland-Karte noch nicht berechnet")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


@router.get("/values")
def lite_values():
    """values.json (gzip) — {ags: {RISK: index}}. Direkt gzip ausliefern."""
    path = _artifact("values.json.gz")
    if not os.path.exists(path):
        raise HTTPException(404, "Deutschland-Karte noch nicht berechnet")
    with open(path, "rb") as fh:
        data = fh.read()
    etag = f'"{os.path.getmtime(path):.0f}"'
    return Response(data, media_type="application/json",
                    headers={"Content-Encoding": "gzip", "ETag": etag,
                             "Cache-Control": "public, max-age=3600"})


@router.get("/geojson/{slug}")
def lite_geojson(slug: str):
    safe = "".join(c for c in slug if c.isalnum() or c == "-")
    path = _artifact(f"geojson/{safe}.geojson.gz")
    if not os.path.exists(path):
        raise HTTPException(404, "Nicht gefunden")
    with open(path, "rb") as fh:
        data = fh.read()
    return Response(data, media_type="application/json",
                    headers={"Content-Encoding": "gzip",
                             "Cache-Control": "public, max-age=3600"})


@router.get("/geojson-index")
def lite_geojson_index():
    path = _artifact("geojson/index.json")
    if not os.path.exists(path):
        raise HTTPException(404, "Nicht gefunden")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


@router.get("/gemeinde/{ags}")
def lite_gemeinde(ags: str, db: Session = Depends(get_db)):
    """Einzelne Gemeinde: Basisdaten + alle Risiken mit Treibern/Quellen."""
    g = db.query(Gemeinde).filter(Gemeinde.ags == ags).first()
    if not g:
        raise HTTPException(404, "Gemeinde nicht gefunden")
    rows = db.query(GemeindeLiteResult).filter(GemeindeLiteResult.ags == ags).all()
    risks = []
    for r in rows:
        cat = catalog.RISKS_BY_CODE.get(r.risk_code, {})
        drivers = dict(r.drivers or {})
        src_keys = drivers.pop("source_refs", None)
        risks.append({
            "code": r.risk_code,
            "name": cat.get("name", r.risk_code),
            "group": cat.get("group"),
            "index": r.index_value,
            "outcome": r.outcome_value,
            "unit": r.outcome_unit,
            "cost_eur": r.cost_eur,
            "drivers": drivers,
            "sources": sources.resolve(src_keys),
        })
    return {
        "ags": g.ags,
        "name": g.name,
        "bez": g.bez,
        "bundesland": g.bundesland,
        "population": g.population,
        "area_km2": g.area_km2,
        "risks": risks,
    }


def _require_study_enabled() -> None:
    """M0-Verschlankung: Studien-Endpunkte offline, kehren mit M3½ zurück (410)."""
    if not settings.STUDY_ENABLED:
        raise HTTPException(410, "Die Deutschland-Studie ist derzeit offline")


@router.get("/studie")
def lite_studie():
    _require_study_enabled()
    path = _artifact("studie.json")
    if not os.path.exists(path):
        raise HTTPException(404, "Studie noch nicht generiert")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


@router.get("/studie.csv")
def lite_studie_csv():
    _require_study_enabled()
    from fastapi.responses import FileResponse
    path = _artifact("studie.csv")
    if not os.path.exists(path):
        raise HTTPException(404, "Studie noch nicht generiert")
    return FileResponse(path, media_type="text/csv", filename="kap2-deutschlandstudie.csv")


@router.get("/study-highlights")
def study_highlights(db: Session = Depends(get_db)):
    """Kernzahlen für die Landingpage (aus den vorberechneten Ergebnissen)."""
    _require_study_enabled()
    path = _artifact("study_highlights.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    # Fallback: leer, wenn Studie noch nicht generiert (Phase 7).
    n = db.query(Gemeinde).count()
    if n == 0:
        raise HTTPException(404, "Noch keine Daten")
    return {"headline_facts": [], "stand": None, "gemeinde_count": n}
