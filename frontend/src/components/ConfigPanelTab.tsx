import { useState, useEffect } from 'react'
import { useStore } from '../store'
import { api } from '../api/client'
import type { ModelParameter } from '../types'
import ParameterTable from './ParameterTable'

export default function ConfigPanelTab() {
  const { kommune, catalog, status, loadStatus } = useStore()
  const [parameters, setParameters] = useState<ModelParameter[]>([])
  const [loading, setLoading] = useState(false)

  const loadParameters = async () => {
    if (!kommune) return
    setLoading(true)
    try {
      const res = await api.getParameters(kommune.id)
      setParameters(res as unknown as ModelParameter[])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (kommune) {
      loadParameters()
      loadStatus(kommune.id)
    }
  }, [kommune?.id])

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
    <div style={{ flex: 1, overflow: 'auto', padding: '1.5rem', maxWidth: 960, margin: '0 auto' }}>
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
      {!loading && (
        <ParameterTable
          kommuneId={kommune.id}
          parameters={parameters}
          onUpdated={loadParameters}
          grouped
          catalog={catalog ?? undefined}
          showExport={false}
        />
      )}
    </div>
  )
}
