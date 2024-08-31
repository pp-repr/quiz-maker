from app.models.enums import Role


def test_get_users_as_admin(auth_admin_client):
    response = auth_admin_client.get("/admin/users")
    assert response.status_code == 200


def test_get_users_as_user(auth_client):
    response = auth_client.get("/admin/users")
    assert response.status_code == 403


def test_get_user_by_id_as_admin(auth_admin_client, user):
    response = auth_admin_client.get(f"/admin/users/{user.id}")
    assert response.status_code == 200


def test_get_user_by_id_as_user(auth_client, user):
    response = auth_client.get(f"/admin/users/{user.id}")
    assert response.status_code == 403


def test_put_user_role_as_admin(auth_admin_client, user):
    params = {"role": Role.ADMIN.value}
    response = auth_admin_client.put(f"/admin/users/{user.id}/role", params=params)
    assert response.status_code == 200


def test_put_user_role_as_user(auth_client, user):
    params = {"role": Role.ADMIN.value}
    response = auth_client.put(f"/admin/users/{user.id}/role", params=params)
    assert response.status_code == 403
