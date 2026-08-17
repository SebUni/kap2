import { useCallback, useMemo, useState } from 'react'
import {
  Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis,
} from 'recharts'
import LandingMap, { DrawShape } from './LandingMap'
import { MEASURE } from './scenario'
import { evaluateSelection, formatEur } from './miniGameLogic'
import {
  DAMAGE_BY_ID, LANDING_BOUNDS, LANDING_CELLS, MEASURE_CELLS, RISK_LAYERS,
} from './landingData'
import ToolExcerptBadge from './ToolExcerptBadge'

const DAMAGE_LAYER = RISK_LAYERS.find((r) => r.key === 'gebaeudeschaden')!

/**
 * Widget C — „Was schützt am wirksamsten?"
 * Echte OSM-Karte (Oschatz) eingefärbt nach erwartetem Gebäudeschaden; man
 * zeichnet EINE Maßnahmenfläche ein (Rechteck/Polygon, neue ersetzt alte) und
 * das Diagramm vergleicht die Jahreskosten ohne vs. mit Maßnahme.
 */
export default function MeasureGameWidget() {
  const [shape, setShape] = useState<DrawShape>('rect')
  const [coveredIds, setCoveredIds] = useState<ReadonlySet<number>>(new Set())
  const [ring, setRing] = useState<[number, number][] | null>(null)

  const valueForId = useCallback((id: number) => DAMAGE_BY_ID[id] ?? null, [])
  const onCoverage = useCallback((ids: Set<number>, r: [number, number][] | null) => {
    setCoveredIds(ids); setRing(r)
  }, [])
  const reset = () => { setCoveredIds(new Set()); setRing(null) }

  const result = useMemo(() => evaluateSelection(MEASURE_CELLS, coveredIds), [coveredIds])
  const baseline = useMemo(
    () => MEASURE_CELLS.filter((c) => coveredIds.has(c.id)).reduce((s, c) => s + c.schadenEurA, 0),
    [coveredIds],
  )
  const hasMeasure = result.cellCount > 0

  const chartData = useMemo(() => [
    { name: 'Ohne Maßnahme', schaden: baseline, rest: 0, capex: 0, opex: 0 },
    {
      name: 'Mit Maßnahme', schaden: 0,
      rest: Math.max(0, baseline - result.avoidedEurA),
      capex: result.capexEur / MEASURE.lifetimeYears,
      opex: result.opexEurA,
    },
  ], [baseline, result])

  return (
    <div className="landing-widget measure-widget">
      <ToolExcerptBadge />
      <div className="measure-toolbar">
        <span className="measure-name">Maßnahme: <strong>{MEASURE.name}</strong></span>
        <div className="widget-toggle measure-shape" role="tablist" aria-label="Zeichenwerkzeug">
          {(['rect', 'polygon'] as const).map((s) => (
            <button key={s} role="tab" aria-selected={shape === s} className={shape === s ? 'active' : ''} onClick={() => setShape(s)}>
              {s === 'rect' ? '▭ Rechteck' : '⬠ Polygon'}
            </button>
          ))}
        </div>
        <button className="game-reset" onClick={reset} disabled={!hasMeasure}>↺ Zurücksetzen</button>
      </div>

      <div className="measure-body">
        <div className="measure-map-col">
          <LandingMap
            cells={LANDING_CELLS}
            bounds={LANDING_BOUNDS}
            valueForId={valueForId}
            legend={{ label: DAMAGE_LAYER.label, unit: DAMAGE_LAYER.unit }}
            ariaLabel="OSM-Karte von Oschatz zum Einzeichnen einer Anpassungsmaßnahme"
            draw={{ shape, coveredIds, ring, onCoverage }}
          />
          <div className="measure-draw-hint">
            {shape === 'rect' ? 'Ziehen Sie ein Rechteck über das Raster auf.' : 'Ecken klicken, grünen Startpunkt zum Schließen klicken.'}
          </div>
        </div>

        <aside className="measure-dashboard" aria-live="polite">
          {!hasMeasure ? (
            <p className="widget-caption-hint">
              Zeichnen Sie eine Begrünungs-/Entsiegelungsfläche ein — probieren Sie das dicht bebaute,
              versiegelte Zentrum gegen die grünen Ränder. Das Diagramm vergleicht die Jahreskosten ohne
              und mit Maßnahme.
            </p>
          ) : (
            <>
              <div className="measure-chart">
                <ResponsiveContainer width="100%" height={230}>
                  <BarChart data={chartData} margin={{ top: 8, right: 8, bottom: 4, left: 8 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
                    <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                    <YAxis tickFormatter={(v: number) => formatEur(v)} tick={{ fontSize: 10 }} width={54} />
                    <Tooltip formatter={(v) => formatEur(Number(v))} />
                    <Legend wrapperStyle={{ fontSize: '0.72rem' }} />
                    <Bar dataKey="schaden" stackId="a" name="Schaden (ohne)" fill="#dc2626" />
                    <Bar dataKey="rest" stackId="a" name="Restschaden" fill="#fca5a5" />
                    <Bar dataKey="capex" stackId="a" name="CAPEX (annualisiert)" fill="#2563eb" />
                    <Bar dataKey="opex" stackId="a" name="OPEX/Jahr" fill="#d97706" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
              <div className={`measure-verdict ${result.win ? 'is-win' : 'is-lose'}`}>
                {result.win ? '✓ Wirkt' : '✗ Verpufft'}
                <span className="measure-verdict-sub">
                  {result.cellCount} {result.cellCount === 1 ? 'Zelle' : 'Zellen'} ·
                  {result.win && result.amortYears !== null && result.amortYears <= 60
                    ? ` amortisiert nach ca. ${Math.round(result.amortYears)} Jahren`
                    : ' Nutzen unter den laufenden Kosten'}
                </span>
              </div>
              <p className="measure-note">
                {result.win
                  ? 'Der „Mit"-Balken liegt unter „Ohne" — vermiedene Schäden übersteigen CAPEX + OPEX. Genau so priorisiert KAP2, Fläche für Fläche.'
                  : 'Hier ist wenig versiegelt und der Schaden gering — CAPEX + OPEX übersteigen den Nutzen. Dieselbe Maßnahme im Zentrum wirkt.'}
              </p>
            </>
          )}
        </aside>
      </div>
    </div>
  )
}
