import { useEffect } from 'react'
import { useStore } from '../store'
import KommuneHeader from './dashboard/KommuneHeader'
import CostTimelineSection from './dashboard/CostTimelineSection'
import { GroupRadarCard, TopRisksCard, GroupRadarGrid } from './dashboard/RiskRadarSection'
import RiskDistributionSection from './dashboard/RiskDistributionSection'
import CostTablesSection from './dashboard/CostTablesSection'

/**
 * Dashboard „Executive Story" (Variante C): Hero-Kopf mit Euro-Kernzahlen und
 * DE-Vergleich → Kosten-Timeline als Centerpiece → Risikofelder-Radar +
 * Top-Schadenstreiber → Einzelrisiko-Radars → Details (Accordion).
 *
 * Berechnungssteuerung lebt im Konfigurations-Screen (ProjectStatusPanel);
 * hier werden nur Ergebnisse gezeigt. Jede Sektion bringt ihren eigenen
 * Lade-Skeleton in Endhöhe mit.
 */
export default function Dashboard() {
  const {
    kommune, status,
    riskSummary, costSummary, riskHistogram, costProjection, kommuneProfile,
    loadCatalog, loadRiskSummary, loadCostSummary, loadRiskHistogram,
    loadCostProjection, loadKommuneProfile,
  } = useStore()

  useEffect(() => { loadCatalog().catch(() => {}) }, [])
  useEffect(() => {
    if (!kommune || status?.status !== 'done') return
    if (!riskSummary) loadRiskSummary(kommune.id).catch(() => {})
    if (!costSummary) loadCostSummary(kommune.id).catch(() => {})
    if (!riskHistogram) loadRiskHistogram(kommune.id).catch(() => {})
    if (!costProjection) loadCostProjection(kommune.id).catch(() => {})
    if (!kommuneProfile) loadKommuneProfile(kommune.id).catch(() => {})
  }, [kommune, status?.status])

  if (!kommune) return null

  return (
    <div className="dashboard-grid-12">
      <KommuneHeader className="col-span-12" />
      <CostTimelineSection className="col-span-12" />
      <GroupRadarCard className="col-span-6" />
      <TopRisksCard className="col-span-6" />
      <GroupRadarGrid className="col-span-12" />

      {riskSummary && (
        <details className="dashboard-section dashboard-details col-span-12">
          <summary>▸ Details: Risikoverteilung & Kostentabellen</summary>
          <RiskDistributionSection />
          <CostTablesSection />
        </details>
      )}
    </div>
  )
}
