# app/schemas/deck.py
import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

# --- Flashcard Schemas ---
class FlashcardBase(BaseModel):
    front: str
    back: str

class FlashcardCreate(FlashcardBase):
    pass

class FlashcardUpdate(BaseModel):
    front: Optional[str] = None
    back: Optional[str] = None

class FlashcardResponse(FlashcardBase):
    id: uuid.UUID
    deck_id: uuid.UUID
    next_review_date: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- Deck Schemas ---
class DeckBase(BaseModel):
    title: str
    description: Optional[str] = None

class DeckCreate(DeckBase):
    pass

class DeckResponse(DeckBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    # We can even return the count of cards in the deck
    card_count: int = 0

    model_config = ConfigDict(from_attributes=True)

# This schema is for when we want to see a Deck AND all its cards
class DeckWithCards(DeckResponse):
    flashcards: List[FlashcardResponse] = []


class AIRequest(BaseModel):
    text_content: str

class RephraseRequest(BaseModel):
    front : str
    back : str
class RephraseResponse(BaseModel):
    front : str
    back : str