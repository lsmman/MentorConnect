import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_signup_and_login():
    # 회원가입
    res = client.post("/api/signup", json={
        "email": "testuser@example.com",
        "password": "testpass123",
        "name": "테스트유저",
        "role": "mentee"
    })
    assert res.status_code == 201 or res.status_code == 400
    # 로그인
    res = client.post("/api/login", json={
        "email": "testuser@example.com",
        "password": "testpass123"
    })
    assert res.status_code == 200
    assert "token" in res.json()
