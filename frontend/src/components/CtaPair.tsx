import { Link } from 'react-router-dom'

interface Props {
  demoLabel?: string
  contactLabel?: string
  /** Zentriert (Hero/Abschluss) oder linksbündig (in Sektionen). */
  align?: 'center' | 'left'
}

/**
 * Doppel-CTA „Demo + Beratungsgespräch" — tritt auf der Landingpage und den
 * öffentlichen Seiten immer als Paar auf (Plan §2.1c): die selbstständige
 * Demo für die, die klicken wollen, daneben der Gesprächseinstieg.
 */
export default function CtaPair({
  demoLabel = 'Demo-Kommune ausprobieren',
  contactLabel = 'Beratungsgespräch vereinbaren',
  align = 'center',
}: Props) {
  return (
    <div className={`cta-pair${align === 'left' ? ' cta-pair-left' : ''}`}>
      <Link to="/demo" className="btn-primary cta-demo">► {demoLabel}</Link>
      <Link to="/kontakt" className="cta-contact">{contactLabel} →</Link>
    </div>
  )
}
