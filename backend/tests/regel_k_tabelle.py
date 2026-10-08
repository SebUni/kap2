"""Registry-Klasse der 11 Blöcke nach Regel K, gelesen zur Laufzeit (T-1898-cto).

``docs/methodik/querschnitt_kennzeichnung.md`` führt unter „Anwendung auf M0“ eine Tabelle, deren
Kopfzeile mit ``| Bericht | Block-ID | Eingänge |`` beginnt. Ihre Spalte „Kennzeichnung nach der
Regel“ nennt für jeden der 11 Blöcke ``quelle``, ``abschaetzung_kap3`` oder ``berechnet``. Die
Kennzeichnungstests der Berichte #95, #96 und #98 lesen sie hier und schreiben sie nicht ab.
Für alle übrigen Blöcke gilt weiter Kapitel 7 des Berichts.
"""

from __future__ import annotations

import os

QUERSCHNITT = os.path.join(os.path.dirname(__file__), "..", "..",
                           "docs", "methodik", "querschnitt_kennzeichnung.md")
KOPF = "| Bericht | Block-ID | Eingänge |"
SPALTE = "Kennzeichnung nach der Regel"
# Kennzeichnung (Aufgabe §4) → Evidenzklasse der Parameterliste.
KLASSE = {"quelle": "belegt", "abschaetzung_kap3": "abgeschaetzt", "berechnet": "berechnet"}


def _zellen(zeile: str) -> list[str]:
    return [c.strip().replace(chr(96), "") for c in zeile.strip().strip("|").split("|")]


def regel_k_kennzeichnung(bericht: str) -> dict[str, str]:
    """Block-ID → Kennzeichnung nach der Regel, für die Blöcke des Berichts (``"95"`` …)."""
    with open(os.path.abspath(QUERSCHNITT), encoding="utf-8") as fh:
        zeilen = fh.read().splitlines()
    start = next(i for i, z in enumerate(zeilen) if z.startswith(KOPF))
    kopf = _zellen(zeilen[start])
    spalte = kopf.index(SPALTE)
    ergebnis: dict[str, str] = {}
    for z in zeilen[start + 2:]:          # Zeile start + 1 ist die Trennzeile |---|
        if not z.startswith("|"):
            break
        zellen = _zellen(z)
        if zellen[0] == bericht:
            ergebnis[zellen[1]] = zellen[spalte]
    assert ergebnis, f"keine Zeile für Bericht {bericht} in der Tabelle der 11 Blöcke"
    assert set(ergebnis.values()) <= set(KLASSE), ergebnis
    return ergebnis


def soll_klasse(bericht: str, bloecke: dict[str, dict]) -> dict[str, str]:
    """Block-ID → erwartete Registry-Klasse: Regel K für die 11, sonst Kapitel 7."""
    regel = regel_k_kennzeichnung(bericht)
    return {bid: KLASSE[regel.get(bid, b["kennzeichnung"])] for bid, b in bloecke.items()}
