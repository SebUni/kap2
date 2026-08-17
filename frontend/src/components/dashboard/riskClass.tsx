import type { RiskAggregate, RiskClass } from '../../types'

/** Status-Farben der Risikoklassen (App-Tokens; Klasse = Zustand, keine Serie). */
export const RISK_CLASS_COLORS: Record<RiskClass, string> = {
  gering: 'var(--success)',
  mittel: 'var(--warning)',
  hoch: 'var(--danger)',
}

export const RISK_CLASS_LABELS: Record<RiskClass, string> = {
  gering: 'Gering',
  mittel: 'Mittel',
  hoch: 'Hoch',
}

/** Fallback-Klassifikation aus den Server-Grenzen (für Einträge ohne risk_class). */
export function classifyIndex(
  value: number, classification?: RiskAggregate['classification'],
): RiskClass {
  const bounds = classification?.bounds ?? { medium_min: 20, high_min: 50 }
  if (value >= bounds.high_min) return 'hoch'
  if (value >= bounds.medium_min) return 'mittel'
  return 'gering'
}

/** Kleines farbiges Badge „Gering/Mittel/Hoch" — Text trägt die Info, Farbe verstärkt. */
export function RiskClassChip({ cls, prefix }: { cls: RiskClass; prefix?: string }) {
  const color = RISK_CLASS_COLORS[cls]
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center', gap: 4,
      fontSize: '0.7rem', fontWeight: 600, lineHeight: 1,
      padding: '3px 8px', borderRadius: 999,
      color, background: 'color-mix(in srgb, currentColor 12%, transparent)',
      border: '1px solid color-mix(in srgb, currentColor 35%, transparent)',
      whiteSpace: 'nowrap',
    }}>
      {prefix && <span style={{ color: 'var(--text-muted)', fontWeight: 500 }}>{prefix}</span>}
      {RISK_CLASS_LABELS[cls]}
    </span>
  )
}
