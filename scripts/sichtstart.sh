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
# Arbeitsbaum an und installiert nichts. Die Datenbank ist eine eigene
# Postgres-Instanz unter ${KAP2_SICHT_PGDATA:-$HOME/.local/share/kap2-sicht/pgdata}
# (nur Socket, ohne Passwort; siehe unten).
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

# Eigene Postgres-Instanz für die Sichtprüfung (T-1774): Datenverzeichnis
# außerhalb des Arbeitsbaums, nur über den Unix-Socket im Datenverzeichnis
# erreichbar (kein TCP), Zugriff `trust` ohne Passwort. Der System-Cluster auf
# localhost:5432 wird weder genutzt noch verändert.
PGDATA="${KAP2_SICHT_PGDATA:-$HOME/.local/share/kap2-sicht/pgdata}"
PGSOCK="$PGDATA"
PGUSER_SICHT="$(id -un)"
PGDB="kap2_sicht"
PG_STARTED=0

# Der Socket-Pfad (Verzeichnis + /.s.PGSQL.5432) darf unter 100 Zeichen bleiben.
if [ "${#PGSOCK}" -gt 80 ]; then
  echo "[sichtstart] Datenverzeichnis zu lang für den Socket-Pfad (${#PGSOCK} Zeichen, höchstens 80): $PGSOCK (KAP2_SICHT_PGDATA kürzer setzen)" >&2
  exit 1
fi

PG_BIN="$(pg_config --bindir)"
PG_SHARE="$(pg_config --sharedir)"
if [ ! -x "$PG_BIN/initdb" ] || [ ! -x "$PG_BIN/pg_ctl" ]; then
  echo "[sichtstart] initdb/pg_ctl fehlen unter $PG_BIN (pg_config --bindir)" >&2
  exit 1
fi
if [ ! -f "$PG_SHARE/extension/postgis.control" ]; then
  echo "[sichtstart] PostGIS fehlt (postgis.control nicht unter $PG_SHARE/extension)" >&2
  exit 1
fi

cleanup() {
  [ -n "$BACKEND_PID" ] && kill "$BACKEND_PID" 2>/dev/null || true
  [ -n "$FRONTEND_PID" ] && kill "$FRONTEND_PID" 2>/dev/null || true
  wait 2>/dev/null || true
  BACKEND_PID=""
  FRONTEND_PID=""
  # Die Instanz stoppt nur der Start, der sie gestartet hat; eine schon
  # laufende (paralleler Sichtstart) wird mitbenutzt und bleibt.
  if [ "$PG_STARTED" = 1 ]; then
    PG_STARTED=0
    "$PG_BIN/pg_ctl" -D "$PGDATA" stop -m fast >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT INT TERM

# Sperre gegen parallelen Start (T-1797): Entwickler und Prüfer können den
# Sichtstart gleichzeitig aufrufen. Wer die Sperre nicht bekommt, beendet sich
# mit Exit 1, ohne initdb, pg_ctl start oder pg_ctl stop zu berühren. Die Sperre
# hält Dateikennung 9 bis zum Ende dieses Skripts (flock gibt sie beim Beenden frei).
LOCKDIR="$HOME/.local/share/kap2-sicht"
LOCKFILE="$LOCKDIR/sichtstart.lock"
mkdir -p "$LOCKDIR"
exec 9>"$LOCKFILE"
if ! flock -n 9; then
  echo "[sichtstart] Sperre $LOCKFILE gehalten: ein anderer Sichtstart läuft; dieser Start tut nichts" >&2
  exit 1
fi

if [ ! -f "$PGDATA/PG_VERSION" ]; then
  mkdir -p "$PGDATA"
  chmod 700 "$PGDATA"
  "$PG_BIN/initdb" -D "$PGDATA" -U "$PGUSER_SICHT" -A trust -E UTF8 --no-instructions >/dev/null
fi

if ! "$PG_BIN/pg_ctl" -D "$PGDATA" status >/dev/null 2>&1; then
  # Dateikennung 9 schließen, damit der Postgres-Daemon die Sperre nicht erbt.
  "$PG_BIN/pg_ctl" -D "$PGDATA" -w -t 60 -l "$PGDATA/../postgres.log" \
    -o "-c listen_addresses='' -c unix_socket_directories='$PGSOCK'" start >/dev/null 9>&-
  PG_STARTED=1
fi

if [ "$(psql -h "$PGSOCK" -U "$PGUSER_SICHT" -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname = '$PGDB'")" != "1" ]; then
  psql -h "$PGSOCK" -U "$PGUSER_SICHT" -d postgres -v ON_ERROR_STOP=1 -qc "CREATE DATABASE $PGDB"
fi
psql -h "$PGSOCK" -U "$PGUSER_SICHT" -d "$PGDB" -v ON_ERROR_STOP=1 -qc "CREATE EXTENSION IF NOT EXISTS postgis"

# Form, die psycopg2 und SQLAlchemy annehmen; das Schema legt der Start des
# Backends selbst an (create_all).
export DATABASE_URL="postgresql://$PGUSER_SICHT@/$PGDB?host=$PGSOCK"

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
