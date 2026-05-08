from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_register():
    response = client.post("/api/auth/register", json={
        "email": "test@octyra.com",
        "password": "test1234",
        "full_name": "Test User"
    })
    assert response.status_code in [200, 400]


def test_login_success():
    client.post("/api/auth/register", json={
        "email": "testlogin@octyra.com",
        "password": "test1234",
    })
    response = client.post("/api/auth/login", data={
        "username": "testlogin@octyra.com",
        "password": "test1234",
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password():
    response = client.post("/api/auth/login", data={
        "username": "testlogin@octyra.com",
        "password": "wrongpassword",
    })
    assert response.status_code == 401


def test_get_me_without_token():
    response = client.get("/api/users/me")
    assert response.status_code == 401