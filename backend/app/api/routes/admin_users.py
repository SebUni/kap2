"""Admin: Nutzerverwaltung (anlegen, Rolle/Status, Kommune-Zuordnung, PW-Reset)."""
import secrets

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.auth_models import ROLE_ADMIN, ROLE_USER, User, user_kommunen
from app.models.models import Kommune
from app.services import auth_service

router = APIRouter()


class UserCreate(BaseModel):
    email: str
    display_name: str | None = None
    role: str = ROLE_USER
    password: str | None = None  # None → zufälliges Initialpasswort
    kommune_ids: list[int] = []


class UserUpdate(BaseModel):
    display_name: str | None = None
    role: str | None = None
    is_active: bool | None = None
    kommune_ids: list[int] | None = None
    password: str | None = None


def _user_out(db: Session, u: User) -> dict:
    rows = db.execute(
        user_kommunen.select().where(user_kommunen.c.user_id == u.id)).all()
    kids = [r.kommune_id for r in rows]
    kommunen = []
    if kids:
        for k in db.query(Kommune).filter(Kommune.id.in_(kids)).all():
            kommunen.append({"id": k.id, "name": k.name})
    return {
        "id": u.id, "email": u.email, "display_name": u.display_name,
        "role": u.role, "is_active": u.is_active,
        "kommunen": kommunen,
        "last_login_at": u.last_login_at.isoformat() if u.last_login_at else None,
    }


def _set_kommunen(db: Session, user_id: int, kommune_ids: list[int]) -> None:
    db.execute(user_kommunen.delete().where(user_kommunen.c.user_id == user_id))
    for kid in set(kommune_ids):
        db.execute(user_kommunen.insert().values(user_id=user_id, kommune_id=kid))
    db.commit()


@router.get("/users")
def list_users(db: Session = Depends(get_db)):
    return [_user_out(db, u) for u in db.query(User).order_by(User.email).all()]


@router.post("/users")
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    email = data.email.strip().lower()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(409, "E-Mail bereits vergeben")
    if data.role not in (ROLE_ADMIN, ROLE_USER):
        raise HTTPException(400, "Ungültige Rolle")
    password = data.password or secrets.token_urlsafe(9)
    user = User(
        email=email, display_name=data.display_name or email.split("@")[0],
        role=data.role, is_active=True,
        password_hash=auth_service.hash_password(password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    if data.kommune_ids:
        _set_kommunen(db, user.id, data.kommune_ids)
    out = _user_out(db, user)
    # Initialpasswort nur bei Erstellung zurückgeben (Admin gibt es weiter).
    out["initial_password"] = password
    return out


@router.patch("/users/{user_id}")
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "Nutzer nicht gefunden")
    if data.display_name is not None:
        user.display_name = data.display_name
    if data.role is not None:
        if data.role not in (ROLE_ADMIN, ROLE_USER):
            raise HTTPException(400, "Ungültige Rolle")
        user.role = data.role
    if data.is_active is not None:
        user.is_active = data.is_active
        if not data.is_active:
            auth_service.revoke_all_sessions(db, user.id)  # sofort abmelden
    result = {}
    if data.password:
        user.password_hash = auth_service.hash_password(data.password)
        auth_service.revoke_all_sessions(db, user.id)
    db.commit()
    if data.kommune_ids is not None:
        _set_kommunen(db, user.id, data.kommune_ids)
    return {**_user_out(db, user), **result}
