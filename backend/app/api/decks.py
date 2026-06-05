# app/api/decks.py
from typing import List, Any
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.deck import Deck
from app.models.user import User
from app.schemas.deck import DeckCreate, DeckResponse, DeckWithCards
from app.api.deps import get_current_user, get_current_deck

router = APIRouter()

@router.post("/", response_model=DeckResponse)
def create_deck(
    deck_in: DeckCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Create a new study deck for the current user."""
    new_deck = Deck(
        title=deck_in.title,
        description=deck_in.description,
        user_id=current_user.id  # Ownership is assigned here!
    )
    db.add(new_deck)
    db.commit()
    db.refresh(new_deck)
    return new_deck

@router.get("/", response_model=List[DeckResponse])
def list_decks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Retrieve all decks belonging to the current user."""
    return db.query(Deck).filter(Deck.user_id == current_user.id).all()

@router.get("/{deck_id}", response_model=DeckWithCards)
def get_deck(
    deck: Deck = Depends(get_current_deck)
) -> Any:
    """Get a specific deck by ID, including its flashcards."""
    return deck