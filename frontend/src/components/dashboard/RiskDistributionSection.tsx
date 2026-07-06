import { useStore } from '../../store'
import InfoTooltip from '../InfoTooltip'
import { fmtEur, LINE_PALETTE } from '../../utils/format'
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Legend,
  ResponsiveContainer, Tooltip,
} from 'recharts'

/** Risikoverteilung: Histogramme + ausklappbare Detailtabellen je Gruppe. */
export default function RiskDistributionSection() {
  const { catalog, riskSummary, riskHistogram } = useStore()
  if (!riskSummary || !riskHistogram) return null
  const groupOrder = catalog?.groups.map(g => g.code) || []

  return (
    <section style={{ marginBottom: '1rem' }}>
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
                            <div className="kpi-label">
                              Ergebnis {r.aggregation === 'p90' ? '(P90 × Kommune)' : '(Σ über Zellen)'}
                            </div>
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
  )
}
