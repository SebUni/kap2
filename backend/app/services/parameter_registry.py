"""Zentrale Parameter-Registry für Info-Fenster, Konfiguration und Engine-Overrides."""

from __future__ import annotations

from typing import Any

from app.data import catalog, sources
from app.services.engine import formulas, tunables
from app.services.engine.impact.params import IMPACT_PARAM_SPECS, IMPACT_GLOBAL_SPECS

# Impact-Parameter (Schicht B) je Risiko gruppiert für die Emission in der Risiko-Schleife.
_IMPACT_SPECS_BY_RISK: dict[str, list[dict]] = {}
for _spec in IMPACT_PARAM_SPECS:
    _IMPACT_SPECS_BY_RISK.setdefault(_spec["risk"], []).append(_spec)

# Hinweis: Die Pfadgewichte (catalog.PATHWAY_WEIGHTS) werden bewusst NICHT mehr als
# Parameter emittiert — die Engine liest sie beim Import fest ein (risk_engine._PATHWAYS),
# ein Override wäre wirkungslos (toter Parameter). Sie bleiben Modellkonstanten des Katalogs.

# Symmetrisches CAPEX/OPEX-Kostenmodell (je fix/Stück/Fläche) + Wirkungs-/Dichte-Parameter.
MEASURE_PARAM_SPECS: tuple[tuple[str, str, str], ...] = (
    ("default_reduction", "Standard-Risikoreduktion", "Anteil"),
    ("capex_fixed", "CAPEX – Grundkosten (einmalig)", "€"),
    ("capex_per_unit", "CAPEX – Investition pro Einheit", "€/Stück"),
    ("capex_per_m2", "CAPEX – Investition pro m²", "€/m²"),
    ("opex_fixed_year", "OPEX – Feste Betriebskosten pro Jahr", "€/a"),
    ("opex_per_unit_year", "OPEX – Betrieb & Unterhalt pro Einheit und Jahr", "€/(Stück·a)"),
    ("opex_per_m2_year", "OPEX – Betrieb & Unterhalt pro m² und Jahr", "€/(m²·a)"),
    ("benefit_per_m2_year", "Direkter Nutzen pro m² und Jahr", "€/(m²·a)"),
    ("unit_density_per_ha", "Richtwert-Dichte", "Stück/ha"),
)

MEASURE_OVERRIDE_FIELDS = tuple(field for field, _, _ in MEASURE_PARAM_SPECS)

# ``source`` in formulas._i steuert die Wertauflösung (const/cell/regional/…); diese Marker
# sind keine belegbaren Quellen. Für die Anzeige greift dann ``doc_source`` oder ein
# ehrlicher Modellannahme-Hinweis.
_RESOLUTION_SOURCE_MARKERS = frozenset(
    {"const", "cell", "regional", "demo", "computed", "hev", "auxiliary", ""}
)


def _param_doc_source(inp: dict) -> str:
    """Anzeigbare Herkunft eines Formel-Parameters für die Registry."""
    doc = inp.get("doc_source")
    if doc:
        return doc
    src = inp.get("source")
    if src and src not in _RESOLUTION_SOURCE_MARKERS:
        return src
    return "Modellannahme (mangels lokaler Daten)"


def _base_param(
    pid: str,
    *,
    layer_code: str,
    layer_category: str,
    label: str,
    value: Any,
    unit: str = "",
    source: str = "",
    source_detail: str = "",
    references: list[dict] | None = None,
    prov: str = "param",
    editable: bool = True,
    applicable: bool = True,
) -> dict:
    return {
        "id": pid,
        "layer_code": layer_code,
        "layer_category": layer_category,
        "label": label,
        "value": value,
        "default_value": value,
        "unit": unit,
        "source": source,
        "source_detail": source_detail,
        "references": references or [],
        "prov": prov,
        "editable": editable,
        "overridden": False,
        "custom_source": None,
        "applicable": applicable,
    }


def catalog_parameters(layer_code: str | None = None, layer_category: str | None = None) -> list[dict]:
    """Alle Katalog-Parameter (Defaults)."""
    params: list[dict] = []

    def match(code: str, cat: str) -> bool:
        if layer_code and code != layer_code:
            return False
        if layer_category and cat != layer_category:
            return False
        return True

    for r in catalog.RISKS:
        if not match(r["code"], "risks"):
            continue
        params.append(_base_param(
            f"risks.{r['code']}.ref_value",
            layer_code=r["code"], layer_category="risks",
            label="Referenzwert (Index = 100)",
            value=float(r.get("ref_value", 0.0)),
            unit=r.get("outcome_unit", ""),
            source=r.get("source") or "Modellannahme (kein Kurz-Key hinterlegt)",
            source_detail=r.get("source_detail", ""),
            references=sources.resolve(r.get("source_refs")),
        ))
        # Monetarisierungs-Kostensatz je nicht-monetärem Risiko: eigenständiger,
        # editierbarer Parameter (€ je Outcome-Einheit). Monetäre Risiken (ref_value
        # bereits in €/Jahr) bekommen keinen Kostensatz-Parameter.
        if not catalog.risk_is_monetary(r):
            params.append(_base_param(
                f"risks.{r['code']}.cost_per_outcome",
                layer_code=r["code"], layer_category="risks",
                label="Kostensatz (Monetarisierung)",
                value=catalog.risk_default_cost_per_outcome(r),
                unit=catalog.cost_unit_label(r.get("outcome_unit", "")),
                source=r.get("cost_source") or "Modellannahme (Kostensatz, unbelegt)",
                source_detail=r.get("cost_source_detail", ""),
                references=sources.resolve(r.get("cost_source_refs")),
            ))
        # Schicht-B-Schadensfunktions-Parameter (baseline_mort, β, Schwellen, Raten …).
        for spec in _IMPACT_SPECS_BY_RISK.get(r["code"], []):
            params.append(_base_param(
                f"risks.{r['code']}.impact.{spec['key']}",
                layer_code=r["code"], layer_category="risks",
                label=f"Schadensfunktion: {spec['label']}",
                value=spec["value"],
                unit=spec.get("unit", ""),
                source=spec.get("source", ""),
                source_detail=spec.get("source_detail", ""),
                references=sources.resolve(spec.get("source_refs")),
            ))

    for cat_key, items in (
        ("hazards", catalog.HAZARDS),
        ("exposures", catalog.EXPOSURES),
        ("vulnerabilities", catalog.VULNERABILITIES),
    ):
        for m in items:
            if not match(m["code"], cat_key):
                continue
            for bound, label in (("norm_min", "Normierung Untergrenze"), ("norm_max", "Normierung Obergrenze")):
                params.append(_base_param(
                    f"{cat_key}.{m['code']}.{bound}",
                    layer_code=m["code"], layer_category=cat_key,
                    label=label,
                    value=float(m.get(bound, 0.0)),
                    unit=m.get("unit", ""),
                    source=m.get("source") or "Modellannahme (Normierungsskala, unbelegt)",
                    source_detail=m.get("source_detail", ""),
                    references=sources.resolve(m.get("source_refs")),
                ))

    for code, recipe in formulas.DETAILED.items():
        cat = "hazards" if code in catalog.HAZARDS_BY_CODE else (
            "exposures" if code in catalog.EXPOSURES_BY_CODE else "vulnerabilities"
        )
        # Bei Risiko-Filter ebenfalls mitliefern: Risiko-Wirkungsdiagramme betten die
        # H/E/V-Teilbäume samt deren Rezeptparametern ein.
        if not match(code, cat) and layer_category != "risks":
            continue
        for inp in recipe.get("inputs", []):
            if inp.get("prov") != "param":
                continue
            # Nur explizit als override-fähig markierte Formel-Parameter emittieren
            # (formulas._i(..., overridable=True)): alle anderen ``param``-Inputs sind
            # in indicators.py fest verdrahtete Literale — als editierbare Parameter
            # wären sie wirkungslos (tote Parameter).
            if not inp.get("overridable"):
                continue
            if inp.get("value") is None:
                continue
            key = inp.get("key", "value")
            params.append(_base_param(
                f"{cat}.{code}.param.{key}",
                layer_code=code, layer_category=cat,
                label=inp.get("label", key),
                value=inp["value"],
                unit=inp.get("unit", ""),
                source=_param_doc_source(inp),
                source_detail=inp.get("source_detail", ""),
                references=sources.resolve(inp.get("source_refs")),
            ))

    for m in catalog.MEASURES:
        if layer_category and layer_category != "measures":
            continue
        if layer_code and m["code"] != layer_code:
            continue
        for field, label, unit in MEASURE_PARAM_SPECS:
            applicable = m.get(field) is not None
            source = (m.get("sources") or {}).get(field) or m.get("source") \
                or "Modellannahme (Maßnahmenkosten, unbelegt)"
            source_detail = (m.get("source_details") or {}).get(field) or ""
            refs = sources.resolve((m.get("source_refs") or {}).get(field))
            params.append(_base_param(
                f"measures.{m['code']}.{field}",
                layer_code=m["code"], layer_category="measures",
                label=label,
                value=float(m.get(field)) if applicable else 0.0,
                unit=unit,
                source=source,
                source_detail=source_detail,
                references=refs,
                editable=applicable,
                applicable=applicable,
            ))

    def emit_globals(cat: str) -> bool:
        """Layer-lose Parametergruppen: ohne Filter immer, mit Kategorie-Filter passend."""
        return not layer_code and (layer_category is None or layer_category == cat)

    uhi_defaults = {"alpha": 6.0, "beta": 2.0, "gamma": 3.5, "delta": 2.0,
                    "epsilon": 1.5, "tree_cooling": 0.3}
    uhi_labels = {
        "alpha": "UHI-Koeffizient α",
        "beta": "UHI-Koeffizient β",
        "gamma": "UHI-Koeffizient γ",
        "delta": "UHI-Koeffizient δ",
        "epsilon": "UHI-Koeffizient ε (Straßenschluchten)",
        "tree_cooling": "UHI-Koeffizient Baumkronen-Kühlung",
    }
    uhi_details = {
        "alpha": "Skaliert den Versiegelungs-/Bebauungsbeitrag zur Wärmeinselintensität. "
            "Größenordnung dokumentierter maximaler UHI-Intensitäten mitteleuropäischer Städte "
            "(Nacht-ΔT bis ~6-10 K; Oke 1982, Stewart & Oke 2012 „Local Climate Zones“, "
            "VDI 3787 Bl.1). Modellwahl im belegten Wertebereich, editierbar.",
        "beta": "Gewichtet den kühlenden Grün-/Wasseranteil gegen die Überwärmung. "
            "Größenordnung aus der UHI-/Grünflächenliteratur (Oke 1982; VDI 3787 Bl.1). "
            "Dokumentierte Modellwahl, editierbar.",
        "gamma": "Skaliert den Albedo-/Oberflächenbeitrag (helle vs. dunkle Beläge). "
            "Belegt durch die Strahlungshaushalts-Betrachtung in Oke 1982 und VDI 3787 Bl.1. "
            "Dokumentierte Modellwahl, editierbar.",
        "delta": "Gewichtet die Belüftung/Kaltluftzufuhr (Frischluftschneisen). "
            "Qualitativ belegt durch VDI 3787 Bl.1 (Stadtklima/Kaltluft). Dokumentierte "
            "Modellwahl, editierbar.",
        "epsilon": "Skaliert den Straßenschluchten-Beitrag: ΔT-Zuschlag ∝ (1 − Sky-View-"
            "Faktor) · Gebäudehöhenfaktor. Die Schluchtengeometrie (Sky-View) ist der "
            "klassische Treiber der nächtlichen UHI (Oke 1982, canyon geometry; VDI 3787 "
            "Bl.1). Dokumentierte Modellwahl im belegten Wirkbereich, editierbar.",
        "tree_cooling": "Kühlwirkung des Baumkronenanteils: ΔT-Abschlag = Koeffizient · "
            "Kronenanteil · 10 (d. h. 0,3 K je 10 % Kronenschluss). Größenordnung aus der "
            "Stadtbaum-/Beschattungsliteratur: dichte Kronen senken die lokale Lufttemperatur "
            "um ~1-3 K (VDI 3787 Bl.1; Stewart & Oke 2012). Dokumentierte Modellwahl, "
            "editierbar.",
    }
    if emit_globals("uhi"):
        for key, val in uhi_defaults.items():
            params.append(_base_param(
                f"uhi.{key}",
                layer_code="", layer_category="uhi",
                label=uhi_labels[key],
                value=val,
                unit="K/Index",
                source="VDI 3787 Bl.1 / Oke 1982 / Stewart & Oke 2012",
                source_detail=uhi_details[key],
                references=sources.resolve(["VDI3787_Stadtklima", "StewartOke_LCZ_2012"]),
            ))

    # Globale Schicht-B-Parameter (Assetwerte, k_indirekt, Kurvenexponent): auch bei
    # Risiko-Layer-Filter mitliefern — das Wirkungsdiagramm referenziert sie als
    # editierbare Parameterknoten (impact.<key>) im Schicht-B-Zweig.
    if emit_globals("impact") or layer_category == "risks":
        for spec in IMPACT_GLOBAL_SPECS:
            params.append(_base_param(
                f"impact.{spec['key']}",
                layer_code="", layer_category="impact",
                label=f"Schadensfunktion: {spec['label']}",
                value=spec["value"],
                unit=spec.get("unit", ""),
                source=spec.get("source", ""),
                source_detail=spec.get("source_detail", ""),
                references=sources.resolve(spec.get("source_refs")),
            ))

    # Modellweite Stellschrauben (Referenzskalierung, Risikozonen-Schwelle,
    # Maßnahmen-Sättigung/-Kappung) — Single Source: engine/tunables.py.
    if emit_globals("model"):
        for spec in tunables.MODEL_PARAM_SPECS:
            params.append(_base_param(
                f"model.{spec['key']}",
                layer_code="", layer_category="model",
                label=spec["label"],
                value=spec["value"],
                unit=spec.get("unit", ""),
                source=spec.get("source", ""),
                source_detail=spec.get("source_detail", ""),
                references=sources.resolve(spec.get("source_refs")),
            ))

    # Regionale Proxy-/Fallback-Klimatreiber (inputs.build_regional_context).
    if emit_globals("regional"):
        for spec in tunables.REGIONAL_FALLBACK_SPECS:
            params.append(_base_param(
                f"regional.{spec['key']}",
                layer_code="", layer_category="regional",
                label=spec["label"],
                value=spec["value"],
                unit=spec.get("unit", ""),
                source=spec.get("source", ""),
                source_detail=spec.get("source_detail", ""),
                references=sources.resolve(spec.get("source_refs")),
            ))

    return params


def merge_overrides(
    params: list[dict],
    db_overrides: list[dict],
) -> list[dict]:
    """Wendet kommune-spezifische Overrides auf die Registry an."""
    by_id = {o["parameter_id"]: o for o in db_overrides if o.get("parameter_id")}
    out = []
    for p in params:
        merged = dict(p)
        o = by_id.get(p["id"])
        if o:
            merged["value"] = o.get("value", p["value"])
            merged["overridden"] = merged["value"] != p["default_value"]
            merged["custom_source"] = o.get("custom_source")
            if o.get("source"):
                merged["source"] = o["source"]
        out.append(merged)
    return out


def overrides_map(db_overrides: list[dict]) -> dict[str, Any]:
    """Flache Map parameter_id → value für die Engine."""
    return {o["parameter_id"]: o["value"] for o in db_overrides if o.get("parameter_id")}


def resolve_measure_def(mdef: dict, overrides: dict[str, Any] | None = None) -> dict:
    """Wendet Parameter-Overrides auf eine Maßnahmen-Katalogdefinition an."""
    if not mdef:
        return mdef
    ov = overrides or {}
    code = mdef["code"]
    out = dict(mdef)
    for field in MEASURE_OVERRIDE_FIELDS:
        val = ov.get(f"measures.{code}.{field}")
        if val is not None:
            out[field] = float(val)
    return out


def load_db_overrides(db, kommune_id: int) -> list[dict]:
    from app.models.models import ConfigParameter

    rows = db.query(ConfigParameter).filter(ConfigParameter.kommune_id == kommune_id).all()
    result = []
    for r in rows:
        if r.parameter_id:
            result.append({
                "parameter_id": r.parameter_id,
                "value": r.value,
                "source": r.source,
                "custom_source": r.custom_source,
            })
        else:
            result.append({
                "parameter_id": f"{r.category}.{r.key}",
                "value": r.value,
                "source": r.source,
                "custom_source": r.custom_source,
            })
    return result
