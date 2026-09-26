import { useCallback, useEffect, useState } from 'react'
import { api } from '../../api/client'
import type { NachweisJeArt } from '../../api/client'
import type { StrukturierterAbschnittProps } from './ErgebnisseInterpretierenTab'

/** ISO-Datum (JJJJ-MM-TT) → TT.MM.JJJJ. */
function datumAnzeigen(iso: string): string {
  const teile = iso.slice(0, 10).split('-')
  return teile.length === 3 ? `${teile[2]}.${teile[1]}.${teile[0]}` : iso
}

const feldStil = {
  background: 'var(--bg)', color: 'var(--text)', border: '1px solid var(--border)',
  borderRadius: 6, padding: '4px 8px', fontSize: '0.85rem',
} as const

export default function NachweiseEinbeziehung({ kommuneId, berichtNeuLaden }: StrukturierterAbschnittProps) {
  const [arten, setArten] = useState<NachweisJeArt[]>([])
  const [laedt, setLaedt] = useState(false)
  const [fehler, setFehler] = useState<string | null>(null)
  const [art, setArt] = useState('')
  const [stelle, setStelle] = useState('')
  const [datum, setDatum] = useState('')
  const [vermerk, setVermerk] = useState('')
  const [speichert, setSpeichert] = useState(false)

  const laden = useCallback(async () => {
    setLaedt(true)
    try {
      setArten(await api.getInterpretationNachweise(kommuneId))
      setFehler(null)
    } catch (e) {
      setFehler(e instanceof Error ? e.message : 'Die Nachweise konnten nicht geladen werden.')
    } finally {
      setLaedt(false)
    }
  }, [kommuneId])

  useEffect(() => { void laden() }, [laden])

  const speichern = async () => {
    setSpeichert(true)
    setFehler(null)
    try {
      await api.createInterpretationNachweis(kommuneId, {
        art: art as NachweisJeArt['art'],
        stelle: stelle.trim(),
        datum,
        vermerk: vermerk.trim() || null,
      })
      setArt(''); setStelle(''); setDatum(''); setVermerk('')
      await laden()
      berichtNeuLaden()
    } catch (e) {
      setFehler(e instanceof Error ? e.message : 'Der Nachweis konnte nicht gespeichert werden.')
    } finally {
      setSpeichert(false)
    }
  }

  const loeschen = async (id: number, stelleText: string) => {
    if (!confirm(`Nachweis "${stelleText}" wirklich löschen?`)) return
    setFehler(null)
    try {
      await api.deleteInterpretationNachweis(kommuneId, id)
      await laden()
      berichtNeuLaden()
    } catch (e) {
      setFehler(e instanceof Error ? e.message : 'Der Nachweis konnte nicht gelöscht werden.')
    }
  }

  const gefuellt = art !== '' && stelle.trim() !== '' && datum !== ''

  return (
    <div>
      <h2>Einbeziehung</h2>
      {laedt && <p style={{ color: 'var(--text-muted)' }}>Nachweise werden geladen …</p>}
      {fehler && <p role="alert" style={{ color: '#dc2626' }}>{fehler}</p>}

      {arten.map(a => (
        <div key={a.art} style={{ marginBottom: '0.75rem' }}>
          <strong>{a.bezeichnung}</strong>
          {a.eintraege.length === 0 ? (
            <div style={{ color: 'var(--text-muted)' }}>nicht erfasst</div>
          ) : (
            <ul style={{ margin: '0.25rem 0', paddingLeft: '1.25rem' }}>
              {a.eintraege.map(e => (
                <li key={e.id}>
                  {e.stelle}, {datumAnzeigen(e.datum)}{e.vermerk ? ` – ${e.vermerk}` : ''}{' '}
                  <button
                    className="btn btn-danger btn-sm"
                    onClick={() => void loeschen(e.id, e.stelle)}
                    title="Löschen"
                    style={{ padding: '2px 6px' }}
                  >✕</button>
                </li>
              ))}
            </ul>
          )}
        </div>
      ))}

      <form
        onSubmit={ev => { ev.preventDefault(); if (gefuellt && !speichert) void speichern() }}
        style={{ display: 'flex', flexDirection: 'column', gap: 8, maxWidth: 480, marginTop: '1rem' }}
      >
        <strong>Nachweis erfassen</strong>
        <label style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          Art
          <select value={art} onChange={e => setArt(e.target.value)} style={feldStil}>
            <option value=""></option>
            {arten.map(a => <option key={a.art} value={a.art}>{a.bezeichnung}</option>)}
          </select>
        </label>
        <label style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          Stelle
          <input
            type="text" value={stelle} onChange={e => setStelle(e.target.value)}
            placeholder="Stelle oder Organisation, kein Personenname" style={feldStil}
          />
          <small style={{ color: 'var(--text-muted)' }}>Stelle oder Organisation, kein Personenname</small>
        </label>
        <label style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          Datum
          <input type="date" value={datum} onChange={e => setDatum(e.target.value)} style={feldStil} />
        </label>
        <label style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          Vermerk (optional)
          <input type="text" value={vermerk} onChange={e => setVermerk(e.target.value)} style={feldStil} />
        </label>
        <div>
          <button type="submit" className="btn btn-primary" disabled={!gefuellt || speichert}>
            Speichern
          </button>
        </div>
      </form>
    </div>
  )
}
