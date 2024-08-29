import os


def test_update_profile_image(auth_client):
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'image.png')
    with open(file_path, 'rb') as image_file:
        image_content = image_file.read()
    files = {'file': ('image.png', image_content, 'image/png')}
    response = auth_client.put("/users/me/profile-image", files=files)
    assert response.status_code == 200
    assert response.json()["image_url"] is not None