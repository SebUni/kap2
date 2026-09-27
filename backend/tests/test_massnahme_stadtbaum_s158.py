"""T-1602-cto: Stadtbaumwahl zusammen mit S158 — die Frühwarnung wirkt auf die Tage
NACH der Pflanzung, kein vermiedener Tag zählt doppelt (Bericht #96 §5 Z. 1102–1107).

Vorhabenskriterium (iv), Vorhaben T-1483-cto. Die Stadtbaumwahl rechnet ihren Nutzen
gegen den Ausgangsstand (Ĝ), die Frühwarnung gegen P̂′ der Zellen, die eine
Stadtbaumwahl DERSELBEN Kommune (und Demo-Sitzung) abdeckt (Muster
``measure_service._hap_measures``/``_hap_cell_factors``, hier
``_stadtbaum_measures``/``_stadtbaum_cell_days_factors``). In ``_adjusted_cell_data``
multiplizieren sich die Faktoren schon (T-1602-cto-Ergänzung der bestehenden
Zell-Schleife); das bleibt so.

Rechenbeispiel Allee-Zelle (Berlin Mitte, Bericht §5.1 Z. 1200–1206): Betroffene B 100,
δ_R = δ_Birke + δ_Gräser = 0,8085 + 1,0710 = 1,8795, Ḡ₀ 0,18125, Ĝ 0,3625 (Ĝ/Ḡ₀ = 2)
→ Zusatztage im Ausgangsstand (P̂ = 1 + 0,70·(2−1) = 1,7): 100·1,8795·1,7 = 319,515.
Die Stadtbaumwahl (``anteil_ersetzt`` 1,0, ``canopy_birch_frac`` 0,078125,
``canopy_unknown_frac`` 0) senkt Ĝ auf Ĝ′ = 0,3625 − 0,464·0,078125 = 0,32625
(Ĝ′/Ḡ₀ = 1,8, P̂′ = 1 + 0,70·(1,8−1) = 1,56) → Tage nach der Pflanzung:
100·1,8795·1,56 = 293,202 (Stadtbaumwahl-Nutzen 319,515 − 293,202 = 26,313 Tage).
S158 (r_S158 0,03, t_warn 0,75) mindert davon 0,03·0,75·293,202 = 6,597 Tage — nicht
0,03·0,75·319,515 = 7,19 Tage (das wäre die doppelt zählende Rechnung gegen den
Ausgangsstand).

Geprüft wird (Abnahmekriterium T-1602-cto):
(a) ``_adjusted_cell_data`` (beide Maßnahmen, volle Deckung) ergibt 286,605 Tage
    (293,202 − 6,597 = 319,515 − 26,313 − 6,597).
(b) ``compute_impact`` der Frühwarnung weist 6,597 vermiedene Tage aus (nicht 7,19),
    die Stadtbaumwahl 26,313 (Delta des Index, hier bitgleich der Tage — s. ``_cell``).
(c) Die Summe beider Einzelnutzen ist exakt 319,515 − Tage mit beiden Maßnahmen (auf
    den unrundeten Werten, kein vermiedener Tag zählt doppelt).
(d) Ohne Stadtbaumwahl in der Zelle bleibt die Frühwarnung bei 7,19 Tagen (unveränderter
    Ausgangsstand, Muster ``test_massnahme_s158.py``).

DB-frei: (c) prüft die reinen Zellfunktionen (``_stadtbaum_cell_factor``,
``_s158_cell_effect``); (a), (b), (d) laufen über ``_adjusted_cell_data`` und
``compute_impact`` gegen ein Session-Doppel (Muster ``test_massnahme_s158_ausgabe.py``),
hier mit echter Attribut-Filterung (``AdaptationMeasure.id``/``.measure_type``), weil
in dieser Datei — anders als dort — mehrere Maßnahmen derselben Kommune vorkommen.
"""

from __future__ import annotations

import pytest

from app.data import catalog
from app.models.models import AdaptationMeasure, CellAssessment, ConfigParameter, Kommune
from app.services import measure_service, parameter_registry
from app.services.engine import override_context
from app.services.engine.impact import health

S158_CODE = "POLLEN_EARLY_WARNING"
STADTBAUM_CODE = "LOW_ALLERGEN_TREE_SELECTION"
RISK = "EXPECTED_ANNUAL_ALLERGY_DAYS"
KOMMUNE_ID = 1
CELL_ID = 42

# Rechenbeispiel (Berlin Mitte, s. Modul-Docstring).
BETROFFENE = 100.0
DELTA_BIRKE = 0.8085
DELTA_GRAESER = 1.0710
G_BAR0 = 0.18125
G_CELL = 0.3625          # Ĝ/Ḡ₀ = 2
CANOPY_BIRKE = 0.078125  # → Ĝ′/Ḡ₀ = 1,8
CANOPY_UNBEK = 0.0
GRUEN = 0.3
ANTEIL_ERSETZT = 1.0
LAM = 0.70
R_S158 = 0.03
T_WARN = 0.75


def setup_function(_fn=None) -> None:
    override_context.set_overrides({})


def teardown_function(_fn=None) -> None:
    override_context.set_overrides({})


def _cell(index_value: float) -> dict:
    """Roheingaben der Allee-Zelle + ``index``/``outcome`` (bitgleich gesetzt, damit
    Faktor·Index in diesem Test direkt als „Tage" lesbar ist, Muster
    ``test_massnahme_s158_ausgabe.py::_cell``)."""
    return {
        "index": index_value, "outcome": index_value,
        "betroffene": BETROFFENE, "delta_birke": DELTA_BIRKE, "delta_graeser": DELTA_GRAESER,
        "pollen_g": G_CELL, "pollen_g_bar0": G_BAR0,
        "canopy_birch_frac": CANOPY_BIRKE, "canopy_unknown_frac": CANOPY_UNBEK,
        "green_frac": GRUEN,
    }


def _tage_ausgangsstand() -> float:
    tage_b, tage_g = health.pollen_zelltage(
        BETROFFENE, DELTA_BIRKE, DELTA_GRAESER, G_CELL, G_BAR0, LAM)
    return tage_b + tage_g


TOTAL0 = _tage_ausgangsstand()  # 319,515


# ── Session-Doppel mit echter Attribut-Filterung (mehrere Maßnahmen je Kommune) ──────

class _Q:
    def __init__(self, rows, conds=None):
        self._rows = list(rows)
        self._conds = list(conds or [])

    @staticmethod
    def _matches(row, cond) -> bool:
        key = getattr(getattr(cond, "left", None), "key", None)
        if key is None:
            return True
        right = getattr(getattr(cond, "right", None), "value", None)
        left_val = getattr(row, key, None)
        if isinstance(right, (list, tuple, set)):
            return left_val in right
        return left_val == right

    def filter(self, *conds):
        return _Q(self._rows, self._conds + list(conds))

    filter_by = filter

    def all(self):
        rows = self._rows
        for c in self._conds:
            rows = [r for r in rows if self._matches(r, c)]
        return rows

    def first(self):
        rows = self.all()
        return rows[0] if rows else None

    def delete(self):
        return 0

    def scalar(self):
        return None

    def yield_per(self, _n):
        return self.all()


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


def _measure(mid: int, code: str, config: dict | None = None) -> AdaptationMeasure:
    return AdaptationMeasure(
        id=mid, kommune_id=KOMMUNE_ID, name=f"Testmaßnahme {mid}", measure_type=code,
        geometry=None, config=config or {}, implementation_year=2027, description="",
        impact_summary={})


def _db(cell_risk: dict, measures: list[AdaptationMeasure]) -> _DB:
    ca = CellAssessment(id=CELL_ID, kommune_id=KOMMUNE_ID, grid_cell_id=CELL_ID,
                        data={"risks": {RISK: cell_risk}, "inputs": {"pop": 100.0}})
    kommune = Kommune(id=KOMMUNE_ID, name="Testheim", osm_id="R-STADTBAUM-S158",
                      population=10_000, area_km2=5.0)
    return _DB({AdaptationMeasure: measures, CellAssessment: [ca],
               ConfigParameter: [], Kommune: [kommune]})


def _patch_common(monkeypatch) -> None:
    monkeypatch.setattr(measure_service, "_coverage",
                        lambda _db, _m: ({CELL_ID: 1.0}, 1000.0))
    monkeypatch.setattr(measure_service, "_params_fingerprint",
                        lambda *a, **k: "fp-test-stadtbaum-s158")
    monkeypatch.setattr(parameter_registry, "load_db_overrides", lambda *a, **k: [])
    monkeypatch.setattr(
        measure_service, "get_risk_aggregate",
        lambda *a, **k: {"risks": {RISK: {"cost_eur": 1_000_000_000.0}}})


# ── (a) _adjusted_cell_data: beide Maßnahmen zusammen, 286,605 Tage ──────────────────

def test_adjusted_cell_data_beide_massnahmen_286_605(monkeypatch):
    m_s158 = _measure(1, S158_CODE)
    m_baum = _measure(2, STADTBAUM_CODE, {"anteil_ersetzt": ANTEIL_ERSETZT})
    db = _db(_cell(TOTAL0), [m_s158, m_baum])
    _patch_common(monkeypatch)

    out = measure_service._adjusted_cell_data(db, KOMMUNE_ID, apply_measures=True)
    assert len(out) == 1
    assert out[0]["risks"][RISK]["outcome"] == pytest.approx(286.605, abs=0.005)
    assert out[0]["risks"][RISK]["index"] == pytest.approx(286.605, abs=0.005)


# ── (b) compute_impact: Frühwarnung 6,597, Stadtbaumwahl 26,313 ─────────────────────

def test_compute_impact_fruehwarnung_6_597_avoided_days(monkeypatch):
    m_s158 = _measure(1, S158_CODE)
    m_baum = _measure(2, STADTBAUM_CODE, {"anteil_ersetzt": ANTEIL_ERSETZT})
    db = _db(_cell(TOTAL0), [m_s158, m_baum])
    _patch_common(monkeypatch)

    measure_service.compute_impact(db, 1)
    zeile = next(o for o in db.added if o.measure_id == 1)
    assert (zeile.savings or {}).get("s158_avoided_days") == pytest.approx(6.597, abs=0.005)


def test_compute_impact_stadtbaumwahl_26_313_avoided_days(monkeypatch):
    m_s158 = _measure(1, S158_CODE)
    m_baum = _measure(2, STADTBAUM_CODE, {"anteil_ersetzt": ANTEIL_ERSETZT})
    db = _db(_cell(TOTAL0), [m_s158, m_baum])
    _patch_common(monkeypatch)

    measure_service.compute_impact(db, 2)
    zeile = next(o for o in db.added if o.measure_id == 2)
    # index == outcome == Tage (s. ``_cell``): das Delta des Index ist hier bitgleich
    # den vermiedenen Tagen der Stadtbaumwahl.
    avoided = -(zeile.indicator_deltas or {}).get(RISK, 0.0)
    assert avoided == pytest.approx(26.313, abs=0.005)


# ── (c) kein vermiedener Tag zählt doppelt: exakte Summe auf den unrundeten Werten ──

def test_summe_beider_nutzen_gleich_ausgangsstand_minus_kombiniert():
    cell = _cell(TOTAL0)
    stadtbaum_factor = measure_service._stadtbaum_cell_factor(
        {"anteil_ersetzt": ANTEIL_ERSETZT}, 1.0, cell)
    total_nach_pflanzung = TOTAL0 * stadtbaum_factor
    vermieden_stadtbaum = TOTAL0 - total_nach_pflanzung

    mdef = catalog.MEASURES_BY_CODE[S158_CODE]
    factor_s158, vermieden_s158, missing = measure_service._s158_cell_effect(
        mdef, 1.0, cell, days_factor=stadtbaum_factor)
    assert missing is False

    kombiniert = TOTAL0 * stadtbaum_factor * factor_s158
    assert (vermieden_stadtbaum + vermieden_s158) == pytest.approx(
        TOTAL0 - kombiniert, abs=1e-6)
    assert kombiniert == pytest.approx(286.605, abs=0.005)
    assert vermieden_stadtbaum == pytest.approx(26.313, abs=0.005)
    assert vermieden_s158 == pytest.approx(6.597, abs=0.005)


# ── (d) ohne Stadtbaumwahl in der Zelle: Frühwarnung bleibt bei 7,19 Tagen ───────────

def test_compute_impact_ohne_stadtbaumwahl_bleibt_bei_7_19(monkeypatch):
    m_s158 = _measure(1, S158_CODE)
    db = _db(_cell(TOTAL0), [m_s158])  # keine Stadtbaumwahl in der Kommune
    _patch_common(monkeypatch)

    measure_service.compute_impact(db, 1)
    zeile = next(o for o in db.added if o.measure_id == 1)
    assert (zeile.savings or {}).get("s158_avoided_days") == pytest.approx(7.19, abs=0.005)


if __name__ == "__main__":
    import sys

    sys.exit(pytest.main([__file__, "-q"]))
