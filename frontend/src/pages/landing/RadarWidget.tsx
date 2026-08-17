import { useState } from 'react'
import {
  PolarAngleAxis, PolarGrid, PolarRadiusAxis, Radar, RadarChart, ResponsiveContainer,
} from 'recharts'
import { RADAR_FIELDS } from './scenario'
import ToolExcerptBadge from './ToolExcerptBadge'

type Mode = 'index' | 'euro'

const BELASTUNG_COLOR = '#2563eb'
const CLASS_TICKS = [20, 50, 100]

function classTick(value: number): string {
  if (value === 20) return 'Gering'
  if (value === 50) return 'Mittel'
  if (value === 100) return 'Hoch'
  return ''
}

/** 45°-Schraffur für die Hotspot-Fläche (SVG-Pattern) — wie im echten Radar. */
function HatchDefs({ id, color }: { id: string; color: string }) {
  return (
    <defs>
      <pattern id={id} patternUnits="userSpaceOnUse" width={5} height={5} patternTransform="rotate(45)">
        <line x1="0" y1="0" x2="0" y2="5" stroke={color} strokeWidth={1.4} opacity={0.4} />
      </pattern>
    </defs>
  )
}

/** HTML-Legende mit Muster-Swatches (Recharts kann Schraffur nicht abbilden). */
function SeriesLegend({ color }: { color: string }) {
  const swatch = { width: 16, height: 11, borderRadius: 2, flexShrink: 0 } as const
  return (
    <div className="radar-series-legend">
      <span>
        <span style={{ ...swatch, background: `${color}4D`, border: `2px solid ${color}` }} />
        Belastung (P90 exponierter Zellen)
      </span>
      <span>
        <span style={{
          ...swatch,
          background: `repeating-linear-gradient(45deg, ${color}66 0 2px, transparent 2px 5px)`,
          border: `1.5px dashed ${color}`,
        }} />
        Hotspot (Maximum)
      </span>
    </div>
  )
}

/**
 * Widget A — „Wo trifft uns der Klimawandel am härtesten?"
 * Netzdiagramm der 5 KWRA-Risikofelder wie im Tool: „Belastung" (gefüllt) plus
 * „Hotspot (Maximum)" (gestrichelt/schraffiert). Umschaltbar KWRA-Index ↔ €/Jahr.
 */
export default function RadarWidget() {
  const [mode, setMode] = useState<Mode>('index')
  const [focus, setFocus] = useState<string | null>(null)

  const data = RADAR_FIELDS.map((f) => ({
    feld: f.feld,
    belastung: f.index,
    hotspot: f.hotspot,
    euro: f.mioEurA,
  }))
  const maxEuro = Math.ceil(Math.max(...RADAR_FIELDS.map((f) => f.mioEurA)) * 1.15 * 10) / 10
  const focused = RADAR_FIELDS.find((f) => f.feld === focus) ?? null

  return (
    <div className="landing-widget">
      <ToolExcerptBadge />
      <div className="widget-toggle" role="tablist" aria-label="Ansicht wählen">
        <button role="tab" aria-selected={mode === 'index'} className={mode === 'index' ? 'active' : ''}
          onClick={() => setMode('index')}>KWRA-Index</button>
        <button role="tab" aria-selected={mode === 'euro'} className={mode === 'euro' ? 'active' : ''}
          onClick={() => setMode('euro')}>€/Jahr</button>
      </div>
      <div className="radar-chart-box">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart data={data} outerRadius="72%" margin={{ top: 8, right: 24, bottom: 8, left: 24 }}>
            <PolarGrid stroke="var(--border)" />
            <PolarAngleAxis
              dataKey="feld"
              tick={({ payload, x, y, textAnchor }) => (
                <text
                  x={x} y={y} textAnchor={textAnchor} fontSize={11.5}
                  fill={focus === payload.value ? 'var(--primary)' : 'var(--text-muted)'}
                  fontWeight={focus === payload.value ? 700 : 400}
                  style={{ cursor: 'pointer' }}
                  onClick={() => setFocus(focus === payload.value ? null : String(payload.value))}
                >
                  {String(payload.value).split('/').map((part: string, i: number, arr: string[]) => (
                    <tspan key={i} x={x} dy={i === 0 ? 0 : 13}>{part}{i < arr.length - 1 ? '/' : ''}</tspan>
                  ))}
                </text>
              )}
            />
            {mode === 'index' ? (
              <>
                <PolarRadiusAxis angle={90} domain={[0, 100]} ticks={CLASS_TICKS}
                  tick={{ fontSize: 9.5, fill: 'var(--text-muted)' }} tickFormatter={classTick}
                  stroke="var(--border)" />
                <HatchDefs id="landing-hatch" color={BELASTUNG_COLOR} />
                <Radar name="Hotspot (Maximum)" dataKey="hotspot" stroke={BELASTUNG_COLOR}
                  strokeWidth={2} strokeDasharray="6 4" fill="url(#landing-hatch)" fillOpacity={1}
                  isAnimationActive animationDuration={450} />
                <Radar name="Belastung" dataKey="belastung" stroke={BELASTUNG_COLOR} strokeWidth={2}
                  fill={BELASTUNG_COLOR} fillOpacity={0.3} isAnimationActive animationDuration={450}
                  dot={{ r: 3, fill: BELASTUNG_COLOR, strokeWidth: 0 }} />
              </>
            ) : (
              <>
                <PolarRadiusAxis angle={90} domain={[0, maxEuro]}
                  tick={{ fontSize: 9.5, fill: 'var(--text-muted)' }} tickCount={5} stroke="var(--border)" />
                <Radar name="Jahresschaden" dataKey="euro" stroke="var(--primary)" strokeWidth={2}
                  fill="var(--primary)" fillOpacity={0.16} isAnimationActive animationDuration={450}
                  dot={{ r: 3.5, fill: 'var(--primary)', strokeWidth: 0 }} />
              </>
            )}
          </RadarChart>
        </ResponsiveContainer>
      </div>
      {mode === 'index' && <SeriesLegend color={BELASTUNG_COLOR} />}
      <div className="widget-caption" aria-live="polite">
        {focused ? (
          mode === 'index' ? (
            <><strong>{focused.feld}:</strong> Belastung {focused.index} · Hotspot {focused.hotspot} / 100
              — größter Treiber: {focused.topTreiber}</>
          ) : (
            <><strong>{focused.feld}:</strong> ≈ {focused.mioEurA.toLocaleString('de-DE')} Mio €/Jahr
              erwarteter Schaden — größter Treiber: {focused.topTreiber}</>
          )
        ) : mode === 'euro' ? (
          <span className="widget-caption-hint">
            Erwartete Schäden in Mio €/Jahr — was Nichtstun heute schon kostet. Feld antippen für Details.
          </span>
        ) : null}
      </div>
    </div>
  )
}
