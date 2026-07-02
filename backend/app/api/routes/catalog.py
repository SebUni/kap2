"""Stellt den festen Fachkatalog (H/E/V/Risiken/Maßnahmen/Gruppen) bereit.

Single source of truth ist ``app/data/catalog.py``. Das Frontend lädt diese
Metadaten einmalig (Labels, Einheiten, Gruppen, Beschreibungen, Proxys) und
nutzt sie für Layer-Spalte, Tooltips und Dashboard.
"""

from fastapi import APIRouter, HTTPException, Query

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
def get_catalog():
    return {
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
    }


@router.get("/catalog/layer/{code}/recipe")
def get_layer_recipe(code: str, category: str | None = Query(None)):
    """Rezept-Metadaten einer Ebene (ohne Assessment / Zellwerte)."""
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
