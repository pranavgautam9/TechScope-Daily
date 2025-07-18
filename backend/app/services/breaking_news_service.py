from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import requests
import json
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import re
from app.models.database import BreakingNews
from app.core.config import settings

class BreakingNewsService:
    def __init__(self):
        self.google_news_url = "https://news.google.com/rss/search"
        self.linkedin_news_url = "https://www.linkedin.com/news/tech/"
        self.tech_keywords = [
            "artificial intelligence", "AI", "machine learning", "ML",
            "tech company", "startup", "venture capital", "IPO",
            "merger", "acquisition", "layoff", "hiring",
            "data breach", "cybersecurity", "blockchain", "crypto",
            "quantum computing", "robotics", "autonomous vehicles",
            "cloud computing", "SaaS", "fintech", "healthtech"
        ]
        
    def get_breaking_news(self, db: Session, limit: int = 10) -> List[Dict]:
        """Get breaking news items"""
        news_items = db.query(BreakingNews).order_by(
            BreakingNews.published_at.desc()
        ).limit(limit).all()
        
        return [
            {
                "id": item.id,
                "title": item.title,
                "content": item.content,
                "source": item.source,
                "url": item.url,
                "category": item.category,
                "importance_score": item.importance_score,
                "is_critical": item.is_critical,
                "sentiment": item.sentiment,
                "impact_level": item.impact_level,
                "published_at": item.published_at,
                "ai_analysis": item.ai_analysis
            }
            for item in news_items
        ]
    
    def get_latest_breaking_news(self, db: Session, hours: int = 24) -> List[Dict]:
        """Get breaking news from the last N hours"""
        time_threshold = datetime.utcnow() - timedelta(hours=hours)
        
        news_items = db.query(BreakingNews).filter(
            BreakingNews.published_at >= time_threshold
        ).order_by(BreakingNews.published_at.desc()).all()
        
        return [
            {
                "id": item.id,
                "title": item.title,
                "content": item.content,
                "source": item.source,
                "url": item.url,
                "category": item.category,
                "importance_score": item.importance_score,
                "is_critical": item.is_critical,
                "published_at": item.published_at
            }
            for item in news_items
        ]
    
    async def fetch_google_news(self, db: Session) -> List[Dict]:
        """Fetch breaking news from Google News RSS"""
        try:
            # Use Google News RSS feed for tech news
            params = {
                'q': 'technology OR "artificial intelligence" OR "machine learning" OR "tech company"',
                'hl': 'en-US',
                'gl': 'US',
                'ceid': 'US:en'
            }
            
            response = requests.get(self.google_news_url, params=params, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item')
            
            fetched_news = []
            
            for item in items[:20]:  # Limit to 20 items
                title = item.find('title').text if item.find('title') else ""
                link = item.find('link').text if item.find('link') else ""
                pub_date = item.find('pubDate').text if item.find('pubDate') else ""
                description = item.find('description').text if item.find('description') else ""
                
                # Check if this is breaking news based on keywords
                if self._is_breaking_news(title, description):
                    # Check if already exists
                    existing = db.query(BreakingNews).filter(
                        BreakingNews.url == link
                    ).first()
                    
                    if not existing:
                        news_item = BreakingNews(
                            title=title,
                            content=description,
                            source="google_news",
                            url=link,
                            category=self._categorize_news(title, description),
                            published_at=self._parse_date(pub_date)
                        )
                        
                        db.add(news_item)
                        fetched_news.append({
                            "title": title,
                            "content": description,
                            "source": "google_news",
                            "url": link
                        })
            
            db.commit()
            return fetched_news
            
        except Exception as e:
            print(f"Error fetching Google News: {e}")
            return []
    
    async def fetch_linkedin_news(self, db: Session) -> List[Dict]:
        """Fetch breaking news from LinkedIn (simulated for now)"""
        try:
            # Note: LinkedIn doesn't have a public API, so we'll simulate this
            # In a real implementation, you'd need to use LinkedIn's API or web scraping
            
            # Simulated LinkedIn news data
            linkedin_news = [
                {
                    "title": "Major Tech Company Announces Revolutionary AI Breakthrough",
                    "content": "A leading technology company has unveiled a groundbreaking artificial intelligence system that promises to transform the industry.",
                    "url": "https://linkedin.com/news/tech-ai-breakthrough",
                    "category": "ai"
                },
                {
                    "title": "Startup Raises $100M in Series B Funding Round",
                    "content": "A promising tech startup has secured significant funding to scale their innovative platform.",
                    "url": "https://linkedin.com/news/startup-funding",
                    "category": "startup"
                },
                {
                    "title": "Tech Giant Acquires AI Startup for $500M",
                    "content": "In a major acquisition, a tech giant has purchased an AI startup to strengthen their machine learning capabilities.",
                    "url": "https://linkedin.com/news/tech-acquisition",
                    "category": "acquisition"
                }
            ]
            
            fetched_news = []
            
            for news in linkedin_news:
                # Check if already exists
                existing = db.query(BreakingNews).filter(
                    BreakingNews.url == news["url"]
                ).first()
                
                if not existing:
                    news_item = BreakingNews(
                        title=news["title"],
                        content=news["content"],
                        source="linkedin",
                        url=news["url"],
                        category=news["category"]
                    )
                    
                    db.add(news_item)
                    fetched_news.append(news)
            
            db.commit()
            return fetched_news
            
        except Exception as e:
            print(f"Error fetching LinkedIn news: {e}")
            return []
    
    def get_trending_news(self, db: Session, limit: int = 10) -> List[Dict]:
        """Get trending breaking news based on importance and recency"""
        # Get news from last 48 hours, ordered by importance and recency
        time_threshold = datetime.utcnow() - timedelta(hours=48)
        
        trending_news = db.query(BreakingNews).filter(
            BreakingNews.published_at >= time_threshold
        ).order_by(
            BreakingNews.importance_score.desc(),
            BreakingNews.published_at.desc()
        ).limit(limit).all()
        
        return [
            {
                "id": item.id,
                "title": item.title,
                "content": item.content,
                "source": item.source,
                "url": item.url,
                "importance_score": item.importance_score,
                "is_critical": item.is_critical,
                "published_at": item.published_at
            }
            for item in trending_news
        ]
    
    def _is_breaking_news(self, title: str, content: str) -> bool:
        """Determine if news is breaking based on keywords and patterns"""
        text = f"{title} {content}".lower()
        
        # Check for breaking news indicators
        breaking_indicators = [
            "breaking", "just in", "urgent", "alert", "announcement",
            "launches", "releases", "acquires", "merges", "partners",
            "funding", "ipo", "layoffs", "hiring", "expansion"
        ]
        
        # Check for tech company names
        tech_companies = [
            "google", "apple", "microsoft", "amazon", "meta", "facebook",
            "tesla", "nvidia", "intel", "amd", "netflix", "spotify",
            "uber", "lyft", "airbnb", "stripe", "openai", "anthropic"
        ]
        
        # Check for AI/ML keywords
        ai_keywords = [
            "artificial intelligence", "machine learning", "deep learning",
            "neural network", "gpt", "llm", "ai model", "algorithm"
        ]
        
        # Score the news
        score = 0
        
        for indicator in breaking_indicators:
            if indicator in text:
                score += 2
        
        for company in tech_companies:
            if company in text:
                score += 3
        
        for keyword in ai_keywords:
            if keyword in text:
                score += 2
        
        # Consider it breaking news if score is high enough
        return score >= 3
    
    def _categorize_news(self, title: str, content: str) -> str:
        """Categorize news based on content"""
        text = f"{title} {content}".lower()
        
        if any(word in text for word in ["ai", "artificial intelligence", "machine learning", "gpt", "llm"]):
            return "ai"
        elif any(word in text for word in ["startup", "funding", "venture", "ipo"]):
            return "startup"
        elif any(word in text for word in ["acquire", "merger", "acquisition"]):
            return "acquisition"
        elif any(word in text for word in ["layoff", "hiring", "job"]):
            return "employment"
        elif any(word in text for word in ["breach", "security", "hack"]):
            return "security"
        else:
            return "tech"
    
    def _parse_date(self, date_string: str) -> datetime:
        """Parse date string from RSS feed"""
        try:
            # Handle common RSS date formats
            formats = [
                "%a, %d %b %Y %H:%M:%S %Z",
                "%a, %d %b %Y %H:%M:%S %z",
                "%Y-%m-%dT%H:%M:%SZ"
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_string, fmt)
                except ValueError:
                    continue
            
            return datetime.utcnow()
        except:
            return datetime.utcnow() 