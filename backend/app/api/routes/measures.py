from fastapi import APIRouter, Depends, HTTPException, Request
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import shape as shapely_shape, mapping
from sqlalchemy.orm import Session

from app.api.deps import Actor, DemoActor, assert_measure_access, demo_session_id_of, require_actor
from app.api.gzip_files import gzip_json_file_response
from app.db.database import get_db
from app.models.models import AdaptationMeasure, MeasureImpact
from app.schemas.schemas import MeasureCreate, MeasureUpdate
from app.services.measure_service import compute_impact
from app.services import artifact_rebuild, dashboard_cache
from app.data import catalog

router = APIRouter()


@router.get("/measure-catalog")
def measure_catalog(request: Request):
    """Verfügbare Maßnahmentypen aus dem festen KAP3-Katalog.

    Demo: nur Maßnahmen, deren Wirkung eines der freigeschalteten Demo-
    Risiken trifft — alles andere hätte in der Demo sichtbar keinen Effekt.
    """
    demo_risks = getattr(request.state, "demo_risk_codes", None)
    if demo_risks:
        wanted = set(demo_risks)
        return [m for m in catalog.MEASURES
                if wanted.intersection(m.get("linked_risk_codes", []))]
    return catalog.MEASURES


@router.get("/kommune/{kommune_id}/cost-summary")
def cost_summary(kommune_id: int, request: Request, db: Session = Depends(get_db)):
    """Kostenübersicht (siehe ``measure_service.build_cost_summary``).

    Produkt: Datei-Auslieferung aus dem ``dashboard_cache`` (ETag/304).
    Demo: live gerechnet mit Session-Maßnahmenfilter — Demo-Sessions dürfen
    weder gemeinsame Artefakte lesen (falsche Maßnahmen) noch bauen.
    """
    demo_sid = demo_session_id_of(request)
    if demo_sid:
        from app.services.measure_service import build_cost_summary
        return build_cost_summary(db, kommune_id, demo_session_id=demo_sid)
    art = dashboard_cache.artifact_file(db, kommune_id, "cost_summary")
    if not art:
        raise HTTPException(404, "Kommune nicht gefunden")
    path, etag = art
    return gzip_json_file_response(
        request, path, etag=etag, download_name=f"cost-summary-{kommune_id}.json",
    )


@router.post("/kommune/{kommune_id}/measures")
def create_measure(
    kommune_id: int,
    data: MeasureCreate,
    db: Session = Depends(get_db),
    actor: Actor = Depends(require_actor),
):
    """Create a new adaptation measure with geometry."""
    is_demo = isinstance(actor, DemoActor)
    if is_demo:
        from app.services import demo_service
        if demo_service.measure_count(db, actor.session_id) >= actor.measure_limit:
            raise HTTPException(
                429,
                f"Demo-Limit erreicht: maximal {actor.measure_limit} Maßnahmen je Sitzung.",
            )

    # Parse GeoJSON geometry
    try:
        shape = shapely_shape(data.geometry_geojson)
    except Exception:
        raise HTTPException(400, "Ungültige Geometrie")

    if shape.geom_type not in ("Polygon", "MultiPolygon"):
        raise HTTPException(400, "Geometrie muss ein Polygon sein")

    if shape.geom_type == "MultiPolygon":
        from shapely.geometry import Polygon
        # Use the largest polygon
        shape = max(shape.geoms, key=lambda g: g.area)

    measure = AdaptationMeasure(
        kommune_id=kommune_id,
        demo_session_id=actor.session_id if is_demo else None,
        name=data.name,
        measure_type=data.measure_type,
        geometry=from_shape(shape, srid=4326),
        config=data.config,
        implementation_year=data.implementation_year,
        description=data.description,
    )
    db.add(measure)
    db.commit()
    db.refresh(measure)

    # Basis-Aggregat hängt nicht von Maßnahmen ab → nur „mit Maßnahmen"-Variante
    # invalidieren; Dashboard-Artefakte werden entprellt im Hintergrund neu gebaut.
    # Demo-Maßnahmen berühren die gemeinsamen Artefakte nicht (Session-Filter).
    if not is_demo:
        artifact_rebuild.invalidate_and_schedule(kommune_id, only_with_measures=True)
    return _measure_to_dict(measure)


@router.get("/kommune/{kommune_id}/measures")
def list_measures(kommune_id: int, request: Request, db: Session = Depends(get_db)):
    """List all measures for a municipality (Demo: nur die eigene Sitzung)."""
    from app.services.measure_service import ensure_fresh_impact_summary
    demo_sid = demo_session_id_of(request)
    q = db.query(AdaptationMeasure).filter(AdaptationMeasure.kommune_id == kommune_id)
    if demo_sid:
        q = q.filter(AdaptationMeasure.demo_session_id == demo_sid)
    else:
        q = q.filter(AdaptationMeasure.demo_session_id.is_(None))
    measures = q.all()
    for m in measures:
        ensure_fresh_impact_summary(db, m)
    return [_measure_to_dict(m) for m in measures]


@router.get("/measures/{measure_id}")
def get_measure(measure_id: int, db: Session = Depends(get_db), actor: Actor = Depends(require_actor)):
    from app.services.measure_service import ensure_fresh_impact_summary
    measure = db.query(AdaptationMeasure).filter(AdaptationMeasure.id == measure_id).first()
    if not measure:
        raise HTTPException(404, "Maßnahme nicht gefunden")
    assert_measure_access(db, actor, measure)
    ensure_fresh_impact_summary(db, measure)
    return _measure_to_dict(measure)


@router.put("/measures/{measure_id}")
def update_measure(measure_id: int, data: MeasureUpdate, db: Session = Depends(get_db), actor: Actor = Depends(require_actor)):
    measure = db.query(AdaptationMeasure).filter(AdaptationMeasure.id == measure_id).first()
    if not measure:
        raise HTTPException(404, "Maßnahme nicht gefunden")
    assert_measure_access(db, actor, measure)

    if data.name is not None:
        measure.name = data.name
    if data.measure_type is not None:
        measure.measure_type = data.measure_type
    if data.config is not None:
        measure.config = data.config
    if data.implementation_year is not None:
        measure.implementation_year = data.implementation_year
    if data.description is not None:
        measure.description = data.description

    db.commit()
    db.refresh(measure)
    if measure.demo_session_id is None:
        artifact_rebuild.invalidate_and_schedule(measure.kommune_id, only_with_measures=True)
    return _measure_to_dict(measure)


@router.delete("/measures/{measure_id}")
def delete_measure(measure_id: int, db: Session = Depends(get_db), actor: Actor = Depends(require_actor)):
    measure = db.query(AdaptationMeasure).filter(AdaptationMeasure.id == measure_id).first()
    if not measure:
        raise HTTPException(404, "Maßnahme nicht gefunden")
    assert_measure_access(db, actor, measure)
    kommune_id = measure.kommune_id
    was_demo = measure.demo_session_id is not None
    db.delete(measure)
    db.commit()
    if not was_demo:
        artifact_rebuild.invalidate_and_schedule(kommune_id, only_with_measures=True)
    return {"message": "Maßnahme gelöscht"}


@router.post("/measures/{measure_id}/calculate-impact")
def calculate_impact(measure_id: int, db: Session = Depends(get_db), actor: Actor = Depends(require_actor)):
    """Calculate the climate impact of a measure.

    Invalidiert die Caches NUR, wenn sich das Ergebnis tatsächlich geändert hat
    (Vergleich ohne den ``params_fingerprint``). Sonst warf jeder Aufruf —
    etwa der frühere Maßnahmen-Tab, der beim Öffnen für JEDE Maßnahme POSTete —
    das Aggregat weg und das Dashboard rechnete anschließend alles neu.
    """
    measure = db.query(AdaptationMeasure).filter(AdaptationMeasure.id == measure_id).first()
    if not measure:
        raise HTTPException(404, "Maßnahme nicht gefunden")
    assert_measure_access(db, actor, measure)
    previous = {k: v for k, v in (measure.impact_summary or {}).items()
                if k != "params_fingerprint"}
    try:
        result = compute_impact(db, measure_id)
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    current = {k: v for k, v in result.items() if k != "params_fingerprint"}
    if current != previous and measure.demo_session_id is None:
        artifact_rebuild.invalidate_and_schedule(measure.kommune_id, only_with_measures=True)
    return result


@router.get("/measures/{measure_id}/impacts")
def get_impacts(measure_id: int, db: Session = Depends(get_db), actor: Actor = Depends(require_actor)):
    """Get cell-level impacts for a measure."""
    measure = db.query(AdaptationMeasure).filter(AdaptationMeasure.id == measure_id).first()
    if not measure:
        raise HTTPException(404, "Maßnahme nicht gefunden")
    assert_measure_access(db, actor, measure)
    impacts = db.query(MeasureImpact).filter(MeasureImpact.measure_id == measure_id).all()
    return [
        {
            "id": imp.id,
            "grid_cell_id": imp.grid_cell_id,
            "indicator_deltas": imp.indicator_deltas,
            "costs": imp.costs,
            "savings": imp.savings,
        }
        for imp in impacts
    ]


def _measure_to_dict(m: AdaptationMeasure) -> dict:
    geom_geojson = None
    if m.geometry is not None:
        geom_geojson = mapping(to_shape(m.geometry))
    return {
        "id": m.id,
        "kommune_id": m.kommune_id,
        "name": m.name,
        "measure_type": m.measure_type,
        "geometry_geojson": geom_geojson,
        "config": m.config,
        "implementation_year": m.implementation_year,
        "description": m.description,
        "created_at": m.created_at.isoformat() if m.created_at else None,
        "impact_summary": m.impact_summary,
    }
