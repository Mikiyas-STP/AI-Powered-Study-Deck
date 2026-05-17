#enviromental configurations with pydantic settings management
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "PAPR Portfolio API"
    API_V1_STR: str = "/api/v1"
    OPENAI_API_KEY: str = "your-key-here"
    # CORS Configuration for React
    # In production, this should be restricted to the  actual frontend domain
    BACKEND_CORS_ORIGINS: List[str] =["*"]
    
    # Database
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "portfolio_db"
    
    # JWT
    SECRET_KEY: str = "CHANGE_THIS_IN_PRODUCTION_TO_A_SECURE_RANDOM_STRING"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()