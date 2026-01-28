from fastapi.testclient import TestClient

def test_get_users_me_unauthorized(client: TestClient):
    """Test that you cannot access /me without a token"""
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401

def test_get_users_me_authorized(client: TestClient):
    """Test that you CAN access /me with a valid token"""
    # 1. Create User
    username = "meuser"
    password = "strongpassword123"
    client.post(
        "/api/v1/users/signup",
        json={"username": username, "email": "me@example.com", "password": password},
    )
    
    # 2. Login to get token
    login_res = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password},
    )
    token = login_res.json()["access_token"]
    
    # 3. Access Route
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == username
