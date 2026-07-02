#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"

if [[ -f "$ROOT/../.venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source "$ROOT/../.venv/bin/activate"
fi

cd "$ROOT"
exec python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 \
  >>"$LOG_DIR/stdout.log" 2>>"$LOG_DIR/stderr.log"
