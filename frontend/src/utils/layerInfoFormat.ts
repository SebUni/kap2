export function provLabel(prov: string): string {
  if (prov === 'extern') return 'extern'
  if (prov === 'param') return 'Parameter'
  if (prov === 'computed') return 'berechnet'
  return prov
}

export function fmtNum(v: number | string | null | undefined, digits = 2): string {
  if (v == null || v === '') return '—'
  const n = Number(v)
  if (Number.isNaN(n)) return String(v)
  return n.toLocaleString('de-DE', { maximumFractionDigits: digits })
}
