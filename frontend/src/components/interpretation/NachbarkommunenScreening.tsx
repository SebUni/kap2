import { useEffect, useState } from 'react'
import { api } from '../../api/client'
import type { NachbarScreeningEintrag } from '../../api/client'
import type { StrukturierterAbschnittProps } from './ErgebnisseInterpretierenTab'

const zelle = { padding: '4px 8px', borderBottom: '1px solid var(--border)', textAlign: 'right' } as const

function indexText(wert: number | null | undefined): string {
  return wert == null ? '–' : wert.toLocaleString('de-DE', { maximumFractionDigits: 1 })
}

/** Screening-Index der eigenen und der angrenzenden Gemeinden je Klimawirkung, als Liste ohne Verdichtung. */
export default function NachbarkommunenScreening({ kommuneId }: StrukturierterAbschnittProps) {
  const [eintraege, setEintraege] = useState<NachbarScreeningEintrag[] | null>(null)
  const [fehler, setFehler] = useState<string | null>(null)

  useEffect(() => {
    let aktiv = true
    setEintraege(null)
    setFehler(null)
    api.getInterpretationNachbarkommunen(kommuneId)
      .then(daten => { if (aktiv) setEintraege(daten) })
      .catch(e => {
        if (aktiv) setFehler(e instanceof Error ? e.message : 'Die Nachbarkommunen konnten nicht geladen werden.')
      })
    return () => { aktiv = false }
  }, [kommuneId])

  if (fehler) {
    return (
      <div>
        <h2>Nachbarkommunen</h2>
        <p role="alert" style={{ color: 'var(--danger, #c0392b)' }}>
          Die Screening-Indizes der Nachbarkommunen konnten nicht geladen werden: {fehler}
        </p>
      </div>
    )
  }
  if (!eintraege) {
    return (
      <div>
        <h2>Nachbarkommunen</h2>
        <p>Lädt …</p>
      </div>
    )
  }

  const mitIndex = eintraege.filter(e => e.index_vorhanden)
  const ohneIndex = eintraege.filter(e => !e.index_vorhanden)

  // Spalten: angrenzende Gemeinden, in der Reihenfolge ihres ersten Auftretens.
  const nachbarn = new Map<string, string>()
  for (const e of mitIndex) {
    for (const n of e.nachbarn) if (!nachbarn.has(n.ags)) nachbarn.set(n.ags, n.name ?? n.ags)
  }

  return (
    <div>
      <h2>Nachbarkommunen</h2>
      <p>
        Skala: Screening-Index 0–100, bundesweit normiert. Die Werte stehen einzeln nebeneinander und sind nicht
        zusammengefasst.
      </p>
      {mitIndex.length === 0 ? (
        <p>Für keine Klimawirkung liegt ein Screening-Index vor.</p>
      ) : (
        <div style={{ overflowX: 'auto' }}>
          <table style={{ borderCollapse: 'collapse', fontSize: '0.9rem' }}>
            <thead>
              <tr>
                <th style={{ ...zelle, textAlign: 'left' }}>Klimawirkung</th>
                <th style={zelle}>Eigene Gemeinde</th>
                {[...nachbarn].map(([ags, name]) => <th key={ags} style={zelle}>{name}</th>)}
              </tr>
            </thead>
            <tbody>
              {mitIndex.map(e => (
                <tr key={e.code}>
                  <td style={{ ...zelle, textAlign: 'left' }}>{e.name ?? e.code}</td>
                  <td style={zelle}>{indexText(e.eigener_index)}</td>
                  {[...nachbarn.keys()].map(ags => (
                    <td key={ags} style={zelle}>{indexText(e.nachbarn.find(n => n.ags === ags)?.index)}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {ohneIndex.length > 0 && (
        <>
          <p>Klimawirkungen ohne Screening-Index:</p>
          <ul>
            {ohneIndex.map(e => (
              <li key={e.code}>{e.name ?? e.code}: kein Screening-Index vorhanden</li>
            ))}
          </ul>
        </>
      )}
    </div>
  )
}
