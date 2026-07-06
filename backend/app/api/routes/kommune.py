import os
import shutil

from fastapi import APIRouter, Depends, HTTPException
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import shape as shapely_shape, mapping
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import (
    Kommune, ConfigParameter,
    CellAssessment, GridCell, AdaptationMeasure,
    MeasureImpact, ProjectStatus, RiskZone, GeoExportJob,
)
from app.services.geodata_export_service import get_exports_dir, assessment_is_done
from app.schemas.schemas import KommuneCreate, KommuneOut, KommuneSearch, GridGenerateRequest
from app.services import aggregate_cache, kommune_profile_service, osm_service, grid_service, layer_cache

router = APIRouter()


@router.get("/search", response_model=list[dict])
async def search(q: str, limit: int = 10):
    """Search for a municipality via OSM Nominatim."""
    if len(q) < 2:
        raise HTTPException(400, "Suchbegriff muss mindestens 2 Zeichen lang sein")
    results = await osm_service.search_kommune(q, limit=limit)
    return results


@router.post("", response_model=KommuneOut)
async def create_kommune(data: KommuneCreate, db: Session = Depends(get_db)):
    """Create a municipality by fetching its boundary from OSM."""
    existing = db.query(Kommune).filter(Kommune.osm_id == data.osm_id).first()
    if existing:
        return _kommune_to_out(existing)

    # Fetch boundary (Nominatim geometry → Nominatim lookup → Overpass mirrors)
    boundary_geojson = await osm_service.fetch_kommune_boundary(
        data.osm_id, data.osm_type, nominatim_geojson=data.geojson
    )
    if not boundary_geojson:
        raise HTTPException(404, "Kommune-Grenze konnte nicht abgerufen werden")

    # Convert GeoJSON to shapely, then to WKB for PostGIS
    shape = shapely_shape(boundary_geojson)
    if shape.geom_type == "Polygon":
        from shapely.geometry import MultiPolygon
        shape = MultiPolygon([shape])

    area_km2 = _estimate_area_km2(shape)

    kommune = Kommune(
        name=data.name,
        osm_id=data.osm_id,
        boundary=from_shape(shape, srid=4326),
        area_km2=round(area_km2, 2),
        bundesland=data.bundesland or osm_service.bundesland_from_address(data.address),
    )
    db.add(kommune)
    db.commit()
    db.refresh(kommune)

    # Set default config parameters
    _set_default_config(db, kommune.id)

    return _kommune_to_out(kommune)


@router.get("/{kommune_id}", response_model=KommuneOut)
def get_kommune(kommune_id: int, db: Session = Depends(get_db)):
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")
    return _kommune_to_out(kommune)


@router.get("/{kommune_id}/profile")
async def get_kommune_profile(kommune_id: int, db: Session = Depends(get_db)):
    """Kommunen-Profil: Basisdaten + Klimakennzahlen mit Deutschland-Vergleich.

    Funktioniert auch ohne abgeschlossene Berechnung (dann ohne Höhenlage/
    ggf. ohne Einwohner). Fehlendes Bundesland wird einmalig per Nominatim-
    Reverse-Geocoding nachgetragen (Lazy-Backfill, degradiert bei Fehlschlag).
    """
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")

    if not kommune.bundesland:
        centroid = kommune_profile_service.centroid_of(kommune)
        if centroid:
            bl = await osm_service.reverse_bundesland(lat=centroid[1], lon=centroid[0])
            if bl:
                kommune.bundesland = bl
                db.commit()

    return kommune_profile_service.build_profile(db, kommune)


@router.get("")
def list_kommunen(calculated: bool = False, db: Session = Depends(get_db)):
    kommunen = db.query(Kommune).order_by(Kommune.name).all()
    if calculated:
        kommunen = [k for k in kommunen if assessment_is_done(db, k.id)]
    return [_kommune_to_out(k, include_boundary=False) for k in kommunen]


@router.post("/{kommune_id}/grid")
def generate_grid(kommune_id: int, req: GridGenerateRequest = GridGenerateRequest(), db: Session = Depends(get_db)):
    """Generate a grid over the municipality boundary."""
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")

    count = grid_service.generate_grid(
        db, kommune_id, cell_size_m=req.cell_size_m, force=req.force,
    )
    aggregate_cache.invalidate(kommune_id)
    layer_cache.invalidate(kommune_id)
    return {"kommune_id": kommune_id, "cells_created": count, "cell_size_m": req.cell_size_m}


@router.get("/{kommune_id}/grid")
def get_grid(kommune_id: int, db: Session = Depends(get_db)):
    """Return grid cells as GeoJSON FeatureCollection."""
    return grid_service.get_grid_geojson(db, kommune_id)


@router.post("/{kommune_id}/reset")
def reset_kommune(kommune_id: int, db: Session = Depends(get_db)):
    """Reset all assessment, grid, and measure data for a municipality.

    Keeps the municipality entry (boundary, name, config) but deletes:
    climate assessments, grid cells, adaptation measures, project statuses,
    risk zones, and all derived data.
    """
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")

    # 1. Delete MeasureImpacts before their parents
    measure_ids = [
        r[0] for r in
        db.query(AdaptationMeasure.id)
        .filter(AdaptationMeasure.kommune_id == kommune_id)
        .all()
    ]
    if measure_ids:
        db.query(MeasureImpact)\
            .filter(MeasureImpact.measure_id.in_(measure_ids))\
            .delete(synchronize_session=False)

    # 2. Cell assessments
    db.query(CellAssessment)\
        .filter(CellAssessment.kommune_id == kommune_id)\
        .delete(synchronize_session=False)

    # 3. Risk zones (DB cascades to risk_zone_cells)
    db.query(RiskZone)\
        .filter(RiskZone.kommune_id == kommune_id)\
        .delete(synchronize_session=False)

    # 4. Grid cells (DB cascades any remaining child records)
    db.query(GridCell)\
        .filter(GridCell.kommune_id == kommune_id)\
        .delete(synchronize_session=False)

    # 5. Adaptation measures
    db.query(AdaptationMeasure)\
        .filter(AdaptationMeasure.kommune_id == kommune_id)\
        .delete(synchronize_session=False)

    # 6. Project statuses
    db.query(ProjectStatus)\
        .filter(ProjectStatus.kommune_id == kommune_id)\
        .delete(synchronize_session=False)

    # 7. Geo export jobs
    db.query(GeoExportJob)\
        .filter(GeoExportJob.kommune_id == kommune_id)\
        .delete(synchronize_session=False)

    db.commit()

    # Remove export files from disk
    export_dir = get_exports_dir(kommune_id)
    if os.path.isdir(export_dir):
        shutil.rmtree(export_dir, ignore_errors=True)

    # Karten-Layer- und Aggregat-Cache verwerfen
    aggregate_cache.invalidate(kommune_id)
    layer_cache.invalidate(kommune_id)

    return {"message": "Zurückgesetzt", "kommune_id": kommune_id}



# ── Helpers ────────────────────────────────────────────────────────────────────

def _kommune_to_out(k: Kommune, include_boundary: bool = True) -> dict:
    out = {
        "id": k.id,
        "name": k.name,
        "bundesland": k.bundesland,
        "osm_id": k.osm_id,
        "area_km2": k.area_km2,
        "population": k.population,
        "created_at": k.created_at.isoformat() if k.created_at else None,
    }
    if include_boundary and k.boundary is not None:
        shape = to_shape(k.boundary)
        out["boundary_geojson"] = mapping(shape)
    return out


def _estimate_area_km2(shape) -> float:
    """Rough area estimate using equirectangular approximation."""
    import math
    bounds = shape.bounds
    mid_lat = (bounds[1] + bounds[3]) / 2
    lat_km = 111.32
    lon_km = 111.32 * math.cos(math.radians(mid_lat))
    dx = (bounds[2] - bounds[0]) * lon_km
    dy = (bounds[3] - bounds[1]) * lat_km
    # Use the actual shape area, not just bounding box
    # shapely area in degrees², approximate conversion
    area_deg2 = shape.area
    area_km2 = area_deg2 * lat_km * lon_km
    return area_km2


def _set_default_config(db: Session, kommune_id: int):
    """Set minimal default configuration parameters for a new kommune.

    Die fachlichen Annahmen (Koeffizienten, Wirkungsstärken, Kostensätze) liegen
    fest im Katalog (``app/data/catalog.py``). Hier werden nur überschreibbare
    Defaults gesetzt, falls später UI-Konfiguration gewünscht ist.
    """
    defaults = [
        ("uhi", "alpha", 6.0, "UHI-Koeffizient α (Albedo & Versiegelung)"),
        ("uhi", "beta", 2.0, "UHI-Koeffizient β (Gebäudedichte)"),
        ("uhi", "gamma", 3.5, "UHI-Koeffizient γ (Grünkühlung)"),
        ("uhi", "delta", 2.0, "UHI-Koeffizient δ (Wasserkühlung)"),
    ]
    for cat, key, val, desc in defaults:
        existing = db.query(ConfigParameter).filter(
            ConfigParameter.kommune_id == kommune_id,
            ConfigParameter.category == cat,
            ConfigParameter.key == key,
        ).first()
        if not existing:
            db.add(ConfigParameter(kommune_id=kommune_id, category=cat, key=key,
                                   value=val, description=desc))
    db.commit()
