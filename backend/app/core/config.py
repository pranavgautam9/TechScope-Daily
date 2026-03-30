from pathlib import Path
from typing import Optional
import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load .env before Settings() so DATABASE_URL, CORS, SECRET_KEY, etc. apply.
_backend_root = Path(__file__).resolve().parents[2]
load_dotenv(_backend_root / ".env")


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
    
    # CORS - Can be set via environment variable as comma-separated string
    # Example: BACKEND_CORS_ORIGINS=http://localhost:3000,https://username.github.io
    BACKEND_CORS_ORIGINS: Optional[str] = None
    
    def get_cors_origins(self):
        """Allowed browser origins. Merges BACKEND_CORS_ORIGINS with safe defaults.

        If the env var is set but parses to an empty list (e.g. commas only), defaults
        are used so production is not accidentally locked to no origins.
        """
        defaults = [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "https://pranavgautam.com",
            "https://www.pranavgautam.com",
        ]
        cors_env = os.getenv("BACKEND_CORS_ORIGINS") or self.BACKEND_CORS_ORIGINS
        if not cors_env or not str(cors_env).strip():
            return defaults
        extra = [
            origin.strip().rstrip("/")
            for origin in str(cors_env).split(",")
            if origin.strip()
        ]
        if not extra:
            return defaults
        seen = set()
        merged = []
        for origin in defaults + extra:
            if origin not in seen:
                seen.add(origin)
                merged.append(origin)
        return merged
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    class Config:
        env_file = str(_backend_root / ".env")
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()