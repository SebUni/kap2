"""Test für T-1981-ceo: Werkzeuge der Läufe — Interpreter und `--schliesse`.

Punkt 2: `ledger.py --pruefe` führt einen Prüfausdruck, der mit `python3 ` beginnt,
mit `sys.executable` aus, nicht mit dem `python3` vom PATH. Der Test ruft die
Ausführungsfunktion des Werkzeugs selbst auf (`_fuehre_aus`), baut sie nicht nach.

Punkt 3: `ledger.py --schliesse` schließt einen Befund mit Status
„zurückgestellt (Termin …)“ genauso wie einen offenen.

Punkt 1: `projektumgebung_neu_starten` in `ledger.py` und `lint_methodik.py` tut
nichts, solange numpy und shapely importierbar sind (so auch in der Testumgebung),
und startet sonst mit `os.execv` neu — hier mit ersetztem `execv`, ohne Prozesswechsel.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import ledger  # noqa: E402
import lint_methodik  # noqa: E402


# ------------------------------------------------------------ Punkt 2


def test_pruefausdruck_mit_python3_nutzt_sys_executable() -> None:
    rc, ausgabe = ledger._fuehre_aus('python3 -c "import sys; print(sys.executable)"')
    assert rc == 0
    assert ausgabe == sys.executable


def test_pruefausdruck_mit_negation_nutzt_sys_executable() -> None:
    rc, _ = ledger._fuehre_aus('! python3 -c "import sys; sys.exit(1)"')
    assert rc == 0


def test_andere_kommandos_bleiben_unveraendert() -> None:
    assert ledger._mit_eigenem_interpreter("grep -q python3 datei") == "grep -q python3 datei"
    assert ledger._mit_eigenem_interpreter("python3.12 -c 1") == "python3.12 -c 1"


# ------------------------------------------------------------ Punkt 3

MINI_LEDGER = """# Befunde 99 (Test)

## Offene Befunde (2)

| Nr | Befund (Ort · Art) | Kat | Status | Nachweis | Prüfausdruck |
|---|---|---|---|---|---|
| 1 | Bericht Kap. 1 · Lücke — offener Beispielbefund | B | offen | – | `python3 -c "pass"` |
| 2 | Bericht Kap. 2 · Lücke — zurückgestellter Beispielbefund | B | zurückgestellt (Termin: Rev. 3) | – | `python3 -c "pass"` |
| 3 | Bericht Kap. 3 · Lücke — zurückgestellt, Ausdruck rot | B | zurückgestellt (Termin: Rev. 4) | – | `python3 -c "raise SystemExit(1)"` |
"""


def test_schliesse_schliesst_zurueckgestellte_wie_offene(tmp_path: Path) -> None:
    pfad = tmp_path / "BEFUNDE_99.md"
    pfad.write_text(MINI_LEDGER, encoding="utf-8")

    assert ledger.cmd_schliesse(pfad) == 0

    lagen = {b.nr: b.lage for b in ledger.parse(pfad)}
    assert lagen == {"1": "geschlossen", "2": "geschlossen", "3": "zurückgestellt"}
    text = pfad.read_text(encoding="utf-8")
    # Nur die Statuszelle der beiden grünen Befunde ändert sich; Befund 3 bleibt Wort für Wort.
    assert "| zurückgestellt (Termin: Rev. 4) |" in text
    assert "zurückgestellt (Termin: Rev. 3)" not in text


# ------------------------------------------------------------ Punkt 1


@pytest.mark.parametrize("modul", [ledger, lint_methodik])
def test_neustart_nur_wenn_pakete_fehlen(modul, tmp_path: Path, monkeypatch, capsys) -> None:
    venv = tmp_path / "venv"
    (venv / "bin").mkdir(parents=True)
    py = venv / "bin" / "python"
    py.write_text("#!/bin/sh\n", encoding="utf-8")
    py.chmod(0o755)
    monkeypatch.setenv("KAP2_VENV", str(venv))
    aufrufe: list[tuple[str, list[str]]] = []
    monkeypatch.setattr(os, "execv", lambda pfad, argv: aufrufe.append((pfad, argv)))
    monkeypatch.setattr(sys, "argv", ["skript.py", "95"])

    # Pakete vorhanden: kein Neustart, keine Ausgabe.
    echte_find_spec = importlib.util.find_spec
    modul.projektumgebung_neu_starten()
    assert aufrufe == []
    assert capsys.readouterr().out == ""

    # numpy fehlt: genau eine Zeile „Projektumgebung: …“, dann execv mit denselben Argumenten.
    monkeypatch.setattr(importlib.util, "find_spec",
                        lambda n, *a, **k: None if n == "numpy" else echte_find_spec(n, *a, **k))
    modul.projektumgebung_neu_starten()
    assert aufrufe == [(str(py), [str(py), "skript.py", "95"])]
    assert capsys.readouterr().out == f"Projektumgebung: {py}\n"

    # Keine Projektumgebung: wie bisher, kein Neustart.
    aufrufe.clear()
    monkeypatch.setenv("KAP2_VENV", str(tmp_path / "gibt-es-nicht"))
    modul.projektumgebung_neu_starten()
    assert aufrufe == []
    assert capsys.readouterr().out == ""
