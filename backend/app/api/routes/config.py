from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import ConfigParameter
from app.schemas.schemas import ConfigParameterOut, ConfigParameterUpdate

router = APIRouter()


@router.get("/kommune/{kommune_id}/config")
def get_config(kommune_id: int, category: str = None, db: Session = Depends(get_db)):
    """Get all configuration parameters for a municipality."""
    query = db.query(ConfigParameter).filter(ConfigParameter.kommune_id == kommune_id)
    if category:
        query = query.filter(ConfigParameter.category == category)
    params = query.order_by(ConfigParameter.category, ConfigParameter.key).all()

    return [
        {
            "id": p.id,
            "category": p.category,
            "key": p.key,
            "value": p.value,
            "description": p.description,
        }
        for p in params
    ]


@router.put("/kommune/{kommune_id}/config")
def update_config(
    kommune_id: int,
    updates: list[ConfigParameterUpdate],
    db: Session = Depends(get_db),
):
    """Update multiple configuration parameters at once."""
    results = []
    for u in updates:
        param = (
            db.query(ConfigParameter)
            .filter(
                ConfigParameter.kommune_id == kommune_id,
                ConfigParameter.category == u.category,
                ConfigParameter.key == u.key,
            )
            .first()
        )
        if param:
            param.value = u.value
            if u.description is not None:
                param.description = u.description
        else:
            param = ConfigParameter(
                kommune_id=kommune_id,
                category=u.category,
                key=u.key,
                value=u.value,
                description=u.description,
            )
            db.add(param)
        results.append({"category": u.category, "key": u.key, "status": "updated"})

    db.commit()
    return results
