import math

from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import box, mapping
from shapely.ops import transform
from sqlalchemy.orm import Session
import pyproj

from app.config import settings
from app.models.models import Kommune, GridCell

CELL_SIZE_M = 100


def gitter_id_from_origin(x0: int, y0: int) -> str:
    """INSPIRE GITTER_ID for 100m cell lower-left corner in EPSG:3035."""
    return f"CRS3035RES100mN{y0}E{x0}"


def generate_grid(db: Session, kommune_id: int, cell_size_m: int = 100, *, force: bool = False) -> int:
    """Generate Zensus INSPIRE 100m grid cells intersecting the municipality.

    Uses EPSG:3035 for alignment with Destatis/BKG Zensus 2022 grid, stores
    geometry in EPSG:4326.
    """
    if cell_size_m != 100:
        raise ValueError("Nur 100m-Zensus-Gitter wird unterstützt")

    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune or kommune.boundary is None:
        raise ValueError(f"Kommune {kommune_id} not found or has no boundary")

    existing_count = db.query(GridCell).filter(GridCell.kommune_id == kommune_id).count()
    if existing_count > 0 and not force:
        return existing_count

    if existing_count > 0:
        db.query(GridCell).filter(GridCell.kommune_id == kommune_id).delete()

    boundary_shape = to_shape(kommune.boundary)

    proj_wgs84 = pyproj.CRS("EPSG:4326")
    proj_laea = pyproj.CRS(f"EPSG:{settings.ZENSUS_SRID}")
    to_laea = pyproj.Transformer.from_crs(proj_wgs84, proj_laea, always_xy=True)
    to_wgs = pyproj.Transformer.from_crs(proj_laea, proj_wgs84, always_xy=True)

    boundary_laea = transform(to_laea.transform, boundary_shape)
    minx, miny, maxx, maxy = boundary_laea.bounds

    x_start = int(math.floor(minx / cell_size_m) * cell_size_m)
    y_start = int(math.floor(miny / cell_size_m) * cell_size_m)
    x_end = int(math.ceil(maxx / cell_size_m) * cell_size_m)
    y_end = int(math.ceil(maxy / cell_size_m) * cell_size_m)

    cells = []
    for y0 in range(y_start, y_end, cell_size_m):
        for x0 in range(x_start, x_end, cell_size_m):
            cell_laea = box(x0, y0, x0 + cell_size_m, y0 + cell_size_m)
            if not cell_laea.intersects(boundary_laea):
                continue

            x_mp = x0 + cell_size_m // 2
            y_mp = y0 + cell_size_m // 2
            gid = gitter_id_from_origin(x0, y0)
            cell_wgs = transform(to_wgs.transform, cell_laea)

            cells.append(GridCell(
                kommune_id=kommune_id,
                geometry=from_shape(cell_wgs, srid=4326),
                gitter_id=gid,
                x_3035=x_mp,
                y_3035=y_mp,
                row_idx=y_mp // cell_size_m,
                col_idx=x_mp // cell_size_m,
                cell_size_m=cell_size_m,
            ))

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
                "gitter_id": cell.gitter_id,
                "x_3035": cell.x_3035,
                "y_3035": cell.y_3035,
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
