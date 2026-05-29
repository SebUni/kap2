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

export interface GridCell {
  id: number
  row: number
  col: number
  cell_size_m: number
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
  climate_type: string
  level: number
  progress_pct: number
  status: 'pending' | 'running' | 'done' | 'error'
  message?: string
  started_at?: string
  finished_at?: string
  step_history: StepHistoryEntry[]
  eta_seconds?: number | null
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

export interface MeasureImpact {
  id: number
  grid_cell_id: number
  indicator_deltas: Record<string, number>
  costs: Record<string, number>
  savings: Record<string, number>
}

export interface MeasureImpactSummary {
  measure_id: number
  affected_cells: number
  affected_area_m2?: number
  total_indicator_deltas: Record<string, number>
  total_costs: Record<string, number>
  total_savings: Record<string, number>
}

export interface MeasureTypeDef {
  label: string
  params: { key: string; label: string; type: string; default: number }[]
}

export interface GeoJSONFeatureCollection {
  type: 'FeatureCollection'
  features: GeoJSONFeature[]
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

export interface ClimateTypeInfo {
  climate_type: string
  label: string
  max_level: number
  indicators: { key: string; label: string; unit: string; description: string }[]
}

// ── Risk Zone Types ───────────────────────────────────────────────────────────

export interface RiskZone {
  zone_index: number
  cell_count: number
  mean_risk: number
  max_risk: number
  area_m2: number
  climate_type: string
}

export interface RiskSummary {
  climate_type: string
  zone_count: number
  total_area_m2: number
  aggregated_risk: number
  highest_zone_risk: number
}

export interface RiskProjectionYear {
  year: number
  rcp45: { zone_count: number; mean_severity: number; max_severity: number; total_cells_at_risk: number }
  rcp85: { zone_count: number; mean_severity: number; max_severity: number; total_cells_at_risk: number }
}

export type RiskProjection = RiskProjectionYear[]

// Climate type display metadata
export const CLIMATE_TYPE_META: Record<string, { label: string; icon: string; color: string }> = {
  heat: { label: 'Hitze', icon: '🌡️', color: '#ef4444' },
  heavy_rain: { label: 'Starkregen', icon: '🌧️', color: '#3b82f6' },
  river_flood: { label: 'Hochwasser', icon: '🌊', color: '#0ea5e9' },
  drought: { label: 'Dürre', icon: '🏜️', color: '#f59e0b' },
  forest_fire: { label: 'Waldbrand', icon: '🌲', color: '#22c55e' },
  agriculture: { label: 'Landwirtschaft', icon: '🌾', color: '#84cc16' },
  storms: { label: 'Stürme', icon: '💨', color: '#8b5cf6' },
  sea_level: { label: 'Meeresspiegel', icon: '🌊', color: '#06b6d4' },
}
