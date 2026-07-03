import { useState, useEffect, type Dispatch, type ReactNode, type SetStateAction } from 'react'
import { api } from '../api/client'
import type { Catalog, ModelParameter } from '../types'
import {
  buildIndicatorUsageIndex,
  indicatorName,
  mainSectionKeyFromAnchor,
  measureOutputLinks,
  paramSectionId,
  riskInputLinks,
  type ParamSectionLink,
} from '../utils/paramSectionLinks'

interface Props {
  kommuneId: number
  parameters: ModelParameter[]
  onUpdated: () => void
  compact?: boolean
  showExport?: boolean
  grouped?: boolean
  catalog?: Catalog
  scrollAnchor?: string | null
  scrollTrigger?: number
}

export default function ParameterTable({
  kommuneId, parameters, onUpdated, compact, showExport = true, grouped, catalog, scrollAnchor, scrollTrigger,
}: Props) {
  const [edits, setEdits] = useState<Record<string, { value: string; source: string }>>({})
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const startEdit = (p: ModelParameter) => {
    setEdits({
      ...edits,
      [p.id]: { value: String(p.value), source: p.custom_source || '' },
    })
  }

  const cancelEdit = (id: string) => {
    const next = { ...edits }
    delete next[id]
    setEdits(next)
  }

  const saveOne = async (p: ModelParameter) => {
    const e = edits[p.id]
    if (!e) return
    const num = parseFloat(e.value)
    const value = Number.isNaN(num) ? e.value : num
    if (value !== p.default_value && !e.source.trim()) {
      setError('Bitte Quellenangabe angeben, wenn der Wert vom Default abweicht.')
      return
    }
    setSaving(true)
    setError(null)
    try {
      await api.updateParameters(kommuneId, [{
        parameter_id: p.id,
        value,
        custom_source: e.source.trim() || undefined,
      }])
      cancelEdit(p.id)
      onUpdated()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Speichern fehlgeschlagen')
    } finally {
      setSaving(false)
    }
  }

  if (!parameters.length) {
    const msg = grouped
      ? 'Keine Parameter geladen. Bitte prüfen Sie, ob das Backend läuft, und laden Sie die Seite neu.'
      : 'Keine Parameter für diese Ebene.'
    return <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{msg}</p>
  }

  if (grouped) {
    return (
      <GroupedParameterList
        kommuneId={kommuneId}
        parameters={parameters}
        catalog={catalog}
        edits={edits}
        setEdits={setEdits}
        saving={saving}
        error={error}
        setError={setError}
        saveOne={saveOne}
        cancelEdit={cancelEdit}
        startEdit={startEdit}
        showExport={showExport}
        scrollAnchor={scrollAnchor}
        scrollTrigger={scrollTrigger}
      />
    )
  }

  return (
    <div className={compact ? 'kap-param-table compact' : 'kap-param-table'}>
      {showExport && (
        <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 8 }}>
          <a
            className="btn btn-secondary"
            href={api.exportParametersUrl(kommuneId)}
            download
            style={{ fontSize: '0.75rem', padding: '4px 10px', textDecoration: 'none' }}
          >
            Parameter exportieren (xlsx)
          </a>
        </div>
      )}
      {error && <div className="kap-param-error">{error}</div>}
      <table>
        <thead>
          <tr>
            <th>Bezeichnung</th>
            <th>Wert</th>
            <th>Einheit</th>
            <th>Quelle</th>
            <th>Status</th>
            {!compact && <th />}
          </tr>
        </thead>
        <tbody>
          {parameters.map(p => {
            const editing = edits[p.id]
            return (
              <tr key={p.id} className={p.overridden ? 'overridden' : ''}>
                <td><span className="kap-param-cell-text" title={p.label}>{p.label}</span></td>
                <td>
                  {editing ? (
                    <input
                      type="number"
                      step="any"
                      value={editing.value}
                      onChange={ev => setEdits({
                        ...edits,
                        [p.id]: { ...editing, value: ev.target.value },
                      })}
                      style={{ width: '100%', fontSize: '0.75rem' }}
                    />
                  ) : (
                    <span>{String(p.value)}</span>
                  )}
                </td>
                <td>{p.unit}</td>
                <td>
                  {editing ? (
                    <input
                      type="text"
                      placeholder="Quelle bei Änderung"
                      value={editing.source}
                      onChange={ev => setEdits({
                        ...edits,
                        [p.id]: { ...editing, source: ev.target.value },
                      })}
                      style={{ width: '100%', fontSize: '0.75rem' }}
                    />
                  ) : (
                    <span className="kap-param-cell-text" title={p.custom_source || p.source || ''}>
                      {p.custom_source || p.source}
                    </span>
                  )}
                </td>
                <td>
                  <span className={`kap-param-status ${p.overridden ? 'is-override' : ''}`}>
                    {p.overridden ? 'Override' : 'Default'}
                  </span>
                </td>
                {!compact && (
                  <td style={{ whiteSpace: 'nowrap' }}>
                    {editing ? (
                      <>
                        <button
                          className="btn btn-primary"
                          style={{ fontSize: '0.7rem', padding: '2px 8px' }}
                          disabled={saving}
                          onClick={() => saveOne(p)}
                        >Speichern</button>
                        <button
                          className="btn btn-secondary"
                          style={{ fontSize: '0.7rem', padding: '2px 8px', marginLeft: 4 }}
                          onClick={() => cancelEdit(p.id)}
                        >Abbrechen</button>
                      </>
                    ) : p.editable ? (
                      <button
                        className="btn btn-secondary"
                        style={{ fontSize: '0.7rem', padding: '2px 8px' }}
                        onClick={() => startEdit(p)}
                      >Bearbeiten</button>
                    ) : null}
                  </td>
                )}
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

function ParamCrossRefHint({ intro, links }: { intro: string; links: ParamSectionLink[] }) {
  if (!links.length) return null
  return (
    <p className="kap-param-crossref-hint">
      <em>{intro}</em>{' '}
      {links.map((link, i) => (
        <span key={link.href}>
          {i > 0 ? ' · ' : ''}
          <a href={link.href} className="kap-param-anchor-link">{link.label}</a>
        </span>
      ))}
    </p>
  )
}

const PARAM_TABLE_COLGROUP = (
  <colgroup>
    <col className="kap-param-col-label" />
    <col className="kap-param-col-value" />
    <col className="kap-param-col-unit" />
    <col className="kap-param-col-source" />
    <col className="kap-param-col-status" />
    <col className="kap-param-col-actions" />
  </colgroup>
)

function CollapsibleParamSection({
  sectionKey,
  title,
  anchorId,
  count,
  expanded,
  onToggle,
  children,
}: {
  sectionKey: string
  title: string
  anchorId: string
  count: number
  expanded: boolean
  onToggle: (key: string) => void
  children: ReactNode
}) {
  return (
    <section className={`kap-param-section${expanded ? ' is-open' : ' is-collapsed'}`}>
      <button
        type="button"
        className="kap-param-section-toggle"
        aria-expanded={expanded}
        onClick={() => onToggle(sectionKey)}
      >
        <span className="kap-param-section-chevron" aria-hidden>{expanded ? '▾' : '▸'}</span>
        <span className="kap-param-section-title" id={anchorId}>{title}</span>
        <span className="kap-param-section-count">{count} Parameter</span>
      </button>
      {expanded && (
        <div className="kap-param-section-body">{children}</div>
      )}
    </section>
  )
}

interface GroupedProps {
  kommuneId: number
  parameters: ModelParameter[]
  catalog?: Catalog
  edits: Record<string, { value: string; source: string }>
  setEdits: Dispatch<SetStateAction<Record<string, { value: string; source: string }>>>
  saving: boolean
  error: string | null
  setError: (e: string | null) => void
  saveOne: (p: ModelParameter) => Promise<void>
  cancelEdit: (id: string) => void
  startEdit: (p: ModelParameter) => void
  showExport: boolean
  scrollAnchor?: string | null
  scrollTrigger?: number
}

function ParameterRows({
  params,
  edits,
  setEdits,
  saving,
  saveOne,
  cancelEdit,
  startEdit,
}: {
  params: ModelParameter[]
  edits: Record<string, { value: string; source: string }>
  setEdits: GroupedProps['setEdits']
  saving: boolean
  saveOne: GroupedProps['saveOne']
  cancelEdit: GroupedProps['cancelEdit']
  startEdit: GroupedProps['startEdit']
}) {
  return (
    <>
      {params.map(p => {
        const editing = edits[p.id]
        return (
          <tr key={p.id} className={p.overridden ? 'overridden' : ''}>
            <td><span className="kap-param-cell-text" title={p.label}>{p.label}</span></td>
            <td>
              {editing ? (
                <input
                  type="number"
                  step="any"
                  value={editing.value}
                  onChange={ev => setEdits({
                    ...edits,
                    [p.id]: { ...editing, value: ev.target.value },
                  })}
                  style={{ width: '100%', fontSize: '0.75rem' }}
                />
              ) : (
                <span>{String(p.value)}</span>
              )}
            </td>
            <td>{p.unit}</td>
            <td>
              {editing ? (
                <input
                  type="text"
                  placeholder="Quelle bei Änderung"
                  value={editing.source}
                  onChange={ev => setEdits({
                    ...edits,
                    [p.id]: { ...editing, source: ev.target.value },
                  })}
                  style={{ width: '100%', fontSize: '0.75rem' }}
                />
              ) : (
                <span className="kap-param-cell-text" title={p.custom_source || p.source || ''}>
                  {p.custom_source || p.source}
                </span>
              )}
            </td>
            <td>
              <span className={`kap-param-status ${p.overridden ? 'is-override' : ''}`}>
                {p.overridden ? 'Override' : 'Default'}
              </span>
            </td>
            <td style={{ whiteSpace: 'nowrap' }}>
              {editing ? (
                <>
                  <button
                    className="btn btn-primary"
                    style={{ fontSize: '0.7rem', padding: '2px 8px' }}
                    disabled={saving}
                    onClick={() => saveOne(p)}
                  >Speichern</button>
                  <button
                    className="btn btn-secondary"
                    style={{ fontSize: '0.7rem', padding: '2px 8px', marginLeft: 4 }}
                    onClick={() => cancelEdit(p.id)}
                  >Abbrechen</button>
                </>
              ) : p.editable ? (
                <button
                  className="btn btn-secondary"
                  style={{ fontSize: '0.7rem', padding: '2px 8px' }}
                  onClick={() => startEdit(p)}
                >Bearbeiten</button>
              ) : null}
            </td>
          </tr>
        )
      })}
    </>
  )
}

function GroupedParameterList({
  kommuneId,
  parameters,
  catalog,
  edits,
  setEdits,
  saving,
  error,
  saveOne,
  cancelEdit,
  startEdit,
  showExport,
  scrollAnchor,
  scrollTrigger,
}: GroupedProps) {
  const [expandedSections, setExpandedSections] = useState<Set<string>>(() => new Set())
  const indicatorUsage = buildIndicatorUsageIndex(catalog)

  const expandForAnchor = (anchorId: string) => {
    const key = mainSectionKeyFromAnchor(anchorId)
    if (!key) return
    setExpandedSections(prev => {
      if (prev.has(key)) return prev
      const next = new Set(prev)
      next.add(key)
      return next
    })
  }

  const toggleSection = (key: string) => {
    setExpandedSections(prev => {
      const next = new Set(prev)
      if (next.has(key)) next.delete(key)
      else next.add(key)
      return next
    })
  }

  useEffect(() => {
    if (!scrollAnchor || !scrollTrigger) return
    const id = scrollAnchor.replace(/^#/, '')
    expandForAnchor(id)
    const timer = window.setTimeout(() => {
      document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }, 120)
    return () => window.clearTimeout(timer)
  }, [scrollAnchor, scrollTrigger])

  const handleAnchorNavigate = (e: React.MouseEvent<HTMLDivElement>) => {
    const link = (e.target as HTMLElement).closest('a.kap-param-anchor-link') as HTMLAnchorElement | null
    if (!link) return
    const href = link.getAttribute('href')
    if (!href?.startsWith('#')) return
    e.preventDefault()
    const id = href.slice(1)
    expandForAnchor(id)
    window.setTimeout(() => {
      document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }, 80)
  }

  const byCategory = (cat: string) => parameters.filter(p => p.layer_category === cat)
  const byIndicator = (cat: string, code: string) =>
    parameters.filter(p => p.layer_category === cat && p.layer_code === code)

  const hazardCodes = [...new Set(parameters.filter(p => p.layer_category === 'hazards').map(p => p.layer_code))]
  const exposureCodes = [...new Set(parameters.filter(p => p.layer_category === 'exposures').map(p => p.layer_code))]
  const vulnCodes = [...new Set(parameters.filter(p => p.layer_category === 'vulnerabilities').map(p => p.layer_code))]
  const riskCodes = [...new Set(parameters.filter(p => p.layer_category === 'risks').map(p => p.layer_code))]
  const measureCodes = [...new Set(parameters.filter(p => p.layer_category === 'measures').map(p => p.layer_code))]

  const tableHead = (
    <thead>
      <tr>
        <th>Bezeichnung</th>
        <th>Wert</th>
        <th>Einheit</th>
        <th>Quelle</th>
        <th>Status</th>
        <th />
      </tr>
    </thead>
  )

  const widthLockTable = (
    <div className="kap-param-table-width-lock" aria-hidden="true">
      <table>
        {PARAM_TABLE_COLGROUP}
        {tableHead}
      </table>
    </div>
  )

  const renderTable = (rows: ModelParameter[]) => (
    <table>
      {PARAM_TABLE_COLGROUP}
      {tableHead}
      <tbody>
        <ParameterRows
          params={rows}
          edits={edits}
          setEdits={setEdits}
          saving={saving}
          saveOne={saveOne}
          cancelEdit={cancelEdit}
          startEdit={startEdit}
        />
      </tbody>
    </table>
  )

  const modelCount = byCategory('model').length
  const uhiCount = byCategory('uhi').length
  const hazardCount = parameters.filter(p => p.layer_category === 'hazards').length
  const exposureCount = parameters.filter(p => p.layer_category === 'exposures').length
  const vulnCount = parameters.filter(p => p.layer_category === 'vulnerabilities').length
  const riskCount = parameters.filter(p => p.layer_category === 'risks').length
  const measureCount = parameters.filter(p => p.layer_category === 'measures').length

  return (
    <div className="kap-param-table kap-param-table--grouped" onClick={handleAnchorNavigate}>
      {showExport && (
        <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 8 }}>
          <a
            className="btn btn-secondary"
            href={api.exportParametersUrl(kommuneId)}
            download
            style={{ fontSize: '0.75rem', padding: '4px 10px', textDecoration: 'none' }}
          >
            Parameter exportieren (xlsx)
          </a>
        </div>
      )}
      {error && <div className="kap-param-error">{error}</div>}
      {widthLockTable}

      {modelCount > 0 && (
        <CollapsibleParamSection
          sectionKey="model"
          title="Modellweite Annahmen"
          anchorId={paramSectionId('model')}
          count={modelCount}
          expanded={expandedSections.has('model')}
          onToggle={toggleSection}
        >
          {renderTable(byCategory('model'))}
        </CollapsibleParamSection>
      )}

      {uhiCount > 0 && (
        <CollapsibleParamSection
          sectionKey="uhi"
          title="UHI-Modell"
          anchorId={paramSectionId('uhi')}
          count={uhiCount}
          expanded={expandedSections.has('uhi')}
          onToggle={toggleSection}
        >
          {renderTable(byCategory('uhi'))}
        </CollapsibleParamSection>
      )}

      {hazardCodes.length > 0 && (
        <CollapsibleParamSection
          sectionKey="hazards"
          title="Klimatische Einflüsse"
          anchorId={paramSectionId('hazards')}
          count={hazardCount}
          expanded={expandedSections.has('hazards')}
          onToggle={toggleSection}
        >
          {hazardCodes.map(code => (
            <div key={code} className="kap-param-subsection">
              <h4 id={paramSectionId('hazards', code)}>{indicatorName(catalog, 'hazards', code)}</h4>
              {renderTable(byIndicator('hazards', code))}
              <ParamCrossRefHint
                intro="Verwendet als Eingang für:"
                links={indicatorUsage[`hazards:${code}`] ?? []}
              />
            </div>
          ))}
        </CollapsibleParamSection>
      )}

      {exposureCodes.length > 0 && (
        <CollapsibleParamSection
          sectionKey="exposures"
          title="Räumliche Expositionen"
          anchorId={paramSectionId('exposures')}
          count={exposureCount}
          expanded={expandedSections.has('exposures')}
          onToggle={toggleSection}
        >
          {exposureCodes.map(code => (
            <div key={code} className="kap-param-subsection">
              <h4 id={paramSectionId('exposures', code)}>{indicatorName(catalog, 'exposures', code)}</h4>
              {renderTable(byIndicator('exposures', code))}
              <ParamCrossRefHint
                intro="Verwendet als Eingang für:"
                links={indicatorUsage[`exposures:${code}`] ?? []}
              />
            </div>
          ))}
        </CollapsibleParamSection>
      )}

      {vulnCodes.length > 0 && (
        <CollapsibleParamSection
          sectionKey="vulnerabilities"
          title="Sensitivitäten"
          anchorId={paramSectionId('vulnerabilities')}
          count={vulnCount}
          expanded={expandedSections.has('vulnerabilities')}
          onToggle={toggleSection}
        >
          {vulnCodes.map(code => (
            <div key={code} className="kap-param-subsection">
              <h4 id={paramSectionId('vulnerabilities', code)}>{indicatorName(catalog, 'vulnerabilities', code)}</h4>
              {renderTable(byIndicator('vulnerabilities', code))}
              <ParamCrossRefHint
                intro="Verwendet als Eingang für:"
                links={indicatorUsage[`vulnerabilities:${code}`] ?? []}
              />
            </div>
          ))}
        </CollapsibleParamSection>
      )}

      {riskCodes.length > 0 && (
        <CollapsibleParamSection
          sectionKey="risks"
          title="Klimarisiken"
          anchorId={paramSectionId('risks')}
          count={riskCount}
          expanded={expandedSections.has('risks')}
          onToggle={toggleSection}
        >
          {riskCodes.map(code => {
            const risk = catalog?.risks.find(r => r.code === code)
            const links = risk ? riskInputLinks(risk, catalog) : []
            return (
              <div key={code} className="kap-param-subsection">
                <h4 id={paramSectionId('risks', code)}>{indicatorName(catalog, 'risks', code)}</h4>
                {renderTable(byIndicator('risks', code))}
                <ParamCrossRefHint
                  intro="Eingangsgrößen für dieses Risiko werden in den Input-Ebenen modelliert:"
                  links={links}
                />
              </div>
            )
          })}
        </CollapsibleParamSection>
      )}

      {measureCodes.length > 0 && (
        <CollapsibleParamSection
          sectionKey="measures"
          title="Maßnahmen"
          anchorId={paramSectionId('measures')}
          count={measureCount}
          expanded={expandedSections.has('measures')}
          onToggle={toggleSection}
        >
          {measureCodes.map(code => {
            const measure = catalog?.measures.find(m => m.code === code)
            const links = measure ? measureOutputLinks(measure, catalog) : []
            return (
              <div key={code} className="kap-param-subsection">
                <h4 id={paramSectionId('measures', code)}>{indicatorName(catalog, 'measures', code)}</h4>
                {renderTable(byIndicator('measures', code))}
                <ParamCrossRefHint
                  intro="Wirkt auf folgende Klimarisiken:"
                  links={links}
                />
              </div>
            )
          })}
        </CollapsibleParamSection>
      )}
    </div>
  )
}
