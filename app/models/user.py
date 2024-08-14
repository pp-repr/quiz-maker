from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from datetime import datetime
from app.config.database import Base
from sqlalchemy.orm import mapped_column, relationship

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
    tokens = relationship("UserToken", back_populates="user")

    def get_context(self, context: str):
        return f"{context}{self.password[-6:]}{self.updated_at.strftime('%m%d%Y%H%M%S')}".strip()


class UserToken(Base):
    __tablename__ = "user_tokens"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(ForeignKey('users.id'))
    access_key = Column(String(250), nullable=True, index=True, default=None)
    refresh_key = Column(String(250), nullable=True, index=True, default=None)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    expires_at = Column(DateTime, nullable=False)
    
    user = relationship("User", back_populates="tokens")
