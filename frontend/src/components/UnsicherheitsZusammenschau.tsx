import { useEffect, useState } from 'react'
import { api } from '../api/client'
import type { UnsicherheitsZusammenschau as Zusammenschau } from '../api/client'

/** Unsicherheits-Zusammenschau je Handlungsfeld mit Interpretationshinweis (ISO 14091, UBA 2.2.6),
 *  angezeigt vor den Handlungsoptionen. */
export default function UnsicherheitsZusammenschau({ kommuneId }: { kommuneId: number }) {
  const [daten, setDaten] = useState<Zusammenschau | null>(null)
  const [fehler, setFehler] = useState(false)

  useEffect(() => {
    let aktiv = true
    setDaten(null)
    setFehler(false)
    api.getUnsicherheitsZusammenschau(kommuneId)
      .then(d => { if (aktiv) setDaten(d) })
      .catch(() => { if (aktiv) setFehler(true) })
    return () => { aktiv = false }
  }, [kommuneId])

  if (fehler) {
    return (
      <div style={{ marginBottom: 16, fontSize: '0.8rem', color: 'var(--text-muted)' }}>
        Die Unsicherheits-Zusammenschau konnte nicht geladen werden.
      </div>
    )
  }
  if (!daten) return null

  return (
    <section style={{ marginBottom: 16, padding: '0.75rem', border: '1px solid var(--border)', borderRadius: 8 }}>
      <h3 style={{ fontSize: '0.95rem', fontWeight: 600, marginBottom: 6 }}>
        Unsicherheiten der Ergebnisse je Handlungsfeld
      </h3>
      {daten.hinweis && (
        <p style={{ fontSize: '0.85rem', marginBottom: 8, color: 'var(--danger)' }}>{daten.hinweis}</p>
      )}
      <table className="data-table">
        <thead>
          <tr>
            <th>Handlungsfeld</th>
            <th>Niedrigste Gewissheitsstufe</th>
            <th>Nicht belegte Parameter</th>
          </tr>
        </thead>
        <tbody>
          {daten.handlungsfelder.map(f => (
            <tr key={f.handlungsfeld}>
              <td>{f.handlungsfeld}</td>
              <td>{f.niedrigste_gewissheit}</td>
              <td>{f.parameter_nicht_belegt}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  )
}
