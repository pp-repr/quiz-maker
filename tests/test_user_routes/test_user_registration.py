from tests.conftest import USER_NAME, USER_EMAIL, USER_PASSWORD, INVALID_EMAIL, EMPTY_PASSWORD, NUMERIC_PASSWORD, CHAR_PASSWORD, ALPHANUMERIC_PASSWORD



def test_create_user(client):
    data = {
        "name": USER_NAME,
        "email": USER_EMAIL,
        "password": USER_PASSWORD
    }
    response = client.post('/users', json=data)
    assert response.status_code == 201
    assert "password" not in response.json()


def test_create_user_with_invalid_email(client):
    data = {
        "name": USER_NAME,
        "email": INVALID_EMAIL,
        "password": USER_PASSWORD
    }
    response = client.post('/users', json=data)
    assert response.status_code != 201


def test_create_user_with_existing_email(client, disabled_user):
    data = {
        "name": USER_NAME,
        "email": disabled_user.email,
        "password": USER_PASSWORD
    }
    response = client.post('/users', json=data)
    assert response.status_code != 201


def test_create_user_with_empty_password(client):
    data = {
        "name": USER_NAME,
        "email": USER_EMAIL,
        "password": EMPTY_PASSWORD
    }
    response = client.post("/users/", json=data)
    assert response.status_code != 201


def test_create_user_with_numeric_password(client):
    data = {
        "name": USER_NAME,
        "email": USER_EMAIL,
        "password": NUMERIC_PASSWORD
    }
    response = client.post("/users/", json=data)
    assert response.status_code != 201


def test_create_user_with_char_password(client):
    data = {
        "name": USER_NAME,
        "email": USER_EMAIL,
        "password": CHAR_PASSWORD
    }
    response = client.post("/users/", json=data)
    assert response.status_code != 201


def test_create_user_with_alphanumeric_password(client):
    data = {
        "name": USER_NAME,
        "email": USER_EMAIL,
        "password": ALPHANUMERIC_PASSWORD
    }
    response = client.post("/users/", json=data)
    assert response.status_code != 201
