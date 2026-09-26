import { Fragment } from 'react'
import { useStore } from '../../store'
import InfoTooltip from '../InfoTooltip'
import { fmtEur } from '../../utils/format'
import type { RiskAggregate } from '../../types'

type Zeile = RiskAggregate['cost']['by_risk'][number]

/** Block der Tabelle: eine Klimawirkung mit Summenzeile und Teilzeilen oder eine Einzelzeile. */
type Block =
  | { art: 'klimawirkung'; kwraId: number; summe: number; teile: Zeile[] }
  | { art: 'einzel'; zeile: Zeile }

/** Höchstens so viele Blöcke (Klimawirkungen bzw. Einzelzeilen) — Teilzeilen zählen nicht mit. */
const MAX_BLOECKE = 20

/**
 * Fasst Zeilen mit derselben kwra_id (Klasse A) zu einer Klimawirkung zusammen (T-1432):
 * Jahresbetrag = Summe der Teilzeilen, z. B. #95 = Mortalität + Erkrankungen. Zeilen ohne
 * kwra_id und Klasse-B-Zeilen bleiben Einzelzeilen. Klasse A steht nach Betrag absteigend,
 * Klasse B danach in der Reihenfolge des Backends.
 */
function bloecke(zeilen: Zeile[]): Block[] {
  const gruppen = new Map<number, Zeile[]>()
  for (const z of zeilen) {
    if (z.kwra_id != null && z.has_euro_layer !== false) {
      const liste = gruppen.get(z.kwra_id) ?? []
      liste.push(z)
      gruppen.set(z.kwra_id, liste)
    }
  }
  const klasseA: Block[] = []
  const klasseB: Block[] = []
  const gesehen = new Set<number>()
  for (const z of zeilen) {
    const teile = z.kwra_id != null ? gruppen.get(z.kwra_id) : undefined
    if (z.kwra_id != null && teile && teile.length > 1) {
      if (gesehen.has(z.kwra_id)) continue
      gesehen.add(z.kwra_id)
      const summe = teile.reduce((s, t) => s + (t.cost_eur ?? 0), 0)
      klasseA.push({ art: 'klimawirkung', kwraId: z.kwra_id, summe, teile })
    } else if (z.has_euro_layer === false || z.cost_eur == null) {
      klasseB.push({ art: 'einzel', zeile: z })
    } else {
      klasseA.push({ art: 'einzel', zeile: z })
    }
  }
  const betrag = (b: Block) => (b.art === 'klimawirkung' ? b.summe : b.zeile.cost_eur ?? 0)
  klasseA.sort((a, b) => betrag(b) - betrag(a))
  return [...klasseA, ...klasseB]
}

/** Kostentabellen: erwartete Schäden je Risiko + Maßnahmen-CAPEX/OPEX/Nutzen. */
export default function CostTablesSection() {
  const { riskSummary, costSummary, catalog } = useStore()
  if (!riskSummary) return null

  // Amtlicher Name der Klimawirkung aus dem Katalog (über die kwra_id).
  const amtlicherName = (kwraId: number) =>
    catalog?.risks.find(r => r.kwra_id === kwraId && r.kwra_name)?.kwra_name ?? 'Klimawirkung'

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
                Klimawirkung werden nie abgeschnitten (T-1432). */}
            {bloecke(costSummary?.by_risk || riskSummary.cost.by_risk).slice(0, MAX_BLOECKE).map(b =>
              b.art === 'einzel' ? <KostenZeile key={b.zeile.code} r={b.zeile} teilzeile={false} /> : (
                <Fragment key={`kwra-${b.kwraId}`}>
                  <tr>
                    <td style={{ fontWeight: 600 }}>{amtlicherName(b.kwraId)} (#{b.kwraId})</td>
                    <td />
                    <td />
                    <td style={{ textAlign: 'right', fontWeight: 600 }}>{fmtEur(b.summe)}</td>
                  </tr>
                  {b.teile.map(t => <KostenZeile key={t.code} r={t} teilzeile />)}
                </Fragment>
              ))}
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
