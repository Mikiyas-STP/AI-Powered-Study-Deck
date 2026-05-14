# app/api/flashcards.py
import uuid
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.flashcard import Flashcard
from app.models.deck import Deck
from app.api.deps import get_current_user
from app.models.user import User
from app.services.ai_service import ai_service
from app.schemas.deck import FlashcardResponse, AIRequest

router = APIRouter()

@router.post("/generate/{deck_id}", response_model=List[FlashcardResponse], status_code=status.HTTP_201_CREATED)
def generate_cards_from_text(
    deck_id: uuid.UUID,
    data: AIRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Takes raw text, 'processes' it via Mock AI, and saves cards to the DB.
    """
    # 1. Security Check: Does the deck exist and does the user own it?
    deck = db.query(Deck).filter(Deck.id == deck_id, Deck.user_id == current_user.id).first()
    if not deck:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Deck not found or you do not have permission to access it."
        )

    # 2. Call the AI Service (The Mock)
    generated_data = ai_service.generate_flashcards(data.text_content)

    # 3. Save to Database
    new_cards = []
    for item in generated_data:
        card = Flashcard(
            front=item["front"],
            back=item["back"],
            deck_id=deck_id
        )
        db.add(card)
        new_cards.append(card)
    
    db.commit()
    
    # Refresh to get the generated UUIDs and timestamps from Postgres
    for card in new_cards:
        db.refresh(card)

    return new_cards