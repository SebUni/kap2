/**
 * Erzeugt den statischen Cache der Landing-Karte aus dem echten Backend
 * (Demo-Kommune Oschatz, id 2), geclippt auf die Landing-Bounding-Box.
 *
 * Lädt Geometrie + je Risiko die Zell-Werte (index/H/E/V/pathways/outcome/value)
 * inkl. Recipe sowie einen Versiegelungs-Proxy (1 − Grünanteil) fürs
 * Maßnahmen-Spiel und schreibt sie gebündelt nach
 * src/pages/landing/data/oschatz-landing.json.
 *
 * Voraussetzung: Backend läuft auf http://localhost:8000 und die Demo ist
 * konfiguriert. Neu erzeugen mit:  node scripts/build-landing-snapshot.mjs
 */
import { writeFileSync, mkdirSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const BASE = process.env.KAP2_API || 'http://localhost:8000'
const KOMMUNE = 2
// Bounding-Box (Landing-Ausschnitt Oschatz): NW → SE.
const BOX = { minLng: 13.10473477561351, maxLng: 13.124507818593578, minLat: 51.28908422229264, maxLat: 51.30008803497496 }

const RISKS = [
  { key: 'hitzemortalitaet', code: 'EXPECTED_ANNUAL_MORTALITY' },
  { key: 'gebaeudeschaden', code: 'EXPECTED_BUILDING_DAMAGE_EUR' },
  { key: 'landw_schaden', code: 'EXPECTED_AGRICULTURAL_DAMAGE_EUR' },
]

const round = (v, p = 6) => (v == null ? v : Math.round(v * 10 ** p) / 10 ** p)

async function main() {
  // Demo-Session (Cookie) besorgen.
  const sess = await fetch(`${BASE}/api/demo/session`, { method: 'POST' })
  const cookie = (sess.headers.get('set-cookie') || '').split(';')[0]
  if (!cookie) throw new Error('Keine Demo-Session-Cookie erhalten')
  const get = async (path) => {
    const r = await fetch(`${BASE}${path}`, { headers: { cookie } })
    if (!r.ok) throw new Error(`${path} → ${r.status}`)
    return r.json()
  }

  // Geometrie clippen.
  const geo = await get(`/api/kommune/${KOMMUNE}/grid-geometry`)
  const inBox = ([lng, lat]) => lng >= BOX.minLng && lng <= BOX.maxLng && lat >= BOX.minLat && lat <= BOX.maxLat
  const centroid = (ring) => {
    const pts = ring.slice(0, -1)
    const n = pts.length
    return [pts.reduce((s, p) => s + p[0], 0) / n, pts.reduce((s, p) => s + p[1], 0) / n]
  }
  const cells = []
  const ids = new Set()
  for (const f of geo.features) {
    const ring = f.geometry.coordinates[0]
    const c = centroid(ring)
    if (!inBox(c)) continue
    const id = f.properties.grid_cell_id
    ids.add(id)
    cells.push({ id, polygon: ring.map(([x, y]) => [round(x), round(y)]), center: [round(c[0]), round(c[1])] })
  }

  // Risiken laden + clippen.
  const risks = {}
  for (const { key, code } of RISKS) {
    const v = await get(`/api/kommune/${KOMMUNE}/layer/${code}/values`)
    // Zahlen runden und die per-Zelle-Wirkungsketten auf die vom Tooltip
    // genutzten Felder eindampfen (Codes/Namen/Gewichte stehen im Recipe).
    const pair = (p) => [round(p[0], 3), round(p[1], 2)]
    const cellsById = {}
    for (const c of v.cells) {
      if (!ids.has(c.grid_cell_id)) continue
      const o = c.outcome || {}
      cellsById[c.grid_cell_id] = {
        index: round(c.index, 2),
        H: (c.H || []).map(pair), E: (c.E || []).map(pair), V: (c.V || []).map(pair),
        outcome: {
          ref_value: round(o.ref_value, 3), scale_factor: round(o.scale_factor, 6),
          index_fraction: round(o.index_fraction, 4), cell_pop: round(o.cell_pop, 1),
          cell_area_km2: round(o.cell_area_km2, 4), outcome: round(o.outcome, 4),
        },
        pathways: {
          max_term: round(c.pathways?.max_term, 4), index: round(c.pathways?.index, 2),
          pathways: (c.pathways?.pathways || []).map((p) => ({
            h_norm: round(p.h_norm, 2), e_norm: round(p.e_norm, 2), v_norm: round(p.v_norm, 2),
            term: round(p.term, 4), is_max: !!p.is_max,
          })),
        },
        value: round(c.value, 4),
      }
    }
    risks[key] = {
      code, label: v.meta.label, unit: v.meta.unit, min: v.meta.min, max: v.meta.max,
      recipe: v.meta.recipe, cells: cellsById,
    }
  }

  const out = {
    generated: new Date().toISOString(),
    kommune: KOMMUNE,
    bounds: [[BOX.minLng, BOX.minLat], [BOX.maxLng, BOX.maxLat]],
    cells,
    risks,
    // Maßnahmen-Spiel färbt/rechnet auf Gebäudeschäden; der Grünanteil-Proxy
    // (GREEN_SPACE_SHARE) ist in der Demo nicht mehr freigeschaltet und wurde
    // ohnehin nicht genutzt (landingData nutzt eine kalibrierte Konstante).
    measure: { damageKey: 'gebaeudeschaden' },
  }

  const dir = resolve(dirname(fileURLToPath(import.meta.url)), '../src/pages/landing/data')
  mkdirSync(dir, { recursive: true })
  const file = resolve(dir, 'oschatz-landing.json')
  writeFileSync(file, JSON.stringify(out))
  const kb = (JSON.stringify(out).length / 1024).toFixed(0)
  console.log(`OK: ${cells.length} Zellen, ${Object.keys(risks).length} Risiken → ${file} (${kb} KB)`)
}

main().catch((e) => { console.error(e); process.exit(1) })
