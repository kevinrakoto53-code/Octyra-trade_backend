from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def get_token():
    client.post("/api/auth/register", json={
        "email": "signaltest@octyra.com",
        "password": "test1234",
    })
    response = client.post("/api/auth/login", data={
        "username": "signaltest@octyra.com",
        "password": "test1234",
    })
    return response.json()["access_token"]


def test_get_signal_btc():
    token = get_token()
    response = client.get("/api/signals/BTC",
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert "final_decision" in data
    assert data["final_decision"] in ["BUY", "SELL", "HOLD"]


def test_get_all_signals():
    token = get_token()
    response = client.get("/api/signals/",
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)