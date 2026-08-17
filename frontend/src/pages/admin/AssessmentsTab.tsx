import { useEffect, useState, useCallback } from 'react'
import { api } from '../../api/client'
import InlineSpinner from '../../components/InlineSpinner'

interface KommuneRow { id: number; name: string; bundesland?: string; area_km2?: number }
interface SearchHit { osm_id: string; display_name: string; name: string; osm_type?: string; geojson?: Record<string, unknown>; address?: Record<string, string> }

export default function AssessmentsTab() {
  const [kommunen, setKommunen] = useState<KommuneRow[]>([])
  const [statuses, setStatuses] = useState<Record<number, { status: string; progress_pct?: number }>>({})
  const [search, setSearch] = useState('')
  const [hits, setHits] = useState<SearchHit[]>([])
  const [busy, setBusy] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    const list = await api.listKommunen() as unknown as KommuneRow[]
    setKommunen(list)
    const st: Record<number, { status: string; progress_pct?: number }> = {}
    await Promise.all(list.map(async (k) => {
      try { st[k.id] = await api.getStatus(k.id) as unknown as { status: string; progress_pct?: number } } catch { /* keine */ }
    }))
    setStatuses(st)
  }, [])

  useEffect(() => { load() }, [load])

  // Laufende Berechnungen pollen
  useEffect(() => {
    const running = Object.entries(statuses).some(([, s]) => s.status === 'running' || s.status === 'queued')
    if (!running) return
    const t = setInterval(load, 2000)
    return () => clearInterval(t)
  }, [statuses, load])

  useEffect(() => {
    if (search.length < 3) { setHits([]); return }
    const t = setTimeout(async () => {
      try { setHits(await api.searchKommune(search) as unknown as SearchHit[]) } catch { setHits([]) }
    }, 400)
    return () => clearTimeout(t)
  }, [search])

  const createAndPrepare = async (hit: SearchHit) => {
    setBusy(hit.osm_id); setError(null)
    try {
      const k = await api.createKommune(hit.osm_id, hit.name, hit.osm_type, hit.geojson, hit.address) as unknown as { id: number }
      await api.generateGrid(k.id)
      setSearch(''); setHits([])
      await load()
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
    } finally { setBusy(null) }
  }

  const trigger = async (id: number) => {
    setBusy(String(id)); setError(null)
    try { await api.startAssessment(id); await load() }
    catch (e) { setError(e instanceof Error ? e.message : String(e)) }
    finally { setBusy(null) }
  }

  const abort = async (id: number) => {
    try { await api.abortAssessment(id); await load() } catch { /* */ }
  }

  return (
    <div className="admin-tab">
      <div className="admin-tab-head"><h2>Berechnungen (100m-Raster)</h2></div>
      <div className="admin-search">
        <input placeholder="Kommune per OSM suchen (anlegen & Grid erzeugen)…" value={search}
          onChange={(e) => setSearch(e.target.value)} />
        {hits.length > 0 && (
          <div className="admin-hits">
            {hits.map((h) => (
              <button key={h.osm_id} onClick={() => createAndPrepare(h)} disabled={busy === h.osm_id}>
                {busy === h.osm_id ? <InlineSpinner /> : h.display_name}
              </button>
            ))}
          </div>
        )}
      </div>
      {error && <div className="login-error">{error}</div>}
      <table className="admin-table">
        <thead><tr><th>Kommune</th><th>Bundesland</th><th>Status</th><th></th></tr></thead>
        <tbody>
          {kommunen.map((k) => {
            const s = statuses[k.id]
            const running = s?.status === 'running' || s?.status === 'queued'
            return (
              <tr key={k.id}>
                <td>{k.name}</td>
                <td>{k.bundesland ?? '—'}</td>
                <td>
                  {s ? (
                    <span className={`status-badge ${s.status === 'done' ? 'done' : running ? 'running' : s.status === 'error' ? 'error' : 'pending'}`}>
                      {s.status === 'done' ? 'fertig' : running ? `läuft ${Math.round(s.progress_pct ?? 0)}%` : s.status}
                    </span>
                  ) : <span className="status-badge pending">keine</span>}
                </td>
                <td>
                  {running ? (
                    <button className="btn-secondary" onClick={() => abort(k.id)}>Abbrechen</button>
                  ) : (
                    <button className="btn-primary" onClick={() => trigger(k.id)} disabled={busy === String(k.id)}>
                      {s?.status === 'done' ? 'Neu berechnen' : 'Berechnen'}
                    </button>
                  )}
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}
