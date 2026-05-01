from app.db.database import SessionLocal
from app.db import models


def log_usage(data: dict):
    db = SessionLocal()
    try:
        log = models.UsageLog(**data)
        db.add(log)
        db.commit()
    except Exception:
        pass
    finally:
        db.close()