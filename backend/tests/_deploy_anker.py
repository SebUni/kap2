"""Strenge Textanker für die Deploy-Tests (T-0530).

Die Deploy-Tests schneiden Blöcke aus `deploy/test-deploy.sh` an Textankern aus
(`SCHRITT="dienst"`, `trap fehler_abbruch ERR`, …) und prüfen Befehle über Teilzeichenketten.
Bis T-0530 lief das über `str.index()` und `in`: Stand ein Anker (auch) in einem Kommentar,
traf die Suche den Kommentar, und die Werkbank prüfte still etwas anderes, als sie
behauptete (T-0484: leerer Ausschnitt, weil ein Kommentar aus T-0442 die Endmarke vorwegnahm).

Hier gilt deshalb:

* Ein Anker zählt nur in einer Befehlszeile. Kommentarzeilen (erstes Nicht-Leerzeichen ist
  `#`) und angehängte Kommentare (`befehl  # …`) zählen bei der Suche nicht mit.
* Fehlt ein Anker in den Befehlszeilen — gar nicht vorhanden oder nur noch in einem
  Kommentar —, bricht der Test mit `AssertionError` ab, und die Meldung nennt den Anker
  beim Namen. Still durchlaufen gibt es nicht.

`KAP2_DEPLOY_SKRIPT` in der Umgebung zeigt die Tests auf eine andere Skriptdatei; das ist die
Stelle für die Rot-Simulation (Kopie mit entferntem bzw. auskommentiertem Anker).
"""

from __future__ import annotations

import os
import re
from pathlib import Path

WURZEL = Path(__file__).resolve().parents[2]
SKRIPT = Path(os.environ.get("KAP2_DEPLOY_SKRIPT") or WURZEL / "deploy" / "test-deploy.sh")

# Beginn eines Shell-Kommentars: `#` am Zeilenanfang oder nach einem Leerraum. `$#`, `${#x}`
# oder `a#b` beginnen keinen Kommentar und werden deshalb nicht getroffen.
_KOMMENTAR = re.compile(r"(^|\s)#")


def skript_text() -> str:
    return SKRIPT.read_text(encoding="utf-8")


def _befehlsende(zeile: str) -> int:
    """Spalte, ab der die Zeile Kommentar ist (Zeilenlänge, wenn sie keinen hat)."""
    treffer = _KOMMENTAR.search(zeile)
    if treffer is None:
        return len(zeile)
    return treffer.start() + len(treffer.group(1))


def _im_befehl(text: str, pos: int, anker: str) -> bool:
    """Liegt der Anker ab `pos` vollständig im Befehlsteil seiner Zeile?"""
    # Führende Zeilenumbrüche des Ankers (etwa "\nfi") gehören zur Vorzeile; maßgeblich ist
    # die Zeile, in der der eigentliche Inhalt des Ankers steht.
    kern = pos + (len(anker) - len(anker.lstrip("\n")))
    zeilenanfang = text.rfind("\n", 0, kern) + 1
    zeilenende = text.find("\n", kern)
    if zeilenende == -1:
        zeilenende = len(text)
    zeile = text[zeilenanfang:zeilenende]
    ende_anker = min(pos + len(anker), zeilenende) - zeilenanfang
    return ende_anker <= _befehlsende(zeile)


def anker_index(text: str, anker: str, start: int = 0, *, wo: str | None = None) -> int:
    """Wie `text.index(anker, start)`, aber nur Treffer in Befehlszeilen zählen.

    Fehlt der Anker dort, scheitert der Test laut und nennt den Anker.
    """
    pos = text.find(anker, start)
    while pos != -1:
        if _im_befehl(text, pos, anker):
            return pos
        pos = text.find(anker, pos + 1)
    if anker in text[start:]:
        grund = "steht nur noch in einem Kommentar"
    else:
        grund = "fehlt"
    raise AssertionError(
        f"ANKER ROT: {anker!r} {grund} ({wo or SKRIPT}, Befehlszeilen ab Zeichen {start})"
    )


def hat_anker(text: str, anker: str, *, wo: str | None = None) -> bool:
    """Für `assert hat_anker(block, "...")`: wahr oder laut scheitern, mit Ankername."""
    anker_index(text, anker, wo=wo)
    return True


def ausschnitt(anfang: str, ende: str, *, bis_einschliesslich: bool = False) -> str:
    """Block aus dem Skript von Anker `anfang` bis Anker `ende` (ende nach anfang gesucht)."""
    text = skript_text()
    a = anker_index(text, anfang)
    e = anker_index(text, ende, a + len(anfang))
    if bis_einschliesslich:
        e += len(ende)
    return text[a:e]
