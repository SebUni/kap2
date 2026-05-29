import { useState, useMemo, useRef, useEffect } from 'react'
import { useStore } from '../store'
import { api } from '../api/client'
import type { Measure, MeasureImpactSummary } from '../types'

export default function MeasuresTableTab() {
  const { kommune, measures, loadMeasures, setActiveTab, setSelectedMeasure, deleteMeasure } = useStore()
  const [sortKey, setSortKey] = useState<string>('measure_type')
  const [sortDir, setSortDir] = useState<1 | -1>(1)
  const [filterType, setFilterType] = useState<string>('')
  const [impacts, setImpacts] = useState<Record<number, MeasureImpactSummary>>({})
  const [loadingImpacts, setLoadingImpacts] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const measureLabels: Record<string, string> = {
    drinking_fountain: 'Trinkbrunnen',
    green_roof: 'Dachbegrünung',
    facade_greening: 'Fassadenbegrünung',
    tree_planting: 'Baumpflanzung',
    unsealing: 'Entsiegelung',
    shade_structure: 'Verschattung',
  }

  const configLabels: Record<string, string> = {
    count: 'Anzahl',
    coverage_pct: 'Abdeckung (%)',
    area_pct: 'Flächenanteil (%)',
    shade_factor: 'Schattenfaktor',
  }

  // Load impacts for all measures
  useEffect(() => {
    if (!measures.length) return
    setLoadingImpacts(true)
    Promise.all(
      measures.map(m =>
        api.calculateImpact(m.id)
          .then(r => ({ id: m.id, impact: r as unknown as MeasureImpactSummary }))
          .catch(() => null)
      )
    ).then(results => {
      const map: Record<number, MeasureImpactSummary> = {}
      for (const r of results) {
        if (r) map[r.id] = r.impact
      }
      setImpacts(map)
    }).finally(() => setLoadingImpacts(false))
  }, [measures])

  const sorted = useMemo(() => {
    let list = [...measures]
    if (filterType) list = list.filter(m => m.measure_type === filterType)
    list.sort((a, b) => {
      const va = (a as unknown as Record<string, unknown>)[sortKey]
      const vb = (b as unknown as Record<string, unknown>)[sortKey]
      if (typeof va === 'string' && typeof vb === 'string') return va.localeCompare(vb) * sortDir
      if (typeof va === 'number' && typeof vb === 'number') return (va - vb) * sortDir
      return 0
    })
    return list
  }, [measures, sortKey, sortDir, filterType])

  // Group by type
  const grouped = useMemo(() => {
    const groups: Record<string, Measure[]> = {}
    for (const m of sorted) {
      const key = m.measure_type
      if (!groups[key]) groups[key] = []
      groups[key].push(m)
    }
    return groups
  }, [sorted])

  const toggleSort = (key: string) => {
    if (sortKey === key) setSortDir(d => (d === 1 ? -1 : 1) as 1 | -1)
    else { setSortKey(key); setSortDir(1) }
  }

  const handleExport = () => {
    if (!kommune) return
    window.open(api.exportMeasuresUrl(kommune.id), '_blank')
  }

  const handleImport = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!kommune || !e.target.files?.[0]) return
    try {
      const result = await api.importMeasures(kommune.id, e.target.files[0])
      alert(`Import: ${result.imported} importiert, ${result.skipped} übersprungen`)
      await loadMeasures(kommune.id)
    } catch (err) {
      alert('Import fehlgeschlagen')
    }
    e.target.value = ''
  }

  const viewOnMap = (m: Measure) => {
    setSelectedMeasure(m)
    setActiveTab(0)
  }

  const handleDelete = async (m: Measure) => {
    if (!confirm(`"${m.name}" wirklich löschen?`)) return
    await deleteMeasure(m.id)
  }

  const fmtCurrency = (v: number) =>
    v.toLocaleString('de-DE', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 })

  const totalCosts = (imp: MeasureImpactSummary | undefined) => {
    if (!imp?.total_costs) return null
    return Object.values(imp.total_costs).reduce((a, b) => a + b, 0)
  }

  const totalSavings = (imp: MeasureImpactSummary | undefined) => {
    if (!imp?.total_savings) return null
    return Object.values(imp.total_savings).reduce((a, b) => a + b, 0)
  }

  const tempDelta = (imp: MeasureImpactSummary | undefined) => {
    if (!imp?.total_indicator_deltas) return null
    return imp.total_indicator_deltas.temperature_estimate ?? null
  }

  if (!kommune) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', flex: 1, color: 'var(--text-muted)' }}>
        Bitte wählen Sie eine Kommune.
      </div>
    )
  }

  // Summary KPIs
  const allImpacts = Object.values(impacts)
  const sumCosts = allImpacts.reduce((s, i) => s + (totalCosts(i) || 0), 0)
  const sumSavings = allImpacts.reduce((s, i) => s + (totalSavings(i) || 0), 0)
  const sumTempDelta = allImpacts.reduce((s, i) => s + (tempDelta(i) || 0), 0)
  const avgTempDelta = allImpacts.length ? sumTempDelta / allImpacts.length : 0

  return (
    <div style={{ flex: 1, overflow: 'auto', padding: '1rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h2 style={{ fontSize: '1.1rem', fontWeight: 600 }}>
          Maßnahmen-Übersicht ({measures.length})
        </h2>
        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
          <select
            value={filterType}
            onChange={e => setFilterType(e.target.value)}
            style={{ padding: '0.3rem 0.5rem', border: '1px solid var(--border)', borderRadius: 6, fontSize: '0.85rem' }}
          >
            <option value="">Alle Typen</option>
            {Object.entries(measureLabels).map(([k, v]) => (
              <option key={k} value={k}>{v}</option>
            ))}
          </select>
          <button className="btn btn-primary btn-sm" onClick={handleExport}>Export</button>
          <button className="btn btn-secondary btn-sm" onClick={() => fileInputRef.current?.click()}>Import</button>
          <input ref={fileInputRef} type="file" accept=".xlsx,.xls" onChange={handleImport} style={{ display: 'none' }} />
        </div>
      </div>

      {/* Summary KPIs */}
      {measures.length > 0 && (
        <div style={{ display: 'flex', gap: 12, marginBottom: 16, flexWrap: 'wrap' }}>
          <div className="kpi-card" style={{ flex: '1 1 140px' }}>
            <div className="kpi-label">Gesamtkosten</div>
            <div className="kpi-value" style={{ fontSize: '1rem' }}>{fmtCurrency(sumCosts)}</div>
          </div>
          <div className="kpi-card" style={{ flex: '1 1 140px' }}>
            <div className="kpi-label">Jährl. Einsparungen</div>
            <div className="kpi-value success" style={{ fontSize: '1rem' }}>{fmtCurrency(sumSavings)}</div>
          </div>
          <div className="kpi-card" style={{ flex: '1 1 140px' }}>
            <div className="kpi-label">⌀ Temp.-Minderung</div>
            <div className="kpi-value" style={{ fontSize: '1rem', color: avgTempDelta < 0 ? 'var(--success)' : 'var(--danger)' }}>
              {avgTempDelta > 0 ? '+' : ''}{avgTempDelta.toFixed(2)} °C
            </div>
          </div>
          <div className="kpi-card" style={{ flex: '1 1 140px' }}>
            <div className="kpi-label">Amortisation</div>
            <div className="kpi-value" style={{ fontSize: '1rem' }}>
              {sumSavings > 0 ? `~${Math.ceil(sumCosts / sumSavings)} Jahre` : '–'}
            </div>
          </div>
        </div>
      )}

      {loadingImpacts && (
        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: 8 }}>Berechne Wirkungen…</div>
      )}

      {measures.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
          <p>Noch keine Maßnahmen angelegt.</p>
          <p style={{ fontSize: '0.85rem' }}>
            Wechseln Sie zur Karte und zeichnen Sie ein Gebiet, um eine Maßnahme anzulegen.
          </p>
        </div>
      ) : (
        Object.entries(grouped).map(([typeKey, typeMeasures]) => (
          <div key={typeKey} style={{ marginBottom: 20 }}>
            <h3 style={{ fontSize: '0.9rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: 6, borderBottom: '1px solid var(--border)', paddingBottom: 4 }}>
              {measureLabels[typeKey] || typeKey} ({typeMeasures.length})
            </h3>
            <table className="data-table">
              <thead>
                <tr>
                  <th onClick={() => toggleSort('name')} style={{ cursor: 'pointer' }}>Name</th>
                  <th onClick={() => toggleSort('implementation_year')} style={{ cursor: 'pointer' }}>Jahr</th>
                  <th>Parameter</th>
                  <th style={{ textAlign: 'right' }}>Kosten</th>
                  <th style={{ textAlign: 'right' }}>Einspar./Jahr</th>
                  <th style={{ textAlign: 'right' }}>Temp. Δ</th>
                  <th>Aktionen</th>
                </tr>
              </thead>
              <tbody>
                {typeMeasures.map(m => {
                  const imp = impacts[m.id]
                  const cost = totalCosts(imp)
                  const sav = totalSavings(imp)
                  const td = tempDelta(imp)
                  return (
                    <tr key={m.id}>
                      <td style={{ fontWeight: 500 }}>{m.name}</td>
                      <td>{m.implementation_year || '–'}</td>
                      <td style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                        {Object.entries(m.config || {}).map(([k, v]) =>
                          `${configLabels[k] || k}: ${v}`
                        ).join(', ')}
                      </td>
                      <td style={{ textAlign: 'right', fontSize: '0.85rem' }}>
                        {cost != null ? fmtCurrency(cost) : '–'}
                      </td>
                      <td style={{ textAlign: 'right', fontSize: '0.85rem', color: 'var(--success)' }}>
                        {sav != null ? fmtCurrency(sav) : '–'}
                      </td>
                      <td style={{ textAlign: 'right', fontSize: '0.85rem', color: td != null && td < 0 ? 'var(--success)' : td != null && td > 0 ? 'var(--danger)' : undefined }}>
                        {td != null ? `${td > 0 ? '+' : ''}${td.toFixed(2)}°C` : '–'}
                      </td>
                      <td>
                        <div style={{ display: 'flex', gap: 4 }}>
                          <button className="btn btn-secondary btn-sm" onClick={() => viewOnMap(m)} title="Auf Karte zeigen">
                            🗺
                          </button>
                          <button
                            className="btn btn-danger btn-sm"
                            onClick={() => handleDelete(m)}
                            title="Löschen"
                            style={{ padding: '2px 6px' }}
                          >
                            ✕
                          </button>
                        </div>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        ))
      )}
    </div>
  )
}
