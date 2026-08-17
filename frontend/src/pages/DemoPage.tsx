import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useStore } from '../store'
import ProductLayout from '../layouts/ProductLayout'
import InlineSpinner from '../components/InlineSpinner'

/**
 * Öffentliche Demo-Kommune: bootstrappt die Demo-Session (Cookie + Meta +
 * Kommune) und rendert dann die Produkt-Shell im Demo-Modus. Ohne Login.
 */
export default function DemoPage() {
  const bootstrapDemo = useStore((s) => s.bootstrapDemo)
  const demoMode = useStore((s) => s.demoMode)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    bootstrapDemo().catch((e) => {
      if (!cancelled) setError(e instanceof Error ? e.message : String(e))
    })
    return () => { cancelled = true }
  }, [bootstrapDemo])

  if (error) {
    return (
      <div className="public-shell">
        <div className="login-page">
          <div className="login-card" style={{ textAlign: 'center' }}>
            <h2>Demo derzeit nicht verfügbar</h2>
            <p style={{ color: 'var(--text-muted)', margin: '0.75rem 0' }}>
              Die Demo-Kommune ist gerade nicht bereit. Bitte versuchen Sie es
              später erneut oder vereinbaren Sie ein Beratungsgespräch.
            </p>
            <Link to="/kontakt" className="btn-primary" style={{ display: 'inline-block', padding: '0.5rem 1rem', borderRadius: 8, textDecoration: 'none' }}>
              Beratungsgespräch vereinbaren →
            </Link>
          </div>
        </div>
      </div>
    )
  }

  if (!demoMode) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', gap: 8, color: 'var(--text-muted)' }}>
        <InlineSpinner /> Demo wird geladen …
      </div>
    )
  }

  return <ProductLayout demo />
}
