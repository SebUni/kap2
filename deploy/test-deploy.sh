#!/usr/bin/env bash
# Test-Deployment von kap2 auf dem Server. Läuft als Benutzer overlord, gestartet vom Watcher
# (Signal deploy_anforderung) oder von Hand: /opt/overlord/kap2/deploy/test-deploy.sh [main|<commit>]
# Am Ende schreibt es betrieb/deploy-status.json ins Firmen-Repo und pusht — das ist das Signal.
# -E: der ERR-Trap gilt auch innerhalb von Shell-Funktionen (status_schreiben, fehler_abbruch).
# Ohne -E blieb ein Fehler dort stumm bzw. brach seit T-0120 wortlos ab: kein Status im
# Firmen-Repo, der zuletzt gemeldete Status blieb stehen und wurde weiter als aktuell gelesen.
set -Eeuo pipefail
# Aus einer Kopie laufen: git reset weiter unten überschreibt sonst das laufende Skript.
# Eigenes, dauerhaftes Verzeichnis statt /tmp (T-0425): Der Watcher startet dieses Skript aus
# einem systemd-Oneshot-Dienst mit PrivateTmp=true (Ursache in firma-supervisor gemeldet, hier
# nicht aenderbar) und beendet seinen eigenen Prozess, sobald Popen() zurueckkehrt -- lange bevor
# dieses Skript fertig ist. Sobald der Oneshot-Dienst dabei als "inaktiv" gilt, loest systemd die
# private /tmp-Einhaengung dieses Dienstlaufs, auch fuer laengst abgekoppelte Kindprozesse (siehe
# https://systemd.io/TEMPORARY_DIRECTORIES/); jeder spaetere Zugriff auf /tmp scheitert dann mit
# "No such file or directory", obwohl das echte /tmp des Servers unveraendert existiert und Platz
# hat. Ein Verzeichnis neben PRODUKT/FIRMA/VENV haengt an keiner Dienst-Sitzung und bleibt daher
# fuer die gesamte Laufzeit dieses Skripts erreichbar.
DEPLOY_TMP="${DEPLOY_TMP:-/opt/overlord/kap2-deploy-tmp}"
# Fallback statt Abbruch (Nacharbeit T-0425 Punkt 3): An dieser Stelle steht weder die ERR-Falle
# noch status_schreiben zur Verfuegung (beides braucht Code, der erst weiter unten kommt) -- ein
# hartes "mkdir ... || exit" wuerde also genau die Luecke aus T-0132 wieder aufreissen: der Lauf
# stuerbe wortlos, ohne einen Statuseintrag im Firmen-Repo, und der zuletzt gemeldete Status bliebe
# faelschlich stehen. Schlaegt das Anlegen fehl (z.B. fehlendes Schreibrecht in /opt/overlord),
# faellt der Lauf deshalb auf das alte Verhalten (Server-/tmp) zurueck, statt zu sterben; das
# ist im ungünstigsten Fall so anfaellig wie vor diesem Ticket, aber nie stumm.
DEPLOY_TMP_RUECKFALL=0
if ! mkdir -p "$DEPLOY_TMP" 2>/dev/null; then
  echo "!! Konnte $DEPLOY_TMP nicht anlegen -- falle auf /tmp zurueck (siehe T-0425)" >&2
  DEPLOY_TMP=/tmp
  DEPLOY_TMP_RUECKFALL=1
fi
# TMPDIR fuer den gesamten Lauf setzen, nicht nur fuer die beiden mktemp-Aufrufe unten: sonst
# griffen pip/npm/alembic weiterhin über die ungesetzte Voreinstellung auf /tmp zu und liefen in
# dieselbe Falle, sobald ein Schritt lang genug dauert.
export TMPDIR="$DEPLOY_TMP"
# Aufraeumen alter Eintraege (T-0442): Seit T-0425 ist DEPLOY_TMP ein dauerhaftes Verzeichnis
# statt /tmp, das der Kernel selbst leert. Nach einem harten Abbruch blieben Skriptkopien und
# pip-/npm-Zwischendateien liegen (Urteil T-0425, Anmerkung a) -- auf einem 8-GB-Server kein
# theoretisches Problem. Deshalb hier, VOR dem Anlegen der Skriptkopie, alles unterhalb von
# DEPLOY_TMP entfernen, was aelter als 24 Stunden ist. Die ERR-Falle (trap fehler_abbruch ERR)
# ist an dieser Stelle noch nicht gesetzt -- jeder Schritt ist deshalb bewusst so gebaut, dass er
# unter "set -e" nie mit einem Fehlschlag durchschlaegt: ein Fehler wird protokolliert, der Lauf
# geht weiter, nichts ausserhalb von DEPLOY_TMP wird angefasst.
aufraeumen_alte_eintraege() {  # $1 = Zielverzeichnis
  local ziel="$1" pfad n=0 fehler=0
  while IFS= read -r -d '' pfad; do
    if rm -rf -- "$pfad" 2>/dev/null; then
      n=$((n + 1))
    else
      fehler=1
    fi
  done < <(find "$ziel" -mindepth 1 -maxdepth 1 -mmin +1440 -print0 2>/dev/null)
  echo "-- aufraeumen $ziel: $n alte(n) Eintrag/Eintraege (>24h) entfernt$( [[ $fehler -eq 1 ]] && echo ', Fehler bei mindestens einem Eintrag -- Lauf geht weiter' )"
}
# Nur im Elternprozess aufraeumen (DEPLOY_KOPIE noch nicht gesetzt): sonst liefe die Funktion ein
# zweites Mal in der Kindkopie, die das gesamte Skript ab Zeile 1 erneut durchlaeuft -- harmlos,
# aber unnoetige doppelte Protokollzeile. UND nur, wenn DEPLOY_TMP wirklich das dedizierte
# Verzeichnis ist: Hat der mkdir-Rueckfall gegriffen, zeigt DEPLOY_TMP auf das echte /tmp des
# Servers -- dort "rm -rf" auf fremde, ueber 24h alte Eintraege anderer Dienste und Laeufe
# anzuwenden, waere genau der Verstoss gegen die Zusage "nur unterhalb des eigenen
# Arbeitsverzeichnisses", den Punkt aus der Nacharbeit zu T-0442 benennt.
if [[ -z "${DEPLOY_KOPIE:-}" ]]; then
  if [[ "$DEPLOY_TMP_RUECKFALL" == "0" ]]; then
    aufraeumen_alte_eintraege "$DEPLOY_TMP"
  else
    echo "-- aufraeumen uebersprungen: DEPLOY_TMP ist im Rueckfall das geteilte /tmp des Servers, dort wird nichts angefasst"
  fi
  KOPIE=$(mktemp "$DEPLOY_TMP/test-deploy.XXXXXX.sh"); cp "$0" "$KOPIE"; export DEPLOY_KOPIE=1
  # Signale an die Kopie weiterreichen (T-0132): trifft ein TERM/INT/HUP nur diesen
  # Elternprozess, liefe die Kopie sonst weiter und die Signalfallen unten kaemen nie
  # zum Zug -- der Lauf endete wortlos, genau die Luecke aus T-0132.
  # Fallen VOR dem Start setzen: sonst toetet ein Signal in der Luecke zwischen "&" und
  # "trap" nur diesen Elternprozess und laesst die Kopie verwaist weiterlaufen.
  KIND=""
  for SIG in TERM INT HUP; do trap "[[ -n \$KIND ]] && kill -$SIG \$KIND 2>/dev/null; true" "$SIG"; done
  # Jobsteuerung einschalten (set -m): ohne sie setzt Bash in einer nicht-interaktiven
  # Shell bei "&" im Kind SIGINT/SIGQUIT auf SIG_IGN; ein beim Start ignoriertes Signal
  # laesst sich in der Kindshell nicht mehr per trap belegen -- die INT-Falle unten waere
  # in genau dem Prozess wirkungslos, der den Statuseintrag schreiben soll.
  set -m
  bash "$KOPIE" "$@" & KIND=$!
  set +m
  RC=0
  # wait bricht mit >128 ab, sobald eine der Fallen zuschlaegt: dann erneut warten,
  # bis die Kopie ihren Status geschrieben hat und wirklich beendet ist.
  while true; do
    if wait "$KIND"; then RC=0; else RC=$?; fi
    if [[ $RC -gt 128 ]] && kill -0 "$KIND" 2>/dev/null; then continue; fi
    break
  done
  rm -f "$KOPIE"; exit $RC
fi
REF="${1:-main}"
PRODUKT=/opt/overlord/kap2
FIRMA=/opt/overlord/firma-deploy
VENV=/opt/overlord/kap2-venv
ENV_DATEI=/etc/overlord/kap2-test.env
PROTOKOLL=/var/log/overlord/deploy.log
# Passwort selbst geht nie in die Statusdatei des Firmen-Repos (T-0169): nur der Pfad der
# Datei auf dem Server, in der es tatsaechlich liegt -- das ist ENV_DATEI (Rechte 600),
# aus der es unten per "source" bezogen wird.
PASSWORT_QUELLE="$ENV_DATEI"
SCHRITT="start"; COMMIT=""
set -a; source "$ENV_DATEI"; set +a
# Rueckfallweg fuer den Dienst-Neustart (T-0342). Der Lauf arbeitet aus einer Kopie in
# $DEPLOY_TMP (siehe oben), deshalb wird die Bibliothek ueber $PRODUKT geladen und nicht ueber
# $0 -- sonst suchte "source" im Ablageverzeichnis der Kopie.
source "$PRODUKT/deploy/lib-neustart.sh"

speicher_zeile() {  # $1 = Marke (vorher|nachher|...) -- Beweismittel im Protokoll (T-0132)
  local mb
  mb=$(free -m 2>/dev/null | awk 'NR==1{for(i=1;i<=NF;i++) if($i=="available") s=i+1}
                                  /^Mem:/{print (s ? $s : $NF)}' 2>/dev/null || true)
  echo "-- speicher $1 available=${mb:-unbekannt} MB, laufzeit=${SECONDS}s"
}
aufseher_zeile() {  # Zustand der Speicherwaechter im Nutzerraum -- die senden TERM, nicht KILL
  local dienst zustand ausgabe=""
  for dienst in earlyoom systemd-oomd; do
    if command -v systemctl >/dev/null 2>&1; then
      zustand=$(systemctl is-active "$dienst" 2>/dev/null || true)
      [[ -n "$zustand" ]] || zustand="unbekannt"
    else
      zustand="unbekannt"
    fi
    ausgabe+="$dienst=$zustand "
  done
  echo "-- aufseher ${ausgabe% }"
}
status_lokal_schreiben() {  # $1 = fertig|fehler, $2 = Fehlertext -- schreibt nur lokal, pusht nicht
  local st="$1" fehler="$2" zeit adresse
  # Vorabpruefung (T-0126): FIRMA muss ein eigenes Repository sein, sonst sucht
  # "git -C $FIRMA" aufwaerts und trifft im Zweifel den umgebenden Arbeitsklon von
  # kap2 -- dort duerfen reset --hard/add/commit/push nie stattfinden.
  local firma_eltern top
  firma_eltern=$(dirname -- "$FIRMA")
  if ! top=$(GIT_CEILING_DIRECTORIES="$firma_eltern" git -C "$FIRMA" rev-parse --show-toplevel 2>&1) \
     || [[ "$(readlink -f -- "$top" 2>/dev/null)" != "$(readlink -f -- "$FIRMA" 2>/dev/null)" ]]; then
    echo "!! FIRMA ist kein eigenes Repository: $FIRMA (git rev-parse --show-toplevel liefert: ${top:-<kein Treffer>})"
    exit 1
  fi
  export GIT_CEILING_DIRECTORIES="$firma_eltern"
  zeit=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  adresse="${KAP2_TEST_URL:-http://localhost}"
  # Passwort selbst geht nie in die Statusdatei des Firmen-Repos (T-0169): nur der Pfad der
  # Datei auf dem Server, in der es liegt.
  # T-1832: Nachweis ohne Browser. Zusaetzlich zwei Felder: "datenbank" (DATENBANK_VORHER/-NACHHER
  # aus dem Schritt datenbank) und "beispielkommune" (feste Auswahl aus der Datei in BEISPIEL_JSON
  # aus dem Schritt beispielkommune). Die Funktion laeuft auch im Abbruchpfad, wenn der Lauf vor
  # diesen Schritten endete: die Variablen sind dann ungesetzt (set -u!), deshalb ${NAME:-} --
  # leer wird im Status zu null. Die Datei in BEISPIEL_JSON wird nie ganz uebernommen.
  python3 - "$st" "$fehler" "$zeit" "$adresse" "$COMMIT" "$PROTOKOLL" "${KAP2_TEST_BENUTZER:-}" "$PASSWORT_QUELLE" \
    "${DATENBANK_VORHER:-}" "${DATENBANK_NACHHER:-}" "${BEISPIEL_JSON:-}" > "$FIRMA/betrieb/deploy-status.json.neu" <<'PY'
import json, sys
st, fehler, zeit, adresse, commit, protokoll, benutzer, passwort_quelle, db_vorher, db_nachher, beispiel_pfad = sys.argv[1:12]


def zahl(w):
    return w if isinstance(w, (int, float)) and not isinstance(w, bool) else None


def text(w):
    if isinstance(w, str):
        return w[:300]
    return zahl(w)


def beispielkommune(pfad):
    """Feste Auswahl aus der Schlusszeile des Beispielkommune-Skripts; sonst null."""
    if not pfad:
        return None
    try:
        with open(pfad, encoding="utf-8") as f:
            roh = json.load(f)
    except (OSError, ValueError):
        return None
    if not isinstance(roh, dict):
        return None
    liste = roh.get("klimawirkungen")
    wirkungen = None
    if isinstance(liste, list):
        wirkungen = [{"bezeichnung": text(k.get("bezeichnung")), "betrag_eur_jahr": zahl(k.get("betrag_eur_jahr"))}
                     for k in liste if isinstance(k, dict)]
    return {"kommune": text(roh.get("kommune")), "gemeindeschluessel": text(roh.get("gemeindeschluessel")),
            "commit": text(roh.get("commit")), "zeit_rechnung": text(roh.get("zeit_rechnung")),
            "klimawirkungen": wirkungen}


d = {"zeit": zeit, "status": st, "adresse": adresse, "commit": commit or None,
     "fehler": (fehler[:1500] if st == "fehler" else None), "protokoll": protokoll}
if benutzer:
    d["zugang"] = {"benutzer": benutzer, "passwort_quelle": passwort_quelle, "hinweis": "HTTP Basic Auth der Testumgebung"}
d["datenbank"] = {"vorher": db_vorher[:500] or None, "nachher": db_nachher[:500] or None}
d["beispielkommune"] = beispielkommune(beispiel_pfad)
print(json.dumps(d, ensure_ascii=False, indent=1))
PY
  # Erst lokal festschreiben, dann veroeffentlichen (T-0132): trifft waehrend des Pushens
  # ein zweites Signal, liegt der Eintrag wenigstens schon in der Arbeitskopie.
  cp "$FIRMA/betrieb/deploy-status.json.neu" "$FIRMA/betrieb/deploy-status.json"
  echo "-- status lokal geschrieben: $st"
}
status_veroeffentlichen() {  # $1 = fertig|fehler -- pusht den zuvor lokal geschriebenen Eintrag
  local st="$1"
  local versuch push_rc=1
  for versuch in 1 2 3 4 5; do
    git -C "$FIRMA" fetch -q origin && git -C "$FIRMA" reset -q --hard origin/main || true
    # cp statt mv: die .neu-Datei muss fuer jeden der bis zu 5 Versuche erhalten bleiben,
    # sonst bricht der Wiederholungsversuch nach dem ersten Durchlauf an einer fehlenden
    # Quelldatei ab, statt tatsaechlich erneut zu pushen.
    cp "$FIRMA/betrieb/deploy-status.json.neu" "$FIRMA/betrieb/deploy-status.json"
    git -C "$FIRMA" add betrieb/deploy-status.json
    git -C "$FIRMA" commit -q -m "Deploy-Status: $st ($COMMIT)" || true
    git -C "$FIRMA" push -q origin main:main && push_rc=0 || push_rc=$?
    if [[ $push_rc -eq 0 ]]; then break; fi
    sleep $((versuch * 3))
  done
  rm -f "$FIRMA/betrieb/deploy-status.json.neu"
  if [[ $push_rc -ne 0 ]]; then
    echo "!! Status konnte nicht veroeffentlicht werden nach $versuch Versuchen (Rueckgabewert letzter Versuch: $push_rc)"
    exit 1
  fi
}
status_schreiben() {  # $1 = fertig|fehler, $2 = Fehlertext
  status_lokal_schreiben "$1" "$2"
  status_veroeffentlichen "$1"
}
fehler_abbruch() {
  local rc=$?
  local zeilen; zeilen=$(tail -n 25 "$PROTOKOLL" 2>/dev/null | tr -d '\r' || true)
  echo "!! Fehler im Schritt $SCHRITT (Rueckgabewert $rc)"
  aufseher_zeile
  status_schreiben fehler "Schritt $SCHRITT fehlgeschlagen. Letzte Protokollzeilen:
$zeilen"
  exit 1
}
signal_abbruch() {  # $1 = Signalname (TERM|INT|HUP), $2 = Signalnummer -- T-0132
  local sig="$1" num="$2"
  # Fallen sofort loesen: der Abbruchpfad darf sich nicht selbst erneut ausloesen.
  # Weitere Signale werden ignoriert (trap ''), nicht auf Vorgabe zurueckgesetzt (trap -):
  # sonst toetet ein zweites TERM den Abbruchpfad genau in dem Fenster, in dem
  # status_veroeffentlichen per "git reset --hard origin/main" den soeben lokal
  # geschriebenen Eintrag kurzzeitig zurueckdreht -- der Eintrag waere dann wieder weg.
  trap - ERR
  trap '' TERM INT HUP
  echo "!! abgebrochen durch Signal $sig im Schritt $SCHRITT"
  speicher_zeile "abbruch"
  aufseher_zeile
  # Erst lokal schreiben, dann pushen: ein zweites Signal waehrend des Pushens kann den
  # Eintrag dann nicht mehr verhindern.
  status_lokal_schreiben fehler "abgebrochen durch Signal $sig im Schritt $SCHRITT"
  # In einer Unter-Shell: status_veroeffentlichen beendet bei endgueltig gescheitertem
  # Push mit "exit 1"; das darf hier nur die Unter-Shell treffen. Sonst waere das "|| true"
  # wirkungslos und der Signalabbruch endete mit 1 statt mit 128+Signalnummer. Der
  # Statuseintrag liegt zu diesem Zeitpunkt bereits lokal fest.
  ( status_veroeffentlichen fehler ) || echo "!! Veroeffentlichen nach Signal $sig fehlgeschlagen; Eintrag liegt lokal vor"
  exit $((128 + num))
}
trap fehler_abbruch ERR
trap 'signal_abbruch TERM 15' TERM
trap 'signal_abbruch INT 2' INT
trap 'signal_abbruch HUP 1' HUP

echo "== $(date -u +%FT%TZ) Deploy $REF"
SCHRITT="git"
cd "$PRODUKT"
git fetch -q origin
if git rev-parse -q --verify "origin/$REF" >/dev/null; then git checkout -q -B deploy "origin/$REF"; else git checkout -q -B deploy "$REF"; fi
COMMIT=$(git rev-parse --short HEAD)
echo "Commit $COMMIT"

SCHRITT="deploy-tests"
# T-0530: Die Deploy-Tests (backend/tests/test_deploy_*.py) laufen vor jedem Deploy, gegen genau
# den Stand, der gleich ausgeliefert wird -- und VOR Abhaengigkeiten, Bau, Migration und Neustart.
# Sonst faellt Drift zwischen Skript und Tests erst beim Ausliefern auf, und dann steht die
# Testumgebung. Rot bricht hier ab (ERR-Falle -> Status "fehler" im Firmen-Repo); gebaut oder
# ausgeliefert wird dann nichts. Die Tests brauchen nur pytest und die Standardbibliothek; fehlt
# pytest im venv, wird es nachinstalliert, statt die Tests stillschweigend auszulassen.
# --tb=line: je rotem Test eine Zeile mit dem Grund (bei Ankern: "ANKER ROT: '<anker>' ..."),
# damit der Grund in den letzten Protokollzeilen des Fehlerstatus steht.
cd "$PRODUKT/backend"
[[ -x "$VENV/bin/pip" ]] || python3.12 -m venv "$VENV"
"$VENV/bin/python" -m pytest --version >/dev/null 2>&1 || "$VENV/bin/pip" install -q pytest
if ! env -u KAP2_DEPLOY_SKRIPT "$VENV/bin/python" -m pytest -q -p no:cacheprovider --tb=line tests/test_deploy_*.py; then
  echo "!! Deploy-Tests rot -- Abbruch vor Bau und Auslieferung (nichts gebaut, nichts neu gestartet)"
  false
fi
echo "Deploy-Tests gruen"

SCHRITT="backend-abhaengigkeiten"
# Explizit ins Backend-Verzeichnis wechseln statt sich auf das cwd des vorherigen Schritts
# (deploy-tests) zu verlassen: Dort steht bereits "$PRODUKT/backend", weshalb der bisherige
# relative Pfad "backend/requirements.txt" ins Leere lief ("Could not open requirements file"),
# und die Datei nur bei zufaellig anderem cwd gefunden wurde.
cd "$PRODUKT/backend"
[[ -x "$VENV/bin/pip" ]] || python3.12 -m venv "$VENV"
"$VENV/bin/pip" install -q --upgrade pip wheel
"$VENV/bin/pip" install -q -r requirements.txt

SCHRITT="frontend-build"
cd "$PRODUKT/frontend"
npm ci --no-audit --no-fund --loglevel=error
# Messung statt Vermutung (T-0132): verfuegbarer Speicher und Laufzeit vor und nach dem Bau.
speicher_zeile "vor frontend-build"
npm run build --silent
speicher_zeile "nach frontend-build"

SCHRITT="datenbank"
cd "$PRODUKT/backend"
mkdir -p logs
# T-1829: Der Schritt fuehrt genau einen Weg aus -- "alembic upgrade head" -- und scheitert laut,
# wenn der misslingt. Es gibt weder einen Rueckfall auf die Anlage per Base.metadata.create_all
# (T-0339) noch ein Setzen des Alembic-Stands ohne Migration. Beides erklaerte ein Schema, das
# beim Dienststart per create_all entstanden ist (app/main.py, _ensure_tables), still fuer
# migriert; beim Deploy vom 06.10.2026 (ce951ead) lief das so, ohne dass das Runbook-Kriterium
# (leere Ausgabe von "alembic check") geprueft worden waere. Eine Bestandsdatenbank, deren Schema
# nicht aus der Migrationskette stammt, hebt ein Mensch nach docs/BETRIEB.md, Abschnitt
# "Bestandsdatenbank auf die Migrationskette heben", auf die Kette.
# Der Stand wird sichtbar gemacht: Ausgabe von "alembic current" vor und nach dem Upgrade, auch
# in den Variablen DATENBANK_VORHER und DATENBANK_NACHHER (Paket 4 schreibt sie in den Status).
# Leer heisst vorher: keine Tabelle alembic_version oder kein Eintrag darin. Schlaegt schon diese
# Abfrage fehl (Datenbank nicht erreichbar), bleibt der Wert leer und das Upgrade meldet den
# Fehler selbst.
DATENBANK_VORHER=$("$VENV/bin/alembic" current 2>/dev/null | tr '\n' ' ' | sed 's/ *$//' || true)
echo "Datenbank vorher: $DATENBANK_VORHER"
ALEMBIC_LOG=$(mktemp "$DEPLOY_TMP/alembic.XXXXXX.log")
if "$VENV/bin/alembic" upgrade head >"$ALEMBIC_LOG" 2>&1; then
  cat "$ALEMBIC_LOG"
  rm -f "$ALEMBIC_LOG"
else
  cat "$ALEMBIC_LOG"
  if grep -qiE 'DuplicateTable|DuplicateColumn|already exists' "$ALEMBIC_LOG"; then
    echo "!! SCHRITT datenbank FEHLGESCHLAGEN (alembic upgrade head): Tabelle oder Spalte existiert bereits -- das Schema stammt nicht aus der Migrationskette. Nichts wird gesetzt oder nachgebaut. Weiter nach docs/BETRIEB.md, Abschnitt \"Bestandsdatenbank auf die Migrationskette heben\"."
  else
    echo "!! SCHRITT datenbank FEHLGESCHLAGEN (alembic upgrade head), Ursache im Alembic-Protokoll oben. Bei einer Bestandsdatenbank ohne Migrationsstand: docs/BETRIEB.md, Abschnitt \"Bestandsdatenbank auf die Migrationskette heben\"."
  fi
  rm -f "$ALEMBIC_LOG"
  false
fi
DATENBANK_NACHHER=$("$VENV/bin/alembic" current 2>/dev/null | tr '\n' ' ' | sed 's/ *$//')
echo "Datenbank nachher: $DATENBANK_NACHHER"

SCHRITT="dienst"
# T-0197: kap2-test.service ist eine System-Unit und wird ohne sudo neu gestartet. "systemctl
# restart" schickt dazu eine D-Bus-Anfrage an PID 1, die polkit fragt; die Berechtigung liegt auf
# dem Server als .pkla-Regel (polkit 0.105 kennt keine JavaScript-Regeln). Das funktioniert auch
# unter der "no new privileges"-Sperre des Deploy-Laufs, an der sudo scheitert, weil kein
# setuid-Programm ausgefuehrt wird.
# Vorbedingung ausdruecklich pruefen: fehlt die Unit, soll der Lauf mit einer verstaendlichen
# Anweisung abbrechen statt mit einer nackten systemctl-Fehlermeldung. Die polkit-Regel wird
# bewusst NICHT vorab geprueft (sie kann als .pkla oder .rules vorliegen) -- ihr Fehlen zeigt
# sich am abgelehnten Neustart, und dort steht der noetige Handgriff woertlich.
if ! /bin/systemctl list-unit-files kap2-test.service >/dev/null 2>&1 \
   || ! /bin/systemctl cat kap2-test.service >/dev/null 2>&1; then
  echo "!! kap2-test.service ist auf diesem Server nicht installiert."
  echo "   Einmalig als root: cp $PRODUKT/deploy/kap2-test.service /etc/systemd/system/kap2-test.service &&"
  echo "   systemctl daemon-reload && systemctl enable --now kap2-test"
  false
fi
ALT_PID=$(/bin/systemctl show -p MainPID --value kap2-test 2>/dev/null || echo 0)
if ! /bin/systemctl restart kap2-test; then
  # T-0342: Erst der Rueckfallweg ueber den eigenen Prozess, bevor der Schritt scheitert.
  # Die Unit faehrt unter derselben Kennung wie dieser Lauf; ein SIGKILL an ihren Hauptprozess
  # braucht kein polkit, und systemd zieht die Unit wegen Restart=on-failure von selbst wieder
  # hoch. "systemctl restart" bleibt der erste Versuch, dieser Weg ist nur der Rueckfall.
  echo "-- systemctl restart abgelehnt; Rueckfall: Signal an den eigenen Dienstprozess (T-0342)"
  NEUSTART_RC=0
  neustart_ueber_eigenen_prozess kap2-test || NEUSTART_RC=$?
  if [[ $NEUSTART_RC -ne 0 ]]; then
    echo "!! Neustart von kap2-test abgelehnt (fehlendes Recht oder kein D-Bus-Zugang),"
    echo "   und der Rueckfall ueber den eigenen Prozess trug nicht (Rueckgabewert $NEUSTART_RC)."
    echo "   Einmalig als root die polkit-Regel anlegen (polkit 0.105, deshalb .pkla, nicht .rules):"
    echo "   /etc/polkit-1/localauthority/50-local.d/50-kap2-test.pkla -- sie erlaubt dem Benutzer"
    echo "   overlord org.freedesktop.systemd1.manage-units fuer die Unit-Datei"
    echo "   /etc/systemd/system/kap2-test.service; danach: systemctl restart polkit"
    echo "   Der Schritt wird bewusst NICHT uebersprungen -- ohne Neustart laeuft der alte Stand."
    false
  fi
  # Ob der Rueckfall wirklich getragen hat, entscheidet nicht dieser Zweig, sondern die
  # Pruefung auf eine gewechselte MainPID und der Health-Check gegen den ausgelieferten Commit.
  echo "-- warte auf den von systemd nachgezogenen Neustart (Restart=on-failure, RestartSec=5)"
fi
# Beweis, dass wirklich ein neuer Prozess laeuft: MainPID muss sich geaendert haben und != 0 sein.
NEU_PID=""
for i in $(seq 1 30); do
  NEU_PID=$(/bin/systemctl show -p MainPID --value kap2-test 2>/dev/null || echo 0)
  if [[ -n "$NEU_PID" && "$NEU_PID" != "0" && "$NEU_PID" != "$ALT_PID" ]]; then break; fi
  if [[ $i -eq 30 ]]; then
    echo "!! kap2-test hat nach dem Neustart keinen neuen Hauptprozess (alt=$ALT_PID, jetzt=${NEU_PID:-leer})"
    false
  fi
  sleep 1
done
echo "kap2-test neu gestartet: MainPID $ALT_PID -> $NEU_PID"
# Health-Check gegen die Identitaet des neuen Prozesses: /api/health meldet seit T-0197 den
# ausgelieferten Commit. Antwortet noch ein alter Prozess auf Port 8010 (etwa eine vergessene
# zweite Unit), meldet er einen anderen Commit -- der Lauf gilt dann als gescheitert, statt
# faelschlich "fertig" zu melden.
for i in $(seq 1 60); do
  ANTWORT=$(curl -sf http://127.0.0.1:8010/api/health || true)
  if [[ -n "$ANTWORT" ]]; then
    GEMELDET=$(printf '%s' "$ANTWORT" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("commit") or "")' 2>/dev/null || true)
    if [[ "$GEMELDET" == "$COMMIT" ]]; then echo "Backend gesund nach ${i}x2s (Commit $GEMELDET)"; break; fi
  fi
  if [[ $i -eq 60 ]]; then
    if [[ -z "$ANTWORT" ]]; then
      echo "Backend antwortet nicht"
    else
      echo "!! Auf 127.0.0.1:8010 antwortet nicht der neu ausgerollte Stand:"
      echo "   erwartet Commit $COMMIT, gemeldet '${GEMELDET:-unbekannt}' (Antwort: $ANTWORT)"
    fi
    false
  fi
  sleep 2
done

SCHRITT="rauchtest"
# T-1957 (Vorhaben T-1950, A-0068): Der Health-Check oben ist nur die Vorstufe auf 127.0.0.1:8010.
# Gesehen wird die Testumgebung aber unter ihrer oeffentlichen Adresse, ueber Apache mit Basic-Auth;
# deshalb prueft dieser Schritt genau dort -- mit derselben Adresse und demselben Zugang, den der
# Aufsichtsrat im Dashboard benutzt. Adresse: TESTUMGEBUNG_ADRESSE, ersatzweise KAP2_TEST_URL;
# Zugang: KAP2_TEST_BENUTZER / KAP2_TEST_PASSWORT. Alle vier kommen aus der oben eingelesenen
# Umgebungsdatei; ihre Werte werden nie ausgegeben. Fehlt die Adresse oder der Zugang, endet der
# Schritt rot (ERR-Falle, Status "fehler"), er wird nicht uebersprungen.
# Geprueft wird nur Erreichbarkeit, Identitaet und Schutz, keine Kommunenseite (die Seiten unter
# /app/ verlangen zusaetzlich eine Anmeldung im Produkt):
#   (a) /api/health mit Zugang meldet den ausgelieferten Commit,
#   (b) / mit Zugang liefert HTTP 200 mit der index.html des gerade gebauten Frontends,
#   (c) / ohne Zugang liefert HTTP 401.
# Das Passwort steht in keinem Argument eines Kindprozesses: curl liest es als Konfiguration von der
# Standardeingabe (-K -); printf ist ein Shell-Builtin und startet keinen Prozess. Anfuehrungszeichen
# und Rueckstrich werden fuer die Konfiguration maskiert.
rauch_zugang() {
  local benutzer="${KAP2_TEST_BENUTZER//\\/\\\\}" geheim="${KAP2_TEST_PASSWORT//\\/\\\\}"
  benutzer="${benutzer//\"/\\\"}"; geheim="${geheim//\"/\\\"}"
  printf 'user = "%s:%s"\n' "$benutzer" "$geheim"
}
RAUCH_ADRESSE="${TESTUMGEBUNG_ADRESSE:-${KAP2_TEST_URL:-}}"
RAUCH_ADRESSE="${RAUCH_ADRESSE%/}"
RAUCH_PAUSE="${RAUCH_PAUSE:-2}"
if [[ -z "$RAUCH_ADRESSE" ]]; then
  echo "!! Rauchtest: weder TESTUMGEBUNG_ADRESSE noch KAP2_TEST_URL gesetzt (Umgebungsdatei des Servers) -- NICHT uebersprungen"
  false
fi
if [[ -z "${KAP2_TEST_BENUTZER:-}" || -z "${KAP2_TEST_PASSWORT:-}" ]]; then
  echo "!! Rauchtest: KAP2_TEST_BENUTZER oder KAP2_TEST_PASSWORT fehlt (Umgebungsdatei des Servers) -- NICHT uebersprungen"
  false
fi
echo "Rauchtest an der oeffentlichen Adresse $RAUCH_ADRESSE (erwarteter Commit $COMMIT)"
# (a) Identitaet: bis zu 5 Versuche, Apache und Dienst brauchen nach dem Neustart einen Moment.
RAUCH_GEMELDET=""
for i in $(seq 1 5); do
  RAUCH_ANTWORT=$(rauch_zugang | curl -sf --max-time 20 -K - "$RAUCH_ADRESSE/api/health" 2>/dev/null || true)
  RAUCH_GEMELDET=$(printf '%s' "$RAUCH_ANTWORT" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("commit") or "")' 2>/dev/null || true)
  if [[ "$RAUCH_GEMELDET" == "$COMMIT" ]]; then break; fi
  if [[ $i -lt 5 ]]; then sleep "$RAUCH_PAUSE"; fi
done
if [[ "$RAUCH_GEMELDET" != "$COMMIT" ]]; then
  if [[ -z "$RAUCH_ANTWORT" ]]; then
    echo "!! Rauchtest (a): $RAUCH_ADRESSE/api/health antwortet mit Zugang nicht (Apache, Weiterleitung oder Zugang pruefen)"
  else
    echo "!! Rauchtest (a): erwartet Commit $COMMIT, gemeldet '${RAUCH_GEMELDET:-unbekannt}'"
  fi
  false
fi
echo "Rauchtest (a) gruen: /api/health meldet Commit $RAUCH_GEMELDET"
# (b) Startseite mit Zugang: HTTP 200 und die index.html des Frontends, das gerade gebaut wurde.
RAUCH_SEITE=$(mktemp "$DEPLOY_TMP/rauchtest.XXXXXX.html")
RAUCH_CODE=$(rauch_zugang | curl -s --max-time 20 -K - -o "$RAUCH_SEITE" -w '%{http_code}' "$RAUCH_ADRESSE/" 2>/dev/null || true)
if [[ "$RAUCH_CODE" != "200" ]]; then
  echo "!! Rauchtest (b): $RAUCH_ADRESSE/ liefert mit Zugang HTTP ${RAUCH_CODE:-keine Antwort}, erwartet 200"
  rm -f "$RAUCH_SEITE"
  false
fi
if ! cmp -s "$RAUCH_SEITE" "$PRODUKT/frontend/dist/index.html"; then
  echo "!! Rauchtest (b): $RAUCH_ADRESSE/ liefert nicht die index.html des gebauten Frontends"
  rm -f "$RAUCH_SEITE"
  false
fi
rm -f "$RAUCH_SEITE"
echo "Rauchtest (b) gruen: / liefert HTTP 200 mit der index.html des Frontends"
# (c) Schutz: ohne Zugang muss Apache abweisen.
RAUCH_CODE=$(curl -s --max-time 20 -o /dev/null -w '%{http_code}' "$RAUCH_ADRESSE/" 2>/dev/null || true)
if [[ "$RAUCH_CODE" != "401" ]]; then
  echo "!! Rauchtest (c): $RAUCH_ADRESSE/ liefert ohne Zugang HTTP ${RAUCH_CODE:-keine Antwort}, erwartet 401 -- die Testumgebung ist nicht geschuetzt"
  false
fi
echo "Rauchtest (c) gruen: / liefert ohne Zugang HTTP 401"

SCHRITT="beispielkommune"
# T-1831 (Vorhaben T-1828, A-0066): Nach dem Neustart rechnet der gerade ausgelieferte Stand die
# Beispielkommune Warmsen vollstaendig neu; der Health-Check oben hat den Commit schon bestaetigt.
# Das Skript legt Gemeindetabelle (VG250), Kommune und Massnahme an, falls sie fehlen, und meldet
# sich mit einer technischen Sitzung an (--anmeldung sitzung). DATABASE_URL steht aus der oben
# eingelesenen Umgebungsdatei in der Umgebung; sie wird hier weder ausgegeben noch kopiert, und das
# Skript gibt den Sitzungsschluessel nie aus.
# Wartegrenze (Frist des Watchers: DEPLOY_FRIST_MIN = 30 min = 1800 s): --warte-sekunden 900 bricht
# die Bewertung nach 15 min ab. Gemessen (T-1830, Sichtstart): Neurechnung 642 s, 399 s, 195 s; ganzer
# Aufruf 801 s, 442 s, 296 s, 208 s. Die bisherigen Deploys ohne diesen Schritt brauchten von der
# Anforderung bis "fertig" hoechstens 8 min (480 s, davon bis zu 2 min Watcher-Takt). Schlechtester Fall:
# 480 s + 900 s = 1380 s (23 min); bleiben 420 s fuer VG250-Import, Raster und Massnahme beim ersten Lauf.
# Die Zeit dieser Zwischenschritte begrenzt --warte-sekunden nicht (je Aufruf des Produktcodes
# hoechstens 1800 s im Skript), deshalb steht die Frist nicht allein auf dieser Grenze.
# Ausgabe: alles geht ins Protokoll (tee); die letzte Zeile (JSON) liegt zusaetzlich in BEISPIEL_JSON,
# das Paket 4 in den Status uebernimmt. Scheitert das Skript oder die Pruefung unten, endet der Schritt
# ueber die ERR-Falle: Status "fehler", nie "fertig". pipefail laesst den Rueckgabewert des Skripts
# durch das tee hindurch wirken.
BEISPIEL_LOG=$(mktemp "$DEPLOY_TMP/beispielkommune.XXXXXX.log")
BEISPIEL_JSON=$(mktemp "$DEPLOY_TMP/beispielkommune.XXXXXX.json")
KAP2_VENV="$VENV" python3 "$PRODUKT/scripts/sicht_beispielkommune.py" \
  --basis http://127.0.0.1:8010 --neu-rechnen --anmeldung sitzung --warte-sekunden 900 2>&1 \
  | tee "$BEISPIEL_LOG"
tail -n 1 "$BEISPIEL_LOG" > "$BEISPIEL_JSON"
rm -f "$BEISPIEL_LOG"
# Pruefung der Schlusszeile: JSON, je eine Klimawirkung #95, #96 und #98 in "bezeichnung", und der
# gemeldete Commit ist der ausgelieferte. Jede Abweichung beendet den Schritt mit Rueckgabewert 1.
python3 - "$BEISPIEL_JSON" "$COMMIT" <<'PY'
import json, sys
pfad, commit = sys.argv[1:3]
zeile = open(pfad, encoding="utf-8").read().strip()
try:
    d = json.loads(zeile)
except ValueError:
    d = None
if not isinstance(d, dict):
    print("!! Beispielkommune: Die letzte Ausgabezeile des Skripts ist kein JSON-Objekt.")
    sys.exit(1)
liste = d.get("klimawirkungen")
bezeichnungen = [str(k.get("bezeichnung") or "") for k in liste if isinstance(k, dict)] if isinstance(liste, list) else []
fehlt = [c for c in ("#95", "#96", "#98") if not any(c in b for b in bezeichnungen)]
if fehlt:
    print("!! Beispielkommune: Keine Klimawirkung mit " + ", ".join(fehlt) + " in der Bezeichnung.")
    sys.exit(1)
if d.get("commit") != commit:
    print("!! Beispielkommune: Gerechnet hat Commit '%s', ausgeliefert ist '%s'." % (d.get("commit"), commit))
    sys.exit(1)
print("Beispielkommune %s: %d Klimawirkungen gerechnet mit Commit %s" % (d.get("kommune"), len(bezeichnungen), commit))
PY

SCHRITT="status"
# Trap bleibt bewusst aktiv: scheitert das Schreiben oder Pushen des Status, ist der Lauf nicht
# bestaetigt -- dann darf er nicht stumm enden und den vorherigen Status stehen lassen.
status_schreiben fertig ""
echo "== fertig: ${KAP2_TEST_URL:-} ($COMMIT)"
