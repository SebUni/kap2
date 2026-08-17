import { useState } from 'react'
import type { ReactNode } from 'react'
import { useStore } from '../../store'
import InfoTooltip from '../InfoTooltip'
import ChartSkeleton from './ChartSkeleton'
import { fmtEur, fmtEurCompact, fmtNum } from '../../utils/format'
import {
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  ResponsiveContainer, Tooltip,
} from 'recharts'

const RADAR_HEIGHT = 280

// Netzgrafik-Flächen: gestufte Belastungsbänder statt zweier diskreter Flächen.
// Fünf ineinander liegende Radar-Flächen (P80 → P85 → P90 → P95 → Max) in EINER
// Farbe; da jede Fläche vom Ursprung bis zu ihrem Wert füllt, überlagern sie sich
// und die Alpha-Werte akkumulieren → dichter Kern (bis P80), nach außen zunehmend
// transparenter; das Maximum bleibt als gestrichelte Kontur. Die Statusfarben
// (grün/amber/rot) bleiben den Klassen-Chips der Schadenstreiber vorbehalten; die
// Risikoklassen stehen als Beschriftung DIREKT an der Radialachse (Gering bis 20,
// Mittel bis 50, Hoch bis 100), die über den Flächen liegt.
const BELASTUNG_COLOR = '#2563eb'
const CLASS_TICKS = [20, 50, 100]

// Bänder außen→innen (Max zuunterst, damit die gestrichelte Kontur an der Außen-
// kante sichtbar bleibt); fillOpacity steigt nach innen, sodass die akkumulierte
// Deckkraft von ~0.10 (Rand) bis ~0.54 (Kern) läuft.
type BandKey = 'p80' | 'p85' | 'p90' | 'p95' | 'max'
const RADAR_BANDS: { key: BandKey; fillOpacity: number }[] = [
  { key: 'max', fillOpacity: 0.10 },
  { key: 'p95', fillOpacity: 0.12 },
  { key: 'p90', fillOpacity: 0.14 },
  { key: 'p85', fillOpacity: 0.16 },
  { key: 'p80', fillOpacity: 0.20 },
]

function classTick(value: number): string {
  if (value === 20) return 'Gering'
  if (value === 50) return 'Mittel'
  if (value === 100) return 'Hoch'
  return ''
}

/** Tooltip der Index-Radare: die fünf Stützstellen der Belastungsverteilung. */
function IndexTooltip({ active, payload }: {
  active?: boolean
  payload?: { dataKey?: string | number; payload?: RadarPoint }[]
}) {
  if (!active || !payload?.length) return null
  const point = payload[0]?.payload
  if (!point) return null
  return (
    <div style={{
      background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 6,
      padding: '8px 10px', fontSize: '0.78rem', boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
    }}>
      <div style={{ fontWeight: 600, marginBottom: 4 }}>{point.label}</div>
      <div>Maximum: <b>{fmtNum(point.max)}</b></div>
      <div>P95: <b>{fmtNum(point.p95)}</b></div>
      <div>P90 (Belastung): <b>{fmtNum(point.p90)}</b></div>
      <div>P85: <b>{fmtNum(point.p85)}</b></div>
      <div>P80: <b>{fmtNum(point.p80)}</b></div>
    </div>
  )
}

type RadarPoint = {
  label: string
  p80: number
  p85: number
  p90: number
  p95: number
  max: number
}

/** Index-Netzgrafik: gestufte Belastungsbänder (P80→Max) plus Max-Kontur;
 *  Grid und Radialachse (Risikoklassen) liegen ÜBER den Flächen. */
function IndexRadarChart({ data, color, height, angleFont = 11,
  radiusFont = 9, outerRadius = '70%', maxWidth = 2 }: {
  data: RadarPoint[]
  color: string
  height: number
  angleFont?: number
  radiusFont?: number
  outerRadius?: string
  maxWidth?: number
}) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <RadarChart data={data} outerRadius={outerRadius}>
        {RADAR_BANDS.map(band => (
          <Radar key={band.key} dataKey={band.key} fill={color}
            fillOpacity={band.fillOpacity} isAnimationActive={false}
            stroke={band.key === 'max' ? color : 'none'}
            strokeWidth={band.key === 'max' ? maxWidth : 0}
            strokeDasharray={band.key === 'max' ? '6 4' : undefined} />
        ))}
        {/* Grid + Achsen NACH den Flächen → sie liegen darüber, sodass ablesbar
            bleibt, welches Risiko bis wohin reicht (Klassenachse Gering/Mittel/Hoch). */}
        <PolarGrid />
        <PolarAngleAxis dataKey="label" tick={{ fontSize: angleFont }} />
        <PolarRadiusAxis domain={[0, 100]} ticks={CLASS_TICKS}
          tick={{ fontSize: radiusFont, fill: 'var(--text-muted)' }}
          tickFormatter={classTick} />
        <Tooltip content={<IndexTooltip />} />
      </RadarChart>
    </ResponsiveContainer>
  )
}

/** €-Netzgrafik eines Risikofelds (Skala bis Feld-Maximum). */
function EurRadarChart({ data, color, height, maxCost, angleFont = 8, radiusFont = 8 }: {
  data: { risk: string; cost: number }[]
  color: string
  height: number
  maxCost: number
  angleFont?: number
  radiusFont?: number
}) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <RadarChart data={data} outerRadius="62%">
        <PolarGrid />
        <PolarAngleAxis dataKey="risk" tick={{ fontSize: angleFont }} />
        <PolarRadiusAxis domain={[0, maxCost]} tick={{ fontSize: radiusFont }}
          tickFormatter={(v: number) => fmtEurCompact(v)} />
        <Radar name="Jahresschaden" dataKey="cost" stroke={color} strokeWidth={2}
          fill={color} fillOpacity={0.4} />
        <Tooltip formatter={(v) => [`${fmtEurCompact(Number(v))}/a`, 'Jahresschaden']} />
      </RadarChart>
    </ResponsiveContainer>
  )
}

/** HTML-Legende: Verlaufs-Swatch für die gestuften Belastungsbänder (Kern dicht →
 *  Rand transparent) plus gestrichelte Max-Kontur. */
function SeriesLegend({ color = '#64748b' }: { color?: string }) {
  return (
    <div style={{
      display: 'flex', gap: 16, justifyContent: 'center', flexWrap: 'wrap',
      alignItems: 'center', fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: 4,
    }}>
      <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}>
        <span style={{ display: 'inline-flex', flexShrink: 0, borderRadius: 2, overflow: 'hidden' }}>
          {['8C', '6E', '52', '36', '1A'].map(a => (
            <span key={a} style={{ width: 11, height: 11, background: `${color}${a}` }} />
          ))}
        </span>
        Belastungsstufen P80 → Max (Kern dicht, außen transparent)
      </span>
      <span style={{ display: 'inline-flex', alignItems: 'center', gap: 5 }}>
        <span style={{ width: 16, height: 0, flexShrink: 0, borderTop: `1.5px dashed ${color}` }} />
        Maximum
      </span>
    </div>
  )
}

/** Vollbild-Knopf (⛶) für eine Diagrammkarte. */
function ZoomButton({ onClick }: { onClick: () => void }) {
  return (
    <button onClick={onClick} title="Vollbild" aria-label="Diagramm im Vollbild öffnen"
      style={{
        marginLeft: 'auto', width: 24, height: 24, display: 'inline-flex',
        alignItems: 'center', justifyContent: 'center', flexShrink: 0,
        border: '1px solid var(--border)', borderRadius: 6, cursor: 'pointer',
        background: 'var(--surface)', color: 'var(--text-muted)', fontSize: '0.85rem',
      }}>⛶</button>
  )
}

/** Vollbild-Overlay für ein Diagramm (nutzt die help-overlay-Styles). */
function ChartZoomModal({ title, onClose, children }: {
  title: ReactNode
  onClose: () => void
  children: ReactNode
}) {
  return (
    <div className="help-overlay" onClick={onClose}>
      <div className="help-overlay-content" style={{ maxWidth: 1100 }}
        onClick={e => e.stopPropagation()}>
        <div className="help-overlay-header">
          <h2 style={{ display: 'flex', alignItems: 'center', gap: 8 }}>{title}</h2>
          <button className="help-overlay-close" onClick={onClose} aria-label="Schließen">✕</button>
        </div>
        <div className="help-overlay-body">{children}</div>
      </div>
    </div>
  )
}

function zoomChartHeight(): number {
  return Math.max(380, Math.min(680, Math.round(window.innerHeight * 0.62)))
}

/** Gruppen-Radar: die 5 KWRA-Risikofelder als Netzgrafik (gestufte Belastungsbänder). */
export function GroupRadarCard({ className = '' }: { className?: string }) {
  const { catalog, riskSummary } = useStore()
  const [zoomed, setZoomed] = useState(false)
  const groupOrder = catalog?.groups.map(g => g.code) || []
  const data: RadarPoint[] = groupOrder
    .filter(code => riskSummary?.groups[code])
    .map(code => {
      const g = riskSummary!.groups[code]
      const p90 = g.exposed_index ?? g.index
      const max = Math.max(0, ...g.risk_codes.map(
        rc => riskSummary!.risks[rc]?.max_index || 0))
      return {
        label: g.label,
        p80: g.exposed_p80_index ?? p90,
        p85: g.exposed_p85_index ?? p90,
        p90,
        p95: g.exposed_p95_index ?? p90,
        max: Math.round(max * 10) / 10,
      }
    })
  const bounds = riskSummary?.classification?.bounds ?? { medium_min: 20, high_min: 50 }
  const info = (
    <InfoTooltip title="Belastungs-Index je Risikofeld"
      description={`Gestufte Flächen: die Belastungsverteilung der EXPONIERTEN Zellen (z. B. nur Zellen mit Wohnbevölkerung — unbewohnte Flur verdünnt nicht) je Risikofeld, gemittelt über die Einzelrisiken. Der dichte Kern reicht bis zum P80, nach außen folgen zunehmend transparentere Bänder P85, P90 und P95 bis hin zum Maximum (gestrichelte Kontur, höchster Zell-Index). Innen also die Belastung, die (fast) flächendeckend erreicht wird, außen die lokalen Spitzen. Die Achse ist in Risikoklassen beschriftet: Gering bis ${fmtNum(bounds.medium_min, 0)}, Mittel bis ${fmtNum(bounds.high_min, 0)} (= Risikozonen-Schwelle der Karte), darüber Hoch.`} />
  )

  return (
    <section className={`dashboard-section ${className}`}>
      <h2 className="section-title" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
        Risikofelder (KWRA)
        {info}
        {riskSummary && <ZoomButton onClick={() => setZoomed(true)} />}
      </h2>
      {!riskSummary ? (
        <ChartSkeleton height={RADAR_HEIGHT} label="Risikoindizes werden geladen …" />
      ) : (
        <>
          <IndexRadarChart data={data} color={BELASTUNG_COLOR} height={RADAR_HEIGHT} />
          <SeriesLegend color={BELASTUNG_COLOR} />
          {zoomed && (
            <ChartZoomModal title={<>Risikofelder (KWRA) {info}</>}
              onClose={() => setZoomed(false)}>
              <IndexRadarChart data={data} color={BELASTUNG_COLOR}
                height={zoomChartHeight()} angleFont={13} radiusFont={11} maxWidth={2.5} />
              <SeriesLegend color={BELASTUNG_COLOR} />
            </ChartZoomModal>
          )}
        </>
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
  const benefitDirect = costSummary?.measures.total_benefit_direct_eur ?? 0
  const annualBenefit = (costSummary?.damage_reduction_eur ?? 0) + benefitDirect

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
          {top.map(r => {
            return (
              <div key={r.code}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 6, fontSize: '0.82rem', marginBottom: 2 }}>
                  <span style={{ fontWeight: 500, display: 'inline-flex', alignItems: 'center', gap: 6, minWidth: 0 }}>
                    <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{r.name}</span>
                  </span>
                  <span style={{ fontWeight: 600, whiteSpace: 'nowrap' }}>{fmtEurCompact(r.cost_eur)}/a</span>
                </div>
                <div style={{ height: 6, background: 'var(--bg)', borderRadius: 4, overflow: 'hidden' }}>
                  <div style={{
                    height: '100%', borderRadius: 4, background: 'var(--danger)',
                    width: `${maxCost > 0 ? Math.max(4, (r.cost_eur / maxCost) * 100) : 0}%`,
                    opacity: 0.75,
                  }} />
                </div>
              </div>
            )
          })}
          {!top.length && (
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              Keine monetarisierten Risiken vorhanden.
            </p>
          )}
          {costSummary && (
            <div style={{ display: 'flex', gap: 8, marginTop: 'auto', flexWrap: 'wrap' }}>
              <div className="kpi-card" style={{ flex: '1 1 160px' }}>
                <div className="kpi-label" style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                  Jährlicher Nutzen
                  {costSummary.measures.benefit_consistency_warning && (
                    <span title="Die Pro-Maßnahmen-Nutzenrechnung weicht deutlich von der Aggregat-Differenz ab — Parameter prüfen."
                      style={{ cursor: 'help' }}>⚠️</span>
                  )}
                  <InfoTooltip title="Jährlicher Nutzen der Maßnahmen"
                    description="Vermiedene Schäden (Differenz der aggregierten Jahresschäden ohne/mit Maßnahmen, inkl. gekoppelter Folgekosten) plus direkter Zusatznutzen der Maßnahmen (zusätzlich erwirtschaftete Erträge/Erlöse, z. B. stabilere Ernten oder Energieerträge). Zwei verschiedene Dinge: Schaden, der nicht eintritt, und Gewinn, der dazukommt." />
                </div>
                <div className="kpi-value success" style={{ fontSize: '1rem' }}>
                  {fmtEur(annualBenefit)}<span className="kpi-unit"> /Jahr</span>
                </div>
                <div style={{ fontSize: '0.68rem', color: 'var(--text-muted)', marginTop: 2 }}>
                  davon vermiedene Schäden {fmtEurCompact(costSummary.damage_reduction_eur)}
                  {benefitDirect > 0 && <> · Zusatznutzen {fmtEurCompact(benefitDirect)}</>}
                </div>
              </div>
              <div className="kpi-card" style={{ flex: '1 1 130px' }}>
                <div className="kpi-label" style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                  CAPEX gesamt
                  <InfoTooltip title="Investitionskosten (CAPEX)"
                    description="Einmalige Investitionskosten aller geplanten Maßnahmen (Errichtung, Anschaffung, Umstellung)." />
                </div>
                <div className="kpi-value" style={{ fontSize: '1rem' }}>
                  {fmtEur(costSummary.measures.total_capex_eur)}
                </div>
              </div>
              <div className="kpi-card" style={{ flex: '1 1 130px' }}>
                <div className="kpi-label" style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                  OPEX pro Jahr
                  <InfoTooltip title="Betriebskosten (OPEX)"
                    description="Jährliche Betriebs- und Unterhaltskosten aller geplanten Maßnahmen (Wartung, Pflege, laufender Aufwand)." />
                </div>
                <div className="kpi-value" style={{ fontSize: '1rem' }}>
                  {fmtEur(costSummary.measures.total_opex_annual_eur)}
                  <span className="kpi-unit"> /Jahr</span>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </section>
  )
}

/** Umschalter Index-Ansicht ↔ absolute €-Ansicht der Einzelrisiko-Netzgrafiken. */
function ModeToggle({ mode, onChange }: {
  mode: 'index' | 'eur'
  onChange: (m: 'index' | 'eur') => void
}) {
  return (
    <div style={{
      display: 'inline-flex', border: '1px solid var(--border)', borderRadius: 6,
      overflow: 'hidden', marginLeft: 'auto',
    }}>
      {([['index', 'Index'], ['eur', '€/Jahr']] as const).map(([m, label]) => (
        <button key={m} onClick={() => onChange(m)} style={{
          padding: '4px 12px', fontSize: '0.75rem', fontWeight: 600,
          border: 'none', cursor: 'pointer',
          background: mode === m ? 'var(--primary)' : 'var(--surface)',
          color: mode === m ? '#fff' : 'var(--text-muted)',
        }}>{label}</button>
      ))}
    </div>
  )
}

/** Fünf Netzgrafiken: Einzelrisiken je KWRA-Gruppe (Index- oder €-Ansicht). */
export function GroupRadarGrid({ className = '' }: { className?: string }) {
  const { catalog, riskSummary } = useStore()
  const [mode, setMode] = useState<'index' | 'eur'>('index')
  const [zoomCode, setZoomCode] = useState<string | null>(null)
  const groupOrder = catalog?.groups.map(g => g.code) || []

  return (
    <section className={`dashboard-section ${className}`}>
      <h2 className="section-title" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
        Einzelrisiken je Risikofeld
        <InfoTooltip title="Einzelrisiken je Risikofeld"
          description="Index-Ansicht: gestufte Belastungsbänder je Einzelrisiko — dichter Kern bis P80, nach außen zunehmend transparenter über P85/P90/P95 bis zum Maximum (gestrichelte Kontur); die Achse ist in den Risikoklassen Gering/Mittel/Hoch beschriftet. €-Ansicht: erwarteter Jahresschaden je Einzelrisiko; die Skala reicht bis zum teuersten Risiko des jeweiligen Felds und ist zwischen den Feldern NICHT vergleichbar." />
        {riskSummary && <ModeToggle mode={mode} onChange={setMode} />}
      </h2>
      {!riskSummary ? (
        <ChartSkeleton height={260} label="Risikoindizes werden geladen …" />
      ) : (
        <>
          {mode === 'index' && <div style={{ marginBottom: 8 }}><SeriesLegend /></div>}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1rem' }}>
            {groupOrder.map(code => {
              const g = riskSummary.groups[code]
              if (!g || !g.risk_codes.length) return null
              const grpDef = catalog?.groups.find(x => x.code === code)
              const zoomed = zoomCode === code
              const header = (
                <h3 className="chart-title" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                  <span style={{ color: g.color }}>●</span> {g.label}
                  {grpDef && <InfoTooltip title={g.label} description={grpDef.description} />}
                  <ZoomButton onClick={() => setZoomCode(code)} />
                </h3>
              )
              const zoomTitle = <><span style={{ color: g.color }}>●</span> {g.label}</>

              if (mode === 'eur') {
                const eurData = g.risk_codes.map(rc => ({
                  risk: riskSummary.risks[rc]?.name || rc,
                  cost: riskSummary.risks[rc]?.cost_eur || 0,
                }))
                const maxCost = Math.max(1, ...eurData.map(d => d.cost))
                const scaleNote = (big = false) => (
                  <div style={{ fontSize: big ? '0.78rem' : '0.66rem', color: 'var(--text-muted)', textAlign: 'center' }}>
                    Skala bis Feld-Maximum ({fmtEurCompact(maxCost)}/a)
                  </div>
                )
                return (
                  <div key={code} className="chart-card">
                    {header}
                    <EurRadarChart data={eurData} color={g.color} height={230} maxCost={maxCost} />
                    {scaleNote()}
                    {zoomed && (
                      <ChartZoomModal title={zoomTitle} onClose={() => setZoomCode(null)}>
                        <EurRadarChart data={eurData} color={g.color} maxCost={maxCost}
                          height={zoomChartHeight()} angleFont={12} radiusFont={11} />
                        {scaleNote(true)}
                      </ChartZoomModal>
                    )}
                  </div>
                )
              }

              const data: RadarPoint[] = g.risk_codes.map(rc => {
                const r = riskSummary.risks[rc]
                const p90 = r?.exposed_p90_index ?? r?.index ?? 0
                return {
                  label: r?.name || rc,
                  p80: r?.exposed_p80_index ?? p90,
                  p85: r?.exposed_p85_index ?? p90,
                  p90,
                  p95: r?.exposed_p95_index ?? p90,
                  max: r?.max_index ?? 0,
                }
              })
              return (
                <div key={code} className="chart-card">
                  {header}
                  <IndexRadarChart data={data} color={g.color}
                    height={230} angleFont={8} radiusFont={8} outerRadius="62%"
                    maxWidth={1.75} />
                  {zoomed && (
                    <ChartZoomModal title={zoomTitle} onClose={() => setZoomCode(null)}>
                      <IndexRadarChart data={data} color={g.color}
                        height={zoomChartHeight()} angleFont={12} radiusFont={11} maxWidth={2.5} />
                      <SeriesLegend color={g.color} />
                    </ChartZoomModal>
                  )}
                </div>
              )
            })}
          </div>
        </>
      )}
    </section>
  )
}
