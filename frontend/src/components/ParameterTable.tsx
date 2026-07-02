import { useState, type Dispatch, type SetStateAction } from 'react'
import { api } from '../api/client'
import type { Catalog, CatalogRisk, ModelParameter } from '../types'

interface Props {
  kommuneId: number
  parameters: ModelParameter[]
  onUpdated: () => void
  compact?: boolean
  showExport?: boolean
  grouped?: boolean
  catalog?: Catalog
}

export default function ParameterTable({
  kommuneId, parameters, onUpdated, compact, showExport = true, grouped, catalog,
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
    return <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Keine Parameter für diese Ebene.</p>
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
                <td>{p.label}</td>
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
                      style={{ width: 90, fontSize: '0.75rem' }}
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
                      style={{ width: '100%', minWidth: 140, fontSize: '0.75rem' }}
                    />
                  ) : (
                    <span title={p.custom_source || ''}>
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

function indicatorName(
  catalog: Catalog | undefined,
  category: string,
  code: string,
): string {
  if (!catalog || !code) return code
  const list = category === 'hazards' ? catalog.hazards
    : category === 'exposures' ? catalog.exposures
      : category === 'vulnerabilities' ? catalog.vulnerabilities
        : category === 'risks' ? catalog.risks
          : category === 'measures' ? catalog.measures
            : []
  const item = list.find((x: { code: string }) => x.code === code)
  return item?.name ?? code
}

function riskInputLinks(risk: CatalogRisk, catalog: Catalog | undefined): { href: string; label: string }[] {
  if (!catalog) return []
  const links: { href: string; label: string }[] = []
  for (const code of risk.hazards) {
    links.push({
      href: `#param-hazards-${code}`,
      label: indicatorName(catalog, 'hazards', code),
    })
  }
  for (const code of risk.exposures) {
    links.push({
      href: `#param-exposures-${code}`,
      label: indicatorName(catalog, 'exposures', code),
    })
  }
  for (const code of risk.vulnerabilities) {
    links.push({
      href: `#param-vulnerabilities-${code}`,
      label: indicatorName(catalog, 'vulnerabilities', code),
    })
  }
  return links
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
            <td>{p.label}</td>
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
                  style={{ width: 90, fontSize: '0.75rem' }}
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
                  style={{ width: '100%', minWidth: 140, fontSize: '0.75rem' }}
                />
              ) : (
                <span title={p.custom_source || ''}>
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
}: GroupedProps) {
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

  const renderTable = (rows: ModelParameter[]) => (
    <table>
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

  return (
    <div className="kap-param-table kap-param-table--grouped">
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

      {byCategory('model').length > 0 && (
        <section className="kap-param-section">
          <h3 id="param-model">Modellweite Annahmen</h3>
          {renderTable(byCategory('model'))}
        </section>
      )}

      {byCategory('uhi').length > 0 && (
        <section className="kap-param-section">
          <h3 id="param-uhi">UHI-Modell</h3>
          {renderTable(byCategory('uhi'))}
        </section>
      )}

      {hazardCodes.length > 0 && (
        <section className="kap-param-section">
          <h3 id="param-hazards">Klimatische Einflüsse</h3>
          {hazardCodes.map(code => (
            <div key={code} className="kap-param-subsection">
              <h4 id={`param-hazards-${code}`}>{indicatorName(catalog, 'hazards', code)}</h4>
              {renderTable(byIndicator('hazards', code))}
            </div>
          ))}
        </section>
      )}

      {exposureCodes.length > 0 && (
        <section className="kap-param-section">
          <h3 id="param-exposures">Räumliche Expositionen</h3>
          {exposureCodes.map(code => (
            <div key={code} className="kap-param-subsection">
              <h4 id={`param-exposures-${code}`}>{indicatorName(catalog, 'exposures', code)}</h4>
              {renderTable(byIndicator('exposures', code))}
            </div>
          ))}
        </section>
      )}

      {vulnCodes.length > 0 && (
        <section className="kap-param-section">
          <h3 id="param-vulnerabilities">Sensitivitäten</h3>
          {vulnCodes.map(code => (
            <div key={code} className="kap-param-subsection">
              <h4 id={`param-vulnerabilities-${code}`}>{indicatorName(catalog, 'vulnerabilities', code)}</h4>
              {renderTable(byIndicator('vulnerabilities', code))}
            </div>
          ))}
        </section>
      )}

      {riskCodes.length > 0 && (
        <section className="kap-param-section">
          <h3 id="param-risks">Klimarisiken</h3>
          {riskCodes.map(code => {
            const risk = catalog?.risks.find(r => r.code === code)
            const links = risk ? riskInputLinks(risk, catalog) : []
            return (
              <div key={code} className="kap-param-subsection">
                <h4 id={`param-risks-${code}`}>{indicatorName(catalog, 'risks', code)}</h4>
                {renderTable(byIndicator('risks', code))}
                {links.length > 0 && (
                  <p className="kap-param-risk-hint">
                    <em>Eingangsgrößen für dieses Risiko werden in den Input-Ebenen modelliert:</em>{' '}
                    {links.map((link, i) => (
                      <span key={link.href}>
                        {i > 0 ? ' · ' : ''}
                        <a href={link.href}>{link.label}</a>
                      </span>
                    ))}
                  </p>
                )}
              </div>
            )
          })}
        </section>
      )}

      {measureCodes.length > 0 && (
        <section className="kap-param-section">
          <h3 id="param-measures">Maßnahmen</h3>
          {measureCodes.map(code => (
            <div key={code} className="kap-param-subsection">
              <h4 id={`param-measures-${code}`}>{indicatorName(catalog, 'measures', code)}</h4>
              {renderTable(byIndicator('measures', code))}
            </div>
          ))}
        </section>
      )}
    </div>
  )
}
