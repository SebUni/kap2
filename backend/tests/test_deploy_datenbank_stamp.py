"""Tests für T-1829 (zuvor T-0339): Der Deploy-Schritt `datenbank` führt genau `alembic upgrade
head` aus, macht den Stand davor und danach sichtbar und scheitert bei jedem Fehler laut.

Anlass: Beim Deploy vom 06.10.2026 (Commit `ce951ead`) scheiterte `alembic upgrade head` an
`relation "app_settings" already exists`, weil das Schema beim Dienststart per `create_all`
entstanden war (`app/main.py`, `_ensure_tables`). Das Skript stempelte die Datenbank daraufhin
auf `head` und meldete `fertig` — ohne die Prüfung, die das Runbook (`docs/BETRIEB.md`, Fall B)
vor einem Stempel verlangt (leere Ausgabe von `alembic check`). Seit T-1829 gibt es im Deploy
weder den Stempel noch den Rückfall auf `create_all`; eine Bestandsdatenbank hebt ein Mensch nach
dem Runbook auf die Migrationskette.

Geprüft wird das echte Skript: der Block zwischen `SCHRITT="datenbank"` und `SCHRITT="dienst"`
wird aus `deploy/test-deploy.sh` herausgeschnitten und mit einem Stub-`alembic` in einem
temporären `PATH` ausgeführt. Drei Fälle, je gegen die wörtliche Protokollausgabe:

(a) `upgrade head` gelingt   → Aufrufe `current`, `upgrade head`, `current`; Schritt grün
(b) Doppelanlage („already exists")
                             → kein `stamp`, Rückgabewert ≠ 0, Verweis auf den Runbook-Abschnitt
(c) anderer Fehler           → kein `stamp`, Rückgabewert ≠ 0, Schritt rot
"""

from __future__ import annotations

import subprocess
from pathlib import Path

# Strenge Anker (T-0530): Treffer nur in Befehlszeilen, fehlender Anker macht den Test rot.
from _deploy_anker import SKRIPT, ausschnitt

# Stub-alembic: verhält sich je nach STUB_MODUS wie ein echter Aufruf und schreibt jeden
# Aufruf mit seinen Argumenten in STUB_PROTOKOLL, damit der Test zählen kann, was passiert ist.
STUB = r"""#!/usr/bin/env bash
echo "$*" >> "$STUB_PROTOKOLL"
case "${1:-}" in
  upgrade)
    case "$STUB_MODUS" in
      gut|gut_leer)
        echo "INFO  [alembic.runtime.migration] Running upgrade  -> a1b2c3d4e5f6"
        exit 0;;
      doppelt)
        echo 'sqlalchemy.exc.ProgrammingError: (psycopg2.errors.DuplicateTable) relation "app_settings" already exists' >&2
        exit 1;;
      *)
        echo 'sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not connect to server: Connection refused' >&2
        exit 1;;
    esac;;
  current)
    AUFRUFE=$(grep -c '^current' "$STUB_PROTOKOLL")
    # Erster Aufruf = Stand vor dem Upgrade. Bei fehlender Tabelle alembic_version
    # (Modus gut_leer, doppelt) ist die Ausgabe leer.
    if [[ "$AUFRUFE" == "1" ]]; then
      if [[ "$STUB_MODUS" == "gut" ]]; then echo "9f1a2b3c4d5e"; fi
      exit 0
    fi
    echo "a1b2c3d4e5f6 (head)"
    exit 0;;
  stamp)
    echo "INFO  [alembic.runtime.migration] Running stamp_revision  -> a1b2c3d4e5f6"
    exit 0;;
esac
exit 0
"""

# Aufrufumgebung des Schritts: dieselben Schalter und dieselbe ERR-Falle wie im echten Skript,
# damit `false` im Block genauso fatal wirkt wie dort (set -Eeuo pipefail, trap fehler_abbruch).
RAHMEN = """set -Eeuo pipefail
PRODUKT="$1"
VENV="$2"
SCHRITT="start"
fehler_abbruch() {{
  local rc=$?
  echo "!! Fehler im Schritt $SCHRITT (Rueckgabewert $rc)"
  exit 1
}}
trap fehler_abbruch ERR

{block}
echo "== schritt datenbank beendet"
echo "== VORHER=[$DATENBANK_VORHER] NACHHER=[$DATENBANK_NACHHER]"
"""

ABSCHNITT = "Bestandsdatenbank auf die Migrationskette heben"


def _datenbank_block() -> str:
    return ausschnitt('SCHRITT="datenbank"', 'SCHRITT="dienst"')


def _befehlszeilen(block: str) -> str:
    """Block ohne Kommentarzeilen (dort wird der Verzicht auf Stempel und Rückfall begründet)."""
    return "\n".join(z for z in block.splitlines() if not z.lstrip().startswith("#"))


def _lauf(tmp_path: Path, modus: str) -> tuple[int, str, list[str]]:
    """Führt den echten `datenbank`-Block mit Stub-alembic aus.

    Gibt Rückgabewert, vollständige Protokollausgabe (stdout+stderr) und die Liste der
    Stub-Aufrufe zurück.
    """
    venv_bin = tmp_path / "venv" / "bin"
    venv_bin.mkdir(parents=True)
    stub = venv_bin / "alembic"
    stub.write_text(STUB, encoding="utf-8")
    stub.chmod(0o755)

    produkt = tmp_path / "produkt"
    (produkt / "backend").mkdir(parents=True)

    # Der Schritt legt sein Alembic-Protokoll mit "mktemp $DEPLOY_TMP/..." an; DEPLOY_TMP wird
    # oberhalb des herausgeschnittenen Blocks gesetzt. Ohne eigenen Wert bricht "set -u" ab.
    deploy_tmp = tmp_path / "deploy-tmp"
    deploy_tmp.mkdir()

    skript = tmp_path / "datenbank-schritt.sh"
    skript.write_text(RAHMEN.format(block=_datenbank_block()), encoding="utf-8")

    protokoll = tmp_path / "stub-aufrufe.txt"
    protokoll.write_text("", encoding="utf-8")

    ergebnis = subprocess.run(
        ["bash", str(skript), str(produkt), str(venv_bin.parent)],
        capture_output=True,
        text=True,
        env={
            "PATH": f"{venv_bin}:/usr/bin:/bin",
            "STUB_MODUS": modus,
            "STUB_PROTOKOLL": str(protokoll),
            "HOME": str(tmp_path),
            "DEPLOY_TMP": str(deploy_tmp),
        },
    )
    aufrufe = [z for z in protokoll.read_text(encoding="utf-8").splitlines() if z.strip()]
    return ergebnis.returncode, ergebnis.stdout + ergebnis.stderr, aufrufe


def test_skript_ist_syntaktisch_fehlerfrei():
    """`bash -n deploy/test-deploy.sh` endet ohne Fehler und ohne Ausgabe."""
    ergebnis = subprocess.run(
        ["bash", "-n", str(SKRIPT)], capture_output=True, text=True, check=True
    )
    assert ergebnis.stdout == ""
    assert ergebnis.stderr == ""


def test_a_upgrade_gelingt_current_upgrade_current(tmp_path):
    """(a) Gelingt der Lauf: `current`, `upgrade head`, `current`; Stand vorher und nachher sichtbar."""
    rc, ausgabe, aufrufe = _lauf(tmp_path, "gut")
    assert rc == 0, ausgabe
    assert aufrufe == ["current", "upgrade head", "current"], aufrufe
    assert "Datenbank vorher: 9f1a2b3c4d5e\n" in ausgabe
    assert "Datenbank nachher: a1b2c3d4e5f6 (head)\n" in ausgabe
    # vorher vor nachher, und das Upgrade dazwischen
    assert (
        ausgabe.index("Datenbank vorher:")
        < ausgabe.index("Running upgrade  -> a1b2c3d4e5f6")
        < ausgabe.index("Datenbank nachher:")
    )
    assert "== VORHER=[9f1a2b3c4d5e] NACHHER=[a1b2c3d4e5f6 (head)]" in ausgabe
    assert "stamp" not in ausgabe
    assert "FEHLGESCHLAGEN" not in ausgabe
    assert "== schritt datenbank beendet" in ausgabe


def test_a_leerer_stand_vorher_ist_eine_leere_angabe(tmp_path):
    """Ohne Tabelle `alembic_version` ist der Stand vorher leer; der Schritt ist trotzdem grün."""
    rc, ausgabe, aufrufe = _lauf(tmp_path, "gut_leer")
    assert rc == 0, ausgabe
    assert aufrufe == ["current", "upgrade head", "current"], aufrufe
    assert "Datenbank vorher: \n" in ausgabe
    assert "Datenbank nachher: a1b2c3d4e5f6 (head)\n" in ausgabe
    assert "== VORHER=[] NACHHER=[a1b2c3d4e5f6 (head)]" in ausgabe


def test_b_doppelanlage_bricht_ab_ohne_stamp_mit_verweis(tmp_path):
    """(b) „already exists": kein `stamp`, Rückgabewert ≠ 0, Verweis auf den Runbook-Abschnitt."""
    rc, ausgabe, aufrufe = _lauf(tmp_path, "doppelt")
    assert rc != 0, ausgabe
    assert aufrufe == ["current", "upgrade head"], aufrufe
    assert "stamp" not in " ".join(aufrufe)
    assert 'relation "app_settings" already exists' in ausgabe
    assert "!! SCHRITT datenbank FEHLGESCHLAGEN (alembic upgrade head)" in ausgabe
    assert f'docs/BETRIEB.md, Abschnitt "{ABSCHNITT}"' in ausgabe
    # Der Abbruch läuft über die ERR-Falle, nicht über ein stilles Weiterlaufen.
    assert "!! Fehler im Schritt datenbank (Rueckgabewert 1)" in ausgabe
    assert "Datenbank nachher:" not in ausgabe
    assert "== schritt datenbank beendet" not in ausgabe


def test_c_anderer_fehler_ist_rot(tmp_path):
    """(c) Jeder andere Fehler: kein `stamp`, Rückgabewert ≠ 0, Zeile mit `FEHLGESCHLAGEN`."""
    rc, ausgabe, aufrufe = _lauf(tmp_path, "anders")
    assert rc != 0, ausgabe
    assert aufrufe == ["current", "upgrade head"], aufrufe
    assert "stamp" not in " ".join(aufrufe)
    assert "could not connect to server: Connection refused" in ausgabe
    assert "!! SCHRITT datenbank FEHLGESCHLAGEN (alembic upgrade head)" in ausgabe
    assert "!! Fehler im Schritt datenbank (Rueckgabewert 1)" in ausgabe
    assert "Datenbank nachher:" not in ausgabe
    assert "== schritt datenbank beendet" not in ausgabe


def test_kein_stempel_und_kein_create_all_in_befehlszeilen():
    """Zwischen den Schrittmarken steht in keiner Befehlszeile `stamp` oder `create_all`."""
    befehle = _befehlszeilen(_datenbank_block())
    assert "stamp" not in befehle
    assert "create_all" not in befehle


def test_vorher_und_nachher_stehen_in_variablen_und_meldung_nennt_abschnitt():
    """Beide Stände liegen in Shell-Variablen (Paket 4); die Fehlermeldungen nennen den Abschnitt."""
    befehle = _befehlszeilen(_datenbank_block())
    assert 'DATENBANK_VORHER=$("$VENV/bin/alembic" current' in befehle
    assert 'DATENBANK_NACHHER=$("$VENV/bin/alembic" current' in befehle
    assert 'echo "Datenbank vorher: $DATENBANK_VORHER"' in befehle
    assert 'echo "Datenbank nachher: $DATENBANK_NACHHER"' in befehle
    assert befehle.index("DATENBANK_VORHER=") < befehle.index("alembic\" upgrade head")
    assert befehle.index("alembic\" upgrade head") < befehle.index("DATENBANK_NACHHER=")
    assert befehle.count(ABSCHNITT) == 2
