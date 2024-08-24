from app.auth.user import create_token_payload
from tests.credentials import INCORRECT_TOKEN



def test_refresh_token(client, user, test_session):
    data = create_token_payload(user, test_session)
    refresh_token = data['refresh_token']
    header = {
        "refresh-token": refresh_token
    }
    response = client.post("/auth/refresh", json={}, headers=header)
    assert response.status_code == 200
    assert 'access_token' in response.json()
    assert 'refresh_token' in response.json()


def test_refresh_token_with_invalid_token(client, user, test_session):
    create_token_payload(user, test_session)
    header = {
        "refresh-token": INCORRECT_TOKEN
    }
    response = client.post("/auth/refresh", json={}, headers=header)
    assert response.status_code == 400
    assert 'access_token' not in response.json()
    assert ' refresh_token' not in response.json()