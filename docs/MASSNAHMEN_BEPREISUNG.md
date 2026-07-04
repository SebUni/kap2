Kontext
Die Bepreisung der 46 Maßnahmen ist aktuell weder nachvollziehbar noch belegt:

Formel zu grob: investment = cost_per_unit (einmalig pauschal) + cost_per_m2 × Fläche (measure_service.py:127). Eine Stückzahl („5 Trinkbrunnen in diesem Gebiet") existiert nicht — measure.config wird gespeichert, aber nie gelesen; das Frontend sendet immer config: {}.
Keine Quellen: Keine der 46 Maßnahmen in catalog.py:887-1118 hat ein source-Feld — im Gegensatz zu allen HAZARDS/RISKS, die bereits die Konvention "source": "<Kurz-Key>" + # Herleitung:-Kommentar haben. Alle Kostenparameter fallen auf „Maßnahmenkosten, unbelegt" zurück (parameter_registry.py:161).
17 Stück-Maßnahmen haben 0 € Unterhalt (Feld maintenance_per_unit_year existiert nicht); der echte count-basierte „Trinkbrunnen" (8.000 €/Stück + 500 €/a) liegt nur in totem Legacy-Code (climate/heat/measures.py, von nichts importiert).
Ziel (Nutzerentscheidungen): (1) Einheitliches 5-Parameter-Kostenmodell mit Fixkosten; nicht anwendbare Parameter ausgegraut. (2) Quellen-Recherche für alle Maßnahmen. (3) Anzahl skaliert Kosten und Wirkung (über Richtwert-Dichte). Wichtigstes Abnahmekriterium: Der Mandant sieht, woher ein Preis kommt (Herleitung + Quelle je Kostenkomponente). Nutzen-Seite (benefit_per_m2_year, vermiedene Schäden) und H·E·V-Methodik bleiben unverändert.

1. Neues Katalog-Schema (catalog.py)
   Felder je Maßnahme (nicht anwendbar = None, nicht 0.0 — 0.0 heißt „anwendbar, aber kostenlos", z. B. Bauverbote):

Feld Einheit Bedeutung
cost_fixed € einmalig Planung/Konzept/Einrichtung
cost_per_unit €/Stück Investition je Einheit
cost_per_m2 €/m² Investition je Fläche
maintenance_per_unit_year €/(Stück·a) neu
maintenance_per_m2_year €/(m²·a) wie bisher
unit_label – z. B. „Brunnen", „Baum", „Anlage"; None ⇒ keine Stück-Logik
unit_density_per_ha Stück/ha Richtwert-Dichte (Pflicht wenn unit_label); skaliert Wirkung
source – Kurz-Key-Fallback (bestehende Konvention)
sources dict per-Feld-Quellen (Keys = Feldnamen inkl. default_reduction, unit_density_per_ha)
Formeln:

Investition = cost_fixed + Anzahl × cost_per_unit + Fläche × cost_per_m2
Unterhalt/a = Anzahl × maintenance_per_unit_year + Fläche × maintenance_per_m2_year
Wirkung: r_eff = clamp(r_default · s(coverage) · u, 0, 0.95) mit u = min(1, Anzahl / Richtwert-Anzahl), Richtwert-Anzahl = max(1, round(density · Fläche_ha)); für Flächenmaßnahmen u = 1.
Trinkbrunnen: COOLING_ROOMS_DRINKING_WATER behalten (DB-Kompatibilität), aber umbenennen zu „Kühle Räume / Kühlzentren" (unit_label: "Raum"); neue Maßnahme DRINKING_FOUNTAINS („Trinkbrunnen") als 47. Eintrag + \_MEASURE_KANG_MAP-Eintrag ("health", "health"). Beispiel (Zahlen werden im Recherche-Pass verifiziert):

# Herleitung cost_per_unit: Berliner Wasserbetriebe: Errichtung inkl. Trinkwasser-

# anschluss ~10–16 T€/Standort → Punktwert 14.000 €.

# Herleitung maintenance_per_unit_year: Betrieb/Wartung/Beprobung ~2,5–5 T€/a → 3.500 €.

{"code": "DRINKING_FOUNTAINS", "name": "Trinkbrunnen", ...
"cost_fixed": 5000.0, "cost_per_unit": 14000.0, "cost_per_m2": None,
"maintenance_per_unit_year": 3500.0, "maintenance_per_m2_year": None,
"unit_label": "Brunnen", "unit_density_per_ha": 0.5,
"source": "Berliner Wasserbetriebe / Modellannahme",
"sources": {"cost_per_unit": "Berliner Wasserbetriebe (Praxiswerte Trinkbrunnen)", ...}}
Mechanische Migration der 46 Einträge (Struktur zuerst, Zahlen unverändert):

26 Flächenmaßnahmen: cost_fixed: 0.0, Stückfelder None.
Bisherige Pauschal-cost_per_unit-Maßnahmen aufteilen: Konzept-Maßnahmen (HEAT_ACTION_PLANS, EVACUATION_EMERGENCY_PLANS, EARLY_WARNING_MEASURE, …) → Wert wandert nach cost_fixed, Stückfelder None; echte Stück-Maßnahmen (GRID_REINFORCEMENT_REDUNDANCY „Station", CRITICAL_NODE_PROTECTION „Knoten", LEVEE_REINFORCEMENT „km", SALTWATER_BARRIERS „Anlage", …) → unit_label + unit_density_per_ha (zunächst Modellannahme).
Kommentarblock catalog.py:875-886 auf neue Formel/Konventionen aktualisieren. 2. Backend
measure_service.py:

Neue testbare Helfer: \_resolve_count(mdef, config, covered_area_m2) -> (count, is_default, recommended) — fehlender config["count"] ⇒ Richtwert-Anzahl als Default (Bestandsmaßnahmen rechnen weiter sinnvoll, Response markiert count_is_default: true); \_unit_effect_factor(count, recommended) = min(1, count/recommended); compute_costs(mdef, count, area) -> cost_breakdown.
\_reduction_factor(mdef, fraction, unit_factor=1.0) (Zeile 50-59): r = base_r · s(fraction) · unit_factor.
compute_impact (Zeile 62-170) umstrukturieren: Fläche vorab aus coverage summieren (unit_factor braucht Gesamtfläche), dann count/unit_factor bestimmen, dann Delta-Schleife. Response zusätzlich: count, count_is_default, recommended_count, unit_label, cost_breakdown; bisherige Summenfelder bleiben. MeasureImpact.costs (erste Zelle) um breakdown + count ergänzen.
\_adjusted_cell_data (Zeile 173-199) synchron halten: dort ebenfalls Fläche+count+unit_factor bestimmen und an \_reduction_factor durchreichen — sonst divergieren Dashboard („mit Maßnahmen") und Sidebar. Empfehlung: \_coverage liefert (frac_map, covered_area_m2).
Quellen im Breakdown: je Komponente source = custom_source (bei Override) sonst sources[feld] sonst source, plus overridden-Flag (Overrides liegen via load_db_overrides schon vor).
parameter_registry.py:

MEASURE_PARAM_SPECS (Zeile 22-28) auf 8 Einträge: + cost_fixed (€), + maintenance_per_unit_year (€/(Stück·a)), + unit_density_per_ha (Stück/ha). MEASURE_OVERRIDE_FIELDS wächst automatisch mit; resolve_measure_def unverändert.
Emission (Zeile 156-170): source = m["sources"].get(field) or m["source"] or "Modellannahme (…)"; applicable = m.get(field) is not None; bei nicht anwendbar: value=0.0, editable=False, applicable=False (\_base_param um applicable erweitern).
cost_breakdown-Shape (neue Pydantic-Modelle CostComponent/CostBlock/EffectScaling/CostBreakdown in schemas.py):

"cost_breakdown": {
"investment": {"total_eur": 75000, "components": [
{"param": "cost_per_unit", "label": "Kosten je Brunnen", "unit_price": 14000,
"quantity": 5, "quantity_unit": "Brunnen", "amount_eur": 70000,
"source": "Berliner Wasserbetriebe (…)", "overridden": false}, …]},
"annual_maintenance": {…},
"effect_scaling": {"unit_factor": 0.5, "count": 5, "recommended_count": 10,
"density_per_ha": 0.5, "source": "Modellannahme (Richtwert-Dichte)"}
}
Sonstiges Backend:

Keine DB-Migration nötig (config und MeasureImpact.costs sind JSON, ConfigParameter.parameter_id freier String).
export_service.py: Spalten „Anzahl"/„Einheit" anhängen (Import liest positional row[:7] — count round-trippt über die Konfigurations-JSON bereits).
Legacy löschen: alle backend/app/services/climate/\*/measures.py (8 Module, verifiziert importfrei) — konkurrierendes Altmodell, verwirrt nur.
Kompat-Hinweis: bestehende ConfigParameter-Overrides auf measures.X.cost_per_unit von Maßnahmen, deren Wert nach cost_fixed migriert, prüfen (SELECT … WHERE parameter_id LIKE 'measures.%') und ggf. umtragen. 3. Frontend
types/index.ts: CatalogMeasure um neue Felder (number | null), MeasureImpactSummary um count/count_is_default/recommended_count/unit_label/cost_breakdown, ModelParameter.applicable?.
MapView.tsx MeasureCreateModal (~679-862): bei unit_label ein Feld „Anzahl (Brunnen)" mit Vorbelegung = Richtwert aus vorhandener Flächenberechnung (~715-730) + Hinweis „Richtwert: X für Y ha"; handleSave sendet config: {count}. Kleine clientseitige Kostenvorschau („Schätzung, Katalogwerte") unter dem Feld.
MeasureSidebar.tsx: Anzahl editierbar (analog Umsetzungsjahr, danach calculateImpact). Kosten-Karte (135-153) bekommt die Herleitungs-UI (Priorität #1): aufklappbar „Herleitung anzeigen" → je Komponente 5 × 14.000 €/Brunnen = 70.000 € + Quelle (muted) + „Override"-Badge; InfoTooltip am Kosten-Titel (erstmalige Nutzung des note-Props). Wirkungs-Karte: bei unit_factor < 1 Hinweis „Wirkung auf 50 % skaliert (5 von 10 Brunnen)"; bei count_is_default Badge „Anzahl = Richtwert".
ParameterTable.tsx: applicable === false ⇒ Zeile ausgegraut, Wert „—", Quelle „nicht anwendbar" (Edit-Button entfällt schon über editable: false).
MeasuresTableTab.tsx: Spalte „Anzahl". 4. Recherche-Pass: Quellen für alle 47 Maßnahmen
Format je belegtem Wert (Konvention wie RISKS): # Herleitung <feld>: <Beleg, Spanne → Punktwert> + Kurz-Key in sources; ohne belastbaren Beleg ehrlich "Modellannahme (…)", editierbar. Web-Recherche (WebSearch), gebatcht nach KAnG-Cluster:

Batch Quellen-Anker
Stadt/Hitze (Trinkbrunnen, Stadtgrün, Schatten, HAP, Kühlräume) Berliner Wasserbetriebe, UBA/BMUV-HAP-Praxishilfen, difu, GALK (Stadtbaumkosten)
Gebäude/Begrünung (Gründach, Cool Roofs, Objektschutz) BuGG-Marktreport, KfW-Programme, BBK-Hochwasserschutzfibel
Wasser/Starkregen (Entsiegelung, Mulden/Rigolen, Retention, Leckage) DWA-A 138 / Kostenkennwerte, Hamburg RISA, LANUV NRW, DVGW
Küste/Fluss (Deich €/km, Barrieren, Auen) NLWKN/MELUND-Richtwerte, IKSR, BfN
Land-/Forstwirtschaft KTBL-Kostenkennwerte, LfL Bayern, Landesforsten-Waldumbausätze
Energie/Wirtschaft BNetzA/dena, HTW-Stromspeicher-Inspektion; org. Maßnahmen meist Modellannahme
Bevölkerungsschutz, Fischerei BBK, kommunale Praxis; überwiegend Modellannahme
Je Batch auch unit_density_per_ha-Richtwerte (meist Modellannahme, im Kommentar begründet). default_reduction bleibt unangetastet, bekommt nur den ehrlichen sources-Eintrag.

5. Doku
   BERECHNUNGS_HANDBUCH.md §7: neue Wirkungs- und Kostenformeln, None-Konvention, sources-Konvention, cost_breakdown-Shape; §9-API-Tabelle ergänzen.

6. Verifikation
   Automatisiert — neu backend/tests/test_measure_pricing.py (Stil wie test_review_wirkungsmechanismen.py, DB-frei über die Helfer):

Katalog-Konsistenz: alle 47 Maßnahmen vollständig (Felder gesetzt oder None); unit_label ⇔ Dichte + mind. ein Stück-Kostenfeld; jede Maßnahme hat source; sources-Keys gültig; keine negativen Werte.
compute_costs: Trinkbrunnen 5 Stück ⇒ 5.000 + 5×14.000 = 75.000 €, Unterhalt 17.500 €/a; Flächenmaßnahme identisch zur Altformel; None erzeugt keine Komponente; Quellen inkl. Override korrekt.
\_resolve_count/\_unit_effect_factor: Richtwert-Default, min(1, count/recommended), Faktor 1 für Flächenmaßnahmen.
Registry: 8 Parameter je Maßnahme, applicable/editable konsistent; resolve_measure_def wendet alle 8 an.
Bestehende Tests grün: python -m pytest backend/tests/.
Manuell E2E (start-dev.sh): Polygon ~10 ha → „Trinkbrunnen", Anzahl 5 → Sidebar zeigt 75.000 € mit Herleitung+Quellen und „Wirkung auf 50 % skaliert"; Parameter-Änderung ohne Quelle wird abgelehnt (custom_source-Pflicht), mit Quelle erscheint Override-Badge; Flächen-Bestandsmaßnahme rechnet unverändert; ParameterTable graut m²-Felder beim Trinkbrunnen aus; Excel-Export/Re-Import erhält Anzahl; Dashboard-cost-summary konsistent zur Sidebar.

7. Reihenfolge
   Cleanup: tote climate/\*/measures.py löschen.
   Katalog-Struktur: Migration aller 46 + Trinkbrunnen-Split (Zahlen unverändert, Quellen zunächst „Modellannahme").
   Backend-Logik: measure_service + parameter_registry + schemas + Export + Tests.
   Frontend: Typen, Create-Modal, Sidebar-Herleitung, ParameterTable, TableTab.
   Recherche-Pass: Batches gem. §4 (parallelisierbar, sobald Schritt 2 steht).
   Doku + E2E: Handbuch, manueller Durchlauf, Override-Altdaten-Check.
