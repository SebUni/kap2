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

/** Wie ``request``, gibt aber die Textantwort (etwa Markdown) unverändert zurück. */
async function requestText(path: string, options?: RequestInit): Promise<string> {
  const res = await fetch(`${BASE}${path}`, options)
  if (!res.ok) {
    if (res.status === 401) handleUnauthorized(path)
    const body = await res.text()
    if (res.status === 500 && !body.trim()) {
      throw new Error('Backend nicht erreichbar (Port 8000). Bitte Backend starten: cd backend && python3 -m uvicorn app.main:app --reload')
    }
    throw new Error(`API ${res.status}: ${body || res.statusText}`)
  }
  return res.text()
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

/** Antwort von GET /catalog/querverbindungen (backend/app/services/querverbindungen.py). */
export type Netzrolle = 'stark ausgehend' | 'stark eingehend'

export interface QuerverbindungKlimawirkung {
  kwra_id: number
  /** Amtlicher Name aus dem Katalog (über die kwra_id), nicht die Schreibweise des Fließtexts. */
  name: string
  /** Erste Netzrolle (einwertig, Altfeld); mehrwertig steht in `netzrollen`. */
  netzrolle: Netzrolle | null
  /** Alle Netzrollen — eine Klimawirkung kann Sender und Empfänger zugleich sein (TB 6, Fn. 21, S. 84). */
  netzrollen: Netzrolle[]
  zentral: boolean
  /** Gedruckte Seiten in TB 6 Kap. 3.4, auf denen die Netzrolle belegt ist; leer ohne Netzrolle. */
  seiten: number[]
  netzrolle_auswertungen: ('gesamt' | 'hochrisiko')[]
  ausgehende_benannte: number
  eingehende_benannte: number
}

/** Netzknoten der Gesamtbetrachtung (TB 6 Kap. 3.4) außerhalb des Katalogs — ohne Index, Betrag oder Rang. */
export interface QuerverbindungNetzknotenAusserhalbKatalog {
  kwra_id: number
  name: string
  handlungsfeld: string
  netzrollen: Netzrolle[]
  zentral: boolean
  /** Gedruckte Seiten in TB 6 Kap. 3.4, auf denen die Netzrolle belegt ist. */
  seiten: number[]
  hinweis: string
}

/** Ein Handlungsfeld der Ablesung aus Abbildung 8 (TB 6, S. 83) — ausgewiesene Ablesung von KAP3, keine Tabelle der Quelle. */
export interface QuerverbindungHandlungsfeld {
  name: string
  ausgehend: number
  eingehend: number
  /** ausgehend + eingehend (Bogenlänge in Abbildung 8). */
  summe: number
}

/** Handlungsfeld-Ablesung aus Abbildung 8 (backend/app/data/kwra_handlungsfeld_querbezuege.py). */
export interface QuerverbindungHandlungsfelder {
  felder: QuerverbindungHandlungsfeld[]
  /** Wie abgelesen wurde und wie genau (Herleitung nach P1). */
  ablesung: string
  genauigkeit_summe: number
  genauigkeit_aufteilung: number
  quelle: string
}

/** Übernommene Aussage der Auswertung (TB 6 Kap. 3.4), wörtlich mit Fundstelle. */
export interface QuerverbindungAussage {
  titel: string
  wortlaut: string
  /** Gedruckte Seite der Hauptstelle (= PDF-Seite). */
  seite: number
  seiten: number[]
  beleg: string
}

/** Beteiligte Klimawirkung einer Rückkopplung; `im_katalog` setzt der Dienst über die kwra_id. */
export interface RueckkopplungKnoten {
  kwra_id: number
  name: string
  handlungsfeld: string
  im_katalog: boolean
}

/** Gerichtete Wirkbeziehung; eine gegenseitige Wirkung steht als zwei Kanten. */
export interface RueckkopplungKante {
  von_kwra_id: number
  nach_kwra_id: number
}

/** Gegenseitige Wechselwirkung oder Rückkopplungskreislauf (TB 6, S. 82, 85–86, Abb. 9;
 *  backend/app/data/kwra_rueckkopplungen.py). */
export interface Rueckkopplung {
  id: string
  art: 'wechselwirkung' | 'kreislauf'
  knoten: RueckkopplungKnoten[]
  kanten: RueckkopplungKante[]
  staerke: string | null
  seiten: number[]
  abbildung: string | null
  beleg: string
  quellen: string[]
}

export interface QuerverbindungsAuswertung {
  klimawirkungen: QuerverbindungKlimawirkung[]
  /** Die drei gegenseitigen Wechselwirkungen, darunter der einzige Rückkopplungskreislauf. */
  rueckkopplungen?: Rueckkopplung[]
  rueckkopplungen_quelle?: string
  netzknoten_ausserhalb_katalog: QuerverbindungNetzknotenAusserhalbKatalog[]
  kennzahlen: Record<string, string | number>
  systembereich_matrix: Record<string, Record<string, number>>
  /** Fundstelle der Matrix: Tabelle 28, TB 6, Kap. 7, S. 153. */
  systembereich_matrix_quelle?: {
    tabelle: number
    seite: number
    titel: string
    kapitel: number
    kapitel_titel: string
    bericht: string
  }
  handlungsfelder: QuerverbindungHandlungsfelder
  /** Schlüssel u. a. „annahme“ (S. 82), „einordnung_cluster“, „kaskadeneffekte“. */
  aussagen: Record<string, QuerverbindungAussage>
  abdeckung: {
    klimawirkungen_im_katalog: number
    klimawirkungen_kwra_gesamt: number
    mit_ausgewiesener_netzrolle: number
    mit_benannter_einzelbeziehung: number
    hinweis: string
  }
  quelle: string
  modellgrenze: string
}

/** Ein KWRA-Systembereich in der Antwort von GET /kommune/{id}/systembereiche. */
export interface Systembereich {
  systembereich: string
  anzahl_klimawirkungen: number
  risk_codes: string[]
  mittlerer_index: number | null
  schadenskosten_eur: number | null
  klimawirkungen_im_katalog: number
  /** Text „x von y Klimawirkungen in Euro beziffert“. */
  euro_beziffert: string
  /** Gesetzt, wenn der Bereich leer ist: Begründung, die in der Zeile steht (nie ausgeblendet). */
  leer_grund: string | null
}

export interface SystembereicheAuswertung {
  kommune_id: number
  bereiche: Systembereich[]
}

/** Ein Bereich des Bundesvergleichs (KWRA 2021, Teilbericht 6, Kap. 7); es wird nichts gerechnet. */
export interface BundesanalyseBereich {
  systembereich: string
  risiko: {
    anzahl_klimawirkungen: number
    risiko_ohne_anpassung: { vergleich: string; seiten: number[] }
    handlungserfordernisse: { sehr_dringend: number; dringend: number; seiten: number[] }
  }
  anpassung: {
    wirksamkeit: { valide_aussage: boolean; vergleich?: string | null; seiten: number[] }
    anpassungsdauer: { valide_aussage: boolean; vergleich?: string | null; seiten: number[] }
  }
}

export interface SystembereicheBundesanalyse {
  quelle: string
  bereiche: BundesanalyseBereich[]
  methodische_grenze: { titel: string; aussage: string }
}

/** Ein KAnG-Handlungsfeld in der Antwort von GET /kommune/{id}/kang-nachweis. */
export interface KangNachweisHandlungsfeld {
  cluster: string
  feld: string
  status: 'berücksichtigt' | 'offen' | 'nicht betroffen'
  risiken: string[]
  /** Jährliche Schadenssumme des Feldes in Euro. */
  schaden_eur: number
  massnahmen: string[]
}

/** Antwort von GET /kommune/{id}/kang-nachweis (§ 8 Abs. 1 KAnG, fachübergreifende Berücksichtigung). */
export interface KangNachweis {
  handlungsfelder: KangNachweisHandlungsfeld[]
  zusammenfassung: {
    betroffen_n: number
    beruecksichtigt_n: number
    offen_n: number
    offene_handlungsfelder: { cluster: string; feld: string }[]
    integrierende_massnahmen: string[]
  }
  /** Abgrenzungstext: keine Rechtskonformität bescheinigt; wörtlich anzuzeigen. */
  abgrenzung: string
  nicht_zugeordnet: {
    risiken: { code: string; schaden_eur: number | null }[]
    massnahmen: string[]
  }
}

/** Ein Handlungsfeld in der Antwort von GET /kommune/{id}/unsicherheits-zusammenschau. */
export interface UnsicherheitsZusammenschauFeld {
  handlungsfeld: string
  niedrigste_gewissheit: string
  parameter_nicht_belegt: number
  klimawirkungen_niedrigste_stufe: string[]
}

/** Antwort von GET /kommune/{id}/unsicherheits-zusammenschau (ISO 14091, UBA 2.2.6). */
export interface UnsicherheitsZusammenschau {
  kommune_id: number
  handlungsfelder: UnsicherheitsZusammenschauFeld[]
  handlungsfelder_vorsicht: string[]
  /** Interpretationshinweis; null, wenn kein Feld gering oder sehr gering ist. */
  hinweis: string | null
}

/** Antwort von GET /kommune/{id}/kang-zustaendigkeit (§ 12 Abs. 1 KAnG, Landesrecht). */
export interface KangZustaendigkeit {
  bundesland: string
  rechtsgrundlage: string
  fundstelle: string
  zustaendige_stelle: string
  pflicht: 'ja' | 'nein' | 'keine Bestimmung getroffen' | 'unbekannt'
  /** Datum JJJJ-MM-TT */
  stand: string
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
  cost_eur: number | null
  /** Verwechslungssperre Klasse A/B: false = Screening ohne Euro-Bezifferung. */
  has_euro_layer?: boolean
  /** Anzeigewert: Betrag (Klasse A) oder Screening-Vermerk (Klasse B). */
  cost_display?: number | string
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

// ── Interpretationsbelege (backend/app/api/routes/ergebnis_interpretation.py) ──
/** Eintrag von GET /kommune/{id}/interpretation/nachbarkommunen (nachbar_screening_aus). */
export interface NachbarIndex {
  ags: string
  name: string | null
  index: number | null
}
export interface NachbarScreeningEintrag {
  code: string
  name: string | null
  index_vorhanden: boolean
  eigener_index: number | null
  nachbarn: NachbarIndex[]
}

/** Nachweisarten (ergebnis_nachweise.NACHWEIS_ARTEN). */
export type NachweisArt = 'fachabteilung' | 'externe_expertise' | 'angrenzende_kommune' | 'land'

export interface NachweisEintrag {
  id: number
  stelle: string
  datum: string // ISO-Datum
  vermerk: string | null
}
/** Je Art ein Eintrag von GET /kommune/{id}/interpretation/nachweise; ``status`` ist ohne Einträge „nicht erfasst“. */
export interface NachweisJeArt {
  art: NachweisArt
  bezeichnung: string
  eintraege: NachweisEintrag[]
  status: string | null
}
export interface NachweisEingabe {
  art: NachweisArt
  stelle: string
  datum: string // ISO-Datum, nicht in der Zukunft
  vermerk?: string | null
}
export interface NachweisOut {
  id: number
  kommune_id: number
  art: NachweisArt
  stelle: string
  datum: string
  vermerk: string | null
}

/** Eintrag von GET /interpretation/massnahmen-gewissheit (massnahmen_gewissheit). */
export interface MassnahmeKlimawirkung {
  code: string
  name: string
  gewissheitsstufe: string
  qualitativ: boolean
}
export interface MassnahmeGewissheit {
  code: string
  name: string
  klimawirkungen: MassnahmeKlimawirkung[]
  wirkung_evidenz: string
}

/** Eintrag von GET /interpretation/massnahmen-umsetzung; Schlüssel der Antwort = Maßnahmencode. */
export interface MassnahmeUmsetzungBeleg {
  quelle?: string
  seite?: string
  abschaetzung?: string
  herleitung?: string
  ebenen_begruendung?: string
  weitere_quellen?: unknown
  fundstelle?: string
  [feld: string]: unknown
}
export interface MassnahmeUmsetzung {
  umsetzung: 'kommune_allein' | 'mit_partnern'
  partner: string[]
  ebenen: Array<'gemeinde' | 'kreis' | 'land'>
  beleg: MassnahmeUmsetzungBeleg
}
export type MassnahmenUmsetzung = Record<string, MassnahmeUmsetzung>

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
  /** KWRA-Querverbindungen je Klimawirkung (Netzrolle, benannte Beziehungen, Kennzahlen). */
  getQuerverbindungen: () => request<QuerverbindungsAuswertung>('/catalog/querverbindungen'),

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
  getKangZustaendigkeit: (kommuneId: number) =>
    request<KangZustaendigkeit>(`/kommune/${kommuneId}/kang-zustaendigkeit`),

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
  getSystembereiche: (kommuneId: number) =>
    request<SystembereicheAuswertung>(`/kommune/${kommuneId}/systembereiche`),
  getSystembereicheBundesanalyse: () =>
    request<SystembereicheBundesanalyse>('/catalog/systembereiche/bundesanalyse'),
  getKangNachweis: (kommuneId: number) =>
    request<KangNachweis>(`/kommune/${kommuneId}/kang-nachweis`),
  getUnsicherheitsZusammenschau: (kommuneId: number) =>
    request<UnsicherheitsZusammenschau>(`/kommune/${kommuneId}/unsicherheits-zusammenschau`),
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

  // ── Interpretationsbelege ───────────────────────────────────────────
  getInterpretationNachbarkommunen: (kommuneId: number) =>
    request<NachbarScreeningEintrag[]>(`/kommune/${kommuneId}/interpretation/nachbarkommunen`),
  getInterpretationNachweise: (kommuneId: number) =>
    request<NachweisJeArt[]>(`/kommune/${kommuneId}/interpretation/nachweise`),
  createInterpretationNachweis: (kommuneId: number, eingabe: NachweisEingabe) =>
    request<NachweisOut>(`/kommune/${kommuneId}/interpretation/nachweise`, {
      method: 'POST', body: JSON.stringify(eingabe),
    }),
  deleteInterpretationNachweis: (kommuneId: number, nachweisId: number) =>
    request<boolean>(`/kommune/${kommuneId}/interpretation/nachweise/${nachweisId}`, { method: 'DELETE' }),
  getMassnahmenGewissheit: () =>
    request<MassnahmeGewissheit[]>('/interpretation/massnahmen-gewissheit'),
  getMassnahmenUmsetzung: () =>
    request<MassnahmenUmsetzung>('/interpretation/massnahmen-umsetzung'),
  getInterpretationsbericht: (kommuneId: number): Promise<string> =>
    requestText(`/kommune/${kommuneId}/interpretation/bericht`),
}
