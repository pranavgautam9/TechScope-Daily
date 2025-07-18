from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.models.database import News

class NewsService:
    def get_daily_news(self, db: Session, limit: int = 10, category: Optional[str] = None) -> List[dict]:
        """Get daily news with optional category filter"""
        query = db.query(News)
        
        if category:
            query = query.filter(News.category == category)
        
        news_items = query.order_by(News.created_at.desc()).limit(limit).all()
        
        return [
            {
                "id": item.id,
                "title": item.title,
                "content": item.content,
                "source": item.source,
                "url": item.url,
                "category": item.category,
                "importance_score": item.importance_score,
                "is_important": item.is_important,
                "published_at": item.published_at,
                "created_at": item.created_at
            }
            for item in news_items
        ]
    
    def get_latest_news(self, db: Session, limit: int = 5) -> List[dict]:
        """Get the most recent news items"""
        news_items = db.query(News).order_by(News.created_at.desc()).limit(limit).all()
        
        return [
            {
                "id": item.id,
                "title": item.title,
                "content": item.content[:200] + "..." if len(item.content) > 200 else item.content,
                "source": item.source,
                "url": item.url,
                "category": item.category,
                "published_at": item.published_at
            }
            for item in news_items
        ]
    
    def get_news_by_category(self, db: Session, category: str, limit: int = 10) -> List[dict]:
        """Get news by specific category"""
        news_items = db.query(News).filter(
            News.category == category
        ).order_by(News.created_at.desc()).limit(limit).all()
        
        return [
            {
                "id": item.id,
                "title": item.title,
                "content": item.content,
                "source": item.source,
                "url": item.url,
                "category": item.category,
                "published_at": item.published_at
            }
            for item in news_items
        ]
    
    def get_important_news(self, db: Session, limit: int = 10) -> List[dict]:
        """Get news marked as important"""
        news_items = db.query(News).filter(
            News.is_important == True
        ).order_by(News.importance_score.desc()).limit(limit).all()
        
        return [
            {
                "id": item.id,
                "title": item.title,
                "content": item.content,
                "source": item.source,
                "url": item.url,
                "importance_score": item.importance_score,
                "published_at": item.published_at
            }
            for item in news_items
        ]
    
    def get_news_trends(self, db: Session, days: int = 7) -> dict:
        """Get news trends over the last N days"""
        start_date = datetime.now() - timedelta(days=days)
        
        # Get news count by category
        category_counts = db.query(News.category, db.func.count(News.id)).filter(
            News.created_at >= start_date
        ).group_by(News.category).all()
        
        # Get importance distribution
        important_count = db.query(News).filter(
            News.created_at >= start_date,
            News.is_important == True
        ).count()
        
        total_count = db.query(News).filter(
            News.created_at >= start_date
        ).count()
        
        return {
            "category_distribution": {cat: count for cat, count in category_counts},
            "important_news_percentage": (important_count / total_count * 100) if total_count > 0 else 0,
            "total_news_count": total_count,
            "important_news_count": important_count
        } 