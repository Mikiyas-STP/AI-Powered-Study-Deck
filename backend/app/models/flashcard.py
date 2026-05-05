import uuid
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, Text, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Flashcard(Base):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    deck_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("deck.id", ondelete="CASCADE"), nullable=False)
    
    # Core Content
    front: Mapped[str] = mapped_column(Text, nullable=False)
    back: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Spaced Repetition System (SRS) Fields - The "Wow" Factor
    next_review_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    ease_factor: Mapped[float] = mapped_column(Float, default=2.5) # Standard SuperMemo-2 starting ease
    interval: Mapped[int] = mapped_column(Integer, default=0)      # Days until next review
    repetitions: Mapped[int] = mapped_column(Integer, default=0)   # Consecutive correct answers
    
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Relationships
    deck = relationship("Deck", back_populates="flashcards")