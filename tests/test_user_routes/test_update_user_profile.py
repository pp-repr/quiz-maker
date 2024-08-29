from app.auth.user import create_token_payload
from tests.credentials import *


def test_update_user_profile(auth_client):
    update_data = {
        "name": NEW_NAME,
        "mobile": NEW_MOBILE,
        "description": NEW_DESCRIPTION
    }
    response = auth_client.patch(
        "/users/me/edit",
        json=update_data,
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == NEW_NAME
    assert response_data["mobile"] == NEW_MOBILE
    assert response_data["description"] == NEW_DESCRIPTION


def test_edit_user_profile(client, user_with_update_profile, test_session):
    data = create_token_payload(user_with_update_profile, test_session)
    header = {
        "Authorization": f"Bearer {data['access_token']}"
    }
    update_data = {
        "name": NEW_NAME,
        "mobile": NEW_MOBILE,
        "description": NEW_DESCRIPTION
    }
    response = client.patch(
        "/users/me/edit",
        json=update_data,
        headers=header
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == NEW_NAME
    assert response_data["mobile"] == NEW_MOBILE
    assert response_data["description"] == NEW_DESCRIPTION


def test_update_user_name(auth_client, user):
    update_data = {
        "name": NEW_NAME
    }
    response = auth_client.patch(
        "/users/me/edit",
        json=update_data,
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == NEW_NAME
    assert response_data["mobile"] == user.mobile
    assert response_data["description"] == user.description


def test_update_user_mobile(auth_client, user):
    update_data = {
        "mobile": NEW_MOBILE
    }
    response = auth_client.patch(
        "/users/me/edit",
        json=update_data,
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == user.name
    assert response_data["mobile"] == NEW_MOBILE
    assert response_data["description"] == user.description


def test_update_user_description(auth_client, user):
    update_data = {
        "description": NEW_DESCRIPTION
    }
    response = auth_client.patch(
        "/users/me/edit",
        json=update_data,
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == user.name
    assert response_data["mobile"] == user.mobile
    assert response_data["description"] == NEW_DESCRIPTION


def test_update_profile_unauthorized(client):
    update_data = {
        "name": NEW_NAME,
        "mobile": NEW_MOBILE,
        "description": NEW_DESCRIPTION
    }
    response = client.patch(
        "/users/me/edit",
        json=update_data,
    )
    assert response.status_code == 401
