from sqlalchemy.orm import Session
from app.db import models
from app.core.security import hash_password, verify_password, create_access_token

def create_user(db: Session, email: str, password: str):
    # check if user exists
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        raise Exception("Email already registered")

    hashed_pw = hash_password(password)

    user = models.User(
        email=email,
        hashed_password=hashed_pw
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    token = create_access_token({"user_id": user.id})

    return token