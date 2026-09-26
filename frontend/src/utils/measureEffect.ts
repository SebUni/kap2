import type { CatalogMeasure } from '../types'

/** Wirkungstext S157 (Bericht #95 §5), gleichlautend zur Kante in lineage_graph.py. */
export const S157_EFFECT_TEXT = 'g_S157 auf die Todesfälle 85+ in Heimen, abhängig von s_gek'

/**
 * Anzeige der Minderung einer Katalog-Maßnahme. Maßnahmen mit eigenem Wirkungsmodell
 * (S157) haben kein default_reduction; dort steht der Wirkungstext statt „0 %“.
 */
/** Wirkungstext der Schutzprogramme δ_VG (Bericht #95 §5), gleichlautend zur Kante in lineage_graph.py. */
export const VG_EFFECT_TEXT = 'δ_VG 0,931 auf die Todesfälle 75–84 und 85+ ohne Heimbewohner'

export function measureReductionText(m: Pick<CatalogMeasure, 'code' | 'default_reduction' | 'effect_model'>): string {
  if (m.effect_model === 's157' || m.code === 'COOLING_ROOMS_DRINKING_WATER') return S157_EFFECT_TEXT
  if (m.effect_model === 'vg' || m.code === 'VULNERABLE_GROUP_PROGRAMS') return VG_EFFECT_TEXT
  return `${Math.round((m.default_reduction || 0) * 100)} %`
}
