import sys
import os
from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.config.database import Base, get_session
from app.models.user import User

USER_NAME = "Jan Kowalski"
USER_EMAIL = "kowalski@gmail.com"
USER_PASSWORD = "haslo123"

engine = create_engine("sqlite:///./fastapi.db")
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def test_session() -> Generator:
    session = SessionTesting()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def app_test():
    Base.metadata.create_all(bind=engine)
    yield app
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(app_test, test_session):
    def _test_db():
        try:
            yield test_session
        finally:
            pass
    
    app_test.dependency_overrides[get_session] = _test_db
    return TestClient(app_test)
