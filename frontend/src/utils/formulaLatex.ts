import katex from 'katex'
import 'katex/dist/katex.min.css'

// Wandelt die strukturierten Formeltexte des Backends („clamp(Heiße Tage +
// 1,5·UHI-ΔT ; 0…40)“) in LaTeX um und rendert sie mit KaTeX. Prosa-Formeln
// („Regionaler Annahmewert“) bleiben Text — dafür entscheidet isMathFormula.

const PROSE_MARKERS = [
  'Konstantwert', 'Annahmewert', 'Fallback', 'invers', 'Direkt aus', 'INKAR',
  'Proxy', 'Zensus je', 'Screening', 'Quelle', ' aus ', 'Index aus',
]

export function isMathFormula(formula: string): boolean {
  if (!formula) return false
  if (!/[·×+/^=]|−|clamp\(|max\(|min\(|≥|≤/.test(formula)) return false
  // Starke Formel-Signale (clamp/min/max mit Rechenzeichen) schlagen
  // Prosa-Marker wie „…; Fallback 40“ — aber nur bei Zeilen, die kurz genug
  // sind, um als (nicht umbrechbare) LaTeX-Zeile gesetzt zu werden.
  if (
    formula.length <= 120
    && /clamp\(|min\(|max\(/.test(formula)
    && /[·×+/^]|−/.test(formula)
  ) return true
  return !PROSE_MARKERS.some(m => formula.includes(m))
}

// Vor-Ersetzungen für bekannte Symbole (vor der Tokenisierung)
const PRE_SUBSTITUTIONS: [RegExp, string][] = [
  [/UHI-ΔT/g, ' @DTUHI@ '],
  [/ΔT/g, ' @DT@ '],
  [/P90-Index/g, ' @P90@ @TXT{-Index}@ '],
  [/P90/g, ' @P90@ '],
  [/Ĥ/g, ' @HH@ '],
  [/Ê/g, ' @HE@ '],
  [/V̂/g, ' @HV@ '],
  [/w_([A-Z])/g, ' @W$1@ '],
  [/\s+[—–]\s+/g, ' ; '],
]

const TOKEN_MAP: Record<string, string> = {
  '@DTUHI@': '\\Delta T_{\\mathrm{UHI}}',
  '@DT@': '\\Delta T',
  '@P90@': 'P_{90}',
  '@HH@': '\\hat{H}',
  '@HE@': '\\hat{E}',
  '@HV@': '\\hat{V}',
}

const FUNCTION_WORDS = new Set(['max', 'min', 'exp'])

/** clamp(X ; a…b) → min(b, max(a, X)) — Begrenzung als bekannte Mathematik. */
function rewriteClamp(s: string): string {
  return s.replace(
    /clamp\((.+);\s*([\d.,]+)\s*…\s*([\d.,]+)\s*\)/,
    (_m, expr: string, lo: string, hi: string) =>
      `min(${hi}; max(${lo}; ${expr.trim()}))`,
  )
}

export function formulaToLatex(formula: string): string {
  let s = rewriteClamp(formula)
  for (const [re, repl] of PRE_SUBSTITUTIONS) s = s.replace(re, repl)

  const tokenRe = /@W([A-Z])@|@[A-Z0-9]+@|@TXT\{([^}]*)\}@|\d+(?:[.,]\d+)?|[A-Za-zÄÖÜäöüß][A-Za-z0-9ÄÖÜäöüß\-²³%]*|…|[·×−+/^=();,<>≥≤]|\s+|./g

  const out: string[] = []
  let textRun: string[] = []
  const flushText = () => {
    if (textRun.length) {
      const t = textRun.join(' ')
        .replace(/\\/g, '')
        .replace(/([%#&_{}])/g, '\\$1')
      out.push(`\\text{${t}}`)
      textRun = []
    }
  }

  for (const m of s.matchAll(tokenRe)) {
    const tok = m[0]
    if (/^\s+$/.test(tok)) continue

    if (m[1]) { flushText(); out.push(`w_{${m[1]}}`); continue }
    if (m[2] !== undefined) { textRun.push(m[2]); continue }
    if (TOKEN_MAP[tok]) { flushText(); out.push(TOKEN_MAP[tok]); continue }

    if (/^\d/.test(tok)) {
      flushText()
      out.push(tok.replace(',', '{,}'))
      continue
    }
    if (/^[A-Za-zÄÖÜäöüß]/.test(tok)) {
      if (FUNCTION_WORDS.has(tok)) {
        flushText()
        out.push(`\\${tok}`)
      } else if (/[²³]$/.test(tok)) {
        // Einheiten mit Hochzahl (km², m³) → \text{km}^{2}
        flushText()
        out.push(`\\text{${tok.slice(0, -1)}}^{${tok.endsWith('²') ? '2' : '3'}}`)
      } else {
        textRun.push(tok)
      }
      continue
    }
    flushText()
    switch (tok) {
      case '·': case '×': out.push('\\cdot '); break
      case '−': out.push('- '); break
      case '/': out.push('/'); break
      case '…': out.push('\\ldots '); break
      case ';': out.push(',\\ '); break
      case ',': out.push(',\\ '); break
      case '≥': out.push('\\ge '); break
      case '≤': out.push('\\le '); break
      case '→': out.push('\\rightarrow '); break
      case '<': out.push('< '); break
      case '>': out.push('> '); break
      case '(': out.push('('); break
      case ')': out.push(')'); break
      case '&': out.push('\\&\\ '); break
      case 'Σ': out.push('\\Sigma\\, '); break
      case '€': out.push('\\text{€}'); break
      default: out.push(tok)
    }
  }
  flushText()
  return out.join(' ')
}

function renderLatex(latex: string): string | null {
  try {
    return katex.renderToString(latex, {
      throwOnError: true,
      output: 'html',
      strict: false,
    })
  } catch {
    return null
  }
}

/** Rendert einen Backend-Formeltext als KaTeX-HTML; null wenn Prosa/Fehler. */
export function renderFormulaHtml(formula: string): string | null {
  if (!isMathFormula(formula)) return null
  return renderLatex(formulaToLatex(formula))
}

/** Rendert eine bereits fertige LaTeX-Zeichenkette ($$…$$-Zeilen des Backends). */
export function renderLatexHtml(latex: string): string | null {
  return renderLatex(latex)
}
