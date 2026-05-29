import { useState, useRef, useEffect } from 'react'
import { useStore } from '../store'
import { api } from '../api/client'
import type { KommuneSearchResult, Kommune } from '../types'

export default function KommuneSelector() {
  const { kommune, setKommune, loadGrid, loadStatuses, loadMeasures, loadConfig } = useStore()
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<KommuneSearchResult[]>([])
  const [open, setOpen] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const ref = useRef<HTMLDivElement>(null)
  const timerRef = useRef<ReturnType<typeof setTimeout>>(undefined)

  useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false)
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
    }, 300)
  }

  const selectResult = async (r: KommuneSearchResult) => {
    setOpen(false)
    setLoading(true)
    setError('')
    setQuery(r.name)
    try {
      const k = await api.createKommune(r.osm_id, r.name, r.osm_type, r.geojson) as unknown as Kommune
      setKommune(k)
      // Auto-generate grid + load data
      try {
        await api.generateGrid(k.id)
      } catch {
        // grid may already exist
      }
      await Promise.all([
        loadGrid(k.id),
        loadStatuses(k.id),
        loadMeasures(k.id),
        loadConfig(k.id),
      ])
    } catch (e) {
      console.error('Failed to load kommune:', e)
      setError(e instanceof Error ? e.message : 'Laden fehlgeschlagen')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="search-container" ref={ref}>
      <input
        type="text"
        placeholder={kommune ? kommune.name : 'Kommune suchen...'}
        value={query}
        onChange={(e) => { setQuery(e.target.value); doSearch(e.target.value) }}
        onFocus={() => results.length > 0 && setOpen(true)}
      />
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
    </div>
  )
}
