import { useStore } from '../../store'
import InfoTooltip from '../InfoTooltip'
import ChartSkeleton from './ChartSkeleton'
import { fmtEur, fmtEurCompact } from '../../utils/format'
import {
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  ResponsiveContainer, Tooltip,
} from 'recharts'

const RADAR_HEIGHT = 280

/** Gruppen-Radar: die 5 KWRA-Risikofelder als Netzgrafik (P90-Index 0–100). */
export function GroupRadarCard({ className = '' }: { className?: string }) {
  const { catalog, riskSummary } = useStore()
  const groupOrder = catalog?.groups.map(g => g.code) || []
  const data = groupOrder
    .filter(code => riskSummary?.groups[code])
    .map(code => ({
      group: riskSummary!.groups[code].label,
      index: riskSummary!.groups[code].index,
    }))

  return (
    <section className={`dashboard-section ${className}`}>
      <h2 className="section-title" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
        Risikofelder (KWRA)
        <InfoTooltip title="Risikogruppen-Index"
          description="Risikogruppen-Index = Mittel der 90.-Perzentil-Einzelrisiko-Indizes (0–100) je KWRA-Herausforderung. Das P90 hebt belastete Zellen hervor und vermeidet die Verflachung durch viele unbelastete Zellen." />
      </h2>
      {!riskSummary ? (
        <ChartSkeleton height={RADAR_HEIGHT} label="Risikoindizes werden geladen …" />
      ) : (
        <ResponsiveContainer width="100%" height={RADAR_HEIGHT}>
          <RadarChart data={data} outerRadius="70%">
            <PolarGrid />
            <PolarAngleAxis dataKey="group" tick={{ fontSize: 11 }} />
            <PolarRadiusAxis domain={[0, 100]} tick={{ fontSize: 9 }} />
            <Radar name="P90-Index" dataKey="index" stroke="#ef4444" fill="#ef4444" fillOpacity={0.4} />
            <Tooltip />
          </RadarChart>
        </ResponsiveContainer>
      )}
    </section>
  )
}

/** Top-Risiken nach erwartetem Jahresschaden (€) + Maßnahmen-Kurzbilanz. */
export function TopRisksCard({ className = '' }: { className?: string }) {
  const { riskSummary, costSummary } = useStore()
  const byRisk = costSummary?.by_risk || riskSummary?.cost.by_risk || []
  const top = byRisk.filter(r => r.cost_eur > 0).slice(0, 5)
  const maxCost = top.length ? top[0].cost_eur : 0

  return (
    <section className={`dashboard-section ${className}`}>
      <h2 className="section-title" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
        Größte Schadenstreiber
        <InfoTooltip title="Top-Risiken nach €"
          description="Die fünf Risiken mit dem höchsten erwarteten Jahresschaden (mit Maßnahmen, falls vorhanden). Vollständige Tabelle unter „Details“ am Seitenende." />
      </h2>
      {!riskSummary ? (
        <ChartSkeleton height={RADAR_HEIGHT} label="Kostendaten werden geladen …" />
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8, minHeight: RADAR_HEIGHT }}>
          {top.map(r => (
            <div key={r.code}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: 2 }}>
                <span style={{ fontWeight: 500 }}>{r.name}</span>
                <span style={{ fontWeight: 600 }}>{fmtEurCompact(r.cost_eur)}/a</span>
              </div>
              <div style={{ height: 6, background: 'var(--bg)', borderRadius: 4, overflow: 'hidden' }}>
                <div style={{
                  height: '100%', borderRadius: 4, background: 'var(--danger)',
                  width: `${maxCost > 0 ? Math.max(4, (r.cost_eur / maxCost) * 100) : 0}%`,
                  opacity: 0.75,
                }} />
              </div>
            </div>
          ))}
          {!top.length && (
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              Keine monetarisierten Risiken vorhanden.
            </p>
          )}
          {costSummary && (
            <div style={{ display: 'flex', gap: 8, marginTop: 'auto', flexWrap: 'wrap' }}>
              <div className="kpi-card" style={{ flex: '1 1 140px' }}>
                <div className="kpi-label">Vermiedene Schäden</div>
                <div className="kpi-value success" style={{ fontSize: '1rem' }}>
                  {fmtEur(costSummary.damage_reduction_eur)}<span className="kpi-unit"> /Jahr</span>
                </div>
              </div>
              <div className="kpi-card" style={{ flex: '1 1 140px' }}>
                <div className="kpi-label">Maßnahmen-CAPEX gesamt</div>
                <div className="kpi-value" style={{ fontSize: '1rem' }}>
                  {fmtEur(costSummary.measures.total_capex_eur)}
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </section>
  )
}

/** Fünf Netzgrafiken: Einzelrisiko-Indizes je KWRA-Gruppe. */
export function GroupRadarGrid({ className = '' }: { className?: string }) {
  const { catalog, riskSummary } = useStore()
  const groupOrder = catalog?.groups.map(g => g.code) || []

  return (
    <section className={`dashboard-section ${className}`}>
      <h2 className="section-title">Einzelrisiken je Risikofeld</h2>
      {!riskSummary ? (
        <ChartSkeleton height={260} label="Risikoindizes werden geladen …" />
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1rem' }}>
          {groupOrder.map(code => {
            const g = riskSummary.groups[code]
            if (!g || !g.risk_codes.length) return null
            const data = g.risk_codes.map(rc => ({
              risk: riskSummary.risks[rc]?.name || rc,
              index: riskSummary.risks[rc]?.index || 0,
            }))
            const grpDef = catalog?.groups.find(x => x.code === code)
            return (
              <div key={code} className="chart-card">
                <h3 className="chart-title" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                  <span style={{ color: g.color }}>●</span> {g.label}
                  {grpDef && <InfoTooltip title={g.label} description={grpDef.description} />}
                </h3>
                <ResponsiveContainer width="100%" height={230}>
                  <RadarChart data={data} outerRadius="62%">
                    <PolarGrid />
                    <PolarAngleAxis dataKey="risk" tick={{ fontSize: 8 }} />
                    <PolarRadiusAxis domain={[0, 100]} tick={{ fontSize: 7 }} />
                    <Radar name="P90-Index" dataKey="index" stroke={g.color} fill={g.color} fillOpacity={0.4} />
                    <Tooltip />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            )
          })}
        </div>
      )}
    </section>
  )
}
