def test_borrow_and_return(client, auth_headers):
    # Create a book
    book = client.post("/books/", json={"title": "BorrowBook", "author": "A"}, headers=auth_headers).json()
    book_id = book["id"]

    # Borrow it
    resp = client.post(f"/borrow/{book_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "borrowed"

    # Try borrowing again - should fail
    resp2 = client.post(f"/borrow/{book_id}", headers=auth_headers)
    assert resp2.status_code == 400

    # Return it
    resp3 = client.post(f"/borrow/return/{book_id}", headers=auth_headers)
    assert resp3.status_code == 200


def test_borrow_unavailable_book(client, auth_headers):
    book = client.post("/books/", json={"title": "UnavailBook", "author": "A", "available": False}, headers=auth_headers).json()
    # Mark unavailable via update
    client.put(f"/books/{book['id']}", json={"available": False})
    # Wait, book starts available. Borrow once to make unavailable, then try again
    client.post(f"/borrow/{book['id']}", headers=auth_headers)
    resp = client.post(f"/borrow/{book['id']}", headers=auth_headers)
    assert resp.status_code == 400
