import { create } from 'zustand'
import { api } from '../api/client'
import type {
  Kommune, AssessmentStatus, ConfigParameter, Measure,
  GeoJSONFeatureCollection, MeasureImpactSummary,
  RiskSummary, RiskProjectionYear,
} from '../types'
import { CLIMATE_TYPE_META } from '../types'

// ── App Store ─────────────────────────────────────────────────────────────────

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
  generateGrid: (kommuneId: number, cellSize?: number) => Promise<void>

  // Assessment
  // Assessment
  assessmentLevel: number
  setAssessmentLevel: (level: number) => void
  assessmentGeoJson: GeoJSONFeatureCollection | null
  statuses: AssessmentStatus[]
  climateHistory: Record<string, unknown> | null
  regionalClimate: Record<string, unknown> | null
  climateProjection: Record<string, unknown> | null
  loadAssessment: (kommuneId: number, climateType?: string, level?: number) => Promise<void>
  loadStatuses: (kommuneId: number) => Promise<void>
  startAssessment: (kommuneId: number, level?: number) => Promise<void>
  abortAssessment: (kommuneId: number, level?: number) => Promise<void>
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
  selectedImpact: MeasureImpactSummary | null
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

  // Multi-risk
  activeClimateType: string
  setActiveClimateType: (ct: string) => void
  riskSummary: RiskSummary[]
  riskZonesGeoJson: GeoJSONFeatureCollection | null
  riskProjections: Record<string, RiskProjectionYear[]>
  loadRiskSummary: (kommuneId: number) => Promise<void>
  loadRiskZones: (kommuneId: number, climateType: string, level?: number) => Promise<void>
  loadRiskProjection: (kommuneId: number, climateType: string, level?: number) => Promise<void>

  // Batch assessment
  startAllAssessments: (kommuneId: number, level?: number) => Promise<void>
  allRunning: boolean

  // Per-type assessments
  assessmentsByType: Record<string, GeoJSONFeatureCollection>
  loadAssessmentForType: (kommuneId: number, climateType: string, level?: number) => Promise<void>
  loadAllAssessments: (kommuneId: number) => Promise<void>

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
    const data = await api.getKommune(id)
    set({ kommune: data as unknown as Kommune })
  },

  // Grid
  gridGeoJson: null,
  loadGrid: async (kommuneId) => {
    const data = await api.getGrid(kommuneId)
    set({ gridGeoJson: data as unknown as GeoJSONFeatureCollection })
  },
  generateGrid: async (kommuneId, cellSize = 100) => {
    await api.generateGrid(kommuneId, cellSize)
    await get().loadGrid(kommuneId)
  },

  // Assessment
  assessmentLevel: 4,
  setAssessmentLevel: (level) => set({ assessmentLevel: level }),
  assessmentGeoJson: null,
  statuses: [],
  climateHistory: null,
  regionalClimate: null,
  climateProjection: null,
  loadAssessment: async (kommuneId, climateType, level?) => {
    const ct = climateType ?? get().activeClimateType
    const lvl = level ?? get().assessmentLevel
    const data = await api.getAssessment(kommuneId, ct, lvl)
    set({ assessmentGeoJson: data as unknown as GeoJSONFeatureCollection })
  },
  loadStatuses: async (kommuneId) => {
    const data = await api.getStatus(kommuneId)
    set({ statuses: data as unknown as AssessmentStatus[] })
  },
  startAssessment: async (kommuneId, level?) => {
    const lvl = level ?? get().assessmentLevel
    const ct = get().activeClimateType
    await api.startAssessment(kommuneId, ct, lvl)
  },
  abortAssessment: async (kommuneId, level?) => {
    const lvl = level ?? get().assessmentLevel
    const ct = get().activeClimateType
    await api.abortAssessment(kommuneId, ct, lvl)
  },
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
  selectedImpact: null,
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
    set({ selectedImpact: result })
    return result
  },

  // Drawing
  isDrawing: false,
  setIsDrawing: (d) => set({ isDrawing: d }),
  drawnGeometry: null,
  setDrawnGeometry: (g) => set({ drawnGeometry: g }),

  // Multi-risk
  activeClimateType: 'heat',
  setActiveClimateType: (ct) => set({ activeClimateType: ct }),
  riskSummary: [],
  riskZonesGeoJson: null,
  riskProjections: {},
  loadRiskSummary: async (kommuneId) => {
    const data = await api.getRiskSummary(kommuneId)
    set({ riskSummary: data as unknown as RiskSummary[] })
  },
  loadRiskZones: async (kommuneId, climateType, level?) => {
    const lvl = level ?? get().assessmentLevel
    const data = await api.getRiskZones(kommuneId, climateType, lvl)
    set({ riskZonesGeoJson: data as unknown as GeoJSONFeatureCollection })
  },
  loadRiskProjection: async (kommuneId, climateType, level?) => {
    const lvl = level ?? get().assessmentLevel
    const data = await api.getRiskProjection(kommuneId, climateType, lvl) as unknown as RiskProjectionYear[]
    set((s) => ({
      riskProjections: { ...s.riskProjections, [climateType]: data },
    }))
  },

  // Batch assessment
  allRunning: false,
  startAllAssessments: async (kommuneId, level?) => {
    const lvl = level ?? get().assessmentLevel
    set({ allRunning: true })
    try {
      // Single backend call that pre-fetches OSM once and runs all types sequentially
      await api.startBatchAssessment(kommuneId, lvl)
    } catch {
      // Fallback: start individually (shouldn't normally happen)
      const types = Object.keys(CLIMATE_TYPE_META)
      for (const ct of types) {
        try {
          await api.startAssessment(kommuneId, ct, lvl)
        } catch { /* skip */ }
      }
    }
  },

  // Per-type assessments
  assessmentsByType: {},
  loadAssessmentForType: async (kommuneId, climateType, level?) => {
    const lvl = level ?? get().assessmentLevel
    try {
      const data = await api.getAssessment(kommuneId, climateType, lvl)
      set((s) => ({
        assessmentsByType: { ...s.assessmentsByType, [climateType]: data as unknown as GeoJSONFeatureCollection },
      }))
    } catch { /* no data */ }
  },
  loadAllAssessments: async (kommuneId) => {
    // Always fetch fresh statuses first so the map layer controls work
    // immediately when navigating to the map tab.
    let currentStatuses = get().statuses
    try {
      const fresh = await api.getStatus(kommuneId)
      currentStatuses = fresh as unknown as AssessmentStatus[]
      set({ statuses: currentStatuses })
    } catch { /* use cached */ }

    const lvl = get().assessmentLevel
    const doneTypes = [...new Set(currentStatuses.filter(s => s.status === 'done').map(s => s.climate_type))]
    const results: Record<string, GeoJSONFeatureCollection> = {}
    await Promise.all(doneTypes.map(async ct => {
      try {
        const data = await api.getAssessment(kommuneId, ct, lvl)
        results[ct] = data as unknown as GeoJSONFeatureCollection
      } catch { /* skip */ }
    }))
    set({ assessmentsByType: results })
  },

  resetKommune: async (kommuneId) => {
    await api.resetKommune(kommuneId)
    set({
      statuses: [],
      assessmentGeoJson: null,
      gridGeoJson: null,
      assessmentsByType: {},
      riskSummary: [],
      riskZonesGeoJson: null,
      riskProjections: {},
      measures: [],
      selectedMeasure: null,
      selectedImpact: null,
      climateHistory: null,
      regionalClimate: null,
      climateProjection: null,
    })
  },
}))
