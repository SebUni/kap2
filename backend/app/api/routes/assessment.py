import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.data import catalog
from app.models.models import (
    Kommune, CellAssessment, GridCell, ProjectStatus, AssessmentStatus,
)
from app.tasks.assessment_task import (
    run_assessment_background, abort_assessment, TASK_KEY,
)
from app.services.measure_service import get_risk_aggregate
from app.services.engine import risk_engine
from app.services.engine import formulas
from app.services.engine.formulas import build_regional_context
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
    if code in catalog.RISKS_BY_CODE:
        return "risks"
    return None


@router.post("/kommune/{kommune_id}/assess")
def start_assessment(kommune_id: int, db: Session = Depends(get_db)):
    """Startet die vollständige KAP3-Bewertung im Hintergrund."""
    cell_count = db.query(GridCell).filter(GridCell.kommune_id == kommune_id).count()
    if cell_count == 0:
        raise HTTPException(400, "Keine Grid-Zellen vorhanden. Bitte zuerst Grid generieren.")

    ps = (db.query(ProjectStatus)
          .filter(ProjectStatus.kommune_id == kommune_id, ProjectStatus.task_key == TASK_KEY)
          .first())
    if not ps:
        ps = ProjectStatus(kommune_id=kommune_id, task_key=TASK_KEY, level=1)
        db.add(ps)
    ps.status = AssessmentStatus.RUNNING
    ps.progress_pct = 0.0
    ps.message = "Berechnung wird vorbereitet …"
    ps.started_at = datetime.utcnow()
    ps.finished_at = None
    db.commit()

    run_assessment_background(kommune_id)
    return {"message": "Berechnung gestartet", "kommune_id": kommune_id}


@router.post("/kommune/{kommune_id}/assess/abort")
def abort_running_assessment(kommune_id: int, db: Session = Depends(get_db)):
    aborted = abort_assessment(kommune_id)
    if aborted:
        ps = (db.query(ProjectStatus)
              .filter(ProjectStatus.kommune_id == kommune_id, ProjectStatus.task_key == TASK_KEY)
              .first())
        if ps:
            ps.status = AssessmentStatus.ERROR
            ps.message = "Berechnung abgebrochen"
            db.commit()
        return {"message": "Berechnung wird abgebrochen", "aborted": True}
    return {"message": "Keine laufende Berechnung gefunden", "aborted": False}


@router.get("/kommune/{kommune_id}/status")
def get_status(kommune_id: int, db: Session = Depends(get_db)):
    ps = (db.query(ProjectStatus)
          .filter(ProjectStatus.kommune_id == kommune_id, ProjectStatus.task_key == TASK_KEY)
          .first())
    if not ps:
        return {"status": None, "progress_pct": 0.0, "message": None,
                "step_history": [], "eta_seconds": None}
    return {
        "status": ps.status.value if ps.status else None,
        "progress_pct": ps.progress_pct,
        "message": ps.message,
        "started_at": ps.started_at.isoformat() if ps.started_at else None,
        "finished_at": ps.finished_at.isoformat() if ps.finished_at else None,
        "step_history": ps.step_history or [],
        "eta_seconds": ps.eta_seconds,
    }


@router.get("/kommune/{kommune_id}/layer/{code}")
def get_layer(kommune_id: int, code: str, db: Session = Depends(get_db)):
    """GeoJSON einer einzelnen Ebene (H/E/V-Code oder Risiko-Code).

    Property ``value`` enthält den darzustellenden Wert in absoluter Einheit
    (H/E/V und Risiken). ``meta`` liefert Min/Max für die Legende.
    """
    category = _layer_category(code)
    if not category:
        raise HTTPException(404, f"Unbekannter Code: {code}")

    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")

    try:
        is_coastal = (kommune.bundesland or "") in COASTAL_BUNDESLAENDER
        regional = build_regional_context(kommune.bundesland, is_coastal)
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
                "row": cell.row_idx,
                "col": cell.col_idx,
            }
            if category == "risks":
                rdef = catalog.RISKS_BY_CODE[code]
                idx = float(data.get("risks", {}).get(code, {}).get("index", 0.0))
                cell_pop = float(data.get("inputs", {}).get("pop", 0.0))
                value = risk_engine.cell_outcome(rdef, idx, cell_pop)
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
            else:
                raw = data.get(category, {}).get(code)
                value = float(raw) if raw is not None else 0.0
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
            meta.update({"label": m["name"], "unit": m["unit"], "scale_max": m.get("norm_max")})

        return {"type": "FeatureCollection", "features": features, "meta": meta}
    except HTTPException:
        raise
    except Exception as exc:
        log.exception("get_layer failed kommune=%s code=%s", kommune_id, code)
        raise HTTPException(500, f"Layer konnte nicht geladen werden: {exc}") from exc


@router.get("/kommune/{kommune_id}/risk-summary")
def risk_summary(kommune_id: int, db: Session = Depends(get_db)):
    """Aggregiertes Risiko (Basis, ohne Maßnahmen): Gruppen + Einzelrisiken."""
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")
    return get_risk_aggregate(db, kommune_id, apply_measures=False)


@router.get("/kommune/{kommune_id}/risk-histogram")
def risk_histogram(kommune_id: int, db: Session = Depends(get_db)):
    """Häufigkeitsverteilung der Risiko-Index-Höhen je Risiko (20 Bins à 5, 0-100).

    Liefert pro Risiko die Zellanzahl je Index-Klasse plus Outcome-/Index-Kennzahlen.
    Botschaft: wenige hohe Zellen → punktuelle Maßnahmen; viele hohe → flächendeckend.
    """
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")

    N_BINS = 20
    WIDTH = 5.0  # 0..100
    bins_labels = [f"{int(i * WIDTH)}-{int((i + 1) * WIDTH)}" for i in range(N_BINS)]
    bin_centers = [round((i + 0.5) * WIDTH, 1) for i in range(N_BINS)]

    rows = (
        db.query(CellAssessment)
        .filter(CellAssessment.kommune_id == kommune_id)
        .all()
    )
    total_cells = len(rows)

    counts: dict[str, list[int]] = {r["code"]: [0] * N_BINS for r in catalog.RISKS}
    nonzero: dict[str, int] = {r["code"]: 0 for r in catalog.RISKS}
    for ca in rows:
        risks = (ca.data or {}).get("risks", {})
        for code, r in risks.items():
            if code not in counts:
                continue
            idx = float(r.get("index", 0.0))
            b = min(N_BINS - 1, max(0, int(idx // WIDTH)))
            counts[code][b] += 1
            if idx > 0.0:
                nonzero[code] += 1

    # Outcome/Index-Kennzahlen aus dem Aggregat (mit/ohne Maßnahmen = Basis)
    agg = get_risk_aggregate(db, kommune_id, apply_measures=False)

    risks_out: dict[str, dict] = {}
    for risk in catalog.RISKS:
        code = risk["code"]
        a = agg["risks"].get(code, {})
        risks_out[code] = {
            "name": risk["name"],
            "group": risk["group"],
            "outcome_unit": risk["outcome_unit"],
            "cost_dimension": risk["cost_dimension"],
            "counts": counts[code],
            "nonzero_cells": nonzero[code],
            "p90_index": a.get("index", 0.0),
            "max_index": a.get("max_index", 0.0),
            "outcome": a.get("outcome", 0.0),
            "cost_eur": a.get("cost_eur", 0.0),
        }

    return {
        "total_cells": total_cells,
        "bin_labels": bins_labels,
        "bin_centers": bin_centers,
        "bin_width": WIDTH,
        "risks": risks_out,
    }


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
