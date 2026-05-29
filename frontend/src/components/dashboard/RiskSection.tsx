import { useState, useEffect } from 'react'
import { useStore } from '../../store'
import { CLIMATE_TYPE_META } from '../../types'
import type { RiskSummary, RiskProjectionYear, AssessmentStatus } from '../../types'
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Legend,
} from 'recharts'

interface Props {
  summary: RiskSummary
  status?: AssessmentStatus
}

export default function RiskSection({ summary, status }: Props) {
  const {
    kommune, assessmentLevel, riskProjections,
    loadRiskProjection, loadAssessment, loadRiskZones,
    setActiveClimateType,
  } = useStore()
  const [expanded, setExpanded] = useState(false)

  const meta = CLIMATE_TYPE_META[summary.climate_type] || {
    label: summary.climate_type, icon: '📊', color: '#6b7280',
  }

  const riskColor = (v: number) =>
    v >= 7 ? '#ef4444' : v >= 5 ? '#f59e0b' : v >= 3 ? '#eab308' : '#22c55e'

  // Load projection when expanded
  useEffect(() => {
    if (expanded && kommune && !riskProjections[summary.climate_type]) {
      loadRiskProjection(kommune.id, summary.climate_type).catch(() => {})
    }
  }, [expanded, kommune])

  const projection: RiskProjectionYear[] = riskProjections[summary.climate_type] || []

  const handleClick = () => {
    setExpanded(e => !e)
    if (kommune) {
      setActiveClimateType(summary.climate_type)
      loadAssessment(kommune.id, summary.climate_type).catch(() => {})
      loadRiskZones(kommune.id, summary.climate_type).catch(() => {})
    }
  }

  return (
    <div className="card" style={{ marginBottom: 8 }}>
      {/* Header */}
      <div
        onClick={handleClick}
        style={{
          display: 'flex', alignItems: 'center', gap: 8,
          cursor: 'pointer', padding: '8px 12px',
          borderBottom: expanded ? '1px solid var(--border)' : 'none',
        }}
      >
        <span style={{ fontSize: '1.1rem' }}>{meta.icon}</span>
        <span style={{ fontWeight: 600, fontSize: '0.9rem', flex: 1 }}>{meta.label}</span>

        {/* ARI badge */}
        <span style={{
          background: riskColor(summary.aggregated_risk),
          color: '#fff', fontWeight: 700, fontSize: '0.75rem',
          padding: '2px 8px', borderRadius: 10,
        }}>
          {summary.aggregated_risk.toFixed(1)}
        </span>

        {/* Zone count */}
        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
          {summary.zone_count} Gebiete
        </span>

        {/* Status indicator */}
        {status && (
          <span className={`status-badge ${status.status}`} style={{ fontSize: '0.65rem' }}>
            {status.status === 'done' ? '✓' : status.status === 'running' ? '⟳' : '○'}
          </span>
        )}

        <span style={{
          fontSize: '0.7rem', color: 'var(--text-muted)',
          transform: expanded ? 'rotate(90deg)' : 'rotate(0deg)',
          transition: 'transform 0.15s',
        }}>▶</span>
      </div>

      {/* Condensed KPIs (always visible) */}
      <div style={{ display: 'flex', gap: 12, padding: '6px 12px', flexWrap: 'wrap' }}>
        <div style={{ fontSize: '0.75rem' }}>
          <span style={{ color: 'var(--text-muted)' }}>Fläche: </span>
          <span style={{ fontWeight: 600 }}>{(summary.total_area_m2 / 10000).toFixed(1)} ha</span>
        </div>
        <div style={{ fontSize: '0.75rem' }}>
          <span style={{ color: 'var(--text-muted)' }}>Max. Risiko: </span>
          <span style={{ fontWeight: 600, color: riskColor(summary.highest_zone_risk) }}>
            {summary.highest_zone_risk.toFixed(1)}
          </span>
        </div>
        <div style={{ fontSize: '0.75rem' }}>
          <span style={{ color: 'var(--text-muted)' }}>Zonen: </span>
          <span style={{ fontWeight: 600 }}>{summary.zone_count}</span>
        </div>
      </div>

      {/* Expanded: projection chart */}
      {expanded && (
        <div style={{ padding: '8px 12px 12px' }}>
          {projection.length > 0 ? (
            <>
              <h4 style={{ fontSize: '0.8rem', fontWeight: 600, marginBottom: 8 }}>
                Risikogebiet-Fortschreibung (2025–2065)
              </h4>
              <ResponsiveContainer width="100%" height={200}>
                <LineChart data={projection}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                  <XAxis dataKey="year" tick={{ fontSize: 9 }} />
                  <YAxis tick={{ fontSize: 9 }} />
                  <Tooltip
                    contentStyle={{
                      background: 'var(--surface)',
                      border: '1px solid var(--border)',
                      borderRadius: 6, fontSize: '0.75rem',
                    }}
                  />
                  <Legend wrapperStyle={{ fontSize: '0.7rem' }} />
                  <Line
                    type="monotone" dataKey="rcp45.zone_count" name="RCP 4.5 Zonen"
                    stroke="#f59e0b" strokeWidth={2} dot={false} strokeDasharray="6 3"
                  />
                  <Line
                    type="monotone" dataKey="rcp85.zone_count" name="RCP 8.5 Zonen"
                    stroke="#ef4444" strokeWidth={2} dot={false} strokeDasharray="6 3"
                  />
                  <Line
                    type="monotone" dataKey="rcp45.mean_severity" name="RCP 4.5 Schwere"
                    stroke="#2563eb" strokeWidth={1.5} dot={false}
                  />
                  <Line
                    type="monotone" dataKey="rcp85.mean_severity" name="RCP 8.5 Schwere"
                    stroke="#dc2626" strokeWidth={1.5} dot={false}
                  />
                </LineChart>
              </ResponsiveContainer>

              {/* Projection KPIs: 2040 / 2060 */}
              <div style={{ display: 'flex', gap: 12, marginTop: 8, flexWrap: 'wrap' }}>
                {[2040, 2060].map(yr => {
                  const row = projection.find(r => r.year === yr)
                  if (!row) return null
                  return (
                    <div key={yr} style={{
                      flex: '1 1 140px', fontSize: '0.72rem',
                      background: 'var(--surface-hover)', borderRadius: 6, padding: '6px 10px',
                    }}>
                      <div style={{ fontWeight: 600, marginBottom: 4 }}>{yr}</div>
                      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                        <span style={{ color: 'var(--text-muted)' }}>RCP 4.5 Zonen:</span>
                        <span>{row.rcp45.zone_count}</span>
                      </div>
                      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                        <span style={{ color: 'var(--text-muted)' }}>RCP 8.5 Zonen:</span>
                        <span style={{ color: '#ef4444' }}>{row.rcp85.zone_count}</span>
                      </div>
                      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                        <span style={{ color: 'var(--text-muted)' }}>Schwere (8.5):</span>
                        <span style={{ color: '#ef4444' }}>{row.rcp85.mean_severity.toFixed(1)}</span>
                      </div>
                    </div>
                  )
                })}
              </div>
            </>
          ) : (
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', padding: 8 }}>
              Keine Projektionsdaten verfügbar. Bitte zuerst eine Berechnung durchführen.
            </div>
          )}
        </div>
      )}
    </div>
  )
}
