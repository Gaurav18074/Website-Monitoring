from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Site(Base):
    __tablename__ = "sites"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    logs = relationship("CheckLog", back_populates="site", cascade="all, delete")

class CheckLog(Base):
    __tablename__ = "check_logs"
    id = Column(Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey("sites.id", ondelete="CASCADE"))
    status_code = Column(Integer)
    response_time_ms = Column(Float)
    is_up = Column(Boolean)
    error = Column(String, nullable=True)
    checked_at = Column(DateTime, default=datetime.utcnow, index=True)
    site = relationship("Site", back_populates="logs")
