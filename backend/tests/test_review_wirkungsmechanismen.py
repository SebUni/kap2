"""Konsistenztests zu REVIEW_WIRKUNGSMECHANISMEN.md §5 (Info-Fenster ⇄ Rechnung).

Deckt ab:
  * B6.1 — Skalierungs-Tooltip ist scale-abhängig (pop/area/flat).
  * B6.6 — jede kuratierte Wirkungskette (CURATED_PATHWAYS) ist wohlgeformt, begründet
           und liefert einen Anzeigetitel (die Kuratierung ist die Quelle der Wahrheit,
           PATHWAY_DESCRIPTIONS nur noch optionaler Titel-Override).
  * B6.4 — Formel-String-Konstanten (formulas.py) == Code-Konstanten (indicators.py).

Läuft mit pytest oder direkt: ``python tests/test_review_wirkungsmechanismen.py``.
"""

from __future__ import annotations

import re
from pathlib import Path

from app.data import catalog
from app.data.pathway_descriptions import PATHWAY_DESCRIPTIONS
from app.services import lineage_graph
from app.services.engine import formulas

_INDICATORS_SRC = (
    Path(__file__).resolve().parents[1] / "app" / "services" / "engine" / "indicators.py"
).read_text(encoding="utf-8")


# ── B6.1 — Skalierungs-Tooltip je scale ────────────────────────────────────────

def _scaling_tooltip(scale: str) -> str:
    node = {
        "id": "op:scaling:X",
        "type": "operator",
        "label": "",
        "meta": {
            "op_kind": "scaling",
            "value": 18.0,
            "unit": "Tote/J",
            "scale": scale,
            "source": "test",
        },
    }
    return lineage_graph._tooltip_for_node(node, {node["id"]: node}, [])


def test_scaling_tooltip_pop():
    assert "Einwohner_zelle/100.000" in _scaling_tooltip("pop")


def test_scaling_tooltip_area():
    tip = _scaling_tooltip("area")
    assert "Fläche/50 km²" in tip
    assert "Einwohner_zelle/100.000" not in tip


def test_scaling_tooltip_flat():
    tip = _scaling_tooltip("flat")
    assert "P90-Index" in tip
    assert "Einwohner_zelle/100.000" not in tip


def test_scaling_tooltip_matches_catalog_scale():
    """Jedes Risiko: die im Tooltip genannte Formel passt zu risk['scale']."""
    from app.services.engine.risk_engine import _scale_factor

    expected = {
        "pop": "Einwohner_zelle/100.000",
        "area": "Fläche/50 km²",
        "flat": "P90-Index",
    }
    for risk in catalog.RISKS:
        scale = risk.get("scale", "pop")
        assert expected[scale] in _scaling_tooltip(scale)
        # Skalierungsformel und _scale_factor beziehen sich auf dieselbe Größe:
        if scale == "pop":
            assert _scale_factor(risk, 100_000.0, 1.0) == 1.0
        elif scale == "area":
            assert _scale_factor(risk, 0.0, 50.0) == 1.0
        else:
            assert _scale_factor(risk, 0.0, 0.0) == 1.0


# ── B6.6 — kuratierte Wirkungsketten wohlgeformt + begründet ───────────────────

def test_every_risk_is_curated_and_wellformed():
    """Jedes Risiko hat kuratierte, gültige, begründete Ketten mit genau 1 Primärpfad."""
    from app.data.pathway_curation import CURATED_PATHWAYS

    errs: list[str] = []
    for risk in catalog.RISKS:
        code = risk["code"]
        spec = CURATED_PATHWAYS.get(code)
        if not spec:
            errs.append(f"{code}: nicht kuratiert")
            continue
        H, E, V = set(risk["hazards"]), set(risk["exposures"]), set(risk["vulnerabilities"])
        paths = catalog.build_pathways(risk)
        n_primary = sum(1 for p in paths if p["pathway_type"] == "primary")
        if n_primary != 1:
            errs.append(f"{code}: {n_primary} Primärpfade (erwartet genau 1)")
        for p in paths:
            if p["hazard"] not in H or p["exposure"] not in E or p["vulnerability"] not in V:
                errs.append(f"{code}: Kette {p['hazard']}×{p['exposure']}×{p['vulnerability']} "
                            "nutzt nicht gelistete H/E/V")
            if not p.get("justification"):
                errs.append(f"{code}: Kette ohne Begründung")
    assert not errs, "Kuratierungs-Fehler:\n" + "\n".join(errs)


def test_curated_pathways_carry_source_and_display_title():
    """Jede Kette liefert Anzeigetitel + auflösbare Begründungsquelle (Info-Fenster)."""
    from app.data import sources
    from app.data.pathway_descriptions import get_pathway_description

    for risk in catalog.RISKS:
        meta = formulas.risk_pathway_meta(risk)
        assert meta, f"{risk['code']}: keine Pfade"
        for p in meta:
            title = get_pathway_description(
                risk["code"], p["hazard"], p["exposure"], p["vulnerability"],
                p["type"], p["hazard_name"], p["exposure_name"], p["vulnerability_name"])
            assert title and title.strip(), f"{risk['code']}: leerer Kettentitel"
            assert p["justification"], f"{risk['code']}: fehlende Begründung"
            ref = p.get("justification_ref")
            assert ref, f"{risk['code']}: fehlende Begründungsquelle"
            assert sources.resolve([ref]), f"{risk['code']}: Quelle {ref} nicht auflösbar"


def test_pathway_descriptions_do_not_contradict_curation():
    """PATHWAY_DESCRIPTIONS ist nur noch Titel-Override — Einträge müssen zu einer
    existierenden (kuratierten) Kette gehören oder sind unbenutzt (kein harter Fehler),
    dürfen aber keine nicht existierenden Risiken referenzieren."""
    for (risk_code, _h, _e, _v) in PATHWAY_DESCRIPTIONS:
        assert risk_code in catalog.RISKS_BY_CODE or risk_code == "EXPECTED_TOTAL_DAMAGE_EAD_EUR", \
            f"PATHWAY_DESCRIPTIONS referenziert unbekanntes Risiko {risk_code}"


# ── B6.4 — Formel-String-Konstanten == indicators.py-Konstanten ────────────────

# (py-Literal im indicators.py-Code der Zeile ; deutscher Formelstring-Baustein)
_CONSTANT_MAP: dict[str, list[tuple[str, str]]] = {
    "MEAN_TEMPERATURE_RISE": [("0.08", "0,08")],
    # Die obere Kappung bei 40 ist entfallen: Das war der Katalog-norm_max, also
    # eine Screening-Grenze, die zuvor auch die absoluten Schadenswerte heißer
    # Stadtzellen kappte (MODELL_KRITIK §3.3).
    "HEAT_WAVE": [("1.5", "1,5")],
    "COLD_EXTREME": [("0.3", "0,3")],
    "DROUGHT": [("0.6", "0,6"), ("0.7", "0,7"), ("60", "60")],
    "EXTRATROPICAL_STORM": [("0.8", "0,8"), ("0.5", "0,5")],
    "HEAVY_RAIN_FLOOD": [("0.4", "0,4"), ("0.5", "0,5"), ("0.6", "0,6"), ("100", "100")],
    "GLACIER_SNOW_LOSS": [("0.25", "0,25"), ("0.75", "0,75"), ("45", "45")],
    "SOIL_MOISTURE_DECLINE": [("0.5", "0,5"), ("0.6", "0,6")],
    "WILDFIRE": [("0.4", "0,4"), ("100", "100")],
    "LANDSLIDE": [("100", "100")],
    "SURFACE_WATER_HEATING": [("0.5", "0,5")],
    "LOW_FLOW_NIEDRIGWASSER": [("0.6", "0,6"), ("0.4", "0,4"), ("0.3", "0,3"), ("60", "60")],
    "SOIL_SALINIZATION": [("0.35", "0,35"), ("0.65", "0,65"),
                          ("0.45", "0,45"), ("0.55", "0,55")],
    # Exposures
    "BIODIVERSITY_HOTSPOTS": [("0.5", "0,5")],
    "OUTDOOR_THERMAL_EXPOSURE": [("2.0", "2"), ("3.0", "3")],
    "FISHERIES_AQUACULTURE_AREAS": [("5.0", "5")],
    # Vulnerabilities
    "HEAT_SENSITIVITY": [("6.0", "6"), ("20.0", "20")],
    "AIR_QUALITY_RISK": [("60.0", "60"), ("200.0", "200")],
    "WATER_STRESS_INDEX": [("40.0", "40"), ("4000", "4.000"), ("20.0", "20")],
    "SOIL_SENSITIVITY": [("60.0", "60"), ("40.0", "40")],
    "IRRIGATION_DEPENDENCY": [("0.5", "0,5")],
    "WILDFIRE_SUSCEPTIBILITY": [("0.5", "0,5")],
    "SINGLE_SITE_DEPENDENCY": [("200.0", "200")],
    "GROUNDWATER_DEPENDENCY": [("50.0", "50")],
    "BIODIVERSITY_RESILIENCE": [("0.6", "0,6")],
}


def _indicator_code_line(code: str) -> str:
    """Codeabschnitt der Zuweisung ``"CODE": ...`` in indicators.py.

    Erfasst auch mehrzeilige Zuweisungen (z. B. HEAVY_RAIN_FLOOD,
    SOIL_SALINIZATION) — bis zum nächsten Dict-Key oder Blockende.
    """
    m = re.search(
        rf'"{re.escape(code)}":.*?(?=\n\s+"[A-Z_]+":|\n    \}})',
        _INDICATORS_SRC,
        re.S,
    )
    assert m, f"{code} nicht in indicators.py gefunden"
    return m.group(0)


def test_pathway_tooltips_show_actual_weight():
    """B6.5: Der Wirkungsketten-Tooltip nennt das echte Kettengewicht.

    Früher stand dort nur das Wort "Gewicht" — jetzt der Zahlenwert aus der
    Kuratierung (z. B. "1 · normierte Gefahr · …").
    """
    for code in ("EXPECTED_ANNUAL_MORTALITY", "AGRICULTURAL_YIELD_LOSS_EUR"):
        risk = catalog.RISKS_BY_CODE.get(code)
        if not risk:
            continue
        g = lineage_graph.build_for_layer(code, "risks")
        pathway_nodes = [n for n in g["nodes"] if n["type"] == "pathway"]
        assert pathway_nodes, f"{code}: keine Wirkungsketten-Knoten"
        for n in pathway_nodes:
            meta = n.get("meta") or {}
            w = meta.get("weight")
            assert isinstance(w, (int, float)), f"{code}: Kette ohne Gewicht"
            tooltip = meta.get("tooltip", "")
            assert f"Berechnung: {w:g} · normierte Gefahr" in tooltip, \
                f"{code}: Tooltip nennt das Gewicht nicht: {tooltip!r}"


def test_formula_operator_factors_match_indicator_constants():
    """B6.4 auf Operator-Ebene: scale_factor/scaling-Faktoren der expliziten
    FORMULA_OPERATORS-Schritte müssen als Literal im indicators.py-Code des
    jeweiligen Indikators vorkommen (kein Drift zwischen Diagramm und Rechnung).
    """
    from app.data.lineage_operators import FORMULA_OPERATORS

    mismatches: list[str] = []
    for code, steps in FORMULA_OPERATORS.items():
        factor_steps = [
            s for s in steps
            if s.get("op_kind") in ("scale_factor", "scaling")
            and s.get("factor") is not None
        ]
        if not factor_steps:
            continue
        code_segment = _indicator_code_line(code)
        for step in factor_steps:
            literal = f"{step['factor']:g}"
            if literal not in code_segment:
                mismatches.append(
                    f"{code}: Faktor {literal} fehlt im Code «{code_segment[:80]}…»")
    assert not mismatches, "Operator-Faktoren driften:\n" + "\n".join(mismatches)


def test_formula_string_constants_match_indicator_constants():
    mismatches: list[str] = []
    for code, pairs in _CONSTANT_MAP.items():
        formula = formulas.get_recipe(code)["formula"]
        code_line = _indicator_code_line(code)
        for py_literal, de_fragment in pairs:
            if de_fragment not in formula:
                mismatches.append(f"{code}: '{de_fragment}' fehlt im Formel-String «{formula}»")
            if py_literal not in code_line:
                mismatches.append(f"{code}: '{py_literal}' fehlt in indicators.py-Zeile «{code_line}»")
    assert not mismatches, "Formel/Code driften:\n" + "\n".join(mismatches)


def _code_only(src: str) -> str:
    """Quelltext OHNE Docstrings und Kommentare.

    Zwingend für die Substring-Prüfungen unten: ``_healthcare_modifier`` begründet
    in seinem Docstring, warum HEAT_SENSITIVITY hier gerade NICHT eingeht — eine
    naive Suche im Rohquelltext fände den Namen und ließe damit genau den Fehler
    durch, den dieser Test fangen soll (per Mutationsprobe verifiziert).
    """
    import ast
    import textwrap

    tree = ast.parse(textwrap.dedent(src))
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if not isinstance(body, list) or not body:
            continue
        first = body[0]
        if (isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)):
            node.body = body[1:] or [ast.Pass()]
    return ast.unparse(tree)  # unparse verwirft Kommentare von sich aus


def _health_impact_source(code: str) -> str:
    """Code der Impact-Funktion INKLUSIVE der Helfer aus demselben Modul.

    Nötig, weil die Verletzten-Kanäle über ``_injuries`` delegieren — ohne das
    Auflösen sähe der Test dort fälschlich kein ``ctx.g(risk)``.
    """
    import inspect

    from app.services.engine.impact import health as health_mod

    fn = health_mod.HEALTH_IMPACTS[code]
    src = inspect.getsource(fn)
    for name in re.findall(r"\b(_[a-z_]+)\s*\(", src):
        helper = getattr(health_mod, name, None)
        if callable(helper):
            try:
                src += "\n" + inspect.getsource(helper)
            except (OSError, TypeError):
                pass
    return _code_only(src)


def test_health_modifier_node_matches_computation():
    """Der Modifikator-Knoten im Wirkungsdiagramm muss zeigen, was gerechnet wird.

    Vorher behauptete das Diagramm für ALLE Gesundheitskanäle ``g(V̂)`` — auch für
    die drei Mortalitätskanäle, die stattdessen Versorgungszugang (Hitze),
    Warnzeit×Alter (Flut) bzw. Bäume×Straßen (Sturm) rechnen. Es zeichnete damit
    Eingänge wie HEAT_SENSITIVITY ein, die den Outcome gar nicht berühren.

    Abdeckung (per Mutationsprobe geprüft): fängt entfernte Modifikatoren, falsche
    und verschwiegene Vulnerabilitäten sowie erfundene Parameter.

    BEWUSSTE LÜCKE: Für ``cell_keys`` prüft der Test nur die Richtung
    deklariert ⊆ Code, nicht umgekehrt. Ein weggelassener Zellwert (das Diagramm
    zeigt weniger als der Code liest) fällt hier nicht auf. Die Gegenrichtung
    bräuchte eine Zuordnung, WELCHE ``ctx.ci``-Zugriffe zum Modifikator gehören
    und welche zu Rate oder Treiber — sonst meldete sie bei der Flut-Mortalität
    fälschlich ``slope_factor``/``depression_factor``, die zur Rate gehören.
    """
    from app.services.engine.impact.health import LINEAGE_SPECS

    problems: list[str] = []
    for code, spec in LINEAGE_SPECS.items():
        src = _health_impact_source(code)
        uses_gv = "ctx.g(risk)" in src
        mod = spec.get("modifier")
        if uses_gv and mod:
            problems.append(f"{code}: rechnet g(V̂), Spec deklariert aber einen Modifikator")
        if not uses_gv and not mod:
            problems.append(f"{code}: rechnet KEIN g(V̂), Spec deklariert aber auch keinen "
                            f"Modifikator — das Diagramm zeigt dann ein falsches g(V̂)")
        if not mod:
            continue
        # Jede im Diagramm gezeichnete Vulnerabilität muss die Funktion auch lesen …
        declared = set(mod.get("vulnerabilities", []))
        for vcode in declared:
            if vcode not in src:
                problems.append(f"{code}: Modifikator zeichnet {vcode}, der Code liest ihn nicht")
        # … und umgekehrt: keine still gelesene Vulnerabilität, die das Diagramm
        # verschweigt. Ohne diese Richtung wäre der Test halbblind.
        for vcode in catalog.VULNERABILITIES_BY_CODE:
            if vcode in src and vcode not in declared:
                problems.append(f"{code}: Code liest {vcode}, der Modifikator zeichnet ihn nicht")
        for ckey in mod.get("cell_keys", []):
            if ckey not in src:
                problems.append(f"{code}: Modifikator zeichnet Zellwert {ckey}, "
                                f"der Code liest ihn nicht")
        for pkey in mod.get("params", []):
            # ast.unparse normalisiert auf einfache Anführungszeichen.
            if f"'{pkey}'" not in src and f'"{pkey}"' not in src:
                problems.append(f"{code}: Modifikator zeichnet Parameter {pkey}, "
                                f"der Code liest ihn nicht")
    assert not problems, "Modifikator-Knoten ⇄ Rechnung driften:\n" + "\n".join(problems)


def test_health_modifier_vulnerabilities_are_drawn_once():
    """Kein Kanal darf eine Vulnerabilität zeichnen, die er nicht verwendet.

    Gegenprobe zum obigen Test aus Sicht des fertigen Graphen: Die Kanten in den
    Modifikator-Knoten müssen exakt den deklarierten Vulnerabilitäten entsprechen,
    nicht der (breiteren) ``vulnerabilities``-Liste des Katalogs.
    """
    from app.services.engine.impact.health import LINEAGE_SPECS

    problems: list[str] = []
    for code, spec in LINEAGE_SPECS.items():
        mod = spec.get("modifier")
        if not mod:
            continue
        g = lineage_graph.build_for_layer(code, "risks")
        byid = {n["id"]: n for n in g["nodes"]}
        op_id = f"op:modifier:{code}"
        assert op_id in byid, f"{code}: Modifikator-Knoten fehlt im Graphen"
        drawn = {byid[e["source"]]["meta"].get("code")
                 for e in g["edges"] if e["target"] == op_id
                 and byid[e["source"]].get("type") == "vulnerability"}
        drawn.discard(None)
        expected = set(mod.get("vulnerabilities", []))
        if drawn != expected:
            problems.append(f"{code}: gezeichnet {sorted(drawn)} != deklariert {sorted(expected)}")
        assert f"op:gv:{code}" not in byid, \
            f"{code}: g(V̂)-Knoten trotz eigenem Modifikator im Graphen"
    assert not problems, "Modifikator-Kanten driften:\n" + "\n".join(problems)


if __name__ == "__main__":
    import traceback

    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except Exception:
            failed += 1
            print(f"FAIL {t.__name__}")
            traceback.print_exc()
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    raise SystemExit(1 if failed else 0)
