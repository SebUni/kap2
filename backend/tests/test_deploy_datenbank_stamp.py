"""Tests für T-0339: Der Deploy-Schritt `datenbank` heilt genau einen Zustand selbst und
scheitert bei allem anderen laut.

Anlass: Das Test-Deployment vom 18.09.2026 ist an `relation "app_settings" already exists`
gescheitert. `app/main.py` legt beim Start alle Tabellen per `create_all` an, setzt dabei aber
nie die Alembic-Versionstabelle. Damit begann jeder folgende Deploy wieder bei der
Basis-Migration und scheiterte erneut — ein Zustand, der sich nicht von selbst löst. Der
frühere Rückfall („Fortsetzung mit create_all-Fallback") hat den Fehler stumm übersprungen.

Geprüft wird das echte Skript: der Block zwischen `SCHRITT="datenbank"` und `SCHRITT="dienst"`
wird aus `deploy/test-deploy.sh` herausgeschnitten und mit einem Stub-`alembic` in einem
temporären `PATH` ausgeführt. Drei Läufe, je gegen die wörtliche Protokollausgabe:

(a) `upgrade` gelingt sofort            → kein `stamp`, Schritt grün
(b) `upgrade` scheitert mit „already exists", `alembic_version` fehlt
                                        → genau ein `stamp head`, danach `upgrade`, Schritt grün
(c) `upgrade` scheitert anders           → kein `stamp`, Schritt rot mit `FEHLGESCHLAGEN`
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
    UPGRADES=$(grep -c '^upgrade' "$STUB_PROTOKOLL")
    case "$STUB_MODUS" in
      gut)
        echo "INFO  [alembic.runtime.migration] Running upgrade  -> 9f1a2b3c4d5e"
        exit 0;;
      doppelt)
        if [[ "$UPGRADES" == "1" ]]; then
          echo 'sqlalchemy.exc.ProgrammingError: (psycopg2.errors.DuplicateTable) relation "app_settings" already exists' >&2
          exit 1
        fi
        echo "INFO  [alembic.runtime.migration] Running upgrade 9f1a2b3c4d5e -> a1b2c3d4e5f6"
        exit 0;;
      *)
        echo 'sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not connect to server: Connection refused' >&2
        exit 1;;
    esac;;
  current)
    # Im heilbaren Fall fehlt die Tabelle alembic_version: leere Ausgabe auf stdout.
    if [[ "$STUB_MODUS" == "doppelt" ]]; then exit 0; fi
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
"""


def _datenbank_block() -> str:
    return ausschnitt('SCHRITT="datenbank"', 'SCHRITT="dienst"')


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

    # Seit T-0425 legt der Schritt sein Alembic-Protokoll mit "mktemp $DEPLOY_TMP/..." an
    # (vorher fest in $DEPLOY_TMP von deploy/test-deploy.sh selbst gesetzt, oberhalb dieses
    # herausgeschnittenen Blocks). Die Werkbank hier schneidet nur den Block aus, nicht die
    # Zeile, die DEPLOY_TMP definiert -- ohne eigenen Wert bricht "set -u" mit "unbound
    # variable" ab, bevor alembic ueberhaupt aufgerufen wird.
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


def test_a_upgrade_gelingt_sofort_kein_stamp(tmp_path):
    """(a) Gelingt `upgrade head` sofort, wird nicht gestempelt und der Schritt ist grün."""
    rc, ausgabe, aufrufe = _lauf(tmp_path, "gut")
    assert rc == 0, ausgabe
    assert aufrufe == ["upgrade head"], aufrufe
    assert "INFO  [alembic.runtime.migration] Running upgrade  -> 9f1a2b3c4d5e" in ausgabe
    assert "stamp" not in ausgabe
    assert "FEHLGESCHLAGEN" not in ausgabe
    assert "== schritt datenbank beendet" in ausgabe


def test_b_doppelanlage_ohne_alembic_stand_wird_gestempelt(tmp_path):
    """(b) „already exists" + fehlende `alembic_version` → genau ein `stamp head`, dann `upgrade`."""
    rc, ausgabe, aufrufe = _lauf(tmp_path, "doppelt")
    assert rc == 0, ausgabe
    # Genau ein Stempel, und zwar zwischen dem gescheiterten und dem wiederholten upgrade.
    assert aufrufe == ["upgrade head", "current", "stamp head", "upgrade head"], aufrufe
    assert aufrufe.count("stamp head") == 1, aufrufe
    assert 'relation "app_settings" already exists' in ausgabe
    assert (
        "Schema vorhanden, aber ohne Alembic-Stand (fruehere create_all-Anlage)"
        " -- stemple einmalig auf head." in ausgabe
    )
    assert "INFO  [alembic.runtime.migration] Running stamp_revision  -> a1b2c3d4e5f6" in ausgabe
    assert (
        "INFO  [alembic.runtime.migration] Running upgrade 9f1a2b3c4d5e -> a1b2c3d4e5f6" in ausgabe
    )
    assert "Datenbank nach dem Stempel regulaer auf head hochgezogen." in ausgabe
    assert "FEHLGESCHLAGEN" not in ausgabe
    assert "== schritt datenbank beendet" in ausgabe


def test_c_anderer_fehler_bricht_fatal_ab(tmp_path):
    """(c) Jeder andere Fehler: kein `stamp`, Rückgabewert ≠ 0, Zeile mit `FEHLGESCHLAGEN`."""
    rc, ausgabe, aufrufe = _lauf(tmp_path, "anders")
    assert rc != 0, ausgabe
    assert aufrufe == ["upgrade head"], aufrufe
    assert "stamp" not in " ".join(aufrufe)
    assert "could not connect to server: Connection refused" in ausgabe
    assert (
        "!! SCHRITT datenbank FEHLGESCHLAGEN (alembic upgrade head), kein heilbarer"
        " Doppelanlage-Fall -- Abbruch ohne create_all-Rueckfall" in ausgabe
    )
    assert "!! Fehler im Schritt datenbank (Rueckgabewert 1)" in ausgabe
    # Kein stilles Weiterlaufen: der Schritt endet nicht regulär.
    assert "== schritt datenbank beendet" not in ausgabe


def test_create_all_rueckfall_ist_entfallen():
    """Der stille Rückfall auf `create_all` steht nicht mehr im Schritt."""
    block = _datenbank_block()
    # Kommentarzeilen ausnehmen: dort wird der Verzicht auf den Rückfall gerade begründet.
    befehle = "\n".join(z for z in block.splitlines() if not z.lstrip().startswith("#"))
    assert "Fortsetzung mit create_all-Fallback" not in befehle
    assert "Tabellen werden beim Start per create_all angelegt" not in befehle
