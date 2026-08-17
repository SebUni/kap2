export interface Kommune {
  id: number
  name: string
  bundesland?: string
  osm_id?: string
  area_km2?: number
  population?: number
  created_at: string
  boundary_geojson?: GeoJSONGeometry
}

export interface KommuneSearchResult {
  name: string
  osm_id: string
  osm_type: string
  display_name: string
  lat: number
  lon: number
  address?: Record<string, string>
  geojson?: Record<string, unknown>
}

export interface StepHistoryEntry {
  label: string
  detail: string
  started: string
  finished: string | null
  pct_start: number
  pct_end: number | null
}

export interface AssessmentStatus {
  status: 'pending' | 'queued' | 'running' | 'done' | 'error' | null
  progress_pct: number
  message?: string | null
  started_at?: string | null
  finished_at?: string | null
  step_history: StepHistoryEntry[]
  eta_seconds?: number | null
  queue_position?: number | null
  recalc_recommended?: boolean
}

export interface GeoExportJob {
  id: number
  export_type: 'geodaten' | 'dashboard' | 'massnahmen' | 'alle'
  status: 'pending' | 'running' | 'done' | 'error'
  created_at: string
  finished_at: string | null
  error_message: string | null
}

export interface ConfigParameter {
  id: number
  category: string
  key: string
  value: number | string | boolean
  description?: string
}

export interface Measure {
  id: number
  kommune_id: number
  name: string
  measure_type: string
  geometry_geojson?: GeoJSONGeometry
  config: Record<string, unknown>
  implementation_year?: number
  description?: string
  created_at: string
  /** Serverseitig frisch gehaltene Wirkung (GET /measures läuft ensure_fresh_impact_summary). */
  impact_summary?: MeasureImpactSummary | null
}

export interface SourceReference {
  key: string
  ieee: string
  url: string
  archive_url: string
  accessed: string
}

export interface CostComponent {
  param: string
  label: string
  unit_price: number
  quantity: number
  quantity_unit: string
  amount_eur: number
  source: string
  source_detail?: string
  references?: SourceReference[]
  overridden: boolean
}

export interface CostBlock {
  total_eur: number
  components: CostComponent[]
}

export interface CostBreakdown {
  capex: CostBlock
  opex: CostBlock
}

export interface MeasureImpactSummary {
  measure_id: number
  measure_type?: string
  affected_cells: number
  affected_area_m2?: number
  linked_risk_codes?: string[]
  avg_index_reduction_pct?: number
  capex_eur?: number
  opex_annual_eur?: number
  annual_benefit_eur?: number
  /** Vermiedene Zellschäden (inkl. gekoppelter Folgekosten). */
  annual_benefit_damage_eur?: number
  /** Vermiedene Ausfallkosten kommunenweiter P90-Risiken. */
  annual_benefit_flat_eur?: number
  /** Direkter Zusatznutzen (Erträge/Erlöse, benefit_per_m2_year · Fläche). */
  annual_benefit_direct_eur?: number
  /** true, wenn der Schadens-Nutzen am Gesamtschaden der verknüpften Risiken gekappt wurde. */
  benefit_capped?: boolean
  count?: number
  count_is_default?: boolean
  recommended_count?: number
  unit_label?: string | null
  unit_factor?: number
  cost_breakdown?: CostBreakdown
  message?: string
}

// ── GeoJSON ─────────────────────────────────────────────────────────────────

export interface GeoJSONFeatureCollection {
  type: 'FeatureCollection'
  features: GeoJSONFeature[]
  meta?: LayerMeta
}

export interface GeoJSONFeature {
  type: 'Feature'
  properties: Record<string, unknown>
  geometry: GeoJSONGeometry
}

export interface GeoJSONGeometry {
  type: string
  coordinates: unknown
}

export type InputProvenance = 'extern' | 'param' | 'computed'

export interface RecipeInputMeta {
  key: string
  label: string
  prov: InputProvenance
  unit: string
  source?: string
  value?: number | string
}

export interface IndicatorRecipe {
  formula: string
  inputs: RecipeInputMeta[]
}

export interface HevRecipeMeta {
  code: string
  name: string
  unit: string
  norm_min?: number
  norm_max?: number
  source?: string
  spatial?: boolean
}

export interface OutcomeFactorMeta {
  key: string
  label: string
  value?: number
  unit?: string
  formula?: string
  source?: string
  prov?: InputProvenance
}

export interface CellOutcomeBreakdown {
  ref_value: number
  scale_factor: number
  index_fraction: number
  cell_pop: number
  cell_area_km2: number
  outcome: number
}

export interface PathwaySource {
  key?: string
  ieee?: string
  url?: string
  archive_url?: string
}

export interface PathwayRecipeMeta {
  type: string
  type_label: string
  weight: number
  hazard: string
  exposure: string
  vulnerability: string
  hazard_name: string
  exposure_name: string
  vulnerability_name: string
  chain_description?: string
  chain_label?: string
  justification?: string
  justification_ref?: string
  justification_source?: PathwaySource | null
  cluster?: string
  formula: string
}

export interface CellPathwayTerm {
  type: string
  weight: number
  hazard: string
  exposure: string
  vulnerability: string
  h_norm: number
  e_norm: number
  v_norm: number
  term: number
  is_max?: boolean
}

export interface CellPathwayBreakdown {
  pathways: CellPathwayTerm[]
  max_term: number
  index: number
}

export interface RiskRecipe {
  formula_index: string
  formula_index_header?: string
  formula_outcome: string
  pathways: PathwayRecipeMeta[]
  weight_sum: number
  hazards: HevRecipeMeta[]
  exposures: HevRecipeMeta[]
  vulnerabilities: HevRecipeMeta[]
  scale: string
  ref_value: number
  outcome_factors: OutcomeFactorMeta[]
}

export type LayerRecipe = IndicatorRecipe | RiskRecipe

export interface LayerRecipeMeta {
  code: string
  category: LayerCategory
  label: string
  description?: string
  unit?: string
  norm_min?: number
  norm_max?: number
  source?: string
  proxy?: string
  spatial?: boolean
  group?: string
  recipe: LayerRecipe
  lineage?: LineageGraph
}

export type LineageNodeType =
  | 'source' | 'parameter' | 'intermediate' | 'hazard' | 'exposure' | 'vulnerability'
  | 'pathway' | 'aggregation' | 'outcome' | 'norm' | 'operator'

export interface LineageNodeData {
  id: string
  type: LineageNodeType
  label: string
  column: number
  collapse_group: string
  // Ergebnisknoten (type 'outcome') tragen meta.result_kind:
  // 'index' (KWRA-Index 0–100) | 'native' (absolutes Ergebnis, z. B. Todesfälle/Jahr)
  // | 'eur' (Monetärer Schaden €/Jahr). Ergebnisse sind im Diagramm nie ausblendbar.
  meta?: Record<string, unknown>
}

export interface LineageEdgeData {
  id: string
  source: string
  target: string
  label?: string | null
  parameter_id?: string | null
  meta?: Record<string, unknown>
}

export interface LineageCollapseGroup {
  id: string
  label: string
  default_collapsed?: boolean
}

export interface LineageGraph {
  nodes: LineageNodeData[]
  edges: LineageEdgeData[]
  collapse_groups: LineageCollapseGroup[]
}

export interface ModelParameter {
  id: string
  layer_code: string
  layer_category: string
  label: string
  value: number | string
  default_value: number | string
  unit: string
  source: string
  source_detail?: string
  references?: SourceReference[]
  prov: string
  editable: boolean
  overridden: boolean
  custom_source?: string | null
  applicable?: boolean
  // Demo: read-only (demo_locked) bzw. Wert/Quelle verborgen (demo_hidden)
  demo_locked?: boolean
  demo_hidden?: boolean
}

export interface ResolvedInput {
  v: number | string | null
  prov: InputProvenance
}

export interface LayerMeta {
  code: string
  category: LayerCategory
  label: string
  unit: string
  min: number
  max: number
  scale_max?: number
  recipe?: LayerRecipe
}

// ── Katalog (vom Backend, single source of truth) ───────────────────────────

export type LayerCategory = 'hazards' | 'exposures' | 'vulnerabilities' | 'risks' | 'auxiliary'
export type GroupKey = 'measures' | 'risks' | 'hazards' | 'exposures' | 'vulnerabilities' | 'auxiliary'

export interface CatalogIndicator {
  code: string
  name: string
  description: string
  unit: string
  spatial?: boolean
  coastal?: boolean
  norm_min: number
  norm_max: number
  proxy: string
  source: string
  category?: string
}

export interface CatalogRisk {
  code: string
  name: string
  description: string
  outcome_unit: string
  group: string
  cost_dimension: string
  hazards: string[]
  exposures: string[]
  vulnerabilities: string[]
  priority?: number
}

export interface CatalogMeasure {
  code: string
  name: string
  description: string
  measure_type: string
  effect_target: string[]
  linked_risk_codes: string[]
  default_reduction: number
  coverage_scaling: string
  capex_fixed: number | null
  capex_per_unit: number | null
  capex_per_m2: number | null
  opex_fixed_year: number | null
  opex_per_unit_year: number | null
  opex_per_m2_year: number | null
  benefit_per_m2_year: number
  unit_label: string | null
  unit_density_per_ha: number | null
  source: string
  sources?: Record<string, string>
  source_details?: Record<string, string>
  kang_cluster?: string
  kang_field?: string
}

export interface CategoryDef {
  code: string
  label: string
}

export interface KangField {
  code: string
  label: string
}

export interface KangCluster {
  code: string
  label: string
  fields: KangField[]
}

export interface KwraGroup {
  code: string
  challenge: string
  label: string
  color: string
  description: string
}

export interface Catalog {
  groups: KwraGroup[]
  hazards: CatalogIndicator[]
  exposures: CatalogIndicator[]
  vulnerabilities: CatalogIndicator[]
  risks: CatalogRisk[]
  measures: CatalogMeasure[]
  hazard_categories: CategoryDef[]
  exposure_categories: CategoryDef[]
  vulnerability_categories: CategoryDef[]
  kang_clusters: KangCluster[]
  auxiliary: CatalogIndicator[]
  auxiliary_categories: CategoryDef[]
}

// ── Risiko-Histogramm (Verteilung Index-Höhen je Risiko) ─────────────────────

export interface RiskHistogramEntry {
  name: string
  group: string
  outcome_unit: string
  cost_dimension: string
  counts: number[]
  nonzero_cells: number
  p90_index: number
  max_index: number
  outcome: number
  /** Aggregierter Outcome (= outcome; Σ über Zellen für pop/area, sonst P90-basiert). */
  outcome_sum?: number
  cost_eur: number
  /** "sum" (Σ über Zellen, pop/area) | "p90" (kommunenweiter Einzelwert, flat). */
  aggregation?: 'sum' | 'p90'
  /** Anteil der Summe aus den stärksten 5 % Zellen (Konzentration/Hotspot-Signal). */
  top5_share?: number
  /** Fläche der Zellen über der Risikozonen-Schwelle (km²). */
  area_km2_affected?: number
  /** Anteil der Zellen über der Risikozonen-Schwelle. */
  share_above_threshold?: number
}

export interface RiskHistogram {
  total_cells: number
  bin_labels: string[]
  bin_centers: number[]
  bin_width: number
  risks: Record<string, RiskHistogramEntry>
}

// ── Aggregierte Risiken / Kosten ─────────────────────────────────────────────

/** Risikoklasse aus Server-Klassifikation (Grenzen in RiskAggregate.classification). */
export type RiskClass = 'gering' | 'mittel' | 'hoch'

export interface RiskAggregateEntry {
  index: number
  /** = index (P90 der Zell-Indizes, Screening-Kennzahl). */
  p90_index?: number
  /** Belastungs-P90: P90 nur über expositionsrelevante Zellen (Anzeige-Leitgröße). */
  exposed_p90_index?: number
  /** Exponierte Perzentile P80/P85/P95 für die gestuften Radar-Bänder. */
  exposed_p80_index?: number
  exposed_p85_index?: number
  exposed_p95_index?: number
  /** Anteil expositionsrelevanter Zellen an allen Zellen (0..1). */
  exposure_share?: number
  risk_class?: RiskClass
  max_index: number
  outcome: number
  /** Aggregierter Outcome (Summe der Zell-Outcomes für pop/area, sonst P90-basiert). */
  outcome_sum?: number
  outcome_unit: string
  cost_eur: number
  cost_dimension: string
  group: string
  name: string
  /** "sum" (Σ über Zellen, pop/area) | "p90" (kommunenweiter Einzelwert, flat). */
  aggregation?: 'sum' | 'p90'
  /** Anteil der Summe aus den stärksten 5 % Zellen (Konzentration/Hotspot-Signal). */
  top5_share?: number
  /** Fläche der Zellen über der Risikozonen-Schwelle (km²). */
  area_km2_affected?: number
  /** Anteil der Zellen über der Risikozonen-Schwelle. */
  share_above_threshold?: number
}

export interface RiskGroupEntry {
  label: string
  color: string
  index: number
  /** Mittel der Belastungs-P90-Werte der Einzelrisiken (Anzeige-Leitgröße). */
  exposed_index?: number
  /** Gruppen-Mittel der exponierten Perzentile P80/P85/P95 (gestufte Radar-Bänder). */
  exposed_p80_index?: number
  exposed_p85_index?: number
  exposed_p95_index?: number
  risk_class?: RiskClass
  risk_codes: string[]
}

export interface RiskAggregate {
  risks: Record<string, RiskAggregateEntry>
  groups: Record<string, RiskGroupEntry>
  cost: {
    total_eur: number
    by_risk: {
      code: string; name: string; cost_eur: number; outcome: number
      outcome_unit: string; cost_dimension: string; index: number
      exposed_p90_index?: number; risk_class?: RiskClass
      aggregation?: 'sum' | 'p90'; top5_share?: number
    }[]
  }
  /** Server-Wahrheit der Risikoklassen (Grenzen folgen model.risk_threshold). */
  classification?: {
    basis: string
    bounds: { medium_min: number; high_min: number }
    labels: Record<RiskClass, string>
  }
}

export interface CostSummary {
  damages_base_eur: number
  damages_with_measures_eur: number
  damage_reduction_eur: number
  by_risk: RiskAggregate['cost']['by_risk']
  measures: {
    total_capex_eur: number
    total_opex_annual_eur: number
    total_annual_benefit_eur: number
    /** Vermiedene Zellschäden (Diagnostik; belastbar ist damage_reduction_eur). */
    total_benefit_damage_eur?: number
    /** Vermiedene Ausfallkosten kommunenweiter P90-Risiken. */
    total_benefit_flat_eur?: number
    /** Direkter Zusatznutzen (Erträge/Erlöse), additiv zu vermiedenen Schäden. */
    total_benefit_direct_eur?: number
    /** true, wenn Σ Pro-Maßnahmen-Schadensnutzen grob von der Aggregat-Differenz abweicht. */
    benefit_consistency_warning?: boolean
    rows: {
      id: number; name: string; measure_type: string
      capex_eur: number; opex_annual_eur: number; annual_benefit_eur: number
      annual_benefit_damage_eur?: number; annual_benefit_flat_eur?: number
      annual_benefit_direct_eur?: number; benefit_capped?: boolean
    }[]
  }
}

export interface RiskProjection {
  years: number[]
  groups: {
    code: string; label: string; color: string; base_index: number
    rcp45: number[]; rcp85: number[]
  }[]
  source: string
}

// ── Kommunen-Profil (GET /kommune/{id}/profile) ─────────────────────────────

export interface ClimateMetric {
  code: string
  label: string
  unit: string
  value: number | null
  data_basis: 'dwd_cdc_raster' | 'regional_fallback' | 'unavailable'
  germany: { value: number; period: string | null } | null
  delta: number | null
  delta_pct: number | null
  references: SourceReference[]
}

export interface KommuneProfile {
  id: number
  name: string
  bundesland: string | null
  landkreis: string | null
  lat: number | null
  lon: number | null
  area_km2: number | null
  population: number | null
  population_source: string | null
  elevation: { mean_m: number; min_m: number; max_m: number; source: string } | null
  /** BIP (amtlich nur Kreisebene, Regionalstatistik); null ohne GENESIS-Zugang.
   *  `estimated_municipal_eur` = auf die Kommune geschätzt (BIP je Einwohner des
   *  Kreises × Einwohner); `gdp_meur` bleibt der amtliche Kreiswert (Mio €). */
  economy: {
    gdp_meur: number; gdp_year: number | null; level: 'kreis'
    gdp_per_capita_eur: number | null
    estimated_municipal_eur: number | null
    source: string; references: SourceReference[]
  } | null
  /** Kommunaler Haushalt: Auszahlungen, Ø der letzten verfügbaren Jahre (Gemeindeebene). */
  municipal_budget: {
    avg_expenditure_eur: number; years: number[]; level: 'gemeinde'
    source: string; references: SourceReference[]
  } | null
  climate: ClimateMetric[]
  sources_note: string
}

// ── Kosten-Projektion (GET /kommune/{id}/cost-projection) ───────────────────

export interface CostProjectionSeries {
  annual: number[]
  cumulative: number[]
}

export interface CostProjectionScenario {
  label: string
  no_measures: CostProjectionSeries
  with_measures: CostProjectionSeries & {
    components: { damages: number[]; opex: number[]; capex: number[] }
  }
}

export interface CostProjection {
  years: number[]
  base_year_damages_eur: number
  has_measures: boolean
  scenarios: { rcp45: CostProjectionScenario; rcp85: CostProjectionScenario }
  by_group_base: Record<string, number>
  measures: {
    id: number; name: string; implementation_year: number
    capex_eur: number; opex_annual_eur: number
  }[]
  assumptions: string[]
  warnings: string[]
  source?: string
}

export const GROUP_ORDER: { key: GroupKey; label: string }[] = [
  { key: 'measures', label: 'Maßnahmen' },
  { key: 'risks', label: 'Klimarisiken' },
  { key: 'hazards', label: 'Klimatische Einflüsse' },
  { key: 'exposures', label: 'Räumliche Expositionen' },
  { key: 'vulnerabilities', label: 'Sensitivitäten' },
  { key: 'auxiliary', label: 'Sonstige' },
]
