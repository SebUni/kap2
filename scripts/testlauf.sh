#!/usr/bin/env bash
# Backend-Tests in einer eigenen Python-Umgebung ausführen (T-0500).
#
#   bash scripts/testlauf.sh backend/tests/test_planned_risks.py -q
#   bash scripts/testlauf.sh                # alle Tests unter backend/tests
#
# Die Umgebung liegt außerhalb des Repos unter ${KAP2_VENV:-$HOME/.venvs/kap2}
# und wird beim ersten Lauf angelegt; danach wird nur noch nachinstalliert,
# wenn sich backend/requirements.txt geändert hat. Das Skript legt nichts
# innerhalb des Arbeitsbaums an: Bytecode-Cache und pytest-Cache liegen
# ebenfalls in der Umgebung (`git status` bleibt nach dem Lauf sauber).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="${KAP2_VENV:-$HOME/.venvs/kap2}"
REQ="$REPO_ROOT/backend/requirements.txt"
PY="$VENV/bin/python"

if [ ! -x "$PY" ]; then
  echo "[testlauf] Lege Python-Umgebung an: $VENV"
  mkdir -p "$(dirname "$VENV")"
  python3 -m venv "$VENV"
fi

# Nachinstallieren nur bei geänderten Anforderungen (Stempel = Prüfsumme).
STEMPEL="$VENV/.kap2-requirements.sha256"
SOLL="$(sha256sum "$REQ" | cut -d' ' -f1)"
IST="$(cat "$STEMPEL" 2>/dev/null || true)"
if [ "$SOLL" != "$IST" ]; then
  echo "[testlauf] Installiere Abhängigkeiten aus backend/requirements.txt"
  "$PY" -m pip install --quiet --upgrade pip
  "$PY" -m pip install --quiet -r "$REQ"
  "$PY" -m pip install --quiet pytest
  echo "$SOLL" >"$STEMPEL"
fi

# backend/ auf den Importpfad legen: Die Testmodule importieren teils direkt
# `app...` (erwarten also backend/ als Arbeitsverzeichnis), teils setzen sie den
# Pfad selbst. Über PYTHONPATH laufen beide Sorten unabhängig davon, aus welchem
# Verzeichnis das Skript aufgerufen wird.
export PYTHONPATH="$REPO_ROOT/backend${PYTHONPATH:+:$PYTHONPATH}"

# Caches außerhalb des Repos halten.
export PYTHONPYCACHEPREFIX="$VENV/pycache"
PYTEST_CACHE="$VENV/pytest_cache"

if [ "$#" -eq 0 ]; then
  set -- backend/tests
fi

cd "$REPO_ROOT"
exec "$PY" -m pytest -o "cache_dir=$PYTEST_CACHE" "$@"
