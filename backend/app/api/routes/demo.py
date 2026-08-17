"""Öffentliche Demo-Endpunkte: Session-Bootstrap + Meta (ohne Login).

Die Demo-Session ist ein Browser-Session-Cookie OHNE Max-Age → sie stirbt,
wenn der Browser schließt; die zugehörigen Maßnahmen werden zusätzlich
serverseitig per TTL-Sweep entfernt (demo_service).
"""
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session

from app.data import catalog
from app.db.database import get_db
from app.services import demo_service

router = APIRouter()


def _meta(db: Session) -> dict:
    cfg = demo_service.get_config(db)
    kommune_id = cfg.get("kommune_id")
    if not kommune_id:
        raise HTTPException(404, "Demo ist derzeit nicht verfügbar")
    risk_codes = cfg.get("risk_codes", [])
    enabled = demo_service.enabled_layers(risk_codes)
    risks = [
        {"code": c, "name": catalog.RISKS_BY_CODE[c]["name"],
         "group": catalog.RISKS_BY_CODE[c].get("group"),
         "unit": catalog.RISKS_BY_CODE[c].get("outcome_unit", "")}
        for c in risk_codes if c in catalog.RISKS_BY_CODE
    ]
    return {
        "kommune_id": kommune_id,
        "risks": risks,
        "enabled_layers": sorted(enabled),
        "measure_limit": cfg.get("measure_limit", 10),
    }


@router.get("/meta")
def demo_meta(db: Session = Depends(get_db)):
    """Demo-Konfiguration für das Frontend (freigeschaltete Risiken/Ebenen)."""
    return _meta(db)


@router.post("/session")
def demo_session(request: Request, response: Response, db: Session = Depends(get_db)):
    """Stellt eine Demo-Session sicher (Cookie ohne Max-Age) und liefert Meta."""
    meta = _meta(db)  # 404, falls Demo nicht konfiguriert
    existing = request.cookies.get(demo_service.DEMO_COOKIE)
    session = demo_service.resolve_session(db, existing) if existing else None
    if session is None:
        session = demo_service.create_session(db)
    response.set_cookie(
        demo_service.DEMO_COOKIE,
        session.id,
        httponly=True,
        samesite="lax",
        path="/",
        # KEIN max_age → Browser-Session-Cookie (weg beim Schließen).
    )
    return {"session_id": session.id, **meta}
