import { useEffect, useState } from 'react'
import { useStore } from '../store'
import InfoTooltip from './InfoTooltip'
import type { MeasureImpactSummary } from '../types'
import { measureReductionText, S157_S_GEK_DEFAULT_PCT, VG_KALIB_FRAGE } from '../utils/measureEffect'

export default function MeasureSidebar() {
  const { selectedMeasure, setSelectedMeasure, calculateImpact, deleteMeasure, updateMeasure, catalog } = useStore()
  const [impact, setImpact] = useState<MeasureImpactSummary | null>(null)
  const [loading, setLoading] = useState(false)
  const [editName, setEditName] = useState('')
  const [editYear, setEditYear] = useState<number>(2026)
  const [editCount, setEditCount] = useState<number | null>(null)
  // S157 (#95 §5): gekühlter Anteil der Heimplätze in Prozent; null = keine Eingabe
  // (dann rechnet das Backend mit der Voreinstellung 11 %, Befund 138).
  const [editSgek, setEditSgek] = useState<number | null>(null)
  // Wächter-Frage (#95 §5, Befund 150): 1 = ja, 0 = nein; null = keine Eingabe
  // (dann gilt die Voreinstellung „nein“).
  const [editVgKalib, setEditVgKalib] = useState<number | null>(null)
  // Stadtbaumwahl (#96 §5, T-1603-cto): Anteil ersetzter allergener Kronen in Prozent;
  // null = keine Eingabe.
  const [editAnteilErsetzt, setEditAnteilErsetzt] = useState<number | null>(null)
  // Ersatzfall der Stadtbaumwahl (Ü-11): 'nachpflanzung' | 'vorgezogen'; null = nicht gewählt.
  const [editErsatzfall, setEditErsatzfall] = useState<string | null>(null)
  const [showBreakdown, setShowBreakdown] = useState(false)
  const [dirty, setDirty] = useState(false)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    if (selectedMeasure) {
      setEditName(selectedMeasure.name)
      setEditYear(selectedMeasure.implementation_year || 2026)
      setEditCount(null)
      const sg = (selectedMeasure.config as Record<string, unknown> | null | undefined)?.s_gek
      setEditSgek(typeof sg === 'number' ? Math.round(sg * 1000) / 10 : null)
      const ae = (selectedMeasure.config as Record<string, unknown> | null | undefined)?.anteil_ersetzt
      setEditAnteilErsetzt(typeof ae === 'number' ? Math.round(ae * 1000) / 10 : null)
      const ef = (selectedMeasure.config as Record<string, unknown> | null | undefined)?.ersatzfall
      setEditErsatzfall(ef === 'nachpflanzung' || ef === 'vorgezogen' ? ef : null)
      const vk = (selectedMeasure.config as Record<string, unknown> | null | undefined)?.vg_in_kalibrierjahren
      setEditVgKalib(typeof vk === 'number' ? (vk >= 0.5 ? 1 : 0)
        : typeof vk === 'boolean' ? (vk ? 1 : 0) : null)
      setShowBreakdown(false)
      setDirty(false)
      setImpact(null)
      setLoading(true)
      calculateImpact(selectedMeasure.id)
        .then(r => {
          setImpact(r)
          if (r.unit_label != null && r.count != null) setEditCount(r.count)
        })
        .catch(() => {})
        .finally(() => setLoading(false))
    } else {
      setImpact(null)
    }
  }, [selectedMeasure])

  if (!selectedMeasure) return null

  const def = catalog?.measures.find(m => m.code === selectedMeasure.measure_type)
  const isS157 = selectedMeasure.measure_type === 'COOLING_ROOMS_DRINKING_WATER'
  const isS158 = selectedMeasure.measure_type === 'POLLEN_EARLY_WARNING'
  const isStadtbaum = selectedMeasure.measure_type === 'LOW_ALLERGEN_TREE_SELECTION'
  // Wächter-Frage „Lief das Programm schon 2012–2024?“ (Befund 150): Schutzprogramme und
  // Kühle Räume / Kühlzentren.
  const hasVgKalib = isS157 || selectedMeasure.measure_type === 'VULNERABLE_GROUP_PROGRAMS'
  const vgKalibSpec = def?.config_inputs?.vg_in_kalibrierjahren
  const vgKalibHelp = def?.config_input_help?.vg_in_kalibrierjahren
  const anteilErsetztHelp = def?.config_input_help?.anteil_ersetzt
  const reductionIsEstimated = def?.evidence_classes?.default_reduction === 'abgeschaetzt'
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
      const payload: Record<string, unknown> = { name: editName, implementation_year: editYear }
      if (impact?.unit_label != null && editCount != null) {
        payload.config = { ...(selectedMeasure.config || {}), count: editCount }
      }
      if (isS157) {
        const base = { ...((payload.config as Record<string, unknown>) || selectedMeasure.config || {}) }
        if (editSgek == null) delete base.s_gek
        else base.s_gek = Math.max(0, Math.min(100, editSgek)) / 100
        payload.config = base
      }
      if (hasVgKalib) {
        const base = { ...((payload.config as Record<string, unknown>) || selectedMeasure.config || {}) }
        if (editVgKalib == null) delete base.vg_in_kalibrierjahren
        else base.vg_in_kalibrierjahren = editVgKalib
        payload.config = base
      }
      if (isStadtbaum) {
        const base = { ...((payload.config as Record<string, unknown>) || selectedMeasure.config || {}) }
        if (editAnteilErsetzt == null) delete base.anteil_ersetzt
        else base.anteil_ersetzt = Math.max(0.1, Math.min(100, editAnteilErsetzt)) / 100
        if (editErsatzfall == null) delete base.ersatzfall
        else base.ersatzfall = editErsatzfall
        payload.config = base
      }
      const updated = await updateMeasure(selectedMeasure.id, payload)
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
            { label: 'Minderung', value: measureReductionText(def) },
          ]} />}
        </h3>
        <div className="value" style={{ fontSize: '1rem' }}>{def?.name || selectedMeasure.measure_type}</div>
        {reductionIsEstimated && (
          <div style={{ fontSize: '0.75rem', color: 'var(--warning, #b45309)', marginTop: 4, lineHeight: 1.4 }}>
            Wirkung: begründete Abschätzung von KAP3, keine belegte Effektgröße
          </div>
        )}
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
            {impact.unit_factor != null && impact.unit_factor < 1 && (
              <div style={{ fontSize: '0.72rem', color: 'var(--warning, #b45309)', marginTop: 4 }}>
                Wirkung auf {Math.round(impact.unit_factor * 100)}% skaliert ({impact.count} von {impact.recommended_count} {impact.unit_label})
              </div>
            )}
          </div>

          {impact.unit_label != null && (
            <div className="card">
              <h3>
                Anzahl ({impact.unit_label})
                {impact.count_is_default && (
                  <span className="kap-prov-badge" style={{ marginLeft: 8 }}>Anzahl = Richtwert</span>
                )}
              </h3>
              <input
                type="number" min={0} value={editCount ?? ''}
                onChange={e => { setEditCount(e.target.value === '' ? null : parseInt(e.target.value, 10) || 0); setDirty(true) }}
                style={{ fontSize: '0.9rem', border: '1px solid var(--border)', borderRadius: 4, padding: '2px 6px', width: 80, background: 'var(--surface)' }}
              />
              <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: 4 }}>
                Richtwert: {impact.recommended_count}
              </div>
            </div>
          )}

          {isS157 && (
            <div className="card">
              <h3>Gekühlter Anteil der Heimplätze (%)</h3>
              <input
                type="number" min={0} max={100} step={1} value={editSgek ?? ''}
                placeholder={`Voreinstellung ${S157_S_GEK_DEFAULT_PCT} %`}
                onChange={e => { setEditSgek(e.target.value === '' ? null : Number(e.target.value)); setDirty(true) }}
                style={{ fontSize: '0.9rem', border: '1px solid var(--border)', borderRadius: 4, padding: '2px 6px', width: 120, background: 'var(--surface)' }}
              />
              <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: 4 }}>
                Nur Heimplätze mit Klimaanlage im Wohnbereich zählen. Ohne Eingabe rechnet KAP3 mit der
                Voreinstellung {S157_S_GEK_DEFAULT_PCT} % (Abschätzung von KAP3; Methodik-Bericht #95, Hebel S157).
              </div>
              {impact.s_gek_is_default && (
                <div style={{ fontSize: '0.72rem', color: 'var(--warning, #b45309)', marginTop: 4 }}>
                  Gerechnet mit der Voreinstellung{impact.s_gek != null
                    ? ` ${(impact.s_gek * 100).toLocaleString('de-DE', { maximumFractionDigits: 1 })} %` : ''}
                  {' '}({impact.s157_estimate_note || 'Abschätzung von KAP3'})
                </div>
              )}
            </div>
          )}

          {hasVgKalib && (
            <div className="card">
              <h3>{VG_KALIB_FRAGE}</h3>
              <select
                value={String(editVgKalib ?? impact.vg_in_kalibrierjahren ?? vgKalibSpec?.voreinstellung ?? 0)}
                onChange={e => { setEditVgKalib(Number(e.target.value)); setDirty(true) }}
                style={{ fontSize: '0.9rem', border: '1px solid var(--border)', borderRadius: 4, padding: '2px 6px', background: 'var(--surface)' }}
              >
                <option value="0">nein</option>
                <option value="1">ja</option>
              </select>
              {(editVgKalib == null && impact.vg_in_kalibrierjahren_is_default !== false) && (
                <span className="kap-prov-badge" style={{ marginLeft: 8 }}>
                  Voreinstellung „{vgKalibSpec?.voreinstellung_text || 'nein'}“
                  ({impact.vg_in_kalibrierjahren_estimate_note || vgKalibSpec?.kennzeichnung || 'Abschätzung von KAP3'})
                </span>
              )}
              {vgKalibHelp && (
                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: 4 }}>
                  {vgKalibHelp}
                </div>
              )}
            </div>
          )}

          {isStadtbaum && (
            <div className="card">
              <h3>Änderung des Kronenanteils (%)</h3>
              <input
                type="number" min={0.1} max={100} step={1} value={editAnteilErsetzt ?? ''}
                placeholder="nicht eingegeben"
                onChange={e => { setEditAnteilErsetzt(e.target.value === '' ? null : Number(e.target.value)); setDirty(true) }}
                style={{ fontSize: '0.9rem', border: '1px solid var(--border)', borderRadius: 4, padding: '2px 6px', width: 120, background: 'var(--surface)' }}
              />
              <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: 4 }}>
                {anteilErsetztHelp || 'Anteil a (0 < a ≤ 1) der ersetzten allergenen Kronen '
                  + '(Methodik-Bericht #96, Stadtbaumwahl).'}
              </div>
            </div>
          )}

          {isStadtbaum && (
            <div className="card">
              <h3>Ersatzfall</h3>
              <select
                value={editErsatzfall ?? ''}
                onChange={e => { setEditErsatzfall(e.target.value === '' ? null : e.target.value); setDirty(true) }}
                style={{ fontSize: '0.9rem', border: '1px solid var(--border)', borderRadius: 4, padding: '2px 6px', background: 'var(--surface)' }}
              >
                <option value="">bitte wählen</option>
                <option value="nachpflanzung">Nachpflanzung ohnehin</option>
                <option value="vorgezogen">vorgezogener Ersatz</option>
              </select>
            </div>
          )}

          <div className="card">
            <h3 style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              Kosten
              <InfoTooltip
                title="Kosten"
                description="CAPEX (einmalige Investition) und OPEX (jährliche Betriebs- & Unterhaltskosten) ergeben sich aus Anzahl/Fläche × Katalog-Einheitspreisen."
                note="Enthält ggf. kommunale Override-Preise – Details unter „Herleitung anzeigen“."
              />
            </h3>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.15rem 0', fontSize: '0.85rem' }}>
              <span style={{ color: 'var(--text-muted)' }}>CAPEX (einmalig)</span>
              <span>{impact.capex_je_fall ? '–' : fmtEur(impact.capex_eur)}</span>
            </div>
            {isStadtbaum && impact.capex_je_fall && (
              <div style={{ fontSize: '0.85rem' }}>
                {([['nachpflanzung', 'CAPEX bei Nachpflanzung ohnehin'], ['vorgezogen', 'CAPEX bei vorgezogenem Ersatz']] as const).map(([fall, label]) => (
                  <div key={fall} style={{ display: 'flex', justifyContent: 'space-between', padding: '0.15rem 0' }}>
                    <span style={{ color: 'var(--text-muted)' }}>{label}</span>
                    <span>{fmtEur(impact.capex_je_fall![fall])}</span>
                  </div>
                ))}
              </div>
            )}
            {isStadtbaum && impact.kosten_vermerk && (
              <div style={{ fontSize: '0.72rem', color: 'var(--warning, #b45309)', marginTop: 4, lineHeight: 1.4 }}>
                {impact.kosten_vermerk}
              </div>
            )}
            {isStadtbaum && impact.stadtbaum_kosten_hinweis && (
              <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: 4, lineHeight: 1.4 }}>
                {impact.stadtbaum_kosten_hinweis}
              </div>
            )}
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.15rem 0', fontSize: '0.85rem' }}>
              <span style={{ color: 'var(--text-muted)' }}>OPEX/Jahr</span>
              <span>{fmtEur(impact.opex_annual_eur)}</span>
            </div>

            {impact.cost_breakdown && (
              <>
                <button
                  type="button" className="btn btn-secondary btn-sm" style={{ marginTop: 6 }}
                  onClick={() => setShowBreakdown(v => !v)}
                >
                  {showBreakdown ? 'Herleitung ausblenden' : 'Herleitung anzeigen'}
                </button>
                {showBreakdown && (
                  <div style={{ marginTop: 6, fontSize: '0.75rem' }}>
                    {(['capex', 'opex'] as const).map(blockKey => (
                      <div key={blockKey} style={{ marginBottom: 6 }}>
                        <div style={{ fontWeight: 600, color: 'var(--text-muted)' }}>
                          {blockKey === 'capex' ? 'CAPEX (einmalige Investition)' : 'OPEX/Jahr (Betrieb & Unterhalt)'}
                        </div>
                        {impact.cost_breakdown![blockKey].components.map((c, i) => (
                          <div key={i} style={{ padding: '2px 0', borderBottom: '1px solid var(--border)' }}>
                            <div>
                              {c.quantity.toLocaleString('de-DE')} × {c.unit_price.toLocaleString('de-DE')} €/{c.quantity_unit}
                              {' = '}{c.amount_eur.toLocaleString('de-DE', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 })}
                              {c.overridden && <span className="kap-prov-badge" style={{ marginLeft: 6 }}>Override</span>}
                            </div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: 4, color: 'var(--text-muted)', fontSize: '0.68rem' }}>
                              <span>{c.source}</span>
                              {(c.source_detail || (c.references && c.references.length > 0)) && (
                                <InfoTooltip
                                  title={c.source || 'Quelle'}
                                  description={c.source_detail}
                                  references={c.references}
                                />
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    ))}
                  </div>
                )}
              </>
            )}
          </div>

          <div className="card" style={{ borderColor: 'var(--primary)' }}>
            <h3>Nutzen (jährlich)</h3>
            {isS158 && !impact.benefit_display && impact.s158_avoided_days_total != null && (
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.15rem 0', fontSize: '0.85rem' }}>
                <span style={{ color: 'var(--text-muted)' }}>Vermiedene Symptomtage/Jahr</span>
                <span style={{ color: 'var(--success)' }}>
                  {impact.s158_avoided_days_total.toLocaleString('de-DE', { maximumFractionDigits: 1 })} Tage
                </span>
              </div>
            )}
            {isStadtbaum && !impact.benefit_display && impact.stadtbaum_avoided_days_total != null && (
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.15rem 0', fontSize: '0.85rem' }}>
                <span style={{ color: 'var(--text-muted)' }}>Vermiedene Zusatztage/Jahr</span>
                <span style={{ color: 'var(--success)' }}>
                  {impact.stadtbaum_avoided_days_total.toLocaleString('de-DE', { maximumFractionDigits: 1 })} Tage
                </span>
              </div>
            )}
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.15rem 0', fontSize: '0.85rem' }}>
              <span style={{ color: 'var(--text-muted)' }}>Vermiedene Schäden / Nutzen</span>
              <span style={{ color: 'var(--success)' }}>{impact.benefit_display
                ? impact.benefit_display
                : <>{fmtEur(impact.annual_benefit_eur)}{impact.benefit_note && <span style={{ display: 'block', fontSize: '0.75rem', color: 'var(--text-muted)' }}>{impact.benefit_note}</span>}</>}</span>
            </div>
            {isStadtbaum && impact.stadtbaum_s_unbek_hinweis && (
              <div style={{ fontSize: '0.72rem', color: 'var(--warning, #b45309)', marginTop: 2 }}>
                {impact.stadtbaum_s_unbek_hinweis}
              </div>
            )}
            {isS157 && !impact.benefit_display && impact.kuehlzentren_benefit_eur != null && (
              <div style={{ marginTop: 4, fontSize: '0.8rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.15rem 0' }}>
                  <span style={{ color: 'var(--text-muted)' }}>davon gekühlte Heimplätze (S157)</span>
                  <span style={{ color: 'var(--success)' }}>{fmtEur(impact.s157_benefit_eur)}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.15rem 0' }}>
                  <span style={{ color: 'var(--text-muted)' }}>davon öffentliche Kühlzentren</span>
                  <span style={{ color: 'var(--success)' }}>{fmtEur(impact.kuehlzentren_benefit_eur)}</span>
                </div>
                <div style={{ fontSize: '0.72rem', color: 'var(--warning, #b45309)', marginTop: 4, lineHeight: 1.4 }}>
                  Beide Beträge sind eine Abschätzung von KAP3: S157 mit dem gekühlten Anteil
                  {impact.s_gek != null
                    ? ` ${(impact.s_gek * 100).toLocaleString('de-DE', { maximumFractionDigits: 1 })} %` : ''}
                  {impact.s_gek_is_default ? ' (Voreinstellung)' : ' (Eingabe der Kommune)'}, Kühlzentren mit δ_KZ
                  {impact.delta_kuehlzentren != null
                    ? ` ${impact.delta_kuehlzentren.toLocaleString('de-DE', { maximumFractionDigits: 4 })}` : ''}
                  {impact.vg_in_kalibrierjahren === 1 ? ' — Kühlzentren liefen schon 2012–2024, daher kein Zusatzbetrag' : ''}
                  {' '}(Methodik-Bericht #95 §5).
                </div>
              </div>
            )}
            {isS158 && !impact.benefit_display && impact.s158_estimate_note && (
              <div style={{ fontSize: '0.72rem', color: 'var(--warning, #b45309)', marginTop: 4 }}>
                {impact.s158_estimate_note}
              </div>
            )}
            {isStadtbaum && !impact.benefit_display && impact.stadtbaum_estimate_note && (
              <div style={{ fontSize: '0.72rem', color: 'var(--warning, #b45309)', marginTop: 4 }}>
                {impact.stadtbaum_estimate_note}
                {impact.stadtbaum_lambda_hinweis && (
                  <div style={{ marginTop: 2 }}>{impact.stadtbaum_lambda_hinweis}</div>
                )}
              </div>
            )}
          </div>
        </>
      )}

      <div style={{ marginTop: '1rem' }}>
        <button className="btn btn-danger btn-sm" onClick={handleDelete}>Maßnahme löschen</button>
      </div>
    </div>
  )
}
