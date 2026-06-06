"""Hintergrund-Export von Geodaten als GeoPackage."""

import logging
import threading
import traceback
from datetime import datetime

from app.db.database import SessionLocal
from app.models.models import GeoExportJob, ExportStatus
from app.services.geodata_export_service import build_geopackage

log = logging.getLogger(__name__)


def run_geodata_export_background(export_id: int):
    """Startet einen Hintergrund-Thread für den GeoPackage-Export."""
    thread = threading.Thread(
        target=_run_export, args=(export_id,), daemon=True,
    )
    thread.start()
    log.info("[EXPORT] Export-Thread gestartet für export_id=%s", export_id)


def _run_export(export_id: int):
    db = SessionLocal()
    try:
        job = db.query(GeoExportJob).filter(GeoExportJob.id == export_id).first()
        if not job:
            log.error("[EXPORT] Job %s nicht gefunden", export_id)
            return

        job.status = ExportStatus.RUNNING
        db.commit()

        file_path = build_geopackage(db, job.kommune_id, export_id)

        job = db.query(GeoExportJob).filter(GeoExportJob.id == export_id).first()
        job.status = ExportStatus.DONE
        job.file_path = file_path
        job.finished_at = datetime.utcnow()
        job.error_message = None
        db.commit()
        log.info("[EXPORT] Job %s abgeschlossen: %s", export_id, file_path)

    except Exception as exc:
        log.error("[EXPORT] Job %s fehlgeschlagen: %s\n%s", export_id, exc, traceback.format_exc())
        try:
            job = db.query(GeoExportJob).filter(GeoExportJob.id == export_id).first()
            if job:
                job.status = ExportStatus.ERROR
                job.error_message = str(exc)
                job.finished_at = datetime.utcnow()
                db.commit()
        except Exception:
            db.rollback()
    finally:
        db.close()
