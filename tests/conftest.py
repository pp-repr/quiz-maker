import sys
import os
from typing import Generator
import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.config.database import Base, get_session
from app.models.user import User
from app.auth.user import create_token_payload
from app.auth.utils import get_hash_password
from tests.credentials import *


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
    def test_db():
        try:
            yield test_session
        finally:
            pass
    
    app_test.dependency_overrides[get_session] = test_db
    return TestClient(app_test)


@pytest.fixture(scope="function")
def disabled_user(test_session):
    model = User()
    model.name = USER_NAME
    model.email = USER_EMAIL
    model.password = get_hash_password(USER_PASSWORD)
    model.updated_at = datetime.datetime.now(datetime.timezone.utc)
    model.is_active = False
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model


@pytest.fixture(scope="function")
def user(test_session):
    model = User()
    model.name = USER_NAME
    model.email = USER_EMAIL
    model.password = get_hash_password(USER_PASSWORD)
    model.updated_at = datetime.datetime.now(datetime.timezone.utc)
    model.verified_at = datetime.datetime.now(datetime.timezone.utc)
    model.is_active = True
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model


@pytest.fixture(scope="function")
def unverified_user(test_session):
    model = User()
    model.name = USER_NAME
    model.email = USER_EMAIL
    model.password = get_hash_password(USER_PASSWORD)
    model.updated_at = datetime.datetime.now(datetime.timezone.utc)
    model.is_active = True
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model


@pytest.fixture(scope="function")
def auth_client(app_test, test_session, user):
    def test_db():
        try:
            yield test_session
        finally:
            pass

    app_test.dependency_overrides[get_session] = test_db
    data = create_token_payload(user, test_session)
    client = TestClient(app_test)
    client.headers['Authorization'] = f"Bearer {data['access_token']}"
    return client
