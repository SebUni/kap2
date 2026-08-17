import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping
from sqlalchemy.orm import Session

from app.api.deps import demo_session_id_of, require_admin
from app.api.gzip_files import file_etag, gzip_json_file_response
from app.db.database import get_db
from app.data import catalog
from app.models.auth_models import User
from app.services import dashboard_cache, layer_cache
from app.models.models import (
    Kommune, CellAssessment, GridCell, ProjectStatus, AssessmentStatus,
)
from app.tasks.assessment_task import (
    run_assessment_background, abort_assessment, is_row_alive, TASK_KEY,
)
from app.services.engine import risk_engine
from app.services.engine import formulas
from app.services.engine.inputs import build_regional_context
from app.services.engine.runner import COASTAL_BUNDESLAENDER

log = logging.getLogger(__name__)
router = APIRouter()


def _layer_category(code: str) -> str | None:
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


@router.post("/kommune/{kommune_id}/assess")
def start_assessment(
    kommune_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    """Reiht die vollständige KAP3-Bewertung ein (läuft als eigener Prozess). (Admin)"""
    cell_count = db.query(GridCell).filter(GridCell.kommune_id == kommune_id).count()
    if cell_count == 0:
        raise HTTPException(400, "Keine Grid-Zellen vorhanden. Bitte zuerst Grid generieren.")

    run_assessment_background(kommune_id)
    return {"message": "Berechnung eingereiht", "kommune_id": kommune_id}


@router.post("/kommune/{kommune_id}/assess/abort")
def abort_running_assessment(
    kommune_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    """Bricht laufende/eingereihte Berechnung ab (Kind-Prozess via DB-Flag+SIGTERM).

    ``abort_assessment`` heilt auch tote RUNNING-Zeilen autoritativ, damit der
    Abbrechen-Knopf nach Standby/Neustart nicht scheinbar wirkungslos bleibt.
    """
    aborted = abort_assessment(db, kommune_id)
    if aborted:
        return {"message": "Berechnung wird abgebrochen", "aborted": True}
    return {"message": "Keine laufende Berechnung gefunden", "aborted": False}


@router.get("/kommune/{kommune_id}/status")
def get_status(kommune_id: int, db: Session = Depends(get_db)):
    ps = (db.query(ProjectStatus)
          .filter(ProjectStatus.kommune_id == kommune_id, ProjectStatus.task_key == TASK_KEY)
          .first())
    if not ps:
        return {"status": None, "progress_pct": 0.0, "message": None,
                "step_history": [], "eta_seconds": None,
                "queue_position": None, "recalc_recommended": False}
    # Selbstheilung: Status RUNNING, aber der Kind-Prozess lebt nicht mehr
    # (PID+Start-Ticks) → Lauf ist tot (SIGKILL/OOM/Absturz). Verwaiste Kinder
    # eines früheren API-Prozesses (--reload) gelten korrekt als lebendig.
    if ps.status == AssessmentStatus.RUNNING and not is_row_alive(ps):
        ps.status = AssessmentStatus.ERROR
        ps.message = "Berechnung unterbrochen (Standby/Neustart) – bitte neu starten"
        ps.finished_at = datetime.utcnow()
        ps.worker_pid = None
        db.commit()
    queue_position = None
    if ps.status == AssessmentStatus.QUEUED and ps.queued_at is not None:
        queue_position = 1 + (
            db.query(ProjectStatus)
            .filter(ProjectStatus.task_key == TASK_KEY,
                    ProjectStatus.status == AssessmentStatus.QUEUED,
                    ProjectStatus.queued_at < ps.queued_at)
            .count()
        )
    return {
        "status": ps.status.value if ps.status else None,
        "progress_pct": ps.progress_pct,
        "message": ps.message,
        "started_at": ps.started_at.isoformat() if ps.started_at else None,
        "finished_at": ps.finished_at.isoformat() if ps.finished_at else None,
        "step_history": ps.step_history or [],
        "eta_seconds": ps.eta_seconds,
        "queue_position": queue_position,
        "recalc_recommended": bool(ps.recalc_recommended),
    }


@router.get("/kommune/{kommune_id}/grid-geometry")
def get_grid_geometry(kommune_id: int, request: Request, db: Session = Depends(get_db)):
    """Statische Zellgeometrie (einmal je Kommune) als gzip-GeoJSON (ETag/304).

    Nur ``grid_cell_id`` (+ gitter_id/row/col) und Geometrie; die Layer-Werte
    kommen getrennt ueber ``/layer/{code}/values``.
    """
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")
    path = layer_cache.geometry_file(db, kommune_id)
    if not path:
        return {"type": "FeatureCollection", "features": []}
    return gzip_json_file_response(
        request, path, etag=file_etag(path),
        download_name=f"grid-geometry-{kommune_id}.json",
    )


@router.get("/kommune/{kommune_id}/layer/{code}/values")
def get_layer_values(kommune_id: int, code: str, request: Request, db: Session = Depends(get_db)):
    """Layer-Werte ohne Geometrie (klein) als gzip-JSON (ETag/304).

    ``cells`` enthaelt je Zelle ``grid_cell_id``, ``value`` und die
    Inspektor-Detailfelder; ``meta`` liefert Min/Max/Label/Unit/Recipe.
    """
    if not layer_cache.layer_category(code):
        raise HTTPException(404, f"Unbekannter Code: {code}")
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")
    try:
        path = layer_cache.values_file(db, kommune_id, code)
    except Exception as exc:
        log.exception("get_layer_values failed kommune=%s code=%s", kommune_id, code)
        raise HTTPException(500, f"Layer konnte nicht geladen werden: {exc}") from exc
    if not path:
        raise HTTPException(404, f"Unbekannter Code: {code}")
    return gzip_json_file_response(
        request, path, etag=file_etag(path),
        download_name=f"layer-{code}-{kommune_id}.json",
    )


@router.get("/kommune/{kommune_id}/layer/{code}")
def get_layer(kommune_id: int, code: str, db: Session = Depends(get_db)):
    """GeoJSON einer einzelnen Ebene (H/E/V-Code oder Risiko-Code).

    DEPRECATED: Das Frontend nutzt ``/grid-geometry`` + ``/layer/{code}/values``
    (vorgebaute gzip-Dateien). Dieser Per-Request-Vollbau bleibt eine Version
    lang für externe Nutzer erhalten und wird dann entfernt.

    Property ``value`` enthält den darzustellenden Wert in absoluter Einheit
    (H/E/V und Risiken). ``meta`` liefert Min/Max für die Legende.
    """
    log.warning("DEPRECATED: GET /kommune/%s/layer/%s — bitte /grid-geometry + "
                "/layer/{code}/values verwenden", kommune_id, code)
    category = _layer_category(code)
    if not category:
        raise HTTPException(404, f"Unbekannter Code: {code}")

    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")

    try:
        is_coastal = (kommune.bundesland or "") in COASTAL_BUNDESLAENDER
        centroid = None
        if kommune.boundary is not None:
            try:
                c = to_shape(kommune.boundary).centroid
                centroid = (c.x, c.y)
            except Exception:
                centroid = None
        # Kommune-Overrides installieren: build_regional_context (regionale Fallbacks),
        # normalize_hev/cell_outcome_breakdown/resolve_inputs und die Rezept-Anzeige-
        # texte lesen Overrides über das Modul-Global (§8/B2-Leak sonst).
        with layer_cache._override_scope_for(db, kommune_id):
            regional = build_regional_context(
                kommune.bundesland, is_coastal, kommune.osm_id, centroid,
            )
            recipe = formulas.recipe_for_layer(code, category)

            rows = (
                db.query(CellAssessment, GridCell)
                .join(GridCell, CellAssessment.grid_cell_id == GridCell.id)
                .filter(CellAssessment.kommune_id == kommune_id)
                .all()
            )
            features = []
            vmin, vmax = None, None
            for ca, cell in rows:
                data = ca.data or {}
                props: dict = {
                    "grid_cell_id": cell.id,
                    "gitter_id": cell.gitter_id,
                    "row": cell.row_idx,
                    "col": cell.col_idx,
                }
                if category == "risks":
                    rdef = catalog.RISKS_BY_CODE[code]
                    rcell = data.get("risks", {}).get(code, {})
                    idx = float(rcell.get("index", 0.0))
                    cell_pop = float(data.get("inputs", {}).get("pop", 0.0))
                    # Materialisierten Outcome nutzen (Schicht B); Fallback für Alt-Daten.
                    stored = rcell.get("outcome")
                    value = float(stored) if stored is not None else risk_engine.cell_outcome(rdef, idx, cell_pop)
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
                features.append({
                    "type": "Feature",
                    "properties": props,
                    "geometry": mapping(to_shape(cell.geometry)),
                })

        meta = {"code": code, "category": category, "min": vmin or 0.0, "max": vmax or 0.0, "recipe": recipe}
        if category == "risks":
            r = catalog.RISKS_BY_CODE[code]
            meta.update({"label": r["name"], "unit": r["outcome_unit"]})
        else:
            m = catalog.INDICATOR_BY_CODE[code]
            meta.update({"label": m["name"], "unit": m["unit"]})

        return {"type": "FeatureCollection", "features": features, "meta": meta}
    except HTTPException:
        raise
    except Exception as exc:
        log.exception("get_layer failed kommune=%s code=%s", kommune_id, code)
        raise HTTPException(500, f"Layer konnte nicht geladen werden: {exc}") from exc


@router.get("/kommune/{kommune_id}/risk-summary")
def risk_summary(kommune_id: int, request: Request, db: Session = Depends(get_db)):
    """Aggregiertes Risiko (Basis, ohne Maßnahmen): Gruppen + Einzelrisiken.

    Payload wird im Hintergrund vorgebaut (``dashboard_cache``); hier nur
    Datei-Auslieferung mit ETag/304, Lazy-Build bei Miss/Stale.
    """
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")
    art = dashboard_cache.artifact_file(db, kommune_id, "risk_summary")
    if not art:
        raise HTTPException(404, "Kommune nicht gefunden")
    path, etag = art
    return gzip_json_file_response(
        request, path, etag=etag, download_name=f"risk-summary-{kommune_id}.json",
    )


@router.get("/kommune/{kommune_id}/risk-histogram")
def risk_histogram(kommune_id: int, request: Request, db: Session = Depends(get_db)):
    """Häufigkeitsverteilung der Risiko-Index-Höhen je Risiko (20 Bins à 5, 0-100).

    Botschaft: wenige hohe Zellen → punktuelle Maßnahmen; viele hohe →
    flächendeckend. Builder: ``dashboard_cache._build_risk_histogram`` (streamt
    die Zell-Blobs) — vorher scannte dieser Endpoint bei JEDEM Aufruf alle
    ``CellAssessment``-Zeilen.
    """
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")
    art = dashboard_cache.artifact_file(db, kommune_id, "risk_histogram")
    if not art:
        raise HTTPException(404, "Kommune nicht gefunden")
    path, etag = art
    return gzip_json_file_response(
        request, path, etag=etag, download_name=f"risk-histogram-{kommune_id}.json",
    )


@router.get("/kommune/{kommune_id}/risk-zones/{risk_code}")
def risk_zones(kommune_id: int, risk_code: str, db: Session = Depends(get_db)):
    from app.services.risk_zone_service import get_risk_zones_geojson
    if risk_code not in catalog.RISKS_BY_CODE:
        raise HTTPException(400, f"Unbekannter Risiko-Code: {risk_code}")
    return get_risk_zones_geojson(db, kommune_id, risk_code)


# ── DWD / Klimadaten (unverändert weiterverwendet) ─────────────────────────────

@router.get("/kommune/{kommune_id}/climate-history")
def get_climate_history(kommune_id: int, db: Session = Depends(get_db)):
    from app.services.climate.dwd_data import get_climate_history as _h
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")
    return _h(kommune.bundesland or None)


@router.get("/kommune/{kommune_id}/regional-climate")
def get_regional_climate(kommune_id: int, db: Session = Depends(get_db)):
    from app.services.climate.dwd_data import get_regional_climate as _r
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")
    return _r(kommune.bundesland or "Nordrhein-Westfalen")


@router.get("/kommune/{kommune_id}/climate-projection")
def get_climate_projection_route(kommune_id: int, db: Session = Depends(get_db)):
    from app.services.climate.dwd_data import get_climate_projection
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")
    return get_climate_projection(kommune.bundesland or None)


@router.get("/kommune/{kommune_id}/risk-projection")
def get_risk_projection(kommune_id: int, db: Session = Depends(get_db)):
    """Projiziert die KWRA-Gruppen-Indizes 2025–2065 (RCP4.5/8.5)."""
    from app.services.projection_service import project_group_risks
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")
    return project_group_risks(db, kommune_id, kommune.bundesland or "Sachsen")


@router.get("/kommune/{kommune_id}/cost-projection")
def get_cost_projection(kommune_id: int, request: Request, db: Session = Depends(get_db)):
    """Erwartete Jahresschäden 2025–2065 (RCP4.5/8.5), mit/ohne Maßnahmen.

    „Mit Maßnahmen" preist die Maßnahmenkosten ein: OPEX jährlich ab
    Umsetzungsjahr, CAPEX einmalig im Umsetzungsjahr. Payload vorgebaut
    (``dashboard_cache``), hier nur Datei-Auslieferung mit ETag/304.
    Demo: live gerechnet mit Session-Maßnahmenfilter (kein geteiltes Artefakt).
    """
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")
    demo_sid = demo_session_id_of(request)
    if demo_sid:
        from app.services.cost_projection_service import project_costs
        return project_costs(db, kommune_id, kommune.bundesland or "Sachsen",
                             demo_session_id=demo_sid)
    art = dashboard_cache.artifact_file(db, kommune_id, "cost_projection")
    if not art:
        raise HTTPException(404, "Kommune nicht gefunden")
    path, etag = art
    return gzip_json_file_response(
        request, path, etag=etag, download_name=f"cost-projection-{kommune_id}.json",
    )
