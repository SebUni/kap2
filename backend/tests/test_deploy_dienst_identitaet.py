"""Tests für T-0197: Der Deploy-Schritt `dienst` startet den Dienst ohne Rechteausweitung
per sudo neu und prüft, dass danach wirklich der neue Prozess mit dem neuen Stand antwortet.

Anlass: Das Test-Deployment konnte `fertig` melden, obwohl der ausgerollte Stand gar nicht
lief — der Health-Check fragte nur, ob auf Port 8010 überhaupt etwas antwortet. Lief der alte
Prozess weiter, war die Antwort grün und die Auslieferung eine Lüge (T-0195, Urteil Runde 1,
Punkt b). Zweiter Befund: `sudo` scheitert im Deploy-Lauf grundsätzlich an der Sperre
„no new privileges"; der Neustart läuft deshalb als Benutzer `overlord` über polkit.
"""

from __future__ import annotations

import os
import re
import signal
import subprocess
import time
from pathlib import Path

# Strenge Anker (T-0530): Treffer nur in Befehlszeilen, fehlender Anker macht den Test rot.
from _deploy_anker import SKRIPT, WURZEL, anker_index, ausschnitt, hat_anker, skript_text
UNIT = WURZEL / "deploy" / "kap2-test.service"
MAIN = WURZEL / "backend" / "app" / "main.py"
LIB = WURZEL / "deploy" / "lib-neustart.sh"


def _dienst_block() -> str:
    return ausschnitt('SCHRITT="dienst"', 'SCHRITT="status"')


def _restart_zweig(block: str) -> str:
    """Fehlerzweig von `if ! /bin/systemctl restart kap2-test; then` bis zu seinem `fi`."""
    kopf = "if ! /bin/systemctl restart kap2-test; then"
    anfang = anker_index(block, kopf)
    ende = anker_index(block, "\nfi", anfang)
    return block[anfang:ende]


def test_skript_ist_syntaktisch_fehlerfrei():
    """`bash -n deploy/test-deploy.sh` endet ohne Fehler."""
    subprocess.run(["bash", "-n", str(SKRIPT)], check=True)


def test_dienst_startet_ohne_sudo_neu():
    """(a) Kein sudo: unter „no new privileges" kann es grundsätzlich nicht nach root wechseln."""
    block = _dienst_block()
    # Kommentarzeilen ausnehmen: dort wird der Verzicht auf sudo gerade begründet.
    befehle = "\n".join(z for z in block.splitlines() if not z.lstrip().startswith("#"))
    assert not re.search(r"(^|\s)sudo\s", befehle), befehle
    assert hat_anker(block, "systemctl restart kap2-test")


def test_dienst_prueft_vorbedingung_unit_vorhanden():
    """(b) Fehlt die Unit, gibt es eine verständliche Anweisung statt einer nackten Fehlermeldung."""
    block = _dienst_block()
    assert hat_anker(block, "systemctl list-unit-files kap2-test.service")
    assert hat_anker(block, "/etc/systemd/system/kap2-test.service")


def test_dienst_prueft_polkit_regel_nicht_als_rules_datei_vorab():
    """(b) Die Vorbedingungsprüfung besteht nicht auf `/etc/polkit-1/rules.d/`.

    Der Server fährt polkit 0.105 und kennt keine JavaScript-Regeln; die Berechtigung liegt
    dort als `.pkla`. Eine Prüfung auf `rules.d` würde die heute laufende Auslieferung brechen.
    """
    block = _dienst_block()
    assert "/etc/polkit-1/rules.d/" not in block
    assert hat_anker(block, "/etc/polkit-1/localauthority/50-local.d/50-kap2-test.pkla")


def test_dienst_schritt_wird_nicht_uebersprungen():
    """(c) Scheitert der Neustart mangels Berechtigung, bricht der Lauf ab — kein Überspringen."""
    block = _dienst_block()
    fehlerzweig = _restart_zweig(block)
    # Im Fehlerzweig steht ein `false`, das den ERR-Trap auslöst (Abbruch mit Fehlerstatus).
    assert re.search(r"^\s*false\s*$", fehlerzweig, re.M), fehlerzweig
    assert hat_anker(fehlerzweig, "NICHT uebersprungen")
    # Der nötige Handgriff steht wörtlich im Abbruchtext.
    assert hat_anker(fehlerzweig, "/etc/polkit-1/localauthority/50-local.d/50-kap2-test.pkla")
    assert hat_anker(fehlerzweig, "/etc/systemd/system/kap2-test.service")


def test_dienst_prueft_identitaet_des_neuen_prozesses():
    """(d) MainPID muss sich ändern und ≠ 0 sein, und /api/health den ausgerollten Commit melden."""
    block = _dienst_block()
    assert hat_anker(block, "MainPID")
    assert hat_anker(block, '"$NEU_PID" != "0"')
    assert hat_anker(block, '"$NEU_PID" != "$ALT_PID"')
    assert hat_anker(block, '"$GEMELDET" == "$COMMIT"')


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


def _stub_systemctl(verzeichnis: Path, mainpid: str) -> Path:
    """Legt ein `systemctl` in `verzeichnis` ab, das eine feste MainPID meldet (T-0342).

    Nur `show -p MainPID --value <unit>` wird beantwortet; alles andere endet mit 1. Damit
    läuft der Test ohne Serverrechte, ohne D-Bus und ohne echte Unit.
    """
    stub = verzeichnis / "systemctl"
    stub.write_text(
        "#!/bin/sh\n"
        'if [ "$1" = "show" ]; then printf "%s\\n" ' + f"'{mainpid}'" + "; exit 0; fi\n"
        "exit 1\n",
        encoding="utf-8",
    )
    stub.chmod(0o755)
    return stub


def _funktion_ausfuehren(pfad_vorne: Path) -> subprocess.CompletedProcess:
    """Führt `neustart_ueber_eigenen_prozess kap2-test` wirklich aus, mit Stub-PATH."""
    umgebung = dict(os.environ)
    umgebung["PATH"] = f"{pfad_vorne}:{umgebung.get('PATH', '')}"
    return subprocess.run(
        ["bash", "-c", f'source "{LIB}"; neustart_ueber_eigenen_prozess kap2-test'],
        capture_output=True,
        text=True,
        env=umgebung,
        timeout=30,
    )


def test_eigenprozess_neustart_toetet_den_gemeldeten_prozess(tmp_path):
    """(a) Echter Wegwerfprozess als MainPID: Rückgabewert 0 und der Prozess ist danach beendet."""
    opfer = subprocess.Popen(["sleep", "300"])
    try:
        _stub_systemctl(tmp_path, str(opfer.pid))
        ergebnis = _funktion_ausfuehren(tmp_path)
        assert ergebnis.returncode == 0, ergebnis.stderr + ergebnis.stdout
        assert opfer.wait(timeout=10) != 0
        assert opfer.returncode == -signal.SIGKILL, opfer.returncode
    finally:
        if opfer.poll() is None:  # Sicherheitsnetz, falls die Funktion nichts gesendet hat
            opfer.kill()
            opfer.wait(timeout=10)


def test_eigenprozess_neustart_bricht_ohne_hauptprozess_ab(tmp_path):
    """(b) MainPID=0: Rückgabewert 1, und es wird kein Signal gesendet."""
    unbeteiligt = subprocess.Popen(["sleep", "300"])
    try:
        _stub_systemctl(tmp_path, "0")
        ergebnis = _funktion_ausfuehren(tmp_path)
        assert ergebnis.returncode == 1, ergebnis.stderr + ergebnis.stdout
        # Beweis, dass kein Signal flog: der nebenher laufende Prozess lebt unverändert weiter.
        time.sleep(0.2)
        assert unbeteiligt.poll() is None
    finally:
        unbeteiligt.kill()
        unbeteiligt.wait(timeout=10)


def test_eigenprozess_neustart_bricht_bei_fremder_pid_ab(tmp_path):
    """(c) Gemeldete PID gehört nicht dem laufenden Benutzer (hier: existiert nicht) → 2."""
    tot = subprocess.Popen(["sleep", "300"])
    tot.kill()
    tot.wait(timeout=10)  # abernten, damit die PID wirklich verschwunden ist
    try:
        os.kill(tot.pid, 0)
    except OSError:
        pass
    else:  # PID sofort wiederverwendet — dann trägt der Test nicht, was er tragen soll
        raise AssertionError(f"PID {tot.pid} existiert noch; Test nicht aussagekräftig")
    _stub_systemctl(tmp_path, str(tot.pid))
    ergebnis = _funktion_ausfuehren(tmp_path)
    assert ergebnis.returncode == 2, ergebnis.stderr + ergebnis.stdout


def test_dienst_faellt_auf_eigenen_prozess_zurueck():
    """(T-0342) Der Dienst-Schritt bricht nach abgelehntem `restart` nicht mehr sofort ab."""
    text = skript_text()
    assert hat_anker(text, 'source "$PRODUKT/deploy/lib-neustart.sh"')
    block = _dienst_block()
    zweig = _restart_zweig(block)
    assert hat_anker(zweig, "neustart_ueber_eigenen_prozess kap2-test")
    # Das `false` liegt hinter der Prüfung des Rückgabewerts, nicht davor.
    assert anker_index(zweig, "neustart_ueber_eigenen_prozess kap2-test") < anker_index(
        zweig, "NEUSTART_RC -ne 0"
    )
    assert anker_index(zweig, "NEUSTART_RC -ne 0") < zweig.rindex("false")


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
