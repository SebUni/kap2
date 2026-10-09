"""Tests für T-1957 (Vorhaben T-1950, A-0068): Der Deploy-Schritt `rauchtest` prüft die
Testumgebung unter ihrer öffentlichen Adresse mit dem Zugang aus der Umgebung.

Der Schritt wird aus `deploy/test-deploy.sh` ausgeschnitten und wirklich in bash ausgeführt. Ein
gefälschtes `curl` ersetzt das Netz: Es zeichnet jeden Aufruf (alle Argumente, Ausgabe,
Rückgabewert) auf, liest den Zugang wie das echte curl als Konfiguration von der Standardeingabe
(`-K -`) und lässt ihn nur bei richtigem Benutzer und richtigem Wert gelten.

Der Testwert des Passworts entsteht zur Laufzeit und enthält ein Anführungszeichen und einen
Rückstrich, damit die Maskierung mitgeprüft wird. Er steht nirgends als Literal in einer Datei.
"""

from __future__ import annotations

import json
import os
import secrets
import subprocess
import sys
from pathlib import Path

import pytest

from _deploy_anker import anker_index, ausschnitt, hat_anker, skript_text

BENUTZER = "rauch_benutzer"
COMMIT = "abc1234"
ADRESSE = "https://test.example.invalid"
STARTSEITE = b"<!doctype html><html><head><script src=\"/assets/index-x1.js\"></script></head></html>\n"

# Gefälschtes curl: Python-Skript, das die für den Schritt nötigen Optionen versteht.
FAKE_CURL = r'''#!__PYTHON__
import json
import os
import sys
from pathlib import Path

argv = sys.argv[1:]
url = None
ziel = None
format_ = None
konfig_stdin = False
mit_fehlercode = False
i = 0
while i < len(argv):
    a = argv[i]
    if a in ("-o", "-w", "--max-time", "-K"):
        wert = argv[i + 1]
        i += 2
        if a == "-o":
            ziel = wert
        elif a == "-w":
            format_ = wert
        elif a == "-K":
            konfig_stdin = wert == "-"
        continue
    if a.startswith("-"):
        if not a.startswith("--") and "f" in a:
            mit_fehlercode = True
        i += 1
        continue
    url = a
    i += 1


def entmaskieren(text):
    """Wie curl in einer Konfiguration: \\ und \" innerhalb von Anführungszeichen."""
    aus = []
    k = 0
    while k < len(text):
        if text[k] == "\\" and k + 1 < len(text):
            aus.append(text[k + 1])
            k += 2
        else:
            aus.append(text[k])
            k += 1
    return "".join(aus)


angemeldet = False
if konfig_stdin:
    for zeile in sys.stdin.read().splitlines():
        if zeile.startswith('user = "') and zeile.endswith('"'):
            angemeldet = entmaskieren(zeile[len('user = "'):-1]) == os.environ["FAKE_ERWARTET"]

rc = 0
ausgabe = ""
if os.environ.get("FAKE_TOT") == "1":
    rc, code, koerper = 7, "000", b""
elif not (angemeldet or os.environ.get("FAKE_OFFEN") == "1"):
    code, koerper = "401", b"Unauthorized"
elif url.endswith("/api/health"):
    code = "200"
    koerper = json.dumps({"status": "ok", "commit": os.environ["FAKE_COMMIT"]}).encode()
else:
    code, koerper = "200", Path(os.environ["FAKE_INDEX"]).read_bytes()

if rc == 0 and mit_fehlercode and int(code) >= 400:
    rc, koerper = 22, b""
if ziel:
    if ziel != "/dev/null":
        Path(ziel).write_bytes(koerper)
else:
    ausgabe += koerper.decode()
if format_:
    ausgabe += format_.replace("%{http_code}", code)
sys.stdout.write(ausgabe)

with open(os.environ["FAKE_LOG"], "a", encoding="utf-8") as f:
    f.write(json.dumps({"argv": argv, "url": url, "angemeldet": angemeldet,
                        "ausgabe": ausgabe, "rc": rc}) + "\n")
sys.exit(rc)
'''


@pytest.fixture()
def umgebung(tmp_path):
    """Arbeitsverzeichnis mit gefälschtem curl, Frontend-Bau und Skriptrahmen."""
    kern = secrets.token_hex(8)
    testwert = kern + chr(34) + chr(92)  # Anführungszeichen und Rückstrich bleiben mitgeprüft
    bin_ = tmp_path / "bin"
    bin_.mkdir()
    curl = bin_ / "curl"
    curl.write_text(FAKE_CURL.replace("__PYTHON__", sys.executable), encoding="utf-8")
    curl.chmod(0o755)
    dist = tmp_path / "produkt" / "frontend" / "dist"
    dist.mkdir(parents=True)
    (dist / "index.html").write_bytes(STARTSEITE)
    (tmp_path / "tmp").mkdir()
    env = dict(os.environ)
    for name in ("TESTUMGEBUNG_ADRESSE", "KAP2_TEST_URL", "KAP2_TEST_BENUTZER", "KAP2_TEST_PASSWORT"):
        env.pop(name, None)
    env["PATH"] = f"{bin_}:{env.get('PATH', '')}"
    env["FAKE_LOG"] = str(tmp_path / "curl.jsonl")
    env["FAKE_COMMIT"] = COMMIT
    env["FAKE_INDEX"] = str(dist / "index.html")
    env["FAKE_ERWARTET"] = BENUTZER + ":" + testwert
    env["TESTUMGEBUNG_ADRESSE"] = ADRESSE
    env["KAP2_TEST_BENUTZER"] = BENUTZER
    env["KAP2_TEST_PASSWORT"] = testwert
    return {"pfad": tmp_path, "env": env, "kern": kern, "testwert": testwert}


def _ausfuehren(u) -> subprocess.CompletedProcess:
    """Führt den echten Block `rauchtest` mit dem Rahmen des Skripts (set -Eeuo, ERR-Falle) aus."""
    pfad = u["pfad"]
    block = ausschnitt('SCHRITT="rauchtest"', 'SCHRITT="beispielkommune"')
    rahmen = (
        "set -Eeuo pipefail\n"
        'SCHRITT="start"\n'
        'fehler_abbruch() { echo "ERR-FALLE bei Schritt $SCHRITT"; exit 1; }\n'
        "trap fehler_abbruch ERR\n"
        f'COMMIT="{COMMIT}"\n'
        f'PRODUKT="{pfad / "produkt"}"\n'
        f'DEPLOY_TMP="{pfad / "tmp"}"\n'
        "RAUCH_PAUSE=0\n"
    )
    datei = pfad / "rauchtest.sh"
    datei.write_text(rahmen + block + '\necho "ENDE erreicht"\n', encoding="utf-8")
    return subprocess.run(
        ["bash", str(datei)], capture_output=True, text=True, env=u["env"], timeout=60
    )


def _aufrufe(u) -> list[dict]:
    log = u["pfad"] / "curl.jsonl"
    if not log.exists():
        return []
    return [json.loads(z) for z in log.read_text(encoding="utf-8").splitlines() if z.strip()]


def _passwort_nirgends(u, ergebnis) -> None:
    """Weder Argumente noch Ausgaben (Block, gefälschtes curl) tragen den Testwert."""
    kern, testwert = u["kern"], u["testwert"]
    aufrufe = _aufrufe(u)
    for aufruf in aufrufe:
        for arg in aufruf["argv"]:
            assert kern not in arg, aufruf["argv"]
        assert kern not in aufruf["ausgabe"]
    log = u["pfad"] / "curl.jsonl"
    if log.exists():
        assert kern not in log.read_text(encoding="utf-8")
    for text in (ergebnis.stdout, ergebnis.stderr):
        assert kern not in text
        assert testwert not in text


def _rot(ergebnis, schritt="rauchtest") -> None:
    assert ergebnis.returncode == 1, ergebnis.stdout + ergebnis.stderr
    assert f"ERR-FALLE bei Schritt {schritt}" in ergebnis.stdout, ergebnis.stdout
    assert "ENDE erreicht" not in ergebnis.stdout


# --- grün ------------------------------------------------------------------------------------


def test_gruen_commit_passt_200_mit_zugang_401_ohne(umgebung):
    ergebnis = _ausfuehren(umgebung)
    assert ergebnis.returncode == 0, ergebnis.stdout + ergebnis.stderr
    assert "ENDE erreicht" in ergebnis.stdout
    for marke in ("Rauchtest (a) gruen", "Rauchtest (b) gruen", "Rauchtest (c) gruen"):
        assert marke in ergebnis.stdout, ergebnis.stdout
    aufrufe = _aufrufe(umgebung)
    assert [a["url"] for a in aufrufe] == [ADRESSE + "/api/health", ADRESSE + "/", ADRESSE + "/"]
    # Die ersten beiden Aufrufe kamen mit dem richtigen Zugang an (über die Standardeingabe),
    # der dritte ohne.
    assert [a["angemeldet"] for a in aufrufe] == [True, True, False]
    assert "-K" not in aufrufe[2]["argv"]
    assert aufrufe[2]["ausgabe"] == "401"
    _passwort_nirgends(umgebung, ergebnis)


def test_gruen_ueber_ersatzadresse_kap2_test_url_mit_schraegstrich(umgebung):
    env = umgebung["env"]
    del env["TESTUMGEBUNG_ADRESSE"]
    env["KAP2_TEST_URL"] = ADRESSE + "/"
    ergebnis = _ausfuehren(umgebung)
    assert ergebnis.returncode == 0, ergebnis.stdout + ergebnis.stderr
    assert [a["url"] for a in _aufrufe(umgebung)] == [
        ADRESSE + "/api/health",
        ADRESSE + "/",
        ADRESSE + "/",
    ]


def test_testumgebung_adresse_hat_vorrang_vor_kap2_test_url(umgebung):
    umgebung["env"]["KAP2_TEST_URL"] = "https://andere.example.invalid"
    ergebnis = _ausfuehren(umgebung)
    assert ergebnis.returncode == 0, ergebnis.stdout + ergebnis.stderr
    assert {a["url"] for a in _aufrufe(umgebung)} == {ADRESSE + "/api/health", ADRESSE + "/"}


# --- rot -------------------------------------------------------------------------------------


def test_rot_bei_falschem_commit(umgebung):
    umgebung["env"]["FAKE_COMMIT"] = "fff9999"
    ergebnis = _ausfuehren(umgebung)
    _rot(ergebnis)
    assert f"erwartet Commit {COMMIT}, gemeldet 'fff9999'" in ergebnis.stdout, ergebnis.stdout
    # Fünf Versuche, danach Schluss; (b) und (c) wurden nicht mehr erreicht.
    aufrufe = _aufrufe(umgebung)
    assert len(aufrufe) == 5
    assert {a["url"] for a in aufrufe} == {ADRESSE + "/api/health"}
    _passwort_nirgends(umgebung, ergebnis)


def test_rot_bei_200_ohne_zugang(umgebung):
    umgebung["env"]["FAKE_OFFEN"] = "1"
    ergebnis = _ausfuehren(umgebung)
    _rot(ergebnis)
    assert "(c)" in ergebnis.stdout and "ohne Zugang HTTP 200" in ergebnis.stdout, ergebnis.stdout
    assert "Rauchtest (c) gruen" not in ergebnis.stdout
    aufrufe = _aufrufe(umgebung)
    assert [a["angemeldet"] for a in aufrufe] == [True, True, False]
    _passwort_nirgends(umgebung, ergebnis)


@pytest.mark.parametrize("variante", ["leer", "ungesetzt"])
def test_rot_ohne_adresse(umgebung, variante):
    env = umgebung["env"]
    if variante == "leer":
        env["TESTUMGEBUNG_ADRESSE"] = ""
    else:
        del env["TESTUMGEBUNG_ADRESSE"]
    ergebnis = _ausfuehren(umgebung)
    _rot(ergebnis)
    assert "weder TESTUMGEBUNG_ADRESSE noch KAP2_TEST_URL gesetzt" in ergebnis.stdout
    assert _aufrufe(umgebung) == []  # nichts wurde angefragt, nicht einmal ohne Zugang


@pytest.mark.parametrize("fehlend", ["KAP2_TEST_BENUTZER", "KAP2_TEST_PASSWORT"])
def test_rot_ohne_zugangsdaten(umgebung, fehlend):
    del umgebung["env"][fehlend]
    ergebnis = _ausfuehren(umgebung)
    _rot(ergebnis)
    assert "KAP2_TEST_BENUTZER oder KAP2_TEST_PASSWORT fehlt" in ergebnis.stdout
    assert _aufrufe(umgebung) == []
    _passwort_nirgends(umgebung, ergebnis)


def test_rot_bei_falschem_zugang(umgebung):
    umgebung["env"]["FAKE_ERWARTET"] = BENUTZER + ":" + secrets.token_hex(8)
    ergebnis = _ausfuehren(umgebung)
    _rot(ergebnis)
    assert all(a["angemeldet"] is False for a in _aufrufe(umgebung))
    _passwort_nirgends(umgebung, ergebnis)


def test_rot_bei_fremder_startseite(umgebung):
    fremd = umgebung["pfad"] / "fremd.html"
    fremd.write_bytes(b"<html>Apache2 Default Page</html>\n")
    umgebung["env"]["FAKE_INDEX"] = str(fremd)
    ergebnis = _ausfuehren(umgebung)
    _rot(ergebnis)
    assert "nicht die index.html des gebauten Frontends" in ergebnis.stdout, ergebnis.stdout
    assert "Rauchtest (c)" not in ergebnis.stdout


def test_rot_wenn_die_adresse_nicht_antwortet(umgebung):
    umgebung["env"]["FAKE_TOT"] = "1"
    ergebnis = _ausfuehren(umgebung)
    _rot(ergebnis)
    assert "antwortet mit Zugang nicht" in ergebnis.stdout, ergebnis.stdout
    _passwort_nirgends(umgebung, ergebnis)


# --- Passwort in keinem Argument ---------------------------------------------------------------


def test_maskierung_anfuehrungszeichen_und_rueckstrich_kommen_unverfaelscht_an(umgebung):
    """Das gefälschte curl entmaskiert wie das echte; passt der Wert, war die Maskierung richtig."""
    assert umgebung["testwert"].endswith(chr(34) + chr(92))
    ergebnis = _ausfuehren(umgebung)
    assert ergebnis.returncode == 0, ergebnis.stdout + ergebnis.stderr
    assert _aufrufe(umgebung)[0]["angemeldet"] is True


def test_curl_aufrufe_im_skript_tragen_den_zugang_nie_im_argument():
    """Statisch: in keiner Befehlszeile mit curl steht das Passwort oder -u/--user."""
    block = ausschnitt('SCHRITT="rauchtest"', 'SCHRITT="beispielkommune"')
    befehle = [z for z in block.splitlines() if not z.lstrip().startswith("#")]
    mit_curl = [z for z in befehle if "curl" in z]
    assert len(mit_curl) == 3, mit_curl
    for zeile in mit_curl:
        assert "PASSWORT" not in zeile and "BENUTZER" not in zeile, zeile
        assert " -u " not in zeile and "--user" not in zeile, zeile
    # Zwei Aufrufe mit Zugang lesen die Konfiguration von der Standardeingabe, einer geht ohne.
    assert sum("-K -" in z for z in mit_curl) == 2
    # Kein ausführlicher Modus, der Kopfzeilen (mit dem Zugang) ausgäbe.
    for zeile in mit_curl:
        assert "-v" not in zeile.split() and "--trace" not in zeile, zeile


# --- Lage im Skript --------------------------------------------------------------------------


def test_schritt_steht_nach_health_check_und_vor_beispielkommune():
    text = skript_text()
    health = anker_index(text, "http://127.0.0.1:8010/api/health")
    rauch = anker_index(text, 'SCHRITT="rauchtest"')
    beispiel = anker_index(text, 'SCHRITT="beispielkommune"')
    assert health < rauch < beispiel


def test_schritt_liest_adresse_und_zugang_aus_der_umgebung_und_endet_rot():
    block = ausschnitt('SCHRITT="rauchtest"', 'SCHRITT="beispielkommune"')
    assert hat_anker(block, "TESTUMGEBUNG_ADRESSE")
    assert hat_anker(block, "KAP2_TEST_URL")
    assert hat_anker(block, "KAP2_TEST_BENUTZER")
    assert hat_anker(block, "KAP2_TEST_PASSWORT")
    assert hat_anker(block, "/api/health")
    assert hat_anker(block, "%{http_code}")
    assert hat_anker(block, '"401"')
    assert hat_anker(block, '"200"')
    assert hat_anker(block, "false")
    befehle = "\n".join(z for z in block.splitlines() if not z.lstrip().startswith("#"))
    assert "sudo" not in befehle  # keine Rechteausweitung im Schritt


def test_skript_ist_syntaktisch_fehlerfrei():
    subprocess.run(["bash", "-n", str(Path(__file__).resolve().parents[2] / "deploy" / "test-deploy.sh")], check=True)
