"""Konsistenztests zu REVIEW_WIRKUNGSMECHANISMEN.md §5 (Info-Fenster ⇄ Rechnung).

Deckt ab:
  * B6.1 — Skalierungs-Tooltip ist scale-abhängig (pop/area/flat).
  * B6.6 — jedes Tupel in PATHWAY_DESCRIPTIONS wird von build_pathways erzeugt.
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
    assert "×1" in tip
    assert "Einwohner_zelle/100.000" not in tip


def test_scaling_tooltip_matches_catalog_scale():
    """Jedes Risiko: die im Tooltip genannte Formel passt zu risk['scale']."""
    from app.services.engine.risk_engine import _scale_factor

    expected = {
        "pop": "Einwohner_zelle/100.000",
        "area": "Fläche/50 km²",
        "flat": "×1",
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


# ── B6.6 — pathway_descriptions ⊆ build_pathways ───────────────────────────────

def test_every_pathway_description_is_produced_by_build_pathways():
    missing: list[tuple[str, str, str, str]] = []
    cache: dict[str, set[tuple[str, str, str]]] = {}
    for (risk_code, h, e, v) in PATHWAY_DESCRIPTIONS:
        if risk_code not in cache:
            risk = catalog.RISKS_BY_CODE.get(risk_code)
            paths = catalog.build_pathways(risk) if risk else []
            cache[risk_code] = {
                (p["hazard"], p["exposure"], p["vulnerability"]) for p in paths
            }
        if (h, e, v) not in cache[risk_code]:
            missing.append((risk_code, h, e, v))
    assert not missing, f"Stale pathway_descriptions (nicht von build_pathways erzeugt): {missing}"


# ── B6.4 — Formel-String-Konstanten == indicators.py-Konstanten ────────────────

# (py-Literal im indicators.py-Code der Zeile ; deutscher Formelstring-Baustein)
_CONSTANT_MAP: dict[str, list[tuple[str, str]]] = {
    "MEAN_TEMPERATURE_RISE": [("0.08", "0,08")],
    "HEAT_WAVE": [("1.5", "1,5"), ("40", "40")],
    "COLD_EXTREME": [("0.3", "0,3")],
    "DROUGHT": [("0.6", "0,6"), ("0.7", "0,7"), ("60", "60")],
    "EXTRATROPICAL_STORM": [("0.8", "0,8"), ("0.5", "0,5")],
}


def _indicator_code_line(code: str) -> str:
    """Zeile(n) der H-Zuweisung ``"CODE": ...`` in indicators.py."""
    m = re.search(rf'"{re.escape(code)}":.*', _INDICATORS_SRC)
    assert m, f"{code} nicht in indicators.py gefunden"
    return m.group(0)


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
