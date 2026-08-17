/**
 * Ausrichtung des INSPIRE-100m-Rasters (EPSG:3035, ETRS89-LAEA) auf einer
 * Web-Mercator-Karte: Die Zellen sind in LAEA achsparallel, erscheinen in
 * Mercator aber um die lokale Meridiankonvergenz gedreht (bis ~±4° über
 * Deutschland). Statt die Geometrie anzufassen (der Zensus-/GITTER_ID-Bezug
 * muss erhalten bleiben), wird die Karte per Bearing gegengedreht, sodass die
 * Gitterkanten parallel zu den Viewport-Rändern verlaufen.
 */

/** Web-Mercator-y (Radiant) einer Breite in Grad. */
const mercY = (latDeg: number) => Math.asinh(Math.tan((latDeg * Math.PI) / 180))

/**
 * MapLibre-Bearing (Grad, im Uhrzeigersinn = Kompassrichtung von "oben"), das
 * die Kanten einer EPSG:3035-Gitterzelle parallel zu den Viewport-Rändern
 * rendert. Nimmt einen lon/lat-Ring der Zelle; Eckreihenfolge ist durch die
 * Normalisierung modulo 90° egal. Ergebnis in [-45, 45], null wenn kein
 * verwertbarer Ring vorliegt.
 */
export function gridAlignBearing(
  ring: ReadonlyArray<ReadonlyArray<number>> | undefined,
): number | null {
  if (!ring || ring.length < 2) return null
  const a = ring[0]
  const b = ring.find((p) => p[0] !== a[0] || p[1] !== a[1])
  if (!b) return null
  const dx = ((b[0] - a[0]) * Math.PI) / 180 // Mercator-x ∝ Länge
  const dy = mercY(b[1]) - mercY(a[1]) // Mercator-y (Nord = +)
  if (dx === 0 && dy === 0) return null
  const az = (Math.atan2(dx, dy) * 180) / Math.PI // Azimut der Kante, im UZS ab Nord
  let r = ((az % 90) + 90) % 90
  if (r > 45) r -= 90
  return r
}

/** Äußerer Ring des ersten (Multi-)Polygon-Features einer Feature-Liste. */
export function firstPolygonRing(
  features?: ReadonlyArray<{ geometry?: unknown }>,
): number[][] | undefined {
  for (const f of features ?? []) {
    const g = f.geometry as GeoJSON.Geometry | undefined
    if (g?.type === 'Polygon') return g.coordinates[0]
    if (g?.type === 'MultiPolygon') return g.coordinates[0]?.[0]
  }
  return undefined
}
