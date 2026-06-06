import math

from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import box, mapping
from shapely.ops import transform
from sqlalchemy.orm import Session
import pyproj

from app.config import settings
from app.models.models import Kommune, GridCell


def generate_grid(db: Session, kommune_id: int, cell_size_m: int = 100, *, force: bool = False) -> int:
    """Generate a rectangular grid of cells over the municipality boundary.

    Uses a projected CRS (UTM) for metric grid generation, then converts
    cells back to WGS84 (EPSG:4326).

    If a grid already exists and ``force`` is False, returns the existing
    cell count without deleting assessments or other derived data.

    Returns the number of cells created (or already present).
    """
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune or kommune.boundary is None:
        raise ValueError(f"Kommune {kommune_id} not found or has no boundary")

    existing_count = (
        db.query(GridCell).filter(GridCell.kommune_id == kommune_id).count()
    )
    if existing_count > 0 and not force:
        return existing_count

    # Delete existing grid for this kommune (cascades to assessments)
    if existing_count > 0:
        db.query(GridCell).filter(GridCell.kommune_id == kommune_id).delete()

    # Load boundary as shapely geometry
    boundary_shape = to_shape(kommune.boundary)

    # Set up coordinate transformations: WGS84 <-> UTM
    proj_wgs84 = pyproj.CRS("EPSG:4326")
    proj_utm = pyproj.CRS(f"EPSG:{settings.CALCULATION_SRID}")

    transformer_to_utm = pyproj.Transformer.from_crs(proj_wgs84, proj_utm, always_xy=True)
    transformer_to_wgs = pyproj.Transformer.from_crs(proj_utm, proj_wgs84, always_xy=True)

    # Transform boundary to UTM
    boundary_utm = transform(transformer_to_utm.transform, boundary_shape)
    minx, miny, maxx, maxy = boundary_utm.bounds

    # Generate grid cells
    cols = math.ceil((maxx - minx) / cell_size_m)
    rows = math.ceil((maxy - miny) / cell_size_m)

    cells = []
    for row_idx in range(rows):
        for col_idx in range(cols):
            x0 = minx + col_idx * cell_size_m
            y0 = miny + row_idx * cell_size_m
            x1 = x0 + cell_size_m
            y1 = y0 + cell_size_m

            cell_utm = box(x0, y0, x1, y1)

            # Only include cells that intersect the municipality boundary
            if not cell_utm.intersects(boundary_utm):
                continue

            # Transform cell back to WGS84
            cell_wgs = transform(transformer_to_wgs.transform, cell_utm)

            cells.append(GridCell(
                kommune_id=kommune_id,
                geometry=from_shape(cell_wgs, srid=4326),
                row_idx=row_idx,
                col_idx=col_idx,
                cell_size_m=cell_size_m,
            ))

    # Bulk insert
    if cells:
        db.bulk_save_objects(cells)
        db.commit()

    return len(cells)


def get_grid_geojson(db: Session, kommune_id: int) -> dict:
    """Return grid cells as a GeoJSON FeatureCollection."""
    cells = db.query(GridCell).filter(GridCell.kommune_id == kommune_id).all()

    features = []
    for cell in cells:
        shape = to_shape(cell.geometry)
        features.append({
            "type": "Feature",
            "properties": {
                "id": cell.id,
                "row": cell.row_idx,
                "col": cell.col_idx,
                "cell_size_m": cell.cell_size_m,
            },
            "geometry": mapping(shape),
        })

    return {
        "type": "FeatureCollection",
        "features": features,
    }
