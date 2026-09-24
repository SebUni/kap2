"""Zahlenformat im Lint nach dem Stil-Skill `kap3-stil` (Aufsichtsrat, 24.09.2026; Aufgabe §8 E5).

Wiederkehrende Arbeit wird immer gleich ausgeführt, bis in die Schreibweise: „1,2 Mio. €“, nicht einmal so und einmal
„1000000 €“. Geprüft wird nur Fließtext — Code-Blöcke, Formeln, Inline-Code und Links bleiben unberührt.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from lint_methodik import Lint, zahlenformat  # noqa: E402


def _fehler(src: str) -> list[str]:
    lint = Lint()
    zahlenformat(src, lint)
    return lint.fehler


def test_richtige_schreibweise_bleibt_gruen():
    assert _fehler("Der Schaden beträgt 1,2 Mio. € je Jahr, in der Spanne 0,8–1,6 Mio. €; 350.000 € entfallen auf "
                   "die Morbidität, 12 % der Fälle auf Männer, 3,4 Mrd. € bundesweit.") == []


def test_falsche_schreibweisen_werden_rot():
    fehler = " | ".join(_fehler("Summe 1.200.000 €.\nOder 1200000 Euro.\nEtwa 1,2 Millionen Euro.\nJe Fall 480 EUR.\n"
                                "Anteil 12%."))
    assert "Mio. €“ — 2×" in fehler
    assert "statt ausgeschriebener Währung" in fehler
    assert "„€“ statt „EUR“" in fehler
    assert "Leerzeichen vor „%“" in fehler
    assert "Z. 1: 1.200.000 €" in fehler


def test_code_formeln_und_links_zaehlen_nicht():
    src = ("```python test: x\nkosten = 1200000  # 1.200.000 €\n```\n"
           "Formel $S = 1{.}200{.}000\\,€$ und `12%` im Code.\n"
           "Quelle: https://example.org/tabelle?wert=12%\n"
           "<!-- alter Wert 1.200.000 € -->\n")
    assert _fehler(src) == []


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-q"]))
