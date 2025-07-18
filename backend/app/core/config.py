from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "TechScope Daily"
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = "sqlite:///./techscope_daily.db"
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = None
    
    # News API Configuration
    NEWS_API_KEY: Optional[str] = None
    
    # Stock API Configuration
    ALPHA_VANTAGE_API_KEY: Optional[str] = None
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Load environment variables from .env file if it exists
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv() 