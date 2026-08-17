import { useEffect, useRef, useState } from 'react'
import { api, ChatError, type ChatMessage, type AiUsage } from '../../api/client'
import { useStore } from '../../store'
import ChatMessageView from './ChatMessageView'

const QUICK_PROMPTS = [
  'Ordne die Ergebnisse dieser Kommune ein.',
  'Entwirf einen Berichtsabschnitt zur Betroffenheit.',
  'Schlage passende Anpassungsmaßnahmen vor.',
]

function fmtK(n: number): string {
  if (n >= 1000) return `${(n / 1000).toLocaleString('de-DE', { maximumFractionDigits: 1 })}k`
  return String(n)
}

/**
 * Schwebender KI-Assistent (Mistral). In ProductLayout einmal gemountet →
 * bleibt über Tab-Wechsel bestehen (lokaler State). Nutzt die aktuell gewählte
 * Kommune als Kontext. Einstellungen (Zahnrad) nur für Admins.
 */
export default function ChatWidget() {
  const kommune = useStore(s => s.kommune)

  const [open, setOpen] = useState(false)
  const [available, setAvailable] = useState(true)  // false → 401, Widget ausblenden
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [draft, setDraft] = useState('')
  const [streaming, setStreaming] = useState(false)
  const [usage, setUsage] = useState<AiUsage | null>(null)
  const [banner, setBanner] = useState<{ kind: 'info' | 'error'; text: string } | null>(null)

  const abortRef = useRef<AbortController | null>(null)
  const listRef = useRef<HTMLDivElement | null>(null)
  const lastKommuneId = useRef<number | null>(null)

  // Verbrauch laden (auch als Login-Check: 401 → Widget verstecken).
  const refreshUsage = () => {
    api.getAiUsage()
      .then(u => { setUsage(u); setAvailable(true) })
      .catch((e: unknown) => { if (e instanceof Error && /401/.test(e.message)) setAvailable(false) })
  }

  useEffect(() => { refreshUsage() }, [])

  // Kommune-Wechsel: dezenter Hinweis im Verlauf (Historie bleibt erhalten).
  useEffect(() => {
    if (!kommune) return
    if (lastKommuneId.current !== null && lastKommuneId.current !== kommune.id) {
      setBanner({ kind: 'info', text: `Kontext gewechselt zu ${kommune.name}.` })
    }
    lastKommuneId.current = kommune.id
  }, [kommune?.id])

  // Autoscroll ans Ende bei neuen Tokens.
  useEffect(() => {
    if (listRef.current) listRef.current.scrollTop = listRef.current.scrollHeight
  }, [messages, open])

  const quotaBlocked = usage?.blocked ?? false

  const send = async (text: string) => {
    const content = text.trim()
    if (!content || streaming) return
    setBanner(null)
    setDraft('')

    const history: ChatMessage[] = [...messages, { role: 'user', content }]
    // Platzhalter-Assistentennachricht, in die gestreamt wird.
    setMessages([...history, { role: 'assistant', content: '' }])
    setStreaming(true)

    const ctrl = new AbortController()
    abortRef.current = ctrl
    try {
      await api.chatStream(
        { messages: history, kommune_id: kommune?.id ?? null },
        {
          onToken: (t) => setMessages(prev => {
            const next = [...prev]
            const last = next[next.length - 1]
            if (last && last.role === 'assistant') next[next.length - 1] = { ...last, content: last.content + t }
            return next
          }),
          onUsage: (u) => setUsage(prev => prev ? { ...prev, day: u.day, month: u.month } : prev),
          onError: (msg) => setBanner({ kind: 'error', text: msg }),
        },
        ctrl.signal,
      )
    } catch (e) {
      if (e instanceof ChatError) {
        setBanner({ kind: 'error', text: e.message })
        // Leere Platzhalter-Antwort entfernen, wenn gar nichts kam.
        setMessages(prev => {
          const last = prev[prev.length - 1]
          return last && last.role === 'assistant' && !last.content ? prev.slice(0, -1) : prev
        })
      } else if (!(e instanceof DOMException && e.name === 'AbortError')) {
        setBanner({ kind: 'error', text: 'Die Anfrage ist fehlgeschlagen.' })
      }
    } finally {
      setStreaming(false)
      abortRef.current = null
      // Leere Assistenten-Antwort (Abbruch/Fehler ohne Token) entfernen — sonst
      // schlägt der nächste Turn serverseitig fehl (Content min. 1 Zeichen → 422).
      setMessages(prev => {
        const last = prev[prev.length - 1]
        return last && last.role === 'assistant' && !last.content ? prev.slice(0, -1) : prev
      })
      refreshUsage()
    }
  }

  const cancel = () => abortRef.current?.abort()
  const clearChat = () => { if (!streaming) { setMessages([]); setBanner(null) } }

  if (!available) return null

  return (
    <>
      {!open && (
        <button className="chat-fab" onClick={() => setOpen(true)} title="KI-Assistent öffnen" aria-label="KI-Assistent öffnen">
          <span aria-hidden>💬</span>
        </button>
      )}

      {open && (
        <div className="chat-panel" role="dialog" aria-label="KI-Assistent">
          <div className="chat-header">
            <span className="chat-title">KI-Assistent</span>
            <div className="chat-header-actions">
              <button className="chat-icon-btn" title="Verlauf leeren" onClick={clearChat} disabled={streaming || messages.length === 0}>🗑</button>
              <button className="chat-icon-btn" title="Schließen" onClick={() => setOpen(false)}>✕</button>
            </div>
          </div>

          <div className="chat-messages" ref={listRef}>
            {messages.length === 0 && (
              <div className="chat-empty">
                <p>Fragen zu den Ergebnissen{kommune ? ` von ${kommune.name}` : ''}, zu Berichtsteilen, Maßnahmen oder allgemein zu Klimafolgen und Anpassung.</p>
                <div className="chat-chips">
                  {QUICK_PROMPTS.map(p => (
                    <button key={p} className="chat-chip" onClick={() => send(p)} disabled={quotaBlocked}>{p}</button>
                  ))}
                </div>
              </div>
            )}
            {messages.map((m, i) => (
              <ChatMessageView key={i} message={m} streaming={streaming && i === messages.length - 1 && m.role === 'assistant'} />
            ))}
          </div>

          {banner && <div className={banner.kind === 'error' ? 'chat-error-banner' : 'chat-info-banner'}>{banner.text}</div>}
          {quotaBlocked && !banner && (
            <div className="chat-error-banner">Das Token-Kontingent ist erschöpft. Bitte später erneut versuchen.</div>
          )}

          <div className="chat-input-row">
            <textarea
              className="chat-textarea"
              rows={2}
              placeholder={quotaBlocked ? 'Kontingent erschöpft' : 'Nachricht…'}
              value={draft}
              disabled={quotaBlocked}
              maxLength={4000}
              onChange={e => setDraft(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(draft) } }}
            />
            {streaming ? (
              <button className="chat-send-btn chat-cancel-btn" onClick={cancel} title="Abbrechen">■</button>
            ) : (
              <button className="chat-send-btn" onClick={() => send(draft)} disabled={quotaBlocked || !draft.trim()} title="Senden">➤</button>
            )}
          </div>

          <div className="chat-footer">
            {usage && (
              <span className="chat-usage">
                Heute {fmtK(usage.day.used)}/{fmtK(usage.day.limit)} · Monat {fmtK(usage.month.used)}/{fmtK(usage.month.limit)}
              </span>
            )}
            <span className="chat-disclaimer">KI-Inhalte können Fehler enthalten – Zahlen im Dashboard prüfen.</span>
          </div>
        </div>
      )}
    </>
  )
}
