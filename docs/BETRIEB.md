# Betrieb: RAM-Budget, Hintergrund-Prozesse, Caches

Stand: Juli 2026 (RAM-Deckel- und Precompute-Umbau). Zielbild: Der
**API-Prozess bleibt dauerhaft klein** (≲ 1,5 GB), alles Schwere läuft in
kurzlebigen Kind-Prozessen, deren Speicher mit dem Exit vollständig ans
Betriebssystem zurückgeht. Dashboard- und Karten-Payloads werden im Hintergrund
als gzip-Dateien vorgebaut und nur noch von Platte gestreamt — der RAM-Bedarf
des Servers ist damit unabhängig von der Zahl der Nutzer und Kommunen.

## Prozessmodell

| Prozess | Startet wann | RAM-Verhalten |
|---|---|---|
| uvicorn (API) | `start-dev.sh` / manuell | dauerhaft klein; hält keine Geodaten |
| `app.tasks.assessment_worker <kommune_id>` | „Berechnen"-Klick (über Warteschlange) | schwer (OSM/Terrain/Fork-Worker), **PSS-Watchdog-Limit**, Exit = RAM frei |
| `app.services.artifact_rebuild <kommune_id>` | nach Mutationen (Maßnahmen/Parameter/Config), entprellt ~3 s | mittel (lädt Zell-Blobs), seriell, Exit = RAM frei |

- **Warteschlange:** höchstens `ASSESSMENT_MAX_CONCURRENT` (Default 1)
  Assessments gleichzeitig; weitere Kommunen stehen als `queued` an (FIFO,
  Status-Panel zeigt die Position). Abbruch geht auch für eingereihte Läufe.
- **Liveness:** Wahrheit liegt in der DB (`project_statuses.worker_pid` +
  `worker_start_ticks` gegen PID-Reuse). Ein uvicorn-Reload/-Neustart tötet
  laufende Berechnungen **nicht** — das verwaiste Kind rechnet weiter und
  schreibt Fortschritt/Ergebnis in DB und Cache-Dateien.
- **Abbruch:** DB-Flag `abort_requested` (Kind prüft es bei jedem
  Fortschritts-Commit) + SIGTERM; reagiert das Kind 30 s nicht, killt der
  Scheduler die ganze Prozessgruppe.
- **RAM-Watchdog:** misst alle `ASSESSMENT_WATCHDOG_INTERVAL_S` Sekunden das
  **PSS** des Kind-Prozessbaums (`/proc/*/smaps_rollup`; PSS statt RSS, weil
  Fork-Worker Copy-on-Write-Seiten teilen). Über `ASSESSMENT_MAX_RSS_MB`:
  sanfter Abbruch mit klarer Meldung; hängt der Prozess, nach 30 s SIGKILL.

## Env-Konfiguration (backend/.env)

| Variable | Default | 16-GB-Laptop (dev) | 24-GB-Server (Strato XXL) |
|---|---|---|---|
| `ASSESSMENT_WORKERS` | `0` = auto → min(4, CPU) | 0 | `6` |
| `ASSESSMENT_MAX_CONCURRENT` | `1` | 1 | 1 (2 nur mit viel Luft) |
| `ASSESSMENT_MAX_RSS_MB` | `5000` | 5000 | `9000` |
| `ASSESSMENT_WATCHDOG_INTERVAL_S` | `3.0` | — | — |
| `ASSESSMENT_RLIMIT_AS_MB` | `0` (aus) | aus lassen | aus lassen (Not-Backstop; begrenzt virtuellen Adressraum, der bei numpy/GEOS weit über RSS liegt) |
| `OSM_CACHE_DIR` / `OSM_CACHE_TTL_S` | `data/osm_cache` / 30 d | — | — |
| `TERRAIN_TILE_CACHE_DIR` / `TERRAIN_TILE_CACHE_TTL_S` | `data/terrain_tiles` / 1 Jahr | — | — |

Faustformel Gesamtbudget: API (~0,5–1,5 GB) + `ASSESSMENT_MAX_CONCURRENT ×
ASSESSMENT_MAX_RSS_MB` + Postgres. Mit den Defaults bleibt eine 16-GB-Maschine
auch während eines Leipzig-Laufs komfortabel nutzbar.

## Cache-/Artefakt-Verzeichnisse

| Pfad | Inhalt | Invalidierung |
|---|---|---|
| `backend/.cache/layers/<id>/` | Karten-Geometrie + Layer-Werte (gzip) | Assessment-Ende, Live-Parameter (€/ref_value), `MODEL_VERSION`, Reset/Grid |
| `backend/.cache/aggregates/<id>/` | Risiko-Aggregat Basis/mit Maßnahmen | jede Mutation (Maßnahmen nur „mit Maßnahmen"-Variante), `MODEL_VERSION` |
| `backend/.cache/dashboard/<id>/` | risk_summary, cost_summary, risk_histogram, cost_projection, profile (+ `.fp`-Fingerprints) | **Fingerprint-basiert** (Zellen-Stand, Maßnahmen, Parameter, Stammdaten; profile/cost_projection zusätzlich wöchentlich) |
| `backend/data/osm_cache/` | Overpass-Roh-JSON je bbox | TTL 30 d |
| `backend/data/terrain_tiles/` | DEM-Kacheln (PNG) | TTL 1 Jahr |

Alle Verzeichnisse sind gefahrlos löschbar (Lazy-Rebuild beim nächsten Zugriff
bzw. Hintergrund-Rebuild). Die Endpoints liefern `ETag` und beantworten
`If-None-Match` mit **304** (kein Body-Transfer bei unverändertem Stand).

## Wann wird was neu gerechnet?

| Ereignis | Automatisch neu gebaut | Voll-Neuberechnung (Zellen) |
|---|---|---|
| Maßnahme anlegen/ändern/löschen | Aggregat (mit Maßnahmen), Dashboard-Artefakte | nein |
| `calculate-impact` | nur wenn Ergebnis sich änderte | nein |
| Live-Parameter (`*.cost_per_outcome`, `*.ref_value`, Modell-Stellschrauben) | Aggregate, Dashboard, **Karten-Layer-Dateien** | nein |
| Rechenrelevante Parameter (Normgrenzen, Impact-/UHI-/Regional-Parameter) | Aggregate/Dashboard (Werte ändern sich erst nach Lauf) | **manuell** — Banner „Neu berechnen" |
| Config-Änderung (UHI etc.) | Aggregate, Dashboard | ggf. manuell |
| Zensus-Sync mit tatsächlich neuen Daten | nichts (Zellwerte basieren auf altem Stand) | **manuell** — `recalc_recommended`-Hinweis im Status |
| Bundesland/Landkreis-Backfill (Nominatim) | Aggregate, Dashboard | nein |
| Assessment abgeschlossen | alles (Layer + Dashboard, noch im Kind-Prozess) | — |
| `MODEL_VERSION`-Bump (Code) | alles, lazy beim ersten Zugriff | empfohlen |

## Verifikations-Rezepte

**API-Prozess bleibt flach (auch während eines Laufs):**

```bash
API=$(pgrep -f "uvicorn app.main:app" | head -1)
while sleep 2; do ps -o rss= -p "$API" | awk '{printf "%d MB\n", $1/1024}'; done
```

**Peak des Assessment-Kind-Prozessbaums:**

```bash
ROOT=$(pgrep -f "app.tasks.assessment_worker" | head -1); peak=0
while kill -0 "$ROOT" 2>/dev/null; do
  cur=$(../.venv/bin/python -c "from app.tasks.memory_watchdog import process_tree_pss_mb; print(int(process_tree_pss_mb($ROOT)))")
  [ "$cur" -gt "$peak" ] && peak=$cur; sleep 2
done; echo "Peak Baum-PSS: $peak MB"
```

(PSS über die Watchdog-Funktion selbst — ein RSS-Summenskript über `ps` zählt
Copy-on-Write-geteilte Fork-Seiten je Worker mehrfach und überschätzt grob;
Achtung bei awk-Baum-Skripten: ``if (arr[x])`` legt leere Einträge an,
``if (x in arr)`` nicht.)
Nach Lauf-Ende: `pgrep -f assessment_worker` leer → RAM vollständig zurück.
Zweiter Lauf derselben Kommune: Log (`backend/logs/worker-<id>.log`) zeigt
`Overpass-Disk-Cache HIT`, keine Downloads.

**Dashboard-Latenz + 304:**

```bash
for e in risk-summary cost-summary risk-histogram cost-projection profile; do
  curl -so /dev/null -w "$e  %{time_total}s  %{size_download}B\n" \
    "http://localhost:8000/api/kommune/2/$e"
done
# Achtung: GET verwenden (HEAD liefert 405 — FastAPI registriert kein Auto-HEAD)
ET=$(curl -s -D - -o /dev/null http://localhost:8000/api/kommune/2/risk-summary \
  | awk -F': ' 'tolower($1)=="etag"{print $2}' | tr -d '\r')
curl -s -o /dev/null -w "%{http_code}\n" -H "If-None-Match: $ET" \
  "http://localhost:8000/api/kommune/2/risk-summary"   # → 304
```

## Migration / Upgrade

```bash
cd backend && ../.venv/bin/alembic upgrade head
```

(Neue Spalten an `project_statuses` + Enum-Wert `QUEUED`; der Server-Start
legt beides über den `create_all`-Guard auch selbst an.) Logs der
Kind-Prozesse: `backend/logs/worker-<kommune_id>.log` und
`backend/logs/artifact-rebuild.log`.

## Grenzen (bewusst so gelassen)

- Ein uvicorn-Worker; Multi-Worker bräuchte DB-basierte Queue-Slots
  (`SELECT … FOR UPDATE SKIP LOCKED`) statt des In-Prozess-Schedulers.
- Der Debounce-Zeitplan lebt im API-Prozess: Ein Reload verwirft nur den
  Zeitplan, nie die Korrektheit (Serving-Pfade bauen bei Miss/Stale lazy nach).
- Der Geodaten-Export (GeoPackage) läuft weiterhin als Thread im API-Prozess,
  liest aber gestreamt (`yield_per`) und streamt den Download von Platte.
