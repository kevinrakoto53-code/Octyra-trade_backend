from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def get_token():
    client.post("/api/auth/register", json={
        "email": "markettest@octyra.com",
        "password": "test1234",
    })
    response = client.post("/api/auth/login", data={
        "username": "markettest@octyra.com",
        "password": "test1234",
    })
    return response.json()["access_token"]


def test_get_prices():
    token = get_token()
    response = client.get("/api/market/prices",
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_single_price():
    token = get_token()
    response = client.get("/api/market/price/BTC",
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "price" in response.json()


def test_get_candles():
    token = get_token()
    response = client.get("/api/market/candles/BTC?period=5d&interval=1h",
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)