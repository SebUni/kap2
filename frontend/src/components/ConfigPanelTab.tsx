import { useState, useEffect } from 'react'
import { useStore } from '../store'

export default function ConfigPanelTab() {
  const { kommune, configParams, loadConfig, updateConfig, statuses, loadStatuses } = useStore()
  const [edits, setEdits] = useState<Record<string, unknown>>({})
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    if (kommune) {
      loadConfig(kommune.id)
      loadStatuses(kommune.id)
    }
  }, [kommune?.id])

  if (!kommune) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', flex: 1, color: 'var(--text-muted)' }}>
        Bitte wählen Sie eine Kommune.
      </div>
    )
  }

  // Group by category
  const categories: Record<string, typeof configParams> = {}
  for (const p of configParams) {
    if (!categories[p.category]) categories[p.category] = []
    categories[p.category].push(p)
  }

  const categoryLabels: Record<string, string> = {
    heat: 'Hitze-Parameter',
    costs: 'Kostenannahmen',
    savings: 'Einsparungsannahmen',
  }

  const handleChange = (category: string, key: string, value: string) => {
    const numVal = parseFloat(value)
    setEdits({ ...edits, [`${category}.${key}`]: isNaN(numVal) ? value : numVal })
  }

  const handleSave = async () => {
    setSaving(true)
    const updates = Object.entries(edits).map(([ck, value]) => {
      const [category, key] = ck.split('.')
      return { category, key, value }
    })
    await updateConfig(kommune.id, updates)
    setEdits({})
    setSaving(false)
  }

  const heatStatus = statuses.find(s => s.climate_type === 'heat')
  const isReady = heatStatus?.status === 'done'
  const isRunning = heatStatus?.status === 'running'

  return (
    <div style={{ flex: 1, overflow: 'auto', padding: '1.5rem', maxWidth: 800, margin: '0 auto' }}>
      <h2 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '1rem' }}>Konfiguration</h2>

      {/* Status Indicator */}
      <div className="card" style={{ marginBottom: '1.5rem', borderColor: isReady ? 'var(--success)' : isRunning ? 'var(--primary)' : 'var(--warning)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h3 style={{ fontSize: '0.9rem', fontWeight: 600, marginBottom: 4 }}>Projektstatus</h3>
            <span className={`status-badge ${heatStatus?.status || 'pending'}`}>
              {isReady ? '✓ Startklar – Anpassungen können modelliert werden' :
               isRunning ? `⟳ Berechnung läuft: ${heatStatus?.progress_pct?.toFixed(0)}%` :
               heatStatus?.status === 'error' ? `✕ Fehler: ${heatStatus?.message}` :
               '○ Berechnung ausstehend'}
            </span>
          </div>
          <div style={{ fontSize: '2rem' }}>
            {isReady ? '🟢' : isRunning ? '🔵' : '🟡'}
          </div>
        </div>
        {isRunning && (
          <div className="progress-bar" style={{ marginTop: 8 }}>
            <div className="fill" style={{ width: `${heatStatus?.progress_pct || 0}%` }} />
          </div>
        )}
      </div>

      {/* Config Parameters */}
      {Object.entries(categories).map(([cat, params]) => (
        <div className="config-section" key={cat}>
          <h3>{categoryLabels[cat] || cat}</h3>
          {params.map(p => {
            const editKey = `${p.category}.${p.key}`
            const currentVal = edits[editKey] !== undefined ? edits[editKey] : p.value
            return (
              <div className="config-row" key={p.key}>
                <label title={p.description || ''}>
                  {p.description || p.key}
                </label>
                <input
                  type="number"
                  step="any"
                  value={String(currentVal)}
                  onChange={e => handleChange(p.category, p.key, e.target.value)}
                />
              </div>
            )
          })}
        </div>
      ))}

      {Object.keys(edits).length > 0 && (
        <div style={{ position: 'sticky', bottom: 0, padding: '1rem 0', background: 'var(--bg)' }}>
          <button className="btn btn-primary" onClick={handleSave} disabled={saving}>
            {saving ? 'Speichern...' : `${Object.keys(edits).length} Änderungen speichern`}
          </button>
          <button className="btn btn-secondary" onClick={() => setEdits({})} style={{ marginLeft: 8 }}>
            Verwerfen
          </button>
        </div>
      )}
    </div>
  )
}
