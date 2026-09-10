"""Test für T-0124: Der ERR-Trap in `deploy/test-deploy.sh` greift auch aus einer
Shell-Funktion heraus (`set -E`), und das Skript ist syntaktisch fehlerfrei.

Anlass: Bei der Abnahme von T-0120 hat der Prüfer festgestellt, dass der ERR-Trap
auch ohne `-e` feuert — auf oberster Ebene. Innerhalb von `status_schreiben` feuert
er ohne `-E` jedoch nicht. Scheitert dort ein Befehl (etwa der `python3`-Aufruf, der
`betrieb/deploy-status.json` erzeugt), blieb der Fehler stumm: kein Status wurde
gepusht, der zuletzt gemeldete Status blieb stehen und wurde weiter als aktuell
gelesen.

Der Test baut aus dem echten Skript eine Werkbank: er übernimmt die `set`-Zeile und
den Block von `speicher_zeile` bis zum `trap` (also auch `aufseher_zeile`,
`status_lokal_schreiben`, `status_veroeffentlichen`, `status_schreiben`,
`fehler_abbruch`, `signal_abbruch`) wörtlich aus
`deploy/test-deploy.sh` und ersetzt nur die Pfade sowie `python3` durch eine
Attrappe, die beim ersten Aufruf scheitert — also genau im Aufruf
`status_schreiben fertig ""`.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

import pytest

SKRIPT = Path(__file__).resolve().parents[2] / "deploy" / "test-deploy.sh"

PYTHON3_ATTRAPPE = """#!/usr/bin/env bash
# Scheitert beim ersten Aufruf (status_schreiben fertig), danach echtes python3.
Z="$ZAEHLER"
C=$(cat "$Z" 2>/dev/null || echo 0)
echo $((C+1)) > "$Z"
if [ "$C" = "0" ]; then
  echo "python3: simulierter Absturz im Schritt status" >&2
  exit 1
fi
exec /usr/bin/python3 "$@"
"""


def _set_zeile() -> str:
    for zeile in SKRIPT.read_text(encoding="utf-8").splitlines():
        if re.match(r"^set\s+-", zeile):
            return zeile
    raise AssertionError("keine set-Zeile in deploy/test-deploy.sh gefunden")


def _funktionsblock() -> str:
    text = SKRIPT.read_text(encoding="utf-8")
    # Anker ist die *erste* Funktion des Blocks, nicht status_schreiben: seit T-0132 ist
    # status_schreiben in status_lokal_schreiben (JSON + lokal festschreiben) und
    # status_veroeffentlichen (Push-Schleife) aufgeteilt, und fehler_abbruch ruft
    # zusaetzlich aufseher_zeile. Wird weiter unten ausgeschnitten, fehlen diese Helfer
    # in der Werkbank und der Lauf endet in "command not found" statt im Fehlerstatus.
    anfang = text.index("speicher_zeile() {")
    ende = text.index("trap fehler_abbruch ERR") + len("trap fehler_abbruch ERR")
    return text[anfang:ende]


def _werkbank(tmp_path: Path, set_zeile: str) -> tuple[Path, dict[str, str]]:
    """Legt Firmen-Repo, Gegenstelle, python3-Attrappe und Lauf-Skript an."""
    firma = tmp_path / "firma"
    (firma / "betrieb").mkdir(parents=True)
    remote = tmp_path / "remote.git"
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()

    umgebung = dict(os.environ)
    umgebung.update(
        {
            "PATH": f"{bin_dir}:{umgebung['PATH']}",
            "ZAEHLER": str(tmp_path / "zaehler"),
            "GIT_AUTHOR_NAME": "Test",
            "GIT_AUTHOR_EMAIL": "test@example.invalid",
            "GIT_COMMITTER_NAME": "Test",
            "GIT_COMMITTER_EMAIL": "test@example.invalid",
        }
    )

    def git(*args: str, cwd: Path) -> None:
        subprocess.run(
            ["git", *args], cwd=cwd, env=umgebung, check=True, capture_output=True
        )

    subprocess.run(
        ["git", "init", "-q", "--bare", str(remote)],
        env=umgebung,
        check=True,
        capture_output=True,
    )
    git("init", "-q", "-b", "main", ".", cwd=firma)
    (firma / "betrieb" / "deploy-status.json").write_text(
        json.dumps({"status": "fertig", "commit": "4fa6eeb8"}) + "\n", encoding="utf-8"
    )
    git("add", "-A", cwd=firma)
    git("commit", "-qm", "Ausgangsstand", cwd=firma)
    git("remote", "add", "origin", str(remote), cwd=firma)
    git("push", "-q", "origin", "main:main", cwd=firma)

    attrappe = bin_dir / "python3"
    attrappe.write_text(PYTHON3_ATTRAPPE, encoding="utf-8")
    attrappe.chmod(0o755)

    protokoll = tmp_path / "deploy.log"
    protokoll.write_text(
        "2026-09-08T11:59:12Z npm run build: FATAL ERROR heap out of memory\n",
        encoding="utf-8",
    )

    lauf = tmp_path / "lauf.sh"
    lauf.write_text(
        "\n".join(
            [
                set_zeile,
                f'FIRMA="{firma}"',
                f'PROTOKOLL="{protokoll}"',
                'COMMIT="4fa6eeb8"',
                'SCHRITT="status"',
                'KAP2_TEST_URL="http://kap2-test.example"',
                _funktionsblock(),
                'status_schreiben fertig ""',
                'echo "== fertig: $KAP2_TEST_URL ($COMMIT)"',
                "",
            ]
        ),
        encoding="utf-8",
    )
    return lauf, umgebung


def _gemeldeter_status(tmp_path: Path, umgebung: dict[str, str]) -> str:
    ergebnis = subprocess.run(
        ["git", "-C", str(tmp_path / "firma"), "show", "origin/main:betrieb/deploy-status.json"],
        env=umgebung,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(ergebnis.stdout)["status"]


def _lauf(tmp_path: Path, set_zeile: str) -> tuple[subprocess.CompletedProcess, str]:
    lauf, umgebung = _werkbank(tmp_path, set_zeile)
    ergebnis = subprocess.run(
        ["bash", str(lauf)], env=umgebung, capture_output=True, text=True
    )
    subprocess.run(
        ["git", "-C", str(tmp_path / "firma"), "fetch", "-q", "origin"],
        env=umgebung,
        check=True,
        capture_output=True,
    )
    return ergebnis, _gemeldeter_status(tmp_path, umgebung)


def test_set_zeile_traegt_grosses_e():
    """Die Fehlerbehandlung muss -E, -e, -u und pipefail setzen."""
    zeile = _set_zeile()
    optionen = zeile.split()[1]
    assert optionen.startswith("-")
    for buchstabe in ("E", "e", "u"):
        assert buchstabe in optionen, f"{buchstabe} fehlt in: {zeile}"
    assert "pipefail" in zeile, zeile


def test_bash_n_laeuft_ohne_ausgabe_durch():
    """`bash -n deploy/test-deploy.sh` — Rueckgabewert 0, keine Ausgabe."""
    ergebnis = subprocess.run(
        ["bash", "-n", str(SKRIPT)], capture_output=True, text=True
    )
    assert ergebnis.returncode == 0
    assert ergebnis.stdout == ""
    assert ergebnis.stderr == ""


@pytest.mark.skipif(not Path("/usr/bin/python3").exists(), reason="kein /usr/bin/python3")
def test_fehler_in_status_schreiben_wird_gemeldet(tmp_path):
    """Ist-Stand: scheitert ein Befehl in status_schreiben, greift der Trap."""
    ergebnis, status = _lauf(tmp_path, _set_zeile())
    assert ergebnis.returncode != 0, ergebnis.stdout
    assert "!! Fehler im Schritt status" in ergebnis.stdout
    assert "== fertig" not in ergebnis.stdout
    assert status == "fehler"


@pytest.mark.skipif(not Path("/usr/bin/python3").exists(), reason="kein /usr/bin/python3")
def test_gegenprobe_ohne_grosses_e_meldet_falsches_gruen(tmp_path):
    """Gegenprobe Stand T-0120 (`set -euo pipefail`): der Trap greift nicht,
    es wird kein Fehlerstatus gemeldet — der alte Status bleibt stehen."""
    ergebnis, status = _lauf(tmp_path, "set -euo pipefail")
    assert "!! Fehler im Schritt status" not in ergebnis.stdout
    assert status != "fehler"
