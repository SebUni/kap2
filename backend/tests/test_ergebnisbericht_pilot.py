"""Formatpilot des PDF-Ergebnisberichts (T-1414): Teile 0, 1, 4 (#95), 7 und 8 für Warmsen.

Der Test ruft im Ordner ``backend/`` mit dem Python der Testlauf-Umgebung

    python -m app.cli ergebnisbericht --beispiel warmsen --teile 0,1,4,7,8 \
        --aus /tmp/kap2-ergebnisbericht/pilot-95.pdf

auf und prüft (a) die PDF-Kennung, (b) die HTML-Vorstufe daneben, (c) die Überschriften der fünf
Teile im Text aus ``scripts/pdf_text.py`` und (d) den Jahresbetrag #95 in der Schreibweise des
Produkts. Der Betrag wird hier über die Schicht-B-Funktionen von #95 (``impact.health.mortality``
und ``impact.health.morbidity``) aus denselben gepinnten Zelldaten gerechnet — mit der Rechnung
des Golden-Tests ``test_methodik_95_golden_betraege.py``, nicht mit dem Code des Berichts und
nicht als abgeschriebene Zahl.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

import pytest

HIER = os.path.dirname(os.path.abspath(__file__))
BACKEND = os.path.dirname(HIER)
REPO = os.path.dirname(BACKEND)
sys.path.insert(0, BACKEND)
sys.path.insert(0, HIER)

from test_methodik_95_golden_betraege import WARMSEN, _jahresbetrag  # noqa: E402

AUS_PDF = "/tmp/kap2-ergebnisbericht/pilot-95.pdf"
AUS_HTML = "/tmp/kap2-ergebnisbericht/pilot-95.html"

UEBERSCHRIFTEN = [
    "Teil 0 · Kopf und Identität",
    "Teil 1 · Beschlussfähige Zusammenfassung",
    "Teil 4 · Betroffenheitsanalyse je Klimawirkung",
    "Teil 7 · Parameter- und Quellenverzeichnis",
    "Teil 8 · Grenzen und Vollständigkeitsanzeige",
]


def _de_euro(wert: float) -> str:
    """Schreibweise des Produkts für Beträge (``kurzfassung_markdown._de_euro``)."""
    from app.services.kurzfassung_markdown import _de_euro as produkt
    return produkt(wert)


@pytest.fixture(scope="module")
def pdf_text() -> str:
    for pfad in (AUS_PDF, AUS_HTML):
        if os.path.exists(pfad):
            os.remove(pfad)
    lauf = subprocess.run(
        [sys.executable, "-m", "app.cli", "ergebnisbericht", "--beispiel", "warmsen",
         "--teile", "0,1,4,7,8", "--aus", AUS_PDF],
        cwd=BACKEND, capture_output=True, text=True, timeout=600,
    )
    assert lauf.returncode == 0, lauf.stdout[-2000:] + lauf.stderr[-4000:]
    text = subprocess.run(
        [sys.executable, os.path.join(REPO, "scripts", "pdf_text.py"), AUS_PDF],
        capture_output=True, text=True, timeout=120,
    )
    assert text.returncode == 0, text.stderr[-2000:]
    return re.sub(r"\s+", " ", text.stdout)


def test_a_pdf_kennung(pdf_text):
    with open(AUS_PDF, "rb") as fh:
        assert fh.read(5) == b"%PDF-"


def test_b_html_vorstufe(pdf_text):
    assert os.path.isfile(AUS_HTML)
    with open(AUS_HTML, encoding="utf-8") as fh:
        assert "Warmsen" in fh.read()


@pytest.mark.parametrize("ueberschrift", UEBERSCHRIFTEN)
def test_c_ueberschriften(pdf_text, ueberschrift):
    assert ueberschrift in pdf_text


def test_d_jahresbetrag_95(pdf_text):
    betrag = _jahresbetrag(WARMSEN)
    erwartet = _de_euro(betrag)
    assert re.fullmatch(r"\d{1,3}(\.\d{3})* €", erwartet), erwartet
    assert erwartet in pdf_text, f"{erwartet} fehlt im PDF-Text"
