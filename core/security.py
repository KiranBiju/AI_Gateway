import os
import bcrypt
import jwt
import hashlib
import hmac
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import HTTPException, status

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 1

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set in .env")


def hash_password(password: str) -> str:
    """
    Hash user password using bcrypt
    """
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against bcrypt hash
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except Exception:
        return False


def hash_api_key(api_key: str) -> str:
    """
    Hash API key using SHA256
    """
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()


def verify_api_key(raw_key: str, stored_hash: str) -> bool:
    """
    Verify API key using constant-time comparison
    """
    if not raw_key or not stored_hash:
        return False

    computed_hash = hash_api_key(raw_key)
    return hmac.compare_digest(computed_hash, stored_hash)


def get_api_key_prefix(api_key: str) -> str:
    """
    Extract first 8 characters of API key
    """
    if not api_key or len(api_key) < 8:
        raise ValueError("Invalid API key format")
    return api_key[:8]


def create_access_token(data: dict) -> str:
    """
    Generate JWT token with expiry
    """
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        hours=ACCESS_TOKEN_EXPIRE_HOURS
    )

    to_encode.update({
        "exp": expire,
        "type": "access"
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    Decode JWT token and return payload
    Raises HTTP-friendly errors
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )