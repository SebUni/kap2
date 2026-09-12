"""Tests für T-0195: Der Deploy-Schritt `dienst` startet den Dienst ohne Rechteausweitung
per sudo neu und prüft, dass danach wirklich der neue Prozess antwortet.

Anlass: Das Test-Deployment brach im Schritt `dienst` ab — `systemctl restart kap2-test`
brauchte root-Rechte, und `sudo` scheitert unter der Sperre „no new privileges" des
aufrufenden Prozesses grundsätzlich. Zweiter Befund: Der frühere Health-Check fragte nur
`/api/health` ab; antwortete dort ein alter, weiterlaufender Prozess, meldete der Deploy
fälschlich `fertig`, obwohl der neue Stand nie gestartet war.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

WURZEL = Path(__file__).resolve().parents[2]
SKRIPT = WURZEL / "deploy" / "test-deploy.sh"
UNIT = WURZEL / "deploy" / "kap2-test.service"
POLKIT = WURZEL / "deploy" / "polkit-kap2-test.rules"
MAIN = WURZEL / "backend" / "app" / "main.py"


def _dienst_block() -> str:
    text = SKRIPT.read_text(encoding="utf-8")
    anfang = text.index('SCHRITT="dienst"')
    ende = text.index('SCHRITT="status"')
    return text[anfang:ende]


def test_dienst_startet_ohne_sudo_neu():
    """Kein sudo: unter „no new privileges" kann es grundsätzlich nicht nach root wechseln."""
    block = _dienst_block()
    # Kommentarzeilen ausnehmen: dort wird der Verzicht auf sudo gerade begründet.
    befehle = "\n".join(
        z for z in block.splitlines() if not z.lstrip().startswith("#")
    )
    assert not re.search(r"(^|\s)sudo\s", befehle), befehle
    assert "systemctl restart kap2-test" in block


def test_dienst_schritt_wird_nicht_uebersprungen():
    """Scheitert der Neustart, bricht der Lauf ab (`false`) — er wird nicht weggelassen."""
    block = _dienst_block()
    assert "if ! systemctl restart kap2-test; then" in block
    # Im Fehlerzweig steht ein `false`, das den ERR-Trap auslöst.
    fehlerzweig = block[block.index("if ! systemctl restart kap2-test; then"):]
    assert "false" in fehlerzweig.split("fi", 1)[0]


def test_dienst_prueft_vorbedingung_unit_vorhanden():
    """Fehlt die Unit, gibt es eine verständliche Anweisung statt einer nackten Fehlermeldung."""
    block = _dienst_block()
    assert "systemctl list-unit-files kap2-test.service" in block
    assert "/etc/systemd/system/" in block
    assert "50-kap2-test.rules" in block


def test_dienst_prueft_identitaet_des_neuen_prozesses():
    """MainPID muss sich ändern und /api/health den ausgerollten Commit melden."""
    block = _dienst_block()
    assert "MainPID" in block
    assert '"$NEU_PID" != "$ALT_PID"' in block
    assert '"$GEMELDET" == "$COMMIT"' in block


def test_unit_laeuft_nicht_als_root():
    """Sicherheitsregression ausschließen: User=/Group= müssen gesetzt sein."""
    text = UNIT.read_text(encoding="utf-8")
    assert "\nUser=overlord\n" in text
    assert "\nGroup=overlord\n" in text


def test_polkit_regel_ist_eng_gefasst():
    """Freigegeben wird genau eine Unit für genau einen Benutzer."""
    text = POLKIT.read_text(encoding="utf-8")
    assert 'subject.user !== "overlord"' in text
    assert 'action.lookup("unit") !== "kap2-test.service"' in text
    assert "org.freedesktop.systemd1.manage-units" in text


def test_health_meldet_commit_und_startzeit():
    """/api/health liefert die Kennung des antwortenden Prozesses."""
    text = MAIN.read_text(encoding="utf-8")
    gesundheit = text[text.index('@app.get("/api/health")'):]
    assert '"commit": COMMIT' in gesundheit
    assert '"gestartet": PROZESS_START' in gesundheit
    assert '"status": "ok"' in gesundheit


def test_commit_ermittlung_liefert_kurz_hash():
    """Die Herleitung des Commits (git rev-parse --short HEAD im Repo) funktioniert hier."""
    ergebnis = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=WURZEL,
        capture_output=True,
        text=True,
        check=True,
    )
    assert re.fullmatch(r"[0-9a-f]{7,40}", ergebnis.stdout.strip())
