from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import CheckLog

router = APIRouter(prefix="/api/logs", tags=["logs"])

@router.get("/{site_id}")
def site_logs(site_id: int, limit: int = 100, db: Session = Depends(get_db)):
    return (db.query(CheckLog)
              .filter(CheckLog.site_id == site_id)
              .order_by(CheckLog.id.desc()).limit(limit).all())
