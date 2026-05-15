# backend/tests/test_decks.py
from app.core.config import settings

def test_create_deck_authenticated(client):
    """Test creating a deck with a valid JWT token."""
    # 1. Create a user and login to get a token
    email = "decktester@example.com"
    password = "password123"
    client.post(f"{settings.API_V1_STR}/auth/register", json={"email": email, "password": password})
    
    login_res = client.post(f"{settings.API_V1_STR}/auth/login", data={"username": email, "password": password})
    token = login_res.json()["access_token"]
    
    # 2. Use the token to create a deck
    response = client.post(
        f"{settings.API_V1_STR}/decks/",
        json={"title": "Test Deck", "description": "Testing protected routes"},
        headers={"Authorization": f"Bearer {token}"} # <--- This is the key!
    )
    
    assert response.status_code == 200
    assert response.json()["title"] == "Test Deck"

def test_create_deck_unauthorized(client):
    """Test that we CANNOT create a deck without a token."""
    response = client.post(
        f"{settings.API_V1_STR}/decks/",
        json={"title": "Hack Deck"}
    )
    assert response.status_code == 401 # Unauthorized