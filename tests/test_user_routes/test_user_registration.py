from tests.conftest import USER_NAME, USER_EMAIL, USER_PASSWORD



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
        "email": "google.com",
        "password": USER_PASSWORD
    }
    response = client.post('/users', json=data)
    assert response.status_code != 201


def test_create_user_with_existing_email(client, user):
    data = {
        "name": USER_NAME,
        "email": user.email,
        "password": USER_PASSWORD
    }
    response = client.post('/users', json=data)
    assert response.status_code != 201


def test_create_user_with_empty_password(client):
    data = {
        "name": USER_NAME,
        "email": USER_EMAIL,
        "password": ""
    }
    response = client.post("/users/", json=data)
    assert response.status_code != 201


def test_create_user_with_numeric_password(client):
    data = {
        "name": USER_NAME,
        "email": USER_EMAIL,
        "password": "12345678"
    }
    response = client.post("/users/", json=data)
    assert response.status_code != 201


def test_create_user_with_char_password(client):
    data = {
        "name": USER_NAME,
        "email": USER_EMAIL,
        "password": "HaslohaslLo"
    }
    response = client.post("/users/", json=data)
    assert response.status_code != 201


def test_create_user_with_alphanumeric_password(client):
    data = {
        "name": USER_NAME,
        "email": USER_EMAIL,
        "password": "Haslo12343"
    }
    response = client.post("/users/", json=data)
    assert response.status_code != 201
