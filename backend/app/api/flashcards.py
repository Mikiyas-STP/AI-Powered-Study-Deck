# app/api/flashcards.py
import uuid
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.flashcard import Flashcard
from app.models.deck import Deck
from app.api.deps import get_current_user
from app.models.user import User
from app.services.ai_service import ai_service
from app.schemas.deck import FlashcardResponse

router = APIRouter()

@router.post("/generate/{deck_id}", response_model=List[FlashcardResponse])
def generate_cards_from_text(
    deck_id: uuid.UUID,
    text_content: str, # In a real app, this would be in a Pydantic body
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Takes raw text, sends it to AI, and saves the resulting cards to the database.
    """
    # 1. Verify the deck exists and belongs to the user
    deck = db.query(Deck).filter(Deck.id == deck_id, Deck.user_id == current_user.id).first()
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")

    # 2. Call the AI Service
    generated_data = ai_service.generate_flashcards(text_content)

    # 3. Create Flashcard objects and save to DB
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
    
    # Refresh to get IDs and timestamps
    for card in new_cards:
        db.refresh(card)

    return new_cards