"""Schnittstelle der Interpretationsbelege (Konformitätszeile 19, T-1140, Vorhaben T-1010).

Jeder Endpunkt gibt die Ausgabe des zugehörigen Dienstes oder Datenmoduls
unverändert weiter; hier wird nichts gerechnet oder umgeformt:

- ``/kommune/{id}/interpretation/nachbarkommunen`` → ``nachbarkommunen_screening``
- ``/kommune/{id}/interpretation/nachweise`` (GET, POST, DELETE) → ``ergebnis_nachweise``
- ``/kommune/{id}/interpretation/abhaengigkeiten`` → ``handlungsfeld_abhaengigkeiten``
- ``/interpretation/massnahmen-gewissheit`` → ``massnahmen_gewissheit``
- ``/interpretation/massnahmen-umsetzung`` → ``data.massnahmen_umsetzung``
- ``/interpretation/diversitaet`` → ``data.diversitaet_aspekte``
- ``/interpretation/leitfragen`` → ``data.kra_leitfragen``

Eine unbekannte Kommune ergibt HTTP 404, ein ``ValueError`` des Nachweisdienstes
HTTP 400. Den Zugriff schützt die Router-Einbindung in ``main.py`` (``_PROTECTED``).
"""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.data.diversitaet_aspekte import DIVERSITAET_JE_KLIMAWIRKUNG
from app.data.kra_leitfragen import LEITFRAGEN
from app.data.massnahmen_umsetzung import MASSNAHMEN_UMSETZUNG
from app.db.database import get_db
from app.models.models import Kommune
from app.services import ergebnis_nachweise
from app.services.handlungsfeld_abhaengigkeiten import abhaengigkeiten_der_kommune
from app.services.massnahmen_gewissheit import massnahmen_gewissheit
from app.services.nachbarkommunen_screening import nachbar_screening_fuer_kommune

router = APIRouter()


class NachweisEingabe(BaseModel):
    # Art, Stelle und Datum prüft der Dienst selbst (ValueError → 400).
    art: str
    stelle: str
    datum: date
    vermerk: str | None = None


class NachweisOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    kommune_id: int
    art: str
    stelle: str
    datum: date
    vermerk: str | None = None


def _kommune_oder_404(db: Session, kommune_id: int) -> Kommune:
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")
    return kommune


@router.get("/kommune/{kommune_id}/interpretation/nachbarkommunen")
def get_nachbarkommunen(kommune_id: int, db: Session = Depends(get_db)):
    kommune = _kommune_oder_404(db, kommune_id)
    return nachbar_screening_fuer_kommune(db, kommune)


@router.get("/kommune/{kommune_id}/interpretation/nachweise")
def get_nachweise(kommune_id: int, db: Session = Depends(get_db)):
    _kommune_oder_404(db, kommune_id)
    return ergebnis_nachweise.nachweise(db, kommune_id)


@router.post("/kommune/{kommune_id}/interpretation/nachweise", response_model=NachweisOut)
def post_nachweis(kommune_id: int, eingabe: NachweisEingabe, db: Session = Depends(get_db)):
    _kommune_oder_404(db, kommune_id)
    try:
        return ergebnis_nachweise.nachweis_anlegen(
            db, kommune_id, eingabe.art, eingabe.stelle, eingabe.datum, eingabe.vermerk,
        )
    except ValueError as fehler:
        raise HTTPException(400, str(fehler))


@router.delete("/kommune/{kommune_id}/interpretation/nachweise/{nachweis_id}")
def delete_nachweis(kommune_id: int, nachweis_id: int, db: Session = Depends(get_db)):
    _kommune_oder_404(db, kommune_id)
    return ergebnis_nachweise.nachweis_loeschen(db, kommune_id, nachweis_id)


@router.get("/kommune/{kommune_id}/interpretation/abhaengigkeiten")
def get_abhaengigkeiten(kommune_id: int, db: Session = Depends(get_db)):
    _kommune_oder_404(db, kommune_id)
    return abhaengigkeiten_der_kommune()


@router.get("/interpretation/massnahmen-gewissheit")
def get_massnahmen_gewissheit():
    return massnahmen_gewissheit()


@router.get("/interpretation/massnahmen-umsetzung")
def get_massnahmen_umsetzung():
    return MASSNAHMEN_UMSETZUNG


@router.get("/interpretation/diversitaet")
def get_diversitaet():
    return DIVERSITAET_JE_KLIMAWIRKUNG


@router.get("/interpretation/leitfragen")
def get_leitfragen():
    return LEITFRAGEN
