# app/schemas/deck.py
import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, field_validator

# --- Flashcard Schemas ---
class FlashcardBase(BaseModel):
    front: str
    back: str

    @field_validator('front', 'back')
    @classmethod
    def validate_non_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be empty or contain only whitespace")
        return v.strip()

class FlashcardCreate(FlashcardBase):
    pass

class FlashcardUpdate(BaseModel):
    front: Optional[str] = None
    back: Optional[str] = None

    @field_validator('front', 'back')
    @classmethod
    def validate_non_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip():
                raise ValueError("Field cannot be empty or contain only whitespace")
            return v.strip()
        return v

class FlashcardResponse(FlashcardBase):
    id: uuid.UUID
    deck_id: uuid.UUID
    next_review_date: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- Deck Schemas ---
class DeckBase(BaseModel):
    title: str
    description: Optional[str] = None

    @field_validator('title')
    @classmethod
    def validate_non_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty or contain only whitespace")
        return v.strip()

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

    @field_validator('text_content')
    @classmethod
    def validate_non_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Text content cannot be empty or contain only whitespace")
        return v.strip()

class RephraseRequest(FlashcardBase):
    pass

class RephraseResponse(FlashcardBase):
    pass