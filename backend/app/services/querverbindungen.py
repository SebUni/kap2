"""Auswertung der KWRA-Querverbindungen je Klimawirkung (Teil 2).

Setzt auf ``app/data/kwra_querverbindungen.py`` (Teil 1: Netzrollen, benannte
Einzelbeziehungen, Kennzahlen, Systembereichs-Matrix — alles quellenfest aus
KWRA 2021, Teilbericht 6, Kapitel 3.4) auf und verknüpft es mit den im Produkt
katalogisierten Klimawirkungen (``app/data/catalog.RISKS`` — aktiv gerechnet —
und ``catalog.PLANNED_RISKS`` — auf der Roadmap, noch gesperrt).

Jede der 52 im Katalog geführten Klimawirkungen (kwra_id) erscheint hier genau
einmal, unabhängig davon, ob sie in ``RISKS`` mehrfach vorkommt (KWRA-1:1-Klammer
#95: Mortalität und Erkrankungen sind zwei Teil-Ausweise derselben Klimawirkung,
siehe Kommentar in catalog.py).
"""

from __future__ import annotations

from app.data import catalog
from app.data import kwra_querverbindungen as kq


def _klimawirkung_name(eintrag: dict) -> str:
    """KWRA-Name einer Klimawirkung: ``kwra_name`` bei RISKS (der Risiko-``name``
    ist der Produktname des Teil-Ausweises, z. B. „Hitzebelastung — Mortalität“),
    sonst ``name`` (PLANNED_RISKS führt dort bereits den KWRA-Namen)."""
    return eintrag.get("kwra_name") or eintrag["name"]


def querverbindungs_auswertung() -> dict:
    """Fasst die KWRA-Querverbindungen je katalogisierter Klimawirkung zusammen.

    Liefert genau einen Eintrag je kwra_id aus ``catalog.RISKS`` und
    ``catalog.PLANNED_RISKS`` zusammengenommen (Dubletten — z. B. #95, das in
    RISKS zweimal als Teil-Ausweis steht — werden auf einen Eintrag verdichtet).
    """
    klimawirkungen_je_id: dict[int, dict] = {}
    for r in catalog.RISKS:
        kid = r["kwra_id"]
        klimawirkungen_je_id.setdefault(kid, {"kwra_id": kid, "name": _klimawirkung_name(r)})
    for p in catalog.PLANNED_RISKS:
        kid = p["kwra_id"]
        klimawirkungen_je_id.setdefault(kid, {"kwra_id": kid, "name": _klimawirkung_name(p)})

    netzrolle_je_id = {e["kwra_id"]: e["rolle"] for e in kq.NETZROLLEN}

    ausgehend_je_id: dict[int, int] = {}
    eingehend_je_id: dict[int, int] = {}
    for beziehung in kq.BENANNTE_BEZIEHUNGEN:
        quelle_id = beziehung.get("quelle_kwra_id")
        ziel_id = beziehung.get("ziel_kwra_id")
        if quelle_id is not None:
            ausgehend_je_id[quelle_id] = ausgehend_je_id.get(quelle_id, 0) + 1
        if ziel_id is not None:
            eingehend_je_id[ziel_id] = eingehend_je_id.get(ziel_id, 0) + 1

    klimawirkungen = [
        {
            "kwra_id": kid,
            "name": eintrag["name"],
            "netzrolle": netzrolle_je_id.get(kid),
            "ausgehende_benannte": ausgehend_je_id.get(kid, 0),
            "eingehende_benannte": eingehend_je_id.get(kid, 0),
        }
        for kid, eintrag in sorted(klimawirkungen_je_id.items())
    ]

    mit_netzrolle = sum(1 for e in klimawirkungen if e["netzrolle"] is not None)
    mit_benannter_beziehung = sum(
        1 for e in klimawirkungen
        if e["ausgehende_benannte"] > 0 or e["eingehende_benannte"] > 0
    )
    abdeckung = {
        "klimawirkungen_im_katalog": len(klimawirkungen),
        "klimawirkungen_kwra_gesamt": 102,
        "mit_ausgewiesener_netzrolle": mit_netzrolle,
        "mit_benannter_einzelbeziehung": mit_benannter_beziehung,
        "hinweis": (
            "Die 52 im Katalog geführten Klimawirkungen (Stufe „aktiv“ oder "
            "Roadmap) sind eine Teilmenge der 102 KWRA-Klimawirkungen; "
            "Netzrolle und benannte Beziehungen liegen nur vor, wo Teilbericht 6 "
            "Kapitel 3.4 sie ausdrücklich nennt (siehe modellgrenze)."
        ),
    }

    modellgrenze = (
        "Die KWRA beziffert 257 Querverbindungen zwischen den 102 Klimawirkungen, "
        "veröffentlicht die Einzelkanten aber in keinem der sechs Teilberichte als "
        "vollständige Liste (Abbildung 8 in Teilbericht 6 ist ein Chord-Diagramm auf "
        "Handlungsfeldebene, aus dem sich keine exakten Kanten ablesen lassen). "
        "Ausgewiesen werden deshalb nur die von Teilbericht 6 Kapitel 3.4 ausdrücklich "
        "belegten Angaben: 25 Klimawirkungen mit benannter Netzrolle, 20 im Fließtext "
        "genannte Einzelbeziehungen (Auszug, nicht vollständig) sowie Kennzahlen und "
        "die 5x5-Systembereichs-Matrix. Eine vollständige, selbst modellierte "
        "Kantenliste wäre ein Parameter ohne Quelle (Eiserne Regel 3 / Vorgabe P1) "
        "und wird deshalb bewusst nicht erzeugt."
    )

    return {
        "klimawirkungen": klimawirkungen,
        "kennzahlen": kq.KENNZAHLEN,
        "systembereich_matrix": kq.SYSTEMBEREICH_MATRIX,
        "abdeckung": abdeckung,
        "quelle": kq.QUELLE,
        "modellgrenze": modellgrenze,
    }
