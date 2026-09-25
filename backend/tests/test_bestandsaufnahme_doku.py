"""Tests gegen docs/BESTANDSAUFNAHME.md (T-0756, Vorhaben T-0447).

Prüft die Methodendoku der Bestandsaufnahme gegen den Katalog
``app.data.bestandsaufnahme``: Überschriften, Tabelle und Lückensätze.
"""
from pathlib import Path

from app.data.bestandsaufnahme import BESTANDSAUFNAHME_GROESSEN as GROESSEN

DOKU_PFAD = Path(__file__).resolve().parents[2] / "docs" / "BESTANDSAUFNAHME.md"

UEBERSCHRIFTEN = [
    "## Zweck und Einordnung",
    "## Erhobene Größen",
    "## Lücken und Abgrenzung",
]


def _text() -> str:
    return DOKU_PFAD.read_text(encoding="utf-8")


def _abschnitt(text: str, ueberschrift: str) -> str:
    zeilen = text.splitlines()
    start = next((i + 1 for i, z in enumerate(zeilen) if z.strip() == ueberschrift), None)
    assert start is not None, f"Überschrift nicht gefunden: {ueberschrift}"
    ende = len(zeilen)
    for j in range(start, len(zeilen)):
        if zeilen[j].startswith("## "):
            ende = j
            break
    return "\n".join(zeilen[start:ende])


def _tabellenzeilen(abschnittstext: str) -> list[list[str]]:
    zeilen = [z for z in abschnittstext.splitlines() if z.strip().startswith("|")]
    assert zeilen, "keine Markdown-Tabelle im Abschnitt gefunden"
    daten = []
    kopf = trenner = False
    for zeile in zeilen:
        zellen = [z.strip() for z in zeile.strip().strip("|").split("|")]
        if not kopf:
            kopf = True
            continue
        if not trenner and all(set(z) <= set("-: ") for z in zellen):
            trenner = True
            continue
        daten.append(zellen)
    return daten


def test_ueberschriften_je_einmal_in_reihenfolge():
    zeilen = [z.strip() for z in _text().splitlines()]
    positionen = []
    for u in UEBERSCHRIFTEN:
        assert zeilen.count(u) == 1, f"{u} nicht genau einmal"
        positionen.append(zeilen.index(u))
    assert positionen == sorted(positionen)


def test_tabelle_20_zeilen_codes_in_katalogreihenfolge():
    zeilen = _tabellenzeilen(_abschnitt(_text(), "## Erhobene Größen"))
    assert len(zeilen) == 20
    assert [z[0] for z in zeilen] == [g["code"] for g in GROESSEN]


def test_alle_elf_lueckensaetze_wortlich():
    text = _text()
    saetze = [g["luecke"] for g in GROESSEN if g["luecke"]]
    assert len(saetze) == 11
    for satz in saetze:
        assert satz in text, f"Lückensatz fehlt: {satz}"
