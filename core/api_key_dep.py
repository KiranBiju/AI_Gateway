from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models


def get_api_key(
    x_api_key: str = Header(...),
    db: Session = Depends(get_db)
):
    key = db.query(models.ApiKey).filter_by(api_key=x_api_key).first()

    if not key:
        raise HTTPException(status_code=403, detail="Invalid API key")

    if not key.is_active:
        raise HTTPException(status_code=403, detail="API key revoked")

    return key