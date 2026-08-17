/**
 * Echter Wirkungs-Lineage-Baum des Risikos „Erwartete jährliche Schäden an
 * Telekommunikationsinfrastruktur" (`EXPECTED_TELECOM_DAMAGE_EUR`), gefiltert
 * auf den **monetären** Ast (Wurzel `out:eur`; der parallele KWRA-Index-Zweig
 * ist weggeschnitten). Erzeugt aus dem echten Katalog über
 * `backend/scripts/export_landing_lineage.py` und hier als JSON eingefroren —
 * exakt dieselbe Datenform, die das Produkt an `LineageFlowDiagram` gibt.
 */
import type { LineageGraph } from '../../types'
import graph from './data/telecom-lineage.json'

export const TELECOM_LINEAGE = graph as unknown as LineageGraph
