from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.core.config import settings

# Database setup
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class News(Base):
    __tablename__ = "news"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    source = Column(String)
    url = Column(String)
    published_at = Column(DateTime, default=datetime.utcnow)
    category = Column(String)  # tech, ai, cs, etc.
    importance_score = Column(Float, default=0.0)  # For determining if news goes to weekly
    is_important = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class BreakingNews(Base):
    __tablename__ = "breaking_news"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    source = Column(String)  # google_news, linkedin, etc.
    url = Column(String)
    published_at = Column(DateTime, default=datetime.utcnow)
    category = Column(String)  # tech, ai, cs, companies, etc.
    importance_score = Column(Float, default=0.0)
    is_critical = Column(Boolean, default=False)  # For critical breaking news
    ai_analysis = Column(Text)  # AI analysis of the news
    sentiment = Column(String)  # positive, negative, neutral
    impact_level = Column(String)  # high, medium, low
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Fact(Base):
    __tablename__ = "facts"
    
    id = Column(Integer, primary_key=True, index=True)
    fact_text = Column(Text)
    category = Column(String)  # cs, ai, tech, companies
    source = Column(String, default="AI Generated")
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class Stock(Base):
    __tablename__ = "stocks"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    company_name = Column(String)
    current_price = Column(Float)
    change = Column(Float)
    change_percent = Column(Float)
    volume = Column(Integer)
    market_cap = Column(Float)
    updated_at = Column(DateTime, default=datetime.utcnow)



# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 