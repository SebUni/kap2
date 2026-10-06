#!/usr/bin/env bash
# Backend und Frontend für die Sichtprüfung des Motors starten (T-1760).
#
#   bash scripts/sichtstart.sh
#
# Aufgerufen wird das Skript von `.overlord/sichtstart` (Motor:
# skripte/sichtpruefung.py). Es nutzt die Projektumgebung außerhalb des Repos
# (${KAP2_VENV:-$HOME/.venvs/kap2}, wie scripts/testlauf.sh), startet uvicorn
# ohne --reload auf 127.0.0.1:8000 und vite auf 127.0.0.1:5173 und läuft, bis
# es beendet wird; dann beendet es beide Kindprozesse. Es legt nichts im
# Arbeitsbaum an und installiert nichts.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="${KAP2_VENV:-$HOME/.venvs/kap2}"
PY="$VENV/bin/python"
VITE="$ROOT/frontend/node_modules/.bin/vite"

if [ ! -x "$PY" ]; then
  echo "[sichtstart] Projektumgebung fehlt: $PY (anlegen mit bash scripts/testlauf.sh)" >&2
  exit 1
fi
if [ ! -x "$VITE" ]; then
  echo "[sichtstart] frontend/node_modules fehlt: $VITE (npm ci im Ordner frontend)" >&2
  exit 1
fi

BACKEND_PID=""
FRONTEND_PID=""

cleanup() {
  [ -n "$BACKEND_PID" ] && kill "$BACKEND_PID" 2>/dev/null || true
  [ -n "$FRONTEND_PID" ] && kill "$FRONTEND_PID" 2>/dev/null || true
  wait 2>/dev/null || true
}
trap cleanup EXIT INT TERM

# Bytecode-Cache außerhalb des Arbeitsbaums halten.
export PYTHONPYCACHEPREFIX="$VENV/pycache"

# Lokale Anmeldung für die Sichtprüfung (T-1771): das Backend behandelt Anfragen
# von 127.0.0.1 ohne Login-Cookie als Admin „Sichtprüfung (lokal)“. Nur dieses
# Skript setzt die Variable; in Umgebungsdateien der Testumgebung oder der
# Produktion darf sie nie stehen (docs/BETRIEB.md, Abschnitt „Sichtprüfung“).
export KAP2_SICHTSTART_ANMELDUNG=1

(
  cd "$ROOT/backend"
  exec "$PY" -m uvicorn app.main:app --host 127.0.0.1 --port 8000
) &
BACKEND_PID=$!

(
  cd "$ROOT/frontend"
  exec "$VITE" --host 127.0.0.1 --port 5173 --strictPort
) &
FRONTEND_PID=$!

# Endet einer der beiden Prozesse, endet das Skript mit seinem Status.
wait -n
