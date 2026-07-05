import { useEffect, useRef, useState, useMemo } from 'react'
import maplibregl from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
import { useStore } from '../store'
import type {
  CellOutcomeBreakdown, CellPathwayBreakdown, HevRecipeMeta, IndicatorRecipe,
  LayerMeta, LayerRecipe, OutcomeFactorMeta, ResolvedInput, RiskRecipe,
} from '../types'

const CHOROPLETH_COLORS = ['#fef9c3', '#fde047', '#fb923c', '#ef4444', '#991b1b']
/** Höherer Wert = bessere Erreichbarkeit → grün statt rot. */
const CHOROPLETH_GOOD_HIGH = new Set([
  'HEALTHCARE_ACCESS_GRID', 'HEALTHCARE_ACCESS_SCORE',
  'HEALTHCARE_INDEX_HOSPITAL', 'HEALTHCARE_INDEX_DOCTOR', 'HEALTHCARE_INDEX_PHARMACY',
])

function choroplethColors(code?: string) {
  return CHOROPLETH_GOOD_HIGH.has(code ?? '') ? [...CHOROPLETH_COLORS].reverse() : CHOROPLETH_COLORS
}
type TooltipMode = 'off' | 'short' | 'detail'
const TOOLTIP_MODE_KEY = 'map-tooltip-mode'

function isRiskRecipe(r: LayerRecipe): r is RiskRecipe {
  return 'formula_index' in r
}

function fmtNum(v: number) {
  return v.toLocaleString('de-DE', { maximumFractionDigits: 3 })
}

/** Skalenende für absolute Werte: Min/Max der aktuell gezeigten Zellen. */
function layerScaleBounds(meta?: LayerMeta): { lo: number; hi: number } {
  const lo = meta?.min ?? 0
  const hi = meta?.max != null && meta.max > lo ? meta.max : lo + 1
  return { lo, hi }
}

function provBadge(prov?: string) {
  const map: Record<string, { bg: string; text: string; label: string }> = {
    extern: { bg: '#dbeafe', text: '#1d4ed8', label: 'extern' },
    param: { bg: '#fef3c7', text: '#b45309', label: 'Parameter' },
    computed: { bg: '#ede9fe', text: '#6d28d9', label: 'berechnet' },
  }
  const s = map[prov || ''] || map.extern
  return ` <span style="font-size:8px;background:${s.bg};color:${s.text};padding:0 3px;border-radius:2px;margin-left:3px">${s.label}</span>`
}

function parseProp<T>(raw: unknown): T | undefined {
  if (raw == null) return undefined
  if (typeof raw === 'string') {
    try { return JSON.parse(raw) as T } catch { return undefined }
  }
  return raw as T
}

const TOOLTIP_MODE_CYCLE: TooltipMode[] = ['off', 'short', 'detail']
const TOOLTIP_MODE_LABEL: Record<TooltipMode, string> = {
  off: 'Inspektor: Aus',
  short: 'Inspektor: Kurz',
  detail: 'Inspektor: Details',
}

function readTooltipMode(): TooltipMode {
  try {
    const v = localStorage.getItem(TOOLTIP_MODE_KEY)
    if (v === 'off' || v === 'short' || v === 'detail') return v
  } catch { /* ignore */ }
  return 'short'
}

function nextTooltipMode(mode: TooltipMode): TooltipMode {
  const i = TOOLTIP_MODE_CYCLE.indexOf(mode)
  return TOOLTIP_MODE_CYCLE[(i + 1) % TOOLTIP_MODE_CYCLE.length]
}

function outcomeFactorValue(
  factor: OutcomeFactorMeta,
  cell: CellOutcomeBreakdown,
  r: RiskRecipe,
): string {
  if (factor.key === 'ref_value')
    return `${fmtNum(factor.value ?? cell.ref_value)}${factor.unit ? ' ' + factor.unit : ''}`
  if (factor.key === 'scale_factor') {
    if (r.scale === 'pop')
      return `${fmtNum(cell.scale_factor)} (= ${fmtNum(cell.cell_pop)} Ew. / 100.000)`
    if (r.scale === 'area')
      return `${fmtNum(cell.scale_factor)} (= ${fmtNum(cell.cell_area_km2)} km² / 50)`
    return fmtNum(cell.scale_factor)
  }
  return '—'
}

const TOOLTIP_MIN_WIDTH = 720
const TOOLTIP_MAX_WIDTH = 1200

function fmtNormFrac(normPct: number) {
  return fmtNum(normPct / 100)
}

function buildRiskFormulaHtml(
  r: RiskRecipe,
  cellPathways: CellPathwayBreakdown | undefined,
) {
  let s = `<div class="kap-formula-block">`
  s += `<div style="font-weight:600;font-size:10px;color:#475569;margin-bottom:3px">Index-Berechnung</div>`
  s += `<div class="kap-formula-line">${
    r.formula_index_header || 'Index = 100 · max(w·Ĥ·Ê·V̂)  (stärkste Wirkungskette; Ĥ,Ê,V̂ normiert 0…1)'
  }</div>`

  const meta = r.pathways || []
  const cells = cellPathways?.pathways || []

  for (let i = 0; i < meta.length; i++) {
    const p = meta[i]
    const c = cells[i]
    if (c) {
      const win = c.is_max
      s += `<div class="kap-formula-line"${win ? ' style="background:#ecfdf5"' : ''}>` +
        `<span style="color:#94a3b8">${p.type_label}${win ? ' ★' : ''}:</span> ` +
        `<code>${fmtNum(p.weight)} · ${fmtNormFrac(c.h_norm)} · ${fmtNormFrac(c.e_norm)} · ${fmtNormFrac(c.v_norm)}</code>` +
        ` <span style="color:#64748b">(Ĥ·Ê·V̂ = ${p.hazard_name} · ${p.exposure_name} · ${p.vulnerability_name})</span>` +
        ` → <strong>${fmtNum(c.term)}</strong></div>`
    } else {
      s += `<div class="kap-formula-line">` +
        `<span style="color:#94a3b8">${p.type_label}:</span> ` +
        `<code>${p.formula}</code></div>`
    }
  }

  if (cellPathways) {
    s += `<div class="kap-formula-line kap-formula-sum">` +
      `<code>max = ${fmtNum(cellPathways.max_term)}` +
      ` → Index = 100 · ${fmtNum(cellPathways.max_term)}` +
      ` = ${fmtNum(cellPathways.index)}</code>` +
      ` <span style="color:#64748b">(stärkste Kette ★)</span></div>`
  } else if (r.formula_index) {
    s += `<div class="kap-formula-line"><code>${r.formula_index}</code></div>`
  }

  s += `</div>`
  if (r.formula_outcome) {
    s += `<div class="kap-formula-line kap-formula-outcome"><code>${r.formula_outcome}</code></div>`
  }
  return s
}

function buildTooltipHtml(
  meta: LayerMeta,
  props: Record<string, unknown>,
  value: number,
  mode: TooltipMode,
) {
  const gridCells: string[] = []
  const gridHeader = () => {
    gridCells.push(
      '<span class="col-head">Name</span>',
      '<span class="col-head col-val">Wert</span>',
      '<span class="col-head col-norm">Norm</span>',
      '<span class="col-head">Quelle</span>',
    )
  }
  const gridSection = (title: string) => {
    gridCells.push(`<span class="grid-section">${title}</span>`)
  }
  const gridRow = (name: string, val: string, norm = '', src = '') => {
    gridCells.push(
      `<span class="col-name">${name}</span>`,
      `<span class="col-val">${val || '—'}</span>`,
      `<span class="col-norm">${norm}</span>`,
      `<span class="col-src">${src}</span>`,
    )
  }
  const gridHtml = () => gridCells.length
    ? `<div class="kap-tooltip-grid">${gridCells.join('')}</div>`
    : ''

  let h = `<div class="kap-tooltip-inner" style="--kap-tooltip-min:${TOOLTIP_MIN_WIDTH}px;--kap-tooltip-max:${TOOLTIP_MAX_WIDTH}px;font-family:system-ui,sans-serif;font-size:11px;line-height:1.4">`
  h += `<div style="font-weight:700;font-size:12px;margin-bottom:2px">${meta.label}</div>`
  h += `<div style="font-size:13px;font-weight:700;color:#0f172a;margin-bottom:4px">${fmtNum(value)} ${meta.unit}</div>`

  const r = meta.recipe
  if (r && isRiskRecipe(r)) {
    const idx = props.index != null ? Number(props.index) : null
    if (idx != null && mode === 'short')
      h += `<div style="margin:2px 0;font-size:10px;color:#64748b">Risiko-Index: <strong style="color:#0f172a">${fmtNum(idx)}</strong> (0–100)</div>`

    if (mode === 'detail') {
      h += buildRiskFormulaHtml(r, parseProp<CellPathwayBreakdown>(props.pathways))

      gridHeader()
      if (idx != null)
        gridRow('Risiko-Index', fmtNum(idx), '', '0–100')

      const sec = (title: string, items?: HevRecipeMeta[], vals?: number[][]) => {
        if (!items?.length) return
        gridSection(title)
        items.forEach((it, i) => {
          const pair = (vals && vals[i]) || [0, 0]
          const src = [
            it.source,
            it.spatial === false ? 'nicht räumlich' : '',
            it.norm_min != null && it.norm_max != null
              ? `[${fmtNum(it.norm_min)}…${fmtNum(it.norm_max)}]`
              : '',
          ].filter(Boolean).join(' · ')
          gridRow(
            it.name,
            `${fmtNum(pair[0])}${it.unit ? '\u00a0' + it.unit : ''}`,
            fmtNum(pair[1]),
            src,
          )
        })
      }
      sec('Klimatische Einflüsse', r.hazards, parseProp(props.H))
      sec('Räumliche Expositionen', r.exposures, parseProp(props.E))
      sec('Sensitivitäten', r.vulnerabilities, parseProp(props.V))

      const cellOutcome = parseProp<CellOutcomeBreakdown>(props.outcome)
      if (cellOutcome && r.outcome_factors?.length) {
        gridSection('Outcome-Faktoren')
        for (const factor of r.outcome_factors) {
          gridRow(
            factor.label,
            `${outcomeFactorValue(factor, cellOutcome, r)}${provBadge(factor.prov)}`,
            '',
            [factor.formula, factor.source].filter(Boolean).join(' · '),
          )
        }
        gridRow(
          'Index-Anteil',
          fmtNum(cellOutcome.index_fraction),
          '',
          `Index\u00a0${fmtNum(idx ?? 0)}/100`,
        )
      }

      h += gridHtml()
      h += '<div style="margin-top:5px;color:#94a3b8;font-size:9px">H,E,V normiert 0–100 für die Multiplikation</div>'

      if (cellOutcome && r.outcome_factors?.length) {
        h += `<div class="kap-formula-line kap-formula-outcome">` +
          `<code>${fmtNum(cellOutcome.ref_value)} · ${fmtNum(cellOutcome.index_fraction)} · ${fmtNum(cellOutcome.scale_factor)}` +
          ` = ${fmtNum(cellOutcome.outcome)} ${meta.unit}</code></div>`
      }
    }
  } else if (r && 'inputs' in r) {
    const ir = r as IndicatorRecipe
    if (mode === 'detail' && ir.formula)
      h += `<div class="kap-formula-line"><code>${ir.formula}</code></div>`
    if (mode === 'detail') {
      gridHeader()
      const cells = (parseProp(props.inputs) as ResolvedInput[]) || []
      ir.inputs.forEach((inp, i) => {
        const c = cells[i] || ({} as ResolvedInput)
        const prov = c.prov || inp.prov
        let disp: string
        const raw = c.v ?? inp.value
        if (raw == null) disp = '—'
        else if (typeof raw === 'string') disp = raw
        else disp = `${fmtNum(raw)}${inp.unit ? '\u00a0' + inp.unit : ''}`
        gridRow(inp.label, `${disp}${provBadge(prov)}`, '', inp.source || '')
      })
      h += gridHtml()
    }
  }
  h += '</div>'
  return h
}

export default function MapView() {
  const mapContainer = useRef<HTMLDivElement>(null)
  const mapRef = useRef<maplibregl.Map | null>(null)
  const popupRef = useRef<maplibregl.Popup | null>(null)
  const {
    kommune, measures, layerGeoJson, showMeasures,
    setIsDrawing, setDrawnGeometry, setSelectedMeasure, drawnGeometry,
    mapLoading, mapProgress,
  } = useStore()

  const [mapLoaded, setMapLoaded] = useState(false)
  const [tooltipMode, setTooltipMode] = useState<TooltipMode>(readTooltipMode)
  const [drawMode, setDrawMode] = useState(false)
  const [drawCoords, setDrawCoords] = useState<[number, number][]>([])
  const [cursorCoord, setCursorCoord] = useState<[number, number] | null>(null)
  const [showMeasureForm, setShowMeasureForm] = useState(false)

  const meta = layerGeoJson?.meta as LayerMeta | undefined
  const scaleBounds = useMemo(() => layerScaleBounds(meta), [meta])
  const { activeLayer, setActiveLayer } = useStore()

  // Layer-Cache ohne aktuelle Tooltip-Metadaten automatisch neu laden
  useEffect(() => {
    if (!kommune || !activeLayer || !layerGeoJson) return
    const layerMeta = layerGeoJson.meta as LayerMeta | undefined
    const recipe = layerMeta?.recipe
    const staleRiskRecipe = activeLayer.category === 'risks' && recipe && isRiskRecipe(recipe)
      && (!recipe.outcome_factors?.length || !recipe.pathways?.length)
    if (layerMeta && (!recipe || staleRiskRecipe)) {
      setActiveLayer(activeLayer).catch(() => {})
    }
  }, [kommune?.id, activeLayer?.code])

  // Initialize map
  useEffect(() => {
    if (!mapContainer.current || mapRef.current) return
    const map = new maplibregl.Map({
      container: mapContainer.current,
      style: {
        version: 8,
        sources: {
          osm: {
            type: 'raster',
            tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
            tileSize: 256,
            attribution: '&copy; OpenStreetMap contributors',
          },
        },
        layers: [{ id: 'osm', type: 'raster', source: 'osm' }],
      },
      center: [10.4515, 51.1657],
      zoom: 6,
    })
    map.addControl(new maplibregl.NavigationControl(), 'top-right')
    map.on('load', () => setMapLoaded(true))
    mapRef.current = map
    return () => { map.remove(); mapRef.current = null; setMapLoaded(false) }
  }, [])

  // Fit to kommune boundary
  useEffect(() => {
    const map = mapRef.current
    if (!map || !mapLoaded || !kommune?.boundary_geojson) return
    try {
      const geojson: GeoJSON.GeoJSON = {
        type: 'Feature', properties: {},
        geometry: kommune.boundary_geojson as unknown as GeoJSON.Geometry,
      }
      const src = map.getSource('kommune-boundary') as maplibregl.GeoJSONSource
      if (src) src.setData(geojson)
      else {
        map.addSource('kommune-boundary', { type: 'geojson', data: geojson })
        map.addLayer({
          id: 'kommune-boundary-line', type: 'line', source: 'kommune-boundary',
          paint: { 'line-color': '#2563eb', 'line-width': 2.5, 'line-dasharray': [3, 2] },
        })
      }
      const coords = kommune.boundary_geojson.coordinates as number[][][][]
      let minLng = Infinity, maxLng = -Infinity, minLat = Infinity, maxLat = -Infinity
      for (const poly of coords) for (const ring of poly) for (const [lng, lat] of ring) {
        if (lng < minLng) minLng = lng; if (lng > maxLng) maxLng = lng
        if (lat < minLat) minLat = lat; if (lat > maxLat) maxLat = lat
      }
      map.fitBounds([[minLng, minLat], [maxLng, maxLat]], { padding: 40 })
    } catch (err) { console.warn('MapView: boundary layer error', err) }
  }, [kommune, mapLoaded])

  // Active choropleth layer (H/E/V/Risiko)
  useEffect(() => {
    const map = mapRef.current
    if (!map || !mapLoaded) return
    const empty: GeoJSON.GeoJSON = { type: 'FeatureCollection', features: [] }
    const data: GeoJSON.GeoJSON = layerGeoJson
      ? {
          type: 'FeatureCollection',
          features: (layerGeoJson.features || []).map(f => ({
            type: 'Feature' as const,
            properties: f.properties || {},
            geometry: f.geometry as unknown as GeoJSON.Geometry,
          })),
        }
      : empty

    const { lo, hi } = layerScaleBounds(meta)
    const colors = choroplethColors(meta?.code)
    const stops = colors.map((c, i) => [lo + (hi - lo) * (i / (colors.length - 1)), c]).flat()

    try {
      if (map.getLayer('active-layer-points')) map.removeLayer('active-layer-points')
      const src = map.getSource('active-layer') as maplibregl.GeoJSONSource
      if (src) {
        src.setData(data)
        if (map.getLayer('active-layer-fill')) {
          map.setPaintProperty('active-layer-fill', 'fill-color',
            ['interpolate', ['linear'], ['coalesce', ['get', 'value'], 0], ...stops] as unknown as maplibregl.ExpressionSpecification)
        }
      } else {
        map.addSource('active-layer', { type: 'geojson', data })
        const beforeId = map.getLayer('measures-fill') ? 'measures-fill' : undefined
        map.addLayer({
          id: 'active-layer-fill', type: 'fill', source: 'active-layer',
          paint: {
            'fill-color': ['interpolate', ['linear'], ['coalesce', ['get', 'value'], 0], ...stops] as unknown as maplibregl.ExpressionSpecification,
            'fill-opacity': 0.6,
          },
        }, beforeId)
        map.addLayer({
          id: 'active-layer-line', type: 'line', source: 'active-layer',
          paint: { 'line-color': '#00000022', 'line-width': 0.3 },
        }, beforeId)
      }
    } catch (err) { console.warn('MapView: active layer error', err) }
  }, [layerGeoJson, mapLoaded, meta])

  const setTooltipModePersist = (mode: TooltipMode) => {
    setTooltipMode(mode)
    try { localStorage.setItem(TOOLTIP_MODE_KEY, mode) } catch { /* ignore */ }
    if (mode === 'off') popupRef.current?.remove()
  }

  const cycleTooltipMode = () => setTooltipModePersist(nextTooltipMode(tooltipMode))

  // Tooltip ausblenden beim Maßnahmen-Zeichnen
  useEffect(() => {
    if (drawMode) popupRef.current?.remove()
  }, [drawMode])

  // Tooltip (eigener Effect: MapLibre unterstützt keine verschachtelten Properties)
  useEffect(() => {
    const map = mapRef.current
    if (!map || !mapLoaded) return

    const onMove = (e: maplibregl.MapMouseEvent & { features?: maplibregl.MapGeoJSONFeature[] }) => {
      if (tooltipMode === 'off' || drawMode) {
        popupRef.current?.remove()
        return
      }
      if (!e.features?.[0]) return
      const hit = e.features[0]
      const layerData = useStore.getState().layerGeoJson
      const m = layerData?.meta as LayerMeta | undefined
      if (!m) return

      const cellId = hit.properties?.grid_cell_id
      const full = layerData?.features?.find(
        f => f.properties?.grid_cell_id === cellId,
      )
      const props = (full?.properties ?? hit.properties) as Record<string, unknown>
      const v = props?.value
      if (v == null) return

      if (!popupRef.current) {
        popupRef.current = new maplibregl.Popup({
          closeButton: false,
          closeOnClick: false,
          maxWidth: `${TOOLTIP_MAX_WIDTH}px`,
          className: 'kap-tooltip',
        })
      } else {
        popupRef.current.setMaxWidth(`${TOOLTIP_MAX_WIDTH}px`)
      }
      popupRef.current
        .setLngLat(e.lngLat)
        .setHTML(buildTooltipHtml(m, props, Number(v), tooltipMode))
        .addTo(map)
    }
    const onLeave = () => popupRef.current?.remove()

    if (!map.getLayer('active-layer-fill')) return

    map.on('mousemove', 'active-layer-fill', onMove)
    map.on('mouseleave', 'active-layer-fill', onLeave)
    return () => {
      map.off('mousemove', 'active-layer-fill', onMove)
      map.off('mouseleave', 'active-layer-fill', onLeave)
    }
  }, [mapLoaded, layerGeoJson, tooltipMode, drawMode])

  // Measures overlay
  useEffect(() => {
    const map = mapRef.current
    if (!map || !mapLoaded) return
    try {
      const features = measures.filter(m => m.geometry_geojson).map(m => ({
        type: 'Feature' as const,
        properties: { id: m.id, name: m.name, type: m.measure_type },
        geometry: m.geometry_geojson as unknown as GeoJSON.Geometry,
      }))
      const geojson: GeoJSON.GeoJSON = { type: 'FeatureCollection', features }
      const src = map.getSource('measures') as maplibregl.GeoJSONSource
      if (src) src.setData(geojson)
      else {
        map.addSource('measures', { type: 'geojson', data: geojson })
        map.addLayer({
          id: 'measures-fill', type: 'fill', source: 'measures',
          paint: { 'fill-color': '#7c3aed', 'fill-opacity': 0.3 },
        })
        map.addLayer({
          id: 'measures-line', type: 'line', source: 'measures',
          paint: { 'line-color': '#7c3aed', 'line-width': 2 },
        })
        map.on('click', 'measures-fill', (e) => {
          if (!e.features?.[0]) return
          const id = e.features[0].properties?.id
          const measure = useStore.getState().measures.find(m => m.id === id)
          if (measure) setSelectedMeasure(measure)
        })
      }
    } catch (err) { console.warn('MapView: measures layer error', err) }
  }, [measures, mapLoaded])

  // Measures visibility
  useEffect(() => {
    const map = mapRef.current
    if (!map || !mapLoaded) return
    for (const id of ['measures-fill', 'measures-line']) {
      if (map.getLayer(id)) map.setLayoutProperty(id, 'visibility', showMeasures ? 'visible' : 'none')
    }
  }, [showMeasures, mapLoaded, measures])

  // Drawing polygon + vertices + cursor line
  useEffect(() => {
    const map = mapRef.current
    if (!map || !mapLoaded) return
    try {
      const allCoords = cursorCoord && drawCoords.length > 0 ? [...drawCoords, cursorCoord] : drawCoords
      const geojson: GeoJSON.GeoJSON = allCoords.length >= 3
        ? { type: 'Feature', properties: {}, geometry: { type: 'Polygon', coordinates: [[...allCoords, allCoords[0]]] } }
        : allCoords.length >= 2
          ? { type: 'Feature', properties: {}, geometry: { type: 'LineString', coordinates: allCoords } }
          : { type: 'FeatureCollection', features: [] }
      const src = map.getSource('drawing') as maplibregl.GeoJSONSource
      if (src) src.setData(geojson)
      else {
        map.addSource('drawing', { type: 'geojson', data: geojson })
        map.addLayer({ id: 'drawing-fill', type: 'fill', source: 'drawing', paint: { 'fill-color': '#ec4899', 'fill-opacity': 0.25 } })
        map.addLayer({ id: 'drawing-line', type: 'line', source: 'drawing', paint: { 'line-color': '#ec4899', 'line-width': 2 } })
      }
      const vertexGeojson: GeoJSON.GeoJSON = {
        type: 'FeatureCollection',
        features: drawCoords.map((c, i) => ({
          type: 'Feature', properties: { index: i, isFirst: i === 0 },
          geometry: { type: 'Point', coordinates: c },
        })),
      }
      const vertexSrc = map.getSource('drawing-vertices') as maplibregl.GeoJSONSource
      if (vertexSrc) vertexSrc.setData(vertexGeojson)
      else {
        map.addSource('drawing-vertices', { type: 'geojson', data: vertexGeojson })
        map.addLayer({
          id: 'drawing-vertices-circle', type: 'circle', source: 'drawing-vertices',
          paint: {
            'circle-radius': ['case', ['get', 'isFirst'], 7, 5],
            'circle-color': ['case', ['get', 'isFirst'], '#22c55e', '#ec4899'],
            'circle-stroke-width': 2, 'circle-stroke-color': '#fff',
          },
        })
      }
    } catch (err) { console.warn('MapView: drawing layer error', err) }
  }, [drawCoords, cursorCoord])

  // Handle map clicks for drawing + mousemove for cursor line
  useEffect(() => {
    const map = mapRef.current
    if (!map || !mapLoaded) return
    const SNAP_DIST = 15

    const handleClick = (e: maplibregl.MapMouseEvent) => {
      if (!drawMode) return
      const coord: [number, number] = [e.lngLat.lng, e.lngLat.lat]
      setDrawCoords(prev => {
        if (prev.length >= 3) {
          const firstPt = map.project(new maplibregl.LngLat(prev[0][0], prev[0][1]))
          const clickPt = map.project(e.lngLat)
          const dist = Math.sqrt((firstPt.x - clickPt.x) ** 2 + (firstPt.y - clickPt.y) ** 2)
          if (dist < SNAP_DIST) {
            setDrawnGeometry({ type: 'Polygon', coordinates: [[...prev, prev[0]]] })
            setShowMeasureForm(true)
            setDrawMode(false); setCursorCoord(null); setIsDrawing(false)
            if (mapRef.current) mapRef.current.doubleClickZoom.enable()
            return []
          }
        }
        return [...prev, coord]
      })
    }

    const handleDblClick = (e: maplibregl.MapMouseEvent) => {
      if (!drawMode) return
      e.preventDefault()
      setDrawCoords(prev => {
        const coords = [...prev, [e.lngLat.lng, e.lngLat.lat] as [number, number]]
        if (coords.length >= 3) {
          setDrawnGeometry({ type: 'Polygon', coordinates: [[...coords, coords[0]]] })
          setShowMeasureForm(true)
        }
        setDrawMode(false); setCursorCoord(null); setIsDrawing(false)
        if (mapRef.current) mapRef.current.doubleClickZoom.enable()
        return []
      })
    }

    const handleMouseMove = (e: maplibregl.MapMouseEvent) => {
      if (!drawMode) return
      setCursorCoord([e.lngLat.lng, e.lngLat.lat])
      setDrawCoords(prev => {
        if (prev.length >= 3) {
          const firstPt = map.project(new maplibregl.LngLat(prev[0][0], prev[0][1]))
          const movePt = map.project(e.lngLat)
          const dist = Math.sqrt((firstPt.x - movePt.x) ** 2 + (firstPt.y - movePt.y) ** 2)
          map.getCanvas().style.cursor = dist < SNAP_DIST ? 'pointer' : 'crosshair'
        } else map.getCanvas().style.cursor = 'crosshair'
        return prev
      })
    }

    map.on('click', handleClick)
    map.on('dblclick', handleDblClick)
    map.on('mousemove', handleMouseMove)
    return () => {
      map.off('click', handleClick)
      map.off('dblclick', handleDblClick)
      map.off('mousemove', handleMouseMove)
      map.getCanvas().style.cursor = ''
    }
  }, [drawMode])

  const startDraw = () => {
    setDrawMode(true); setDrawCoords([]); setIsDrawing(true); setDrawnGeometry(null)
    if (mapRef.current) mapRef.current.doubleClickZoom.disable()
  }
  const cancelDraw = () => {
    setDrawMode(false); setDrawCoords([]); setCursorCoord(null); setIsDrawing(false); setDrawnGeometry(null)
    if (mapRef.current) { mapRef.current.doubleClickZoom.enable(); mapRef.current.getCanvas().style.cursor = '' }
  }

  const fmt = (v: number) => v.toLocaleString('de-DE', { maximumFractionDigits: 2 })

  const progressPct = Math.round((mapProgress ?? 0) * 100)

  return (
    <>
      <div ref={mapContainer} style={{ width: '100%', height: '100%' }} />

      {mapLoading && (
        <div className="map-loading-overlay" role="status" aria-live="polite">
          <div className="map-loading-box">
            <div className="map-spinner" />
            <div className="map-loading-label">Karte wird geladen …</div>
            <div className="map-progress">
              <div className="map-progress-bar" style={{ width: `${progressPct}%` }} />
            </div>
            <div className="map-progress-value">{progressPct}%</div>
          </div>
        </div>
      )}

      <div className="draw-toolbar">
        {!drawMode ? (
          <button onClick={startDraw} title="Maßnahme einzeichnen">✏️ Maßnahme zeichnen</button>
        ) : (
          <>
            <button className="active">Ecken klicken · grünen Startpunkt klicken zum Schließen</button>
            <button onClick={cancelDraw}>✕ Abbrechen</button>
          </>
        )}
        <button
          type="button"
          className={`tooltip-mode-btn${tooltipMode !== 'off' ? ' active' : ''}`}
          onClick={cycleTooltipMode}
          title="Inspektor: Aus → Kurz → Details"
          aria-label={TOOLTIP_MODE_LABEL[tooltipMode]}
        >{TOOLTIP_MODE_LABEL[tooltipMode]}</button>
      </div>

      {/* Legend for active layer */}
      {meta && layerGeoJson?.features && layerGeoJson.features.length > 0 && (
        <div className="map-legend">
          <div style={{ fontWeight: 600, marginBottom: 4 }}>{meta.label}</div>
          <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: 4 }}>{meta.unit}</div>
          <div style={{ display: 'flex', height: 10, borderRadius: 3, overflow: 'hidden' }}>
            {choroplethColors(meta.code).map(c => <div key={c} style={{ flex: 1, background: c }} />)}
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.7rem', marginTop: 2 }}>
            <span>{fmt(scaleBounds.lo)}</span>
            <span>{fmt(scaleBounds.hi)}</span>
          </div>
          {meta.code === 'HEALTHCARE_ACCESS_INDEX' && (
            <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginTop: 4 }}>
              Höher = schlechterer Zugang
            </div>
          )}
          {meta.code === 'HEALTHCARE_ACCESS_GRID' && (
            <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginTop: 4 }}>
              0,50·KH + 0,35·Arzt + 0,15·Apo (höher = besser)
            </div>
          )}
        </div>
      )}

      {showMeasureForm && <MeasureCreateModal onClose={() => setShowMeasureForm(false)} />}
    </>
  )
}

// ── Measure creation modal (catalog-driven) ─────────────────────────────────

function MeasureCreateModal({ onClose }: { onClose: () => void }) {
  const { kommune, drawnGeometry, measures, catalog, createMeasure, calculateImpact, setSelectedMeasure } = useStore()
  const measureDefs = catalog?.measures || []
  const clusters = catalog?.kang_clusters || []
  const risks = catalog?.risks || []
  const [mode, setMode] = useState<'kang' | 'risk'>('kang')
  const [clusterCode, setClusterCode] = useState('')
  const [fieldCode, setFieldCode] = useState('')
  const [riskCode, setRiskCode] = useState('')
  const [measureCode, setMeasureCode] = useState('')
  const [implYear, setImplYear] = useState(2026)
  const [saving, setSaving] = useState(false)
  const [count, setCount] = useState<number | null>(null)

  const activeCluster = clusters.find(c => c.code === clusterCode)

  // Auswahlmenge je nach Modus
  const filteredMeasures = useMemo(() => {
    if (mode === 'kang') {
      return measureDefs.filter(m =>
        (!clusterCode || m.kang_cluster === clusterCode) &&
        (!fieldCode || m.kang_field === fieldCode))
    }
    return measureDefs.filter(m => !riskCode || m.linked_risk_codes.includes(riskCode))
  }, [mode, clusterCode, fieldCode, riskCode, measureDefs])

  // Bei Wechsel der Vorauswahl: erste passende Maßnahme wählen
  useEffect(() => {
    if (filteredMeasures.length > 0 && !filteredMeasures.some(m => m.code === measureCode)) {
      setMeasureCode(filteredMeasures[0].code)
    } else if (filteredMeasures.length === 0) {
      setMeasureCode('')
    }
  }, [filteredMeasures])

  const current = measureDefs.find(m => m.code === measureCode)

  const polyArea = useMemo(() => {
    if (!drawnGeometry) return 0
    const coords = (drawnGeometry as { coordinates: number[][][] }).coordinates?.[0]
    if (!coords || coords.length < 3) return 0
    const R = 6371000
    const toRad = (d: number) => d * Math.PI / 180
    const refLat = coords[0][1]
    const points = coords.map(c => [
      R * toRad(c[0] - coords[0][0]) * Math.cos(toRad(refLat)),
      R * toRad(c[1] - coords[0][1]),
    ])
    let area = 0
    for (let i = 0; i < points.length - 1; i++) area += points[i][0] * points[i + 1][1] - points[i + 1][0] * points[i][1]
    return Math.abs(area / 2)
  }, [drawnGeometry])
  const polyAreaHa = polyArea / 10000

  const recommendedCount = useMemo(() => {
    if (!current || current.unit_label == null) return null
    return Math.max(1, Math.round((current.unit_density_per_ha ?? 0) * polyAreaHa))
  }, [current, polyAreaHa])

  useEffect(() => { setCount(recommendedCount) }, [measureCode])

  const autoName = useMemo(() => {
    const label = current?.name || measureCode
    const existing = measures.filter(m => m.measure_type === measureCode).length + 1
    const areaStr = polyAreaHa >= 1 ? `${polyAreaHa.toFixed(1)} ha` : `${Math.round(polyArea)} m²`
    return `${label} #${existing} (${areaStr})`
  }, [measureCode, measures, polyArea, current])

  const [name, setName] = useState(autoName)
  useEffect(() => { setName(autoName) }, [autoName])

  const handleSave = async () => {
    if (!kommune || !drawnGeometry || !current) return
    setSaving(true)
    try {
      const measure = await createMeasure(kommune.id, {
        name: name || autoName,
        measure_type: measureCode,
        geometry_geojson: drawnGeometry,
        config: current?.unit_label != null ? { count: count ?? recommendedCount ?? 1 } : {},
        implementation_year: implYear,
      })
      await calculateImpact(measure.id)
      setSelectedMeasure(measure)
      onClose()
    } catch (e) {
      console.error('Failed to create measure:', e)
    } finally {
      setSaving(false)
    }
  }

  return (
    <div style={{
      position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)',
      background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 12,
      padding: '1.5rem', width: 420, zIndex: 100, boxShadow: '0 8px 32px rgba(0,0,0,0.2)',
    }}>
      <h3 style={{ marginBottom: '0.5rem', fontSize: '1rem' }}>Neue Anpassungsmaßnahme</h3>

      {polyArea > 0 && (
        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.75rem' }}>
          Fläche: {polyAreaHa >= 1 ? `${polyAreaHa.toFixed(2)} ha` : `${Math.round(polyArea)} m²`}
        </div>
      )}

      <div style={{ display: 'flex', gap: 6, marginBottom: '0.75rem' }}>
        <button
          type="button"
          className={`btn ${mode === 'kang' ? 'btn-primary' : 'btn-secondary'}`}
          style={{ flex: 1, fontSize: '0.76rem', padding: '6px 8px' }}
          onClick={() => setMode('kang')}
        >Nach Handlungsfeld</button>
        <button
          type="button"
          className={`btn ${mode === 'risk' ? 'btn-primary' : 'btn-secondary'}`}
          style={{ flex: 1, fontSize: '0.76rem', padding: '6px 8px' }}
          onClick={() => setMode('risk')}
        >Nach Ziel-Risiko</button>
      </div>

      {mode === 'kang' ? (
        <>
          <div className="form-group">
            <label>KAnG-Cluster</label>
            <select value={clusterCode} onChange={e => { setClusterCode(e.target.value); setFieldCode('') }}>
              <option value="">Alle Cluster</option>
              {clusters.map(c => <option key={c.code} value={c.code}>{c.label}</option>)}
            </select>
          </div>
          {activeCluster && activeCluster.fields.length > 1 && (
            <div className="form-group">
              <label>Handlungsfeld</label>
              <select value={fieldCode} onChange={e => setFieldCode(e.target.value)}>
                <option value="">Alle Handlungsfelder</option>
                {activeCluster.fields.map(f => <option key={f.code} value={f.code}>{f.label}</option>)}
              </select>
            </div>
          )}
        </>
      ) : (
        <div className="form-group">
          <label>Ziel-Risiko</label>
          <select value={riskCode} onChange={e => setRiskCode(e.target.value)}>
            <option value="">Alle Risiken</option>
            {risks.map(r => <option key={r.code} value={r.code}>{r.name}</option>)}
          </select>
        </div>
      )}

      <div className="form-group">
        <label>Maßnahme ({filteredMeasures.length})</label>
        <select value={measureCode} onChange={e => setMeasureCode(e.target.value)}>
          {filteredMeasures.length === 0 && <option value="">Keine passende Maßnahme</option>}
          {filteredMeasures.map(m => <option key={m.code} value={m.code}>{m.name}</option>)}
        </select>
      </div>

      {current && (
        <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '0.75rem', lineHeight: 1.4 }}>
          {current.description}
          <div style={{ marginTop: 4 }}>
            <strong>Wirkt auf:</strong> {current.effect_target.join(', ')} ·{' '}
            <strong>Minderung:</strong> {Math.round((current.default_reduction || 0) * 100)}%
          </div>
          {current.linked_risk_codes.length > 0 && (
            <div style={{ marginTop: 2 }}>
              <strong>Verknüpfte Risiken:</strong> {current.linked_risk_codes.length}
            </div>
          )}
        </div>
      )}

      {current?.unit_label != null && (
        <div className="form-group">
          <label>Anzahl ({current.unit_label})</label>
          <input
            type="number" min={0} value={count ?? ''}
            onChange={e => setCount(e.target.value === '' ? null : parseInt(e.target.value, 10) || 0)}
          />
          <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: 4 }}>
            Richtwert: {recommendedCount} {current.unit_label}
            {current.unit_density_per_ha != null && ` (Dichte ${current.unit_density_per_ha}/ha × ${polyAreaHa.toFixed(2)} ha)`}
          </div>
        </div>
      )}

      {current && (() => {
        const c = count ?? recommendedCount ?? 0
        const capexParts: { label: string; amount: number }[] = []
        if (current.capex_fixed != null) capexParts.push({ label: 'Grundkosten (Planung/Konzept)', amount: current.capex_fixed })
        if (current.capex_per_unit != null && current.unit_label != null)
          capexParts.push({ label: `${c} × ${current.capex_per_unit.toLocaleString('de-DE')} €/${current.unit_label}`, amount: c * current.capex_per_unit })
        if (current.capex_per_m2 != null)
          capexParts.push({ label: `${Math.round(polyArea)} m² × ${current.capex_per_m2.toLocaleString('de-DE')} €/m²`, amount: polyArea * current.capex_per_m2 })
        const opexParts: { label: string; amount: number }[] = []
        if (current.opex_fixed_year != null) opexParts.push({ label: 'Feste Betriebskosten/Jahr', amount: current.opex_fixed_year })
        if (current.opex_per_unit_year != null && current.unit_label != null)
          opexParts.push({ label: `${c} × ${current.opex_per_unit_year.toLocaleString('de-DE')} €/${current.unit_label}·a`, amount: c * current.opex_per_unit_year })
        if (current.opex_per_m2_year != null)
          opexParts.push({ label: `${Math.round(polyArea)} m² × ${current.opex_per_m2_year.toLocaleString('de-DE')} €/m²·a`, amount: polyArea * current.opex_per_m2_year })
        if (!capexParts.length && !opexParts.length) return null
        const fmt = (v: number) => v.toLocaleString('de-DE', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 })
        const capexTotal = capexParts.reduce((s, p) => s + p.amount, 0)
        const opexTotal = opexParts.reduce((s, p) => s + p.amount, 0)
        return (
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.75rem' }}>
            <strong>Kostenschätzung (Katalogwerte, vorläufig):</strong>
            {capexParts.length > 0 && (
              <div style={{ marginTop: 2 }}>
                CAPEX (einmalig): {fmt(capexTotal)}
                {capexParts.map((p, i) => <div key={i} style={{ marginLeft: 8 }}>· {p.label}</div>)}
              </div>
            )}
            {opexParts.length > 0 && (
              <div style={{ marginTop: 2 }}>
                OPEX (jährlich): {fmt(opexTotal)}
                {opexParts.map((p, i) => <div key={i} style={{ marginLeft: 8 }}>· {p.label}</div>)}
              </div>
            )}
          </div>
        )
      })()}

      <div className="form-group">
        <label>Name</label>
        <input value={name} onChange={e => setName(e.target.value)} placeholder={autoName} />
      </div>

      <div className="form-group">
        <label>Umsetzungsjahr</label>
        <input type="number" value={implYear} onChange={e => setImplYear(parseInt(e.target.value) || 2026)} />
      </div>

      <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem' }}>
        <button className="btn btn-primary" onClick={handleSave} disabled={saving || !current}>
          {saving ? 'Speichern...' : 'Anlegen & Berechnen'}
        </button>
        <button className="btn btn-secondary" onClick={onClose}>Abbrechen</button>
      </div>
    </div>
  )
}
