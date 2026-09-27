import { useEffect, useState } from 'react'
import { api } from '../../api/client'
import type { InterpretationLeitfragen } from '../../api/client'

/**
 * Leitfragen der UBA-Broschüre mit Seite, Stand und Begründung (Checkliste Zeile 19, A1).
 * Die Fundstelle im Programm (``beantwortet_durch``, ein Code-Pfad) erscheint nur klein als
 * Nebenangabe, nie als Haupttext (A-0034: kein Code-Pfad im Text für die Kommune).
 */
export default function LeitfragenUebersicht() {
  const [daten, setDaten] = useState<InterpretationLeitfragen | null>(null)
  const [fehler, setFehler] = useState<string | null>(null)

  useEffect(() => {
    let aktiv = true
    setDaten(null)
    setFehler(null)
    api.getInterpretationLeitfragen()
      .then(d => { if (aktiv) setDaten(d) })
      .catch(e => {
        if (aktiv) setFehler(e instanceof Error ? e.message : 'Die Leitfragen konnten nicht geladen werden.')
      })
    return () => { aktiv = false }
  }, [])

  if (fehler) {
    return (
      <div>
        <h2>Leitfragen</h2>
        <p role="alert" style={{ color: 'var(--danger, #c0392b)' }}>
          Die Leitfragen konnten nicht geladen werden: {fehler}
        </p>
      </div>
    )
  }
  if (!daten) {
    return (
      <div>
        <h2>Leitfragen</h2>
        <p>Lädt …</p>
      </div>
    )
  }

  const quelle = daten.quelle

  return (
    <div>
      <h2>Leitfragen</h2>
      <p>
        Quelle:{' '}
        <a href={quelle.url} target="_blank" rel="noopener noreferrer">{quelle.titel}</a>
      </p>
      <ul>
        {daten.leitfragen.map(f => {
          const beantwortet = f.beantwortet_durch !== 'nicht beantwortet'
          return (
            <li key={f.nr} style={{ marginBottom: '1rem' }}>
              <p style={{ margin: 0 }}>
                <strong>Leitfrage {f.nr}:</strong> {f.wortlaut} <em>(S. {f.seite})</em>
              </p>
              <p style={{ margin: 0 }}>
                Stand: {beantwortet ? 'beantwortet' : 'nicht beantwortet'}
                {beantwortet && <> — {f.stelle_im_produkt}</>}
              </p>
              <p style={{ margin: 0 }}>{f.begruendung}</p>
              <p style={{ margin: 0, fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                Fundstelle im Programm: {f.beantwortet_durch}
              </p>
            </li>
          )
        })}
      </ul>
    </div>
  )
}
