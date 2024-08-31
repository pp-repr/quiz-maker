
def test_delete_user_as_admin(auth_admin_client, user_to_delete):
    id = user_to_delete.id
    response = auth_admin_client.delete(f"/admin/users/delete/{id}")
    assert response.status_code == 200


def test_delete_user_as_user(auth_client, user_to_delete):
    id = user_to_delete.id
    response = auth_client.delete(f"/admin/users/delete/{id}")
    assert response.status_code == 403
