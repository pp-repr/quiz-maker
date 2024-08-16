
def test_forgot_password_request(client, user):
    data = {'email': user.email}
    response = client.post('/auth/forgot-password', json=data)
    assert response.status_code == 200


def test_forgot_password_request_with_invalid_email(client, user):
    data = {'email': 'invalid_email'}
    response = client.post('/auth/forgot-password', json=data)
    assert response.status_code == 422


def test__forgot_password_request_for_unverified_user(client, unverified_user):
    data = {'email': unverified_user.email}
    response = client.post('/auth/forgot-password', json=data)
    assert response.status_code == 400


def test_forgot_password_request_for_disabled_user(client, disabled_user):
    data = {'email': disabled_user.email}
    response = client.post('/auth/forgot-password', json=data)
    assert response.status_code == 400