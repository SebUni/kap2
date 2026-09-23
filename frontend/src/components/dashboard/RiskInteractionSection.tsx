import { useEffect, useState } from 'react'
import { api } from '../../api/client'
import type { QuerverbindungsAuswertung, QuerverbindungKlimawirkung } from '../../api/client'
import InfoTooltip from '../InfoTooltip'

/**
 * Querverbindungen zwischen Klimawirkungen (KWRA 2021, Teilbericht 6, Kap. 3.4).
 *
 * Zeigt je im Katalog geführter Klimawirkung die ausdrücklich belegte Netzrolle
 * („stark ausgehend" / „stark eingehend") und die Zahl der im Fließtext benannten
 * Einzelbeziehungen („wirkt auf" = ausgehend, „beeinflusst von" = eingehend).
 * Daten kommen unverändert aus GET /catalog/querverbindungen; hier wird nichts
 * modelliert oder ergänzt — die Modellgrenze des Backends wird wörtlich angezeigt.
 */

/** Gesamtzahl der Querverbindungen laut KWRA 2021, TB 6 Kap. 3.4 — nur Rückfallwert,
 *  falls die Kennzahl in der API-Antwort fehlt (Quelle wie backend/app/data/kwra_querverbindungen.py). */
const KWRA_QUERVERBINDUNGEN_GESAMT = 257

function netzrolleText(rolle: QuerverbindungKlimawirkung['netzrolle']): string {
  if (rolle === 'stark ausgehend') return 'stark ausgehend (Sender)'
  if (rolle === 'stark eingehend') return 'stark eingehend (Empfänger)'
  return '—'
}

export default function RiskInteractionSection({ className = '' }: { className?: string }) {
  const [daten, setDaten] = useState<QuerverbindungsAuswertung | null>(null)
  const [fehler, setFehler] = useState<string | null>(null)

  useEffect(() => {
    let aktiv = true
    api.getQuerverbindungen()
      .then(d => { if (aktiv) setDaten(d) })
      .catch(e => { if (aktiv) setFehler(e instanceof Error ? e.message : String(e)) })
    return () => { aktiv = false }
  }, [])

  const gesamt = daten?.kennzahlen?.querverbindungen_gesamt ?? KWRA_QUERVERBINDUNGEN_GESAMT
  const zeilen = (daten?.klimawirkungen ?? []).filter(
    k => k.netzrolle !== null || k.ausgehende_benannte > 0 || k.eingehende_benannte > 0,
  )

  return (
    <section className={`dashboard-section ${className}`}>
      <h2 className="section-title" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
        Querverbindungen zwischen Klimawirkungen
        <InfoTooltip title="Netzrolle und Wechselwirkungen"
          description={`Die KWRA 2021 zählt ${gesamt} Querverbindungen zwischen den 102 Klimawirkungen. Netzrolle: ob eine Klimawirkung im Wirkungsnetz ausdrücklich als starker Sender (wirkt auf viele andere) oder starker Empfänger (wird von vielen beeinflusst) benannt ist. „wirkt auf" und „beeinflusst von" zählen nur die in Teilbericht 6 Kapitel 3.4 wörtlich genannten Einzelbeziehungen.`} />
      </h2>
      <div className="chart-card">
        {fehler && (
          <p style={{ color: 'var(--text-muted)' }}>Querverbindungen konnten nicht geladen werden: {fehler}</p>
        )}
        {!daten && !fehler && (
          <p style={{ color: 'var(--text-muted)' }}>Lade Querverbindungen …</p>
        )}
        {daten && (
          <>
            <p style={{ fontSize: '0.9rem', marginBottom: 8 }}>
              Laut KWRA 2021 bestehen <strong>{gesamt}</strong> Querverbindungen zwischen den{' '}
              {daten.abdeckung.klimawirkungen_kwra_gesamt} Klimawirkungen
              {daten.kennzahlen.durchschnitt_je_klimawirkung
                ? ` (${daten.kennzahlen.durchschnitt_je_klimawirkung})` : ''}.
              {' '}Von den {daten.abdeckung.klimawirkungen_im_katalog} im Produkt geführten Klimawirkungen
              haben {daten.abdeckung.mit_ausgewiesener_netzrolle} eine ausgewiesene Netzrolle und{' '}
              {daten.abdeckung.mit_benannter_einzelbeziehung} mindestens eine benannte Einzelbeziehung.
            </p>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Klimawirkung</th>
                  <th>Netzrolle</th>
                  <th style={{ textAlign: 'right' }}>wirkt auf (benannt)</th>
                  <th style={{ textAlign: 'right' }}>beeinflusst von (benannt)</th>
                </tr>
              </thead>
              <tbody>
                {zeilen.map(k => (
                  <tr key={k.kwra_id}>
                    <td style={{ fontWeight: 500 }}>
                      <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>#{k.kwra_id}</span>{' '}
                      {k.name}
                    </td>
                    <td>{netzrolleText(k.netzrolle)}</td>
                    <td style={{ textAlign: 'right' }}>{k.ausgehende_benannte}</td>
                    <td style={{ textAlign: 'right' }}>{k.eingehende_benannte}</td>
                  </tr>
                ))}
                {zeilen.length === 0 && (
                  <tr><td colSpan={4} style={{ color: 'var(--text-muted)' }}>
                    Für keine der im Produkt geführten Klimawirkungen ist eine Netzrolle oder Einzelbeziehung belegt.
                  </td></tr>
                )}
              </tbody>
            </table>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 6 }}>
              Modellgrenze: {daten.modellgrenze}
            </p>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 4 }}>
              Quelle: {daten.quelle}
            </p>
          </>
        )}
      </div>
    </section>
  )
}
