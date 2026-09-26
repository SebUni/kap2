import { useEffect, useState } from 'react'
import { api } from '../../api/client'
import type { InterpretationDiversitaet } from '../../api/client'

/** Gender- und Diversitätsaspekte je Klimawirkung im Wortlaut der Schnittstelle, mit Quelle. Keine Bewertung. */
export default function DiversitaetAspekte() {
  const [daten, setDaten] = useState<InterpretationDiversitaet | null>(null)
  const [fehler, setFehler] = useState<string | null>(null)

  useEffect(() => {
    let aktiv = true
    setDaten(null)
    setFehler(null)
    api.getInterpretationDiversitaet()
      .then(d => { if (aktiv) setDaten(d) })
      .catch(e => {
        if (aktiv) setFehler(e instanceof Error ? e.message : 'Die Aspekte konnten nicht geladen werden.')
      })
    return () => { aktiv = false }
  }, [])

  if (fehler) {
    return (
      <div>
        <h2>Gender und Diversität</h2>
        <p role="alert" style={{ color: 'var(--danger, #c0392b)' }}>
          Die Gender- und Diversitätsaspekte konnten nicht geladen werden: {fehler}
        </p>
      </div>
    )
  }
  if (!daten) {
    return (
      <div>
        <h2>Gender und Diversität</h2>
        <p>Lädt …</p>
      </div>
    )
  }

  const eintraege = Object.entries(daten.je_klimawirkung)
  const quelle = daten.quelle

  return (
    <div>
      <h2>Gender und Diversität</h2>
      <p>
        Quelle:{' '}
        <a href={quelle.url} target="_blank" rel="noopener noreferrer">{quelle.titel}</a>
        {quelle.seite != null && <>, S. {quelle.seite}</>}
      </p>
      {eintraege.length === 0 && <p>Für keine Klimawirkung sind Aspekte hinterlegt.</p>}
      {eintraege.map(([code, e]) => (
        <div key={code} style={{ marginBottom: '1rem' }}>
          <h3>{code}</h3>
          {e.beruecksichtigt.length > 0 && (
            <>
              <p>Geht in die Rechnung ein:</p>
              <ul>
                {e.beruecksichtigt.map((b, i) => (
                  <li key={`${i}-${b.aspekt}`}>
                    <strong>{b.aspekt}</strong>: {b.wie} <em>(Fundstelle: {b.fundstelle})</em>
                  </li>
                ))}
              </ul>
            </>
          )}
          {e.nicht_beruecksichtigt.length > 0 && (
            <>
              <p>Geht nicht in die Rechnung ein:</p>
              <ul>
                {e.nicht_beruecksichtigt.map((n, i) => (
                  <li key={`${i}-${n.aspekt}`}>
                    {n.aspekt} <em>({n.quelle}, S. {n.seite})</em>
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>
      ))}
    </div>
  )
}
