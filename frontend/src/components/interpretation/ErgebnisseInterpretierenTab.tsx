import { useCallback, useEffect, useState } from 'react'
import type { ComponentType } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { api } from '../../api/client'
import { useStore } from '../../store'
import NachweiseEinbeziehung from './NachweiseEinbeziehung'

export interface StrukturierterAbschnittProps {
  kommuneId: number
  berichtNeuLaden: () => void
}

/**
 * Überschrift (Text nach "## ") → Komponente. Hat eine Überschrift hier einen Eintrag, wird nur die Komponente
 * gerendert, nicht zusätzlich das Markdown. Die Einträge folgen mit den
 * späteren Paketen.
 */
export const STRUKTURIERTE_ABSCHNITTE: Record<string, ComponentType<StrukturierterAbschnittProps>> = {
  Einbeziehung: NachweiseEinbeziehung,
}

interface Abschnitt {
  /** Überschrift ohne "## "; leer für den Text vor der ersten Überschrift. */
  titel: string
  markdown: string
}

/** Teilt den Bericht an Zeilen, die mit "## " beginnen. */
function teileBericht(text: string): Abschnitt[] {
  const abschnitte: Abschnitt[] = []
  let aktuell: { titel: string; zeilen: string[] } = { titel: '', zeilen: [] }
  const abschliessen = () => {
    const markdown = aktuell.zeilen.join('\n')
    if (aktuell.titel || markdown.trim()) abschnitte.push({ titel: aktuell.titel, markdown })
  }
  for (const zeile of text.split('\n')) {
    if (zeile.startsWith('## ')) {
      abschliessen()
      aktuell = { titel: zeile.slice(3).trim(), zeilen: [zeile] }
    } else {
      aktuell.zeilen.push(zeile)
    }
  }
  abschliessen()
  return abschnitte
}

export default function ErgebnisseInterpretierenTab() {
  const kommune = useStore(s => s.kommune)
  const kommuneId = kommune?.id
  const [bericht, setBericht] = useState<string | null>(null)
  const [laedt, setLaedt] = useState(false)
  const [fehler, setFehler] = useState<string | null>(null)
  const [version, setVersion] = useState(0)

  const berichtNeuLaden = useCallback(() => setVersion(v => v + 1), [])

  useEffect(() => {
    if (kommuneId == null) return
    let abgebrochen = false
    setLaedt(true)
    setFehler(null)
    api.getInterpretationsbericht(kommuneId)
      .then(text => { if (!abgebrochen) setBericht(text) })
      .catch(e => {
        if (!abgebrochen) setFehler(e instanceof Error ? e.message : 'Der Bericht konnte nicht geladen werden.')
      })
      .finally(() => { if (!abgebrochen) setLaedt(false) })
    return () => { abgebrochen = true }
  }, [kommuneId, version])

  const herunterladen = () => {
    if (bericht == null) return
    const blob = new Blob([bericht], { type: 'text/markdown;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `ergebnisse-interpretieren-${kommuneId ?? 'kommune'}.md`
    document.body.appendChild(a)
    a.click()
    a.remove()
    URL.revokeObjectURL(url)
  }

  if (kommuneId == null) {
    return <div style={{ padding: '1.5rem', color: 'var(--text-muted)' }}>Bitte zuerst eine Kommune wählen.</div>
  }

  return (
    <div style={{ flex: 1, overflowY: 'auto', padding: '1rem 1.5rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
        <h2 style={{ margin: 0, fontSize: '1.2rem' }}>Ergebnisse interpretieren</h2>
        <button
          onClick={herunterladen}
          disabled={bericht == null || laedt}
          style={{
            marginLeft: 'auto', background: 'transparent', color: 'var(--text)',
            border: '1px solid var(--border)', borderRadius: 8, padding: '0 12px', height: 34,
            cursor: bericht == null || laedt ? 'not-allowed' : 'pointer',
            opacity: bericht == null || laedt ? 0.5 : 1, fontSize: '0.85rem',
          }}
        >
          Bericht herunterladen
        </button>
      </div>

      {laedt && <p style={{ color: 'var(--text-muted)' }}>Bericht wird geladen …</p>}
      {fehler && (
        <p role="alert" style={{ color: '#dc2626' }}>
          Der Bericht konnte nicht geladen werden: {fehler}
        </p>
      )}

      {!laedt && !fehler && bericht != null && teileBericht(bericht).map((abschnitt, i) => {
        const Strukturiert = STRUKTURIERTE_ABSCHNITTE[abschnitt.titel]
        return (
          <section key={`${i}-${abschnitt.titel}`} className="chat-markdown" style={{ marginBottom: '1.5rem' }}>
            {Strukturiert
              ? <Strukturiert kommuneId={kommuneId} berichtNeuLaden={berichtNeuLaden} />
              : <ReactMarkdown remarkPlugins={[remarkGfm]}>{abschnitt.markdown}</ReactMarkdown>}
          </section>
        )
      })}
    </div>
  )
}
