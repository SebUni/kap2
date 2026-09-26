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

Den Gemeindeschlüssel führt das Kommune-Modell nicht; er kommt wie in der
Bestandsaufnahme aus ``inkar_loader.resolve_ags(osm_id)`` (Overpass-Abfrage).
Gefundene Schlüssel werden je ``osm_id`` im Prozess zwischengespeichert, damit
nicht jeder Download eine Netzabfrage auslöst; ein Fehlschlag wird nicht
gespeichert und beim nächsten Download erneut versucht.
"""

from __future__ import annotations

import logging
import re
import unicodedata

log = logging.getLogger(__name__)

_UMSCHRIFT = str.maketrans({
    "ä": "ae", "ö": "oe", "ü": "ue",
    "Ä": "Ae", "Ö": "Oe", "Ü": "Ue",
    "ß": "ss", "ẞ": "SS",
})

_AGS_CACHE: dict[str, str] = {}


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


def gemeindeschluessel(kommune) -> str | None:
    """Gemeindeschlüssel der Kommune oder ``None``; bricht nie einen Download ab."""
    osm_id = getattr(kommune, "osm_id", None)
    if not osm_id:
        return None
    if osm_id in _AGS_CACHE:
        return _AGS_CACHE[osm_id]
    try:
        from app.services import inkar_loader

        ags = inkar_loader.resolve_ags(osm_id)
    except Exception as exc:  # Download nie wegen des Namens abbrechen
        log.warning("gemeindeschluessel: Auflösung für osm_id=%s fehlgeschlagen: %s", osm_id, exc)
        return None
    if ags:
        _AGS_CACHE[osm_id] = ags
    return ags or None


def download_dateiname_fuer(art: str, kommune, endung: str) -> str:
    """Dateiname für eine Kommune (Name und Gemeindeschlüssel aus dem Modell)."""
    return download_dateiname(art, getattr(kommune, "name", None), gemeindeschluessel(kommune), endung)


def content_disposition(dateiname: str) -> str:
    """Header-Wert für einen Download mit diesem (ASCII-)Dateinamen."""
    return f'attachment; filename="{dateiname}"'
