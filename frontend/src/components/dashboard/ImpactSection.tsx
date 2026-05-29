import { useStore } from '../../store'
import { IMPACT_DATA, GERMANY_POPULATION } from '../../data/impactData'
import type { ImpactCategory } from '../../data/impactData'
import { CLIMATE_TYPE_META } from '../../types'
import {
  BarChart, Bar, XAxis, YAxis,
  Tooltip, ResponsiveContainer, Cell,
} from 'recharts'

interface Props {
  /** Show impacts for one climate type, or null for aggregated overview */
  climateType?: string | null
}

export default function ImpactSection({ climateType }: Props) {
  const { kommune, riskSummary, statuses, measures } = useStore()

  // ── Guard: only show after at least one IST calculation is done ───────────
  const hasCompleted = climateType
    ? statuses.some(s => s.climate_type === climateType && s.status === 'done')
    : statuses.some(s => s.status === 'done')

  if (!hasCompleted || !kommune) return null

  const population = kommune.population || 0
  if (population === 0) return null   // can't scale without population

  const popFactor = population / GERMANY_POPULATION
  const hasMeasures = measures.length > 0

  // Risk-score weighting
  const riskScale = (ct: string) => {
    const s = riskSummary.find(r => r.climate_type === ct)
    return s ? Math.max(0.5, s.aggregated_risk / 5) : 1.0
  }

  // Convert national reference value → absolute kommun value
  const toAbsolute = (cat: ImpactCategory, ct: string, value: number): number => {
    if (cat.perCapita) {
      // per-100k rate → absolute persons
      return value * (population / 100_000) * riskScale(ct)
    }
    // national monetary total → kommun proportion
    return value * popFactor * riskScale(ct)
  }

  // Measures reduction: each measure reduces ~4% of projected increase, capped at 50%
  const measureFactor = hasMeasures ? Math.min(measures.length * 0.04, 0.5) : 0
  const withMeasures = (ist: number, projected: number) =>
    ist + (projected - ist) * (1 - measureFactor)

  // Unified formatting (toAbsolute already gives kommun-level raw number)
  const fmt = (v: number, cat: ImpactCategory): string => {
    if (cat.perCapita) {
      if (v >= 1000) return Math.round(v).toLocaleString('de-DE')
      if (v >= 10) return v.toFixed(0)
      if (v >= 1) return v.toFixed(1)
      if (v >= 0.01) return v.toFixed(2)
      return '< 0.01'
    }
    // Monetary: toAbsolute gives value in original unit * popFactor (e.g. 6.5 Mrd * 0.000166 = 0.00108 Mrd)
    // Convert to €
    const multiplier = cat.unit.includes('Mrd') ? 1e9 : cat.unit.includes('Mio') ? 1e6 : 1
    const euros = v * multiplier
    if (euros >= 1e6) return (euros / 1e6).toFixed(1) + ' Mio. €'
    if (euros >= 1e3) return Math.round(euros / 1e3).toLocaleString('de-DE') + ' Tsd. €'
    return Math.round(euros).toLocaleString('de-DE') + ' €'
  }

  const unitLabel = (cat: ImpactCategory): string => {
    if (cat.perCapita) return 'Personen / Jahr'
    return '€ / Jahr'
  }

  const typesToShow = climateType ? [climateType] : Object.keys(IMPACT_DATA)

  return (
    <div className="dashboard-section">
      <h3 className="section-title">
        {climateType
          ? `${CLIMATE_TYPE_META[climateType]?.icon} Gesellschaftliche Auswirkungen – ${CLIMATE_TYPE_META[climateType]?.label}`
          : '⚠️ Gesellschaftliche & Wirtschaftliche Auswirkungen'}
      </h3>
      <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: 16, marginTop: -4 }}>
        Absolute Werte für {kommune.name} ({population.toLocaleString('de-DE')} EW).
        {' '}IST (aktuell) → Projektion 2050 ohne Maßnahmen.
        {hasMeasures && ` → Geschätzte Wirkung Ihrer ${measures.length} Maßnahme(n).`}
      </p>

      {typesToShow.map(ct => {
        const data = IMPACT_DATA[ct]
        if (!data) return null
        const meta = CLIMATE_TYPE_META[ct]

        // For single-type mode, check if that type's assessment is done
        if (climateType && !statuses.some(s => s.climate_type === ct && s.status === 'done')) return null

        return (
          <div key={ct} style={{ marginBottom: 20 }}>
            {!climateType && (
              <div style={{
                display: 'flex', alignItems: 'center', gap: 6, marginBottom: 10,
                fontSize: '0.85rem', fontWeight: 600,
              }}>
                <span>{meta?.icon}</span>
                <span>{data.label}</span>
                <span style={{ fontSize: '0.72rem', fontWeight: 400, color: 'var(--text-muted)', marginLeft: 8 }}>
                  {data.summary}
                </span>
              </div>
            )}

            {data.categories.map(cat => {
              const cur = toAbsolute(cat, ct, cat.current)
              const p45 = toAbsolute(cat, ct, cat.projected45)
              const p85 = toAbsolute(cat, ct, cat.projected85)
              const mit = hasMeasures ? withMeasures(cur, p85) : 0

              const chartData = [
                { name: 'IST', value: cur },
                { name: 'RCP 4.5', value: p45 },
                { name: 'RCP 8.5', value: p85 },
                ...(hasMeasures ? [{ name: `${measures.length} Maßn.`, value: mit }] : []),
              ]
              const barColors = hasMeasures
                ? ['#64748b', '#f59e0b', '#ef4444', '#22c55e']
                : ['#64748b', '#f59e0b', '#ef4444']

              return (
                <div key={cat.label} className="impact-card">
                  <div className="impact-card-header">
                    <span className="impact-icon">{cat.icon}</span>
                    <div>
                      <div style={{ fontWeight: 600, fontSize: '0.82rem' }}>{cat.label}</div>
                      <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>{cat.source}</div>
                    </div>
                    <div style={{ marginLeft: 'auto', fontSize: '0.65rem', color: 'var(--text-muted)' }}>
                      {unitLabel(cat)}
                    </div>
                  </div>

                  <div className="impact-comparison">
                    <div className="impact-col">
                      <div className="impact-col-label">IST (aktuell)</div>
                      <div className="impact-col-value" style={{ color: '#64748b' }}>
                        {fmt(cur, cat)}
                      </div>
                    </div>
                    <div className="impact-arrow">→</div>
                    <div className="impact-col">
                      <div className="impact-col-label">2050 (RCP 4.5)</div>
                      <div className="impact-col-value" style={{ color: '#f59e0b' }}>
                        {fmt(p45, cat)}
                      </div>
                      <div className="impact-col-unit">
                        <span style={{ color: '#f59e0b', fontWeight: 600 }}>
                          +{((p45 / cur - 1) * 100).toFixed(0)}%
                        </span>
                      </div>
                    </div>
                    <div className="impact-arrow">→</div>
                    <div className="impact-col">
                      <div className="impact-col-label">2050 (RCP 8.5)</div>
                      <div className="impact-col-value" style={{ color: '#ef4444' }}>
                        {fmt(p85, cat)}
                      </div>
                      <div className="impact-col-unit">
                        <span style={{ color: '#ef4444', fontWeight: 600 }}>
                          +{((p85 / cur - 1) * 100).toFixed(0)}%
                        </span>
                      </div>
                    </div>
                    {hasMeasures && (
                      <>
                        <div className="impact-arrow">→</div>
                        <div className="impact-col">
                          <div className="impact-col-label">{measures.length} Maßnahme(n)</div>
                          <div className="impact-col-value" style={{ color: '#22c55e' }}>
                            {fmt(mit, cat)}
                          </div>
                          <div className="impact-col-unit">
                            <span style={{ color: '#22c55e', fontWeight: 600 }}>
                              −{((1 - mit / p85) * 100).toFixed(0)}% ggü. RCP 8.5
                            </span>
                          </div>
                        </div>
                      </>
                    )}
                  </div>

                  {/* Mini bar chart */}
                  <div style={{ height: hasMeasures ? 64 : 50, marginTop: 4 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={chartData} layout="vertical" margin={{ left: 50, right: 10 }}>
                        <XAxis type="number" hide />
                        <YAxis type="category" dataKey="name" tick={{ fontSize: 9 }} width={55} />
                        <Tooltip
                          contentStyle={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 6, fontSize: '0.75rem' }}
                          formatter={(v: unknown) => fmt(Number(v), cat)}
                        />
                        <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                          {chartData.map((_, i) => (
                            <Cell key={i} fill={barColors[i]} />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              )
            })}
          </div>
        )
      })}
    </div>
  )
}
