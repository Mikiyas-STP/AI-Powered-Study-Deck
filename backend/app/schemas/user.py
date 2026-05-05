#here i de
# app/schemas/user.py
import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

# Shared properties
class UserBase(BaseModel):
    email: EmailStr  # Automatically validates that the string is a valid email format

# Properties to receive via API on creation (React -> FastAPI)
class UserCreate(UserBase):
    password: str

# Properties to return to client (FastAPI -> React)
class UserResponse(UserBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    
    # This is crucial! It tells Pydantic to read data from SQLAlchemy ORM models,
    # not just standard Python dictionaries.
    model_config = ConfigDict(from_attributes=True)

# Schema for the JWT Token response
class Token(BaseModel):
    access_token: str
    token_type: str