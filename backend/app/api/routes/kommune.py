import asyncio
import os
import shutil

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import shape as shapely_shape, mapping
from sqlalchemy.orm import Session, load_only

from app.api.deps import require_admin, require_user, user_kommune_ids
from app.api.gzip_files import file_etag, gzip_json_file_response
from app.db.database import get_db
from app.models.auth_models import User
from app.models.models import (
    Kommune, ConfigParameter,
    CellAssessment, GridCell, AdaptationMeasure,
    MeasureImpact, ProjectStatus, RiskZone, GeoExportJob,
)
from app.data import catalog
from app.data.kang_handlungsfelder import handlungsfeld_fuer_risiko
from app.data.kang_zustaendigkeit import zustaendigkeit_fuer
from app.services import kang_beruecksichtigung
from app.services.bestandsaufnahme_markdown import bestandsaufnahme_markdown
from app.services.kurzfassung_markdown import kurzfassung_fuer_kommune
from app.services.measure_service import get_risk_aggregate, kommune_measures_query
from app.services.systembereiche import systembereich_auswertung
from app.services.geodata_export_service import get_exports_dir, assessment_is_done
from app.schemas.schemas import KommuneCreate, KommuneOut, KommuneSearch, GridGenerateRequest
from app.services import (
    aggregate_cache, artifact_rebuild, bestandsaufnahme_service, dashboard_cache,
    kommune_profile_service,
    osm_service, grid_service, layer_cache, unsicherheits_zusammenschau,
)

router = APIRouter()


@router.get("/search", response_model=list[dict])
async def search(q: str, limit: int = 10):
    """Search for a municipality via OSM Nominatim."""
    if len(q) < 2:
        raise HTTPException(400, "Suchbegriff muss mindestens 2 Zeichen lang sein")
    results = await osm_service.search_kommune(q, limit=limit)
    return results


@router.post("", response_model=KommuneOut)
async def create_kommune(
    data: KommuneCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    """Create a municipality by fetching its boundary from OSM. (Admin)"""
    existing = db.query(Kommune).filter(Kommune.osm_id == data.osm_id).first()
    if existing:
        return _kommune_to_out(existing)

    # Fetch boundary (Nominatim geometry → Nominatim lookup → Overpass mirrors)
    boundary_geojson = await osm_service.fetch_kommune_boundary(
        data.osm_id, data.osm_type, nominatim_geojson=data.geojson
    )
    if not boundary_geojson:
        raise HTTPException(404, "Kommune-Grenze konnte nicht abgerufen werden")

    # Convert GeoJSON to shapely, then to WKB for PostGIS
    shape = shapely_shape(boundary_geojson)
    if shape.geom_type == "Polygon":
        from shapely.geometry import MultiPolygon
        shape = MultiPolygon([shape])

    area_km2 = _estimate_area_km2(shape)

    kommune = Kommune(
        name=data.name,
        osm_id=data.osm_id,
        boundary=from_shape(shape, srid=4326),
        area_km2=round(area_km2, 2),
        bundesland=data.bundesland or osm_service.bundesland_from_address(data.address),
        landkreis=osm_service.landkreis_from_address(data.address),
    )
    db.add(kommune)
    db.commit()
    db.refresh(kommune)

    # Set default config parameters
    _set_default_config(db, kommune.id)

    return _kommune_to_out(kommune)


@router.get("/{kommune_id}", response_model=KommuneOut)
def get_kommune(kommune_id: int, db: Session = Depends(get_db)):
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")
    return _kommune_to_out(kommune)


@router.get("/{kommune_id}/profile")
async def get_kommune_profile(kommune_id: int, request: Request, db: Session = Depends(get_db)):
    """Kommunen-Profil: Basisdaten + Klimakennzahlen mit Deutschland-Vergleich.

    Payload wird im Hintergrund vorgebaut (``dashboard_cache``, inkl. BIP/
    Kommunalhaushalt via finance_loader); hier nur Datei-Auslieferung mit
    ETag/304 (Lazy-Build im Thread, damit der erste, langsame GENESIS-Abruf den
    Event-Loop nicht blockiert). Fehlendes Bundesland/Landkreis wird vorab
    einmalig per Nominatim-Reverse-Geocoding nachgetragen (Lazy-Backfill) —
    das Bundesland speist den Regionalkontext, deshalb danach Rebuild anstoßen.
    """
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")

    if not kommune.bundesland or not kommune.landkreis:
        centroid = kommune_profile_service.centroid_of(kommune)
        if centroid:
            bl, lk = await osm_service.reverse_admin(lat=centroid[1], lon=centroid[0])
            if bl and not kommune.bundesland:
                kommune.bundesland = bl
            if lk and not kommune.landkreis:
                kommune.landkreis = lk
            if bl or lk:
                db.commit()
                artifact_rebuild.invalidate_and_schedule(kommune_id)

    art = await asyncio.to_thread(dashboard_cache.artifact_file, db, kommune_id, "profile")
    if not art:
        raise HTTPException(404, "Kommune nicht gefunden")
    path, etag = art
    return gzip_json_file_response(
        request, path, etag=etag, download_name=f"profile-{kommune_id}.json",
    )


@router.get("/{kommune_id}/bestandsaufnahme")
async def get_kommune_bestandsaufnahme(kommune_id: int, db: Session = Depends(get_db)):
    """Bestandsaufnahme der Kommune als Markdown-Bericht (Zeile 16, T-0447).

    Mandantenschutz über die Router-Dependency ``require_kommune_access``.
    Geladen werden nur die Spalten, die der Dienst braucht (keine Geometrie);
    der blockierende Datenzugriff läuft wie beim Profil in einem Thread.
    """
    kommune = (
        db.query(Kommune)
        .options(load_only(Kommune.id, Kommune.name, Kommune.osm_id))
        .filter(Kommune.id == kommune_id)
        .first()
    )
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")
    ergebnis = await asyncio.to_thread(
        bestandsaufnahme_service.bestandsaufnahme_fuer_kommune, db, kommune,
    )
    return Response(
        content=bestandsaufnahme_markdown(ergebnis),
        media_type="text/markdown; charset=utf-8",
    )


@router.get("/{kommune_id}/kurzfassung")
async def get_kommune_kurzfassung(kommune_id: int, db: Session = Depends(get_db)):
    """Kurzfassung für politische Entscheidungsträger als Markdown (Zeile 20, T-0452).

    Fünf feste Abschnitte; alle Zahlen unverändert aus ``get_risk_aggregate``,
    ``project_costs`` und ``build_cost_summary``. Mandantenschutz über die
    Router-Dependency ``require_kommune_access``.
    """
    kommune = (
        db.query(Kommune)
        .options(load_only(Kommune.id, Kommune.name, Kommune.bundesland))
        .filter(Kommune.id == kommune_id)
        .first()
    )
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")
    inhalt = await asyncio.to_thread(kurzfassung_fuer_kommune, db, kommune)
    return Response(content=inhalt, media_type="text/markdown; charset=utf-8")


@router.get("/{kommune_id}/kang-zustaendigkeit")
def get_kommune_kang_zustaendigkeit(kommune_id: int, db: Session = Depends(get_db)):
    """Zuständige Stelle für das Klimaanpassungskonzept nach § 12 Abs. 1 KAnG (T-0751)."""
    kommune = (
        db.query(Kommune)
        .options(load_only(Kommune.id, Kommune.bundesland))
        .filter(Kommune.id == kommune_id)
        .first()
    )
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")
    return zustaendigkeit_fuer(kommune.bundesland)


@router.get("/{kommune_id}/unsicherheits-zusammenschau")
def get_kommune_unsicherheits_zusammenschau(kommune_id: int, db: Session = Depends(get_db)):
    """Handlungsfeldübergreifende Unsicherheits-Zusammenschau vor der Ableitung von
    Handlungsoptionen (Checkliste Zeile 19, T-0451)."""
    kommune = (
        db.query(Kommune)
        .options(load_only(Kommune.id))
        .filter(Kommune.id == kommune_id)
        .first()
    )
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")
    return unsicherheits_zusammenschau.unsicherheits_zusammenschau(kommune.id)


@router.get("/{kommune_id}/systembereiche")
def get_kommune_systembereiche(kommune_id: int, db: Session = Depends(get_db)):
    """Auswertung über die fünf KWRA-Systembereiche (Checkliste Zeile 10, KWRA TB 6 Kap. 7).

    Alle fünf Bereiche stehen immer da, in der Reihenfolge ``catalog.KWRA_SYSTEMBEREICHE``.
    Ein Bereich ohne Klimawirkung wird nicht ausgeblendet, sondern mit ``leer_grund``
    ausgewiesen (P2); ohne Risiko-Aggregat sind alle fünf so leer.
    """
    kommune = (
        db.query(Kommune)
        .options(load_only(Kommune.id))
        .filter(Kommune.id == kommune_id)
        .first()
    )
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")
    # Ein Aggregat gibt es erst nach der Berechnung. Ohne sie legt die Engine für jedes
    # Katalogrisiko einen Nulleintrag an; das wäre keine leere, sondern eine falsche Auswertung.
    liegt_aggregat_vor = assessment_is_done(db, kommune.id)
    if liegt_aggregat_vor:
        agg = get_risk_aggregate(db, kommune.id, apply_measures=False)
    else:
        agg = {"cost": {"by_risk": []}}
    auswertung = systembereich_auswertung(agg)
    bereiche = []
    for name in catalog.KWRA_SYSTEMBEREICHE:
        eintrag = auswertung[name]
        if eintrag["anzahl_klimawirkungen"] == 0:
            grund = (
                f"Für den Systembereich „{name}“ ist in KAP3 heute keine Klimawirkung "
                "gerechnet; der Bereich bleibt als leer ausgewiesen."
                if liegt_aggregat_vor else
                f"Für diese Kommune liegt noch keine Risikoberechnung vor; der Systembereich "
                f"„{name}“ ist deshalb leer."
            )
        else:
            grund = None
        bereiche.append({"systembereich": name, **eintrag, "leer_grund": grund})
    return {"kommune_id": kommune.id, "bereiche": bereiche}


def _risiko_zuordenbar(code) -> bool:
    """True, wenn der Nachweis den Risikocode einem KAnG-Handlungsfeld zuordnen kann."""
    try:
        handlungsfeld_fuer_risiko(code)
    except KeyError:
        return False
    return True


def _massnahme_zuordenbar(code) -> bool:
    """True, wenn der Katalog die Maßnahme samt Handlungsfeld und verknüpften Risiken kennt."""
    eintrag = catalog.MEASURES_BY_CODE.get(code)
    if eintrag is None or "kang_cluster" not in eintrag or "kang_field" not in eintrag:
        return False
    return all(_risiko_zuordenbar(r) for r in (eintrag.get("linked_risk_codes") or []))


@router.get("/{kommune_id}/kang-nachweis")
def get_kommune_kang_nachweis(kommune_id: int, db: Session = Depends(get_db)):
    """Nachweis der fachübergreifenden Berücksichtigung nach § 8 Abs. 1 KAnG
    (Checkliste Zeile 13, T-1064).

    ``schaeden`` ist die jährliche Schadenssumme je Risikocode aus dem Risiko-Aggregat
    (leer, solange keine Berechnung vorliegt), ``massnahmen`` die Maßnahmencodes der
    Kommune. Codes, die der Katalog nicht kennt, werden nicht still weggelassen, sondern
    unter ``nicht_zugeordnet`` mit ihrem Betrag bzw. Code ausgewiesen.
    """
    kommune = (
        db.query(Kommune)
        .options(load_only(Kommune.id))
        .filter(Kommune.id == kommune_id)
        .first()
    )
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")

    # Wie bei den Systembereichen: ohne Berechnung legt die Engine Nulleinträge an.
    schaeden: dict = {}
    if assessment_is_done(db, kommune.id):
        agg = get_risk_aggregate(db, kommune.id, apply_measures=False)
        for eintrag in agg["cost"]["by_risk"]:
            code = eintrag["code"]
            # Verwechslungssperre Klasse A/B (T-0879): Eine Wirkung ohne Euro-Schicht
            # trägt keinen Betrag — None statt 0 €, auch unter ``nicht_zugeordnet``.
            # Der Nachweis lässt None aus der Feldsumme heraus (wie risk_engine.aggregate).
            if eintrag.get("has_euro_layer") is False:
                schaeden[code] = None
                continue
            schaeden[code] = schaeden.get(code, 0.0) + float(eintrag.get("cost_eur") or 0.0)

    massnahmen = [
        m.measure_type
        for m in kommune_measures_query(db, kommune.id).options(
            load_only(AdaptationMeasure.id, AdaptationMeasure.measure_type)
        )
    ]

    risiken_bekannt = {c: b for c, b in schaeden.items() if _risiko_zuordenbar(c)}
    risiken_unbekannt = [
        {"code": c, "schaden_eur": b} for c, b in schaeden.items() if c not in risiken_bekannt
    ]
    massnahmen_bekannt = [c for c in massnahmen if _massnahme_zuordenbar(c)]
    massnahmen_unbekannt = sorted({c for c in massnahmen if not _massnahme_zuordenbar(c)})

    nachweis = kang_beruecksichtigung.nachweis_fachuebergreifend(
        risiken_bekannt, massnahmen_bekannt,
    )
    nachweis["nicht_zugeordnet"] = {
        "risiken": risiken_unbekannt,
        "massnahmen": massnahmen_unbekannt,
    }
    return nachweis


@router.get("")
def list_kommunen(
    calculated: bool = False,
    db: Session = Depends(get_db),
    user: User = Depends(require_user),
):
    kommunen = db.query(Kommune).order_by(Kommune.name).all()
    if not user.is_admin:
        allowed = user_kommune_ids(db, user)
        kommunen = [k for k in kommunen if k.id in allowed]
    if calculated:
        kommunen = [k for k in kommunen if assessment_is_done(db, k.id)]
    return [_kommune_to_out(k, include_boundary=False) for k in kommunen]


@router.post("/{kommune_id}/grid")
def generate_grid(
    kommune_id: int,
    req: GridGenerateRequest = GridGenerateRequest(),
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    """Generate a grid over the municipality boundary. (Admin)"""
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")

    count = grid_service.generate_grid(
        db, kommune_id, cell_size_m=req.cell_size_m, force=req.force,
    )
    # Kein Rebuild anstoßen: nach Grid-Neubau gibt es noch keine Zellwerte.
    aggregate_cache.invalidate(kommune_id)
    layer_cache.invalidate(kommune_id)
    dashboard_cache.invalidate(kommune_id)
    return {"kommune_id": kommune_id, "cells_created": count, "cell_size_m": req.cell_size_m}


@router.get("/{kommune_id}/grid")
def get_grid(kommune_id: int, request: Request, db: Session = Depends(get_db)):
    """Zellgeometrie als gzip-GeoJSON (Legacy-Pfad; identische Datei wie
    ``/grid-geometry`` aus dem layer_cache statt teurem Per-Request-Build)."""
    path = layer_cache.geometry_file(db, kommune_id)
    if not path:
        return {"type": "FeatureCollection", "features": []}
    return gzip_json_file_response(
        request, path, etag=file_etag(path), download_name=f"grid-{kommune_id}.json",
    )


@router.post("/{kommune_id}/reset")
def reset_kommune(
    kommune_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    """Reset all assessment, grid, and measure data for a municipality. (Admin)

    Keeps the municipality entry (boundary, name, config) but deletes:
    climate assessments, grid cells, adaptation measures, project statuses,
    risk zones, and all derived data.
    """
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")

    # 1. Delete MeasureImpacts before their parents
    measure_ids = [
        r[0] for r in
        db.query(AdaptationMeasure.id)
        .filter(AdaptationMeasure.kommune_id == kommune_id)
        .all()
    ]
    if measure_ids:
        db.query(MeasureImpact)\
            .filter(MeasureImpact.measure_id.in_(measure_ids))\
            .delete(synchronize_session=False)

    # 2. Cell assessments
    db.query(CellAssessment)\
        .filter(CellAssessment.kommune_id == kommune_id)\
        .delete(synchronize_session=False)

    # 3. Risk zones (DB cascades to risk_zone_cells)
    db.query(RiskZone)\
        .filter(RiskZone.kommune_id == kommune_id)\
        .delete(synchronize_session=False)

    # 4. Grid cells (DB cascades any remaining child records)
    db.query(GridCell)\
        .filter(GridCell.kommune_id == kommune_id)\
        .delete(synchronize_session=False)

    # 5. Adaptation measures
    db.query(AdaptationMeasure)\
        .filter(AdaptationMeasure.kommune_id == kommune_id)\
        .delete(synchronize_session=False)

    # 6. Project statuses
    db.query(ProjectStatus)\
        .filter(ProjectStatus.kommune_id == kommune_id)\
        .delete(synchronize_session=False)

    # 7. Geo export jobs
    db.query(GeoExportJob)\
        .filter(GeoExportJob.kommune_id == kommune_id)\
        .delete(synchronize_session=False)

    db.commit()

    # Remove export files from disk
    export_dir = get_exports_dir(kommune_id)
    if os.path.isdir(export_dir):
        shutil.rmtree(export_dir, ignore_errors=True)

    # Alle Datei-Caches verwerfen (kein Rebuild: es gibt keine Daten mehr)
    aggregate_cache.invalidate(kommune_id)
    layer_cache.invalidate(kommune_id)
    dashboard_cache.invalidate(kommune_id)

    return {"message": "Zurückgesetzt", "kommune_id": kommune_id}



# ── Helpers ────────────────────────────────────────────────────────────────────

def _kommune_to_out(k: Kommune, include_boundary: bool = True) -> dict:
    out = {
        "id": k.id,
        "name": k.name,
        "bundesland": k.bundesland,
        "landkreis": k.landkreis,
        "osm_id": k.osm_id,
        "area_km2": k.area_km2,
        "population": k.population,
        "created_at": k.created_at.isoformat() if k.created_at else None,
    }
    if include_boundary and k.boundary is not None:
        shape = to_shape(k.boundary)
        out["boundary_geojson"] = mapping(shape)
    return out


def _estimate_area_km2(shape) -> float:
    """Rough area estimate using equirectangular approximation."""
    import math
    bounds = shape.bounds
    mid_lat = (bounds[1] + bounds[3]) / 2
    lat_km = 111.32
    lon_km = 111.32 * math.cos(math.radians(mid_lat))
    dx = (bounds[2] - bounds[0]) * lon_km
    dy = (bounds[3] - bounds[1]) * lat_km
    # Use the actual shape area, not just bounding box
    # shapely area in degrees², approximate conversion
    area_deg2 = shape.area
    area_km2 = area_deg2 * lat_km * lon_km
    return area_km2


def _set_default_config(db: Session, kommune_id: int):
    """Set minimal default configuration parameters for a new kommune.

    Die fachlichen Annahmen (Koeffizienten, Wirkungsstärken, Kostensätze) liegen
    fest im Katalog (``app/data/catalog.py``). Hier werden nur überschreibbare
    Defaults gesetzt, falls später UI-Konfiguration gewünscht ist.
    """
    defaults = [
        ("uhi", "alpha", 6.0, "UHI-Koeffizient α (Albedo & Versiegelung)"),
        ("uhi", "beta", 2.0, "UHI-Koeffizient β (Gebäudedichte)"),
        ("uhi", "gamma", 3.5, "UHI-Koeffizient γ (Grünkühlung)"),
        ("uhi", "delta", 2.0, "UHI-Koeffizient δ (Wasserkühlung)"),
    ]
    for cat, key, val, desc in defaults:
        existing = db.query(ConfigParameter).filter(
            ConfigParameter.kommune_id == kommune_id,
            ConfigParameter.category == cat,
            ConfigParameter.key == key,
        ).first()
        if not existing:
            db.add(ConfigParameter(kommune_id=kommune_id, category=cat, key=key,
                                   value=val, description=desc))
    db.commit()
