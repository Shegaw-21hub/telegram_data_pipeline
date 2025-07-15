# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ChannelBase(BaseModel):
    channel_name: str
    first_seen_date: Optional[date] = None
    last_seen_date: Optional[date] = None
    total_messages: Optional[int] = None

class Channel(ChannelBase):
    channel_key: str
    
    class Config:
        orm_mode = True

class MessageBase(BaseModel):
    message_text: Optional[str] = None
    view_count: Optional[int] = None
    has_media: Optional[bool] = None
    media_type: Optional[str] = None
    contains_drug_mention: Optional[bool] = None

class Message(MessageBase):
    message_key: str
    channel_key: str
    date_key: date
    
    class Config:
        orm_mode = True

class DetectionBase(BaseModel):
    class_name: str
    confidence: float
    detection_category: str

class Detection(DetectionBase):
    detection_id: int
    message_key: str
    
    class Config:
        orm_mode = True

class TopProduct(BaseModel):
    product_name: str
    mention_count: int

class ChannelActivity(BaseModel):
    date: date
    message_count: int

class SearchResult(BaseModel):
    message_id: int
    channel_name: str
    message_date: date
    message_text: str