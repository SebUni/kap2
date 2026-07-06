import type { LineageNodeData } from '../types'

const TYPE_HEIGHT: Record<string, number> = {
  source: 44,
  parameter: 64,
  intermediate: 56,
  hazard: 52,
  exposure: 52,
  vulnerability: 52,
  pathway: 72,
  aggregation: 48,
  outcome: 48,
  operator: 56,
}

const TYPE_WIDTH: Record<string, number> = {
  source: 120,
  parameter: 110,
  intermediate: 140,
  hazard: 140,
  exposure: 140,
  vulnerability: 140,
  pathway: 260,
  aggregation: 120,
  outcome: 160,
  operator: 56,
}

const OP_HEIGHT: Record<string, number> = {
  scaling: 72,
  norm: 88,
  max: 56,
  multiply: 48,
  weight: 64,
  count: 56,
  coverage: 56,
  divide: 48,
  add: 44,
  clamp: 48,
  formula: 52,
  af: 48,
  gv: 48,
  damage_curve: 48,
  sum_cells: 48,
  p90: 48,
  intensity: 48,
  ratio: 48,
}

export function labelLineCount(label: string, type: string): number {
  if (type === 'pathway') return Math.max(1, Math.ceil(label.length / 42))
  if (type === 'outcome' || type === 'aggregation') return 1
  return Math.max(1, (label.match(/\n/g)?.length ?? 0) + 1)
}

export function estimateNodeHeight(node: LineageNodeData): number {
  const meta = node.meta ?? {}
  if (node.type === 'operator') {
    const kind = meta.op_kind as string
    return OP_HEIGHT[kind] ?? TYPE_HEIGHT.operator
  }
  const base = TYPE_HEIGHT[node.type] ?? 52
  const lines = labelLineCount(node.label, node.type)
  return base + Math.max(0, lines - 1) * 18
}

export function estimateNodeWidth(node: LineageNodeData): number {
  const meta = node.meta ?? {}
  if (node.type === 'operator') {
    const kind = meta.op_kind as string
    if (kind === 'multiply' || kind === 'divide' || kind === 'scale_factor') return 48
    if (kind === 'scaling' || kind === 'norm') return 96
    if (kind === 'max' || kind === 'intensity' || kind === 'damage_curve' || kind === 'ratio') return 92
    if (kind === 'sum_cells' || kind === 'gv' || kind === 'p90' || kind === 'af') return 72
    return TYPE_WIDTH.operator
  }
  if (node.type === 'pathway') {
    return Math.max(TYPE_WIDTH.pathway, Math.min(360, node.label.length * 7))
  }
  return TYPE_WIDTH[node.type] ?? 180
}

export const COL_GAP = 24
export const ROW_PAD = 8
