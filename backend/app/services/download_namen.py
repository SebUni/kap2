"""Einheitliche Dateinamen für alle Downloads einer Kommune (T-1424).

Regel (Nachtrag CEO zu T-1267, 26.09.2026): Art des Dokuments, Name der Kommune
(dateinamensicher) und Gemeindeschlüssel, getrennt durch Unterstrich::

    download_dateiname("massnahmen", "Bad Tölz", "09173112", "xlsx")
    → "massnahmen_Bad-Toelz_09173112.xlsx"

Fehlt der Gemeindeschlüssel, entfällt der letzte Teil (``massnahmen_Bad-Toelz.xlsx``).

Dateinamensicher heißt: Umlaute und ß werden umschrieben (ä → ae, ß → ss),
übrige diakritische Zeichen verlieren ihr Zeichen (é → e), und jede Folge von
Zeichen außer Buchstaben A–Z und Ziffern wird zu einem Bindestrich. So bleibt der
Name in jedem Betriebssystem und im Header ``Content-Disposition`` reines ASCII.

Den Gemeindeschlüssel führt das Kommune-Modell nicht (T-1469). Er kommt aus der
VG250-Tabelle ``gemeinden`` (``lite_models.Gemeinde.ags``): gesucht wird die
Gemeinde, deren Fläche ``ST_PointOnSurface`` der Kommunengrenze enthält — dieselbe
Abfrage wie in ``nachbarkommunen_screening.nachbar_screening_fuer_kommune``.
Fehlt die Grenze, gibt es keinen Treffer, oder schlägt die Abfrage fehl (etwa ohne
PostGIS), bleibt der Name ohne diesen Teil; es gibt keinen Rückgriff auf eine
Overpass-Abfrage mehr. Gefundene Werte werden je Kommune im Prozess
zwischengespeichert, damit nicht jeder Download eine erneute Abfrage auslöst; ein
Fehlschlag wird nicht gespeichert und beim nächsten Download erneut versucht.
"""

from __future__ import annotations

import logging
import re
import unicodedata
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

log = logging.getLogger(__name__)

_UMSCHRIFT = str.maketrans({
    "ä": "ae", "ö": "oe", "ü": "ue",
    "Ä": "Ae", "Ö": "Oe", "Ü": "Ue",
    "ß": "ss", "ẞ": "SS",
})

_AGS_CACHE: dict[int, str] = {}


def dateinamensicher(text: str | None) -> str:
    """Text auf ASCII-Buchstaben, Ziffern und Bindestriche bringen."""
    if not text:
        return ""
    umgeschrieben = str(text).translate(_UMSCHRIFT)
    zerlegt = unicodedata.normalize("NFKD", umgeschrieben)
    ascii_text = zerlegt.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^A-Za-z0-9]+", "-", ascii_text).strip("-")


def download_dateiname(art: str, kommune_name: str | None, gemeindeschluessel: str | None,
                       endung: str) -> str:
    """Dateiname nach der Regel ``<art>_<Name>_<Gemeindeschlüssel>.<endung>``."""
    teile = [art, dateinamensicher(kommune_name) or "Kommune"]
    schluessel = re.sub(r"\D", "", gemeindeschluessel or "")
    if schluessel:
        teile.append(schluessel)
    return "_".join(teile) + "." + endung.lstrip(".")


def _ags_aus_gemeinden(db: "Session", kommune) -> str | None:
    """Reine VG250-Abfrage: Gemeinde, deren Fläche den Innenpunkt der Kommune enthält.

    Übernimmt wörtlich die Abfrage aus
    ``nachbarkommunen_screening.nachbar_screening_fuer_kommune`` (Zeilen 76–85);
    braucht PostGIS (``ST_PointOnSurface``, ``ST_Contains``).
    """
    from geoalchemy2 import functions as func
    from sqlalchemy import select

    from app.models.lite_models import Gemeinde
    from app.models.models import Kommune as KommuneModell

    punkt = (
        select(func.ST_PointOnSurface(KommuneModell.boundary))
        .where(KommuneModell.id == kommune.id)
        .scalar_subquery()
    )
    treffer = (
        db.query(Gemeinde)
        .filter(func.ST_Contains(Gemeinde.geometry, punkt))
        .first()
    )
    return treffer.ags if treffer else None


def gemeindeschluessel(db: "Session", kommune) -> str | None:
    """Gemeindeschlüssel der Kommune aus der VG250-Tabelle; bricht nie einen Download ab."""
    kommune_id = getattr(kommune, "id", None)
    if kommune_id is None:
        return None
    if kommune_id in _AGS_CACHE:
        return _AGS_CACHE[kommune_id]
    try:
        ags = _ags_aus_gemeinden(db, kommune)
    except Exception as exc:  # noqa: BLE001 — Download nie wegen des Namens abbrechen
        log.warning("gemeindeschluessel: Ermittlung für kommune_id=%s fehlgeschlagen: %s", kommune_id, exc)
        db.rollback()
        return None
    if ags:
        _AGS_CACHE[kommune_id] = ags
    return ags or None


def download_dateiname_fuer(art: str, db: "Session", kommune, endung: str) -> str:
    """Dateiname für eine Kommune (Name und Gemeindeschlüssel aus dem Modell/der VG250-Tabelle)."""
    return download_dateiname(art, getattr(kommune, "name", None), gemeindeschluessel(db, kommune), endung)


def content_disposition(dateiname: str) -> str:
    """Header-Wert für einen Download mit diesem (ASCII-)Dateinamen."""
    return f'attachment; filename="{dateiname}"'
