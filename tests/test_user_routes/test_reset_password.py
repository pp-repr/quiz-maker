from app.auth.utils import get_hash_password
from app.utils.context import FORGOT_PASSWORD
from tests.credentials import NEW_PASSWORD, INCORRECT_TOKEN, INVALID_EMAIL, UNREGISTERED_EMAIL


def get_token(user):
    string_context = user.get_context(FORGOT_PASSWORD)
    return get_hash_password(string_context)


def test_reset_password(client, user):
    data = {
        "token": get_token(user),
        "email": user.email,
        "password": NEW_PASSWORD
    }
    response = client.put("/auth/reset-password", json=data)
    assert response.status_code == 200
    del data['token']
    del data['email']
    data['username'] = user.email
    login_resp = client.post("/auth/login", data=data)
    assert login_resp.status_code == 200
    

def test_reset_password_invalid_token(client, user):
    data = {
        "token": INCORRECT_TOKEN,
        "email": user.email,
        "password": NEW_PASSWORD
    }
    response = client.put("/auth/reset-password", json=data)
    assert response.status_code == 400
    del data['token']
    del data['email']
    data['username'] = user.email
    login_resp = client.post("/auth/login", data=data)
    assert login_resp.status_code != 200
    

def test_reset_password_invalid_email(client, user):
    data = {
        "token": get_token(user),
        "email": INVALID_EMAIL,
        "password": NEW_PASSWORD
    }
    response = client.put("/auth/reset-password", json=data)
    assert response.status_code == 422
    del data['token']
    del data['email']
    data['username'] = user.email
    login_resp = client.post("/auth/login", data=data)
    assert login_resp.status_code != 200
    

def test_reset_password_unregistered_email(client, user):
    data = {
        "token": get_token(user),
        "email": UNREGISTERED_EMAIL,
        "password": NEW_PASSWORD
    }
    response = client.put("/auth/reset-password", json=data)
    assert response.status_code == 400
    del data['token']
    del data['email']
    data['username'] = user.email
    login_resp = client.post("/auth/login", data=data)
    assert login_resp.status_code != 200
