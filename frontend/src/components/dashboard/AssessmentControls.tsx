import { useState, useEffect } from 'react'
import { useStore } from '../../store'
import { CLIMATE_TYPE_META } from '../../types'
import type { AssessmentStatus, StepHistoryEntry, ClimateTypeInfo } from '../../types'

interface Props {
  /** If set, controls only this type (no dropdown). null = overview mode with "Alle berechnen". */
  climateType?: string | null
  /** Show the "Alle berechnen" button (overview mode) */
  showAllButton?: boolean
}

export default function AssessmentControls({ climateType, showAllButton }: Props) {
  const {
    kommune, statuses, assessmentLevel, setAssessmentLevel,
    activeClimateType,
    loadStatuses, loadAssessment, startAssessment, abortAssessment,
    loadRiskSummary, loadRiskZones, startAllAssessments, allRunning,
    loadAllAssessments,
  } = useStore()
  const [polling, setPolling] = useState(false)
  const [allPolling, setAllPolling] = useState(false)
  const [stepsExpanded, setStepsExpanded] = useState(false)
  const [climateTypeDefs, setClimateTypeDefs] = useState<ClimateTypeInfo[]>([])

  const effectiveType = climateType ?? activeClimateType

  // Load climate types from API
  useEffect(() => {
    import('../../api/client').then(({ api }) =>
      api.getClimateTypes().then(data =>
        setClimateTypeDefs(data as unknown as ClimateTypeInfo[])
      )
    ).catch(() => {})
  }, [])

  const currentStatus = statuses.find(
    s => s.climate_type === effectiveType && s.level === assessmentLevel
  ) as AssessmentStatus | undefined

  const formatDuration = (seconds: number): string => {
    if (seconds < 60) return `${Math.round(seconds)}s`
    const m = Math.floor(seconds / 60)
    const s = Math.round(seconds % 60)
    return s > 0 ? `${m}:${String(s).padStart(2, '0')} min` : `${m} min`
  }

  const stepDuration = (step: StepHistoryEntry): string | null => {
    if (!step.started || !step.finished) return null
    const d = (new Date(step.finished).getTime() - new Date(step.started).getTime()) / 1000
    return formatDuration(d)
  }

  // Auto-poll single type
  useEffect(() => {
    if (currentStatus?.status === 'running' && !polling) setPolling(true)
  }, [currentStatus?.status])

  useEffect(() => {
    if (!kommune || !polling) return
    const iv = setInterval(async () => {
      await loadStatuses(kommune.id)
      const st = useStore.getState().statuses.find(
        s => s.climate_type === effectiveType && s.level === assessmentLevel
      )
      if (st && (st.status === 'done' || st.status === 'error')) {
        setPolling(false)
        if (st.status === 'done') {
          await loadAssessment(kommune.id, effectiveType)
          loadRiskSummary(kommune.id).catch(() => {})
          loadRiskZones(kommune.id, effectiveType).catch(() => {})
        }
      }
    }, 500)
    return () => clearInterval(iv)
  }, [kommune, polling, effectiveType, assessmentLevel])

  // Auto-poll "Alle" mode
  useEffect(() => {
    if (allRunning && !allPolling) setAllPolling(true)
  }, [allRunning])

  useEffect(() => {
    if (!kommune || !allPolling) return
    const iv = setInterval(async () => {
      await loadStatuses(kommune.id)
      const sts = useStore.getState().statuses
      const types = Object.keys(CLIMATE_TYPE_META)
      const allDone = types.every(ct => {
        const s = sts.find(x => x.climate_type === ct)
        return s && (s.status === 'done' || s.status === 'error')
      })
      if (allDone) {
        setAllPolling(false)
        useStore.setState({ allRunning: false })
        loadRiskSummary(kommune.id).catch(() => {})
        loadAllAssessments(kommune.id).catch(() => {})
      }
    }, 800)
    return () => clearInterval(iv)
  }, [kommune, allPolling])

  const handleStart = async () => {
    if (!kommune) return
    setPolling(true)
    await startAssessment(kommune.id)
    await loadStatuses(kommune.id)
  }

  const handleAbort = async () => {
    if (!kommune) return
    await abortAssessment(kommune.id)
    setPolling(false)
    await loadStatuses(kommune.id)
  }

  const handleStartAll = async () => {
    if (!kommune) return
    setAllPolling(true)
    await startAllAssessments(kommune.id)
    await loadStatuses(kommune.id)
  }

  const meta = CLIMATE_TYPE_META[effectiveType]
  const maxLevel = climateTypeDefs.find(ct => ct.climate_type === effectiveType)?.max_level || 2

  // Multi-type status summary
  const anyRunning = statuses.some(s => s.status === 'running')
  const doneCount = Object.keys(CLIMATE_TYPE_META).filter(ct =>
    statuses.find(s => s.climate_type === ct)?.status === 'done'
  ).length
  const totalTypes = Object.keys(CLIMATE_TYPE_META).length

  if (!kommune) return null

  return (
    <div className="dashboard-section">
      <div className="dashboard-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span style={{ fontSize: '1.2rem' }}>{meta?.icon}</span>
          <h2 className="dashboard-title" style={{ margin: 0 }}>
            {showAllButton ? 'Klimarisiko-Analyse' : `${meta?.label || effectiveType} – Analyse`}
          </h2>
        </div>
        <div className="dashboard-actions" style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          {/* Level selector */}
          <select
            value={assessmentLevel}
            onChange={e => setAssessmentLevel(Number(e.target.value))}
            disabled={anyRunning}
            style={{ fontSize: '0.8rem', padding: '2px 6px', borderRadius: 4, border: '1px solid var(--border)' }}
          >
            {Array.from({ length: maxLevel }, (_, i) => i + 1).map(l => (
              <option key={l} value={l}>Level {l}</option>
            ))}
          </select>

          {/* Start single / Abort */}
          {!showAllButton && (
            currentStatus?.status === 'running' ? (
              <button className="btn btn-danger btn-sm" onClick={handleAbort}>✕ Abbrechen</button>
            ) : (
              <button className="btn btn-primary btn-sm" onClick={handleStart}>▶ Berechnen</button>
            )
          )}

          {/* "Alle berechnen" button (overview mode) */}
          {showAllButton && (
            <button
              className="btn btn-primary btn-sm"
              onClick={handleStartAll}
              disabled={anyRunning}
              style={{ fontWeight: 600 }}
            >
              ▶▶ Alle berechnen ({doneCount}/{totalTypes})
            </button>
          )}
        </div>
      </div>

      {/* Multi-type status strip (overview mode) */}
      {showAllButton && (allPolling || doneCount > 0) && (
        <div style={{
          display: 'flex', gap: 6, flexWrap: 'wrap', marginTop: 8,
          padding: '8px 10px', background: 'var(--bg)', borderRadius: 8,
        }}>
          {Object.entries(CLIMATE_TYPE_META).map(([ct, m]) => {
            const s = statuses.find(x => x.climate_type === ct)
            const badge = s?.status === 'done' ? '✓' : s?.status === 'running' ? '⟳' : s?.status === 'error' ? '✕' : '○'
            const color = s?.status === 'done' ? 'var(--success)' : s?.status === 'running' ? 'var(--primary)' : s?.status === 'error' ? 'var(--danger)' : 'var(--text-muted)'
            return (
              <div key={ct} style={{
                display: 'flex', alignItems: 'center', gap: 3,
                fontSize: '0.72rem', color,
                padding: '2px 6px', borderRadius: 6,
                background: s?.status === 'running' ? '#dbeafe' : 'transparent',
              }}>
                <span>{m.icon}</span>
                <span style={{ fontWeight: 600 }}>{badge}</span>
                {s?.status === 'running' && (
                  <span style={{ fontSize: '0.65rem' }}>{s.progress_pct}%</span>
                )}
              </div>
            )
          })}
        </div>
      )}

      {/* Single-type status bar */}
      {!showAllButton && currentStatus && (
        <div className="dashboard-status-card" style={{ marginTop: 8 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              {(currentStatus.step_history?.length > 0 || currentStatus.status === 'done') && (
                <button
                  onClick={() => setStepsExpanded(e => !e)}
                  style={{
                    background: 'none', border: 'none', cursor: 'pointer', padding: 0,
                    fontSize: '0.75rem', color: 'var(--text-muted)',
                    transform: stepsExpanded ? 'rotate(90deg)' : 'rotate(0deg)',
                    transition: 'transform 0.15s ease',
                  }}
                >▶</button>
              )}
              <span style={{ fontSize: '0.85rem', fontWeight: 500 }}>
                {meta?.label} (Level {currentStatus.level})
              </span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              {currentStatus.status === 'running' && currentStatus.eta_seconds != null && currentStatus.eta_seconds > 0 && (
                <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
                  ~{formatDuration(currentStatus.eta_seconds)} verbleibend
                </span>
              )}
              <span className={`status-badge ${currentStatus.status}`}>
                {currentStatus.status === 'done' ? '✓ Fertig' :
                 currentStatus.status === 'running' ? '⟳ Läuft …' :
                 currentStatus.status === 'error' ? '✕ Fehler' : '○ Ausstehend'}
              </span>
            </div>
          </div>
          {currentStatus.status === 'running' && (
            <div className="progress-bar" style={{ marginTop: 8 }}>
              <div className="fill" style={{ width: `${currentStatus.progress_pct}%` }} />
            </div>
          )}
          {currentStatus.message && (
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: 4 }}>
              {currentStatus.message}
            </div>
          )}

          {stepsExpanded && currentStatus.step_history?.length > 0 && (
            <div style={{ marginTop: 8, borderTop: '1px solid var(--border)', paddingTop: 8 }}>
              <div style={{ fontSize: '0.7rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: 4 }}>
                Berechnungsschritte
              </div>
              {currentStatus.step_history.map((step, i) => {
                const dur = stepDuration(step)
                const isActive = !step.finished
                return (
                  <div key={i} style={{
                    display: 'flex', alignItems: 'flex-start', gap: 6,
                    fontSize: '0.72rem', color: isActive ? 'var(--text)' : 'var(--text-muted)',
                    marginBottom: 2,
                  }}>
                    <span style={{ width: 14, textAlign: 'center' }}>
                      {isActive ? '⟳' : '✓'}
                    </span>
                    <div style={{ flex: 1 }}>
                      <div style={{ fontWeight: isActive ? 500 : 400 }}>{step.label}</div>
                      {step.detail && (
                        <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>{step.detail}</div>
                      )}
                    </div>
                    {dur && <span style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>{dur}</span>}
                  </div>
                )
              })}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
