import sys
import os
from typing import Generator
from datetime import datetime, timezone

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
from app.models.enums import Role
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


def create_client(app, session, user=None):
    def test_db():
        try:
            yield session
        finally:
            pass
    app.dependency_overrides[get_session] = test_db
    client = TestClient(app)
    if user:
        data = create_token_payload(user, session)
        client.headers['Authorization'] = f"Bearer {data['access_token']}"
    return client


@pytest.fixture(scope="function")
def client(app_test, test_session):
    return create_client(app_test, test_session)


@pytest.fixture(scope="function")
def auth_client(app_test, test_session, user):
    return create_client(app_test, test_session, user)


@pytest.fixture(scope="function")
def auth_admin_client(app_test, test_session, admin):
    return create_client(app_test, test_session, admin)


def create_user(session, **kwargs):
    defaults = {
        'name': USER_NAME,
        'email': USER_EMAIL,
        'password': get_hash_password(USER_PASSWORD),
        'updated_at': datetime.now(timezone.utc),
        'verified_at': datetime.now(timezone.utc),
        'is_active': True,
        'role': Role.USER
    }
    user_data = {**defaults, **kwargs}
    user = User(**user_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(scope="function")
def disabled_user(test_session):
    return create_user(session=test_session, 
                        verified_at=None,
                        is_active=False)


@pytest.fixture(scope="function")
def user(test_session):
    return create_user(session=test_session)


@pytest.fixture(scope="function")
def admin(test_session):
    admin_password = get_hash_password(ADMIN_PASSWORD)
    return create_user(session=test_session,
                       name=ADMIN_NAME,
                       email=ADMIN_NAME,
                       password=admin_password,
                       role=Role.ADMIN)


@pytest.fixture(scope="function")
def unverified_user(test_session):
    return create_user(session=test_session,
                       verified_at=None)


@pytest.fixture(scope="function")
def user_with_update_profile(test_session):
    return create_user(session=test_session,
                       mobile=USER_MOBILE,
                       description=USER_DESCRIPTION)


@pytest.fixture(scope="function")
def user_to_delete(test_session):
    delete_password = get_hash_password(DELETE_PASSWORD)
    return create_user(session=test_session,
                       name=DELETE_NAME,
                       email=DELETE_EMAIL,
                       password=delete_password)
