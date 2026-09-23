import { useEffect, useState } from 'react'
import { api, type KangZustaendigkeit as KangDaten } from '../../api/client'

const HINWEIS = 'Abbildung der Rechtslage, keine Rechtsauskunft'

function pflichtText(pflicht: KangDaten['pflicht']): string {
  if (pflicht === 'ja') return 'Pflicht: ja'
  if (pflicht === 'nein') return 'Pflicht: nein'
  return 'Pflicht: keine Landesbestimmung'
}

/** JJJJ-MM-TT → TT.MM.JJJJ; andere Formen bleiben unverändert. */
function datumText(stand: string): string {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(stand)
  return m ? `${m[3]}.${m[2]}.${m[1]}` : stand
}

/**
 * Kompakte Anzeige in der Meta-Zeile des Kommunenkopfs: ob die Kommune nach
 * Landesrecht (§ 12 Abs. 1 KAnG) ein Klimaanpassungskonzept aufstellen muss,
 * welche Stelle zuständig ist, mit Rechtsgrundlage als Link auf die Fundstelle
 * und Stand. Bei „unbekannt" oder Ladefehler erscheint ein neutraler Hinweis.
 */
export default function KangZustaendigkeit({ kommuneId }: { kommuneId: number }) {
  const [daten, setDaten] = useState<KangDaten | null>(null)
  const [fehler, setFehler] = useState(false)

  useEffect(() => {
    let aktiv = true
    setDaten(null)
    setFehler(false)
    api.getKangZustaendigkeit(kommuneId)
      .then(d => { if (aktiv) setDaten(d) })
      .catch(() => { if (aktiv) setFehler(true) })
    return () => { aktiv = false }
  }, [kommuneId])

  const stil = { fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: 4 }

  if (!daten && !fehler) return null

  if (fehler || !daten || daten.pflicht === 'unbekannt') {
    return (
      <div className="kang-zustaendigkeit" style={stil}>
        Klimaanpassungskonzept nach § 12 KAnG: Für diese Kommune liegt derzeit keine
        Angabe zur landesrechtlichen Zuständigkeit vor.
      </div>
    )
  }

  const link = /^https?:\/\//i.test(daten.fundstelle)
  return (
    <div className="kang-zustaendigkeit" style={stil} title={HINWEIS}>
      <strong>Klimaanpassungskonzept nach § 12 KAnG</strong>
      {' · '}{pflichtText(daten.pflicht)}
      {daten.zustaendige_stelle && <>{' · '}Zuständig: {daten.zustaendige_stelle}</>}
      {daten.rechtsgrundlage && (
        <>
          {' · '}
          {link
            ? <a href={daten.fundstelle} target="_blank" rel="noopener noreferrer">{daten.rechtsgrundlage}</a>
            : <span title={daten.fundstelle || undefined}>{daten.rechtsgrundlage}</span>}
        </>
      )}
      {daten.stand && <>{' · '}Stand {datumText(daten.stand)}</>}
      {' · '}<em>{HINWEIS}</em>
    </div>
  )
}
