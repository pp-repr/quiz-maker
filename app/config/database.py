from app.config.settings import get_settings
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator
from sqlalchemy import create_engine


settings = get_settings()

engine = create_engine(settings.DATABASE_URL,
                        pool_pre_ping=True,
                        pool_recycle=3600,
                        pool_size=20,
                        max_overflow=0)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

from app.config.admin import create_admin_if_not_exists

def get_session() -> Generator:
    session = SessionLocal()
    try:
        create_admin_if_not_exists(session)
        yield session
    finally:
        session.close()
