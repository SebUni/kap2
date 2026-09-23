"""Selbsteinschätzung der Anpassungskapazität (Konformitätszeile 18, T-0764).

``POST /api/anpassungskapazitaet/bewertung`` nimmt die Stufen je Komponente
entgegen und liefert die Bewertung nach der Engpassregel samt Markdown-Abschnitt.
Die Route ist zustandslos: keine Datenbank, keine Kommunendaten. Den Zugriff
schützt die Router-Einbindung in ``main.py`` (``_PROTECTED``).
"""

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.anpassungskapazitaet import bewerte_anpassungskapazitaet
from app.services.anpassungskapazitaet_markdown import anpassungskapazitaet_als_markdown

router = APIRouter()


class AnpassungskapazitaetEingabe(BaseModel):
    # Werte bleiben unverändert (Any), damit der Dienst Stufen selbst prüft.
    einschaetzung: dict[str, Any]


@router.post("/anpassungskapazitaet/bewertung")
def post_anpassungskapazitaet_bewertung(eingabe: AnpassungskapazitaetEingabe) -> dict:
    try:
        bewertung = bewerte_anpassungskapazitaet(eingabe.einschaetzung)
    except ValueError as fehler:
        raise HTTPException(422, str(fehler))
    return {
        "bewertung": bewertung,
        "markdown": anpassungskapazitaet_als_markdown(bewertung),
    }
