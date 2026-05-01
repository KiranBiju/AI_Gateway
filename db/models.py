from sqlalchemy import Boolean, Float, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users" 

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    api_keys = relationship("ApiKey", back_populates="user", cascade="all, delete-orphan")

class ApiKey(Base):
    __tablename__ = "api_keys" 

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    api_key = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="api_keys")

class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    api_key_id = Column(Integer)

    model = Column(String)
    provider = Column(String)

    input_tokens = Column(Integer)
    output_tokens = Column(Integer)
    total_tokens = Column(Integer)

    cost = Column(Float)
    latency = Column(Float)

    cache_hit = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())