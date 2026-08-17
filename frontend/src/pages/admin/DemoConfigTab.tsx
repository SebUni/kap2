import { useEffect, useState } from 'react'
import { api, type DemoConfig } from '../../api/client'
import InlineSpinner from '../../components/InlineSpinner'

interface KommuneRow { id: number; name: string }

export default function DemoConfigTab() {
  const [cfg, setCfg] = useState<DemoConfig | null>(null)
  const [kommunen, setKommunen] = useState<KommuneRow[]>([])
  const [kommuneId, setKommuneId] = useState<number | ''>('')
  const [risks, setRisks] = useState<string[]>([])
  const [limit, setLimit] = useState(10)
  const [ttl, setTtl] = useState(24)
  const [busy, setBusy] = useState(false)
  const [msg, setMsg] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    (async () => {
      const c = await api.admin.getDemoConfig()
      setCfg(c)
      setKommuneId(c.kommune_id ?? '')
      setRisks(c.risk_codes)
      setLimit(c.measure_limit)
      setTtl(c.session_ttl_h)
      try { setKommunen(await api.listKommunen(true) as unknown as KommuneRow[]) } catch { /* */ }
    })()
  }, [])

  const toggleRisk = (code: string) => {
    setRisks((cur) => cur.includes(code) ? cur.filter((c) => c !== code)
      : cur.length < 3 ? [...cur, code] : cur)
  }

  const save = async () => {
    setBusy(true); setError(null); setMsg(null)
    try {
      await api.admin.updateDemoConfig({
        kommune_id: kommuneId || null, risk_codes: risks,
        measure_limit: limit, session_ttl_h: ttl,
      })
      setMsg('Gespeichert.')
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
    } finally { setBusy(false) }
  }

  if (!cfg) return <InlineSpinner />

  return (
    <div className="admin-tab">
      <div className="admin-tab-head"><h2>Demo-Kommune</h2></div>
      <p className="admin-stand">Aktive Demo-Sitzungen: {cfg.active_sessions}</p>

      <label className="admin-field">Demo-Kommune (nur mit fertiger Berechnung)
        <select value={kommuneId} onChange={(e) => setKommuneId(e.target.value ? Number(e.target.value) : '')}>
          <option value="">— wählen —</option>
          {kommunen.map((k) => <option key={k.id} value={k.id}>{k.name}</option>)}
        </select>
      </label>

      <div className="admin-field">Demo-Risiken (genau 3) — {risks.length}/3 gewählt
        <div className="admin-risk-grid">
          {cfg.risk_options.map((r) => (
            <label key={r.code} className={`admin-risk-opt${risks.includes(r.code) ? ' active' : ''}`}>
              <input type="checkbox" checked={risks.includes(r.code)}
                disabled={!risks.includes(r.code) && risks.length >= 3}
                onChange={() => toggleRisk(r.code)} />
              {r.name}
            </label>
          ))}
        </div>
      </div>

      <div className="admin-field-row">
        <label className="admin-field">Maßnahmen-Limit / Sitzung
          <input type="number" min={1} max={50} value={limit} onChange={(e) => setLimit(Number(e.target.value))} />
        </label>
        <label className="admin-field">Session-TTL (Stunden)
          <input type="number" min={1} max={168} value={ttl} onChange={(e) => setTtl(Number(e.target.value))} />
        </label>
      </div>

      {error && <div className="login-error">{error}</div>}
      {msg && <div className="admin-notice">{msg}</div>}
      <div className="admin-modal-actions">
        <button className="btn-secondary" onClick={() => api.admin.cleanupDemo().then((r) => setMsg(`${r.removed} abgelaufene Sitzungen entfernt.`))}>
          Jetzt aufräumen
        </button>
        <button className="btn-primary" onClick={save} disabled={busy || risks.length !== 3}>
          {busy ? <InlineSpinner /> : 'Speichern'}
        </button>
      </div>
    </div>
  )
}
