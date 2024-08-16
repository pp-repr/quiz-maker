from tests.credentials import USER_PASSWORD, INCORRECT_PASSWORD, UNREGISTERED_EMAIL


def test_user_login(client, user):
    data = {
        'username': user.email,
        'password': USER_PASSWORD
    }
    response = client.post('/auth/login', data=data)
    assert response.status_code == 200
    assert response.json()['access_token'] is not None
    assert response.json()['refresh_token'] is not None
    assert response.json()['expires_in'] is not None


def test_user_login_with_invalid_password(client, user):
    data = {
        'username': user.email,
        'password': INCORRECT_PASSWORD
    }
    response = client.post('/auth/login', data=data)
    assert response.status_code == 400
    assert response.json()['detail'] == 'Invalid email or password'


def test_user_login_with_invalid_email(client):
    data = {
        'username': UNREGISTERED_EMAIL,
        'password': USER_PASSWORD
    }
    response = client.post('/auth/login', data=data)
    assert response.status_code == 400


def test_user_login_for_inactive_account(client, disabled_user):
    data = {
        'username': disabled_user.email,
        'password': USER_PASSWORD
    }
    response = client.post('/auth/login', data=data)
    assert response.status_code == 400


def test_user_login_for_unverified_account(client, unverified_user):
    data = {
        'username': unverified_user.email,
        'password': USER_PASSWORD
    }
    response = client.post('/auth/login', data=data)
    assert response.status_code == 400