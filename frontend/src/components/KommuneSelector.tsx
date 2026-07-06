import { useState, useRef, useEffect } from 'react'
import { useStore } from '../store'
import { api } from '../api/client'
import type { KommuneSearchResult, Kommune } from '../types'

export default function KommuneSelector() {
  const { kommune, loadKommune, loadGrid, loadStatus, loadMeasures, loadConfig } = useStore()
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<KommuneSearchResult[]>([])
  const [open, setOpen] = useState(false)
  const [gebieteOpen, setGebieteOpen] = useState(false)
  const [gebiete, setGebiete] = useState<Kommune[]>([])
  const [gebieteLoading, setGebieteLoading] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const ref = useRef<HTMLDivElement>(null)
  const timerRef = useRef<ReturnType<typeof setTimeout>>(undefined)

  useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false)
        setGebieteOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClick)
    return () => document.removeEventListener('mousedown', handleClick)
  }, [])

  const doSearch = (q: string) => {
    if (q.length < 2) { setResults([]); return }
    clearTimeout(timerRef.current)
    timerRef.current = setTimeout(async () => {
      const data = await api.searchKommune(q)
      setResults(data as unknown as KommuneSearchResult[])
      setOpen(true)
      setGebieteOpen(false)
    }, 300)
  }

  const loadKommuneData = async (id: number, name: string) => {
    setLoading(true)
    setError('')
    setQuery(name)
    try {
      await loadKommune(id)
      await Promise.all([
        loadGrid(id),
        loadStatus(id),
        loadMeasures(id),
        loadConfig(id),
      ])
    } catch (e) {
      console.error('Failed to load kommune:', e)
      setError(e instanceof Error ? e.message : 'Laden fehlgeschlagen')
    } finally {
      setLoading(false)
    }
  }

  const selectResult = async (r: KommuneSearchResult) => {
    setOpen(false)
    setGebieteOpen(false)
    try {
      const k = await api.createKommune(r.osm_id, r.name, r.osm_type, r.geojson, r.address) as unknown as Kommune
      const grid = await api.getGrid(k.id) as { features?: unknown[] }
      if (!grid.features?.length) {
        await api.generateGrid(k.id)
      }
      await loadKommuneData(k.id, k.name)
    } catch (e) {
      console.error('Failed to load kommune:', e)
      setError(e instanceof Error ? e.message : 'Laden fehlgeschlagen')
      setLoading(false)
    }
  }

  const selectGebiet = async (k: Kommune) => {
    setOpen(false)
    setGebieteOpen(false)
    await loadKommuneData(k.id, k.name)
  }

  const toggleGebiete = async () => {
    const next = !gebieteOpen
    setGebieteOpen(next)
    setOpen(false)
    if (!next) return

    setGebieteLoading(true)
    setError('')
    try {
      const data = await api.listKommunen(true)
      setGebiete(data as unknown as Kommune[])
    } catch (e) {
      console.error('Failed to load gebiete:', e)
      setError(e instanceof Error ? e.message : 'Gebiete konnten nicht geladen werden')
      setGebieteOpen(false)
    } finally {
      setGebieteLoading(false)
    }
  }

  return (
    <div className="search-container" ref={ref}>
      <div className="search-row">
        <input
          type="text"
          placeholder={kommune ? kommune.name : 'Kommune suchen...'}
          value={query}
          onChange={(e) => { setQuery(e.target.value); doSearch(e.target.value) }}
          onFocus={() => results.length > 0 && setOpen(true)}
        />
        <button
          type="button"
          className="btn btn-secondary btn-sm"
          onClick={toggleGebiete}
          disabled={loading || gebieteLoading}
        >
          Meine Gebiete
        </button>
      </div>
      {loading && <span style={{ marginLeft: 8, fontSize: '0.8rem' }}>Lade Kommune...</span>}
      {error && <div style={{ color: '#e74c3c', fontSize: '0.8rem', marginTop: 4 }}>{error}</div>}
      {open && results.length > 0 && (
        <div className="search-results">
          {results.map((r, i) => (
            <div key={i} className="result-item" onClick={() => selectResult(r)}>
              <strong>{r.name}</strong>
              <br />
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                {r.display_name}
              </span>
            </div>
          ))}
        </div>
      )}
      {gebieteOpen && (
        <div className="search-results">
          {gebieteLoading && (
            <div className="result-item" style={{ cursor: 'default', color: 'var(--text-muted)' }}>
              Lade Gebiete...
            </div>
          )}
          {!gebieteLoading && gebiete.length === 0 && (
            <div className="result-item" style={{ cursor: 'default', color: 'var(--text-muted)' }}>
              Noch keine berechneten Gebiete vorhanden.
            </div>
          )}
          {!gebieteLoading && gebiete.map((k) => (
            <div key={k.id} className="result-item" onClick={() => selectGebiet(k)}>
              <strong>{k.name}</strong>
              {k.area_km2 != null && (
                <>
                  <br />
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                    {k.area_km2.toLocaleString('de-DE')} km²
                    {k.bundesland ? ` · ${k.bundesland}` : ''}
                  </span>
                </>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
