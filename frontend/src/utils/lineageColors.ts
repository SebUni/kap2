import type { LineageNodeType } from '../types'

export interface LineageTypeColor {
  bg: string
  border: string
}

/** Einheitliches Farbsystem für Knoten, Pfeile, Legende und Overlays. */
export const LINEAGE_TYPE_COLORS: Record<string, LineageTypeColor> = {
  source: { bg: '#f1f5f9', border: '#64748b' },
  parameter: { bg: '#f5f3ff', border: '#7c3aed' },
  intermediate: { bg: '#eff6ff', border: '#2563eb' },
  hazard: { bg: '#fee2e2', border: '#dc2626' },
  exposure: { bg: '#ffedd5', border: '#ea580c' },
  vulnerability: { bg: '#f3e8ff', border: '#9333ea' },
  pathway: { bg: '#f8fafc', border: '#64748b' },
  aggregation: { bg: '#eef2ff', border: '#4f46e5' },
  outcome: { bg: '#dcfce7', border: '#047857' },
  norm: { bg: '#dcfce7', border: '#047857' },
  operator: { bg: '#fffbeb', border: '#d97706' },
}

export const LINEAGE_CSS_VARS: Record<string, string> = {
  source: '#64748b',
  parameter: '#7c3aed',
  intermediate: '#2563eb',
  hazard: '#dc2626',
  exposure: '#ea580c',
  vulnerability: '#9333ea',
  pathway: '#64748b',
  aggregation: '#4f46e5',
  outcome: '#047857',
  norm: '#047857',
  operator: '#d97706',
}

export function lineageNodeColors(type: string): LineageTypeColor {
  return LINEAGE_TYPE_COLORS[type] ?? LINEAGE_TYPE_COLORS.intermediate
}

export function edgeColorFromSource(type: LineageNodeType | string | undefined): string {
  return lineageNodeColors(type ?? 'intermediate').border
}
