import pytest
pytestmark = pytest.mark.integration

def test_create_user_and_get(client):
    r = client.post("/users", json={"email":"Demo@Example.com", "full_name":"Demo"})
    assert r.status_code == 201, r.text
    user = r.json()
    assert user["email"] == "demo@example.com"

    r2 = client.get(f"/users/{user['id']}")
    assert r2.status_code == 200
    assert r2.json()["id"] == user["id"]

def test_create_user_duplicate_email(client):
    r1 = client.post("/users", json={"email":"a@b.com", "full_name":"A"})
    assert r1.status_code == 201
    r2 = client.post("/users", json={"email":"A@B.COM", "full_name":"B"})
    assert r2.status_code == 409
