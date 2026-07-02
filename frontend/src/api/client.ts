const BASE = '/api'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options,
  })
  if (!res.ok) {
    const body = await res.text()
    if (res.status === 500 && !body.trim()) {
      throw new Error('Backend nicht erreichbar (Port 8000). Bitte Backend starten: cd backend && python3 -m uvicorn app.main:app --reload')
    }
    throw new Error(`API ${res.status}: ${body || res.statusText}`)
  }
  return res.json()
}

export const api = {
  // ── Kommune ─────────────────────────────────────────────────────────
  searchKommune: (q: string) =>
    request<Record<string, unknown>[]>(`/kommune/search?q=${encodeURIComponent(q)}`),

  createKommune: (osm_id: string, name: string, osm_type?: string, geojson?: Record<string, unknown>) =>
    request<Record<string, unknown>>('/kommune', {
      method: 'POST',
      body: JSON.stringify({ osm_id, name, osm_type: osm_type || 'relation', geojson: geojson || null }),
    }),

  getKommune: (id: number) => request<Record<string, unknown>>(`/kommune/${id}`),
  listKommunen: (calculated = false) =>
    request<Record<string, unknown>[]>(`/kommune${calculated ? '?calculated=true' : ''}`),

  // ── Grid ────────────────────────────────────────────────────────────
  generateGrid: (kommuneId: number, cellSizeM = 100, force = false) =>
    request<{ cells_created: number }>(`/kommune/${kommuneId}/grid`, {
      method: 'POST', body: JSON.stringify({ cell_size_m: cellSizeM, force }),
    }),
  getGrid: (kommuneId: number) => request<Record<string, unknown>>(`/kommune/${kommuneId}/grid`),

  // ── Katalog ─────────────────────────────────────────────────────────
  getCatalog: () => request<Record<string, unknown>>('/catalog'),
  getLayerRecipe: (code: string, category?: string) =>
    request<Record<string, unknown>>(
      `/catalog/layer/${code}/recipe${category ? `?category=${category}` : ''}`,
    ),

  // ── Parameter ───────────────────────────────────────────────────────
  getParameters: (kommuneId: number, layer?: string, category?: string) => {
    const q = new URLSearchParams()
    if (layer) q.set('layer', layer)
    if (category) q.set('category', category)
    const qs = q.toString()
    return request<Record<string, unknown>[]>(
      `/kommune/${kommuneId}/parameters${qs ? `?${qs}` : ''}`,
    )
  },
  updateParameters: (kommuneId: number, updates: { parameter_id: string; value: unknown; custom_source?: string }[]) =>
    request<Record<string, unknown>[]>(`/kommune/${kommuneId}/parameters`, {
      method: 'PUT', body: JSON.stringify(updates),
    }),
  exportParametersUrl: (kommuneId: number) => `${BASE}/kommune/${kommuneId}/parameters/export`,

  // ── Assessment ──────────────────────────────────────────────────────
  startAssessment: (kommuneId: number) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/assess`, { method: 'POST' }),
  abortAssessment: (kommuneId: number) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/assess/abort`, { method: 'POST' }),
  getStatus: (kommuneId: number) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/status`),

  getLayer: (kommuneId: number, code: string) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/layer/${code}`),
  getRiskSummary: (kommuneId: number) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/risk-summary`),
  getRiskZones: (kommuneId: number, riskCode: string) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/risk-zones/${riskCode}`),
  getRiskHistogram: (kommuneId: number) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/risk-histogram`),
  getRiskProjection: (kommuneId: number) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/risk-projection`),

  // ── Config ──────────────────────────────────────────────────────────
  getConfig: (kommuneId: number) =>
    request<Record<string, unknown>[]>(`/kommune/${kommuneId}/config`),
  updateConfig: (kommuneId: number, updates: Record<string, unknown>[]) =>
    request<Record<string, unknown>[]>(`/kommune/${kommuneId}/config`, {
      method: 'PUT', body: JSON.stringify(updates),
    }),

  // ── Measures ────────────────────────────────────────────────────────
  getMeasureCatalog: () => request<Record<string, unknown>[]>('/measure-catalog'),
  createMeasure: (kommuneId: number, data: Record<string, unknown>) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/measures`, {
      method: 'POST', body: JSON.stringify(data),
    }),
  listMeasures: (kommuneId: number) =>
    request<Record<string, unknown>[]>(`/kommune/${kommuneId}/measures`),
  getMeasure: (id: number) => request<Record<string, unknown>>(`/measures/${id}`),
  updateMeasure: (id: number, data: Record<string, unknown>) =>
    request<Record<string, unknown>>(`/measures/${id}`, {
      method: 'PUT', body: JSON.stringify(data),
    }),
  deleteMeasure: (id: number) =>
    request<Record<string, unknown>>(`/measures/${id}`, { method: 'DELETE' }),
  calculateImpact: (measureId: number) =>
    request<Record<string, unknown>>(`/measures/${measureId}/calculate-impact`, { method: 'POST' }),
  getCostSummary: (kommuneId: number) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/cost-summary`),

  // ── Export/Import ───────────────────────────────────────────────────
  listExports: (kommuneId: number) =>
    request<Record<string, unknown>[]>(`/kommune/${kommuneId}/exports`),
  startGeodataExport: (kommuneId: number) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/exports/geodaten`, { method: 'POST' }),
  exportDownloadUrl: (kommuneId: number, exportId: number) =>
    `${BASE}/kommune/${kommuneId}/exports/${exportId}/download`,
  exportMeasuresUrl: (kommuneId: number) => `${BASE}/kommune/${kommuneId}/measures/export`,
  importMeasures: async (kommuneId: number, file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    const res = await fetch(`${BASE}/kommune/${kommuneId}/measures/import`, { method: 'POST', body: formData })
    if (!res.ok) throw new Error(`Import failed: ${res.status}`)
    return res.json()
  },

  // ── Klimadaten ──────────────────────────────────────────────────────
  getClimateHistory: (kommuneId: number) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/climate-history`),
  getRegionalClimate: (kommuneId: number) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/regional-climate`),
  getClimateProjection: (kommuneId: number) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/climate-projection`),

  // ── Reset ───────────────────────────────────────────────────────────
  resetKommune: (kommuneId: number) =>
    request<{ message: string }>(`/kommune/${kommuneId}/reset`, { method: 'POST' }),
}
