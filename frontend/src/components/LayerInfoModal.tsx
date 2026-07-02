import { useEffect, useState } from 'react'
import { api } from '../api/client'
import type { ActiveLayer } from '../store'
import type { CatalogMeasure, LayerRecipeMeta, ModelParameter } from '../types'
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
