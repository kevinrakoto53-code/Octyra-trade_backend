from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TradeResponse(BaseModel):
    id: int
    bot_id: int
    asset: str
    action: str
    price: float
    quantity: float
    rf_signal: Optional[str] = None
    xgb_signal: Optional[str] = None
    final_decision: str
    executed_at: Optional[datetime] = None

    class Config:
        from_attributes = True