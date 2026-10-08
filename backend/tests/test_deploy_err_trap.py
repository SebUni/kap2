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
import shlex
import subprocess
from pathlib import Path

import pytest

# Strenge Anker (T-0530): Treffer nur in Befehlszeilen, fehlender Anker macht den Test rot.
from _deploy_anker import SKRIPT, anker_index, skript_text

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
    text = skript_text()
    # Anker ist die *erste* Funktion des Blocks, nicht status_schreiben: seit T-0132 ist
    # status_schreiben in status_lokal_schreiben (JSON + lokal festschreiben) und
    # status_veroeffentlichen (Push-Schleife) aufgeteilt, und fehler_abbruch ruft
    # zusaetzlich aufseher_zeile. Wird weiter unten ausgeschnitten, fehlen diese Helfer
    # in der Werkbank und der Lauf endet in "command not found" statt im Fehlerstatus.
    anfang = anker_index(text, "speicher_zeile() {")
    # Ab T-0442 nennt schon ein Kommentar vor dem Funktionsblock (Begruendung der
    # Aufraeumlogik zu DEPLOY_TMP) die Zeichenkette "trap fehler_abbruch ERR" beilaeufig --
    # text.index() faende dort die erste, viel zu fruehe Stelle und ende laege vor anfang
    # (leerer Ausschnitt). Deshalb ab anfang weitersuchen, nicht vom Dateianfang. Seit T-0530
    # zaehlen Kommentarzeilen bei der Suche ohnehin nicht mit (anker_index).
    ende = anker_index(text, "trap fehler_abbruch ERR", anfang) + len("trap fehler_abbruch ERR")
    return text[anfang:ende]


def _werkbank(
    tmp_path: Path,
    set_zeile: str,
    datenbank: tuple[str, str] | None = None,
    beispiel: dict | str | None = None,
) -> tuple[Path, dict[str, str]]:
    """Legt Firmen-Repo, Gegenstelle, python3-Attrappe und Lauf-Skript an.

    Seit T-1832 liest `status_lokal_schreiben` auch DATENBANK_VORHER, DATENBANK_NACHHER und die
    Datei in BEISPIEL_JSON. `datenbank` und `beispiel` setzen sie wie die Schritte `datenbank` und
    `beispielkommune` des echten Skripts; ohne beide Angaben bleiben die drei Variablen ungesetzt
    (Abbruch vor diesen Schritten, unter `set -u`)."""
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

    schritt_variablen: list[str] = []
    if datenbank is not None:
        schritt_variablen.append(f"DATENBANK_VORHER={shlex.quote(datenbank[0])}")
        schritt_variablen.append(f"DATENBANK_NACHHER={shlex.quote(datenbank[1])}")
    if beispiel is not None:
        beispiel_datei = tmp_path / "beispielkommune.json"
        roh = beispiel if isinstance(beispiel, str) else json.dumps(beispiel, ensure_ascii=False)
        beispiel_datei.write_text(roh + "\n" if roh else "", encoding="utf-8")
        schritt_variablen.append(f"BEISPIEL_JSON={shlex.quote(str(beispiel_datei))}")

    lauf = tmp_path / "lauf.sh"
    lauf.write_text(
        "\n".join(
            [
                set_zeile,
                *schritt_variablen,
                f'FIRMA="{firma}"',
                f'PROTOKOLL="{protokoll}"',
                'COMMIT="4fa6eeb8"',
                'SCHRITT="status"',
                'KAP2_TEST_URL="http://kap2-test.example"',
                # Seit T-0169 liest status_lokal_schreiben PASSWORT_QUELLE; die Zuweisung steht
                # im echten Skript oberhalb des uebernommenen Funktionsblocks. Ohne sie bricht
                # die Werkbank unter "set -u" mit "unbound variable" ab, bevor der ERR-Trap
                # ueberhaupt zum Zug kommt -- gepruefte Wirkung waere dann eine andere.
                'PASSWORT_QUELLE="/etc/overlord/kap2-test.env"',
                _funktionsblock(),
                'status_schreiben fertig ""',
                'echo "== fertig: $KAP2_TEST_URL ($COMMIT)"',
                "",
            ]
        ),
        encoding="utf-8",
    )
    return lauf, umgebung


def _gemeldete_datei(tmp_path: Path, umgebung: dict[str, str]) -> tuple[dict, str]:
    """Gepushte `betrieb/deploy-status.json` als Objekt und als Rohtext."""
    ergebnis = subprocess.run(
        ["git", "-C", str(tmp_path / "firma"), "show", "origin/main:betrieb/deploy-status.json"],
        env=umgebung,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(ergebnis.stdout), ergebnis.stdout


def _gemeldeter_status(tmp_path: Path, umgebung: dict[str, str]) -> str:
    return _gemeldete_datei(tmp_path, umgebung)[0]["status"]


def _lauf_datei(
    tmp_path: Path, set_zeile: str, **werkbank: object
) -> tuple[subprocess.CompletedProcess, dict, str]:
    lauf, umgebung = _werkbank(tmp_path, set_zeile, **werkbank)
    ergebnis = subprocess.run(
        ["bash", str(lauf)], env=umgebung, capture_output=True, text=True
    )
    subprocess.run(
        ["git", "-C", str(tmp_path / "firma"), "fetch", "-q", "origin"],
        env=umgebung,
        check=True,
        capture_output=True,
    )
    datei, roh = _gemeldete_datei(tmp_path, umgebung)
    return ergebnis, datei, roh


def _lauf(tmp_path: Path, set_zeile: str) -> tuple[subprocess.CompletedProcess, str]:
    ergebnis, datei, _ = _lauf_datei(tmp_path, set_zeile)
    return ergebnis, datei["status"]


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


BEISPIEL_DATEI = {
    "kommune": "Warmsen",
    "gemeindeschluessel": "03256033",
    "status": "done",
    "commit": "4fa6eeb8",
    "zeit_rechnung": "2026-10-08T10:45:59+00:00",
    "klimawirkungen": [
        {"bezeichnung": "Hitzebelastung (#95)", "betrag_eur_jahr": 179020.81, "intern": "nicht uebernehmen"},
        {"bezeichnung": "Allergische Reaktionen durch Aeroallergene (#96)", "betrag_eur_jahr": 2280.6},
        {"bezeichnung": "UV-bedingte Gesundheitsschaedigungen (#98)", "betrag_eur_jahr": None},
    ],
    # Felder ausserhalb der festen Liste: duerfen nie in die Statusdatei.
    "sitzung": "GEHEIMER-SITZUNGSWERT",
    "zugang": {"passwort": "GEHEIMES-PASSWORT"},
}


@pytest.mark.skipif(not Path("/usr/bin/python3").exists(), reason="kein /usr/bin/python3")
def test_abbruch_schreibt_datenbank_und_beispielkommune_in_den_gepushten_status(tmp_path):
    """T-1832, Fall 1: Mit Beispieldatei in BEISPIEL_JSON enthält der gepushte Status beide Felder
    mit genau diesen Werten — und nur die Felder der festen Liste."""
    ergebnis, datei, roh = _lauf_datei(
        tmp_path,
        _set_zeile(),
        datenbank=("0042_abc (head)", "0043_def (head)"),
        beispiel=BEISPIEL_DATEI,
    )
    assert ergebnis.returncode != 0, ergebnis.stdout
    assert datei["status"] == "fehler"
    assert "Schritt status fehlgeschlagen" in datei["fehler"]
    assert datei["datenbank"] == {"vorher": "0042_abc (head)", "nachher": "0043_def (head)"}
    assert datei["beispielkommune"] == {
        "kommune": "Warmsen",
        "gemeindeschluessel": "03256033",
        "commit": "4fa6eeb8",
        "zeit_rechnung": "2026-10-08T10:45:59+00:00",
        "klimawirkungen": [
            {"bezeichnung": "Hitzebelastung (#95)", "betrag_eur_jahr": 179020.81},
            {"bezeichnung": "Allergische Reaktionen durch Aeroallergene (#96)", "betrag_eur_jahr": 2280.6},
            {"bezeichnung": "UV-bedingte Gesundheitsschaedigungen (#98)", "betrag_eur_jahr": None},
        ],
    }
    for fremd in ("GEHEIMER-SITZUNGSWERT", "GEHEIMES-PASSWORT", "nicht uebernehmen", '"sitzung"'):
        assert fremd not in roh, fremd


@pytest.mark.skipif(not Path("/usr/bin/python3").exists(), reason="kein /usr/bin/python3")
def test_abbruch_ohne_datei_und_variablen_schreibt_status_fehler_und_null(tmp_path):
    """T-1832, Fall 2: Ohne Beispieldatei und ohne DATENBANK_VORHER/-NACHHER/BEISPIEL_JSON (Abbruch
    vor diesen Schritten, `set -u` aktiv) wird der Fehlerstatus trotzdem geschrieben."""
    assert "u" in _set_zeile().split()[1]
    ergebnis, datei, _ = _lauf_datei(tmp_path, _set_zeile())
    assert "unbound variable" not in ergebnis.stderr, ergebnis.stderr
    assert ergebnis.returncode != 0
    assert datei["status"] == "fehler"
    assert "Schritt status fehlgeschlagen" in datei["fehler"]
    assert "npm run build: FATAL ERROR" in datei["fehler"]  # Protokollzeilen stehen weiter drin
    assert datei["beispielkommune"] is None
    assert datei["datenbank"] == {"vorher": None, "nachher": None}


@pytest.mark.skipif(not Path("/usr/bin/python3").exists(), reason="kein /usr/bin/python3")
def test_leere_oder_unlesbare_beispieldatei_ergibt_null(tmp_path):
    """BEISPIEL_JSON zeigt auf eine leere Datei (Skript vor der Schlusszeile abgebrochen) oder auf
    eine Datei ohne JSON: `beispielkommune` ist null, der Status wird geschrieben."""
    for name, inhalt in (("leer", ""), ("kein_json", "Dauer dieses Aufrufs: 12 s")):
        unter = tmp_path / name
        unter.mkdir()
        _, datei, _ = _lauf_datei(unter, _set_zeile(), datenbank=("", ""), beispiel=inhalt)
        assert datei["status"] == "fehler", name
        assert datei["beispielkommune"] is None, name
        assert datei["datenbank"] == {"vorher": None, "nachher": None}, name
    # Ein JSON-Objekt ohne die Felder der festen Liste: jedes Feld null, nichts erfunden.
    ohne = tmp_path / "ohne_felder"
    ohne.mkdir()
    _, datei, _ = _lauf_datei(ohne, _set_zeile(), beispiel={"anderes": 1})
    assert datei["beispielkommune"] == {
        "kommune": None, "gemeindeschluessel": None, "commit": None, "zeit_rechnung": None,
        "klimawirkungen": None,
    }


@pytest.mark.skipif(not Path("/usr/bin/python3").exists(), reason="kein /usr/bin/python3")
def test_gegenprobe_ohne_grosses_e_meldet_falsches_gruen(tmp_path):
    """Gegenprobe Stand T-0120 (`set -euo pipefail`): der Trap greift nicht,
    es wird kein Fehlerstatus gemeldet — der alte Status bleibt stehen."""
    ergebnis, status = _lauf(tmp_path, "set -euo pipefail")
    assert "!! Fehler im Schritt status" not in ergebnis.stdout
    assert status != "fehler"
