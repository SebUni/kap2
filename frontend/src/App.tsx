import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, useNavigate, useLocation } from 'react-router-dom'
import { useStore } from './store'
import KommuneSelector from './components/KommuneSelector'
import MapDashboardTab from './components/MapDashboardTab'
import Dashboard from './components/Dashboard'
import MeasuresTableTab from './components/MeasuresTableTab'
import ConfigPanelTab from './components/ConfigPanelTab'
import ExportModal from './components/ExportModal'

const TAB_ROUTES = [
  { label: 'Dashboard', path: '/' },
  { label: 'Karte', path: '/karte' },
  { label: 'Maßnahmen-Übersicht', path: '/massnahmen' },
]

function AppContent() {
  const {
    hasAssessment, kommune, status, setActiveTab, resetKommune, loadStatus,
    configPanelRequested, showConfig, setShowConfig,
  } = useStore()
  const navigate = useNavigate()
  const location = useLocation()
  const [showExport, setShowExport] = useState(false)
  const [confirmReset, setConfirmReset] = useState(false)
  const [resetting, setResetting] = useState(false)

  const handleReset = async () => {
    if (!kommune) return
    setResetting(true)
    try {
      await resetKommune(kommune.id)
      navigate('/', { replace: true })
    } finally {
      setResetting(false)
      setConfirmReset(false)
    }
  }

  const hasCompletedAssessment = hasAssessment

  // Load status when kommune changes (drives tab locking)
  useEffect(() => { if (kommune) loadStatus(kommune.id).catch(() => {}) }, [kommune])

  useEffect(() => {
    if (configPanelRequested > 0) {
      setShowConfig(true)
    }
  }, [configPanelRequested])

  // Projekt-Setup-Flow: Kommune ohne abgeschlossene Berechnung → Konfiguration
  // als Vollbild erzwingen (dort wird die Berechnung gestartet; das Dashboard
  // zeigt nur noch Ergebnisse).
  useEffect(() => {
    if (kommune && status && status.status !== 'done') {
      setShowConfig(true)
    }
  }, [kommune?.id, status?.status])

  // Sync store activeTab from URL
  const activeIdx = Math.max(0, TAB_ROUTES.findIndex(t => t.path === location.pathname))
  useEffect(() => { setActiveTab(activeIdx) }, [activeIdx])

  // Redirect away from locked tabs if no assessment done
  useEffect(() => {
    if (!hasCompletedAssessment && (location.pathname === '/karte' || location.pathname === '/massnahmen')) {
      navigate('/', { replace: true })
    }
  }, [hasCompletedAssessment, location.pathname])

  return (
    <>
      <div className="top-bar">
        <h1>KAP2</h1>
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
        </div>
      </div>

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
          <span style={{
            marginLeft: 'auto', alignSelf: 'center',
            fontSize: '0.8rem', color: 'var(--text-muted)'
          }}>
            {kommune.name} {kommune.area_km2 ? `(${kommune.area_km2.toFixed(1)} km²)` : ''}
          </span>
        )}
      </div>}

      {/* Export Modal */}
      {showExport && kommune && (
        <ExportModal kommuneId={kommune.id} onClose={() => setShowExport(false)} />
      )}

      {showConfig ? (
        <ConfigPanelTab />
      ) : (
        <Routes>
          <Route path="/" element={
            kommune
              ? <div style={{ flex: 1, overflowY: 'auto' }}><Dashboard /></div>
              : <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', flex: 1, color: 'var(--text-muted)' }}>
                  <div style={{ textAlign: 'center' }}>
                    <p style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>Willkommen bei KAP2</p>
                    <p>Bitte suchen Sie oben eine Kommune, um zu beginnen.</p>
                  </div>
                </div>
          } />
          <Route path="/karte" element={<MapDashboardTab />} />
          <Route path="/massnahmen" element={<MeasuresTableTab />} />
          {/* Fallback to dashboard */}
          <Route path="*" element={
            kommune
              ? <div style={{ flex: 1, overflowY: 'auto' }}><Dashboard /></div>
              : <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', flex: 1, color: 'var(--text-muted)' }}>
                  <div style={{ textAlign: 'center' }}>
                    <p style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>Willkommen bei KAP2</p>
                    <p>Bitte suchen Sie oben eine Kommune, um zu beginnen.</p>
                  </div>
                </div>
          } />
        </Routes>
      )}
    </>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  )
}
