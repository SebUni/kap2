import { useEffect } from 'react'
import { useStore } from '../../store'
import { CLIMATE_TYPE_META } from '../../types'
import type { RiskSummary } from '../../types'
import {
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  ResponsiveContainer, Tooltip,
} from 'recharts'

export default function RiskOverview() {
  const { kommune, riskSummary, loadRiskSummary } = useStore()

  useEffect(() => {
    if (kommune) loadRiskSummary(kommune.id).catch(() => {})
  }, [kommune])

  const radarData = riskSummary
    .filter(s => s.climate_type !== 'health')
    .map(s => ({
      type: CLIMATE_TYPE_META[s.climate_type]?.label || s.climate_type,
      risk: s.aggregated_risk,
      fullMark: 10,
    }))

  // Overall risk = max of all ARIs
  const overallRisk = riskSummary.length > 0
    ? Math.max(...riskSummary.map(s => s.aggregated_risk))
    : 0

  const riskColor = (v: number) =>
    v >= 7 ? '#ef4444' : v >= 5 ? '#f59e0b' : v >= 3 ? '#eab308' : '#22c55e'

  // Top 3 risks
  const top3 = [...riskSummary]
    .sort((a, b) => b.aggregated_risk - a.aggregated_risk)
    .slice(0, 3)

  if (!kommune) return null

  return (
    <div className="dashboard-section">
      <h3 className="section-title">Risiko-Übersicht</h3>
      <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap', alignItems: 'flex-start' }}>
        {/* Overall risk gauge */}
        <div style={{
          display: 'flex', flexDirection: 'column', alignItems: 'center',
          padding: 16, minWidth: 120,
        }}>
          <div style={{
            width: 80, height: 80, borderRadius: '50%',
            border: `4px solid ${riskColor(overallRisk)}`,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: '1.8rem', fontWeight: 700,
            color: riskColor(overallRisk),
          }}>
            {overallRisk.toFixed(1)}
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: 6 }}>
            Gesamt-Risiko
          </div>
        </div>

        {/* Radar chart */}
        {radarData.length > 0 && (
          <div style={{ flex: '1 1 280px', minWidth: 240, height: 220 }}>
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid stroke="var(--border)" />
                <PolarAngleAxis dataKey="type" tick={{ fontSize: 10 }} />
                <PolarRadiusAxis domain={[0, 10]} tick={{ fontSize: 9 }} />
                <Tooltip
                  contentStyle={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 6, fontSize: '0.8rem' }}
                />
                <Radar dataKey="risk" name="ARI" stroke="#ef4444" fill="#ef4444" fillOpacity={0.25} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Top 3 */}
        <div style={{ flex: '0 0 auto', display: 'flex', flexDirection: 'column', gap: 8, minWidth: 180 }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)' }}>
            Top-3 Handlungsfelder
          </div>
          {top3.map((s: RiskSummary) => {
            const meta = CLIMATE_TYPE_META[s.climate_type]
            return (
              <div key={s.climate_type} className="kpi-card" style={{ padding: '8px 12px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                  <span>{meta?.icon}</span>
                  <span style={{ fontWeight: 600, fontSize: '0.85rem' }}>{meta?.label}</span>
                  <span style={{
                    marginLeft: 'auto', fontWeight: 700, fontSize: '0.9rem',
                    color: riskColor(s.aggregated_risk),
                  }}>
                    {s.aggregated_risk.toFixed(1)}
                  </span>
                </div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: 2 }}>
                  {s.zone_count} Risikogebiete · {(s.total_area_m2 / 10000).toFixed(1)} ha
                </div>
              </div>
            )
          })}
          {riskSummary.length === 0 && (
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              Noch keine Berechnungen durchgeführt
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
