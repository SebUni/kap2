"""Verwechslungssperre Klasse A/B in den Nebenansichten (T-0518, Vorhaben T-0358).

Liest die Lite-Ansicht (LitePanel.tsx) und die Studienseite (StudyPage.tsx) als
Text (ohne Node/Browser) und prüft je Datei:

(1) an der Stelle des Schadenswerts steht ein Zweig auf ``has_euro_layer``, der
    ``cost_display`` ausgibt (Klasse B → Screening-Vermerk des Backends);
(2) die Ausgabe des Schadenswerts hängt nicht mehr allein an der Bedingung
    ``cost_eur > 0`` — jede solche Bedingung steht zusammen mit einem Zweig auf
    ``has_euro_layer`` (gleiche Zeile oder die zwei Zeilen davor).

Kommentare werden vor der Prüfung entfernt, damit ein Kommentar allein keinen
Treffer erzeugt. Muster: test_klasse_b_oberflaeche.py.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

PAGES = Path(__file__).resolve().parents[2] / "frontend" / "src" / "pages"

LITE_PANEL = "lite/LitePanel.tsx"
STUDY_PAGE = "StudyPage.tsx"

# Anker der Schadenswert-Stelle je Datei.
ANKER = {
    LITE_PANEL: "lite-outcome",
    STUDY_PAGE: "Schaden/Jahr",
}


def _code(name: str) -> str:
    """Quelltext ohne Block-/JSX-Kommentare und ohne reine Zeilenkommentare."""
    text = re.sub(r"/\*.*?\*/", "", (PAGES / name).read_text(encoding="utf-8"), flags=re.S)
    return "\n".join(z for z in text.splitlines() if not z.lstrip().startswith("//"))


# Ternärer Zweig auf has_euro_layer, dessen einer Arm cost_display ausgibt —
# der Zweig darf über wenige Zeilen gehen (JSX), aber nicht über ein anderes ':' hinweg
# in den Klasse-A-Arm (oder umgekehrt, wenn der Vermerk im zweiten Arm steht).
_ZWEIG = re.compile(
    r"has_euro_layer\s*===\s*false\s*\?[^:]{0,160}?cost_display"
    r"|has_euro_layer\s*(?:!==\s*false\s*)?\?[^?]{0,300}?:[^:?]{0,160}?cost_display",
    re.S,
)

_NUR_COST = re.compile(r"cost_eur\s*>\s*0")


@pytest.mark.parametrize("name", [LITE_PANEL, STUDY_PAGE])
def test_schadenswert_zweig_auf_has_euro_layer(name):
    code = _code(name)
    pos = code.find(ANKER[name])
    assert pos != -1, f"{name}: Schadenswert-Stelle „{ANKER[name]}“ fehlt"
    assert any(m.start() > pos for m in _ZWEIG.finditer(code)), (
        f"{name}: kein Zweig auf has_euro_layer, der beim Schadenswert cost_display ausgibt")


@pytest.mark.parametrize("name", [LITE_PANEL, STUDY_PAGE])
def test_schadenswert_nicht_allein_an_cost_eur(name):
    zeilen = _code(name).splitlines()
    for i, zeile in enumerate(zeilen):
        if not _NUR_COST.search(zeile):
            continue
        umfeld = "\n".join(zeilen[max(0, i - 2): i + 1])
        assert "has_euro_layer" in umfeld, (
            f"{name}: Zeile {i + 1} hängt allein an cost_eur > 0: {zeile.strip()}")
