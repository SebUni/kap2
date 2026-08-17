# Review Wirkungsmechanismen — Datenquelle → Annahme → Ergebnis

Ziel: belegbare, KWRA-nahe Klimarisiko-Berechnung; jede Annahme/jeder Parameter mit prüfbarer Quelle; Kommunen unterscheiden sich sachgerecht; Verantwortung bei der Kommune (editierbare Parameter). Alle Quellen mit Autor/Titel/Herausgeber/Jahr, damit ein Mensch sie prüfen kann; aus Fachkenntnis zitierte Werte vor Veröffentlichung final verifizieren.

## 1. Gesamturteil Methodik

Das Grundgerüst ist **methodisch tragfähig und KWRA/IPCC-kompatibel — beibehalten.** Schwächen liegen in (a) den Eingaben (zu viele Konstanten/Proxys ⇒ Kommunen zu ähnlich, Quellenangaben überzeichnet), (b) den Skalierungsfaktoren (unbelegt), (c) Info-Fenster-Text ≠ tatsächliche Rechnung.

| Aspekt | Ist | Urteil | Quelle |
|---|---|---|---|
| Risiko = f(H, E, V), multiplikativ H·E·V | Produkt normierter H·E·V je Pfad | OK, belegbar | IPCC AR6 WGII (2022) Risikokonzept; UNDRR/Crichton (1999) Risk triangle |
| Wirkungsketten (Pfade prim./alt./compound) | `build_pathways` | OK, KWRA-konform | KWRA 2021 Teilbericht 2 (Methodik); ISO 14091:2021 |
| Normierung min–max auf feste Referenzskala | `override_context.normalize_value` | OK | GIZ/EURAC Vulnerability Sourcebook (2014) + Risk Supplement (2017) |
| Aggregation P90 über Zellen, Mittel je Gruppe | `risk_engine.aggregate` | OK (P90 dokumentieren) | KWRA-Praxis (Perzentil statt Mittel bei Extrembelastung) |
| Übersetzung in Absolutwerte (ref·Index/100·scale) | `estimate_outcome_and_cost` | Struktur OK, **Faktoren unbelegt** (§3) | UBA Methodenkonvention 3.1 (2020); Prognos/GWS/IÖW (2023) |
| Einheitlichkeit über Risiken | Rahmen einheitlich, Indikatorformeln bespoke | OK | — |

**Kernaussage:** Rahmen behalten. Priorität = Eingaben ortsaufgelöst & belegt machen (§2–§4) + Skalierung belegen (§3) + Info-Fenster synchronisieren (§5).

## 2. Befunde & Fixes

Schweregrad: 🔴 kritisch (Glaubwürdigkeit/Angreifbarkeit) · 🟠 wichtig · 🟡 klein.

### B1 — Provenance-Mismatch (Quellenangabe ≠ genutzte Daten) 🔴
| # | Datei:Zeile | Befund | Fix |
|---|---|---|---|
| B1.1 | `catalog.py:57` u.v.a. | `source` behauptet „DWD CDC / Copernicus C3S-CORDEX", tatsächlich `mean_temp_rise = 1.6+(mean_temp−9.5)·0.1` aus **einem** Bundesland-Skalar. Analog für Starkregen, Dürre, Sturm, Niedrigwasser. | Entweder echte Daten ingesten (B2) **oder** `source`/`proxy`-Text ehrlich als „Proxy aus DWD-Bundesland-Mittel" kennzeichnen. Keine Quelle behaupten, die nicht in die Rechnung eingeht. |
| B1.2 | `parameter_registry.py:71,89,104,125,139,157` | Parameter-Quellen sind generische Strings („Modellannahme", „Risikokatalog"), nicht prüfbar. | Jede `source` durch konkrete Zitation aus §6 ersetzen (Kurz-Key, z.B. „RKI 2022"). |

### B2 — Regionale Treiber: Proxy → echte offene Daten 🔴
Alle in `inputs.py:279-289` aus 2 Skalaren (hot_days, mean_temp) linear erfunden ⇒ alle Zellen eines Bundeslands identisch, kaum Differenzierung zwischen Kommunen.

| # | Treiber (Zeile) | Ersetzen durch (offen, kostenlos) |
|---|---|---|
| B2.1 | `hot_days`, `frost_days` (Regionalquelle) | **DWD CDC Rasterdaten** (annual grids „heiße Tage", „Frosttage", 1 km) am Kommune-/Zell-Zentroid abgreifen |
| B2.2 | `heavy_rain_index` (:283) | **KOSTRA-DWD 2020** (Starkniederschlagshöhen, Bemessungsregen) |
| B2.3 | `drought_days`, `dry_index`, `soil_moisture_decline` (:279,280,285) | **UFZ Dürremonitor** (Bodenfeuchte-Index/SMI) und/oder DWD Bodenfeuchte |
| B2.4 | `mean_temp_rise` (:284) | **DWD Klimaatlas / Copernicus C3S-CORDEX** (CDS, kostenlos) — Delta ggü. Referenzperiode |
| B2.5 | `storm_days` = 6.0 konstant (:282) | **DWD Wind/Sturm-Klimatologie** oder ERA5 (Copernicus CDS, kostenlos); mind. regionalisieren |
| B2.6 | `low_flow_days` (:286) | **BfG / PEGELONLINE (WSV)** Niedrigwasser nächster Pegel (kostenlose API) |
| B2.7 | `sea_level_rise` = 4.5 konstant (:288) | **BSH** + IPCC AR6 Sea-Level-Projection-Tool (kostenlos) |
| B2.8 | `surface_water_heating` (:287) | Proxy zulässig (Sentinel/Landsat LST kostenlos, aber aufwändig) — als Proxy kennzeichnen |
| B2.9 | `glacier_loss_rate` = 0.5 (:289) | Nur alpine Lagen relevant; OSM glacier + DWD Schnee, sonst 0 |

Ergebnis: Treiber werden ortsaufgelöst ⇒ Kommunen unterscheiden sich sachgerecht.

### B3 — Feste Konstanten (Vulnerabilitäten) → differenzieren 🔴
`indicators.py` — identisch für **jede** Kommune (verletzt Differenzierungsziel), keine Quelle:

| # | Zeile | Konstante | Fix |
|---|---|---|---|
| B3.1 | :184,202 (45), :174,183,186,187,204 (50), :200,201,205 (40) | Adaptive-Kapazitäts-/Zustands-Konstanten | Wo Daten existieren, ortsaufgelöst; sonst neutral 50 + editierbar + als „Modellannahme (mangels lokaler Daten)" markiert |
| B3.2 | :184 `FINANCIAL_ADAPTATION_CAPACITY`, :202 `PLANNING_IMPLEMENTATION_CAPACITY`, :177 income | **BBSR INKAR** (Gemeinde-/Kreis-Sozioökonomie: Kaufkraft, Steuerkraft, Arbeitslosigkeit — kostenlos) |
| B3.3 | :200 `EARLY_WARNING_SYSTEMS`, :201 `EMERGENCY_MANAGEMENT` | **OSM** `amenity=fire_station`, `emergency=*`-Dichte je Kommune |
| B3.4 | :195 `LEVEE_CONDITION` | **OSM** `man_made=dyke`/`embankment` in Gewässernähe |
| B3.5 | :174 `CRITICAL_INFRA_CONDITION`, :186 `REDUNDANCY_BACKUP` | Proxy: Zensus-Gebäudealter + Infrastruktur-Assetdichte (B4); sonst neutral+editierbar |

### B4 — Infrastruktur-Kritikalität: nur Gebäude statt Assets 🔴
| # | Datei:Zeile | Befund | Fix |
|---|---|---|---|
| B4.1 | `indicators.py:185` | `INFRA_CRITICALITY = clamp(bldg_count·0.3)` — **nur Gebäudezahl**, obwohl Beschreibung „Dichte kritischer OSM-Infrastruktur" sagt (`catalog.py:360`). | Neu definieren als gewichtete Dichte echter KRITIS-Assets, die bereits geladen werden: `energy_infra_count`, `water_wastewater_count`, `communication_count`, Healthcare-Präsenz, Verkehr. Gewichte nach BBK-KRITIS-Sektoren, editierbar. |
| B4.2 | `indicators.py:152` | `TRANSPORT_HUBS = road_cov·18` — Straßenanteil-Proxy, nicht echte Knoten. | OSM `public_transport=station`, `railway=station/halt`, `highway` Knoten zählen (Assets liegen in OSM vor). |
| B4.3 | `catalog.py:360` | Beschreibung passt nicht zur Rechnung. | Beschreibung an neue Formel angleichen. |

### B5 — Sonstige Indikator-Konstanten (belegen oder als Annahme kennzeichnen) 🟠
Konstante/erfundene Faktoren mit Zeile → Quelle in §6: UHI-Koeffizienten α/β/γ/δ (`inputs.py:20-24`, `parameter_registry.py:142`) → VDI 3787 Bl.1 / Oke (1982) / Stewart&Oke (2012); `HEAT_WAVE uhi_weight 1.5` (`indicators.py:104`) → Stadtklima-Literatur; `road_cov·0.95` (`lineage_operators.py:52`) → Modellannahme; Healthcare-Gewichte 0.5/0.35/0.15 & 20 km (`catalog.py:232,331`) → Erreichbarkeitsmodell (BBSR-Erreichbarkeitsanalysen); Demografie-Fallbacks 22/18 (`indicators.py:81-83`) → Zensus 2022 Bundesmittel; Pathway-Gewichte (`catalog.py:755-765`) → transparente Modellwahl (keine externe Quelle, Begründung dokumentieren). Regel: jeder Faktor bekommt `source` + wird editierbar.

## 3. Skalierungsfaktoren / ref_values — Kalibrierung (Punktwerte)

Prinzip (einfach & belegbar): **Differenzierung kommt aus dem Index** (echte Spatialdaten, §2–§4). Der `ref_value` ist nur der **nationale Größenanker bei Index=100** und wird an publizierte Statistik gehängt. `scale` (pop/area/flat) sorgt für Größenskalierung der Kommune.

| Risiko(-familie) | Datei:Zeile | Wert heute | Anker / Kalibrierung | Quelle |
|---|---|---|---|---|
| `EXPECTED_ANNUAL_MORTALITY` | `catalog.py:459` | 18 Tote/J | ~18/100k als Extrem bei Index=100; RKI-Hitzejahre ~4–11/100k (2018≈10,5) ⇒ typischer Index 20–40 liefert ~3,6–7,2/100k, statistikkonform | an der Heiden et al. 2020; Winklmayr et al. 2022 (Dtsch Arztebl 119:451); RKI JoHM; UBA DAS-Monitoring GE-I-2 |
| `cost_per_outcome_eur` Tod = 3,5 Mio € | `catalog.py:459` | 3,5 Mio | Mit UBA-VSL abgleichen | UBA Methodenkonvention 3.1 (2020), Kostensätze |
| Morbidität/Verletzte/Mental/Evakuierte | `:467,474,481,488` | 320/45/150/800 | Gesundheitskostensätze | UBA Methodenkonvention 3.1; RKI |
| Monetär (Gebäude/Verkehr/Energie/… €/J) | `:509,515,521,527,533,539,545,551,557,671,677,683,689,695,701,731,737` | 4,5 Mio … 200k | Sektorale Schadenskosten DE als Anker | Prognos/GWS/IÖW (2023) „Kosten durch Klimawandelfolgen"; GDV Naturgefahrenreport (jährlich) |
| Operativ (Ausfallstunden, flat) | `:563-611` | 120…15 h | BBK/Betreiber-Kennzahlen; sonst als Modellannahme | BBK KRITIS; als Annahme markieren |
| Umwelt (Arten/ha, area) | `:623-641` | 5/8/12/15 | Naturschutz-Monitoring | BfN / UBA; als Annahme markieren |
| Index-Risiken ref=100 flat | `:617,647,653,659,665,707,713,719,725,743,749` | 100 | Outcome = Index selbst (bewusst); dokumentieren | — |

Regel für den Umsetzer: Jeder `ref_value` und jedes `cost_per_outcome_eur` erhält im Code einen `source`-Eintrag (Kurz-Key) + Kommentar mit Herleitung; unbelegbare bleiben editierbar & werden als „Modellannahme" gekennzeichnet.

## 4. Differenzierungs-Check (Nutzerziel)

| Risiko | Differenziert heute über | Nach Fix zusätzlich |
|---|---|---|
| Hitze/Mortalität | Dichte, UHI, Grün, Altersbänder (Zensus), **Zell-Sommertemperatur aus DWD-Monatsrastern** ✅ | B2.1 auf dem Mortalitätspfad erledigt: die Dosis-Wirkungs-Kurve läuft über die je Zelle abgegriffene Sommertemperatur (`SUMMER_MEAN_TEMP` → `CELL_SUMMER_TEMP`), nicht über `hot_days`. `HOT_DAYS` bleibt Zentroid-basiert und trägt nur noch den Screening-Index |
| Fischerei/Gewässer | Wasseranteil E/V ✅ (Kommune ohne Gewässer → ~0) | — (bereits sachlogisch) |
| Kritische Infrastruktur | heute kaum (Konstanten 50) ❌ | KRITIS-Assetdichte (B4), Zustand via Gebäudealter (B3.5) |
| Sozioökonomie/Anpassung | heute gar nicht (Konstanten) ❌ | INKAR (B3.2) |
| Starkregen/Hochwasser | Versiegelung, TWI, Senken ✅ | KOSTRA-Regen (B2.2) |

## 5. Info-Fenster / Wirkungsmechanismus — Korrektheit (muss Rechnung entsprechen)

| # | Datei:Zeile | Befund | Fix |
|---|---|---|---|
| B6.1 🔴 | `lineage_graph.py:581` | Skalierungs-Tooltip zeigt **immer** „Index/100 · Einwohner_zelle/100.000", auch für `area`- und `flat`-Risiken (falsch). | Scale-abhängig: pop→`Einw./100.000`, area→`Fläche/50 km²`, flat→`×1`. Wert aus `risk['scale']`. |
| B6.2 🟠 | `indicators.py:135-137` vs `override_context.py:47` | `COMPOUND_EVENT` nutzt `catalog.normalize_value` (ignoriert Overrides), Pipeline nutzt `override_context.normalize_value` (mit Overrides) ⇒ Divergenz. | Einheitlich `override_context.normalize_value` verwenden. |
| B6.3 🟠 | `lineage_operators.py:235-244` | Nur 8 von ~87 Indikatoren haben explizite Operator-Schritte; Rest zeigt generisches „Formel". | Für alle risikorelevanten Indikatoren Schritte ergänzen oder Fallback ehrlich beschriften. |
| B6.4 🟠 | `formulas.py` (87 `"formula"`-Strings) | Formel-Strings handgeschrieben, nicht aus Engine ⇒ können driften (z.B. wenn Koeffizient im Code geändert wird). | Konsistenz-Test: Formel-String-Konstanten gegen `indicators.py`-Konstanten prüfen (CI-Test). |
| B6.5 🟡 | `lineage_graph.py:567` | Pfad-„Berechnung"-Zeile ist fix, unabhängig von tatsächlichen Gewichten. | Gewicht/Anteil des Pfads einsetzen. |
| B6.6 🟡 | `pathway_descriptions.py:5` | Kuratiertes Dictionary kann von `build_pathways` abweichen (stale). | Test: jedes vorhandene Pfad-Tupel muss von `build_pathways` erzeugt werden. |
| B6.7 🟡 | `LineageFlowDiagram.tsx:130-134` | Fehlt `parameter_id`-Match, zeigt still „—". | Fehlende Werte sichtbar kennzeichnen. |

## 6. Quellenverzeichnis (prüfbar)

**Methodik:** KWRA 2021 (Kahlenborn u.a., UBA Climate Change 20–26/2021, Teilbericht 2 Methodik) · ISO 14091:2021 · GIZ/EURAC Vulnerability Sourcebook 2014 + Risk Supplement 2017 · IPCC AR6 WGII 2022 · UNDRR/Crichton 1999.

**Klima (offen/kostenlos):** DWD CDC opendata.dwd.de (heiße Tage/Frosttage-Raster) · KOSTRA-DWD 2020 · UFZ Dürremonitor (Helmholtz) · DWD Klimaatlas / Copernicus C3S-CORDEX (CDS) · ERA5 (CDS) · BfG/PEGELONLINE · BSH + IPCC AR6 Sea-Level-Tool.

**Geodaten:** OpenStreetMap (ODbL) · Zensus 2022 (Destatis, 100 m) · BBSR INKAR · Copernicus DEM GLO-30 / AWS Terrain.

**Gesundheit:** an der Heiden u.a. 2020 (Bundesgesundheitsbl) · Winklmayr u.a. 2022 (Dtsch Arztebl Int 119:451-457) · RKI Journal of Health Monitoring · UBA DAS-Monitoringbericht 2019/2023.

**Ökonomie:** UBA Methodenkonvention 3.1 (2020) · Prognos/GWS/IÖW 2023 „Kosten durch Klimawandelfolgen in Deutschland" (BMWK/BMUV) · GDV Naturgefahrenreport.

**Infrastruktur/Stadtklima:** BBK KRITIS-Sektoren / BSI-KritisV · VDI 3787 Blatt 1 · Oke 1982 · Stewart & Oke 2012 (Local Climate Zones).
