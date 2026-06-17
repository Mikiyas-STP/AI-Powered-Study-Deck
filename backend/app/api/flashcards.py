# app/api/flashcards.py
import uuid
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.flashcard import Flashcard
from app.models.deck import Deck
from app.api.deps import get_current_user, get_current_deck
from app.models.user import User
from app.services.ai_services import ai_services
from app.schemas.deck import FlashcardResponse, AIRequest, FlashcardCreate, FlashcardUpdate,RephraseRequest,RephraseResponse,ClarifyRequest,ClarifyResponse

router = APIRouter()

@router.post("/rephrase", response_model=RephraseResponse)
def rephrase_card(data: RephraseRequest, current_user = Depends(get_current_user)) -> Any:
    try:
        refined = ai_services.rephrase_flashcard(data.front, data.back)
        return refined
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service unavailable"
        )

@router.post("/generate/{deck_id}", response_model=List[FlashcardResponse], status_code=status.HTTP_201_CREATED)
def generate_cards_from_text(
    data: AIRequest,
    deck: Deck = Depends(get_current_deck),
    db: Session = Depends(get_db)
) -> Any:
    """
    Takes raw text, 'processes' it via Mock AI, and saves cards to the DB.
    """
    try:
        generated_data = ai_services.generate_flashcards(data.text_content)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service unavailable"
        )

    new_cards = []
    for item in generated_data:
        existing_card = db.query(Flashcard).filter(
            Flashcard.deck_id == deck.id,
            func.lower(Flashcard.front) == func.lower(item["front"])
        ).first()
        
        if existing_card:
            continue

        card = Flashcard(
            front=item["front"],
            back=item["back"],
            deck_id=deck.id
        )
        db.add(card)
        new_cards.append(card)
    
    if new_cards:
        db.commit()
        # Refresh to get the generated UUIDs and timestamps from Postgres
        for card in new_cards:
            db.refresh(card)

    return new_cards

@router.post("/clarify", response_model=ClarifyResponse)
def clarify_card(data:ClarifyRequest,current_user = Depends(get_current_user)):
    try:
        clarification = ai_services.clarify_flashcard(data.front,data.back)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service unavailable"
        )
    return clarification

@router.post("/{deck_id}", response_model=FlashcardResponse, status_code=status.HTTP_201_CREATED)
def create_manual_card(
    card_in: FlashcardCreate,
    deck: Deck = Depends(get_current_deck),
    db: Session = Depends(get_db)
) -> Any:
    existing_card = db.query(Flashcard).filter(
        Flashcard.deck_id == deck.id,
        func.lower(Flashcard.front) == func.lower(card_in.front)
    ).first()
    
    if existing_card:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A flashcard with this front text already exists in this deck."
        )

    card = Flashcard(
        front=card_in.front,
        back=card_in.back,
        deck_id=deck.id
    )
    db.add(card)
    db.commit()
    db.refresh(card)
    return card

@router.put("/{card_id}", response_model=FlashcardResponse)
def update_card(
    card_id: uuid.UUID,
    card_in: FlashcardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Manually updates an existing flashcard if the user owns the deck it belongs to.
    """
    card = db.query(Flashcard).join(Deck).filter(
        Flashcard.id == card_id, 
        Deck.user_id == current_user.id
    ).first()
    
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flashcard not found or you do not have permission to edit it."
        )
    
    if card_in.front is not None:
        existing_card = db.query(Flashcard).filter(
            Flashcard.deck_id == card.deck_id,
            Flashcard.id != card.id,
            func.lower(Flashcard.front) == func.lower(card_in.front)
        ).first()
        if existing_card:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A flashcard with this front text already exists in this deck."
            )
        card.front = card_in.front
    if card_in.back is not None:
        card.back = card_in.back
        
    db.commit()
    db.refresh(card)
    return card

@router.delete("/{card_id}", response_model=FlashcardResponse)
def delete_card(
    card_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Deletes an existing flashcard if the user owns the deck it belongs to.
    """
    card = db.query(Flashcard).join(Deck).filter(
        Flashcard.id == card_id, 
        Deck.user_id == current_user.id
    ).first()
    
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flashcard not found or you do not have permission to delete it."
        )
    
    db.delete(card)
    db.commit()
    return card

