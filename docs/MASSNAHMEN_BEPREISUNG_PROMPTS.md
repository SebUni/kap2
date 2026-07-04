# Maßnahmen-Bepreisung — Sessions

Zerlegung von `docs/MASSNAHMEN_BEPREISUNG.md` in 13 eigenständige, copy-paste-fertige
Claude-Code-Sessions. Reihenfolge = Abhängigkeit (nicht überspringen: 2 braucht 1,
3–4 brauchen 2, 5 braucht 3, 6 braucht 2 (läuft parallel zu 3–5), 7 braucht 3–6).

## Wie du eine Session startest

1. **Neue Session** (frischer Kontext, nicht in einer laufenden weiterarbeiten).
2. Modell setzen: `/model sonnet` bzw. `/model opus` (siehe Tabelle je Prompt) — als
   eigene Eingabe, bevor du den Prompt-Block einfügst.
3. Den ganzen Codeblock der Session copy-pasten und abschicken. Denk-Trigger
   (`think` / `think hard` / `ultrathink`) und ggf. die Plan-Anweisung stehen
   bereits im Text — nichts weiter nötig.
4. Nach Abschluss: committen lassen ("committe das mit einer passenden Nachricht"),
   dann neue Session für den nächsten Block.

| # | Session | Modell | Denken | Planen zuerst | Abhängig von |
|---|---|---|---|---|---|
| 1 | Legacy-Cleanup | Sonnet | ohne | nein | — |
| 2 | Katalog-Migration (Struktur, Zahlen unverändert) | Sonnet | think | nein | 1 |
| 3 | Backend-Logik: measure_service.py | Opus | ultrathink | **ja** | 2 |
| 4 | Backend: parameter_registry.py + schemas.py + Export | Sonnet | think hard | ja | 3 |
| 5 | Frontend: Typen, Modal, Sidebar, Tabellen | Sonnet | think | ja | 4 |
| 6a–6g | Recherche-Pass, 7 Batches (KAnG-Cluster) | Sonnet | think | nein | 2 |
| 7 | Doku + Tests + E2E | Sonnet | think | nein | 3–6 |

Batches 6a–6g sind gegenseitig unabhängig (können in beliebiger Reihenfolge oder
parallel in mehreren Fenstern laufen), solange Session 2 committed ist.

---

## Session 1 — Legacy-Cleanup

```
Kontext: Klimarisiko-Tool, Repo /opt/lampp/htdocs/kap2. Plan: docs/MASSNAHMEN_BEPREISUNG.md.
Rahmenmethodik (H·E·V, Risiko-Engine) NICHT anfassen — nur dieser Block.

Umsetzen: Verifiziere zuerst, dass keines der folgenden Module irgendwo importiert wird
(grep -rn "climate\.\(heat\|drought\|flood\|storms\|forest_fire\|river_flood\|heavy_rain\|agriculture\|sea_level\)\.measures" backend/):
  backend/app/services/climate/heat/measures.py
  backend/app/services/climate/drought/measures.py
  backend/app/services/climate/heavy_rain/measures.py (falls vorhanden)
  backend/app/services/climate/river_flood/measures.py
  backend/app/services/climate/storms/measures.py
  backend/app/services/climate/forest_fire/measures.py
  backend/app/services/climate/agriculture/measures.py
  backend/app/services/climate/sea_level/measures.py
Falls ein Treffer existiert (außerhalb des Moduls selbst und außerhalb von Tests, die
explizit dieses Legacy-Modul testen) — stoppen und mir den Fund melden, nicht löschen.
Sonst: alle 8 Dateien löschen. Prüfe, ob dadurch leere Verzeichnisse entstehen; wenn ja,
diese ebenfalls entfernen. Bestehende Tests müssen weiter grün sein:
python -m pytest backend/tests/.

Akzeptanz: Legacy-Module weg, keine Importfehler, bestehende Tests grün. Danach committen.
```

---

## Session 2 — Katalog-Migration (Struktur, Zahlen unverändert)

```
Kontext: Klimarisiko-Tool, Repo /opt/lampp/htdocs/kap2. Plan: docs/MASSNAHMEN_BEPREISUNG.md
Abschnitt 1 ("Neues Katalog-Schema") + Abschnitt 7 Schritt "Katalog-Struktur".
Rahmenmethodik (H·E·V, Risiko-Engine, benefit_per_m2_year, default_reduction-Werte)
NICHT ändern — nur Struktur, keine Zahlen außer den zwei explizit neuen Trinkbrunnen-Werten.

think

Umsetzen in backend/app/data/catalog.py (MEASURES, ab Zeile ~887):
1. Jede der 46 bestehenden Maßnahmen bekommt die neuen Felder:
   cost_fixed, cost_per_unit, cost_per_m2, maintenance_per_unit_year,
   maintenance_per_m2_year, unit_label, unit_density_per_ha, source, sources.
   Nicht anwendbar = None (nicht 0.0 — 0.0 heißt "anwendbar, aber kostenlos").
   Bestehende Werte (default_reduction, cost_per_m2 usw.) NICHT verändern, nur umsortieren:
   - Reine Flächenmaßnahmen (26 Stück): cost_fixed: 0.0, alle Stückfelder None.
   - Bisherige Pauschal-cost_per_unit-Maßnahmen aufteilen:
     - Konzept-/Planungsmaßnahmen (z.B. HEAT_ACTION_PLANS, EVACUATION_EMERGENCY_PLANS,
       EARLY_WARNING_MEASURE — finde alle mit reinem cost_per_unit ohne physische Stückzahl-
       Semantik): Wert wandert nach cost_fixed, Stückfelder bleiben None.
     - Echte Stück-Maßnahmen (z.B. GRID_REINFORCEMENT_REDUNDANCY → "Station",
       CRITICAL_NODE_PROTECTION → "Knoten", LEVEE_REINFORCEMENT → "km",
       SALTWATER_BARRIERS → "Anlage" — finde alle mit physischer Zähleinheit):
       unit_label setzen + unit_density_per_ha als vorläufige Modellannahme (plausibler
       Schätzwert, im sources-Kommentar als "Modellannahme (Richtwert-Dichte, unbelegt)"
       kennzeichnen — die echte Recherche kommt in einem späteren Schritt).
   - source: vorläufig überall "Modellannahme (Maßnahmenkosten, unbelegt)" (echte Quellen
     kommen im Recherche-Pass); sources: {} vorerst leer oder mit demselben Platzhalter je
     gesetztem Feld.
2. Trinkbrunnen-Split: bestehende COOLING_ROOMS_DRINKING_WATER behalten (DB-Kompatibilität),
   umbenennen zu "Kühle Räume / Kühlzentren" (unit_label: "Raum"). Neue Maßnahme
   DRINKING_FOUNTAINS ("Trinkbrunnen") als 47. Eintrag hinzufügen:
     cost_fixed: 5000.0, cost_per_unit: 14000.0, cost_per_m2: None,
     maintenance_per_unit_year: 3500.0, maintenance_per_m2_year: None,
     unit_label: "Brunnen", unit_density_per_ha: 0.5,
     source: "Berliner Wasserbetriebe / Modellannahme",
     sources: {"cost_per_unit": "Berliner Wasserbetriebe (Praxiswerte Trinkbrunnen)",
               "maintenance_per_unit_year": "Berliner Wasserbetriebe (Betrieb/Wartung/Beprobung)"}
   Mit Herleitungskommentaren direkt über dem Eintrag:
     # Herleitung cost_per_unit: Berliner Wasserbetriebe: Errichtung inkl. Trinkwasser-
     # anschluss ~10-16 T€/Standort → Punktwert 14.000 €.
     # Herleitung maintenance_per_unit_year: Betrieb/Wartung/Beprobung ~2,5-5 T€/a → 3.500 €.
   effect_target/default_reduction/coverage_scaling/linked_risk_codes sinnvoll analog zu
   COOLING_ROOMS_DRINKING_WATER wählen (Gesundheit/Hitze-Cluster).
   In parameter_registry.py oder wo _MEASURE_KANG_MAP definiert ist: Eintrag
   "DRINKING_FOUNTAINS": ("health", "health") ergänzen.
3. Kommentarblock catalog.py:875-886 (Konventions-Doku über MEASURES) auf die neuen
   Felder/Formeln aktualisieren (kurz, keine Redundanz zum Handbuch).

Arbeite Maßnahme für Maßnahme mit dem Edit-Tool (nicht die ganze Datei neu schreiben).
Falls der Kontext eng wird: nach den ersten ~23 Einträgen zwischendurch committen und
in derselben Session mit den restlichen ~24 fortfahren.

Akzeptanz: 47 Maßnahmen mit vollständigem neuem Feldset (gesetzt oder None); kein
bestehender default_reduction/cost_per_m2/cost_per_unit-Wert hat sich geändert außer den
beiden neuen Trinkbrunnen-Werten; GET /api/catalog liefert die neuen Felder.
Bestehende Tests bleiben grün (measure_service.py liest die neuen Felder noch nicht —
das ist Session 3). Danach committen.
```

---

## Session 3 — Backend-Logik: measure_service.py

```
Kontext: Klimarisiko-Tool, Repo /opt/lampp/htdocs/kap2. Plan: docs/MASSNAHMEN_BEPREISUNG.md
Abschnitt 2 ("Backend") Unterpunkt measure_service.py.
Voraussetzung: Session 2 (Katalog-Migration) ist bereits committed — catalog.py MEASURES
hat schon cost_fixed/cost_per_unit/cost_per_m2/maintenance_per_unit_year/
maintenance_per_m2_year/unit_label/unit_density_per_ha/source/sources.
Rahmenmethodik (H·E·V, risk_engine, benefit_per_m2_year-Nutzenseite) NICHT ändern —
nur die Kosten-/Wirkungs-Berechnung in measure_service.py.

ultrathink

Erstelle zuerst einen kurzen Plan (welche Funktionen du wo einfügst/änderst, welche
Signaturen sich ändern, welche Aufrufer betroffen sind) und zeig ihn mir, bevor du Code
änderst. Warte auf meine Bestätigung ("go").

Nach Bestätigung umsetzen in backend/app/services/measure_service.py:
1. Neuer Helfer _resolve_count(mdef, config, covered_area_m2) -> tuple[int, bool, int]:
   (count, is_default, recommended_count). Wenn config.get("count") fehlt: recommended_count
   = max(1, round(mdef["unit_density_per_ha"] * covered_area_m2 / 10_000)) als Default,
   is_default=True. Für Flächenmaßnahmen (unit_label is None): count=0 (ungenutzt),
   is_default=False, recommended_count=0.
2. Neuer Helfer _unit_effect_factor(count, recommended_count) -> float:
   min(1.0, count / recommended_count) falls recommended_count > 0, sonst 1.0.
3. Neuer Helfer compute_costs(mdef, count, area_m2) -> dict (cost_breakdown-Rohdaten:
   investment total + components-Liste, annual_maintenance total + components-Liste;
   jede Komponente nur wenn das zugehörige Feld nicht None ist):
   investment = cost_fixed + count * cost_per_unit + area_m2 * cost_per_m2 (None-Felder
   überspringen, nicht als 0 rechnen außer sie sind explizit 0.0)
   annual_maintenance = count * maintenance_per_unit_year + area_m2 * maintenance_per_m2_year
   Jede Komponente: {param, label, unit_price, quantity, quantity_unit, amount_eur, source,
   overridden}. source = custom_source falls Override vorliegt, sonst
   mdef["sources"].get(field) or mdef["source"]; overridden = bool(custom_source vorhanden).
4. _reduction_factor(mdef, fraction, unit_factor=1.0) (bisher Zeile ~50-59) erweitern:
   r = base_r * s(fraction) * unit_factor (bestehende s(fraction)-Logik/coverage_scaling
   unverändert lassen, nur den zusätzlichen Faktor multiplizieren).
5. compute_impact (bisher Zeile ~62-170) umstrukturieren: Fläche zuerst über die
   coverage-Zellen aufsummieren (covered_area_m2), dann count/unit_factor via
   _resolve_count + _unit_effect_factor bestimmen, dann erst die Delta-Schleife über die
   Zellen mit dem so bestimmten unit_factor durchführen. Response um zusätzliche Felder
   erweitern: count, count_is_default, recommended_count, unit_label, cost_breakdown
   (aus compute_costs). Bisherige Summenfelder (Investition/Unterhalt/Nutzen gesamt)
   bleiben zusätzlich bestehen, jetzt aus cost_breakdown-Totalen gespeist statt aus der
   alten Pauschalformel. MeasureImpact.costs (erste befüllte Zelle) um breakdown + count
   ergänzen.
6. _adjusted_cell_data (bisher Zeile ~173-199) synchron halten: dieselbe Fläche+count+
   unit_factor-Bestimmung hier ebenfalls durchführen und an _reduction_factor
   durchreichen, damit Dashboard ("mit Maßnahmen") und Sidebar nicht auseinanderlaufen.
   Empfehlung aus dem Plan: _coverage liefert künftig (frac_map, covered_area_m2) statt
   nur frac_map — alle Aufrufer anpassen.
7. config wird jetzt tatsächlich gelesen (config["count"]) statt immer {} zu erwarten —
   prüfe, ob das Frontend das schon sendet (aktuell nicht, das kommt in Session 5); bis
   dahin muss der Default-Pfad (is_default=True) korrekt greifen.

Nutze parameter_registry.resolve_measure_def, um Overrides (custom_source, geänderte
Werte) einzubeziehen, bevor du count/costs berechnest — dieselbe Konvention wie bisher.

Akzeptanz: bestehende Tests grün (python -m pytest backend/tests/) ODER, wo sie die alte
Formel direkt prüfen, bewusst und nachvollziehbar angepasst (Kommentar warum). Eine
manuelle Prüfung: Flächenmaßnahme ohne unit_label rechnet zahlenmäßig identisch zur alten
Formel (cost_per_m2 * Fläche + maintenance_per_m2_year * Fläche, jetzt zusätzlich +
cost_fixed, was bei Flächenmaßnahmen 0.0 ist). Trinkbrunnen mit count=5 ⇒ Investition
5.000 + 5×14.000 = 75.000 €, Unterhalt 5×3.500 = 17.500 €/a (rechne das im Kopf/mit einem
Testaufruf nach, bevor du fertig meldest). Danach committen.
```

---

## Session 4 — parameter_registry.py + schemas.py + Export

```
Kontext: Klimarisiko-Tool, Repo /opt/lampp/htdocs/kap2. Plan: docs/MASSNAHMEN_BEPREISUNG.md
Abschnitt 2 ("Backend") Unterpunkte parameter_registry.py + cost_breakdown-Shape +
"Sonstiges Backend". Voraussetzung: Session 3 (measure_service.py: _resolve_count,
_unit_effect_factor, compute_costs, erweiterte compute_impact-Response) ist committed.
Rahmenmethodik NICHT ändern — nur Registry/Schema/Export für die neuen Kostenfelder.

think hard

Erstelle zuerst kurz einen Plan (welche neuen Pydantic-Modelle, wie sie mit
measure_service.compute_costs-Output zusammenpassen) und zeig ihn mir vor der Umsetzung.

Nach Bestätigung umsetzen:
1. backend/app/services/parameter_registry.py:
   - MEASURE_PARAM_SPECS (bisher Zeile ~22-28) auf 8 Einträge erweitern: bestehende 5 +
     cost_fixed ("Fixkosten", "€"), maintenance_per_unit_year
     ("Wartungskosten pro Einheit und Jahr", "€/(Stück·a)"), unit_density_per_ha
     ("Richtwert-Dichte", "Stück/ha"). MEASURE_OVERRIDE_FIELDS bezieht sich automatisch
     mit (ist ein tuple-comprehension über MEASURE_PARAM_SPECS) — prüfen, dass das noch
     stimmt. resolve_measure_def selbst muss nicht geändert werden, wenn es generisch über
     MEASURE_OVERRIDE_FIELDS iteriert (verifizieren).
   - Die Emissions-Stelle für Maßnahmen-Parameter (bisher Zeile ~156-170): source =
     m["sources"].get(field) or m["source"] or "Modellannahme (Maßnahmenkosten, unbelegt)".
     applicable = m.get(field) is not None. Wenn nicht anwendbar: value=0.0, editable=False,
     applicable=False. Dafür muss der zugrunde liegende _base_param-Helfer (oder wie er
     heißt) um ein applicable-Feld erweitert werden — an allen Aufrufstellen mit
     applicable=True als Default ergänzen, damit Hazard/Risk-Parameter (die das Feld nicht
     kennen) nicht brechen.
2. backend/app/schemas/schemas.py: neue Pydantic-Modelle CostComponent, CostBlock,
   EffectScaling, CostBreakdown gemäß dieser Shape:
     CostComponent: param, label, unit_price, quantity, quantity_unit, amount_eur, source,
       overridden
     CostBlock: total_eur, components: list[CostComponent]
     EffectScaling: unit_factor, count, recommended_count, density_per_ha, source
     CostBreakdown: investment: CostBlock, annual_maintenance: CostBlock,
       effect_scaling: EffectScaling
   In das Response-Schema für MeasureImpact (oder wo compute_impact seriali siert wird)
   cost_breakdown: CostBreakdown | None sowie count, count_is_default, recommended_count,
   unit_label als neue optionale Felder einfügen.
3. ModelParameter-Schema (Parameter-API-Response) um applicable: bool | None ergänzen.
4. export_service.py: Export-Spalten "Anzahl"/"Einheit" ergänzen (aus count/unit_label).
   Beim Import: bestehendes positional row[:7]-Parsing beibehalten, count zusätzlich aus
   der neuen Spalte lesen (Round-Trip über die Konfigurations-JSON, keine Schema-Änderung
   an der DB nötig).
5. Kompat-Check: SELECT * FROM config_parameters (oder das ORM-Äquivalent) WHERE
   parameter_id LIKE 'measures.%' — liste alle bestehenden Overrides, deren Wert nach der
   Migration in Session 2 von cost_per_unit nach cost_fixed gewandert ist (Konzept-
   maßnahmen). Für diese Fälle: gib mir eine Liste (kein automatisches Umschreiben ohne
   Rückfrage, das sind Kundendaten).

Akzeptanz: neue Pydantic-Modelle validieren den Output aus measure_service.compute_costs
(kurzer manueller Testaufruf); GET /kommune/{id}/parameters zeigt applicable korrekt;
bestehende Tests grün. Danach committen.
```

---

## Session 5 — Frontend: Typen, Create-Modal, Sidebar, Tabellen

```
Kontext: Klimarisiko-Tool, Repo /opt/lampp/htdocs/kap2. Plan: docs/MASSNAHMEN_BEPREISUNG.md
Abschnitt 3 ("Frontend"). Voraussetzung: Session 4 (Backend liefert cost_breakdown,
count, count_is_default, recommended_count, unit_label, applicable) ist committed —
prüfe die tatsächliche Response von GET /api/catalog und dem Impact-Endpunkt, bevor du
Frontend-Typen schreibst.

think

Kurzer Plan zuerst (welche Komponenten betroffen, welche UI-States neu), dann umsetzen:
1. types/index.ts: CatalogMeasure um die neuen Felder erweitern (number | null wo
   nicht anwendbar sein kann), MeasureImpactSummary um count, count_is_default,
   recommended_count, unit_label, cost_breakdown, ModelParameter um applicable?: boolean.
2. MapView.tsx, MeasureCreateModal (~Zeile 679-862): wenn die gewählte Maßnahme
   unit_label hat, ein Eingabefeld "Anzahl (<unit_label>)" anzeigen, vorbelegt mit dem
   Richtwert aus der vorhandenen Flächenberechnung (~715-730 nutzt bereits die
   Polygonfläche) + Hinweistext "Richtwert: X für Y ha". handleSave sendet
   config: {count}. Darunter eine kleine clientseitige Kostenvorschau
   ("Schätzung, Katalogwerte") aus cost_fixed/cost_per_unit/cost_per_m2 — rein informativ,
   keine Serverlogik duplizieren, nur die Katalogwerte direkt aus CatalogMeasure lesen.
3. MeasureSidebar.tsx: Anzahl editierbar machen (gleiches Muster wie das bestehende
   Umsetzungsjahr-Feld, danach calculateImpact erneut aufrufen). Kosten-Karte
   (~Zeile 135-153) um eine aufklappbare "Herleitung anzeigen"-Sektion erweitern: pro
   cost_breakdown-Komponente eine Zeile "<quantity> × <unit_price>/<quantity_unit> =
   <amount_eur> €" + Quelle (gedämpfte Schrift) + "Override"-Badge wenn overridden.
   Nutze InfoTooltip (note-Prop, falls noch nicht verwendet — erste Nutzungsstelle) am
   Kosten-Titel. Wirkungs-Karte: wenn unit_factor < 1, Hinweis "Wirkung auf X % skaliert
   (<count> von <recommended_count> <unit_label>)"; wenn count_is_default, Badge
   "Anzahl = Richtwert".
4. ParameterTable.tsx: applicable === false ⇒ Zeile ausgrauen, Wert "—", Quelle
   "nicht anwendbar" anzeigen (Edit-Button entfällt schon automatisch über editable:
   false, prüfen dass das weiterhin so greift).
5. MeasuresTableTab.tsx: neue Spalte "Anzahl".

Akzeptanz: `npm run build` (bzw. das Projekt-Äquivalent) fehlerfrei; manuell im Browser
(Dev-Server starten): Polygon zeichnen, Trinkbrunnen als Maßnahme wählen, Anzahl-Feld
erscheint mit Richtwert-Vorbelegung, Sidebar zeigt Kosten-Herleitung mit Quellen nach dem
Speichern. Melde explizit, dass du es im Browser getestet hast (nicht nur Build). Danach
committen.
```

---

## Session 6a — Recherche: Stadt/Hitze

```
Kontext: Klimarisiko-Tool, Repo /opt/lampp/htdocs/kap2. Plan: docs/MASSNAHMEN_BEPREISUNG.md
Abschnitt 4 ("Recherche-Pass"), Batch "Stadt/Hitze". Voraussetzung: Session 2
(Katalog-Migration) ist committed — catalog.py MEASURES hat schon cost_fixed/
cost_per_unit/cost_per_m2/maintenance_per_unit_year/maintenance_per_m2_year/unit_label/
unit_density_per_ha/source/sources mit Platzhalter "Modellannahme (Maßnahmenkosten,
unbelegt)". Rahmenmethodik/default_reduction NICHT anfassen — nur source/sources +
ggf. unit_density_per_ha für die Maßnahmen dieses Batches.

think

Umsetzen: Finde alle Maßnahmen im Katalog aus dem KAnG-Cluster "health"/Stadt-Hitze
(Trinkbrunnen, Stadtgrün, Beschattung, Hitzeaktionspläne, Kühlräume/Kühlzentren — grep
nach _MEASURE_KANG_MAP-Einträgen mit "health" oder ähnlichen Codes wie HEAT_*, COOLING_*,
DRINKING_FOUNTAINS, URBAN_GREENING, SHADING_*, HEAT_ACTION_PLANS). Für jede Maßnahme
dieses Batches per WebSearch belastbare Kostenkennwerte recherchieren, Anker:
Berliner Wasserbetriebe, UBA/BMUV-Praxishilfen zu Hitzeaktionsplänen, difu
(Deutsches Institut für Urbanistik), GALK (Stadtbaumkosten/Straßenbaumkataster).
Format je belegtem Feld (Konvention wie bei RISKS/HAZARDS in catalog.py):
  # Herleitung <feld>: <Beleg mit Quelle, Jahr, Spanne> → Punktwert <X> €.
plus Kurz-Key in sources[<feld>]. Ohne belastbaren Beleg ehrlich
"Modellannahme (mangels belastbarer Quelle)" stehen lassen, NICHT erfinden.
Trinkbrunnen (DRINKING_FOUNTAINS) hat bereits Platzhalterwerte aus Session 2 — hier bei
Bedarf verifizieren/verfeinern, nicht neu erfinden falls schon belegt.
Auch unit_density_per_ha für Stück-Maßnahmen dieses Batches recherchieren/plausibilisieren
(meist Modellannahme — dann im Kommentar begründen warum dieser Wert plausibel ist,
z.B. Referenz auf ein städtisches Hitzeaktionsplan-Konzept).
default_reduction bleibt unangetastet, bekommt nur den ehrlichen sources-Eintrag falls
dafür eine Quelle auffindbar ist.

Akzeptanz: jede Maßnahme dieses Batches hat ein nicht-generisches source-Feld ODER
explizit "Modellannahme (mangels belastbarer Quelle)"; jeder belegte Zahlenwert hat einen
Herleitungskommentar direkt darüber. Bestehende Tests bleiben grün. Danach committen.
```

---

## Session 6b — Recherche: Gebäude/Begrünung

```
[Wie Session 6a, aber Batch "Gebäude/Begrünung" ersetzen:]
Batch "Gebäude/Begrünung" (Gründach, Cool Roofs, Objektschutz, Fassadenbegrünung,
bauliche Nachrüstung). Anker: BuGG-Marktreport (Bundesverband GebäudeGrün), KfW-
Förderprogramme (energieeffizientes Bauen/Sanieren), BBK-Hochwasserschutzfibel
(für Objektschutz-Maßnahmen mit Hochwasserbezug).
```

---

## Session 6c — Recherche: Wasser/Starkregen

```
[Wie Session 6a, aber Batch "Wasser/Starkregen" ersetzen:]
Batch "Wasser/Starkregen" (Entsiegelung, Mulden/Rigolen, Retentionsflächen,
Leckage-/Netzsanierung). Anker: DWA-A 138 (Arbeitsblatt Planung/Bau/Betrieb von
Versickerungsanlagen, Kostenkennwerte), Hamburg RISA (Regeninfrastrukturanpassung),
LANUV NRW, DVGW (Wasserfach).
```

---

## Session 6d — Recherche: Küste/Fluss

```
[Wie Session 6a, aber Batch "Küste/Fluss" ersetzen:]
Batch "Küste/Fluss" (Deichverstärkung €/km, Sturmflutbarrieren, Auenrenaturierung).
Anker: NLWKN/MELUND-Richtwerte (Niedersachsen/Schleswig-Holstein Küstenschutz), IKSR
(Internationale Kommission zum Schutz des Rheins), BfN (Bundesamt für Naturschutz,
Auen-Renaturierungskosten).
```

---

## Session 6e — Recherche: Land-/Forstwirtschaft

```
[Wie Session 6a, aber Batch "Land-/Forstwirtschaft" ersetzen:]
Batch "Land-/Forstwirtschaft" (Waldumbau, Bewässerungseffizienz, Bodenschutz-
Maßnahmen). Anker: KTBL-Kostenkennwerte (Kuratorium für Technik und Bauwesen in der
Landwirtschaft), LfL Bayern (Landesanstalt für Landwirtschaft), Landesforsten-
Waldumbausätze (je Bundesland, z.B. Niedersächsische Landesforsten).
```

---

## Session 6f — Recherche: Energie/Wirtschaft

```
[Wie Session 6a, aber Batch "Energie/Wirtschaft" ersetzen:]
Batch "Energie/Wirtschaft" (Netzverstärkung, dezentrale Energie, Betriebs-
Resilienzmaßnahmen). Anker: BNetzA/dena (Bundesnetzagentur, Deutsche Energie-Agentur),
HTW-Stromspeicher-Inspektion (HTW Berlin, jährlicher Marktreport). Organisatorische
Maßnahmen (Notfallpläne, Redundanz-Konzepte) bleiben meist "Modellannahme" — das ist hier
der erwartete, ehrliche Regelfall, nicht ein Rechercheversagen.
```

---

## Session 6g — Recherche: Bevölkerungsschutz, Fischerei

```
[Wie Session 6a, aber Batch "Bevölkerungsschutz, Fischerei" ersetzen:]
Batch "Bevölkerungsschutz, Fischerei" (Evakuierungspläne, Frühwarnsysteme,
Fischereibewirtschaftung, Laichhabitat-Renaturierung — ADAPTIVE_FISHERIES_MANAGEMENT,
FISH_PASSAGE_RESTORATION, AQUACULTURE_RESILIENCE_SYSTEMS,
FISHERIES_SPAWNING_HABITAT_RESTORATION, FISHERIES_WATER_QUALITY_PROTECTION u.ä., siehe
catalog.py ab Zeile ~1093). Anker: BBK (Bundesamt für Bevölkerungsschutz und
Katastrophenhilfe), kommunale Praxisberichte. Überwiegend "Modellannahme" erwartet —
ehrlich kennzeichnen statt erfinden.
```

---

## Session 7 — Doku, Tests, E2E

```
Kontext: Klimarisiko-Tool, Repo /opt/lampp/htdocs/kap2. Plan: docs/MASSNAHMEN_BEPREISUNG.md
Abschnitt 5+6 ("Doku", "Verifikation"). Voraussetzung: Sessions 2-5 sind committed
(neues Katalogschema, Backend-Logik, Frontend). Die Recherche-Batches 6a-6g müssen NICHT
alle fertig sein — Platzhalter-Sources sind für die Tests hier ausreichend.

think

Umsetzen:
1. docs/BERECHNUNGS_HANDBUCH.md §7 ("Maßnahmen"): neue Wirkungs- und Kostenformeln
   (Investition = cost_fixed + Anzahl×cost_per_unit + Fläche×cost_per_m2; Unterhalt/a =
   Anzahl×maintenance_per_unit_year + Fläche×maintenance_per_m2_year; r_eff = clamp(r_default
   · s(coverage) · u, 0, 0.95) mit u = min(1, Anzahl/Richtwert-Anzahl)) dokumentieren,
   None-Konvention erklären, sources-Konvention (wie bei RISKS) übernehmen,
   cost_breakdown-Response-Shape zeigen. §9 (API-Tabelle) um die neuen Felder ergänzen.
2. Neue Datei backend/tests/test_measure_pricing.py (Stil wie
   backend/tests/test_review_wirkungsmechanismen.py — lies diese Datei zuerst als
   Vorbild, DB-frei über die reinen Helferfunktionen):
   - Katalog-Konsistenz: alle 47 Maßnahmen vollständig (jedes Feld gesetzt oder bewusst
     None); unit_label impliziert unit_density_per_ha gesetzt + mind. ein
     Stück-Kostenfeld gesetzt; jede Maßnahme hat ein source-Feld; alle Keys in sources
     sind gültige Feldnamen; keine negativen Zahlenwerte.
   - compute_costs: Trinkbrunnen mit count=5 ⇒ Investition 5.000 + 5×14.000 = 75.000 €,
     Unterhalt 17.500 €/a; eine reine Flächenmaßnahme rechnet identisch zur Altformel
     (cost_per_m2 × Fläche + maintenance_per_m2_year × Fläche, cost_fixed=0); Felder mit
     None erzeugen keine Kostenkomponente; overridden-Flag korrekt bei einem
     custom_source-Override.
   - _resolve_count/_unit_effect_factor: Richtwert wird als Default übernommen wenn
     config["count"] fehlt; min(1, count/recommended) korrekt; Faktor exakt 1 für
     Flächenmaßnahmen (unit_label is None).
   - Registry: 8 Parameter-Specs je Maßnahme vorhanden; applicable/editable konsistent
     mit None-Feldern; resolve_measure_def wendet alle 8 Override-Felder an.
3. python -m pytest backend/tests/ — alle Tests grün, auch die bereits bestehenden.
4. Manueller E2E-Durchlauf (Dev-Server starten, z.B. via start-dev.sh falls vorhanden):
   Polygon ~10 ha zeichnen → Maßnahme "Trinkbrunnen" wählen, Anzahl 5 setzen → Sidebar
   zeigt 75.000 € mit aufklappbarer Herleitung + Quellen + "Wirkung auf 50 % skaliert";
   einen Parameter ohne Quelle ändern → wird abgelehnt (custom_source-Pflicht bleibt
   bestehen); mit Quelle ändern → Override-Badge erscheint; eine bestehende
   Flächen-Maßnahme rechnet unverändert weiter; ParameterTable graut die
   Fläche-Felder beim Trinkbrunnen korrekt aus; Excel-Export und Re-Import erhalten die
   Anzahl-Spalte; Dashboard-Kostensektion (cost-summary) ist konsistent zur Sidebar.
   Melde explizit für jeden Punkt, ob er im Browser verifiziert wurde.

Akzeptanz: alle Punkte in 1-4 durchlaufen und bestätigt. Danach committen.
```
