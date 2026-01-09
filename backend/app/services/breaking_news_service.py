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
        self.wired_rss_url = "https://www.wired.com/feed/rss"
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
        """Fetch breaking news from Google News RSS - filtered for tech news"""
        try:
            # Use Google News RSS feed for tech news, prioritize Wired.com
            params = {
                'q': '(technology OR "artificial intelligence" OR "machine learning" OR "tech company") (site:wired.com OR "wired")',
                'hl': 'en-US',
                'gl': 'US',
                'ceid': 'US:en'
            }
            
            response = requests.get(self.google_news_url, params=params, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item')
            
            fetched_news = []
            
            for item in items[:15]:  # Limit to 15 items
                title_elem = item.find('title')
                link_elem = item.find('link')
                pub_date_elem = item.find('pubDate')
                description_elem = item.find('description')
                
                # Extract and clean text
                title = title_elem.get_text(strip=True) if title_elem else ""
                link = link_elem.get_text(strip=True) if link_elem else ""
                pub_date = pub_date_elem.get_text(strip=True) if pub_date_elem else ""
                
                # Clean description - remove HTML tags and get meaningful content
                if description_elem:
                    # Get the raw HTML first
                    desc_html = str(description_elem)
                    desc_soup = BeautifulSoup(desc_html, 'html.parser')
                    
                    # Remove all script and style elements
                    for script in desc_soup(["script", "style", "a"]):
                        script.decompose()
                    
                    # Try to extract meaningful content
                    # First, try to get text from paragraph tags
                    paragraphs = desc_soup.find_all('p')
                    if paragraphs:
                        description = ' '.join([p.get_text(strip=True) for p in paragraphs[:3] if p.get_text(strip=True)])
                    else:
                        # If no paragraphs, get all text
                        description = desc_soup.get_text(separator=' ', strip=True)
                    
                    # Clean up the description
                    description = description.replace('&nbsp;', ' ').replace('&amp;', '&')
                    description = description.replace('&lt;', '<').replace('&gt;', '>')
                    description = description.replace('&quot;', '"').replace('&#39;', "'")
                    # Remove extra whitespace
                    description = ' '.join(description.split())
                    
                    # If description is same as title or too short, try to fetch from article
                    if description.lower().strip() == title.lower().strip() or len(description) < 100:
                        # Try to fetch article content
                        try:
                            article_content = self._fetch_article_content(link)
                            if article_content and len(article_content) > 100:
                                description = article_content
                        except Exception as e:
                            print(f"Could not fetch article content: {e}")
                            # Use a more descriptive fallback
                            description = f"This article covers {title.lower()}. Click 'Read Full Story' to view the complete article."
                else:
                    description = f"This article covers {title.lower()}. Click 'Read Full Story' to view the complete article."
                
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
    
    async def fetch_wired_news(self, db: Session) -> List[Dict]:
        """Fetch news from Wired.com RSS feed"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(self.wired_rss_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item')
            
            fetched_news = []
            
            for item in items[:15]:  # Limit to 15 items
                title_elem = item.find('title')
                link_elem = item.find('link')
                pub_date_elem = item.find('pubDate')
                description_elem = item.find('description')
                
                # Extract and clean text
                title = title_elem.get_text(strip=True) if title_elem else ""
                link = link_elem.get_text(strip=True) if link_elem else ""
                pub_date = pub_date_elem.get_text(strip=True) if pub_date_elem else ""
                
                # Clean description - remove HTML tags and get meaningful content
                if description_elem:
                    desc_html = str(description_elem)
                    desc_soup = BeautifulSoup(desc_html, 'html.parser')
                    
                    # Remove all script and style elements
                    for script in desc_soup(["script", "style", "a"]):
                        script.decompose()
                    
                    # Try to extract meaningful content
                    paragraphs = desc_soup.find_all('p')
                    if paragraphs:
                        description = ' '.join([p.get_text(strip=True) for p in paragraphs[:3] if p.get_text(strip=True)])
                    else:
                        description = desc_soup.get_text(separator=' ', strip=True)
                    
                    # Clean up the description
                    description = description.replace('&nbsp;', ' ').replace('&amp;', '&')
                    description = description.replace('&lt;', '<').replace('&gt;', '>')
                    description = description.replace('&quot;', '"').replace('&#39;', "'")
                    description = ' '.join(description.split())
                    
                    # If description is too short, try to fetch from article
                    if len(description) < 100:
                        try:
                            article_content = self._fetch_article_content(link)
                            if article_content and len(article_content) > 100:
                                description = article_content
                        except Exception as e:
                            print(f"Could not fetch article content: {e}")
                            description = f"This Wired article covers {title.lower()}. Click 'Read Full Story' to view the complete article."
                else:
                    description = f"This Wired article covers {title.lower()}. Click 'Read Full Story' to view the complete article."
                
                # Check if already exists
                existing = db.query(BreakingNews).filter(
                    BreakingNews.url == link
                ).first()
                
                if not existing and title and link:
                    news_item = BreakingNews(
                        title=title,
                        content=description,
                        source="wired.com",
                        url=link,
                        category=self._categorize_news(title, description),
                        published_at=self._parse_date(pub_date)
                    )
                    
                    db.add(news_item)
                    fetched_news.append({
                        "title": title,
                        "content": description,
                        "source": "wired.com",
                        "url": link
                    })
            
            db.commit()
            return fetched_news
            
        except Exception as e:
            print(f"Error fetching Wired news: {e}")
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
    
    def _fetch_article_content(self, url: str, max_length: int = 800) -> str:
        """Fetch article content from URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
                script.decompose()
            
            # Try to find main content in common article tags
            article = soup.find('article') or soup.find('main') or soup.find('div', class_=lambda x: x and ('article' in x.lower() or 'content' in x.lower() or 'post' in x.lower()))
            
            if article:
                # Get all paragraph text
                paragraphs = article.find_all('p')
                if paragraphs:
                    content = ' '.join([p.get_text(strip=True) for p in paragraphs[:5] if p.get_text(strip=True)])
                    if len(content) > 100:
                        return content[:max_length] + '...' if len(content) > max_length else content
            
            # Fallback: get all paragraph text from body
            paragraphs = soup.find_all('p')
            if paragraphs:
                content = ' '.join([p.get_text(strip=True) for p in paragraphs[:5] if p.get_text(strip=True) and len(p.get_text(strip=True)) > 50])
                if len(content) > 100:
                    return content[:max_length] + '...' if len(content) > max_length else content
            
            return ""
        except Exception as e:
            print(f"Error fetching article content from {url}: {e}")
            return ""
    
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