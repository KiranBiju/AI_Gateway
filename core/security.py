import os
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 1

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set in .env")


#PASSWORD HASHING

def hash_password(password: str) -> str:
    """
    Convert plain password → hashed password
    """
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


#PASSWORD VERIFICATION

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compare plain password with hashed password
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except Exception:
        return False


#CREATE JWT TOKEN

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

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


#DECODE JWT TOKEN

def decode_access_token(token: str) -> dict:
    """
    Decode JWT token and return payload
    Raises HTTP-friendly errors
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")

    except jwt.InvalidTokenError:
        raise Exception("Invalid token")