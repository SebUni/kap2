import { useState, useEffect } from 'react'
import { Routes, Route, useNavigate, useLocation, Link } from 'react-router-dom'
import { useStore } from '../store'
import { useAuthStore } from '../store/authStore'
import KommuneSelector from '../components/KommuneSelector'
import MapDashboardTab from '../components/MapDashboardTab'
import Dashboard from '../components/Dashboard'
import MeasuresTableTab from '../components/MeasuresTableTab'
import ConfigPanelTab from '../components/ConfigPanelTab'
import ExportModal from '../components/ExportModal'
import ChatWidget from '../components/chat/ChatWidget'

interface Props {
  /** Demo-Modus: öffentliche Demo-Kommune, unter /demo gemountet. */
  demo?: boolean
}

function tabRoutes(base: string) {
  return [
    { label: 'Dashboard', path: base },
    { label: 'Karte', path: `${base}/karte` },
    { label: 'Maßnahmen-Übersicht', path: `${base}/massnahmen` },
  ]
}

function WelcomePlaceholder() {
  return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', flex: 1, color: 'var(--text-muted)' }}>
      <div style={{ textAlign: 'center' }}>
        <p style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>Willkommen bei KAP2</p>
        <p>Bitte suchen Sie oben eine Kommune, um zu beginnen.</p>
      </div>
    </div>
  )
}

/**
 * Produkt-Shell (ehem. AppContent in App.tsx): fixe Topbar + Tab-Bar +
 * Inhalt, unter /app gemountet. Läuft in einer .app-shell (fixe Viewport-
 * Höhe), damit öffentliche Seiten unabhängig scrollen können.
 */
export default function ProductLayout({ demo = false }: Props) {
  const {
    hasAssessment, kommune, status, setActiveTab, resetKommune, loadStatus,
    configPanelRequested, showConfig, setShowConfig, demoMeta, exitDemo,
  } = useStore()
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()
  const location = useLocation()
  const [showExport, setShowExport] = useState(false)
  const [confirmReset, setConfirmReset] = useState(false)
  const [resetting, setResetting] = useState(false)

  const isAdmin = user?.role === 'admin'
  const base = demo ? '/demo' : '/app'
  const TAB_ROUTES = tabRoutes(base)

  const handleReset = async () => {
    if (!kommune) return
    setResetting(true)
    try {
      await resetKommune(kommune.id)
      navigate(base, { replace: true })
    } finally {
      setResetting(false)
      setConfirmReset(false)
    }
  }

  const handleLogout = async () => {
    await logout()
    navigate('/', { replace: true })
  }

  const hasCompletedAssessment = hasAssessment

  // Produkt betreten → etwaigen geleakten Demo-Zustand des Store-Singletons
  // verwerfen (Demo sperrt Ebenen und hält session-gebundene Maßnahmen). No-op,
  // wenn ohnehin kein Demo-Zustand aktiv ist (normaler Produkt-Start).
  useEffect(() => { if (!demo) exitDemo() }, [demo])

  // Load status when kommune changes (drives tab locking)
  useEffect(() => { if (kommune) loadStatus(kommune.id).catch(() => {}) }, [kommune])

  useEffect(() => {
    if (configPanelRequested > 0) {
      setShowConfig(true)
    }
  }, [configPanelRequested])

  // Projekt-Setup-Flow: Kommune ohne abgeschlossene Berechnung → Konfiguration
  // als Vollbild erzwingen. In der Demo NIE (die Kommune ist vorberechnet und
  // der Nutzer soll die Berechnung nicht anstoßen können).
  useEffect(() => {
    if (!demo && kommune && status && status.status !== 'done') {
      setShowConfig(true)
    }
  }, [demo, kommune?.id, status?.status])

  // Sync store activeTab from URL
  const activeIdx = Math.max(0, TAB_ROUTES.findIndex(t => t.path === location.pathname))
  useEffect(() => { setActiveTab(activeIdx) }, [activeIdx])

  // Redirect away from locked tabs if no assessment done
  useEffect(() => {
    if (!hasCompletedAssessment && (location.pathname === `${base}/karte` || location.pathname === `${base}/massnahmen`)) {
      navigate(base, { replace: true })
    }
  }, [hasCompletedAssessment, location.pathname])

  if (demo) {
    return (
      <div className="app-shell">
        <div className="top-bar">
          <Link to="/" title="Zur Startseite" style={{ textDecoration: 'none', color: 'inherit' }}>
            <h1>KAP2</h1>
          </Link>
          <span className="demo-badge">DEMO</span>
          <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
            {kommune ? `${kommune.name} (vorberechnet)` : 'Demo-Kommune'}
          </span>
          <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <Link to="/kontakt" className="btn-primary" style={{ padding: '0 14px', height: 34, display: 'inline-flex', alignItems: 'center', borderRadius: 8, fontSize: '0.85rem', textDecoration: 'none' }}>
              Vollversion anfragen
            </Link>
            <button
              onClick={() => setShowConfig(!showConfig)}
              title="Parameter ansehen (in der Demo gesperrt)"
              style={{
                background: showConfig ? 'var(--primary)' : 'transparent',
                color: showConfig ? '#fff' : 'var(--text)',
                border: '1px solid var(--border)', borderRadius: 8,
                width: 36, height: 36, display: 'flex', alignItems: 'center',
                justifyContent: 'center', cursor: 'pointer', fontSize: '1.1rem', flexShrink: 0,
              }}
            >
              ⚙
            </button>
            <Link to="/" title="Demo verlassen" style={{ color: 'var(--text-muted)', fontSize: '1.2rem', textDecoration: 'none', padding: '0 4px' }}>✕</Link>
          </div>
        </div>
        <div className="demo-banner">
          ⓘ Demo: {demoMeta?.risks.length ?? 3} von 47 Risiken freigeschaltet. Ihre
          Maßnahmen gelten nur in dieser Sitzung und werden danach gelöscht.
        </div>
        {renderTabsAndContent()}
        {showExport && kommune && (
          <ExportModal kommuneId={kommune.id} onClose={() => setShowExport(false)} />
        )}
      </div>
    )
  }

  function renderTabsAndContent() {
    return (
      <>
        {!showConfig && <div className="tab-bar">
          {TAB_ROUTES.map((tab, i) => {
            const disabled = i > 0 && !hasCompletedAssessment
            return (
              <button
                key={i}
                className={`${activeIdx === i ? 'active' : ''} ${disabled ? 'tab-disabled' : ''}`}
                onClick={() => !disabled && navigate(tab.path)}
                title={disabled ? 'Erst IST-Berechnung durchführen' : undefined}
                style={disabled ? { opacity: 0.4, cursor: 'not-allowed' } : undefined}
              >
                {tab.label}
                {disabled && <span style={{ fontSize: '0.65rem', marginLeft: 4 }}>🔒</span>}
              </button>
            )
          })}
          {kommune && (
            <span style={{ marginLeft: 'auto', alignSelf: 'center', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              {kommune.name} {kommune.area_km2 ? `(${kommune.area_km2.toFixed(1)} km²)` : ''}
            </span>
          )}
        </div>}
        {showConfig ? (
          <ConfigPanelTab />
        ) : (
          <Routes>
            <Route path="/" element={
              kommune ? <div style={{ flex: 1, overflowY: 'auto' }}><Dashboard /></div> : <WelcomePlaceholder />
            } />
            <Route path="karte" element={<MapDashboardTab />} />
            <Route path="massnahmen" element={<MeasuresTableTab />} />
            <Route path="*" element={
              kommune ? <div style={{ flex: 1, overflowY: 'auto' }}><Dashboard /></div> : <WelcomePlaceholder />
            } />
          </Routes>
        )}
      </>
    )
  }

  return (
    <div className="app-shell">
      <div className="top-bar">
        <Link to="/" title="Zur Startseite" style={{ textDecoration: 'none', color: 'inherit' }}>
          <h1>KAP2</h1>
        </Link>
        <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
          Klimafolgen-Anpassungsplanung
        </span>
        <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <KommuneSelector />
          {kommune && (
            confirmReset ? (
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Alle Daten löschen?</span>
                <button
                  onClick={handleReset}
                  disabled={resetting}
                  style={{
                    background: '#dc2626', color: '#fff',
                    border: 'none', borderRadius: 8,
                    padding: '0 12px', height: 34,
                    cursor: resetting ? 'wait' : 'pointer', fontWeight: 600, fontSize: '0.85rem',
                  }}
                >
                  {resetting ? '…' : 'Ja, löschen'}
                </button>
                <button
                  onClick={() => setConfirmReset(false)}
                  disabled={resetting}
                  style={{
                    background: 'transparent', color: 'var(--text)',
                    border: '1px solid var(--border)', borderRadius: 8,
                    padding: '0 12px', height: 34,
                    cursor: 'pointer', fontSize: '0.85rem',
                  }}
                >
                  Abbrechen
                </button>
              </div>
            ) : (
              isAdmin && (
                <button
                  onClick={() => setConfirmReset(true)}
                  title="Alle Berechnungen und Maßnahmen dieser Kommune zurücksetzen"
                  style={{
                    background: 'transparent', color: '#dc2626',
                    border: '1px solid #dc2626', borderRadius: 8,
                    width: 36, height: 36,
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    cursor: 'pointer', fontSize: '1rem', flexShrink: 0,
                  }}
                >
                  🗑
                </button>
              )
            )
          )}
          <button
            onClick={() => setShowExport(true)}
            disabled={!kommune || !hasCompletedAssessment}
            title={hasCompletedAssessment ? 'Daten exportieren' : 'Erst IST-Berechnung durchführen'}
            style={{
              background: 'transparent',
              color: 'var(--text)',
              border: '1px solid var(--border)',
              borderRadius: 8,
              width: 36, height: 36,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              cursor: (!kommune || !hasCompletedAssessment) ? 'not-allowed' : 'pointer',
              fontSize: '1.1rem', flexShrink: 0,
              opacity: (!kommune || !hasCompletedAssessment) ? 0.4 : 1,
            }}
          >
            ⬇
          </button>
          <button
            onClick={() => setShowConfig(!showConfig)}
            title="Konfiguration"
            style={{
              background: showConfig ? 'var(--primary)' : 'transparent',
              color: showConfig ? '#fff' : 'var(--text)',
              border: '1px solid var(--border)',
              borderRadius: 8,
              width: 36, height: 36,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              cursor: 'pointer', fontSize: '1.1rem', flexShrink: 0,
            }}
          >
            ⚙
          </button>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', paddingLeft: '0.5rem', borderLeft: '1px solid var(--border)' }}>
            {isAdmin && (
              <button
                onClick={() => navigate('/admin')}
                title="Admin-Bereich"
                style={{
                  background: 'transparent', color: 'var(--text)',
                  border: '1px solid var(--border)', borderRadius: 8,
                  padding: '0 10px', height: 34, cursor: 'pointer', fontSize: '0.8rem',
                }}
              >
                Admin
              </button>
            )}
            <span title={user?.email} style={{ fontSize: '0.8rem', color: 'var(--text-muted)', maxWidth: 140, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              {user?.display_name || user?.email}
            </span>
            <button
              onClick={handleLogout}
              title="Abmelden"
              style={{
                background: 'transparent', color: 'var(--text)',
                border: '1px solid var(--border)', borderRadius: 8,
                padding: '0 10px', height: 34, cursor: 'pointer', fontSize: '0.8rem',
              }}
            >
              Abmelden
            </button>
          </div>
        </div>
      </div>

      {/* Export Modal */}
      {showExport && kommune && (
        <ExportModal kommuneId={kommune.id} onClose={() => setShowExport(false)} />
      )}

      {renderTabsAndContent()}

      {/* KI-Assistent: schwebendes Chat-Widget (nur Produkt-Shell, nicht Demo) */}
      <ChatWidget />
    </div>
  )
}
