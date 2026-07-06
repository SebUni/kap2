import { useState } from 'react'
import { useStore } from '../../store'
import InfoTooltip from '../InfoTooltip'
import ChartSkeleton from './ChartSkeleton'
import { fmtEur, fmtEurCompact } from '../../utils/format'
import {
  ComposedChart, Line, Area, Bar, XAxis, YAxis, CartesianGrid,
  Legend, Tooltip, ResponsiveContainer,
} from 'recharts'

const CHART_HEIGHT = 'min(300px, 34vh)'

type Scenario = 'rcp45' | 'rcp85'
type Mode = 'annual' | 'cumulative'

function ToggleGroup<T extends string>({ value, onChange, options }: {
  value: T
  onChange: (v: T) => void
  options: { value: T; label: string }[]
}) {
  return (
    <div style={{ display: 'inline-flex', border: '1px solid var(--border)', borderRadius: 8, overflow: 'hidden' }}>
      {options.map(o => (
        <button
          key={o.value}
          onClick={() => onChange(o.value)}
          style={{
            border: 'none', cursor: 'pointer', fontSize: '0.75rem', padding: '4px 10px',
            background: value === o.value ? 'var(--primary)' : 'transparent',
            color: value === o.value ? '#fff' : 'var(--text)',
          }}
        >
          {o.label}
        </button>
      ))}
    </div>
  )
}

/**
 * Centerpiece des Dashboards: Kostenentwicklung 2025–2065 als zwei Pfade —
 * ohne Maßnahmen vs. mit Maßnahmen (inkl. eingepreister CAPEX/OPEX), mit
 * Differenzfläche „vermiedene Schäden" und CAPEX-Spitzen als Balken.
 */
export default function CostTimelineSection({ className = '' }: { className?: string }) {
  const { costProjection } = useStore()
  const [scenario, setScenario] = useState<Scenario>('rcp45')
  const [mode, setMode] = useState<Mode>('annual')

  const proj = costProjection
  const scen = proj?.scenarios[scenario]

  const data = proj && scen
    ? proj.years.map((year, i) => {
        const ohne = scen.no_measures[mode][i]
        const mit = proj.has_measures ? scen.with_measures[mode][i] : null
        return {
          year,
          ohne,
          mit,
          band: mit !== null ? [Math.min(mit, ohne), Math.max(mit, ohne)] : null,
          capex: mode === 'annual' && proj.has_measures ? scen.with_measures.components.capex[i] : null,
        }
      })
    : []

  return (
    <section className={`dashboard-section ${className}`}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, flexWrap: 'wrap', marginBottom: 6 }}>
        <h2 className="section-title" style={{ margin: 0, display: 'flex', alignItems: 'center', gap: 6 }}>
          Kostenentwicklung durch den Klimawandel
          <InfoTooltip
            title="Kosten-Projektion 2025–2065"
            description={proj
              ? `${proj.assumptions.join(' · ')}${proj.source ? ` · Quelle Klimasignal: ${proj.source}` : ''}`
              : 'Erwartete Jahresschäden, skaliert mit dem regionalisierten DWD-Klimatrend; Maßnahmenpfad inkl. CAPEX/OPEX.'}
          />
        </h2>
        <div style={{ marginLeft: 'auto', display: 'flex', gap: 8 }}>
          <ToggleGroup value={scenario} onChange={setScenario} options={[
            { value: 'rcp45', label: 'RCP 4.5' },
            { value: 'rcp85', label: 'RCP 8.5' },
          ]} />
          <ToggleGroup value={mode} onChange={setMode} options={[
            { value: 'annual', label: 'jährlich' },
            { value: 'cumulative', label: 'kumuliert' },
          ]} />
        </div>
      </div>

      {!proj ? (
        <ChartSkeleton height={CHART_HEIGHT} label="Kostenprojektion wird berechnet …" />
      ) : (
        <>
          <div style={{ width: '100%', height: CHART_HEIGHT }}>
            <ResponsiveContainer width="100%" height="100%">
              <ComposedChart data={data} margin={{ top: 8, right: 16, bottom: 4, left: 8 }}>
                <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
                <XAxis dataKey="year" tick={{ fontSize: 10 }} />
                <YAxis
                  tick={{ fontSize: 10 }}
                  tickFormatter={(v: number) => fmtEurCompact(v)}
                  width={80}
                />
                <Tooltip
                  formatter={(value, name) => {
                    if (typeof value !== 'number') return [null, null]
                    return [fmtEur(value), String(name)]
                  }}
                  labelFormatter={(l) => `Jahr ${l}`}
                  wrapperStyle={{ fontSize: 12 }}
                />
                <Legend wrapperStyle={{ fontSize: 11 }} />
                {proj.has_measures && (
                  <Area
                    dataKey="band"
                    name="Vermiedene Schäden"
                    stroke="none"
                    fill="var(--success)"
                    fillOpacity={0.12}
                    legendType="rect"
                    isAnimationActive={false}
                  />
                )}
                {proj.has_measures && mode === 'annual' && (
                  <Bar dataKey="capex" name="CAPEX (einmalig)" fill="#94a3b8" barSize={6} />
                )}
                <Line
                  dataKey="ohne" name="Ohne Maßnahmen" type="monotone"
                  stroke="var(--danger)" strokeWidth={2.5} dot={false}
                />
                {proj.has_measures && (
                  <Line
                    dataKey="mit" name="Mit Maßnahmen (inkl. Kosten)" type="monotone"
                    stroke="var(--primary)" strokeWidth={2.5} dot={false}
                  />
                )}
              </ComposedChart>
            </ResponsiveContainer>
          </div>
          <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: 4 }}>
            {!proj.has_measures && (
              <span style={{ marginRight: 10 }}>
                Noch keine Maßnahmen erfasst — der Pfad „mit Maßnahmen" erscheint, sobald Maßnahmen angelegt und berechnet sind.
              </span>
            )}
            {proj.warnings.map((w, i) => (
              <span key={i} style={{ color: 'var(--warning)', marginRight: 10 }}>⚠ {w}</span>
            ))}
          </div>
        </>
      )}
    </section>
  )
}
