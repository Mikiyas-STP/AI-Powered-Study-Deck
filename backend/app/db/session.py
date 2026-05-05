# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# create_engine establishes the connection pool to PostgreSQL
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True, # Verifies connections are alive before using them
    pool_size=5,        # Standard connection pool size
    max_overflow=10
)

# SessionLocal will be used in our API dependencies to talk to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency generator to yield a database session per request.
    Ensures the session is closed after the request completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()