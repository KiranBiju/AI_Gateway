from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.dependencies import get_current_user
from app.services.api_key_service import create_api_key, get_api_keys
from app.schemas.api_key import ApiKeyResponse, ApiKeyListResponse

router = APIRouter(prefix="/api-keys", tags=["API Keys"])

@router.post("/create", response_model=ApiKeyResponse)
def create_key(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        key = create_api_key(current_user.id, db)

        return key

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/list", response_model=ApiKeyListResponse)
def list_keys(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        keys = get_api_keys(current_user.id, db)

        return {"api_keys": keys}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))