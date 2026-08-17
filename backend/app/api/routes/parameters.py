from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.api.deps import demo_session_id_of
from app.db.database import get_db
from app.models.models import ConfigParameter, Kommune, RiskZone, RiskZoneCell
from app.schemas.schemas import ParameterUpdate
from app.services import artifact_rebuild, parameter_registry
from app.services.export_service import export_parameters_xlsx

router = APIRouter()


def _find_default(parameter_id: str) -> dict | None:
    for p in parameter_registry.catalog_parameters():
        if p["id"] == parameter_id:
            return p
    return None


# Live wirksame Modell-Parameter (Aggregation/Zonen/Maßnahmen-Rechnung zur Laufzeit,
# kein materialisierter Zellwert betroffen).
_LIVE_MODEL_PARAMS = {
    "model.risk_threshold",
    "model.measure_coverage_saturation",
    "model.measure_reduction_cap",
}


def _needs_recalc(parameter_id: str) -> bool:
    """True, wenn ein Parameter-Override eine Neuberechnung der CellAssessment erfordert.

    LIVE wirksam (keine Neuberechnung): Kostensätze ``*.cost_per_outcome`` (aggregate
    monetarisiert live aus dem gespeicherten Outcome), ``*.ref_value`` (für Schicht-B-
    Risiken nur noch Sanity-Anker, für flat-Risiken live in der Aggregation) sowie die
    Modell-Stellschrauben Risikozonen-Schwelle und Maßnahmen-Sättigung/-Kappung
    (werden je Request/Aggregation neu gelesen).

    Alles, was den beim Lauf materialisierten Per-Zell-Wert (Index oder Outcome) bestimmt,
    braucht dagegen eine Neuberechnung: Normgrenzen (``*.norm_min/max``), Impact-Parameter
    (``risks.*.impact.*`` / ``impact.*``), UHI-/Formelparameter, regionale Fallbacks
    (``regional.*``) und die Referenzskalierung ``model.ref_*`` (§8/B2).
    """
    if parameter_id.endswith(".cost_per_outcome") or parameter_id.endswith(".ref_value"):
        return False
    if parameter_id in _LIVE_MODEL_PARAMS:
        return False
    return True


@router.get("/kommune/{kommune_id}/parameters")
def list_parameters(
    kommune_id: int,
    request: Request,
    layer: str | None = Query(None),
    category: str | None = Query(None),
    db: Session = Depends(get_db),
):
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")

    params = parameter_registry.catalog_parameters(layer_code=layer, layer_category=category)
    overrides = parameter_registry.load_db_overrides(db, kommune_id)
    merged = parameter_registry.merge_overrides(params, overrides)

    # Demo: alles read-only; für gesperrte Ebenen Wert/Quelle entfernen.
    if demo_session_id_of(request):
        from app.services import demo_service
        enabled = getattr(request.state, "demo_enabled_layers", set())
        return demo_service.filter_parameters(merged, enabled)
    return merged


@router.put("/kommune/{kommune_id}/parameters")
def update_parameters(
    kommune_id: int,
    updates: list[ParameterUpdate],
    request: Request,
    db: Session = Depends(get_db),
):
    if demo_session_id_of(request):
        raise HTTPException(403, "Parameter sind in der Demo nicht veränderbar")
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")

    results = []
    for u in updates:
        default = _find_default(u.parameter_id)
        if not default:
            raise HTTPException(400, f"Unbekannter Parameter: {u.parameter_id}")

        if u.value != default["default_value"] and not u.custom_source:
            raise HTTPException(
                400,
                f"Quellenangabe (custom_source) erforderlich für Änderung von {u.parameter_id}",
            )

        parts = u.parameter_id.split(".", 1)
        category = parts[0] if len(parts) > 1 else "model"
        key = parts[1] if len(parts) > 1 else u.parameter_id

        param = (
            db.query(ConfigParameter)
            .filter(
                ConfigParameter.kommune_id == kommune_id,
                ConfigParameter.parameter_id == u.parameter_id,
            )
            .first()
        )
        if not param:
            param = ConfigParameter(
                kommune_id=kommune_id,
                category=category,
                key=key,
                parameter_id=u.parameter_id,
                value=u.value,
                source=default.get("source"),
                custom_source=u.custom_source,
                description=default.get("label"),
            )
            db.add(param)
        else:
            param.value = u.value
            param.custom_source = u.custom_source

        results.append({
            "parameter_id": u.parameter_id,
            "status": "updated",
            "overridden": u.value != default["default_value"],
            "recalculation_required": _needs_recalc(u.parameter_id),
        })

    db.commit()
    # Kostensatz-/Modell-Overrides fließen live in die Aggregat-Kosten ein →
    # Datei-Caches invalidieren + entprellter Hintergrund-Rebuild. layers=True,
    # wenn Live-Parameter betroffen sind, die in die Karten-Werte-Dateien
    # gebacken werden (€-Sätze/ref_value in Tooltips/Outcome-Breakdown) —
    # sonst zeigten Karten-Tooltips bis zur nächsten Voll-Berechnung alte Werte.
    live_layer_params = any(
        u.parameter_id.endswith(".cost_per_outcome") or u.parameter_id.endswith(".ref_value")
        for u in updates
    )
    artifact_rebuild.invalidate_and_schedule(kommune_id, layers=live_layer_params)
    # Geänderte Risikozonen-Schwelle: bestehende Zonen der Kommune verwerfen —
    # sie werden beim nächsten Abruf mit der neuen Schwelle lazy neu geclustert.
    if any(u.parameter_id == "model.risk_threshold" for u in updates):
        zone_ids = [z.id for z in db.query(RiskZone.id).filter(RiskZone.kommune_id == kommune_id)]
        if zone_ids:
            db.query(RiskZoneCell).filter(RiskZoneCell.risk_zone_id.in_(zone_ids)).delete(
                synchronize_session=False)
            db.query(RiskZone).filter(RiskZone.id.in_(zone_ids)).delete(synchronize_session=False)
            db.commit()
    return {
        "results": results,
        # Sammelsignal fürs Frontend: mindestens ein geänderter Parameter wirkt erst nach
        # einer Neuberechnung der CellAssessment (Normgrenzen/Impact-Parameter/Gewichte).
        "recalculation_required": any(r["recalculation_required"] for r in results),
    }


@router.get("/kommune/{kommune_id}/parameters/export")
def export_parameters(kommune_id: int, db: Session = Depends(get_db)):
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")

    xlsx_bytes = export_parameters_xlsx(db, kommune_id, kommune.name)
    return Response(
        content=xlsx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=parameter_kommune_{kommune_id}.xlsx"},
    )
