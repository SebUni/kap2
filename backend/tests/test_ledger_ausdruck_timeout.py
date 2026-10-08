"""Test für T-1893-ceo: Die Zeitgrenze eines Prüfausdrucks in `ledger.py` kommt aus
`LEDGER_AUSDRUCK_TIMEOUT_S`; ohne die Variable gilt 90 s, ein ungültiger Wert
fällt mit Warnzeile auf 90 s zurück. Kein Datenbankzugriff.

Anlass: Bei Serverlast (07.10.2026, Last 43 auf 2 Kernen) brauchte ein Ausdruck
37,6 s; die feste Grenze von 25 s erzeugte ein falsches Rot.
"""

from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import ledger  # noqa: E402

VARIABLE = "LEDGER_AUSDRUCK_TIMEOUT_S"
SCHLAEFT_3S = 'python3 -c "import time; time.sleep(3)"'


def test_variable_1_beendet_schlafenden_ausdruck_mit_124(monkeypatch):
    monkeypatch.setenv(VARIABLE, "1")
    rc, meldung = ledger._fuehre_aus(SCHLAEFT_3S)
    assert rc == 124
    assert meldung.startswith("TIMEOUT nach 1s")
    assert VARIABLE in meldung


def test_ohne_variable_gilt_90(monkeypatch):
    monkeypatch.delenv(VARIABLE, raising=False)
    assert ledger._ausdruck_timeout() == 90


@pytest.mark.parametrize("roh", ["abc", "0", "-5", "nan", "inf"])
def test_ungueltiger_wert_faellt_mit_warnung_auf_90(monkeypatch, capsys, roh):
    monkeypatch.setenv(VARIABLE, roh)
    ledger._WARNUNG_GEZEIGT.discard(roh)
    assert ledger._ausdruck_timeout() == 90
    assert "WARNUNG" in capsys.readouterr().err


def test_gueltige_dezimalzahl_wird_uebernommen(monkeypatch):
    monkeypatch.setenv(VARIABLE, "12.5")
    assert ledger._ausdruck_timeout() == 12.5
