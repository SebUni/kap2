/**
 * Landingpage-Stammdaten: Maßnahmen-Kostensätze (Katalog) und die statischen
 * KWRA-Radar-Felder. Die Karten-Zellwerte kommen aus dem echten Backend-Cache
 * (landingData.ts / data/oschatz-landing.json); der `ScenarioCell`-Typ dient
 * als gemeinsame Form für die Maßnahmen-Schadensfunktion (miniGameLogic.ts).
 */

export type CellType = 'bebauung' | 'park' | 'marktplatz' | 'strasse' | 'acker'

export type RiskKey = 'hitzemortalitaet' | 'gebaeudeschaden' | 'landw_schaden'

export interface ScenarioCell {
  id: number
  row: number
  col: number
  typ: CellType
  /** Versiegelungsgrad 0..1 — steuert, wo Begrünung wirkt. */
  versiegelung: number
  /** Erwarteter Schaden €/Jahr (Spielgrundlage Widget C). */
  schadenEurA: number
  /** Risiko-Indizes 0–100 je echtem Risiko. */
  indizes: Record<RiskKey, number>
  kontext: {
    einwohner: number
    ue65Anteil: number
    baujahr: number | null
    ackerHa: number
  }
}

// ── Maßnahme „Entsiegelung & Stadtgrün" (Kombination, Katalogwerte) ─────────
export const MEASURE = {
  name: 'Entsiegelung & Stadtgrün',
  /** €/m² CAPEX: Entsiegelung 35 + Stadtgrün 25 (Katalog). */
  capexPerM2Desiegelung: 35,
  capexPerM2Gruen: 25,
  /** €/m²/a OPEX: 0,5 + 3,0 (Katalog). */
  opexPerM2Year: 3.5,
  /** Kombinierte Reduktion: 1 − (1−0,30)(1−0,25) = 0,475. */
  reduction: 1 - (1 - 0.3) * (1 - 0.25),
  /** Umgesetzte Fläche je gewählter Zelle (realistisch: Teil des Platzes). */
  areaM2PerCell: 400,
  /** Abschreibungszeitraum für die Annualisierung der CAPEX. */
  lifetimeYears: 20,
  budgetEur: 120_000,
} as const

export function measureCapexPerCell(capexPerM2 = MEASURE.capexPerM2Desiegelung + MEASURE.capexPerM2Gruen): number {
  return MEASURE.areaM2PerCell * capexPerM2
}

export function measureOpexPerCellYear(): number {
  return MEASURE.areaM2PerCell * MEASURE.opexPerM2Year
}

// ── Widget A: KWRA-Risikofelder (Netzdiagramm) ──────────────────────────────
export interface RadarField {
  feld: string
  /** Belastung: mittlerer KWRA-Index (P90 exponierter Zellen) 0–100. */
  index: number
  /** Hotspot (Maximum): höchster Zell-Index im Feld 0–100 (≥ index). */
  hotspot: number
  /** Erwartete Schäden Mio €/Jahr. */
  mioEurA: number
  topTreiber: string
}

export const RADAR_FIELDS: RadarField[] = [
  { feld: 'Hitze', index: 78, hotspot: 91, mioEurA: 2.1, topTreiber: 'Erwartete Mortalität (Hitze)' },
  { feld: 'Trockenheit', index: 52, hotspot: 90, mioEurA: 0.9, topTreiber: 'Landwirtschaftliche Schäden' },
  { feld: 'Hochwasser/Starkregen', index: 65, hotspot: 92, mioEurA: 1.6, topTreiber: 'Gebäudeschäden' },
  { feld: 'Gradueller Wandel', index: 38, hotspot: 58, mioEurA: 0.3, topTreiber: 'Verlust Ökosystemleistungen' },
  { feld: 'Verbund/Kaskade', index: 44, hotspot: 70, mioEurA: 0.5, topTreiber: 'Ausfall kritischer Infrastruktur' },
]
