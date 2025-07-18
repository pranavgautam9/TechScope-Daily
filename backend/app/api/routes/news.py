from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from app.models.database import get_db, News
from app.ai.content_generator import AIContentGenerator
from app.services.news_service import NewsService

router = APIRouter()
ai_generator = AIContentGenerator()
news_service = NewsService()

@router.get("/")
async def get_daily_news(
    limit: int = 10,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get daily tech news"""
    try:
        news_items = news_service.get_daily_news(db, limit=limit, category=category)
        return {
            "success": True,
            "data": news_items,
            "count": len(news_items)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/latest")
async def get_latest_news(db: Session = Depends(get_db)):
    """Get the most recent news items"""
    try:
        latest_news = news_service.get_latest_news(db, limit=5)
        return {
            "success": True,
            "data": latest_news
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_news(
    title: str,
    content: str,
    source: str,
    url: str,
    category: str = "tech",
    db: Session = Depends(get_db)
):
    """Create a new news item with AI importance analysis"""
    try:
        # Analyze importance using AI
        importance_analysis = await ai_generator.analyze_news_importance(title, content)
        
        # Create news item
        news_item = News(
            title=title,
            content=content,
            source=source,
            url=url,
            category=category,
            importance_score=importance_analysis.get("importance_score", 0.5),
            is_important=importance_analysis.get("is_important", False)
        )
        
        db.add(news_item)
        db.commit()
        db.refresh(news_item)
        
        return {
            "success": True,
            "data": {
                "id": news_item.id,
                "title": news_item.title,
                "importance_score": news_item.importance_score,
                "is_important": news_item.is_important
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/important")
async def get_important_news(db: Session = Depends(get_db)):
    """Get news marked as important (for weekly section)"""
    try:
        important_news = db.query(News).filter(
            News.is_important == True
        ).order_by(News.importance_score.desc()).limit(10).all()
        
        return {
            "success": True,
            "data": [
                {
                    "id": item.id,
                    "title": item.title,
                    "content": item.content,
                    "source": item.source,
                    "importance_score": item.importance_score,
                    "published_at": item.published_at
                }
                for item in important_news
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories")
async def get_news_categories(db: Session = Depends(get_db)):
    """Get available news categories"""
    try:
        categories = db.query(News.category).distinct().all()
        return {
            "success": True,
            "categories": [cat[0] for cat in categories if cat[0]]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{news_id}")
async def delete_news(news_id: int, db: Session = Depends(get_db)):
    """Delete a news item"""
    try:
        news_item = db.query(News).filter(News.id == news_id).first()
        if not news_item:
            raise HTTPException(status_code=404, detail="News item not found")
        
        db.delete(news_item)
        db.commit()
        
        return {"success": True, "message": "News item deleted"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e)) 