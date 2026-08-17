"""Login/Logout/Me/Passwort — öffentlicher Auth-Endpunkt (Session-Cookie)."""
import os

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import SESSION_COOKIE, get_current_user, require_user
from app.db.database import get_db
from app.models.auth_models import User
from app.services import auth_service

router = APIRouter()

# Secure-Flag nur setzen, wenn hinter HTTPS betrieben (Prod); lokal (http) aus.
_COOKIE_SECURE = os.environ.get("KAP2_COOKIE_SECURE", "0") == "1"


class LoginRequest(BaseModel):
    email: str
    password: str


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


def _user_out(user: User) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "display_name": user.display_name,
        "role": user.role,
    }


def _set_session_cookie(response: Response, raw_token: str) -> None:
    response.set_cookie(
        SESSION_COOKIE,
        raw_token,
        max_age=int(auth_service.SESSION_TTL.total_seconds()),
        httponly=True,
        samesite="lax",
        secure=_COOKIE_SECURE,
        path="/",
    )


@router.post("/login")
def login(data: LoginRequest, response: Response, db: Session = Depends(get_db)):
    result = auth_service.login(db, data.email, data.password)
    if result is None:
        raise HTTPException(401, "E-Mail oder Passwort falsch")
    user, raw_token = result
    _set_session_cookie(response, raw_token)
    return _user_out(user)


@router.post("/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    token = request.cookies.get(SESSION_COOKIE)
    if token:
        auth_service.revoke_session(db, token)
    response.delete_cookie(SESSION_COOKIE, path="/")
    return {"message": "Abgemeldet"}


@router.get("/me")
def me(user: User | None = Depends(get_current_user)):
    if user is None:
        return {"authenticated": False}
    return {"authenticated": True, "user": _user_out(user)}


@router.post("/change-password")
def change_password(
    data: ChangePasswordRequest,
    response: Response,
    db: Session = Depends(get_db),
    user: User = Depends(require_user),
):
    if not auth_service.verify_password(data.current_password, user.password_hash):
        raise HTTPException(403, "Aktuelles Passwort falsch")
    if len(data.new_password) < 8:
        raise HTTPException(400, "Neues Passwort muss mindestens 8 Zeichen haben")
    user.password_hash = auth_service.hash_password(data.new_password)
    db.commit()
    # Alle anderen Sessions beenden, die aktuelle bleibt via neuem Cookie gültig.
    auth_service.revoke_all_sessions(db, user.id)
    _set_session_cookie(response, auth_service.create_session(db, user))
    return {"message": "Passwort geändert"}
