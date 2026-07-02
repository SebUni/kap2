import type { LineageEdgeData, LineageGraph, LineageNodeData } from '../types'
import {
  COL_GAP,
  ROW_PAD,
  estimateNodeHeight,
  estimateNodeWidth,
} from './lineageLayout'

export function findTerminalNode(graph: LineageGraph): LineageNodeData | undefined {
  const outcome = graph.nodes.find(n => n.type === 'outcome' && n.id.startsWith('out:'))
  if (outcome) return outcome
  const outcomes = graph.nodes.filter(n => n.type === 'outcome')
  if (outcomes.length === 1) return outcomes[0]
  if (outcomes.length > 1) {
    return outcomes.reduce((a, b) => (a.column >= b.column ? a : b))
  }
  return graph.nodes.filter(n => n.type === 'norm').sort((a, b) => b.column - a.column)[0]
}

export function isPinnedNode(node: LineageNodeData, graph: LineageGraph): boolean {
  const terminal = findTerminalNode(graph)
  if (terminal && node.id === terminal.id) return true
  if (node.type === 'aggregation') return true
  return false
}

function combineLabels(a?: string | null, b?: string | null): string | undefined {
  const parts = [a, b].filter(Boolean) as string[]
  if (parts.length === 0) return undefined
  return parts.join(' · ')
}

function contractHiddenNodes(
  nodes: LineageNodeData[],
  edges: LineageEdgeData[],
  hidden: Set<string>,
  graph: LineageGraph,
): LineageEdgeData[] {
  const nodeById = new Map(nodes.map(n => [n.id, n]))
  const activeHidden = new Set(
    [...hidden].filter(id => {
      const n = nodeById.get(id)
      return n && !isPinnedNode(n, graph)
    }),
  )
  if (activeHidden.size === 0) return edges

  const out = new Map<string, LineageEdgeData[]>()
  for (const e of edges) {
    if (!out.has(e.source)) out.set(e.source, [])
    out.get(e.source)!.push(e)
  }

  const result: LineageEdgeData[] = []
  const seen = new Set<string>()

  function addEdge(
    source: string,
    target: string,
    label?: string,
    parameter_id?: string | null,
    meta?: Record<string, unknown>,
  ) {
    const key = `${source}|${target}|${label ?? ''}`
    if (seen.has(key)) return
    seen.add(key)
    const edge: LineageEdgeData = {
      id: `bridge:${source}:${target}:${result.length}`,
      source,
      target,
      label: label ?? null,
      parameter_id: parameter_id ?? null,
    }
    if (meta) edge.meta = meta
    result.push(edge)
  }

  function expandForward(
    startId: string,
    labelSoFar?: string,
    paramId?: string | null,
    edgeMeta?: Record<string, unknown>,
    visited: Set<string> = new Set(),
  ): { target: string; label?: string; parameter_id?: string | null; meta?: Record<string, unknown> }[] {
    if (visited.has(startId)) return []
    visited.add(startId)

    if (!activeHidden.has(startId)) {
      return [{ target: startId, label: labelSoFar, parameter_id: paramId, meta: edgeMeta }]
    }

    const outs = out.get(startId) ?? []
    const acc: { target: string; label?: string; parameter_id?: string | null; meta?: Record<string, unknown> }[] = []
    for (const e of outs) {
      const nextLabel = combineLabels(labelSoFar, e.label)
      const nextParam = e.parameter_id ?? paramId
      const nextMeta = e.meta ?? edgeMeta
      acc.push(...expandForward(e.target, nextLabel, nextParam, nextMeta, visited))
    }
    return acc
  }

  for (const e of edges) {
    if (!activeHidden.has(e.source) && !activeHidden.has(e.target)) {
      addEdge(e.source, e.target, e.label ?? undefined, e.parameter_id, e.meta)
      continue
    }
    if (activeHidden.has(e.source)) continue
    if (!activeHidden.has(e.source) && activeHidden.has(e.target)) {
      for (const t of expandForward(e.target, e.label ?? undefined, e.parameter_id, e.meta)) {
        addEdge(e.source, t.target, t.label, t.parameter_id, t.meta)
      }
    }
  }

  return result
}

export interface FilteredLineage {
  nodes: LineageNodeData[]
  edges: LineageEdgeData[]
}

export function filterHiddenTypes(
  filtered: FilteredLineage,
  fullGraph: LineageGraph,
  hiddenTypes: ReadonlySet<string>,
): FilteredLineage {
  if (hiddenTypes.size === 0) return filtered

  const hidden = new Set(
    filtered.nodes
      .filter(n => hiddenTypes.has(n.type))
      .map(n => n.id),
  )
  if (hidden.size === 0) return filtered

  const visibleNodes = filtered.nodes.filter(
    n => !hidden.has(n.id) || isPinnedNode(n, fullGraph),
  )
  const visibleIds = new Set(visibleNodes.map(n => n.id))
  const bridged = contractHiddenNodes(filtered.nodes, filtered.edges, hidden, fullGraph)
  const edges = bridged.filter(e => visibleIds.has(e.source) && visibleIds.has(e.target))

  return { nodes: visibleNodes, edges }
}

export function filterLineageGraph(
  graph: LineageGraph,
  focusColumn: number | null,
): FilteredLineage {
  const hidden = new Set<string>()
  if (focusColumn !== null) {
    for (const n of graph.nodes) {
      if (n.column < focusColumn) hidden.add(n.id)
    }
  }

  const visibleNodes = graph.nodes.filter(n => !hidden.has(n.id) || isPinnedNode(n, graph))
  const visibleIds = new Set(visibleNodes.map(n => n.id))
  const bridged = contractHiddenNodes(graph.nodes, graph.edges, hidden, graph)
  const edges = bridged.filter(e => visibleIds.has(e.source) && visibleIds.has(e.target))

  return { nodes: visibleNodes, edges }
}

function columnXPositions(nodes: LineageNodeData[]): Map<number, number> {
  const byCol = new Map<number, LineageNodeData[]>()
  for (const n of nodes) {
    if (!byCol.has(n.column)) byCol.set(n.column, [])
    byCol.get(n.column)!.push(n)
  }
  const sortedCols = [...byCol.keys()].sort((a, b) => a - b)
  const colWidths = new Map<number, number>()
  for (const col of sortedCols) {
    const list = byCol.get(col)!
    colWidths.set(col, Math.max(72, ...list.map(estimateNodeWidth)) + 12)
  }
  const xByCol = new Map<number, number>()
  let x = 0
  for (const col of sortedCols) {
    xByCol.set(col, x)
    x += (colWidths.get(col) ?? 180) + COL_GAP
  }
  return xByCol
}

const ROW_HEIGHT = 52

function hasLayoutRow(n: LineageNodeData): boolean {
  return typeof n.meta?.layout_row === 'number'
}

function layoutRowOf(n: LineageNodeData): number {
  const row = n.meta?.layout_row
  if (typeof row === 'number') return row
  if (n.type === 'intermediate' && n.id.startsWith('int:')) {
    return n.id.charCodeAt(4) % 12
  }
  return 0
}

export function assignColumnPositions(
  nodes: LineageNodeData[],
  viewport?: { width: number; height: number },
): Map<string, { x: number; y: number }> {
  const xByCol = columnXPositions(nodes)
  const positions = new Map<string, { x: number; y: number }>()

  const withRow = nodes.filter(hasLayoutRow)
  const withoutRow = nodes.filter(n => !hasLayoutRow(n))

  if (withRow.length) {
    const rows = [...new Set(withRow.map(layoutRowOf))].sort((a, b) => a - b)
    const rowOffset = -(rows.length - 1) * ROW_HEIGHT / 2
    for (const n of withRow) {
      const y = rowOffset + layoutRowOf(n) * ROW_HEIGHT
      positions.set(n.id, {
        x: xByCol.get(n.column) ?? n.column * 130,
        y,
      })
    }
  }

  const byCol = new Map<number, LineageNodeData[]>()
  for (const n of withoutRow) {
    if (!byCol.has(n.column)) byCol.set(n.column, [])
    byCol.get(n.column)!.push(n)
  }

  for (const [col, list] of byCol) {
    const sorted = [...list].sort((a, b) => a.label.localeCompare(b.label, 'de'))
    const heights = sorted.map(n => estimateNodeHeight(n) + ROW_PAD)
    const totalH = heights.reduce((a, b) => a + b, 0)
    let yCursor = -totalH / 2
    sorted.forEach((n, i) => {
      const h = heights[i]
      yCursor += h / 2
      positions.set(n.id, { x: xByCol.get(col) ?? col * 130, y: yCursor })
      yCursor += h / 2
    })
  }

  return positions
}

export interface TreeNode {
  instanceId: string
  parentInstanceId: string | null
  data: LineageNodeData
  childCount: number
  collapsed: boolean
}

export interface TreeEdge {
  id: string
  source: string
  target: string
  label?: string | null
  meta?: Record<string, unknown>
}

export interface TreeResult {
  nodes: TreeNode[]
  edges: TreeEdge[]
}

export function unfoldToTree(
  graph: LineageGraph,
  isCollapsed: (instanceId: string, node: LineageNodeData) => boolean,
): TreeResult {
  const terminal = findTerminalNode(graph)
  if (!terminal) return { nodes: [], edges: [] }

  const nodeById = new Map(graph.nodes.map(n => [n.id, n]))
  const incoming = new Map<string, LineageEdgeData[]>()
  for (const e of graph.edges) {
    if (!incoming.has(e.target)) incoming.set(e.target, [])
    incoming.get(e.target)!.push(e)
  }

  const nodes: TreeNode[] = []
  const edges: TreeEdge[] = []

  function visit(
    origId: string,
    instanceId: string,
    parentInstanceId: string | null,
    pathOrigIds: Set<string>,
  ) {
    const data = nodeById.get(origId)
    if (!data) return
    const ins = incoming.get(origId) ?? []
    const collapsed = ins.length > 0 && isCollapsed(instanceId, data)
    nodes.push({
      instanceId,
      parentInstanceId,
      data,
      childCount: ins.length,
      collapsed,
    })
    if (collapsed) return
    for (const e of ins) {
      if (pathOrigIds.has(e.source)) continue
      const childInstance = `${instanceId}>${e.source}`
      const childPath = new Set(pathOrigIds)
      childPath.add(e.source)
      edges.push({
        id: `te:${childInstance}`,
        source: childInstance,
        target: instanceId,
        label: e.label ?? null,
        meta: e.meta,
      })
      visit(e.source, childInstance, instanceId, childPath)
    }
  }

  visit(terminal.id, terminal.id, null, new Set([terminal.id]))
  return { nodes, edges }
}

export function pathwayInstanceIds(graph: LineageGraph): string[] {
  const { nodes } = unfoldToTree(
    graph,
    (_id, node) => node.type === 'pathway',
  )
  return nodes.filter(n => n.data.type === 'pathway').map(n => n.instanceId)
}

export function treeLayout(
  tree: TreeResult,
  viewport?: { width: number; height: number },
): Map<string, { x: number; y: number }> {
  const children = new Map<string, TreeNode[]>()
  let root: TreeNode | undefined
  for (const n of tree.nodes) {
    if (n.parentInstanceId === null) {
      root = n
    } else {
      if (!children.has(n.parentInstanceId)) children.set(n.parentInstanceId, [])
      children.get(n.parentInstanceId)!.push(n)
    }
  }

  const xByCol = columnXPositions(tree.nodes.map(n => n.data))

  const yById = new Map<string, number>()
  let leafCursor = 0

  function place(n: TreeNode): number {
    const ch = n.collapsed ? [] : (children.get(n.instanceId) ?? [])
    let y: number
    if (ch.length === 0) {
      const gap = estimateNodeHeight(n.data) + ROW_PAD
      y = leafCursor + gap / 2
      leafCursor += gap
    } else {
      const ys = ch.map(place)
      y = (Math.min(...ys) + Math.max(...ys)) / 2
    }
    yById.set(n.instanceId, y)
    return y
  }
  if (root) place(root)

  const positions = new Map<string, { x: number; y: number }>()
  for (const n of tree.nodes) {
    positions.set(n.instanceId, {
      x: xByCol.get(n.data.column) ?? n.data.column * 130,
      y: yById.get(n.instanceId) ?? 0,
    })
  }
  return positions
}

export function layoutContentHeight(tree: TreeResult): number {
  let maxY = 0
  const children = new Map<string, TreeNode[]>()
  for (const n of tree.nodes) {
    if (n.parentInstanceId) {
      if (!children.has(n.parentInstanceId)) children.set(n.parentInstanceId, [])
      children.get(n.parentInstanceId)!.push(n)
    }
  }
  let leafCursor = 0
  function walk(n: TreeNode) {
    const ch = n.collapsed ? [] : (children.get(n.instanceId) ?? [])
    if (ch.length === 0) {
      leafCursor += estimateNodeHeight(n.data) + ROW_PAD
      maxY = Math.max(maxY, leafCursor)
    } else {
      ch.forEach(walk)
    }
  }
  const root = tree.nodes.find(n => n.parentInstanceId === null)
  if (root) walk(root)
  return Math.max(420, maxY + 80)
}
