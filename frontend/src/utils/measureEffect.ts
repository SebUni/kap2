import type { CatalogMeasure } from '../types'

/** Wirkungstext der Maßnahme COOLING_ROOMS_DRINKING_WATER (Bericht #95 §5): zwei Hebel,
 *  S157 (gekühlte Heimplätze, Befund 138: ohne Eingabe Voreinstellung s_gek = 11 %) und
 *  öffentliche Kühlzentren (Befunde 139/148: δ_KZ 0,9956, Block heat.delta_kuehlzentren). */
export const S157_EFFECT_TEXT = 'g_S157 auf die Todesfälle 85+ in Heimen, abhängig von s_gek '
  + '(ohne Eingabe Voreinstellung 11 %, Abschätzung von KAP3); öffentliche Kühlzentren: '
  + 'δ_KZ 0,9956 auf die Todesfälle ab 75 zu Hause (Abschätzung von KAP3)'

/** Voreinstellung s_gek in Prozent (Bericht #95 §5, Block heat.s_gek, Befund 138):
 *  gilt, wenn die Kommune keinen gekühlten Anteil der Heimplätze eingibt. */
export const S157_S_GEK_DEFAULT_PCT = 11

/** Wächter-Frage (Bericht #95 §5, Befund 150, Block heat.vg_in_kalibrierjahren) für
 *  VULNERABLE_GROUP_PROGRAMS und COOLING_ROOMS_DRINKING_WATER; Voreinstellung „nein“. */
export const VG_KALIB_FRAGE = 'Lief das Programm schon in den Jahren 2012–2024?'

/**
 * Anzeige der Minderung einer Katalog-Maßnahme. Maßnahmen mit eigenem Wirkungsmodell
 * (S157) haben kein default_reduction; dort steht der Wirkungstext statt „0 %“.
 */
/** Wirkungstext der Schutzprogramme δ_VG (Bericht #95 §5), gleichlautend zur Kante in lineage_graph.py. */
export const VG_EFFECT_TEXT = 'δ_VG 0,931 auf die Todesfälle 75–84 und 85+ ohne Heimbewohner'

/** Wirkungstext S158 (Bericht #96 §5.1): keine pauschale Prozentangabe, weil r_S158
 *  je gewarntem Tag auf die Zusatztage wirkt, nicht auf den Risiko-Index. */
export const S158_EFFECT_TEXT = 'r_S158 × t_warn auf die gewarnten Zusatztage im Geltungsbereich'

export function measureReductionText(m: Pick<CatalogMeasure, 'code' | 'default_reduction' | 'effect_model'>): string {
  if (m.effect_model === 's157' || m.code === 'COOLING_ROOMS_DRINKING_WATER') return S157_EFFECT_TEXT
  if (m.effect_model === 'vg' || m.code === 'VULNERABLE_GROUP_PROGRAMS') return VG_EFFECT_TEXT
  if (m.effect_model === 's158' || m.code === 'POLLEN_EARLY_WARNING') return S158_EFFECT_TEXT
  return `${Math.round((m.default_reduction || 0) * 100)} %`
}
