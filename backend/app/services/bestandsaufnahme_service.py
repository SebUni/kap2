"""Bestandsaufnahme je Kommune (ISO 14091, Checklistenzeile 16, Teil 2).

Ticket T-0755, Vorhaben T-0447. Liest ausschließlich bereits gespeicherte
Zelldaten (``CellAssessment.data["inputs"]``) und die Sozialdaten aus
``inkar_loader`` (Regionalstatistik, Disk-/Memory-Cache) — kein neuer Overpass-
oder Zensus-Download. Katalog und Reihenfolge: ``app.data.bestandsaufnahme``.

Rechenregeln (keine neuen Zahlenparameter):

- Anteile (65+, unter 18): bevölkerungsgewichtetes Mittel über die Zellen, die
  einen Wert tragen; keine Zelle mit Wert → ``None``.
- KRITIS-Sektoren: Summe der rohen Klassenzählungen (``*_classes``) über alle Zellen.
- Krankenhäuser/Pflegeeinrichtungen: Summe der Zählungen über die Zellen.
- Arbeitslosenquote: Rohwert ``unemployment_rate_pct``.
- Trägt keine Zelle das Feld (bzw. fehlt der Sozialwert), ist der Wert ``None``
  mit Laufzeitsatz, nie 0.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from app.data.bestandsaufnahme import BESTANDSAUFNAHME_GROESSEN, LAUFZEITSATZ_VORLAGE

log = logging.getLogger(__name__)

# Größe → Zellfeld des Anteils (Prozent je Zelle, Zensus 2022).
_ANTEIL_FELDER = {
    "aeltere_ab_65": "share_over_65",
    "kinder_unter_18": "share_under_18",
}

# Größe → Zellfeld der rohen Klassenzählung (app/data/infra_assets.py).
_KRITIS_FELDER = {
    "energie": "energy_infra_classes",
    "wasser_abwasser": "water_wastewater_classes",
    "verkehrsknoten": "transport_hub_classes",
    "kommunikation": "communication_classes",
}

# Größe → Zellfeld der Zählung (OSM-Merkmale aus climate/heat/osm_data.py).
# Gemessen (T-0755): Die gespeicherten Zellen tragen diese Felder heute nicht —
# dort liegen nur Distanzen (``dist_hospital_m``) und der Heimbewohner-Anteil
# (``share_care_home_85p``). Der Wert bleibt dann ``None`` mit Laufzeitsatz.
_ZAEHL_FELDER = {
    "krankenhaeuser": "healthcare_hospital",
    "pflegeeinrichtungen": "care_home_geoms",
}

_SOZIO_FELDER = {
    "arbeitslosenquote": "unemployment_rate_pct",
}


def _zahl(v: Any) -> Optional[float]:
    if isinstance(v, bool) or v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    return None


def _anteil_gewichtet(zellen: list[dict], feld: str) -> Optional[float]:
    """Bevölkerungsgewichtetes Mittel über die Zellen mit Wert."""
    summe = 0.0
    gewicht = 0.0
    for z in zellen:
        wert = _zahl((z or {}).get(feld))
        if wert is None:
            continue
        pop = _zahl((z or {}).get("pop")) or 0.0
        if pop <= 0.0:
            continue
        summe += wert * pop
        gewicht += pop
    if gewicht <= 0.0:
        return None
    return summe / gewicht


def _klassen_summe(zellen: list[dict], feld: str) -> Optional[int]:
    """Summe der Klassenzählungen über alle Zellen; kein Feld in keiner Zelle → None."""
    gesehen = False
    summe = 0
    for z in zellen:
        klassen = (z or {}).get(feld)
        if not isinstance(klassen, dict):
            continue
        gesehen = True
        for anzahl in klassen.values():
            n = _zahl(anzahl)
            if n is not None:
                summe += int(n)
    return summe if gesehen else None


def _zaehl_summe(zellen: list[dict], feld: str) -> Optional[int]:
    """Summe einer Zählung (Zahl oder Merkmalsliste) über die Zellen; ohne Feld → None."""
    gesehen = False
    summe = 0
    for z in zellen:
        wert = (z or {}).get(feld)
        if isinstance(wert, (list, tuple)):
            gesehen = True
            summe += len(wert)
        else:
            n = _zahl(wert)
            if n is not None:
                gesehen = True
                summe += int(n)
    return summe if gesehen else None


def _wert(code: str, zellen: list[dict], sozio: dict) -> Optional[float | int]:
    if code in _ANTEIL_FELDER:
        return _anteil_gewichtet(zellen, _ANTEIL_FELDER[code])
    if code in _KRITIS_FELDER:
        return _klassen_summe(zellen, _KRITIS_FELDER[code])
    if code in _ZAEHL_FELDER:
        return _zaehl_summe(zellen, _ZAEHL_FELDER[code])
    if code in _SOZIO_FELDER:
        return _zahl((sozio or {}).get(_SOZIO_FELDER[code]))
    return None


def bestandsaufnahme_aus_daten(zellen: list[dict], sozio: dict) -> list[dict]:
    """Reine Funktion: 20 Einträge in Katalogreihenfolge aus Zell- und Sozialdaten.

    ``zellen`` sind die ``inputs``-Dicts der gespeicherten Zellen, ``sozio`` die
    Rohgrößen der Regionalstatistik (``unemployment_rate_pct``).
    """
    eintraege: list[dict] = []
    for g in BESTANDSAUFNAHME_GROESSEN:
        if g["luecke"]:
            wert = None
            satz = g["luecke"]
        else:
            wert = _wert(g["code"], zellen or [], sozio or {})
            satz = LAUFZEITSATZ_VORLAGE.format(label=g["label"]) if wert is None else ""
        eintrag = {
            "code": g["code"],
            "gruppe": g["gruppe"],
            "label": g["label"],
            "einheit": g["einheit"],
            "wert": wert,
            "quellen": list(g["quellen"]),
            "luecke_satz": satz,
        }
        if g.get("hinweis"):
            eintrag["hinweis"] = g["hinweis"]
        eintraege.append(eintrag)
    return eintraege


# ── Datenzugriffe (nur gespeicherte Daten) ────────────────────────────────────

def _zellen_der_kommune(db, kommune_id: int) -> list[dict]:
    """``inputs``-Dicts aller gespeicherten Zellbewertungen der Kommune."""
    from app.models.models import CellAssessment

    zeilen = (
        db.query(CellAssessment.data)
        .filter(CellAssessment.kommune_id == kommune_id)
        .all()
    )
    return [((z[0] or {}).get("inputs") or {}) for z in zeilen]


def _sozialdaten(kommune) -> dict:
    """Rohgrößen der Regionalstatistik; ``{}`` bei jedem Fehlschlag.

    ``inkar_loader.socioeconomic_for_kommune`` liefert nur die abgeleiteten
    Indizes, nicht den Rohwert ``unemployment_rate_pct`` — deshalb dieselben
    Schritte (AGS auflösen, gecachte Rohgrößen lesen) ohne Indexbildung.
    """
    from app.services import inkar_loader

    try:
        ags = inkar_loader.resolve_ags(getattr(kommune, "osm_id", None))
        if not ags:
            return {}
        return dict(inkar_loader.fetch_socioeconomic(ags) or {})
    except Exception as exc:  # niemals die Bestandsaufnahme abbrechen
        log.warning("Sozialdaten fehlgeschlagen (kommune=%s): %s", getattr(kommune, "id", None), exc)
        return {}


def bestandsaufnahme_fuer_kommune(db, kommune) -> dict:
    """Bestandsaufnahme einer Kommune aus gespeicherten Zell- und Sozialdaten."""
    zellen = _zellen_der_kommune(db, kommune.id)
    sozio = _sozialdaten(kommune)
    return {
        "kommune_id": kommune.id,
        "name": kommune.name,
        "groessen": bestandsaufnahme_aus_daten(zellen, sozio),
    }
