import { useEffect, useState, useCallback } from 'react'
import { api, type LiteBatchRun } from '../../api/client'
import InlineSpinner from '../../components/InlineSpinner'

const BUNDESLAENDER = [
  'Baden-Württemberg', 'Bayern', 'Berlin', 'Brandenburg', 'Bremen', 'Hamburg',
  'Hessen', 'Mecklenburg-Vorpommern', 'Niedersachsen', 'Nordrhein-Westfalen',
  'Rheinland-Pfalz', 'Saarland', 'Sachsen', 'Sachsen-Anhalt',
  'Schleswig-Holstein', 'Thüringen',
]

export default function LiteBatchTab() {
  const [runs, setRuns] = useState<LiteBatchRun[]>([])
  const [bundesland, setBundesland] = useState('')
  const [forceZensus, setForceZensus] = useState(false)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    try { setRuns(await api.admin.listLiteBatches()) } catch { /* */ }
  }, [])
  useEffect(() => { load() }, [load])

  const active = runs.find((r) => r.status === 'running' || r.status === 'pending')
  useEffect(() => {
    if (!active) return
    const t = setInterval(load, 2000)
    return () => clearInterval(t)
  }, [active, load])

  const start = async () => {
    setBusy(true); setError(null)
    try {
      await api.admin.startLiteBatch({ bundesland: bundesland || null, force_zensus: forceZensus })
      await load()
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
    } finally { setBusy(false) }
  }

  const last = runs.find((r) => r.status === 'done')

  return (
    <div className="admin-tab">
      <div className="admin-tab-head"><h2>Deutschland-Batch (Gemeinde-Grobkarte)</h2></div>
      {last && (
        <p className="admin-stand">
          Stand: Batch #{last.id} · {last.total.toLocaleString('de-DE')} Gemeinden ·
          {' '}{last.finished_at?.slice(0, 10)}
        </p>
      )}

      <div className="admin-batch-controls">
        <label className="admin-field">Bundesland-Filter (leer = ganz Deutschland)
          <select value={bundesland} onChange={(e) => setBundesland(e.target.value)}>
            <option value="">Ganz Deutschland</option>
            {BUNDESLAENDER.map((b) => <option key={b} value={b}>{b}</option>)}
          </select>
        </label>
        <label className="admin-check">
          <input type="checkbox" checked={forceZensus} onChange={(e) => setForceZensus(e.target.checked)} />
          Zensus neu aggregieren
        </label>
        <button className="btn-primary" onClick={start} disabled={busy || !!active}>
          {busy ? <InlineSpinner /> : '▶ Neuen Lauf starten'}
        </button>
      </div>
      {error && <div className="login-error">{error}</div>}

      {active && (
        <div className="admin-batch-progress">
          <div className="admin-batch-phase">{active.phase} — {active.message}</div>
          <div className="admin-progressbar"><div style={{ width: `${active.progress_pct}%` }} /></div>
          <div className="admin-batch-meta">
            {active.processed.toLocaleString('de-DE')} / {active.total.toLocaleString('de-DE')} ·
            {' '}{Math.round(active.progress_pct)}%
            <button className="btn-secondary" onClick={() => api.admin.abortLiteBatch(active.id).then(load)}>
              Abbrechen
            </button>
          </div>
        </div>
      )}

      <h3 className="admin-subhead">Historie</h3>
      <table className="admin-table">
        <thead><tr><th>#</th><th>Start</th><th>Status</th><th>Gemeinden</th><th>Filter</th></tr></thead>
        <tbody>
          {runs.map((r) => (
            <tr key={r.id}>
              <td>{r.id}</td>
              <td>{r.started_at?.slice(0, 16).replace('T', ' ')}</td>
              <td><span className={`status-badge ${r.status === 'done' ? 'done' : r.status === 'error' ? 'error' : r.status === 'running' ? 'running' : 'pending'}`}>{r.status}</span></td>
              <td>{r.total || '—'}</td>
              <td>{r.params?.bundesland ?? 'DE'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
