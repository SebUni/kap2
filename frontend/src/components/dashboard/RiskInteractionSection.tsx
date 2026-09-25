import { useEffect, useState } from 'react'
import { api } from '../../api/client'
import type { Netzrolle, QuerverbindungsAuswertung } from '../../api/client'
import InfoTooltip from '../InfoTooltip'
import QuerverbindungenHandlungsfelder from './QuerverbindungenHandlungsfelder'
import RueckkopplungKreislauf from './RueckkopplungKreislauf'

/**
 * Querverbindungen zwischen Klimawirkungen (KWRA 2021, Teilbericht 6, Kap. 3.4).
 *
 * Zeigt je im Katalog geführter Klimawirkung die ausdrücklich belegten Netzrollen
 * („stark ausgehend" / „stark eingehend", auch beide zugleich) und die Zahl der im
 * Fließtext benannten Einzelbeziehungen („wirkt auf" = ausgehend, „beeinflusst von"
 * = eingehend). Netzknoten der Gesamtbetrachtung außerhalb des Katalogs erscheinen
 * als benannte Knoten mit dem Hinweis „nicht im Katalog" — nie mit Index, Betrag
 * oder Rang (Verwechslungssperre, P2).
 * Daten kommen unverändert aus GET /catalog/querverbindungen; hier wird nichts
 * modelliert oder ergänzt — die Modellgrenze des Backends wird wörtlich angezeigt.
 */

/** Gesamtzahl der Querverbindungen laut KWRA 2021, TB 6 Kap. 3.4 — nur Rückfallwert,
 *  falls die Kennzahl in der API-Antwort fehlt (Quelle wie backend/app/data/kwra_querverbindungen.py). */
const KWRA_QUERVERBINDUNGEN_GESAMT = 257

const NETZROLLE_TEXT: Record<Netzrolle, string> = {
  'stark ausgehend': 'stark ausgehend (Sender)',
  'stark eingehend': 'stark eingehend (Empfänger)',
}

function netzrollenText(rollen: Netzrolle[], zentral: boolean): string {
  if (rollen.length === 0) return '—'
  const text = rollen.map(r => NETZROLLE_TEXT[r]).join(' und ')
  return zentral ? `${text}, zentral` : text
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
    k => (k.netzrollen ?? []).length > 0 || k.ausgehende_benannte > 0 || k.eingehende_benannte > 0,
  )
  const ausserhalb = daten?.netzknoten_ausserhalb_katalog ?? []

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
              {ausserhalb.length > 0 && (
                <>
                  {' '}Weitere {ausserhalb.length} Netzknoten der Gesamtbetrachtung stehen nicht im Katalog;
                  sie sind nur benannt, ohne Index, Betrag oder Rang.
                </>
              )}
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
                    <td>{netzrollenText(k.netzrollen ?? [], k.zentral ?? false)}</td>
                    <td style={{ textAlign: 'right' }}>{k.ausgehende_benannte}</td>
                    <td style={{ textAlign: 'right' }}>{k.eingehende_benannte}</td>
                  </tr>
                ))}
                {ausserhalb.map(n => (
                  <tr key={`ausserhalb-${n.kwra_id}`}>
                    <td style={{ fontWeight: 500 }}>
                      <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>#{n.kwra_id}</span>{' '}
                      {n.name}{' '}
                      <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                        ({n.hinweis || 'nicht im Katalog'}; Handlungsfeld {n.handlungsfeld})
                      </span>
                    </td>
                    <td>{netzrollenText(n.netzrollen, n.zentral)}</td>
                    <td style={{ textAlign: 'right', color: 'var(--text-muted)' }}>—</td>
                    <td style={{ textAlign: 'right', color: 'var(--text-muted)' }}>—</td>
                  </tr>
                ))}
                {zeilen.length === 0 && ausserhalb.length === 0 && (
                  <tr><td colSpan={4} style={{ color: 'var(--text-muted)' }}>
                    Für keine der im Produkt geführten Klimawirkungen ist eine Netzrolle oder Einzelbeziehung belegt.
                  </td></tr>
                )}
              </tbody>
            </table>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 6 }}>
              Modellgrenze: {daten.modellgrenze}
            </p>
            <RueckkopplungKreislauf daten={daten} />
            <QuerverbindungenHandlungsfelder daten={daten} />
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 4 }}>
              Quelle: {daten.quelle}
            </p>
          </>
        )}
      </div>
    </section>
  )
}
