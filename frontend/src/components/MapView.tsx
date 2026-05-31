import { useEffect, useRef, useState, useMemo } from 'react'
import maplibregl from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
import { useStore } from '../store'
import type { LayerMeta } from '../types'

const CHOROPLETH_COLORS = ['#fef9c3', '#fde047', '#fb923c', '#ef4444', '#991b1b']

export default function MapView() {
  const mapContainer = useRef<HTMLDivElement>(null)
  const mapRef = useRef<maplibregl.Map | null>(null)
  const popupRef = useRef<maplibregl.Popup | null>(null)
  const {
    kommune, measures, layerGeoJson, showMeasures,
    setIsDrawing, setDrawnGeometry, setSelectedMeasure, drawnGeometry,
  } = useStore()

  const [mapLoaded, setMapLoaded] = useState(false)
  const [drawMode, setDrawMode] = useState(false)
  const [drawCoords, setDrawCoords] = useState<[number, number][]>([])
  const [cursorCoord, setCursorCoord] = useState<[number, number] | null>(null)
  const [showMeasureForm, setShowMeasureForm] = useState(false)

  const meta = layerGeoJson?.meta as LayerMeta | undefined

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

    const lo = meta?.min ?? 0
    const hi = meta?.scale_max && meta.scale_max > lo ? meta.scale_max : (meta?.max && meta.max > lo ? meta.max : lo + 1)
    const stops = CHOROPLETH_COLORS.map((c, i) => [lo + (hi - lo) * (i / (CHOROPLETH_COLORS.length - 1)), c]).flat()

    try {
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

        map.on('mousemove', 'active-layer-fill', (e) => {
          if (!e.features?.[0]) return
          const v = e.features[0].properties?.value
          const m = useStore.getState().layerGeoJson?.meta as LayerMeta | undefined
          if (v == null || !m) return
          if (!popupRef.current) popupRef.current = new maplibregl.Popup({ closeButton: false, closeOnClick: false })
          popupRef.current
            .setLngLat(e.lngLat)
            .setHTML(`<strong>${m.label}</strong><br/>${Number(v).toLocaleString('de-DE', { maximumFractionDigits: 2 })} ${m.unit}`)
            .addTo(map)
        })
        map.on('mouseleave', 'active-layer-fill', () => popupRef.current?.remove())
      }
    } catch (err) { console.warn('MapView: active layer error', err) }
  }, [layerGeoJson, mapLoaded])

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

  return (
    <>
      <div ref={mapContainer} style={{ width: '100%', height: '100%' }} />

      <div className="draw-toolbar">
        {!drawMode ? (
          <button onClick={startDraw} title="Maßnahme einzeichnen">✏️ Maßnahme zeichnen</button>
        ) : (
          <>
            <button className="active">Ecken klicken · grünen Startpunkt klicken zum Schließen</button>
            <button onClick={cancelDraw}>✕ Abbrechen</button>
          </>
        )}
      </div>

      {/* Legend for active layer */}
      {meta && layerGeoJson?.features && layerGeoJson.features.length > 0 && (
        <div className="map-legend">
          <div style={{ fontWeight: 600, marginBottom: 4 }}>{meta.label}</div>
          <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: 4 }}>{meta.unit}</div>
          <div style={{ display: 'flex', height: 10, borderRadius: 3, overflow: 'hidden' }}>
            {CHOROPLETH_COLORS.map(c => <div key={c} style={{ flex: 1, background: c }} />)}
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.7rem', marginTop: 2 }}>
            <span>{fmt(meta.min)}</span>
            <span>{fmt(meta.scale_max && meta.scale_max > meta.min ? meta.scale_max : meta.max)}</span>
          </div>
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
        config: {},
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
