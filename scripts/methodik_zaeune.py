#!/usr/bin/env python3
"""Schreibt die Zaunform „python test: <name>“ in gewöhnliche Python-Zäune um.

pandoc erkennt einen Zaun mit dem Infostring „python test: <name>“ nicht als Code-Block;
das Rechenbeispiel erscheint im Lese-PDF als Fließtext. Der PDF-Export ruft deshalb diese
Vorverarbeitung auf einer Kopie auf. Die Markdown-Quelle bleibt unverändert, denn die
Golden-Tests lesen die Zaunform „python test:“ aus der Quelle.

Aufruf: python3 scripts/methodik_zaeune.py <ein.md> <aus.md>
"""
from __future__ import annotations

import sys

_ZAUN = "`" * 3
_PRAEFIX = _ZAUN + "python test:"


def zaeune_normalisieren(text: str) -> str:
    """Ersetzt jede Zeile „```python test: <name>“ durch „```python“; alles andere bleibt gleich."""
    zeilen = text.splitlines(keepends=True)
    for i, zeile in enumerate(zeilen):
        if zeile.startswith(_PRAEFIX) and zeile[len(_PRAEFIX):].strip():
            inhalt = zeile.rstrip("\r\n")
            zeilen[i] = _ZAUN + "python" + zeile[len(inhalt):]
    return "".join(zeilen)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("Aufruf: methodik_zaeune.py <ein.md> <aus.md>", file=sys.stderr)
        return 2
    with open(argv[1], encoding="utf-8", newline="") as f:
        text = f.read()
    with open(argv[2], "w", encoding="utf-8", newline="") as f:
        f.write(zaeune_normalisieren(text))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
