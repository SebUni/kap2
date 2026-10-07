import type { CostSummary, RiskAggregate } from '../types'

/**
 * Betrag „nach Maßnahmen“ der Karte „Erwartete Schäden je Risiko“ (T-1816).
 *
 * Die Spalte „Schaden/Jahr“ zeigt immer den Schaden ohne Wirkung der Maßnahmen
 * (`risk-summary`). Der Betrag aus `cost-summary` (Schaden mit Maßnahmen) steht nur
 * dann in einer zweiten Spalte, wenn er für die Zeile davon abweicht. Verglichen wird
 * auf ganze Euro, weil die Karte ganze Euro zeigt: zwei gleich aussehende Beträge
 * sind keine Abweichung.
 *
 * Reine Funktion ohne React, damit `backend/tests/test_schaden_nach_massnahmen.py` sie
 * unverändert ausführen kann (das Frontend hat keinen Testläufer).
 */
export interface NachMassnahmen {
  /** Es gibt mindestens eine abweichende, angezeigte Zeile: die Spalte wird gezeigt. */
  hatSpalte: boolean
  /** Summenzeile einer Klimawirkung mit Teilzeilen: Schlüssel `schluesselKlimawirkung`. */
  summe: Map<string, number>
  /** Zeile (Teilzeile oder einzelne Klimawirkung), Schlüssel `code`. */
  zeile: Map<string, number>
}

type Kosten = Pick<RiskAggregate['cost'], 'by_risk' | 'klimawirkungen'>

export const schluesselKlimawirkung = (k: { codes: string[] }): string => k.codes.join('|')

/** Betrag nach Maßnahmen, wenn er sich im Anzeigewert (ganze Euro) vom Ausgangswert unterscheidet. */
function abweichung(ausgang: number | null | undefined, mit: number | null | undefined): number | null {
  if (ausgang == null || mit == null) return null
  return Math.round(ausgang) !== Math.round(mit) ? mit : null
}

/**
 * @param ausgang  `riskSummary.cost` — Schaden ohne Wirkung der Maßnahmen
 * @param mit      `costSummary` — Schaden mit Wirkung der Maßnahmen; null = nicht geladen
 * @param maxBloecke  so viele Klimawirkungen zeigt die Karte höchstens
 */
export function schadenNachMassnahmen(
  ausgang: Kosten,
  mit: Pick<CostSummary, 'by_risk' | 'klimawirkungen'> | null | undefined,
  maxBloecke: number,
): NachMassnahmen {
  const summe = new Map<string, number>()
  const zeile = new Map<string, number>()
  if (!mit) return { hatSpalte: false, summe, zeile }

  const mitZeilen = new Map(mit.by_risk.map(z => [z.code, z]))
  const ausgangZeilen = new Map(ausgang.by_risk.map(z => [z.code, z]))
  const mitBloecke = new Map(mit.klimawirkungen.map(k => [schluesselKlimawirkung(k), k]))

  const zeileMerken = (code: string) => {
    const a = abweichung(ausgangZeilen.get(code)?.cost_eur, mitZeilen.get(code)?.cost_eur)
    if (a != null) zeile.set(code, a)
  }

  for (const k of ausgang.klimawirkungen.slice(0, maxBloecke)) {
    if (k.teile.length > 0) {
      const key = schluesselKlimawirkung(k)
      const a = abweichung(k.cost_eur, mitBloecke.get(key)?.cost_eur)
      if (a != null) summe.set(key, a)
      k.teile.forEach(t => zeileMerken(t.code))
    } else {
      zeileMerken(k.codes[0])
    }
  }
  return { hatSpalte: summe.size > 0 || zeile.size > 0, summe, zeile }
}

/** Gesamtschaden nach Maßnahmen, nur wenn er sich vom Gesamtschaden ohne Maßnahmen unterscheidet. */
export function gesamtNachMassnahmen(
  gesamtOhne: number,
  mit: Pick<CostSummary, 'damages_with_measures_eur'> | null | undefined,
): number | null {
  return mit ? abweichung(gesamtOhne, mit.damages_with_measures_eur) : null
}
