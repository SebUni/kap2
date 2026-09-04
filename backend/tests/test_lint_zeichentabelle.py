"""Test für T-0006: `zeichentabelle()` findet den Abschnitt über die Überschrift,
nicht über eine fest verdrahtete Abschnittsnummer.

Anlass: Der Lint suchte hartcodiert `### 3.5 Zeichentabelle` und meldete bei den
Berichten #95/#96 (Zeichentabelle unter `### 3.6 Zeichentabelle`) fälschlich einen
fehlenden Abschnitt, obwohl die Tabelle dort vollständig vorhanden ist.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from lint_methodik import Lint, zeichentabelle  # noqa: E402

TABELLE = """
| Zeichen | Name | Einheit | Wert / Herkunft |
|---|---|---|---|
| \\(a\\) | Altersband | -- | Zensus-Altersbaender |
| \\(c\\) | Kostensatz | EUR | 7.152 [17]; register:95-E02-02 |
"""


def _bericht(ueberschrift: str) -> str:
    return (
        "### 3.4 Irgendwas\n"
        "Text davor.\n\n"
        f"{ueberschrift}\n"
        f"{TABELLE}\n"
        "### 4 Naechster Abschnitt\n"
        "Text danach.\n"
    )


def test_zeichentabelle_unter_3_5_wird_gefunden():
    lint = Lint()
    zeichentabelle(_bericht("### 3.5 Zeichentabelle"), lint)
    zeichentabelle_fehler = [f for f in lint.fehler if f.startswith("Zeichentabelle:")]
    assert zeichentabelle_fehler == []


def test_zeichentabelle_unter_3_6_wird_ebenfalls_gefunden():
    lint = Lint()
    zeichentabelle(_bericht("### 3.6 Zeichentabelle"), lint)
    zeichentabelle_fehler = [f for f in lint.fehler if f.startswith("Zeichentabelle:")]
    assert zeichentabelle_fehler == []


def test_ohne_zeichentabellen_ueberschrift_genau_ein_fehler():
    bericht = (
        "### 3.4 Irgendwas\n"
        "Text ohne jede Zeichentabelle.\n\n"
        "### 4 Naechster Abschnitt\n"
        "Text danach.\n"
    )
    lint = Lint()
    zeichentabelle(bericht, lint)
    zeichentabelle_fehler = [f for f in lint.fehler if f.startswith("Zeichentabelle:")]
    assert len(zeichentabelle_fehler) == 1


def test_malformed_zeile_mit_drei_zellen_erzeugt_fehler():
    kaputte_tabelle = """
| Zeichen | Name | Einheit | Wert / Herkunft |
|---|---|---|---|
| \\(a\\) | Altersband | Zensus-Altersbaender |
"""
    bericht = (
        "### 3.5 Zeichentabelle\n"
        f"{kaputte_tabelle}\n"
        "### 4 Naechster Abschnitt\n"
    )
    lint = Lint()
    zeichentabelle(bericht, lint)
    malformed = [f for f in lint.fehler if "malformed" in f]
    assert len(malformed) == 1


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-q"]))
