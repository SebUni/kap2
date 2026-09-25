"""Nachweise zur Einbeziehung (ISO 14091 A6 und A10).

A6: Fachabteilungen und externe Expertise einbeziehen.
A10: angrenzende Kommunen und Ländervertreter frühzeitig einbeziehen.

Was nur Menschen leisten, führt die Software als Nachweisfeld: welche Stelle
die Ergebnisse gelesen hat, mit Datum. Die Software behauptet nie eine
Einbeziehung, die nicht erfasst ist — fehlt ein Eintrag, steht dort
``nicht erfasst``. ``stelle`` ist eine Stelle oder Organisation, kein
Personenname.
"""

from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Session

from app.models.models import ErgebnisNachweis


NICHT_ERFASST = "nicht erfasst"

NACHWEIS_ARTEN: dict[str, str] = {
    "fachabteilung": "Fachabteilung der Verwaltung",
    "externe_expertise": "Externe Expertise",
    "angrenzende_kommune": "Angrenzende Kommune",
    "land": "Land (Landesbehörde)",
}


def nachweis_anlegen(
    db: Session,
    kommune_id: int,
    art: str,
    stelle: str,
    datum: date,
    vermerk: str | None = None,
) -> ErgebnisNachweis:
    """Legt einen Nachweis an; prüft Art, Stelle und Datum."""
    if art not in NACHWEIS_ARTEN:
        raise ValueError(f"Unbekannte Nachweisart: {art!r}")
    stelle = (stelle or "").strip()
    if not stelle:
        raise ValueError("Die Stelle darf nicht leer sein.")
    if not isinstance(datum, date):
        raise ValueError("Das Datum fehlt.")
    if datum > date.today():
        raise ValueError("Das Datum darf nicht in der Zukunft liegen.")
    vermerk = (vermerk or "").strip() or None

    eintrag = ErgebnisNachweis(
        kommune_id=kommune_id,
        art=art,
        stelle=stelle,
        datum=datum,
        vermerk=vermerk,
    )
    db.add(eintrag)
    db.commit()
    db.refresh(eintrag)
    return eintrag


def nachweis_loeschen(db: Session, kommune_id: int, nachweis_id: int) -> bool:
    """Löscht einen Nachweis der Kommune; False, wenn es ihn nicht gibt."""
    eintrag = (
        db.query(ErgebnisNachweis)
        .filter(
            ErgebnisNachweis.id == nachweis_id,
            ErgebnisNachweis.kommune_id == kommune_id,
        )
        .first()
    )
    if eintrag is None:
        return False
    db.delete(eintrag)
    db.commit()
    return True


def nachweise(db: Session, kommune_id: int) -> list[dict]:
    """Je Art die erfassten Einträge; ohne Eintrag genau ``nicht erfasst``."""
    zeilen = (
        db.query(ErgebnisNachweis)
        .filter(ErgebnisNachweis.kommune_id == kommune_id)
        .order_by(ErgebnisNachweis.datum, ErgebnisNachweis.id)
        .all()
    )
    ergebnis: list[dict] = []
    for code, bezeichnung in NACHWEIS_ARTEN.items():
        eintraege = [
            {
                "id": z.id,
                "stelle": z.stelle,
                "datum": z.datum,
                "vermerk": z.vermerk,
            }
            for z in zeilen
            if z.art == code
        ]
        ergebnis.append(
            {
                "art": code,
                "bezeichnung": bezeichnung,
                "eintraege": eintraege,
                "status": None if eintraege else NICHT_ERFASST,
            }
        )
    return ergebnis
