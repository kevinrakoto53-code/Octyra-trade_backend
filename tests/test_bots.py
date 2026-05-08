from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def get_token():
    client.post("/api/auth/register", json={
        "email": "bottest@octyra.com",
        "password": "test1234",
    })
    response = client.post("/api/auth/login", data={
        "username": "bottest@octyra.com",
        "password": "test1234",
    })
    return response.json()["access_token"]


def test_create_bot():
    token = get_token()
    response = client.post("/api/bots/", json={
        "name": "Mon bot BTC",
        "asset": "BTC",
        "strategy": "ensemble",
        "interval": "5m",
        "email_alert": False
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["name"] == "Mon bot BTC"


def test_plan_limit():
    token = get_token()
    client.post("/api/bots/", json={
        "name": "Bot 1", "asset": "BTC",
        "strategy": "ensemble", "interval": "5m", "email_alert": False
    }, headers={"Authorization": f"Bearer {token}"})

    response = client.post("/api/bots/", json={
        "name": "Bot 2", "asset": "ETH",
        "strategy": "ensemble", "interval": "5m", "email_alert": False
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_get_bots():
    token = get_token()
    response = client.get("/api/bots/",
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)