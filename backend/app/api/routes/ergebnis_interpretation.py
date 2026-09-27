"""Schnittstelle der Interpretationsbelege (Konformitätszeile 19, T-1140, Vorhaben T-1010).

Jeder Endpunkt gibt die Ausgabe des zugehörigen Dienstes oder Datenmoduls
unverändert weiter; hier wird nichts gerechnet. Drei Endpunkte hüllen die
Ausgabe ein (T-1299): ``abhaengigkeiten`` in ``{kommune_id, umfang,
klimawirkungen}``, ``diversitaet`` in ``{quelle, umfang, je_klimawirkung}`` (T-1580) und
``leitfragen`` in ``{quelle, leitfragen}``.

- ``/kommune/{id}/interpretation/nachbarkommunen`` → ``nachbarkommunen_screening``
- ``/kommune/{id}/interpretation/nachweise`` (GET, POST, DELETE) → ``ergebnis_nachweise``
- ``/kommune/{id}/interpretation/abhaengigkeiten`` → ``handlungsfeld_abhaengigkeiten``
- ``/kommune/{id}/interpretation/diversitaet`` → ``data.diversitaet_aspekte``, nur die für die
  Kommune gerechneten Klimawirkungen, nach ``kwra_id`` gruppiert (T-1475)
- ``/interpretation/massnahmen-gewissheit`` → ``massnahmen_gewissheit``
- ``/interpretation/massnahmen-umsetzung`` → ``data.massnahmen_umsetzung``
- ``/interpretation/diversitaet`` → ``data.diversitaet_aspekte``, unverändert (Altbestand)
- ``/interpretation/leitfragen`` → ``data.kra_leitfragen``
- ``/kommune/{id}/interpretation/bericht`` → ``ergebnis_interpretation_markdown``
  (Markdown mit sieben festen Abschnitten, T-1141)

Eine unbekannte Kommune oder ein unbekannter Nachweis ergibt HTTP 404, ein
``ValueError`` des Nachweisdienstes HTTP 400. Den Zugriff schützt die Router-Einbindung in ``main.py`` (``_PROTECTED``).
"""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.data import catalog
from app.data.diversitaet_aspekte import DIVERSITAET_JE_KLIMAWIRKUNG
from app.data.diversitaet_aspekte import QUELLE as DIVERSITAET_QUELLE
from app.data.kra_leitfragen import LEITFRAGEN
from app.data.kra_leitfragen import QUELLE as LEITFRAGEN_QUELLE
from app.data.massnahmen_umsetzung import MASSNAHMEN_UMSETZUNG
from app.db.database import get_db
from app.models.models import Kommune
from app.services import ergebnis_nachweise
from app.services.download_namen import content_disposition, download_dateiname_fuer
from app.services.ergebnis_interpretation_markdown import interpretationsbericht_fuer_kommune
from app.services.geodata_export_service import assessment_is_done
from app.services.handlungsfeld_abhaengigkeiten import abhaengigkeiten_der_kommune
from app.services.massnahmen_gewissheit import massnahmen_gewissheit
from app.services.measure_service import get_risk_aggregate
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
    if not ergebnis_nachweise.nachweis_loeschen(db, kommune_id, nachweis_id):
        raise HTTPException(404, "Nachweis nicht gefunden")
    return True


@router.get("/kommune/{kommune_id}/interpretation/abhaengigkeiten")
def get_abhaengigkeiten(kommune_id: int, db: Session = Depends(get_db)):
    """Abhängigkeiten der für diese Kommune gerechneten Klimawirkungen.

    Die gerechneten Risiko-Codes stammen wie bei ``GET /kommune/{id}/systembereiche``
    (``routes/kommune.py``) aus ``get_risk_aggregate(...)["cost"]["by_risk"]``, sofern
    ``assessment_is_done`` eine Berechnung meldet. Ohne Berechnung steht der ganze
    Katalog da, und ``umfang`` sagt das: ``gerechnet`` oder ``katalog``.
    """
    kommune = _kommune_oder_404(db, kommune_id)
    if assessment_is_done(db, kommune.id):
        agg = get_risk_aggregate(db, kommune.id, apply_measures=False)
        codes = [eintrag["code"] for eintrag in agg["cost"]["by_risk"]]
        umfang = "gerechnet"
    else:
        codes = None
        umfang = "katalog"
    return {
        "kommune_id": kommune.id,
        "umfang": umfang,
        "klimawirkungen": abhaengigkeiten_der_kommune(codes),
    }


def _diversitaet_je_kwra(codes: list[str]) -> dict[str, dict]:
    """``DIVERSITAET_JE_KLIMAWIRKUNG`` nach ``kwra_id`` gruppiert, für ``codes``.

    Mehrere Katalogcodes derselben Klimawirkung (z. B. #95 Mortalität und
    Morbidität) tragen zu einer Überschrift zusammen; gleiche Aspekte (gleicher
    Eintrag in ``beruecksichtigt``/``nicht_beruecksichtigt``, etwa der allgemeine
    Diversitätshinweis) erscheinen dabei nur einmal.
    """
    je_kwra: dict[int, dict] = {}
    for code in codes:
        if code not in DIVERSITAET_JE_KLIMAWIRKUNG:
            continue
        risiko = catalog.RISKS_BY_CODE[code]
        kwra_id = risiko["kwra_id"]
        eintrag = je_kwra.setdefault(kwra_id, {
            "bezeichnung": f"{risiko.get('kwra_name') or risiko['name']} (#{kwra_id})",
            "beruecksichtigt": [],
            "nicht_beruecksichtigt": [],
        })
        for feld in ("beruecksichtigt", "nicht_beruecksichtigt"):
            for aspekt in DIVERSITAET_JE_KLIMAWIRKUNG[code][feld]:
                if aspekt not in eintrag[feld]:
                    eintrag[feld].append(aspekt)
    return {str(kwra_id): eintrag for kwra_id, eintrag in sorted(je_kwra.items())}


@router.get("/kommune/{kommune_id}/interpretation/diversitaet")
def get_diversitaet_kommune(kommune_id: int, db: Session = Depends(get_db)):
    """Gender- und Diversitätsaspekte nur der für diese Kommune gerechneten Klimawirkungen.

    Die gerechneten Risiko-Codes stammen wie bei ``get_abhaengigkeiten`` aus
    ``get_risk_aggregate(...)["cost"]["by_risk"]``, sofern ``assessment_is_done`` eine
    Berechnung meldet; ohne Berechnung steht der ganze Bestand von
    ``DIVERSITAET_JE_KLIMAWIRKUNG`` da, und ``umfang`` sagt das wie bei
    ``get_abhaengigkeiten``: ``gerechnet`` oder ``katalog`` (T-1580). Gruppiert wird nach
    ``kwra_id``: eine Überschrift je Klimawirkung (``bezeichnung`` = „<kwra_name>
    (#<kwra_id>)“), die Aspekte mehrerer Codes derselben Klimawirkung stehen zusammen, ohne
    doppelte Einträge.
    """
    kommune = _kommune_oder_404(db, kommune_id)
    if assessment_is_done(db, kommune.id):
        agg = get_risk_aggregate(db, kommune.id, apply_measures=False)
        codes = [eintrag["code"] for eintrag in agg["cost"]["by_risk"]]
        umfang = "gerechnet"
    else:
        codes = list(DIVERSITAET_JE_KLIMAWIRKUNG.keys())
        umfang = "katalog"
    return {
        "quelle": DIVERSITAET_QUELLE,
        "umfang": umfang,
        "je_klimawirkung": _diversitaet_je_kwra(codes),
    }


@router.get("/interpretation/massnahmen-gewissheit")
def get_massnahmen_gewissheit():
    return massnahmen_gewissheit()


@router.get("/interpretation/massnahmen-umsetzung")
def get_massnahmen_umsetzung():
    return MASSNAHMEN_UMSETZUNG


@router.get("/interpretation/diversitaet")
def get_diversitaet():
    return {"quelle": DIVERSITAET_QUELLE, "je_klimawirkung": DIVERSITAET_JE_KLIMAWIRKUNG}


@router.get("/interpretation/leitfragen")
def get_leitfragen():
    return {"quelle": LEITFRAGEN_QUELLE, "leitfragen": LEITFRAGEN}


@router.get("/kommune/{kommune_id}/interpretation/bericht")
def get_interpretationsbericht(kommune_id: int, db: Session = Depends(get_db)):
    kommune = _kommune_oder_404(db, kommune_id)
    inhalt = interpretationsbericht_fuer_kommune(db, kommune)
    dateiname = download_dateiname_fuer("ergebnisse-interpretieren", db, kommune, "md")
    return Response(
        content=inhalt,
        media_type="text/markdown; charset=utf-8",
        headers={"Content-Disposition": content_disposition(dateiname)},
    )
