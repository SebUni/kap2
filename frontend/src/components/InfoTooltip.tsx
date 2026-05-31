import { useState, useRef } from 'react'

interface InfoRow {
  label: string
  value?: string
}

interface Props {
  title: string
  description?: string
  rows?: InfoRow[]
  note?: string
}

/**
 * Kleines (i)-Icon mit Hover-Infobox. Dokumentation "am Objekt" für
 * Hazards/Expositionen/Verwundbarkeiten/Risiken/Maßnahmen.
 */
export default function InfoTooltip({ title, description, rows, note }: Props) {
  const [open, setOpen] = useState(false)
  const [pos, setPos] = useState<{ top: number; left: number }>({ top: 0, left: 0 })
  const iconRef = useRef<HTMLSpanElement>(null)

  const show = () => {
    const el = iconRef.current
    if (el) {
      const r = el.getBoundingClientRect()
      setPos({ top: r.bottom + 6, left: Math.min(r.left, window.innerWidth - 320) })
    }
    setOpen(true)
  }

  return (
    <span
      ref={iconRef}
      className="info-tooltip"
      onMouseEnter={show}
      onMouseLeave={() => setOpen(false)}
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
          style={{
            position: 'fixed', top: pos.top, left: pos.left, zIndex: 9999,
            width: 300, background: 'var(--surface)', border: '1px solid var(--border)',
            borderRadius: 8, padding: '0.6rem 0.7rem', boxShadow: '0 8px 24px rgba(0,0,0,0.18)',
            fontSize: '0.75rem', fontWeight: 400, color: 'var(--text)', textAlign: 'left',
            cursor: 'default', whiteSpace: 'normal',
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
