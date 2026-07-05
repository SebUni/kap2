import { useEffect, useState } from 'react'
import { api } from '../api/client'
import type { ActiveLayer } from '../store'
import type {
  CatalogMeasure, LayerRecipeMeta, ModelParameter, PathwayRecipeMeta, RiskRecipe,
} from '../types'
import LineageFlowDiagram from './LineageFlowDiagram'
import { useStore } from '../store'

interface Props {
  layer: ActiveLayer
  onClose: () => void
  onOpenConfig: () => void
}

export default function LayerInfoModal({ layer, onClose, onOpenConfig }: Props) {
  const { kommune, catalog } = useStore()
  const [meta, setMeta] = useState<LayerRecipeMeta | null>(null)
  const [parameters, setParameters] = useState<ModelParameter[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = async () => {
    if (!kommune) return
    setLoading(true)
    setError(null)
    try {
      const [recipeRes, paramsRes] = await Promise.all([
        api.getLayerRecipe(layer.code, layer.category),
        api.getParameters(kommune.id, layer.code, layer.category),
      ])
      setMeta(recipeRes as unknown as LayerRecipeMeta)
      setParameters(paramsRes as unknown as ModelParameter[])
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Laden fehlgeschlagen')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [kommune?.id, layer.code, layer.category])

  const measureMeta = layer.category === 'measures' && catalog
    ? catalog.measures.find(m => m.code === layer.code)
    : null

  const title = meta?.description?.trim() || meta?.label || layer.code
  const showDescription = meta?.description && meta.description.trim() !== title

  return (
    <div className="help-overlay" onClick={onClose}>
      <div
        className="help-overlay-content layer-info-modal"
        onClick={e => e.stopPropagation()}
      >
        <div className="help-overlay-header layer-info-header">
          <div className="layer-info-header-text">
            <span className="layer-info-kicker">Wirkungsdiagramm</span>
            <h2>{title}</h2>
          </div>
          <button type="button" onClick={onClose} className="help-overlay-close">✕</button>
        </div>

        <div className="help-overlay-body layer-info-body">
          {loading && <p style={{ color: 'var(--text-muted)' }}>Lade …</p>}
          {error && <p style={{ color: 'var(--danger, #dc2626)' }}>{error}</p>}

          {!loading && !error && meta && (
            <>
              {showDescription && (
                <p className="layer-info-desc">{meta.description}</p>
              )}
              {meta.lineage && meta.lineage.nodes.length > 0 ? (
                <LineageFlowDiagram
                  lineage={meta.lineage}
                  parameters={parameters}
                  kommuneId={kommune?.id}
                  onParametersUpdated={load}
                  embedded
                />
              ) : (
                <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                  Kein Herkunftsdiagramm für diese Ebene verfügbar.
                </p>
              )}
              {measureMeta && <MeasureInfo measure={measureMeta} />}
              <PathwayJustifications recipe={meta.recipe} />
            </>
          )}
        </div>

        <div className="layer-info-footer">
          <p>
            Parameter bearbeiten unter{' '}
            <button type="button" className="layer-info-link" onClick={onOpenConfig}>
              Konfiguration
            </button>
            .
          </p>
        </div>
      </div>
    </div>
  )
}

function isRiskRecipe(r: LayerRecipeMeta['recipe']): r is RiskRecipe {
  return !!r && Array.isArray((r as RiskRecipe).pathways)
}

const PATHWAY_TYPE_ORDER: Record<string, number> = {
  primary: 0, aligned: 1, alternate_hazard: 2, alternate_exposure: 3,
  alternate_vulnerability: 4, compound_he: 5, compound_hv: 6, compound_ev: 7,
  compound_multi: 8,
}

/**
 * Begründung der Wirkungsketten: eigene Info-Sektion, die für jede kuratierte
 * Wirkungskette die fachliche Herleitung + Quelle (KWRA 2021 / GIZ Vulnerability
 * Sourcebook) sichtbar macht (Stufe 1 — Pfad-Kuratierung).
 */
function PathwayJustifications({ recipe }: { recipe: LayerRecipeMeta['recipe'] }) {
  if (!isRiskRecipe(recipe)) return null
  const pathways = (recipe.pathways || [])
    .filter((p): p is PathwayRecipeMeta => !!p.justification)
    .slice()
    .sort((a, b) => (PATHWAY_TYPE_ORDER[a.type] ?? 9) - (PATHWAY_TYPE_ORDER[b.type] ?? 9))
  if (!pathways.length) return null

  const cluster = pathways.find(p => p.cluster)?.cluster

  return (
    <section className="kap-pathway-justify">
      <h3 className="kap-pathway-justify-title">Begründung der Wirkungsketten</h3>
      {cluster && (
        <p className="kap-pathway-justify-cluster">
          Handlungsfeld/Cluster: <strong>{cluster}</strong>
        </p>
      )}
      <p className="kap-pathway-justify-intro">
        Die Ketten folgen dem Wirkungsketten-Ansatz (Klimasignal → Exposition ×
        Empfindlichkeit) der KWRA 2021 bzw. des GIZ Vulnerability Sourcebook. Der Index
        ist das Maximum der gewichteten Ketten (die stärkste Kette bestimmt den Wert).
      </p>
      <ol className="kap-pathway-justify-list">
        {pathways.map((p, i) => {
          const src = p.justification_source
          const isPrimary = p.type === 'primary'
          return (
            <li key={i} className={`kap-pathway-justify-item${isPrimary ? ' is-primary' : ''}`}>
              <div className="kap-pathway-justify-head">
                <span className="kap-pathway-justify-badge">{p.type_label}</span>
                <span className="kap-pathway-justify-chain">
                  {p.hazard_name} × {p.exposure_name} × {p.vulnerability_name}
                </span>
                <span className="kap-pathway-justify-weight">Gewicht {p.weight}</span>
              </div>
              <p className="kap-pathway-justify-note">{p.justification}</p>
              {src && (
                <p className="kap-pathway-justify-src">
                  Quelle:{' '}
                  {src.url
                    ? <a href={src.archive_url || src.url} target="_blank" rel="noopener noreferrer">{src.ieee || src.key}</a>
                    : (src.ieee || src.key)}
                </p>
              )}
            </li>
          )
        })}
      </ol>
    </section>
  )
}

function MeasureInfo({ measure }: { measure: CatalogMeasure }) {
  return (
    <div className="kap-measure-info">
      <p><strong>Wirkungsziel:</strong> {measure.effect_target?.join(', ') || '—'}</p>
      <p><strong>Verknüpfte Risiken:</strong> {measure.linked_risk_codes?.join(', ') || '—'}</p>
      <p><strong>Standard-Reduktion:</strong> {(measure.default_reduction * 100).toFixed(0)} %</p>
      {measure.description && <p>{measure.description}</p>}
    </div>
  )
}
