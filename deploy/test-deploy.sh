#!/usr/bin/env bash
# Test-Deployment von kap2 auf dem Server. Läuft als Benutzer overlord, gestartet vom Watcher
# (Signal deploy_anforderung) oder von Hand: /opt/overlord/kap2/deploy/test-deploy.sh [main|<commit>]
# Am Ende schreibt es betrieb/deploy-status.json ins Firmen-Repo und pusht — das ist das Signal.
# -E: der ERR-Trap gilt auch innerhalb von Shell-Funktionen (status_schreiben, fehler_abbruch).
# Ohne -E blieb ein Fehler dort stumm bzw. brach seit T-0120 wortlos ab: kein Status im
# Firmen-Repo, der zuletzt gemeldete Status blieb stehen und wurde weiter als aktuell gelesen.
set -Eeuo pipefail
# Aus einer Kopie laufen: git reset weiter unten überschreibt sonst das laufende Skript.
if [[ -z "${DEPLOY_KOPIE:-}" ]]; then
  KOPIE=$(mktemp /tmp/test-deploy.XXXXXX.sh); cp "$0" "$KOPIE"; export DEPLOY_KOPIE=1
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
SCHRITT="start"; COMMIT=""
set -a; source "$ENV_DATEI"; set +a

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
  python3 - "$st" "$fehler" "$zeit" "$adresse" "$COMMIT" "$PROTOKOLL" "${KAP2_TEST_BENUTZER:-}" "${KAP2_TEST_PASSWORT:-}" > "$FIRMA/betrieb/deploy-status.json.neu" <<'PY'
import json, sys
st, fehler, zeit, adresse, commit, protokoll, benutzer, passwort = sys.argv[1:9]
d = {"zeit": zeit, "status": st, "adresse": adresse, "commit": commit or None,
     "fehler": (fehler[:1500] if st == "fehler" else None), "protokoll": protokoll}
if benutzer:
    d["zugang"] = {"benutzer": benutzer, "passwort": passwort, "hinweis": "HTTP Basic Auth der Testumgebung"}
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

SCHRITT="backend-abhaengigkeiten"
[[ -x "$VENV/bin/pip" ]] || python3.12 -m venv "$VENV"
"$VENV/bin/pip" install -q --upgrade pip wheel
"$VENV/bin/pip" install -q -r backend/requirements.txt

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
"$VENV/bin/alembic" upgrade head || echo "Warnung: alembic upgrade head fehlgeschlagen — Tabellen werden beim Start per create_all angelegt"

SCHRITT="dienst"
sudo /bin/systemctl restart kap2-test
for i in $(seq 1 60); do
  if curl -sf http://127.0.0.1:8010/api/health >/dev/null; then echo "Backend gesund nach ${i}x2s"; break; fi
  if [[ $i -eq 60 ]]; then echo "Backend antwortet nicht"; false; fi
  sleep 2
done

SCHRITT="status"
# Trap bleibt bewusst aktiv: scheitert das Schreiben oder Pushen des Status, ist der Lauf nicht
# bestaetigt -- dann darf er nicht stumm enden und den vorherigen Status stehen lassen.
status_schreiben fertig ""
echo "== fertig: ${KAP2_TEST_URL:-} ($COMMIT)"
