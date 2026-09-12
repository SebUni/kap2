"""Tests für T-0197: Der Deploy-Schritt `dienst` startet den Dienst ohne Rechteausweitung
per sudo neu und prüft, dass danach wirklich der neue Prozess mit dem neuen Stand antwortet.

Anlass: Das Test-Deployment konnte `fertig` melden, obwohl der ausgerollte Stand gar nicht
lief — der Health-Check fragte nur, ob auf Port 8010 überhaupt etwas antwortet. Lief der alte
Prozess weiter, war die Antwort grün und die Auslieferung eine Lüge (T-0195, Urteil Runde 1,
Punkt b). Zweiter Befund: `sudo` scheitert im Deploy-Lauf grundsätzlich an der Sperre
„no new privileges"; der Neustart läuft deshalb als Benutzer `overlord` über polkit.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

WURZEL = Path(__file__).resolve().parents[2]
SKRIPT = WURZEL / "deploy" / "test-deploy.sh"
UNIT = WURZEL / "deploy" / "kap2-test.service"
MAIN = WURZEL / "backend" / "app" / "main.py"


def _dienst_block() -> str:
    text = SKRIPT.read_text(encoding="utf-8")
    anfang = text.index('SCHRITT="dienst"')
    ende = text.index('SCHRITT="status"')
    return text[anfang:ende]


def test_skript_ist_syntaktisch_fehlerfrei():
    """`bash -n deploy/test-deploy.sh` endet ohne Fehler."""
    subprocess.run(["bash", "-n", str(SKRIPT)], check=True)


def test_dienst_startet_ohne_sudo_neu():
    """(a) Kein sudo: unter „no new privileges" kann es grundsätzlich nicht nach root wechseln."""
    block = _dienst_block()
    # Kommentarzeilen ausnehmen: dort wird der Verzicht auf sudo gerade begründet.
    befehle = "\n".join(z for z in block.splitlines() if not z.lstrip().startswith("#"))
    assert not re.search(r"(^|\s)sudo\s", befehle), befehle
    assert "systemctl restart kap2-test" in block


def test_dienst_prueft_vorbedingung_unit_vorhanden():
    """(b) Fehlt die Unit, gibt es eine verständliche Anweisung statt einer nackten Fehlermeldung."""
    block = _dienst_block()
    assert "systemctl list-unit-files kap2-test.service" in block
    assert "/etc/systemd/system/kap2-test.service" in block


def test_dienst_prueft_polkit_regel_nicht_als_rules_datei_vorab():
    """(b) Die Vorbedingungsprüfung besteht nicht auf `/etc/polkit-1/rules.d/`.

    Der Server fährt polkit 0.105 und kennt keine JavaScript-Regeln; die Berechtigung liegt
    dort als `.pkla`. Eine Prüfung auf `rules.d` würde die heute laufende Auslieferung brechen.
    """
    block = _dienst_block()
    assert "/etc/polkit-1/rules.d/" not in block
    assert "/etc/polkit-1/localauthority/50-local.d/50-kap2-test.pkla" in block


def test_dienst_schritt_wird_nicht_uebersprungen():
    """(c) Scheitert der Neustart mangels Berechtigung, bricht der Lauf ab — kein Überspringen."""
    block = _dienst_block()
    assert "if ! /bin/systemctl restart kap2-test; then" in block
    fehlerzweig = block[block.index("if ! /bin/systemctl restart kap2-test; then"):]
    fehlerzweig = fehlerzweig.split("\nfi", 1)[0]
    # Im Fehlerzweig steht ein `false`, das den ERR-Trap auslöst (Abbruch mit Fehlerstatus).
    assert re.search(r"^\s*false\s*$", fehlerzweig, re.M), fehlerzweig
    assert "NICHT uebersprungen" in fehlerzweig
    # Der nötige Handgriff steht wörtlich im Abbruchtext.
    assert "/etc/polkit-1/localauthority/50-local.d/50-kap2-test.pkla" in fehlerzweig
    assert "/etc/systemd/system/kap2-test.service" in fehlerzweig


def test_dienst_prueft_identitaet_des_neuen_prozesses():
    """(d) MainPID muss sich ändern und ≠ 0 sein, und /api/health den ausgerollten Commit melden."""
    block = _dienst_block()
    assert "MainPID" in block
    assert '"$NEU_PID" != "0"' in block
    assert '"$NEU_PID" != "$ALT_PID"' in block
    assert '"$GEMELDET" == "$COMMIT"' in block


def test_unit_laeuft_nicht_als_root():
    """(e) Sicherheitsregression ausschließen: User=/Group= müssen gesetzt sein."""
    text = UNIT.read_text(encoding="utf-8")
    assert "\nUser=overlord\n" in text
    assert "\nGroup=overlord\n" in text


def test_health_meldet_commit_und_startzeit():
    """(f) /api/health liefert die Kennung des antwortenden Prozesses — additiv zu `status`."""
    text = MAIN.read_text(encoding="utf-8")
    gesundheit = text[text.index('@app.get("/api/health")'):]
    assert '"status": "ok"' in gesundheit
    assert '"commit": COMMIT' in gesundheit
    assert '"gestartet": PROZESS_START' in gesundheit
    assert 'os.environ.get("KAP2_DEPLOY_COMMIT")' in text


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
