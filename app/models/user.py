from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Enum
from datetime import datetime
from sqlalchemy.orm import mapped_column, relationship

from app.config.database import Base
from app.models.enums import Role


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    email = Column(String(100), unique=True, index=True)
    mobile = Column(String(9), index=True)
    description = Column(String(1000))
    image_url = Column(String(1000), nullable=True)
    password = Column(String(100))
    is_active = Column(Boolean, default=False)
    role = Column(Enum(Role), default=Role.USER, nullable=False)
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
    token = Column(String(250), nullable=True, index=True, default=None)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    expires_at = Column(DateTime, nullable=False)
    
    user = relationship("User", back_populates="tokens")
