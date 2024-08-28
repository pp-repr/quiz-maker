from app.auth.user import create_token_payload


def test_admin(client, admin, test_session):
    data = create_token_payload(admin, test_session)
    header = {
        "Authorization": f"Bearer {data['access_token']}"
    }
    response = client.get("/admin/", headers=header)
    assert response.status_code == 200


def test_user(client, user, test_session):
    data = create_token_payload(user, test_session)
    header = {
        "Authorization": f"Bearer {data['access_token']}"
    }
    response = client.get("/admin/", headers=header)
    assert response.status_code == 403
