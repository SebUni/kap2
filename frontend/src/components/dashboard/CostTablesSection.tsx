import { useStore } from '../../store'
import InfoTooltip from '../InfoTooltip'
import { fmtEur } from '../../utils/format'

/** Kostentabellen: erwartete Schäden je Risiko + Maßnahmen-CAPEX/OPEX/Nutzen. */
export default function CostTablesSection() {
  const { riskSummary, costSummary } = useStore()
  if (!riskSummary) return null

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
            {(costSummary?.by_risk || riskSummary.cost.by_risk).slice(0, 20).map(r => (
              <tr key={r.code}>
                <td style={{ fontWeight: 500 }}>{r.name}</td>
                <td style={{ textAlign: 'right' }}>{r.index.toFixed(1)}</td>
                <td style={{ textAlign: 'right', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                  {r.outcome.toLocaleString('de-DE', { maximumFractionDigits: 1 })} {r.outcome_unit}
                </td>
                <td style={{ textAlign: 'right' }}>
                  {r.cost_dimension === 'monetary' || r.cost_eur > 0 ? fmtEur(r.cost_eur) : '–'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {costSummary && costSummary.measures.rows.length > 0 && (
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
                  <td style={{ textAlign: 'right', color: 'var(--success)' }}>{fmtEur(m.annual_benefit_eur)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  )
}
