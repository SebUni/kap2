import { useMemo, useState } from 'react'
import { MEASURE } from './scenario'
import { evaluateSelection, formatEur } from './miniGameLogic'
import { MEASURE_CELLS, SAMPLE_MEASURE_IDS } from './landingData'
import ToolExcerptBadge from './ToolExcerptBadge'

const DEFAULT_CAPEX = MEASURE.capexPerM2Desiegelung // Katalog-Standard: 35 €/m²

interface Row {
  label: string
  value: string
  unit: string
  source: string
}

/** Feste Katalog-Parameter (Anzeige) — nur der Entsiegelungs-CAPEX ist editierbar. */
const STATIC_ROWS: Row[] = [
  { label: 'Stadtgrün — Kosten je m²', value: '25', unit: '€/m²', source: 'KAP2-Maßnahmenkatalog · Stadtgrün' },
  { label: 'Entsiegelung + Grün — OPEX', value: '3,5', unit: '€/m²·a', source: 'KAP2-Maßnahmenkatalog · Pflege' },
  { label: 'Kombinierte Wirkung (Reduktion)', value: '0,48', unit: '—', source: '1 − (1−0,30)(1−0,25)' },
]

/**
 * Mini-Widget D — Parameter zum Anfassen (Transparenz-Sektion).
 * Kompakte Version der echten ParameterTable: Wert/Einheit/Quelle je Zeile,
 * ein editierbarer Katalog-Parameter (Entsiegelungs-CAPEX) mit Pflicht-Quelle
 * bei Abweichung — die Beispielrechnung aus Widget C zieht live mit.
 */
export default function ParamSliderWidget() {
  const [capexRaw, setCapexRaw] = useState<string>(String(DEFAULT_CAPEX))
  const capex = Number(capexRaw.replace(',', '.')) || 0
  const changed = capex !== DEFAULT_CAPEX
  const [source, setSource] = useState('')

  const combined = capex + MEASURE.capexPerM2Gruen
  const result = useMemo(() => evaluateSelection(MEASURE_CELLS, SAMPLE_MEASURE_IDS, combined), [combined])
  const defaultResult = useMemo(
    () => evaluateSelection(MEASURE_CELLS, SAMPLE_MEASURE_IDS, DEFAULT_CAPEX + MEASURE.capexPerM2Gruen), [],
  )
  const sourceMissing = changed && source.trim() === ''

  return (
    <div className="landing-widget mini-widget">
      <ToolExcerptBadge />
      <h4>Ein Parameter von über 400 — mit Wert, Einheit und Quelle</h4>
      <div className="kap-param-table landing-param-table">
        <table>
          <thead>
            <tr>
              <th className="kap-param-col-label">Parameter</th>
              <th className="kap-param-th-value">Wert</th>
              <th className="kap-param-td-unit">Einheit</th>
              <th className="kap-param-col-source">Quelle</th>
            </tr>
          </thead>
          <tbody>
            <tr className={changed ? 'overridden' : ''}>
              <td>
                Entsiegelung — Kosten je m²
                {changed && <span className="kap-param-status is-override"> · geändert</span>}
              </td>
              <td className="kap-param-td-value">
                <input
                  type="number" min={20} max={120} step={5} value={capexRaw}
                  onChange={(e) => setCapexRaw(e.target.value)}
                  aria-label="Entsiegelungskosten je Quadratmeter"
                  className="landing-param-input"
                />
              </td>
              <td className="kap-param-td-unit">€/m²</td>
              <td>
                {changed ? (
                  <input
                    type="text" value={source} placeholder="Eigene Quelle angeben …"
                    onChange={(e) => setSource(e.target.value)}
                    aria-label="Quelle für den geänderten Wert"
                    className={`landing-param-input${sourceMissing ? ' is-missing' : ''}`}
                  />
                ) : (
                  <span className="kap-param-value">KAP2-Maßnahmenkatalog (35 €/m², quellenbelegt)</span>
                )}
              </td>
            </tr>
            {STATIC_ROWS.map((r) => (
              <tr key={r.label}>
                <td>{r.label}</td>
                <td className="kap-param-td-value kap-param-value">{r.value}</td>
                <td className="kap-param-td-unit">{r.unit}</td>
                <td className="kap-param-value">{r.source}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {sourceMissing && (
        <p className="landing-param-warn">⚠ Abweichung vom Standardwert — im Produkt ist hier eine Quellenangabe Pflicht.</p>
      )}
      <div className="param-effect">
        ↓ wirkt sofort auf die Beispielmaßnahme (die 4 wirksamsten Zellen im Zentrum):
        <div className="param-effect-values">
          <span>
            CAPEX{' '}
            <strong>
              {formatEur(defaultResult.capexEur)}
              {result.capexEur !== defaultResult.capexEur && <> → {formatEur(result.capexEur)}</>}
            </strong>
          </span>
          <span>
            Amortisation{' '}
            <strong>
              {defaultResult.amortYears !== null && `${Math.round(defaultResult.amortYears)} J.`}
              {result.amortYears !== null && result.amortYears !== defaultResult.amortYears &&
                <> → {Math.round(result.amortYears)} J.</>}
            </strong>
          </span>
        </div>
      </div>
      <p className="mini-widget-quote">
        „Ihre Kämmerei rechnet mit anderen Sätzen? In KAP2 ändern Sie den
        Parameter — mit eigener Quelle, nicht das Vertrauen in die Rechnung."
      </p>
    </div>
  )
}
