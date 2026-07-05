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
