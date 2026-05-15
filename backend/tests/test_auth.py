# tests/test_auth.py
from app.core.config import settings

def test_register_user(client):
    """Test that the /register endpoint creates a user in the DB."""
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={"email": "tester@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "tester@example.com"
    assert "id" in data

def test_login_user(client):
    """Test that a registered user can get a JWT token."""
    # First, register the user
    email = "login_test@example.com"
    password = "password123"
    client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={"email": email, "password": password}
    )
    
    # Now, try to login
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": email, "password": password} # OAuth2 uses 'username'
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"