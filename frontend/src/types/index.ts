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

export interface LayerMeta {
  code: string
  category: LayerCategory
  label: string
  unit: string
  min: number
  max: number
  scale_max?: number
}

// ── Katalog (vom Backend, single source of truth) ───────────────────────────

export type LayerCategory = 'hazards' | 'exposures' | 'vulnerabilities' | 'risks'
export type GroupKey = 'measures' | 'risks' | 'hazards' | 'exposures' | 'vulnerabilities'

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
  cost_per_m2: number
  cost_per_unit: number
  maintenance_per_m2_year: number
  benefit_per_m2_year: number
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
}

// ── Risiko-Histogramm (Verteilung Index-Höhen je Risiko) ─────────────────────

export interface RiskHistogramEntry {
  name: string
  group: string
  outcome_unit: string
  cost_dimension: string
  counts: number[]
  nonzero_cells: number
  mean_index: number
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
  { key: 'hazards', label: 'Klimatreiber' },
  { key: 'exposures', label: 'Expositionen' },
  { key: 'vulnerabilities', label: 'Verwundbarkeiten' },
]
