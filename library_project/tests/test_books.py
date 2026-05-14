def test_create_book(client, auth_headers):
    resp = client.post("/books/", json={"title": "Clean Code", "author": "Robert C. Martin"}, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["title"] == "Clean Code"


def test_get_books(client):
    resp = client.get("/books/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_get_book_not_found(client):
    resp = client.get("/books/99999")
    assert resp.status_code == 404


def test_update_book(client, auth_headers):
    create = client.post("/books/", json={"title": "OldTitle", "author": "Author"}, headers=auth_headers)
    book_id = create.json()["id"]
    resp = client.put(f"/books/{book_id}", json={"title": "NewTitle"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "NewTitle"


def test_delete_book(client, auth_headers):
    create = client.post("/books/", json={"title": "ToDelete", "author": "Author"}, headers=auth_headers)
    book_id = create.json()["id"]
    resp = client.delete(f"/books/{book_id}")
    assert resp.status_code == 200
