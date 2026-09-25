"""Screening-Index der angrenzenden Gemeinden (T-1133, Vorhaben T-1010, Anforderung A5).

Zeigt je Klimawirkung aus ``catalog.RISKS`` den vorberechneten Screening-Index
(``gemeinde_lite_results.index_value``, 0 bis 100, bundesweit normiert) der eigenen
Gemeinde und der angrenzenden Gemeinden. Es wird nichts neu gerechnet.

- Ausgegeben wird nur der Index. ``cost_eur`` und ``outcome_value`` der Lite-Tabelle
  sind eine Hochrechnung aus dem Screening und werden nie ausgegeben (Vorgabe P2).
- Die Werte der Nachbarn werden nur aufgelistet, nicht verdichtet. Wie sie
  verdichtet werden, legt der CMO fest (Anmerkung M-0005).
- Für eine Wirkung ohne Lite-Zeile steht ``index_vorhanden: False``; die Indexwerte
  sind dann leer (``None``), nie null.

Die reine Funktion ``nachbar_screening_aus`` ist ohne Datenbank prüfbar. Die
räumliche Abfrage in ``nachbar_screening_fuer_kommune`` braucht PostGIS
(``ST_PointOnSurface``, ``ST_Contains``, ``ST_Touches``) und ist davon getrennt.
"""
from __future__ import annotations

from typing import Iterable

from geoalchemy2 import functions as func
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data import catalog
from app.models.lite_models import Gemeinde, GemeindeLiteResult
from app.models.models import Kommune


def nachbar_screening_aus(
    eigene: Gemeinde | None,
    nachbarn: Iterable[Gemeinde],
    ergebnisse: Iterable[GemeindeLiteResult],
) -> list[dict]:
    """Je Code aus ``catalog.RISKS`` den Index der eigenen Gemeinde und der Nachbarn.

    ``ergebnisse`` sind die Lite-Zeilen der eigenen Gemeinde und der Nachbarn;
    Zeilen anderer Gemeinden werden nicht beachtet.
    """
    nachbarn = sorted(nachbarn, key=lambda g: (g.name or "", g.ags))
    relevante_ags = {g.ags for g in nachbarn}
    if eigene is not None:
        relevante_ags.add(eigene.ags)

    index_je: dict[tuple[str, str], float | None] = {}
    for zeile in ergebnisse:
        if zeile.ags in relevante_ags:
            index_je[(zeile.risk_code, zeile.ags)] = zeile.index_value

    eintraege = []
    for risk in catalog.RISKS:
        code = risk["code"]
        vorhanden = any(c == code for c, _ in index_je)
        eintraege.append({
            "code": code,
            "name": risk.get("name"),
            "index_vorhanden": vorhanden,
            "eigener_index": (index_je.get((code, eigene.ags))
                              if eigene is not None else None),
            "nachbarn": [
                {"ags": g.ags, "name": g.name, "index": index_je.get((code, g.ags))}
                for g in nachbarn
            ],
        })
    return eintraege


def nachbar_screening_fuer_kommune(db: Session, kommune: Kommune) -> list[dict]:
    """Eigene VG250-Gemeinde und angrenzende Gemeinden bestimmen, dann auflisten.

    Eigene Gemeinde: die VG250-Gemeinde, die ``ST_PointOnSurface`` der
    Kommunengrenze enthält. Nachbarn: VG250-Gemeinden, deren Geometrie die der
    eigenen berührt (``ST_Touches``), ohne Puffer. Braucht PostGIS.
    """
    punkt = (
        select(func.ST_PointOnSurface(Kommune.boundary))
        .where(Kommune.id == kommune.id)
        .scalar_subquery()
    )
    eigene = (
        db.query(Gemeinde)
        .filter(func.ST_Contains(Gemeinde.geometry, punkt))
        .first()
    )
    if eigene is None:
        return nachbar_screening_aus(None, [], [])

    eigene_geometrie = (
        select(Gemeinde.geometry)
        .where(Gemeinde.ags == eigene.ags)
        .scalar_subquery()
    )
    nachbarn = (
        db.query(Gemeinde)
        .filter(func.ST_Touches(Gemeinde.geometry, eigene_geometrie),
                Gemeinde.ags != eigene.ags)
        .all()
    )
    alle_ags = [eigene.ags] + [g.ags for g in nachbarn]
    ergebnisse = (
        db.query(GemeindeLiteResult)
        .filter(GemeindeLiteResult.ags.in_(alle_ags))
        .all()
    )
    return nachbar_screening_aus(eigene, nachbarn, ergebnisse)
