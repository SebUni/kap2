"""Test des Methodendokuments docs/ANPASSUNGSKAPAZITAET.md (T-0761, Teil D von T-0448).

Liest die Datei als Text, ohne Import aus ``app`` (unabhängig von Teil A).
Läuft mit pytest oder direkt: ``python tests/test_anpassungskapazitaet_doku.py``.
"""

from __future__ import annotations

import os
import re

DOKUMENT_PFAD = os.path.join(
    os.path.dirname(__file__), "..", "..", "docs", "ANPASSUNGSKAPAZITAET.md"
)

UEBERSCHRIFTEN = [
    "## Zweck",
    "## Komponenten",
    "## Reifegradskala",
    "## Gesamtstufe und Ableitung der Risikominderung",
    "## Quellen und Abschätzung",
    "## Grenzen",
]

OPTIONAL_SATZ = (
    "Die Analyse der Anpassungskapazität ist nach ISO 14091 ein optionaler "
    "Analyseschritt; sie ergänzt die Bewertung des Klimarisikos ohne (weitere) "
    "Anpassung und ersetzt sie nicht."
)

KOMPONENTEN = [
    "Organisationsbezogene Fähigkeit",
    "Technisches Vermögen",
    "Finanzielle Fähigkeit",
    "Fähigkeit des Ökosystems",
]

REIFEGRADE = ["nicht vorhanden", "im Aufbau", "etabliert", "vorausschauend"]


def _text() -> str:
    with open(DOKUMENT_PFAD, encoding="utf-8") as f:
        return f.read()


def test_ueberschriften_in_reihenfolge():
    ueberschriften = re.findall(r"^## .*$", _text(), flags=re.MULTILINE)
    assert ueberschriften == UEBERSCHRIFTEN


def test_optional_satz_wortlich():
    assert OPTIONAL_SATZ in _text()


def test_komponentenbezeichnungen():
    text = _text()
    for name in KOMPONENTEN:
        assert name in text, name


def test_reifegradbezeichnungen():
    text = _text()
    for name in REIFEGRADE:
        assert name in text, name


if __name__ == "__main__":
    test_ueberschriften_in_reihenfolge()
    test_optional_satz_wortlich()
    test_komponentenbezeichnungen()
    test_reifegradbezeichnungen()
    print("ok")
