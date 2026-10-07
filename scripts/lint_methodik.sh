#!/usr/bin/env bash
# Methodik-Lint in der Projektumgebung ausführen (T-1862).
#
#   bash scripts/lint_methodik.sh 95
#   bash scripts/lint_methodik.sh 98
#
# Ruft backend/scripts/lint_methodik.py mit allen übergebenen Argumenten über
# denselben Interpreter auf wie scripts/testlauf.sh
# (${KAP2_VENV:-$HOME/.venvs/kap2}/bin/python), weil die Beispiel-Blöcke der
# Berichte numpy brauchen. Fehlt der Interpreter, bricht das Skript ab; es
# fällt nicht auf das System-Python zurück.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="${KAP2_VENV:-$HOME/.venvs/kap2}"
PY="$VENV/bin/python"

if [ ! -x "$PY" ]; then
  echo "[lint_methodik] Interpreter nicht gefunden: $PY (KAP2_VENV=$VENV). Umgebung mit 'bash scripts/testlauf.sh' anlegen." >&2
  exit 2
fi

export PYTHONPATH="$REPO_ROOT/backend${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONPYCACHEPREFIX="$VENV/pycache"

cd "$REPO_ROOT"
exec "$PY" backend/scripts/lint_methodik.py "$@"
