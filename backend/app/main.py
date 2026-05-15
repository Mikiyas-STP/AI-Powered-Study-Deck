from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.decks import router as deck_router
from app.api.flashcards import router as flashcard_router
#import my auth runner from my register/login endpoint file(auth.py)
from app.api.auth import router as auth_router

from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions import sqlalchemy_exception_handler, general_exception_handler


def get_application() -> FastAPI:
    """
    Application factory pattern. 
    Useful for testing and keeping the global namespace clean.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        description="Production-ready backend for React frontend",
        version="1.0.0"
    )

    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.BACKEND_CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],  # Allows GET, POST, PUT, DELETE, OPTIONS
            allow_headers=["*"],  # Allows all headers (Authorization, Content-Type, etc.)
        )
    
    #i include the router here
    app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
    app.include_router(deck_router, prefix=f"{settings.API_V1_STR}/decks", tags=["Decks"])
    app.include_router(flashcard_router, prefix=f"{settings.API_V1_STR}/flashcards", tags=["Flashcards"])
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    return app

app = get_application()

@app.get("/health", tags=["System"])
async def health_check():
    """
    Basic health check endpoint for load balancers and deployment checks.
    """
    return {"status": "ok", "environment": settings.PROJECT_NAME}