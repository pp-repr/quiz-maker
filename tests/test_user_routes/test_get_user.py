from app.auth.user import create_token_payload
from tests.credentials import INCORRECT_TOKEN


def test_get_user(client, user, test_session):
    data = create_token_payload(user, test_session)
    header = {
        "Authorization": f"Bearer {data['access_token']}"
    }
    response = client.get("/users/me", headers=header)
    assert response.status_code == 200
    assert response.json()['email'] == user.email


def test_get_user_with_incorrect_token(client, user, test_session):
    create_token_payload(user, test_session)
    header = {
        "Authorization": f"Bearer {INCORRECT_TOKEN}"
    }
    response = client.get("/users/me", headers=header)
    assert response.status_code == 401
    assert 'email' not in response.json()
    assert 'id' not in response.json()


def test_get_user_details_by_email(auth_client, user):
    response = auth_client.get(f"/users/{user.id}")
    assert response.status_code == 200