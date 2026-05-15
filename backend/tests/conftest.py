# backend/tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database

# Import your app components
from app.main import app
from app.db.base_class import Base
from app.db.session import get_db
from app.core.config import settings

# 1. Setup a dedicated Test Database (e.g., portfolio_db_test)
TEST_SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI + "_test"

engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """
    Create a clean test database once per test session.
    'autouse=True' means this runs automatically when you start pytest.
    """
    if database_exists(TEST_SQLALCHEMY_DATABASE_URL):
        drop_database(TEST_SQLALCHEMY_DATABASE_URL)
    
    create_database(TEST_SQLALCHEMY_DATABASE_URL)
    
    # Create all tables (User, Deck, Flashcard) in the test DB
    Base.metadata.create_all(bind=engine)
    
    yield # This is where the tests happen
    
    # Optional: drop_database(TEST_SQLALCHEMY_DATABASE_URL)

@pytest.fixture
def db():
    """
    Provides a clean database session for every single test.
    Rolls back changes after each test so tests don't interfere with each other.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db):
    """
    Provides a TestClient with a database dependency override.
    This ensures the API uses the Test DB instead of the Production DB.
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass
            
    # Swap the real get_db for our test version
    app.dependency_overrides[get_db] = override_get_db
    
    # Standard FastAPI TestClient usage
    with TestClient(app) as c:
        yield c
        
    # Clean up the override after the test is done
    app.dependency_overrides.clear()