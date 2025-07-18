from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import calendar

from app.models.database import get_db, WeeklyContent, News
from app.ai.content_generator import AIContentGenerator

router = APIRouter()
ai_generator = AIContentGenerator()

@router.get("/")
async def get_weekly_content(
    week_number: Optional[int] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get weekly curated content"""
    try:
        query = db.query(WeeklyContent)
        
        if week_number:
            query = query.filter(WeeklyContent.week_number == week_number)
        else:
            # Get current week
            current_week = datetime.now().isocalendar()[1]
            query = query.filter(WeeklyContent.week_number == current_week)
        
        if category:
            query = query.filter(WeeklyContent.category == category)
        
        content = query.order_by(WeeklyContent.created_at.desc()).all()
        
        return {
            "success": True,
            "data": [
                {
                    "id": item.id,
                    "title": item.title,
                    "content": item.content,
                    "category": item.category,
                    "source_news_id": item.source_news_id,
                    "created_at": item.created_at,
                    "week_number": item.week_number
                }
                for item in content
            ],
            "count": len(content)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/current")
async def get_current_week_content(db: Session = Depends(get_db)):
    """Get current week's content"""
    try:
        current_week = datetime.now().isocalendar()[1]
        current_year = datetime.now().year
        
        content = db.query(WeeklyContent).filter(
            WeeklyContent.week_number == current_week
        ).order_by(WeeklyContent.created_at.desc()).all()
        
        return {
            "success": True,
            "data": [
                {
                    "id": item.id,
                    "title": item.title,
                    "content": item.content,
                    "category": item.category,
                    "source_news_id": item.source_news_id,
                    "created_at": item.created_at,
                    "week_number": item.week_number
                }
                for item in content
            ],
            "week_info": {
                "week_number": current_week,
                "year": current_year
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/move-important-news")
async def move_important_news_to_weekly(db: Session = Depends(get_db)):
    """Move important news from daily to weekly section"""
    try:
        # Get important news from the last 7 days
        week_ago = datetime.now() - timedelta(days=7)
        important_news = db.query(News).filter(
            News.is_important == True,
            News.created_at >= week_ago,
            News.importance_score >= 0.7
        ).order_by(News.importance_score.desc()).all()
        
        current_week = datetime.now().isocalendar()[1]
        moved_count = 0
        
        for news in important_news:
            # Check if already moved
            existing = db.query(WeeklyContent).filter(
                WeeklyContent.source_news_id == news.id
            ).first()
            
            if not existing:
                weekly_content = WeeklyContent(
                    title=f"Weekly Highlight: {news.title}",
                    content=news.content,
                    category="news",
                    source_news_id=news.id,
                    week_number=current_week
                )
                
                db.add(weekly_content)
                moved_count += 1
        
        db.commit()
        
        return {
            "success": True,
            "message": f"Moved {moved_count} important news items to weekly section",
            "moved_count": moved_count,
            "week_number": current_week
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_weekly_content(
    title: str,
    content: str,
    category: str = "news",
    source_news_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Create new weekly content"""
    try:
        current_week = datetime.now().isocalendar()[1]
        
        weekly_content = WeeklyContent(
            title=title,
            content=content,
            category=category,
            source_news_id=source_news_id,
            week_number=current_week
        )
        
        db.add(weekly_content)
        db.commit()
        db.refresh(weekly_content)
        
        return {
            "success": True,
            "data": {
                "id": weekly_content.id,
                "title": weekly_content.title,
                "content": weekly_content.content,
                "category": weekly_content.category,
                "week_number": weekly_content.week_number,
                "created_at": weekly_content.created_at
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary")
async def get_weekly_summary(db: Session = Depends(get_db)):
    """Get weekly content summary"""
    try:
        current_week = datetime.now().isocalendar()[1]
        
        # Get content by category
        news_content = db.query(WeeklyContent).filter(
            WeeklyContent.week_number == current_week,
            WeeklyContent.category == "news"
        ).count()
        
        analysis_content = db.query(WeeklyContent).filter(
            WeeklyContent.week_number == current_week,
            WeeklyContent.category == "analysis"
        ).count()
        
        trends_content = db.query(WeeklyContent).filter(
            WeeklyContent.week_number == current_week,
            WeeklyContent.category == "trends"
        ).count()
        
        total_content = news_content + analysis_content + trends_content
        
        return {
            "success": True,
            "data": {
                "week_number": current_week,
                "total_content": total_content,
                "news_count": news_content,
                "analysis_count": analysis_content,
                "trends_count": trends_content
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories")
async def get_weekly_categories(db: Session = Depends(get_db)):
    """Get available weekly content categories"""
    try:
        categories = db.query(WeeklyContent.category).distinct().all()
        return {
            "success": True,
            "categories": [cat[0] for cat in categories if cat[0]]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{content_id}")
async def delete_weekly_content(content_id: int, db: Session = Depends(get_db)):
    """Delete weekly content"""
    try:
        content = db.query(WeeklyContent).filter(WeeklyContent.id == content_id).first()
        if not content:
            raise HTTPException(status_code=404, detail="Weekly content not found")
        
        db.delete(content)
        db.commit()
        
        return {"success": True, "message": "Weekly content deleted"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e)) 