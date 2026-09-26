import type { QuerverbindungsAuswertung, Rueckkopplung, RueckkopplungKnoten } from '../../api/client'
import InfoTooltip from '../InfoTooltip'

/**
 * Rückkopplungskreislauf und gegenseitige Wechselwirkungen (KWRA 2021, Teilbericht 6, Kap. 3.4).
 *
 * Zeigt den einzigen Rückkopplungskreislauf der Gesamtauswertung — Hitzebelastung → Bedarf an
 * Kühlenergie ↔ Stadtklima/Wärmeinseln → Hitzebelastung (S. 85–86, Abbildung 9) — als kurze Liste
 * der Wirkschritte, ohne Netzwerkformeln (A-0034), und darunter die beiden weiteren gegenseitigen
 * Wechselwirkungen. Klimawirkungen außerhalb des Katalogs stehen nur mit Namen und dem Hinweis
 * „nicht im Katalog“ — nie mit Index, Betrag oder Rang (Verwechslungssperre, P2). Ausnahme: Ihre
 * KWRA-Nummer steht dabei, allein zum Nachschlagen in der Quelle (Entscheidung T-1072-ceo).
 * Daten kommen unverändert aus `rueckkopplungen` von GET /catalog/querverbindungen; die Pfeilrichtungen
 * sind die ausgewiesene Ablesung aus Abbildung 9 (backend/app/data/kwra_rueckkopplungen.py).
 */

const TB6 = 'KWRA 2021, Teilbericht 6'

interface Schritt {
  von: RueckkopplungKnoten
  nach: RueckkopplungKnoten
  gegenseitig: boolean
}

/** Fasst die Kanten zu Schritten zusammen; eine Kante mit Gegenkante erscheint einmal als „↔“. */
function schritte(r: Rueckkopplung): Schritt[] {
  const knoten = new Map(r.knoten.map(k => [k.kwra_id, k]))
  const gesehen = new Set<string>()
  const liste: Schritt[] = []
  for (const k of r.kanten) {
    const von = knoten.get(k.von_kwra_id)
    const nach = knoten.get(k.nach_kwra_id)
    if (!von || !nach) continue
    const schluessel = [k.von_kwra_id, k.nach_kwra_id].sort((a, b) => a - b).join('-')
    if (gesehen.has(schluessel)) continue
    gesehen.add(schluessel)
    const gegenseitig = r.kanten.some(g => g.von_kwra_id === k.nach_kwra_id && g.nach_kwra_id === k.von_kwra_id)
    liste.push({ von, nach, gegenseitig })
  }
  return liste
}

/** Beginnt der Kreislauf bei Hitzebelastung (#95), wenn sie beteiligt ist — so liest ihn die Quelle. */
function kreislaufSchritte(r: Rueckkopplung): Schritt[] {
  const liste = schritte(r)
  const start = liste.findIndex(s => s.von.kwra_id === 95 && !s.gegenseitig)
  return start > 0 ? [...liste.slice(start), ...liste.slice(0, start)] : liste
}

function KnotenName({ k }: { k: RueckkopplungKnoten }) {
  return (
    <>
      <strong>{k.name}</strong>{' '}
      <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>
        {k.im_katalog ? `(#${k.kwra_id}, ${k.handlungsfeld})` : `(#${k.kwra_id}, nicht im Katalog; Handlungsfeld ${k.handlungsfeld})`}
      </span>
    </>
  )
}

function fundstelle(r: Rueckkopplung): string {
  const seiten = r.seiten.length === 1 ? `S. ${r.seiten[0]}` : `S. ${r.seiten.join(', ')}`
  return r.abbildung ? `${TB6}, ${seiten}, ${r.abbildung}` : `${TB6}, ${seiten}`
}

export default function RueckkopplungKreislauf({ daten }: { daten: QuerverbindungsAuswertung }) {
  const rueckkopplungen = daten.rueckkopplungen ?? []
  const kreislauf = rueckkopplungen.find(r => r.art === 'kreislauf')
  const wechselwirkungen = rueckkopplungen.filter(r => r.art === 'wechselwirkung')

  return (
    <div style={{ marginTop: 20 }}>
      <h3 style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: '1rem', marginBottom: 6 }}>
        Rückkopplungskreislauf Hitze – Kühlenergie – Stadtklima
        <InfoTooltip
          title="Einziger Rückkopplungskreislauf"
          description={`Die KWRA 2021 findet unter allen Querverbindungen genau einen Kreislauf, in dem sich Klimawirkungen gegenseitig verstärken (${TB6}, S. 85–86, Abbildung 9). Die Pfeilrichtungen sind aus Abbildung 9 abgelesen; der Fließtext beschreibt dieselben Richtungen.`}
          note={daten.rueckkopplungen_quelle ? `Quelle: ${daten.rueckkopplungen_quelle}` : undefined}
        />
      </h3>

      {!kreislauf && (
        <p style={{ color: 'var(--text-muted)' }}>Der Rückkopplungskreislauf liegt in der Antwort des Dienstes nicht vor.</p>
      )}

      {kreislauf && (
        <>
          <ol style={{ fontSize: '0.9rem', margin: '0 0 8px 20px', padding: 0 }}>
            {kreislaufSchritte(kreislauf).map(s => (
              <li key={`${s.von.kwra_id}-${s.nach.kwra_id}`} style={{ marginBottom: 4 }}>
                <KnotenName k={s.von} /> {s.gegenseitig ? '↔' : '→'} <KnotenName k={s.nach} />
                {s.gegenseitig && (
                  <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}> (wirkt in beide Richtungen)</span>
                )}
              </li>
            ))}
          </ol>
          <p style={{ fontSize: '0.85rem', marginBottom: 6, padding: '6px 10px',
            borderLeft: '3px solid var(--border, #ccc)', background: 'var(--bg-muted, transparent)' }}>
            {kreislauf.beleg}{' '}
            <span style={{ color: 'var(--text-muted)' }}>
              ({fundstelle(kreislauf)}{kreislauf.quellen.length > 0 ? `; dort zitiert: ${kreislauf.quellen.join(', ')}` : ''})
            </span>
          </p>
          <p style={{ fontSize: '0.85rem', marginBottom: 6 }}>
            Für die Kommune heißt das: Anpassung an diesen Kreislauf liegt laut Quelle neben dem Bund auch in ihrer
            Verantwortung ({TB6}, S. 86).
          </p>
          {kreislauf.knoten.some(k => !k.im_katalog) && (
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: 6 }}>
              Modellgrenze: {kreislauf.knoten.filter(k => !k.im_katalog).map(k => k.name).join(', ')} steht nicht im
              Katalog des Produkts; die Klimawirkung ist nur benannt, ohne Index, Betrag oder Rang.
            </p>
          )}
        </>
      )}

      {wechselwirkungen.length > 0 && (
        <>
          <h4 style={{ fontSize: '0.95rem', margin: '14px 0 6px' }}>Weitere gegenseitige Wechselwirkungen</h4>
          <ul style={{ fontSize: '0.85rem', margin: '0 0 6px 20px', padding: 0 }}>
            {wechselwirkungen.map(r => (
              <li key={r.id} style={{ marginBottom: 4 }}>
                {schritte(r).map(s => (
                  <span key={`${s.von.kwra_id}-${s.nach.kwra_id}`}>
                    <KnotenName k={s.von} /> {s.gegenseitig ? '↔' : '→'} <KnotenName k={s.nach} />
                  </span>
                ))}
                {r.staerke && <span style={{ color: 'var(--text-muted)' }}> — {r.staerke}</span>}
                <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}> ({fundstelle(r)})</span>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  )
}
