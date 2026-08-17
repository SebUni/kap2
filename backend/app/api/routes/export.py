import os
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse, Response
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import GeoExportJob, ExportStatus, Kommune
from app.services.export_service import export_measures_xlsx, import_measures_xlsx
from app.services.geodata_export_service import assessment_is_done
from app.tasks.geodata_export_task import run_geodata_export_background

router = APIRouter()


def _job_to_dict(job: GeoExportJob) -> dict:
    return {
        "id": job.id,
        "export_type": job.export_type,
        "status": job.status.value if job.status else None,
        "created_at": job.created_at.isoformat() if job.created_at else None,
        "finished_at": job.finished_at.isoformat() if job.finished_at else None,
        "error_message": job.error_message,
    }


@router.get("/kommune/{kommune_id}/exports")
def list_exports(kommune_id: int, db: Session = Depends(get_db)):
    """List all geo export jobs for a municipality (newest first)."""
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")

    jobs = (
        db.query(GeoExportJob)
        .filter(GeoExportJob.kommune_id == kommune_id)
        .order_by(GeoExportJob.created_at.desc())
        .all()
    )
    return [_job_to_dict(j) for j in jobs]


@router.post("/kommune/{kommune_id}/exports/geodaten")
def start_geodata_export(kommune_id: int, db: Session = Depends(get_db)):
    """Create a geodata export job and start background GeoPackage generation."""
    kommune = db.query(Kommune).filter(Kommune.id == kommune_id).first()
    if not kommune:
        raise HTTPException(404, "Kommune nicht gefunden")
    if not assessment_is_done(db, kommune_id):
        raise HTTPException(400, "Berechnung noch nicht abgeschlossen")

    job = GeoExportJob(
        kommune_id=kommune_id,
        export_type="geodaten",
        status=ExportStatus.PENDING,
        created_at=datetime.utcnow(),
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    run_geodata_export_background(job.id)
    return _job_to_dict(job)


@router.get("/kommune/{kommune_id}/exports/{export_id}/download")
def download_export(kommune_id: int, export_id: int, db: Session = Depends(get_db)):
    """Download a completed GeoPackage export."""
    job = (
        db.query(GeoExportJob)
        .filter(GeoExportJob.id == export_id, GeoExportJob.kommune_id == kommune_id)
        .first()
    )
    if not job:
        raise HTTPException(404, "Export nicht gefunden")
    if job.status != ExportStatus.DONE:
        raise HTTPException(400, "Export noch nicht abgeschlossen")
    if not job.file_path or not os.path.isfile(job.file_path):
        raise HTTPException(404, "Exportdatei nicht gefunden")

    # FileResponse streamt von Platte, statt die ganze .gpkg in den RAM zu lesen.
    return FileResponse(
        job.file_path,
        media_type="application/geopackage+sqlite3",
        filename=os.path.basename(job.file_path),
    )


@router.get("/kommune/{kommune_id}/measures/export")
def export_measures(kommune_id: int, db: Session = Depends(get_db)):
    """Export all measures as an Excel file."""
    xlsx_bytes = export_measures_xlsx(db, kommune_id)
    return Response(
        content=xlsx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=massnahmen_kommune_{kommune_id}.xlsx"},
    )


@router.post("/kommune/{kommune_id}/measures/import")
async def import_measures(
    kommune_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Import measures from an Excel file."""
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(400, "Nur Excel-Dateien (.xlsx) werden unterstützt")

    result = import_measures_xlsx(db, kommune_id, file.file)
    return result
