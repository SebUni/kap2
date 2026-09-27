"""T-1515-cto: Ausgabe vermiedene Tage und Euro der Pollen-Frühwarnung (#96 S158).

Integrationsauflage S158, Punkt 5 (Bericht #96 §5.1 Z. 1416 f.) und Vorhabens-Kriterium
(iv): Vorgaben P1/P2. Das ``impact_summary`` einer S158-Maßnahme (``POLLEN_EARLY_WARNING``)
trägt die vermiedenen Symptomtage und Euro/Jahr der Kommune, gekennzeichnet als
begründete Abschätzung von KAP3 (``r_S158``, ``t_warn`` sind keine belegten
Effektgrößen). Fehlt in einer abgedeckten Zelle mit Zusatztagen die Gruppenaufteilung
(Alt-Zelle vor der Neuberechnung), entsteht kein zu niedriger Betrag, sondern ein
Vermerk (P2: nie 0 € wegen fehlender Eingabe).

Geprüft wird über ``measure_service.compute_impact`` (die volle Rechenkette, kein
Ausschnitt) mit einer Session-Doppel (Muster ``test_massnahmen_export_gewissheit.py``:
Filter geben immer die vollständigen vorgehaltenen Zeilen zurück, weil je Test nur
eine Maßnahme/Kommune vorkommt):

(a) Zwei abgedeckte Zellen mit vollständiger Gruppenaufteilung: die Kommunensumme der
    vermiedenen Tage entspricht der Summe der MeasureImpact-Zeilen je Zelle, dazu ein
    Euro-Betrag und die Kennzeichnung „Abschätzung von KAP3“.
(b) Eine abgedeckte Zelle mit Zusatztagen (Outcome > 0), aber ohne Gruppenaufteilung
    (Alt-Zelle): ``benefit_display`` trägt einen Vermerk statt eines Betrags, kein
    Zahlenfeld für die vermiedenen Tage/Euro, und ``annual_benefit_damage_eur`` bleibt
    0 (kein 0 € als sichtbarer Nutzen #96, weil ``benefit_display`` das Feld verdeckt).
(c) Ohne Überschreibung ist der Euro-Betrag der Kommune (``s158_avoided_days_eur``)
    gleich dem Anteil #96 an ``annual_benefit_damage_eur`` — hier: gleich dem ganzen
    Betrag, weil POLLEN_EARLY_WARNING ausschließlich EXPECTED_ANNUAL_ALLERGY_DAYS
    verknüpft.

DB-frei (Session-Doppel); ``_coverage`` (PostGIS) und ``get_risk_aggregate`` (Kappungs-
Basis) werden mit festen Werten ersetzt.
"""

from __future__ import annotations

import pytest

from app.data import catalog
from app.models.models import AdaptationMeasure, CellAssessment, ConfigParameter, Kommune
from app.services import measure_service, parameter_registry

CODE = "POLLEN_EARLY_WARNING"
RISK = "EXPECTED_ANNUAL_ALLERGY_DAYS"
KOMMUNE_ID = 1


class _Q:
    """Query-Doppel: ``filter`` ignoriert das Prädikat (je Test genau eine Maßnahme/
    Kommune) und liefert immer die vollständige vorgehaltene Zeilenmenge zurück
    (Muster ``test_massnahmen_export_gewissheit.py``)."""

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


def _cell(betroffene: float, delta_birke: float, delta_graeser: float,
         outcome: float | None = None) -> dict:
    """Roheingaben + Outcome einer Zelle mit voller Gruppenaufteilung.

    ``outcome`` = Σ Gruppentage (P̂ = 1, Ĝ_z = Ḡ₀), damit der Zellkosten-Nutzen im Test
    bitgleich dem Rate-Produkt der vermiedenen Tage ist (kein Rundungsrauschen).
    """
    tage = betroffene * (delta_birke + delta_graeser)
    return {
        "index": tage, "outcome": outcome if outcome is not None else tage,
        "betroffene": betroffene, "delta_birke": delta_birke, "delta_graeser": delta_graeser,
        "pollen_g": 1.0, "pollen_g_bar0": 1.0,
    }


def _run(cells: dict[int, dict], frac_map: dict[int, float], monkeypatch,
        area_m2: float = 1000.0, base_agg_cost_eur: float = 1_000_000.0) -> tuple[dict, list]:
    """Führt ``compute_impact`` gegen eine Session-Doppel aus und gibt (summary,
    gespeicherte MeasureImpact-Zeilen) zurück."""
    measure = AdaptationMeasure(
        id=1, kommune_id=KOMMUNE_ID, name="Pollen-Frühwarnung Test", measure_type=CODE,
        geometry=None, config={}, implementation_year=2027, description="",
        impact_summary={})
    kommune = Kommune(id=KOMMUNE_ID, name="Testheim", osm_id="R-S158", population=10_000,
                      area_km2=5.0)
    assessments = [
        CellAssessment(id=cid, kommune_id=KOMMUNE_ID, grid_cell_id=cid,
                       data={"risks": {RISK: risk}, "inputs": {"pop": 100.0}})
        for cid, risk in cells.items()
    ]
    db = _DB({AdaptationMeasure: [measure], CellAssessment: assessments,
             ConfigParameter: [], Kommune: [kommune]})

    monkeypatch.setattr(measure_service, "_coverage", lambda _db, _m: (frac_map, area_m2))
    monkeypatch.setattr(measure_service, "_params_fingerprint",
                        lambda *a, **k: "fp-test-s158")
    monkeypatch.setattr(parameter_registry, "load_db_overrides", lambda *a, **k: [])
    monkeypatch.setattr(
        measure_service, "get_risk_aggregate",
        lambda *a, **k: {"risks": {RISK: {"cost_eur": base_agg_cost_eur}}})

    summary = measure_service.compute_impact(db, measure.id)
    return summary, db.added


# ── (a) vollständige Gruppenaufteilung: Kommunensumme = Summe der Zellzeilen ─────

def test_kommune_avoided_days_and_euro_match_cell_rows(monkeypatch):
    cells = {
        10: _cell(betroffene=100.0, delta_birke=0.5, delta_graeser=0.5),  # Tage = 100
        11: _cell(betroffene=200.0, delta_birke=0.4, delta_graeser=0.6),  # Tage = 200
    }
    frac_map = {10: 1.0, 11: 0.5}
    summary, added = _run(cells, frac_map, monkeypatch)

    assert summary["s158_estimate_note"] == "Abschätzung von KAP3"
    assert summary.get("benefit_display") is None
    assert summary["s158_avoided_days_total"] > 0.0
    assert summary["s158_avoided_days_eur"] > 0.0

    rows_sum = sum(o.indicator_deltas.get("s158_avoided_days", 0.0) for o in added)
    assert rows_sum == pytest.approx(summary["s158_avoided_days_total"], abs=0.05)

    # Erwartungswert unabhängig nachgerechnet (r = 0,03 Katalog, t_warn = 0,75 Default).
    r = catalog.MEASURES_BY_CODE[CODE]["default_reduction"]
    t_warn = 0.75
    vermieden_10 = 1.0 * r * t_warn * 100.0  # Ĝ/Ḡ₀ = 1 ⇒ P̂ = 1, Tage = Betroffene·Σδ
    vermieden_11 = 0.5 * r * t_warn * 200.0
    erwartet = vermieden_10 + vermieden_11
    assert summary["s158_avoided_days_total"] == pytest.approx(round(erwartet, 1), abs=0.05)


# ── (b) Zelle mit Zusatztagen ohne Gruppenaufteilung: Vermerk statt Betrag ───────

def test_missing_group_split_shows_note_not_amount(monkeypatch):
    legacy_cell = {"index": 150.0, "outcome": 150.0}  # Alt-Zelle: keine Roheingaben
    summary, added = _run({20: legacy_cell}, {20: 1.0}, monkeypatch)

    assert summary["benefit_display"] == measure_service.S158_MISSING_SPLIT_TEXT
    assert summary.get("benefit_missing_input") == "pollen_group_split"
    assert "s158_avoided_days_total" not in summary
    assert "s158_avoided_days_eur" not in summary
    # Kein 0 € als Nutzen #96: die Zelle bleibt unverändert (Faktor 1,0), damit trägt
    # annual_benefit_damage_eur hier 0 — sichtbar wird das nicht, weil benefit_display
    # den Betrag in Sidebar/Tabelle verdeckt (dieselbe Weiche wie bei S157).
    assert summary["annual_benefit_damage_eur"] == 0.0
    assert added and added[0].indicator_deltas.get("s158_avoided_days") is None


# ── (c) ohne Überschreibung: Euro-Kommunenwert = Anteil #96 an annual_benefit_damage_eur ──

def test_euro_value_equals_share_of_annual_benefit_damage(monkeypatch):
    cells = {30: _cell(betroffene=100.0, delta_birke=0.5, delta_graeser=0.5)}
    summary, _ = _run(cells, {30: 1.0}, monkeypatch)

    assert summary["s158_avoided_days_eur"] == pytest.approx(
        summary["annual_benefit_damage_eur"], rel=1e-9)


if __name__ == "__main__":
    import sys

    sys.exit(pytest.main([__file__, "-q"]))
