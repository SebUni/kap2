# KAP2 – Berechnungshandbuch (KAP3-Kataloge)

Kompakte Gesamtreferenz zu allen Approximationen, Proxys, Koeffizienten,
Normalisierungen, Pathway-Gewichten, Maßnahmen-Wirkungsstärken und Datenquellen.
Die ausführliche Doku liegt **am Objekt**: jedes H/E/V/Risiko/Maßnahme hat in der
Karten-Layerspalte und im Dashboard ein `(i)`-Icon mit Beschreibung, Einheit,
Proxy/Quelle und Normierung.

> Single Source of Truth ist `backend/app/data/catalog.py`. Dieses Handbuch
> erläutert die Logik; konkrete Werte je Code stehen dort und in den Tooltips.

---

## 1. Grundprinzipien

- **Fest verdrahtet:** Klimatische Einflüsse (23), Räumliche Expositionen (23), Sensitivitäten (33),
  Risiken (48) und Maßnahmen (47) sind als Python-Konstanten in
  `catalog.py` hinterlegt (einmalig aus den KAP3-CSVs portiert). Kein
  Laufzeit-CSV-Parser.
- **H/E/V absolut:** Jeder Indikator wird pro **100 m × 100 m**-Zelle in seiner
  natürlichen Einheit berechnet und angezeigt (z. B. K, heiße Tage/Jahr,
  Pers./km², %, Index).
- **Normalisierung nur fürs Risiko:** Eine pro Indikator dokumentierte
  Referenzskala `[norm_min, norm_max]` bildet den Absolutwert linear auf `0..1`
  ab, ausschließlich um `Risiko = Σ(w·H·E·V)` zu rechnen.
- **Risiko-Index 0–100** ist die vergleichbare Metrik.
- **Fehlende räumliche Daten:** Wo kein OSM/DWD/Terrain/Zensus-Proxy existiert,
  wird ein regionaler/nationaler Konstantwert verwendet und über `spatial=false`
  als „nicht räumlich aufgelöst“ markiert (Tooltip-Hinweis).
- **Küsten-/Meeres-Hazards** nur für Küstenkommunen (`is_coastal`).

### Pipeline pro Bewertungslauf
```
gather_cell_inputs  →  compute_cell_hev  →  normalize_hev  →  cell_risk_indices
   (OSM/DWD/Zensus)      (absolute H/E/V)     (0..1)            (Index 0..100)
                                                              ↓
                                                     CellAssessment.data (JSONB)
```
Code: `backend/app/services/engine/{inputs,indicators,risk_engine,runner}.py`.

---

## 2. Datenquellen

| Quelle | Verwendung |
|---|---|
| **OSM** (Overpass) | Gebäudepolygone (+Höhe/Stockwerke), Straßen, Landnutzung, Bäume → Versiegelung, Albedo, Bebauungsgrad, Baumkronen, Grün-/Wasseranteil |
| **DWD CDC** (regional, je Bundesland) | Sommer-Tagesmaximum, heiße Tage/Jahr, Tropennächte, Jahresmittel; Klimafortschreibung RCP4.5/8.5 |
| **DWD CDC Raster** (1 km, EPSG:31467, am Zentroid) | `hot_days`, `frost_days`; **neu (Stufe 2):** Starkregen-Häufigkeit `precipGE20mm_days`/`precipGE30mm_days` → speist den `heavy_rain_index`; `summer_days` verfügbar |
| **BfG/PEGELONLINE** (nächster WSV-Pegel) | `low_flow_days` (Niedrigwassertage < MNW) |
| **Zensus 2022** (Destatis INSPIRE 100m-Gitter, EPSG:3035) | Bevölkerung, Altersanteile (≥65, **<18**), Wohnfläche/Bewohner, Eigentümerquote, Nettokaltmiete, Gebäudealter je Zelle — Pflichtdaten, kein OSM-Proxy |
| **AWS Terrarium DEM** | Mittelhöhe, Hangneigung, Senkentiefe, D8-Abfluss, TWI je Zelle |
| **OSM Gewässer** | `natural=water`, `waterway` → Distanz/Proximität zu Fließ- und Stillgewässern |

**Provenienz der regionalen Klimatreiber** (`build_regional_context`, Feld
`provenance`): Jeder Treiber ist als echte Quelle (`dwd_cdc_raster`, `pegelonline`)
oder dokumentierter Proxy (`proxy_mean_temp`, `regional_constant`, …) gekennzeichnet.
Real ortsaufgelöst: `hot_days`, `frost_days`, `low_flow_days`, `heavy_rain_index`
(Stufe 2) sowie **`storm_days`** (Stufe 5b: ERA5-Böenklimatologie, Tage/Jahr ≥ 25 m/s,
falls der Betreiber das Raster mit `scripts/fetch_era5_storm.py` + kostenlosem CDS-Key
erzeugt hat — ERA5 ist kostenlos und kommerziell nutzbar, seit 02.07.2025 CC-BY 4.0;
ohne Raster bleibt der dokumentierte Konstantwert, Provenienz `regional_constant`).
Weiterhin Proxy: die Dürre-Treiber `drought_days`/`dry_index` (aus realen `hot_days`
abgeleitet; echte Bodenfeuchte via UFZ-Dürremonitor-SMI wäre eine spätere Verfeinerung). Der frühere `heavy_rain_index` aus der Mitteltemperatur ist
damit ersetzt (MODELL_KRITIK: fachlich unhaltbarer Proxy).

### Zensus-Autoloader

Pflicht-Themen (Manifest in `zensus_loader.py`): `population`, `share_over_65`,
`share_under_18`, `living_area_per_person`, `owner_share`, `net_cold_rent`,
`building_age`. Beim Assessment-Lauf werden fehlende ZIPs von Destatis geladen,
bbox-gefiltert je Kommune gecacht unter `backend/data/zensus/extract/{key}/`.

Manuell: `python -m app.cli zensus-download [--keys population,...]` oder
`POST /api/admin/zensus/sync`.

Geheimhaltung (`–`, `KLAMMERN`): Zelle ohne Wert → NULL in Sonstige-Layern;
abgeleitete H/E/V nutzen regionalen Fallback nur wenn Zensus-Zelle fehlt.

Mehrkern-Verarbeitung: `multiprocessing` (fork, bis 8 Worker, Chunk 50) für die
OSM-Aggregation je Zelle (wiederverwendet aus dem alten Hitze-Assessor).

---

## 2a. Gitter (100 m, EPSG:3035)

Das Bewertungsgitter folgt dem **Destatis INSPIRE 100m-Gitter** (EPSG:3035),
nicht mehr einer lokalen UTM-Bbox. Pro Zelle werden gespeichert:

| Feld | Bedeutung |
|---|---|
| `gitter_id` | INSPIRE-ID, z. B. `CRS3035RES100mN4340900E2698700` |
| `x_3035`, `y_3035` | Zellmittelpunkt in EPSG:3035 |
| `row_idx`, `col_idx` | `y_3035/100`, `x_3035/100` (Nachbar-Lookup ±1 = ±100 m) |

Code: `grid_service.generate_grid`. Nach Gitter-Umstellung sind bestehende
Assessments ungültig (Alembic-Migration leert abgeleitete Tabellen).

---

## 2b. Sonstige Layer (Sidebar)

Kategorie **Sonstige** (`catalog.AUXILIARY`, ~42 Indikatoren) dokumentiert
Rohdaten für Nachvollziehbarkeit: Zensus, OSM, Gelände, Gewässer, regionale
DWD-Werte. Werte werden in `CellAssessment.data["auxiliary"]` persistiert und
als eigener GeoPackage-Layer **`sonstige_100m`** exportiert (eine Spalte pro
Katalog-Code). H/E/V-Tooltips verweisen über `formulas.py` auf die zugehörigen
Sonstige-Codes (`aux_layer`).

Unterkategorien: `zensus`, `osm`, `terrain`, `water`, `regional` — siehe
`catalog_auxiliary.py`.


## 3. Urbane Überwärmung (UHI) – ΔT pro Zelle

Tag-UHI nach KAP2/KAP3-Formel (`inputs.compute_uhi_delta`). Eingaben aus OSM
(Gebäude/Straßen/Landnutzung/Bäume), Referenz aus DWD.

**Koeffizienten:** α = 6.0, β = 2.0, γ = 3.5, δ = 2.0, ε = 1.5, Baum = 0.3

| Größe | Formel |
|---|---|
| `imp` (Versiegelung) | `clamp(bldg_cov + road_cov·0.95, 0.02, 0.98)` (Fallback Landnutzung) |
| `height_factor` | `min(avg_height / 15, 2.0)` |
| `bldg_factor` | `bldg_cov · height_factor` |
| `meadow` | `max(0, green − forest)` |
| `green_cooling` | `γ·forest·1.8 + γ·meadow + γ·farmland·0.5` |
| `water_cooling` | `δ·water` |
| `tree_cooling` | `0.3·canopy·10` |
| `canyon` | `ε·(1 − svf)·height_factor` |
| Aufheizung | `α·(1 − albedo)·imp + β·bldg_factor` |

$$\Delta T = \max\!\bigl(0,\ \text{Aufheizung} - \text{green} - \text{water} - \text{tree} + \text{canyon}\bigr)$$

$$T_{\text{Zelle}} = T_{\text{ref}} + \Delta T \quad (T_{\text{ref}} = \text{DWD-Sommer-Tagesmaximum})$$

Daraus speisen sich u. a. `HEAT_WAVE`, `UHI_INTENSITY`, `MEAN_TEMPERATURE_RISE`.

---

## 4. Klimatische Einflüsse / Räumliche Expositionen / Sensitivitäten (absolut)

Berechnung in `engine/indicators.py:compute_cell_hev`. Jeder Code besitzt im
Katalog: `unit`, `[norm_min, norm_max]`, `spatial`, `proxy`, `source`,
`description` (alle im `(i)`-Tooltip sichtbar).

- **Räumlich aufgelöst (`spatial=true`):** aus Zell-Inputs abgeleitet
  (z. B. `POPULATION_DENSITY` aus Zensus-100m-Bevölkerung,
  `AGE_STRUCTURE` aus Anteil ≥65 + **<18** je Zelle,
  `HEAT_WAVE`/`UHI_INTENSITY` aus ΔT, `IMPERVIOUSNESS` aus OSM).
- **Konstant (`spatial=false`):** regionaler Wert für alle Zellen
  (z. B. `SEA_LEVEL_RISE`, `MEAN_TEMPERATURE_RISE`, einige Sturm-/Dürre-Proxys).
  Diese sind in den Tooltips als „nicht räumlich aufgelöst“ gekennzeichnet.

### Wichtige abgeleitete Formeln (Zensus-basiert)

| Code | Formel (Kurz) |
|---|---|
| `POPULATION_DENSITY` | `pop / Fläche_km²` (pop aus Zensus-100m) |
| `AGE_STRUCTURE` | `share_over_65 + share_under_18` (%, je Zelle) |
| `VULNERABLE_GROUPS_POPULATION` | `pop × (share_over_65 + share_under_18) / 100` |
| `BUILDING_STABILITY` | Index steigt mit Gebäudealter (Zensus mittleres Baujahr) + OSM-Höhe/Deckung |
| `INCOME_SOCIAL_RESILIENCE` | Mittel aus Miete-, Eigentümer- und Wohnflächen-Indizes (Zensus-100m) |

### Normalisierung (nur fürs Risiko)
`risk_engine.normalize_hev` → `catalog.normalize_value(code, x)`:
$$\hat{x} = \mathrm{clamp}\!\left(\frac{x - \text{norm\_min}}{\text{norm\_max} - \text{norm\_min}},\,0,\,1\right)$$

---

## 5. Risiko-Komposition

`Risiko = Σ(w · Ĥ · Ê · V̂)` über alle Wirkungsketten eines Risikos, normiert
auf den Gewichtssummen → Index `0..100` (`risk_engine.cell_risk_indices`).

### Wirkungsketten (`catalog.build_pathways`)
Aus den geordneten H/E/V-Listen eines Risikos werden deterministisch erzeugt:

| Pathway-Typ | Kombination | Gewicht |
|---|---|---|
| `primary` | H₀·E₀·V₀ | 1.00 |
| `aligned` | Hᵢ·Eᵢ·Vᵢ | 0.85 |
| `alternate_hazard` | Hᵢ·E₀·V₀ | 0.75 |
| `alternate_exposure` | H₀·Eᵢ·V₀ | 0.70 |
| `alternate_vulnerability` | H₀·E₀·Vᵢ | 0.70 |
| `compound_he` | H₁·E₁·V₀ | 0.65 |
| `compound_hv` | H₁·E₀·V₁ | 0.60 |
| `compound_ev` | H₀·E₁·V₁ | 0.55 |
| `compound_multi` | (mehrfach) | 0.50 |

$$\text{Index} = 100 \cdot \frac{\sum_p w_p\,\hat H_p\,\hat E_p\,\hat V_p}{\sum_p w_p}$$

**Compound/Cascade:** als Hazards mit `max_of_constituent_hazards` bzw. als
regionaler Konstantwert (`COMPOUND_EVENT`, `CASCADE_EVENT`) modelliert.

### Outcome & Kosten (`estimate_outcome_and_cost`)
> **Schicht A vs. B:** Der hier beschriebene lineare `ref_value`-Weg ist seit dem
> Schicht-B-Umbau (Option C, `MODELL_KRITIK.md` §5–6) nur noch der **Screening-/
> Fallback-Pfad** und der **primäre Rechenweg für `flat`-Risiken** (kommunenweite
> Einzelwerte). Bevölkerungs- und flächenbezogene Schadensrisiken rechnen stattdessen
> **absolute, per-Zelle berechnete Schadensfunktionen** (nächster Abschnitt), deren
> Zell-Werte die Kommune-Summe bilden. `ref_value` ist für diese Risiken nur noch
> Kalibrier-/Sanity-Anker (`impact/sanity.py`).

- `outcome = ref_value · (mean_index/100) · scale_factor`
- `scale`: `pop` → Einwohner/100 000, `area` → Fläche/50 km², `flat` → 1
- **Monetarisierung (jedes Risiko fließt monetär ein):**
  - `cost_dimension = monetary` → `ref_value` liegt bereits in €/Jahr vor,
    also `cost_eur = outcome` (impliziter Kostensatz 1 €/€, kein separater
    Parameter).
  - alle anderen (Gesundheit, operativ, Umwelt) → `cost_eur = outcome ·
    cost_per_outcome`, wobei `cost_per_outcome` ein **eigenständiger, editier-
    und override-fähiger Registry-Parameter** je Risiko ist
    (`risks.<CODE>.cost_per_outcome`, Einheit „€ je <Outcome>“). Beispiele:
    Mortalität × VSL (3,5 Mio €, OECD 2012), Ausfallstunden × Cost-of-Outage
    (EWI-VoLL 2015 / BBK-KRITIS), Habitat-ha × Ökosystemwert (TEEB-DE).
  - Der VSL und alle übrigen Kostensätze sind damit in der Konfigurations-UI,
    im Info-Tooltip und im Parameter-Excel sichtbar/belegt – nicht mehr als
    Prosa im `ref_value`-Tooltip versteckt.
- **Reine Screening-Index-Risiken** (`outcome_unit = "Index"`,
  `catalog.INDEX_ONLY_RISK_CODES`) tragen bewusst **0 €** bei: ihr Schaden ist
  bereits über die konkreten monetär bewerteten Risiken erfasst; eine eigene
  €-Bewertung wäre Doppelzählung (im `cost_source_detail` begründet). Ihr
  Kostensatz ist editierbar 0 und kann bei Bedarf gesetzt werden.
- Helfer: `catalog.risk_is_monetary`, `risk_contributes_to_total`,
  `risk_default_cost_per_outcome`, `cost_unit_label`.

### Schicht B — absolute Schadensfunktionen (Σ über Zellen)

Paket `services/engine/impact/` (per-Risk-Dispatch, `IMPACT_FUNCTIONS`). Jedes der
22 Schadensrisiken liefert je Zelle einen **absoluten** Outcome + monetarisierte
Kosten; Risiken ohne registrierte Funktion rechnen den linearen `legacy_cell_impact`
(= `ref·Index/100·Skalierung`, aber je Zelle). Der Runner materialisiert je Zelle
`{index, outcome, cost_eur}`.

- **Gesundheit** (`impact/health.py`): `Betroffene · Rate · Dosis-Wirkung · g(V̂)`.
  Hitzegetrieben über die nichtlineare attributable Fraktion
  `AF = 1 − exp(−β·(Intensität − Schwelle)₊)` (überproportional durch die Schwelle).
- **Monetäre Sektorschäden** (`impact/monetary.py`): `Assetwert · Jahresverlustrate ·
  Schadenskurve(Intensität) · g(V̂)`; Assetwert aus realen Zell-Rohgrößen ×
  editierbaren €-Parametern. Schadenskurve konvex (`curves.py`, Exponent > 1).
- **Umwelt** (`impact/environment.py`): `exponierte Naturfläche · Verlustrate(Hazard)
  · g(V̂)`, monetarisiert über den Kostensatz.
- `g(V̂) = 0,5 + mittlere normierte Vulnerabilität` (Vulnerabilitäts-Modifikator).
- **k_indirekt-Konsolidierung** (`consolidate_indirect`, behebt §3.7): indirekte
  Verluste = `k · Σ direkte Sektorschäden`; Versorgungsengpass/Standortnachteil/
  verzögerte Schäden = 0 € (darin konsolidiert); Restaurierung = `quote · Σ direkt`
  als **nicht-additive** Teilkennzahl (`NON_ADDITIVE_RISK_CODES`, aus `total_eur` raus).
- **Operative Ausfallrisiken** (9, `flat`): bewusst keine per-Zell-Funktion —
  Ausfallstunden sind nicht zell-additiv; sie bleiben P90-basiert (VoLL-Kostensatz).
  Die Ausfall**stunden** sind kommunenweit, die **€-Bewertung** skaliert aber mit der
  Last (`pop/100.000`) — der VoLL-Satz ist je ~100.000-Ew.-Kommune kalibriert, sonst
  zahlte eine Kleingemeinde denselben €-Ausfall wie eine Großstadt (§8/B6).
- **Hazard-Intensität der Schadensfunktionen** nutzt FIXE Katalog-Referenzgrenzen
  (`CellContext.haz_intensity`), entkoppelt von den editierbaren Screening-Normgrenzen
  (`norm_min/max`) — ein Screening-Norm-Override verschiebt damit NICHT die absoluten
  Schäden (§3.3-Restlücke, §8/B-Rest). Die Hitze-Gesundheitsfunktionen rechnen ohnehin
  mit der absoluten Hitzetage-Intensität.
- Alle Raten/Koeffizienten/Assetwerte sind editierbare, quellenbelegte Registry-
  Parameter (`impact/params.py` → `risks.<CODE>.impact.*` / `impact.*`).

### Gesamtschaden = Summe der Einzelrisiken
`cost.total_eur = Σ cost_eur` über alle Risiken. Es gibt **kein eigenständiges
Gesamtschaden-/EAD-Risiko mehr** (früher `EXPECTED_TOTAL_DAMAGE_EAD_EUR`, das
per Konstruktion ~die Summe der Sektorschäden abbildete und diese in `total_eur`
verdoppelte). Der Dashboard-KPI „Erwartete Schäden gesamt“ ist damit die
nachrechenbare Summe der monetarisierten Einzelrisiken.

> **Folgekosten-Konsolidierung (Schicht B, umgesetzt):** Die Doppelzählung der
> Folgekosten (§3.7) ist über den Indirekt-Multiplikator `k_indirekt` konsolidiert
> (`consolidate_indirect`, s. o.): indirekte Verluste = `k · Σ direkte Sektorschäden`;
> Versorgungsengpass/Standortnachteil/verzögerte Schäden zählen 0 € (darin enthalten);
> Restaurierung ist eine **nicht-additive** Teilkennzahl und aus `total_eur`
> ausgenommen (`NON_ADDITIVE_RISK_CODES`). Die physischen Umwelt-Flächenverluste
> (Biodiversität/Habitat) grenzen sich weiterhin vom laufenden „Verlust von
> Ökosystemleistungen“ ab (im `cost_source_detail` erläutert).

### Aggregation (`risk_engine.aggregate`)
Je Risiko (Schicht B):
- **pop-/area-skaliert:** `outcome`/`cost_eur` = **Summe der Zell-Werte**
  (`aggregation = "sum"`) — behebt den Karte↔Dashboard-Widerspruch (§3.6), weil
  Kartenschwerpunkte und Dashboard-Summe aus derselben Zellquelle stammen.
- **`flat`:** kommunenweiter Einzelwert P90-basiert (`aggregation = "p90"`) —
  eine Summe über Zellen wäre hier unsinnig (Ausfallstunden/Index-Screening).
- Zusätzliche Felder (auch für das Dashboard): `p90_index` (= `index`), `max_index`,
  `outcome_sum`, `top5_share` (Anteil der Summe aus den stärksten 5 % Zellen →
  Hotspot-Signal), `area_km2_affected` und `share_above_threshold` (Zellen ≥
  Risikozonen-Schwelle). **Robuster Fallback:** Alt-Zelldaten ohne materialisierten
  Outcome werden je Zelle über `legacy_cell_impact` nachgerechnet (kein 500er).

Je KWRA-Gruppe: Mittelwert der Risiko-P90-Indizes (übergreifende Spinnen-Metrik).
`total_eur` = Summe der Einzel-`cost_eur` **ohne** `NON_ADDITIVE_RISK_CODES`.

### Modellversion & Cache-Invalidierung
Strukturelle Modelländerungen (Risiko-Set, Schadensfunktionen, Hazard-Daten) erhöhen
`catalog.MODEL_VERSION`. Der Layer-Cache (`layer_cache.py`) stempelt jedes
Kommune-Cache-Verzeichnis mit dieser Version (`.model_version`) und leert es beim
ersten Zugriff automatisch, wenn die Version nicht mehr passt. Seit Schicht B
materialisiert der Runner je Zelle `{index, outcome, cost_eur}`; ändern sich die
**Schadensfunktionen** (Stufe 4/5) oder die **Hazard-Ingestion** (Stufe 2/5b), ist eine
Neuberechnung der `CellAssessment` erforderlich (MODEL_VERSION-Bump). **Anzeige-/
Aggregations-Änderungen** (Stufe 6 Maßnahmen-Nutzenformel, Stufe 7 Dashboard-Felder)
ändern die Per-Zell-Ausgabe nicht und lösen daher **bewusst keinen** Bump aus.

**Welche Overrides wirken live, welche brauchen Neuberechnung (§8/B2):** `aggregate`
monetarisiert die Kommune-Kosten **live aus dem gespeicherten Per-Zell-`outcome` ×
aktuellem Kostensatz** (`cost_from_outcome`), nicht aus dem beim Lauf materialisierten
`cost_eur`. Deshalb wirken **Kostensatz-Overrides** (`risks.*.cost_per_outcome`) und —
für flat-Risiken — **Referenzwert-Overrides** (`ref_value`) **sofort ohne
Neuberechnung**. Alle Overrides, die den materialisierten Per-Zell-Wert (Index oder
Outcome) selbst bestimmen — **Normgrenzen** (`*.norm_min/max`), **Impact-Parameter**
(`risks.*.impact.*`, `impact.*`), **Pfadgewichte**, **UHI-/Formelparameter** — brauchen
eine Neuberechnung; die API (`PUT …/parameters`) meldet das je Änderung im Feld
`recalculation_required`, das Frontend zeigt danach den Hinweis „wirkt erst nach
Neuberechnung". Die Overrides einer Kommune werden für Aggregation/Export als
**request-scoped Engine-Kontext** gesetzt (`override_context.override_scope`), damit sie
nicht in die Berechnung einer anderen Kommune durchsickern (Leak-Fix §8/B2).

### Risikozonen
Zusammenhängende Zellen mit hohem Risiko-Index (Connected Components),
`risk_zone_service.get_risk_zones_geojson(risk_code)`.

---

## 6. KWRA-Risikogruppen (5)

| Code | Label | Inhalt |
|---|---|---|
| `heat` | Hitze | Hitze, Gesundheit, urbane Überwärmung |
| `drought` | Trockenheit & Niedrigwasser | Trockenheit, Niedrigwasser, Grundwasser |
| `flood` | Hochwasser & Starkregen | Fluss-/Starkregen-/Sturzfluten |
| `gradual` | Gradueller Wandel | langfristige Trends, Ökosysteme |
| `compound` | Verbund & Kaskade | Compound-Events, Domino-/Systemrisiken |

Farben und Beschreibungen: `catalog.KWRA_GROUPS`.

---

## 7. Maßnahmen

Modell in `services/measure_service.py`. Eine Maßnahme reduziert ihre
Zielkomponente(n) `effect_target ∈ {hazard, exposure, vulnerability}` in den
abgedeckten Zellen, deckungs- und (bei Stück-Maßnahmen) anzahl-skaliert. Da
der Risiko-Index multiplikativ in H·E·V ist, wirkt die Reduktion analytisch
als Index-Skalierung:

$$r_{\text{eff}} = \mathrm{clamp}(r_{\text{default}} \cdot s(\text{coverage}) \cdot u,\,0,\,0.95)$$
$$\text{factor} = (1 - r_{\text{eff}})^{\,n_{\text{targets}}}, \qquad \text{Index}_{\text{neu}} = \text{Index} \cdot \text{factor}$$

- `coverage_scaling = linear` → `s = fraction`;
  `saturating` → `s = min(1, fraction·1.5)`.
- `default_reduction` je Maßnahme im Katalog (typabhängig, dokumentiert; in
  Config überschreibbar). Quelle: KAP3-Vorschlag + Plausibilitätskalibrierung.
- `u` (`_unit_effect_factor`) skaliert die Wirkung von **Stück-Maßnahmen**
  (`unit_label` gesetzt) über die Anzahl relativ zu einem Richtwert:
  `u = min(1, Anzahl / Richtwert-Anzahl)`, mit
  `Richtwert-Anzahl = max(1, round(unit_density_per_ha · Fläche_ha))`.
  Für reine Flächenmaßnahmen (`unit_label is None`) ist `u = 1` — die Formel
  bleibt dort identisch zur bisherigen Rechnung.

### Kostenmodell — symmetrisch CAPEX / OPEX

Jede Maßnahme trägt im Katalog (`catalog.py`) sechs Kostenfelder plus die
Stück-Metadaten. Das Modell ist **MECE**: jeder Euro ist entweder einmalige
Investition (**CAPEX**) oder wiederkehrende Betriebs- und Unterhaltskosten
(**OPEX**); innerhalb beider Blöcke disjunkt nach Bezugsgröße (mengenunabhängig
/ je Stück / je Fläche). **Nicht anwendbar = `None`, nicht `0.0`** — `0.0`
bedeutet „anwendbar, aber kostenlos" (z. B. planungsrechtliche Bauverbote). Ein
`None`-Feld erzeugt keine Kostenkomponente im Breakdown und keinen editierbaren
Registry-Parameter (`applicable: false`).

| Feld | Einheit | Block | Bedeutung |
|---|---|---|---|
| `capex_fixed` | € | CAPEX | einmalig, mengenunabhängig (Planung/Konzept/Einrichtung) |
| `capex_per_unit` | €/Stück | CAPEX | Investition je Einheit (`unit_label`) |
| `capex_per_m2` | €/m² | CAPEX | Investition je abgedeckter Polygonfläche |
| `opex_fixed_year` | €/a | OPEX | wiederkehrend, mengenunabhängig (Betrieb/Koordination, z. B. Fortschreibung eines Hitzeaktionsplans) |
| `opex_per_unit_year` | €/(Stück·a) | OPEX | Betrieb & Unterhalt je Einheit und Jahr |
| `opex_per_m2_year` | €/(m²·a) | OPEX | Betrieb & Unterhalt je m² und Jahr |
| `unit_label` | – | – | z. B. „Brunnen", „Station", „km"; `None` ⇒ keine Stück-Logik |
| `unit_density_per_ha` | Stück/ha | – | Richtwert-Dichte (gesetzt, wenn `unit_label` gesetzt ist) |

> **Warum CAPEX/OPEX statt „Investition + Wartung":** Das frühere 5-Parameter-
> Modell stellte „Fixkosten" und „Investitionskosten" als Geschwister nebeneinander
> (zwei vermischte Achsen) und kannte auf der laufenden Seite nur `maintenance_*`.
> „Wartung" war faktisch schon eine Untermenge der Betriebskosten (Trinkbrunnen:
> „Betrieb/**Wartung**/Beprobung"; PV: „Betrieb, Wartung … und **Versicherung**").
> **OPEX** (Betrieb **und** Unterhalt) ist collectively exhaustive; `opex_fixed_year`
> schließt zusätzlich die Lücke für Konzept-/Planungsmaßnahmen mit mengen-
> unabhängigen Jahreskosten (z. B. Hitzeaktionsplan-Koordination).

**Formeln:**

$$\text{CAPEX} = \text{capex\_fixed} + \text{Anzahl} \times \text{capex\_per\_unit} + \text{Fläche} \times \text{capex\_per\_m2}$$
$$\text{OPEX/a} = \text{opex\_fixed\_year} + \text{Anzahl} \times \text{opex\_per\_unit\_year} + \text{Fläche} \times \text{opex\_per\_m2\_year}$$

- **Direkter Nutzen/Jahr:** `benefit_per_m2_year · Fläche` (unverändert, von der
  Kostenseite getrennt).
- **Vermiedene Schäden/Jahr (E3, Schicht B):** tatsächliches **Delta der summierten
  Zellkosten** — je abgedeckter Zelle und verknüpftem Risiko
  `Zellkosten · (1 − factor)`. Für pop-/area-skalierte Risiken ist das exakt der
  Beitrag der Maßnahme zur „Vermiedene Schäden"-Kennzahl des Kommunen-Aggregats,
  weil `compute_impact` und `_adjusted_cell_data`/`aggregate` dieselbe Zellkosten-
  Basis (`_cell_cost`, inkl. Legacy-Fallback für Alt-Zellen) und denselben Zell-
  Faktor benutzen. Flache Ausfall-/Screening-Risiken sind nicht zell-additiv
  (Aggregat P90-basiert) und tragen zu dieser Einzelmaßnahmen-Zeile nichts bei;
  ihre Minderung erscheint im Kommunen-Aggregat „mit Maßnahmen".
  Mindert eine Maßnahme **direkte Sektorschäden**, sinken auch die gekoppelten
  **Folgekosten** (`indirekt = k · Σ direkt`): das Aggregat „mit Maßnahmen"
  rekonsolidiert sie je Zelle aus den reduzierten Direktschäden
  (`_reconsolidate_cell_folgekosten`), und der Einzelmaßnahmen-Nutzen enthält den
  Anteil `k · Reduktion`, sodass Sidebar-Nutzen == Aggregat-Delta bleibt (§8/B3).
- Dashboard-Kostensektion (`cost-summary`) vergleicht Schäden **Basis** vs. **mit
  Maßnahmen** und summiert `capex_eur` / `opex_annual_eur` je Maßnahme; dieselbe
  Fläche/Anzahl/`unit_factor`-Herleitung wie `compute_impact`, damit Dashboard,
  Tabellen und Sidebar nicht divergieren (`_adjusted_cell_data`).

### Quellen & Provenienz (`sources`, `source_details`, `source_refs`)

Provenienz je Kostenfeld auf drei Ebenen (Keys = Feldnamen, inkl.
`default_reduction`/`unit_density_per_ha`) — Konvention wie bei `HAZARDS`/`RISKS`:

- **`source`** — Maßnahmen-Kurz-Key als Fallback.
- **`sources[feld]`** — kurze Inline-Quelle je Feld (Anzeige-Label in der Tabelle).
- **`source_details[feld]`** — Langtext für den Hover-Tooltip: *woher* der Wert
  stammt bzw. *wie* er hergeleitet/plausibilisiert wurde (z. B. „Blend aus Gründach
  40–70 €/m² (BuGG) und bodengebundener Fassade 15–35 €/m² (co2online) → 55 €/m²").
  Ohne belastbaren Beleg ehrlich „Modellannahme (…)".
- **`source_refs[feld] = [key, …]`** — Verweise auf die zentrale, zitierfähige
  Bibliografie `app/data/sources.py` (`SOURCE_REFERENCES`). Jeder Eintrag trägt
  eine **IEEE-Zitation**, die **Live-URL** und einen **archivierten Wayback-
  Snapshot** (`archive_url`) für den Fall, dass die Quelle offline geht.
  `sources.resolve()` löst die Keys auf; die aufgelösten Referenzen hängen an
  jeder `CostComponent` (`cost_breakdown`) und an jedem Maßnahmen-Registry-
  Parameter (`references`) und werden im (i)-Tooltip von **Sidebar und
  Konfigurations-Tabelle** als klickbare „Original"/„Archiv-Snapshot"-Links
  gerendert.

Neuen Snapshot ziehen (Internet Archive / Wayback Machine):
`curl -s -I "https://web.archive.org/save/<url>" | grep -i '^location:'` bzw.
jüngsten vorhandenen via `https://web.archive.org/cdx/search/cdx?url=<url>&output=json&limit=-1`.
Alle Werte bleiben per Config (`PUT /kommune/{id}/parameters`, mit
`custom_source`-Pflicht) überschreibbar.

### Anzahl (`count`)

`_resolve_count(mdef, config, covered_area_m2)` liefert `(count, is_default,
recommended_count)`. Fehlt `config["count"]` (Flächenmaßnahmen haben keine
Anzahl, Bestandsmaßnahmen ohne Frontend-Eingabe), greift die Richtwert-Anzahl
als Default und die Response markiert `count_is_default: true`, damit
bestehende Maßnahmen ohne Migration weiter sinnvoll rechnen.

### `cost_breakdown`-Response-Shape

`compute_costs(mdef, count, area_m2)` liefert die Rohdaten, die `compute_impact`
unter `cost_breakdown` zurückgibt (Pydantic-Dokumentation:
`CostComponent`/`CostBlock`/`CostBreakdown` in `schemas.py`). Nur Felder mit
`mdef[field] is not None` erzeugen eine Komponente; Quelle je Komponente ist
`custom_source` (bei kommunalem Override) sonst `sources[feld]` sonst `source`,
mit `overridden`-Flag, `source_detail` (Tooltip-Langtext) und `references`
(aufgelöste Bibliografie-Einträge):

```json
{
  "capex": {
    "total_eur": 75000,
    "components": [
      {"param": "capex_fixed", "label": "Grundkosten (Planung/Konzept)",
       "unit_price": 5000, "quantity": 1, "quantity_unit": "pauschal",
       "amount_eur": 5000, "source": "Modellannahme (…)",
       "source_detail": "…", "references": [], "overridden": false},
      {"param": "capex_per_unit", "label": "Investition je Brunnen",
       "unit_price": 14000, "quantity": 5, "quantity_unit": "Brunnen",
       "amount_eur": 70000, "source": "Berliner Wasserbetriebe",
       "source_detail": "Errichtung inkl. Anschluss ~10-16 T€/Standort -> 14.000 €",
       "references": [
         {"key": "BWB_Trinkbrunnen",
          "ieee": "Berliner Wasserbetriebe, „Trinkbrunnen in Berlin,“ … [Zugriff: 4. Juli 2026].",
          "url": "https://www.bwb.de/de/trinkbrunnen.php",
          "archive_url": "https://web.archive.org/web/20260704083542/https://www.bwb.de/de/trinkbrunnen.php",
          "accessed": "2026-07-04"}],
       "overridden": false}
    ]
  },
  "opex": {"total_eur": 17500, "components": [ … ]}
}
```

`unit_factor`/`count`/`recommended_count`/`unit_label` liegen zusätzlich als
eigene Top-Level-Felder auf der `MeasureImpactSummary`-Response; die
Summenfelder heißen `capex_eur` und `opex_annual_eur`.

---

## 8. Klimafortschreibung

`projection_service.project_group_risks`: skaliert die aktuellen KWRA-Gruppen-
Indizes mit dem DWD-Trend der heißen Tage (RCP4.5/8.5) bis ~2065.

---

## 9. API-Überblick

| Endpoint | Zweck |
|---|---|
| `GET /api/catalog` | fester H/E/V/Risiken/Maßnahmen/Sonstige/Gruppen-Katalog |
| `POST /api/admin/zensus/sync` | Zensus-CSVs herunterladen/cachen |
| `POST /api/kommune/{id}/assess` | vollständigen Lauf starten |
| `GET /api/kommune/{id}/status` | Fortschritt/Status (Polling) |
| `GET /api/kommune/{id}/layer/{code}` | GeoJSON einer Ebene (absolute Einheit bzw. Index) |
| `GET /api/kommune/{id}/risk-summary` | aggregierte Risiken + Gruppen + Kosten |
| `GET /api/kommune/{id}/risk-zones/{risk_code}` | Risikozonen |
| `GET /api/kommune/{id}/cost-summary` | Schäden mit/ohne Maßnahmen + Maßnahmenkosten |
| `GET /api/kommune/{id}/risk-projection` | Gruppen-Projektion RCP4.5/8.5 |
| `POST /api/kommune/{id}/measures` | Maßnahme anlegen (`config: {"count": …}` bei Stück-Maßnahmen) |
| `POST /api/measures/{id}/calculate-impact` | Wirkung/Kosten neu berechnen — Response inkl. `count`, `count_is_default`, `recommended_count`, `unit_label`, `unit_factor`, `cost_breakdown` (§7) |
| `GET /api/kommune/{id}/parameters` | Registry-Parameter (inkl. `measures.<code>.<feld>`), je Parameter `applicable`, `source_detail` (Tooltip-Langtext) und `references` (aufgelöste IEEE-Bibliografie mit Live- + Archiv-URL) |
| `PUT /api/kommune/{id}/parameters` | Parameter-Override setzen (`custom_source`-Pflicht für Kostenkomponenten-Herleitung) |

---

## 10. Datenmodell

- **`CellAssessment.data`** (JSONB) je Zelle:
  `{"inputs": {…}, "hazards": {CODE: wert}, "exposures": {…}, "vulnerabilities": {…},
   "auxiliary": {CODE: wert|null}, "risks": {CODE: {"index": …}}}`
- **`GridCell`:** `gitter_id`, `x_3035`, `y_3035` (Zensus INSPIRE 100m)
- **`ProjectStatus.task_key`** (String) statt früherem `climate_type`-Enum.
- **`RiskZone.layer_code`** (String) statt Enum.
- DB wurde für das neue Schema zurückgesetzt; Tabellen werden beim App-Start
  via `Base.metadata.create_all` sichergestellt.

### GeoPackage-Export

Layer **`bewertung_100m`**: H/E/V/R + `gitter_id` als Join-Schlüssel.
Layer **`sonstige_100m`**: alle `catalog.AUXILIARY`-Spalten aus `data.auxiliary`
(NULL bei fehlenden/geheimen Zensus-Werten).

---

## 11. „Nicht räumlich aufgelöst“ (Konstantwerte)

Alle Indikatoren mit `spatial=false` in `catalog.py` werden als regionaler/
nationaler Konstantwert auf alle Zellen angewendet (u. a. Meeresspiegelanstieg,
mittlerer Temperaturanstieg, demografische Quoten, einige Sturm-/Dürre-Proxys).
Sie sind in den Layer- und Dashboard-Tooltips entsprechend markiert.
