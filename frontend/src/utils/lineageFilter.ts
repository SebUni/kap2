import type { LineageGraph, LineageNodeData } from '../types'
import {
  COL_GAP,
  ROW_PAD,
  estimateNodeHeight,
  estimateNodeWidth,
} from './lineageLayout'

// Ein Wirkungsdiagramm hat eine einzige Ansicht: der Backend-DAG wird zu einem
// WALD aufgefächert (jeder Knoten hat höchstens EINEN Pfeil nach rechts; geteilte
// Eingaben werden je Zweig dupliziert). Wurzeln sind die Ergebnisknoten
// (KWRA-Index, natives Ergebnis, Monetärer Schaden). Beim Ausblenden von
// Detailstufen werden Kanten überbrückt (bridgeHiddenTypes) und entstehende
// Duplikate wieder verschmolzen (mergeDuplicates) — die Out-Grad-≤-1-Regel
// bleibt dabei immer erhalten.

/** Ergebnisknoten sind nie ausblendbar. */
export function isPinnedNode(node: LineageNodeData): boolean {
  return node.type === 'outcome'
}

/** Alle Ergebnisknoten (für Hervorhebung/Reihenfolge). */
export function findResultNodes(graph: LineageGraph): LineageNodeData[] {
  return graph.nodes.filter(n => n.type === 'outcome')
}

function combineLabels(a?: string | null, b?: string | null): string | undefined {
  const parts = [a, b].filter(Boolean) as string[]
  if (parts.length === 0) return undefined
  return parts.join(' · ')
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

function resultRank(n: LineageNodeData): number {
  const kind = n.meta?.result_kind as string | undefined
  if (kind === 'index') return 0
  if (kind === 'native') return 1
  if (kind === 'eur') return 2
  return 3
}

/** Wurzeln des Waldes: Knoten ohne ausgehende Kante (Ergebnisse zuerst sortiert). */
function findRoots(graph: LineageGraph): LineageNodeData[] {
  const hasOutgoing = new Set(graph.edges.map(e => e.source))
  const roots = graph.nodes.filter(n => !hasOutgoing.has(n.id))
  return roots.sort(
    (a, b) => resultRank(a) - resultRank(b) || a.id.localeCompare(b.id),
  )
}

/**
 * Fächert den DAG zu einem Wald auf: jeder Zweig dupliziert geteilte Eingaben
 * (Out-Grad ≤ 1 per Konstruktion). Eine Wurzel je Ergebnisknoten.
 */
export function unfoldToForest(
  graph: LineageGraph,
  isCollapsed: (instanceId: string, node: LineageNodeData) => boolean,
): TreeResult {
  const roots = findRoots(graph)
  if (roots.length === 0) return { nodes: [], edges: [] }

  const nodeById = new Map(graph.nodes.map(n => [n.id, n]))
  const incoming = new Map<string, { source: string; label?: string | null; meta?: Record<string, unknown> }[]>()
  for (const e of graph.edges) {
    if (!incoming.has(e.target)) incoming.set(e.target, [])
    incoming.get(e.target)!.push({ source: e.source, label: e.label, meta: e.meta })
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

  for (const root of roots) {
    visit(root.id, root.id, null, new Set([root.id]))
  }
  return { nodes, edges }
}

/**
 * Blendet Knotentypen aus, indem sie ÜBERBRÜCKT werden: die Kinder eines
 * ausgeblendeten Knotens hängen sich an dessen sichtbaren Vorfahren, Kanten-
 * Attribute (Label, Gewichts-Meta) werden dabei kombiniert. Ergebnisknoten
 * sind gepinnt und werden nie ausgeblendet.
 */
export function bridgeHiddenTypes(
  tree: TreeResult,
  hiddenTypes: ReadonlySet<string>,
): TreeResult {
  if (hiddenTypes.size === 0) return tree

  const children = new Map<string, TreeNode[]>()
  const roots: TreeNode[] = []
  for (const n of tree.nodes) {
    if (n.parentInstanceId === null) {
      roots.push(n)
    } else {
      if (!children.has(n.parentInstanceId)) children.set(n.parentInstanceId, [])
      children.get(n.parentInstanceId)!.push(n)
    }
  }
  const edgeByChild = new Map(tree.edges.map(e => [e.source, e]))

  const nodes: TreeNode[] = []
  const edges: TreeEdge[] = []
  const isHidden = (n: TreeNode) => hiddenTypes.has(n.data.type) && !isPinnedNode(n.data)

  interface Carried {
    label?: string | null
    meta?: Record<string, unknown>
  }

  function combineCarried(edge: TreeEdge | undefined, carried: Carried | null): Carried {
    if (!edge) return carried ?? {}
    return {
      label: combineLabels(edge.label, carried?.label) ?? null,
      meta: edge.meta ?? carried?.meta,
    }
  }

  function visit(n: TreeNode, effectiveParent: string | null, carried: Carried | null) {
    const ownEdge = edgeByChild.get(n.instanceId)
    if (isHidden(n) && effectiveParent !== null) {
      const next = combineCarried(ownEdge, carried)
      for (const c of children.get(n.instanceId) ?? []) visit(c, effectiveParent, next)
      return
    }
    nodes.push({ ...n, parentInstanceId: effectiveParent })
    if (effectiveParent !== null) {
      const merged = combineCarried(ownEdge, carried)
      edges.push({
        id: `te:${n.instanceId}`,
        source: n.instanceId,
        target: effectiveParent,
        label: merged.label ?? null,
        meta: merged.meta,
      })
    }
    for (const c of children.get(n.instanceId) ?? []) visit(c, n.instanceId, null)
  }

  for (const r of roots) visit(r, null, null)
  return { nodes, edges }
}

function edgeSignature(e: TreeEdge | undefined): string {
  if (!e) return ''
  const meta = (e.meta ?? {}) as Record<string, unknown>
  return [
    e.label ?? '',
    meta.op_kind ?? '',
    meta.weight ?? '',
    meta.parameter_id ?? '',
  ].join('|')
}

/**
 * Vereinfachung nach dem Ausblenden: Instanzen DESSELBEN Backend-Knotens, die
 * (nach Überbrückung bzw. vorherigen Merges) auf dasselbe Ziel zeigen, werden
 * zu einer Instanz verschmolzen — z. B. eine Quelle, die ohne die Zwischenwerte
 * mehrfach in dasselbe Ergebnis flösse, erscheint nur einmal mit einem Pfeil.
 * Tragen die verschmolzenen Kanten unterschiedliche mitgeführte Attribute
 * (z. B. Ketten-Gewichte ausgeblendeter Wirkungsketten), werden diese verworfen —
 * sie gehören zur ausgeblendeten Detailstufe. Fixpunkt-Iteration; Out-Grad ≤ 1
 * bleibt erhalten. Voll ausgeklappt greift der Merge nie (jeder Zweig hat eine
 * eigene Elternkette, Duplikate teilen nie ein Ziel).
 */
export function mergeDuplicates(tree: TreeResult): TreeResult {
  const nodes = new Map(tree.nodes.map(n => [n.instanceId, { ...n }]))
  let edges = tree.edges.map(e => ({ ...e }))

  let changed = true
  while (changed) {
    changed = false
    const edgeByChild = new Map(edges.map(e => [e.source, e]))
    const groups = new Map<string, TreeNode[]>()
    for (const n of nodes.values()) {
      if (n.parentInstanceId === null) continue
      const key = [n.parentInstanceId, n.data.id, n.collapsed ? 1 : 0].join('§')
      if (!groups.has(key)) groups.set(key, [])
      groups.get(key)!.push(n)
    }
    for (const group of groups.values()) {
      if (group.length < 2) continue
      group.sort((a, b) => a.instanceId.localeCompare(b.instanceId))
      const canonical = group[0]
      const dupIds = new Set(group.slice(1).map(d => d.instanceId))
      const sigs = new Set(group.map(n => edgeSignature(edgeByChild.get(n.instanceId))))
      for (const n of nodes.values()) {
        if (n.parentInstanceId && dupIds.has(n.parentInstanceId)) {
          n.parentInstanceId = canonical.instanceId
        }
      }
      edges = edges.filter(e => !dupIds.has(e.source))
      for (const e of edges) {
        if (dupIds.has(e.target)) e.target = canonical.instanceId
        if (e.source === canonical.instanceId && sigs.size > 1) {
          // Uneinheitliche Kanten-Attribute stammen aus ausgeblendeten Ebenen.
          e.label = null
          e.meta = undefined
        }
      }
      for (const d of dupIds) nodes.delete(d)
      changed = true
    }
  }
  return { nodes: [...nodes.values()], edges }
}

/** Instanz-IDs aller Wirkungsketten-Knoten (für „Alle Ketten ausklappen“). */
export function pathwayInstanceIds(graph: LineageGraph): string[] {
  const { nodes } = unfoldToForest(
    graph,
    (_id, node) => node.type === 'pathway',
  )
  return nodes.filter(n => n.data.type === 'pathway').map(n => n.instanceId)
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
  // Knoten sind an x ZENTRIERT: der Abstand zweier Spalten muss daher die halben
  // Breiten BEIDER Spalten überbrücken, sonst ragen breite Boxen (Wirkungsketten)
  // in schmale Nachbarspalten (Quellen, Operatoren) hinein.
  const xByCol = new Map<number, number>()
  let x = 0
  let prevHalf = 0
  sortedCols.forEach((col, i) => {
    const half = (colWidths.get(col) ?? 180) / 2
    if (i > 0) x += prevHalf + COL_GAP + half
    xByCol.set(col, x)
    prevHalf = half
  })
  return xByCol
}

const TREE_GAP = ROW_PAD * 3

/** Layout des Waldes: Spalten → x, Blatt-Cursor je Teilbaum → y (Wurzeln gestapelt). */
export function forestLayout(
  tree: TreeResult,
): Map<string, { x: number; y: number }> {
  const children = new Map<string, TreeNode[]>()
  const roots: TreeNode[] = []
  for (const n of tree.nodes) {
    if (n.parentInstanceId === null) {
      roots.push(n)
    } else {
      if (!children.has(n.parentInstanceId)) children.set(n.parentInstanceId, [])
      children.get(n.parentInstanceId)!.push(n)
    }
  }
  roots.sort((a, b) => resultRank(a.data) - resultRank(b.data))

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
  roots.forEach((r, i) => {
    if (i > 0) leafCursor += TREE_GAP
    place(r)
  })

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
  const roots: TreeNode[] = []
  for (const n of tree.nodes) {
    if (n.parentInstanceId === null) {
      roots.push(n)
    } else {
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
  roots.forEach((r, i) => {
    if (i > 0) leafCursor += TREE_GAP
    walk(r)
  })
  return Math.max(420, maxY + 80)
}

/**
 * Dev-Prüfung der Kern-Invarianten: Out-Grad ≤ 1 und Pfeile strikt
 * links→rechts (Spalte des Kindes < Spalte des Ziels).
 */
export function assertForestInvariants(tree: TreeResult, context: string): void {
  const nodeById = new Map(tree.nodes.map(n => [n.instanceId, n]))
  const outCount = new Map<string, number>()
  for (const e of tree.edges) {
    outCount.set(e.source, (outCount.get(e.source) ?? 0) + 1)
    const src = nodeById.get(e.source)
    const tgt = nodeById.get(e.target)
    if (src && tgt && src.data.column >= tgt.data.column) {
      console.warn(
        `[lineage:${context}] Kante nicht links→rechts: ${src.data.id} (Spalte ${src.data.column}) → ${tgt.data.id} (Spalte ${tgt.data.column})`,
      )
    }
  }
  for (const [id, count] of outCount) {
    if (count > 1) {
      console.warn(`[lineage:${context}] Out-Grad > 1 bei ${id} (${count} ausgehende Pfeile)`)
    }
  }
}
