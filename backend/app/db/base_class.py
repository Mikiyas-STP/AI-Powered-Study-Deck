# Instead of manually naming every single database table, a great mid-level trick is to create a custom Base class that automatically generates table names based on your Python class names (e.g., UserModel becomes user).
# app/db/base_class.py
from typing import Any
from sqlalchemy.orm import DeclarativeBase, declared_attr

class Base(DeclarativeBase):
    id: Any
    __name__: str
    
    # Generate __tablename__ automatically
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()