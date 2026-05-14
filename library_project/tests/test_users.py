def test_list_users_admin(client, auth_headers):
    resp = client.get("/users/", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_list_users_unauthorized(client):
    resp = client.get("/users/")
    assert resp.status_code == 401
