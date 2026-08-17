// Einheitliche Farbzuordnung der 7 KAnG-Cluster (Reihenfolge wie im Gesetz).
// Genutzt für Maßnahmen-Flächen auf der Karte, Legende und ggf. Panels.
export const KANG_CLUSTER_COLORS: Record<string, string> = {
  infrastructure: '#2563eb', // Infrastruktur – blau
  land: '#16a34a',           // Land und Landnutzung – grün
  health: '#dc2626',         // Gesundheit und Pflege – rot
  urban: '#f59e0b',          // Stadtentwicklung/Raumplanung – amber
  water: '#06b6d4',          // Wasser – cyan
  economy: '#9333ea',        // Wirtschaft – violett
  crosscutting: '#64748b',   // Übergreifend – schiefergrau
}

export const KANG_CLUSTER_FALLBACK = '#64748b'

/** Farbe für einen Cluster-Code (fällt auf „crosscutting"/grau zurück). */
export function kangClusterColor(clusterCode: string | null | undefined): string {
  if (!clusterCode) return KANG_CLUSTER_FALLBACK
  return KANG_CLUSTER_COLORS[clusterCode] ?? KANG_CLUSTER_FALLBACK
}
