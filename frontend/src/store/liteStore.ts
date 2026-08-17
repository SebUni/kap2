import { create } from 'zustand'
import { api, type LiteMeta, type LiteGemeinde } from '../api/client'

/** Client-seitige Demo-Maßnahmen (Reduktionsfaktoren aus dem echten Katalog). */
export interface LiteMeasure {
  code: string
  name: string
  reduction: number
  scaling: 'linear' | 'saturating'
  linkedRisks: string[]
  unitLabel: string  // Slider-Beschriftung
}

export const LITE_MEASURES: LiteMeasure[] = [
  {
    code: 'DESEALING_SURFACE', name: 'Entsiegelung', reduction: 0.3, scaling: 'linear',
    linkedRisks: ['HYDROLOGICAL_STRESS_RISK_INDEX', 'EXPECTED_BUILDING_DAMAGE_EUR'],
    unitLabel: 'Umsetzungsgrad',
  },
  {
    code: 'URBAN_GREEN', name: 'Stadtgrün', reduction: 0.25, scaling: 'linear',
    linkedRisks: ['EXPECTED_THERMAL_STRESS_HOURS', 'EXPECTED_ANNUAL_MORTALITY'],
    unitLabel: 'Umsetzungsgrad',
  },
  {
    code: 'DRINKING_FOUNTAINS', name: 'Trinkbrunnen', reduction: 0.1, scaling: 'saturating',
    linkedRisks: ['EXPECTED_THERMAL_STRESS_HOURS', 'EXPECTED_ANNUAL_MORTALITY'],
    unitLabel: 'Ausbaugrad',
  },
]

/** g(s): linear = s, saturating = (1−e^−3s)/(1−e^−3). */
function coverage(s: number, scaling: LiteMeasure['scaling']): number {
  if (scaling === 'saturating') return (1 - Math.exp(-3 * s)) / (1 - Math.exp(-3))
  return s
}

/** adjusted = base × Π_{Maßnahmen mit Bezug zum Risiko} (1 − r·g(level)). */
export function adjustedIndex(
  baseIndex: number, riskCode: string, levels: Record<string, number>,
): number {
  let factor = 1
  for (const m of LITE_MEASURES) {
    if (!m.linkedRisks.includes(riskCode)) continue
    const s = levels[m.code] ?? 0
    if (s > 0) factor *= 1 - m.reduction * coverage(s, m.scaling)
  }
  return baseIndex * factor
}

interface LiteState {
  meta: LiteMeta | null
  values: Record<string, Record<string, number>> | null
  selectedRisk: string | null
  selectedAgs: string | null
  gemeindeDetail: LiteGemeinde | null
  detailLoading: boolean
  measureLevels: Record<string, number>  // code → 0..1
  error: string | null

  bootstrap: () => Promise<void>
  setRisk: (code: string) => void
  selectGemeinde: (ags: string) => Promise<void>
  setMeasureLevel: (code: string, level: number) => void
  resetMeasures: () => void
}

export const useLiteStore = create<LiteState>((set, get) => ({
  meta: null,
  values: null,
  selectedRisk: null,
  selectedAgs: null,
  gemeindeDetail: null,
  detailLoading: false,
  measureLevels: {},
  error: null,

  bootstrap: async () => {
    try {
      const [meta, values] = await Promise.all([api.lite.meta(), api.lite.values()])
      set({
        meta, values,
        selectedRisk: get().selectedRisk || meta.risks[0]?.code || null,
        error: null,
      })
    } catch (e) {
      set({ error: e instanceof Error ? e.message : String(e) })
    }
  },

  setRisk: (code) => set({ selectedRisk: code }),

  selectGemeinde: async (ags) => {
    set({ selectedAgs: ags, detailLoading: true })
    try {
      const detail = await api.lite.gemeinde(ags)
      set({ gemeindeDetail: detail, detailLoading: false })
    } catch (e) {
      set({ detailLoading: false, error: e instanceof Error ? e.message : String(e) })
    }
  },

  setMeasureLevel: (code, level) =>
    set((s) => ({ measureLevels: { ...s.measureLevels, [code]: level } })),
  resetMeasures: () => set({ measureLevels: {} }),
}))
