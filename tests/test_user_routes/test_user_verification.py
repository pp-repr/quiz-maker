import time
from app.utils.context import USER_VERIFY_ACCOUNT
from app.config.security import get_hash_password
from app.config.security import get_user_by_email
from tests.conftest import INCORRECT_TOKEN, UNREGISTERED_EMAIL


def test_user_account_verification(client, disabled_user, test_session):
    user_context = disabled_user.get_context(USER_VERIFY_ACCOUNT)
    token = get_hash_password(user_context)
    data = {
        "email": disabled_user.email,
        "token": token
    }
    response = client.post('/users/verify', json=data)
    assert response.status_code == 200
    activated_user = get_user_by_email(disabled_user.email, test_session)
    assert activated_user.is_active is True
    assert activated_user.verified_at is not None


def test_user_account_verification_with_invalid_token(client, disabled_user, test_session):
    data = {
        "email": disabled_user.email,
        "token": INCORRECT_TOKEN
    }
    response = client.post('/users/verify', json=data)
    assert response.status_code != 200
    activated_user = get_user_by_email(disabled_user.email, test_session)
    assert activated_user.is_active is False
    assert activated_user.verified_at is None


def test_user_account_verification_with_invalid_email(client, disabled_user, test_session):
    user_context = disabled_user.get_context(USER_VERIFY_ACCOUNT)
    token = get_hash_password(user_context)
    data = {
        "email": UNREGISTERED_EMAIL,
        "token": token
    }
    response = client.post('/users/verify', json=data)
    assert response.status_code != 200
    activated_user = get_user_by_email(disabled_user.email, test_session)
    assert activated_user.is_active is False
    assert activated_user.verified_at is None


def test_user_account_verification_twice(client, disabled_user, test_session):
    user_context = disabled_user.get_context(USER_VERIFY_ACCOUNT)
    token = get_hash_password(user_context)
    time.sleep(1)
    data = {
        "email": disabled_user.email,
        "token": token
    }
    response = client.post('/users/verify', json=data)
    assert response.status_code == 200
    response = client.post('/users/verify', json=data)
    assert response.status_code != 200