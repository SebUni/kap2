import { useEffect } from 'react'
import { useStore } from '../store'
import MapView from './MapView'
import MeasureSidebar from './MeasureSidebar'
import LayerPanel from './LayerPanel'

export default function MapDashboardTab() {
  const { kommune, selectedMeasure, catalog, loadCatalog, loadMeasures, activeLayer, setActiveLayer } = useStore()

  useEffect(() => { loadCatalog().catch(() => {}) }, [])

  useEffect(() => {
    if (!kommune) return
    loadMeasures(kommune.id).catch(() => {})
  }, [kommune])

  // Default to first risk layer once catalog is available
  useEffect(() => {
    if (catalog && !activeLayer && catalog.risks.length > 0) {
      setActiveLayer({ category: 'risks', code: catalog.risks[0].code }).catch(() => {})
    }
  }, [catalog])

  if (!kommune) {
    return (
      <div style={{
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        flex: 1, color: 'var(--text-muted)'
      }}>
        <div style={{ textAlign: 'center' }}>
          <p style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>
            Willkommen bei KAP2
          </p>
          <p>Bitte suchen Sie oben eine Kommune, um zu beginnen.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="main-content" style={{ display: 'flex', flex: 1, minHeight: 0 }}>
      <LayerPanel />
      <div className="map-container" style={{ flex: 1, position: 'relative' }}>
        <MapView />
        {selectedMeasure && <MeasureSidebar />}
      </div>
    </div>
  )
}
