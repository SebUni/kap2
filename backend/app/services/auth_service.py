"""Passwort-Hashing (bcrypt) und DB-Session-Verwaltung für den Login-Bereich.

Sicherheitsmodell:
- Opaques 32-Byte-Token im Cookie; in der DB liegt nur der SHA-256-Hash
  (DB-Leak verrät keine gültigen Tokens).
- Sliding Expiry: jede Nutzung innerhalb der Laufzeit verlängert die Session
  auf SESSION_TTL ab jetzt (höchstens einmal pro Stunde geschrieben, damit
  nicht jeder Request ein UPDATE auslöst).
- Login-Fehler antworten verzögert (Brute-Force-Dämpfung).
"""
import hashlib
import secrets
import time
from datetime import datetime, timedelta

import bcrypt
from sqlalchemy.orm import Session

from app.models.auth_models import User, UserSession

SESSION_TTL = timedelta(days=30)
# Sliding-Expiry-Updates höchstens einmal pro Stunde persistieren.
_TOUCH_INTERVAL = timedelta(hours=1)
LOGIN_FAILURE_DELAY_S = 0.5


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("ascii")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("ascii"))
    except ValueError:
        return False


def _token_hash(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode("ascii")).hexdigest()


def create_session(db: Session, user: User) -> str:
    """Legt eine Session an und gibt das ROHE Token zurück (einzige Stelle)."""
    raw_token = secrets.token_urlsafe(32)
    now = datetime.utcnow()
    db.add(UserSession(
        token_hash=_token_hash(raw_token),
        user_id=user.id,
        created_at=now,
        expires_at=now + SESSION_TTL,
        last_seen_at=now,
    ))
    user.last_login_at = now
    db.commit()
    return raw_token


def resolve_session(db: Session, raw_token: str) -> User | None:
    """Token → aktiver Nutzer (oder None). Verlängert die Session gleitend."""
    if not raw_token:
        return None
    now = datetime.utcnow()
    session = (
        db.query(UserSession)
        .filter(UserSession.token_hash == _token_hash(raw_token))
        .first()
    )
    if not session or session.expires_at < now:
        return None
    user = session.user
    if not user or not user.is_active:
        return None
    if (session.last_seen_at or session.created_at) + _TOUCH_INTERVAL < now:
        session.last_seen_at = now
        session.expires_at = now + SESSION_TTL
        db.commit()
    return user


def revoke_session(db: Session, raw_token: str) -> None:
    if not raw_token:
        return
    db.query(UserSession).filter(
        UserSession.token_hash == _token_hash(raw_token)
    ).delete(synchronize_session=False)
    db.commit()


def revoke_all_sessions(db: Session, user_id: int) -> None:
    """Alle Sessions eines Nutzers beenden (Deaktivierung, Passwort-Reset)."""
    db.query(UserSession).filter(UserSession.user_id == user_id).delete(
        synchronize_session=False
    )
    db.commit()


def purge_expired(db: Session) -> int:
    """Abgelaufene Sessions löschen (Startup + periodisch)."""
    n = db.query(UserSession).filter(
        UserSession.expires_at < datetime.utcnow()
    ).delete(synchronize_session=False)
    db.commit()
    return n


def login(db: Session, email: str, password: str) -> tuple[User, str] | None:
    """E-Mail + Passwort → (User, rohes Session-Token) oder None.

    Antwortet bei Fehlschlag verzögert und prüft auch bei unbekannter E-Mail
    einen Dummy-Hash (konstantere Antwortzeit).
    """
    user = db.query(User).filter(User.email == email.strip().lower()).first()
    if user and user.is_active and verify_password(password, user.password_hash):
        return user, create_session(db, user)
    # Dummy-Verify gegen Timing-Unterschied bekannte/unbekannte E-Mail
    if not user:
        verify_password(password, hash_password("dummy-timing-equalizer"))
    time.sleep(LOGIN_FAILURE_DELAY_S)
    return None
