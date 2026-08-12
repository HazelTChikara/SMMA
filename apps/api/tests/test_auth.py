from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def test_register_authenticate_logout_and_login() -> None:
    email = f"auth-{uuid4().hex}@example.com"
    password = "a-secure-test-password"
    with TestClient(app) as client:
        register = client.post("/auth/register", json={"email": email, "full_name": "Test Owner", "password": password})
        assert register.status_code == 201
        assert register.json()["email"] == email
        assert register.cookies.get("smma_session")

        assert client.get("/auth/me").status_code == 200
        assert client.post("/auth/logout").status_code == 204
        assert client.get("/auth/me").status_code == 401

        failed = client.post("/auth/login", json={"email": email, "password": "wrong-password"})
        assert failed.status_code == 401
        login = client.post("/auth/login", json={"email": email, "password": password})
        assert login.status_code == 200
        assert client.get("/auth/me").json()["full_name"] == "Test Owner"


def test_registration_requires_a_strong_minimum_length() -> None:
    with TestClient(app) as client:
        response = client.post("/auth/register", json={"email": "owner@example.com", "full_name": "Owner", "password": "too-short"})
        assert response.status_code == 422
