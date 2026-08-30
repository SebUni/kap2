"""Stellt den festen Fachkatalog (H/E/V/Risiken/Maßnahmen/Gruppen) bereit.

Single source of truth ist ``app/data/catalog.py``. Das Frontend lädt diese
Metadaten einmalig (Labels, Einheiten, Gruppen, Beschreibungen, Proxys) und
nutzt sie für Layer-Spalte, Tooltips und Dashboard.
"""

from fastapi import APIRouter, HTTPException, Query, Request

from app.api.deps import demo_session_id_of
from app.data import catalog
from app.services.engine import formulas
from app.services import lineage_graph

router = APIRouter()


def _layer_category(code: str) -> str | None:
    if code in catalog.HAZARDS_BY_CODE:
        return "hazards"
    if code in catalog.EXPOSURES_BY_CODE:
        return "exposures"
    if code in catalog.VULNERABILITIES_BY_CODE:
        return "vulnerabilities"
    if code in catalog.AUXILIARY_BY_CODE:
        return "auxiliary"
    if code in catalog.RISKS_BY_CODE:
        return "risks"
    return None


@router.get("/catalog")
def get_catalog(request: Request):
    payload = {
        "groups": catalog.KWRA_GROUPS,
        "hazards": catalog.HAZARDS,
        "exposures": catalog.EXPOSURES,
        "vulnerabilities": catalog.VULNERABILITIES,
        "risks": catalog.RISKS,
        "measures": catalog.MEASURES,
        "hazard_categories": catalog.HAZARD_CATEGORIES,
        "exposure_categories": catalog.EXPOSURE_CATEGORIES,
        "vulnerability_categories": catalog.VULNERABILITY_CATEGORIES,
        "kang_clusters": catalog.KANG_CLUSTERS,
        "auxiliary": catalog.AUXILIARY,
        "auxiliary_categories": catalog.AUXILIARY_CATEGORIES,
        # Geplante (gesperrte) KWRA-Klimawirkungen inkl. aufgelöstem
        # Verfügbarkeits-Label — Anzeige im LayerPanel als 🔒-Einträge.
        "planned_risks": [
            {**p, "available_from": catalog.planned_available_from(p)}
            for p in catalog.PLANNED_RISKS
        ],
        "stage_labels": catalog.STAGE_LABELS,
    }
    if demo_session_id_of(request):
        from app.services import demo_service
        enabled = getattr(request.state, "demo_enabled_layers", set())
        risk_codes = getattr(request.state, "demo_risk_codes", [])
        return demo_service.filter_catalog(payload, enabled, risk_codes)
    return payload


@router.get("/catalog/layer/{code}/recipe")
def get_layer_recipe(code: str, request: Request, category: str | None = Query(None)):
    """Rezept-Metadaten einer Ebene (ohne Assessment / Zellwerte)."""
    # Demo: Wirkungsmechanismus nur für freigeschaltete Ebenen (Plan §3.6).
    if demo_session_id_of(request):
        enabled = getattr(request.state, "demo_enabled_layers", set())
        if code not in enabled:
            raise HTTPException(403, "Diese Ebene ist in der Demo nicht freigeschaltet")
    cat = category or _layer_category(code)
    if not cat:
        raise HTTPException(404, f"Unbekannter Code: {code}")
    if cat == "risks" and code not in catalog.RISKS_BY_CODE:
        raise HTTPException(404, f"Unbekannter Risiko-Code: {code}")
    if cat in ("hazards", "exposures", "vulnerabilities") and code not in catalog.INDICATOR_BY_CODE:
        raise HTTPException(404, f"Unbekannter Indikator: {code}")

    recipe = formulas.recipe_for_layer(code, cat)
    meta: dict = {"code": code, "category": cat, "recipe": recipe}

    if cat == "risks":
        r = catalog.RISKS_BY_CODE[code]
        meta.update({
            "label": r["name"],
            "description": r.get("description", ""),
            "unit": r.get("outcome_unit", ""),
            "group": r.get("group"),
        })
    elif cat == "auxiliary":
        m = catalog.AUXILIARY_BY_CODE[code]
        meta.update({
            "label": m["name"],
            "description": m.get("description", ""),
            "unit": m.get("unit", ""),
        })
    else:
        m = catalog.INDICATOR_BY_CODE[code]
        meta.update({
            "label": m["name"],
            "description": m.get("description", ""),
            "unit": m.get("unit", ""),
            "norm_min": m.get("norm_min"),
            "norm_max": m.get("norm_max"),
            "source": m.get("source"),
            "proxy": m.get("proxy"),
            "spatial": m.get("spatial", True),
        })

    return {**meta, "lineage": lineage_graph.build_for_layer(code, cat)}
