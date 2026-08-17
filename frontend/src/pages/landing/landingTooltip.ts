/**
 * Detail-Inspektor-Tooltip der Landing-Karte — abgeleitet aus
 * components/MapView.tsx (`buildTooltipHtml`, Risiko-Zweig), aber **kompakt**:
 * ohne den grauen Index-Berechnungs-Kasten, ohne Formelzeilen und ohne die
 * „Norm"-Spalte. Bleibt: Titel + großer Wert + Faktoren-Tabelle
 * (Risiko-Index, H/E/V mit Wert+Quelle, Outcome-Faktoren, Index-Anteil).
 * Die CSS-Klassen (`kap-tooltip*`, `kap-tooltip-grid`, `landing-tooltip-grid`,
 * `col-*`) sind global in index.css definiert; wir erzeugen nur den HTML-String.
 */
import type { HevRecipeMeta, LayerMeta, OutcomeFactorMeta, RiskRecipe } from '../../types'

const TOOLTIP_MIN_WIDTH = 300
const TOOLTIP_MAX_WIDTH = 440

// Minimal-Formen (der Cache-Snapshot ist auf die genutzten Felder eingedampft).
export interface CellPathwayTerm {
  h_norm: number; e_norm: number; v_norm: number; term: number; is_max?: boolean
}
export interface CellPathwayBreakdown {
  pathways: CellPathwayTerm[]; max_term: number; index: number
}
export interface CellOutcomeBreakdown {
  ref_value: number; scale_factor: number; index_fraction: number
  cell_pop: number; cell_area_km2: number; outcome: number
}

export interface RiskCellProps {
  index: number
  H: number[][]
  E: number[][]
  V: number[][]
  pathways: CellPathwayBreakdown
  outcome: CellOutcomeBreakdown
  value: number
}

function fmtNum(v: number) {
  return v.toLocaleString('de-DE', { maximumFractionDigits: 3 })
}

function provBadge(prov?: string) {
  const map: Record<string, { bg: string; text: string; label: string }> = {
    extern: { bg: '#dbeafe', text: '#1d4ed8', label: 'extern' },
    param: { bg: '#fef3c7', text: '#b45309', label: 'Parameter' },
    computed: { bg: '#ede9fe', text: '#6d28d9', label: 'berechnet' },
  }
  const s = map[prov || ''] || map.extern
  return ` <span style="font-size:8px;background:${s.bg};color:${s.text};padding:0 3px;border-radius:2px;margin-left:3px">${s.label}</span>`
}

function outcomeFactorValue(factor: OutcomeFactorMeta, cell: CellOutcomeBreakdown, r: RiskRecipe): string {
  if (factor.key === 'ref_value')
    return `${fmtNum(factor.value ?? cell.ref_value)}${factor.unit ? ' ' + factor.unit : ''}`
  if (factor.key === 'scale_factor') {
    if (r.scale === 'pop')
      return `${fmtNum(cell.scale_factor)} (= ${fmtNum(cell.cell_pop)} Ew. / 100.000)`
    if (r.scale === 'area')
      return `${fmtNum(cell.scale_factor)} (= ${fmtNum(cell.cell_area_km2)} km² / 50)`
    return fmtNum(cell.scale_factor)
  }
  return '—'
}

/** Baut den kompakten Risiko-Inspektor als HTML-String (ohne Formeln/Norm-Spalte). */
export function buildRiskTooltipHtml(meta: LayerMeta, props: RiskCellProps, value: number): string {
  const gridCells: string[] = []
  const gridHeader = () => {
    gridCells.push(
      '<span class="col-head">Name</span>',
      '<span class="col-head col-val">Wert</span>',
      '<span class="col-head">Quelle</span>',
    )
  }
  const gridSection = (title: string) => { gridCells.push(`<span class="grid-section">${title}</span>`) }
  const gridRow = (name: string, val: string, src = '') => {
    gridCells.push(
      `<span class="col-name">${name}</span>`,
      `<span class="col-val">${val || '—'}</span>`,
      `<span class="col-src">${src}</span>`,
    )
  }
  const gridHtml = () => gridCells.length ? `<div class="kap-tooltip-grid landing-tooltip-grid">${gridCells.join('')}</div>` : ''

  let h = `<div class="kap-tooltip-inner" style="--kap-tooltip-min:${TOOLTIP_MIN_WIDTH}px;--kap-tooltip-max:${TOOLTIP_MAX_WIDTH}px;font-family:system-ui,sans-serif;font-size:11px;line-height:1.4">`
  h += `<div style="font-weight:700;font-size:12px;margin-bottom:2px">${meta.label}</div>`
  h += `<div style="font-size:13px;font-weight:700;color:#0f172a;margin-bottom:4px">${fmtNum(value)} ${meta.unit}</div>`

  const r = meta.recipe as RiskRecipe
  const idx = props.index

  gridHeader()
  gridRow('Risiko-Index', fmtNum(idx), '0–100')

  const sec = (title: string, items?: HevRecipeMeta[], vals?: number[][]) => {
    if (!items?.length) return
    gridSection(title)
    items.forEach((it, i) => {
      const pair = (vals && vals[i]) || [0, 0]
      const src = [
        it.source,
        it.spatial === false ? 'nicht räumlich' : '',
        it.norm_min != null && it.norm_max != null ? `[${fmtNum(it.norm_min)}…${fmtNum(it.norm_max)}]` : '',
      ].filter(Boolean).join(' · ')
      gridRow(it.name, `${fmtNum(pair[0])}${it.unit ? ' ' + it.unit : ''}`, src)
    })
  }
  sec('Klimatische Einflüsse', r.hazards, props.H)
  sec('Räumliche Expositionen', r.exposures, props.E)
  sec('Sensitivitäten', r.vulnerabilities, props.V)

  const cellOutcome = props.outcome
  if (cellOutcome && r.outcome_factors?.length) {
    gridSection('Outcome-Faktoren')
    for (const factor of r.outcome_factors) {
      gridRow(
        factor.label,
        `${outcomeFactorValue(factor, cellOutcome, r)}${provBadge(factor.prov)}`,
        [factor.formula, factor.source].filter(Boolean).join(' · '),
      )
    }
    gridRow('Index-Anteil', fmtNum(cellOutcome.index_fraction), `Index ${fmtNum(idx)}/100`)
  }

  h += gridHtml()
  h += '</div>'
  return h
}
