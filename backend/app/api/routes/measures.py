from fastapi import APIRouter, Depends, HTTPException
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import shape as shapely_shape, mapping
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import AdaptationMeasure, MeasureImpact
from app.schemas.schemas import MeasureCreate, MeasureUpdate
from app.services.impact_service import compute_impact
from app.services.climate.heat.measures import get_measure_catalog

router = APIRouter()


@router.get("/measure-catalog")
def measure_catalog():
    """Get available measure types and their parameters."""
    return get_measure_catalog()


@router.post("/kommune/{kommune_id}/measures")
def create_measure(
    kommune_id: int,
    data: MeasureCreate,
    db: Session = Depends(get_db),
):
    """Create a new adaptation measure with geometry."""
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

    return _measure_to_dict(measure)


@router.get("/kommune/{kommune_id}/measures")
def list_measures(kommune_id: int, db: Session = Depends(get_db)):
    """List all measures for a municipality."""
    measures = (
        db.query(AdaptationMeasure)
        .filter(AdaptationMeasure.kommune_id == kommune_id)
        .all()
    )
    return [_measure_to_dict(m) for m in measures]


@router.get("/measures/{measure_id}")
def get_measure(measure_id: int, db: Session = Depends(get_db)):
    measure = db.query(AdaptationMeasure).filter(AdaptationMeasure.id == measure_id).first()
    if not measure:
        raise HTTPException(404, "Maßnahme nicht gefunden")
    return _measure_to_dict(measure)


@router.put("/measures/{measure_id}")
def update_measure(measure_id: int, data: MeasureUpdate, db: Session = Depends(get_db)):
    measure = db.query(AdaptationMeasure).filter(AdaptationMeasure.id == measure_id).first()
    if not measure:
        raise HTTPException(404, "Maßnahme nicht gefunden")

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
    return _measure_to_dict(measure)


@router.delete("/measures/{measure_id}")
def delete_measure(measure_id: int, db: Session = Depends(get_db)):
    measure = db.query(AdaptationMeasure).filter(AdaptationMeasure.id == measure_id).first()
    if not measure:
        raise HTTPException(404, "Maßnahme nicht gefunden")
    db.delete(measure)
    db.commit()
    return {"message": "Maßnahme gelöscht"}


@router.post("/measures/{measure_id}/calculate-impact")
def calculate_impact(measure_id: int, db: Session = Depends(get_db)):
    """Calculate the climate impact of a measure."""
    try:
        result = compute_impact(db, measure_id)
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    return result


@router.get("/measures/{measure_id}/impacts")
def get_impacts(measure_id: int, db: Session = Depends(get_db)):
    """Get cell-level impacts for a measure."""
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
    }
