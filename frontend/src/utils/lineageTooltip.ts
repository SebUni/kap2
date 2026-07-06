import type { LineageNodeData } from '../types'
import { renderFormulaHtml, renderLatexHtml } from './formulaLatex'

function esc(text: string): string {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

// Tooltip-Schlüssel, deren Wert eine Formel ist → als LaTeX rendern
const FORMULA_KEYS = new Set(['Berechnung', 'Formel'])

/** „Key: Wert“-Zeile mit Key aus FORMULA_KEYS? Dann Wert als LaTeX rendern. */
function formulaKeyOf(line: string): string | null {
  const colon = line.indexOf(':')
  if (colon <= 0 || colon >= 24) return null
  const key = line.slice(0, colon)
  return FORMULA_KEYS.has(key) ? key : null
}

/** Wandelt Backend-Tooltip-Text (Zeilen mit \n) in HTML für vis-network um. */
export function formatLineageTooltip(text: string): string {
  const lines = text.split('\n').map(l => l.trim()).filter(Boolean)
  if (lines.length === 0) return ''

  // Beginnt der Tooltip direkt mit einer Formelzeile („Berechnung: …“),
  // gibt es keine Titelzeile — sonst würde die Formel roh angezeigt.
  const firstIsFormula = formulaKeyOf(lines[0]) !== null
  const body = firstIsFormula ? lines : lines.slice(1)
  const parts = firstIsFormula
    ? []
    : [`<div class="kap-lineage-tip-title">${esc(lines[0])}</div>`]

  for (const line of body) {
    // Fertige LaTeX-Zeilen des Backends: $$…$$
    if (line.startsWith('$$') && line.endsWith('$$')) {
      const html = renderLatexHtml(line.slice(2, -2))
      if (html) {
        parts.push(`<div class="kap-lineage-tip-math">${html}</div>`)
        continue
      }
    }
    const colon = line.indexOf(':')
    if (colon > 0 && colon < 24) {
      const key = line.slice(0, colon)
      const val = line.slice(colon + 1).trim()
      const mathHtml = FORMULA_KEYS.has(key) ? renderFormulaHtml(val) : null
      parts.push(
        `<div class="kap-lineage-tip-row">`
        + `<span class="kap-lineage-tip-key">${esc(key)}:</span> `
        + (mathHtml
          ? `<span class="kap-lineage-tip-math">${mathHtml}</span>`
          : `<span>${esc(val)}</span>`)
        + `</div>`,
      )
    } else {
      parts.push(`<div class="kap-lineage-tip-text">${esc(line)}</div>`)
    }
  }
  return parts.join('')
}

/** Baut den Hover-Tooltip für einen Knoten im Lineage-Diagramm. */
export function buildNodeTooltip(
  data: LineageNodeData,
  incomingLabels: string[] = [],
): string {
  const meta = data.meta ?? {}
  if (meta.tooltip) {
    return formatLineageTooltip(String(meta.tooltip))
  }

  // Fallback, falls Backend kein tooltip-Feld liefert
  const lines = [data.label]
  if (meta.formula) lines.push(`Berechnung: ${meta.formula}`)
  if (incomingLabels.length) lines.push(`Eingaben: ${incomingLabels.join(', ')}`)
  return formatLineageTooltip(lines.join('\n'))
}
