# i will create a reusable dependency for my routes here in deps.py
import uuid
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.models.deck import Deck

# This tells FastAPI where the client can get a token.
# It automatically hooks into the Swagger UI "Authorize" button!
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2)
) -> User:
    """
    Dependency to get the current authenticated user from the JWT token.
    Throws 401 Unauthorized if the token is invalid, expired, or user doesn't exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the JWT token
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        # Extract the user ID (subject) we stored in the token during login
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except (JWTError, ValidationError):
        raise credentials_exception
        
    # Fetch the user from the database
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise credentials_exception
        
    # Optional: Check if the user was deactivated after the token was issued
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    return user


def get_current_deck(
    deck_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Deck:
    deck = db.query(Deck).filter(Deck.id == deck_id, Deck.user_id == current_user.id).first()
    if not deck:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deck not found or you do not have permission to access it."
        )
    return deck