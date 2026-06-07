"""Admin endpoints (Zensus sync, maintenance)."""

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.zensus_loader import ZENSUS_DATASETS, ensure_zensus_datasets

router = APIRouter()


class ZensusSyncRequest(BaseModel):
    keys: Optional[list[str]] = None


@router.post("/zensus/sync")
def sync_zensus(body: ZensusSyncRequest = ZensusSyncRequest()):
    """Download/extract Zensus 2022 datasets (bbox CSVs cached locally)."""
    keys = body.keys
    if keys:
        unknown = [k for k in keys if k not in ZENSUS_DATASETS]
        if unknown:
            raise HTTPException(400, f"Unbekannte Keys: {', '.join(unknown)}")
    paths = ensure_zensus_datasets(keys)
    return {"datasets": keys or list(ZENSUS_DATASETS.keys()), "paths": paths}
