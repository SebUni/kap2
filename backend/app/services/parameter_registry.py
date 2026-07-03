"""Zentrale Parameter-Registry für Info-Fenster, Konfiguration und Engine-Overrides."""

from __future__ import annotations

from typing import Any

from app.data import catalog
from app.services.engine import formulas

PATHWAY_WEIGHT_LABELS = {
    "primary": "Gewicht primärer Pfad",
    "aligned": "Gewicht paralleler Pfade",
    "alternate_hazard": "Gewicht alternativer Klimatreiber",
    "alternate_exposure": "Gewicht alternativer Exposition",
    "alternate_vulnerability": "Gewicht alternativer Sensitivität",
    "compound_he": "Gewicht verbundener H·E-Pfade",
    "compound_hv": "Gewicht verbundener H·V-Pfade",
    "compound_ev": "Gewicht verbundener E·V-Pfade",
    "compound_multi": "Gewicht Compound-Pfade",
}

MEASURE_PARAM_SPECS: tuple[tuple[str, str, str], ...] = (
    ("default_reduction", "Standard-Risikoreduktion", "Anteil"),
    ("cost_per_m2", "Investitionskosten pro m²", "€/m²"),
    ("cost_per_unit", "Investitionskosten pro Einheit", "€/Stück"),
    ("maintenance_per_m2_year", "Wartungskosten pro m² und Jahr", "€/(m²·a)"),
    ("benefit_per_m2_year", "Direkter Nutzen pro m² und Jahr", "€/(m²·a)"),
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
    prov: str = "param",
    editable: bool = True,
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
        "prov": prov,
        "editable": editable,
        "overridden": False,
        "custom_source": None,
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
                ))

    for ptype, label in PATHWAY_WEIGHT_LABELS.items():
        if layer_category and layer_category != "risks":
            continue
        if layer_code and layer_category != "risks":
            continue
        val = float(catalog.PATHWAY_WEIGHTS.get(ptype, 0.0))
        params.append(_base_param(
            f"pathway_weights.{ptype}",
            layer_code="", layer_category="model",
            label=label,
            value=val,
            unit="Gewicht",
            source=catalog.PATHWAY_WEIGHT_SOURCE,
        ))

    for code, recipe in formulas.DETAILED.items():
        cat = "hazards" if code in catalog.HAZARDS_BY_CODE else (
            "exposures" if code in catalog.EXPOSURES_BY_CODE else "vulnerabilities"
        )
        if not match(code, cat):
            continue
        for inp in recipe.get("inputs", []):
            if inp.get("prov") != "param":
                continue
            if "value" not in inp:
                continue
            key = inp.get("key", "value")
            params.append(_base_param(
                f"{cat}.{code}.param.{key}",
                layer_code=code, layer_category=cat,
                label=inp.get("label", key),
                value=inp["value"],
                unit=inp.get("unit", ""),
                source=_param_doc_source(inp),
            ))

    for m in catalog.MEASURES:
        if layer_category and layer_category != "measures":
            continue
        if layer_code and m["code"] != layer_code:
            continue
        source = m.get("source") or "KAP3-Vorschlag + Plausibilität (Maßnahmenkosten, unbelegt)"
        for field, label, unit in MEASURE_PARAM_SPECS:
            params.append(_base_param(
                f"measures.{m['code']}.{field}",
                layer_code=m["code"], layer_category="measures",
                label=label,
                value=float(m.get(field) or 0.0),
                unit=unit,
                source=source,
            ))

    uhi_defaults = {"alpha": 6.0, "beta": 2.0, "gamma": 3.5, "delta": 2.0}
    uhi_labels = {
        "alpha": "UHI-Koeffizient α",
        "beta": "UHI-Koeffizient β",
        "gamma": "UHI-Koeffizient γ",
        "delta": "UHI-Koeffizient δ",
    }
    if not layer_code and not layer_category:
        for key, val in uhi_defaults.items():
            params.append(_base_param(
                f"uhi.{key}",
                layer_code="", layer_category="uhi",
                label=uhi_labels[key],
                value=val,
                unit="K/Index",
                source="VDI 3787 Bl.1 / Oke 1982 / Stewart & Oke 2012",
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
