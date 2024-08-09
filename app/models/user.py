from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from datetime import datetime
from app.config.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), index=True)
    email = Column(String(40), unique=True, index=True)
    mobile = Column(String(20), index=True)
    password = Column(String(100))
    is_active = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True, default=None)
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    created_at = Column(DateTime, nullable=False, server_default=func.now())