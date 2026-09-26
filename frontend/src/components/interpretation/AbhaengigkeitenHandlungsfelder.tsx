import { useEffect, useState } from 'react'
import { api } from '../../api/client'
import type { AbhaengigkeitBeziehung, InterpretationAbhaengigkeiten } from '../../api/client'
import type { StrukturierterAbschnittProps } from './ErgebnisseInterpretierenTab'

const UEBERSCHRIFT = 'Abhängigkeiten über Handlungsfelder'

/** Richtungslogik wie in _abschnitt_abhaengigkeiten (ergebnis_interpretation_markdown.py). */
function richtungText(b: AbhaengigkeitBeziehung): string {
  if (b.wirkt_auf_partner && b.partner_wirkt_ein) return 'wechselseitig'
  if (b.wirkt_auf_partner) return 'wirkt auf'
  return 'wird beeinflusst von'
}

/** Beziehungen je Klimawirkung über Handlungsfelder hinweg, ungewichtet und ohne Rangfolge. */
export default function AbhaengigkeitenHandlungsfelder({ kommuneId }: StrukturierterAbschnittProps) {
  const [daten, setDaten] = useState<InterpretationAbhaengigkeiten | null>(null)
  const [fehler, setFehler] = useState<string | null>(null)

  useEffect(() => {
    let aktiv = true
    setDaten(null)
    setFehler(null)
    api.getInterpretationAbhaengigkeiten(kommuneId)
      .then(d => { if (aktiv) setDaten(d) })
      .catch(e => {
        if (aktiv) setFehler(e instanceof Error ? e.message : 'Die Abhängigkeiten konnten nicht geladen werden.')
      })
    return () => { aktiv = false }
  }, [kommuneId])

  if (fehler) {
    return (
      <div>
        <h2>{UEBERSCHRIFT}</h2>
        <p role="alert" style={{ color: 'var(--danger, #c0392b)' }}>
          Die Abhängigkeiten konnten nicht geladen werden: {fehler}
        </p>
      </div>
    )
  }
  if (!daten) {
    return (
      <div>
        <h2>{UEBERSCHRIFT}</h2>
        <p>Lädt …</p>
      </div>
    )
  }

  const umfangSatz = daten.umfang === 'gerechnet'
    ? 'Die Liste beruht auf den gerechneten Klimawirkungen dieser Kommune.'
    : 'Die Liste beruht auf dem ganzen Katalog der Klimawirkungen, weil für diese Kommune noch keine Rechnung vorliegt.'

  return (
    <div>
      <h2>{UEBERSCHRIFT}</h2>
      <p>{umfangSatz}</p>
      <p>Wie stark eine Abhängigkeit wirkt, ist nicht bewertet.</p>
      {daten.klimawirkungen.map(k => (
        <div key={k.kwra_id} style={{ marginBottom: '1rem' }}>
          <p style={{ marginBottom: 4 }}>
            <strong>{k.name}</strong> (Handlungsfeld {k.handlungsfeld || '—'})
          </p>
          <p style={{ margin: '0 0 4px' }}>
            {k.andere_handlungsfelder.length > 0
              ? `Weitere Handlungsfelder: ${k.andere_handlungsfelder.join(', ')}.`
              : 'Keine benannte Beziehung in ein anderes Handlungsfeld.'}
          </p>
          {k.beziehungen.length > 0 && (
            <ul style={{ margin: 0 }}>
              {k.beziehungen.map(b => (
                <li key={b.beziehung_nr}>
                  {richtungText(b)}: {b.partner_name} ({b.partner_handlungsfeld || 'Handlungsfeld nicht geführt'})
                </li>
              ))}
            </ul>
          )}
        </div>
      ))}
    </div>
  )
}
