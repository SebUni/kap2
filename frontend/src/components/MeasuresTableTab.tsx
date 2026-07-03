import { useState, useMemo, useRef, useEffect } from 'react'
import { useStore } from '../store'
import { api } from '../api/client'
import type { Measure, MeasureImpactSummary } from '../types'

export default function MeasuresTableTab() {
  const { kommune, measures, catalog, loadMeasures, loadCatalog, setActiveTab, setSelectedMeasure, deleteMeasure } = useStore()
  const [filterType, setFilterType] = useState<string>('')
  const [impacts, setImpacts] = useState<Record<number, MeasureImpactSummary>>({})
  const [loadingImpacts, setLoadingImpacts] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  useEffect(() => { loadCatalog().catch(() => {}) }, [])

  const measureCat = (code: string) => catalog?.measures.find(m => m.code === code)
  const measureName = (code: string) => measureCat(code)?.name || code
  const clusterOf = (m: Measure) => measureCat(m.measure_type)?.kang_cluster || 'crosscutting'
  const clusterLabel = (code: string) => catalog?.kang_clusters.find(c => c.code === code)?.label || code
  const fieldLabel = (clusterCode: string, fieldCode?: string) =>
    catalog?.kang_clusters.find(c => c.code === clusterCode)?.fields.find(f => f.code === fieldCode)?.label || ''

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
      for (const r of results) if (r) map[r.id] = r.impact
      setImpacts(map)
    }).finally(() => setLoadingImpacts(false))
  }, [measures])

  // Cluster → Handlungsfeld → Maßnahmen (zweistufig, gefiltert nach Cluster)
  const groupedByCluster = useMemo(() => {
    const order = catalog?.kang_clusters.map(c => c.code) || []
    const list = filterType ? measures.filter(m => clusterOf(m) === filterType) : measures
    const byCluster: Record<string, Measure[]> = {}
    for (const m of list) {
      const c = clusterOf(m)
      if (!byCluster[c]) byCluster[c] = []
      byCluster[c].push(m)
    }
    return order
      .filter(c => byCluster[c]?.length)
      .map(c => ({ cluster: c, items: byCluster[c] }))
  }, [measures, filterType, catalog])

  const handleExport = () => { if (kommune) window.open(api.exportMeasuresUrl(kommune.id), '_blank') }

  const handleImport = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!kommune || !e.target.files?.[0]) return
    try {
      const result = await api.importMeasures(kommune.id, e.target.files[0])
      alert(`Import: ${result.imported} importiert, ${result.skipped} übersprungen`)
      await loadMeasures(kommune.id)
    } catch {
      alert('Import fehlgeschlagen')
    }
    e.target.value = ''
  }

  const viewOnMap = (m: Measure) => { setSelectedMeasure(m); setActiveTab(1) }
  const handleDelete = async (m: Measure) => {
    if (!confirm(`"${m.name}" wirklich löschen?`)) return
    await deleteMeasure(m.id)
  }

  const fmtCurrency = (v: number) => v.toLocaleString('de-DE', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 })

  if (!kommune) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', flex: 1, color: 'var(--text-muted)' }}>
        Bitte wählen Sie eine Kommune.
      </div>
    )
  }

  const allImpacts = Object.values(impacts)
  const sumInvest = allImpacts.reduce((s, i) => s + (i.investment_eur || 0), 0)
  const sumMaint = allImpacts.reduce((s, i) => s + (i.annual_maintenance_eur || 0), 0)
  const sumBenefit = allImpacts.reduce((s, i) => s + (i.annual_benefit_eur || 0), 0)
  const netAnnual = sumBenefit - sumMaint

  const usedClusters = [...new Set(measures.map(m => clusterOf(m)))]

  return (
    <div style={{ flex: 1, overflow: 'auto', padding: '1rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h2 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Maßnahmen-Übersicht ({measures.length})</h2>
        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
          <select value={filterType} onChange={e => setFilterType(e.target.value)}
            style={{ padding: '0.3rem 0.5rem', border: '1px solid var(--border)', borderRadius: 6, fontSize: '0.85rem' }}>
            <option value="">Alle Cluster</option>
            {usedClusters.map(c => <option key={c} value={c}>{clusterLabel(c)}</option>)}
          </select>
          <button className="btn btn-primary btn-sm" onClick={handleExport}>Export</button>
          <button className="btn btn-secondary btn-sm" onClick={() => fileInputRef.current?.click()}>Import</button>
          <input ref={fileInputRef} type="file" accept=".xlsx,.xls" onChange={handleImport} style={{ display: 'none' }} />
        </div>
      </div>

      {measures.length > 0 && (
        <div style={{ display: 'flex', gap: 12, marginBottom: 16, flexWrap: 'wrap' }}>
          <div className="kpi-card" style={{ flex: '1 1 140px' }}>
            <div className="kpi-label">Gesamtinvestition</div>
            <div className="kpi-value" style={{ fontSize: '1rem' }}>{fmtCurrency(sumInvest)}</div>
          </div>
          <div className="kpi-card" style={{ flex: '1 1 140px' }}>
            <div className="kpi-label">Unterhalt/Jahr</div>
            <div className="kpi-value" style={{ fontSize: '1rem' }}>{fmtCurrency(sumMaint)}</div>
          </div>
          <div className="kpi-card" style={{ flex: '1 1 140px' }}>
            <div className="kpi-label">Nutzen/Jahr</div>
            <div className="kpi-value success" style={{ fontSize: '1rem' }}>{fmtCurrency(sumBenefit)}</div>
          </div>
          <div className="kpi-card" style={{ flex: '1 1 140px' }}>
            <div className="kpi-label">Netto-Nutzen/Jahr</div>
            <div className="kpi-value" style={{ fontSize: '1rem', color: netAnnual >= 0 ? 'var(--success)' : 'var(--danger)' }}>
              {fmtCurrency(netAnnual)}
            </div>
          </div>
        </div>
      )}

      {loadingImpacts && <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: 8 }}>Berechne Wirkungen…</div>}

      {measures.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
          <p>Noch keine Maßnahmen angelegt.</p>
          <p style={{ fontSize: '0.85rem' }}>Wechseln Sie zur Karte und zeichnen Sie ein Gebiet, um eine Maßnahme anzulegen.</p>
        </div>
      ) : (
        groupedByCluster.map(({ cluster, items }) => (
          <div key={cluster} style={{ marginBottom: 24 }}>
            <h3 style={{ fontSize: '0.95rem', fontWeight: 700, marginBottom: 8, borderBottom: '2px solid var(--primary)', paddingBottom: 4 }}>
              {clusterLabel(cluster)} ({items.length})
            </h3>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Handlungsfeld</th>
                  <th>Typ</th>
                  <th>Jahr</th>
                  <th style={{ textAlign: 'right' }}>Anzahl</th>
                  <th style={{ textAlign: 'right' }}>Investition</th>
                  <th style={{ textAlign: 'right' }}>Unterhalt/Jahr</th>
                  <th style={{ textAlign: 'right' }}>Nutzen/Jahr</th>
                  <th style={{ textAlign: 'right' }}>Risiko-Minderung</th>
                  <th>Aktionen</th>
                </tr>
              </thead>
              <tbody>
                {items.map(m => {
                  const imp = impacts[m.id]
                  const cat = measureCat(m.measure_type)
                  return (
                    <tr key={m.id}>
                      <td style={{ fontWeight: 500 }}>{m.name}</td>
                      <td style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{fieldLabel(cluster, cat?.kang_field) || '–'}</td>
                      <td style={{ fontSize: '0.8rem' }}>{measureName(m.measure_type)}</td>
                      <td>{m.implementation_year || '–'}</td>
                      <td style={{ textAlign: 'right', fontSize: '0.85rem' }}>
                        {imp?.unit_label != null ? `${imp.count ?? '–'} ${imp.unit_label}` : '–'}
                      </td>
                      <td style={{ textAlign: 'right', fontSize: '0.85rem' }}>{imp ? fmtCurrency(imp.investment_eur || 0) : '–'}</td>
                      <td style={{ textAlign: 'right', fontSize: '0.85rem' }}>{imp ? fmtCurrency(imp.annual_maintenance_eur || 0) : '–'}</td>
                      <td style={{ textAlign: 'right', fontSize: '0.85rem', color: 'var(--success)' }}>{imp ? fmtCurrency(imp.annual_benefit_eur || 0) : '–'}</td>
                      <td style={{ textAlign: 'right', fontSize: '0.85rem', color: 'var(--success)' }}>
                        {imp?.avg_index_reduction_pct != null ? `−${imp.avg_index_reduction_pct.toFixed(1)} %` : '–'}
                      </td>
                      <td>
                        <div style={{ display: 'flex', gap: 4 }}>
                          <button className="btn btn-secondary btn-sm" onClick={() => viewOnMap(m)} title="Auf Karte zeigen">🗺</button>
                          <button className="btn btn-danger btn-sm" onClick={() => handleDelete(m)} title="Löschen" style={{ padding: '2px 6px' }}>✕</button>
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
