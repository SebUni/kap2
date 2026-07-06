/** Gemeinsame Formatierer und Chart-Palette des Dashboards. */

export const fmtEur = (v: number): string =>
  v.toLocaleString('de-DE', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 })

/** Kompakte €-Angabe für Hero-KPIs (1,2 Mio. €, 340 Tsd. €). */
export const fmtEurCompact = (v: number): string => {
  const abs = Math.abs(v)
  if (abs >= 1e9) return `${(v / 1e9).toLocaleString('de-DE', { maximumFractionDigits: 2 })} Mrd. €`
  if (abs >= 1e6) return `${(v / 1e6).toLocaleString('de-DE', { maximumFractionDigits: 2 })} Mio. €`
  if (abs >= 1e4) return `${(v / 1e3).toLocaleString('de-DE', { maximumFractionDigits: 0 })} Tsd. €`
  return fmtEur(v)
}

export const fmtNum = (v: number, digits = 1): string =>
  v.toLocaleString('de-DE', { maximumFractionDigits: digits })

export const LINE_PALETTE = [
  '#ef4444', '#f59e0b', '#3b82f6', '#10b981',
  '#8b5cf6', '#ec4899', '#14b8a6', '#f97316',
]
