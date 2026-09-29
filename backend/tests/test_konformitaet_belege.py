"""Konformitätsliste: Jeder Pfad in der Spalte „Beleg im Produkt“ existiert im Repo.

Geprüft wird nur die Existenz der genannten Dateien — kein Status, kein Urteil,
keine Spaltenzahl (Status und Gegenproben schreibt der CMO fort).
"""
from __future__ import annotations

import pathlib
import re

WURZEL = pathlib.Path(__file__).resolve().parents[2]
CHECKLISTE = WURZEL / "docs" / "KONFORMITAET_CHECKLISTE.md"

_ZEILE = re.compile(r"^\|\s*\d+\s*\|")
_BACKTICK = re.compile(r"`([^`]*)`")


def _pfade(text: str) -> list[str]:
    pfade: list[str] = []
    for zeile in text.splitlines():
        if not _ZEILE.match(zeile):
            continue
        spalten = zeile.split(" | ")
        if len(spalten) <= 5:
            continue
        for stueck in spalten[5].split(","):
            stueck = stueck.strip()
            if not stueck:
                continue
            treffer = _BACKTICK.search(stueck)
            if treffer:
                inhalt = treffer.group(1).strip()
            else:
                inhalt = re.split(r"[ (]", stueck, maxsplit=1)[0]
            inhalt = inhalt.split("::", 1)[0].split("#", 1)[0]
            if "/" in inhalt:
                pfade.append(inhalt)
    return pfade


def fehlende_belege(text: str, wurzel: pathlib.Path) -> list[str]:
    """Pfade aus der Belegspalte, die unter ``wurzel`` nicht existieren."""
    return [p for p in _pfade(text) if not (wurzel / p).exists()]


def test_alle_belegpfade_existieren():
    text = CHECKLISTE.read_text(encoding="utf-8")
    assert fehlende_belege(text, WURZEL) == []


def test_mindestens_70_pfade_gefunden():
    text = CHECKLISTE.read_text(encoding="utf-8")
    assert len(_pfade(text)) >= 70


def test_rotprobe_fehlender_pfad_wird_gemeldet():
    zeile = "| 99 | a | b | c | d | backend/gibt_es_nicht.py, docs/BETRIEB.md | e |"
    assert fehlende_belege(zeile, WURZEL) == ["backend/gibt_es_nicht.py"]
