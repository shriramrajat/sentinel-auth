from fastapi.testclient import TestClient

def test_signup(client: TestClient):
    response = client.post(
        "/api/v1/users/signup",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "strongpassword123"
        },
    )
    assert response.status_code == 201
    content = response.json()
    assert content["email"] == "test@example.com"
    assert "id" in content

def test_login(client: TestClient):
    # Ensure user exists first
    client.post(
        "/api/v1/users/signup",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "strongpassword123"
        },
    )
    
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "loginuser",
            "password": "strongpassword123"
        },
    )
    assert response.status_code == 200
    content = response.json()
    assert "access_token" in content
    assert content["token_type"] == "bearer"
