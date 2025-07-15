# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud
import schemas
import models
from database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ethiopian Medical Data API",
    description="API for analyzing Telegram medical business data",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/reports/top-products", response_model=List[schemas.TopProduct])
def get_top_products(limit: int = 10, db: Session = Depends(get_db)):
    """Get top mentioned medical products"""
    return crud.get_top_products(db, limit)

@app.get("/api/channels/{channel_name}/activity", response_model=List[schemas.ChannelActivity])
def get_channel_activity(channel_name: str, db: Session = Depends(get_db)):
    """Get posting activity for a specific channel"""
    return crud.get_channel_activity(db, channel_name)

@app.get("/api/search/messages", response_model=List[schemas.SearchResult])
def search_messages(query: str, db: Session = Depends(get_db)):
    """Search messages containing a specific keyword"""
    return crud.search_messages(db, query)

@app.get("/api/reports/visual-content")
def get_visual_content_stats(db: Session = Depends(get_db)):
    """Get statistics about visual content in channels"""
    return crud.get_visual_content_stats(db)

@app.get("/api/reports/price-variation")
def get_price_variation(product: str, db: Session = Depends(get_db)):
    """Get price variation for a specific product"""
    # This is a placeholder - you would need to implement actual price extraction
    # from messages which is complex without structured price data
    return {"message": "Price analysis would require more sophisticated NLP to extract prices from messages"}