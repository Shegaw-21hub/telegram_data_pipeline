# app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
import models
import schemas
from typing import List

def get_top_products(db: Session, limit: int = 10) -> List[schemas.TopProduct]:
    # Common drug names to look for
    drug_names = [
        'paracetamol', 'amoxicillin', 'insulin', 'ventolin',
        'metformin', 'atenolol', 'losartan', 'simvastatin',
        'omeprazole', 'diclofenac'
    ]
    
    conditions = []
    for drug in drug_names:
        conditions.append(
            func.lower(models.Message.message_text).like(f'%{drug}%')
        )
    
    query = db.query(
        func.unnest(func.string_to_array(
            func.array_to_string(
                func.array_agg(models.Message.message_text), 
                ' '
            ), 
            ' '
        )).label('word'),
        func.count().label('count')
    ).filter(
        or_(*conditions)
    ).group_by(
        'word'
    ).order_by(
        func.count().desc()
    ).limit(limit)
    
    results = query.all()
    
    # Filter to only include actual drug names
    top_products = []
    for word, count in results:
        lower_word = word.lower()
        for drug in drug_names:
            if drug in lower_word and len(word) > 3:  # Basic filtering
                top_products.append(schemas.TopProduct(
                    product_name=word,
                    mention_count=count
                ))
                break
    
    return top_products[:limit]

def get_channel_activity(db: Session, channel_name: str) -> List[schemas.ChannelActivity]:
    return db.query(
        models.Date.date,
        func.count(models.Message.message_key).label('message_count')
    ).join(
        models.Message,
        models.Message.date_key == models.Date.date
    ).join(
        models.Channel,
        models.Message.channel_key == models.Channel.channel_key
    ).filter(
        models.Channel.channel_name == channel_name
    ).group_by(
        models.Date.date
    ).order_by(
        models.Date.date
    ).all()

def search_messages(db: Session, query: str) -> List[schemas.SearchResult]:
    return db.query(
        models.Message.message_id,
        models.Channel.channel_name,
        models.Date.date.label('message_date'),
        models.Message.message_text
    ).join(
        models.Channel,
        models.Message.channel_key == models.Channel.channel_key
    ).join(
        models.Date,
        models.Message.date_key == models.Date.date
    ).filter(
        func.lower(models.Message.message_text).like(f'%{query.lower()}%')
    ).order_by(
        models.Date.date.desc()
    ).limit(100).all()

def get_visual_content_stats(db: Session):
    return db.query(
        models.Detection.class_name,
        func.count().label('count'),
        models.Channel.channel_name
    ).join(
        models.Message,
        models.Detection.message_key == models.Message.message_key
    ).join(
        models.Channel,
        models.Message.channel_key == models.Channel.channel_key
    ).filter(
        models.Detection.detection_category == 'medical'
    ).group_by(
        models.Detection.class_name,
        models.Channel.channel_name
    ).order_by(
        func.count().desc()
    ).all()