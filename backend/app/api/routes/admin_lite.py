"""Admin: Deutschland-Batch triggern, überwachen, abbrechen."""
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.lite_models import LiteBatchRun
from app.tasks import lite_batch_task

router = APIRouter()


class LiteBatchRequest(BaseModel):
    bundesland: str | None = None
    force_zensus: bool = False


def _run_out(r: LiteBatchRun) -> dict:
    return {
        "id": r.id, "status": r.status, "phase": r.phase,
        "progress_pct": round(r.progress_pct or 0, 1),
        "processed": r.processed, "total": r.total,
        "message": r.message, "error_count": r.error_count,
        "params": r.params,
        "started_at": r.started_at.isoformat() if r.started_at else None,
        "finished_at": r.finished_at.isoformat() if r.finished_at else None,
    }


@router.post("/lite-batch")
def start_lite_batch(data: LiteBatchRequest, request: Request, db: Session = Depends(get_db)):
    # Nur ein aktiver Lauf zur Zeit.
    active = db.query(LiteBatchRun).filter(
        LiteBatchRun.status.in_(["pending", "running"])).first()
    if active:
        raise HTTPException(409, "Es läuft bereits ein Batch")
    user = get_current_user(request, db)
    run = LiteBatchRun(
        status="pending",
        params={"bundesland": data.bundesland, "force_zensus": data.force_zensus},
        created_by=user.id if user else None,
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    lite_batch_task.start_batch_thread(run.id)
    return _run_out(run)


@router.get("/lite-batch")
def list_lite_batches(db: Session = Depends(get_db)):
    runs = db.query(LiteBatchRun).order_by(LiteBatchRun.id.desc()).limit(20).all()
    return [_run_out(r) for r in runs]


@router.post("/lite-batch/{run_id}/abort")
def abort_lite_batch(run_id: int, db: Session = Depends(get_db)):
    run = db.query(LiteBatchRun).filter(LiteBatchRun.id == run_id).first()
    if not run:
        raise HTTPException(404, "Lauf nicht gefunden")
    ok = lite_batch_task.request_abort(run_id)
    return {"aborted": ok, "status": run.status}
