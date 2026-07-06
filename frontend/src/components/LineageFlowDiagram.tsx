import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { DataSet } from 'vis-data'
import { Network, type Edge, type Node, type Options } from 'vis-network'
import 'vis-network/styles/vis-network.min.css'
import type { LineageGraph, LineageNodeData, LineageNodeType } from '../types'
import {
  assertForestInvariants,
  bridgeHiddenTypes,
  forestLayout,
  mergeDuplicates,
  pathwayInstanceIds,
  unfoldToForest,
  type TreeNode,
} from '../utils/lineageFilter'
import { estimateNodeWidth } from '../utils/lineageLayout'
import { buildNodeTooltip, formatLineageTooltip } from '../utils/lineageTooltip'
import { edgeColorFromSource, lineageNodeColors } from '../utils/lineageColors'
import LineageOperatorOverlays from './LineageOperatorOverlays'
import type { ModelParameter } from '../types'

interface LegendGroup {
  label: string
  types: LineageNodeType[]
  rounded?: boolean
}

const LEGEND_LABELS: Record<LineageNodeType, string> = {
  source: 'Quelle',
  parameter: 'Parameter',
  intermediate: 'Zwischenwert',
  hazard: 'Klimatische Einflüsse',
  exposure: 'Räumliche Expositionen',
  vulnerability: 'Sensitivitäten',
  pathway: 'Wirkungskette',
  aggregation: 'Index',
  outcome: 'Ergebnis',
  norm: 'Normierung',
  operator: '× Operator',
}

const LEGEND_GROUPS: LegendGroup[] = [
  { label: 'Eingaben', types: ['source', 'parameter'] },
  { label: 'Zwischenergebnisse', types: ['intermediate'] },
  { label: 'Risiko-Ebenen', types: ['hazard', 'exposure', 'vulnerability', 'pathway'] },
  { label: 'Operatoren', types: ['operator'], rounded: true },
  { label: 'Ergebnisse', types: ['outcome'] },
]

// Startzustand: Quellen, Wirkungsketten und Ergebnisse sichtbar; alle weiteren
// Detailstufen werden über die Legenden-Chips zugeschaltet. Ergebnisse sind
// gepinnt und nie ausblendbar.
const DEFAULT_HIDDEN_TYPES: ReadonlySet<LineageNodeType> = new Set([
  'parameter',
  'intermediate',
  'hazard',
  'exposure',
  'vulnerability',
  'operator',
] as LineageNodeType[])

function truncate(text: string, max: number): string {
  return text.length > max ? `${text.slice(0, max - 1)}…` : text
}

function esc(text: string): string {
  return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
}

interface DisplayNode {
  id: string
  data: LineageNodeData
  x: number
  y: number
  isTerminal: boolean
  collapsed?: boolean
  childCount?: number
}

interface DisplayEdge {
  id: string
  source: string
  target: string
  label?: string | null
  meta?: Record<string, unknown>
}

/** Erzeugt ein mehrzeiliges HTML-Label, das den Knoten verständlich macht. */
function formatLabel(dn: DisplayNode): string {
  const { data, collapsed, childCount } = dn
  const badge = collapsed && childCount ? `  ▸ +${childCount}` : ''

  if (data.type === 'outcome') {
    return `<b>${esc(data.label)}</b>${badge}`
  }

  if (data.type === 'aggregation') {
    return `${esc(data.label)}${badge}`
  }

  if (data.type === 'pathway') {
    return `<b>${esc(data.label)}</b>${badge}`
  }

  const main = `<b>${esc(truncate(data.label, 32))}</b>`
  return `${main}${badge}`
}

function nodeWidthConstraint(data: LineageNodeData): { minimum?: number; maximum: number } {
  const w = estimateNodeWidth(data)
  if (data.type === 'pathway') return { minimum: 200, maximum: w }
  return { maximum: w }
}

function toVisData(
  displayNodes: DisplayNode[],
  displayEdges: DisplayEdge[],
  parameters: ModelParameter[],
): { nodes: DataSet<Node>; edges: DataSet<Edge>; tooltips: Map<string, string> } {
  const labelById = new Map(displayNodes.map(dn => [dn.id, dn.data.label]))
  const incomingByTarget = new Map<string, string[]>()
  for (const e of displayEdges) {
    const srcLabel = labelById.get(e.source)
    if (!srcLabel) continue
    if (!incomingByTarget.has(e.target)) incomingByTarget.set(e.target, [])
    incomingByTarget.get(e.target)!.push(srcLabel)
  }

  const nodeById = new Map(displayNodes.map(dn => [dn.id, dn.data]))
  const tooltips = new Map<string, string>()
  const nodes = new DataSet<Node>(
    displayNodes.map(dn => {
      const isOp = dn.data.type === 'operator'
      const isParam = dn.data.type === 'parameter'
      const opKind = (dn.data.meta?.op_kind as string) ?? ''
      const colors = lineageNodeColors(dn.data.type)
      const emphasize = !isOp && !isParam && dn.isTerminal && dn.data.type === 'outcome'
      const isIndex = dn.data.type === 'aggregation'
      const incoming = incomingByTarget.get(dn.id) ?? []
      tooltips.set(dn.id, buildNodeTooltip(dn.data, incoming))

      if (isParam) {
        const pid = dn.data.meta?.parameter_id as string | undefined
        const param = pid ? parameters.find(p => p.id === pid) : undefined
        const metaValue = dn.data.meta?.value
        const val = param
          ? String(param.value)
          : metaValue != null ? String(metaValue) : '—'
        const unit = param?.unit || String(dn.data.meta?.unit ?? '')
        const node: Record<string, unknown> = {
          id: dn.id,
          label: ' ',
          x: dn.x,
          y: dn.y,
          fixed: { x: true, y: true },
          shape: 'box',
          widthConstraint: { minimum: 100, maximum: 148 },
          heightConstraint: { minimum: 52, maximum: 72 },
          margin: 4,
          font: { size: 1, color: 'transparent' },
          color: {
            background: 'transparent',
            border: 'transparent',
            highlight: { background: 'transparent', border: 'transparent' },
            hover: { background: 'transparent', border: 'transparent' },
          },
          borderWidth: 0,
          shapeProperties: { borderRadius: 10 },
        }
        tooltips.set(
          dn.id,
          formatLineageTooltip(`${dn.data.label}\nWert: ${val}\nEinheit: ${unit}`),
        )
        return node as unknown as Node
      }

      if (isOp) {
        const isSymbol = ['multiply', 'divide', 'add', 'scale_factor'].includes(opKind)
        const node: Record<string, unknown> = {
          id: dn.id,
          label: ' ',
          x: dn.x,
          y: dn.y,
          fixed: { x: true, y: true },
          shape: 'box',
          widthConstraint: isSymbol ? { minimum: 40, maximum: 44 } : { minimum: 56, maximum: 88 },
          heightConstraint: isSymbol ? { minimum: 40, maximum: 44 } : { minimum: 44, maximum: 72 },
          margin: 4,
          font: { size: 1, color: 'transparent' },
          color: {
            background: 'transparent',
            border: 'transparent',
            highlight: { background: 'transparent', border: 'transparent' },
            hover: { background: 'transparent', border: 'transparent' },
          },
          borderWidth: 0,
          shapeProperties: { borderRadius: 12 },
        }
        return node as unknown as Node
      }

      const node: Record<string, unknown> = {
        id: dn.id,
        label: formatLabel(dn),
        x: dn.x,
        y: dn.y,
        fixed: { x: true, y: true },
        shape: 'box',
        widthConstraint: nodeWidthConstraint(dn.data),
        margin: emphasize ? 10 : 7,
        font: {
          size: dn.data.type === 'outcome' ? 14 : 12,
          multi: 'html',
          face: 'system-ui, sans-serif',
          color: '#1e293b',
        },
        color: {
          background: colors.bg,
          border: colors.border,
          highlight: { background: colors.bg, border: colors.border },
          hover: { background: colors.bg, border: colors.border },
        },
        borderWidth: emphasize ? 3 : isIndex ? 1.5 : 1.5,
        shapeProperties: {
          borderDashes: dn.collapsed ? [4, 3] : isIndex,
          borderRadius: dn.data.type === 'source' ? 0 : 0,
        },
      }
      return node as unknown as Node
    }),
  )

  const edges = new DataSet<Edge>(
    displayEdges.map((e, i) => {
      const srcNode = nodeById.get(e.source)
      const sourceColor = edgeColorFromSource(srcNode?.type)
      const edge: Record<string, unknown> = {
        id: e.id || `edge-${i}`,
        from: e.source,
        to: e.target,
        arrows: { to: { enabled: true, scaleFactor: 0.6 } },
        smooth: { enabled: true, type: 'cubicBezier', forceDirection: 'horizontal', roundness: 0.45 },
        color: {
          color: sourceColor,
          highlight: sourceColor,
          hover: sourceColor,
          opacity: 0.85,
        },
        width: 1.4,
      }
      return edge as unknown as Edge
    }),
  )

  return { nodes, edges, tooltips }
}

const NETWORK_OPTIONS: Options = {
  layout: { improvedLayout: false },
  physics: { enabled: false },
  interaction: {
    zoomView: false,
    dragView: true,
    dragNodes: false,
    hover: true,
    tooltipDelay: 300,
    navigationButtons: false,
    keyboard: { enabled: false },
  },
}

function bindTooltipHandlers(
  net: Network,
  tooltip: HTMLDivElement,
  getTooltips: () => Map<string, string>,
): () => void {
  const show = (nodeId: string, x: number, y: number) => {
    const html = getTooltips().get(nodeId)
    if (!html) return
    tooltip.innerHTML = html
    tooltip.style.display = 'block'
    tooltip.style.left = `${x + 14}px`
    tooltip.style.top = `${y + 14}px`
  }
  const hide = () => { tooltip.style.display = 'none' }

  const onHoverNode = (params: { node: string | number; pointer?: { DOM: { x: number; y: number } } }) => {
    const p = params.pointer?.DOM
    if (p) show(String(params.node), p.x, p.y)
  }

  net.on('hoverNode', onHoverNode)
  net.on('blurNode', hide)
  return () => {
    net.off('hoverNode', onHoverNode)
    net.off('blurNode', hide)
    hide()
  }
}

interface Props {
  lineage: LineageGraph
  parameters?: ModelParameter[]
  kommuneId?: number
  onParametersUpdated?: () => void
  embedded?: boolean
}

export default function LineageFlowDiagram({
  lineage,
  parameters = [],
  kommuneId,
  onParametersUpdated,
  embedded = false,
}: Props) {
  const containerRef = useRef<HTMLDivElement>(null)
  const canvasWrapRef = useRef<HTMLDivElement>(null)
  const tooltipRef = useRef<HTMLDivElement>(null)
  const networkRef = useRef<Network | null>(null)
  const clickHandlerRef = useRef<(nodeId: string) => void>(() => {})
  const tooltipMapRef = useRef<Map<string, string>>(new Map())
  const tooltipCleanupRef = useRef<(() => void) | null>(null)
  const [networkReady, setNetworkReady] = useState(false)

  const [hiddenTypes, setHiddenTypes] = useState<Set<LineageNodeType>>(
    () => new Set(DEFAULT_HIDDEN_TYPES),
  )
  // Klick-Overrides gegenüber der Standard-Regel (alles ausgeklappt).
  const [expandedSet, setExpandedSet] = useState<Set<string>>(new Set())
  const [collapsedSet, setCollapsedSet] = useState<Set<string>>(new Set())

  const hasPathways = useMemo(
    () => lineage.nodes.some(n => n.type === 'pathway'),
    [lineage],
  )

  // Standard: ausgeklappt; ausgeblendete Typen werden beim Auffächern nie als
  // eingeklappt behandelt (sonst verschwänden ihre Teilbäume statt überbrückt zu werden).
  const isCollapsed = useCallback(
    (instanceId: string, node: LineageNodeData): boolean => {
      if (hiddenTypes.has(node.type)) return false
      if (expandedSet.has(instanceId)) return false
      return collapsedSet.has(instanceId)
    },
    [expandedSet, collapsedSet, hiddenTypes],
  )

  const toggleLegendType = useCallback((type: LineageNodeType) => {
    if (type === 'outcome') return
    setHiddenTypes(prev => {
      const next = new Set(prev)
      if (next.has(type)) next.delete(type)
      else next.add(type)
      return next
    })
  }, [])

  const { displayNodes, displayEdges } = useMemo(() => {
    const forest = unfoldToForest(lineage, isCollapsed)
    const visible = mergeDuplicates(bridgeHiddenTypes(forest, hiddenTypes))
    if (import.meta.env.DEV) assertForestInvariants(visible, 'diagram')
    const pos = forestLayout(visible)
    const nodes: DisplayNode[] = visible.nodes.map((tn: TreeNode) => {
      const p = pos.get(tn.instanceId) ?? { x: 0, y: 0 }
      return {
        id: tn.instanceId,
        data: tn.data,
        x: p.x,
        y: p.y,
        isTerminal: tn.data.type === 'outcome',
        collapsed: tn.collapsed,
        childCount: tn.childCount,
      }
    })
    const edges: DisplayEdge[] = visible.edges.map(e => ({
      id: e.id,
      source: e.source,
      target: e.target,
      label: e.label,
      meta: e.meta,
    }))
    return { displayNodes: nodes, displayEdges: edges }
  }, [lineage, hiddenTypes, isCollapsed])

  const fitNetwork = useCallback(() => {
    const net = networkRef.current
    if (!net) return
    requestAnimationFrame(() => {
      net.fit({ animation: { duration: 200, easingFunction: 'easeInOutQuad' } })
    })
  }, [])

  const syncNetworkSize = useCallback(() => {
    const el = containerRef.current
    const net = networkRef.current
    if (!el || !net) return false

    const rect = el.getBoundingClientRect()
    const width = Math.round(rect.width)
    const height = Math.round(rect.height)
    if (width < 20 || height < 20) return false

    net.setSize(`${width}px`, `${height}px`)
    net.redraw()
    return true
  }, [])

  const applySizeAndFit = useCallback(() => {
    if (syncNetworkSize()) fitNetwork()
  }, [syncNetworkSize, fitNetwork])

  const handleCanvasWheel = useCallback((e: WheelEvent) => {
    const net = networkRef.current
    const wrap = canvasWrapRef.current
    if (!net || !wrap) return

    e.preventDefault()
    e.stopPropagation()

    const rect = wrap.getBoundingClientRect()
    const dom = { x: e.clientX - rect.left, y: e.clientY - rect.top }
    const pointer = net.DOMtoCanvas(dom)
    const scaleOld = net.getScale()
    const factor = Math.exp(-e.deltaY * 0.002)
    const scaleNew = Math.min(6, Math.max(0.08, scaleOld * factor))
    const view = net.getViewPosition()
    const ratio = scaleNew / scaleOld
    net.moveTo({
      position: {
        x: pointer.x - (pointer.x - view.x) * ratio,
        y: pointer.y - (pointer.y - view.y) * ratio,
      },
      scale: scaleNew,
      animation: false,
    })
  }, [])

  const fitRevision = useMemo(
    () => `${lineage.nodes.length}|${lineage.edges.length}`,
    [lineage.nodes.length, lineage.edges.length],
  )

  const handleNodeClick = useCallback((nodeId: string) => {
    const tn = displayNodes.find(d => d.id === nodeId)
    if (!tn || tn.data.type === 'operator' || (tn.childCount ?? 0) === 0) return
    const currentlyCollapsed = !!tn.collapsed
    setExpandedSet(prev => {
      const next = new Set(prev)
      if (currentlyCollapsed) next.add(nodeId)
      else next.delete(nodeId)
      return next
    })
    setCollapsedSet(prev => {
      const next = new Set(prev)
      if (currentlyCollapsed) next.delete(nodeId)
      else next.add(nodeId)
      return next
    })
  }, [displayNodes])

  clickHandlerRef.current = handleNodeClick

  const expandAll = useCallback(() => {
    setExpandedSet(new Set())
    setCollapsedSet(new Set())
  }, [])

  const collapseAll = useCallback(() => {
    setExpandedSet(new Set())
    setCollapsedSet(new Set(pathwayInstanceIds(lineage)))
  }, [lineage])

  useEffect(() => {
    const el = containerRef.current
    if (!el) return

    const { nodes, edges, tooltips } = toVisData(displayNodes, displayEdges, parameters)
    tooltipMapRef.current = tooltips

    if (!networkRef.current) {
      const net = new Network(el, { nodes, edges }, NETWORK_OPTIONS)
      net.on('click', params => {
        if (params.nodes.length === 1) clickHandlerRef.current(String(params.nodes[0]))
      })
      networkRef.current = net
      setNetworkReady(true)
      const tip = tooltipRef.current
      if (tip) {
        tooltipCleanupRef.current?.()
        tooltipCleanupRef.current = bindTooltipHandlers(
          net,
          tip,
          () => tooltipMapRef.current,
        )
      }
    } else {
      const net = networkRef.current
      const scale = net.getScale()
      const position = net.getViewPosition()
      net.setData({ nodes, edges })
      net.moveTo({ scale, position, animation: false })
    }
  }, [displayNodes, displayEdges, parameters])

  useEffect(() => {
    const timers = [0, 100, 300].map(ms =>
      window.setTimeout(applySizeAndFit, ms),
    )
    return () => timers.forEach(window.clearTimeout)
  }, [fitRevision, applySizeAndFit])

  useEffect(() => {
    const wrap = canvasWrapRef.current
    if (!wrap) return
    wrap.addEventListener('wheel', handleCanvasWheel, { passive: false })
    return () => wrap.removeEventListener('wheel', handleCanvasWheel)
  }, [handleCanvasWheel, networkReady])

  useEffect(() => {
    if (!networkReady) return
    let cancelled = false
    let attempts = 0
    const trySync = () => {
      if (cancelled) return
      if (syncNetworkSize()) return
      if (attempts++ < 16) requestAnimationFrame(trySync)
    }
    trySync()
    return () => { cancelled = true }
  }, [networkReady, syncNetworkSize])

  useEffect(() => {
    const el = containerRef.current
    if (!el) return
    const ro = new ResizeObserver(() => syncNetworkSize())
    ro.observe(el)
    syncNetworkSize()
    return () => ro.disconnect()
  }, [syncNetworkSize])

  useEffect(() => () => {
    tooltipCleanupRef.current?.()
    tooltipCleanupRef.current = null
    networkRef.current?.destroy()
    networkRef.current = null
    setNetworkReady(false)
  }, [])

  return (
    <div className={`kap-lineage-wrap${embedded ? ' kap-lineage-wrap--embedded' : ''}`}>
      <div className="kap-lineage-toolbar">
        <div className="kap-lineage-legend">
          {LEGEND_GROUPS.map(group => (
            <div key={group.label} className="kap-lineage-legend-group">
              <span className="kap-lineage-legend-group-label">{group.label}</span>
              <div className="kap-lineage-legend-chips">
                {group.types.map(type => {
                  const pinned = type === 'outcome'
                  return (
                    <button
                      key={type}
                      type="button"
                      className={`kap-lineage-chip kap-lineage-node--${type}${group.rounded ? ' kap-lineage-chip--rounded' : ' kap-lineage-chip--square'}${hiddenTypes.has(type) ? ' is-off' : ''}`}
                      onClick={() => toggleLegendType(type)}
                      aria-pressed={!hiddenTypes.has(type)}
                      disabled={pinned}
                      title={pinned
                        ? 'Ergebnisse sind immer sichtbar'
                        : hiddenTypes.has(type)
                          ? `${LEGEND_LABELS[type]} einblenden`
                          : `${LEGEND_LABELS[type]} ausblenden`}
                    >
                      {LEGEND_LABELS[type]}
                    </button>
                  )
                })}
              </div>
            </div>
          ))}
        </div>
        <div className="kap-lineage-actions">
          {hasPathways && (
            <>
              <button type="button" className="kap-lineage-reset" onClick={expandAll}>
                Alles ausklappen
              </button>
              <button type="button" className="kap-lineage-reset" onClick={collapseAll}>
                Ketten einklappen
              </button>
            </>
          )}
        </div>
      </div>

      <div ref={canvasWrapRef} className="kap-lineage-canvas-wrap">
        <div ref={containerRef} className="kap-lineage-canvas" />
        {networkReady && (
          <LineageOperatorOverlays
            network={networkRef.current}
            displayNodes={displayNodes}
            displayEdges={displayEdges}
            parameters={parameters}
            kommuneId={kommuneId}
            onUpdated={onParametersUpdated}
          />
        )}
        <div ref={tooltipRef} className="kap-lineage-tooltip" role="tooltip" />
      </div>
    </div>
  )
}
