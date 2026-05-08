from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NewsItem(BaseModel):
    id: int
    title: str
    source: Optional[str] = None
    url: Optional[str] = None
    sentiment: str
    impact: float
    asset_related: Optional[str] = None
    published_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SentimentResult(BaseModel):
    title: str
    sentiment: str
    impact: float
    explanation: str