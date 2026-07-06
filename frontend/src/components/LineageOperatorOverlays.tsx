import { useCallback, useEffect, useMemo, useState } from 'react'
import type { Network } from 'vis-network'
import { api } from '../api/client'
import type { LineageNodeData, ModelParameter } from '../types'
import {
  edgeWeightEditField,
  fmtNum,
  operatorDisplayValue,
  operatorEditFields,
  operatorKindLabel,
  operatorShowsSingleLabel,
} from '../utils/lineageOperatorFormat'

interface DisplayNodeRef {
  id: string
  data: LineageNodeData
}

interface DisplayEdgeRef {
  id: string
  source: string
  target: string
  meta?: Record<string, unknown>
}

interface Props {
  network: Network | null
  displayNodes: DisplayNodeRef[]
  displayEdges: DisplayEdgeRef[]
  parameters: ModelParameter[]
  kommuneId?: number
  onUpdated?: () => void
}

interface NodePos {
  x: number
  y: number
}

function paramUnit(pid: string | undefined, parameters: ModelParameter[]): string {
  if (!pid) return ''
  return parameters.find(p => p.id === pid)?.unit ?? ''
}

function ComputeOpBody({ kind, meta, label }: { kind: string; meta: Record<string, unknown>; label: string }) {
  const kindLbl = operatorKindLabel(kind, meta) || label
  const display = operatorDisplayValue(kind, meta)
  const isSymbolKind = ['multiply', 'divide', 'add', 'scale_factor'].includes(kind)

  if (isSymbolKind) {
    const sym = display || kindLbl
    return (
      <div className={`kap-op kap-op--symbol kap-op--${kind}`}>
        <div className="kap-op-value kap-op-value--symbol">{sym}</div>
      </div>
    )
  }

  if (operatorShowsSingleLabel(kind) || !display || display === kindLbl || display === label) {
    return (
      <div className={`kap-op kap-op--${kind}`}>
        <div className="kap-op-kind">{kindLbl}</div>
      </div>
    )
  }

  return (
    <div className={`kap-op kap-op--${kind}`}>
      <div className="kap-op-kind">{kindLbl}</div>
      <div className="kap-op-value">{display}</div>
    </div>
  )
}

function samePositions(a: Record<string, NodePos>, b: Record<string, NodePos>): boolean {
  const aKeys = Object.keys(a)
  const bKeys = Object.keys(b)
  if (aKeys.length !== bKeys.length) return false
  for (const key of aKeys) {
    const pa = a[key]
    const pb = b[key]
    if (!pb || pa.x !== pb.x || pa.y !== pb.y) return false
  }
  return true
}

function overlayStyle(x: number, y: number, scale: number): React.CSSProperties {
  return {
    left: x,
    top: y,
    transform: `translate(-50%, -50%) scale(${scale})`,
    transformOrigin: 'center center',
  }
}

export default function LineageOperatorOverlays({
  network,
  displayNodes,
  displayEdges,
  parameters,
  kommuneId,
  onUpdated,
}: Props) {
  const [nodePositions, setNodePositions] = useState<Record<string, NodePos>>({})
  const [edgePositions, setEdgePositions] = useState<Record<string, NodePos>>({})
  const [viewScale, setViewScale] = useState(1)
  const [editingKey, setEditingKey] = useState<string | null>(null)
  const [draft, setDraft] = useState('')
  const [saving, setSaving] = useState(false)

  const operatorNodes = useMemo(
    () => displayNodes.filter(d => d.data.type === 'operator'),
    [displayNodes],
  )
  const parameterNodes = useMemo(
    () => displayNodes.filter(d => d.data.type === 'parameter'),
    [displayNodes],
  )
  const weightEdges = useMemo(
    () => displayEdges.filter(e => e.meta?.op_kind === 'weight'),
    [displayEdges],
  )

  const syncPositions = useCallback(() => {
    if (!network) return
    const scale = typeof network.getScale === 'function' ? network.getScale() : 1
    setViewScale(prev => (prev === scale ? prev : scale))

    const nextNodes: Record<string, NodePos> = {}
    if (operatorNodes.length) {
      const ids = operatorNodes.map(d => d.id)
      const pos = network.getPositions(ids)
      for (const id of ids) {
        const canvas = pos[id]
        if (!canvas) continue
        const dom = network.canvasToDOM({ x: canvas.x, y: canvas.y })
        nextNodes[id] = { x: dom.x, y: dom.y }
      }
    }
    if (parameterNodes.length) {
      const ids = parameterNodes.map(d => d.id)
      const pos = network.getPositions(ids)
      for (const id of ids) {
        const canvas = pos[id]
        if (!canvas) continue
        const dom = network.canvasToDOM({ x: canvas.x, y: canvas.y })
        nextNodes[id] = { x: dom.x, y: dom.y }
      }
    }
    setNodePositions(prev => (samePositions(prev, nextNodes) ? prev : nextNodes))

    const nextEdges: Record<string, NodePos> = {}
    for (const e of weightEdges) {
      const pos = network.getPositions([e.source, e.target])
      const from = pos[e.source]
      const to = pos[e.target]
      if (!from || !to) continue
      const mid = { x: (from.x + to.x) / 2, y: (from.y + to.y) / 2 }
      const dom = network.canvasToDOM(mid)
      nextEdges[e.id] = { x: dom.x, y: dom.y }
    }
    setEdgePositions(prev => (samePositions(prev, nextEdges) ? prev : nextEdges))
  }, [network, operatorNodes, parameterNodes, weightEdges])

  useEffect(() => {
    if (!network) return
    // 'afterDrawing' feuert bei jeder Ansichtsänderung (Pan/Zoom/Drag) → deckt die
    // Overlay-Neupositionierung ab; 'viewChanged' ist kein vis-network-Event (Typfehler).
    const events = ['afterDrawing', 'zoom', 'dragEnd', 'stabilizationIterationsDone'] as const
    for (const ev of events) network.on(ev, syncPositions)
    syncPositions()
    return () => {
      for (const ev of events) network.off(ev, syncPositions)
    }
  }, [network, syncPositions])

  const saveField = async (parameterId: string, editable: boolean) => {
    if (!kommuneId || !editable) return
    const num = parseFloat(draft.replace(',', '.'))
    const value = Number.isNaN(num) ? draft : num
    const param = parameters.find(p => p.id === parameterId)
    const payload: { parameter_id: string; value: unknown; custom_source?: string } = {
      parameter_id: parameterId,
      value,
    }
    if (param && value !== param.default_value) {
      payload.custom_source = param.custom_source?.trim() || 'Anpassung im Wirkungsdiagramm'
    }
    setSaving(true)
    try {
      await api.updateParameters(kommuneId, [payload])
      setEditingKey(null)
      onUpdated?.()
    } catch {
      /* keep editor */
    } finally {
      setSaving(false)
    }
  }

  if (!operatorNodes.length && !parameterNodes.length && !weightEdges.length) return null

  return (
    <>
      {parameterNodes.map(dn => {
        const pos = nodePositions[dn.id]
        if (!pos) return null
        const pid = dn.data.meta?.parameter_id as string | undefined
        const param = pid ? parameters.find(p => p.id === pid) : undefined
        const metaValue = dn.data.meta?.value
        const val = param
          ? fmtNum(param.value)
          : metaValue != null ? fmtNum(metaValue) : '—'
        const unit = param?.unit || String(dn.data.meta?.unit ?? '')
        const editable = !!param?.editable && !!pid
        const key = `param:${dn.id}`
        return (
          <div
            key={dn.id}
            className="kap-op-overlay kap-op-overlay--parameter"
            style={overlayStyle(pos.x, pos.y, viewScale)}
            onPointerDown={e => e.stopPropagation()}
          >
            <div className="kap-param-node">
              <div className="kap-param-node-name">{dn.data.label}</div>
              {editingKey === key && editable ? (
                <input
                  className="kap-op-input kap-op-input--value"
                  value={draft}
                  autoFocus
                  disabled={saving}
                  onChange={ev => setDraft(ev.target.value)}
                  onBlur={() => pid && void saveField(pid, editable)}
                  onKeyDown={ev => {
                    if (ev.key === 'Enter' && pid) void saveField(pid, editable)
                    if (ev.key === 'Escape') setEditingKey(null)
                  }}
                />
              ) : (
                <button
                  type="button"
                  className={`kap-param-node-value kap-op-value--btn${editable ? ' kap-op-value--editable' : ''}`}
                  onClick={() => {
                    if (editable && param) {
                      setEditingKey(key)
                      setDraft(String(param.value))
                    }
                  }}
                >
                  {val}
                </button>
              )}
              {unit ? <div className="kap-param-node-unit">{unit}</div> : null}
            </div>
          </div>
        )
      })}

      {operatorNodes.map(dn => {
        const pos = nodePositions[dn.id]
        if (!pos) return null
        const meta = dn.data.meta ?? {}
        const kind = meta.op_kind as string
        const fields = operatorEditFields(dn.data, parameters)
        const editableKinds = new Set(['scaling', 'multiplier', 'norm'])

        if (editableKinds.has(kind)) {
          return (
            <div
              key={dn.id}
              className={`kap-op-overlay kap-op-overlay--${kind}`}
              style={overlayStyle(pos.x, pos.y, viewScale)}
              onPointerDown={e => e.stopPropagation()}
            >
              {(kind === 'scaling' || kind === 'multiplier') && (
                <div className="kap-op kap-op--scaling">
                  <div className="kap-op-kind">{operatorKindLabel(kind, meta)}</div>
                  {editingKey === dn.id && fields[0]?.editable ? (
                    <input
                      className="kap-op-input kap-op-input--value"
                      value={draft}
                      autoFocus
                      disabled={saving}
                      onChange={ev => setDraft(ev.target.value)}
                      onBlur={() => void saveField(fields[0].parameterId, fields[0].editable)}
                      onKeyDown={ev => {
                        if (ev.key === 'Enter') void saveField(fields[0].parameterId, fields[0].editable)
                        if (ev.key === 'Escape') setEditingKey(null)
                      }}
                    />
                  ) : (
                    <button
                      type="button"
                      className={`kap-op-value kap-op-value--btn${fields[0]?.editable ? ' kap-op-value--editable' : ''}`}
                      onClick={() => {
                        if (fields[0]?.editable) {
                          setEditingKey(dn.id)
                          setDraft(fields[0].value)
                        }
                      }}
                    >
                      {fields[0] ? fmtNum(fields[0].value) : fmtNum(meta.value)}
                    </button>
                  )}
                  <div className="kap-op-unit">
                    {paramUnit(fields[0]?.parameterId, parameters) || String(meta.unit ?? '')}
                  </div>
                </div>
              )}

              {kind === 'norm' && (
                <div className="kap-op kap-op--norm">
                  <div className="kap-op-kind">Normierung</div>
                  {(['max', 'min'] as const).map((bound, idx) => {
                    const key = `${dn.id}:${bound}`
                    const field = fields[idx]
                    return (
                      <div key={bound} className={`kap-op-bound kap-op-bound--${bound}`}>
                        {editingKey === key && field?.editable ? (
                          <input
                            className="kap-op-input kap-op-input--limit"
                            value={draft}
                            autoFocus
                            disabled={saving}
                            onChange={ev => setDraft(ev.target.value)}
                            onBlur={() => void saveField(field.parameterId, field.editable)}
                            onKeyDown={ev => {
                              if (ev.key === 'Enter') void saveField(field.parameterId, field.editable)
                              if (ev.key === 'Escape') setEditingKey(null)
                            }}
                          />
                        ) : (
                          <button
                            type="button"
                            className={`kap-op-limit kap-op-value--btn${field?.editable ? ' kap-op-value--editable' : ''}`}
                            onClick={() => {
                              if (field?.editable) {
                                setEditingKey(key)
                                setDraft(field.value)
                              }
                            }}
                          >
                            {field ? fmtNum(field.value) : '—'}
                          </button>
                        )}
                        <span className="kap-op-map">{bound === 'max' ? '→ 1' : '→ 0'}</span>
                      </div>
                    )
                  })}
                  <div className="kap-op-unit">
                    {paramUnit(fields[0]?.parameterId, parameters) || String(meta.unit ?? '')}
                  </div>
                </div>
              )}
            </div>
          )
        }

        return (
          <div
            key={dn.id}
            className={`kap-op-overlay kap-op-overlay--${kind}`}
            style={overlayStyle(pos.x, pos.y, viewScale)}
            onPointerDown={e => e.stopPropagation()}
          >
            <ComputeOpBody kind={kind} meta={meta} label={dn.data.label} />
          </div>
        )
      })}

      {weightEdges.map(e => {
        const pos = edgePositions[e.id]
        if (!pos) return null
        const meta = e.meta ?? {}
        const field = edgeWeightEditField(meta, parameters)
        const val = field?.value ?? meta.weight
        const key = `edge:${e.id}`

        return (
          <div
            key={e.id}
            className="kap-op-overlay kap-op-overlay--weight kap-op-overlay--edge"
            style={overlayStyle(pos.x, pos.y, viewScale)}
            onPointerDown={ev => ev.stopPropagation()}
          >
            <div className="kap-op kap-op--weight kap-op--weight-edge">
              <div className="kap-op-kind">Gewicht</div>
              {editingKey === key && field?.editable ? (
                <input
                  className="kap-op-input kap-op-input--weight"
                  value={draft}
                  autoFocus
                  disabled={saving}
                  onChange={ev => setDraft(ev.target.value)}
                  onBlur={() => field && void saveField(field.parameterId, field.editable)}
                  onKeyDown={ev => {
                    if (ev.key === 'Enter' && field) void saveField(field.parameterId, field.editable)
                    if (ev.key === 'Escape') setEditingKey(null)
                  }}
                />
              ) : (
                <button
                  type="button"
                  className={`kap-op-value kap-op-value--btn kap-op-value--weight${field?.editable ? ' kap-op-value--editable' : ''}`}
                  onClick={() => {
                    if (field?.editable) {
                      setEditingKey(key)
                      setDraft(field.value)
                    }
                  }}
                >
                  {fmtNum(val)}
                </button>
              )}
            </div>
          </div>
        )
      })}
    </>
  )
}
