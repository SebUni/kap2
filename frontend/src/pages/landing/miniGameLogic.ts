/**
 * Pure Spiellogik für Widget C (Maßnahme einzeichnen) — unit-testbar.
 *
 * Vereinfachte Produktlogik (Plan §2.1b): der Nutzen einer Begrünungs-/
 * Entsiegelungsmaßnahme in einer Zelle skaliert mit dem dortigen Schaden UND
 * dem Versiegelungsgrad — im schon grünen Park (versiegelung ≈ 0, kleiner
 * Basisschaden) verpufft das Budget, am versiegelten Marktplatz wirkt es.
 */
import {
  MEASURE, ScenarioCell, measureCapexPerCell, measureOpexPerCellYear,
} from './scenario'

export interface GameResult {
  cellCount: number
  capexEur: number
  opexEurA: number
  avoidedEurA: number
  /** CAPEX annualisiert + OPEX. */
  annualCostEurA: number
  /** Nutzen/Kosten pro Jahr. */
  benefitCostRatio: number
  /** Jahre bis CAPEX durch (Nutzen − OPEX) getilgt ist; null = nie. */
  amortYears: number | null
  win: boolean
  /** Index-Reduktion der am stärksten betroffenen gewählten Zelle. */
  bestCell: { before: number; after: number } | null
}

export function cellBenefitEurA(cell: ScenarioCell): number {
  return cell.schadenEurA * MEASURE.reduction * cell.versiegelung
}

export function maxSelectableCells(capexPerM2?: number): number {
  return Math.max(1, Math.floor(MEASURE.budgetEur / measureCapexPerCell(capexPerM2)))
}

export function evaluateSelection(
  cells: ScenarioCell[],
  selectedIds: ReadonlySet<number>,
  capexPerM2?: number,
): GameResult {
  const selected = cells.filter((c) => selectedIds.has(c.id))
  const capexEur = selected.length * measureCapexPerCell(capexPerM2)
  const opexEurA = selected.length * measureOpexPerCellYear()
  const avoidedEurA = selected.reduce((sum, c) => sum + cellBenefitEurA(c), 0)
  const annualCostEurA = capexEur / MEASURE.lifetimeYears + opexEurA
  const benefitCostRatio = annualCostEurA > 0 ? avoidedEurA / annualCostEurA : 0
  const netPerYear = avoidedEurA - opexEurA
  const amortYears = netPerYear > 0 ? capexEur / netPerYear : null

  let bestCell: GameResult['bestCell'] = null
  if (selected.length > 0) {
    const hottest = selected.reduce((a, b) =>
      a.indizes.hitzemortalitaet >= b.indizes.hitzemortalitaet ? a : b)
    const before = hottest.indizes.hitzemortalitaet
    const after = Math.round(before * (1 - MEASURE.reduction * hottest.versiegelung))
    bestCell = { before, after }
  }

  return {
    cellCount: selected.length,
    capexEur,
    opexEurA,
    avoidedEurA,
    annualCostEurA,
    benefitCostRatio,
    amortYears,
    win: selected.length > 0 && benefitCostRatio >= 1,
    bestCell,
  }
}

export function formatEur(v: number): string {
  if (Math.abs(v) >= 1_000_000) return `${(v / 1_000_000).toLocaleString('de-DE', { maximumFractionDigits: 1 })} Mio €`
  if (Math.abs(v) >= 1_000) return `${Math.round(v / 1_000).toLocaleString('de-DE')} T€`
  return `${Math.round(v).toLocaleString('de-DE')} €`
}
