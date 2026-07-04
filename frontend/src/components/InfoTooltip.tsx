import { useState, useRef } from 'react'
import type { SourceReference } from '../types'

interface InfoRow {
  label: string
  value?: string
}

interface Props {
  title: string
  description?: string
  rows?: InfoRow[]
  note?: string
  references?: SourceReference[]
}

/**
 * Kleines (i)-Icon mit Hover-Infobox. Dokumentation "am Objekt" für
 * Klimatische Einflüsse/Räumliche Expositionen/Sensitivitäten/Risiken/Maßnahmen.
 *
 * Enthält die Box klickbare Quellen (references), bleibt sie beim Hinüberfahren
 * offen (verzögertes Schließen), damit Original-/Archiv-Links anklickbar sind.
 */
export default function InfoTooltip({ title, description, rows, note, references }: Props) {
  const [open, setOpen] = useState(false)
  const [pos, setPos] = useState<{ top: number; left: number }>({ top: 0, left: 0 })
  const iconRef = useRef<HTMLSpanElement>(null)
  const closeTimer = useRef<ReturnType<typeof setTimeout> | null>(null)

  const clearClose = () => {
    if (closeTimer.current) { clearTimeout(closeTimer.current); closeTimer.current = null }
  }
  const show = () => {
    clearClose()
    const el = iconRef.current
    if (el) {
      const r = el.getBoundingClientRect()
      setPos({ top: r.bottom + 6, left: Math.min(r.left, window.innerWidth - 410) })
    }
    setOpen(true)
  }
  // Verzögertes Schließen, damit der Weg vom Icon in die Box (Links anklicken) nicht abbricht.
  const scheduleClose = () => {
    clearClose()
    closeTimer.current = setTimeout(() => setOpen(false), 180)
  }

  return (
    <span
      ref={iconRef}
      className="info-tooltip"
      onMouseEnter={show}
      onMouseLeave={scheduleClose}
      style={{
        display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
        width: 15, height: 15, borderRadius: '50%',
        border: '1px solid var(--border)', color: 'var(--text-muted)',
        fontSize: '0.62rem', fontWeight: 700, cursor: 'help',
        flexShrink: 0, lineHeight: 1,
      }}
    >
      i
      {open && (
        <div
          onMouseEnter={clearClose}
          onMouseLeave={scheduleClose}
          style={{
            position: 'fixed', top: pos.top, left: pos.left, zIndex: 9999,
            minWidth: 390, width: 390, maxWidth: 'min(390px, 96vw)', background: 'var(--surface)', border: '1px solid var(--border)',
            borderRadius: 8, padding: '0.6rem 0.7rem', boxShadow: '0 8px 24px rgba(0,0,0,0.18)',
            fontSize: '0.75rem', fontWeight: 400, color: 'var(--text)', textAlign: 'left',
            cursor: 'default', whiteSpace: 'normal', maxHeight: '70vh', overflowY: 'auto',
          }}
        >
          <div style={{ fontWeight: 700, marginBottom: 4 }}>{title}</div>
          {description && (
            <div style={{ color: 'var(--text-muted)', marginBottom: rows?.length ? 6 : 0 }}>
              {description}
            </div>
          )}
          {rows?.map((r, i) => (
            <div key={i} style={{ display: 'flex', gap: 6, marginTop: 2 }}>
              <span style={{ color: 'var(--text-muted)', minWidth: 70 }}>{r.label}:</span>
              <span style={{ flex: 1 }}>{r.value}</span>
            </div>
          ))}
          {references && references.length > 0 && (
            <div style={{ marginTop: 6, paddingTop: 6, borderTop: '1px solid var(--border)' }}>
              <div style={{ fontWeight: 600, marginBottom: 3 }}>Quellen (IEEE)</div>
              {references.map((r, i) => (
                <div key={i} style={{ marginBottom: 5, fontSize: '0.7rem', lineHeight: 1.35 }}>
                  <div style={{ color: 'var(--text-muted)' }}>[{i + 1}] {r.ieee}</div>
                  <div style={{ display: 'flex', gap: 10, marginTop: 1 }}>
                    {r.url && (
                      <a href={r.url} target="_blank" rel="noopener noreferrer" style={{ color: 'var(--accent, #2563eb)' }}>
                        ↗ Original
                      </a>
                    )}
                    {r.archive_url && (
                      <a href={r.archive_url} target="_blank" rel="noopener noreferrer" style={{ color: 'var(--accent, #2563eb)' }}>
                        🗄 Archiv-Snapshot
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
          {note && (
            <div style={{
              marginTop: 6, paddingTop: 6, borderTop: '1px solid var(--border)',
              color: 'var(--warning, #b45309)', fontSize: '0.7rem',
            }}>
              {note}
            </div>
          )}
        </div>
      )}
    </span>
  )
}
