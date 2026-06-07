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

- **Fest verdrahtet:** Hazards (23), Expositionen (23), Verwundbarkeiten (33),
  Risiken (48) und Maßnahmen (46) sind als Python-Konstanten in
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
| **Zensus 2022** (100m-Gitter, falls vorhanden) | Bevölkerung je Zelle; sonst OSM-Wohngebäudevolumen-Proxy |
| **Zensus Demografie** | Alters-/Risikogruppen-Anteile |
| **AWS Terrarium DEM** | Mittelhöhe, Hangneigung, Senkentiefe, D8-Abfluss, TWI je Zelle |
| **OSM Gewässer** | `natural=water`, `waterway` → Distanz/Proximität zu Fließ- und Stillgewässern |

Mehrkern-Verarbeitung: `multiprocessing` (fork, bis 8 Worker, Chunk 50) für die
OSM-Aggregation je Zelle (wiederverwendet aus dem alten Hitze-Assessor).

---

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

## 4. Hazards / Expositionen / Verwundbarkeiten (absolut)

Berechnung in `engine/indicators.py:compute_cell_hev`. Jeder Code besitzt im
Katalog: `unit`, `[norm_min, norm_max]`, `spatial`, `proxy`, `source`,
`description` (alle im `(i)`-Tooltip sichtbar).

- **Räumlich aufgelöst (`spatial=true`):** aus Zell-Inputs abgeleitet
  (z. B. `POPULATION_DENSITY` aus Zensus/OSM, `HEAT_WAVE`/`UHI_INTENSITY` aus ΔT,
  `IMPERVIOUSNESS` aus OSM).
- **Konstant (`spatial=false`):** regionaler Wert für alle Zellen
  (z. B. `SEA_LEVEL_RISE`, `MEAN_TEMPERATURE_RISE`, demografische Quoten).
  Diese sind in den Tooltips als „nicht räumlich aufgelöst“ gekennzeichnet.

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
- `outcome = ref_value · (mean_index/100) · scale_factor`
- `scale`: `pop` → Einwohner/100 000, `area` → Fläche/50 km², `flat` → 1
- Kosten: bei `cost_dimension = monetary` ist `cost_eur = outcome`;
  sonst `outcome · cost_per_outcome_eur` (z. B. Mortalität × Wert eines
  statistischen Lebens).

### Aggregation (`risk_engine.aggregate`)
Je Risiko: Mittel-Index über alle Zellen, Max-Index, Outcome, Kosten.
Je KWRA-Gruppe: Mittelwert der Risiko-Indizes (übergreifende Metrik fürs
Spinnendiagramm).

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
abgedeckten Zellen, deckungs-skaliert. Da der Risiko-Index multiplikativ in
H·E·V ist, wirkt die Reduktion analytisch als Index-Skalierung:

$$r_{\text{eff}} = \mathrm{clamp}(r_{\text{default}} \cdot s(\text{coverage}),\,0,\,0.95)$$
$$\text{factor} = (1 - r_{\text{eff}})^{\,n_{\text{targets}}}, \qquad \text{Index}_{\text{neu}} = \text{Index} \cdot \text{factor}$$

- `coverage_scaling = linear` → `s = fraction`;
  `saturating` → `s = min(1, fraction·1.5)`.
- `default_reduction` je Maßnahme im Katalog (typabhängig, dokumentiert; in
  Config überschreibbar). Quelle: KAP3-Vorschlag + Plausibilitätskalibrierung.

### Kosten / Nutzen
- **Investition:** `cost_per_unit + cost_per_m2 · abgedeckte_Fläche`
- **Unterhalt/Jahr:** `maintenance_per_m2_year · Fläche`
- **Direkter Nutzen/Jahr:** `benefit_per_m2_year · Fläche`
- **Vermiedene Schäden/Jahr:** monetarisierte Index-Reduktion der verknüpften
  monetären Risiken (Anteil der reduzierten Indexsumme an der Gesamtsumme ×
  Risikokosten).
- Dashboard-Kostensektion vergleicht Schäden **Basis** vs. **mit Maßnahmen**
  (`measures.get_risk_aggregate(apply_measures=True/False)`).

---

## 8. Klimafortschreibung

`projection_service.project_group_risks`: skaliert die aktuellen KWRA-Gruppen-
Indizes mit dem DWD-Trend der heißen Tage (RCP4.5/8.5) bis ~2065.

---

## 9. API-Überblick

| Endpoint | Zweck |
|---|---|
| `GET /api/catalog` | fester H/E/V/Risiken/Maßnahmen/Gruppen-Katalog |
| `POST /api/kommune/{id}/assess` | vollständigen Lauf starten |
| `GET /api/kommune/{id}/status` | Fortschritt/Status (Polling) |
| `GET /api/kommune/{id}/layer/{code}` | GeoJSON einer Ebene (absolute Einheit bzw. Index) |
| `GET /api/kommune/{id}/risk-summary` | aggregierte Risiken + Gruppen + Kosten |
| `GET /api/kommune/{id}/risk-zones/{risk_code}` | Risikozonen |
| `GET /api/kommune/{id}/cost-summary` | Schäden mit/ohne Maßnahmen + Maßnahmenkosten |
| `GET /api/kommune/{id}/risk-projection` | Gruppen-Projektion RCP4.5/8.5 |

---

## 10. Datenmodell

- **`CellAssessment.data`** (JSONB) je Zelle:
  `{"hazards": {CODE: wert}, "exposures": {…}, "vulnerabilities": {…}, "risks": {CODE: {"index": …}}}`
- **`ProjectStatus.task_key`** (String) statt früherem `climate_type`-Enum.
- **`RiskZone.layer_code`** (String) statt Enum.
- DB wurde für das neue Schema zurückgesetzt; Tabellen werden beim App-Start
  via `Base.metadata.create_all` sichergestellt.

---

## 11. „Nicht räumlich aufgelöst“ (Konstantwerte)

Alle Indikatoren mit `spatial=false` in `catalog.py` werden als regionaler/
nationaler Konstantwert auf alle Zellen angewendet (u. a. Meeresspiegelanstieg,
mittlerer Temperaturanstieg, demografische Quoten, einige Sturm-/Dürre-Proxys).
Sie sind in den Layer- und Dashboard-Tooltips entsprechend markiert.
