import type { LineageNodeData, ModelParameter } from '../types'

function esc(text: string): string {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
}

function fmtNum(v: unknown): string {
  const n = Number(v)
  if (Number.isNaN(n)) return String(v ?? '—')
  return n.toLocaleString('de-DE', { maximumFractionDigits: 4 })
}

export function operatorKindLabel(kind: string, meta: Record<string, unknown>): string {
  // Skalierungs-Operatoren tragen ihr Label im Meta (z. B. "Kostensatz").
  if (kind === 'scaling') return String(meta.label || 'Skalierung')
  if (kind === 'norm') return 'Normierung'
  if (kind === 'multiply' || kind === 'scale_factor') return '×'
  if (kind === 'divide') return '÷'
  if (kind === 'add') return '+'
  if (kind === 'weight') return 'Gewicht'
  return String(meta.label || kind)
}

const SINGLE_LABEL_KINDS = new Set([
  'count', 'coverage', 'neighbor', 'weighted_sum', 'formula', 'max', 'min',
  // Schicht-B-Operatoren (Schadensfunktionen): Label kommt aus dem Backend-Meta.
  'af', 'gv', 'damage_curve', 'sum_cells', 'p90', 'intensity', 'ratio',
])

export function operatorShowsSingleLabel(kind: string): boolean {
  return SINGLE_LABEL_KINDS.has(kind)
}

export function operatorDisplayValue(kind: string, meta: Record<string, unknown>): string {
  if (operatorShowsSingleLabel(kind)) return ''
  if (kind === 'multiply' || kind === 'divide' || kind === 'add' || kind === 'scale_factor') {
    return String(meta.label || (kind === 'divide' ? '÷' : kind === 'add' ? '+' : '×'))
  }
  const label = meta.label as string
  if (label && !['×', '+', '÷', 'max', 'min'].includes(label)) return label
  return ''
}

export interface OperatorEditField {
  parameterId: string
  value: string
  editable: boolean
  label: string
}

export function operatorEditFields(
  data: LineageNodeData,
  parameters: ModelParameter[],
): OperatorEditField[] {
  const meta = data.meta ?? {}
  const kind = meta.op_kind as string

  if (kind === 'scaling' || kind === 'multiplier') {
    const pid = meta.parameter_id as string
    const p = parameters.find(x => x.id === pid)
    if (!p) return []
    return [{
      parameterId: pid,
      value: String(p.value),
      editable: p.editable,
      label: 'Referenzwert',
    }]
  }

  if (kind === 'norm') {
    const fields: OperatorEditField[] = []
    for (const [key, label] of [
      [meta.param_max_id, 'Obergrenze'],
      [meta.param_min_id, 'Untergrenze'],
    ] as const) {
      const p = parameters.find(x => x.id === key)
      if (!p) continue
      fields.push({
        parameterId: p.id,
        value: String(p.value),
        editable: p.editable,
        label,
      })
    }
    return fields
  }

  return []
}

export function edgeWeightEditField(
  meta: Record<string, unknown>,
  parameters: ModelParameter[],
): OperatorEditField | null {
  if (meta.op_kind !== 'weight') return null
  const pid = meta.parameter_id as string | undefined
  const p = pid ? parameters.find(x => x.id === pid) : undefined
  if (!p) {
    // Ohne Registry-Parameter (Pfadgewichte sind Modellkonstanten): nur anzeigen.
    return {
      parameterId: pid ?? '',
      value: String(meta.weight ?? ''),
      editable: false,
      label: 'Gewicht',
    }
  }
  return {
    parameterId: p.id,
    value: String(p.value),
    editable: p.editable,
    label: 'Gewicht',
  }
}

export { fmtNum, esc }
