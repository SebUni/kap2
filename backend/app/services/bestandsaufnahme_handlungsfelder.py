"""Handlungsfelder der Bestandsaufnahme (Ticket T-1170, Vorhaben T-1160, ISO 14091 A9).

Reine Funktion ohne Datenbank und ohne Netz. Führt alle KAnG-Handlungsfelder aus
``catalog.KANG_CLUSTERS`` auf und weist je Feld aus, ob der Katalog dazu ein Risiko
führt. Ob ein Feld eine Kommune betrifft, legt das Modul nicht fest.
"""

from __future__ import annotations

from app.data import catalog
from app.data.kang_handlungsfelder import handlungsfeld_fuer_risiko

IM_KATALOG = "im Katalog"
NICHT_IM_KATALOG = "nicht im Katalog"


def handlungsfelder_im_katalog() -> list[dict]:
    """Je KAnG-Feld: ``cluster``, ``feld``, ``label``, ``risiken`` (Codes) und ``status``."""
    zuordnung: dict[tuple[str, str], list] = {}
    for risiko in catalog.RISKS:
        zuordnung.setdefault(handlungsfeld_fuer_risiko(risiko["code"]), []).append(risiko["code"])
    ergebnis = []
    for cluster in catalog.KANG_CLUSTERS:
        for feld in cluster["fields"]:
            risiken = zuordnung.get((cluster["code"], feld["code"]), [])
            ergebnis.append({
                "cluster": cluster["code"],
                "feld": feld["code"],
                "label": feld["label"],
                "risiken": list(risiken),
                "status": IM_KATALOG if risiken else NICHT_IM_KATALOG,
            })
    return ergebnis
