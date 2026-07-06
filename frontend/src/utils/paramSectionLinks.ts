import type { Catalog, CatalogMeasure, CatalogRisk } from '../types'

export function paramSectionId(category: string, code?: string): string {
  if (!code || category === 'model' || category === 'uhi'
      || category === 'impact' || category === 'regional') {
    return `param-${category}`
  }
  return `param-${category}-${code}`
}

export function configScrollAnchorForLayer(category: string, code: string): string {
  return paramSectionId(category, code)
}

export function mainSectionKeyFromAnchor(anchorId: string): string | null {
  const id = anchorId.replace(/^#/, '')
  if (id === paramSectionId('model')) return 'model'
  if (id === paramSectionId('uhi')) return 'uhi'
  if (id === paramSectionId('impact')) return 'impact'
  if (id === paramSectionId('regional')) return 'regional'
  if (id.startsWith('param-hazards')) return 'hazards'
  if (id.startsWith('param-exposures')) return 'exposures'
  if (id.startsWith('param-vulnerabilities')) return 'vulnerabilities'
  if (id.startsWith('param-risks')) return 'risks'
  if (id.startsWith('param-measures')) return 'measures'
  return null
}

export function indicatorName(
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
  const item = list.find(x => x.code === code)
  return item?.name ?? code
}

export interface ParamSectionLink {
  href: string
  label: string
}

export function riskInputLinks(risk: CatalogRisk, catalog: Catalog | undefined): ParamSectionLink[] {
  if (!catalog) return []
  const links: ParamSectionLink[] = []
  for (const code of risk.hazards) {
    links.push({
      href: `#${paramSectionId('hazards', code)}`,
      label: indicatorName(catalog, 'hazards', code),
    })
  }
  for (const code of risk.exposures) {
    links.push({
      href: `#${paramSectionId('exposures', code)}`,
      label: indicatorName(catalog, 'exposures', code),
    })
  }
  for (const code of risk.vulnerabilities) {
    links.push({
      href: `#${paramSectionId('vulnerabilities', code)}`,
      label: indicatorName(catalog, 'vulnerabilities', code),
    })
  }
  return links
}

export function measureOutputLinks(measure: CatalogMeasure, catalog: Catalog | undefined): ParamSectionLink[] {
  if (!catalog) return []
  return measure.linked_risk_codes.map(code => ({
    href: `#${paramSectionId('risks', code)}`,
    label: indicatorName(catalog, 'risks', code),
  }))
}

export type IndicatorUsageMap = Record<string, ParamSectionLink[]>

export function buildIndicatorUsageIndex(catalog: Catalog | undefined): IndicatorUsageMap {
  const usage: IndicatorUsageMap = {}
  if (!catalog) return usage

  const add = (inputCategory: string, inputCode: string, risk: CatalogRisk) => {
    const key = `${inputCategory}:${inputCode}`
    if (!usage[key]) usage[key] = []
    if (usage[key].some(l => l.href === `#${paramSectionId('risks', risk.code)}`)) return
    usage[key].push({
      href: `#${paramSectionId('risks', risk.code)}`,
      label: indicatorName(catalog, 'risks', risk.code),
    })
  }

  for (const risk of catalog.risks) {
    for (const code of risk.hazards) add('hazards', code, risk)
    for (const code of risk.exposures) add('exposures', code, risk)
    for (const code of risk.vulnerabilities) add('vulnerabilities', code, risk)
  }
  return usage
}
