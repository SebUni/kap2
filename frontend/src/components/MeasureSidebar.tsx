import { useEffect, useState } from 'react'
import { useStore } from '../store'
import type { MeasureImpactSummary } from '../types'

export default function MeasureSidebar() {
  const { selectedMeasure, setSelectedMeasure, calculateImpact, deleteMeasure, updateMeasure } = useStore()
  const [impact, setImpact] = useState<MeasureImpactSummary | null>(null)
  const [loading, setLoading] = useState(false)
  const [editName, setEditName] = useState('')
  const [editConfig, setEditConfig] = useState<Record<string, number>>({})
  const [editYear, setEditYear] = useState<number>(2026)
  const [dirty, setDirty] = useState(false)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    if (selectedMeasure) {
      setEditName(selectedMeasure.name)
      setEditConfig(Object.fromEntries(
        Object.entries(selectedMeasure.config || {}).map(([k, v]) => [k, Number(v)])
      ))
      setEditYear(selectedMeasure.implementation_year || 2026)
      setDirty(false)
      setImpact(null)
      setLoading(true)
      calculateImpact(selectedMeasure.id)
        .then(r => setImpact(r))
        .catch(() => {})
        .finally(() => setLoading(false))
    } else {
      setImpact(null)
    }
  }, [selectedMeasure])

  if (!selectedMeasure) return null

  const measureLabels: Record<string, string> = {
    drinking_fountain: 'Trinkbrunnen',
    green_roof: 'Dachbegrünung',
    facade_greening: 'Fassadenbegrünung',
    tree_planting: 'Baumpflanzung',
    unsealing: 'Entsiegelung',
    shade_structure: 'Verschattung',
  }

  const configLabels: Record<string, string> = {
    count: 'Anzahl',
    coverage_pct: 'Abdeckung (%)',
    area_pct: 'Flächenanteil (%)',
    shade_factor: 'Schattenfaktor',
  }

  const handleDelete = async () => {
    if (confirm('Maßnahme wirklich löschen?')) {
      await deleteMeasure(selectedMeasure.id)
      setSelectedMeasure(null)
    }
  }

  const handleSave = async () => {
    setSaving(true)
    try {
      const updated = await updateMeasure(selectedMeasure.id, {
        name: editName,
        config: editConfig,
        implementation_year: editYear,
      })
      setSelectedMeasure(updated)
      setDirty(false)
      setLoading(true)
      const r = await calculateImpact(selectedMeasure.id)
      setImpact(r)
    } catch (e) {
      console.error('Failed to update measure:', e)
    } finally {
      setSaving(false)
      setLoading(false)
    }
  }

  return (
    <div className="measure-sidebar">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <input
          value={editName}
          onChange={e => { setEditName(e.target.value); setDirty(true) }}
          style={{
            fontSize: '1rem', fontWeight: 600, border: '1px solid var(--border)',
            borderRadius: 4, padding: '2px 6px', flex: 1, marginRight: 8,
            background: 'var(--surface)',
          }}
        />
        <button
          onClick={() => setSelectedMeasure(null)}
          style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '1.2rem' }}
        >
          ✕
        </button>
      </div>

      <div className="card">
        <h3>Typ</h3>
        <div className="value" style={{ fontSize: '1rem' }}>
          {measureLabels[selectedMeasure.measure_type] || selectedMeasure.measure_type}
        </div>
      </div>

      <div className="card">
        <h3>Umsetzungsjahr</h3>
        <input
          type="number"
          value={editYear}
          onChange={e => { setEditYear(parseInt(e.target.value) || 2026); setDirty(true) }}
          style={{
            fontSize: '0.9rem', border: '1px solid var(--border)',
            borderRadius: 4, padding: '2px 6px', width: 80,
            background: 'var(--surface)',
          }}
        />
      </div>

      {Object.entries(editConfig).length > 0 && (
        <div className="card">
          <h3>Konfiguration</h3>
          {Object.entries(editConfig).map(([k, v]) => (
            <div key={k} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.85rem', padding: '0.2rem 0' }}>
              <span style={{ color: 'var(--text-muted)' }}>{configLabels[k] || k}</span>
              <input
                type="number"
                value={v}
                onChange={e => {
                  setEditConfig({ ...editConfig, [k]: parseFloat(e.target.value) || 0 })
                  setDirty(true)
                }}
                style={{
                  width: 70, textAlign: 'right', border: '1px solid var(--border)',
                  borderRadius: 4, padding: '1px 4px', fontSize: '0.85rem',
                  background: 'var(--surface)',
                }}
              />
            </div>
          ))}
        </div>
      )}

      {dirty && (
        <button
          className="btn btn-primary btn-sm"
          onClick={handleSave}
          disabled={saving}
          style={{ width: '100%', marginBottom: 8 }}
        >
          {saving ? 'Speichere…' : 'Speichern & neu berechnen'}
        </button>
      )}

      {loading && <div style={{ padding: '1rem', color: 'var(--text-muted)', textAlign: 'center' }}>Berechne Wirkung...</div>}

      {impact && (
        <>
          <div className="card" style={{ borderColor: 'var(--success)' }}>
            <h3>Wirkung</h3>
            <div style={{ fontSize: '0.85rem' }}>
              <strong>{impact.affected_cells}</strong> Zellen betroffen
              {impact.affected_area_m2 != null && (
                <span style={{ color: 'var(--text-muted)', marginLeft: 6 }}>
                  ({(impact.affected_area_m2 / 10000).toFixed(2)} ha)
                </span>
              )}
            </div>
            {Object.entries(impact.total_indicator_deltas || {}).map(([k, v]) => (
              <div key={k} style={{ display: 'flex', justifyContent: 'space-between', padding: '0.15rem 0', fontSize: '0.85rem' }}>
                <span style={{ color: 'var(--text-muted)' }}>{k.replace(/_/g, ' ')}</span>
                <span style={{ color: v < 0 ? 'var(--success)' : 'var(--danger)' }}>
                  {v > 0 ? '+' : ''}{v.toFixed(2)}
                </span>
              </div>
            ))}
          </div>

          <div className="card">
            <h3>Kosten</h3>
            {Object.entries(impact.total_costs || {}).map(([k, v]) => (
              <div key={k} style={{ display: 'flex', justifyContent: 'space-between', padding: '0.15rem 0', fontSize: '0.85rem' }}>
                <span style={{ color: 'var(--text-muted)' }}>{k.replace(/_/g, ' ')}</span>
                <span>{v.toLocaleString('de-DE', { style: 'currency', currency: 'EUR' })}</span>
              </div>
            ))}
          </div>

          <div className="card" style={{ borderColor: 'var(--primary)' }}>
            <h3>Einsparungen (jährlich)</h3>
            {Object.entries(impact.total_savings || {}).map(([k, v]) => (
              <div key={k} style={{ display: 'flex', justifyContent: 'space-between', padding: '0.15rem 0', fontSize: '0.85rem' }}>
                <span style={{ color: 'var(--text-muted)' }}>{k.replace(/_/g, ' ')}</span>
                <span style={{ color: 'var(--success)' }}>
                  {v.toLocaleString('de-DE', { style: 'currency', currency: 'EUR' })}
                </span>
              </div>
            ))}
          </div>
        </>
      )}

      <div style={{ marginTop: '1rem' }}>
        <button className="btn btn-danger btn-sm" onClick={handleDelete}>Maßnahme löschen</button>
      </div>
    </div>
  )
}
