# backend/tests/test_flashcards.py
from unittest.mock import patch
from app.core.config import settings
from app.models.flashcard import Flashcard

def _get_auth_token(client, email, password):
    client.post(f"{settings.API_V1_STR}/auth/register", json={"email": email, "password": password})
    login_res = client.post(f"{settings.API_V1_STR}/auth/login", data={"username": email, "password": password})
    return login_res.json()["access_token"]

def test_create_manual_flashcard_success(client, db):
    token = _get_auth_token(client, "user1@example.com", "pass123")
    headers = {"Authorization": f"Bearer {token}"}

    # Create Deck
    deck_res = client.post(
        f"{settings.API_V1_STR}/decks/",
        json={"title": "Math", "description": "Basic math"},
        headers=headers
    )
    deck_id = deck_res.json()["id"]

    # Create Card
    response = client.post(
        f"{settings.API_V1_STR}/flashcards/{deck_id}",
        json={"front": "1 + 1", "back": "2"},
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["front"] == "1 + 1"
    assert data["back"] == "2"

    # Verify in DB
    card_in_db = db.query(Flashcard).filter(Flashcard.id == data["id"]).first()
    assert card_in_db is not None

def test_create_flashcard_unauthorized_user(client):
    # Owner creates deck
    token1 = _get_auth_token(client, "owner@example.com", "owner123")
    deck_res = client.post(
        f"{settings.API_V1_STR}/decks/",
        json={"title": "Owner Deck"},
        headers={"Authorization": f"Bearer {token1}"}
    )
    deck_id = deck_res.json()["id"]

    # Unauthorized user tries to add card to owner's deck
    token2 = _get_auth_token(client, "hacker@example.com", "hack123")
    response = client.post(
        f"{settings.API_V1_STR}/flashcards/{deck_id}",
        json={"front": "Hack", "back": "No"},
        headers={"Authorization": f"Bearer {token2}"}
    )
    assert response.status_code == 404

def test_update_flashcard_success(client, db):
    token = _get_auth_token(client, "updater@example.com", "up123")
    headers = {"Authorization": f"Bearer {token}"}

    # Create Deck & Card
    deck_res = client.post(f"{settings.API_V1_STR}/decks/", json={"title": "Science"}, headers=headers)
    deck_id = deck_res.json()["id"]
    card_res = client.post(
        f"{settings.API_V1_STR}/flashcards/{deck_id}",
        json={"front": "Water", "back": "H2O"},
        headers=headers
    )
    card_id = card_res.json()["id"]

    # Update Front only
    response = client.put(
        f"{settings.API_V1_STR}/flashcards/{card_id}",
        json={"front": "Water chemical formula"},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["front"] == "Water chemical formula"
    assert response.json()["back"] == "H2O"

def test_delete_flashcard_success(client, db):
    token = _get_auth_token(client, "deleter@example.com", "del123")
    headers = {"Authorization": f"Bearer {token}"}

    # Create Deck & Card
    deck_res = client.post(f"{settings.API_V1_STR}/decks/", json={"title": "Delete me"}, headers=headers)
    deck_id = deck_res.json()["id"]
    card_res = client.post(
        f"{settings.API_V1_STR}/flashcards/{deck_id}",
        json={"front": "Delete Me", "back": "Yes"},
        headers=headers
    )
    card_id = card_res.json()["id"]

    # Delete Card
    response = client.delete(f"{settings.API_V1_STR}/flashcards/{card_id}", headers=headers)
    
    # We assert 200 here since your endpoint returns the deleted card
    assert response.status_code == 200
    assert response.json()["front"] == "Delete Me"

    # Verify card is gone from DB
    card_in_db = db.query(Flashcard).filter(Flashcard.id == card_id).first()
    assert card_in_db is None

def test_rephrase_flashcard_success(client):
    token = _get_auth_token(client, "rephrase_succ@example.com", "pass123")
    headers = {"Authorization": f"Bearer {token}"}
    
    with patch("app.api.flashcards.ai_services.rephrase_flashcard") as mock_rephrase:
        mock_rephrase.return_value = {"front": "Optimized Front", "back": "Optimized Back"}
        
        response = client.post(
            f"{settings.API_V1_STR}/flashcards/rephrase",
            json={"front": "original front", "back": "original back"},
            headers=headers
        )
        assert response.status_code == 200
        assert response.json()["front"] == "Optimized Front"
        assert response.json()["back"] == "Optimized Back"
        mock_rephrase.assert_called_once_with("original front", "original back")

def test_rephrase_flashcard_failure(client):
    token = _get_auth_token(client, "rephrase_fail@example.com", "pass123")
    headers = {"Authorization": f"Bearer {token}"}
    
    with patch("app.api.flashcards.ai_services.rephrase_flashcard") as mock_rephrase:
        mock_rephrase.side_effect = Exception("AI failure")
        
        response = client.post(
            f"{settings.API_V1_STR}/flashcards/rephrase",
            json={"front": "original front", "back": "original back"},
            headers=headers
        )
        assert response.status_code == 503
        assert response.json()["detail"] == "AI service unavailable"

def test_generate_flashcards_success(client, db):
    token = _get_auth_token(client, "gen_succ@example.com", "pass123")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create Deck
    deck_res = client.post(
        f"{settings.API_V1_STR}/decks/",
        json={"title": "Math", "description": "Basic math"},
        headers=headers
    )
    deck_id = deck_res.json()["id"]
    
    with patch("app.api.flashcards.ai_services.generate_flashcards") as mock_generate:
        mock_generate.return_value = [
            {"front": "Generated Front 1", "back": "Generated Back 1"},
            {"front": "Generated Front 2", "back": "Generated Back 2"}
        ]
        
        response = client.post(
            f"{settings.API_V1_STR}/flashcards/generate/{deck_id}",
            json={"text_content": "some text"},
            headers=headers
        )
        assert response.status_code == 201
        assert len(response.json()) == 2
        assert response.json()[0]["front"] == "Generated Front 1"
        assert response.json()[1]["back"] == "Generated Back 2"

def test_generate_flashcards_failure(client):
    token = _get_auth_token(client, "gen_fail@example.com", "pass123")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create Deck
    deck_res = client.post(
        f"{settings.API_V1_STR}/decks/",
        json={"title": "Math", "description": "Basic math"},
        headers=headers
    )
    deck_id = deck_res.json()["id"]
    
    with patch("app.api.flashcards.ai_services.generate_flashcards") as mock_generate:
        mock_generate.side_effect = Exception("AI failure")
        
        response = client.post(
            f"{settings.API_V1_STR}/flashcards/generate/{deck_id}",
            json={"text_content": "some text"},
            headers=headers
        )
        assert response.status_code == 503
        assert response.json()["detail"] == "AI service unavailable"

def test_create_flashcard_empty_fields_fail(client):
    token = _get_auth_token(client, "empty_fail@example.com", "pass123")
    headers = {"Authorization": f"Bearer {token}"}
    
    deck_res = client.post(
        f"{settings.API_V1_STR}/decks/",
        json={"title": "Math", "description": "Basic math"},
        headers=headers
    )
    deck_id = deck_res.json()["id"]

    res1 = client.post(
        f"{settings.API_V1_STR}/flashcards/{deck_id}",
        json={"front": "   ", "back": "Valid Back"},
        headers=headers
    )
    assert res1.status_code == 422

    res2 = client.post(
        f"{settings.API_V1_STR}/flashcards/{deck_id}",
        json={"front": "Valid Front", "back": ""},
        headers=headers
    )
    assert res2.status_code == 422

def test_update_flashcard_empty_fields_fail(client, db):
    token = _get_auth_token(client, "update_empty_fail@example.com", "pass123")
    headers = {"Authorization": f"Bearer {token}"}
    
    deck_res = client.post(f"{settings.API_V1_STR}/decks/", json={"title": "Science"}, headers=headers)
    deck_id = deck_res.json()["id"]
    card_res = client.post(
        f"{settings.API_V1_STR}/flashcards/{deck_id}",
        json={"front": "Water", "back": "H2O"},
        headers=headers
    )
    card_id = card_res.json()["id"]
    res = client.put(
        f"{settings.API_V1_STR}/flashcards/{card_id}",
        json={"front": "  "},
        headers=headers
    )
    assert res.status_code == 422
