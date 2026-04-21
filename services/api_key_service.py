import secrets
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.db import models
from typing import List, Dict


def generate_api_key() -> str:
    
    return secrets.token_urlsafe(32)


def create_api_key(user_id: int, db: Session) -> str:
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise ValueError("User does not exist")

    try:
        
        while True:
            key = generate_api_key()

            existing = (
                db.query(models.ApiKey)
                .filter(models.ApiKey.api_key == key)
                .first()
            )

            if not existing:
                break

        api_key_obj = models.ApiKey(
            user_id=user_id,
            api_key=key
        )

        db.add(api_key_obj)
        db.commit()
        db.refresh(api_key_obj)

        return api_key_obj

    except SQLAlchemyError:
        db.rollback()  
        raise Exception("Failed to create API key")


def get_api_keys(user_id: int, db: Session) -> List[Dict]:
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise ValueError("User does not exist")

    try:
        api_keys = (
            db.query(models.ApiKey)
            .filter(models.ApiKey.user_id == user_id)
            .order_by(models.ApiKey.created_at.desc())
            .all()
        )

        return [
            {
                "id": key.id,
                "api_key": key.api_key,
                "created_at": key.created_at,
            }
            for key in api_keys
        ]

    except SQLAlchemyError:
        raise Exception("Failed to fetch API keys")