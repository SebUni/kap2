"""Test für T-0234: `pflichtkapitel_gefuellt()` zählt Substanz, nicht Checks.

Anlass (Befund 17 zu #60, Messrunde T-0232): Der Lint meldete 83 grüne Checks für
einen Bericht, dessen Kapitel 3, 4 und 6 zusammen drei Zeichen Substanz außerhalb
von HTML-Kommentaren trugen — er sah Kommentare nicht und prüfte die Pflichtkapitel
nie auf Füllung. Dieser Test deckt beide Richtungen ab: ein Bericht mit einem
leeren Pflichtkapitel (Kommentartext zählt nicht mit) wird rot, ein Bericht mit
gefüllten Pflichtkapiteln bleibt grün.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from lint_methodik import Lint, pflichtkapitel_gefuellt  # noqa: E402

FUELLTEXT = (
    "Dies ist echter Berichtstext mit ausreichend Substanz, damit das Kapitel "
    "nicht als leer gilt. " * 15
)


def _bericht(kapitel_3_inhalt: str) -> str:
    kapitel = {
        1: FUELLTEXT,
        2: FUELLTEXT,
        3: kapitel_3_inhalt,
        4: FUELLTEXT,
        5: FUELLTEXT,
        6: FUELLTEXT,
        7: FUELLTEXT,
        8: FUELLTEXT,
        9: FUELLTEXT,
    }
    namen = {
        1: "Wirkungskette & Knoten-Bilanz", 2: "Evidenz-Register", 3: "Modell",
        4: "Kalibrierung & Validierung", 5: "Maßnahmen-Hebel",
        6: "Szenario-Anwendung & Modellgrenzen", 7: "Parameter-Blöcke",
        8: "Quellen", 9: "Ansatz-Vergleich",
    }
    teile = [f"## {n} {namen[n]}\n{kapitel[n]}\n" for n in range(1, 10)]
    return "\n".join(teile)


def test_leeres_pflichtkapitel_wird_rot():
    """Ein Pflichtkapitel, das nur einen HTML-Kommentar trägt, zählt als leer."""
    bericht = _bericht("<!-- wird spaeter nachgezogen, hier steht noch nichts -->")
    lint = Lint()
    pflichtkapitel_gefuellt(bericht, lint)
    rot = [f for f in lint.fehler if f.startswith("Pflichtkapitel 3")]
    assert len(rot) == 1
    assert "Modell" in rot[0]
    assert "Zeichen Substanz" in rot[0]


def test_wenige_zeichen_ausserhalb_kommentar_bleibt_rot():
    """Drei Zeichen Substanz (Befund 17) reichen nicht — bleibt unter der Schwelle."""
    bericht = _bericht("xyz")
    lint = Lint()
    pflichtkapitel_gefuellt(bericht, lint)
    rot = [f for f in lint.fehler if f.startswith("Pflichtkapitel 3")]
    assert len(rot) == 1


def test_gefuellte_pflichtkapitel_bleiben_gruen():
    bericht = _bericht(FUELLTEXT)
    lint = Lint()
    pflichtkapitel_gefuellt(bericht, lint)
    assert lint.fehler == []
    assert any(f.startswith("Pflichtkapitel 3") for f in lint.ok)


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-q"]))
