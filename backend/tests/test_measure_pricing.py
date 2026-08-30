"""Konsistenztests zum symmetrischen CAPEX/OPEX-Kostenmodell (MASSNAHMEN_BEPREISUNG).

Deckt ab:
  * Katalog-Konsistenz — alle 47 Maßnahmen vollständig, unit_label ⇔ Dichte +
    Stück-Kostenfeld, jede Maßnahme hat eine Quelle, sources/source_details/
    source_refs-Keys gültig, keine negativen Werte.
  * compute_costs — CAPEX/OPEX-Formel, None-Felder ohne Komponente, Quellen inkl.
    Override, aufgelöste Bibliografie-Referenzen (IEEE + Live-URL + Archiv-Snapshot).
  * _resolve_count/_unit_effect_factor — Richtwert-Default, Skalierungsfaktor.
  * parameter_registry — 9 Parameter-Specs je Maßnahme, applicable/editable,
    resolve_measure_def wendet alle Override-Felder an.

DB-frei: nutzt ausschließlich die reinen Helferfunktionen (kein Session-Objekt).
Läuft mit pytest oder direkt: ``python tests/test_measure_pricing.py``.
"""

from __future__ import annotations

from app.data import catalog, catalog_parked, sources
from app.services import parameter_registry
from app.services.measure_service import (
    _resolve_count,
    _unit_effect_factor,
    compute_costs,
)

# M0-Verschlankung (docs/ROADMAP.md §5): aktiv sind nur HEAT_ACTION_PLANS und
# VULNERABLE_GROUP_PROGRAMS; die übrigen 45 Maßnahmen liegen VERBATIM in
# catalog_parked und kehren mit den Stufen 1–4 zurück. Die Katalog-Konsistenz-
# und compute_costs-Tests (reine Dict-Helfer, kein Katalog-Lookup) prüfen
# weiterhin aktive + geparkte Definitionen in voller Strenge.
_ALL_MEASURES = list(catalog.MEASURES) + list(catalog_parked._PARKED_MEASURES)
_ALL_BY_CODE = {m["code"]: m for m in _ALL_MEASURES}

_CAPEX_FIELDS = ("capex_fixed", "capex_per_unit", "capex_per_m2")
_OPEX_FIELDS = ("opex_fixed_year", "opex_per_unit_year", "opex_per_m2_year")
_COST_FIELDS = _CAPEX_FIELDS + _OPEX_FIELDS
_ALL_NUMERIC_FIELDS = _COST_FIELDS + ("unit_density_per_ha", "default_reduction", "benefit_per_m2_year")

# Konzept-/Planungsmaßnahmen mit laufenden, mengenunabhängigen Betriebskosten.
_CONCEPT_MEASURES_WITH_OPEX_FIXED = {
    "HEAT_ACTION_PLANS", "EARLY_WARNING_MEASURE", "EVACUATION_EMERGENCY_PLANS",
    "RISK_BASED_INVESTMENTS", "PREVENTION_INCENTIVES", "SUPPLY_CHAIN_RESILIENCE",
    "VULNERABLE_GROUP_PROGRAMS", "HEAT_WORK_SCHEDULES",
    "ADAPTIVE_FISHERIES_MANAGEMENT", "FISHERIES_WATER_QUALITY_PROTECTION",
}


# ── Katalog-Konsistenz ──────────────────────────────────────────────────────

def test_measure_count_is_47():
    # M0-Verschlankung: 2 aktive Maßnahmen; wird 4 mit Aktivierung von #96/#98
    # (docs/ROADMAP.md §5). Die 45 geparkten liegen verbatim in catalog_parked.
    assert len(catalog.MEASURES) == 2
    assert len(_ALL_MEASURES) == 47


def test_every_measure_has_source():
    missing = [m["code"] for m in _ALL_MEASURES if not m.get("source")]
    assert not missing, f"Maßnahmen ohne source-Feld: {missing}"


def test_every_measure_has_all_cost_field_slots():
    """Jede Maßnahme trägt jedes Kostenfeld (gesetzt oder bewusst None)."""
    bad = []
    for m in _ALL_MEASURES:
        for field in _COST_FIELDS:
            if field not in m:
                bad.append((m["code"], field))
    assert not bad, f"Fehlende Kostenfeld-Slots: {bad}"


def test_unit_label_implies_density_and_a_unit_cost_field():
    bad = []
    for m in _ALL_MEASURES:
        if m.get("unit_label") is not None:
            if m.get("unit_density_per_ha") is None:
                bad.append((m["code"], "unit_density_per_ha fehlt trotz unit_label"))
            if m.get("capex_per_unit") is None and m.get("opex_per_unit_year") is None:
                bad.append((m["code"], "weder capex_per_unit noch opex_per_unit_year gesetzt"))
        else:
            if m.get("unit_density_per_ha") is not None:
                bad.append((m["code"], "unit_density_per_ha gesetzt ohne unit_label"))
            if m.get("capex_per_unit") is not None or m.get("opex_per_unit_year") is not None:
                bad.append((m["code"], "Stück-Kostenfeld gesetzt ohne unit_label"))
    assert not bad, f"unit_label/Stück-Felder inkonsistent: {bad}"


def test_source_maps_keys_are_valid_field_names():
    """sources/source_details/source_refs dürfen nur auf existierende Feldnamen zeigen."""
    bad = []
    for m in _ALL_MEASURES:
        for mapname in ("sources", "source_details", "source_refs"):
            for key in (m.get(mapname) or {}).keys():
                if key not in _ALL_NUMERIC_FIELDS:
                    bad.append((m["code"], mapname, key))
    assert not bad, f"Ungültige Quellen-Map-Keys: {bad}"


def test_no_negative_numeric_values():
    bad = []
    for m in _ALL_MEASURES:
        for field in _ALL_NUMERIC_FIELDS:
            val = m.get(field)
            if val is not None and val < 0:
                bad.append((m["code"], field, val))
    assert not bad, f"Negative Kostenwerte: {bad}"


def test_concept_measures_have_fixed_opex():
    """Konzept-/Planungsmaßnahmen haben laufende (mengenunabhängige) OPEX > 0."""
    bad = []
    for code in _CONCEPT_MEASURES_WITH_OPEX_FIXED:
        m = _ALL_BY_CODE[code]
        val = m.get("opex_fixed_year")
        if val is None or val <= 0:
            bad.append((code, val))
    assert not bad, f"Konzeptmaßnahmen ohne feste OPEX: {bad}"


# ── Quellen-Bibliografie (IEEE + Live-URL + Archiv-Snapshot) ────────────────

def test_source_refs_resolve_to_bibliography():
    """Jeder in source_refs referenzierte Key existiert in der Bibliografie."""
    bad = []
    for m in _ALL_MEASURES:
        for field, keys in (m.get("source_refs") or {}).items():
            for k in keys:
                if k not in sources.SOURCE_REFERENCES:
                    bad.append((m["code"], field, k))
    assert not bad, f"Unbekannte source_refs-Keys: {bad}"


def test_bibliography_entries_are_complete():
    """Jeder Bibliografie-Eintrag trägt IEEE-Zitation, Live-URL und Archiv-Snapshot."""
    bad = []
    for key, entry in sources.SOURCE_REFERENCES.items():
        for field in ("ieee", "url", "archive_url"):
            if not entry.get(field):
                bad.append((key, field))
        if entry.get("archive_url") and "web.archive.org" not in entry["archive_url"]:
            bad.append((key, "archive_url ist kein Wayback-Permalink"))
    assert not bad, f"Unvollständige Bibliografie-Einträge: {bad}"


def test_green_roofs_capex_has_resolved_references():
    """Das vom Nutzer genannte Gründach-Beispiel liefert klickbare, archivierte Quellen."""
    mdef = _ALL_BY_CODE["GREEN_ROOFS_FACADES"]   # M0: geparkt, compute_costs ist katalogfrei
    result = compute_costs(mdef, count=0, area_m2=1000.0)
    comp = next(c for c in result["capex"]["components"] if c["param"] == "capex_per_m2")
    assert len(comp["references"]) >= 2
    for ref in comp["references"]:
        assert ref["ieee"] and ref["url"] and ref["archive_url"]


# ── compute_costs ───────────────────────────────────────────────────────────

def test_compute_costs_drinking_fountains_five_units():
    mdef = _ALL_BY_CODE["DRINKING_FOUNTAINS"]   # M0: geparkt
    result = compute_costs(mdef, count=5, area_m2=0.0)
    assert result["capex"]["total_eur"] == 5000.0 + 5 * 14000.0 == 75000.0
    assert result["opex"]["total_eur"] == 5 * 3500.0 == 17500.0


def test_compute_costs_area_only_measure_matches_legacy_formula():
    mdef = _ALL_BY_CODE["DECENTRALIZED_ENERGY_PV_STORAGE"]   # M0: geparkt
    assert mdef["unit_label"] is None
    assert mdef["capex_fixed"] == 0.0            # 0.0 = anwendbar, aber ohne Grundkosten
    assert mdef["opex_fixed_year"] is None       # Flächenmaßnahme: keine festen OPEX
    area = 1234.5
    result = compute_costs(mdef, count=0, area_m2=area)
    expected_capex = mdef["capex_per_m2"] * area
    expected_opex = mdef["opex_per_m2_year"] * area
    assert result["capex"]["total_eur"] == round(expected_capex, 2)
    assert result["opex"]["total_eur"] == round(expected_opex, 2)


def test_compute_costs_none_fields_produce_no_component():
    mdef = _ALL_BY_CODE["DRINKING_FOUNTAINS"]   # M0: geparkt
    assert mdef["capex_per_m2"] is None
    assert mdef["opex_per_m2_year"] is None
    assert mdef["opex_fixed_year"] is None
    result = compute_costs(mdef, count=5, area_m2=100.0)
    capex_params = {c["param"] for c in result["capex"]["components"]}
    opex_params = {c["param"] for c in result["opex"]["components"]}
    assert "capex_per_m2" not in capex_params
    assert capex_params == {"capex_fixed", "capex_per_unit"}
    assert opex_params == {"opex_per_unit_year"}


def test_compute_costs_overridden_flag_on_custom_source():
    mdef = dict(_ALL_BY_CODE["DRINKING_FOUNTAINS"])   # M0: geparkt
    mdef["custom_sources"] = {"capex_per_unit": "Kommune-Angebot 2026"}
    result = compute_costs(mdef, count=5, area_m2=0.0)
    by_param = {c["param"]: c for c in result["capex"]["components"]}
    assert by_param["capex_per_unit"]["overridden"] is True
    assert by_param["capex_per_unit"]["source"] == "Kommune-Angebot 2026"
    assert by_param["capex_fixed"]["overridden"] is False
    assert by_param["capex_fixed"]["source"] == mdef["sources"]["capex_fixed"]


# ── _resolve_count / _unit_effect_factor ────────────────────────────────────

def test_resolve_count_uses_recommended_as_default():
    mdef = _ALL_BY_CODE["DRINKING_FOUNTAINS"]   # M0: geparkt
    covered_area_m2 = 100_000.0  # 10 ha, density 0.5/ha -> recommended 5
    count, is_default, recommended = _resolve_count(mdef, None, covered_area_m2)
    assert recommended == 5
    assert count == 5
    assert is_default is True


def test_resolve_count_explicit_config_overrides_default():
    mdef = _ALL_BY_CODE["DRINKING_FOUNTAINS"]   # M0: geparkt
    covered_area_m2 = 100_000.0
    count, is_default, recommended = _resolve_count(mdef, {"count": 3}, covered_area_m2)
    assert count == 3
    assert is_default is False
    assert recommended == 5


def test_unit_effect_factor_scales_with_count_vs_recommended():
    assert _unit_effect_factor(3, 5) == 3 / 5
    assert _unit_effect_factor(5, 5) == 1.0
    assert _unit_effect_factor(10, 5) == 1.0  # capped at 1


def test_area_measure_has_no_count_and_full_unit_factor():
    mdef = _ALL_BY_CODE["DECENTRALIZED_ENERGY_PV_STORAGE"]   # M0: geparkt
    assert mdef["unit_label"] is None
    count, is_default, recommended = _resolve_count(mdef, {"count": 99}, 5000.0)
    assert (count, is_default, recommended) == (0, False, 0)
    assert _unit_effect_factor(count, recommended) == 1.0


# ── parameter_registry ───────────────────────────────────────────────────────

def test_measure_param_specs_has_nine_entries():
    assert len(parameter_registry.MEASURE_PARAM_SPECS) == 9
    assert len(parameter_registry.MEASURE_OVERRIDE_FIELDS) == 9


def test_registry_applicable_and_editable_match_none_fields():
    for m in catalog.MEASURES:
        params = parameter_registry.catalog_parameters(layer_code=m["code"], layer_category="measures")
        assert len(params) == 9, f"{m['code']}: erwartet 9 Parameter, bekommen {len(params)}"
        for p in params:
            field = p["id"].rsplit(".", 1)[-1]
            expected_applicable = m.get(field) is not None
            assert p["applicable"] == expected_applicable, f"{m['code']}.{field}: applicable falsch"
            assert p["editable"] == expected_applicable, f"{m['code']}.{field}: editable != applicable"
            if not expected_applicable:
                assert p["value"] == 0.0


def test_registry_emits_references_for_cited_field():
    # M0: die Registry emittiert nur AKTIVE Maßnahmen — geprüft am aktiven
    # HEAT_ACTION_PLANS (source_refs auf default_reduction) statt am geparkten
    # Gründach-Beispiel.
    params = parameter_registry.catalog_parameters(
        layer_code="HEAT_ACTION_PLANS", layer_category="measures")
    p = next(p for p in params if p["id"].endswith(".default_reduction"))
    assert [r["key"] for r in p["references"]] == ["Urban_HHAP_Wirksamkeit_2025"]


def test_resolve_measure_def_applies_all_nine_override_fields():
    code = "DRINKING_FOUNTAINS"
    mdef = _ALL_BY_CODE[code]   # M0: geparkt, resolve_measure_def ist katalogfrei
    overrides = {
        f"measures.{code}.{field}": idx + 1.0
        for idx, field in enumerate(parameter_registry.MEASURE_OVERRIDE_FIELDS)
    }
    resolved = parameter_registry.resolve_measure_def(mdef, overrides)
    for idx, field in enumerate(parameter_registry.MEASURE_OVERRIDE_FIELDS):
        assert resolved[field] == idx + 1.0, f"Override für {field} nicht angewendet"


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
