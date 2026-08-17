"""Öffentliche Kontakt-/Beratungsanfrage (Lead) — ohne Login, rate-limited.

Leads landen als JSON-Zeilen in ``backend/data/leads/leads.jsonl`` (append-only,
kein Mail-Server nötig; Admin-UI kann die Datei später anzeigen). Ein sehr
einfaches In-Process-Rate-Limit dämpft Missbrauch.
"""
import json
import logging
import os
import re
import threading
import time
from datetime import datetime

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from app.config import settings

log = logging.getLogger(__name__)
router = APIRouter()

LEADS_DIR = os.path.join(os.path.dirname(settings.ZENSUS_DATA_DIR), "leads")
LEADS_FILE = os.path.join(LEADS_DIR, "leads.jsonl")

# Rate-Limit: max. N Anfragen pro IP pro Stunde (in-process, reicht für v1).
_RATE_LIMIT = 5
_RATE_WINDOW_S = 3600
_rate_lock = threading.Lock()
_rate_buckets: dict[str, list[float]] = {}

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class ContactRequest(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    email: str = Field(max_length=255)
    organisation: str = Field(default="", max_length=255)
    message: str = Field(min_length=5, max_length=5000)


def _rate_limited(ip: str) -> bool:
    now = time.time()
    with _rate_lock:
        bucket = [t for t in _rate_buckets.get(ip, []) if now - t < _RATE_WINDOW_S]
        if len(bucket) >= _RATE_LIMIT:
            _rate_buckets[ip] = bucket
            return True
        bucket.append(now)
        _rate_buckets[ip] = bucket
        return False


@router.post("/contact")
def submit_contact(data: ContactRequest, request: Request):
    ip = request.client.host if request.client else "unknown"
    if _rate_limited(ip):
        raise HTTPException(429, "Zu viele Anfragen — bitte später erneut versuchen.")
    if not _EMAIL_RE.match(data.email.strip()):
        raise HTTPException(400, "Ungültige E-Mail-Adresse")

    os.makedirs(LEADS_DIR, exist_ok=True)
    entry = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "name": data.name.strip(),
        "email": data.email.strip(),
        "organisation": data.organisation.strip(),
        "message": data.message.strip(),
        "ip": ip,
    }
    with open(LEADS_FILE, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    log.info("Kontaktanfrage von %s (%s)", entry["email"], entry["organisation"] or "-")
    return {"message": "Vielen Dank — wir melden uns zeitnah."}
