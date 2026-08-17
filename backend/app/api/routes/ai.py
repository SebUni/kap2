"""KI-Assistent (Mistral): Einstellungen, Nutzung, Chat-Streaming.

Absicherung (nutzt das bestehende Auth-System, app/api/deps.py):
- /settings (GET+PUT): admin-only — Betreiber-Konfiguration (API-Schlüssel, Modell,
  Limits). Der Schlüssel wird nie zurückgegeben (nur Vorhanden-Flag + letzte 4 Zeichen).
- /usage (GET) + /chat (POST): eingeloggte Nutzer. /chat prüft zusätzlich den
  Kommune-Zugriff des Nutzers (kommune_id steckt im Body, nicht im Pfad — der
  Router-Level-Guard require_kommune_access greift dort nicht, daher hier explizit).
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session

from app.api.deps import has_kommune_access, require_admin, require_user
from app.db.database import get_db
from app.models.auth_models import User
from app.schemas.ai import AiSettingsOut, AiSettingsUpdate, AiUsageOut, ChatRequest
from app.services import ai_context_service, app_settings_service, chat_service

router = APIRouter()


def _settings_payload(db: Session) -> AiSettingsOut:
    key = app_settings_service.get_api_key(db)
    s = app_settings_service.get_ai_settings(db)
    return AiSettingsOut(
        api_key_set=bool(key),
        api_key_hint=(key[-4:] if key else None),  # nur letzte 4 Zeichen, nie der Key
        model=s["model"],
        monthly_token_limit=s["monthly_token_limit"],
        daily_token_limit=s["daily_token_limit"],
    )


@router.get("/settings", response_model=AiSettingsOut)
def get_settings(db: Session = Depends(get_db), _admin: User = Depends(require_admin)):
    return _settings_payload(db)


@router.put("/settings", response_model=AiSettingsOut)
def update_settings(
    payload: AiSettingsUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    if payload.api_key:  # nur bei nicht-leerem Wert schreiben → nie versehentlich löschen
        app_settings_service.set_api_key(db, payload.api_key)
    if payload.model is not None:
        app_settings_service.set_setting(db, "ai_model", payload.model)
    if payload.monthly_token_limit is not None:
        app_settings_service.set_setting(db, "ai_monthly_token_limit", payload.monthly_token_limit)
    if payload.daily_token_limit is not None:
        app_settings_service.set_setting(db, "ai_daily_token_limit", payload.daily_token_limit)
    return _settings_payload(db)


@router.get("/usage", response_model=AiUsageOut)
def get_usage(db: Session = Depends(get_db), _user: User = Depends(require_user)):
    return chat_service.usage_snapshot(db)


@router.post("/chat")
def chat(
    payload: ChatRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_user),
):
    # Kommune-Zugriff explizit prüfen (kommune_id im Body, nicht im Pfad).
    if payload.kommune_id is not None and not has_kommune_access(db, user, payload.kommune_id):
        raise HTTPException(403, "Kein Zugriff auf diese Kommune")

    api_key = app_settings_service.get_api_key(db)
    if not api_key:
        return JSONResponse(status_code=400, content={"code": "no_api_key"})

    ai = app_settings_service.get_ai_settings(db)
    context = ai_context_service.build_context(db, payload.kommune_id)
    history = [{"role": m.role, "content": m.content} for m in payload.messages]
    messages = chat_service.build_messages(context, history)

    prompt_chars = sum(len(m["content"]) for m in messages)
    estimate = chat_service.estimate_tokens(
        "".join(m["content"] for m in messages), ai["max_response_tokens"]
    )
    try:
        chat_service.check_quota(db, estimate)
    except chat_service.QuotaExceeded as q:
        return JSONResponse(status_code=429, content={
            "code": "quota_exceeded", "scope": q.scope, "used": q.used, "limit": q.limit,
        })

    generator = chat_service.stream_chat(
        api_key=api_key,
        model=ai["model"],
        messages=messages,
        max_response_tokens=ai["max_response_tokens"],
        kommune_id=payload.kommune_id,
        prompt_chars=prompt_chars,
    )
    return StreamingResponse(
        generator,
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
