import { useState } from 'react'
import { useStore } from '../store'
import InfoTooltip from './InfoTooltip'
import type {
  CatalogIndicator, CatalogRisk, CatalogMeasure, CategoryDef, LayerCategory,
} from '../types'

const GROUP_DEFS: { key: 'measures' | LayerCategory; label: string }[] = [
  { key: 'measures', label: 'Maßnahmen' },
  { key: 'risks', label: 'Klimarisiken' },
  { key: 'hazards', label: 'Klimatreiber' },
  { key: 'exposures', label: 'Expositionen' },
  { key: 'vulnerabilities', label: 'Verwundbarkeiten' },
  { key: 'auxiliary', label: 'Sonstige' },
]

export default function LayerPanel() {
  const {
    catalog, activeLayer, setActiveLayer,
    showMeasures, setShowMeasures, measures,
    selectedMeasure, setSelectedMeasure,
  } = useStore()
  // Gruppen-Kollaps (oberste Ebene)
  const [collapsedGroups, setCollapsedGroups] = useState<Record<string, boolean>>({
    exposures: true, vulnerabilities: true, auxiliary: true,
  })
  // Kategorie-Kollaps (Zwischenebene), Default: eingeklappt
  const [collapsedCats, setCollapsedCats] = useState<Record<string, boolean>>({})

  if (!catalog) {
    return <div className="layer-panel" style={{ padding: '0.75rem', fontSize: '0.8rem', color: 'var(--text-muted)' }}>Lade Katalog…</div>
  }

  const groupCollapsed = (key: string) => collapsedGroups[key] ?? false
  const toggleGroup = (key: string) =>
    setCollapsedGroups(c => ({ ...c, [key]: !(c[key] ?? false) }))
  const catCollapsed = (key: string) => collapsedCats[key] ?? true
  const toggleCat = (key: string) =>
    setCollapsedCats(c => ({ ...c, [key]: !(c[key] ?? true) }))

  const indicatorRows = (it: CatalogIndicator) => ([
    { label: 'Einheit', value: it.unit },
    { label: 'Proxy', value: it.proxy },
    { label: 'Quelle', value: it.source },
    { label: 'Normierung', value: `${it.norm_min} … ${it.norm_max} ${it.unit}` },
  ])

  const riskRows = (r: CatalogRisk) => ([
    { label: 'Ergebnis', value: r.outcome_unit },
    { label: 'Treiber', value: r.hazards.join(', ') },
    { label: 'Exposition', value: r.exposures.join(', ') },
    { label: 'Verwundbark.', value: r.vulnerabilities.join(', ') },
  ])

  const renderItem = (
    code: string, name: string, category: LayerCategory,
    info: React.ReactNode, spatial?: boolean,
  ) => {
    const active = activeLayer?.code === code
    return (
      <div
        key={code}
        className={`layer-item ${active ? 'active' : ''}`}
        onClick={() => setActiveLayer(active ? null : { category, code })}
        style={{
          display: 'flex', alignItems: 'center', gap: 6, padding: '4px 8px 4px 18px',
          cursor: 'pointer', fontSize: '0.78rem', borderRadius: 6,
          fontWeight: active ? 600 : 400,
        }}
      >
        <input
          type="checkbox"
          checked={active}
          readOnly
          tabIndex={-1}
          style={{ flexShrink: 0, pointerEvents: 'none', margin: 0 }}
        />
        <span style={{ flex: 1, opacity: spatial === false ? 0.7 : 1 }}>{name}</span>
        <span onClick={e => e.stopPropagation()}>{info}</span>
      </div>
    )
  }

  // Eine einklappbare Kategorie-Zwischenebene rendern
  const renderCategory = (
    groupKey: string, catCode: string, catLabel: string,
    count: number, children: React.ReactNode,
  ) => {
    if (count === 0) return null
    const key = `${groupKey}:${catCode}`
    const collapsed = catCollapsed(key)
    return (
      <div key={key}>
        <div
          onClick={() => toggleCat(key)}
          style={{
            display: 'flex', alignItems: 'center', gap: 6, padding: '4px 8px',
            cursor: 'pointer', fontSize: '0.72rem', fontWeight: 600,
            color: 'var(--text)',
          }}
        >
          <span style={{ fontSize: '0.6rem', transform: collapsed ? 'rotate(-90deg)' : 'none', transition: 'transform 0.15s', color: 'var(--text-muted)' }}>▾</span>
          <span style={{ flex: 1 }}>{catLabel}</span>
          <span style={{ fontSize: '0.68rem', color: 'var(--text-muted)' }}>{count}</span>
        </div>
        {!collapsed && <div>{children}</div>}
      </div>
    )
  }

  // Indikator-Gruppe (H/E/V) nach category aufteilen
  const renderIndicatorGroup = (
    groupKey: LayerCategory, items: CatalogIndicator[], cats: CategoryDef[],
  ) => cats.map(cat => {
    const inCat = items.filter(it => (it.category ?? cats[0]?.code) === cat.code)
    return renderCategory(groupKey, cat.code, cat.label, inCat.length, (
      inCat.map(it => renderItem(it.code, it.name, groupKey,
        <InfoTooltip title={it.name} description={it.description} rows={indicatorRows(it)}
          note={it.spatial === false ? 'Nicht räumlich aufgelöst (Konstantwert)' : undefined} />,
        it.spatial))
    ))
  })

  // Maßnahmen: erstellte Maßnahmen nach KAnG-Cluster gruppieren
  const measureCatByCode: Record<string, CatalogMeasure> = {}
  catalog.measures.forEach(m => { measureCatByCode[m.code] = m })
  const fieldLabel = (clusterCode: string, fieldCode: string) =>
    catalog.kang_clusters.find(c => c.code === clusterCode)?.fields
      .find(f => f.code === fieldCode)?.label ?? ''

  return (
    <div className="layer-panel" style={{
      width: 280, flexShrink: 0, borderRight: '1px solid var(--border)',
      background: 'var(--surface)', overflowY: 'auto', height: '100%',
    }}>
      <div style={{ padding: '0.6rem 0.8rem', borderBottom: '1px solid var(--border)', fontWeight: 600, fontSize: '0.9rem' }}>
        Ebenen
      </div>

      {GROUP_DEFS.map(group => {
        const isCollapsed = groupCollapsed(group.key)
        return (
          <div key={group.key} style={{ borderBottom: '1px solid var(--border)' }}>
            <div
              onClick={() => toggleGroup(group.key)}
              style={{
                display: 'flex', alignItems: 'center', gap: 6, padding: '6px 8px',
                cursor: 'pointer', fontWeight: 600, fontSize: '0.8rem',
                color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.03em',
              }}
            >
              <span style={{ transform: isCollapsed ? 'rotate(-90deg)' : 'none', transition: 'transform 0.15s' }}>▾</span>
              {group.label}
            </div>

            {!isCollapsed && (
              <div style={{ padding: '0 4px 6px' }}>
                {group.key === 'measures' && (
                  <>
                    <label style={{ display: 'flex', alignItems: 'center', gap: 6, padding: '4px 8px', fontSize: '0.78rem', cursor: 'pointer' }}>
                      <input type="checkbox" checked={showMeasures} onChange={e => setShowMeasures(e.target.checked)} />
                      <span style={{ flex: 1 }}>Auf Karte anzeigen ({measures.length})</span>
                    </label>
                    {catalog.kang_clusters.map(cluster => {
                      const inCluster = measures.filter(m =>
                        measureCatByCode[m.measure_type]?.kang_cluster === cluster.code)
                      return renderCategory('measures', cluster.code, cluster.label, inCluster.length, (
                        inCluster.map(m => {
                          const cat = measureCatByCode[m.measure_type]
                          const active = selectedMeasure?.id === m.id
                          return (
                            <div
                              key={m.id}
                              onClick={() => setSelectedMeasure(active ? null : m)}
                              style={{
                                display: 'flex', flexDirection: 'column', padding: '4px 8px 4px 18px',
                                cursor: 'pointer', fontSize: '0.78rem', borderRadius: 6,
                                background: active ? 'var(--primary)' : 'transparent',
                                color: active ? '#fff' : 'var(--text)',
                              }}
                            >
                              <span>{m.name}</span>
                              <span style={{ fontSize: '0.66rem', opacity: 0.7 }}>
                                {fieldLabel(cluster.code, cat?.kang_field ?? '')}
                              </span>
                            </div>
                          )
                        })
                      ))
                    })}
                  </>
                )}

                {group.key === 'risks' && catalog.groups.map(g => {
                  const inGroup = catalog.risks.filter(r => r.group === g.code)
                  return renderCategory('risks', g.code, g.label, inGroup.length, (
                    inGroup.map(r => renderItem(r.code, r.name, 'risks',
                      <InfoTooltip title={r.name} description={r.description} rows={riskRows(r)} />))
                  ))
                })}

                {group.key === 'hazards' &&
                  renderIndicatorGroup('hazards', catalog.hazards, catalog.hazard_categories)}
                {group.key === 'exposures' &&
                  renderIndicatorGroup('exposures', catalog.exposures, catalog.exposure_categories)}
                {group.key === 'vulnerabilities' &&
                  renderIndicatorGroup('vulnerabilities', catalog.vulnerabilities, catalog.vulnerability_categories)}
                {group.key === 'auxiliary' &&
                  renderIndicatorGroup('auxiliary', catalog.auxiliary, catalog.auxiliary_categories)}
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}
