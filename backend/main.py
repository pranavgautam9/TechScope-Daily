from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn

from app.api.routes import news, facts, stocks, breaking_news, auth
from app.core.config import settings
from app.services.scheduler import start_breaking_news_scheduler
from app.models.database import SessionLocal, User
from app.core.security import get_password_hash

def create_test_user_if_not_exists():
    """Create test user if it doesn't exist"""
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == "testuser@gmail.com").first()
        if existing_user:
            print("Test user already exists!")
            return
        
        # Create test user
        test_user = User(
            email="testuser@gmail.com",
            first_name="Test",
            last_name="User",
            hashed_password=get_password_hash("Password123!")
        )
        
        db.add(test_user)
        db.commit()
        print("Test user created successfully!")
        print(f"Email: testuser@gmail.com")
        print(f"Password: Password123!")
    except Exception as e:
        db.rollback()
        print(f"Error creating test user: {e}")
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_test_user_if_not_exists()
    start_breaking_news_scheduler()
    yield
    # Shutdown
    pass

app = FastAPI(
    title="TechScope Daily API",
    description="AI-powered tech news and insights API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for frontend communication
# Supports GitHub Pages and other domains via BACKEND_CORS_ORIGINS environment variable
cors_origins = settings.get_cors_origins()
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(news.router, prefix="/api/news", tags=["news"])
app.include_router(facts.router, prefix="/api/facts", tags=["facts"])
app.include_router(stocks.router, prefix="/api/stocks", tags=["stocks"])
app.include_router(breaking_news.router, prefix="/api/breaking-news", tags=["breaking-news"])

@app.get("/")
async def root():
    return JSONResponse(
        status_code=200,
        content={
            "message": "TechScope Daily API",
            "version": "1.0.0",
            "status": "running"
        }
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 