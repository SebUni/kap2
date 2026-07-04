#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_LOG_DIR="$ROOT/backend/logs"
mkdir -p "$BACKEND_LOG_DIR"

if [[ -x "$ROOT/.venv/bin/python3" ]]; then
  PYTHON="$ROOT/.venv/bin/python3"
elif [[ -f "$ROOT/.venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source "$ROOT/.venv/bin/activate"
  PYTHON="python3"
else
  PYTHON="python3"
  echo "Warnung: .venv nicht gefunden, nutze $(command -v python3)"
fi

BACKEND_PID=""
FRONTEND_PID=""

cleanup() {
  echo ""
  echo "Beende Prozesse …"
  [[ -n "$BACKEND_PID" ]] && kill "$BACKEND_PID" 2>/dev/null || true
  [[ -n "$FRONTEND_PID" ]] && kill "$FRONTEND_PID" 2>/dev/null || true
  wait 2>/dev/null || true
}
trap cleanup EXIT INT TERM

show_backend_error() {
  echo ""
  echo "Backend konnte nicht starten. Letzte Einträge aus backend/logs/stderr.log:"
  echo "────────────────────────────────────────────────────────────────────"
  tail -25 "$BACKEND_LOG_DIR/stderr.log" 2>/dev/null || echo "(keine stderr.log)"
  echo "────────────────────────────────────────────────────────────────────"
}

wait_for_backend() {
  local attempt
  for attempt in $(seq 1 30); do
    if curl -sf "http://127.0.0.1:8000/api/health" >/dev/null 2>&1; then
      return 0
    fi
    if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
      show_backend_error
      return 1
    fi
    sleep 0.5
  done
  show_backend_error
  return 1
}

echo "Starte Backend (http://0.0.0.0:8000) – Logs: backend/logs/"
(
  cd "$ROOT/backend"
  exec "$PYTHON" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
) >>"$BACKEND_LOG_DIR/stdout.log" 2>>"$BACKEND_LOG_DIR/stderr.log" &
BACKEND_PID=$!

if ! wait_for_backend; then
  exit 1
fi
echo "Backend bereit."

echo "Starte Frontend (http://0.0.0.0:5173)"
(
  cd "$ROOT/frontend"
  exec ./node_modules/.bin/vite --host 0.0.0.0 --port 5173
) &
FRONTEND_PID=$!

echo ""
echo "KAP2 Dev-Server läuft. Strg+C zum Beenden."
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:5173"
echo "  Logs:     backend/logs/"

wait
