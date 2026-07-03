import { useState, useEffect, useCallback } from 'react'
import { useStore } from '../store'
import { api } from '../api/client'
import type { ModelParameter } from '../types'
import ParameterTable from './ParameterTable'

export default function ConfigPanelTab() {
  const {
    kommune, catalog, status, loadStatus, loadCatalog,
    configPanelRequested, configScrollAnchor,
  } = useStore()
  const [parameters, setParameters] = useState<ModelParameter[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const loadParameters = useCallback(async () => {
    if (!kommune) return
    setLoading(true)
    setError(null)
    try {
      const res = await api.getParameters(kommune.id)
      setParameters(res as unknown as ModelParameter[])
    } catch (err) {
      setParameters([])
      setError(err instanceof Error ? err.message : 'Parameter konnten nicht geladen werden')
    } finally {
      setLoading(false)
    }
  }, [kommune?.id])

  useEffect(() => {
    loadCatalog().catch(() => {})
  }, [loadCatalog])

  useEffect(() => {
    if (kommune) {
      loadParameters()
      loadStatus(kommune.id)
    }
  }, [kommune?.id, loadParameters, loadStatus])

  if (!kommune) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', flex: 1, color: 'var(--text-muted)' }}>
        Bitte wählen Sie eine Kommune.
      </div>
    )
  }

  const heatStatus = status
  const isReady = heatStatus?.status === 'done'
  const isRunning = heatStatus?.status === 'running'

  return (
    <div className="kap-config-panel">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h2 style={{ fontSize: '1.1rem', fontWeight: 600, margin: 0 }}>Konfiguration</h2>
        <a
          className="btn btn-secondary"
          href={api.exportParametersUrl(kommune.id)}
          download
          style={{ fontSize: '0.8rem', textDecoration: 'none' }}
        >
          Parameter exportieren (xlsx)
        </a>
      </div>

      <div className="card" style={{ marginBottom: '1.5rem', borderColor: isReady ? 'var(--success)' : isRunning ? 'var(--primary)' : 'var(--warning)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h3 style={{ fontSize: '0.9rem', fontWeight: 600, marginBottom: 4 }}>Projektstatus</h3>
            <span className={`status-badge ${heatStatus?.status || 'pending'}`}>
              {isReady ? '✓ Startklar – Anpassungen können modelliert werden' :
               isRunning ? `⟳ Berechnung läuft: ${heatStatus?.progress_pct?.toFixed(0)}%` :
               heatStatus?.status === 'error' ? `✕ Fehler: ${heatStatus?.message}` :
               '○ Berechnung ausstehend'}
            </span>
          </div>
          <div style={{ fontSize: '2rem' }}>
            {isReady ? '🟢' : isRunning ? '🔵' : '🟡'}
          </div>
        </div>
        {isRunning && (
          <div className="progress-bar" style={{ marginTop: 8 }}>
            <div className="fill" style={{ width: `${heatStatus?.progress_pct || 0}%` }} />
          </div>
        )}
      </div>

      {loading && <p style={{ color: 'var(--text-muted)' }}>Parameter werden geladen …</p>}
      {error && !loading && (
        <div className="kap-param-error" style={{ marginBottom: '1rem' }}>
          {error}
          <button
            type="button"
            className="btn btn-secondary"
            style={{ marginLeft: 8, fontSize: '0.75rem', padding: '2px 8px' }}
            onClick={() => loadParameters()}
          >
            Erneut laden
          </button>
        </div>
      )}
      {!loading && (
        <ParameterTable
          kommuneId={kommune.id}
          parameters={parameters}
          onUpdated={loadParameters}
          grouped
          catalog={catalog ?? undefined}
          showExport={false}
          scrollAnchor={configScrollAnchor}
          scrollTrigger={configPanelRequested}
        />
      )}
    </div>
  )
}
