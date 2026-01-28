import pytest
pytestmark = pytest.mark.integration

def _create_user(client):
    r = client.post("/users", json={"email":"buyer@example.com", "full_name":"Buyer"})
    assert r.status_code == 201, r.text
    return r.json()["id"]

def test_create_order_and_pay(client):
    user_id = _create_user(client)
    payload = {
        "user_id": user_id,
        "discount_code": "OFF10",
        "items": [
            {"sku": "SKU1", "qty": 2, "unit_price": 50000},
            {"sku": "SKU2", "qty": 1, "unit_price": 80000},
        ]
    }
    r = client.post("/orders", json=payload)
    assert r.status_code == 201, r.text
    order = r.json()
    assert order["status"] == "CREATED"
    assert order["subtotal"] == 180000
    assert order["discount"] == 18000
    assert order["total"] == 162000
    assert len(order["items"]) == 2

    r2 = client.get(f"/orders/{order['id']}")
    assert r2.status_code == 200
    assert r2.json()["id"] == order["id"]

    r3 = client.post(f"/orders/{order['id']}/pay")
    assert r3.status_code == 200
    assert r3.json()["status"] == "PAID"

    r4 = client.post(f"/orders/{order['id']}/pay")
    assert r4.status_code == 409
