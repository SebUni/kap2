import { useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import { useLiteStore } from '../../store/liteStore'
import LiteMap from './LiteMap'
import LitePanel from './LitePanel'

/**
 * Öffentliche Deutschland-Karte: Panel links (Risikoauswahl, Gemeinde-Info,
 * Maßnahmen-Slider), MapLibre-Choropleth rechts. Deep-Link ``?ags=…`` aus den
 * SEO-Seiten wählt direkt eine Gemeinde.
 */
export default function LiteMapPage() {
  const { bootstrap, selectGemeinde, meta } = useLiteStore()
  const [params] = useSearchParams()

  useEffect(() => { bootstrap() }, [bootstrap])

  // Deep-Link: ?ags=… nach dem Laden der Metadaten auflösen.
  useEffect(() => {
    const ags = params.get('ags')
    if (ags && meta) selectGemeinde(ags)
  }, [params, meta, selectGemeinde])

  return (
    <div className="lite-page">
      <LitePanel />
      <LiteMap />
    </div>
  )
}
