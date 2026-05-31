"""Stellt den festen Fachkatalog (H/E/V/Risiken/Maßnahmen/Gruppen) bereit.

Single source of truth ist ``app/data/catalog.py``. Das Frontend lädt diese
Metadaten einmalig (Labels, Einheiten, Gruppen, Beschreibungen, Proxys) und
nutzt sie für Layer-Spalte, Tooltips und Dashboard.
"""

from fastapi import APIRouter

from app.data import catalog

router = APIRouter()


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
    }
