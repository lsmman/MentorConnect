from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_sql_injection():
    # SQL Injection 시도
    res = client.post("/api/login", json={"email": "' OR 1=1 --", "password": "any"})
    assert res.status_code == 401 or res.status_code == 400

def test_xss_sanitize():
    # XSS 시도
    token = client.post("/api/login", json={"email": "mentor@example.com", "password": "mentorpass"}).json()["token"]
    res = client.put(
        "/api/profile",
        headers={"Authorization": f"Bearer {token}"},
        json={"id": 1, "name": "<script>alert(1)</script>", "role": "mentor", "bio": "<img src=x onerror=alert(1)>", "image": "", "skills": ["React"]}
    )
    assert res.status_code == 200
    data = res.json()
    assert "<" not in data["profile"]["name"]
    assert "<" not in data["profile"]["bio"]
