from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import yfinance as yf

from app.models.database import get_db, Stock
from app.services.stock_service import StockService

router = APIRouter()
stock_service = StockService()

# Major tech companies to track
TECH_COMPANIES = [
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

@router.get("/")
async def get_all_stocks(db: Session = Depends(get_db)):
    """Get all tracked tech stocks"""
    try:
        stocks = db.query(Stock).order_by(Stock.symbol).all()
        
        return {
            "success": True,
            "data": [
                {
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
                for stock in stocks
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/live")
async def get_live_stocks(db: Session = Depends(get_db)):
    """Get live stock data (fetch from API and update database)"""
    try:
        updated_stocks = []
        
        for company in TECH_COMPANIES:
            try:
                # Fetch live data from Yahoo Finance
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
                print(f"Error fetching data for {company['symbol']}: {e}")
                continue
        
        db.commit()
        
        return {
            "success": True,
            "data": updated_stocks,
            "updated_at": datetime.utcnow()
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{symbol}")
async def get_stock_by_symbol(symbol: str, db: Session = Depends(get_db)):
    """Get specific stock by symbol"""
    try:
        stock = db.query(Stock).filter(Stock.symbol == symbol.upper()).first()
        
        if not stock:
            raise HTTPException(status_code=404, detail="Stock not found")
        
        return {
            "success": True,
            "data": {
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
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/top-gainers")
async def get_top_gainers(db: Session = Depends(get_db)):
    """Get top gaining stocks"""
    try:
        gainers = db.query(Stock).filter(
            Stock.change_percent > 0
        ).order_by(Stock.change_percent.desc()).limit(5).all()
        
        return {
            "success": True,
            "data": [
                {
                    "symbol": stock.symbol,
                    "company_name": stock.company_name,
                    "current_price": stock.current_price,
                    "change_percent": stock.change_percent
                }
                for stock in gainers
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/top-losers")
async def get_top_losers(db: Session = Depends(get_db)):
    """Get top losing stocks"""
    try:
        losers = db.query(Stock).filter(
            Stock.change_percent < 0
        ).order_by(Stock.change_percent.asc()).limit(5).all()
        
        return {
            "success": True,
            "data": [
                {
                    "symbol": stock.symbol,
                    "company_name": stock.company_name,
                    "current_price": stock.current_price,
                    "change_percent": stock.change_percent
                }
                for stock in losers
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/market-summary")
async def get_market_summary(db: Session = Depends(get_db)):
    """Get market summary statistics"""
    try:
        stocks = db.query(Stock).all()
        
        if not stocks:
            return {
                "success": True,
                "data": {
                    "total_stocks": 0,
                    "gainers": 0,
                    "losers": 0,
                    "unchanged": 0,
                    "avg_change_percent": 0
                }
            }
        
        gainers = len([s for s in stocks if s.change_percent > 0])
        losers = len([s for s in stocks if s.change_percent < 0])
        unchanged = len([s for s in stocks if s.change_percent == 0])
        avg_change = sum(s.change_percent for s in stocks) / len(stocks)
        
        return {
            "success": True,
            "data": {
                "total_stocks": len(stocks),
                "gainers": gainers,
                "losers": losers,
                "unchanged": unchanged,
                "avg_change_percent": round(avg_change, 2)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 