import { Fragment } from 'react'
import { useStore } from '../../store'
import InfoTooltip from '../InfoTooltip'
import { fmtEur } from '../../utils/format'
import { gesamtNachMassnahmen, schadenNachMassnahmen, schluesselKlimawirkung } from '../../utils/schadenNachMassnahmen'
import type { RiskAggregate } from '../../types'

type Zeile = RiskAggregate['cost']['by_risk'][number]

/** Höchstens so viele Klimawirkungen (Teilzeilen zählen nicht mit). */
const MAX_BLOECKE = 20

/** Kostentabellen: erwartete Schäden je Risiko + Maßnahmen-CAPEX/OPEX/Nutzen. */
export default function CostTablesSection() {
  const { riskSummary, costSummary } = useStore()
  if (!riskSummary) return null

  // Die Karte zeigt immer die Ausgangslage (risk-summary, ohne Wirkung der Maßnahmen),
  // unabhängig davon, ob und wann cost-summary geladen ist (T-1816). Der Betrag mit
  // Maßnahmen steht nur bei Abweichung in der Spalte „nach Maßnahmen“.
  const byRiskCode = new Map(riskSummary.cost.by_risk.map(z => [z.code, z]))
  const klimawirkungen = riskSummary.cost.klimawirkungen
  const nach = schadenNachMassnahmen(riskSummary.cost, costSummary, MAX_BLOECKE)
  const gesamtNach = gesamtNachMassnahmen(riskSummary.cost.total_eur, costSummary)

  return (
    <section>
      <h2 className="section-title">Kostentabellen</h2>
      <div className="chart-card">
        <h3 className="chart-title" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          Erwartete Schäden je Risiko
          <InfoTooltip title="Aggregation je Risiko"
            description="Schaden/Jahr = Σ über alle 100m-Zellen (bevölkerungs-/flächenbezogene Risiken) bzw. P90-Index × Kommune (Ausfall-/Screening-Risiken, nicht zell-additiv). Der Gesamtschaden ist die nachrechenbare Summe dieser Zeilen – ohne nicht-additive Teilkennzahlen (z. B. Restaurierung, = Anteil bereits gezählter Sektorschäden). Die Spalte „Schaden/Jahr“ zeigt den Schaden ohne Wirkung der Maßnahmen; weicht der Betrag mit den Maßnahmen der Kommune davon ab, steht er daneben in der Spalte „nach Maßnahmen“." />
        </h3>
        <table className="data-table">
          <thead>
            <tr>
              <th>Risiko</th>
              <th style={{ textAlign: 'right' }}>Index</th>
              <th style={{ textAlign: 'right' }}>Ergebnis</th>
              <th style={{ textAlign: 'right' }}>Schaden/Jahr</th>
              {nach.hatSpalte && <th style={{ textAlign: 'right' }}>nach Maßnahmen</th>}
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
                      {nach.hatSpalte && <NachMassnahmenZelle eur={nach.summe.get(schluesselKlimawirkung(k))} fett />}
                    </tr>
                    {k.teile.map(t => <KostenZeile key={t.code} r={t} teilzeile nach={nach.hatSpalte ? { eur: nach.zeile.get(t.code) } : undefined} />)}
                  </Fragment>
                )
              }
              // Eine Klimawirkung mit genau einer Zeile (z. B. #96, #98) hat keine
              // Summenzeile; ihre einzige Zeile trägt Name und Nummer (bezeichnung).
              const zeile = byRiskCode.get(k.codes[0])
              if (!zeile) return null
              return <KostenZeile key={zeile.code} r={{ ...zeile, name: k.bezeichnung }} teilzeile={false}
                nach={nach.hatSpalte ? { eur: nach.zeile.get(zeile.code) } : undefined} />
            })}
          </tbody>
        </table>
        {riskSummary.cost.euro_coverage && (
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 6 }}>
            Gesamtschaden {fmtEur(riskSummary.cost.total_eur)}/Jahr
            {gesamtNach != null && <>{' · '}nach Maßnahmen {fmtEur(gesamtNach)}/Jahr</>}
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
function KostenZeile({ r, teilzeile, nach }: { r: Zeile; teilzeile: boolean; nach?: { eur?: number } }) {
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
      {nach && <NachMassnahmenZelle eur={nach.eur} muted={teilzeile} />}
    </tr>
  )
}

/** Zelle der Spalte „nach Maßnahmen“: nur bei Abweichung ein Betrag, sonst leer. */
function NachMassnahmenZelle({ eur, fett, muted }: { eur?: number; fett?: boolean; muted?: boolean }) {
  return (
    <td style={{
      textAlign: 'right',
      ...(fett ? { fontWeight: 600 } : {}),
      ...(muted ? { color: 'var(--text-muted)' } : {}),
    }}>{eur == null ? '' : fmtEur(eur)}</td>
  )
}
