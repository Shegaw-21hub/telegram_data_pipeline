# app/models.py
from sqlalchemy import Column, Integer, String, Float, JSON, Date, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean
from database import Base

class Channel(Base):
    __tablename__ = "dim_channels"

    channel_key = Column(String, primary_key=True, index=True)
    channel_name = Column(String, index=True)
    first_seen_date = Column(Date)
    last_seen_date = Column(Date)
    total_messages = Column(Integer)

class Date(Base):
    __tablename__ = "dim_dates"

    date = Column(Date, primary_key=True, index=True)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    quarter = Column(Integer)
    day_of_week = Column(Integer)
    day_of_year = Column(Integer)
    is_weekend = Column(Boolean)

class Message(Base):
    __tablename__ = "fct_messages"

    message_key = Column(String, primary_key=True, index=True)
    message_id = Column(Integer)
    channel_key = Column(String, ForeignKey("dim_channels.channel_key"))
    date_key = Column(Date, ForeignKey("dim_dates.date"))
    message_text = Column(String)
    view_count = Column(Integer)
    has_media = Column(Boolean)
    media_type = Column(String)
    media_path = Column(String)
    message_length = Column(Integer)
    contains_drug_mention = Column(Boolean)

class Detection(Base):
    __tablename__ = "fct_image_detections"

    detection_id = Column(Integer, primary_key=True, index=True)
    message_key = Column(String, ForeignKey("fct_messages.message_key"))
    class_id = Column(Integer)
    class_name = Column(String)
    confidence = Column(Float)
    bbox = Column(JSON)
    detection_category = Column(String)