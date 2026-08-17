import { useEffect, useState } from 'react'
import { api, type AiSettings, type AiUsage } from '../../api/client'
import InlineSpinner from '../../components/InlineSpinner'

function fmt(n: number): string {
  return n.toLocaleString('de-DE')
}

/**
 * Admin-Konfiguration des KI-Assistenten (Mistral): API-Schlüssel (write-only),
 * Token-Limits (Tag/Monat) und aktueller Verbrauch. Das Modell wird serverseitig
 * gesetzt und hier bewusst nicht als Nutzer-Auswahl angeboten.
 */
export default function AiConfigTab() {
  const [settings, setSettings] = useState<AiSettings | null>(null)
  const [usage, setUsage] = useState<AiUsage | null>(null)
  const [apiKey, setApiKey] = useState('')
  const [daily, setDaily] = useState('')
  const [monthly, setMonthly] = useState('')
  const [busy, setBusy] = useState(false)
  const [msg, setMsg] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const load = () => {
    Promise.all([api.getAiSettings(), api.getAiUsage()])
      .then(([s, u]) => {
        setSettings(s)
        setUsage(u)
        setDaily(String(s.daily_token_limit))
        setMonthly(String(s.monthly_token_limit))
      })
      .catch(() => setError('Einstellungen konnten nicht geladen werden.'))
  }

  useEffect(() => { load() }, [])

  const save = async () => {
    setBusy(true); setError(null); setMsg(null)
    try {
      const payload: Record<string, unknown> = {}
      if (apiKey.trim()) payload.api_key = apiKey.trim()  // nur bei Eingabe senden
      const d = parseInt(daily, 10)
      const m = parseInt(monthly, 10)
      if (!Number.isNaN(d)) payload.daily_token_limit = d
      if (!Number.isNaN(m)) payload.monthly_token_limit = m
      const updated = await api.updateAiSettings(payload)
      setSettings(updated)
      setApiKey('')
      setMsg('Gespeichert.')
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Speichern fehlgeschlagen.')
    } finally { setBusy(false) }
  }

  if (!settings) return <InlineSpinner />

  return (
    <div className="admin-tab">
      <div className="admin-tab-head"><h2>KI-Assistent</h2></div>
      <p className="admin-stand">
        Anbieter: Mistral AI (EU-Hosting). Modell serverseitig: {settings.model}.
      </p>

      <label className="admin-field">Mistral-API-Schlüssel
        <input
          type="password"
          autoComplete="off"
          placeholder={settings.api_key_set ? `Gespeichert: …${settings.api_key_hint ?? ''}` : 'Noch kein Schlüssel hinterlegt'}
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
        />
      </label>
      <p className="admin-stand">
        Wird serverseitig gespeichert und nie wieder angezeigt. Leer lassen, um den
        gespeicherten Schlüssel unverändert zu lassen. Schlüssel unter console.mistral.ai erstellen.
      </p>

      <div className="admin-field-row">
        <label className="admin-field">Tageslimit (Tokens)
          <input type="number" min={0} value={daily} onChange={(e) => setDaily(e.target.value)} />
        </label>
        <label className="admin-field">Monatslimit (Tokens)
          <input type="number" min={0} value={monthly} onChange={(e) => setMonthly(e.target.value)} />
        </label>
      </div>

      {usage && (
        <p className="admin-stand">
          Aktueller Verbrauch — heute: {fmt(usage.day.used)} / {fmt(usage.day.limit)} ·
          Monat: {fmt(usage.month.used)} / {fmt(usage.month.limit)}
        </p>
      )}

      <p className="admin-stand">
        Der an Mistral übermittelte Datenkontext enthält nur aggregierte
        Kommunalstatistik, keine personenbezogenen Daten.
      </p>

      {error && <div className="login-error">{error}</div>}
      {msg && <div className="admin-notice">{msg}</div>}
      <div className="admin-modal-actions">
        <button className="btn-primary" onClick={save} disabled={busy}>
          {busy ? <InlineSpinner /> : 'Speichern'}
        </button>
      </div>
    </div>
  )
}
