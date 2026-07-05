"""Tests zur Max-Kombination der Wirkungsketten (Stufe 1, MODELL_KRITIK §3.1/3.5).

Der Risiko-Index ist ``100 · max_p(w_p · Ĥ_p · Ê_p · V̂_p)`` — die stärkste einzelne
Wirkungskette. Deckt ab:
  (a) Der Index hängt NICHT von der Anzahl der Ketten ab (Verdünnungs-Artefakt behoben).
  (b) Der Primärpfad (w=1,0) dominiert bei gleichen normierten Werten.
  (c) Das durchgerechnete Mortalitäts-Beispiel aus §3.1 ergibt 13,5 (nicht 7,4).
  (d) Die Kuratierung erzeugt genau einen Primärpfad je Risiko.

Läuft mit pytest oder direkt: ``python tests/test_pathway_max_composition.py``.
"""

from __future__ import annotations

from app.data import catalog
from app.services.engine import risk_engine


def _norm(hazards: dict, exposures: dict, vulns: dict) -> dict:
    return {"hazards": hazards, "exposures": exposures, "vulnerabilities": vulns}


# ── (a) Pfadanzahl-Invarianz ───────────────────────────────────────────────────

def test_index_is_independent_of_pathway_count(monkeypatch):
    """Zwei Risiken mit identischem Primärpfad, aber unterschiedlich vielen (schwächeren)
    Nebenketten, ergeben denselben Index — anders als beim früheren Mittelwert."""
    pw = catalog.PATHWAY_WEIGHTS
    few = [
        {"hazard": "H", "exposure": "E", "vulnerability": "V",
         "pathway_type": "primary", "weight": pw["primary"]},
    ]
    many = few + [
        {"hazard": "H2", "exposure": "E", "vulnerability": "V",
         "pathway_type": "alternate_hazard", "weight": pw["alternate_hazard"]},
        {"hazard": "H3", "exposure": "E", "vulnerability": "V",
         "pathway_type": "alternate_exposure", "weight": pw["alternate_exposure"]},
    ]
    monkeypatch.setitem(risk_engine._PATHWAYS, "R_FEW", few)
    monkeypatch.setitem(risk_engine._PATHWAYS, "R_MANY", many)
    # catalog.RISKS steuert die Iteration in cell_risk_indices → temporär ergänzen
    fake = [{"code": "R_FEW"}, {"code": "R_MANY"}]
    monkeypatch.setattr(catalog, "RISKS", fake)

    hev = _norm({"H": 0.6, "H2": 0.1, "H3": 0.1}, {"E": 0.5}, {"V": 0.4})
    idx = risk_engine.cell_risk_indices(hev)
    assert idx["R_FEW"] == idx["R_MANY"]
    # Primärpfad: 100 · 1,0 · 0,6 · 0,5 · 0,4 = 12,0
    assert abs(idx["R_FEW"] - 12.0) < 1e-6


# ── (b) Primärpfad-Dominanz ────────────────────────────────────────────────────

def test_primary_dominates_at_equal_values(monkeypatch):
    pw = catalog.PATHWAY_WEIGHTS
    paths = [
        {"hazard": "H", "exposure": "E", "vulnerability": "V",
         "pathway_type": "primary", "weight": pw["primary"]},
        {"hazard": "H", "exposure": "E", "vulnerability": "V",
         "pathway_type": "alternate_hazard", "weight": pw["alternate_hazard"]},
    ]
    monkeypatch.setitem(risk_engine._PATHWAYS, "R", paths)
    monkeypatch.setattr(catalog, "RISKS", [{"code": "R"}])
    hev = _norm({"H": 0.5}, {"E": 0.5}, {"V": 0.5})
    idx = risk_engine.cell_risk_indices(hev)
    # max ist der Primärpfad: 100·1,0·0,125 = 12,5 (nicht der gedämpfte Alternativpfad)
    assert abs(idx["R"] - 12.5) < 1e-6


# ── (c) Zahlenbeispiel MODELL_KRITIK §3.1 → 13,5 ───────────────────────────────

def test_mortality_example_matches_primary_signal():
    """Die Werte aus §3.1 ergeben mit der Max-Formel 13,5 (Primärsignal), nicht 7,4."""
    hev = _norm(
        {"HEAT_WAVE": 0.60, "COLD_EXTREME": 0.20, "COMPOUND_EVENT": 0.30},
        {"POPULATION_DENSITY": 0.375, "VULNERABLE_GROUPS_POPULATION": 0.30,
         "AGE_STRUCTURE": 0.40},
        {"HEAT_SENSITIVITY": 0.60, "HEALTHCARE_ACCESS": 0.40,
         "VULNERABLE_GROUPS_SHARE": 0.35},
    )
    idx = risk_engine.cell_risk_indices(hev)
    # Primärkette HEAT_WAVE×POPULATION_DENSITY×HEAT_SENSITIVITY: 100·1,0·0,6·0,375·0,6 = 13,5
    assert abs(idx["EXPECTED_ANNUAL_MORTALITY"] - 13.5) < 0.01


# ── (d) genau ein Primärpfad je Risiko ─────────────────────────────────────────

def test_exactly_one_primary_pathway_per_risk():
    for risk in catalog.RISKS:
        paths = catalog.build_pathways(risk)
        n_primary = sum(1 for p in paths if p["pathway_type"] == "primary")
        assert n_primary == 1, f"{risk['code']}: {n_primary} Primärpfade"


def test_index_clamped_to_100(monkeypatch):
    pw = catalog.PATHWAY_WEIGHTS
    monkeypatch.setitem(risk_engine._PATHWAYS, "R", [
        {"hazard": "H", "exposure": "E", "vulnerability": "V",
         "pathway_type": "primary", "weight": pw["primary"]},
    ])
    monkeypatch.setattr(catalog, "RISKS", [{"code": "R"}])
    hev = _norm({"H": 1.0}, {"E": 1.0}, {"V": 1.0})
    idx = risk_engine.cell_risk_indices(hev)
    assert idx["R"] == 100.0


if __name__ == "__main__":
    import traceback

    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            # monkeypatch-Tests hier überspringen (brauchen pytest-Fixture)
            import inspect
            if "monkeypatch" in inspect.signature(t).parameters:
                print(f"SKIP {t.__name__} (braucht pytest)")
                continue
            t()
            print(f"PASS {t.__name__}")
        except Exception:
            failed += 1
            print(f"FAIL {t.__name__}")
            traceback.print_exc()
    raise SystemExit(1 if failed else 0)
