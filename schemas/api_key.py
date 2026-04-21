from pydantic import BaseModel
from datetime import datetime
from typing import List


class ApiKeyResponse(BaseModel):
    api_key: str
    created_at: datetime

    class Config:
        from_attributes = True

class ApiKeyListResponse(BaseModel):
    api_keys: List[ApiKeyResponse]