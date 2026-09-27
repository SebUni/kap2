import { Fragment } from 'react'
import { useStore } from '../../store'
import InfoTooltip from '../InfoTooltip'
import { fmtEur } from '../../utils/format'
import type { RiskAggregate } from '../../types'

type Zeile = RiskAggregate['cost']['by_risk'][number]

/** Höchstens so viele Klimawirkungen (Teilzeilen zählen nicht mit). */
const MAX_BLOECKE = 20

/** Kostentabellen: erwartete Schäden je Risiko + Maßnahmen-CAPEX/OPEX/Nutzen. */
export default function CostTablesSection() {
  const { riskSummary, costSummary } = useStore()
  if (!riskSummary) return null

  const byRisk = costSummary?.by_risk || riskSummary.cost.by_risk
  const byRiskCode = new Map(byRisk.map(z => [z.code, z]))
  const klimawirkungen = costSummary?.klimawirkungen || riskSummary.cost.klimawirkungen

  return (
    <section>
      <h2 className="section-title">Kostentabellen</h2>
      <div className="chart-card">
        <h3 className="chart-title" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          Erwartete Schäden je Risiko
          <InfoTooltip title="Aggregation je Risiko"
            description="Schaden/Jahr = Σ über alle 100m-Zellen (bevölkerungs-/flächenbezogene Risiken) bzw. P90-Index × Kommune (Ausfall-/Screening-Risiken, nicht zell-additiv). Der Gesamtschaden ist die nachrechenbare Summe dieser Zeilen – ohne nicht-additive Teilkennzahlen (z. B. Restaurierung, = Anteil bereits gezählter Sektorschäden)." />
        </h3>
        <table className="data-table">
          <thead>
            <tr>
              <th>Risiko</th>
              <th style={{ textAlign: 'right' }}>Index</th>
              <th style={{ textAlign: 'right' }}>Ergebnis</th>
              <th style={{ textAlign: 'right' }}>Schaden/Jahr</th>
            </tr>
          </thead>
          <tbody>
            {/* Die Grenze zählt Klimawirkungen, nicht Zeilen: Teilzeilen einer angezeigten
                Klimawirkung werden nie abgeschnitten (T-1432, T-1474-cto: Gruppierung
                kommt serverseitig aus cost.klimawirkungen, nicht mehr aus einer eigenen
                Frontend-Regel). */}
            {klimawirkungen.slice(0, MAX_BLOECKE).map(k => {
              if (k.teile.length > 0) {
                return (
                  <Fragment key={`kwra-${k.kwra_id}`}>
                    <tr>
                      <td style={{ fontWeight: 600 }}>{k.bezeichnung}</td>
                      <td />
                      <td />
                      <td style={{ textAlign: 'right', fontWeight: 600 }}>{fmtEur(k.cost_eur ?? 0)}</td>
                    </tr>
                    {k.teile.map(t => <KostenZeile key={t.code} r={t} teilzeile />)}
                  </Fragment>
                )
              }
              // Eine Klimawirkung mit genau einer Zeile (z. B. #96, #98) hat keine
              // Summenzeile; ihre einzige Zeile trägt Name und Nummer (bezeichnung).
              const zeile = byRiskCode.get(k.codes[0])
              if (!zeile) return null
              return <KostenZeile key={zeile.code} r={{ ...zeile, name: k.bezeichnung }} teilzeile={false} />
            })}
          </tbody>
        </table>
        {riskSummary.cost.euro_coverage && (
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 6 }}>
            Gesamtschaden {fmtEur(costSummary?.damages_with_measures_eur ?? riskSummary.cost.total_eur)}/Jahr
            {' · '}{riskSummary.cost.euro_coverage.text}
          </p>
        )}
      </div>

      {costSummary &&costSummary.measures.rows.length > 0 && (
        <div className="chart-card" style={{ marginTop: '1rem' }}>
          <h3 className="chart-title">Maßnahmen – CAPEX/OPEX & Nutzen</h3>
          <table className="data-table">
            <thead>
              <tr>
                <th>Maßnahme</th>
                <th style={{ textAlign: 'right' }}>CAPEX</th>
                <th style={{ textAlign: 'right' }}>OPEX/Jahr</th>
                <th style={{ textAlign: 'right' }}>Nutzen/Jahr</th>
              </tr>
            </thead>
            <tbody>
              {costSummary.measures.rows.map(m => (
                <tr key={m.id}>
                  <td style={{ fontWeight: 500 }}>{m.name}</td>
                  <td style={{ textAlign: 'right' }}>{fmtEur(m.capex_eur)}</td>
                  <td style={{ textAlign: 'right' }}>{fmtEur(m.opex_annual_eur)}</td>
                  <td style={{ textAlign: 'right', color: 'var(--success)' }}>{m.benefit_display
                    ? m.benefit_display
                    : <>{fmtEur(m.annual_benefit_eur)}{m.benefit_note && <span style={{ display: 'block', fontSize: '0.7rem', color: 'var(--text-muted)' }}>{m.benefit_note}</span>}</>}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  )
}

/** Zeile der Tabelle „Erwartete Schäden je Risiko“; Teilzeilen einer Klimawirkung stehen eingerückt. */
function KostenZeile({ r, teilzeile }: { r: Zeile; teilzeile: boolean }) {
  return (
    <tr>
      <td style={teilzeile
        ? { paddingLeft: '1.5rem', color: 'var(--text-muted)' }
        : { fontWeight: 500 }}>{r.name}</td>
      <td style={{ textAlign: 'right' }}>{r.index.toFixed(1)}</td>
      <td style={{ textAlign: 'right', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
        {r.outcome.toLocaleString('de-DE', { maximumFractionDigits: 1 })} {r.outcome_unit}
      </td>
      <td style={teilzeile ? { textAlign: 'right', color: 'var(--text-muted)' } : { textAlign: 'right' }}>
        {/* Verwechslungssperre Klasse A/B (T-0517): Klasse B zeigt den
            Screening-Vermerk des Backends, nie einen Strich oder 0 €. */}
        {r.has_euro_layer === false || r.cost_eur == null ? String(r.cost_display ?? '') : fmtEur(r.cost_eur)}
      </td>
    </tr>
  )
}
