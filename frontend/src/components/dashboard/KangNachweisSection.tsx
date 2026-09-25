import { useEffect, useState } from 'react'
import { api } from '../../api/client'
import type { KangNachweis } from '../../api/client'
import { useStore } from '../../store'

/**
 * Fachübergreifende Berücksichtigung nach § 8 Abs. 1 KAnG (Konformitätszeile 13).
 *
 * Zeigt je KAnG-Handlungsfeld Status, Risiken, Schadenssumme und Maßnahmen aus
 * GET /kommune/{id}/kang-nachweis, darunter die Zusammenfassung und den Abgrenzungstext
 * wörtlich. Felder mit Status „nicht betroffen“ bleiben als Zeile stehen. Die Sektion
 * bescheinigt keine Rechtskonformität; der Abgrenzungstext der Antwort ist immer sichtbar.
 */

function euroText(wert: number | null): string {
  if (wert === null) return '—'
  if (Math.abs(wert) >= 1e9) return `${(wert / 1e9).toLocaleString('de-DE', { maximumFractionDigits: 2 })} Mrd. €`
  if (Math.abs(wert) >= 1e6) return `${(wert / 1e6).toLocaleString('de-DE', { maximumFractionDigits: 2 })} Mio. €`
  return `${wert.toLocaleString('de-DE', { maximumFractionDigits: 0 })} €`
}

function liste(werte: string[]): string {
  return werte.length ? werte.join(', ') : '—'
}

export default function KangNachweisSection({ className = '' }: { className?: string }) {
  const kommune = useStore(s => s.kommune)
  const kommuneId = kommune?.id
  const [daten, setDaten] = useState<KangNachweis | null>(null)
  const [fehler, setFehler] = useState<string | null>(null)

  useEffect(() => {
    if (kommuneId === undefined) return
    let aktiv = true
    setDaten(null)
    setFehler(null)
    api.getKangNachweis(kommuneId)
      .then(d => { if (aktiv) setDaten(d) })
      .catch(e => { if (aktiv) setFehler(e instanceof Error ? e.message : String(e)) })
    return () => { aktiv = false }
  }, [kommuneId])

  const z = daten?.zusammenfassung

  return (
    <section className={`dashboard-section ${className}`}>
      <h2 className="section-title">Fachübergreifende Berücksichtigung nach § 8 Abs. 1 KAnG</h2>
      <div className="chart-card">
        {fehler && (
          <p style={{ color: 'var(--text-muted)' }}>Nachweis konnte nicht geladen werden: {fehler}</p>
        )}
        {!daten && !fehler && (
          <p style={{ color: 'var(--text-muted)' }}>Lade Nachweis …</p>
        )}
        {daten && z && (
          <>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Handlungsfeld</th>
                  <th>Status</th>
                  <th>Risiken</th>
                  <th style={{ textAlign: 'right' }}>Schadenssumme</th>
                  <th>Maßnahmen</th>
                </tr>
              </thead>
              <tbody>
                {daten.handlungsfelder.map(h => (
                  <tr key={`${h.cluster}/${h.feld}`}>
                    <td style={{ fontWeight: 500 }}>
                      {h.feld}
                      <div style={{ fontWeight: 400, fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                        {h.cluster}
                      </div>
                    </td>
                    <td style={h.status === 'nicht betroffen' ? { color: 'var(--text-muted)' } : undefined}>
                      {h.status}
                    </td>
                    <td>{liste(h.risiken)}</td>
                    <td style={{ textAlign: 'right' }}>{euroText(h.schaden_eur)}</td>
                    <td>{liste(h.massnahmen)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <p style={{ fontSize: '0.85rem', marginTop: 8 }}>
              <strong>Zusammenfassung:</strong> {z.betroffen_n} Felder betroffen,{' '}
              {z.beruecksichtigt_n} berücksichtigt, {z.offen_n} offen.{' '}
              Integrierende Maßnahmen (über mehrere Handlungsfelder): {liste(z.integrierende_massnahmen)}.
            </p>
            {(daten.nicht_zugeordnet.risiken.length > 0 || daten.nicht_zugeordnet.massnahmen.length > 0) && (
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                Nicht zugeordnet: Risiken {liste(daten.nicht_zugeordnet.risiken.map(r => r.code))};
                Maßnahmen {liste(daten.nicht_zugeordnet.massnahmen)}.
              </p>
            )}
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 6 }}>
              {daten.abgrenzung}
            </p>
          </>
        )}
      </div>
    </section>
  )
}
