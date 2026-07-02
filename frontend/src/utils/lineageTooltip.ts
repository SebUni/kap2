import type { LineageNodeData } from '../types'

function esc(text: string): string {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

/** Wandelt Backend-Tooltip-Text (Zeilen mit \n) in HTML für vis-network um. */
export function formatLineageTooltip(text: string): string {
  const lines = text.split('\n').map(l => l.trim()).filter(Boolean)
  if (lines.length === 0) return ''

  const [title, ...body] = lines
  const parts = [`<div class="kap-lineage-tip-title">${esc(title)}</div>`]

  for (const line of body) {
    const colon = line.indexOf(':')
    if (colon > 0 && colon < 24) {
      const key = line.slice(0, colon)
      const val = line.slice(colon + 1).trim()
      parts.push(
        `<div class="kap-lineage-tip-row">`
        + `<span class="kap-lineage-tip-key">${esc(key)}:</span> `
        + `<span>${esc(val)}</span>`
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
