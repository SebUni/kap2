"""Öffentliche Kühlzentren an COOLING_ROOMS_DRINKING_WATER (Bericht #95 §5 Z. 1203–1246,
Block ``heat.delta_kuehlzentren`` Kap. 7 Z. 1781–1790, Befunde 139, 148, Log 46).

``ΔD_KZ = [D_75–84 + D_85+ · (1 − h_Heim)] · (1 − δ_KZ)``, δ_KZ = 1 − 0,05 × 0,71 × 3/24
= 0,9956, im abgedeckten Teil der Kommune (wie die Schutzprogramme). Berlin (Kette):
1.054 YLL = 169,5 Mio. €, × 0,05 × 0,089 = 0,75 Mio. € je Jahr (Z. 1228). Zusammen mit
Hitzeaktionsplan und Schutzprogrammen gilt max(δ_HAP × δ_VG × δ_KZ; 0,794).

DB-frei: Rechenfunktionen in ``health``, Zellfaktor der Maßnahmen-Engine und
``compute_impact`` gegen eine Session-Doppel (Muster ``test_massnahme_s158_ausgabe.py``)
an einer Zelle mit den Berlin-Werten aus Kette 3.0 (Ebene 6: D_75–84 = 71,4, D_85+ = 153,6).
"""

from __future__ import annotations

import pytest

from app.data import catalog
from app.models.models import AdaptationMeasure, CellAssessment, ConfigParameter, Kommune
from app.services import measure_service, parameter_registry
from app.services.engine import override_context, risk_engine
from app.services.engine.impact import health

CODE = "COOLING_ROOMS_DRINKING_WATER"
MORT = "EXPECTED_ANNUAL_MORTALITY"
D75_BERLIN, D85_BERLIN = 71.4, 153.6     # Bericht #95 Kette 3.0, Ebene 6
KOMMUNE_ID = 1


@pytest.fixture(autouse=True)
def _keine_overrides():
    override_context.set_overrides({})
    yield
    override_context.set_overrides({})


def _berlin_cell() -> dict:
    yll = (D75_BERLIN * health.AGE_LIFE_YEARS["a75_84"]
           + D85_BERLIN * health.AGE_LIFE_YEARS["a85p"] + 1000.0)
    return {"index": 50.0, "outcome": yll,
            "deaths_a75_84": D75_BERLIN, "deaths_a85p": D85_BERLIN}


def _base_eur(cell: dict) -> float:
    return risk_engine.cost_from_outcome(catalog.RISKS_BY_CODE[MORT], cell["outcome"])


def _kz_eur(frac: float = 1.0, **kw) -> float:
    cell = _berlin_cell()
    return _base_eur(cell) * (1.0 - measure_service._kz_cell_factor(frac, cell, **kw))


# ── Parameter und Formel ─────────────────────────────────────────────────────────

def test_delta_kz_from_registry():
    assert health.DELTA_KZ == pytest.approx(0.9956, abs=1e-12)
    assert 1.0 - 0.05 * 0.71 * 3.0 / 24.0 == pytest.approx(health.DELTA_KZ, abs=0.00005)
    assert measure_service._s157_param("delta_kuehlzentren", -1.0) == pytest.approx(0.9956)


def test_formula_deaths_berlin():
    """ΔD_KZ = [71,4 + 153,6 × (1 − 0,344)] × 0,0044 ≈ 0,76 Todesfälle."""
    d = health.kz_avoided(D75_BERLIN, D85_BERLIN)
    soll = (D75_BERLIN + D85_BERLIN * (1.0 - health.h_heim())) * (1.0 - 0.9956)
    assert d == pytest.approx(soll, rel=1e-12)


# ── Kette Berlin (Bericht §5 Z. 1228) ────────────────────────────────────────────

def test_berlin_chain_0_75_mio_eur():
    eur = _kz_eur()
    assert eur / 1e6 == pytest.approx(0.75, abs=0.05)
    # Rechenweg des Berichts: 169,5 Mio. € × 0,05 × 0,089
    assert 169.5 * 0.05 * 0.089 == pytest.approx(0.75, abs=0.005)


def test_band_reichweite_0_15_bis_1_50_mio_eur():
    for r, soll in ((0.01, 0.15), (0.10, 1.50)):
        override_context.set_overrides(
            {f"risks.{MORT}.impact.delta_kuehlzentren": 1.0 - r * 0.71 * 3.0 / 24.0})
        assert _kz_eur() / 1e6 == pytest.approx(soll, abs=0.02)


def test_covered_part_only():
    """Wie die Schutzprogramme im abgedeckten Teil: halbe Deckung, halber Betrag."""
    assert _kz_eur(0.5) == pytest.approx(_kz_eur(1.0) / 2.0, rel=1e-12)
    assert _kz_eur(0.0) == 0.0


def test_old_cells_without_band_values_unchanged():
    assert measure_service._kz_cell_factor(1.0, {"outcome": 10.0, "deaths_a85p": 5.0}) == 1.0


# ── Kappung max(δ_HAP × δ_VG × δ_KZ; 0,794) ──────────────────────────────────────

def test_kappung_zentral_greift_nicht():
    """0,95 × 0,931 × 0,9956 = 0,881 > 0,794 (Bericht Z. 1238)."""
    d_and = 0.95 * health.DELTA_VG
    assert d_and * health.kz_effective_delta(health.DELTA_KZ, d_and) == \
        pytest.approx(0.881, abs=0.001)
    assert health.kz_effective_delta(health.DELTA_KZ, d_and) == health.DELTA_KZ


def test_kappung_am_paketwert():
    # δ_HAP × δ_VG schon am Paketwert: die Kühlzentren nehmen nichts mehr weg
    assert health.kz_effective_delta(health.DELTA_KZ, 0.794) == pytest.approx(1.0)
    assert _kz_eur(hap_cap=0.85, vg_cap=0.794 / 0.85) == pytest.approx(0.0, abs=1e-6)
    # knapp darüber: nur der Rest bis 0,794
    d_and = 0.797
    assert d_and * health.kz_effective_delta(health.DELTA_KZ, d_and) == \
        pytest.approx(0.794, abs=1e-12)


# ── Maßnahme: S157 plus Kühlzentren, Summe der Einzelnutzen = Aggregat ─────────────

def test_measure_factor_adds_s157_and_kz():
    mdef = catalog.MEASURES_BY_CODE[CODE]
    cell = _berlin_cell()
    f = measure_service._measure_cell_factor(mdef, {}, MORT, 1.0, 1.0, cell)
    f_s157 = measure_service._s157_cell_factor(0.11, 1.0, cell)
    f_kz = measure_service._kz_cell_factor(1.0, cell)
    assert f == pytest.approx(f_s157 + f_kz - 1.0, rel=1e-12)
    assert f < f_s157 < 1.0


def test_sum_of_single_benefits_equals_aggregate_with_hap_and_vg():
    cell = _berlin_cell()
    base = _base_eur(cell)
    d_hap = 0.95
    f_vg = measure_service._vg_cell_factor(MORT, 1.0, cell, 1.0, d_hap)
    d_vg, vg_cap = measure_service._vg_kz_factors([1.0], cell, d_hap)
    assert d_vg == pytest.approx(f_vg, rel=1e-12)
    f_kz_agg = measure_service._kz_cell_factor(1.0, cell, hap_cap=d_hap, vg_cap=vg_cap)
    aggregat = base * (1.0 - d_hap * f_vg * f_kz_agg)
    einzel_hap = base * (1.0 - d_hap)
    einzel_vg = base * (1.0 - measure_service._vg_cell_factor(MORT, 1.0, cell, d_hap, d_hap))
    einzel_kz = base * (1.0 - measure_service._kz_cell_factor(
        1.0, cell, d_hap, d_hap, d_vg, vg_cap))
    assert einzel_hap + einzel_vg + einzel_kz == pytest.approx(aggregat, rel=1e-9)


# ── Zusammenfassung der Maßnahme: Betrag der Kühlzentren getrennt von S157 ─────────

class _Q:
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


def _summary(monkeypatch) -> dict:
    measure = AdaptationMeasure(
        id=1, kommune_id=KOMMUNE_ID, name="Kühle Räume Test", measure_type=CODE,
        geometry=None, config={}, implementation_year=2027, description="",
        impact_summary={})
    kommune = Kommune(id=KOMMUNE_ID, name="Berlin (Kette)", osm_id="R-KZ",
                      population=3_700_000, area_km2=891.0)
    cell = CellAssessment(id=10, kommune_id=KOMMUNE_ID, grid_cell_id=10,
                          data={"risks": {MORT: _berlin_cell()}, "inputs": {"pop": 1000.0}})
    db = _DB({AdaptationMeasure: [measure], CellAssessment: [cell],
              ConfigParameter: [], Kommune: [kommune]})
    monkeypatch.setattr(measure_service, "_coverage", lambda _db, _m: ({10: 1.0}, 200_000.0))
    monkeypatch.setattr(measure_service, "_params_fingerprint", lambda *a, **k: "fp-kz")
    monkeypatch.setattr(parameter_registry, "load_db_overrides", lambda *a, **k: [])
    monkeypatch.setattr(measure_service, "get_risk_aggregate",
                        lambda *a, **k: {"risks": {MORT: {"cost_eur": 1e12}}})
    return measure_service.compute_impact(db, measure.id)


def test_summary_kuehlzentren_berlin_0_75_mio_eur_getrennt_von_s157(monkeypatch):
    s = _summary(monkeypatch)
    assert s["kuehlzentren_benefit_eur"] / 1e6 == pytest.approx(0.75, abs=0.05)
    assert s["kuehlzentren_estimate_note"] == "Abschätzung von KAP3"
    assert s["delta_kuehlzentren"] == pytest.approx(0.9956)
    # S157 ohne Eingabe (Voreinstellung 0,11): 1,2 Mio. € (Bericht Z. 1148), getrennt
    assert s["s157_benefit_eur"] / 1e6 == pytest.approx(1.2, abs=0.05)
    assert s["kuehlzentren_benefit_eur"] + s["s157_benefit_eur"] == \
        pytest.approx(s["annual_benefit_damage_eur"], abs=0.02)


def test_catalog_entry_describes_s157_and_public_cooling_centres():
    m = catalog.MEASURES_BY_CODE[CODE]
    assert m["effect_model"] == "s157"
    assert m["linked_risk_codes"] == [MORT]
    text = m["description"]
    assert "S157" in text and "Heim" in text
    assert "Öffentliche Kühlzentren" in text and "δ_KZ" in text
