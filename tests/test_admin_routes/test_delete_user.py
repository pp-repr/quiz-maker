
def test_delete_user_by_admin(auth_admin_client, user_to_delete):
    data = {"email": user_to_delete.email}
    response = auth_admin_client.request("DELETE", "/admin/delete-user", json=data)
    assert response.status_code == 200


def test_delete_user_by_user(auth_client, user_to_delete):
    data = {"email": user_to_delete.email}
    response = auth_client.request("DELETE", "/admin/delete-user", json=data)
    assert response.status_code == 403
