import asyncio
import schedule
import time
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.database import SessionLocal, Fact
from app.services.breaking_news_service import BreakingNewsService
from app.services.stock_service import StockService
from app.ai.content_generator import AIContentGenerator
from app.models.database import BreakingNews

class NewsScheduler:
    def __init__(self):
        self.breaking_news_service = BreakingNewsService()
        self.stock_service = StockService()
        self.ai_generator = AIContentGenerator()
    
    async def generate_daily_fact(self):
        """Generate a new daily fact"""
        try:
            db = SessionLocal()
            
            # Check if we already have a fact for today
            today = datetime.now().date()
            tomorrow = today + timedelta(days=1)
            
            existing_fact = db.query(Fact).filter(
                Fact.is_active == True,
                Fact.created_at >= datetime.combine(today, datetime.min.time()),
                Fact.created_at < datetime.combine(tomorrow, datetime.min.time())
            ).first()
            
            if existing_fact:
                print(f"[{datetime.now()}] Daily fact already exists for today: {existing_fact.fact_text[:50]}...")
                db.close()
                return
            
            # Generate new fact
            print(f"[{datetime.now()}] Generating new daily fact...")
            fact_data = await self.ai_generator.generate_tech_fact("random")
            
            new_fact = Fact(
                fact_text=fact_data["fact_text"],
                category=fact_data["category"],
                source=fact_data["source"]
            )
            
            db.add(new_fact)
            db.commit()
            
            print(f"[{datetime.now()}] Generated daily fact: {fact_data['fact_text'][:50]}...")
            
        except Exception as e:
            print(f"Error generating daily fact: {e}")
            import traceback
            traceback.print_exc()
        finally:
            db.close()
    
    async def fetch_and_analyze_breaking_news(self):
        """Fetch breaking news and analyze with AI"""
        try:
            db = SessionLocal()
            
            # Fetch from Google News (filtered for tech/Wired)
            print(f"[{datetime.now()}] Fetching Google News...")
            google_news = await self.breaking_news_service.fetch_google_news(db)
            
            # Fetch from Wired.com
            print(f"[{datetime.now()}] Fetching Wired.com News...")
            wired_news = await self.breaking_news_service.fetch_wired_news(db)
            
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
            print(f"[{datetime.now()}] Completed breaking news update. Fetched: {len(google_news) + len(wired_news)} items (Google: {len(google_news)}, Wired: {len(wired_news)})")
            
        except Exception as e:
            print(f"Error in scheduled breaking news fetch: {e}")
        finally:
            db.close()
    
    async def update_daily_stocks(self):
        """Update stock data daily"""
        try:
            db = SessionLocal()
            
            print(f"[{datetime.now()}] Updating daily stock data...")
            updated_stocks = self.stock_service.update_stock_data(db)
            
            db.commit()
            print(f"[{datetime.now()}] Updated {len(updated_stocks)} stocks")
            
        except Exception as e:
            print(f"Error updating stocks: {e}")
            import traceback
            traceback.print_exc()
        finally:
            db.close()
    
    def start_scheduler(self):
        """Start the news scheduler"""
        print("Starting Breaking News Scheduler...")
        
        # Schedule daily fact generation at midnight (00:00)
        schedule.every().day.at("00:00").do(
            lambda: asyncio.run(self.generate_daily_fact())
        )
        
        # Schedule daily stock update at 9:00 AM (market open time)
        schedule.every().day.at("09:00").do(
            lambda: asyncio.run(self.update_daily_stocks())
        )
        
        # Schedule daily news fetch at 6:00 AM (after fact generation)
        schedule.every().day.at("06:00").do(
            lambda: asyncio.run(self.fetch_and_analyze_breaking_news())
        )
        
        # Also fetch news at noon for updates
        schedule.every().day.at("12:00").do(
            lambda: asyncio.run(self.fetch_and_analyze_breaking_news())
        )
        
        # Schedule breaking news fetch every 2 hours during the day
        schedule.every(2).hours.do(
            lambda: asyncio.run(self.fetch_and_analyze_breaking_news())
        )
        
        # Run initial fetches on startup
        print(f"[{datetime.now()}] Running initial fact generation...")
        asyncio.run(self.generate_daily_fact())
        
        print(f"[{datetime.now()}] Running initial news fetch...")
        asyncio.run(self.fetch_and_analyze_breaking_news())
        
        print(f"[{datetime.now()}] Running initial stock update...")
        asyncio.run(self.update_daily_stocks())
        
        print(f"[{datetime.now()}] Scheduler started. Next fact generation at 00:00, next news fetch at 06:00, next stock update at 09:00")
        
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