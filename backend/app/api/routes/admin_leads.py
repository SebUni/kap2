"""Admin: Kontaktanfragen (Leads) lesbar machen.

Liest die JSON-Zeilen aus ``backend/data/leads/leads.jsonl`` (geschrieben von
``app/api/routes/contact.py``, ``POST /api/public/contact``). Reine Lese-
Schnittstelle — keine Änderung an Datei, Format oder Schreibpfad.
"""
import json
import os

from fastapi import APIRouter

from app.api.routes.contact import LEADS_FILE

router = APIRouter()


def read_leads(path: str, limit: int = 100) -> list[dict]:
    """Liest die JSON-Zeilen aus ``path``, neueste zuerst, höchstens ``limit``.

    Fehlt die Datei, wird eine leere Liste geliefert. Zeilen, die sich nicht
    als JSON parsen lassen, werden übersprungen (Aufruf schlägt nicht fehl).
    """
    if not os.path.isfile(path):
        return []
    entries: list[dict] = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    entries.reverse()
    return entries[:limit]


@router.get("/leads")
def list_leads(limit: int = 100):
    gesamt = 0
    if os.path.isfile(LEADS_FILE):
        with open(LEADS_FILE, "r", encoding="utf-8") as fh:
            gesamt = sum(1 for line in fh if line.strip())
    return {"leads": read_leads(LEADS_FILE, limit=limit), "gesamt": gesamt}
