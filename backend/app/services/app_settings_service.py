"""Zugriff auf globale Betreiber-Einstellungen (Tabelle app_settings).

Kapselt Lesen/Schreiben der KI-Assistent-Konfiguration mit sinnvollen Defaults.
Der API-Schlüssel wird zusätzlich per Env-Variable (MISTRAL_API_KEY) überschreibbar
gemacht — nützlich für Deployments, die Secrets nicht in der DB halten wollen.
"""
from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.config import settings as env_settings
from app.models.demo_models import AppSetting  # bestehender globaler Key-Value-Store


# Default-Werte + zentrale Schlüssel-Liste. Limits sind großzügig, aber endlich
# (Missbrauchs-/Kosten-Backstop). Ein Token ≈ 3–4 Zeichen; 200k/Tag reichen für
# viele Berichtsentwürfe, 2 Mio/Monat sind ein harter Kostendeckel.
DEFAULTS: dict[str, Any] = {
    "ai_model": "mistral-medium-latest",
    "ai_monthly_token_limit": 2_000_000,
    "ai_daily_token_limit": 200_000,
    "ai_max_response_tokens": 2000,
}

_API_KEY = "ai_api_key"


def get_setting(db: Session, key: str, default: Any = None) -> Any:
    row = db.get(AppSetting, key)
    if row is None or row.value is None:
        return DEFAULTS.get(key, default)
    return row.value


def set_setting(db: Session, key: str, value: Any) -> None:
    row = db.get(AppSetting, key)
    if row is None:
        row = AppSetting(key=key, value=value)
        db.add(row)
    else:
        row.value = value
    db.commit()


def get_api_key(db: Session) -> str:
    """Effektiver Mistral-API-Schlüssel: Env-Override hat Vorrang vor DB-Wert."""
    if env_settings.MISTRAL_API_KEY:
        return env_settings.MISTRAL_API_KEY
    return str(get_setting(db, _API_KEY, "") or "")


def set_api_key(db: Session, key: str) -> None:
    set_setting(db, _API_KEY, key)


def get_ai_settings(db: Session) -> dict[str, Any]:
    """Alle KI-Einstellungen mit angewandten Defaults (ohne den Klartext-Key)."""
    return {
        "model": str(get_setting(db, "ai_model")),
        "monthly_token_limit": int(get_setting(db, "ai_monthly_token_limit")),
        "daily_token_limit": int(get_setting(db, "ai_daily_token_limit")),
        "max_response_tokens": int(get_setting(db, "ai_max_response_tokens")),
    }
