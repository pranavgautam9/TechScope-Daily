from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import yfinance as yf
from app.models.database import Stock

class StockService:
    def __init__(self):
        self.tech_companies = [
            {"symbol": "AAPL", "name": "Apple Inc."},
            {"symbol": "MSFT", "name": "Microsoft Corporation"},
            {"symbol": "GOOGL", "name": "Alphabet Inc."},
            {"symbol": "AMZN", "name": "Amazon.com Inc."},
            {"symbol": "TSLA", "name": "Tesla Inc."},
            {"symbol": "META", "name": "Meta Platforms Inc."},
            {"symbol": "NVDA", "name": "NVIDIA Corporation"},
            {"symbol": "NFLX", "name": "Netflix Inc."},
            {"symbol": "ADBE", "name": "Adobe Inc."},
            {"symbol": "CRM", "name": "Salesforce Inc."}
        ]
    
    def update_stock_data(self, db: Session) -> List[Dict]:
        """Update stock data from Yahoo Finance API"""
        updated_stocks = []
        
        for company in self.tech_companies:
            try:
                ticker = yf.Ticker(company["symbol"])
                info = ticker.info
                
                current_price = info.get('regularMarketPrice', 0)
                previous_close = info.get('regularMarketPreviousClose', current_price)
                change = current_price - previous_close
                change_percent = (change / previous_close * 100) if previous_close else 0
                
                # Update or create stock record
                stock = db.query(Stock).filter(Stock.symbol == company["symbol"]).first()
                
                if stock:
                    stock.current_price = current_price
                    stock.change = change
                    stock.change_percent = change_percent
                    stock.volume = info.get('volume', 0)
                    stock.market_cap = info.get('marketCap', 0)
                    stock.updated_at = datetime.utcnow()
                else:
                    stock = Stock(
                        symbol=company["symbol"],
                        company_name=company["name"],
                        current_price=current_price,
                        change=change,
                        change_percent=change_percent,
                        volume=info.get('volume', 0),
                        market_cap=info.get('marketCap', 0)
                    )
                    db.add(stock)
                
                updated_stocks.append({
                    "symbol": company["symbol"],
                    "company_name": company["name"],
                    "current_price": current_price,
                    "change": change,
                    "change_percent": change_percent,
                    "volume": info.get('volume', 0),
                    "market_cap": info.get('marketCap', 0)
                })
                
            except Exception as e:
                print(f"Error updating {company['symbol']}: {e}")
                continue
        
        return updated_stocks
    
    def get_market_summary(self, db: Session) -> Dict:
        """Get market summary statistics"""
        stocks = db.query(Stock).all()
        
        if not stocks:
            return {
                "total_stocks": 0,
                "gainers": 0,
                "losers": 0,
                "unchanged": 0,
                "avg_change_percent": 0,
                "total_market_cap": 0
            }
        
        gainers = len([s for s in stocks if s.change_percent > 0])
        losers = len([s for s in stocks if s.change_percent < 0])
        unchanged = len([s for s in stocks if s.change_percent == 0])
        avg_change = sum(s.change_percent for s in stocks) / len(stocks)
        total_market_cap = sum(s.market_cap for s in stocks if s.market_cap)
        
        return {
            "total_stocks": len(stocks),
            "gainers": gainers,
            "losers": losers,
            "unchanged": unchanged,
            "avg_change_percent": round(avg_change, 2),
            "total_market_cap": total_market_cap
        }
    
    def get_top_performers(self, db: Session, limit: int = 5) -> List[Dict]:
        """Get top performing stocks"""
        stocks = db.query(Stock).filter(
            Stock.change_percent > 0
        ).order_by(Stock.change_percent.desc()).limit(limit).all()
        
        return [
            {
                "symbol": stock.symbol,
                "company_name": stock.company_name,
                "current_price": stock.current_price,
                "change_percent": stock.change_percent,
                "change": stock.change
            }
            for stock in stocks
        ]
    
    def get_worst_performers(self, db: Session, limit: int = 5) -> List[Dict]:
        """Get worst performing stocks"""
        stocks = db.query(Stock).filter(
            Stock.change_percent < 0
        ).order_by(Stock.change_percent.asc()).limit(limit).all()
        
        return [
            {
                "symbol": stock.symbol,
                "company_name": stock.company_name,
                "current_price": stock.current_price,
                "change_percent": stock.change_percent,
                "change": stock.change
            }
            for stock in stocks
        ]
    
    def get_stock_by_symbol(self, db: Session, symbol: str) -> Optional[Dict]:
        """Get specific stock by symbol"""
        stock = db.query(Stock).filter(Stock.symbol == symbol.upper()).first()
        
        if not stock:
            return None
        
        return {
            "id": stock.id,
            "symbol": stock.symbol,
            "company_name": stock.company_name,
            "current_price": stock.current_price,
            "change": stock.change,
            "change_percent": stock.change_percent,
            "volume": stock.volume,
            "market_cap": stock.market_cap,
            "updated_at": stock.updated_at
        }
    
    def get_market_trends(self, db: Session) -> Dict:
        """Get market trends and analysis"""
        stocks = db.query(Stock).all()
        
        if not stocks:
            return {"trend": "neutral", "strength": 0}
        
        # Calculate market sentiment
        positive_changes = len([s for s in stocks if s.change_percent > 0])
        negative_changes = len([s for s in stocks if s.change_percent < 0])
        
        total_stocks = len(stocks)
        positive_ratio = positive_changes / total_stocks
        
        # Determine trend
        if positive_ratio > 0.6:
            trend = "bullish"
            strength = positive_ratio
        elif positive_ratio < 0.4:
            trend = "bearish"
            strength = 1 - positive_ratio
        else:
            trend = "neutral"
            strength = 0.5
        
        return {
            "trend": trend,
            "strength": round(strength, 2),
            "positive_stocks": positive_changes,
            "negative_stocks": negative_changes,
            "total_stocks": total_stocks
        } 