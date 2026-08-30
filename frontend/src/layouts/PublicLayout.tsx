import { useEffect } from 'react'
import { Link, NavLink, Outlet } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import { FEATURES } from '../config/features'

const NAV_ITEMS = [
  { label: 'Das ist KAP2', to: '/' },
  ...(FEATURES.demo ? [{ label: 'Demo', to: '/demo' }] : []),
  ...(FEATURES.deutschlandKarte ? [{ label: 'Deutschland-Karte', to: '/deutschland' }] : []),
  ...(FEATURES.roadmap ? [{ label: 'Roadmap', to: '/roadmap' }] : []),
]

/**
 * Öffentliche Seiten (Landing, Login, Kontakt, Deutschland-Karte, Studie):
 * schlanke Topbar mit Wortmarke + Navigation, scrollender Inhalt.
 * Login-Zugang genau EINMAL: rechts in dieser Topbar.
 */
export default function PublicLayout() {
  const { user, checked, fetchMe } = useAuthStore()

  useEffect(() => {
    if (!checked) fetchMe()
  }, [checked, fetchMe])

  return (
    <div className="public-shell">
      <header className="public-topbar">
        <Link to="/" className="public-wordmark">KAP2</Link>
        <nav className="public-nav">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
              className={({ isActive }) => `public-nav-link${isActive ? ' active' : ''}`}
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="public-topbar-right">
          {user ? (
            <Link to="/app" className="btn-primary public-login-btn">Zum Produkt</Link>
          ) : (
            <Link to="/login" className="btn-primary public-login-btn">Anmelden</Link>
          )}
        </div>
      </header>
      <main className="public-content">
        <Outlet />
      </main>
    </div>
  )
}
