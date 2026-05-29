import { useEffect, useRef, useState, useCallback, useMemo } from 'react'
import maplibregl from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
import { useStore } from '../store'
import { CLIMATE_TYPE_META } from '../types'
import type { GeoJSONFeature } from '../types'

export default function MapView() {
  const mapContainer = useRef<HTMLDivElement>(null)
  const mapRef = useRef<maplibregl.Map | null>(null)
  const popupRef = useRef<maplibregl.Popup | null>(null)
  const {
    kommune, assessmentGeoJson, measures, isDrawing, setIsDrawing,
    setDrawnGeometry, setSelectedMeasure, drawnGeometry,
    riskZonesGeoJson, activeClimateType, loadRiskZones,
    assessmentsByType, loadAllAssessments, statuses,
  } = useStore()

  const [mapLoaded, setMapLoaded] = useState(false)
  const [drawMode, setDrawMode] = useState(false)
  const [drawCoords, setDrawCoords] = useState<[number, number][]>([])
  const [cursorCoord, setCursorCoord] = useState<[number, number] | null>(null)
  const [showMeasureForm, setShowMeasureForm] = useState(false)
  const [layerVisibility, setLayerVisibility] = useState<Record<string, boolean>>(() => {
    const init: Record<string, boolean> = {
      'measures-fill': true,
      'measures-line': true,
      'risk-zones-fill': false,
      'risk-zones-line': false,
    }
    // Per-type assessment layers: active type visible, rest hidden
    for (const ct of Object.keys(CLIMATE_TYPE_META)) {
      init[`assessment-${ct}-fill`] = ct === 'heat'
      init[`assessment-${ct}-line`] = ct === 'heat'
    }
    return init
  })

  const toggleLayer = useCallback((layerId: string) => {
    setLayerVisibility(prev => {
      const next = { ...prev, [layerId]: !prev[layerId] }
      const map = mapRef.current
      if (map && map.getLayer(layerId)) {
        map.setLayoutProperty(layerId, 'visibility', next[layerId] ? 'visible' : 'none')
      }
      // For paired layers (fill+line), toggle both
      const pair = layerId.endsWith('-fill')
        ? layerId.replace('-fill', '-line')
        : layerId.endsWith('-line') ? layerId.replace('-line', '-fill') : null
      if (pair && map && map.getLayer(pair)) {
        next[pair] = next[layerId]
        map.setLayoutProperty(pair, 'visibility', next[layerId] ? 'visible' : 'none')
      }
      return next
    })
  }, [])

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
        layers: [{
          id: 'osm',
          type: 'raster',
          source: 'osm',
        }],
      },
      center: [10.4515, 51.1657], // Germany center
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
      const src = map.getSource('kommune-boundary') as maplibregl.GeoJSONSource
      const geojson: GeoJSON.GeoJSON = {
        type: 'Feature',
        properties: {},
        geometry: kommune.boundary_geojson as unknown as GeoJSON.Geometry,
      }

      if (src) {
        src.setData(geojson)
      } else {
        map.addSource('kommune-boundary', { type: 'geojson', data: geojson })
        map.addLayer({
          id: 'kommune-boundary-line',
          type: 'line',
          source: 'kommune-boundary',
          paint: { 'line-color': '#2563eb', 'line-width': 2.5, 'line-dasharray': [3, 2] },
        })
      }

      // Fit bounds
      const coords = kommune.boundary_geojson.coordinates as number[][][][]
      let minLng = Infinity, maxLng = -Infinity, minLat = Infinity, maxLat = -Infinity
      for (const poly of coords) {
        for (const ring of poly) {
          for (const [lng, lat] of ring) {
            if (lng < minLng) minLng = lng
            if (lng > maxLng) maxLng = lng
            if (lat < minLat) minLat = lat
            if (lat > maxLat) maxLat = lat
          }
        }
      }
      map.fitBounds([[minLng, minLat], [maxLng, maxLat]], { padding: 40 })
    } catch (err) {
      console.warn('MapView: boundary layer error', err)
    }
  }, [kommune, mapLoaded])

  // Multi-risk popup: query all visible per-type layers at mouse position
  useEffect(() => {
    const map = mapRef.current
    if (!map || !mapLoaded) return

    const handleMouseMove = (e: maplibregl.MapMouseEvent) => {
      if (!map) return
      // Collect all visible assessment-{ct}-fill layers
      const visibleLayers: string[] = []
      for (const ct of Object.keys(CLIMATE_TYPE_META)) {
        const layerId = `assessment-${ct}-fill`
        if (map.getLayer(layerId) && map.getLayoutProperty(layerId, 'visibility') !== 'none') {
          visibleLayers.push(layerId)
        }
      }
      if (visibleLayers.length === 0) {
        popupRef.current?.remove()
        return
      }

      const features = map.queryRenderedFeatures(e.point, { layers: visibleLayers })
      if (!features.length) {
        popupRef.current?.remove()
        return
      }

      // Build multi-risk popup
      const lines: string[] = []
      const seen = new Set<string>()
      for (const f of features) {
        // Determine climate type from layer id
        const layerId = f.layer?.id || ''
        const ctMatch = layerId.match(/^assessment-(.+)-fill$/)
        if (!ctMatch) continue
        const ct = ctMatch[1]
        if (seen.has(ct)) continue
        seen.add(ct)
        const meta = CLIMATE_TYPE_META[ct]
        if (!meta) continue
        const props = f.properties || {}
        const rs = props.risk_score
        if (rs != null) {
          lines.push(`${meta.icon} <strong>${meta.label}:</strong> ${Number(rs).toFixed(1)}/10`)
        }
      }
      // Also show detail props from the first feature
      const firstProps = features[0].properties || {}
      if (firstProps.temperature_estimate != null)
        lines.push(`<span style="color:#999">Temperatur: ${firstProps.temperature_estimate}°C</span>`)
      if (firstProps.impervious_fraction != null)
        lines.push(`<span style="color:#999">Versiegelung: ${(firstProps.impervious_fraction * 100).toFixed(0)}%</span>`)

      if (lines.length === 0) return

      if (!popupRef.current) {
        popupRef.current = new maplibregl.Popup({ closeButton: false, closeOnClick: false })
      }
      popupRef.current.setLngLat(e.lngLat).setHTML(lines.join('<br/>')).addTo(map)
    }

    const handleMouseLeave = () => {
      popupRef.current?.remove()
    }

    map.on('mousemove', handleMouseMove)
    // Remove popup when mouse leaves the map
    map.getCanvas().addEventListener('mouseleave', handleMouseLeave)

    return () => {
      map.off('mousemove', handleMouseMove)
      map.getCanvas().removeEventListener('mouseleave', handleMouseLeave)
    }
  }, [mapLoaded, assessmentsByType])

  // Measures layer
  useEffect(() => {
    const map = mapRef.current
    if (!map || !mapLoaded) return

    try {
      const features = measures
        .filter(m => m.geometry_geojson)
        .map(m => ({
          type: 'Feature' as const,
          properties: { id: m.id, name: m.name, type: m.measure_type },
          geometry: m.geometry_geojson as unknown as GeoJSON.Geometry,
        }))

      const geojson: GeoJSON.GeoJSON = { type: 'FeatureCollection', features }

      const src = map.getSource('measures') as maplibregl.GeoJSONSource
      if (src) {
        src.setData(geojson)
      } else {
        map.addSource('measures', { type: 'geojson', data: geojson })
        map.addLayer({
          id: 'measures-fill',
          type: 'fill',
          source: 'measures',
          paint: { 'fill-color': '#7c3aed', 'fill-opacity': 0.3 },
        })
        map.addLayer({
          id: 'measures-line',
          type: 'line',
          source: 'measures',
          paint: { 'line-color': '#7c3aed', 'line-width': 2 },
        })

        map.on('click', 'measures-fill', (e) => {
          if (!e.features?.[0]) return
          const id = e.features[0].properties?.id
          const measure = useStore.getState().measures.find(m => m.id === id)
          if (measure) setSelectedMeasure(measure)
        })
      }
    } catch (err) {
      console.warn('MapView: measures layer error', err)
    }
  }, [measures, mapLoaded])

  // Risk zones layer
  useEffect(() => {
    const map = mapRef.current
    if (!map || !mapLoaded) return

    try {
      const geojson: GeoJSON.GeoJSON = riskZonesGeoJson
        ? (riskZonesGeoJson as GeoJSON.GeoJSON)
        : { type: 'FeatureCollection', features: [] }

      const src = map.getSource('risk-zones') as maplibregl.GeoJSONSource
      if (src) {
        src.setData(geojson)
      } else {
        map.addSource('risk-zones', { type: 'geojson', data: geojson })
        map.addLayer({
          id: 'risk-zones-fill',
          type: 'fill',
          source: 'risk-zones',
          layout: { visibility: layerVisibility['risk-zones-fill'] ? 'visible' : 'none' },
          paint: {
            'fill-color': [
              'interpolate', ['linear'], ['get', 'mean_risk'],
              3, '#fbbf24',
              5, '#f97316',
              7, '#ef4444',
              9, '#991b1b',
            ],
            'fill-opacity': 0.45,
          },
        })
        map.addLayer({
          id: 'risk-zones-line',
          type: 'line',
          source: 'risk-zones',
          layout: { visibility: layerVisibility['risk-zones-line'] ? 'visible' : 'none' },
          paint: { 'line-color': '#dc2626', 'line-width': 2, 'line-dasharray': [4, 2] },
        })

        // Risk zone tooltip — shows zone info + dominant risk types
        map.on('mousemove', 'risk-zones-fill', (e) => {
          if (!e.features?.[0]) return
          const p = e.features[0].properties
          if (!p) return
          const ct = p.climate_type
          const meta = ct ? CLIMATE_TYPE_META[ct] : null
          const typeLabel = meta ? `${meta.icon} ${meta.label}` : (ct || '')
          const lines = [
            `<strong>Risikogebiet #${p.zone_index}</strong>${typeLabel ? ` (${typeLabel})` : ''}`,
            `Ø Risiko: ${Number(p.mean_risk).toFixed(1)}/10`,
            `Max: ${Number(p.max_risk).toFixed(1)}/10`,
            `Zellen: ${p.cell_count}`,
            `Fläche: ${(p.area_m2 / 10000).toFixed(1)} ha`,
          ]

          // Query per-type layers at this point to show dominant risks
          const map_ = mapRef.current
          if (map_) {
            const riskEntries: { label: string; score: number }[] = []
            for (const [rct, rmeta] of Object.entries(CLIMATE_TYPE_META)) {
              const lid = `assessment-${rct}-fill`
              if (!map_.getLayer(lid)) continue
              const feats = map_.queryRenderedFeatures(e.point, { layers: [lid] })
              if (feats.length && feats[0].properties?.risk_score != null) {
                riskEntries.push({ label: `${rmeta.icon} ${rmeta.label}`, score: Number(feats[0].properties.risk_score) })
              }
            }
            if (riskEntries.length > 0) {
              riskEntries.sort((a, b) => b.score - a.score)
              lines.push('<hr style="margin:4px 0;border-color:#555">')
              lines.push('<strong>Risiken an dieser Stelle:</strong>')
              for (const re of riskEntries) {
                lines.push(`${re.label}: ${re.score.toFixed(1)}/10`)
              }
            }
          }

          if (!popupRef.current) {
            popupRef.current = new maplibregl.Popup({ closeButton: false, closeOnClick: false })
          }
          popupRef.current.setLngLat(e.lngLat).setHTML(lines.join('<br/>')).addTo(map)
        })
        map.on('mouseleave', 'risk-zones-fill', () => {
          popupRef.current?.remove()
        })
      }
    } catch (err) {
      console.warn('MapView: risk zones layer error', err)
    }
  }, [riskZonesGeoJson, mapLoaded])

  // Per-type assessment layers
  useEffect(() => {
    const map = mapRef.current
    if (!map || !mapLoaded) return

    for (const [ct, geojson] of Object.entries(assessmentsByType)) {
      const sourceId = `assessment-${ct}`
      const fillId = `${sourceId}-fill`
      const lineId = `${sourceId}-line`
      const meta = CLIMATE_TYPE_META[ct]
      if (!meta || !geojson) continue

      const data: GeoJSON.GeoJSON = {
        type: 'FeatureCollection',
        features: (geojson.features || []).map(f => ({
          type: 'Feature' as const,
          properties: f.properties || {},
          geometry: f.geometry as unknown as GeoJSON.Geometry,
        })),
      }

      try {
        const src = map.getSource(sourceId) as maplibregl.GeoJSONSource
        if (src) {
          src.setData(data)
        } else {
          map.addSource(sourceId, { type: 'geojson', data })
          map.addLayer({
            id: fillId,
            type: 'fill',
            source: sourceId,
            layout: { visibility: layerVisibility[fillId] ? 'visible' : 'none' },
            paint: {
              'fill-color': meta.color,
              'fill-opacity': [
                'interpolate', ['linear'], ['coalesce', ['get', 'risk_score'], 0],
                0, 0.05,
                3, 0.2,
                5, 0.35,
                8, 0.55,
                10, 0.7,
              ],
            },
          })
          map.addLayer({
            id: lineId,
            type: 'line',
            source: sourceId,
            layout: { visibility: layerVisibility[lineId] ? 'visible' : 'none' },
            paint: { 'line-color': meta.color, 'line-width': 0.3, 'line-opacity': 0.5 },
          })
        }
      } catch (err) {
        console.warn(`MapView: ${ct} layer error`, err)
      }
    }
  }, [assessmentsByType, mapLoaded])

  // When activeClimateType changes, show that type's layer (hide others if not explicitly toggled)
  useEffect(() => {
    const map = mapRef.current
    if (!map || !mapLoaded) return
    // Auto-show the active climate type's per-type layer
    const fillId = `assessment-${activeClimateType}-fill`
    const lineId = `assessment-${activeClimateType}-line`
    setLayerVisibility(prev => {
      const next = { ...prev }
      next[fillId] = true
      next[lineId] = true
      if (map.getLayer(fillId)) map.setLayoutProperty(fillId, 'visibility', 'visible')
      if (map.getLayer(lineId)) map.setLayoutProperty(lineId, 'visibility', 'visible')
      return next
    })
  }, [activeClimateType, mapLoaded])

  // Load all assessments and risk zones when kommune changes
  useEffect(() => {
    if (!kommune) return
    loadRiskZones(kommune.id, activeClimateType).catch(() => {})
    loadAllAssessments(kommune.id).catch(() => {})
  }, [kommune, activeClimateType])

  // Drawing polygon + vertices + cursor line
  useEffect(() => {
    const map = mapRef.current
    if (!map || !mapLoaded) return

    try {
      // Build polygon/line geometry from confirmed coords
      const allCoords = cursorCoord && drawCoords.length > 0
        ? [...drawCoords, cursorCoord]
        : drawCoords

      const geojson: GeoJSON.GeoJSON = allCoords.length >= 3
        ? {
            type: 'Feature' as const,
            properties: {},
            geometry: {
              type: 'Polygon' as const,
              coordinates: [[...allCoords, allCoords[0]]],
            },
          }
        : allCoords.length >= 2
          ? {
              type: 'Feature' as const,
              properties: {},
              geometry: {
                type: 'LineString' as const,
                coordinates: allCoords,
              },
            }
          : { type: 'FeatureCollection' as const, features: [] }

      const src = map.getSource('drawing') as maplibregl.GeoJSONSource
      if (src) {
        src.setData(geojson)
      } else {
        map.addSource('drawing', { type: 'geojson', data: geojson })
        map.addLayer({
          id: 'drawing-fill',
          type: 'fill',
          source: 'drawing',
          paint: { 'fill-color': '#ec4899', 'fill-opacity': 0.25 },
        })
        map.addLayer({
          id: 'drawing-line',
          type: 'line',
          source: 'drawing',
          paint: { 'line-color': '#ec4899', 'line-width': 2 },
        })
      }

      // Vertex markers
      const vertexGeojson: GeoJSON.GeoJSON = {
        type: 'FeatureCollection',
        features: drawCoords.map((c, i) => ({
          type: 'Feature' as const,
          properties: { index: i, isFirst: i === 0 },
          geometry: { type: 'Point' as const, coordinates: c },
        })),
      }
      const vertexSrc = map.getSource('drawing-vertices') as maplibregl.GeoJSONSource
      if (vertexSrc) {
        vertexSrc.setData(vertexGeojson)
      } else {
        map.addSource('drawing-vertices', { type: 'geojson', data: vertexGeojson })
        map.addLayer({
          id: 'drawing-vertices-circle',
          type: 'circle',
          source: 'drawing-vertices',
          paint: {
            'circle-radius': ['case', ['get', 'isFirst'], 7, 5],
            'circle-color': ['case', ['get', 'isFirst'], '#22c55e', '#ec4899'],
            'circle-stroke-width': 2,
            'circle-stroke-color': '#fff',
          },
        })
      }
    } catch (err) {
      console.warn('MapView: drawing layer error', err)
    }
  }, [drawCoords, cursorCoord])

  // Handle map clicks for drawing + mousemove for cursor line
  useEffect(() => {
    const map = mapRef.current
    if (!map || !mapLoaded) return

    const SNAP_DIST = 15 // px distance to snap to first point

    const handleClick = (e: maplibregl.MapMouseEvent) => {
      if (!drawMode) return
      const coord: [number, number] = [e.lngLat.lng, e.lngLat.lat]

      // Check if clicking near the first vertex to close the polygon
      setDrawCoords(prev => {
        if (prev.length >= 3) {
          const firstPt = map.project(new maplibregl.LngLat(prev[0][0], prev[0][1]))
          const clickPt = map.project(e.lngLat)
          const dist = Math.sqrt((firstPt.x - clickPt.x) ** 2 + (firstPt.y - clickPt.y) ** 2)
          if (dist < SNAP_DIST) {
            // Close the polygon
            const polygon = {
              type: 'Polygon',
              coordinates: [[...prev, prev[0]]],
            }
            setDrawnGeometry(polygon)
            setShowMeasureForm(true)
            setDrawMode(false)
            setCursorCoord(null)
            setIsDrawing(false)
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
          const polygon = {
            type: 'Polygon',
            coordinates: [[...coords, coords[0]]],
          }
          setDrawnGeometry(polygon)
          setShowMeasureForm(true)
        }
        setDrawMode(false)
        setCursorCoord(null)
        setIsDrawing(false)
        if (mapRef.current) mapRef.current.doubleClickZoom.enable()
        return []
      })
    }

    const handleMouseMove = (e: maplibregl.MapMouseEvent) => {
      if (!drawMode) return
      setCursorCoord([e.lngLat.lng, e.lngLat.lat])

      // Change cursor when near first point
      setDrawCoords(prev => {
        if (prev.length >= 3) {
          const firstPt = map.project(new maplibregl.LngLat(prev[0][0], prev[0][1]))
          const movePt = map.project(e.lngLat)
          const dist = Math.sqrt((firstPt.x - movePt.x) ** 2 + (firstPt.y - movePt.y) ** 2)
          map.getCanvas().style.cursor = dist < SNAP_DIST ? 'pointer' : 'crosshair'
        } else {
          map.getCanvas().style.cursor = 'crosshair'
        }
        return prev // don't change drawCoords
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
    setDrawMode(true)
    setDrawCoords([])
    setIsDrawing(true)
    setDrawnGeometry(null)
    if (mapRef.current) mapRef.current.doubleClickZoom.disable()
  }

  const cancelDraw = () => {
    setDrawMode(false)
    setDrawCoords([])
    setCursorCoord(null)
    setIsDrawing(false)
    setDrawnGeometry(null)
    if (mapRef.current) {
      mapRef.current.doubleClickZoom.enable()
      mapRef.current.getCanvas().style.cursor = ''
    }
  }

  return (
    <>
      <div ref={mapContainer} style={{ width: '100%', height: '100%' }} />

      {/* Draw toolbar */}
      <div className="draw-toolbar">
        {!drawMode ? (
          <button onClick={startDraw} title="Maßnahme einzeichnen">
            ✏️ Maßnahme zeichnen
          </button>
        ) : (
          <>
            <button className="active">Ecken klicken · grünen Startpunkt klicken zum Schließen</button>
            <button onClick={cancelDraw}>✕ Abbrechen</button>
          </>
        )}
      </div>

      {/* Layer toggle controls */}
      <div className="layer-control">
        <div className="layer-control-title">Layer</div>
        <label>
          <input
            type="checkbox"
            checked={layerVisibility['risk-zones-fill'] === true}
            onChange={() => toggleLayer('risk-zones-fill')}
          />
          🔴 Risikogebiete
        </label>
        <label>
          <input
            type="checkbox"
            checked={layerVisibility['measures-fill'] !== false}
            onChange={() => toggleLayer('measures-fill')}
          />
          Maßnahmen
        </label>
        <div style={{ borderTop: '1px solid var(--border)', marginTop: 6, paddingTop: 6 }}>
          <div className="layer-control-title">Klimatypen</div>
          {Object.entries(CLIMATE_TYPE_META).map(([ct, meta]) => {
            const hasData = !!assessmentsByType[ct]?.features?.length
            return (
              <label key={ct} style={{ opacity: hasData ? 1 : 0.5 }}>
                <input
                  type="checkbox"
                  checked={layerVisibility[`assessment-${ct}-fill`] === true}
                  onChange={() => toggleLayer(`assessment-${ct}-fill`)}
                  disabled={!hasData}
                />
                <span style={{ color: meta.color, marginRight: 2 }}>●</span>
                {meta.icon} {meta.label}
              </label>
            )
          })}
        </div>
      </div>

      {/* Color Legend — risk score 0-10 */}
      {Object.values(assessmentsByType).some(g => g?.features?.length > 0) && (
        <div className="map-legend">
          <div style={{ fontWeight: 600, marginBottom: 4 }}>
            Risiko-Score (0–10)
          </div>
          <div style={{ display: 'flex', gap: 2, marginBottom: 2 }}>
            {Object.entries(CLIMATE_TYPE_META).map(([ct, meta]) => {
              const active = layerVisibility[`assessment-${ct}-fill`]
              const hasData = !!assessmentsByType[ct]?.features?.length
              if (!hasData) return null
              return (
                <span key={ct} style={{ opacity: active ? 1 : 0.4, fontSize: '0.75rem' }} title={meta.label}>
                  <span style={{ color: meta.color }}>●</span>
                </span>
              )
            })}
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.7rem' }}>
            <span>0</span>
            <span>2.5</span>
            <span>5</span>
            <span>7.5</span>
            <span>10</span>
          </div>
          <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginTop: 2 }}>
            Transparenz = Risikohöhe
          </div>
        </div>
      )}

      {/* Measure creation form (modal) */}
      {showMeasureForm && <MeasureCreateModal onClose={() => setShowMeasureForm(false)} />}
    </>
  )
}

// ── Measure creation modal ──────────────────────────────────────────────────

function MeasureCreateModal({ onClose }: { onClose: () => void }) {
  const { kommune, drawnGeometry, measures, createMeasure, calculateImpact, setSelectedMeasure } = useStore()
  const [measureType, setMeasureType] = useState('tree_planting')
  const [config, setConfig] = useState<Record<string, number>>({})
  const [implYear, setImplYear] = useState(2026)
  const [saving, setSaving] = useState(false)

  const measureTypes: Record<string, { label: string; params: { key: string; label: string; default: number; unit?: string }[] }> = {
    drinking_fountain: { label: 'Trinkbrunnen', params: [{ key: 'count', label: 'Anzahl', default: 5 }] },
    green_roof: { label: 'Dachbegrünung', params: [{ key: 'coverage_pct', label: 'Abdeckung', default: 60, unit: '%' }] },
    facade_greening: { label: 'Fassadenbegrünung', params: [{ key: 'coverage_pct', label: 'Abdeckung', default: 30, unit: '%' }] },
    tree_planting: { label: 'Baumpflanzung', params: [{ key: 'count', label: 'Anzahl Bäume', default: 20 }, { key: 'shade_factor', label: 'Schattenfaktor', default: 0.03 }] },
    unsealing: { label: 'Entsiegelung', params: [{ key: 'area_pct', label: 'Flächenanteil', default: 50, unit: '%' }] },
    shade_structure: { label: 'Verschattung', params: [{ key: 'coverage_pct', label: 'Abdeckung', default: 30, unit: '%' }] },
  }

  // Compute polygon area in m²
  const polyArea = useMemo(() => {
    if (!drawnGeometry) return 0
    const coords = (drawnGeometry as { coordinates: number[][][] }).coordinates?.[0]
    if (!coords || coords.length < 3) return 0
    // Approximate area using Shoelace formula on projected coords
    const R = 6371000 // Earth radius in meters
    const toRad = (d: number) => d * Math.PI / 180
    const refLat = coords[0][1]
    const points = coords.map(c => [
      R * toRad(c[0] - coords[0][0]) * Math.cos(toRad(refLat)),
      R * toRad(c[1] - coords[0][1])
    ])
    let area = 0
    for (let i = 0; i < points.length - 1; i++) {
      area += points[i][0] * points[i + 1][1] - points[i + 1][0] * points[i][1]
    }
    return Math.abs(area / 2)
  }, [drawnGeometry])

  const polyAreaHa = polyArea / 10000

  // Auto-generate descriptive name
  const autoName = useMemo(() => {
    const label = measureTypes[measureType]?.label || measureType
    const existing = measures.filter(m => m.measure_type === measureType).length
    const num = existing + 1
    const areaStr = polyAreaHa >= 1 ? `${polyAreaHa.toFixed(1)} ha` : `${Math.round(polyArea)} m²`
    return `${label} #${num} (${areaStr})`
  }, [measureType, measures, polyArea])

  const [name, setName] = useState(autoName)

  // Update auto-name when type changes
  useEffect(() => {
    setName(autoName)
  }, [autoName])

  const currentType = measureTypes[measureType]

  const handleSave = async () => {
    if (!kommune || !drawnGeometry) return
    setSaving(true)
    try {
      const finalConfig: Record<string, number> = {}
      for (const p of currentType.params) {
        finalConfig[p.key] = config[p.key] ?? p.default
      }

      const measure = await createMeasure(kommune.id, {
        name: name || autoName,
        measure_type: measureType,
        geometry_geojson: drawnGeometry,
        config: finalConfig,
        implementation_year: implYear,
      })

      // Auto-calculate impact
      await calculateImpact(measure.id)
      setSelectedMeasure(measure)
      onClose()
    } catch (e) {
      console.error('Failed to create measure:', e)
    } finally {
      setSaving(false)
    }
  }

  // Per-hectare info for tree planting
  const treesPerHa = measureType === 'tree_planting' && polyAreaHa > 0
    ? Math.round((config.count ?? currentType.params[0].default) / polyAreaHa)
    : null

  return (
    <div style={{
      position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)',
      background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 12,
      padding: '1.5rem', width: 400, zIndex: 100, boxShadow: '0 8px 32px rgba(0,0,0,0.2)',
    }}>
      <h3 style={{ marginBottom: '0.5rem', fontSize: '1rem' }}>Neue Anpassungsmaßnahme</h3>

      {/* Polygon area info */}
      {polyArea > 0 && (
        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.75rem' }}>
          Fläche: {polyAreaHa >= 1 ? `${polyAreaHa.toFixed(2)} ha` : `${Math.round(polyArea)} m²`}
        </div>
      )}

      <div className="form-group">
        <label>Maßnahmentyp</label>
        <select value={measureType} onChange={e => { setMeasureType(e.target.value); setConfig({}) }}>
          {Object.entries(measureTypes).map(([key, val]) => (
            <option key={key} value={key}>{val.label}</option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label>Name</label>
        <input value={name} onChange={e => setName(e.target.value)} placeholder={autoName} />
      </div>

      {currentType.params.map(p => (
        <div className="form-group" key={p.key}>
          <label>{p.label}{p.unit ? ` (${p.unit})` : ''}</label>
          <input
            type="number"
            value={config[p.key] ?? p.default}
            onChange={e => setConfig({ ...config, [p.key]: parseFloat(e.target.value) || 0 })}
          />
          {/* Per-hectare info for tree count */}
          {p.key === 'count' && treesPerHa != null && (
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: 2 }}>
              ≈ {treesPerHa} Bäume/ha
            </div>
          )}
        </div>
      ))}

      <div className="form-group">
        <label>Umsetzungsjahr</label>
        <input type="number" value={implYear} onChange={e => setImplYear(parseInt(e.target.value) || 2026)} />
      </div>

      <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem' }}>
        <button className="btn btn-primary" onClick={handleSave} disabled={saving}>
          {saving ? 'Speichern...' : 'Anlegen & Berechnen'}
        </button>
        <button className="btn btn-secondary" onClick={onClose}>Abbrechen</button>
      </div>
    </div>
  )
}
