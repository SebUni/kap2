"""S157 (COOLING_ROOMS_DRINKING_WATER): Quellen und Parameterliste nach Vorgabe P1/P2 (T-1410).

DB-frei. Prüft:
  1. Jeder Quellschlüssel jedes als ``belegt`` gekennzeichneten S157-Parameters ist in
     ``SOURCE_REFERENCES`` aufgelöst (Quelle [46] Katz u. a. 2026), ebenso ``heat.gamma_hoehe``.
  2. Keine Herleitung von default_reduction enthält das Wort „Kostenart“; für
     ``default_reduction`` steht die Erklärung, dass S157 über g_S157 wirkt.
  3. Ein Parameter, den der Nutzer ändern kann, wirkt: Eine Überschreibung von ``ror_s157``
     ändert den S157-Betrag — oder ``ror_s157`` ist als nicht editierbar markiert.
"""

from __future__ import annotations

from app.data import catalog, sources
from app.services import measure_service, parameter_registry
from app.services.engine import override_context, risk_engine

CODE = "COOLING_ROOMS_DRINKING_WATER"
MORT = "EXPECTED_ANNUAL_MORTALITY"


def _s157_params() -> list[dict]:
    """Parameterliste der Maßnahme S157 samt der S157-Parameter der Mortalität."""
    params = list(parameter_registry.catalog_parameters(
        layer_code=CODE, layer_category="measures"))
    params += [p for p in parameter_registry.catalog_parameters(
        layer_code=MORT, layer_category="risks")
        if p["id"].endswith((".ror_s157", ".g_s157"))]
    return params


def _by_suffix(params: list[dict], suffix: str) -> dict:
    return next(p for p in params if p["id"].endswith(suffix))


def _catalog_refs_of(params: list[dict]) -> dict[str, list[str]]:
    return {p["id"]: [r["key"] for r in p["references"]] for p in params}


def test_belegte_s157_parameter_loesen_quelle_auf():
    """Jeder Quellschlüssel eines belegten S157-Parameters steht in SOURCE_REFERENCES."""
    from app.services.engine.impact.params import IMPACT_PARAM_SPECS

    specs = {s["key"]: s for s in IMPACT_PARAM_SPECS if s["risk"] == MORT}
    mdef = catalog.MEASURES_BY_CODE[CODE]
    belegt: list[tuple[str, list[str]]] = []
    for p in _s157_params():
        if p["evidence_class"] != "belegt":
            continue
        if p["layer_category"] == "risks":
            keys = specs[p["id"].rsplit(".", 1)[1]].get("source_refs") or []
        else:
            field = p["id"].rsplit(".", 1)[1]
            keys = (mdef.get("source_refs") or {}).get(field) or []
        belegt.append((p["id"], list(keys)))
    assert any(pid.endswith(".ror_s157") for pid, _ in belegt)
    for pid, keys in belegt:
        assert keys, f"{pid}: als belegt gekennzeichnet, aber ohne Quellschlüssel"
        for k in keys:
            assert k in sources.SOURCE_REFERENCES, f"{pid}: Quelle {k} nicht im Register"
            assert sources.SOURCE_REFERENCES[k]["ieee"] and sources.SOURCE_REFERENCES[k]["url"]
    # ...und die aufgelösten Referenzen der Registry tragen sie tatsächlich
    refs = _catalog_refs_of(_s157_params())
    ror = _by_suffix(_s157_params(), ".ror_s157")
    assert refs[ror["id"]], "ror_s157: keine aufgelöste Referenz in der Parameterliste"
    assert "Katz" in sources.SOURCE_REFERENCES[refs[ror["id"]][0]]["ieee"]


def test_gamma_hoehe_loest_icao_quelle_auf():
    p = _by_suffix(parameter_registry.catalog_parameters(
        layer_code=MORT, layer_category="risks"), ".gamma_hoehe")
    assert p["references"], "gamma_hoehe: keine aufgelöste Referenz"
    for r in p["references"]:
        assert r["ieee"] and r["url"]
    assert any("ICAO" in r["ieee"] for r in p["references"])


def test_keine_herleitung_der_s157_liste_nennt_kostenart():
    """default_reduction ist keine Kostenart. Die nicht angesetzten echten Kostenfelder
    (capex_per_m2, opex_fixed_year, opex_per_m2_year) behalten ihre Standard-Herleitung."""
    for p in _s157_params():
        if not p["id"].endswith(".default_reduction"):
            continue
        for teil, text in (p.get("evidence_derivation") or {}).items():
            assert "Kostenart" not in text, f"{p['id']} ({teil}): {text}"
    dr = _by_suffix(_s157_params(), ".default_reduction")
    assert dr["evidence_derivation"]["wert"] == (
        "Die Maßnahme wirkt nicht über eine pauschale Minderung, sondern über g_S157 auf die "
        "Todesfälle ab 85 Jahren in Heimen, abhängig vom gekühlten Anteil s_gek.")


def test_andere_massnahmen_behalten_kostenart_herleitung():
    others = [m["code"] for m in catalog.MEASURES
              if m["code"] != CODE and any(m.get(f) is None for f in ("capex_per_m2",))]
    assert others
    p = _by_suffix(parameter_registry.catalog_parameters(
        layer_code=others[0], layer_category="measures"), ".capex_per_m2")
    assert p["evidence_derivation"]["wert"].startswith("Die Maßnahme setzt diese Kostenart nicht an")


def _s157_benefit_eur() -> float:
    risk = catalog.RISKS_BY_CODE[MORT]
    mdef = catalog.MEASURES_BY_CODE[CODE]
    cell = {"outcome": 153.6 * 4.16 + 1000.0, "deaths_a85p": 153.6}
    factor = measure_service._measure_cell_factor(
        mdef, {"s_gek": 1.0}, MORT, 1.0, 1.0, cell, 1.0)
    return risk_engine.cost_from_outcome(risk, cell["outcome"]) * (1.0 - factor)


def test_ror_s157_wirkt_oder_ist_nicht_editierbar():
    ror = _by_suffix(_s157_params(), ".ror_s157")
    override_context.set_overrides({})
    basis = _s157_benefit_eur()
    assert basis > 0.0
    try:
        override_context.set_overrides({f"risks.{MORT}.impact.ror_s157": 0.5})
        geaendert = _s157_benefit_eur()
    finally:
        override_context.set_overrides({})
    assert geaendert != basis or ror["editable"] is False, (
        "ror_s157 ist editierbar, ändert aber den S157-Betrag nicht")
