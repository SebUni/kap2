import { useStore } from '../../store'
import ChartSkeleton from './ChartSkeleton'
import type { ClimateMetric } from '../../types'
import { fmtEurCompact, fmtNum } from '../../utils/format'

/** Kurzbezeichner je Klimametrik für die Chip-Zeile. */
const CHIP_LABELS: Record<string, string> = {
  mean_temp_annual: 'Ø-Temp',
  precipitation_mm: 'Niederschlag',
  hot_days: 'Hitzetage',
  summer_days: 'Sommertage',
  frost_days: 'Frosttage',
  tropical_nights: 'Tropennächte',
  snow_days: 'Schneetage',
  precip_ge20_days: 'Starkregentage',
}

const CHIP_UNITS: Record<string, string> = {
  mean_temp_annual: '°C',
  precipitation_mm: 'mm',
}

function chipValue(m: ClimateMetric): string {
  if (m.value === null) return '–'
  const unit = CHIP_UNITS[m.code] ?? ''
  const digits = m.code === 'mean_temp_annual' ? 1 : 0
  return `${fmtNum(m.value, digits)}${unit ? ` ${unit}` : ''}`
}

function ClimateChip({ m }: { m: ClimateMetric }) {
  const de = m.germany
  const basis = m.data_basis === 'dwd_cdc_raster'
    ? 'DWD-CDC-Raster am Gemeindezentroid (Mittel der letzten verfügbaren Jahre)'
    : m.data_basis === 'regional_fallback'
      ? 'DWD-Gebietsmittel des Bundeslands'
      : 'Derzeit keine Datenbasis verfügbar'
  const title = [
    m.label,
    `Kommune: ${m.value !== null ? `${fmtNum(m.value)} ${m.unit}` : 'n. v.'} — ${basis}`,
    de ? `Deutschland: ${fmtNum(de.value)} ${m.unit}${de.period ? ` (${de.period})` : ''}` : null,
    m.references[0]?.ieee ? `Quelle DE-Referenz: ${m.references[0].ieee}` : null,
  ].filter(Boolean).join('\n')

  return (
    <span className="climate-chip" title={title}>
      <span className="chip-label">{CHIP_LABELS[m.code] ?? m.label}</span>
      <span className="chip-value">{chipValue(m)}</span>
      {de && <span className="chip-de">DE {fmtNum(de.value, m.code === 'mean_temp_annual' ? 1 : 0)}</span>}
      {m.delta !== null && m.delta !== 0 && (
        <span className={m.delta > 0 ? 'chip-delta-up' : 'chip-delta-down'}>
          {m.delta > 0 ? '▲' : '▼'}{fmtNum(Math.abs(m.delta))}
        </span>
      )}
    </span>
  )
}

/**
 * Hero-Kopf des Dashboards: Kommunenname, Meta-Zeile (Bundesland · Landkreis ·
 * Höhe · Einwohner · Fläche · BIP Kreisebene · Kommunalhaushalt Ø — die beiden
 * Wirtschafts-/Finanz-Kennzahlen aus der Regionalstatistik mit Quellen-Tooltip),
 * drei Euro-Kernzahlen (heute / 2065 ohne Maßnahmen / 2065 mit Maßnahmen inkl.
 * Maßnahmenkosten) sowie die Klima-Chips mit Deutschland-Vergleich.
 */
export default function KommuneHeader({ className = '' }: { className?: string }) {
  const { kommune, kommuneProfile, riskSummary, costProjection } = useStore()
  if (!kommune) return null

  const p = kommuneProfile
  const proj = costProjection
  const lastIdx = proj ? proj.years.length - 1 : 0
  const scen = proj?.scenarios.rcp45

  const metaParts: string[] = []
  if (p?.bundesland) metaParts.push(p.bundesland)
  // Nominatim liefert je nach Zoom mal „Landkreis Nordsachsen", mal nur
  // „Nordsachsen" — ohne Bezeichner Präfix ergänzen, damit der Eintrag nicht
  // wie ein zweites Bundesland liest. Eigenbezeichner (Kreis/Region/Stadt,
  // z. B. „Städteregion Aachen") bleiben unangetastet.
  if (p?.landkreis) {
    metaParts.push(/kreis|region|stadt/i.test(p.landkreis)
      ? p.landkreis : `Landkreis ${p.landkreis}`)
  }
  if (p?.elevation) metaParts.push(`${fmtNum(p.elevation.mean_m, 0)} m ü. NN (${fmtNum(p.elevation.min_m, 0)}–${fmtNum(p.elevation.max_m, 0)} m)`)
  if (p?.population) metaParts.push(`${p.population.toLocaleString('de-DE')} Einwohner`)
  if (p?.area_km2) metaParts.push(`${fmtNum(p.area_km2)} km²`)

  // Wirtschafts-/Finanz-Kennzahlen (Regionalstatistik) als eigene Meta-Einträge
  // mit Quellen-Tooltip — direkt in der „·"-Zeile neben den Strukturdaten.
  const econParts: { text: string; title: string }[] = []
  if (p?.economy) {
    const e = p.economy
    const kreisLine = `Kreis-BIP${e.gdp_year ? ` (${e.gdp_year})` : ''}: ${fmtEurCompact(e.gdp_meur * 1e6)}`
    if (e.estimated_municipal_eur != null) {
      econParts.push({
        text: `BIP ≈ ${fmtEurCompact(e.estimated_municipal_eur)}`,
        title: [
          'Geschätztes BIP der Kommune: BIP je Einwohner des Kreises'
          + (e.gdp_per_capita_eur ? ` (${fmtNum(e.gdp_per_capita_eur, 0)} €)` : '')
          + (p.population ? ` × ${p.population.toLocaleString('de-DE')} Einwohner` : '')
          + '. Amtlich wird das BIP nur auf Kreisebene ausgewiesen.',
          kreisLine,
          `Quelle: ${e.source}`,
          e.references[0]?.ieee ?? null,
        ].filter(Boolean).join('\n'),
      })
    } else {
      econParts.push({
        text: `BIP ${fmtEurCompact(e.gdp_meur * 1e6)} (Kreis)`,
        title: [
          'Bruttoinlandsprodukt in jeweiligen Preisen — amtlich nur auf '
          + 'Kreisebene verfügbar (kein Gemeindewert).',
          e.gdp_year ? `Jahr: ${e.gdp_year}` : null,
          `Quelle: ${e.source}`,
          e.references[0]?.ieee ?? null,
        ].filter(Boolean).join('\n'),
      })
    }
  }
  if (p?.municipal_budget) {
    const yrs = p.municipal_budget.years
    econParts.push({
      text: `Haushalt ${fmtEurCompact(p.municipal_budget.avg_expenditure_eur)}/a`,
      title: [
        'Auszahlungen insgesamt (bereinigt) der kommunalen Kernhaushalte '
        + `(Gemeindeebene), Ø der Jahre ${yrs[0]}–${yrs[yrs.length - 1]}.`,
        `Quelle: ${p.municipal_budget.source}`,
        p.municipal_budget.references[0]?.ieee ?? null,
      ].filter(Boolean).join('\n'),
    })
  }

  return (
    <section className={`dashboard-section kommune-hero ${className}`}>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: 12, flexWrap: 'wrap' }}>
        <h1 className="hero-name">{kommune.name}</h1>
        <div className="hero-meta" title={p?.population_source ?? undefined}>
          {metaParts.length || econParts.length
            ? (<>
                {metaParts.join(' · ')}
                {econParts.map((e, i) => (
                  <span key={i} className="hero-meta-econ" title={e.title}>
                    {(metaParts.length || i > 0) ? ' · ' : ''}{e.text}
                  </span>
                ))}
              </>)
            : p ? '' : 'Profil wird geladen …'}
        </div>
      </div>

      <div className="hero-kpis">
        <div className="hero-kpi">
          <div className="hero-kpi-label">Erwartete Schäden heute</div>
          <div className="hero-kpi-value">
            {riskSummary ? `${fmtEurCompact(riskSummary.cost.total_eur)}/a` : '…'}
          </div>
          <div className="hero-kpi-sub">Summe aller monetarisierten Klimarisiken</div>
        </div>
        <div className="hero-kpi">
          <div className="hero-kpi-label">{proj ? proj.years[lastIdx] : 2065} ohne Maßnahmen</div>
          <div className="hero-kpi-value" style={{ color: 'var(--danger)' }}>
            {scen ? `${fmtEurCompact(scen.no_measures.annual[lastIdx])}/a` : '…'}
          </div>
          <div className="hero-kpi-sub">Projektion, Szenario RCP 4.5</div>
        </div>
        <div className="hero-kpi">
          <div className="hero-kpi-label">{proj ? proj.years[lastIdx] : 2065} mit Maßnahmen</div>
          <div className="hero-kpi-value" style={{ color: 'var(--primary)' }}>
            {scen
              ? proj?.has_measures
                ? `${fmtEurCompact(scen.with_measures.annual[lastIdx])}/a`
                : '–'
              : '…'}
          </div>
          <div className="hero-kpi-sub">
            {proj && !proj.has_measures
              ? 'Noch keine Maßnahmen erfasst'
              : 'inkl. Maßnahmenkosten (CAPEX/OPEX)'}
          </div>
        </div>
      </div>

      {p ? (
        <div className="climate-chips">
          {p.climate
            .filter(m => m.value !== null || m.germany !== null)
            .map(m => <ClimateChip key={m.code} m={m} />)}
        </div>
      ) : (
        <div style={{ marginTop: '0.75rem' }}>
          <ChartSkeleton height={34} label="Klimadaten & Deutschland-Vergleich werden geladen …" />
        </div>
      )}
    </section>
  )
}
