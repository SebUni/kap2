"""Prüft das Rücksprungziel-Muster nach der Anmeldung (T-0560, Anschluss an T-0502).

Liest die Musterzeile ``RUECKSPRUNG_MUSTER`` wörtlich aus der TypeScript-Quelle
``frontend/src/lib/ruecksprung.ts``, übersetzt das JS-Regex-Literal in ein Python-``re``-
Muster und prüft damit dieselben Fälle, die die Anmeldeseite gegen ein aus der URL
kommendes Rücksprungziel (``state.from``) entscheiden muss: interne, einfache Pfade
werden angenommen, alles, was auf eine andere Domain, ein Backslash-Trickpfad oder
eingebettete Kontrollzeichen (Tabulator, Zeilenumbruch) hindeutet, wird abgelehnt.

Die Quelle bleibt die TypeScript-Datei — dieser Test liest sie nur, er duplisiert das
Muster nicht als eigene Wahrheit (vgl. ``test_parameter_docs_complete.py``).
"""

from __future__ import annotations

import os
import re

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
RUECKSPRUNG_TS = os.path.join(REPO_ROOT, "frontend", "src", "lib", "ruecksprung.ts")


def _lade_python_muster() -> re.Pattern[str]:
    with open(RUECKSPRUNG_TS, "r", encoding="utf-8") as f:
        for zeile in f:
            if "RUECKSPRUNG_MUSTER" in zeile and "=" in zeile:
                treffer = re.search(r"=\s*/(.*)/\s*$", zeile.strip())
                assert treffer, f"Regex-Literal nicht gefunden in Zeile: {zeile!r}"
                js_quelle = treffer.group(1)
                return re.compile(js_quelle)
    raise AssertionError(f"RUECKSPRUNG_MUSTER nicht in {RUECKSPRUNG_TS} gefunden")


MUSTER = _lade_python_muster()

ANGENOMMEN = [
    "/",
    "/app",
    "/app/kommune/05315000?tab=karte",
]

ABGELEHNT = [
    "//evil.example",
    "/\\evil.example",
    "/app\\..\\x",
    "https://evil.example",
    "evil.example",
    "",
    "\t/app",
    "/ap\np",
]


def test_angenommene_ziele_passen() -> None:
    for ziel in ANGENOMMEN:
        assert MUSTER.match(ziel), f"sollte angenommen werden: {ziel!r}"


def test_abgelehnte_ziele_passen_nicht() -> None:
    for ziel in ABGELEHNT:
        assert not MUSTER.match(ziel), f"sollte abgelehnt werden: {ziel!r}"


def test_rot_lauf_bei_geaendertem_muster() -> None:
    """Gegenprobe: ein zu lockeres Muster (kein Ausschluss von '//') lässt die
    abgelehnten Fälle zu Unrecht durch — belegt, dass der Test tatsächlich prüft."""
    zu_lockeres_muster = re.compile(r"^/.*$")
    faelschlich_angenommen = [z for z in ABGELEHNT if zu_lockeres_muster.match(z)]
    assert faelschlich_angenommen, (
        "Rot-Lauf-Erwartung nicht erfüllt: das absichtlich zu lockere Muster hätte "
        "mindestens einen der abgelehnten Fälle durchlassen müssen, tat es aber nicht."
    )
