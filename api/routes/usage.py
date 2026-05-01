from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.database import get_db
from app.db import models
from app.core.api_key_dep import get_api_key

router = APIRouter(prefix="/v1", tags=["Usage"])


@router.get("/usage")
def get_usage(
    api_key=Depends(get_api_key),
    db: Session = Depends(get_db)
):
    result = db.query(
        func.count(models.UsageLog.id),
        func.sum(models.UsageLog.total_tokens),
        func.sum(models.UsageLog.cost)
    ).filter(
        models.UsageLog.user_id == api_key.user_id
    ).first()

    return {
        "total_requests": result[0] or 0,
        "total_tokens": result[1] or 0,
        "total_cost": result[2] or 0
    }