"""T-1604-cto: Ausgabe vermiedene Tage und Euro der Stadtbaumwahl (#96 §5, Integrationsauflage
Punkt (4), Z. 1111–1125).

Vorhaben T-1483-cto Teilpaket #6, Vorgabe P1/P2. Das ``impact_summary`` einer Stadtbaumwahl-
Maßnahme (``LOW_ALLERGEN_TREE_SELECTION``) trägt die vermiedenen Zusatztage und Euro/Jahr der
Kommune, gekennzeichnet als begründete Abschätzung von KAP3 (Δk_Birke/Δk_unbek sind keine
belegten Effektgrößen), mit einem Hinweis auf die Richtung des Fehlers in λ (§6 Modellgrenze 7).
Fehlt ``config['anteil_ersetzt']`` (Punkt 2 der Auflage ohne Eingabe), entsteht kein Betrag statt
eines erfundenen (P2, Muster S158 ``benefit_missing_input``). Führt keine abgedeckte Zelle im
Ausgangsstand Baumkronen, wäre ein ausgewiesenes 0 € nicht von einer Datenlücke unterscheidbar
(P2) — auch dort steht ein Vermerk statt des Betrags.

Rechenbeispiel Allee-Zelle nach Ü-13 (Bericht §5, Block ``beispiel_96_stadtbaum_allee``, wie
``test_massnahme_stadtbaum_kosten.py``): Betroffene B 100, δ_B 0,43659, δ_G 0,57834, Ḡ₀ 0,18125,
Ĝ 0,3625 (Ĝ/Ḡ₀ = 2) → 172,538 Tage im Ausgangsstand. ``anteil_ersetzt`` 1,0,
``canopy_birch_frac`` 0,078125, ``canopy_unknown_frac`` 0 senkt Ĝ auf Ĝ′ = 0,3625 −
0,464·0,078125 = 0,32625 (Ĝ′/Ḡ₀ = 1,8); Nutzen 14,209 Tage, ≈ 88 € je Jahr (14,209 Tage ×
6,20 € = 88,10 €, Rate aus dem Katalog-Kostensatz von #96).

Geprüft wird (Abnahmekriterium T-1604-cto):
(a) ``compute_impact`` liefert an der Allee-Zelle ``stadtbaum_avoided_days`` je Zelle und
    ``stadtbaum_avoided_days_total`` = 14,2 ± 0,05, ``stadtbaum_avoided_days_eur`` = 88 ± 0,5,
    ``stadtbaum_estimate_note`` == „Abschätzung von KAP3“, dazu ein Hinweistext mit
    „Modellgrenze 7“ zur Richtung des Fehlers in λ.
(a2) Ü-4 (Befund 237): die Zelle trägt ``stadtbaum_avoided_eur`` = 88,10 ± 0,01 €; die Summe der
    Zell-Euro ist der Euro-Betrag der Kommune ± 0,01 €.
(b) Ohne ``anteil_ersetzt`` steht ``benefit_missing_input`` == 'anteil_ersetzt' und kein Betrag
    (keine Zahlenfelder, ``annual_benefit_damage_eur`` bleibt 0 — sichtbar wird das nicht, weil
    ``benefit_display`` den Betrag verdeckt).
(c) In einer abgedeckten Zelle ohne Baumkronen im Ausgangsstand (``canopy_birch_frac`` +
    ``canopy_unknown_frac`` = 0) steht ein Vermerk statt des (sonst als 0 € lesbaren) Betrags.

DB-frei (Session-Doppel, Muster ``test_massnahme_s158_ausgabe.py``); ``_coverage`` (PostGIS)
und ``get_risk_aggregate`` (Kappungs-Basis) werden mit festen Werten ersetzt.
"""

from __future__ import annotations

import pytest

from app.models.models import AdaptationMeasure, CellAssessment, ConfigParameter, Kommune
from app.services import measure_service, parameter_registry

CODE = "LOW_ALLERGEN_TREE_SELECTION"
RISK = "EXPECTED_ANNUAL_ALLERGY_DAYS"
KOMMUNE_ID = 1
CELL_ID = 42

# Allee-Zelle nach Ü-13 (s. Modul-Docstring).
BETROFFENE = 100.0
AUSGANGSSTAND_TAGE = 172.538
DELTA_BIRKE = 0.43659
DELTA_GRAESER = 0.57834
G_BAR0 = 0.18125
G_CELL = 0.3625          # Ĝ/Ḡ₀ = 2
CANOPY_BIRKE = 0.078125  # → Ĝ′/Ḡ₀ = 1,8
CANOPY_UNBEK = 0.0
GRUEN = 0.3
ANTEIL_ERSETZT = 1.0


class _Q:
    """Query-Doppel: ``filter`` ignoriert das Prädikat (je Test genau eine Maßnahme/Kommune)
    und liefert immer die vollständige vorgehaltene Zeilenmenge zurück (Muster
    ``test_massnahme_s158_ausgabe.py``)."""

    def __init__(self, rows):
        self._rows = list(rows)

    def filter(self, *a, **k):
        return self

    def all(self):
        return list(self._rows)

    def first(self):
        return self._rows[0] if self._rows else None

    def delete(self):
        return 0

    def scalar(self):
        return None


class _DB:
    def __init__(self, rows):
        self._rows = rows
        self.added: list = []

    def query(self, model, *a, **k):
        return _Q(self._rows.get(model, []))

    def add(self, obj):
        self.added.append(obj)

    def commit(self):
        pass


def _allee_cell() -> dict:
    return {
        "index": AUSGANGSSTAND_TAGE, "outcome": AUSGANGSSTAND_TAGE,
        "betroffene": BETROFFENE, "delta_birke": DELTA_BIRKE, "delta_graeser": DELTA_GRAESER,
        "pollen_g": G_CELL, "pollen_g_bar0": G_BAR0,
        "canopy_birch_frac": CANOPY_BIRKE, "canopy_unknown_frac": CANOPY_UNBEK,
        "green_frac": GRUEN,
    }


def _no_canopy_cell() -> dict:
    """Dieselbe Allee-Zelle, aber ohne Baumkronen im Ausgangsstand (mechanisch nichts zu
    ersetzen)."""
    cell = dict(_allee_cell())
    cell["canopy_birch_frac"] = 0.0
    cell["canopy_unknown_frac"] = 0.0
    return cell


def _run_cells(cells: dict[int, dict], config: dict, monkeypatch,
              area_m2: float = 1000.0, base_agg_cost_eur: float = 1_000_000_000.0
              ) -> tuple[dict, list]:
    """Führt ``compute_impact`` gegen eine Session-Doppel mit ggf. mehreren Zellen aus
    und gibt (summary, gespeicherte MeasureImpact-Zeilen) zurück."""
    measure = AdaptationMeasure(
        id=1, kommune_id=KOMMUNE_ID, name="Stadtbaumwahl Test", measure_type=CODE,
        geometry=None, config=config, implementation_year=2027, description="",
        impact_summary={})
    kommune = Kommune(id=KOMMUNE_ID, name="Testheim", osm_id="R-STADTBAUM", population=10_000,
                      area_km2=5.0)
    assessments = [
        CellAssessment(id=cid, kommune_id=KOMMUNE_ID, grid_cell_id=cid,
                       data={"risks": {RISK: risk}, "inputs": {"pop": 100.0}})
        for cid, risk in cells.items()
    ]
    db = _DB({AdaptationMeasure: [measure], CellAssessment: assessments,
             ConfigParameter: [], Kommune: [kommune]})

    frac_map = {cid: 1.0 for cid in cells}
    monkeypatch.setattr(measure_service, "_coverage", lambda _db, _m: (frac_map, area_m2))
    monkeypatch.setattr(measure_service, "_params_fingerprint",
                        lambda *a, **k: "fp-test-stadtbaum-ausgabe")
    monkeypatch.setattr(parameter_registry, "load_db_overrides", lambda *a, **k: [])
    monkeypatch.setattr(
        measure_service, "get_risk_aggregate",
        lambda *a, **k: {"risks": {RISK: {"cost_eur": base_agg_cost_eur}}})

    summary = measure_service.compute_impact(db, measure.id)
    return summary, db.added


def _run(cell: dict, config: dict, monkeypatch,
        area_m2: float = 1000.0, base_agg_cost_eur: float = 1_000_000_000.0) -> tuple[dict, list]:
    """Einzelzellen-Fall (Muster ``test_massnahme_s158_ausgabe.py``)."""
    return _run_cells({CELL_ID: cell}, config, monkeypatch, area_m2, base_agg_cost_eur)


# ── (a) Allee-Zelle: 14,2 Tage, 88 €, Kennzeichnung, Hinweis Modellgrenze 7 ─────────

def test_allee_zelle_14_2_tage_88_euro_gekennzeichnet(monkeypatch):
    summary, added = _run(_allee_cell(), {"anteil_ersetzt": ANTEIL_ERSETZT}, monkeypatch)

    assert summary["stadtbaum_avoided_days_total"] == pytest.approx(14.2, abs=0.05)
    assert summary["stadtbaum_avoided_days_eur"] == pytest.approx(88, abs=0.5)
    assert summary["stadtbaum_estimate_note"] == "Abschätzung von KAP3"
    assert "Modellgrenze 7" in summary["stadtbaum_lambda_hinweis"]
    assert summary.get("benefit_display") is None
    assert summary.get("benefit_missing_input") is None

    zeile = next(o for o in added if o.measure_id == 1)
    assert (zeile.savings or {}).get("stadtbaum_avoided_days") == pytest.approx(14.2, abs=0.05)
    assert (zeile.savings or {}).get("stadtbaum_avoided_days") == pytest.approx(
        summary["stadtbaum_avoided_days_total"], abs=0.05)


# ── (b) ohne anteil_ersetzt: kein Betrag ─────────────────────────────────────────────

def test_ohne_anteil_ersetzt_kein_betrag(monkeypatch):
    summary, added = _run(_allee_cell(), {}, monkeypatch)

    assert summary.get("benefit_missing_input") == "anteil_ersetzt"
    assert summary.get("benefit_display") == measure_service.STADTBAUM_MISSING_ANTEIL_TEXT
    assert "stadtbaum_avoided_days_total" not in summary
    assert "stadtbaum_avoided_days_eur" not in summary
    assert summary["annual_benefit_damage_eur"] == 0.0
    zeile = next(o for o in added if o.measure_id == 1)
    assert (zeile.savings or {}).get("stadtbaum_avoided_days") is None


# ── (c) Zelle ohne Baumkronen im Ausgangsstand: Vermerk statt 0 € ────────────────────

def test_zelle_ohne_kronen_vermerk_statt_0_euro(monkeypatch):
    summary, added = _run(_no_canopy_cell(), {"anteil_ersetzt": ANTEIL_ERSETZT}, monkeypatch)

    assert summary.get("benefit_missing_input") == "canopy"
    assert summary.get("benefit_display") == measure_service.STADTBAUM_NO_CANOPY_TEXT
    assert "stadtbaum_avoided_days_total" not in summary
    assert "stadtbaum_avoided_days_eur" not in summary
    # Kein 0 € als Nutzen #96: die Zelle bleibt unverändert (Faktor 1,0, nichts zu
    # ersetzen), damit trägt annual_benefit_damage_eur hier 0 — sichtbar wird das
    # nicht, weil benefit_display den Betrag verdeckt (dieselbe Weiche wie bei S158).
    assert summary["annual_benefit_damage_eur"] == 0.0
    zeile = next(o for o in added if o.measure_id == 1)
    assert (zeile.savings or {}).get("stadtbaum_avoided_days") is None
    # Zellweiser Vermerk (Nacharbeit Runde 1): die kronenlose Zelle trägt selbst den
    # Grund, verschwindet nicht nur stumm auf Kommunenebene.
    assert (zeile.savings or {}).get("stadtbaum_missing_reason") == "canopy"


# ── (d) gemischte Deckung: kronenlose Zelle bekommt eigenen Vermerk, Kommune bleibt
#        eine Zahl (die andere Zelle trägt einen positiven Effekt) ──────────────────

def test_gemischte_deckung_kronenlose_zelle_bekommt_eigenen_vermerk(monkeypatch):
    cells = {CELL_ID: _allee_cell(), CELL_ID + 1: _no_canopy_cell()}
    summary, added = _run_cells(cells, {"anteil_ersetzt": ANTEIL_ERSETZT}, monkeypatch)

    # Kommune: die Allee-Zelle trägt einen positiven Effekt, deshalb eine Zahl statt
    # eines Vermerks (kein 0 € insgesamt).
    assert summary.get("benefit_missing_input") is None
    assert summary.get("benefit_display") is None
    assert summary["stadtbaum_avoided_days_total"] == pytest.approx(14.2, abs=0.05)

    zeile_allee = next(o for o in added if o.grid_cell_id == CELL_ID)
    zeile_ohne_kronen = next(o for o in added if o.grid_cell_id == CELL_ID + 1)
    assert (zeile_allee.savings or {}).get("stadtbaum_avoided_days") == pytest.approx(
        14.2, abs=0.05)
    assert (zeile_allee.savings or {}).get("stadtbaum_missing_reason") is None
    # Die kronenlose Zelle verschwindet nicht stumm: eigener Vermerk trotz positiver
    # Kommunensumme.
    assert (zeile_ohne_kronen.savings or {}).get("stadtbaum_avoided_days") is None
    assert (zeile_ohne_kronen.savings or {}).get("stadtbaum_missing_reason") == "canopy"


# ── (e) Euro je Zelle (Ü-4, Befund 237): vermiedene Tage × c_Tag ─────────────────────

def test_zelle_traegt_vermiedene_euro(monkeypatch):
    """Allee-Zelle: 14,209 Tage × 6,20 € = 88,10 €; die Summe der Zell-Euro ist der
    Euro-Betrag der Kommune (ohne Kappung)."""
    summary, added = _run(_allee_cell(), {"anteil_ersetzt": ANTEIL_ERSETZT}, monkeypatch)

    zeile = next(o for o in added if o.measure_id == 1)
    assert (zeile.savings or {})["stadtbaum_avoided_days"] == pytest.approx(14.209, abs=0.001)
    assert (zeile.savings or {})["stadtbaum_avoided_eur"] == pytest.approx(88.10, abs=0.01)

    summe = sum((o.savings or {}).get("stadtbaum_avoided_eur", 0.0) for o in added)
    assert summe == pytest.approx(summary["stadtbaum_avoided_days_eur"], abs=0.01)
    assert summe == pytest.approx(summary["annual_benefit_damage_eur"], abs=0.01)


if __name__ == "__main__":
    import sys

    sys.exit(pytest.main([__file__, "-q"]))
