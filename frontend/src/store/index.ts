import { create } from 'zustand'
import { api } from '../api/client'
import type {
  Kommune, AssessmentStatus, ConfigParameter, Measure,
  GeoJSONFeatureCollection, MeasureImpactSummary,
  Catalog, RiskAggregate, CostSummary, RiskProjection, RiskHistogram,
  LayerCategory,
} from '../types'

export interface ActiveLayer {
  category: LayerCategory
  code: string
}

interface AppState {
  activeTab: number
  setActiveTab: (tab: number) => void

  // Kommune
  kommune: Kommune | null
  setKommune: (k: Kommune | null) => void
  loadKommune: (id: number) => Promise<void>

  // Grid
  gridGeoJson: GeoJSONFeatureCollection | null
  loadGrid: (kommuneId: number) => Promise<void>
  generateGrid: (kommuneId: number, cellSize?: number, force?: boolean) => Promise<void>

  // Catalog (single source of truth, loaded once)
  catalog: Catalog | null
  loadCatalog: () => Promise<void>

  // Assessment (single full run)
  status: AssessmentStatus | null
  hasAssessment: boolean
  loadStatus: (kommuneId: number) => Promise<AssessmentStatus | null>
  startAssessment: (kommuneId: number) => Promise<void>
  abortAssessment: (kommuneId: number) => Promise<void>

  // Active map layer (choropleth)
  activeLayer: ActiveLayer | null
  layerGeoJson: GeoJSONFeatureCollection | null
  setActiveLayer: (layer: ActiveLayer | null) => Promise<void>
  showMeasures: boolean
  setShowMeasures: (v: boolean) => void

  // Risk / cost aggregates
  riskSummary: RiskAggregate | null
  costSummary: CostSummary | null
  riskProjection: RiskProjection | null
  riskHistogram: RiskHistogram | null
  loadRiskSummary: (kommuneId: number) => Promise<void>
  loadCostSummary: (kommuneId: number) => Promise<void>
  loadRiskProjection: (kommuneId: number) => Promise<void>
  loadRiskHistogram: (kommuneId: number) => Promise<void>

  // Climate data (DWD)
  climateHistory: Record<string, unknown> | null
  regionalClimate: Record<string, unknown> | null
  climateProjection: Record<string, unknown> | null
  loadClimateHistory: (kommuneId: number) => Promise<void>
  loadRegionalClimate: (kommuneId: number) => Promise<void>
  loadClimateProjection: (kommuneId: number) => Promise<void>

  // Config
  configParams: ConfigParameter[]
  loadConfig: (kommuneId: number) => Promise<void>
  updateConfig: (kommuneId: number, updates: { category: string; key: string; value: unknown }[]) => Promise<void>

  // Measures
  measures: Measure[]
  selectedMeasure: Measure | null
  setSelectedMeasure: (m: Measure | null) => void
  loadMeasures: (kommuneId: number) => Promise<void>
  createMeasure: (kommuneId: number, data: Record<string, unknown>) => Promise<Measure>
  updateMeasure: (id: number, data: Record<string, unknown>) => Promise<Measure>
  deleteMeasure: (id: number) => Promise<void>
  calculateImpact: (measureId: number) => Promise<MeasureImpactSummary>

  // Drawing
  isDrawing: boolean
  setIsDrawing: (d: boolean) => void
  drawnGeometry: Record<string, unknown> | null
  setDrawnGeometry: (g: Record<string, unknown> | null) => void

  // Reset
  resetKommune: (kommuneId: number) => Promise<void>
}

export const useStore = create<AppState>((set, get) => ({
  activeTab: 0,
  setActiveTab: (tab) => set({ activeTab: tab }),

  // Kommune
  kommune: null,
  setKommune: (k) => set({ kommune: k }),
  loadKommune: async (id) => {
    if (get().kommune?.id !== id) {
      set({ riskSummary: null, costSummary: null, riskHistogram: null })
    }
    const data = await api.getKommune(id)
    set({ kommune: data as unknown as Kommune })
  },

  // Grid
  gridGeoJson: null,
  loadGrid: async (kommuneId) => {
    const data = await api.getGrid(kommuneId)
    set({ gridGeoJson: data as unknown as GeoJSONFeatureCollection })
  },
  generateGrid: async (kommuneId, cellSize = 100, force = false) => {
    await api.generateGrid(kommuneId, cellSize, force)
    await get().loadGrid(kommuneId)
  },

  // Catalog
  catalog: null,
  loadCatalog: async () => {
    if (get().catalog) return
    const data = await api.getCatalog()
    set({ catalog: data as unknown as Catalog })
  },

  // Assessment
  status: null,
  hasAssessment: false,
  loadStatus: async (kommuneId) => {
    const data = await api.getStatus(kommuneId) as unknown as AssessmentStatus
    set({ status: data, hasAssessment: data?.status === 'done' })
    return data
  },
  startAssessment: async (kommuneId) => {
    await api.startAssessment(kommuneId)
    await get().loadStatus(kommuneId)
  },
  abortAssessment: async (kommuneId) => {
    await api.abortAssessment(kommuneId)
    await get().loadStatus(kommuneId)
  },

  // Active layer
  activeLayer: null,
  layerGeoJson: null,
  setActiveLayer: async (layer) => {
    set({ activeLayer: layer })
    const k = get().kommune
    if (!layer || !k) { set({ layerGeoJson: null }); return }
    try {
      const data = await api.getLayer(k.id, layer.code)
      set({ layerGeoJson: data as unknown as GeoJSONFeatureCollection })
    } catch {
      set({ layerGeoJson: null })
    }
  },
  showMeasures: true,
  setShowMeasures: (v) => set({ showMeasures: v }),

  // Aggregates
  riskSummary: null,
  costSummary: null,
  riskProjection: null,
  riskHistogram: null,
  loadRiskSummary: async (kommuneId) => {
    const data = await api.getRiskSummary(kommuneId)
    set({ riskSummary: data as unknown as RiskAggregate })
  },
  loadCostSummary: async (kommuneId) => {
    const data = await api.getCostSummary(kommuneId)
    set({ costSummary: data as unknown as CostSummary })
  },
  loadRiskProjection: async (kommuneId) => {
    const data = await api.getRiskProjection(kommuneId)
    set({ riskProjection: data as unknown as RiskProjection })
  },
  loadRiskHistogram: async (kommuneId) => {
    const data = await api.getRiskHistogram(kommuneId)
    set({ riskHistogram: data as unknown as RiskHistogram })
  },

  // Climate data
  climateHistory: null,
  regionalClimate: null,
  climateProjection: null,
  loadClimateHistory: async (kommuneId) => {
    const data = await api.getClimateHistory(kommuneId)
    set({ climateHistory: data as Record<string, unknown> })
  },
  loadRegionalClimate: async (kommuneId) => {
    const data = await api.getRegionalClimate(kommuneId)
    set({ regionalClimate: data as Record<string, unknown> })
  },
  loadClimateProjection: async (kommuneId) => {
    const data = await api.getClimateProjection(kommuneId)
    set({ climateProjection: data as Record<string, unknown> })
  },

  // Config
  configParams: [],
  loadConfig: async (kommuneId) => {
    const data = await api.getConfig(kommuneId)
    set({ configParams: data as unknown as ConfigParameter[] })
  },
  updateConfig: async (kommuneId, updates) => {
    await api.updateConfig(kommuneId, updates)
    await get().loadConfig(kommuneId)
  },

  // Measures
  measures: [],
  selectedMeasure: null,
  setSelectedMeasure: (m) => set({ selectedMeasure: m }),
  loadMeasures: async (kommuneId) => {
    const data = await api.listMeasures(kommuneId)
    set({ measures: data as unknown as Measure[] })
  },
  createMeasure: async (kommuneId, data) => {
    const m = await api.createMeasure(kommuneId, data) as unknown as Measure
    await get().loadMeasures(kommuneId)
    return m
  },
  updateMeasure: async (id, data) => {
    const m = await api.updateMeasure(id, data) as unknown as Measure
    const k = get().kommune
    if (k) await get().loadMeasures(k.id)
    return m
  },
  deleteMeasure: async (id) => {
    await api.deleteMeasure(id)
    const k = get().kommune
    if (k) await get().loadMeasures(k.id)
  },
  calculateImpact: async (measureId) => {
    const result = await api.calculateImpact(measureId) as unknown as MeasureImpactSummary
    return result
  },

  // Drawing
  isDrawing: false,
  setIsDrawing: (d) => set({ isDrawing: d }),
  drawnGeometry: null,
  setDrawnGeometry: (g) => set({ drawnGeometry: g }),

  // Reset
  resetKommune: async (kommuneId) => {
    await api.resetKommune(kommuneId)
    set({
      status: null,
      hasAssessment: false,
      gridGeoJson: null,
      activeLayer: null,
      layerGeoJson: null,
      riskSummary: null,
      costSummary: null,
      riskProjection: null,
      riskHistogram: null,
      measures: [],
      selectedMeasure: null,
      climateHistory: null,
      regionalClimate: null,
      climateProjection: null,
    })
  },
}))
