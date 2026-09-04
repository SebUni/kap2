"""Test für T-0007: `verbotene_formulierungen()` prüft zeilenweise und respektiert
den Historie-Marker.

Anlass: Der Check sass bislang im Rumpf von `zeichentabelle()` — er lief also nur,
wenn deren Abschnitt gefunden wurde — und verglich `wort not in src` über den
GESAMTEN Bericht. Das schlug auch innerhalb längerer Wörter an (»Platzhalterzitat«
enthält »Platzhalter«, Bericht #95 Quelle [47]) und nannte nie, WO im Bericht der
Treffer sitzt. Jetzt läuft er unabhängig von `zeichentabelle()`, meldet die
Zeilennummer und lässt sich — wie der Abgelöste-Werte-Check — über den expliziten
`HISTORIE_MARKER` mit Pflicht-`REVISIONSVERMERK` als dokumentierter, behobener
Befund kennzeichnen.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from lint_methodik import Lint, UNTERDRUECKT, verbotene_formulierungen  # noqa: E402


def test_verbotswort_in_gewoehnlicher_zeile_erzeugt_genau_einen_fehler_mit_zeilennummer():
    bericht = (
        "### 1 Einleitung\n"
        "Text ohne Auffaelligkeiten.\n"
        "Dieser Wert ist ein Platzhalter und muss noch ersetzt werden.\n"
        "Weiterer Text.\n"
    )
    lint = Lint()
    UNTERDRUECKT.clear()
    verbotene_formulierungen(bericht, lint)
    treffer = [f for f in lint.fehler if "verbotene Formulierung" in f]
    assert len(treffer) == 1
    assert "Zeile 3" in treffer[0]


def test_verbotswort_mit_marker_und_revisionsvermerk_wird_unterdrueckt():
    bericht = (
        "### 1 Einleitung\n"
        "Text ohne Auffaelligkeiten.\n"
        "Die fruehere Angabe stammte aus dem unverifizierten Rev.-5-"
        "Platzhalterzitat und steht nicht in der Studie. <!--hist-->\n"
        "Weiterer Text.\n"
    )
    lint = Lint()
    UNTERDRUECKT.clear()
    verbotene_formulierungen(bericht, lint)
    treffer = [f for f in lint.fehler if "verbotene Formulierung" in f]
    assert treffer == []
    assert UNTERDRUECKT.get("<!--hist-->")


def test_verbotswort_mit_marker_ohne_revisionsvermerk_bleibt_rot():
    bericht = (
        "### 1 Einleitung\n"
        "Text ohne Auffaelligkeiten.\n"
        "Dieser Wert ist ein Platzhalter und gilt heute. <!--hist-->\n"
        "Weiterer Text.\n"
    )
    lint = Lint()
    UNTERDRUECKT.clear()
    verbotene_formulierungen(bericht, lint)
    treffer = [f for f in lint.fehler
               if f.startswith("Historie-Marker ohne Revisionsvermerk")]
    assert len(treffer) == 1


def test_bericht_ohne_verbotswort_erzeugt_keinen_fehler():
    bericht = (
        "### 1 Einleitung\n"
        "Text ohne jede Auffaelligkeit.\n"
        "Noch mehr unauffaelliger Text.\n"
    )
    lint = Lint()
    UNTERDRUECKT.clear()
    verbotene_formulierungen(bericht, lint)
    treffer = [f for f in lint.fehler if "verbotene Formulierung" in f]
    assert treffer == []


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-q"]))
