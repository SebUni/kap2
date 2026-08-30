import LineageFlowDiagram from '../../components/LineageFlowDiagram'
import { TELECOM_LINEAGE } from './landingLineage'
import ToolExcerptBadge from './ToolExcerptBadge'

/**
 * Mini-Widget E — Die Wirkungskette als echtes Tool-Wirkungsdiagramm.
 * Nutzt direkt die Produkt-Komponente `LineageFlowDiagram` mit dem echten
 * Lineage-Baum des Risikos „Erwartete jährliche Schäden an Telekommunikations-
 * infrastruktur" (nur der monetäre Ast): Quellen (OSM/DWD/DEM) → Gefahren
 * (Stürme, Starkregen) × Assetwert × Schadenskurve × Vulnerabilität → €-Schaden.
 * Gefahren/Exposition/Vulnerabilität sind vorab sichtbar; Operatoren/Parameter/
 * Zwischenergebnisse blendet der Nutzer über die Legende ein — wie im Produkt.
 */
export default function ChainWidget() {
  return (
    <div className="landing-widget chain-widget">
      <ToolExcerptBadge />
      <h4>Vom Rohdatum zum Euro — der komplette Rechenweg eines Risikos</h4>
      <p className="widget-caption-hint" style={{ marginBottom: '0.75rem' }}>
        Ein echtes Wirkungsdiagramm: erwartete jährliche Schäden an Telekommunikationsinfrastruktur.
        Blenden Sie über die Legende Quellen, Gefahren, Vulnerabilität und Operatoren ein oder aus —
        genau wie im Produkt.
      </p>
      <div className="landing-lineage">
        <LineageFlowDiagram
          lineage={TELECOM_LINEAGE}
          embedded
          initialHiddenTypes={['parameter', 'intermediate', 'operator']}
        />
      </div>
      <p className="mini-widget-quote">
        So sieht jede Wirkungskette im Produkt aus — bis in die einzelne Rasterzelle.
      </p>
    </div>
  )
}
