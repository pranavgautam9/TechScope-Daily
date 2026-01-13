from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn

from app.api.routes import news, facts, stocks, breaking_news
from app.core.config import settings
from app.services.scheduler import start_breaking_news_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
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