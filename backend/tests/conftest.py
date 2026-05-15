# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database

from app.main import app
from app.db.base_class import Base
from app.db.session import get_db
from app.core.config import settings

# 1. Setup a dedicated Test Database
TEST_SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI + "_test"

engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Create a clean test database once per test session."""
    if database_exists(TEST_SQLALCHEMY_DATABASE_URL):
        drop_database(TEST_SQLALCHEMY_DATABASE_URL)
    
    create_database(TEST_SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield
    # drop_database(TEST_SQLALCHEMY_DATABASE_URL) # Optional: keep it to inspect failures

@pytest.fixture
def db():
    """Provides a clean database session for every single test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db):
    """Provides a TestClient with a database dependency override."""
    def override_get_db():
        try:
            yield db
        finally:
            pass
            
    # This is the 'Magic': it swaps the real DB for the Test DB
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()