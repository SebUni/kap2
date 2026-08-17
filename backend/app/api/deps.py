"""FastAPI-Dependencies für Auth, Demo-Sessions und Kommune-Zugriff.

Verdrahtung: die bestehenden Produkt-Router werden in ``main.py`` mit
``dependencies=[Depends(require_kommune_access)]`` gemountet — die Routen-
Dateien selbst bleiben (bis auf Admin-Only-, Demo- und Measure-ID-Checks)
unberührt.

Principals:
- ``User`` (Login-Cookie ``kap2_session``): Admin alles, Nutzer nur
  zugeordnete Kommunen (``user_kommunen``).
- ``DemoActor`` (Demo-Cookie ``kap2_demo``, nur wenn KEIN Login vorliegt):
  ausschließlich die Demo-Kommune, nur GET + Maßnahmen-Schreibpfade, nur
  freigeschaltete Ebenen (Plan §3.4). Der Guard hinterlegt den Demo-Zustand
  auf ``request.state``, damit Routen (Parameter-Stripping, Live-Aggregate)
  darauf reagieren können.
"""
from dataclasses import dataclass, field

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.auth_models import User, user_kommunen
from app.models.demo_models import DemoSession
from app.models.models import AdaptationMeasure
from app.services import auth_service, demo_service

SESSION_COOKIE = "kap2_session"


@dataclass
class DemoActor:
    """Demo-Principal: anonyme Session + Demo-Konfiguration."""
    session: DemoSession
    kommune_id: int
    risk_codes: list[str]
    enabled_layers: set[str] = field(default_factory=set)
    measure_limit: int = 10

    is_admin = False

    @property
    def session_id(self) -> str:
        return self.session.id


Actor = User | DemoActor


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User | None:
    """Login-Cookie → Nutzer (oder None). Wirft nie."""
    token = request.cookies.get(SESSION_COOKIE)
    if not token:
        return None
    return auth_service.resolve_session(db, token)


def get_demo_actor(request: Request, db: Session) -> DemoActor | None:
    """Demo-Cookie → DemoActor, sofern Demo konfiguriert und Session lebt."""
    session_id = request.cookies.get(demo_service.DEMO_COOKIE)
    if not session_id:
        return None
    cfg = demo_service.get_config(db)
    if not cfg.get("kommune_id"):
        return None
    session = demo_service.resolve_session(db, session_id)
    if not session:
        return None
    return DemoActor(
        session=session,
        kommune_id=int(cfg["kommune_id"]),
        risk_codes=list(cfg.get("risk_codes", [])),
        enabled_layers=demo_service.enabled_layers(cfg.get("risk_codes", [])),
        measure_limit=int(cfg.get("measure_limit", 10)),
    )


def require_user(user: User | None = Depends(get_current_user)) -> User:
    if user is None:
        raise HTTPException(401, "Nicht angemeldet")
    return user


def require_admin(user: User = Depends(require_user)) -> User:
    if not user.is_admin:
        raise HTTPException(403, "Nur für Administratoren")
    return user


def user_kommune_ids(db: Session, user: User) -> set[int]:
    rows = db.execute(
        user_kommunen.select().where(user_kommunen.c.user_id == user.id)
    ).all()
    return {r.kommune_id for r in rows}


def has_kommune_access(db: Session, user: User, kommune_id: int) -> bool:
    if user.is_admin:
        return True
    row = db.execute(
        user_kommunen.select().where(
            user_kommunen.c.user_id == user.id,
            user_kommunen.c.kommune_id == kommune_id,
        )
    ).first()
    return row is not None


# ── Demo-Regelwerk (Plan §3.4) ──────────────────────────────────────────────

# Schreibzugriff nur auf Maßnahmen-Pfade — aber nicht Import/Export.
_DEMO_WRITE_ALLOWED_MARKER = "/measures"
_DEMO_BLOCKED_MARKERS = ("/export", "/import", "/kommune/search")


def _check_demo_access(request: Request, actor: DemoActor) -> None:
    path = request.url.path
    method = request.method.upper()

    for marker in _DEMO_BLOCKED_MARKERS:
        if marker in path:
            raise HTTPException(403, "In der Demo nicht verfügbar")

    raw = request.path_params.get("kommune_id")
    if raw is not None and int(raw) != actor.kommune_id:
        raise HTTPException(403, "Demo-Zugriff nur auf die Demo-Kommune")

    if method not in ("GET", "HEAD", "OPTIONS"):
        if _DEMO_WRITE_ALLOWED_MARKER not in path:
            raise HTTPException(403, "In der Demo nicht veränderbar (nur Maßnahmen)")

    # Ebenen-Whitelist: /layer/{code}, /layer/{code}/values,
    # /risk-zones/{risk_code}, /catalog/layer/{code}/recipe
    code = request.path_params.get("code") or request.path_params.get("risk_code")
    if code and code not in actor.enabled_layers:
        raise HTTPException(403, "Diese Ebene ist in der Demo nicht freigeschaltet")


def _mark_demo_request(request: Request, actor: DemoActor) -> None:
    request.state.demo_session_id = actor.session_id
    request.state.demo_risk_codes = actor.risk_codes
    request.state.demo_enabled_layers = actor.enabled_layers


def demo_session_id_of(request: Request) -> str | None:
    """Für Routen: Demo-Session-ID des Requests (oder None im Produktpfad)."""
    return getattr(request.state, "demo_session_id", None)


# ── Router-Level-Guards ─────────────────────────────────────────────────────

def require_actor(
    request: Request,
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user),
) -> Actor:
    """Login ODER Demo-Session (Login hat Vorrang)."""
    if user is not None:
        return user
    demo = get_demo_actor(request, db)
    if demo is not None:
        _check_demo_access(request, demo)
        _mark_demo_request(request, demo)
        return demo
    raise HTTPException(401, "Nicht angemeldet")


def require_kommune_access(
    request: Request,
    db: Session = Depends(get_db),
    actor: Actor = Depends(require_actor),
) -> Actor:
    """Router-Level-Guard: erzwingt Login/Demo und, falls die Route eine
    ``kommune_id`` trägt, die Kommune-Zuordnung."""
    if isinstance(actor, DemoActor):
        return actor  # Demo-Regeln liefen bereits in require_actor
    raw = request.path_params.get("kommune_id")
    if raw is None:
        return actor
    try:
        kommune_id = int(raw)
    except (TypeError, ValueError):
        raise HTTPException(422, "Ungültige kommune_id")
    if not has_kommune_access(db, actor, kommune_id):
        raise HTTPException(403, "Kein Zugriff auf diese Kommune")
    return actor


def assert_measure_access(db: Session, actor: Actor, measure: AdaptationMeasure) -> None:
    """Für Maßnahmen-ID-Routen ohne ``kommune_id`` im Pfad."""
    if isinstance(actor, DemoActor):
        if measure.demo_session_id != actor.session_id:
            raise HTTPException(403, "Kein Zugriff auf diese Maßnahme")
        return
    # Produkt: nur NULL-Session-Maßnahmen zugeordneter Kommunen
    if measure.demo_session_id is not None:
        raise HTTPException(403, "Kein Zugriff auf diese Maßnahme")
    if not has_kommune_access(db, actor, measure.kommune_id):
        raise HTTPException(403, "Kein Zugriff auf diese Kommune")
