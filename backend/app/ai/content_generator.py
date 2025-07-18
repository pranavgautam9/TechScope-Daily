import openai
from typing import List, Dict, Optional
from app.core.config import settings
import random

class AIContentGenerator:
    def __init__(self):
        if settings.OPENAI_API_KEY:
            self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        else:
            self.client = None
            print("Warning: OpenAI API key not found. AI features will be limited.")
    
    async def generate_tech_fact(self, category: str = "random") -> Dict:
        """Generate a tech fact using AI"""
        
        if not self.client:
            return self._get_fallback_fact(category)
        
        categories = {
            "cs": "computer science concepts, algorithms, data structures",
            "ai": "artificial intelligence, machine learning, neural networks",
            "tech": "technology companies, innovations, tech history",
            "companies": "tech companies, founders, company facts"
        }
        
        prompt = f"""
        Generate an interesting, educational fact about {categories.get(category, 'technology')}.
        The fact should be:
        - Accurate and verifiable
        - Engaging and surprising
        - Related to computer science, AI, or technology
        - Suitable for a daily newsletter
        
        Return only the fact text, nothing else.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a tech fact generator for a daily newsletter."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            fact_text = response.choices[0].message.content.strip()
            
            return {
                "fact_text": fact_text,
                "category": category,
                "source": "AI Generated"
            }
        except Exception as e:
            print(f"Error generating AI fact: {e}")
            return self._get_fallback_fact(category)
    
    async def analyze_news_importance(self, news_title: str, news_content: str) -> Dict:
        """Analyze news importance to determine if it should go to weekly section"""
        
        if not self.client:
            return {"importance_score": random.uniform(0.1, 0.9), "is_important": random.choice([True, False])}
        
        prompt = f"""
        Analyze the importance of this tech news:
        
        Title: {news_title}
        Content: {news_content[:500]}...
        
        Rate the importance from 0.0 to 1.0 where:
        - 0.0-0.3: Minor news, not important
        - 0.4-0.6: Moderate importance
        - 0.7-1.0: High importance, should be in weekly section
        
        Consider factors like:
        - Impact on industry
        - Innovation level
        - Market significance
        - Public interest
        
        Return only a JSON object with:
        {{"importance_score": float, "is_important": boolean, "reason": "brief explanation"}}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a news importance analyzer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.3
            )
            
            result = response.choices[0].message.content.strip()
            # Parse the JSON response
            import json
            return json.loads(result)
        except Exception as e:
            print(f"Error analyzing news importance: {e}")
            return {"importance_score": random.uniform(0.1, 0.9), "is_important": random.choice([True, False])}
    
    async def analyze_breaking_news_importance(self, news_title: str, news_content: str) -> Dict:
        """Analyze breaking news importance and criticality"""
        
        if not self.client:
            return {
                "importance_score": random.uniform(0.5, 1.0),
                "is_critical": random.choice([True, False]),
                "sentiment": random.choice(["positive", "negative", "neutral"]),
                "impact_level": random.choice(["high", "medium", "low"])
            }
        
        prompt = f"""
        Analyze this breaking tech news for importance and criticality:
        
        Title: {news_title}
        Content: {news_content[:500]}...
        
        Analyze for:
        1. Importance score (0.0-1.0): How significant is this news?
        2. Criticality: Is this critical breaking news that requires immediate attention?
        3. Sentiment: positive, negative, or neutral
        4. Impact level: high, medium, or low
        5. Reason: Brief explanation of the analysis
        
        Consider factors like:
        - Company size and influence
        - Market impact
        - Innovation level
        - Industry disruption potential
        - Public interest and media coverage
        
        Return only a JSON object with:
        {{
            "importance_score": float,
            "is_critical": boolean,
            "sentiment": "positive|negative|neutral",
            "impact_level": "high|medium|low",
            "reason": "brief explanation"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a breaking news analyzer for tech industry news."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            result = response.choices[0].message.content.strip()
            # Parse the JSON response
            import json
            return json.loads(result)
        except Exception as e:
            print(f"Error analyzing breaking news importance: {e}")
            return {
                "importance_score": random.uniform(0.5, 1.0),
                "is_critical": random.choice([True, False]),
                "sentiment": random.choice(["positive", "negative", "neutral"]),
                "impact_level": random.choice(["high", "medium", "low"]),
                "reason": "Analysis unavailable"
            }
    
    def _get_fallback_fact(self, category: str) -> Dict:
        """Fallback facts when AI is not available"""
        fallback_facts = {
            "cs": [
                "The first computer bug was an actual bug - a moth found in the Harvard Mark II computer in 1947.",
                "The term 'algorithm' comes from the name of Persian mathematician Al-Khwarizmi.",
                "The first programming language was FORTRAN, created in 1957 by IBM."
            ],
            "ai": [
                "The term 'Artificial Intelligence' was first coined at a conference at Dartmouth College in 1956.",
                "The first AI program was written in 1951 to play checkers.",
                "Machine learning algorithms can now detect patterns invisible to the human eye."
            ],
            "tech": [
                "The first iPhone was announced by Steve Jobs in 2007, revolutionizing mobile computing.",
                "Google was originally called 'Backrub' before being renamed in 1997.",
                "The first email was sent in 1971 by Ray Tomlinson, who also introduced the @ symbol."
            ],
            "companies": [
                "Microsoft was founded in 1975 by Bill Gates and Paul Allen in a garage.",
                "Apple was founded on April 1, 1976, by Steve Jobs, Steve Wozniak, and Ronald Wayne.",
                "Amazon started as an online bookstore in 1994 before becoming the e-commerce giant."
            ]
        }
        
        facts = fallback_facts.get(category, fallback_facts["tech"])
        return {
            "fact_text": random.choice(facts),
            "category": category,
            "source": "Fallback Database"
        } 