"""Golden-Tests der Methodik #95 (Hitzebelastung, Bericht Rev. 7).

Drei Prüfklassen (Integrations-Kontrakt, AUFGABE §7 / integriere-risiko §4):

1. **Beispiel-Blöcke**: jeder ausführbare ```python test:``-Block des Berichts
   ``docs/methodik/95_hitzebelastung.md`` läuft als Test — Bericht und Repo
   können nicht divergieren, ohne dass CI rot wird.
2. **Registry ⇄ Bericht**: die maschinenlesbaren Kap.-7-Werte des Berichts
   müssen exakt den Registry-Specs/Katalogwerten entsprechen (kein stiller
   Code-Fix; Eiserne Regel 5).
3. **Sanity-/Struktur-Anker aus Kap. 4**: Morbiditäts-Bundessumme im
   Destatis/K&Z-Band; Verteilschlüssel-Lackmustest (§3.1) für die Mortalität.
"""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402
from app.services.engine import override_context  # noqa: E402
from app.services.engine.impact import health as H  # noqa: E402

REPORT = os.path.join(os.path.dirname(__file__), "..", "..",
                      "docs", "methodik", "95_hitzebelastung.md")

MORT, MORB = "EXPECTED_ANNUAL_MORTALITY", "EXPECTED_ANNUAL_MORBIDITY"


def _report_text() -> str:
    with open(os.path.abspath(REPORT), encoding="utf-8") as fh:
        return fh.read()


def _spec(risk: str, key: str) -> dict:
    from app.services.engine.impact.params import IMPACT_PARAM_SPECS
    for s in IMPACT_PARAM_SPECS:
        if s["risk"] == risk and s["key"] == key:
            return s
    raise AssertionError(f"Registry-Spec fehlt: {risk}.{key}")


# ── 1. Beispiel-Blöcke des Berichts ───────────────────────────────────────────

def test_report_example_blocks_green():
    """Jeder ```python test:``-Block des Berichts muss ausführbar und grün sein."""
    blocks = re.findall(r"```python test: (\S+)\n(.*?)```", _report_text(), re.S)
    assert len(blocks) >= 10, "Bericht #95 muss mindestens 10 Beispiel-Blöcke tragen"
    for name, code in blocks:
        try:
            exec(compile(code, f"95:{name}", "exec"), {})  # noqa: S102
        except Exception as e:  # pragma: no cover - Fehlerpfad
            raise AssertionError(f"Beispiel-Block {name} rot: {e}") from e


# ── 2. Registry/Katalog ⇄ Bericht (Kap. 7) ───────────────────────────────────

def test_registry_matches_report_parameters():
    """Kap.-7-Werte des Berichts == Registry-Specs (Divergenz = Ledger-Fall)."""
    # Mortalität
    assert _spec(MORT, "calibration")["value"] == 0.581
    assert _spec(MORT, "beta_85p_nord")["value"] == 0.0634
    assert _spec(MORT, "beta_85p_mitte")["value"] == 0.0625
    assert _spec(MORT, "beta_85p_sued")["value"] == 0.0876     # 0,0531 × 1,65 (Rev. 7)
    assert abs(_spec(MORT, "beta_85p_sued")["value"] - 0.0531 * 1.65) < 1e-4
    for key, val in (("threshold_nord", 19.7), ("threshold_mitte", 20.2),
                     ("threshold_sued", 20.8)):
        assert _spec(MORT, key)["value"] == val
    for key, val in (("beta_factor_u65", 0.357), ("beta_factor_a65_74", 0.588),
                     ("beta_factor_a75_84", 0.631), ("beta_factor_a85p", 1.0)):
        assert _spec(MORT, key)["value"] == val
    for key, val in (("baseline_mort_u65", 213.2), ("baseline_mort_a65_74", 1737.9),
                     ("baseline_mort_a75_84", 4812.3), ("baseline_mort_a85p", 14800.2)):
        assert _spec(MORT, key)["value"] == val
    for key, val in (("life_years_u65", 23.39), ("life_years_a65_74", 15.59),
                     ("life_years_a75_84", 8.90), ("life_years_a85p", 4.16)):
        assert _spec(MORT, key)["value"] == val
    assert _spec(MORT, "beta_iso")["value"] == 0.90
    assert _spec(MORT, "beta_pfl")["value"] == 1.54
    assert _spec(MORT, "qbar_1p")["value"] == 0.346
    assert _spec(MORT, "qbar_pfl")["value"] == 0.149
    assert _spec(MORT, "beta_dist_km")["value"] == 0.0         # Sensitivität, Basiswert 0
    # Morbidität
    for key, val in (("r0_u65", 1.9), ("r0_a65_74", 6.3), ("r0_a75_84", 10.8),
                     ("r0_a85p", 15.6), ("excess_per_hotday", 0.024),
                     ("hotday_ref_days", 7.2)):
        assert _spec(MORB, key)["value"] == val


def test_cost_rates_match_report():
    """Monetarisierung (Bericht §3.5): VOLY 160.800 €₂₀₂₄, c_Fall 7.152 €₂₀₂₄."""
    mort = catalog.RISKS_BY_CODE[MORT]
    morb = catalog.RISKS_BY_CODE[MORB]
    assert catalog.risk_default_cost_per_outcome(mort) == 160_800.0
    assert catalog.risk_default_cost_per_outcome(morb) == 7_152.0
    # Native Ergebnisgröße (§3.6): genau eine je Code — YLL bzw. Fälle.
    assert mort["outcome_unit"] == "YLL/Jahr"
    assert morb["outcome_unit"] == "Fälle/Jahr"


def test_week_anomalies_match_report_table():
    """Wochenquantile (§3.2): Produktionskonstanten == Berichtstabelle (±0,006 K —
    die Berichtstabelle rundet die CSV-Anlage auf 2 Dezimalen; halbe
    Rundungseinheit + Fließkomma-Epsilon)."""
    table = {
        "nord": (-4.17, -2.81, -2.00, -1.45, -0.99, -0.50, 0.00,
                 0.42, 0.89, 1.54, 2.10, 2.83, 4.22),
        "mitte": (-4.59, -3.04, -2.27, -1.64, -1.12, -0.57, -0.04,
                  0.51, 1.05, 1.65, 2.32, 3.16, 4.60),
        "sued": (-4.67, -2.99, -2.23, -1.65, -1.11, -0.57, -0.03,
                 0.51, 1.12, 1.75, 2.36, 3.18, 4.46),
    }
    for region, vals in table.items():
        got = H.REGION_WEEK_ANOMALIES[region]
        assert len(got) == 13, region
        for w, (a, b) in enumerate(zip(vals, got), start=1):
            assert abs(a - b) < 0.006, (region, w, a, b)


def test_voly_consistency_check():
    """§3.2-Konsistenzcheck des Berichts: VSL ÷ VOLY ≈ plausible Lebensjahre."""
    assert abs(6_190_000 / 160_800 - 38.5) < 0.1


# ── 3. Sanity-/Struktur-Anker (Bericht Kap. 4) ───────────────────────────────

def _bands(pop: float) -> dict[str, float]:
    share_65p, split = 0.2186, {"a65_74": 0.5003, "a75_84": 0.3555, "a85p": 0.1442}
    out = {b: pop * share_65p * f for b, f in split.items()}
    out["u65"] = pop * (1.0 - share_65p)
    return out


def _ctx(pop: float, summer_temp: float, hd: float, bundesland: str):
    from app.services.engine.impact.base import CellContext
    return CellContext(
        ci={"pop": pop, "summer_temp_cell": summer_temp,
            "pop_age_bands": _bands(pop)},
        hev={"hazards": {"HEAT_WAVE": hd}, "exposures": {}, "vulnerabilities": {}},
        hev_norm={"hazards": {}, "exposures": {}, "vulnerabilities": {}},
        indices={}, regional={"bundesland": bundesland})


def test_morbidity_national_sum_in_sanity_band():
    """Kap. 4 Morbiditäts-Sanity-Band: Baseline ≈ 2.950 Fälle/Jahr ∈ [1.400, 20.000]
    (Untergrenze Destatis T67; Obergrenze K&Z-Größenordnung)."""
    override_context.set_overrides({})
    from app.services.engine import impact
    ctx = _ctx(83_456_045.0, 19.08, hd=7.2, bundesland="Nordrhein-Westfalen")
    total = impact.compute_all_cell_impacts(ctx)[MORB]["outcome"]
    assert 1_400.0 <= total <= 20_000.0, total
    # Punktprobe der Berichtsrechnung: 83,456 Mio × 3,54/100k ≈ 2.950
    assert abs(total - 83_456_045.0 * 3.54 / 100_000.0) < 60.0


def test_morbidity_hd_term_two_sided_capped():
    """§3.4: HD = 0 ⇒ Faktor 1 − 0,024·7,2 = 0,83 (zweiseitig, bei 0 gedeckelt)."""
    override_context.set_overrides({})
    from app.services.engine import impact
    base = impact.compute_all_cell_impacts(
        _ctx(100_000.0, 19.0, hd=7.2, bundesland="Hessen"))[MORB]["outcome"]
    zero = impact.compute_all_cell_impacts(
        _ctx(100_000.0, 19.0, hd=0.0, bundesland="Hessen"))[MORB]["outcome"]
    assert abs(zero / base - (1 - 0.024 * 7.2)) < 1e-9
    # Extrem negative HD-Differenz darf nicht unter 0 fallen (Deckel).
    override_context.set_overrides(
        {f"risks.{MORB}.impact.excess_per_hotday": 0.2})
    capped = impact.compute_all_cell_impacts(
        _ctx(100_000.0, 19.0, hd=0.0, bundesland="Hessen"))[MORB]["outcome"]
    override_context.set_overrides({})
    assert capped == 0.0


def test_mortality_lackmus_no_heat_signal():
    """§3.1-Verteilschlüssel-Lackmustest: Kommune ohne Hitzesignal → ~0 Mortalität."""
    override_context.set_overrides({})
    from app.services.engine import impact
    cold = impact.compute_all_cell_impacts(
        _ctx(100_000.0, 12.0, hd=0.0, bundesland="Schleswig-Holstein"))[MORT]
    warm = impact.compute_all_cell_impacts(
        _ctx(100_000.0, 20.0, hd=20.0, bundesland="Schleswig-Holstein"))[MORT]
    assert cold["outcome"] < 0.01 * warm["outcome"]


def test_measure_hap_marginal_effect():
    """§5-Maßnahme: δ_HAP = 0,95 ⇒ default_reduction 0,05 (marginal, nicht der
    Urban-Einführungseffekt 0,25 — Doppelzählungs-Wächter)."""
    m = next(m for m in catalog.MEASURES if m["code"] == "HEAT_ACTION_PLANS")
    assert m["default_reduction"] == 0.05


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-q"]))


# ── 4. Producer-Test der Ebene CARE_HOME_SHARE_85P (Rev. 8 §3.6; Befund 93) ──

def _mk_cells_and_inputs():
    """Drei Zellen mit Mittelpunkts-Koordinaten (grid_service-Konvention: +50)."""
    from pyproj import Transformer
    tr = Transformer.from_crs(3035, 4326, always_xy=True)
    cells, cis = [], []
    # Zelle 0: Heimstandort, pop85 = 20 · Zelle 1: pop85 = 80 · Zelle 2: pop85 = 0
    for i, p85 in enumerate((20.0, 80.0, 0.0)):
        x0, y0 = 4_300_000 + i * 100, 3_000_000
        cells.append({"x_3035": x0 + 50, "y_3035": y0 + 50})
        cis.append({"pop": 100.0, "pop_age_bands": {"u65": 50.0, "a65_74": 0.0,
                                                    "a75_84": 0.0, "a85p": p85}})
    # Heim-Punkt exakt im Mittelpunkt von Zelle 0 (Minimalreproduktion Befund 93)
    lon, lat = tr.transform(4_300_050.0, 3_000_050.0)
    return cells, cis, lon, lat


def test_care_home_share_producer_expectation_true():
    """Producer (inputs.apply_care_home_share): Zellzuordnung trifft die
    Mittelpunkts-Konvention (Befund 93), Verteilung ist kommunen-erwartungstreu
    auf q̄_pfl und Zellen mit pop_85+ = 0 bleiben außen vor (§3.6)."""
    from shapely.geometry import Point

    from app.services.engine import override_context
    from app.services.engine.inputs import apply_care_home_share

    override_context.set_overrides({})
    cells, cis, lon, lat = _mk_cells_and_inputs()
    infra = {"care_home_geoms": [{"geometry": Point(lon, lat)}]}
    apply_care_home_share(cis, cells, infra)

    # Zelle 0 trägt das gesamte Heim-Gewicht: Bewohner = q̄·(20+80) = 14,9
    # → share = min(1, 14,9/20) = 0,745; Zelle 1 explizit 0 (Kommune HAT Heimdaten);
    # Zelle 2 (pop85 = 0) bekommt keinen Wert.
    assert abs(cis[0]["share_care_home_85p"] - 0.745) < 1e-6, cis[0]
    assert cis[1]["share_care_home_85p"] == 0.0
    assert "share_care_home_85p" not in cis[2]
    # Erwartungstreue (vor Kappung): Σ share·pop85 = q̄ · Σ pop85
    got = sum((ci.get("share_care_home_85p") or 0.0)
              * ci["pop_age_bands"]["a85p"] for ci in cis)
    assert abs(got - 0.149 * 100.0) < 1e-6


def test_care_home_share_cap_binds():
    """Kappung min(1, ·) bindend (Befund 94): kleine 85+-Zelle mit Heim → exakt 1,0."""
    from shapely.geometry import Point

    from app.services.engine import override_context
    from app.services.engine.inputs import apply_care_home_share

    override_context.set_overrides({})
    cells, cis, lon, lat = _mk_cells_and_inputs()
    cis[0]["pop_age_bands"]["a85p"] = 5.0   # Bewohner 0,149·85 = 12,7 > 5 → Kappung
    apply_care_home_share(cis, cells, {"care_home_geoms": [{"geometry": Point(lon, lat)}]})
    assert cis[0]["share_care_home_85p"] == 1.0
    # Kappungs-Verlust ist der dokumentierte Restfehler: Σ share·pop85 < q̄·Σpop85.
    got = sum((ci.get("share_care_home_85p") or 0.0)
              * ci["pop_age_bands"]["a85p"] for ci in cis)
    assert got < 0.149 * 85.0


def test_care_home_share_no_osm_leaves_fallback():
    """Kommune ohne OSM-Heim: Schlüssel bleibt ungesetzt → v_vers rechnet mit q̄."""
    from app.services.engine.inputs import apply_care_home_share

    cells, cis, _, _ = _mk_cells_and_inputs()
    apply_care_home_share(cis, cells, {"care_home_geoms": []})
    assert all("share_care_home_85p" not in ci for ci in cis)
