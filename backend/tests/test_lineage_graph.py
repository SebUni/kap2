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
        ("auxiliary", catalog.AUXILIARY),
    ):
        for it in items:
            yield it["code"], _graph(it["code"], cat)


# ── (h) Sonstige-Ebenen: ehrliche Graphen ohne Normierung ──────────────────────

def test_auxiliary_graphs_are_honest():
    """Ratchet für alle Sonstige-Ebenen (Nutzer-Feedback Layer-Review).

    Jede Sonstige-Ebene zeigt (1) mindestens eine ECHTE benannte Quelle (nie
    den anonymen "Parameter/Modellannahme"-Kasten), (2) KEINEN Normierungs-
    Schritt und keinen Knoten "Normierter Wert" — die Karten zeigen Rohwerte —
    und (3) genau einen Ergebnisknoten mit dem Layer-Code. Zudem muss jeder
    AUXILIARY-Code einen AUX_LINEAGE-Eintrag haben (Vollständigkeits-Ratchet).
    """
    from app.data.lineage_operators import AUX_LINEAGE

    for a in catalog.AUXILIARY:
        code = a["code"]
        assert code in AUX_LINEAGE, f"{code}: AUX_LINEAGE-Eintrag fehlt"
        g = _graph(code, "auxiliary")
        nodes = {n["id"]: n for n in g["nodes"]}
        assert g["nodes"], f"{code}: leerer Graph"
        assert _is_acyclic(g), f"{code}: Zyklus im Graph"

        sources = [n for n in g["nodes"] if n["type"] == "source"]
        assert sources, f"{code}: keine Quell-Box im Graph"
        assert "src:param" not in nodes, \
            f"{code}: anonyme Parameter-Quelle statt benannter Datenquelle"

        for n in g["nodes"]:
            meta = n.get("meta") or {}
            assert meta.get("op_kind") != "norm", \
                f"{code}: Normierungs-Operator {n['id']} (Karte zeigt Rohwerte)"
            assert n["label"] != "Normierter Wert", \
                f"{code}: Knoten 'Normierter Wert' (Karte zeigt Rohwerte)"

        outs = [n for n in g["nodes"] if n["type"] == "outcome"]
        assert len(outs) == 1, f"{code}: erwartet genau einen Ergebnisknoten"
        assert (outs[0].get("meta") or {}).get("code") == code, \
            f"{code}: Ergebnisknoten ohne Layer-Code"

        for e in g["edges"]:
            assert e["source"] in nodes and e["target"] in nodes, \
                f"{code}: Kante mit unbekanntem Knoten {e}"
            assert nodes[e["source"]]["column"] < nodes[e["target"]]["column"], \
                f"{code}: Kante nicht links→rechts: {e['source']} → {e['target']}"


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
    """Der generische Formel-Fallback trägt das „Berechnung:“-Präfix.

    Nur so rendert das Frontend die Rezeptformel als LaTeX statt als Rohtext
    (Nutzer-Feedback: „clamp(Vulnerable + UHI·6 + …)“ war unlesbar).
    Synthetischer Unit-Test — der Fallback selbst wird durch den Honesty-
    Ratchet (test_indicator_graphs_are_honest) ausgedünnt, das Präfix-
    Verhalten muss trotzdem stabil bleiben.
    """
    from app.data.lineage_operators import formula_operators_for

    steps = formula_operators_for("__TEST__", "x + y")
    assert steps[0]["op_kind"] == "formula"
    assert steps[0].get("generic") is True
    assert steps[0]["note"].startswith("Berechnung: ")
    assert formula_operators_for("__TEST__", "")[0]["note"] == "Berechnung für __TEST__."


# ── (i) H/E/V-Indikatoren: ehrliche Operator-Ketten (Honesty-Ratchet) ──────────

# Codes, deren Diagramm noch den generischen "Formel"-Kasten zeigt.
# RATCHET: Diese Liste darf nur SCHRUMPFEN (Gleichheits-Assertion unten) —
# jeder abgearbeitete Code wird hier entfernt und erhält stattdessen einen
# expliziten FORMULA_OPERATORS-Eintrag, der der echten Rechnung in
# engine/indicators.py entspricht.
_GENERIC_FORMULA_REMAINING: set[str] = set()


# Indikatoren, deren Rezept nur ein fester Annahmewert ist — ehrlich als
# Platzhalter gekennzeichnet (op_kind constant, meta.placeholder).
_CONSTANT_INDICATORS: dict[str, list[str]] = {
    "hazards": [
        "OCEAN_WARMING", "OCEAN_ACIDIFICATION", "PERMAFROST_THAW",
        "TROPICAL_CYCLONE", "STORM_SURGE", "SALTWATER_INTRUSION",
        "COASTAL_EROSION", "CASCADE_EVENT",
    ],
    "vulnerabilities": [
        "CRITICAL_INFRA_CONDITION", "SUPPLY_CHAIN_DEPENDENCY",
        "REDUNDANCY_BACKUP", "INFRA_DEPENDENCY_CHAIN",
        "SALTWATER_INTRUSION_RISK", "AQUACULTURE_TECHNICAL_VULNERABILITY",
        "FISHERIES_MANAGEMENT_CAPACITY",
    ],
}


def test_constant_indicators_are_marked_placeholder():
    """Konstantwert-Indikatoren sind ehrlich als Platzhalter gekennzeichnet.

    Genau ein constant-Operator mit meta.placeholder, die Notiz benennt den
    Platzhalter-Charakter, und der Wert erscheint als benannter
    Parameterknoten. Kein anderer H/E/V-Code trägt die Kennzeichnung.
    """
    const_codes = {c for codes in _CONSTANT_INDICATORS.values() for c in codes}
    for cat, items in (
        ("hazards", catalog.HAZARDS),
        ("exposures", catalog.EXPOSURES),
        ("vulnerabilities", catalog.VULNERABILITIES),
    ):
        for it in items:
            code = it["code"]
            g = _graph(code, cat)
            nodes = {n["id"]: n for n in g["nodes"]}
            const_ops = [
                n for n in g["nodes"]
                if n["type"] == "operator"
                and (n.get("meta") or {}).get("op_kind") == "constant"
                and n["id"].startswith(f"op:constant:ind:{code}:")
            ]
            if code not in const_codes:
                assert not const_ops, f"{code}: unerwarteter Konstantwert-Operator"
                continue
            assert len(const_ops) == 1, f"{code}: erwartet genau einen constant-Operator"
            op = const_ops[0]
            meta = op.get("meta") or {}
            assert meta.get("placeholder") is True, f"{code}: placeholder-Flag fehlt"
            assert "Platzhalter" in meta.get("note", ""), \
                f"{code}: Notiz benennt den Platzhalter nicht"
            in_types = {
                nodes[e["source"]]["type"]
                for e in g["edges"] if e["target"] == op["id"]
            }
            assert "parameter" in in_types, \
                f"{code}: Konstantwert ohne benannten Parameterknoten"


def test_indicator_graphs_are_honest():
    """Ratchet für H/E/V-Diagramme (Schwester-Test zu test_auxiliary_graphs_are_honest).

    Der generische "Formel"-Kasten (formula_operators_for-Fallback,
    meta.generic) erklärt nichts — jeder Indikator soll explizite, der echten
    Rechnung in engine/indicators.py entsprechende Operator-Schritte zeigen.
    Die Gleichheits-Assertion verhindert beides: neue Codes ohne explizite
    Schritte UND stilles Zurückfallen bereits abgearbeiteter Codes.
    Risiko-Graphen betten die Indikator-Untergraphen ein und werden mitgeprüft.
    """
    offenders: set[str] = set()
    for _code, g in _all_graphs():
        for n in g["nodes"]:
            meta = n.get("meta") or {}
            if n["type"] == "operator" and meta.get("generic"):
                assert n["id"].startswith("op:formula:ind:"), \
                    f"generischer Operator mit unerwarteter ID {n['id']}"
                offenders.add(n["id"].split(":")[3])
    assert offenders == _GENERIC_FORMULA_REMAINING, (
        "Honesty-Ratchet verletzt.\n"
        f"Neu ohne explizite Schritte: {sorted(offenders - _GENERIC_FORMULA_REMAINING)}\n"
        f"Erledigt (aus Liste entfernen): {sorted(_GENERIC_FORMULA_REMAINING - offenders)}"
    )


def test_regional_inputs_use_cell_keys():
    """Regionale Rezept-Eingaben laufen durch die Zellkey-Maschinerie.

    Vorher zeigte z. B. LOW_FLOW_NIEDRIGWASSER eine nackte DWD-Quellbox,
    obwohl die Daten von PEGELONLINE stammen; der "Regionalwert abrufen"-
    Schritt und das Zwischenwert-Label fehlten ganz.
    """
    g = _graph("LOW_FLOW_NIEDRIGWASSER", "hazards")
    ids = {n["id"] for n in g["nodes"]}
    assert "int:low_flow_days" in ids, "Niedrigwasser-Zwischenknoten fehlt"
    assert "src:pegelonline" in ids, "PEGELONLINE-Quelle fehlt"
    assert "src:dwd" not in ids or any(
        n["id"] == "int:dry_index" for n in g["nodes"]
    ), "DWD-Quelle ohne zugehörige Kette"

    g = _graph("DROUGHT", "hazards")
    ids = {n["id"] for n in g["nodes"]}
    assert "int:drought_days" in ids, "Trockentage-Zwischenknoten fehlt"


# ── Beschreibungskonzept: Operator-Klassen + Tooltip-Komposition ───────────────

# Feste Taxonomie der Operator-Klassen (siehe lineage_operators.py-Docstring).
# Neue op_kinds müssen bewusst klassifiziert werden — kein Durchrutschen.
_ALLOWED_OP_KINDS = {
    # Zell-Ebene
    "count", "ratio", "neighbor", "distance", "distance_score", "mean",
    "lookup", "constant", "derived_index", "weighted_sum",
    # Arithmetik/Verkettung
    "add", "multiply", "divide", "max", "min", "scale_factor",
    "scaling", "multiplier", "formula", "norm",
    # Schicht B (Schadensfunktionen)
    "af", "gv", "damage_curve", "sum_cells", "p90", "intensity",
    # Expositions-Wirkungs-Kurve (RKI/Winklmayr): Summe über die Sommerwochen
    "erf",
}

# Kürzel, die in Tooltip-Titeln in Klammern an den ausgeschriebenen Namen
# angehängt werden dürfen — sonst sind Klammern im Titel verboten.
_TITLE_ABBREV_PARENS = ("(AF)", "(P90)", "(Σ)", "(TWI)", "(SVF)", "g(V̂)")

# Nackte Kürzel, die NIE allein als Titel stehen dürfen (Nutzer-Feedback:
# "Woher soll der Mandant wissen was AF bedeutet?").
_BARE_ABBREVS = {"AF", "g(V̂)", "P90", "Σ", "Σ Zellen", "TWI", "SVF"}


def test_operator_kind_taxonomy():
    for code, g in _all_graphs():
        for n in g["nodes"]:
            if n["type"] != "operator":
                continue
            kind = (n.get("meta") or {}).get("op_kind")
            assert kind in _ALLOWED_OP_KINDS, \
                f"{code}: unklassifizierter op_kind {kind!r} an {n['id']}"


def test_operator_tooltips_have_eingaben_line():
    """Jeder Operator mit fachlichen Eingaben listet sie im Tooltip.

    Die "Eingaben:"-Zeile wird maschinell aus den echten Kanten erzeugt
    (_enrich_tooltips komponiert IMMER) — dieser Test fixiert, dass kein
    handgeschriebener Tooltip die Komposition wieder aushebelt. Quell-Boxen
    (OSM/DWD/…) und vorgelagerte Operatoren zählen nicht als Eingaben
    (Nutzerwunsch: keine Quellen in Tooltips).
    """
    for code, g in _all_graphs():
        nodes = {n["id"]: n for n in g["nodes"]}
        for n in g["nodes"]:
            if n["type"] != "operator":
                continue
            preds = [
                nodes[e["source"]] for e in g["edges"]
                if e["target"] == n["id"] and e["source"] in nodes
            ]
            expects_line = any(
                p["type"] not in ("source", "operator") and p["label"]
                for p in preds
            )
            tooltip = (n.get("meta") or {}).get("tooltip", "")
            if expects_line:
                assert "Eingaben:" in tooltip, \
                    f"{code}: Operator {n['id']} ohne Eingaben-Zeile: {tooltip!r}"
            # nie eine leere Eingaben-Zeile
            for line in tooltip.split("\n"):
                if line.startswith("Eingaben:"):
                    assert line.removeprefix("Eingaben:").strip(), \
                        f"{code}: leere Eingaben-Zeile an {n['id']}"


def test_tooltips_contain_no_source_rows():
    """Keine "Quelle:"-Zeilen in Tooltips (Nutzerwunsch).

    Quellen stehen sichtbar als Boxen im Diagramm; Tooltips erklären nur
    die Rechnung.
    """
    for code, g in _all_graphs():
        for n in g["nodes"]:
            if n["type"] == "source":
                continue
            tooltip = (n.get("meta") or {}).get("tooltip", "")
            for line in tooltip.split("\n"):
                assert not line.strip().startswith("Quelle:"), \
                    f"{code}: Quellen-Zeile im Tooltip von {n['id']}: {line!r}"


def test_operator_titles_follow_style_rules():
    """Titelzeile: kein nacktes Kürzel, Klammern nur für Kürzel-Erklärungen."""
    for code, g in _all_graphs():
        for n in g["nodes"]:
            if n["type"] != "operator":
                continue
            tooltip = (n.get("meta") or {}).get("tooltip", "")
            title = tooltip.split("\n", 1)[0].strip()
            assert title, f"{code}: Operator {n['id']} ohne Titel"
            assert title not in _BARE_ABBREVS, \
                f"{code}: nacktes Kürzel als Titel an {n['id']}: {title!r}"
            if "(" in title:
                assert any(a in title for a in _TITLE_ABBREV_PARENS), \
                    f"{code}: unerlaubte Klammer im Titel an {n['id']}: {title!r}"


if __name__ == "__main__":
    test_lineage_specs_cover_impacts()
    test_lineage_spec_hazards_exist()
    test_all_risk_graphs_invariants()
    test_result_contract_per_category()
    test_no_screening_norm_on_eur_paths()
    test_cost_operator_wiring()
    test_all_graph_parameters_available()
    test_indicator_graphs_have_norm_result()
    test_auxiliary_graphs_are_honest()
    test_scaling_without_registry_param_has_parameter_node()
    test_formula_fallback_tooltips_latexifiable()
    test_indicator_graphs_are_honest()
    test_regional_inputs_use_cell_keys()
    test_constant_indicators_are_marked_placeholder()
    test_operator_kind_taxonomy()
    test_operator_tooltips_have_eingaben_line()
    test_tooltips_contain_no_source_rows()
    test_operator_titles_follow_style_rules()
    print("Alle lineage_graph-Tests OK")
