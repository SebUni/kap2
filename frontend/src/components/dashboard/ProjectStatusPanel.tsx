import { useEffect, useRef, useState } from 'react'
import { useStore } from '../../store'
import InlineSpinner from '../InlineSpinner'
import type { StepHistoryEntry } from '../../types'

function formatStepTime(iso: string): string {
  try {
    return new Date(iso).toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
  } catch {
    return ''
  }
}

function StepRow({ step, active, faded }: { step: StepHistoryEntry; active?: boolean; faded?: boolean }) {
  return (
    <div className={`assessment-step-row${active ? ' active' : ''}${faded ? ' faded' : ''}${step.finished ? ' done' : ''}`}>
      <span className="assessment-step-time">{formatStepTime(step.started)}</span>
      <span className="assessment-step-label">{step.label}</span>
      {step.detail && <span className="assessment-step-detail">{step.detail}</span>}
    </div>
  )
}

/**
 * Projektstatus mit vollständiger Berechnungssteuerung: Start/Abbrechen,
 * Fortschrittsbalken und Live-Schrittprotokoll (800-ms-Polling). Lädt nach
 * Abschluss alle Dashboard-Daten nach (Summaries, Kostenprojektion, Profil).
 * Lebt im Konfigurations-Screen — das Dashboard zeigt nur noch Ergebnisse.
 */
export default function ProjectStatusPanel() {
  const {
    kommune, status, loadStatus, startAssessment, abortAssessment,
    loadRiskSummary, loadCostSummary, loadRiskHistogram,
    loadCostProjection, loadKommuneProfile,
    activeLayer, setActiveLayer,
  } = useStore()
  const [polling, setPolling] = useState(false)
  const [stepsExpanded, setStepsExpanded] = useState(false)
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null)

  useEffect(() => {
    if (!kommune) return
    loadStatus(kommune.id).catch(() => {})
  }, [kommune])

  useEffect(() => {
    if ((status?.status === 'running' || status?.status === 'queued') && !polling) setPolling(true)
  }, [status?.status])

  useEffect(() => {
    if (!kommune || !polling) return
    pollRef.current = setInterval(async () => {
      const st = await loadStatus(kommune.id).catch(() => null)
      if (st && (st.status === 'done' || st.status === 'error')) {
        setPolling(false)
        if (st.status === 'done') {
          loadRiskSummary(kommune.id).catch(() => {})
          loadCostSummary(kommune.id).catch(() => {})
          loadRiskHistogram(kommune.id).catch(() => {})
          loadCostProjection(kommune.id).catch(() => {})
          loadKommuneProfile(kommune.id).catch(() => {})
          if (activeLayer) {
            setActiveLayer(activeLayer).catch(() => {})
          }
        }
      }
    }, 800)
    return () => { if (pollRef.current) clearInterval(pollRef.current) }
  }, [kommune, polling, activeLayer])

  if (!kommune) return null
  const running = status?.status === 'running'
  const queued = status?.status === 'queued'
  const done = status?.status === 'done'
  const steps = status?.step_history ?? []
  const showStepLog = steps.length > 0 && (running || done || status?.status === 'error')
  const currentIdx = steps.findIndex(s => !s.finished)
  const currentStep = currentIdx >= 0 ? steps[currentIdx] : steps[steps.length - 1]
  const previousStep = currentIdx > 0 ? steps[currentIdx - 1] : currentIdx === -1 && steps.length > 1 ? steps[steps.length - 2] : undefined
  const pct = Math.round(status?.progress_pct ?? 0)
  const runningLabel = currentStep?.label ?? 'Berechnung'

  const handleStartAssessment = async () => {
    if (!kommune) return
    setStepsExpanded(false)
    try {
      await startAssessment(kommune.id)
      setPolling(true)
    } catch {
      setPolling(false)
    }
  }

  const canRecalculate = done || status?.status === 'error'
  const startButtonLabel = canRecalculate ? '↻ Neu berechnen' : '▶ Berechnen'

  return (
    <div
      className="card"
      style={{
        marginBottom: '1.5rem',
        borderColor: done ? 'var(--success)' : (running || queued) ? 'var(--primary)' : 'var(--warning)',
        display: 'flex', alignItems: 'flex-start', gap: 12, flexWrap: 'wrap',
      }}
    >
      <div style={{ flex: 1, minWidth: 220 }}>
        <h3 style={{ fontSize: '0.9rem', fontWeight: 600, marginBottom: 4 }}>Projektstatus</h3>
        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
          {done ? (
              <span>
                <span style={{ fontWeight: 600, color: 'var(--success)', marginRight: 6 }}>✓</span>
                Startklar – Ergebnisse im Dashboard, Anpassungen können modelliert werden
                {currentStep?.detail && (
                  <span style={{ marginLeft: 6, opacity: 0.75 }}>({currentStep.detail})</span>
                )}
              </span>
            )
            : running ? (
              <span>
                <span style={{ fontWeight: 600, color: 'var(--text)', marginRight: 6 }}>{pct}%</span>
                {runningLabel}
                {currentStep?.detail && (
                  <span style={{ marginLeft: 6, opacity: 0.75 }}>{currentStep.detail}</span>
                )}
              </span>
            )
            : queued ? (
              <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}>
                <InlineSpinner size={12} />
                {status?.message || 'Wartet auf freien Berechnungs-Slot …'}
                {status?.queue_position != null && status.queue_position > 1 && (
                  <span style={{ opacity: 0.75 }}>(Position {status.queue_position})</span>
                )}
              </span>
            )
            : status?.status === 'error' ? `✕ ${status?.message || 'Fehler'}`
            : !status ? (
              <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}>
                <InlineSpinner size={12} />
                Status wird geladen …
              </span>
            )
            : 'Noch keine Berechnung – Klimatische Einflüsse, Räumliche Expositionen, Sensitivitäten & Risiken pro 100m-Zelle.'}
        </div>
        {(running || done) && (
          <div className="progress-bar" style={{ marginTop: 6 }}>
            <div
              className="fill"
              style={{
                width: done ? '100%' : `${status?.progress_pct || 0}%`,
                ...(done ? { background: 'var(--success)' } : {}),
              }}
            />
          </div>
        )}
        {showStepLog && (
          <div className={`assessment-steps-panel${stepsExpanded ? ' expanded' : ''}`} style={{ marginTop: running || done ? 8 : 0 }}>
            <button
              type="button"
              className="assessment-steps-toggle"
              onClick={() => setStepsExpanded(v => !v)}
              aria-expanded={stepsExpanded}
              aria-label={stepsExpanded ? 'Protokoll einklappen' : 'Protokoll ausklappen'}
            >
              {stepsExpanded ? '▼' : '▶'}
            </button>
            <div className="assessment-steps-body">
              {stepsExpanded ? (
                steps.map((step, i) => (
                  <StepRow key={`${step.label}-${step.started}-${i}`} step={step} active={!step.finished && i === currentIdx} />
                ))
              ) : (
                <>
                  {currentStep && <StepRow step={currentStep} active={running} />}
                  {previousStep && <StepRow step={previousStep} faded />}
                </>
              )}
            </div>
          </div>
        )}
      </div>
      {(running || queued) ? (
        <button className="btn btn-danger btn-sm" onClick={() => kommune && abortAssessment(kommune.id)}>✕ Abbrechen</button>
      ) : (
        <button
          className="btn btn-primary btn-sm"
          onClick={handleStartAssessment}
          title={canRecalculate ? 'Assessment mit aktuellen Daten erneut ausführen' : 'Erstberechnung für alle 100m-Zellen starten'}
        >
          {startButtonLabel}
        </button>
      )}
    </div>
  )
}
