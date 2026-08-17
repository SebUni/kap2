"""Pydantic-Schemas für den KI-Assistenten (Einstellungen, Nutzung, Chat).

Die Validierungsgrenzen sind bewusst Teil der Sicherheitsarchitektur:
- Rollen sind auf 'user'/'assistant' beschränkt → der Client kann keine
  'system'-Nachricht einschleusen (Prompt-Injection-Schutz).
- Längen- und Anzahllimits deckeln die pro Anfrage verarbeiteten Tokens
  (Kosten-Backstop, ergänzend zum Tages-/Monatskontingent).
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator


# ── Einstellungen ────────────────────────────────────────────────────────────

class AiSettingsUpdate(BaseModel):
    # Alle Felder optional → partielles Update. Ein weggelassenes api_key-Feld
    # lässt den gespeicherten Schlüssel unangetastet (nie versehentlich löschen).
    api_key: Optional[str] = Field(default=None, max_length=200)
    model: Optional[str] = Field(default=None, max_length=50)
    monthly_token_limit: Optional[int] = Field(default=None, ge=0)
    daily_token_limit: Optional[int] = Field(default=None, ge=0)


class AiSettingsOut(BaseModel):
    api_key_set: bool
    api_key_hint: Optional[str] = None  # nur die letzten 4 Zeichen, nie der Schlüssel
    model: str
    monthly_token_limit: int
    daily_token_limit: int


# ── Nutzung ──────────────────────────────────────────────────────────────────

class UsageScope(BaseModel):
    used: int
    limit: int


class AiUsageOut(BaseModel):
    day: UsageScope
    month: UsageScope
    blocked: bool


# ── Chat ─────────────────────────────────────────────────────────────────────

# Nutzereingaben werden knapp gedeckelt (Kosten-/Missbrauchs-Backstop).
# Assistenten-Nachrichten sind unsere eigenen, bereits über max_response_tokens
# begrenzten Antworten; sie werden im Folge-Turn als Historie zurückgeschickt und
# überschreiten das Nutzer-Limit regelmäßig (2000 Tokens ≈ mehrere Tausend Zeichen).
# Daher rollenabhängige Obergrenzen — sonst 422 beim zweiten Chat-Turn.
_USER_MAX_CHARS = 4000
_ASSISTANT_MAX_CHARS = 24000


class ChatMessageIn(BaseModel):
    role: Literal["user", "assistant"]  # 'system' bewusst nicht erlaubt
    content: str = Field(min_length=1, max_length=_ASSISTANT_MAX_CHARS)

    @model_validator(mode="after")
    def _limit_user_length(self) -> "ChatMessageIn":
        if self.role == "user" and len(self.content) > _USER_MAX_CHARS:
            raise ValueError(
                f"Nutzernachricht zu lang (max. {_USER_MAX_CHARS} Zeichen)"
            )
        return self


class ChatRequest(BaseModel):
    messages: list[ChatMessageIn] = Field(min_length=1, max_length=24)
    kommune_id: Optional[int] = None
