import { useEffect, useMemo, useRef, useState } from 'react'
import maplibregl from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
import { CHOROPLETH_COLORS, GeoCell } from './landingData'
import { gridAlignBearing } from '../../utils/gridBearing'

export type DrawShape = 'rect' | 'polygon'

export interface LandingMapDraw {
  shape: DrawShape
  coveredIds: ReadonlySet<number>
  ring: [number, number][] | null
  onCoverage: (ids: Set<number>, ring: [number, number][] | null) => void
}

interface Props {
  /** Zellgeometrie (aus dem echten Oschatz-Cache). */
  cells: GeoCell[]
  bounds: [[number, number], [number, number]]
  /** Kartenwert je Zelle-ID (Choropleth relativ zu Min/Max); null = keine Färbung. */
  valueForId: (id: number) => number | null | undefined
  /** Optionaler Hover-Detail-Tooltip (HTML) je Zelle-ID. */
  tooltipForId?: (id: number) => string | null
  legend?: { label: string; unit: string }
  ariaLabel: string
  draw?: LandingMapDraw
}

const SNAP_DIST = 15
const EMPTY: GeoJSON.FeatureCollection = { type: 'FeatureCollection', features: [] }

function setSourceData(map: maplibregl.Map, id: string, data: GeoJSON.GeoJSON) {
  // Beim Unmount läuft map.remove() (Init-Effekt) vor den Cleanups der
  // Zeichnen-/Overlay-Effekte — danach ist der Style weg und getSource wirft
  // "this.style is undefined". In dem Fall ist nichts mehr zu setzen.
  if (map._removed) return
  const src = map.getSource(id) as maplibregl.GeoJSONSource | undefined
  if (src) src.setData(data)
}

function ringFeature(ring: [number, number][] | null): GeoJSON.GeoJSON {
  return ring && ring.length >= 4
    ? { type: 'Feature', properties: {}, geometry: { type: 'Polygon', coordinates: [ring] } }
    : EMPTY
}

function rectRing(a: [number, number], b: [number, number]): [number, number][] {
  const [x1, y1] = a
  const [x2, y2] = b
  return [[x1, y1], [x2, y1], [x2, y2], [x1, y2], [x1, y1]]
}

function pointInRing(pt: [number, number], ring: [number, number][]): boolean {
  const [x, y] = pt
  let inside = false
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const [xi, yi] = ring[i]
    const [xj, yj] = ring[j]
    if (yi > y !== yj > y && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) inside = !inside
  }
  return inside
}

const fmtLegend = (v: number) => v.toLocaleString('de-DE', { maximumFractionDigits: 2 })

/**
 * MapLibre-Karte der Landing-Widgets: echte OSM-Kacheln mit dem echten
 * Oschatz-100 m-Raster als Choropleth (wie das Hauptkartenfenster,
 * components/MapView.tsx) — feste Ansicht, Tool-Legende, optionaler
 * Detail-Inspektor und Einzeichnen einer einzigen Maßnahme.
 */
export default function LandingMap({ cells, bounds, valueForId, tooltipForId, legend, ariaLabel, draw }: Props) {
  const container = useRef<HTMLDivElement>(null)
  const mapRef = useRef<maplibregl.Map | null>(null)
  const popupRef = useRef<maplibregl.Popup | null>(null)
  const [loaded, setLoaded] = useState(false)

  const tooltipRef = useRef(tooltipForId)
  const onCoverageRef = useRef(draw?.onCoverage)
  const coveredIdsRef = useRef(draw?.coveredIds)
  const drawCoordsRef = useRef<[number, number][]>([])
  const rectStartRef = useRef<[number, number] | null>(null)
  useEffect(() => { tooltipRef.current = tooltipForId })
  useEffect(() => { onCoverageRef.current = draw?.onCoverage })
  useEffect(() => { coveredIdsRef.current = draw?.coveredIds })

  const data = useMemo<GeoJSON.FeatureCollection>(() => ({
    type: 'FeatureCollection',
    features: cells.map((c) => ({
      type: 'Feature', properties: { id: c.id, value: valueForId(c.id) ?? null },
      geometry: { type: 'Polygon', coordinates: [c.polygon] },
    })),
  }), [cells, valueForId])

  const scale = useMemo(() => {
    const vals = data.features.map((f) => f.properties?.value).filter((v): v is number => typeof v === 'number')
    const lo = vals.length ? Math.min(...vals) : 0
    const hiRaw = vals.length ? Math.max(...vals) : 1
    return { lo, hi: hiRaw > lo ? hiRaw : lo + 1 }
  }, [data])

  const coveredGeoJson = (ids: ReadonlySet<number>): GeoJSON.FeatureCollection => ({
    type: 'FeatureCollection',
    features: cells.filter((c) => ids.has(c.id)).map((c) => ({
      type: 'Feature', properties: { id: c.id }, geometry: { type: 'Polygon', coordinates: [c.polygon] },
    })),
  })
  const coverIds = (ring: [number, number][]): Set<number> => {
    const ids = new Set<number>()
    if (ring.length < 3) return ids
    for (const c of cells) if (pointInRing(c.center, ring)) ids.add(c.id)
    return ids
  }

  // ── Map-Init (einmalig) ────────────────────────────────────────────────
  useEffect(() => {
    if (!container.current || mapRef.current) return
    // Bearing, das das EPSG:3035-Raster viewport-parallel stellt (Zellen sind
    // statische Snapshot-Daten → einmalige Berechnung genügt, Deps bleiben leer).
    const bearing = gridAlignBearing(cells[0]?.polygon) ?? 0
    const map = new maplibregl.Map({
      container: container.current,
      style: {
        version: 8,
        sources: {
          osm: { type: 'raster', tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'], tileSize: 256, attribution: '&copy; OpenStreetMap contributors' },
        },
        layers: [{ id: 'osm', type: 'raster', source: 'osm' }],
      },
      bounds,
      fitBoundsOptions: { padding: 0, bearing },
      maxBounds: bounds,
      dragRotate: false,
    })
    map.touchZoomRotate.disableRotation()
    map.keyboard.disableRotation()
    map.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'top-right')
    map.on('load', () => { map.setMinZoom(map.getZoom()); setLoaded(true) })
    mapRef.current = map
    return () => { map.remove(); mapRef.current = null; setLoaded(false) }
  }, [])

  // ── Grid-Layer + Choropleth ────────────────────────────────────────────
  useEffect(() => {
    const map = mapRef.current
    if (!map || !loaded) return
    const stops = CHOROPLETH_COLORS.map((c, i) => [scale.lo + (scale.hi - scale.lo) * (i / (CHOROPLETH_COLORS.length - 1)), c]).flat()
    const fillColor = ['interpolate', ['linear'], ['coalesce', ['get', 'value'], 0], ...stops]

    if (map.getSource('grid')) {
      setSourceData(map, 'grid', data)
      map.setPaintProperty('grid-fill', 'fill-color', fillColor as maplibregl.ExpressionSpecification)
      return
    }
    map.addSource('grid', { type: 'geojson', data })
    map.addLayer({ id: 'grid-fill', type: 'fill', source: 'grid', paint: { 'fill-color': fillColor as maplibregl.ExpressionSpecification, 'fill-opacity': ['case', ['==', ['get', 'value'], null], 0, 0.6] } })
    map.addLayer({ id: 'grid-line', type: 'line', source: 'grid', paint: { 'line-color': '#00000022', 'line-width': 0.3 } })
    map.addSource('covered', { type: 'geojson', data: EMPTY })
    map.addLayer({ id: 'covered-fill', type: 'fill', source: 'covered', paint: { 'fill-color': '#7c3aed', 'fill-opacity': 0.35 } })
    map.addSource('measure', { type: 'geojson', data: EMPTY })
    map.addLayer({ id: 'measure-line', type: 'line', source: 'measure', paint: { 'line-color': '#7c3aed', 'line-width': 2 } })
    map.addSource('drawing', { type: 'geojson', data: EMPTY })
    map.addLayer({ id: 'drawing-fill', type: 'fill', source: 'drawing', paint: { 'fill-color': '#ec4899', 'fill-opacity': 0.2 } })
    map.addLayer({ id: 'drawing-line', type: 'line', source: 'drawing', paint: { 'line-color': '#ec4899', 'line-width': 2 } })
    map.addSource('drawing-vertices', { type: 'geojson', data: EMPTY })
    map.addLayer({
      id: 'drawing-vertices-circle', type: 'circle', source: 'drawing-vertices',
      paint: { 'circle-radius': ['case', ['get', 'isFirst'], 7, 5], 'circle-color': ['case', ['get', 'isFirst'], '#22c55e', '#ec4899'], 'circle-stroke-width': 2, 'circle-stroke-color': '#fff' },
    })
  }, [data, scale, loaded])

  // ── Hover-Detail-Tooltip (nur wenn tooltipForId & nicht im Zeichenmodus) ─
  useEffect(() => {
    const map = mapRef.current
    if (!map || !loaded || !tooltipForId || draw) return
    const onMove = (e: maplibregl.MapMouseEvent & { features?: maplibregl.MapGeoJSONFeature[] }) => {
      const id = e.features?.[0]?.properties?.id
      const build = tooltipRef.current
      if (id == null || !build) return
      const html = build(Number(id))
      if (!html) { popupRef.current?.remove(); return }
      if (!popupRef.current) {
        popupRef.current = new maplibregl.Popup({ closeButton: false, closeOnClick: false, maxWidth: '96vw', className: 'kap-tooltip landing-map-tooltip' })
      }
      popupRef.current.setLngLat(e.lngLat).setHTML(html).addTo(map)
    }
    const onLeave = () => popupRef.current?.remove()
    if (!map.getLayer('grid-fill')) return
    map.on('mousemove', 'grid-fill', onMove)
    map.on('mouseleave', 'grid-fill', onLeave)
    return () => {
      map.off('mousemove', 'grid-fill', onMove)
      map.off('mouseleave', 'grid-fill', onLeave)
      popupRef.current?.remove()
    }
  }, [loaded, tooltipForId, !!draw, data])

  // ── Maßnahme + Abdeckung spiegeln den Elternzustand ────────────────────
  useEffect(() => {
    const map = mapRef.current
    if (!map || !loaded || !map.getSource('covered')) return
    setSourceData(map, 'covered', coveredGeoJson(draw?.coveredIds ?? new Set()))
    setSourceData(map, 'measure', ringFeature(draw?.ring ?? null))
  }, [loaded, draw?.coveredIds, draw?.ring])

  // ── Zeichnen (Rechteck / Polygon) ──────────────────────────────────────
  useEffect(() => {
    const map = mapRef.current
    if (!map || !loaded || !draw) return
    popupRef.current?.remove()
    const shape = draw.shape
    map.getCanvas().style.cursor = 'crosshair'
    if (shape === 'rect') map.dragPan.disable()
    else map.doubleClickZoom.disable()

    const dropOld = () => { if (coveredIdsRef.current && coveredIdsRef.current.size > 0) onCoverageRef.current?.(new Set(), null) }
    const finalize = (ring: [number, number][]) => {
      setSourceData(map, 'drawing', EMPTY)
      setSourceData(map, 'drawing-vertices', EMPTY)
      onCoverageRef.current?.(coverIds(ring), ring)
    }

    const rectDown = (e: maplibregl.MapMouseEvent) => { dropOld(); rectStartRef.current = [e.lngLat.lng, e.lngLat.lat] }
    const rectMove = (e: maplibregl.MapMouseEvent) => {
      const s = rectStartRef.current
      if (!s) return
      setSourceData(map, 'drawing', ringFeature(rectRing(s, [e.lngLat.lng, e.lngLat.lat])))
    }
    const rectUp = (e: maplibregl.MapMouseEvent) => {
      const s = rectStartRef.current
      rectStartRef.current = null
      if (!s) return
      finalize(rectRing(s, [e.lngLat.lng, e.lngLat.lat]))
    }

    const renderPolygon = (cursor?: [number, number]) => {
      const pts = cursor && drawCoordsRef.current.length > 0 ? [...drawCoordsRef.current, cursor] : drawCoordsRef.current
      const geo: GeoJSON.GeoJSON = pts.length >= 3
        ? { type: 'Feature', properties: {}, geometry: { type: 'Polygon', coordinates: [[...pts, pts[0]]] } }
        : pts.length >= 2 ? { type: 'Feature', properties: {}, geometry: { type: 'LineString', coordinates: pts } } : EMPTY
      setSourceData(map, 'drawing', geo)
      setSourceData(map, 'drawing-vertices', {
        type: 'FeatureCollection',
        features: drawCoordsRef.current.map((c, i) => ({ type: 'Feature', properties: { index: i, isFirst: i === 0 }, geometry: { type: 'Point', coordinates: c } })),
      })
    }
    const polyClick = (e: maplibregl.MapMouseEvent) => {
      const pts = drawCoordsRef.current
      if (pts.length === 0) dropOld()
      if (pts.length >= 3) {
        const first = map.project(new maplibregl.LngLat(pts[0][0], pts[0][1]))
        const here = map.project(e.lngLat)
        if (Math.hypot(first.x - here.x, first.y - here.y) < SNAP_DIST) {
          const ring: [number, number][] = [...pts, pts[0]]
          drawCoordsRef.current = []
          finalize(ring)
          return
        }
      }
      drawCoordsRef.current = [...pts, [e.lngLat.lng, e.lngLat.lat]]
      renderPolygon()
    }
    const polyDbl = (e: maplibregl.MapMouseEvent) => {
      e.preventDefault()
      const pts = [...drawCoordsRef.current, [e.lngLat.lng, e.lngLat.lat] as [number, number]]
      drawCoordsRef.current = []
      if (pts.length >= 3) finalize([...pts, pts[0]])
    }
    const polyMove = (e: maplibregl.MapMouseEvent) => {
      if (drawCoordsRef.current.length === 0) return
      renderPolygon([e.lngLat.lng, e.lngLat.lat])
      const pts = drawCoordsRef.current
      if (pts.length >= 3) {
        const first = map.project(new maplibregl.LngLat(pts[0][0], pts[0][1]))
        const here = map.project(e.lngLat)
        map.getCanvas().style.cursor = Math.hypot(first.x - here.x, first.y - here.y) < SNAP_DIST ? 'pointer' : 'crosshair'
      }
    }

    if (shape === 'rect') { map.on('mousedown', rectDown); map.on('mousemove', rectMove); map.on('mouseup', rectUp) }
    else { map.on('click', polyClick); map.on('dblclick', polyDbl); map.on('mousemove', polyMove) }
    return () => {
      map.off('mousedown', rectDown); map.off('mousemove', rectMove); map.off('mouseup', rectUp)
      map.off('click', polyClick); map.off('dblclick', polyDbl); map.off('mousemove', polyMove)
      map.dragPan.enable(); map.doubleClickZoom.enable(); map.getCanvas().style.cursor = ''
      drawCoordsRef.current = []; rectStartRef.current = null
      setSourceData(map, 'drawing', EMPTY); setSourceData(map, 'drawing-vertices', EMPTY)
    }
  }, [loaded, draw?.shape, !!draw])

  return (
    <div className="landing-map-wrap">
      <div ref={container} className="landing-map" role="img" aria-label={ariaLabel} />
      {legend && (
        <div className="map-legend landing-map-legend">
          <div style={{ fontWeight: 600, marginBottom: 4 }}>{legend.label}</div>
          <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: 4 }}>{legend.unit}</div>
          <div style={{ display: 'flex', height: 10, borderRadius: 3, overflow: 'hidden' }}>
            {CHOROPLETH_COLORS.map((c) => <div key={c} style={{ flex: 1, background: c }} />)}
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.7rem', marginTop: 2 }}>
            <span>{fmtLegend(scale.lo)}</span>
            <span>{fmtLegend(scale.hi)}</span>
          </div>
        </div>
      )}
    </div>
  )
}
