/**
 * Standalone-Vorschau des Wirkungsmechanismus (Methodik-Workflow, Schritt PDF-Export).
 *
 * Rendert das echte Produkt-Wirkungsdiagramm (LineageFlowDiagram) außerhalb der App:
 * `scripts/wirkungsmechanismus_preview.py` injiziert die Graph-Daten als
 * `window.__LINEAGE_PREVIEW__` und inlinet das gebaute Bundle in eine
 * eigenständige HTML-Datei neben dem Methodik-PDF.
 */
import { StrictMode, useState } from 'react'
import { createRoot } from 'react-dom/client'
import LineageFlowDiagram from '../components/LineageFlowDiagram'
import type { LineageGraph, ModelParameter } from '../types'
import '../index.css'

interface PreviewTab {
  label: string
  note?: string
  lineage: LineageGraph
  parameters: ModelParameter[]
}

interface PreviewPayload {
  title: string
  subtitle?: string
  banner?: string
  generated?: string
  tabs: PreviewTab[]
}

declare global {
  interface Window {
    __LINEAGE_PREVIEW__?: PreviewPayload
  }
}

// Vorschau nutzt die volle Bildschirmhöhe/-breite (Produkt-CSS begrenzt das
// Diagramm auf 560 px — hier bewusst übersteuert, nur im Preview-Scope).
const PREVIEW_CSS = `
  .wm-preview .kap-lineage-canvas-wrap {
    height: calc(100vh - 235px);
    max-height: none;
    min-height: 480px;
  }
  body { background: var(--bg, #f8fafc); }
`

function PreviewApp({ payload }: { payload: PreviewPayload }) {
  const [active, setActive] = useState(0)
  const tab = payload.tabs[active]
  return (
    <div className="wm-preview" style={{ margin: '0 auto', padding: '12px 18px 24px' }}>
      <style>{PREVIEW_CSS}</style>
      <header style={{ marginBottom: 12 }}>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: 10, flexWrap: 'wrap' }}>
          <h1 style={{ fontSize: '1.25rem', margin: 0 }}>{payload.title}</h1>
          <span style={{ color: 'var(--text-muted, #64748b)', fontSize: '0.85rem' }}>
            Wirkungsmechanismus — Produktdarstellung (KAP3)
            {payload.generated ? ` · Stand ${payload.generated}` : ''}
          </span>
        </div>
        {payload.subtitle && (
          <p style={{ margin: '4px 0 0', color: 'var(--text-muted, #64748b)', fontSize: '0.9rem' }}>
            {payload.subtitle}
          </p>
        )}
        {payload.banner && (
          <div
            style={{
              marginTop: 10,
              padding: '8px 12px',
              borderRadius: 8,
              background: '#fffbeb',
              border: '1px solid #d97706',
              color: '#7c2d12',
              fontSize: '0.85rem',
            }}
          >
            {payload.banner}
          </div>
        )}
      </header>

      {payload.tabs.length > 1 && (
        <div style={{ display: 'flex', gap: 8, marginBottom: 12, flexWrap: 'wrap' }}>
          {payload.tabs.map((t, i) => (
            <button
              key={t.label}
              onClick={() => setActive(i)}
              style={{
                padding: '6px 14px',
                borderRadius: 999,
                border: i === active ? '2px solid #2563eb' : '1px solid #cbd5e1',
                background: i === active ? '#eff6ff' : '#fff',
                fontWeight: i === active ? 600 : 400,
                cursor: 'pointer',
                fontSize: '0.9rem',
              }}
            >
              {t.label}
            </button>
          ))}
        </div>
      )}

      {tab.note && (
        <p style={{ margin: '0 0 10px', color: 'var(--text-muted, #64748b)', fontSize: '0.85rem' }}>
          {tab.note}
        </p>
      )}

      {/* key erzwingt einen frischen Netzwerk-Aufbau je Tab */}
      <LineageFlowDiagram
        key={active}
        lineage={tab.lineage}
        parameters={tab.parameters}
        initialHiddenTypes={[]}
      />

      <p style={{ marginTop: 14, color: 'var(--text-muted, #64748b)', fontSize: '0.78rem' }}>
        Vorschau aus dem Methodik-Workflow (`scripts/wirkungsmechanismus_preview.py`) — rendert
        dieselbe Diagramm-Komponente wie das Produkt (Ebenen-Info „Wirkungsdiagramm"). Alle
        Detailstufen sind eingeblendet; über die Legenden-Chips lassen sich Stufen ausblenden.
        Parameter-Bearbeitung ist in der Vorschau ohne Wirkung (keine Kommune verbunden).
      </p>
    </div>
  )
}

const payload = window.__LINEAGE_PREVIEW__
const rootEl = document.getElementById('root')!
if (!payload || !payload.tabs?.length) {
  rootEl.innerHTML =
    '<p style="padding:2rem;font-family:sans-serif">Keine Vorschau-Daten (window.__LINEAGE_PREVIEW__ fehlt).</p>'
} else {
  createRoot(rootEl).render(
    <StrictMode>
      <PreviewApp payload={payload} />
    </StrictMode>,
  )
}
