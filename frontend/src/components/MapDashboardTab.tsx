import { useStore } from '../store'
import MapView from './MapView'
import MeasureSidebar from './MeasureSidebar'

export default function MapDashboardTab() {
  const { kommune, selectedMeasure } = useStore()

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
    <div className="main-content">
      <div className="map-container" style={{ flex: 1, position: 'relative' }}>
        <MapView />
        {selectedMeasure && <MeasureSidebar />}
      </div>
    </div>
  )
}
