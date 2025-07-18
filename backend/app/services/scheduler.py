import asyncio
import schedule
import time
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.services.breaking_news_service import BreakingNewsService
from app.ai.content_generator import AIContentGenerator
from app.models.database import BreakingNews

class NewsScheduler:
    def __init__(self):
        self.breaking_news_service = BreakingNewsService()
        self.ai_generator = AIContentGenerator()
    
    async def fetch_and_analyze_breaking_news(self):
        """Fetch breaking news and analyze with AI"""
        try:
            db = SessionLocal()
            
            # Fetch from Google News
            print(f"[{datetime.now()}] Fetching Google News...")
            google_news = await self.breaking_news_service.fetch_google_news(db)
            
            # Fetch from LinkedIn (simulated)
            print(f"[{datetime.now()}] Fetching LinkedIn News...")
            linkedin_news = await self.breaking_news_service.fetch_linkedin_news(db)
            
            # Analyze importance for new breaking news
            breaking_news = db.query(BreakingNews).filter(
                BreakingNews.ai_analysis.is_(None)
            ).all()
            
            for news in breaking_news:
                try:
                    analysis = await self.ai_generator.analyze_breaking_news_importance(
                        news.title, 
                        news.content
                    )
                    
                    news.importance_score = analysis.get("importance_score", 0.5)
                    news.is_critical = analysis.get("is_critical", False)
                    news.ai_analysis = analysis.get("reason", "")
                    news.sentiment = analysis.get("sentiment", "neutral")
                    news.impact_level = analysis.get("impact_level", "medium")
                    
                    print(f"[{datetime.now()}] Analyzed: {news.title[:50]}... (Score: {news.importance_score:.2f})")
                    
                except Exception as e:
                    print(f"Error analyzing news {news.id}: {e}")
                    continue
            
            db.commit()
            print(f"[{datetime.now()}] Completed breaking news update. Fetched: {len(google_news) + len(linkedin_news)} items")
            
        except Exception as e:
            print(f"Error in scheduled breaking news fetch: {e}")
        finally:
            db.close()
    
    def start_scheduler(self):
        """Start the news scheduler"""
        print("Starting Breaking News Scheduler...")
        
        # Schedule breaking news fetch every 30 minutes
        schedule.every(30).minutes.do(
            lambda: asyncio.run(self.fetch_and_analyze_breaking_news())
        )
        
        # Schedule breaking news fetch every 15 minutes during business hours
        schedule.every().day.at("09:00").do(
            lambda: asyncio.run(self.fetch_and_analyze_breaking_news())
        )
        schedule.every().day.at("12:00").do(
            lambda: asyncio.run(self.fetch_and_analyze_breaking_news())
        )
        schedule.every().day.at("15:00").do(
            lambda: asyncio.run(self.fetch_and_analyze_breaking_news())
        )
        schedule.every().day.at("18:00").do(
            lambda: asyncio.run(self.fetch_and_analyze_breaking_news())
        )
        
        # Run initial fetch
        asyncio.run(self.fetch_and_analyze_breaking_news())
        
        # Keep the scheduler running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

# Global scheduler instance
news_scheduler = NewsScheduler()

def start_breaking_news_scheduler():
    """Start the breaking news scheduler in a separate thread"""
    import threading
    
    scheduler_thread = threading.Thread(
        target=news_scheduler.start_scheduler,
        daemon=True
    )
    scheduler_thread.start()
    print("Breaking News Scheduler started in background thread") 