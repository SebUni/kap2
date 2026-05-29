import { useStore } from '../../store'
import { CLIMATE_TYPE_META } from '../../types'

interface Props {
  activeTab: string | null // null = Übersicht
  onTabChange: (tab: string | null) => void
}

export default function ClimateTabs({ activeTab, onTabChange }: Props) {
  const { statuses } = useStore()

  const statusDot = (climateType: string) => {
    const s = statuses.find(x => x.climate_type === climateType)
    if (!s) return 'var(--text-muted)'
    if (s.status === 'done') return 'var(--success)'
    if (s.status === 'running') return 'var(--primary)'
    if (s.status === 'error') return 'var(--danger)'
    return 'var(--text-muted)'
  }

  return (
    <div className="climate-tabs">
      {/* Übersicht tab */}
      <button
        className={`climate-tab ${activeTab === null ? 'active' : ''}`}
        onClick={() => onTabChange(null)}
        style={{ borderBottomColor: activeTab === null ? 'var(--primary)' : 'transparent' }}
      >
        <span style={{ fontSize: '0.95rem' }}>📊</span>
        <span>Übersicht</span>
      </button>

      {/* Per-type tabs */}
      {Object.entries(CLIMATE_TYPE_META).map(([ct, meta]) => (
        <button
          key={ct}
          className={`climate-tab ${activeTab === ct ? 'active' : ''}`}
          onClick={() => onTabChange(ct)}
          style={{
            borderBottomColor: activeTab === ct ? meta.color : 'transparent',
          }}
        >
          <span style={{ fontSize: '0.95rem' }}>{meta.icon}</span>
          <span>{meta.label}</span>
          <span
            className="tab-status-dot"
            style={{ background: statusDot(ct) }}
          />
        </button>
      ))}
    </div>
  )
}
