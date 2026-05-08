from pydantic import BaseModel
from typing import Optional


class PriceData(BaseModel):
    asset: str
    price: float
    change_24h: Optional[float] = None
    volume: Optional[float] = None
    currency: str = "USD"


class CandleData(BaseModel):
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float