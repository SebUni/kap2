import { useEffect } from 'react'
import { useStore } from '../../store'
import { CLIMATE_TYPE_META } from '../../types'
import type { AssessmentStatus, RiskProjectionYear } from '../../types'
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Legend,
} from 'recharts'
import AssessmentControls from './AssessmentControls'
import ImpactSection from './ImpactSection'

interface Props {
  climateType: string
}

export default function ClimateDetail({ climateType }: Props) {
  const {
    kommune, statuses, assessmentLevel, assessmentsByType,
    riskSummary, riskProjections,
    setActiveClimateType, loadAssessmentForType, loadRiskProjection, loadRiskZones,
  } = useStore()

  const meta = CLIMATE_TYPE_META[climateType] || { label: climateType, icon: '📊', color: '#6b7280' }
  const status = statuses.find(s => s.climate_type === climateType) as AssessmentStatus | undefined
  const summary = riskSummary.find(s => s.climate_type === climateType)
  const projection: RiskProjectionYear[] = riskProjections[climateType] || []

  // Set active type and load data
  useEffect(() => {
    setActiveClimateType(climateType)
    if (!kommune) return
    loadAssessmentForType(kommune.id, climateType).catch(() => {})
    if (!riskProjections[climateType]) {
      loadRiskProjection(kommune.id, climateType).catch(() => {})
    }
    loadRiskZones(kommune.id, climateType).catch(() => {})
  }, [climateType, kommune])

  const features = assessmentsByType[climateType]?.features || []

  const riskColor = (v: number) =>
    v >= 7 ? '#ef4444' : v >= 5 ? '#f59e0b' : v >= 3 ? '#eab308' : '#22c55e'

  return (
    <div>
      {/* Controls for this type only */}
      <AssessmentControls climateType={climateType} />

      {/* Risk Summary */}
      {summary && (
        <div className="dashboard-section">
          <h3 className="section-title" style={{ borderColor: meta.color }}>
            {meta.icon} {meta.label} – Risikozusammenfassung
          </h3>
          <div className="kpi-row">
            <div className="kpi-card">
              <div className="kpi-label">Aggregiertes Risiko (ARI)</div>
              <div className="kpi-value" style={{ color: riskColor(summary.aggregated_risk) }}>
                {summary.aggregated_risk.toFixed(1)}
              </div>
              <div className="kpi-unit">von 10</div>
            </div>
            <div className="kpi-card">
              <div className="kpi-label">Max. Zonenrisiko</div>
              <div className="kpi-value" style={{ color: riskColor(summary.highest_zone_risk) }}>
                {summary.highest_zone_risk.toFixed(1)}
              </div>
            </div>
            <div className="kpi-card">
              <div className="kpi-label">Risikozonen</div>
              <div className="kpi-value">{summary.zone_count}</div>
            </div>
            <div className="kpi-card">
              <div className="kpi-label">Betroffene Fläche</div>
              <div className="kpi-value">{(summary.total_area_m2 / 10000).toFixed(1)}</div>
              <div className="kpi-unit">Hektar</div>
            </div>
          </div>
        </div>
      )}

      {/* Assessment KPIs from grid data */}
      {features.length > 0 && (
        <div className="dashboard-section">
          <h3 className="section-title" style={{ borderColor: meta.color }}>
            Berechnungsergebnisse ({features.length} Zellen)
          </h3>
          <div className="kpi-row">
            {(() => {
              const props = features.map(f => f.properties as Record<string, number>)
              const keys = Object.keys(props[0] || {}).filter(k =>
                !['grid_cell_id', 'row', 'col'].includes(k)
              ).slice(0, 6)
              return keys.map(key => {
                const vals = props.map(p => (p[key] as number) || 0)
                const avg = vals.reduce((a, b) => a + b, 0) / vals.length
                return (
                  <div key={key} className="kpi-card">
                    <div className="kpi-label">{key.replace(/_/g, ' ')}</div>
                    <div className="kpi-value">{avg < 100 ? avg.toFixed(2) : Math.round(avg).toLocaleString('de-DE')}</div>
                  </div>
                )
              })
            })()}
          </div>
        </div>
      )}

      {/* Projection chart */}
      {projection.length > 0 && (
        <div className="dashboard-section">
          <h3 className="section-title" style={{ borderColor: meta.color }}>
            Risikogebiet-Fortschreibung (2025–2065)
          </h3>
          <div className="dashboard-charts">
            <div className="chart-card">
              <h3 className="chart-title">Risikozonen & Schwere</h3>
              <ResponsiveContainer width="100%" height={240}>
                <LineChart data={projection}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                  <XAxis dataKey="year" tick={{ fontSize: 10 }} />
                  <YAxis tick={{ fontSize: 10 }} />
                  <Tooltip contentStyle={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 6, fontSize: '0.8rem' }} />
                  <Legend wrapperStyle={{ fontSize: '0.7rem' }} />
                  <Line type="monotone" dataKey="rcp45.zone_count" name="RCP 4.5 Zonen" stroke="#f59e0b" strokeWidth={2} dot={false} strokeDasharray="6 3" />
                  <Line type="monotone" dataKey="rcp85.zone_count" name="RCP 8.5 Zonen" stroke="#ef4444" strokeWidth={2} dot={false} strokeDasharray="6 3" />
                  <Line type="monotone" dataKey="rcp45.mean_severity" name="RCP 4.5 Schwere" stroke="#2563eb" strokeWidth={1.5} dot={false} />
                  <Line type="monotone" dataKey="rcp85.mean_severity" name="RCP 8.5 Schwere" stroke="#dc2626" strokeWidth={1.5} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Projection KPIs */}
            <div className="chart-card">
              <h3 className="chart-title">Projektion Eckdaten</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 10, padding: '8px 0' }}>
                {[2030, 2040, 2050, 2060].map(yr => {
                  const row = projection.find(r => r.year === yr)
                  if (!row) return null
                  return (
                    <div key={yr} style={{
                      display: 'flex', gap: 16, fontSize: '0.78rem',
                      padding: '6px 10px', background: 'var(--bg)', borderRadius: 6,
                    }}>
                      <span style={{ fontWeight: 700, minWidth: 40 }}>{yr}</span>
                      <div>
                        <span style={{ color: 'var(--text-muted)' }}>RCP 4.5: </span>
                        <span>{row.rcp45.zone_count} Zonen, Ø {row.rcp45.mean_severity.toFixed(1)}</span>
                      </div>
                      <div>
                        <span style={{ color: '#ef4444' }}>RCP 8.5: </span>
                        <span style={{ color: '#ef4444' }}>{row.rcp85.zone_count} Zonen, Ø {row.rcp85.mean_severity.toFixed(1)}</span>
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Impact Section */}
      <ImpactSection climateType={climateType} />

      {/* Empty state */}
      {!summary && features.length === 0 && (!status || status.status === 'pending') && (
        <div className="dashboard-empty">
          <p style={{ fontSize: '1rem', marginBottom: '0.5rem' }}>{meta.icon} {meta.label}</p>
          <p>Noch keine Berechnung durchgeführt. Starten Sie die Analyse oben.</p>
        </div>
      )}
    </div>
  )
}
