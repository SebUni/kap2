"""Tests des Wirkungsdiagramm-Graphaufbaus (lineage_graph, Zwei-Schichten-Umbau).

Deckt ab:
  (a) LINEAGE_SPECS spiegeln die Impact-Registrierungen (Key-Gleichheit je Modul).
  (b) Struktur-Invarianten JEDES Risiko-Graphen: azyklisch, Spalten strikt
      links→rechts (col(src) < col(tgt) für jede Kante), keine "Mittelung"-Reste,
      op:max:index vorhanden, Kanten nur zwischen existierenden Knoten.
  (c) Ergebnis-Kontrakt je Risikokategorie: health/environment → Index + native + €
      (mit Pfad native → Kostensatz → €); monetär → Index + € ohne native; flat →
      Index + native + € UND Pfad Index → … → €; index_only → nur Index;
      indirekt/restoration/konsolidiert → Index + €.
  (d) Kein Screening-Norm-Operator auf Pfaden in out:eur bei Schadensfunktions-Risiken.
  (e) Kostensatz-Operator trägt die richtige parameter_id und den Katalog-Kostensatz.
  (f) Alle im Graph referenzierten parameter_ids kommen im risiko-gefilterten
      Parameter-Endpoint vor (inkl. globaler impact.*-Parameter).
  (g) Indikator-Graphen enden in einem Ergebnisknoten "Normierter Wert".

Läuft mit pytest oder direkt: ``python tests/test_lineage_graph.py``.
"""

from __future__ import annotations

from collections import deque

from app.data import catalog
from app.services import lineage_graph, parameter_registry
from app.services.engine import impact
from app.services.engine.impact.environment import ENVIRONMENT_IMPACTS
from app.services.engine.impact.environment import LINEAGE_SPECS as ENV_SPECS
from app.services.engine.impact.health import HEALTH_IMPACTS
from app.services.engine.impact.health import LINEAGE_SPECS as HEALTH_SPECS
from app.services.engine.impact.monetary import MONETARY_IMPACTS
from app.services.engine.impact.monetary import LINEAGE_SPECS as MONETARY_SPECS


# ── (a) LINEAGE_SPECS ↔ Impact-Registrierung ───────────────────────────────────

def test_lineage_specs_cover_impacts():
    assert set(HEALTH_SPECS) == set(HEALTH_IMPACTS)
    assert set(MONETARY_SPECS) == set(MONETARY_IMPACTS)
    assert set(ENV_SPECS) == set(ENVIRONMENT_IMPACTS)


def test_lineage_spec_hazards_exist():
    for specs in (HEALTH_SPECS, MONETARY_SPECS, ENV_SPECS):
        for code, spec in specs.items():
            driver = spec["driver"]
            hazards = driver.get("hazards", []) + driver.get("event_hazards", [])
            if driver.get("hazard"):
                hazards.append(driver["hazard"])
            for h in hazards:
                assert h in catalog.HAZARDS_BY_CODE, f"{code}: Hazard {h} unbekannt"


# ── Helfer ─────────────────────────────────────────────────────────────────────

def _graph(code: str, category: str = "risks") -> dict:
    return lineage_graph.build_for_layer(code, category)


def _results(g: dict) -> dict[str, dict]:
    return {
        (n.get("meta") or {}).get("result_kind"): n
        for n in g["nodes"] if n["type"] == "outcome"
    }


def _has_path(g: dict, src: str, dst: str) -> bool:
    adj: dict[str, list[str]] = {}
    for e in g["edges"]:
        adj.setdefault(e["source"], []).append(e["target"])
    seen, stack = set(), [src]
    while stack:
        u = stack.pop()
        if u == dst:
            return True
        if u in seen:
            continue
        seen.add(u)
        stack.extend(adj.get(u, []))
    return False


def _is_acyclic(g: dict) -> bool:
    indeg: dict[str, int] = {n["id"]: 0 for n in g["nodes"]}
    adj: dict[str, list[str]] = {}
    for e in g["edges"]:
        indeg[e["target"]] += 1
        adj.setdefault(e["source"], []).append(e["target"])
    q = deque([nid for nid, d in indeg.items() if d == 0])
    seen = 0
    while q:
        u = q.popleft()
        seen += 1
        for v in adj.get(u, []):
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return seen == len(g["nodes"])


# ── (b) Struktur-Invarianten aller Risiko-Graphen ──────────────────────────────

def test_all_risk_graphs_invariants():
    for risk in catalog.RISKS:
        code = risk["code"]
        g = _graph(code)
        nodes = {n["id"]: n for n in g["nodes"]}
        assert g["nodes"], f"{code}: leerer Graph"
        assert _is_acyclic(g), f"{code}: Zyklus im Graph"
        for e in g["edges"]:
            assert e["source"] in nodes and e["target"] in nodes, \
                f"{code}: Kante mit unbekanntem Knoten {e}"
            assert nodes[e["source"]]["column"] < nodes[e["target"]]["column"], \
                f"{code}: Kante nicht links→rechts: {e['source']} → {e['target']}"
        txt = str(g)
        assert "Mittelung" not in txt and "Durchschnitt" not in txt, \
            f"{code}: Mittelungs-Rest im Graph"
        if catalog.build_pathways(risk):
            assert "op:max:index" in nodes, f"{code}: Maximum-Operator fehlt"
            assert (nodes["op:max:index"].get("meta") or {}).get("op_kind") == "max"


# ── (c) Ergebnis-Kontrakt je Kategorie ─────────────────────────────────────────

def test_result_contract_per_category():
    for risk in catalog.RISKS:
        code = risk["code"]
        kind = impact.lineage_kind(risk)
        g = _graph(code)
        res = _results(g)
        assert "index" in res, f"{code}: KWRA-Index-Ergebnis fehlt"
        if kind == "index_only":
            assert set(res) == {"index"}, f"{code}: index_only darf nur Index haben"
            continue
        assert "eur" in res, f"{code} ({kind}): €-Ergebnis fehlt"
        if kind in ("health", "environment", "flat"):
            assert "native" in res, f"{code} ({kind}): natives Ergebnis fehlt"
            assert _has_path(g, "out:native", f"op:cost:{code}"), \
                f"{code}: Pfad native → Kostensatz fehlt"
            assert _has_path(g, f"op:cost:{code}", "out:eur"), \
                f"{code}: Pfad Kostensatz → € fehlt"
        else:
            assert "native" not in res, \
                f"{code} ({kind}): unerwartetes natives Ergebnis (Outcome ist bereits €)"
        if kind == "flat":
            assert _has_path(g, "out:index", "out:eur"), \
                f"{code}: flat-€ muss sich aus dem Index ableiten"
        else:
            assert not _has_path(g, "out:index", "out:eur"), \
                f"{code} ({kind}): € darf nicht vom Screening-Index abhängen"


# ── (d) Keine Screening-Normierung im Schicht-B-Zweig ──────────────────────────

def test_no_screening_norm_on_eur_paths():
    for risk in catalog.RISKS:
        if not impact.has(risk["code"]):
            continue
        g = _graph(risk["code"])
        nodes = {n["id"]: n for n in g["nodes"]}
        norm_ops = [
            nid for nid, n in nodes.items()
            if n["type"] == "operator" and (n.get("meta") or {}).get("op_kind") == "norm"
        ]
        for nid in norm_ops:
            assert not _has_path(g, nid, "out:eur"), \
                f"{risk['code']}: Screening-Norm-Operator {nid} auf €-Pfad"


# ── (e) Kostensatz-Operator ────────────────────────────────────────────────────

def test_cost_operator_wiring():
    for risk in catalog.RISKS:
        kind = impact.lineage_kind(risk)
        if kind not in ("health", "environment", "flat"):
            continue
        code = risk["code"]
        g = _graph(code)
        nodes = {n["id"]: n for n in g["nodes"]}
        op = nodes.get(f"op:cost:{code}")
        assert op is not None, f"{code}: Kostensatz-Operator fehlt"
        meta = op.get("meta") or {}
        assert meta.get("parameter_id") == f"risks.{code}.cost_per_outcome"
        assert meta.get("value") == catalog.risk_default_cost_per_outcome(risk)


# ── (f) Parameter-Abdeckung des gefilterten Endpoints ──────────────────────────

def test_all_graph_parameters_available():
    for risk in catalog.RISKS:
        code = risk["code"]
        g = _graph(code)
        available = {
            p["id"]
            for p in parameter_registry.catalog_parameters(
                layer_code=code, layer_category="risks")
        }
        referenced: set[str] = set()
        for n in g["nodes"]:
            m = n.get("meta") or {}
            for k in ("parameter_id", "param_min_id", "param_max_id"):
                if m.get(k):
                    referenced.add(m[k])
        for e in g["edges"]:
            if e.get("parameter_id"):
                referenced.add(e["parameter_id"])
            m = e.get("meta") or {}
            if m.get("parameter_id"):
                referenced.add(m["parameter_id"])
        missing = referenced - available
        assert not missing, f"{code}: Parameter fehlen im Endpoint: {sorted(missing)}"


# ── (g) Indikator-Graphen enden im Ergebnisknoten ──────────────────────────────

def test_indicator_graphs_have_norm_result():
    samples = [
        ("HEAT_WAVE", "hazards"),
        (catalog.EXPOSURES[0]["code"], "exposures"),
        (catalog.VULNERABILITIES[0]["code"], "vulnerabilities"),
    ]
    for code, cat in samples:
        g = _graph(code, cat)
        nodes = {n["id"]: n for n in g["nodes"]}
        res = [n for n in g["nodes"] if n["type"] == "outcome"]
        assert res, f"{code}: Ergebnisknoten fehlt"
        for e in g["edges"]:
            assert nodes[e["source"]]["column"] < nodes[e["target"]]["column"], \
                f"{code}: Kante nicht links→rechts"


def _all_graphs():
    for risk in catalog.RISKS:
        yield risk["code"], _graph(risk["code"])
    for cat, items in (
        ("hazards", catalog.HAZARDS),
        ("exposures", catalog.EXPOSURES),
        ("vulnerabilities", catalog.VULNERABILITIES),
    ):
        for it in items:
            yield it["code"], _graph(it["code"], cat)


def test_scaling_without_registry_param_has_parameter_node():
    """Nicht editierbare Skalierungs-Konstanten erscheinen als Parameterknoten.

    Jeder scaling/scale_factor-Operator ohne ``parameter_id`` (Modellkonstante,
    kein Registry-Override möglich) muss einen eingehenden Parameterknoten
    haben, der den Faktor benannt zeigt.
    """
    for code, g in _all_graphs():
        nodes = {n["id"]: n for n in g["nodes"]}
        for n in g["nodes"]:
            meta = n.get("meta") or {}
            if n["type"] != "operator":
                continue
            if meta.get("op_kind") not in ("scaling", "scale_factor"):
                continue
            if meta.get("parameter_id"):
                continue
            in_types = {
                nodes[e["source"]]["type"]
                for e in g["edges"] if e["target"] == n["id"]
            }
            assert "parameter" in in_types, \
                f"{code}: Skalierung {n['id']} ohne Parameterknoten"


def test_formula_fallback_tooltips_latexifiable():
    """Generische Formel-Operatoren tragen das „Berechnung:“-Präfix.

    Nur so rendert das Frontend die Rezeptformel als LaTeX statt als Rohtext
    (Nutzer-Feedback: „clamp(Vulnerable + UHI·6 + …)“ war unlesbar).
    """
    checked = 0
    for code, g in _all_graphs():
        for n in g["nodes"]:
            meta = n.get("meta") or {}
            if meta.get("op_kind") != "formula" or not n["id"].startswith("op:formula:ind:"):
                continue
            tooltip = meta.get("tooltip", "")
            assert "Berechnung" in tooltip, \
                f"{code}: Formel-Operator {n['id']} ohne Berechnung:-Zeile: {tooltip!r}"
            checked += 1
    assert checked > 0, "kein generischer Formel-Operator gefunden"


if __name__ == "__main__":
    test_lineage_specs_cover_impacts()
    test_lineage_spec_hazards_exist()
    test_all_risk_graphs_invariants()
    test_result_contract_per_category()
    test_no_screening_norm_on_eur_paths()
    test_cost_operator_wiring()
    test_all_graph_parameters_available()
    test_indicator_graphs_have_norm_result()
    test_scaling_without_registry_param_has_parameter_node()
    test_formula_fallback_tooltips_latexifiable()
    print("Alle lineage_graph-Tests OK")
