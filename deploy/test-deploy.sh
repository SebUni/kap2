#!/usr/bin/env bash
# Test-Deployment von kap2 auf dem Server. Läuft als Benutzer overlord, gestartet vom Watcher
# (Signal deploy_anforderung) oder von Hand: /opt/overlord/kap2/deploy/test-deploy.sh [main|<commit>]
# Am Ende schreibt es betrieb/deploy-status.json ins Firmen-Repo und pusht — das ist das Signal.
set -uo pipefail
# Aus einer Kopie laufen: git reset weiter unten überschreibt sonst das laufende Skript.
if [[ -z "${DEPLOY_KOPIE:-}" ]]; then
  KOPIE=$(mktemp /tmp/test-deploy.XXXXXX.sh); cp "$0" "$KOPIE"; export DEPLOY_KOPIE=1
  bash "$KOPIE" "$@"; RC=$?; rm -f "$KOPIE"; exit $RC
fi
REF="${1:-main}"
PRODUKT=/opt/overlord/kap2
FIRMA=/opt/overlord/firma-deploy
VENV=/opt/overlord/kap2-venv
ENV_DATEI=/etc/overlord/kap2-test.env
PROTOKOLL=/var/log/overlord/deploy.log
SCHRITT="start"; COMMIT=""
set -a; source "$ENV_DATEI"; set +a

status_schreiben() {  # $1 = fertig|fehler, $2 = Fehlertext
  local st="$1" fehler="$2" zeit adresse
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
  for versuch in 1 2 3 4 5; do
    git -C "$FIRMA" fetch -q origin && git -C "$FIRMA" reset -q --hard origin/main
    mv "$FIRMA/betrieb/deploy-status.json.neu" "$FIRMA/betrieb/deploy-status.json" 2>/dev/null || cp "$FIRMA/betrieb/deploy-status.json.neu" "$FIRMA/betrieb/deploy-status.json"
    git -C "$FIRMA" add betrieb/deploy-status.json
    git -C "$FIRMA" commit -q -m "Deploy-Status: $st ($COMMIT)" || true
    git -C "$FIRMA" push -q origin main:main && break
    sleep $((versuch * 3))
  done
  rm -f "$FIRMA/betrieb/deploy-status.json.neu"
}
fehler_abbruch() {
  local zeilen; zeilen=$(tail -n 25 "$PROTOKOLL" 2>/dev/null | tr -d '\r')
  echo "!! Fehler im Schritt $SCHRITT"
  status_schreiben fehler "Schritt $SCHRITT fehlgeschlagen. Letzte Protokollzeilen:
$zeilen"
  exit 1
}
trap fehler_abbruch ERR

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
npm ci --legacy-peer-deps --no-audit --no-fund --loglevel=error
npm run build --silent

SCHRITT="datenbank"
cd "$PRODUKT/backend"
mkdir -p logs
"$VENV/bin/alembic" upgrade head || echo "Warnung: alembic upgrade head fehlgeschlagen — Tabellen werden beim Start per create_all angelegt"

SCHRITT="dienst"
sudo /bin/systemctl restart kap2-test
for i in $(seq 1 60); do
  if curl -sf http://127.0.0.1:8010/api/health >/dev/null; then echo "Backend gesund nach ${i}x2s"; break; fi
  [[ $i -eq 60 ]] && { echo "Backend antwortet nicht"; false; }
  sleep 2
done

SCHRITT="status"
trap - ERR
status_schreiben fertig ""
echo "== fertig: ${KAP2_TEST_URL:-} ($COMMIT)"
