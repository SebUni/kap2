#!/usr/bin/env bash
# Befund-Ledger in der Projektumgebung prüfen (T-1914).
#
#   bash scripts/ledger.sh 98 --pruefe
#   bash scripts/ledger.sh 95 --pruefe
#
# Ruft backend/scripts/ledger.py mit allen übergebenen Argumenten über
# denselben Interpreter auf wie scripts/lint_methodik.sh und scripts/testlauf.sh
# (${KAP2_VENV:-$HOME/.venvs/kap2}/bin/python). Fehlt der Interpreter, bricht das
# Skript ab; es fällt nicht auf das System-Python zurück. Das bin-Verzeichnis
# steht vorn in PATH, damit Prüfausdrücke, die selbst python3 aufrufen
# (etwa lint_methodik.py), denselben Interpreter nutzen.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="${KAP2_VENV:-$HOME/.venvs/kap2}"
PY="$VENV/bin/python"

if [ ! -x "$PY" ]; then
  echo "[ledger] Interpreter nicht gefunden: $PY (KAP2_VENV=$VENV). Umgebung mit 'bash scripts/testlauf.sh' anlegen." >&2
  exit 2
fi

export PATH="$VENV/bin:$PATH"
export PYTHONPATH="$REPO_ROOT/backend${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONPYCACHEPREFIX="$VENV/pycache"

cd "$REPO_ROOT"
exec "$PY" backend/scripts/ledger.py "$@"
