import { useState, useEffect, useCallback } from 'react'
import { useStore } from '../store'
import { api } from '../api/client'
import type { ModelParameter } from '../types'
import ParameterTable from './ParameterTable'
import ProjectStatusPanel from './dashboard/ProjectStatusPanel'

export default function ConfigPanelTab() {
  const {
    kommune, catalog, status, loadStatus, loadCatalog,
    configPanelRequested, configScrollAnchor, setShowConfig, demoMode,
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

  const isReady = status?.status === 'done'

  return (
    <div className="kap-config-panel">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h2 style={{ fontSize: '1.1rem', fontWeight: 600, margin: 0 }}>
          {demoMode ? 'Parameter (Demo — schreibgeschützt)' : 'Konfiguration'}
        </h2>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          {!demoMode && (
            <a
              className="btn btn-secondary"
              href={api.exportParametersUrl(kommune.id)}
              download
              style={{ fontSize: '0.8rem', textDecoration: 'none' }}
            >
              Parameter exportieren (xlsx)
            </a>
          )}
          <button
            className="btn btn-primary"
            style={{ fontSize: '0.8rem' }}
            disabled={!isReady}
            title={isReady
              ? 'Zur Auswertung wechseln'
              : 'Erst verfügbar, wenn die Berechnung abgeschlossen ist'}
            onClick={() => setShowConfig(false)}
          >
            Schließen
          </button>
        </div>
      </div>

      {demoMode ? (
        <div className="demo-banner" style={{ marginBottom: '1rem' }}>
          🔒 Parameter sind in der Demo gesperrt und können nur in der
          Vollversion angepasst werden. Für gesperrte Ebenen sind Wert und
          Quelle ausgeblendet.
        </div>
      ) : (
        <ProjectStatusPanel />
      )}

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
