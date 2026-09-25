import type { QuerverbindungsAuswertung } from '../../api/client'
import InfoTooltip from '../InfoTooltip'

/**
 * Handlungsfeld-Sicht der Querverbindungen (KWRA 2021, Teilbericht 6, Kap. 3.4).
 *
 * Zeigt in dieser Reihenfolge:
 * 1. die Annahme der Auswertung (`aussagen.annahme`, wörtlich mit Fundstelle) als Lesehinweis,
 * 2. die Ablesung aus Abbildung 8 (S. 83) als Rangfolge der 13 Handlungsfelder mit „rund N“ —
 *    Genauigkeit und Herleitung stehen im Info-Symbol, nicht in der Tabelle (A-0034),
 * 3. die Kennzahlen der Auswertung (Text S. 84–85),
 * 4. die Einordnung nach Systembereichen (`aussagen.einordnung_cluster`, Tabelle 28; Fundstelle
 *    aus `systembereich_matrix_quelle`, S. 153).
 * Die Stärke der Verbindung von Handlungsfeld zu Handlungsfeld (Dicke der Bänder) ist nicht
 * abgelesen und steht als Modellgrenze. Daten kommen unverändert aus GET /catalog/querverbindungen.
 */

const TB6 = 'KWRA 2021, Teilbericht 6'

/** Anzeige einer abgelesenen Zahl; 0 ist im Text der Quelle belegt („nur aus-/eingehend“). */
function rund(n: number): string {
  return n === 0 ? 'keine' : `rund ${n}`
}

function seitenText(seiten: number[], seite: number): string {
  const liste = seiten.length > 0 ? seiten : [seite]
  return liste.length === 1 ? `S. ${liste[0]}` : `S. ${liste.join(', ')}`
}

const KENNZAHL_TEXT: [string, string][] = [
  ['querverbindungen_gesamt', 'Querverbindungen zwischen den 102 Klimawirkungen'],
  ['durchschnitt_je_klimawirkung', 'Durchschnitt je Klimawirkung'],
  ['klimawirkungen_mit_ausgehenden_beziehungen', 'Klimawirkungen mit ausgehenden Beziehungen'],
  ['klimawirkungen_mit_eingehenden_beziehungen', 'Klimawirkungen mit eingehenden Beziehungen'],
  ['handlungsfeld_meiste_ausgehende_beziehungen', 'Handlungsfeld mit den meisten ausgehenden Beziehungen'],
  ['handlungsfeld_meiste_eingehende_beziehungen', 'Handlungsfeld mit den meisten eingehenden Beziehungen'],
  ['nur_ausgehende_beziehungen', 'Handlungsfeld nur mit ausgehenden Beziehungen'],
  ['nur_eingehende_beziehungen', 'Handlungsfeld nur mit eingehenden Beziehungen'],
]

export default function QuerverbindungenHandlungsfelder({ daten }: { daten: QuerverbindungsAuswertung }) {
  const hf = daten.handlungsfelder
  const annahme = daten.aussagen?.annahme
  const einordnung = daten.aussagen?.einordnung_cluster
  const kennzahlen = daten.kennzahlen ?? {}
  const gesamtQuelle = Number(kennzahlen.querverbindungen_gesamt ?? 0)

  const felder = [...(hf?.felder ?? [])].sort(
    (a, b) => b.summe - a.summe || b.ausgehend - a.ausgehend || a.name.localeCompare(b.name, 'de'),
  )
  const summeAblesung = felder.reduce((s, f) => s + f.ausgehend, 0)

  const matrix = daten.systembereich_matrix ?? {}
  const matrixQuelle = daten.systembereich_matrix_quelle
  const bereiche = Object.keys(matrix)
  const systembereiche = bereiche.map(b => {
    const zeile = matrix[b] ?? {}
    const innerhalb = zeile[b] ?? 0
    const ausgehend = zeile.summe_ausgehend ?? 0
    const eingehend = bereiche
      .filter(andere => andere !== b)
      .reduce((s, andere) => s + (matrix[andere]?.[b] ?? 0), 0)
    return { name: b, ausgehend, eingehend, innerhalb }
  })

  return (
    <div style={{ marginTop: 20 }}>
      <h3 style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: '1rem', marginBottom: 6 }}>
        Querverbindungen je Handlungsfeld
        {hf && (
          <InfoTooltip
            title="Ablesung aus Abbildung 8"
            description={`Die Zahlen sind abgelesen aus Abbildung 8 „Querverbindungen zwischen den Handlungsfeldern“, ${TB6}, S. 83. Die Quelle hat dafür keine Tabelle; es ist eine ausgewiesene Ablesung von KAP3.`}
            rows={[
              { label: 'Genauigkeit Summe', value: `± ${hf.genauigkeit_summe} Querbezüge` },
              { label: 'Genauigkeit aus-/eingehend', value: `± ${hf.genauigkeit_aufteilung} Querbezüge` },
              { label: 'Fundstelle', value: `Abbildung 8, ${TB6}, S. 83` },
            ]}
            note={`Wie abgelesen wurde: ${hf.ablesung}`}
          />
        )}
      </h3>

      {annahme && (
        <p style={{ fontSize: '0.85rem', marginBottom: 8, padding: '6px 10px',
          borderLeft: '3px solid var(--border, #ccc)', background: 'var(--bg-muted, transparent)' }}>
          <strong>Lesehinweis — {annahme.titel}:</strong> „{annahme.wortlaut}“{' '}
          <span style={{ color: 'var(--text-muted)' }}>
            ({annahme.titel}, {TB6}, {seitenText(annahme.seiten ?? [], annahme.seite)})
          </span>
        </p>
      )}

      {!hf && (
        <p style={{ color: 'var(--text-muted)' }}>Die Ablesung aus Abbildung 8 liegt in der Antwort des Dienstes nicht vor.</p>
      )}

      {hf && (
        <>
          <p style={{ fontSize: '0.85rem', marginBottom: 6 }}>
            Rangfolge der 13 Handlungsfelder nach der Zahl ihrer Querbezüge zu anderen Handlungsfeldern,
            abgelesen aus Abbildung 8 ({TB6}, S. 83). „Wirkt auf“ zählt ausgehende, „beeinflusst von“ eingehende
            Beziehungen.
          </p>
          <table className="data-table">
            <thead>
              <tr>
                <th style={{ textAlign: 'right' }}>Rang</th>
                <th>Handlungsfeld</th>
                <th style={{ textAlign: 'right' }}>wirkt auf</th>
                <th style={{ textAlign: 'right' }}>beeinflusst von</th>
                <th style={{ textAlign: 'right' }}>zusammen</th>
              </tr>
            </thead>
            <tbody>
              {felder.map((f, i) => (
                <tr key={f.name}>
                  <td style={{ textAlign: 'right' }}>{i + 1}</td>
                  <td style={{ fontWeight: 500 }}>{f.name}</td>
                  <td style={{ textAlign: 'right' }}>{rund(f.ausgehend)}</td>
                  <td style={{ textAlign: 'right' }}>{rund(f.eingehend)}</td>
                  <td style={{ textAlign: 'right' }}>{rund(f.summe)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 6 }}>
            Modellgrenze: Wie stark ein Handlungsfeld mit einem bestimmten anderen verbunden ist (Dicke der Bänder in
            Abbildung 8), ist nicht als Zahl abgelesen; die Quelle hat dafür keine Kantenliste.
            {gesamtQuelle > 0 && summeAblesung !== gesamtQuelle && (
              <> Die Ablesung ergibt zusammen rund {summeAblesung} Querbezüge, die Quelle nennt {gesamtQuelle}.</>
            )}
          </p>
        </>
      )}

      <h4 style={{ fontSize: '0.95rem', margin: '14px 0 6px' }}>Kennzahlen der Auswertung</h4>
      <table className="data-table">
        <tbody>
          {KENNZAHL_TEXT.filter(([k]) => kennzahlen[k] !== undefined && kennzahlen[k] !== '').map(([k, text]) => (
            <tr key={k}>
              <td>{text}</td>
              <td style={{ fontWeight: 500 }}>{String(kennzahlen[k])}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 4 }}>
        Quelle: {TB6}, Kap. 3.4 „Analyse der Querverbindungen“, Fließtext und Hinweistext zu Abbildung 8 (S. 83).
      </p>

      {(einordnung || systembereiche.length > 0) && (
        <>
          <h4 style={{ fontSize: '0.95rem', margin: '14px 0 6px' }}>Einordnung nach Systembereichen</h4>
          {einordnung && (
            <p style={{ fontSize: '0.85rem', marginBottom: 8 }}>
              „{einordnung.wortlaut}“{' '}
              <span style={{ color: 'var(--text-muted)' }}>
                ({einordnung.titel}, {TB6}, {seitenText(einordnung.seiten ?? [], einordnung.seite)})
              </span>
            </p>
          )}
          {systembereiche.length > 0 && (
            <>
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Systembereich</th>
                    <th style={{ textAlign: 'right' }}>wirkt auf andere Bereiche</th>
                    <th style={{ textAlign: 'right' }}>beeinflusst von anderen Bereichen</th>
                    <th style={{ textAlign: 'right' }}>innerhalb des Bereichs</th>
                  </tr>
                </thead>
                <tbody>
                  {systembereiche.map(s => (
                    <tr key={s.name}>
                      <td style={{ fontWeight: 500 }}>{s.name}</td>
                      <td style={{ textAlign: 'right' }}>{s.ausgehend}</td>
                      <td style={{ textAlign: 'right' }}>{s.eingehend}</td>
                      <td style={{ textAlign: 'right' }}>{s.innerhalb}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 4 }}>
                Quelle:{' '}
                {matrixQuelle
                  ? <>{TB6}, Tabelle {matrixQuelle.tabelle} „{matrixQuelle.titel}“, Kap. {matrixQuelle.kapitel} „{matrixQuelle.kapitel_titel}“, S. {matrixQuelle.seite}.</>
                  : <>{TB6}, Tabelle 28 (Querverbindungen zwischen den Systembereichen).</>}
                {' '}„Beeinflusst von anderen
                Bereichen“ ist die Spaltensumme der Tabelle ohne den eigenen Bereich. Rein vorgelagerte
                Klimawirkungen sind in der Tabelle nicht enthalten.
              </p>
            </>
          )}
        </>
      )}
    </div>
  )
}
