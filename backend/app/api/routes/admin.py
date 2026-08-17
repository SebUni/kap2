"""Admin endpoints (Zensus sync, maintenance)."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import AssessmentStatus, ProjectStatus
from app.services.zensus_loader import ZENSUS_DATASETS, dataset_mtime, ensure_zensus_datasets
from app.tasks.assessment_task import TASK_KEY

router = APIRouter()


class ZensusSyncRequest(BaseModel):
    keys: Optional[list[str]] = None


@router.post("/zensus/sync")
def sync_zensus(body: ZensusSyncRequest = ZensusSyncRequest(), db: Session = Depends(get_db)):
    """Download/extract Zensus 2022 datasets (bbox CSVs cached locally).

    Haben sich Datensätze tatsächlich geändert (Datei-mtime), wird an allen
    abgeschlossenen Läufen ``recalc_recommended`` gesetzt: Die Zellwerte basieren
    dann auf alten Quelldaten. Eine Neuberechnung startet bewusst NIE automatisch
    (minutenlanger Lauf) — das Frontend zeigt den Hinweis über ``/status``.
    """
    keys = body.keys
    if keys:
        unknown = [k for k in keys if k not in ZENSUS_DATASETS]
        if unknown:
            raise HTTPException(400, f"Unbekannte Keys: {', '.join(unknown)}")
    effective = list(keys or ZENSUS_DATASETS.keys())
    before = {k: dataset_mtime(k) for k in effective}
    paths = ensure_zensus_datasets(keys)
    updated = [k for k in effective if dataset_mtime(k) != before[k]]
    if updated:
        db.query(ProjectStatus).filter(
            ProjectStatus.task_key == TASK_KEY,
            ProjectStatus.status == AssessmentStatus.DONE,
        ).update({ProjectStatus.recalc_recommended: True}, synchronize_session=False)
        db.commit()
    return {"datasets": effective, "paths": paths, "updated": updated}
