import { useEffect, useState } from 'react'
import { useStore } from '../store'
import { CLIMATE_TYPE_META } from '../types'
import type { AssessmentStatus } from '../types'
import {
  BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Legend,
} from 'recharts'
import RiskOverview from './dashboard/RiskOverview'
import RiskSection from './dashboard/RiskSection'
import AssessmentControls from './dashboard/AssessmentControls'
import ClimateTabs from './dashboard/ClimateTabs'
import ClimateDetail from './dashboard/ClimateDetail'
import ImpactSection from './dashboard/ImpactSection'

export default function Dashboard() {
  const {
    kommune, assessmentGeoJson, statuses, climateHistory, regionalClimate,
    climateProjection, measures, riskSummary, activeClimateType,
    loadStatuses, loadClimateHistory, loadRegionalClimate, loadClimateProjection,
    loadRiskSummary,
  } = useStore()

  // Climate sub-tab: null = Übersicht, string = specific climate type
  const [climateTab, setClimateTab] = useState<string | null>(null)

  // Load climate data when kommune changes
  useEffect(() => {
    if (!kommune) return
    loadClimateHistory(kommune.id).catch(() => {})
    loadRegionalClimate(kommune.id).catch(() => {})
    loadClimateProjection(kommune.id).catch(() => {})
    loadStatuses(kommune.id).catch(() => {})
    loadRiskSummary(kommune.id).catch(() => {})
  }, [kommune])

  // ── Data for Übersicht charts ─────────────────────────────────────────────
  const rc = regionalClimate as Record<string, unknown> | null

  const historyData: { year: number; hot_days: number; mean_temp: number; summer_max: number }[] = []
  if (climateHistory) {
    const years = (climateHistory.years as number[]) || []
    const hotDays = (climateHistory.hot_days as number[]) || []
    const meanTemp = (climateHistory.mean_temp as number[]) || []
    const summerMax = (climateHistory.summer_max_temp as number[]) || []
    for (let i = 0; i < years.length; i++) {
      historyData.push({
        year: years[i], hot_days: hotDays[i] ?? 0,
        mean_temp: meanTemp[i] ?? 0, summer_max: summerMax[i] ?? 0,
      })
    }
  }

  type ProjectionRow = {
    year: number
    hot_days_hist?: number; mean_temp_hist?: number
    hot_days_rcp45?: number; hot_days_rcp85?: number
    mean_temp_rcp45?: number; mean_temp_rcp85?: number
    tropical_nights_rcp45?: number; tropical_nights_rcp85?: number
  }
  const projectionData: ProjectionRow[] = []
  if (climateProjection || climateHistory) {
    const rowMap = new Map<number, ProjectionRow>()
    if (climateHistory) {
      const years = (climateHistory.years as number[]) || []
      const hotDays = (climateHistory.hot_days as number[]) || []
      const meanTemp = (climateHistory.mean_temp as number[]) || []
      for (let i = 0; i < years.length; i++) {
        rowMap.set(years[i], { year: years[i], hot_days_hist: hotDays[i], mean_temp_hist: meanTemp[i] })
      }
    }
    if (climateProjection) {
      const years = (climateProjection.years as number[]) || []
      const scenarios = climateProjection.scenarios as Record<string, Record<string, unknown>> | undefined
      if (scenarios) {
        const rcp45 = scenarios.rcp45 || {}; const rcp85 = scenarios.rcp85 || {}
        const hd45 = (rcp45.hot_days as number[]) || []; const hd85 = (rcp85.hot_days as number[]) || []
        const mt45 = (rcp45.mean_temp as number[]) || []; const mt85 = (rcp85.mean_temp as number[]) || []
        const tn45 = (rcp45.tropical_nights as number[]) || []; const tn85 = (rcp85.tropical_nights as number[]) || []
        for (let i = 0; i < years.length; i++) {
          const existing = rowMap.get(years[i]) || { year: years[i] }
          rowMap.set(years[i], {
            ...existing,
            hot_days_rcp45: hd45[i], hot_days_rcp85: hd85[i],
            mean_temp_rcp45: mt45[i], mean_temp_rcp85: mt85[i],
            tropical_nights_rcp45: tn45[i], tropical_nights_rcp85: tn85[i],
          })
        }
      }
    }
    Array.from(rowMap.keys()).sort((a, b) => a - b).forEach(y => projectionData.push(rowMap.get(y)!))
  }

  const sortedSummaries = [...riskSummary]
    .filter(s => s.climate_type !== 'health')
    .sort((a, b) => b.aggregated_risk - a.aggregated_risk)

  const measureLabelsMap: Record<string, string> = {
    drinking_fountain: 'Trinkbrunnen', green_roof: 'Dachbegrünung',
    facade_greening: 'Fassadenbegrünung', tree_planting: 'Baumpflanzung',
    unsealing: 'Entsiegelung', shade_structure: 'Verschattung',
  }
  const typeColors: Record<string, string> = {
    drinking_fountain: '#3b82f6', green_roof: '#22c55e', facade_greening: '#10b981',
    tree_planting: '#84cc16', unsealing: '#f59e0b', shade_structure: '#8b5cf6',
  }

  return (
    <div className="dashboard-grid">
      {/* ── Climate Tab Navigation ─────────────────────────────────── */}
      <ClimateTabs activeTab={climateTab} onTabChange={setClimateTab} />

      {/* ── Per-Type Detail View ───────────────────────────────────── */}
      {climateTab !== null ? (
        <ClimateDetail climateType={climateTab} />
      ) : (
        /* ── Übersicht Content ───────────────────────────────────── */
        <>
          {/* Assessment Controls (overview mode with "Alle berechnen") */}
          <AssessmentControls showAllButton />

          {/* Risk Overview (Radar + Top 3) */}
          <RiskOverview />

          {/* Per-Risk Sections */}
          {sortedSummaries.length > 0 && (
            <div className="dashboard-section">
              <h3 className="section-title">Einzelrisiken</h3>
              {sortedSummaries.map(s => (
                <RiskSection
                  key={s.climate_type}
                  summary={s}
                  status={statuses.find(st => st.climate_type === s.climate_type) as AssessmentStatus | undefined}
                />
              ))}
            </div>
          )}

          {/* Regional Climate Info */}
          {rc && (
            <div className="dashboard-section">
              <h3 className="section-title">Regionale Klimadaten (DWD)</h3>
              <div className="kpi-row">
                <div className="kpi-card">
                  <div className="kpi-label">Heiße Tage/Jahr</div>
                  <div className="kpi-value accent">{(rc.hot_days_per_year as number)?.toFixed(1)}</div>
                  <div className="kpi-unit">Tmax ≥ 30°C</div>
                </div>
                <div className="kpi-card">
                  <div className="kpi-label">Sommertage/Jahr</div>
                  <div className="kpi-value">{(rc.summer_days_per_year as number)?.toFixed(0)}</div>
                  <div className="kpi-unit">Tmax ≥ 25°C</div>
                </div>
                <div className="kpi-card">
                  <div className="kpi-label">Tropenächte/Jahr</div>
                  <div className="kpi-value">{(rc.tropical_nights_per_year as number)?.toFixed(1)}</div>
                  <div className="kpi-unit">Tmin ≥ 20°C</div>
                </div>
                <div className="kpi-card">
                  <div className="kpi-label">Sommer-Ø Tmax</div>
                  <div className="kpi-value">{(rc.summer_max_temp_avg as number)?.toFixed(1)}°C</div>
                  <div className="kpi-unit">Referenztemperatur</div>
                </div>
              </div>
            </div>
          )}

          {/* Climate Charts */}
          <div className="dashboard-charts">
            {historyData.length > 0 && (
              <div className="chart-card">
                <h3 className="chart-title">Heiße Tage pro Jahr (ab 1990)</h3>
                <ResponsiveContainer width="100%" height={220}>
                  <BarChart data={historyData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                    <XAxis dataKey="year" tick={{ fontSize: 10 }} />
                    <YAxis tick={{ fontSize: 10 }} />
                    <Tooltip contentStyle={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 6 }} />
                    <Bar dataKey="hot_days" name="Heiße Tage (≥30°C)" fill="#ef4444" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}
            {historyData.length > 0 && (
              <div className="chart-card">
                <h3 className="chart-title">Temperaturentwicklung (ab 1990)</h3>
                <ResponsiveContainer width="100%" height={220}>
                  <LineChart data={historyData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                    <XAxis dataKey="year" tick={{ fontSize: 10 }} />
                    <YAxis tick={{ fontSize: 10 }} domain={['auto', 'auto']} />
                    <Tooltip contentStyle={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 6 }} />
                    <Legend wrapperStyle={{ fontSize: '0.75rem' }} />
                    <Line type="monotone" dataKey="mean_temp" name="Jahresmittel (°C)" stroke="#2563eb" strokeWidth={2} dot={false} />
                    <Line type="monotone" dataKey="summer_max" name="Sommer Ø Tmax (°C)" stroke="#ef4444" strokeWidth={2} dot={false} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>

          {/* Climate Projection */}
          {projectionData.length > 0 && (
            <div className="dashboard-section">
              <h3 className="section-title">Klimafortschreibung (bis 2065)</h3>
              <div className="dashboard-charts">
                <div className="chart-card">
                  <h3 className="chart-title">Heiße Tage – Fortschreibung</h3>
                  <ResponsiveContainer width="100%" height={220}>
                    <LineChart data={projectionData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                      <XAxis dataKey="year" tick={{ fontSize: 10 }} />
                      <YAxis tick={{ fontSize: 10 }} />
                      <Tooltip contentStyle={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 6 }} />
                      <Legend wrapperStyle={{ fontSize: '0.75rem' }} />
                      <Line type="monotone" dataKey="hot_days_hist" name="Historisch" stroke="#64748b" strokeWidth={2} dot={false} />
                      <Line type="monotone" dataKey="hot_days_rcp45" name="RCP 4.5" stroke="#f59e0b" strokeWidth={2} dot={false} strokeDasharray="6 3" />
                      <Line type="monotone" dataKey="hot_days_rcp85" name="RCP 8.5" stroke="#ef4444" strokeWidth={2} dot={false} strokeDasharray="6 3" />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
                <div className="chart-card">
                  <h3 className="chart-title">Jahresmitteltemperatur – Fortschreibung</h3>
                  <ResponsiveContainer width="100%" height={220}>
                    <LineChart data={projectionData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                      <XAxis dataKey="year" tick={{ fontSize: 10 }} />
                      <YAxis tick={{ fontSize: 10 }} domain={['auto', 'auto']} />
                      <Tooltip contentStyle={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 6 }} />
                      <Legend wrapperStyle={{ fontSize: '0.75rem' }} />
                      <Line type="monotone" dataKey="mean_temp_hist" name="Historisch" stroke="#64748b" strokeWidth={2} dot={false} />
                      <Line type="monotone" dataKey="mean_temp_rcp45" name="RCP 4.5" stroke="#2563eb" strokeWidth={2} dot={false} strokeDasharray="6 3" />
                      <Line type="monotone" dataKey="mean_temp_rcp85" name="RCP 8.5" stroke="#ef4444" strokeWidth={2} dot={false} strokeDasharray="6 3" />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          )}

          {/* Measure timeline */}
          {measures.length > 0 && (() => {
            const yearMap = new Map<number, { type: string; count: number }[]>()
            for (const m of measures) {
              const yr = m.implementation_year || 2026
              if (!yearMap.has(yr)) yearMap.set(yr, [])
              const group = yearMap.get(yr)!
              const existing = group.find(g => g.type === m.measure_type)
              if (existing) existing.count++
              else group.push({ type: m.measure_type, count: 1 })
            }
            const years = Array.from(yearMap.keys()).sort((a, b) => a - b)
            const minYear = Math.min(...years) - 1
            const maxYear = Math.max(...years, 2035) + 1
            const allTypes = [...new Set(measures.map(m => m.measure_type))]
            const timelineData: Record<string, number | string>[] = []
            for (let yr = minYear; yr <= maxYear; yr++) {
              const row: Record<string, number | string> = { year: yr }
              const groups = yearMap.get(yr)
              if (groups) for (const g of groups) row[g.type] = g.count
              timelineData.push(row)
            }
            return (
              <div className="dashboard-section">
                <h3 className="section-title">Maßnahmen-Zeitplan</h3>
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart data={timelineData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                    <XAxis dataKey="year" tick={{ fontSize: 10 }} />
                    <YAxis tick={{ fontSize: 10 }} allowDecimals={false} />
                    <Tooltip
                      contentStyle={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 6 }}
                      formatter={(value: unknown, name: unknown) => [String(value), measureLabelsMap[String(name)] || String(name)]}
                    />
                    <Legend wrapperStyle={{ fontSize: '0.75rem' }} formatter={(v: string) => measureLabelsMap[v] || v} />
                    {allTypes.map(t => (
                      <Bar key={t} dataKey={t} stackId="measures" fill={typeColors[t] || '#94a3b8'} radius={[2, 2, 0, 0]} />
                    ))}
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )
          })()}

          {/* Impact Overview (aggregated – only shown after IST calculation) */}
          <ImpactSection />

          {/* Empty state */}
          {statuses.length === 0 && historyData.length === 0 && sortedSummaries.length === 0 && (
            <div className="dashboard-empty">
              <p style={{ fontSize: '1.1rem', marginBottom: '0.5rem' }}>Keine Analyseergebnisse vorhanden</p>
              <p>Wählen Sie oben &quot;▶▶ Alle berechnen&quot; um alle Klimarisiken zu berechnen.</p>
            </div>
          )}
        </>
      )}
    </div>
  )
}
