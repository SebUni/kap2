import { useEffect, useRef, useState } from 'react'
import { useStore } from '../store'
import InfoTooltip from './InfoTooltip'
import type { StepHistoryEntry } from '../types'
import {
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  ResponsiveContainer, Tooltip,
  LineChart, Line, XAxis, YAxis, CartesianGrid, Legend,
} from 'recharts'

const LINE_PALETTE = ['#ef4444', '#f59e0b', '#3b82f6', '#10b981', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316']

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

function AssessmentBar() {
  const { kommune, status, loadStatus, startAssessment, abortAssessment, loadRiskSummary, loadCostSummary, loadRiskHistogram } = useStore()
  const [polling, setPolling] = useState(false)
  const [stepsExpanded, setStepsExpanded] = useState(false)
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null)

  useEffect(() => {
    if (!kommune) return
    loadStatus(kommune.id).catch(() => {})
  }, [kommune])

  useEffect(() => {
    if (status?.status === 'running' && !polling) setPolling(true)
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
        }
      }
    }, 800)
    return () => { if (pollRef.current) clearInterval(pollRef.current) }
  }, [kommune, polling])

  useEffect(() => {
    if (status?.status !== 'running') setStepsExpanded(false)
  }, [status?.status])

  if (!kommune) return null
  const running = status?.status === 'running'
  const steps = status?.step_history ?? []
  const currentIdx = steps.findIndex(s => !s.finished)
  const currentStep = currentIdx >= 0 ? steps[currentIdx] : steps[steps.length - 1]
  const previousStep = currentIdx > 0 ? steps[currentIdx - 1] : currentIdx === -1 && steps.length > 1 ? steps[steps.length - 2] : undefined
  const pct = Math.round(status?.progress_pct ?? 0)
  const runningLabel = currentStep?.label ?? 'Berechnung'

  return (
    <div className="dashboard-section" style={{ display: 'flex', alignItems: 'center', gap: 12, flexWrap: 'wrap' }}>
      <div style={{ flex: 1, minWidth: 200 }}>
        <h2 className="dashboard-title" style={{ margin: 0, fontSize: '1.05rem' }}>Klimarisiko-Analyse</h2>
        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 2 }}>
          {status?.status === 'done' ? '✓ Berechnung abgeschlossen'
            : running ? (
              <span>
                <span style={{ fontWeight: 600, color: 'var(--text)', marginRight: 6 }}>{pct}%</span>
                {runningLabel}
                {currentStep?.detail && (
                  <span style={{ marginLeft: 6, opacity: 0.75 }}>{currentStep.detail}</span>
                )}
              </span>
            )
            : status?.status === 'error' ? `✕ ${status?.message || 'Fehler'}`
            : 'Noch keine Berechnung – Klimatreiber, Expositionen, Verwundbarkeiten & Risiken pro 100m-Zelle.'}
        </div>
        {running && (
          <>
            <div className="progress-bar" style={{ marginTop: 6 }}>
              <div className="fill" style={{ width: `${status?.progress_pct || 0}%` }} />
            </div>
            {steps.length > 0 && (
              <div className={`assessment-steps-panel${stepsExpanded ? ' expanded' : ''}`}>
                <button
                  type="button"
                  className="assessment-steps-toggle"
                  onClick={() => setStepsExpanded(v => !v)}
                  aria-expanded={stepsExpanded}
                  aria-label={stepsExpanded ? 'Schritte einklappen' : 'Schritte ausklappen'}
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
                      {currentStep && <StepRow step={currentStep} active />}
                      {previousStep && <StepRow step={previousStep} faded />}
                    </>
                  )}
                </div>
              </div>
            )}
          </>
        )}
      </div>
      {running ? (
        <button className="btn btn-danger btn-sm" onClick={() => kommune && abortAssessment(kommune.id)}>✕ Abbrechen</button>
      ) : (
        <button className="btn btn-primary btn-sm" onClick={() => { if (kommune) { setPolling(true); startAssessment(kommune.id) } }}>
          ▶ Berechnen
        </button>
      )}
    </div>
  )
}

export default function Dashboard() {
  const { kommune, catalog, riskSummary, costSummary, riskHistogram, status, loadCatalog, loadRiskSummary, loadCostSummary, loadRiskHistogram } = useStore()

  useEffect(() => { loadCatalog().catch(() => {}) }, [])
  useEffect(() => {
    if (!kommune || status?.status !== 'done') return
    loadRiskSummary(kommune.id).catch(() => {})
    loadCostSummary(kommune.id).catch(() => {})
    loadRiskHistogram(kommune.id).catch(() => {})
  }, [kommune, status?.status])

  const fmtEur = (v: number) => v.toLocaleString('de-DE', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 })

  // ── Summary spider: 5 KWRA groups ────────────────────────────────────────
  const groupOrder = catalog?.groups.map(g => g.code) || []
  const groupRadar = groupOrder
    .filter(code => riskSummary?.groups[code])
    .map(code => ({
      group: riskSummary!.groups[code].label,
      index: riskSummary!.groups[code].index,
    }))

  return (
    <div className="dashboard-grid" style={{ padding: '1rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <AssessmentBar />

      {status?.status === 'done' && riskSummary ? (
        <>
          {/* ── ZUSAMMENFASSUNG ──────────────────────────────────────── */}
          <section className="dashboard-section">
            <h2 className="section-title" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              Zusammenfassung
              <InfoTooltip title="Übergreifende Metrik"
                description="Risikogruppen-Index = Mittel der 90.-Perzentil-Einzelrisiko-Indizes (0–100) je KWRA-Herausforderung. Das P90 hebt belastete Zellen hervor und vermeidet die Verflachung durch viele leere Insel-/Strandzellen." />
            </h2>
            <div style={{ display: 'flex', gap: '1.5rem', flexWrap: 'wrap' }}>
              <div className="chart-card" style={{ flex: '1 1 360px', minHeight: 320 }}>
                <h3 className="chart-title">Risikogruppen (P90-Index 0–100)</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <RadarChart data={groupRadar} outerRadius="70%">
                    <PolarGrid />
                    <PolarAngleAxis dataKey="group" tick={{ fontSize: 11 }} />
                    <PolarRadiusAxis domain={[0, 100]} tick={{ fontSize: 9 }} />
                    <Radar name="P90-Index" dataKey="index" stroke="#ef4444" fill="#ef4444" fillOpacity={0.4} />
                    <Tooltip />
                  </RadarChart>
                </ResponsiveContainer>
              </div>

              <div className="chart-card" style={{ flex: '1 1 280px' }}>
                <h3 className="chart-title">Kostenzusammenfassung</h3>
                <div className="kpi-row" style={{ flexDirection: 'column', gap: 8 }}>
                  <div className="kpi-card">
                    <div className="kpi-label">Erwartete Schäden (Basis)</div>
                    <div className="kpi-value accent" style={{ fontSize: '1.1rem' }}>
                      {fmtEur(riskSummary.cost.total_eur)}<span className="kpi-unit"> /Jahr</span>
                    </div>
                  </div>
                  {costSummary && (
                    <>
                      <div className="kpi-card">
                        <div className="kpi-label">Mit Maßnahmen</div>
                        <div className="kpi-value" style={{ fontSize: '1.1rem' }}>
                          {fmtEur(costSummary.damages_with_measures_eur)}<span className="kpi-unit"> /Jahr</span>
                        </div>
                      </div>
                      <div className="kpi-card">
                        <div className="kpi-label">Vermiedene Schäden</div>
                        <div className="kpi-value success" style={{ fontSize: '1.1rem' }}>
                          {fmtEur(costSummary.damage_reduction_eur)}<span className="kpi-unit"> /Jahr</span>
                        </div>
                      </div>
                      <div className="kpi-card">
                        <div className="kpi-label">Maßnahmen-Investition</div>
                        <div className="kpi-value" style={{ fontSize: '1.1rem' }}>
                          {fmtEur(costSummary.measures.total_investment_eur)}
                        </div>
                      </div>
                    </>
                  )}
                </div>
              </div>
            </div>
          </section>

          {/* ── RISIKEN: Spinne je KWRA-Gruppe ───────────────────────── */}
          <section className="dashboard-section">
            <h2 className="section-title">Risiken</h2>
            <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
              {groupOrder.map(code => {
                const g = riskSummary.groups[code]
                if (!g || !g.risk_codes.length) return null
                const data = g.risk_codes.map(rc => ({
                  risk: riskSummary.risks[rc]?.name || rc,
                  index: riskSummary.risks[rc]?.index || 0,
                }))
                const grpDef = catalog?.groups.find(x => x.code === code)
                return (
                  <div key={code} className="chart-card" style={{ flex: '1 1 340px', minHeight: 320 }}>
                    <h3 className="chart-title" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                      <span style={{ color: g.color }}>●</span> {g.label}
                      {grpDef && <InfoTooltip title={g.label} description={grpDef.description} />}
                    </h3>
                    <ResponsiveContainer width="100%" height={280}>
                      <RadarChart data={data} outerRadius="65%">
                        <PolarGrid />
                        <PolarAngleAxis dataKey="risk" tick={{ fontSize: 9 }} />
                        <PolarRadiusAxis domain={[0, 100]} tick={{ fontSize: 8 }} />
                        <Radar name="P90-Index" dataKey="index" stroke={g.color} fill={g.color} fillOpacity={0.4} />
                        <Tooltip />
                      </RadarChart>
                    </ResponsiveContainer>
                  </div>
                )
              })}
            </div>
          </section>

          {/* ── RISIKOVERTEILUNG ─────────────────────────────────────── */}
          {riskHistogram && (
            <section className="dashboard-section">
              <h2 className="section-title" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                Risikoverteilung
                <InfoTooltip title="Häufigkeit der Risiko-Index-Höhen"
                  description="Zeigt, in wie vielen 100m-Zellen ein Risiko welche Index-Höhe (0–100, 20 Klassen à 5) erreicht. Wenige Zellen mit hohem Index → punktuelle Maßnahmen; viele Zellen mit hohem Index → flächendeckender Handlungsbedarf." />
              </h2>
              <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
                {groupOrder.map(code => {
                  const g = riskSummary.groups[code]
                  if (!g || !g.risk_codes.length) return null
                  const risksInGroup = g.risk_codes.filter(rc => riskHistogram.risks[rc])
                  if (!risksInGroup.length) return null
                  const data = riskHistogram.bin_labels.map((label, i) => {
                    const row: Record<string, number | string> = { bin: label }
                    risksInGroup.forEach(rc => {
                      row[riskHistogram.risks[rc].name] = riskHistogram.risks[rc].counts[i]
                    })
                    return row
                  })
                  return (
                    <div key={code} className="chart-card" style={{ flex: '1 1 460px', minWidth: 360 }}>
                      <h3 className="chart-title" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                        <span style={{ color: g.color }}>●</span> {g.label}
                      </h3>
                      <ResponsiveContainer width="100%" height={260}>
                        <LineChart data={data} margin={{ top: 8, right: 12, bottom: 4, left: 0 }}>
                          <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
                          <XAxis dataKey="bin" tick={{ fontSize: 9 }} interval={1} />
                          <YAxis tick={{ fontSize: 9 }} allowDecimals={false}
                            label={{ value: 'Zellen', angle: -90, position: 'insideLeft', fontSize: 10 }} />
                          <Tooltip wrapperStyle={{ fontSize: 11 }} />
                          <Legend wrapperStyle={{ fontSize: 10 }} />
                          {risksInGroup.map((rc, idx) => (
                            <Line key={rc} type="monotone" dataKey={riskHistogram.risks[rc].name}
                              stroke={LINE_PALETTE[idx % LINE_PALETTE.length]} strokeWidth={2} dot={false} />
                          ))}
                        </LineChart>
                      </ResponsiveContainer>

                      {/* Ausklappbare Absolutwerte je Risiko */}
                      <div style={{ marginTop: 8 }}>
                        {risksInGroup.map(rc => {
                          const r = riskHistogram.risks[rc]
                          return (
                            <details key={rc} style={{ borderTop: '1px solid var(--border)', padding: '4px 0' }}>
                              <summary style={{ cursor: 'pointer', fontSize: '0.8rem', fontWeight: 500 }}>
                                {r.name}
                              </summary>
                              <div style={{ padding: '6px 4px' }}>
                                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginBottom: 8 }}>
                                  <div className="kpi-card" style={{ flex: '1 1 110px' }}>
                                    <div className="kpi-label">P90-Index</div>
                                    <div className="kpi-value" style={{ fontSize: '0.95rem' }}>{r.p90_index.toFixed(1)}</div>
                                  </div>
                                  <div className="kpi-card" style={{ flex: '1 1 110px' }}>
                                    <div className="kpi-label">Max. Index</div>
                                    <div className="kpi-value" style={{ fontSize: '0.95rem' }}>{r.max_index.toFixed(1)}</div>
                                  </div>
                                  <div className="kpi-card" style={{ flex: '1 1 110px' }}>
                                    <div className="kpi-label">Betroffene Zellen</div>
                                    <div className="kpi-value" style={{ fontSize: '0.95rem' }}>
                                      {r.nonzero_cells.toLocaleString('de-DE')}
                                      <span className="kpi-unit"> / {riskHistogram.total_cells.toLocaleString('de-DE')}</span>
                                    </div>
                                  </div>
                                  <div className="kpi-card" style={{ flex: '1 1 110px' }}>
                                    <div className="kpi-label">Ergebnis</div>
                                    <div className="kpi-value" style={{ fontSize: '0.95rem' }}>
                                      {r.outcome.toLocaleString('de-DE', { maximumFractionDigits: 1 })}
                                      <span className="kpi-unit"> {r.outcome_unit}</span>
                                    </div>
                                  </div>
                                  {(r.cost_dimension === 'monetary' || r.cost_eur > 0) && (
                                    <div className="kpi-card" style={{ flex: '1 1 110px' }}>
                                      <div className="kpi-label">Schaden/Jahr</div>
                                      <div className="kpi-value accent" style={{ fontSize: '0.95rem' }}>{fmtEur(r.cost_eur)}</div>
                                    </div>
                                  )}
                                </div>
                                <table className="data-table" style={{ fontSize: '0.74rem' }}>
                                  <thead>
                                    <tr><th>Index-Klasse</th><th style={{ textAlign: 'right' }}>Zellen</th><th style={{ textAlign: 'right' }}>Anteil</th></tr>
                                  </thead>
                                  <tbody>
                                    {riskHistogram.bin_labels.map((label, i) => {
                                      const cnt = r.counts[i]
                                      if (cnt === 0) return null
                                      const pct = riskHistogram.total_cells > 0 ? (cnt / riskHistogram.total_cells) * 100 : 0
                                      return (
                                        <tr key={label}>
                                          <td>{label}</td>
                                          <td style={{ textAlign: 'right' }}>{cnt.toLocaleString('de-DE')}</td>
                                          <td style={{ textAlign: 'right', color: 'var(--text-muted)' }}>{pct.toFixed(1)} %</td>
                                        </tr>
                                      )
                                    })}
                                  </tbody>
                                </table>
                              </div>
                            </details>
                          )
                        })}
                      </div>
                    </div>
                  )
                })}
              </div>
            </section>
          )}

          {/* ── KOSTEN ───────────────────────────────────────────────── */}
          <section className="dashboard-section">
            <h2 className="section-title">Kosten</h2>
            <div className="chart-card">
              <h3 className="chart-title">Erwartete Schäden je Risiko</h3>
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Risiko</th>
                    <th style={{ textAlign: 'right' }}>Index</th>
                    <th style={{ textAlign: 'right' }}>Ergebnis</th>
                    <th style={{ textAlign: 'right' }}>Schaden/Jahr</th>
                  </tr>
                </thead>
                <tbody>
                  {(costSummary?.by_risk || riskSummary.cost.by_risk).slice(0, 20).map(r => (
                    <tr key={r.code}>
                      <td style={{ fontWeight: 500 }}>{r.name}</td>
                      <td style={{ textAlign: 'right' }}>{r.index.toFixed(1)}</td>
                      <td style={{ textAlign: 'right', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                        {r.outcome.toLocaleString('de-DE', { maximumFractionDigits: 1 })} {r.outcome_unit}
                      </td>
                      <td style={{ textAlign: 'right' }}>
                        {r.cost_dimension === 'monetary' || r.cost_eur > 0 ? fmtEur(r.cost_eur) : '–'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {costSummary && costSummary.measures.rows.length > 0 && (
              <div className="chart-card" style={{ marginTop: '1rem' }}>
                <h3 className="chart-title">Maßnahmen – Investition & Nutzen</h3>
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Maßnahme</th>
                      <th style={{ textAlign: 'right' }}>Investition</th>
                      <th style={{ textAlign: 'right' }}>Unterhalt/Jahr</th>
                      <th style={{ textAlign: 'right' }}>Nutzen/Jahr</th>
                    </tr>
                  </thead>
                  <tbody>
                    {costSummary.measures.rows.map(m => (
                      <tr key={m.id}>
                        <td style={{ fontWeight: 500 }}>{m.name}</td>
                        <td style={{ textAlign: 'right' }}>{fmtEur(m.investment_eur)}</td>
                        <td style={{ textAlign: 'right' }}>{fmtEur(m.annual_maintenance_eur)}</td>
                        <td style={{ textAlign: 'right', color: 'var(--success)' }}>{fmtEur(m.annual_benefit_eur)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </section>
        </>
      ) : status?.status === 'done' ? (
        <div className="dashboard-empty">
          <p style={{ fontSize: '1.1rem', marginBottom: '0.5rem' }}>Ergebnisse werden geladen …</p>
        </div>
      ) : (
        <div className="dashboard-empty">
          <p style={{ fontSize: '1.1rem', marginBottom: '0.5rem' }}>Noch keine Analyseergebnisse</p>
          <p>Klicken Sie oben auf „▶ Berechnen“, um alle Klimarisiken für die 100m-Zellen zu ermitteln.</p>
        </div>
      )}
    </div>
  )
}
