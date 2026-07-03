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
  status: 'pending' | 'running' | 'done' | 'error' | null
  progress_pct: number
  message?: string | null
  started_at?: string | null
  finished_at?: string | null
  step_history: StepHistoryEntry[]
  eta_seconds?: number | null
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
}

export interface CostComponent {
  param: string
  label: string
  unit_price: number
  quantity: number
  quantity_unit: string
  amount_eur: number
  source: string
  overridden: boolean
}

export interface CostBlock {
  total_eur: number
  components: CostComponent[]
}

export interface CostBreakdown {
  investment: CostBlock
  annual_maintenance: CostBlock
}

export interface MeasureImpactSummary {
  measure_id: number
  measure_type?: string
  affected_cells: number
  affected_area_m2?: number
  linked_risk_codes?: string[]
  avg_index_reduction_pct?: number
  investment_eur?: number
  annual_maintenance_eur?: number
  annual_benefit_eur?: number
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
}

export interface CellPathwayBreakdown {
  pathways: CellPathwayTerm[]
  weight_sum: number
  term_sum: number
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
  prov: string
  editable: boolean
  overridden: boolean
  custom_source?: string | null
  applicable?: boolean
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
  cost_fixed: number | null
  cost_per_m2: number | null
  cost_per_unit: number | null
  maintenance_per_m2_year: number | null
  maintenance_per_unit_year: number | null
  benefit_per_m2_year: number
  unit_label: string | null
  unit_density_per_ha: number | null
  source: string
  sources?: Record<string, string>
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
  cost_eur: number
}

export interface RiskHistogram {
  total_cells: number
  bin_labels: string[]
  bin_centers: number[]
  bin_width: number
  risks: Record<string, RiskHistogramEntry>
}

// ── Aggregierte Risiken / Kosten ─────────────────────────────────────────────

export interface RiskAggregateEntry {
  index: number
  max_index: number
  outcome: number
  outcome_unit: string
  cost_eur: number
  cost_dimension: string
  group: string
  name: string
}

export interface RiskGroupEntry {
  label: string
  color: string
  index: number
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
    }[]
  }
}

export interface CostSummary {
  damages_base_eur: number
  damages_with_measures_eur: number
  damage_reduction_eur: number
  by_risk: RiskAggregate['cost']['by_risk']
  measures: {
    total_investment_eur: number
    total_annual_maintenance_eur: number
    total_annual_benefit_eur: number
    rows: {
      id: number; name: string; measure_type: string
      investment_eur: number; annual_maintenance_eur: number; annual_benefit_eur: number
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

export const GROUP_ORDER: { key: GroupKey; label: string }[] = [
  { key: 'measures', label: 'Maßnahmen' },
  { key: 'risks', label: 'Klimarisiken' },
  { key: 'hazards', label: 'Klimatische Einflüsse' },
  { key: 'exposures', label: 'Räumliche Expositionen' },
  { key: 'vulnerabilities', label: 'Sensitivitäten' },
  { key: 'auxiliary', label: 'Sonstige' },
]
