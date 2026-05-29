const BASE = '/api'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options,
  })
  if (!res.ok) {
    const body = await res.text()
    throw new Error(`API ${res.status}: ${body}`)
  }
  return res.json()
}

// ── Kommune ─────────────────────────────────────────────────────────────

export const api = {
  searchKommune: (q: string) =>
    request<Record<string, unknown>[]>(`/kommune/search?q=${encodeURIComponent(q)}`),

  createKommune: (osm_id: string, name: string, osm_type?: string, geojson?: Record<string, unknown>) =>
    request<Record<string, unknown>>('/kommune', {
      method: 'POST',
      body: JSON.stringify({ osm_id, name, osm_type: osm_type || 'relation', geojson: geojson || null }),
    }),

  getKommune: (id: number) =>
    request<Record<string, unknown>>(`/kommune/${id}`),

  listKommunen: () =>
    request<Record<string, unknown>[]>('/kommune'),

  // ── Grid ────────────────────────────────────────────────────────────

  generateGrid: (kommuneId: number, cellSizeM = 100) =>
    request<{ cells_created: number }>(`/kommune/${kommuneId}/grid`, {
      method: 'POST',
      body: JSON.stringify({ cell_size_m: cellSizeM }),
    }),

  getGrid: (kommuneId: number) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/grid`),

  // ── Assessment ──────────────────────────────────────────────────────

  getClimateTypes: () =>
    request<Record<string, unknown>[]>('/climate-types'),

  startAssessment: (kommuneId: number, climateType = 'heat', level = 1) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/assess`, {
      method: 'POST',
      body: JSON.stringify({ climate_type: climateType, level }),
    }),

  startBatchAssessment: (kommuneId: number, level = 4) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/assess/batch?level=${level}`, {
      method: 'POST',
    }),

  abortAssessment: (kommuneId: number, climateType = 'heat', level = 1) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/assess/abort`, {
      method: 'POST',
      body: JSON.stringify({ climate_type: climateType, level }),
    }),

  getStatus: (kommuneId: number) =>
    request<Record<string, unknown>[]>(`/kommune/${kommuneId}/status`),

  getAssessment: (kommuneId: number, climateType: string, level = 1) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/assessment/${climateType}?level=${level}`),

  // ── Config ──────────────────────────────────────────────────────────

  getConfig: (kommuneId: number) =>
    request<Record<string, unknown>[]>(`/kommune/${kommuneId}/config`),

  updateConfig: (kommuneId: number, updates: Record<string, unknown>[]) =>
    request<Record<string, unknown>[]>(`/kommune/${kommuneId}/config`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    }),

  // ── Measures ────────────────────────────────────────────────────────

  getMeasureCatalog: () =>
    request<Record<string, Record<string, unknown>>>('/measure-catalog'),

  createMeasure: (kommuneId: number, data: Record<string, unknown>) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/measures`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  listMeasures: (kommuneId: number) =>
    request<Record<string, unknown>[]>(`/kommune/${kommuneId}/measures`),

  getMeasure: (id: number) =>
    request<Record<string, unknown>>(`/measures/${id}`),

  updateMeasure: (id: number, data: Record<string, unknown>) =>
    request<Record<string, unknown>>(`/measures/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  deleteMeasure: (id: number) =>
    request<Record<string, unknown>>(`/measures/${id}`, { method: 'DELETE' }),

  calculateImpact: (measureId: number) =>
    request<Record<string, unknown>>(`/measures/${measureId}/calculate-impact`, {
      method: 'POST',
    }),

  getMeasureImpacts: (measureId: number) =>
    request<Record<string, unknown>[]>(`/measures/${measureId}/impacts`),

  // ── Export/Import ───────────────────────────────────────────────────

  exportMeasuresUrl: (kommuneId: number) =>
    `${BASE}/kommune/${kommuneId}/measures/export`,

  importMeasures: async (kommuneId: number, file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    const res = await fetch(`${BASE}/kommune/${kommuneId}/measures/import`, {
      method: 'POST',
      body: formData,
    })
    if (!res.ok) throw new Error(`Import failed: ${res.status}`)
    return res.json()
  },

  // ── Climate History ─────────────────────────────────────────────────

  getClimateHistory: (kommuneId: number) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/climate-history`),

  getRegionalClimate: (kommuneId: number) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/regional-climate`),

  getClimateProjection: (kommuneId: number) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/climate-projection`),

  // ── Risk Zones ──────────────────────────────────────────────────────

  getRiskZones: (kommuneId: number, climateType: string, level = 1) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/risk-zones/${climateType}?level=${level}`),

  getRiskSummary: (kommuneId: number) =>
    request<Record<string, unknown>[]>(`/kommune/${kommuneId}/risk-summary`),

  getRiskProjection: (kommuneId: number, climateType: string, level = 1) =>
    request<Record<string, unknown>[]>(`/kommune/${kommuneId}/risk-projection/${climateType}?level=${level}`),
  // ── Reset ────────────────────────────────────────────────────────────────────

  resetKommune: (kommuneId: number) =>
    request<{ message: string }>(`/kommune/${kommuneId}/reset`, { method: 'POST' }),}
