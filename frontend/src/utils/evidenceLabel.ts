import type { EvidenceClass } from '../types'

/** Anzeigetext je Evidenzklasse (Vorgabe P1) — einzige Zuordnung, von Parameterliste und Maßnahmentabelle genutzt. */
export function evidenzAnzeige(klasse: EvidenceClass): string {
  if (klasse === 'abgeschaetzt') return 'abgeschätzt (KAP3)'
  if (klasse === 'berechnet') return 'berechnet aus amtlichen Daten'
  return 'belegt'
}

/** Ist der Wert eine der drei Evidenzklassen? */
export function istEvidenzklasse(wert: string): wert is EvidenceClass {
  return wert === 'belegt' || wert === 'abgeschaetzt' || wert === 'berechnet'
}
