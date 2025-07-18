from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from app.models.database import get_db, Fact
from app.ai.content_generator import AIContentGenerator

router = APIRouter()
ai_generator = AIContentGenerator()

@router.get("/")
async def get_daily_facts(
    limit: int = 5,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get daily tech facts"""
    try:
        query = db.query(Fact).filter(Fact.is_active == True)
        
        if category:
            query = query.filter(Fact.category == category)
        
        facts = query.order_by(Fact.created_at.desc()).limit(limit).all()
        
        return {
            "success": True,
            "data": [
                {
                    "id": fact.id,
                    "fact_text": fact.fact_text,
                    "category": fact.category,
                    "source": fact.source,
                    "created_at": fact.created_at
                }
                for fact in facts
            ],
            "count": len(facts)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/today")
async def get_today_facts(db: Session = Depends(get_db)):
    """Get facts created today"""
    try:
        today = datetime.now().date()
        today_facts = db.query(Fact).filter(
            Fact.is_active == True,
            Fact.created_at >= today
        ).order_by(Fact.created_at.desc()).all()
        
        return {
            "success": True,
            "data": [
                {
                    "id": fact.id,
                    "fact_text": fact.fact_text,
                    "category": fact.category,
                    "source": fact.source,
                    "created_at": fact.created_at
                }
                for fact in today_facts
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate")
async def generate_new_fact(
    category: str = "random",
    db: Session = Depends(get_db)
):
    """Generate a new tech fact using AI"""
    try:
        # Generate fact using AI
        fact_data = await ai_generator.generate_tech_fact(category)
        
        # Save to database
        new_fact = Fact(
            fact_text=fact_data["fact_text"],
            category=fact_data["category"],
            source=fact_data["source"]
        )
        
        db.add(new_fact)
        db.commit()
        db.refresh(new_fact)
        
        return {
            "success": True,
            "data": {
                "id": new_fact.id,
                "fact_text": new_fact.fact_text,
                "category": new_fact.category,
                "source": new_fact.source,
                "created_at": new_fact.created_at
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_fact(
    fact_text: str,
    category: str = "tech",
    source: str = "Manual",
    db: Session = Depends(get_db)
):
    """Create a manual fact"""
    try:
        new_fact = Fact(
            fact_text=fact_text,
            category=category,
            source=source
        )
        
        db.add(new_fact)
        db.commit()
        db.refresh(new_fact)
        
        return {
            "success": True,
            "data": {
                "id": new_fact.id,
                "fact_text": new_fact.fact_text,
                "category": new_fact.category,
                "source": new_fact.source,
                "created_at": new_fact.created_at
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories")
async def get_fact_categories(db: Session = Depends(get_db)):
    """Get available fact categories"""
    try:
        categories = db.query(Fact.category).distinct().all()
        return {
            "success": True,
            "categories": [cat[0] for cat in categories if cat[0]]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/random")
async def get_random_fact(db: Session = Depends(get_db)):
    """Get a random fact"""
    try:
        import random
        facts = db.query(Fact).filter(Fact.is_active == True).all()
        
        if not facts:
            raise HTTPException(status_code=404, detail="No facts available")
        
        random_fact = random.choice(facts)
        
        return {
            "success": True,
            "data": {
                "id": random_fact.id,
                "fact_text": random_fact.fact_text,
                "category": random_fact.category,
                "source": random_fact.source,
                "created_at": random_fact.created_at
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{fact_id}")
async def delete_fact(fact_id: int, db: Session = Depends(get_db)):
    """Delete a fact (soft delete by setting is_active to False)"""
    try:
        fact = db.query(Fact).filter(Fact.id == fact_id).first()
        if not fact:
            raise HTTPException(status_code=404, detail="Fact not found")
        
        fact.is_active = False
        db.commit()
        
        return {"success": True, "message": "Fact deleted"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e)) 