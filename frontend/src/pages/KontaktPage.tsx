import { useState } from 'react'
import InlineSpinner from '../components/InlineSpinner'

export default function KontaktPage() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [organisation, setOrganisation] = useState('')
  const [message, setMessage] = useState('')
  const [busy, setBusy] = useState(false)
  const [done, setDone] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setBusy(true)
    try {
      const res = await fetch('/api/public/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, organisation, message }),
      })
      if (!res.ok) {
        const body = await res.json().catch(() => null)
        throw new Error(body?.detail || `Fehler ${res.status}`)
      }
      setDone(true)
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err))
    } finally {
      setBusy(false)
    }
  }

  if (done) {
    return (
      <div className="login-page">
        <div className="login-card" style={{ textAlign: 'center' }}>
          <h2>Vielen Dank!</h2>
          <p style={{ color: 'var(--text-muted)', marginTop: '0.75rem' }}>
            Ihre Anfrage ist eingegangen — wir melden uns zeitnah für ein
            unverbindliches Beratungsgespräch.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="login-page">
      <form className="login-card kontakt-card" onSubmit={handleSubmit}>
        <h2>Beratungsgespräch vereinbaren</h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '1rem' }}>
          Erzählen Sie uns kurz, für welche Kommune oder welches Mandat Sie
          planen — wir zeigen KAP2 gern an Ihrem konkreten Fall.
        </p>
        <label className="login-label">
          Name
          <input value={name} onChange={(e) => setName(e.target.value)} required minLength={2} />
        </label>
        <label className="login-label">
          E-Mail
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>
        <label className="login-label">
          Kommune / Büro (optional)
          <input value={organisation} onChange={(e) => setOrganisation(e.target.value)} />
        </label>
        <label className="login-label">
          Nachricht
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            required
            minLength={5}
            rows={5}
          />
        </label>
        {error && <div className="login-error">{error}</div>}
        <button type="submit" className="btn-primary login-submit" disabled={busy}>
          {busy ? <><InlineSpinner /> Senden …</> : 'Anfrage senden'}
        </button>
      </form>
    </div>
  )
}
