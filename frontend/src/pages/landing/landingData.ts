/**
 * Gebündelter Cache der echten Oschatz-Analyse (Demo-Kommune) für die
 * Landing-Karten — einmal aus dem Backend gezogen und als JSON eingefroren
 * (siehe scripts/build-landing-snapshot.mjs). Kein Backend-Zugriff zur Laufzeit.
 */
import type { RiskRecipe } from '../../types'
import snapshot from './data/oschatz-landing.json'
import type { RiskCellProps } from './landingTooltip'
import type { ScenarioCell } from './scenario'

/** Choropleth-Rampe des Produkts (MapView) — Konsistenz mit der echten Karte. */
export const CHOROPLETH_COLORS = ['#fef9c3', '#fde047', '#fb923c', '#ef4444', '#991b1b']

export interface GeoCell {
  id: number
  polygon: [number, number][]
  center: [number, number]
}

export interface RiskLayer {
  key: string
  code: string
  label: string
  unit: string
  min: number
  max: number
  recipe: RiskRecipe
  cells: Record<string, RiskCellProps>
}

interface Snapshot {
  bounds: [[number, number], [number, number]]
  cells: GeoCell[]
  risks: Record<string, Omit<RiskLayer, 'key'>>
  measure: { damageKey: string }
}

const data = snapshot as unknown as Snapshot

export const LANDING_BOUNDS = data.bounds
export const LANDING_CELLS: GeoCell[] = data.cells

/** Risiko-Reihenfolge im Radio-Menü (Auszug der Demo-Risiken). */
const RISK_ORDER = ['hitzemortalitaet', 'gebaeudeschaden', 'landw_schaden'] as const
export type LandingRiskKey = (typeof RISK_ORDER)[number]

/** Kurzer Erklärsatz je Risiko (i-Tooltip im Radio-Menü). */
const RISK_HINTS: Record<LandingRiskKey, string> = {
  hitzemortalitaet: 'Menschen sterben an Hitze im dichten Zentrum — dort, wo viele (ältere) Menschen wohnen und die Stadt sich aufheizt.',
  gebaeudeschaden: 'Gebäude leiden im Starkregen dort, wo das Wasser zusammenläuft und wertige Bebauung steht.',
  landw_schaden: 'Ernten fallen am Ackerrand aus — dort, wo Böden bei Dürre trockenfallen und die Bewässerung fehlt.',
}

export const RISK_LAYERS: (RiskLayer & { hint: string })[] = RISK_ORDER.map((key) => ({
  key, ...data.risks[key], hint: RISK_HINTS[key],
}))

// ── Maßnahmen-Spiel: reale Schadens- und Versiegelungswerte je Zelle ────────
const damageLayer = data.risks[data.measure.damageKey]
export const DAMAGE_BY_ID: Record<number, number> = Object.fromEntries(
  Object.entries(damageLayer.cells).map(([id, c]) => [Number(id), c.value ?? 0]),
)
/**
 * Effektiver Wirkungsanteil der Begrünung je Zelle (× Katalog-Reduktion 0,475
 * ≈ 0,15). Kalibriert, damit eine gut platzierte Maßnahme im dicht bebauten
 * Zentrum den Nutzen über die laufenden Kosten hebt, eine flächige oder am
 * Rand platzierte hingegen nicht. (Ein per-Zelle-Versiegelungsproxy fehlt in
 * den Demo-Daten — der Grünanteil liegt fast überall bei ~100 %.)
 */
const GREENING_EFFECTIVENESS = 0.32

/**
 * Reale Oschatz-Zellen als Grundlage des Maßnahmen-Spiels (Schadensfunktion in
 * miniGameLogic): Schaden = Gebäudeschaden (€/Jahr); der Nutzen skaliert mit
 * dem dortigen Schaden — dort wirkt Handeln, wo viel Schaden entsteht.
 */
export const MEASURE_CELLS: ScenarioCell[] = LANDING_CELLS.map((c) => ({
  id: c.id, row: 0, col: 0, typ: 'bebauung',
  versiegelung: GREENING_EFFECTIVENESS,
  schadenEurA: DAMAGE_BY_ID[c.id] ?? 0,
  indizes: { hitzemortalitaet: 0, gebaeudeschaden: 0, landw_schaden: 0 },
  kontext: { einwohner: 0, ue65Anteil: 0, baujahr: null, ackerHa: 0 },
}))

/** 4 wirksamste Zellen (höchster reduzierbarer Schaden) als Parameter-Beispiel. */
export const SAMPLE_MEASURE_IDS: Set<number> = new Set(
  [...MEASURE_CELLS]
    .sort((a, b) => b.schadenEurA * b.versiegelung - a.schadenEurA * a.versiegelung)
    .slice(0, 4).map((c) => c.id),
)

/** Ray-Casting: liegt der Punkt im (geschlossenen) Ring? */
function pointInRing(pt: [number, number], ring: [number, number][]): boolean {
  const [x, y] = pt
  let inside = false
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const [xi, yi] = ring[i]
    const [xj, yj] = ring[j]
    if (yi > y !== yj > y && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) inside = !inside
  }
  return inside
}

/** IDs aller Zellen, deren Mittelpunkt im gezeichneten Ring liegt. */
export function coveredCellIds(ring: [number, number][]): Set<number> {
  const ids = new Set<number>()
  if (ring.length < 3) return ids
  for (const c of LANDING_CELLS) if (pointInRing(c.center, ring)) ids.add(c.id)
  return ids
}
