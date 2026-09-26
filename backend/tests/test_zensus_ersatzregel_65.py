"""Ersatzregel für den geheimgehaltenen Anteil 65+ (Bericht #95 §3.3, Log 41, Befund 116).

Die Zellen sind synthetisch, aber so gebaut, dass Einwohnersumme im Gitter, Einwohner ab 65 der
Zellen mit veröffentlichtem Anteil und Stufe 1 den Zahlen aus §3.3 entsprechen; die Gemeindezeile
kommt echt aus der Anlage backend/data/kalibrierung/zensus2022_demografie_ab65.csv ([69]).
Zielzahlen aus §3.3: Berlin 707.318, Warmsen 697 Einwohner ab 65.
"""
from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services import zensus_loader as zl  # noqa: E402
from app.services.engine import override_context  # noqa: E402

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def _gemeinde(published: list[tuple[float, float]], stufe1: list[tuple[float, float]],
              stufe2: list[float]):
    """Zellen: (Einwohner, Anteil 65+ in %), (Einwohner, Personen ab 65 im Altersgitter),
    Einwohner der Zellen ohne jede Angabe ab 65. Gibt (cell_inputs, grid_cells, zensus)."""
    pop, o65, ages, grid = {}, {}, {}, []
    n = 0
    for e, anteil in published:
        gid = f"P{n}"; n += 1
        pop[gid] = {"Einwohner": e}
        o65[gid] = {"AnteilUeber65": anteil}
        grid.append({"gitter_id": gid})
    for e, n65 in stufe1:
        gid = f"S1_{n}"; n += 1
        pop[gid] = {"Einwohner": e}
        ages[gid] = {"a65bis69": n65}  # übrige Gruppen ab 65 geheim („–“, zählen als 0)
        grid.append({"gitter_id": gid})
    for e in stufe2:
        gid = f"S2_{n}"; n += 1
        pop[gid] = {"Einwohner": e}
        grid.append({"gitter_id": gid})
    zensus = {"population": pop, "share_over_65": o65, "age_groups": ages}
    return [{} for _ in grid], grid, zensus


def _summe65(cis):
    return sum(ci["pop_over_65"] for ci in cis)


@pytest.fixture(autouse=True)
def _ohne_overrides():
    override_context.set_overrides(None)
    yield
    override_context.set_overrides(None)


def test_warmsen_zielzahl_697():
    # §3.3: Gitter 3087 Einwohner; 508 ab 65 in Zellen mit veröffentlichtem Anteil, 36 aus
    # Stufe 1; 1897 Einwohner in Zellen der Stufe 2.
    cis, grid, zensus = _gemeinde([(1000.0, 50.8)], [(190.0, 36.0)], [1000.0, 897.0])
    assert sum(z["Einwohner"] for z in zensus["population"].values()) == 3087
    zl.apply_zensus_to_cell_inputs(cis, grid, zensus, "03256034")
    assert round(_summe65(cis)) == 697
    s2 = [ci for ci in cis if ci["gitter_id"].startswith("S2_")]
    assert all(ci["share_over_65_herkunft"] == "ersatz_stufe2_gemeinde" for ci in s2)
    # §3.3 rechnet mit gerundeten Zahlen: R = 697 − 508 − 36 = 153 → 153 / 1897 = 8,07 %.
    # Ungerundet ist Z = 696,82, R = 152,82 → 8,056 %; daher 0,02 Prozentpunkte Toleranz.
    assert abs(s2[0]["share_over_65_ersatz"] - 8.07) < 0.02
    s1 = next(ci for ci in cis if ci["gitter_id"].startswith("S1_"))
    assert s1["share_over_65_herkunft"] == "ersatz_stufe1"
    assert abs(s1["pop_over_65"] - 36.0) < 1e-9
    # Bänder tragen dieselbe Menge 65+
    bands = sum(ci["pop_age_bands"][b] for ci in cis for b in ("a65_74", "a75_84", "a85p"))
    assert abs(bands - _summe65(cis)) < 1e-6


def test_berlin_zielzahl_707318():
    # §3.3: Gitter 3.593.357 Einwohner, davon 2,8 % in Zellen mit geheimgehaltenem Anteil.
    cis, grid, zensus = _gemeinde([(3_400_000.0, 20.3)], [(93_357.0, 2252.0)], [100_000.0])
    assert sum(z["Einwohner"] for z in zensus["population"].values()) == 3_593_357
    zl.apply_zensus_to_cell_inputs(cis, grid, zensus, "11000000")
    assert round(_summe65(cis)) == 707_318


def test_gemeindezeilen_aus_regionaltabelle():
    # [69]: Warmsen 3158 / 388 / 602, Berlin 3.596.999 / 292.354 / 624.505
    assert zl.demografie_zeile_ab65("03256034") == ((3158.0, 388.0, 602.0), "gemeinde")
    assert zl.demografie_zeile_ab65("11000000") == ((3596999.0, 292354.0, 624505.0), "gemeinde")
    a_g = zl.anteil_ab65_gemeinde((3158.0, 388.0, 602.0), 2 / 7)
    assert abs(a_g - 0.2257) < 0.00005


def test_kreiszeile_als_rueckfall_und_ohne_zeile():
    # Gemeinde ohne Zeile in [69] (anderer Gebietsstand): Kreiszeile, Befund 119
    zeile, ebene = zl.demografie_zeile_ab65("03256999")
    assert ebene == "kreis" and zeile == (120611.0, 13112.0, 24323.0)
    # Hanau: VG250 06415000, weder Gemeinde- noch Kreiszeile → kein Ersatzwert
    assert zl.demografie_zeile_ab65("06415000") == (None, None)
    cis, grid, zensus = _gemeinde([(1000.0, 50.8)], [], [500.0])
    zl.apply_zensus_to_cell_inputs(cis, grid, zensus, "06415000")
    assert cis[1]["share_over_65_herkunft"] == "ohne_ersatzwert"
    assert cis[1]["pop_over_65"] == 0.0


def test_ohne_ags_nur_stufe1():
    cis, grid, zensus = _gemeinde([(1000.0, 50.8)], [(190.0, 36.0)], [1897.0])
    zl.apply_zensus_to_cell_inputs(cis, grid, zensus)
    assert round(_summe65(cis)) == 508 + 36


def test_rest_negativ_gibt_null():
    # Zellen mit veröffentlichtem Anteil tragen schon mehr als Z → Stufe 2 bekommt 0 %
    cis, grid, zensus = _gemeinde([(3000.0, 40.0)], [], [87.0])
    zl.apply_zensus_to_cell_inputs(cis, grid, zensus, "03256034")
    assert cis[1]["share_over_65_ersatz"] == 0.0


def test_anteil_60_66_ist_registry_parameter_und_wirkt():
    from app.services.engine.impact.params import IMPACT_PARAM_SPECS
    spec = next(s for s in IMPACT_PARAM_SPECS
                if s["risk"] == "EXPECTED_ANNUAL_MORTALITY" and s["key"] == "anteil_60_66_ab65")
    assert spec["value"] == 2 / 7
    assert spec["evidence_class"] == "abgeschaetzt"
    assert zl.ANTEIL_60_66_PARAM_ID == "risks.EXPECTED_ANNUAL_MORTALITY.impact.anteil_60_66_ab65"
    # 7/7: die ganze Gruppe 60–66 zählt → Z = 990 / 3158 × 3087
    override_context.set_overrides({zl.ANTEIL_60_66_PARAM_ID: 1.0})
    cis, grid, zensus = _gemeinde([(1000.0, 50.8)], [(190.0, 36.0)], [1897.0])
    zl.apply_zensus_to_cell_inputs(cis, grid, zensus, "03256034")
    assert round(_summe65(cis)) == round(990 / 3158 * 3087)


def test_befund_116_alte_nullsetzung_entfernt():
    with open(os.path.join(REPO, "backend", "app", "services", "zensus_loader.py"),
              encoding="utf-8") as fh:
        assert 'share_o = ci.get("share_over_65") or 0.0' not in fh.read()
