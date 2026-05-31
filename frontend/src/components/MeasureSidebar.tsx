import { useEffect, useState } from 'react'
import { useStore } from '../store'
import InfoTooltip from './InfoTooltip'
import type { MeasureImpactSummary } from '../types'

export default function MeasureSidebar() {
  const { selectedMeasure, setSelectedMeasure, calculateImpact, deleteMeasure, updateMeasure, catalog } = useStore()
  const [impact, setImpact] = useState<MeasureImpactSummary | null>(null)
  const [loading, setLoading] = useState(false)
  const [editName, setEditName] = useState('')
  const [editYear, setEditYear] = useState<number>(2026)
  const [dirty, setDirty] = useState(false)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    if (selectedMeasure) {
      setEditName(selectedMeasure.name)
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

  const def = catalog?.measures.find(m => m.code === selectedMeasure.measure_type)
  const linkedRisks = (def?.linked_risk_codes || [])
    .map(c => catalog?.risks.find(r => r.code === c)?.name || c)

  const handleDelete = async () => {
    if (confirm('Maßnahme wirklich löschen?')) {
      await deleteMeasure(selectedMeasure.id)
      setSelectedMeasure(null)
    }
  }

  const handleSave = async () => {
    setSaving(true)
    try {
      const updated = await updateMeasure(selectedMeasure.id, { name: editName, implementation_year: editYear })
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

  const fmtEur = (v?: number) =>
    (v ?? 0).toLocaleString('de-DE', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 })

  return (
    <div className="measure-sidebar">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <input
          value={editName}
          onChange={e => { setEditName(e.target.value); setDirty(true) }}
          style={{
            fontSize: '1rem', fontWeight: 600, border: '1px solid var(--border)',
            borderRadius: 4, padding: '2px 6px', flex: 1, marginRight: 8, background: 'var(--surface)',
          }}
        />
        <button onClick={() => setSelectedMeasure(null)} style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '1.2rem' }}>✕</button>
      </div>

      <div className="card">
        <h3 style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          Typ
          {def && <InfoTooltip title={def.name} description={def.description} rows={[
            { label: 'Wirkt auf', value: def.effect_target.join(', ') },
            { label: 'Minderung', value: `${Math.round((def.default_reduction || 0) * 100)} %` },
          ]} />}
        </h3>
        <div className="value" style={{ fontSize: '1rem' }}>{def?.name || selectedMeasure.measure_type}</div>
      </div>

      <div className="card">
        <h3>Umsetzungsjahr</h3>
        <input
          type="number" value={editYear}
          onChange={e => { setEditYear(parseInt(e.target.value) || 2026); setDirty(true) }}
          style={{ fontSize: '0.9rem', border: '1px solid var(--border)', borderRadius: 4, padding: '2px 6px', width: 80, background: 'var(--surface)' }}
        />
      </div>

      {linkedRisks.length > 0 && (
        <div className="card">
          <h3>Verknüpfte Risiken ({linkedRisks.length})</h3>
          <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', lineHeight: 1.5 }}>
            {linkedRisks.join(' · ')}
          </div>
        </div>
      )}

      {dirty && (
        <button className="btn btn-primary btn-sm" onClick={handleSave} disabled={saving} style={{ width: '100%', marginBottom: 8 }}>
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
            {impact.avg_index_reduction_pct != null && (
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.15rem 0', fontSize: '0.85rem' }}>
                <span style={{ color: 'var(--text-muted)' }}>Ø Risiko-Minderung</span>
                <span style={{ color: 'var(--success)' }}>−{impact.avg_index_reduction_pct.toFixed(1)} %</span>
              </div>
            )}
          </div>

          <div className="card">
            <h3>Kosten</h3>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.15rem 0', fontSize: '0.85rem' }}>
              <span style={{ color: 'var(--text-muted)' }}>Investition</span>
              <span>{fmtEur(impact.investment_eur)}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.15rem 0', fontSize: '0.85rem' }}>
              <span style={{ color: 'var(--text-muted)' }}>Unterhalt/Jahr</span>
              <span>{fmtEur(impact.annual_maintenance_eur)}</span>
            </div>
          </div>

          <div className="card" style={{ borderColor: 'var(--primary)' }}>
            <h3>Nutzen (jährlich)</h3>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.15rem 0', fontSize: '0.85rem' }}>
              <span style={{ color: 'var(--text-muted)' }}>Vermiedene Schäden / Nutzen</span>
              <span style={{ color: 'var(--success)' }}>{fmtEur(impact.annual_benefit_eur)}</span>
            </div>
          </div>
        </>
      )}

      <div style={{ marginTop: '1rem' }}>
        <button className="btn btn-danger btn-sm" onClick={handleDelete}>Maßnahme löschen</button>
      </div>
    </div>
  )
}
