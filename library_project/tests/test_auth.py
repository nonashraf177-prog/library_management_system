def test_register(client):
    resp = client.post("/auth/register", json={"username": "user1", "password": "pass"})
    assert resp.status_code == 200
    assert resp.json()["username"] == "user1"


def test_register_duplicate(client):
    client.post("/auth/register", json={"username": "dup", "password": "pass"})
    resp = client.post("/auth/register", json={"username": "dup", "password": "pass"})
    assert resp.status_code == 400


def test_login(client):
    client.post("/auth/register", json={"username": "loginuser", "password": "mypass"})
    resp = client.post("/auth/login", json={"username": "loginuser", "password": "mypass"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_wrong_password(client):
    client.post("/auth/register", json={"username": "wrongpass", "password": "correct"})
    resp = client.post("/auth/login", json={"username": "wrongpass", "password": "wrong"})
    assert resp.status_code == 401
