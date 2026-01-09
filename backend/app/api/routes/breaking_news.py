from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import requests
import json
from bs4 import BeautifulSoup
import asyncio
import aiohttp

from app.models.database import get_db, BreakingNews
from app.ai.content_generator import AIContentGenerator
from app.services.breaking_news_service import BreakingNewsService

router = APIRouter()
ai_generator = AIContentGenerator()
breaking_news_service = BreakingNewsService()

@router.get("/")
async def get_breaking_news(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get breaking news items"""
    try:
        news_items = breaking_news_service.get_breaking_news(db, limit=limit)
        return {
            "success": True,
            "data": news_items,
            "count": len(news_items)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/latest")
async def get_latest_breaking_news(db: Session = Depends(get_db)):
    """Get the most recent breaking news (last 24 hours)"""
    try:
        latest_news = breaking_news_service.get_latest_breaking_news(db, hours=24)
        return {
            "success": True,
            "data": latest_news
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/fetch-google-news")
async def fetch_google_news(db: Session = Depends(get_db)):
    """Fetch breaking news from Google News"""
    try:
        news_items = await breaking_news_service.fetch_google_news(db)
        return {
            "success": True,
            "message": f"Fetched {len(news_items)} breaking news items",
            "data": news_items
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/fetch-wired-news")
async def fetch_wired_news(db: Session = Depends(get_db)):
    """Fetch breaking news from Wired.com"""
    try:
        news_items = await breaking_news_service.fetch_wired_news(db)
        return {
            "success": True,
            "message": f"Fetched {len(news_items)} breaking news items from Wired.com",
            "data": news_items
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-importance")
async def analyze_breaking_news_importance(
    news_id: int,
    db: Session = Depends(get_db)
):
    """Analyze the importance of breaking news using AI"""
    try:
        news_item = db.query(BreakingNews).filter(BreakingNews.id == news_id).first()
        if not news_item:
            raise HTTPException(status_code=404, detail="Breaking news not found")
        
        # Analyze importance using AI
        importance_analysis = await ai_generator.analyze_breaking_news_importance(
            news_item.title, 
            news_item.content
        )
        
        # Update the news item
        news_item.importance_score = importance_analysis.get("importance_score", 0.5)
        news_item.is_critical = importance_analysis.get("is_critical", False)
        news_item.ai_analysis = importance_analysis.get("reason", "")
        
        db.commit()
        
        return {
            "success": True,
            "data": {
                "id": news_item.id,
                "title": news_item.title,
                "importance_score": news_item.importance_score,
                "is_critical": news_item.is_critical,
                "ai_analysis": news_item.ai_analysis
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/critical")
async def get_critical_breaking_news(db: Session = Depends(get_db)):
    """Get critical breaking news items"""
    try:
        critical_news = db.query(BreakingNews).filter(
            BreakingNews.is_critical == True
        ).order_by(BreakingNews.importance_score.desc()).limit(5).all()
        
        return {
            "success": True,
            "data": [
                {
                    "id": item.id,
                    "title": item.title,
                    "content": item.content,
                    "source": item.source,
                    "url": item.url,
                    "importance_score": item.importance_score,
                    "published_at": item.published_at,
                    "ai_analysis": item.ai_analysis
                }
                for item in critical_news
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trending")
async def get_trending_breaking_news(db: Session = Depends(get_db)):
    """Get trending breaking news based on importance and recency"""
    try:
        trending_news = breaking_news_service.get_trending_news(db, limit=10)
        return {
            "success": True,
            "data": trending_news
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{news_id}")
async def delete_breaking_news(news_id: int, db: Session = Depends(get_db)):
    """Delete a breaking news item"""
    try:
        news_item = db.query(BreakingNews).filter(BreakingNews.id == news_id).first()
        if not news_item:
            raise HTTPException(status_code=404, detail="Breaking news not found")
        
        db.delete(news_item)
        db.commit()
        
        return {"success": True, "message": "Breaking news deleted"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e)) 