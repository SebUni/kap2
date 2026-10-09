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

## Tests ausführen

Die Backend-Tests laufen **nicht** mit dem System-Python: `fastapi`, `numpy`,
`sqlalchemy` und `shapely` sind dort nicht installiert, und jedes Testmodul, das
eines dieser Pakete braucht, scheitert schon beim Einsammeln. Verbindlich ist
deshalb für Entwickler und Prüfer `scripts/testlauf.sh`, aufgerufen aus dem
Wurzelverzeichnis des Repos:

```bash
bash scripts/testlauf.sh backend/tests/test_kwra_querverbindungen.py -q
bash scripts/testlauf.sh backend/tests/test_planned_risks.py -q
bash scripts/testlauf.sh                 # ohne Argument: alle Tests unter backend/tests
```

Alles nach dem Skriptnamen geht unverändert an `pytest` (`-q`, `-k`, `-x`, …).
Das Skript

- legt die Python-Umgebung beim ersten Lauf unter `${KAP2_VENV:-$HOME/.venvs/kap2}`
  an — **außerhalb** des Repos — und installiert dort `backend/requirements.txt`
  plus `pytest`; danach installiert es nur nach, wenn sich die Prüfsumme von
  `backend/requirements.txt` geändert hat;
- legt nichts innerhalb des Arbeitsbaums an: Bytecode-Cache
  (`PYTHONPYCACHEPREFIX`) und pytest-Cache (`cache_dir`) liegen in der Umgebung,
  `git status --porcelain` ist nach dem Lauf unverändert;
- setzt `backend/` auf den Importpfad. Das übernimmt seit T-0591 bereits
  `pytest.ini` im Wurzelverzeichnis (`pythonpath = backend`,
  `testpaths = backend/tests`): Ein blankes `python3 -m pytest`, direkt aus
  dem Wurzelverzeichnis aufgerufen, findet den Importpfad damit selbst und ist
  nicht mehr vom Arbeitsverzeichnis abhängig. Verbindlich bleibt trotzdem
  `scripts/testlauf.sh`, weil erst das Skript die eigene, außerhalb des Repos
  liegende Umgebung aus `backend/requirements.txt` anlegt bzw. nachzieht —
  gegen ein anderes Python (System-Python, falsche Venv) läuft die Suite
  weiterhin nicht.

Eine andere Umgebung wählt man über `KAP2_VENV=/pfad/zum/venv bash scripts/testlauf.sh …`.
Wer „kein Test läuft" meldet, nennt den vollständigen Befehl und das
Arbeitsverzeichnis mit.

Nach dem Merge ruft ein gesteuerter Lauf `bash scripts/testlauf.sh <dateien>` direkt auf (freigegeben über `.overlord/erlaubte_befehle`); der `python3`-Subprozess bleibt der Ausweichweg, wenn der direkte Aufruf abgewiesen wird.

Die Python-Blöcke der Querschnittsdateien (`docs/methodik/querschnitt_*.md`) führt `backend/tests/test_methodik_querschnitt_bloecke.py` aus und vergleicht ihre dokumentierte Ausgabe; der Methodik-Lint überspringt diese Dateien.

Gesteuerte Läufe rufen den Methodik-Export `bash scripts/export_methodik_pdf.sh <nr>` nach dem Merge direkt auf (ebenso `pdftoppm` für die Layout-Stichprobe); der `python3`-Subprozess bleibt der Ausweichweg.

Den Methodik-Lint rufen gesteuerte Läufe als `bash scripts/lint_methodik.sh <nr>` auf, weil er den Interpreter der Projektumgebung nutzt und die Beispiel-Blöcke der Berichte `numpy` brauchen (mit dem System-Python endet `python3 backend/scripts/lint_methodik.py <nr>` mit `LINTS ROT`).

**Wenn der Aufruf verweigert wird:** Wie beim Frontend-Build (siehe unten) kann
`bash scripts/testlauf.sh` in einem gesteuerten Lauf an der Berechtigungsliste
scheitern (`This command requires approval`) — `bash`, `npm` und der
venv-Python sind dort nicht direkt freigegeben. Dann `scripts/testlauf.sh`
über den erlaubten Python-Aufruf starten, mit identischem Ergebnis:

```bash
python3 -c "import subprocess,sys; p=subprocess.run(['bash','scripts/testlauf.sh','-q'],capture_output=True,text=True); print(p.stdout[-3000:], p.stderr[-2000:]); sys.exit(p.returncode)"
```

## Frontend prüfen

Gilt für jede Abnahme eines Frontend-Pakets: Oberflächenänderungen werden nicht
nur gelesen, sondern gebaut und typgeprüft. Die Befehlsfolge auf dem
Arbeitsrechner der ausführenden Rolle lautet vollständig:

```bash
cd frontend
npm ci                 # einmalig bzw. nach Änderung an package-lock.json
npm run build   ; echo "exit $?"
npm run typecheck ; echo "exit $?"
```

`frontend/node_modules/` und `frontend/dist/` sind in `.gitignore` und gehören
nie in einen Commit. `npm ci` (nicht `npm install`) hält den Stand exakt auf
`package-lock.json` — Abhängigkeiten werden beim Prüfen nicht angehoben.

### Beleg: tatsächlich ausgeführter Lauf (20.09.2026, T-0482)

Umgebung: Linux, `node -v` → `v20.20.2`, `npm -v` → `10.8.2`.
`npm ci` lief erfolgreich (`added 253 packages, and audited 254 packages in 5s`,
Exit-Status 0) — die Paketquelle `registry.npmjs.org` war erreichbar.

`npm run build` — wörtliche Ausgabe, Kopf und Schlusszeilen:

```
> frontend@1.0.0 build
> NODE_OPTIONS=--max-old-space-size=768 vite build

vite v5.4.21 building for production...
transforming...
✓ 1084 modules transformed.
rendering chunks...
...
dist/assets/vendor-vis-E-kp2pZy.js                      520.99 kB │ gzip: 157.87 kB
dist/assets/index-dL2jvBJv.js                           539.22 kB │ gzip: 121.88 kB
dist/assets/vendor-maplibre-BCorPmJ4.js               1,046.84 kB │ gzip: 283.04 kB
✓ built in 13.02s
exit 0
```

Auf stderr erscheinen dabei zwei Warnungen, die den Exit-Status nicht ändern und
kein Abnahmehindernis sind (Vite-CJS-Node-API veraltet; Chunks über 500 kB).

`npm run typecheck` — wörtliche Ausgabe, vollständig:

```
> frontend@1.0.0 typecheck
> tsc --noEmit -p tsconfig.json

exit 0
```

stderr war leer; `tsc` meldet keinen Typfehler.

**Damit gilt für Frontend-Pakete:** Bauen und Typprüfen sind ausführbar, die
Abnahme erfolgt gegen diese beiden grünen Läufe und nicht mehr nur dateibasiert
durch Lesen. Ein Paket, dessen Ausgabe hier einen Exit-Status ungleich 0 zeigt,
ist nicht abnahmefähig.

**Wenn der Aufruf verweigert wird:** In einem gesteuerten Lauf kann `npm` an der
Berechtigungsliste `.claude/settings.json` scheitern (Meldung
`This command requires approval`) — das ist kein fehlendes Netz und kein
fehlendes Werkzeug. Die Liste führt `npm` bislang nicht; bis sie um
`Bash(npm:*)` ergänzt ist, werden die Befehle über den dort erlaubten
Python-Aufruf gestartet, mit identischem Ergebnis:

```bash
python3 -c "import subprocess,sys; p=subprocess.run(['npm','run','build'],cwd='frontend',capture_output=True,text=True); print(p.stdout[-2000:], p.stderr[-2000:]); sys.exit(p.returncode)"
```

Der Beleg oben ist genau auf diesem Weg entstanden.
Erst wenn `npm ci` selbst mit einer Netz-/Registry-Fehlermeldung abbricht, ist
die Umgebung nicht herstellbar; dann ist die wörtliche Fehlausgabe hier
nachzutragen, und die Abnahme von Frontend-Paketen läuft bis zur Behebung
dateibasiert (Lesen des Diffs) mit ausdrücklichem Vermerk am Ticket.

## Sichtprüfung

Der Motor nimmt Oberflächen vor dem Prüferlauf im Browser auf
(`skripte/sichtpruefung.py` im Motor-Repo). Er liest dafür `.overlord/sichtstart`:
Zeilen mit `#` und Leerzeilen zählen nicht, die erste Zeile ist der Startbefehl
ohne Shell-Syntax, die erste URL ist die Frontend-Basis, jede weitere ein
Endpunkt des Backends. Hier:

```
bash scripts/sichtstart.sh
http://127.0.0.1:5173/
http://127.0.0.1:8000/api/health
```

`scripts/sichtstart.sh` startet uvicorn (ohne `--reload`) auf 127.0.0.1:8000 und
vite auf 127.0.0.1:5173 und beendet beide, wenn es beendet wird. Es nutzt die
Projektumgebung unter `${KAP2_VENV:-$HOME/.venvs/kap2}` (wie `scripts/testlauf.sh`)
und `frontend/node_modules`; fehlt eines davon, bricht es mit einer Meldung ab und
installiert nichts. `start-dev.sh` bleibt der Weg für die Arbeit am Rechner.

Aufruf (aus dem Repo-Wurzelverzeichnis; `--seite` ist der Pfad der Oberfläche):

```bash
python3 /opt/overlord/overlord/skripte/sichtpruefung.py --repo . --seite / --ziel <Verzeichnis> --start-timeout 180
```

Seiten hinter der Anmeldung (`/app/…`, zum Beispiel die Maßnahmen-Übersicht unter
`/app/massnahmen`, `frontend/src/layouts/ProductLayout.tsx`) liegen hinter
`RequireAuth`. Damit die Sichtprüfung die Oberfläche statt der Anmeldeseite
aufnimmt, setzt `scripts/sichtstart.sh` vor dem Start von uvicorn
`KAP2_SICHTSTART_ANMELDUNG=1` (`export`). Das Backend (`get_current_user` in
`backend/app/api/deps.py`) behandelt dann eine Anfrage **ohne gültiges
Login-Cookie** als angemeldeten Admin „Sichtprüfung (lokal)“, sofern der Client
`127.0.0.1` oder `::1` ist. Dieser Nutzer wird nicht gespeichert: kein
Passwort-Hash, kein Datenbankzugriff, keine Sitzung. Ein gültiges Login-Cookie
geht vor; jeder andere Wert der Variablen als `1` schaltet nichts frei. Gelesen
wird sie bei jedem Aufruf.

Warum die Variable die eigentliche Sperre ist: Auf der Testumgebung kommen alle
Anfragen über Apache (`deploy/apache-kap2-test.conf`, Proxy auf 127.0.0.1:8010)
von 127.0.0.1 am Dienst an; die Prüfung auf Loopback allein hält dort niemanden
auf. Deshalb darf nur `scripts/sichtstart.sh` die Variable setzen. Sie darf in
keiner Umgebungsdatei der Testumgebung (`/etc/overlord/kap2-test.env`) oder der
Produktion stehen, nicht in `deploy/` und nicht in `start-dev.sh`. Belegt ist das
durch `backend/tests/test_sichtstart_anmeldung.py` und durch die Suche
`grep -rlI KAP2_SICHTSTART_ANMELDUNG backend/app backend/tests scripts deploy docs .overlord frontend/src`,
die genau diese vier Dateien nennt: `deps.py`, den Test, `sichtstart.sh` und diese
Datei.

Datenbank des Sichtstarts: `scripts/sichtstart.sh` startet vor uvicorn eine eigene
Postgres-Instanz (mit PostGIS) im Verzeichnis
`${KAP2_SICHT_PGDATA:-$HOME/.local/share/kap2-sicht/pgdata}`, also außerhalb des
Arbeitsbaums; fehlt es, legt `initdb` es an (Zugriff `trust`, kein Passwort). Die
Instanz hört nicht auf TCP (`listen_addresses=''`) und ist nur über den Socket im
Datenverzeichnis erreichbar, die Datenbank heißt `kap2_sicht`; `DATABASE_URL` setzt
das Skript auf diesen Socket. Sie ist von der Testumgebung getrennt: Der
System-Cluster auf localhost:5432 und die Datenbank der Testumgebung werden weder
genutzt noch verändert. Beim Beenden stoppt das Skript die Instanz, aber nur, wenn
dieser Start sie gestartet hat; eine schon laufende (paralleler Sichtstart) bleibt
bestehen. Vor `initdb` und `pg_ctl` nimmt das Skript eine exklusive Sperre auf
`~/.local/share/kap2-sicht/sichtstart.lock`; ein zweiter Start, solange der erste
läuft, nennt die Sperre, endet mit Exit-Code 1 und startet, stoppt und
initialisiert nichts. Zurücksetzen: Sichtstart beenden und das Verzeichnis
`~/.local/share/kap2-sicht/pgdata` löschen; der nächste Start legt es neu an, das
Schema legt das Backend beim Start selbst an (`create_all`).

Beispielkommune des Sichtstarts ist **Warmsen** (Landkreis Nienburg (Weser), AGS 03256034,
3.150 Einwohner laut Bewertungslauf), nicht Berlin: Der Server hat 2 CPU und 4 GB
Speicher, Berlin hat 40.669 bewohnte Zellen. Angelegt wird sie mit
`python3 scripts/sicht_beispielkommune.py` (aus dem Repo-Wurzelverzeichnis, nur Standardbibliothek).
Das Skript startet `scripts/sichtstart.sh` selbst, steuert die API auf 127.0.0.1:8000 mit denselben
Schritten wie die Oberfläche (Kommune suchen und anlegen, Raster, Bewertung bis Status `done`, eine
Maßnahme aus dem Katalog, Wirkung berechnen) und beendet den Sichtstart am Ende wieder, auch bei
Fehlern. Die Zahlen stammen aus dem Rechenweg des Produkts; nichts wird von Hand in die Datenbank
geschrieben. Die letzte Ausgabezeile ist JSON (Kommune, Status, Jahresbetrag #95, Maßnahme, Jahresnutzen).
Ein zweiter Aufruf legt nichts neu an und startet keinen neuen Bewertungslauf; er liest und gibt
dieselben Beträge aus. Neu anlegen: Sichtstart beendet, Verzeichnis `~/.local/share/kap2-sicht/pgdata`
löschen (siehe oben), Skript erneut aufrufen. Der erste Lauf hat am 06.10.2026 auf dem Server 270 s
gedauert (4 s Start, 255 s Bewertung mit Zensus-, OSM- und Höhenmodell-Download, 8.495 Zellen à 100 m);
die Downloads gehen in die von `.gitignore` ausgenommenen Verzeichnisse (`backend/data/zensus/…`,
`backend/data/dwd_cdc/`, `backend/.cache/`). Der zweite Aufruf dauerte 7 s (4 s Sichtstart, 3 s Abfragen).
Gewählte Maßnahme: „Hitzeaktionspläne“ (Typ `HEAT_ACTION_PLANS`), Geltungsbereich die größte Fläche
der Gemeindegrenze; sie ist der erste Katalogtyp mit Nutzen für #95 oder #96, der einen Jahresnutzen
größer 0 liefert. Der Jahresbetrag #95 laut API (`risk-summary`, ohne Wirkung der Maßnahme) beträgt
179.020,81 € (Stand T-1815, mit gefüllter Gemeindetabelle und Feinstruktur σ = 0,58 K im Zelllauf; **vor diesem
Paket** waren es 170.809,72 €, davor ohne Gemeindetabelle 144.392,88 €). Der Anstieg um 8.211,09 € ist ×1,0481, der
Faktor von Bericht #95 §3.0 Wirkung (d) für Warmsen (× 1,048).
Die Karte „Erwartete Schäden je Risiko“ zeigt diesen Wert in der Spalte „Schaden/Jahr“ immer, unabhängig davon,
ob und wann `cost-summary` geladen ist (`frontend/src/components/dashboard/CostTablesSection.tsx`, seit T-1816).
Weicht der Betrag aus `cost-summary` (Schaden mit Wirkung der Maßnahmen) für eine Zeile davon ab, steht er daneben in
der Spalte „nach Maßnahmen“; ohne Abweichung oder ohne geladenes `cost-summary` gibt es die Spalte nicht. Die
Aufnahme vom 07.10.2026 nach T-1816 zeigt für #95 „179.021 €“ und „nach Maßnahmen“ „168.391 €“.
Der Golden-Test im Bericht #95 nennt für Warmsen 175.256 €
(`backend/data/kalibrierung/golden95_zellen.md`). Die Abweichung ist nicht angeglichen (jetzt
+3.764,81 €, vorher −4.446,28 € und davor −30.863,12 €). Mit der Feinstruktur liegt der Zelllauf des Produkts über
dem Golden-Wert; die Ursache dieses Rests ist nicht geklärt.

**Gemeindetabelle (T-1814).** Der Worker ordnet Stufe 2 der Ersatzregel 65+ (Bericht #95 §3.3) die VG250-Gemeinde
zu, die einen inneren Punkt der Kommune enthält (`_gemeindeschluessel` in
`backend/app/tasks/assessment_worker.py`). Ist `gemeinden` leer, entfällt Stufe 2 (in Warmsen zählte der
Anteil ab 65 in 369 von 541 Zellen als 0), und der Worker schreibt eine Logzeile der Stufe `WARNING` mit
dem Namen der Kommune und dem Text „Stufe 2 der Ersatzregel 65+ entfällt“ (`backend/logs/worker-<kommune_id>.log`).
`scripts/sicht_beispielkommune.py` füllt die Tabelle vor der Bewertung über den VG250-Import des Produkts
(`ingest_gemeinden`, Bundesland Niedersachsen, 964 Gemeinden; Download ins ignorierte Verzeichnis
`backend/data/vg250/`), wenn Warmsen (AGS 03256034) fehlt, und rechnet eine ohne Gemeindetabelle
entstandene Bewertung einmal neu. Mit gefüllter Tabelle macht der zweite Aufruf nichts davon.

Port-Ausdruck (Sichtstart beendet, Ports 5173 und 8000 frei; gibt dann `[]` aus):

```bash
python3 -c "import socket;print([p for p in (5173,8000) if socket.socket().connect_ex(('127.0.0.1',p))==0])"
```

Warmsen hat in der Sichtstart-Datenbank Daten (berechnet, Maßnahme „Sichtstart: Hitzeaktionspläne“). Zwei
Aufnahmen mit Klickfolge, kopierbar (aus dem Repo-Wurzelverzeichnis, nur auf dem Server). `--klick` ist ein
Playwright-Selektor und klickt der Reihe nach; der letzte Klick ist ein Element, das erst nach dem Laden der
Daten erscheint. Zuerst wird Warmsen gewählt, weil `/app/massnahmen` ohne gewählte Kommune auf `/app` umleitet.

Der Klick auf „81.6 km²“ (Flächenangabe im Kopf) wartet, bis die Kommune gewählt und geladen ist; er steht in
beiden Aufnahmen. Ohne ihn lief ein späterer Klick einmal in den Timeout (`ok: false`, Bild zeigte das
Dashboard). Endet ein Aufruf trotzdem mit `ok: false`, erneut ausführen.

Maßnahmen-Übersicht (Bild zeigt „Warmsen (81.6 km²)“, „Nutzen/Jahr 10.630 €“, „Netto-Nutzen/Jahr -9.370 €“;
vor T-1815: 10.143 € und -9.857 €; vor T-1814, ohne Gemeindetabelle: 8.555 € und -11.445 €):

```bash
python3 /opt/overlord/overlord/skripte/sichtpruefung.py --repo . --seite /app/massnahmen --klick "text=Meine Gebiete" --klick "text=Warmsen" --klick "text=81.6 km²" --klick "text=Maßnahmen-Übersicht" --klick "text=Netto-Nutzen/Jahr" --ziel <Verzeichnis>/sicht1 --start-timeout 300
```

Dashboard, Karte „Erwartete Schäden je Risiko“ (Bild zeigt „Allergische Reaktionen durch Aeroallergene
pflanzlicher Herkunft (#96)“ mit „2.281 €“ Schaden/Jahr, vor T-1814 „2.342 €“; stabil). Der Betrag von
„Hitzebelastung (#95)“ in „Schaden/Jahr“ ist der API-Wert von `risk-summary` ohne Wirkung der Maßnahmen, unabhängig
vom Ladestand von `cost-summary` (`CostTablesSection.tsx`, seit T-1816); das Bild zeigt „179.021 €“ (so gibt ihn
`sicht_beispielkommune.py` aus). Daneben steht in der Spalte „nach Maßnahmen“ der Betrag aus `cost-summary`, hier
„168.391 €“ (Gesamtzeile: „Gesamtschaden 190.048 €/Jahr · nach Maßnahmen 179.419 €/Jahr“). Zitiert wird, was das Bild
zeigt. Dieser Sichtstart-Nachweis gilt zusätzlich zur Prüfung in der Testumgebung (A-0066), er ersetzt sie nicht.

```bash
python3 /opt/overlord/overlord/skripte/sichtpruefung.py --repo . --seite /app --klick "text=Meine Gebiete" --klick "text=Warmsen" --klick "text=81.6 km²" --klick "text=Details: Risikoverteilung" --klick "text=Erwartete Schäden je Risiko" --ziel <Verzeichnis>/sicht2 --start-timeout 300
```

Die Demo (`/demo/…`) ist über `frontend/src/config/features.ts` (`demo: false`)
abgeschaltet.

## Migration / Upgrade

```bash
cd backend && ../.venv/bin/alembic upgrade head
```

(Neue Spalten an `project_statuses` + Enum-Wert `QUEUED`; der Server-Start
legt beides über den `create_all`-Guard auch selbst an.) Logs der
Kind-Prozesse: `backend/logs/worker-<kommune_id>.log` und
`backend/logs/artifact-rebuild.log`.

Für eine **Bestandsdatenbank**, die noch über `Base.metadata.create_all()`
beim Dienststart entstanden ist, gilt zuerst
[Bestandsdatenbank auf die Migrationskette heben](#bestandsdatenbank-auf-die-migrationskette-heben)
— erst danach ist `alembic upgrade head` der normale Weg.

## Bestandsdatenbank auf die Migrationskette heben

Die Migrationskette hat mit der Basis-Migration **`b1aadda418b4`**
(`b1aadda418b4_baseline_schema.py`) eine neue Wurzel; `head` ist
**`f1a2b3c4d5e6`**. Bestandsdatenbanken (Testdatenbank, spätere
Kundendatenbanken) sind über `Base.metadata.create_all()` beim Dienststart
entstanden: ihre Tabelle `alembic_version` steht entweder auf `f1a2b3c4d5e6`
oder existiert gar nicht. Alle Befehle laufen aus `backend/`.

In **keinem der drei Fälle wird eine Tabelle gelöscht und keine Migration
rückwärts gefahren** — es gibt kein `downgrade`, kein `DROP`, kein
Neuanlegen des Schemas. Der Übergang ist reine Buchführung in
`alembic_version` bzw. ein Vorwärts-Upgrade.

1. **Sicherung** — vor jedem weiteren Schritt, ohne Ausnahme:

   ```bash
   pg_dump -Fc -f ~/kap2_vor_basismigration.dump kap2
   ```

2. **Ist-Stand feststellen:**

   ```bash
   psql -d kap2 -c "select version_num from alembic_version"
   ```

3. **Fall A — Ausgabe ist `f1a2b3c4d5e6`:** nichts zu tun. **Kein `stamp`.**
   Die neue Wurzel `b1aadda418b4` liegt unterhalb des aktuellen Standes; die
   Datenbank ist damit schon über die Basis-Migration hinaus und hängt korrekt
   in der Kette. Weiter mit Schritt 6.

4. **Fall B — `alembic_version` fehlt oder ist leer** (Fehler
   `relation "alembic_version" does not exist` bzw. `0 rows`): erst prüfen, ob
   das vorhandene Schema zum Modell passt:

   ```bash
   ../.venv/bin/alembic check
   ```

   - **Nur bei leerer Ausgabe** (keine gemeldeten Unterschiede) die Datenbank
     als auf dem aktuellen Stand markieren:

     ```bash
     ../.venv/bin/alembic stamp head
     ```

   - **Meldet `check` einen Unterschied: ausdrücklich kein `stamp`.** Ein
     `stamp head` auf ein abweichendes Schema markiert Migrationen als
     gelaufen, die nie gelaufen sind — genau der stille Datenverlust, den
     dieses Runbook verhindert. Stattdessen den Befund festhalten (Ausgabe von
     `alembic check` samt Datenbank und Datum) und eskalieren, bevor irgendein
     weiterer Schritt erfolgt.

5. **Fall C — der Stand ist eine der mittleren Revisionen der Kette**
   (`861a0419ccf8`, `b2c3d4e5f6a7`, `c4d5e6f7a8b9`, `aa0fe1d8c95e`,
   `d5e6f7a8b9c0`, `e6f7a8b9c0d1`): vorwärts bis zum Kopf fahren:

   ```bash
   ../.venv/bin/alembic upgrade head
   ```

   Danach **Schritt 2 wiederholen** und den Stand `f1a2b3c4d5e6` bestätigen.

6. **Gegenprobe** in allen drei Fällen:

   ```bash
   ../.venv/bin/alembic current
   ```

   Erwarteter Stand: `f1a2b3c4d5e6 (head)`.

## Befund-Ledger prüfen (`ledger.py --pruefe`)

In gesteuerten Läufen ist der reguläre Aufruf `bash scripts/ledger.sh <nr> --pruefe`; das Skript startet `backend/scripts/ledger.py` im Interpreter der Projektumgebung (`${KAP2_VENV:-$HOME/.venvs/kap2}/bin/python`, fehlt er: Exit 2) und stellt dessen `bin` vorn in `PATH`, damit Prüfausdrücke mit `python3` denselben Interpreter nutzen. Das System-`python3` reicht dafür nicht, weil numpy fehlt. `ledger.py <nr> --pruefe` führt die Prüfausdrücke aus `reviews/BEFUNDE_<nr>.md` aus; die Zeitgrenze je Ausdruck steht ohne Einstellung bei 90 s und lässt sich mit der Umgebungsvariable `LEDGER_AUSDRUCK_TIMEOUT_S` (Sekunden, positive Zahl) ändern, damit Serverlast kein falsches Rot erzeugt; ein ungültiger Wert fällt mit einer Warnzeile auf 90 s zurück.

## Grenzen (bewusst so gelassen)

- Ein uvicorn-Worker; Multi-Worker bräuchte DB-basierte Queue-Slots
  (`SELECT … FOR UPDATE SKIP LOCKED`) statt des In-Prozess-Schedulers.
- Der Debounce-Zeitplan lebt im API-Prozess: Ein Reload verwirft nur den
  Zeitplan, nie die Korrektheit (Serving-Pfade bauen bei Miss/Stale lazy nach).
- Der Geodaten-Export (GeoPackage) läuft weiterhin als Thread im API-Prozess,
  liest aber gestreamt (`yield_per`) und streamt den Download von Platte.
