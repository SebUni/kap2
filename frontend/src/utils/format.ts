/** Gemeinsame Formatierer und Chart-Palette des Dashboards. */

export const fmtEur = (v: number): string =>
  v.toLocaleString('de-DE', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 })

/** Kompakte €-Angabe für Hero-KPIs (1,2 Mio. €, 340 Tsd. €). */
export const fmtEurCompact = (v: number): string => {
  if (v === 0) return fmtEur(0)
  const sign = v < 0 ? -1 : 1
  const abs = Math.abs(v)
  // Erst runden, dann die Größenklasse wählen: sonst erscheint 9.960 als „10.000 €“
  // neben „10 Tsd. €“ und 999.600 als „1.000 Tsd. €“.
  const magnitude = Math.pow(10, 1 - Math.floor(Math.log10(abs)))
  const small = Math.abs(Math.round(v * magnitude) / magnitude)
  const tsd = Math.round(abs / 1e3)
  const mio = Math.round((abs / 1e6) * 100) / 100
  const de = (x: number, d: number) => (sign * x).toLocaleString('de-DE', { maximumFractionDigits: d })
  if (abs >= 1e9 || mio >= 1000) return `${de(abs / 1e9, 2)} Mrd. €`
  if (abs >= 1e6 || tsd >= 1000) return `${de(abs / 1e6, 2)} Mio. €`
  if (abs >= 1e4 || small >= 1e4) return `${de(tsd, 0)} Tsd. €`
  return fmtEur(sign * small)
}

export const fmtNum = (v: number, digits = 1): string =>
  v.toLocaleString('de-DE', { maximumFractionDigits: digits })

export const LINE_PALETTE = [
  '#ef4444', '#f59e0b', '#3b82f6', '#10b981',
  '#8b5cf6', '#ec4899', '#14b8a6', '#f97316',
]
