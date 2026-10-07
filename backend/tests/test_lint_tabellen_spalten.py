"""Test für T-1817-ceo: Jede Tabellenzeile hat die Spaltenzahl ihrer Kopfzeile.

Anlass: Befund 494 (T-1728-methodik_manager) — eine Zelle mit zwei unmaskierten
senkrechten Strichen verschob die Spalten im PDF.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from lint_methodik import Lint, tabellen_spalten, tabellen_spaltenzahl  # noqa: E402

RICHTIG = (
    "Text davor.\n\n"
    "| A | B | C |\n"
    "|---|---|---|\n"
    "| 1 | a \\| b | `x|y` |\n"
    "| 2 | d | e |\n"
)

ZU_VIEL = (
    "Text davor.\n\n"
    "| A | B | C |\n"
    "|---|---|---|\n"
    "| 1 | b | c |\n"
    "| 2 | d | e | f |\n"
)


def test_richtige_tabelle_ohne_fund():
    # maskierte Pipe und Pipe im Code-Span zaehlen nicht als Trenner
    assert tabellen_spaltenzahl(RICHTIG, "r.md") == []
    lint = Lint()
    tabellen_spalten(RICHTIG, lint, "r.md")
    assert lint.fehler == []


def test_zelle_zu_viel_meldet_datei_zeile_soll_ist():
    assert tabellen_spaltenzahl(ZU_VIEL, "k.md") == ["k.md Z. 6: Soll 3, Ist 4"]
    lint = Lint()
    tabellen_spalten(ZU_VIEL, lint, "k.md")
    assert len(lint.fehler) == 1 and "k.md Z. 6: Soll 3, Ist 4" in lint.fehler[0]


def test_code_zaun_wird_uebersprungen():
    src = "```\n| A | B |\n|---|---|\n| 1 | 2 | 3 |\n```\n"
    assert tabellen_spaltenzahl(src, "z.md") == []


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-q"]))
