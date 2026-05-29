from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.export_service import export_measures_xlsx, import_measures_xlsx

router = APIRouter()


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
