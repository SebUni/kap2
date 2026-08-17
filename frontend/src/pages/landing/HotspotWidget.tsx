import { useCallback, useMemo, useState } from 'react'
import type { LayerMeta } from '../../types'
import LandingMap from './LandingMap'
import { LANDING_BOUNDS, LANDING_CELLS, RISK_LAYERS } from './landingData'
import { buildRiskTooltipHtml } from './landingTooltip'
import ToolExcerptBadge from './ToolExcerptBadge'

/**
 * Widget B — „Wo müssen wir zuerst handeln — und wen schützen?"
 * Echte OSM-Karte mit dem echten Oschatz-100 m-Raster als Choropleth (Outcome
 * je Risiko), Risiko-Auswahl als Radio-Menü, Tool-Legende und dem ausführlichen
 * Inspektor beim Hover über eine Zelle. Werte + Rechenweg aus dem Backend-Cache.
 */
export default function HotspotWidget() {
  const [idx, setIdx] = useState(0)
  const layer = RISK_LAYERS[idx]

  const meta = useMemo<LayerMeta>(() => ({
    code: layer.code, category: 'risks', label: layer.label, unit: layer.unit,
    min: layer.min, max: layer.max, recipe: layer.recipe,
  }), [layer])

  const valueForId = useCallback((id: number) => layer.cells[id]?.value ?? null, [layer])
  const tooltipForId = useCallback((id: number) => {
    const c = layer.cells[id]
    if (!c) return null
    return buildRiskTooltipHtml(meta, c, c.value)
  }, [layer, meta])

  return (
    <div className="landing-widget hotspot-widget">
      <ToolExcerptBadge />
      <fieldset className="risk-radio">
        <legend>Klimarisiken (Auszug)</legend>
        {RISK_LAYERS.map((r, i) => (
          <label className="risk-radio-row" key={r.key}>
            <input type="radio" name="landing-risk" checked={idx === i} onChange={() => setIdx(i)} />
            <span className="risk-radio-label">{r.label}</span>
            <span className="risk-info" tabIndex={0} aria-label={`Info zu ${r.label}`}>
              ⓘ<span className="risk-info-pop" role="tooltip">{r.hint}</span>
            </span>
          </label>
        ))}
      </fieldset>
      <LandingMap
        cells={LANDING_CELLS}
        bounds={LANDING_BOUNDS}
        valueForId={valueForId}
        tooltipForId={tooltipForId}
        legend={{ label: layer.label, unit: layer.unit }}
        ariaLabel={`OSM-Karte von Oschatz, eingefärbt nach ${layer.label}`}
      />
      <p className="widget-caption widget-caption-hint">
        Fahren Sie mit der Maus über eine Rasterzelle — der Inspektor zeigt den vollständigen Rechenweg.
      </p>
    </div>
  )
}
