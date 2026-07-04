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

/** Lesbare Darstellung für Konfigurations-Parameter (Tausendertrennzeichen, sinnvolle Nachkommastellen). */
export function fmtParamValue(v: number | string | null | undefined): string {
  if (v == null || v === '') return '—'
  const n = Number(v)
  if (Number.isNaN(n)) return String(v)

  const isWhole = Math.abs(n - Math.round(n)) < 1e-9
  const abs = Math.abs(n)
  let digits: number
  if (isWhole) {
    digits = 0
  } else if (abs >= 1) {
    digits = 2
  } else if (abs >= 0.01) {
    digits = 4
  } else {
    digits = 6
  }

  return n.toLocaleString('de-DE', {
    minimumFractionDigits: 0,
    maximumFractionDigits: digits,
  })
}
