"""GeoPackage export for municipality geodata (boundary + assessment grid + auxiliary)."""

import logging
import os
from datetime import datetime

import numpy as np
import pyogrio.raw as ogr_write
from geoalchemy2.shape import to_shape
from shapely import wkb
from sqlalchemy.orm import Session

from app.data import catalog
from app.models.models import CellAssessment, GridCell, Kommune, ProjectStatus, AssessmentStatus
from app.tasks.assessment_task import TASK_KEY

log = logging.getLogger(__name__)

EXPORTS_BASE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "exports",
)


def get_exports_dir(kommune_id: int) -> str:
    return os.path.join(EXPORTS_BASE, str(kommune_id))


def _build_output_path(kommune_id: int, export_id: int) -> str:
    export_dir = get_exports_dir(kommune_id)
    os.makedirs(export_dir, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"geodaten_{kommune_id}_{export_id}_{ts}.gpkg"
    return os.path.join(export_dir, filename)


def assessment_is_done(db: Session, kommune_id: int) -> bool:
    ps = (
        db.query(ProjectStatus)
        .filter(ProjectStatus.kommune_id == kommune_id, ProjectStatus.task_key == TASK_KEY)
        .first()
    )
    if ps and ps.status == AssessmentStatus.DONE:
        return True
    return (
        db.query(CellAssessment)
        .filter(CellAssessment.kommune_id == kommune_id)
        .count() > 0
    )


def _wkb_array(geometries) -> np.ndarray:
    return np.array([wkb.dumps(g) for g in geometries], dtype=object)


def _write_layer(path: str, layer: str, geometries, field_data: list, fields: list,
                 *, append: bool = False, geometry_type: str = "Polygon"):
    wkb_arr = _wkb_array(geometries)
    np_fields = []
    for col in field_data:
        if col is None:
            np_fields.append(np.array([None] * len(geometries), dtype=object))
        elif isinstance(col[0], str):
            np_fields.append(np.array(col, dtype=object))
        elif isinstance(col[0], (int, np.integer)):
            np_fields.append(np.array(col, dtype=np.int64))
        else:
            np_fields.append(np.array(col, dtype=np.float64))

    ogr_write.write(
        path,
        wkb_arr,
        np_fields,
        fields,
        layer=layer,
        driver="GPKG",
        crs="EPSG:4326",
        geometry_type=geometry_type,
        append=append,
    )


def build_geopackage(db: Session, kommune_id: int, export_id: int) -> str:
    """Build a multi-layer GeoPackage and return the file path."""
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise ValueError("Kommune nicht gefunden")
    if not assessment_is_done(db, kommune_id):
        raise ValueError("Berechnung noch nicht abgeschlossen")
    if kommune.boundary is None:
        raise ValueError("Kommune hat keine Grenze")

    output_path = _build_output_path(kommune_id, export_id)

    boundary = to_shape(kommune.boundary)
    boundary_type = boundary.geom_type if boundary.geom_type in ("Polygon", "MultiPolygon") else "MultiPolygon"
    _write_layer(
        output_path,
        "kommune",
        [boundary],
        [
            [kommune.name or ""],
            [kommune.bundesland or ""],
            [kommune.area_km2 if kommune.area_km2 is not None else 0.0],
            [kommune.population if kommune.population is not None else 0],
        ],
        ["name", "bundesland", "area_km2", "population"],
        geometry_type=boundary_type,
    )

    rows = (
        db.query(CellAssessment, GridCell)
        .join(GridCell, CellAssessment.grid_cell_id == GridCell.id)
        .filter(CellAssessment.kommune_id == kommune_id)
        .all()
    )
    if not rows:
        raise ValueError("Keine Bewertungsdaten vorhanden")

    hazard_codes = [h["code"] for h in catalog.HAZARDS]
    exposure_codes = [e["code"] for e in catalog.EXPOSURES]
    vulnerability_codes = [v["code"] for v in catalog.VULNERABILITIES]
    risk_codes = [r["code"] for r in catalog.RISKS]
    auxiliary_codes = [a["code"] for a in catalog.AUXILIARY]

    geometries = []
    gitter_ids, x3035_vals, y3035_vals = [], [], []
    hazard_cols: dict[str, list] = {c: [] for c in hazard_codes}
    exposure_cols: dict[str, list] = {c: [] for c in exposure_codes}
    vulnerability_cols: dict[str, list] = {c: [] for c in vulnerability_codes}
    risk_index_cols: dict[str, list] = {c: [] for c in risk_codes}
    risk_outcome_cols: dict[str, list] = {f"{c}_outcome": [] for c in risk_codes}
    risk_cost_cols: dict[str, list] = {f"{c}_cost_eur": [] for c in risk_codes}
    auxiliary_cols: dict[str, list] = {c: [] for c in auxiliary_codes}

    for ca, cell in rows:
        data = ca.data or {}
        geometries.append(to_shape(cell.geometry))
        gitter_ids.append(cell.gitter_id or "")
        x3035_vals.append(cell.x_3035)
        y3035_vals.append(cell.y_3035)

        hazards = data.get("hazards", {})
        for code in hazard_codes:
            hazard_cols[code].append(float(hazards.get(code, 0.0)))

        exposures = data.get("exposures", {})
        for code in exposure_codes:
            exposure_cols[code].append(float(exposures.get(code, 0.0)))

        vulnerabilities = data.get("vulnerabilities", {})
        for code in vulnerability_codes:
            vulnerability_cols[code].append(float(vulnerabilities.get(code, 0.0)))

        risks = data.get("risks", {})
        for code in risk_codes:
            rdata = risks.get(code, {})
            risk_index_cols[code].append(float(rdata.get("index", 0.0)))
            risk_outcome_cols[f"{code}_outcome"].append(float(rdata.get("outcome", 0.0)))
            risk_cost_cols[f"{code}_cost_eur"].append(float(rdata.get("cost_eur", 0.0)))

        auxiliary = data.get("auxiliary", {})
        for code in auxiliary_codes:
            val = auxiliary.get(code)
            auxiliary_cols[code].append(float(val) if val is not None else None)

    # Layer: bewertung_100m
    field_data: list = [gitter_ids, x3035_vals, y3035_vals]
    fields = ["gitter_id", "x_3035", "y_3035"]

    for code in hazard_codes:
        field_data.append(hazard_cols[code])
        fields.append(code)
    for code in exposure_codes:
        field_data.append(exposure_cols[code])
        fields.append(code)
    for code in vulnerability_codes:
        field_data.append(vulnerability_cols[code])
        fields.append(code)
    for code in risk_codes:
        field_data.append(risk_index_cols[code])
        fields.append(f"{code}_index")
    for code in risk_codes:
        field_data.append(risk_outcome_cols[f"{code}_outcome"])
        fields.append(f"{code}_outcome")
    for code in risk_codes:
        field_data.append(risk_cost_cols[f"{code}_cost_eur"])
        fields.append(f"{code}_cost_eur")

    _write_layer(
        output_path,
        "bewertung_100m",
        geometries,
        field_data,
        fields,
        append=True,
    )

    # Layer: sonstige_100m
    aux_field_data: list = [gitter_ids, x3035_vals, y3035_vals]
    aux_fields = ["gitter_id", "x_3035", "y_3035"]
    for code in auxiliary_codes:
        aux_field_data.append(auxiliary_cols[code])
        aux_fields.append(code)

    _write_layer(
        output_path,
        "sonstige_100m",
        geometries,
        aux_field_data,
        aux_fields,
        append=True,
    )

    log.info("[EXPORT] GeoPackage erstellt: %s (%d Zellen)", output_path, len(geometries))
    return output_path
