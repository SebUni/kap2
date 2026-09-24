"""Übersicht der Methodik-Berichte (Aufsichtsrat, 24.09.2026): erzeugt aus Berichten, Prüfakten und Exporten."""

from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import methodik_uebersicht as u  # noqa: E402

LEDGER = """# Befund-Ledger #95

## Runde 3

| Nr | Befund | Kat. | Status | Umsetzungsnachweis | Prüfausdruck |
|---|---|---|---|---|---|
| 101 | Rechenkette fehlt | A | offen | — | — |
| 102 | Zeichentabelle | B | geschlossen: ergänzt | Z. 12 | `grep x` |
| 103 | Zahlenformat | C | offen | — | — |
"""


def _repo(tmp: Path) -> Path:
    (tmp / "docs" / "methodik").mkdir(parents=True)
    (tmp / "reviews").mkdir()
    (tmp / "docs" / "methodik" / "95_hitze.md").write_text(
        "# Methodik-Bericht #95 — Hitzebelastung\n\nStatus: **Rev. 9 — NICHT ABNAHMEREIF** · 24.09.2026\n\n"
        "## 3 Modell\n\n### 3.0 Rechenkette\n\n| Ebene | Rechenschritt | Wert (Beispielkommune X) | Quelle |\n", encoding="utf-8")
    (tmp / "docs" / "methodik" / "95_hitze.pdf").write_bytes(b"%PDF")
    (tmp / "docs" / "methodik" / "60_flut.md").write_text(
        "# Methodik-Bericht #60 — Flusshochwasser\n\nStatus: Rev. 4 — ABNAHMEREIF & INTEGRIERT\n\n## 3 Modell\n\nText.\n",
        encoding="utf-8")
    (tmp / "reviews" / "BEFUNDE_95.md").write_text(LEDGER, encoding="utf-8")
    return tmp


def test_zeilen_mit_stand_rechenkette_befunden_und_exporten(tmp_path):
    text = u.erzeugen(_repo(tmp_path))
    z95 = next(z for z in text.splitlines() if "| #95 |" in z)
    assert "| M0 | #95 | [Hitzebelastung](95_hitze.md) | Rev. 9, nicht abnahmereif | ja | 1/0/1 | 3 | [PDF](95_hitze.pdf) | — |" in z95
    z60 = next(z for z in text.splitlines() if "| #60 |" in z)
    assert "| M1+ | #60 |" in z60 and "Rev. 4, abnahmereif, integriert" in z60 and "**fehlt**" in z60
    assert text.index("| #60 |") < text.index("| #95 |"), "nach Nummer sortiert"
    assert "nicht von Hand ändern" in text


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-q"]))
