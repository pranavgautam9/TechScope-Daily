import requests
from typing import List, Dict, Optional
from app.core.config import settings
import random
import json
from datetime import datetime

class AIContentGenerator:
    def __init__(self):
        # Hugging Face Inference API (free, no API key required for public models)
        self.hf_api_url = "https://api-inference.huggingface.co/models"
        # Using a free, fast model for text generation
        self.model_name = "mistralai/Mistral-7B-Instruct-v0.2"
        # Fallback to simpler model if main one fails
        self.fallback_model = "gpt2"
    
    async def generate_tech_fact(self, category: str = "random") -> Dict:
        """Generate a tech fact using free Hugging Face AI"""
        
        categories = {
            "cs": "computer science concepts, algorithms, data structures",
            "ai": "artificial intelligence, machine learning, neural networks",
            "tech": "technology companies, innovations, tech history",
            "companies": "tech companies, founders, company facts",
            "random": "technology in general"
        }
        
        category_desc = categories.get(category, "technology")
        
        # Try to get a unique fact by using date-based seed
        date_seed = datetime.now().toordinal()
        
        # Try Hugging Face API first (free, but may be rate-limited)
        try:
            prompt = f"Generate one interesting, educational fact about {category_desc}. The fact should be accurate, engaging, and related to computer science, AI, or technology. Return only the fact text, nothing else. Maximum 100 words."
            
            headers = {
                "Content-Type": "application/json",
            }
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 100,
                    "temperature": 0.7,
                    "return_full_text": False
                }
            }
            
            # Try main model first
            try:
                response = requests.post(
                    f"{self.hf_api_url}/{self.model_name}",
                    headers=headers,
                    json=payload,
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        generated_text = result[0].get("generated_text", "").strip()
                        if generated_text:
                            # Clean up the generated text
                            fact_text = generated_text.split("\n")[0].strip()
                            fact_text = fact_text.replace('"', '').strip()
                            
                            return {
                                "fact_text": fact_text,
                                "category": category,
                                "source": "AI Generated (Hugging Face)"
                            }
            except Exception as e:
                print(f"Error with main model: {e}")
            
            # Fallback to simpler model
            try:
                response = requests.post(
                    f"{self.hf_api_url}/{self.fallback_model}",
                    headers=headers,
                    json=payload,
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        generated_text = result[0].get("generated_text", "").strip()
                        if generated_text:
                            fact_text = generated_text.split("\n")[0].strip()
                            fact_text = fact_text.replace('"', '').strip()
                            
                            return {
                                "fact_text": fact_text,
                                "category": category,
                                "source": "AI Generated (Hugging Face)"
                            }
            except Exception as e:
                print(f"Error with fallback model: {e}")
                
        except Exception as e:
            print(f"Error generating AI fact from Hugging Face: {e}")
        
        # Final fallback to database (ensures unique facts daily)
        return self._get_fallback_fact(category, date_seed)
    
    async def analyze_news_importance(self, news_title: str, news_content: str) -> Dict:
        """Analyze news importance using rule-based analysis"""
        text = f"{news_title} {news_content}".lower()
        
        # Keywords that indicate high importance
        high_importance_keywords = [
            "breakthrough", "revolutionary", "major", "critical", "significant",
            "first", "launch", "release", "announcement", "acquisition", "merger",
            "ipo", "funding", "billion", "million", "partnership", "deal"
        ]
        
        # Major tech companies
        major_companies = [
            "apple", "microsoft", "google", "amazon", "meta", "facebook",
            "tesla", "nvidia", "netflix", "openai", "anthropic", "x",
            "twitter", "linkedin", "uber", "airbnb", "spotify"
        ]
        
        # Calculate importance score
        score = 0.5  # Base score
        
        # Check for high importance keywords
        for keyword in high_importance_keywords:
            if keyword in text:
                score += 0.1
        
        # Check for major companies
        for company in major_companies:
            if company in text:
                score += 0.15
        
        # Check for breaking/urgent indicators
        if any(word in text for word in ["breaking", "urgent", "alert", "critical"]):
            score += 0.2
        
        # Normalize score to 0.0-1.0
        score = min(1.0, max(0.0, score))
        
        is_important = score >= 0.7
        
        return {
            "importance_score": round(score, 2),
            "is_important": is_important,
            "reason": "Rule-based analysis based on keywords and company mentions"
        }
    
    async def analyze_breaking_news_importance(self, news_title: str, news_content: str) -> Dict:
        """Analyze breaking news importance and criticality using rule-based analysis"""
        text = f"{news_title} {news_content}".lower()
        
        # Calculate importance score
        score = 0.6  # Base score for breaking news
        
        # High importance indicators
        high_importance = [
            "breakthrough", "revolutionary", "major", "critical", "significant",
            "first", "launch", "release", "announcement", "acquisition", "merger",
            "ipo", "funding", "billion", "partnership", "deal", "crisis", "breach"
        ]
        
        # Major tech companies
        major_companies = [
            "apple", "microsoft", "google", "amazon", "meta", "facebook",
            "tesla", "nvidia", "netflix", "openai", "anthropic", "x",
            "twitter", "linkedin", "uber", "airbnb", "spotify"
        ]
        
        # Critical indicators
        critical_indicators = [
            "critical", "urgent", "breaking", "alert", "crisis", "breach",
            "security", "hack", "attack", "outage", "down", "failure"
        ]
        
        # Positive sentiment indicators
        positive_words = [
            "launch", "release", "announcement", "partnership", "acquisition",
            "growth", "success", "breakthrough", "innovation", "achievement",
            "milestone", "record", "profit", "gain", "up"
        ]
        
        # Negative sentiment indicators
        negative_words = [
            "breach", "hack", "attack", "crisis", "failure", "outage",
            "down", "loss", "decline", "layoff", "cut", "down", "drop"
        ]
        
        # Calculate score
        for keyword in high_importance:
            if keyword in text:
                score += 0.1
        
        for company in major_companies:
            if company in text:
                score += 0.15
        
        # Determine criticality
        is_critical = any(indicator in text for indicator in critical_indicators)
        if is_critical:
            score += 0.2
        
        # Determine sentiment
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        if positive_count > negative_count:
            sentiment = "positive"
        elif negative_count > positive_count:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        # Determine impact level
        if score >= 0.8:
            impact_level = "high"
        elif score >= 0.6:
            impact_level = "medium"
        else:
            impact_level = "low"
        
        # Normalize score
        score = min(1.0, max(0.0, score))
        
        return {
            "importance_score": round(score, 2),
            "is_critical": is_critical,
            "sentiment": sentiment,
            "impact_level": impact_level,
            "reason": f"Rule-based analysis: {impact_level} impact, {sentiment} sentiment"
        }
    
    def _get_daily_fact_from_database(self, category: str, date_seed: int) -> Optional[Dict]:
        """Get a fact from expanded database, rotated daily based on date"""
        expanded_facts = {
            "cs": [
                "The first computer bug was an actual bug - a moth found in the Harvard Mark II computer in 1947.",
                "The term 'algorithm' comes from the name of Persian mathematician Al-Khwarizmi.",
                "The first programming language was FORTRAN, created in 1957 by IBM.",
                "Ada Lovelace is considered the first computer programmer for her work on Charles Babbage's Analytical Engine.",
                "The first computer mouse was made of wood and had two wheels.",
                "The QWERTY keyboard layout was designed to slow down typists to prevent typewriter jams.",
                "The first hard drive weighed over a ton and stored only 5MB of data.",
                "The first domain name ever registered was symbolics.com in 1985.",
                "The first computer virus was created in 1983 and was called 'Elk Cloner'.",
                "The first webcam was created to monitor a coffee pot at Cambridge University.",
                "The first email was sent in 1971 by Ray Tomlinson, who also introduced the @ symbol.",
                "The first computer game was 'Spacewar!' created in 1962 at MIT.",
                "The first computer to use a mouse and GUI was the Xerox Alto in 1973.",
                "The first computer to pass the Turing Test was Eugene Goostman in 2014.",
                "The first computer to beat a human at chess was Deep Blue in 1997.",
                "The first computer to beat a human at Go was AlphaGo in 2016.",
                "The first computer to pass the CAPTCHA test was created in 2014.",
                "The first computer to write a novel was in 2016, called 'The Day A Computer Writes A Novel'.",
                "The first computer to create art was in 2018, called 'Portrait of Edmond de Belamy'.",
                "The first computer to compose music was in 1957, called 'Illiac Suite'.",
                "The first computer to translate languages was in 1954, called 'Georgetown-IBM experiment'.",
                "The first computer to recognize speech was in 1962, called 'Shoebox'.",
                "The first computer to recognize faces was in 1964, called 'Face Recognition System'.",
                "The first computer to drive a car was in 1986, called 'Navlab'.",
                "The first computer to fly a plane was in 1987, called 'Pilot's Associate'.",
                "The first computer to perform surgery was in 1985, called 'PUMA 560'.",
                "The first computer to diagnose diseases was in 1972, called 'MYCIN'.",
                "The first computer to play poker was in 2015, called 'Libratus'.",
                "The first computer to play Jeopardy! was in 2011, called 'Watson'.",
                "The first computer to play StarCraft was in 2019, called 'AlphaStar'.",
            ],
            "ai": [
                "The term 'Artificial Intelligence' was first coined at a conference at Dartmouth College in 1956.",
                "The first AI program was written in 1951 to play checkers.",
                "Machine learning algorithms can now detect patterns invisible to the human eye.",
                "The first neural network was created in 1943 by Warren McCulloch and Walter Pitts.",
                "The first AI chatbot was ELIZA, created in 1966 at MIT.",
                "The first AI to win a game show was Watson, which won Jeopardy! in 2011.",
                "The first AI to beat a world champion at Go was AlphaGo in 2016.",
                "The first AI to create realistic images was DALL-E in 2021.",
                "The first AI to write code was GitHub Copilot in 2021.",
                "The first AI to generate music was Jukebox in 2020.",
                "The first AI to create videos was Make-A-Video in 2022.",
                "The first AI to understand natural language was GPT-3 in 2020.",
                "The first AI to pass the Turing Test was Eugene Goostman in 2014.",
                "The first AI to drive a car was in 2004, called 'Stanley'.",
                "The first AI to fly a drone was in 2017, called 'AlphaPilot'.",
                "The first AI to play chess was Deep Blue in 1997.",
                "The first AI to play poker was Libratus in 2017.",
                "The first AI to play StarCraft was AlphaStar in 2019.",
                "The first AI to create art was AARON in 1973.",
                "The first AI to compose music was AIVA in 2016.",
                "The first AI to write a novel was in 2016.",
                "The first AI to diagnose diseases was MYCIN in 1972.",
                "The first AI to perform surgery was da Vinci in 2000.",
                "The first AI to recognize faces was in 1964.",
                "The first AI to recognize speech was Shoebox in 1962.",
                "The first AI to translate languages was in 1954.",
                "The first AI to understand emotions was in 2015.",
                "The first AI to create memes was in 2020.",
                "The first AI to generate code was GitHub Copilot in 2021.",
                "The first AI to write poetry was in 2018.",
            ],
            "tech": [
                "The first iPhone was announced by Steve Jobs in 2007, revolutionizing mobile computing.",
                "Google was originally called 'Backrub' before being renamed in 1997.",
                "The first email was sent in 1971 by Ray Tomlinson, who also introduced the @ symbol.",
                "The first website is still online at info.cern.ch.",
                "The first computer was the size of a room and weighed 30 tons.",
                "The first smartphone was the IBM Simon, released in 1994.",
                "The first tablet computer was the GRiDPad, released in 1989.",
                "The first laptop was the Osborne 1, released in 1981.",
                "The first digital camera was created in 1975 by Kodak.",
                "The first MP3 player was the MPMan, released in 1998.",
                "The first streaming service was RealAudio, launched in 1995.",
                "The first social media platform was Six Degrees, launched in 1997.",
                "The first search engine was Archie, created in 1990.",
                "The first web browser was WorldWideWeb, created in 1990.",
                "The first video game was 'Tennis for Two', created in 1958.",
                "The first computer virus was created in 1983.",
                "The first spam email was sent in 1978.",
                "The first emoji was created in 1999 by Shigetaka Kurita.",
                "The first GIF was created in 1987.",
                "The first YouTube video was uploaded in 2005.",
                "The first tweet was sent in 2006.",
                "The first Facebook post was made in 2004.",
                "The first Instagram photo was posted in 2010.",
                "The first Snapchat message was sent in 2011.",
                "The first TikTok video was uploaded in 2016.",
                "The first cryptocurrency was Bitcoin, created in 2009.",
                "The first blockchain was created in 2008.",
                "The first NFT was created in 2014.",
                "The first VR headset was created in 1968.",
                "The first AR app was created in 2009.",
            ],
            "companies": [
                "Microsoft was founded in 1975 by Bill Gates and Paul Allen in a garage.",
                "Apple was founded on April 1, 1976, by Steve Jobs, Steve Wozniak, and Ronald Wayne.",
                "Amazon started as an online bookstore in 1994 before becoming the e-commerce giant.",
                "Google was founded in 1998 by Larry Page and Sergey Brin in a garage.",
                "Facebook was founded in 2004 by Mark Zuckerberg in his Harvard dorm room.",
                "Twitter was founded in 2006 by Jack Dorsey, Biz Stone, and Evan Williams.",
                "Uber was founded in 2009 by Travis Kalanick and Garrett Camp.",
                "Airbnb was founded in 2008 by Brian Chesky, Joe Gebbia, and Nathan Blecharczyk.",
                "Tesla was founded in 2003 by Martin Eberhard and Marc Tarpenning.",
                "SpaceX was founded in 2002 by Elon Musk.",
                "Netflix was founded in 1997 by Reed Hastings and Marc Randolph.",
                "Spotify was founded in 2006 by Daniel Ek and Martin Lorentzon.",
                "Instagram was founded in 2010 by Kevin Systrom and Mike Krieger.",
                "Snapchat was founded in 2011 by Evan Spiegel, Bobby Murphy, and Reggie Brown.",
                "TikTok was founded in 2016 by Zhang Yiming.",
                "Zoom was founded in 2011 by Eric Yuan.",
                "Slack was founded in 2013 by Stewart Butterfield.",
                "Discord was founded in 2015 by Jason Citron.",
                "Reddit was founded in 2005 by Steve Huffman and Alexis Ohanian.",
                "LinkedIn was founded in 2002 by Reid Hoffman.",
                "Pinterest was founded in 2010 by Ben Silbermann, Paul Sciarra, and Evan Sharp.",
                "WhatsApp was founded in 2009 by Jan Koum and Brian Acton.",
                "Telegram was founded in 2013 by Pavel Durov.",
                "Signal was founded in 2014 by Moxie Marlinspike.",
                "GitHub was founded in 2008 by Tom Preston-Werner, Chris Wanstrath, and PJ Hyett.",
                "GitLab was founded in 2011 by Dmitriy Zaporozhets and Valery Sizov.",
                "Docker was founded in 2013 by Solomon Hykes.",
                "Kubernetes was created by Google in 2014.",
                "React was created by Facebook in 2013.",
                "Vue.js was created by Evan You in 2014.",
            ]
        }
        
        facts = expanded_facts.get(category, expanded_facts["tech"])
        # Use date_seed to select a fact that changes daily
        selected_fact = facts[date_seed % len(facts)]
        
        return {
            "fact_text": selected_fact,
            "category": category,
            "source": "Daily Rotated Database"
        }
    
    def _get_fallback_fact(self, category: str, date_seed: int) -> Dict:
        """Fallback facts when AI is not available"""
        return self._get_daily_fact_from_database(category, date_seed) 