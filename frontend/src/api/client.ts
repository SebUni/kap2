const BASE = '/api'

/** Wird vom authStore registriert: 401 auf geschützten Pfaden → Login-Redirect. */
let onUnauthorized: (() => void) | null = null
export function setUnauthorizedHandler(handler: (() => void) | null) {
  onUnauthorized = handler
}

function handleUnauthorized(path: string) {
  // Auth- und öffentliche Endpunkte lösen keinen Redirect aus.
  if (!path.startsWith('/auth/') && !path.startsWith('/public/')) {
    onUnauthorized?.()
  }
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options,
  })
  if (!res.ok) {
    if (res.status === 401) handleUnauthorized(path)
    const body = await res.text()
    if (res.status === 500 && !body.trim()) {
      throw new Error('Backend nicht erreichbar (Port 8000). Bitte Backend starten: cd backend && python3 -m uvicorn app.main:app --reload')
    }
    throw new Error(`API ${res.status}: ${body || res.statusText}`)
  }
  return res.json()
}

export type ProgressCallback = (fraction: number) => void

/**
 * Lädt eine (gzip-)JSON-Antwort und meldet echten Byte-Fortschritt.
 * Der Browser dekomprimiert gzip transparent; als Gesamtgröße dient der
 * ``X-Uncompressed-Length``-Header (Fallback: ``Content-Length``).
 */
async function requestWithProgress<T>(path: string, onProgress?: ProgressCallback): Promise<T> {
  const res = await fetch(`${BASE}${path}`)
  if (!res.ok) {
    if (res.status === 401) handleUnauthorized(path)
    const body = await res.text()
    throw new Error(`API ${res.status}: ${body || res.statusText}`)
  }
  const totalStr = res.headers.get('X-Uncompressed-Length') || res.headers.get('Content-Length')
  const total = totalStr ? parseInt(totalStr, 10) : 0

  if (!res.body || typeof res.body.getReader !== 'function') {
    onProgress?.(1)
    return res.json() as Promise<T>
  }

  const reader = res.body.getReader()
  const chunks: Uint8Array[] = []
  let received = 0
  for (;;) {
    const { done, value } = await reader.read()
    if (done) break
    if (value) {
      chunks.push(value)
      received += value.length
      if (onProgress && total > 0) onProgress(Math.min(1, received / total))
    }
  }

  let bytes: Uint8Array
  if (chunks.length === 1) {
    bytes = chunks[0]
  } else {
    bytes = new Uint8Array(received)
    let offset = 0
    for (const c of chunks) { bytes.set(c, offset); offset += c.length }
  }
  onProgress?.(1)
  return JSON.parse(new TextDecoder().decode(bytes)) as T
}

export interface AuthUser {
  id: number
  email: string
  display_name: string | null
  role: 'admin' | 'user'
}

export interface DemoMeta {
  kommune_id: number
  risks: { code: string; name: string; group: string | null; unit: string }[]
  enabled_layers: string[]
  measure_limit: number
}

export interface LiteRiskMeta {
  code: string
  name: string
  group: string | null
  unit: string
  description: string
  source_refs: { key: string; ieee: string; url?: string; archive_url?: string }[]
}

export interface LiteMeta {
  risks: LiteRiskMeta[]
  gemeinde_count: number
  vg250_stand: string | null
  choropleth_colors: string[]
}

export interface AdminUser {
  id: number
  email: string
  display_name: string | null
  role: 'admin' | 'user'
  is_active: boolean
  kommunen: { id: number; name: string }[]
  last_login_at: string | null
}

export interface LiteBatchRun {
  id: number
  status: string
  phase: string | null
  progress_pct: number
  processed: number
  total: number
  message: string | null
  error_count: number
  params: { bundesland?: string | null; force_zensus?: boolean } | null
  started_at: string | null
  finished_at: string | null
}

export interface DemoConfig {
  kommune_id: number | null
  risk_codes: string[]
  measure_limit: number
  session_ttl_h: number
  kommune: { id: number; name: string } | null
  active_sessions: number
  risk_options: { code: string; name: string; group: string | null }[]
}

export interface LiteGemeindeRisk {
  code: string
  name: string
  group: string | null
  index: number
  outcome: number
  unit: string
  cost_eur: number
  drivers: Record<string, unknown>
  sources: { key: string; ieee: string; url?: string; archive_url?: string }[]
}

export interface LiteGemeinde {
  ags: string
  name: string
  bez: string | null
  bundesland: string | null
  population: number | null
  area_km2: number | null
  risks: LiteGemeindeRisk[]
}

// ── KI-Assistent (Mistral) ────────────────────────────────────────────
export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export interface AiSettings {
  api_key_set: boolean
  api_key_hint: string | null
  model: string
  monthly_token_limit: number
  daily_token_limit: number
}

export interface AiUsageScope { used: number; limit: number }
export interface AiUsage {
  day: AiUsageScope
  month: AiUsageScope
  blocked: boolean
}

/** Strukturierter Fehler des /ai/chat-Endpunkts (vor Stream-Start). */
export class ChatError extends Error {
  code: 'no_api_key' | 'quota_exceeded' | 'forbidden' | 'unknown'
  scope?: 'day' | 'month'
  constructor(code: ChatError['code'], message: string, scope?: 'day' | 'month') {
    super(message)
    this.code = code
    this.scope = scope
  }
}

/**
 * Streamt eine Chat-Antwort (SSE). Ruft ``onToken`` je Text-Fragment und
 * ``onUsage`` mit dem finalen Verbrauch. Wirft ChatError bei 400/429/403.
 * Abbruch via ``signal`` (AbortController).
 */
export async function chatStream(
  payload: { messages: ChatMessage[]; kommune_id?: number | null },
  handlers: {
    onToken: (text: string) => void
    onUsage?: (usage: { day: AiUsageScope; month: AiUsageScope }) => void
    onError?: (message: string) => void
  },
  signal?: AbortSignal,
): Promise<void> {
  const res = await fetch(`${BASE}/ai/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
    signal,
  })
  if (!res.ok) {
    if (res.status === 401) { handleUnauthorized('/ai/chat'); throw new ChatError('unknown', 'Nicht angemeldet.') }
    let body: Record<string, unknown> = {}
    try { body = await res.json() } catch { /* leer */ }
    const code = body.code as string | undefined
    if (code === 'no_api_key')
      throw new ChatError('no_api_key', 'Es ist kein KI-Schlüssel hinterlegt. Bitte an eine Administratorin/einen Administrator wenden.')
    if (code === 'quota_exceeded')
      throw new ChatError('quota_exceeded', 'Das Token-Kontingent ist erschöpft.', body.scope as 'day' | 'month')
    if (res.status === 403)
      throw new ChatError('forbidden', 'Kein Zugriff auf diese Kommune.')
    throw new ChatError('unknown', `Fehler ${res.status}`)
  }
  if (!res.body) return

  const reader = res.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''
  for (;;) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    let idx: number
    while ((idx = buffer.indexOf('\n\n')) !== -1) {
      const frame = buffer.slice(0, idx).trim()
      buffer = buffer.slice(idx + 2)
      if (!frame.startsWith('data:')) continue
      let evt: Record<string, unknown>
      try { evt = JSON.parse(frame.slice(5).trim()) } catch { continue }
      if (evt.type === 'token') handlers.onToken(String(evt.content ?? ''))
      else if (evt.type === 'usage') handlers.onUsage?.({ day: evt.day as AiUsageScope, month: evt.month as AiUsageScope })
      else if (evt.type === 'error') handlers.onError?.(String(evt.message ?? 'Unbekannter Fehler'))
    }
  }
}

export const api = {
  // ── Auth ────────────────────────────────────────────────────────────
  auth: {
    login: (email: string, password: string) =>
      request<AuthUser>('/auth/login', {
        method: 'POST', body: JSON.stringify({ email, password }),
      }),
    logout: () => request<{ message: string }>('/auth/logout', { method: 'POST' }),
    me: () => request<{ authenticated: boolean; user?: AuthUser }>('/auth/me'),
    changePassword: (currentPassword: string, newPassword: string) =>
      request<{ message: string }>('/auth/change-password', {
        method: 'POST',
        body: JSON.stringify({ current_password: currentPassword, new_password: newPassword }),
      }),
  },

  // ── Demo ────────────────────────────────────────────────────────────
  demo: {
    meta: () => request<DemoMeta>('/demo/meta'),
    startSession: () => request<DemoMeta & { session_id: string }>('/demo/session', { method: 'POST' }),
  },

  // ── Deutschland-Karte (öffentlich) ──────────────────────────────────
  lite: {
    meta: () => request<LiteMeta>('/public/lite/meta'),
    values: () => request<Record<string, Record<string, number>>>('/public/lite/values'),
    gemeinde: (ags: string) => request<LiteGemeinde>(`/public/lite/gemeinde/${ags}`),
    geojsonIndex: () => request<Record<string, { slug: string; count: number }>>('/public/lite/geojson-index'),
    geojsonUrl: (slug: string) => `${BASE}/public/lite/geojson/${slug}`,
  },

  // ── Admin ───────────────────────────────────────────────────────────
  admin: {
    listUsers: () => request<AdminUser[]>('/admin/users'),
    createUser: (data: Record<string, unknown>) =>
      request<AdminUser & { initial_password?: string }>('/admin/users', {
        method: 'POST', body: JSON.stringify(data),
      }),
    updateUser: (id: number, data: Record<string, unknown>) =>
      request<AdminUser>(`/admin/users/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),
    listLiteBatches: () => request<LiteBatchRun[]>('/admin/lite-batch'),
    startLiteBatch: (data: { bundesland?: string | null; force_zensus?: boolean }) =>
      request<LiteBatchRun>('/admin/lite-batch', { method: 'POST', body: JSON.stringify(data) }),
    abortLiteBatch: (id: number) =>
      request<{ aborted: boolean }>(`/admin/lite-batch/${id}/abort`, { method: 'POST' }),
    getDemoConfig: () => request<DemoConfig>('/admin/demo/config'),
    updateDemoConfig: (data: Record<string, unknown>) =>
      request<Record<string, unknown>>('/admin/demo/config', { method: 'PUT', body: JSON.stringify(data) }),
    cleanupDemo: () => request<{ removed: number }>('/admin/demo/cleanup', { method: 'POST' }),
  },

  // ── Kommune ─────────────────────────────────────────────────────────
  searchKommune: (q: string) =>
    request<Record<string, unknown>[]>(`/kommune/search?q=${encodeURIComponent(q)}`),

  createKommune: (osm_id: string, name: string, osm_type?: string, geojson?: Record<string, unknown>, address?: Record<string, string>) =>
    request<Record<string, unknown>>('/kommune', {
      method: 'POST',
      body: JSON.stringify({ osm_id, name, osm_type: osm_type || 'relation', geojson: geojson || null, address: address || null }),
    }),

  getKommune: (id: number) => request<Record<string, unknown>>(`/kommune/${id}`),
  listKommunen: (calculated = false) =>
    request<Record<string, unknown>[]>(`/kommune${calculated ? '?calculated=true' : ''}`),

  // ── Grid ────────────────────────────────────────────────────────────
  generateGrid: (kommuneId: number, cellSizeM = 100, force = false) =>
    request<{ cells_created: number }>(`/kommune/${kommuneId}/grid`, {
      method: 'POST', body: JSON.stringify({ cell_size_m: cellSizeM, force }),
    }),

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
    request<{ results: Record<string, unknown>[]; recalculation_required: boolean }>(
      `/kommune/${kommuneId}/parameters`, {
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

  getGridGeometry: (kommuneId: number, onProgress?: ProgressCallback) =>
    requestWithProgress<Record<string, unknown>>(`/kommune/${kommuneId}/grid-geometry`, onProgress),
  getLayerValues: (kommuneId: number, code: string, onProgress?: ProgressCallback) =>
    requestWithProgress<Record<string, unknown>>(`/kommune/${kommuneId}/layer/${code}/values`, onProgress),
  getRiskSummary: (kommuneId: number) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/risk-summary`),
  getRiskZones: (kommuneId: number, riskCode: string) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/risk-zones/${riskCode}`),
  getRiskHistogram: (kommuneId: number) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/risk-histogram`),
  getRiskProjection: (kommuneId: number) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/risk-projection`),
  getCostProjection: (kommuneId: number) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/cost-projection`),
  getKommuneProfile: (kommuneId: number) =>
    request<Record<string, unknown>>(`/kommune/${kommuneId}/profile`),

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

  // ── KI-Assistent ────────────────────────────────────────────────────
  getAiSettings: () => request<AiSettings>('/ai/settings'),           // admin-only
  updateAiSettings: (payload: Partial<{ api_key: string; model: string; monthly_token_limit: number; daily_token_limit: number }>) =>
    request<AiSettings>('/ai/settings', { method: 'PUT', body: JSON.stringify(payload) }),  // admin-only
  getAiUsage: () => request<AiUsage>('/ai/usage'),
  chatStream,
}
