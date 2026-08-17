import { useEffect, useRef, useState } from 'react'
import maplibregl from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
import { api } from '../../api/client'
import { useLiteStore, adjustedIndex } from '../../store/liteStore'

type FC = GeoJSON.FeatureCollection

/**
 * Deutschland-Choropleth je Gemeinde. GeoJSON-Fallback (kein tippecanoe/PMTiles):
 * lädt die vereinfachten Bundesland-GeoJSONs, färbt via feature-state nach dem
 * gewählten Risiko-Index. Risikowechsel/Maßnahmen = reine Recolor-Schleife.
 */
export default function LiteMap() {
  const mapContainer = useRef<HTMLDivElement>(null)
  const mapRef = useRef<maplibregl.Map | null>(null)
  const [ready, setReady] = useState(false)
  const agsListRef = useRef<string[]>([])

  const { meta, values, selectedRisk, measureLevels, selectGemeinde, selectedAgs } = useLiteStore()

  // Karte einmal aufsetzen + GeoJSON laden.
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
      zoom: 5.4,
    })
    map.addControl(new maplibregl.NavigationControl(), 'top-right')
    mapRef.current = map

    map.on('load', async () => {
      const colors = meta?.choropleth_colors ?? ['#fef9c3', '#fde047', '#fb923c', '#ef4444', '#991b1b']
      try {
        const index = await api.lite.geojsonIndex()
        const parts = await Promise.all(
          Object.values(index).map((v) => fetch(api.lite.geojsonUrl(v.slug)).then((r) => r.json() as Promise<FC>)),
        )
        const features = parts.flatMap((fc) => fc.features)
        agsListRef.current = features.map((f) => String((f.properties as { ags: string }).ags))
        map.addSource('gemeinden', {
          type: 'geojson',
          data: { type: 'FeatureCollection', features },
        })
        map.addLayer({
          id: 'gem-fill', type: 'fill', source: 'gemeinden',
          paint: {
            'fill-color': [
              'interpolate', ['linear'], ['coalesce', ['feature-state', 'v'], 0],
              0, colors[0], 25, colors[1], 50, colors[2], 75, colors[3], 100, colors[4],
            ],
            'fill-opacity': 0.75,
          },
        })
        map.addLayer({
          id: 'gem-line', type: 'line', source: 'gemeinden',
          paint: { 'line-color': '#ffffff', 'line-width': 0.4 },
        })
        map.addLayer({
          id: 'gem-sel', type: 'line', source: 'gemeinden',
          paint: { 'line-color': '#1d4ed8', 'line-width': 2.5 },
          filter: ['==', ['get', 'ags'], ''],
        })
        setReady(true)
      } catch {
        /* Karte noch nicht berechnet — Panel zeigt Hinweis. */
      }
    })

    map.on('click', 'gem-fill', (e) => {
      const f = e.features?.[0]
      if (f) selectGemeinde(String((f.properties as { ags: string }).ags))
    })
    map.on('mouseenter', 'gem-fill', () => { map.getCanvas().style.cursor = 'pointer' })
    map.on('mouseleave', 'gem-fill', () => { map.getCanvas().style.cursor = '' })

    return () => { map.remove(); mapRef.current = null }
  }, [meta])

  // Recolor bei Risiko-/Maßnahmen-Wechsel (setFeatureState je Gemeinde).
  useEffect(() => {
    const map = mapRef.current
    if (!ready || !map || !values || !selectedRisk) return
    for (const ags of agsListRef.current) {
      const base = values[ags]?.[selectedRisk] ?? 0
      const v = adjustedIndex(base, selectedRisk, measureLevels)
      map.setFeatureState({ source: 'gemeinden', id: Number(ags) }, { v })
    }
  }, [ready, values, selectedRisk, measureLevels])

  // Ausgewählte Gemeinde hervorheben.
  useEffect(() => {
    const map = mapRef.current
    if (!ready || !map) return
    map.setFilter('gem-sel', ['==', ['get', 'ags'], selectedAgs ?? ''])
  }, [ready, selectedAgs])

  return <div ref={mapContainer} className="lite-map" />
}
