"""Exportiert den echten Wirkungs-Lineage-Baum eines Risikos als statisches JSON
für das Landing-Wirkungsmechanismus-Widget (ChainWidget).

Der Graph kommt aus `lineage_graph.build_risk_lineage` (reine Katalog-Berechnung,
keine DB/HTTP nötig) und wird auf den **monetären** Ast geprunt: nur Knoten, von
denen aus der €-Outcome (`out:eur`) erreichbar ist, bleiben — der parallele
terminale KWRA-Index-Outcome (`out:index`) und rein indexspezifische Dekoration
fallen weg. Ergebnis: ein Baum mit genau einer Wurzel (`out:eur`), passend zur
`LineageFlowDiagram`-Invariante.

Nutzung:  python scripts/export_landing_lineage.py
Neu erzeugt:  ../frontend/src/pages/landing/data/telecom-lineage.json
"""
import json
import sys
from pathlib import Path

# Backend-Root (Elternverzeichnis von scripts/) importierbar machen.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services import lineage_graph  # noqa: E402

# „Erwartete jährliche Schäden an Telekommunikationsinfrastruktur" (monetär).
RISK_CODE = "EXPECTED_TELECOM_DAMAGE_EUR"
EUR_OUTCOME_ID = "out:eur"

OUT_FILE = (
    Path(__file__).resolve().parents[2]
    / "frontend" / "src" / "pages" / "landing" / "data" / "telecom-lineage.json"
)


def prune_to_eur_tree(graph: dict) -> dict:
    """Behalte nur Knoten, von denen aus `out:eur` über Kanten erreichbar ist
    (Vorfahren), plus `out:eur` selbst. Kappt den parallelen `out:index`-Ast."""
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    # Rückwärts-Adjazenz: target -> [sources]. Rückwärts-BFS von out:eur liefert
    # alle Vorfahren (= Knoten, die out:eur erreichen).
    parents: dict[str, list[str]] = {}
    for e in edges:
        parents.setdefault(e["target"], []).append(e["source"])

    keep: set[str] = set()
    stack = [EUR_OUTCOME_ID]
    while stack:
        nid = stack.pop()
        if nid in keep:
            continue
        keep.add(nid)
        stack.extend(parents.get(nid, []))

    kept_nodes = [n for n in nodes if n["id"] in keep]
    kept_edges = [e for e in edges if e["source"] in keep and e["target"] in keep]
    kept_group_ids = {n.get("collapse_group") for n in kept_nodes}
    kept_groups = [
        g for g in graph.get("collapse_groups", [])
        if g.get("id") in kept_group_ids
    ]
    return {"nodes": kept_nodes, "edges": kept_edges, "collapse_groups": kept_groups}


def main() -> None:
    graph = lineage_graph.build_risk_lineage(RISK_CODE)
    pruned = prune_to_eur_tree(graph)

    # Sanity: genau eine Wurzel (out:eur), und die ist es auch.
    sources = {e["source"] for e in pruned["edges"]}
    roots = [n["id"] for n in pruned["nodes"] if n["id"] not in sources]
    assert roots == [EUR_OUTCOME_ID], f"Erwartete einzige Wurzel {EUR_OUTCOME_ID}, gefunden: {roots}"

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(
        json.dumps(pruned, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"OK: {RISK_CODE} → {OUT_FILE.name}: "
        f"{len(pruned['nodes'])} Knoten (von {len(graph['nodes'])}), "
        f"{len(pruned['edges'])} Kanten, {len(pruned['collapse_groups'])} Gruppen"
    )


if __name__ == "__main__":
    main()
