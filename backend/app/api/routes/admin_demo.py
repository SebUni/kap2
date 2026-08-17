"""Admin: Demo-Konfiguration (Kommune, 3 Risiken, Limit, TTL) + Aufräumen."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.data import catalog
from app.db.database import get_db
from app.models.models import Kommune
from app.services import demo_service
from app.services.geodata_export_service import assessment_is_done

router = APIRouter()


class DemoConfigUpdate(BaseModel):
    kommune_id: int | None = None
    risk_codes: list[str] | None = None
    measure_limit: int | None = None
    session_ttl_h: int | None = None


@router.get("/demo/config")
def get_demo_config(db: Session = Depends(get_db)):
    cfg = demo_service.get_config(db)
    ttl_h = cfg.get("session_ttl_h", 24)
    kommune = None
    if cfg.get("kommune_id"):
        k = db.query(Kommune).filter(Kommune.id == cfg["kommune_id"]).first()
        if k:
            kommune = {"id": k.id, "name": k.name}
    return {
        **cfg,
        "kommune": kommune,
        "active_sessions": demo_service.active_session_count(db, ttl_h),
        "risk_options": [
            {"code": r["code"], "name": r["name"], "group": r.get("group")}
            for r in catalog.RISKS
        ],
    }


@router.put("/demo/config")
def update_demo_config(data: DemoConfigUpdate, db: Session = Depends(get_db)):
    updates = data.model_dump(exclude_none=True)
    if "kommune_id" in updates and updates["kommune_id"] is not None:
        k = db.query(Kommune).filter(Kommune.id == updates["kommune_id"]).first()
        if not k:
            raise HTTPException(404, "Kommune nicht gefunden")
        if not assessment_is_done(db, k.id):
            raise HTTPException(400, "Demo-Kommune muss eine fertige Berechnung haben")
    try:
        cfg = demo_service.set_config(db, updates)
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    return cfg


@router.post("/demo/cleanup")
def cleanup_demo_sessions(db: Session = Depends(get_db)):
    """Alle abgelaufenen Demo-Sessions jetzt entfernen (Maßnahmen kaskadieren)."""
    n = demo_service.sweep_expired(db)
    return {"removed": n}
