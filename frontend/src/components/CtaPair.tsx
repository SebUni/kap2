import { Link } from 'react-router-dom'
import { FEATURES } from '../config/features'

interface Props {
  demoLabel?: string
  contactLabel?: string
  /** Zentriert (Hero/Abschluss) oder linksbündig (in Sektionen). */
  align?: 'center' | 'left'
}

/**
 * Doppel-CTA — tritt auf der Landingpage und den öffentlichen Seiten immer
 * als Paar auf (Plan §2.1c): der selbstständige Einstieg für die, die klicken
 * wollen, daneben der Gesprächseinstieg. Solange die Demo offline ist
 * (M0-Verschlankung), übernimmt die Roadmap den ersten Platz.
 */
export default function CtaPair({
  demoLabel = 'Demo-Kommune ausprobieren',
  contactLabel = 'Beratungsgespräch vereinbaren',
  align = 'center',
}: Props) {
  return (
    <div className={`cta-pair${align === 'left' ? ' cta-pair-left' : ''}`}>
      {FEATURES.demo ? (
        <Link to="/demo" className="btn-primary cta-demo">► {demoLabel}</Link>
      ) : (
        <Link to="/roadmap" className="btn-primary cta-demo">Roadmap ansehen →</Link>
      )}
      <Link to="/kontakt" className="cta-contact">{contactLabel} →</Link>
    </div>
  )
}
