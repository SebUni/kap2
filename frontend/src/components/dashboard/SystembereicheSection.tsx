import { useEffect, useState } from 'react'
import { api } from '../../api/client'
import type { SystembereicheAuswertung, SystembereicheBundesanalyse } from '../../api/client'
import { useStore } from '../../store'

/**
 * Auswertung je KWRA-Systembereich (KWRA 2021, Teilbericht 6, Kap. 7; Konformitätszeile 10).
 *
 * Zeigt alle fünf Systembereiche aus GET /kommune/{id}/systembereiche. Ein Bereich ohne
 * Klimawirkung bleibt als Zeile stehen und nennt seinen `leer_grund` — nie ausgeblendet (P2).
 * Die Sektion hängt an keinem Betriebsmodus.
 *
 * Dieselbe Tabelle trägt je Zeile den Bundesvergleich der KWRA 2021 (Teilbericht 6, Kap. 7,
 * S. 146–154): Risiko ohne Anpassung, Handlungserfordernisse, Wirksamkeit und Anpassungsdauer.
 * Die Werte der Bundesanalyse sind übernommen, nicht gerechnet, und nicht der Produkt-Risikoindex.
 */

function euroText(wert: number | null): string {
  if (wert === null) return '—'
  if (Math.abs(wert) >= 1e9) return `${(wert / 1e9).toLocaleString('de-DE', { maximumFractionDigits: 2 })} Mrd. €`
  if (Math.abs(wert) >= 1e6) return `${(wert / 1e6).toLocaleString('de-DE', { maximumFractionDigits: 2 })} Mio. €`
  return `${wert.toLocaleString('de-DE', { maximumFractionDigits: 0 })} €`
}

export default function SystembereicheSection({ className = '' }: { className?: string }) {
  const kommune = useStore(s => s.kommune)
  const kommuneId = kommune?.id
  const [daten, setDaten] = useState<SystembereicheAuswertung | null>(null)
  const [fehler, setFehler] = useState<string | null>(null)
  const [bund, setBund] = useState<SystembereicheBundesanalyse | null>(null)
  const [bundFehler, setBundFehler] = useState<string | null>(null)

  useEffect(() => {
    let aktiv = true
    api.getSystembereicheBundesanalyse()
      .then(d => { if (aktiv) setBund(d) })
      .catch(e => { if (aktiv) setBundFehler(e instanceof Error ? e.message : String(e)) })
    return () => { aktiv = false }
  }, [])

  useEffect(() => {
    if (kommuneId === undefined) return
    let aktiv = true
    setDaten(null)
    setFehler(null)
    api.getSystembereiche(kommuneId)
      .then(d => { if (aktiv) setDaten(d) })
      .catch(e => { if (aktiv) setFehler(e instanceof Error ? e.message : String(e)) })
    return () => { aktiv = false }
  }, [kommuneId])

  return (
    <section className={`dashboard-section ${className}`}>
      <h2 className="section-title">Auswertung je KWRA-Systembereich</h2>
      <div className="chart-card">
        {fehler && (
          <p style={{ color: 'var(--text-muted)' }}>Systembereiche konnten nicht geladen werden: {fehler}</p>
        )}
        {!daten && !fehler && (
          <p style={{ color: 'var(--text-muted)' }}>Lade Systembereiche …</p>
        )}
        {daten && (
          <>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Systembereich</th>
                  <th style={{ textAlign: 'right' }}>Klimawirkungen</th>
                  <th style={{ textAlign: 'right' }}>mittlerer Index</th>
                  <th style={{ textAlign: 'right' }}>Schadenskosten</th>
                  <th>Bundesvergleich: Risiko ohne Anpassung</th>
                  <th style={{ textAlign: 'right' }}>Handlungserfordernis (sehr dringend / dringend)</th>
                  <th>Wirksamkeit der Anpassung</th>
                  <th>Anpassungsdauer</th>
                </tr>
              </thead>
              <tbody>
                {daten.bereiche.map(b => {
                  const bv = bund?.bereiche.find(x => x.systembereich === b.systembereich)
                  const muted = { color: 'var(--text-muted)', fontSize: '0.8rem' }
                  return (
                  <tr key={b.systembereich}>
                    <td style={{ fontWeight: 500 }}>
                      {b.systembereich}
                      <div style={{ fontWeight: 400, fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                        {b.klimawirkungen_im_katalog} Klimawirkungen im Katalog · {b.euro_beziffert}
                      </div>
                    </td>
                    {b.leer_grund ? (
                      <td colSpan={3} style={{ color: 'var(--text-muted)' }}>
                        leer: {b.leer_grund}
                      </td>
                    ) : (
                      <>
                        <td style={{ textAlign: 'right' }}>{b.anzahl_klimawirkungen}</td>
                        <td style={{ textAlign: 'right' }}>
                          {b.mittlerer_index === null
                            ? '—'
                            : b.mittlerer_index.toLocaleString('de-DE', { maximumFractionDigits: 2 })}
                        </td>
                        <td style={{ textAlign: 'right' }}>{euroText(b.schadenskosten_eur)}</td>
                      </>
                    )}
                    {bv ? (
                      <>
                        <td style={muted}>{bv.risiko.risiko_ohne_anpassung.vergleich}</td>
                        <td style={{ textAlign: 'right' }}>
                          {bv.risiko.handlungserfordernisse.sehr_dringend} / {bv.risiko.handlungserfordernisse.dringend}
                        </td>
                        <td style={muted}>
                          {bv.anpassung.wirksamkeit.valide_aussage && bv.anpassung.wirksamkeit.vergleich
                            ? bv.anpassung.wirksamkeit.vergleich
                            : 'keine belastbare Aussage der Bundesanalyse'}
                        </td>
                        <td style={muted}>
                          {bv.anpassung.anpassungsdauer.vergleich ?? 'keine belastbare Aussage der Bundesanalyse'}
                        </td>
                      </>
                    ) : (
                      <td colSpan={4} style={muted}>
                        {bundFehler ? `Bundesvergleich nicht geladen: ${bundFehler}` : 'Lade Bundesvergleich …'}
                      </td>
                    )}
                  </tr>
                  )
                })}
              </tbody>
            </table>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 6 }}>
              Die Tabelle vergleicht den Risikoindex des Produkts je Systembereich. Die Spalten des
              Bundesvergleichs sind die Aussagen der KWRA 2021, Teilbericht 6, Kap. 7, ohne eigene
              Rechnung; sie sind nicht der Produkt-Risikoindex und nicht mit ihm verrechnet.
              {bund && <> {bund.methodische_grenze.titel}: {bund.methodische_grenze.aussage}</>}
            </p>
          </>
        )}
      </div>
    </section>
  )
}
