# Produktreife — Übergabe-Prompts („Plan der Pläne")

Stand: Juli 2026. Ziel: KAP2 zum kundenfertigen Produkt bringen. Dieses Dokument
enthält **10 vollständig eigenständige Prompts**. Jeder Prompt wird **unverändert
per Copy & Paste** an einen Agenten übergeben — nichts zusammensetzen, nichts
ausfüllen, nichts anpassen.

## So nutzt du dieses Dokument

1. **Eine frische Claude-Code-Session pro Prompt** (im Repo `/opt/lampp/htdocs/kap2` starten bzw. `/clear`).
2. **Modell + Effort einstellen** (steht über jedem Prompt), z. B. `/model claude-opus-4-8` bzw. `/model claude-fable-5`, Effort gemäß Empfehlung.
3. Wenn „Plan-Modus: ja" empfohlen ist: Plan-Modus aktivieren (Shift+Tab), Prompt einfügen, Plan prüfen, freigeben.
4. Prompt **komplett** kopieren (gesamter Codeblock) und einfügen.
5. Nach Abschluss: Commits prüfen, Checkbox unten abhaken.

## Kapazitätsleitfaden (Claude Pro, 5-Stunden-Fenster)

| Größe | Bedeutung | Faustregel fürs 5h-Fenster |
|-------|-----------|----------------------------|
| S | Kleiner, klar umrissener Fix | Läuft nebenbei, Fenster bleibt fast voll |
| M | Halbe Session | 2 M-Prompts pro Fenster sind realistisch |
| L | Volle Session | Frisch am Fensteranfang starten, sonst nichts einplanen |
| XL | Sprengt eine Session | Auf 2 Fenster einstellen; Prompt ist **wiederaufsetzbar** formuliert |

- **Opus-Prompts schonen dein Budget** — Fable nur dort, wo Konzept-/Architekturarbeit nötig ist.
- L-/XL-Prompts sind so formuliert, dass der Agent **kleinteilig committet**. Bricht die Session ab (Token-Limit): im nächsten Fenster **denselben Prompt erneut einwerfen** — der Agent erkennt am Code-/Commit-Stand, was schon erledigt ist, und macht weiter.
- Prompts 8 und 10 sind unabhängige „Lückenfüller" für Restbudget.

## Fortschritt

- [x] Prompt 1 — Sofort-Fixes (Render-Loop + falscher Status)
- [ ] Prompt 2 — Modell-Kritik (nur Doku)
- [ ] Prompt 3 — Modell-Umbau: Monetarisierung + EAD als Summe
- [ ] Prompt 4 — Zitationssystem: Author-Year
- [ ] Prompt 5 — Quellen-Inhalte bereinigen
- [ ] Prompt 6 — Parameter-Beschreibungen vervollständigen
- [ ] Prompt 7 — Dashboard ehrlich machen
- [ ] Prompt 8 — Klimaprofil-KPI-Leiste
- [ ] Prompt 9 — Info-Fenster/Lineage-Redesign
- [ ] Prompt 10 — Karten-Performance & Caching

## Reihenfolge & Abhängigkeiten

Empfohlene Reihenfolge = Nummerierung. Harte Abhängigkeiten sind wenige; die
Prompts sind robust formuliert (bedingte Klauseln statt Platzhalter), sodass auch
eine abweichende Reihenfolge nichts kaputt macht — nur ggf. Doppelarbeit kostet.

| # | Titel | Modell | Effort | Größe | Plan-Modus | Voraussetzung | Deckt ab (TODO.md-Zeilen) |
|---|-------|--------|--------|-------|------------|---------------|---------------------------|
| 1 | Sofort-Fixes | Opus 4.8 | mittel | S | nein | — | 1, 27–44 |
| 2 | Modell-Kritik (nur Doku) | Fable 5 | hoch | M | nein | — | 19 |
| 3 | Modell-Umbau Monetarisierung | Fable 5 | hoch | XL | ja | 2 empfohlen | 16 |
| 4 | Zitationssystem Author-Year | Opus 4.8 | mittel | M | nein | — | 12–14 |
| 5 | Quellen-Inhalte | Fable 5 | hoch | L (Batches) | nein | 4 empfohlen | 10, 11 |
| 6 | Parameter-Beschreibungen | Opus 4.8 | mittel | L (Batches) | nein | 3+4 empfohlen | 9, 15 |
| 7 | Dashboard ehrlich machen | Fable 5 | hoch | L | ja | 3 empfohlen | 4, 5, 7, 17 |
| 8 | Klimaprofil-KPI-Leiste | Opus 4.8 | mittel | M | nein | — (jederzeit) | 3, 18 |
| 9 | Lineage-Redesign | Fable 5 | hoch | L | ja | 1; 3 empfohlen | 20–25 |
| 10 | Karten-Performance | Opus 4.8 | hoch | M–L | empfohlen | — (jederzeit) | 2, 6, 26 |

---

## Prompt 1 — Sofort-Fixes: Endlos-Render-Loop + falscher „Noch keine Berechnung"-Status

**Modell:** Opus 4.8 · **Effort:** mittel · **Umfang:** S · **Plan-Modus:** nein · **Voraussetzung:** keine

```
Du arbeitest im Repo /opt/lampp/htdocs/kap2 — KAP2, ein Klimarisiko-Analyse-Tool für
deutsche Kommunen. Backend: Python/FastAPI (backend/app), PostgreSQL/PostGIS, pytest.
Frontend: React 18 + TypeScript + Vite (frontend/src), Zustand-Store, Recharts,
MapLibre GL (Karte), vis-network (Herkunfts-Diagramme). UI-Sprache Deutsch.
Hinweis: Genannte Zeilennummern sind Stand Juli 2026 — falls verschoben, per grep verifizieren.

Behebe zwei klar umrissene Frontend-Bugs. Ändere nichts darüber hinaus.

BUG A — Endlos-Render-Loop im Info-Fenster (massenhaft Console-Warnungen):
  Warning: Maximum update depth exceeded. This can happen when a component calls
  setState inside useEffect, but useEffect either doesn't have a dependency array,
  or one of the dependencies changes on every render.
  Component Stack: LineageOperatorOverlays (LineageOperatorOverlays.tsx:102) >
  LineageFlowDiagram (LineageFlowDiagram.tsx:296) > LayerInfoModal (LayerInfoModal.tsx:14) >
  MapDashboardTab (MapDashboardTab.tsx:13)

Diagnose (verifizieren, dann beheben) in frontend/src/components/LineageOperatorOverlays.tsx:
- Z. 117–119: operatorNodes/parameterNodes/weightEdges werden per .filter() OHNE
  useMemo erzeugt -> neue Array-Identität bei jedem Render.
- syncPositions ist ein useCallback mit Deps [network, operatorNodes, parameterNodes,
  weightEdges] (Z. 121–160) und ruft 3x setState (setViewScale, setNodePositions,
  setEdgePositions).
- Der useEffect (Z. 162–170) hängt an [network, syncPositions], registriert die
  vis-network-Events afterDrawing/viewChanged/zoom/dragEnd/stabilizationIterationsDone
  und ruft syncPositions() sofort auf. afterDrawing feuert bei jedem Redraw -> setState
  -> Redraw -> Rückkopplung; zusätzlich erzwingt die instabile syncPositions-Identität
  ständiges De-/Re-Registrieren.

Anforderungen an den Fix:
- Loop vollständig eliminieren (stabile Identitäten, setState nur bei tatsächlich
  geänderten Positionen/Skalierung, afterDrawing-Rückkopplung entkoppeln).
- Verhalten erhalten: Operator-/Parameter-Boxen und Gewichts-Badges müssen beim
  Pan/Zoom des Graphen weiterhin exakt mitwandern; editierbare Felder
  (api.updateParameters, Z. 172–194) müssen weiter funktionieren.

BUG B — Falscher Status beim Dashboard-Laden:
In frontend/src/components/Dashboard.tsx zeigt die Kopfleiste (interne Komponente
AssessmentBar, Statustext Z. 95–114) bei Status null — also bevor das erste
Status-Polling (useEffect ~Z. 40–63) geantwortet hat — den Text „Noch keine
Berechnung – …" (Z. 114). Für eine Kommune MIT abgeschlossener Berechnung erscheint
dadurch beim Laden kurz/fälschlich „noch keine Berechnung" im Hauptbereich, während
oben schon „Abgeschlossen" steht.
Anforderungen:
- Unterscheide drei Zustände sauber: (1) Status noch unbekannt/lädt -> neutraler
  Lade-Hinweis („Ergebnisse werden geladen …" mit Spinner), (2) Backend meldet
  wirklich keine Berechnung -> bisheriger Hinweis, (3) done -> Ergebnisse.
- Auch der Hauptbereich des Dashboards (Rendering erst bei status done, ~Z. 193)
  zeigt während des Ladens den Lade-Hinweis statt der „keine Berechnung"-Botschaft.

Verifikation:
- cd frontend && npm run build läuft fehlerfrei.
- Manuell: App starten (start-dev.sh), Info-Fenster eines Layers öffnen, pannen/zoomen,
  Ketten auf-/zuklappen -> keine „Maximum update depth exceeded"-Warnung in der Console.
- Dashboard einer berechneten Kommune neu laden -> nie „Noch keine Berechnung" zu sehen,
  sondern Lade-Hinweis, dann Ergebnisse.
- cd backend && python -m pytest tests/ -q bleibt grün (keine Backend-Änderung erwartet).

Committe die beiden Fixes als getrennte Commits mit aussagekräftigen deutschen
Commit-Messages. Entferne abschließend die erledigten Punkte aus TODO.md (Zeile 1
„loading results hint" und der Block „Maximum update depth exceeded" Z. 27–44) und
hake in docs/PRODUKTREIFE_PROMPTS.md unter „Fortschritt" Prompt 1 ab.
```

---

## Prompt 2 — Modell-Kritik: Mittelung vs. Summe, HxVxE/KWRA vs. absolute Werte

**Modell:** Fable 5 · **Effort:** hoch · **Umfang:** M · **Plan-Modus:** nein (reine Analyse + Doku) · **Voraussetzung:** keine

```
Du arbeitest im Repo /opt/lampp/htdocs/kap2 — KAP2, ein Klimarisiko-Analyse-Tool für
deutsche Kommunen nach KWRA-Logik (Klimawirkungs- und Risikoanalyse, HxVxE). Backend:
Python/FastAPI (backend/app). Lies zuerst docs/BERECHNUNGS_HANDBUCH.md und
docs/REVIEW_WIRKUNGSMECHANISMEN.md.
Hinweis: Genannte Zeilennummern sind Stand Juli 2026 — falls verschoben, per grep verifizieren.

AUFGABE: Erstelle eine schonungslos kritische, methodisch fundierte Prüfung des
Rechenmodells und schreibe sie nach docs/MODELL_KRITIK.md. KEINE Code-Änderungen —
Deliverable ist ausschließlich dieses Dokument. Sei sehr kritisch; ein Gefälligkeits-
gutachten ist wertlos. Wo das Modell nicht trägt, sage es klar und liefere vollständige
Alternativen.

IST-MODELL (verifiziere diese Fakten im Code, sie sind Grundlage der Kritik):
- Zell-Risikoindex: backend/app/services/engine/risk_engine.py, cell_risk_indices():
  Risiko = Summe(w · H·E·V) / Summe(w) über die Wirkungsketten eines Risikos, skaliert
  auf 0–100. Das ist ein GEWICHTETER MITTELWERT über die Ketten, keine Addition.
  Gewichte: catalog.PATHWAY_WEIGHTS (backend/app/data/catalog.py ~Z. 1030): primary 1.0,
  aligned 0.85, alternate 0.70–0.75, compound 0.50–0.65. Ketten werden deterministisch
  in build_pathways() (catalog.py ~Z. 1043–1088) erzeugt; „Erwartete jährliche
  Mortalität" (EXPECTED_ANNUAL_MORTALITY, catalog.py ~Z. 508) hat 12 Ketten.
- Normierung: H/E/V linear auf 0..1 via norm_min/norm_max (catalog.normalize_value ~Z. 2427).
- Absolutwert: outcome = ref_value · (Index/100) · scale_factor, mit scale_factor
  pop/100000, area_km2/50 oder 1.0 (risk_engine.cell_outcome() bzw.
  estimate_outcome_and_cost()). ref_value = „Outcome bei Index=100 für Referenzkommune
  mit 100 000 Ew" (catalog.py ~Z. 503), z. B. Mortalität ref_value=18 Todesfälle/Jahr.
- Kommune-Aggregation: risk_engine.aggregate() nimmt das 90. PERZENTIL der
  Zell-Indizes je Risiko (AGGREGATION_PERCENTILE = 90.0); Gruppen-Index = arithmetisches
  Mittel der Einzelrisiko-P90 je KWRA-Gruppe.
- Kosten: cost_eur = outcome (bei cost_dimension monetary) bzw. outcome ·
  cost_per_outcome_eur (health, nur 12/48 Risiken); operational/environment durchgehend
  0 EUR. total_eur = Summe über ALLE Risiken INKLUSIVE des eigenständigen Risikos
  „Gesamtschäden (EAD)" (EXPECTED_TOTAL_DAMAGE_EAD_EUR, catalog.py ~Z. 608,
  ref_value=10 Mio) -> mutmaßliche Doppelzählung.

ZU BEANTWORTENDE KERNFRAGEN (je Frage: Analyse mit durchgerechnetem Zahlenbeispiel aus
dem echten Katalog, dann Urteil „haltbar / bedingt haltbar / nicht haltbar" + Begründung):
1. Mitteln statt Addieren: Aus jeder Wirkungskette können reale Outcomes (z. B. Tote)
   resultieren. Ist der gewichtete Mittelwert über 12 Ketten fachlich vertretbar, oder
   müsste addiert werden? Wird das durch ref_value-Kalibrierung implizit „ausgeglichen"
   — und falls ja: ist diese Kopplung transparent und robust (z. B. wenn ein Nutzer
   norm_min/max oder Gewichte ändert)?
2. Taugt ein normierter HxVxE-Index (0–100) überhaupt als Basis für ABSOLUTE Outcomes
   via linearer ref_value-Skalierung? Wo bricht die Linearität (Sättigung,
   Schwellwerteffekte, Extremereignisse)?
3. Kommune-Aggregation P90 + „Mittel der P90s" je Gruppe: Ist das für absolute
   Schadenssummen korrekt (P90 eines Index vs. Summe der Zell-Outcomes)? Konsistenz
   zwischen Karte (Zellwerte), Dashboard (P90) und Kostensumme (Summe)?
4. Doppelzählungen: EAD als eigenes Risiko in der Gesamtsumme; Überlappungen zwischen
   Sektorschäden (z. B. Gebäude vs. Wiederherstellungskosten vs. indirekte Verluste).
5. Ist die Kettenkonstruktion (build_pathways: automatische primary/aligned/alternate/
   compound-Kombinatorik) fachlich begründbar oder ein Artefakt?
6. Passt das alles zum Anspruch, bei der KWRA-Methodik (UBA 2021) anschlussfähig zu
   bleiben UND absolute, monetarisierbare Werte je Kommune auszuweisen?

DELIVERABLE docs/MODELL_KRITIK.md mit dieser Struktur:
1. Ist-Modell kompakt (mit Code-Fundstellen) — max. 1 Seite.
2. Stärken (ehrlich, kurz).
3. Schwachstellen — je mit konkretem Zahlenbeispiel aus dem Katalog durchgerechnet.
4. Urteil je Kernfrage (Tabelle: Frage, Urteil, Begründung in 2–3 Sätzen).
5. EMPFEHLUNG mit klarer Ansage: (a) Modell so lassen, (b) gezielt reparieren
   (welche Stellschrauben genau), oder (c) Outcome-Schicht ersetzen. Der Wunsch ist,
   an der KWRA (HxVxE als Screening-/Vergleichslogik) festzuhalten — prüfe insbesondere
   die Architektur „HxVxE-Index fürs Screening + getrennte Wirkmodell-Schicht
   (Schadensfunktionen je Risiko) für Absolutwerte".
6. Falls (b) oder (c): VOLLSTÄNDIGE Alternativ-Spezifikation, die ALLE 48 Risiken
   abdeckt (gruppiert nach cost_dimension health/monetary/environment/operational):
   je Gruppe Formelwerk, benötigte Parameter (inkl. Einheiten und plausibler
   Quellenlage: KWRA 2021, UBA Methodenkonvention 3.1, GDV, Prognos 2023, RKI),
   Aggregationsregeln Zelle->Kommune, Migrationsskizze vom Ist-Zustand und was an
   bestehenden Daten/Parametern weiterverwendbar ist.
7. Entscheidungsvorlage: 3–5 Ankreuz-Optionen für den Product Owner, mit Aufwand
   (S/M/L) und Konsequenzen.

Anschließende Prompts (Modell-Umbau, Dashboard) lesen dieses Dokument und setzen
deine Empfehlung um — schreibe es so konkret, dass ein Agent ohne Rückfragen damit
arbeiten kann.

Verifikation: Dokument vollständig nach obiger Struktur; alle Code-Fundstellen
stichprobenhaft korrekt; keine Code-/Datenänderung im Repo (git status zeigt nur
docs/MODELL_KRITIK.md). Committe das Dokument. Entferne den erledigten Punkt aus
TODO.md (Z. 19, „kritische Einschätzung des Modells") und hake in
docs/PRODUKTREIFE_PROMPTS.md unter „Fortschritt" Prompt 2 ab.
```

---

## Prompt 3 — Modell-Umbau: Jedes Risiko monetarisiert, Kostensätze als Parameter, Gesamtschaden = Summe

**Modell:** Fable 5 · **Effort:** hoch · **Umfang:** XL (auf 2 Sessions einstellen, wiederaufsetzbar) · **Plan-Modus:** ja · **Voraussetzung:** Prompt 2 empfohlen (Prompt funktioniert auch ohne)

```
Du arbeitest im Repo /opt/lampp/htdocs/kap2 — KAP2, ein Klimarisiko-Analyse-Tool für
deutsche Kommunen (KWRA/HxVxE). Backend: Python/FastAPI (backend/app), PostgreSQL/
PostGIS, pytest. Frontend: React 18 + TS + Vite (frontend/src). UI-Sprache Deutsch.
Hinweis: Zeilennummern Stand Juli 2026 — bei Abweichung per grep verifizieren.
WICHTIG: Falls docs/MODELL_KRITIK.md existiert, lies es zuerst und setze dessen
Empfehlungen zur Outcome-/Aggregationslogik mit um. Falls nicht: behalte die bestehende
HxVxE->ref_value-Outcome-Logik bei und setze nur das Folgende um.

ZIEL (ganz wichtig, Kernanforderung des Product Owners): JEDES Risiko fließt monetär
bewertet in den Gesamtschaden ein. Jeder nicht-monetäre Indikator (Tote, Fälle,
Stunden, ha, Arten, Index) erhält einen EIGENSTÄNDIGEN, editierbaren, mit Quellen
belegten Monetarisierungs-Parameter. Der Gesamtschaden ist die SUMME der
monetarisierten Einzelrisiken — kein eigenständig „gemessener" Parameter mehr.

IST-ZUSTAND (verifizieren):
- 48 Risiken in backend/app/data/catalog.py (RISKS, ab ~Z. 507) mit cost_dimension
  in {monetary, health, environment, operational} und outcome_unit.
- Nur 12/48 Risiken haben cost_per_outcome_eur (z. B. Mortalität 3 500 000 EUR/Todesfall,
  ~Z. 515; Morbidität 5 000; Verletzte 12 000; Betroffene 2 500). health teils 0 EUR
  (Belastungsstunden), operational und environment KOMPLETT 0 EUR -> diese Risiken
  fehlen heute in jeder Kostensumme.
- cost_per_outcome_eur wird von backend/app/services/parameter_registry.py NICHT als
  Parameter emittiert (Risiko-Schleife ~Z. 101–113 erzeugt nur risks.<CODE>.ref_value)
  -> der VSL von 3,5 Mio EUR ist weder in der Konfigurations-UI noch im Excel-Export
  sichtbar/editierbar, sondern nur Katalogfeld + Prosa im source_detail des
  Mortalitäts-ref_value (catalog.py ~Z. 872–880, BESPOKE) — dort gehört er nicht hin.
- „Gesamtschäden (EAD)": EXPECTED_TOTAL_DAMAGE_EAD_EUR (catalog.py ~Z. 608,
  ref_value=10 Mio, group compound) ist ein EIGENES HxVxE-Risiko, UND
  risk_engine.aggregate() summiert cost_eur ALLER Risiken inklusive EAD in total_eur
  (gespeist in Dashboard-KPI „Erwartete Schäden", frontend/src/components/Dashboard.tsx
  ~Z. 222) -> Doppelzählung.
- Berechnung: backend/app/services/engine/risk_engine.py (cell_outcome,
  estimate_outcome_and_cost, aggregate), Overrides via override_context.py,
  Maßnahmen-Verrechnung in backend/app/services/measure_service.py (nutzt cost_eur
  für vermiedene Schäden), Export backend/app/services/export_service.py.

ANFORDERUNGEN:
1. Monetarisierungs-Parameter: Für jedes Risiko mit nicht-monetärem outcome ein
   Registry-Parameter (z. B. ID risks.<CODE>.cost_per_outcome, Einheit „EUR je
   <outcome_unit>", editierbar, override-fähig wie ref_value, mit source,
   source_detail und references über backend/app/data/sources.py). Sichtbar in:
   Konfigurations-UI (frontend ParameterTable, Gruppe Klimarisiken), Parameter-Excel
   (export_parameters_xlsx), Info-Tooltip. Der Mortalitäts-VSL (3,5 Mio) wird dabei
   aus dem ref_value-source_detail herausgelöst und an den neuen Parameter verschoben.
2. Kostensätze recherchieren und belegen: Für ALLE bisher unbelegten/0-EUR-Risiken
   fachlich plausible Sätze festlegen. Primärquellen: UBA Methodenkonvention 3.1
   (Umwelt- und Gesundheitskosten), VSL-Literatur (EU/OECD-Band), Ausfall-/
   Unterbrechungskostensätze (KRITIS/BBK, VDE/dena), Ökosystemleistungs-Bewertung
   (BfN/TEEB DE, Grunewald u. a.), GDV-Schadenstatistik. Jede Quelle als Eintrag in
   sources.py-Bibliografie (Schema der Datei folgen, inkl. Wayback-archive_url; neue
   URLs mit https://web.archive.org/save/<url> archivieren). Wo keine belastbare
   Quelle existiert: dokumentierte, im source_detail ehrlich begründete Modellannahme.
   Ein Risiko darf NUR dann unmonetarisiert bleiben, wenn Monetarisierung eine
   Doppelzählung wäre — dann im source_detail begründen und das Risiko explizit von
   der Summe ausnehmen (nachvollziehbar im Code + Doku).
3. Gesamtschaden = Summe: EXPECTED_TOTAL_DAMAGE_EAD_EUR verliert seine Rolle als
   eigenständiges HxVxE-Risiko. Entscheide begründet: entfernen ODER zu reiner
   Anzeige-Summe umwidmen (API-/Frontend-Kompatibilität beachten). total_eur,
   cost-summary, Dashboard-KPIs, Maßnahmen-Wirkung (measure_service, vermiedene
   Schäden) und Excel-Exporte müssen konsistent die Summe der monetarisierten
   Einzelrisiken ausweisen, ohne Doppelzählung. Achte auf weitere Überlappungen
   (z. B. Wiederherstellungskosten vs. Sektorschäden) — wo vorhanden, dokumentieren.
4. Doku nachziehen: docs/BERECHNUNGS_HANDBUCH.md (Kostenkapitel) aktualisieren.
5. Tests: bestehende backend/tests grün halten und ergänzen: (a) Registry emittiert
   für jedes nicht-monetäre Risiko einen Kostensatz-Parameter, (b) total_eur ==
   Summe der Einzel-cost_eur (ohne Ausgenommene), (c) Excel-Export enthält die neuen
   Parameter, (d) Override eines Kostensatzes wirkt auf cost_eur.
6. Invalidierung: Nach Modelländerung müssen gecachte Layer/Ergebnisse konsistent
   bleiben (backend layer_cache.invalidate() bzw. Hinweis auf Neuberechnung) — wähle
   und implementiere eine saubere Lösung.

ARBEITSWEISE (wiederaufsetzbar, Session kann am Token-Limit enden):
Arbeite in committeten Stufen: (1) Registry/Engine-Verdrahtung des Kostensatz-
Parameters, (2) Datenpflege aller Kostensätze inkl. Quellen (in 2–3 Commits nach
cost_dimension gebatcht), (3) EAD-Umbau + Summenlogik, (4) Frontend/Export/Tests/Doku.
Nach jeder Stufe: Tests laufen lassen, committen (deutsche Messages). Wenn du in einer
Folge-Session mit demselben Prompt startest: prüfe per git log und Code-Stand, welche
Stufe erledigt ist, und setze dort fort.

Verifikation: cd backend && python -m pytest tests/ -q grün; cd frontend && npm run
build grün; manuell: Konfiguration zeigt Kostensatz-Parameter mit Tooltip+Quelle,
Dashboard-Gesamtschaden = nachrechenbare Summe der Risiko-Schäden. Entferne den
erledigten Punkt aus TODO.md (Z. 16, „wieso gibt es einen Parameter für Gesamtschäden
(EAD) …") und hake in docs/PRODUKTREIFE_PROMPTS.md unter „Fortschritt" Prompt 3 ab.
```

---

## Prompt 4 — Zitationssystem: Author-Year statt IEEE, „Quelle" statt „Quelle (IEEE)"

**Modell:** Opus 4.8 · **Effort:** mittel · **Umfang:** M · **Plan-Modus:** nein · **Voraussetzung:** keine

```
Du arbeitest im Repo /opt/lampp/htdocs/kap2 — KAP2, ein Klimarisiko-Analyse-Tool für
deutsche Kommunen. Backend: Python/FastAPI (backend/app), pytest. Frontend: React 18 +
TS + Vite (frontend/src). UI-Sprache Deutsch.
Hinweis: Zeilennummern Stand Juli 2026 — bei Abweichung per grep verifizieren.

PROBLEM: Das Quellen-System nutzt IEEE-Zitationen und ist uneinheitlich beschriftet.
Gewünscht ist durchgängiger Author-Year-Stil: In der Spalte „Quelle" steht immer
einheitlich kurz „Name Jahr", im Info-Fenster/Tooltip die vollständige Zitation.
Nirgendwo in der UI darf mehr „IEEE" stehen — die Überschrift heißt schlicht „Quellen".

IST-ZUSTAND (verifizieren):
- backend/app/data/sources.py: SOURCE_REFERENCES mit 37 Einträgen, Felder je Eintrag:
  ieee (IEEE-Vollzitat), url, archive_url (Wayback), accessed. resolve(keys) hängt
  Einträge an Parameter/Kostenkomponenten; Aufrufer: backend/app/services/
  parameter_registry.py (~Z. 112, 132, 171, 184, 230) und backend/app/services/
  measure_service.py (~Z. 168).
- Frontend: frontend/src/components/InfoTooltip.tsx ~Z. 89 rendert die Überschrift
  „Quellen (IEEE)" und je Referenz das ieee-Feld + Links „Original"/„Archiv-Snapshot".
  Typ SourceReference in frontend/src/types/index.ts (Feld ieee).
- Parameter-Tabelle: frontend/src/components/ParameterTable.tsx, Spalten Bezeichnung/
  Wert/Einheit/Quelle/Status — Spalte „Quelle" zeigt die source-Kurzlabels aus dem
  Katalog (backend/app/data/catalog.py), die derzeit uneinheitlich sind („Prognos/GWS/
  IÖW 2023", „RKI 2022 / Winklmayr u.a. 2022 / UBA MK3.1 2020", „BBK KRITIS
  (Modellannahme)", „DWD CDC / Copernicus C3S-CORDEX (regionalisiert)" …).
- Excel-Export: backend/app/services/export_service.py, export_parameters_xlsx
  (~Z. 182–240), Spalte 12 heißt „Quellen (IEEE + Archiv-Snapshot)" und formatiert
  die references (~Z. 205–212).

ANFORDERUNGEN:
1. sources.py umstellen: je Eintrag statt ieee zwei Felder: citation = vollständige
   deutsche Author-Year-Zitation (Schema: Autor(en)/Institution (Jahr): Titel.
   Ort/Publikation. Online verfügbar, Zugriff <Datum>. — bei >3 Autoren „u. a.") und
   short = Kurzform „Name Jahr" (z. B. „Winklmayr u. a. 2022", „UBA 2020",
   „Prognos/GWS/IÖW 2023"). Alle 37 Einträge sorgfältig konvertieren (Inhalte aus dem
   ieee-Text übernehmen, nichts erfinden). resolve() liefert beide Felder;
   Pydantic-Schema (schemas.SourceReference o. ä.) und frontend/src/types/index.ts
   angleichen. Rückwärtskompatibilität ist NICHT nötig (kein externer Konsument),
   aber alle Verwendungsstellen im Repo müssen mitgezogen werden (grep nach "ieee").
2. UI: InfoTooltip-Überschrift „Quellen (IEEE)" -> „Quellen"; Liste rendert citation;
   Links Original/Archiv bleiben. Wo references vorhanden sind, soll die Spalte
   „Quelle" die short-Labels (kommagetrennt) anzeigen statt des freien source-Strings,
   damit Spalte und Tooltip zusammenpassen; der freie source-String bleibt Fallback,
   wo (noch) keine references verdrahtet sind.
3. Format-Konvention für source-Kurzlabels im Katalog dokumentieren (Kommentar am
   Kopf von catalog.py): immer „Name Jahr", mehrere Quellen mit „ / " getrennt,
   Zusatz „(Modellannahme)" nur wenn tatsächlich Annahme. Bestehende Labels, die sich
   OHNE inhaltliche Recherche eindeutig umformen lassen, direkt vereinheitlichen
   (reine Formatfrage). Inhaltlich unklare Labels NICHT umdeuten — deren Klärung ist
   ein separater Auftrag (Quellen-Inhalte).
4. Excel: Spaltentitel zu „Quellen (Vollzitate + Archiv-Snapshot)", Inhalt nutzt
   citation. Spalte „Quelle" (Kurzlabel) analog zur UI mit short-Labels befüllen,
   wo references existieren.
5. Doku: docs/QUELLEN_ANREICHERUNG_PROMPTS.md oben mit Hinweis versehen
   „Überholt (Juli 2026): Zitierstil auf Author-Year umgestellt, Feld ieee -> citation
   + short; Schema-Beispiele unten entsprechend lesen." Erwähnungen von IEEE in
   docs/BERECHNUNGS_HANDBUCH.md ggf. anpassen.
6. Tests: backend-Tests, die das ieee-Feld prüfen (z. B. tests/test_measure_pricing.py),
   auf citation/short umstellen; Vollständigkeits-Check ergänzen: jeder
   SOURCE_REFERENCES-Eintrag hat citation, short, url, archive_url, accessed.

Verifikation: cd backend && python -m pytest tests/ -q grün; cd frontend && npm run
build grün; grep -rn "IEEE" frontend/src backend/app liefert keine nutzersichtbaren
Strings mehr (nur ggf. Kommentare/Changelog); manuell: Tooltip eines belegten
Parameters zeigt „Quellen" mit Author-Year-Vollzitaten, Spalte „Quelle" zeigt
„Name Jahr". Committe granular (sources.py-Umbau, Frontend, Export, Doku getrennt).
Entferne die erledigten Punkte aus TODO.md (Z. 12–14, „Benennung der Quellen") und
hake in docs/PRODUKTREIFE_PROMPTS.md unter „Fortschritt" Prompt 4 ab.
```

---

## Prompt 5 — Quellen-Inhalte: Unklare Labels auflösen, fehlende Referenzen ergänzen

**Modell:** Fable 5 · **Effort:** hoch · **Umfang:** L (Batches, wiederaufsetzbar) · **Plan-Modus:** nein · **Voraussetzung:** Prompt 4 empfohlen (Prompt passt sich dem vorgefundenen Schema an)

```
Du arbeitest im Repo /opt/lampp/htdocs/kap2 — KAP2, ein Klimarisiko-Analyse-Tool für
deutsche Kommunen. Backend: Python/FastAPI (backend/app), pytest. Quellen-Bibliografie:
backend/app/data/sources.py (SOURCE_REFERENCES: key -> Eintrag mit Vollzitat, url,
archive_url, accessed; resolve() hängt sie als references an Parameter). Katalog:
backend/app/data/catalog.py (HAZARDS/EXPOSURES/VULNERABILITIES/RISKS/MEASURES mit
source, source_detail, source_refs). PRÜFE ZUERST das vorgefundene Feldschema der
Bibliografie (citation/short oder noch ieee) und folge exakt dem vorhandenen Schema.
Hinweis: Zeilennummern Stand Juli 2026 — bei Abweichung per grep verifizieren.

PROBLEM (Product Owner): „Noch nicht alle Quellen sind klar. Beispiel ‚Berliner
Wasserbetriebe / Modellannahme' — ja was jetzt, Quelle oder Annahme? Beispiel Risiko
‚Erwartete jährliche Mortalität': source sagt ‚RKI 2022 / Winklmayr u.a. 2022 /
UBA MK3.1 2020', aber im Info-Fenster sind nur RKI und UBA als Referenz ausgeschrieben
— Winklmayr fehlt als eigene Referenz. Am Ende darf es KEINE unverständlichen Quellen
mehr geben."

IST-ZUSTAND (verifizieren):
- source_detail/source_refs werden für Risiken und H/E/V großteils beim Import
  GENERISCH erzeugt: _enrich_risk_sources() (catalog.py ~Z. 862, nur 4 BESPOKE-Risiken
  handkuratiert) und _enrich_hev_sources() (~Z. 970) hängen Template-Prosa ans grobe
  source-Label.
- Mengengerüst Risiken (48): 17x „Prognos/GWS/IÖW 2023", 11x „Modellannahme
  (Index=Outcome, dokumentiert)", 9x „BBK KRITIS (Modellannahme)", 4x „UBA MK3.1 2020 /
  RKI JoHM", 4x „BfN / UBA (Modellannahme)", 2x „Modellannahme (Belastungsstunden,
  unbelegt)", 1x „RKI 2022 / Winklmayr u.a. 2022 / UBA MK3.1 2020"; ~13 Risiken ganz
  ohne references. „Modellannahme" kommt 235x in catalog.py vor. Bibliografie hat
  37 Einträge. Bei Maßnahmen (47) sind Kostenfelder teils ohne source_refs.

AUFTRAG — für JEDEN Parameter mit unklarem oder zusammengesetztem Quellenlabel:
1. Slash-Komposita auflösen: Jede im Label genannte echte Quelle wird ein eigener
   Bibliografie-Eintrag (z. B. Winklmayr u. a. 2022, Dtsch Arztebl — als eigene
   Referenz, nicht nur als „Methodik des RKI" erwähnt) und per source_refs verdrahtet.
   Der Annahme-Anteil wird im source_detail sauber getrennt erklärt nach dem Muster:
   „Wert X aus <Quelle kurz>; Übertragung auf <Kontext> ist Modellannahme, weil <…>".
   Ein Label wie „Berliner Wasserbetriebe / Modellannahme" muss danach im Tooltip
   glasklar beantworten: WAS stammt aus der Quelle, WAS ist Annahme, WARUM.
2. „Modellannahme" ohne nachvollziehbare Erklärung: Recherchiere ernsthaft nach einer
   belastbaren realen Quelle (Web). Wenn gefunden und der Wert abweicht: Wert im
   Katalog auf den belegten Wert ändern (Konsistenzregel des Projekts). Wenn keine
   Quelle existiert: ehrliches, spezifisches Rational ins source_detail (kein
   Textbaustein). NIEMALS Quellen oder URLs erfinden; jede URL vor Eintrag abrufen.
3. Jede neue Quelle archivieren (Wayback): curl -s -I "https://web.archive.org/save/<url>"
   und den Location-Permalink als archive_url übernehmen; falls das scheitert, den
   jüngsten vorhandenen Snapshot über die CDX-API verwenden
   (https://web.archive.org/cdx/search/cdx?url=<url>&output=json&limit=-1&filter=statuscode:200).
4. Generische Template-Prosa der Enrichment-Funktionen gilt NICHT als Erklärung —
   betroffene Einträge bekommen individuelle source_detail-Texte. Passe bei Bedarf
   _enrich_risk_sources/_enrich_hev_sources so an, dass handgepflegte Einträge nie
   überschrieben werden.

ARBEITSWEISE (wiederaufsetzbar): Batches in dieser Reihenfolge, nach JEDEM Batch
pytest + Commit (deutsche Message, Batch-Name nennen):
A Risiken health (Mortalität zuerst — das ist das Referenzbeispiel), B Risiken
monetär, C Risiken operational+environment, D Hazards, E Expositionen,
F Sensitivitäten/Vulnerabilitäten, G Formel-/UHI-/Pfadgewicht-Parameter,
H Maßnahmen-Restfelder. Erledigt erkennst du an individuellen (nicht Template-)
source_detail-Texten + verdrahteten source_refs. Startest du mit diesem Prompt in
einer Folge-Session: identifiziere den ersten unfertigen Batch und setze dort fort.

ENDZUSTAND (Akzeptanz): Kein source-Label mehr, das Quelle und Annahme unerklärt
vermischt; jede im Label genannte Quelle als klickbare Referenz (inkl. Archiv-Link)
im Tooltip; ~13 referenzlose Risiken sind belegt oder tragen ein ehrliches,
spezifisches Rational; Winklmayr u. a. 2022 ist eigener Bibliografie-Eintrag am
Mortalitäts-Parameter.

Verifikation: cd backend && python -m pytest tests/ -q grün; Stichprobe im Frontend
(npm run dev): Tooltips von 5 zufälligen Parametern je Kategorie sind verständlich.
Entferne die erledigten Punkte aus TODO.md (Z. 10 und 11) und hake in
docs/PRODUKTREIFE_PROMPTS.md unter „Fortschritt" Prompt 5 ab.
```

---

## Prompt 6 — Parameter-Beschreibungen: Jeder Parameter erklärt (UI + Excel), Tooltip nur zum eigenen Parameter

**Modell:** Opus 4.8 · **Effort:** mittel · **Umfang:** L (Batches, wiederaufsetzbar) · **Plan-Modus:** nein · **Voraussetzung:** Prompts 3+4 empfohlen (Prompt funktioniert auch ohne)

```
Du arbeitest im Repo /opt/lampp/htdocs/kap2 — KAP2, ein Klimarisiko-Analyse-Tool für
deutsche Kommunen. Backend: Python/FastAPI (backend/app), pytest. Frontend: React 18 +
TS + Vite (frontend/src). UI-Sprache Deutsch.
Hinweis: Zeilennummern Stand Juli 2026 — bei Abweichung per grep verifizieren.

PROBLEM (Product Owner): „Noch nicht alle Parameter werden beschrieben. Für jeden
einzelnen Parameter muss — sowohl in der Konfiguration als auch im Parameter-Export-
Excel — eine Erklärung hinterlegt sein. Auch wo es keine Quellen gab, muss das
Rational hinter der Entscheidung klar beschrieben werden." Zusätzlich: „Info-Fenster
dürfen immer nur den EINEN Parameter beschreiben. Negativbeispiel: Beim Referenzwert
der Erwarteten jährlichen Mortalität steht der Satz ‚Kostensatz 3,5 Mio EUR (VSL …)
als Punktwert; editierbar' — das gehört nicht zum Referenzwert."

IST-ZUSTAND (verifizieren):
- Registry: backend/app/services/parameter_registry.py, catalog_parameters() erzeugt
  ~670 Parameter: 48 risks.*.ref_value, 46+48+66 norm_min/max (Hazards/Expositionen/
  Vulnerabilitäten), ~28 Formel-Parameter, 423 Maßnahmen-Kostenfelder (47 Maßnahmen x
  9 Felder, viele „nicht anwendbar"), 9 Pfadgewichte, 4 UHI-Koeffizienten.
- Es gibt KEIN description-Feld: Die inhaltliche Erklärung lebt im Feld source_detail
  („Herleitung") und wird im (i)-Tooltip (frontend/src/components/InfoTooltip.tsx via
  ParameterTable.tsx, ConfigPanelTab.tsx, MeasureSidebar.tsx) und in der Excel-Spalte
  „Herleitung" (backend/app/services/export_service.py, export_parameters_xlsx,
  ~Z. 182–240) angezeigt. Nur ~10 source_detail-Texte sind handgepflegt; der Rest ist
  generisches Template aus _enrich_*-Funktionen in backend/app/data/catalog.py oder leer.

AUFTRAG:
1. Entscheide zuerst die Struktur und ziehe sie überall durch: EMPFOHLEN ist ein
   eigenes Beschreibungsfeld (z. B. description) je Registry-Parameter, getrennt von
   der Quellen-Herleitung (source_detail), emittiert in parameter_registry, angezeigt
   im Tooltip (eigener Absatz „Was ist das?" vor der Herleitung) und als eigene
   Excel-Spalte „Beschreibung". Alternativ (begründen!) eine klar strukturierte
   Konvention innerhalb von source_detail. Einheitlichkeit ist Pflicht.
2. Inhalt je Parameter (deutsch, 2–5 Sätze, für kommunale Fachleute ohne
   Modellierungs-Hintergrund): (a) Was bedeutet der Parameter konkret? (b) Wie fließt
   er in die Berechnung ein (wo wirkt er)? (c) Warum dieser Wert — Quelle ODER offen
   deklariertes Rational der Modellannahme. Floskeln und identische Textbausteine für
   unterschiedliche Parameter sind nicht akzeptabel; bei den 423 Maßnahmen-Feldern
   sind feldtyp-spezifische Vorlagen ok (z. B. was capex_per_m2 generell bedeutet),
   aber der maßnahmenspezifische Teil muss individuell sein. „Nicht anwendbar"-Felder
   erklären in einem Satz, WARUM sie für diese Maßnahme nicht gelten.
3. Scoping-Regel durchsetzen: Jeder Tooltip-Text beschreibt NUR seinen Parameter.
   Konkret zu bereinigen: der VSL-/Kostensatz-Passus im source_detail des
   Mortalitäts-ref_value (catalog.py ~Z. 872–880). Falls es (nach dem Modell-Umbau)
   eigene Kostensatz-Parameter risks.*.cost_per_outcome gibt, gehört der Text dorthin;
   falls nicht, in einen neutralen Hinweis am richtigen Ort verschieben. Prüfe
   systematisch alle handgepflegten Texte auf solche Vermischungen.
4. Excel-Export: Für JEDEN der ~670 Parameter ist die Beschreibungs-/Herleitungsspalte
   nicht leer. Spaltenbreiten/Zeilenumbruch so setzen, dass das Excel lesbar bleibt.

ARBEITSWEISE (wiederaufsetzbar): Batches mit Commit + pytest nach jedem Batch:
A Risiken (48), B Hazards (23 Einträge/46 Parameter), C Expositionen (24/48),
D Vulnerabilitäten (33/66), E Formel+UHI+Pfadgewichte (~41), F Maßnahmen (47x9).
Schreibe dir zu Beginn ein kleines Prüfskript (backend, z. B. scripts/ oder Test),
das alle Registry-Parameter mit leerer/generischer Beschreibung auflistet — es ist
zugleich dein Fortschritts-Tracker über Sessions hinweg und am Ende dein
Akzeptanznachweis (0 Treffer). In einer Folge-Session mit demselben Prompt: Skript
laufen lassen, ersten unfertigen Batch fortsetzen.

Verifikation: Prüfskript meldet 0 unbeschriebene Parameter; cd backend && python -m
pytest tests/ -q grün; cd frontend && npm run build grün; manuell: Konfigurations-Tab
— jeder (i)-Tooltip hat eine verständliche Beschreibung, die nur den eigenen Parameter
behandelt; Parameter-Excel exportieren und Stichprobe prüfen. Entferne die erledigten
Punkte aus TODO.md (Z. 9 und 15) und hake in docs/PRODUKTREIFE_PROMPTS.md unter
„Fortschritt" Prompt 6 ab.
```

---

## Prompt 7 — Dashboard ehrlich machen: Hotspots sichtbar, betroffene Fläche + Geldwerte, Absolutwert-Diagramme, Parameter in der Risikoverteilung

**Modell:** Fable 5 · **Effort:** hoch · **Umfang:** L · **Plan-Modus:** ja · **Voraussetzung:** Prompt 3 empfohlen (Prompt funktioniert auch ohne)

```
Du arbeitest im Repo /opt/lampp/htdocs/kap2 — KAP2, ein Klimarisiko-Analyse-Tool für
deutsche Kommunen (KWRA/HxVxE). Backend: Python/FastAPI (backend/app), PostgreSQL/
PostGIS, pytest. Frontend: React 18 + TS + Vite (frontend/src), Recharts, Zustand,
MapLibre-Karte. UI-Sprache Deutsch. Nutze vor dem Bauen von Diagrammen den
dataviz-Skill, falls verfügbar.
Hinweis: Zeilennummern Stand Juli 2026 — bei Abweichung per grep verifizieren.
Falls docs/MODELL_KRITIK.md existiert: Empfehlungen zur Aggregation berücksichtigen.

PROBLEM (Product Owner, wörtlich): „Derzeit sieht es so aus, als ob für eine Kommune
immer alles völlig okay ist. Beispiel Oschatz: fast kein Ausschlag für
landwirtschaftliche Schäden im Dashboard, aber die Karte zur Landwirtschaft ist tief
rot — das passt nicht zusammen. Wenn ich 10 000 Zellen habe und nur in 20 extreme
Hitze-Events, dann scheine ich kein Problem zu haben; dass es in diesen 20 Zellen
richtig brenzlig werden könnte und Handlungsbedarf besteht, kommt nicht hervor. Ich
mag die Netzdiagramme eigentlich sehr, aber es sieht immer alles völlig in Ordnung
aus — was es ja nicht ist."

IST-ZUSTAND (verifizieren):
- Dashboard: frontend/src/components/Dashboard.tsx (~467 Z.): „Zusammenfassung" mit
  Radar der 5 KWRA-Gruppen + Kosten-KPIs (~Z. 196–247), „Risiken" mit Radar je Gruppe
  (~Z. 253), „Risikoverteilung" mit Histogramm (20 Bins) + KPIs P90/Max/„betroffene
  Zellen"/Schaden pro Jahr (~Z. 285 ff.).
- Aggregation im Backend: risk_engine.aggregate() liefert je Risiko P90-Index
  (AGGREGATION_PERCENTILE=90), max_index, outcome, cost_eur; Gruppen-Index = Mittel
  der P90s. Histogramm: backend/app/api/routes/assessment.py, risk_histogram()
  (~Z. 273–335, zählt live aus CellAssessment-Zeilen, kennt nonzero_cells/total_cells).
  Endpoints: /kommune/{id}/risk-summary, /risk-histogram, /cost-summary
  (frontend/src/api/client.ts). Zellwerte gibt es nur über die Karten-Endpoints
  (/layer/{code}/values).
- Karte färbt RELATIV zum Min/Max des jeweiligen Layers (frontend/src/components/
  MapView.tsx, interpolate-Expression ~Z. 360–400) — daher „Karte tiefrot, Dashboard
  unauffällig": zwei verschiedene Wahrheiten aus denselben Daten.
- Zellgröße 100 m -> eine Zelle = 0,01 km² (für Flächenangaben).

AUFTRAG (Konzept zuerst, dann Umsetzung — du bist im Plan-Modus):
1. Konzipiere ein ehrliches Kennzahlen-Set, das Tail-Risiken sichtbar macht, und
   setze es um. Kandidaten (triff eine begründete Auswahl, keine Kennzahlen-Flut):
   betroffene Fläche in km² UND % (statt „betroffene Zellen" — überall, auch in
   Tabellen/Tooltips), Anteil der Zellen über kritischem Schwellindex, Max vs. P90
   nebeneinander, Anteil der Schadenssumme aus den Top-5%-Zellen (Konzentration),
   absoluter Schaden EUR/Jahr je Risiko. Schwellwerte begründen und dokumentieren.
2. Radar-Diagramme behalten, aber ehrlich machen: feste Skala 0–100 mit sichtbaren
   Bewertungsringen/Schwellen und Beschriftung der Werte; zusätzlich muss pro Gruppe
   erkennbar sein, wenn einzelne Zell-Hotspots existieren, obwohl der P90 niedrig ist
   (z. B. Hotspot-Marker/Badge am Radar-Eckpunkt oder Max-Overlay). Wähle eine
   saubere Lösung und begründe sie kurz im Code-Kommentar.
3. Je Risiko ein Diagramm mit ABSOLUTEN Werten (Outcome in Originaleinheit und EUR/
   Jahr), nicht nur Indizes (TODO Z. 5). Für nicht-monetarisierte Risiken (falls der
   Modell-Umbau noch nicht gelaufen ist): Outcome zeigen und EUR-Lücke explizit als
   „nicht monetarisiert" kennzeichnen statt 0 anzuzeigen.
4. Konsistenz Karte <-> Dashboard: gleiche Daten, gleiche Botschaft. Entscheide dich
   für eine nachvollziehbare Farb-/Schwellenlogik (z. B. Karte färbt nach absolutem
   Indexwert 0–100 statt relativ zu Layer-Min/Max, plus Legende mit denselben
   Schwellen wie im Dashboard) und setze sie beidseitig um. Der Oschatz-Fall
   (Karte rot, Dashboard grün) darf danach nicht mehr auftreten können.
5. Risikoverteilung interaktiv: Im aufgeklappten Risiko-Abschnitt die variablen
   Parameter dieses Risikos (ref_value, ggf. Kostensatz, beteiligte Gewichte)
   anzeigen und direkt editierbar machen (bestehende Parameter-API/Override-Mechanik
   und ParameterTable-Bausteine wiederverwenden; nach Änderung Ergebnisse neu laden)
   (TODO Z. 7).
6. Backend liefert, was das Frontend braucht: erweitere aggregate()/risk_histogram()
   bzw. die Endpoints um die nötigen Felder (z. B. area_km2_affected, share_above_
   threshold, top5_share, sum_outcome). Keine Zell-Rohdaten-Massen ins Dashboard
   laden. Tests für neue Aggregatfelder ergänzen.

Verifikation: cd backend && python -m pytest tests/ -q grün; cd frontend && npm run
build grün; manuell mit einer berechneten Kommune: (a) ein Risiko mit wenigen
Extremzellen ist im Dashboard auf einen Blick als Handlungsbedarf erkennbar,
(b) Kartenfarbe und Dashboard-Aussage widersprechen sich nicht mehr, (c) Flächen-
angaben in km²/%, (d) Parameter im Risikoabschnitt änderbar mit Wirkung. Committe
in nachvollziehbaren Schritten (Backend-Felder, Kennzahlen, Radar, Karte-Konsistenz,
Interaktivität). Entferne die erledigten Punkte aus TODO.md (Z. 4, 5, 7, 17) und hake
in docs/PRODUKTREIFE_PROMPTS.md unter „Fortschritt" Prompt 7 ab.
```

---

## Prompt 8 — Dashboard-Einstieg: Klimaprofil-KPI-Leiste (~10 Kennzahlen vs. Deutschland)

**Modell:** Opus 4.8 · **Effort:** mittel · **Umfang:** M · **Plan-Modus:** nein · **Voraussetzung:** keine (jederzeit einschiebbar)

```
Du arbeitest im Repo /opt/lampp/htdocs/kap2 — KAP2, ein Klimarisiko-Analyse-Tool für
deutsche Kommunen. Backend: Python/FastAPI (backend/app), pytest; DWD-Rohdaten liegen
unter backend/data/dwd_cdc. Frontend: React 18 + TS + Vite (frontend/src), Recharts,
Zustand. UI-Sprache Deutsch. Nutze für die visuelle Gestaltung den dataviz-Skill,
falls verfügbar.
Hinweis: Zeilennummern Stand Juli 2026 — bei Abweichung per grep verifizieren.

ZIEL (Product Owner): „Im Dashboard sollten zum Einstieg allgemeine Parameter der
Kommune stehen, die ein Vorgefühl für Klimarisiken geben — sowas wie derzeitige
Temperatur, Regentage, Schneetage im Vergleich zum deutschen Durchschnitt. Rund
10 sinnvolle Kennzahlen, visuell gut aufbereitet, oberhalb der Zusammenfassung."

IST-ZUSTAND (verifizieren — vieles existiert schon ungenutzt):
- backend/app/services/climate/dwd_data.py: REGIONAL_CLIMATE je Bundesland (~Z. 65–80)
  mit hot_days_avg, snow_days_avg, tropical_nights_avg, summer_days_avg,
  summer_temp_avg, mean_temp_annual. KEINE Regentage, KEIN Deutschland-Eintrag.
- Zentroid-genaue Werte (hot_days, frost_days): backend/app/services/climate/
  dwd_cdc_grid.py.
- Endpoints existieren: /regional-climate, /climate-history, /climate-projection
  (backend/app/api/routes/assessment.py ~Z. 348–367). Store-Loader existieren:
  loadRegionalClimate/loadClimateHistory (frontend/src/store/index.ts ~Z. 285–298).
  ABER: Keine einzige Komponente konsumiert sie bisher.
- Dashboard: frontend/src/components/Dashboard.tsx; Kopfleiste = interne Komponente
  AssessmentBar (~Z. 90–164), darunter die Sektion „Zusammenfassung" (~Z. 196).
  KPI-Kachel-Muster existiert bereits (CSS-Klassen kpi-row/kpi-card/kpi-value,
  siehe Kostenzusammenfassung ~Z. 218–247).

AUFTRAG:
1. Neue Sektion „Klimaprofil <Kommune>" ZWISCHEN Kopfleiste und „Zusammenfassung",
   sichtbar auch OHNE abgeschlossene Risiko-Berechnung (Klimadaten sind unabhängig
   vom Assessment — die Sektion darf nicht hinter status==done hängen).
2. ~10 Kennzahlen, jeweils Kommune-Wert vs. Deutschland-Durchschnitt mit farbcodierter
   Abweichung (mehr Hitze/Trockenheit = warnfarben, Logik einheitlich) und kleinem
   Trend-Indikator wo Historie vorhanden. Pflicht-Kandidaten: Jahresmitteltemperatur,
   heiße Tage (>=30 °C), Sommertage (>=25 °C), Tropennächte, Frosttage, Schneetage,
   Regentage/Jahr, Jahresniederschlag, Erwärmungstrend seit Referenzperiode (aus
   /climate-history), Projektionswert 2050 (aus /climate-projection). Ersetze
   begründet, was aus den Daten nicht seriös ableitbar ist — keine Fantasiewerte.
3. Backend ergänzen: Regentage + Jahresniederschlag je Kommune (aus backend/data/
   dwd_cdc bzw. dwd_data-Erweiterung) und Deutschland-Referenzwerte (als klar
   belegte Konstanten mit Quelle DWD in backend/app/data/sources.py-Bibliografie
   oder berechnet). Endpoint /regional-climate entsprechend erweitern.
4. Jede Kachel bekommt einen (i)-Tooltip (bestehende InfoTooltip-Komponente) mit
   Definition der Kennzahl, Referenzperiode und Quelle (DWD). Responsives Layout
   (Grid), das mit 8–12 Kacheln funktioniert; dezente, konsistente Optik passend
   zum bestehenden kpi-card-Stil.
5. Laden über die existierenden Store-Loader (einmal je Kommune, gecacht im Store);
   Skeleton-/Ladezustand statt Layout-Springen.

Verifikation: cd backend && python -m pytest tests/ -q grün (Tests für neue
Kennzahlen/Endpoint-Felder ergänzen); cd frontend && npm run build grün; manuell:
Kommune ohne Berechnung öffnen -> Klimaprofil erscheint mit plausiblen Werten und
Tooltips; Kommune wechseln -> Werte aktualisieren. Committe Backend- und
Frontend-Anteil getrennt. Entferne die erledigten Punkte aus TODO.md (Z. 3 und 18)
und hake in docs/PRODUKTREIFE_PROMPTS.md unter „Fortschritt" Prompt 8 ab.
```

---

## Prompt 9 — Info-Fenster/Lineage-Redesign: Interaktionen, Filter-Semantik, Legende, Pfeilrichtungen, fehlende Operatoren

**Modell:** Fable 5 · **Effort:** hoch · **Umfang:** L · **Plan-Modus:** ja · **Voraussetzung:** Prompt 1 (Render-Loop-Fix); Prompt 3 empfohlen

```
Du arbeitest im Repo /opt/lampp/htdocs/kap2 — KAP2, ein Klimarisiko-Analyse-Tool für
deutsche Kommunen. Backend: Python/FastAPI (backend/app), pytest. Frontend: React 18 +
TS + Vite (frontend/src); das Herkunfts-/Wirkungsdiagramm („Info-Fenster" je Layer)
wird mit vis-network gerendert. UI-Sprache Deutsch.
Hinweis: Zeilennummern Stand Juli 2026 — bei Abweichung per grep verifizieren.

ARCHITEKTUR (verifizieren):
- Kette: MapDashboardTab.tsx -> LayerInfoModal.tsx (lädt GET /api/catalog/layer/
  {code}/recipe + Parameter) -> LineageFlowDiagram.tsx (~659 Z., vis-network, Physics
  aus, Positionen aus frontend/src/utils/lineageFilter.ts [treeLayout,
  assignColumnPositions, unfoldToTree] + lineageLayout.ts) -> LineageOperatorOverlays.tsx
  (HTML-Overlays für Operator-/Parameter-Boxen via network.canvasToDOM).
- Graphdaten baut das Backend: backend/app/services/lineage_graph.py (~1282 Z.,
  build_for_layer, Spaltenmodell column 0=Quellen, 1=Zwischenwerte, …,
  _wire_operator_chain). Kettendefinitionen: backend/app/data/lineage_operators.py
  (CELL_DIRECT, CELL_OPERATORS, formula_operators_for) und backend/app/data/
  pathway_descriptions.py. Knotentypen/Farben: frontend/src/utils/lineageColors.ts.
- Ansichts-Optionen heute: Modus „Kompakt"/„Aufgefächert" (mode-State ~Z. 312, Buttons
  ~Z. 606–624), Legenden-Chips als Typ-Filter (hiddenTypes ~Z. 314, Anwendung
  ~Z. 371–384), Spalten-Fokus per Knotenklick (nur Kompakt), Ketten ein-/ausklappen
  (nur Baum; expandAll/collapseAll ~Z. 494–499).

PROBLEME (Product Owner, mit konkreten Beispielen):
1. Die Kompakt-Ansicht soll ENTFERNT werden — es bleibt nur die aufgefächerte
   Baum-Ansicht (inkl. sauberem Ersatz/Entfall des Spalten-Fokus).
2. Filter sind zu statisch/kaputt: „Wenn ich nur wissen will, welche Quellen
   einfließen, kann ich zwar ‚nur Quellen und Ergebnis' auswählen, aber dann werden
   die Quellen nicht eingeblendet; und selbst wenn ich vorher alle Ketten ausgeklappt
   habe, zeigen keine Pfeile von den Quellen auf das Ergebnis." Das ist EIN Beispiel —
   durchdenke ALLE Kombinationen (Typ-Filter x Ein-/Ausklappen x Interaktionen)
   vollständig: Jede Kombination muss einen zusammenhängenden, lesbaren Graphen
   ergeben. Kernregel: Werden Knotentypen ausgeblendet, müssen die Kanten die Lücke
   TRANSITIV überbrücken (Quelle -> … -> Ergebnis als direkter Pfeil), niemals
   isolierte Knoten oder abreißende Pfade. Ausgeblendete eingeklappte Ketten dürfen
   Sichtbarkeit nicht aushebeln (Filter wirkt auf den entfalteten Graphen).
3. Legende passt nicht zum Canvas: Im Canvas sind H/V/E gestrichelt (weil eingeklappte
   Knoten borderDashes [4,3] bekommen, LineageFlowDiagram ~Z. 210), in der Legende
   nicht; das Index-Dashing wirkt mit [4,3] zu grob. Definiere je Knotentyp EINEN
   bewussten Stil (Form, Füllung, Rahmen, Dashing dezent) und rendere ihn IDENTISCH
   im Canvas und in der Legende (Legende ist bisher reines CSS in index.css —
   angleichen, ggf. Legenden-Swatches aus derselben Stildefinition generieren).
4. Elemente überlagern sich bis zur Unlesbarkeit (Operator-Overlays vs. Knoten vs.
   Kantenbeschriftung) — Layout-Abstände (treeLayout/estimateNodeWidth) und
   Overlay-Platzierung so überarbeiten, dass nichts kollidiert.
5. Falsche Richtungen und fehlende Operatoren (Beispiele vom Risiko „Erwartete
   jährliche Mortalität"):
   a) „OSM -> Grünfläche ermitteln -> Grünanteil" ist korrekt, aber direkt daneben
      „OSM -> Baumkronenanteil" OHNE Operator-Knoten — inkonsistent.
   b) „DWD -> Heiße Tage ermitteln -> Heiße Tage/Jahr -> Addition -> Begrenzen ->
      Skalierung", aber der Skalierungs-Operator steht ganz rechts und zeigt ZURÜCK
      nach links auf die Addition — inhaltlich falsch (dann würden rohe mit skalierten
      Werten addiert) und darstellerisch inakzeptabel.
   Diese Muster existieren an VIELEN Stellen. Prüfe systematisch ALLE Layer:
   Schreibe einen Backend-Test/Lint (pytest), der für jeden Layer-Code den Recipe-
   Graphen baut und hart prüft: (i) keine Kante zeigt gegen die Spaltenrichtung
   (nie „nach rechts zurück"), (ii) zwischen Quelle und Zwischenwert liegt immer ein
   Operator, (iii) keine verwaisten/unerreichbaren Knoten, (iv) Operator-Ketten sind
   sequenziell korrekt verdrahtet. Behebe alle Verstöße in lineage_graph.py/
   lineage_operators.py — unterscheide dabei Darstellungsfehler von inhaltlich
   falschen Kettendefinitionen (letztere fachlich korrekt reparieren, im Zweifel an
   docs/BERECHNUNGS_HANDBUCH.md orientieren). Der Lint bleibt als dauerhafter Test.
6. Falls es (nach dem Modell-Umbau) Monetarisierungs-Parameter risks.*.cost_per_outcome
   gibt: Sie erscheinen als Parameter-Knoten am Ergebnis, konsistent zum Rest.

VORGEHEN: Du bist im Plan-Modus — entwirf zuerst das Interaktionskonzept (Zustands-
matrix: welche Kontrollen gibt es nach Entfall des Kompakt-Modus, was zeigt der Graph
in jeder Kombination) und das einheitliche Stilsystem, DANN implementieren. Halte das
Konzept knapp in docs/LINEAGE_KONZEPT.md fest (Zielzustand, Regeln, Stiltabelle), damit
künftige Änderungen dagegen geprüft werden können.

Verifikation: cd backend && python -m pytest tests/ -q grün (inkl. neuem Graph-Lint
über alle Layer); cd frontend && npm run build grün; manuell am Beispiel „Erwartete
jährliche Mortalität": (a) nur Ergebnis+Quellen sichtbar -> Quellen sind da und
durchgehende Pfeile führen zum Ergebnis, (b) alle Ketten ausgeklappt -> keine
Überlappungen, alle Pfeile strikt links->rechts, (c) Legende entspricht 1:1 den
Canvas-Stilen, (d) OSM->Baumkronenanteil hat einen Operator, die Skalierungs-Kette
läuft vorwärts. Keine Console-Warnungen. Committe in nachvollziehbaren Schritten
(Backend-Lint+Fixes, Kompakt-Entfernung, Filter-Semantik, Stilsystem, Overlays).
Entferne die erledigten Punkte aus TODO.md (Z. 20–25) und hake in
docs/PRODUKTREIFE_PROMPTS.md unter „Fortschritt" Prompt 9 ab.
```

---

## Prompt 10 — Karten-Performance: Hintergrund-Preload, persistenter Browser-Cache, Aggregat-Persistenz, tote Dependencies

**Modell:** Opus 4.8 · **Effort:** hoch · **Umfang:** M–L · **Plan-Modus:** empfohlen · **Voraussetzung:** keine (jederzeit einschiebbar)

```
Du arbeitest im Repo /opt/lampp/htdocs/kap2 — KAP2, ein Klimarisiko-Analyse-Tool für
deutsche Kommunen. Backend: Python/FastAPI (backend/app), PostgreSQL/PostGIS, pytest.
Frontend: React 18 + TS + Vite (frontend/src), Zustand-Store, MapLibre-Karte.
UI-Sprache Deutsch.
Hinweis: Zeilennummern Stand Juli 2026 — bei Abweichung per grep verifizieren.

PROBLEM (Product Owner): „Die Ladezeiten sind immer noch viel zu lang. Alle Karten im
Hintergrund vorladen und speicherplatzsparend bereithalten; alle Daten in den
Browser-Cache — wir können nicht ewig warten, bis Karten laden." Zusätzlich: „Es
werden nur die Zell-Berechnungen gespeichert; die Dashboard-Ergebnisse sollten
ebenfalls gespeichert werden, ähnlich wie die Maßnahmen-Wirkungen."

IST-ZUSTAND (verifizieren):
- Layer laden lazy erst bei Auswahl: frontend/src/store/index.ts, setActiveLayer
  (~Z. 208–249); In-Memory-Cache nur im Zustand-Store (layerValueCache, gridGeometry)
  -> bei Seiten-Reload alles weg.
- Endpoints liefern gzip-JSON mit Cache-Control: no-cache (backend/app/api/routes/
  assessment.py, _gzip_json_response ~Z. 112–129): /kommune/{id}/grid-geometry
  (~211 KB gzip) und /kommune/{id}/layer/{code}/values (41–676 KB gzip je Layer).
  Der KOMPLETTE Layer-Satz einer Kommune liegt serverseitig vorgerechnet unter
  backend/.cache/layers/{kommune_id}/ (backend/app/services/layer_cache.py mit
  precompute() nach der Berechnung und invalidate()) und ist insgesamt nur ~3,5 MB
  gzip -> Komplett-Vorladen ist billig.
- Dashboard-Aggregate (risk-summary, cost-summary, risk-histogram) werden bei JEDEM
  Request neu aus den CellAssessment-Zeilen aggregiert (measure_service.
  get_risk_aggregate -> risk_engine.aggregate; Histogramm zählt live). Vorbild für
  Persistenz existiert: Maßnahmen-Wirkung wird in AdaptationMeasure.impact_summary
  (JSON) + Tabelle MeasureImpact gespeichert (backend/app/models/models.py
  ~Z. 132–155, geschrieben von measure_service.compute_impact).
- Tote Frontend-Dependencies (0 Importe in frontend/src, per grep verifizieren!):
  @deck.gl/core, @deck.gl/geo-layers, @deck.gl/layers, @deck.gl/mapbox, @deck.gl/react,
  @xyflow/react, @dagrejs/dagre, @nebula.gl/edit-modes, @nebula.gl/layers. Vorsicht:
  react-is kann Peer-Dependency von recharts sein — vor Entfernen prüfen.

AUFTRAG:
1. Hintergrund-Preload: Nach Laden der Geometrie alle Layer-Werte der aktiven Kommune
   im Hintergrund vorladen (Warteschlange, gedrosselt z. B. 2–3 parallel, niedrige
   Priorität, Abbruch bei Kommune-Wechsel; aktiver/angeklickter Layer hat immer
   Vorrang). Ziel: Nach wenigen Sekunden ist jeder Layer-Wechsel augenblicklich.
2. Persistenter Browser-Cache: Layer-Pakete + Geometrie in IndexedDB (saubere kleine
   Eigenlösung oder etablierte Minimal-Lib — begründe die Wahl) mit Cache-Key aus
   kommune_id + layer_code + Berechnungsstand. Als Berechnungsstand einen
   verlässlichen Versionsmarker verwenden (z. B. calculated_at des Assessments —
   falls der Status-Endpoint ihn nicht liefert, Backend minimal erweitern).
   Invalidierung: neue Berechnung/Kommune-Reset macht alte Einträge unbrauchbar
   (Versionsvergleich), alte Kommunen per einfachem LRU/Limit räumen —
   speicherplatzsparend, wir reden über wenige MB je Kommune.
3. HTTP-Caching überdenken: Cache-Control: no-cache ersetzen durch eine Strategie,
   die zum Versionsmarker passt (z. B. ETag/If-None-Match oder versionierte URL mit
   langem max-age). Konsistenz mit layer_cache.invalidate() sicherstellen.
4. Dashboard-Aggregate persistieren (Vorbild impact_summary): risk-summary/
   cost-summary/histogram nach Abschluss der Berechnung einmal berechnen und
   speichern (neue Tabelle oder JSON-Spalte + Alembic-Migration), Endpoints liefern
   das Gespeicherte; Invalidierung bei Neu-Berechnung und bei Parameter-Overrides,
   die Ergebnisse ändern (prüfe, wo Overrides heute Neuberechnungen triggern —
   Aggregate müssen dem folgen, sonst zeigt das Dashboard veraltete Werte).
5. Tote Dependencies entfernen (Liste oben, jede einzeln per grep verifizieren),
   package-lock aktualisieren, npm run build muss danach fehlerfrei sein. Notiere
   Bundle-Größe vorher/nachher (vite build Ausgabe) im Commit-Text.
6. Miss Ladezeiten vorher/nachher (Netzwerk-Tab oder curl-Timings für Geometrie +
   3 große Layer; Kalt- und Warm-Start) und dokumentiere die Zahlen im Commit-/
   PR-Text. Keine gefühlten Verbesserungen — Zahlen.

Verifikation: cd backend && python -m pytest tests/ -q grün (Tests für Aggregat-
Persistenz + Invalidierung ergänzen); cd frontend && npm run build grün; manuell:
(a) Kommune öffnen, kurz warten, durch 10 Layer klicken -> keine Ladepausen,
(b) Seite neu laden -> Karte + Dashboard sofort da (aus IndexedDB/persistierten
Aggregaten), (c) Neu-Berechnung -> alle Ansichten zeigen frische Werte (keine
Stale-Daten). Committe in Schritten (Preload, IndexedDB, HTTP-Caching, Aggregat-
Persistenz, Dependency-Cleanup). Entferne die erledigten Punkte aus TODO.md
(Z. 2, 6, 26) und hake in docs/PRODUKTREIFE_PROMPTS.md unter „Fortschritt"
Prompt 10 ab.
```

---

## Abdeckungs-Matrix (TODO.md ↔ Prompts)

| TODO.md-Zeile(n) | Punkt | Prompt |
|---|---|---|
| 1 | Falsche „keine Berechnung"-Meldung → Lade-Hinweis | 1 |
| 2 | Dashboard-Ergebnisse persistieren | 10 |
| 3 | Allgemeine Klima-Parameter vs. Deutschland-Schnitt | 8 |
| 4 | Betroffene Fläche statt Zellen + Geldwert | 7 |
| 5 | Je Risiko ein Absolutwert-Diagramm | 7 |
| 6 | Alle Daten in Browser-Cache | 10 |
| 7 | Parameter in Risikoverteilung einseh-/änderbar | 7 |
| 9 | Alle Parameter beschrieben (UI + Excel) | 6 |
| 10 | Unklare Quellen („X / Modellannahme") | 5 |
| 11 | Fehlende Zitate (Winklmayr) | 5 |
| 12–14 | Quellen-Benennung, Author-Year-Stil | 4 |
| 15 | Infofenster nur zum eigenen Parameter | 6 |
| 16 | EAD = Summe, alles monetarisieren | 3 |
| 17 | Dashboard beschönigt (Oschatz-Beispiel) | 7 |
| 18 | Einstiegs-KPIs im Dashboard | 8 |
| 19 | Kritische Modell-Einschätzung | 2 |
| 20–25 | Info-Fenster/Lineage-Mängel | 9 |
| 26 | Ladezeiten / Vorladen | 10 |
| 27–44 | „Maximum update depth exceeded" | 1 |

## Weitere Prompts aus Produkt-Review

_Reserviert: Wird nach einem eigenständigen Produkt-Review (separater Arbeitsschritt,
auf Zuruf) mit zusätzlichen Prompts im selben Format gefüllt._
