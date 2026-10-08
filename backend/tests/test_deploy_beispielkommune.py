"""Tests für T-1831: Der Deploy-Schritt `beispielkommune` rechnet Warmsen nach dem Neustart mit dem
ausgelieferten Stand und endet bei jeder Abweichung rot (ERR-Falle), nie mit `fertig`.

Anlass: A-0066 verlangt, dass in der Testumgebung jederzeit eine vollständig gerechnete
Beispielkommune liegt. Der Schritt steht nach dem Health-Check des Schritts `dienst` und vor
`status`; das Skript `scripts/sicht_beispielkommune.py` (T-1830) rechnet gegen den Dienst auf
127.0.0.1:8010.

Der Deploy führt diese Datei vor der Installation der Abhängigkeiten aus: nur Standardbibliothek
und pytest. Geprüft wird das echte Skript: der Block zwischen `SCHRITT="beispielkommune"` und
`SCHRITT="status"` wird aus `deploy/test-deploy.sh` herausgeschnitten und mit einem Ersatzskript
unter `$PRODUKT/scripts/` ausgeführt. Je Fall gegen die wörtliche Protokollausgabe:

(a) gültige Schlusszeile mit #95, #96, #98 und passendem Commit → Schritt grün, Datei in BEISPIEL_JSON
(b) das Skript endet mit Exit 1                                  → rot, "!! Fehler im Schritt beispielkommune"
(c) #98 fehlt in `klimawirkungen`                               → rot
(d) Schlusszeile ist kein JSON                                   → rot
(e) gemeldeter Commit ist nicht der ausgelieferte                → rot
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

# Strenge Anker (T-0530): Treffer nur in Befehlszeilen, fehlender Anker macht den Test rot.
from _deploy_anker import SKRIPT, anker_index, ausschnitt, hat_anker, skript_text

COMMIT = "abc1234"

# Ersatz für scripts/sicht_beispielkommune.py: schreibt Argumente und KAP2_VENV in eine Datei und
# verhält sich je nach ERSATZ_MODUS. Die Schlusszeile ist die letzte Zeile der Standardausgabe.
ERSATZ = r'''#!/usr/bin/env python3
import json, os, sys

with open(os.environ["ERSATZ_PROTOKOLL"], "w", encoding="utf-8") as f:
    json.dump({"argv": sys.argv[1:], "venv": os.environ.get("KAP2_VENV")}, f)

modus = os.environ["ERSATZ_MODUS"]
commit = os.environ["ERSATZ_COMMIT"]
wirkungen = [
    {"bezeichnung": "Hitzebelastung (#95)", "betrag_eur_jahr": 179020.81},
    {"bezeichnung": "Allergische Reaktionen durch Aeroallergene pflanzlicher Herkunft (#96)", "betrag_eur_jahr": 2280.6},
    {"bezeichnung": "UV-bedingte Gesundheitsschädigungen (insbesondere Hautkrebs) (#98)", "betrag_eur_jahr": 13053.03},
]
print("Dienst unter http://127.0.0.1:8010 bereit nach 0 s.", flush=True)
print("Bewertung wird neu berechnet (--neu-rechnen).", flush=True)
if modus == "exit1":
    print("FEHLER: Bewertung nach 900 s nicht fertig.", file=sys.stderr, flush=True)
    sys.exit(1)
if modus == "kein_json":
    print("Dauer dieses Aufrufs ohne Sichtstart-Start: 12 s", flush=True)
    sys.exit(0)
if modus == "ohne_98":
    wirkungen = [w for w in wirkungen if "#98" not in w["bezeichnung"]]
if modus == "fremder_commit":
    commit = "fff0000"
print(json.dumps({"kommune": "Warmsen", "status": "done", "klimawirkungen": wirkungen,
                  "commit": commit, "zeit_rechnung": "2026-10-08T10:45:59+00:00"}, ensure_ascii=False), flush=True)
'''

# Aufrufumgebung des Schritts: dieselben Schalter und dieselbe ERR-Falle wie im echten Skript,
# damit ein Rückgabewert ≠ 0 im Block genauso fatal wirkt wie dort.
RAHMEN = """set -Eeuo pipefail
PRODUKT="$1"
VENV="$2"
COMMIT="$3"
SCHRITT="start"
fehler_abbruch() {{
  local rc=$?
  echo "!! Fehler im Schritt $SCHRITT (Rueckgabewert $rc)"
  exit 1
}}
trap fehler_abbruch ERR

{block}
echo "== schritt beispielkommune beendet"
echo "== BEISPIEL_JSON=$BEISPIEL_JSON"
"""


def _block() -> str:
    return ausschnitt('SCHRITT="beispielkommune"', 'SCHRITT="status"')


def _befehlszeilen(block: str) -> str:
    return "\n".join(z for z in block.splitlines() if not z.lstrip().startswith("#"))


def _lauf(tmp_path: Path, modus: str):
    """Führt den echten Block mit dem Ersatzskript aus.

    Gibt Rückgabewert, Protokollausgabe (stdout+stderr), den Pfad aus BEISPIEL_JSON (oder None) und
    die Aufzeichnung des Ersatzskripts zurück.
    """
    produkt = tmp_path / "produkt"
    (produkt / "scripts").mkdir(parents=True)
    ersatz = produkt / "scripts" / "sicht_beispielkommune.py"
    ersatz.write_text(ERSATZ, encoding="utf-8")

    venv = tmp_path / "venv"
    venv.mkdir()
    deploy_tmp = tmp_path / "deploy-tmp"
    deploy_tmp.mkdir()
    aufzeichnung = tmp_path / "ersatz-aufruf.json"

    skript = tmp_path / "beispielkommune-schritt.sh"
    skript.write_text(RAHMEN.format(block=_block()), encoding="utf-8")

    python_verzeichnis = str(Path(shutil.which("python3") or "/usr/bin/python3").parent)
    ergebnis = subprocess.run(
        ["bash", str(skript), str(produkt), str(venv), COMMIT],
        capture_output=True,
        text=True,
        timeout=60,
        env={
            "PATH": f"{python_verzeichnis}:/usr/bin:/bin",
            "HOME": str(tmp_path),
            "DEPLOY_TMP": str(deploy_tmp),
            "ERSATZ_MODUS": modus,
            "ERSATZ_COMMIT": COMMIT,
            "ERSATZ_PROTOKOLL": str(aufzeichnung),
        },
    )
    ausgabe = ergebnis.stdout + ergebnis.stderr
    pfad = None
    for zeile in ausgabe.splitlines():
        if zeile.startswith("== BEISPIEL_JSON="):
            pfad = Path(zeile.split("BEISPIEL_JSON=", 1)[1])
    aufruf = json.loads(aufzeichnung.read_text(encoding="utf-8")) if aufzeichnung.exists() else None
    return ergebnis.returncode, ausgabe, pfad, aufruf, deploy_tmp


def test_skript_ist_syntaktisch_fehlerfrei():
    """`bash -n deploy/test-deploy.sh` endet ohne Fehler und ohne Ausgabe."""
    ergebnis = subprocess.run(["bash", "-n", str(SKRIPT)], capture_output=True, text=True, check=True)
    assert ergebnis.stdout == ""
    assert ergebnis.stderr == ""


def test_schritt_steht_nach_health_check_und_vor_status():
    """Reihenfolge: Neustart → Health-Check → beispielkommune → status."""
    text = skript_text()
    gesund = anker_index(text, 'echo "Backend gesund nach ')
    schritt = anker_index(text, 'SCHRITT="beispielkommune"')
    status = anker_index(text, 'SCHRITT="status"')
    assert anker_index(text, 'SCHRITT="dienst"') < gesund < schritt < status


def test_aufruf_traegt_alle_verlangten_argumente_und_eine_wartegrenze():
    """Der Aufruf nennt Basis, Neurechnung, Anmeldung über Sitzung, die Projektumgebung und eine Grenze."""
    befehle = _befehlszeilen(_block())
    assert hat_anker(befehle, 'KAP2_VENV="$VENV" python3 "$PRODUKT/scripts/sicht_beispielkommune.py"')
    assert hat_anker(befehle, "--basis http://127.0.0.1:8010")
    assert hat_anker(befehle, "--neu-rechnen")
    assert hat_anker(befehle, "--anmeldung sitzung")
    assert hat_anker(befehle, "--warte-sekunden 900")
    assert hat_anker(befehle, 'BEISPIEL_JSON=$(mktemp "$DEPLOY_TMP/')


def test_schritt_liest_und_kopiert_die_umgebungsdatei_nicht():
    """Der Schritt nennt die Umgebungsdatei nicht und gibt DATABASE_URL nicht aus."""
    befehle = _befehlszeilen(_block())
    assert "ENV_DATEI" not in befehle
    assert "source " not in befehle
    assert "DATABASE_URL" not in befehle
    assert "cat /etc" not in befehle


def test_a_gueltige_schlusszeile_ist_gruen_und_json_datei_liegt_vor(tmp_path):
    """(a) #95, #96, #98 und passender Commit: Schritt grün, Schlusszeile in BEISPIEL_JSON."""
    rc, ausgabe, pfad, aufruf, deploy_tmp = _lauf(tmp_path, "gut")
    assert rc == 0, ausgabe
    assert "== schritt beispielkommune beendet" in ausgabe
    assert "!! Fehler im Schritt" not in ausgabe
    # Ausgabe des Skripts steht im Protokoll.
    assert "Bewertung wird neu berechnet (--neu-rechnen)." in ausgabe
    assert f"Beispielkommune Warmsen: 3 Klimawirkungen gerechnet mit Commit {COMMIT}" in ausgabe
    # Die Datei in BEISPIEL_JSON liegt unter DEPLOY_TMP und enthält genau die JSON-Schlusszeile.
    assert pfad is not None and pfad.parent == deploy_tmp, pfad
    inhalt = json.loads(pfad.read_text(encoding="utf-8"))
    assert inhalt["commit"] == COMMIT
    assert [k["bezeichnung"][-4:-1] for k in inhalt["klimawirkungen"]] == ["#95", "#96", "#98"]
    assert len(pfad.read_text(encoding="utf-8").strip().splitlines()) == 1
    # Aufruf des Skripts: genau die verlangten Argumente und die Projektumgebung.
    assert aufruf["argv"] == [
        "--basis", "http://127.0.0.1:8010", "--neu-rechnen", "--anmeldung", "sitzung",
        "--warte-sekunden", "900",
    ]
    assert aufruf["venv"] == str(tmp_path / "venv")


def test_b_exit_1_ist_rot(tmp_path):
    """(b) Das Skript endet mit Exit 1: Schritt rot über die ERR-Falle, kein Weiterlaufen."""
    rc, ausgabe, pfad, _, _ = _lauf(tmp_path, "exit1")
    assert rc != 0, ausgabe
    assert "FEHLER: Bewertung nach 900 s nicht fertig." in ausgabe
    assert "!! Fehler im Schritt beispielkommune" in ausgabe
    assert "== schritt beispielkommune beendet" not in ausgabe
    assert pfad is None


def test_c_fehlende_klimawirkung_98_ist_rot(tmp_path):
    """(c) Keine Klimawirkung mit #98 in `bezeichnung`: rot, und die Meldung nennt #98."""
    rc, ausgabe, pfad, _, _ = _lauf(tmp_path, "ohne_98")
    assert rc != 0, ausgabe
    assert "!! Beispielkommune: Keine Klimawirkung mit #98 in der Bezeichnung." in ausgabe
    assert "!! Fehler im Schritt beispielkommune" in ausgabe
    assert "== schritt beispielkommune beendet" not in ausgabe
    assert pfad is None


def test_d_schlusszeile_kein_json_ist_rot(tmp_path):
    """(d) Exit 0, aber die letzte Zeile ist kein JSON: rot."""
    rc, ausgabe, pfad, _, _ = _lauf(tmp_path, "kein_json")
    assert rc != 0, ausgabe
    assert "!! Beispielkommune: Die letzte Ausgabezeile des Skripts ist kein JSON-Objekt." in ausgabe
    assert "!! Fehler im Schritt beispielkommune" in ausgabe
    assert pfad is None


def test_e_fremder_commit_ist_rot(tmp_path):
    """(e) Das Skript meldet einen anderen Commit als den ausgelieferten: rot, beide Commits genannt."""
    rc, ausgabe, pfad, _, _ = _lauf(tmp_path, "fremder_commit")
    assert rc != 0, ausgabe
    assert f"Gerechnet hat Commit 'fff0000', ausgeliefert ist '{COMMIT}'." in ausgabe
    assert "!! Fehler im Schritt beispielkommune" in ausgabe
    assert pfad is None
