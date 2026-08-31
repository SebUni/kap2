"""Golden-Tests der Methodik #98 (UV-Schädigungen, Bericht Rev. 1).

Prüfklassen wie bei #95/#96 (Integrations-Kontrakt, AUFGABE §7 /
integriere-risiko §4):

1. **Beispiel-Blöcke** des Berichts laufen als Test — Bericht und Repo können
   nicht divergieren, ohne dass CI rot wird.
2. **Registry ⇄ Bericht**: die maschinenlesbaren Kap.-7-Werte müssen exakt den
   Registry-Specs/Katalogwerten entsprechen (kein stiller Code-Fix).
3. **Sanity-/Struktur-Anker aus Kap. 4**: Bundessumme YLL/€ im Band, Ablese-
   Validierung ±15 %, Verteilschlüssel-Lackmustest (Zelle ohne SSD-Anstieg → 0).
4. **Zellrechnung + Ebene**: Handrechnung der Schadensfunktion, Fallback-Kette
   der Ebene UV_RADIATION, Trennung Schicht A ⇄ Schicht B.
"""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data import catalog  # noqa: E402
from app.services.engine import impact, override_context  # noqa: E402
from app.services.engine.impact import health as H  # noqa: E402
from app.services.engine.impact.base import CellContext  # noqa: E402

REPORT = os.path.join(os.path.dirname(__file__), "..", "..",
                      "docs", "methodik", "98_uv_schaedigungen.md")
CODE = "EXPECTED_ANNUAL_UV_YLL"

# Bundes-Altersmix (Bevölkerung 31.12.2023, Bandsummen wie #96 §3.2).
_BAND_POP = {"u20": 15_583_456, "a20_64": 49_163_992, "a65_74": 9_569_640,
             "a75_84": 6_294_744, "a85p": 2_844_213}
_POP_DE = sum(_BAND_POP.values())

# Amtliche Fallzahlen 2023 (ZfKD KID 2025, Bericht §3.3).
_FAELLE_MM_DE = 27_430
_FAELLE_C44_DE = 242_820


def _spec(key: str) -> dict:
    from app.services.engine.impact.params import IMPACT_PARAM_SPECS
    for s in IMPACT_PARAM_SPECS:
        if s["risk"] == CODE and s["key"] == key:
            return s
    raise AssertionError(f"Registry-Spec fehlt: {CODE}.{key}")


def _ctx(pop: float, ssd_ref: float = 1000.0, ssd_neu: float = 1078.2,
         bundesland: str = "Nordrhein-Westfalen", **ci_extra) -> CellContext:
    """Zelle im Bundes-Altersmix; ΔSSD-Default = DE-Gebietsmittel +7,82 %."""
    bands = {b: pop * n / _POP_DE for b, n in _BAND_POP.items()}
    bands["u65"] = bands["u20"] + bands["a20_64"]
    ci = {"pop": pop, "pop_age_bands": bands,
          "ssd_ref": ssd_ref, "ssd_neu": ssd_neu, **ci_extra}
    return CellContext(
        ci=ci,
        hev={"hazards": {"UV_RADIATION": ssd_neu}, "exposures": {},
             "vulnerabilities": {}},
        hev_norm={"hazards": {}, "exposures": {}, "vulnerabilities": {}},
        indices={}, regional={"bundesland": bundesland})


# ── 1. Beispiel-Blöcke des Berichts ───────────────────────────────────────────

def test_report_example_blocks_green():
    with open(os.path.abspath(REPORT), encoding="utf-8") as fh:
        blocks = re.findall(r"```python test: (\S+)\n(.*?)```", fh.read(), re.S)
    assert len(blocks) >= 5, "Bericht #98 muss mindestens 5 Beispiel-Blöcke tragen"
    for name, code in blocks:
        try:
            exec(compile(code, f"98:{name}", "exec"), {})  # noqa: S102
        except Exception as e:  # pragma: no cover
            raise AssertionError(f"Beispiel-Block {name} rot: {e}") from e


# ── 2. Registry/Katalog ⇄ Bericht (Kap. 7) ───────────────────────────────────

def test_registry_matches_report_parameters():
    """Kap.-7-Werte des Berichts == Registry-Specs (Divergenz = Ledger-Fall)."""
    for key, val in (("k_uv", 0.84), ("a_attr", 0.75),
                     ("baf_mm", 0.60), ("baf_c44", 1.675), ("w_scc", 0.25),
                     ("c_kal_mm", 1.022), ("c_kal_c44", 0.999),
                     ("lambda_mm", 0.1155), ("lambda_c44", 0.00549),
                     ("l_rest_mm", 10.58), ("l_rest_c44", 5.30),
                     ("c_fall_mm", 6724.0), ("c_fall_c44", 5883.0),
                     ("or_out", 1.77), ("qbar_out", 0.070),
                     ("r_out_enabled", 0.0), ("v_verh", 1.0)):
        assert _spec(key)["value"] == val, key
    # Ablese-Kette (§3.3): Roh-Bandraten je Entität.
    for band, val in (("u20", 0.5), ("a20_64", 24.7), ("a65_74", 64.0),
                      ("a75_84", 94.9), ("a85p", 88.5)):
        assert _spec(f"i_mm_{band}")["value"] == val, band
    for band, val in (("u20", 2.0), ("a20_64", 125.9), ("a65_74", 617.6),
                      ("a75_84", 1267.2), ("a85p", 1479.5)):
        assert _spec(f"i_c44_{band}")["value"] == val, band
    # Produktionskonstanten spiegeln die Specs (Call-Site-Defaults, §3.9).
    assert H.UV_INCIDENCE_MM == {b: _spec(f"i_mm_{b}")["value"]
                                 for b in H.UV_INCIDENCE_MM}
    assert H.UV_INCIDENCE_C44 == {b: _spec(f"i_c44_{b}")["value"]
                                  for b in H.UV_INCIDENCE_C44}


def test_baf_c44_derives_from_scc_split():
    """BAF_C44 = (1−w_SCC)·1,4 + w_SCC·2,5 (§3.1) — Kopplung testgebunden.

    w_SCC ist editierbar (Quellen-Widerspruch, Band 0,25–0,50); wer ihn ändert,
    ohne BAF_C44 nachzuziehen, bricht die Herleitung des Berichts.
    """
    w = _spec("w_scc")["value"]
    assert abs(_spec("baf_c44")["value"] - ((1 - w) * 1.4 + w * 2.5)) < 1e-9
    # Obere Bandstütze (BfS-2015-Split) ist die im Bericht genannte 1,95.
    assert abs(0.50 * 1.4 + 0.50 * 2.5 - 1.95) < 1e-9


def test_cost_rate_is_voly_and_native_unit_is_yll():
    """Native Ergebnisgröße YLL; Katalog-Kostensatz = VOLY (§3.4/§3.6)."""
    risk = catalog.RISKS_BY_CODE[CODE]
    assert risk["outcome_unit"] == "YLL/Jahr"
    assert risk["scale"] == "pop"
    assert abs(catalog.risk_default_cost_per_outcome(risk) - 160_800.0) < 1e-9
    # Gleiche VOLY-Kette wie #95 — der Preisstand darf nicht auseinanderlaufen.
    heat = catalog.RISKS_BY_CODE["EXPECTED_ANNUAL_MORTALITY"]
    assert (catalog.risk_default_cost_per_outcome(risk)
            == catalog.risk_default_cost_per_outcome(heat))


def test_cost_is_treatment_plus_voly_not_outcome_times_rate():
    """§3.4: € = Σ ΔF_e·c_e + YLL·VOLY — Behandlungskosten sind KEIN VOLY-Anteil.

    Der Katalog-Kostensatz allein (outcome × VOLY) unterschätzt den Ausweis um
    genau die Behandlungskosten. Der Test bindet beide Bestandteile: ein stiller
    Rückfall auf „outcome × Kostensatz" wird rot.
    """
    override_context.set_overrides({})
    res = impact.compute_all_cell_impacts(_ctx(float(_POP_DE)))[CODE]
    behandlung = (res["cases_melanoma"] * _spec("c_fall_mm")["value"]
                  + res["cases_c44"] * _spec("c_fall_c44")["value"])
    mortalitaet = res["outcome"] * 160_800.0
    assert abs(res["cost_eur"] - (behandlung + mortalitaet)) < 1.0
    assert behandlung > 0.2 * res["cost_eur"]      # ≈ 124 von 378 Mio (Kap. 4)


# ── 3. Sanity-/Struktur-Anker (Bericht Kap. 4) ───────────────────────────────

def test_national_sum_matches_report_sanity_band():
    """Kap. 4: ΔF ≈ 814 MM + 20.118 C44, YLL ≈ 1.580, € ≈ 378 Mio (Band 119–653)."""
    override_context.set_overrides({})
    res = impact.compute_all_cell_impacts(_ctx(float(_POP_DE)))[CODE]
    assert abs(res["cases_melanoma"] - 814) < 10, res["cases_melanoma"]
    assert abs(res["cases_c44"] - 20_118) < 200, res["cases_c44"]
    assert abs(res["outcome"] - 1580) < 20, res["outcome"]
    assert abs(res["cost_eur"] / 1e6 - 378) < 6, res["cost_eur"]
    # Sanity-Band der Kap.-4-Bandkombination.
    assert 119e6 <= res["cost_eur"] <= 653e6


def test_lower_band_combination_stays_positive():
    """Untergrenze k_UV 0,4 × a_attr 0,5 ⇒ ≈ 119 Mio € (Kap. 4) — messfest > 0."""
    override_context.set_overrides({f"risks.{CODE}.impact.k_uv": 0.4,
                                    f"risks.{CODE}.impact.a_attr": 0.5})
    res = impact.compute_all_cell_impacts(_ctx(float(_POP_DE)))[CODE]
    override_context.set_overrides({})
    assert abs(res["cost_eur"] / 1e6 - 119) < 6, res["cost_eur"]
    assert res["cost_eur"] > 0


def test_baseline_reproduces_official_case_numbers():
    """Ablese-Validierung (Kap. 4): Roh-Bandraten ±15 %, danach c_kal exakt.

    Prüft die PRODUKTIONS-Baseline (nicht eine lokale Nachrechnung): F_e der
    Bundes-Zelle muss die amtlichen ZfKD-Fallzahlen 2023 treffen. Da ΔF = F·BAF·ΔD
    linear ist, lässt sich F aus dem Teil-Ausweis zurückrechnen.
    """
    override_context.set_overrides({})
    ctx = _ctx(float(_POP_DE))
    dd = H.uv_delta_dosis(ctx, CODE)
    res = impact.compute_all_cell_impacts(ctx)[CODE]
    f_mm = res["cases_melanoma"] / (_spec("baf_mm")["value"] * dd)
    f_c44 = res["cases_c44"] / (_spec("baf_c44")["value"] * dd)
    assert abs(f_mm - _FAELLE_MM_DE) / _FAELLE_MM_DE < 0.005, f_mm
    assert abs(f_c44 - _FAELLE_C44_DE) / _FAELLE_C44_DE < 0.005, f_c44
    # Rohraten vor Normierung liegen innerhalb der vorab fixierten ±15 %.
    roh_mm = f_mm / _spec("c_kal_mm")["value"]
    roh_c44 = f_c44 / _spec("c_kal_c44")["value"]
    assert abs(roh_mm / _FAELLE_MM_DE - 1) < 0.15
    assert abs(roh_c44 / _FAELLE_C44_DE - 1) < 0.15


def test_distribution_key_is_bottom_up():
    """§3.1-Lackmustest: keine Bevölkerung → 0; kein SSD-Anstieg → 0."""
    override_context.set_overrides({})
    leer = impact.compute_all_cell_impacts(_ctx(0.0))[CODE]
    assert leer["outcome"] == 0.0 and leer["cost_eur"] == 0.0
    # Zelle mit Bevölkerung, aber ohne gemessenen SSD-Anstieg: der Ausweis
    # enthält NUR den Zusatz, keinen Baseline-Sockel.
    flach = impact.compute_all_cell_impacts(
        _ctx(10_000.0, ssd_ref=1600.0, ssd_neu=1600.0))[CODE]
    assert flach["outcome"] == 0.0 and flach["cost_eur"] == 0.0
    assert flach["cases_melanoma"] == 0.0 and flach["cases_c44"] == 0.0


def test_example_cell_matches_report():
    """§3.4-Beispielzelle: 1.000 EW im Bundesmix, Region Mitte (ΔSSD +8,42 %)."""
    override_context.set_overrides({})
    res = impact.compute_all_cell_impacts(
        _ctx(1000.0, ssd_ref=1000.0, ssd_neu=1084.2))[CODE]
    assert abs(res["cases_melanoma"] - 0.0105) < 0.0002, res["cases_melanoma"]
    assert abs(res["cases_c44"] - 0.2598) < 0.003, res["cases_c44"]
    assert abs(res["cost_eur"] - 4880) < 60, res["cost_eur"]


# ── 4. Ebene UV_RADIATION: Anlagepflicht, Fallback-Kette, Schichtentrennung ──

def test_uv_layer_exists_with_fallback_chain():
    """§3.1-Anlagepflicht: die Ebene existiert und liefert nie einen stillen 0."""
    from app.services.engine.indicators import uv_radiation

    meta = catalog.INDICATOR_BY_CODE["UV_RADIATION"]
    assert meta["unit"] == "h/Jahr" and meta["spatial"] is True
    # 1. Zellwert aus dem Normalperioden-Raster.
    assert uv_radiation({"ssd_neu": 1723.4}, {}) == 1723.4
    # 2./3. Ohne Zellwert: Bundesland- bzw. Deutschland-Gebietsmittel — ein
    # Null-Wert hieße „keine Sonne", nicht „keine Daten".
    assert uv_radiation({}, {"bundesland": "Bayern"}) > 1300.0
    assert uv_radiation({}, {}) > 1300.0


def test_delta_dosis_uses_change_not_level():
    """§3.2: die Schadensfunktion hängt an der ÄNDERUNG, nicht am SSD-Pegel."""
    override_context.set_overrides({})
    a = _ctx(10_000.0, ssd_ref=1400.0, ssd_neu=1400.0 * 1.0782)
    b = _ctx(10_000.0, ssd_ref=1800.0, ssd_neu=1800.0 * 1.0782)
    assert abs(H.uv_delta_dosis(a, CODE) - H.uv_delta_dosis(b, CODE)) < 1e-12
    ra = impact.compute_all_cell_impacts(a)[CODE]
    rb = impact.compute_all_cell_impacts(b)[CODE]
    assert abs(ra["outcome"] - rb["outcome"]) < 1e-12
    # ΔDosis DE = 7,82 % × k_UV × a_attr. Produktion rechnet mit dem
    # maschinenlesbaren Kap.-7-Wert k_UV = 0,84 ⇒ 4,927 %; die §3.2-Prosa nennt
    # 4,95 %, weil sie die UNGERUNDETE Kette 4,9/5,81 = 0,8434 einsetzt
    # (Ledger #98 Befund 213 — berichtsinterne Rundungsdivergenz, 0,5 %
    # relativ, kein Code-Fix). Beide Stände sind hier festgenagelt, damit die
    # Differenz sichtbar bleibt und nicht stillschweigend wächst.
    assert abs(H.uv_delta_dosis(a, CODE) - 0.049266) < 1e-6
    assert abs(0.0782 * (4.9 / 5.81) * 0.75 - 0.0495) < 0.0001
    assert abs(H.uv_delta_dosis(a, CODE) / 0.0495 - 1) < 0.005


def test_screening_norm_override_does_not_move_euro_path():
    """§3.3: ein editierter Screening-Normbereich darf den €-Pfad nicht bewegen."""
    override_context.set_overrides({})
    base = impact.compute_all_cell_impacts(_ctx(10_000.0))[CODE]["cost_eur"]
    override_context.set_overrides({"indicators.UV_RADIATION.norm_max": 3000.0,
                                    "indicators.UV_RADIATION.norm_min": 0.0})
    after = impact.compute_all_cell_impacts(_ctx(10_000.0))[CODE]["cost_eur"]
    override_context.set_overrides({})
    assert abs(base - after) < 1e-9


def test_r_out_modifier_is_parked_and_neutral():
    """§3.6: Außenbeschäftigten-Ebene ist GEPARKT ⇒ r_out exakt neutral.

    Der Schalter ``r_out_enabled`` steht im Basiswert auf 0 (keine keyless
    Zellquelle, Beschaffungs-Watchlist). Selbst eine Zelle, die den Anteil
    mitbrächte, darf den Basiswert nicht verschieben.
    """
    override_context.set_overrides({})
    ohne = impact.compute_all_cell_impacts(_ctx(10_000.0))[CODE]["outcome"]
    mit = impact.compute_all_cell_impacts(
        _ctx(10_000.0, share_outdoor_workers=0.14))[CODE]["outcome"]
    assert ohne == mit
    # Eingeschaltet reproduziert er die Bericht-Rechnung (+1,9 % auf den
    # C44-Zusatz bei q_out = 0,14).
    override_context.set_overrides({f"risks.{CODE}.impact.r_out_enabled": 1.0})
    an = impact.compute_all_cell_impacts(
        _ctx(10_000.0, share_outdoor_workers=0.14))[CODE]
    aus = impact.compute_all_cell_impacts(_ctx(10_000.0))[CODE]
    override_context.set_overrides({})
    assert abs(an["cases_c44"] / aus["cases_c44"] - 1.019) < 0.001
    # Zentrierung: q_out = q̄_out ⇒ exakt 1.
    zentriert = impact.compute_all_cell_impacts(
        _ctx(10_000.0, share_outdoor_workers=0.070))[CODE]
    assert abs(zentriert["cases_c44"] - aus["cases_c44"]) < 1e-9


if __name__ == "__main__":
    import pytest

    sys.exit(pytest.main([__file__, "-q"]))
