from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class BotCreate(BaseModel):
    name: str
    asset: str
    strategy: str = "ensemble"
    interval: str = "5m"
    email_alert: bool = False


class BotUpdate(BaseModel):
    name: Optional[str] = None
    asset: Optional[str] = None
    strategy: Optional[str] = None
    interval: Optional[str] = None
    email_alert: Optional[bool] = None
    status: Optional[str] = None


class BotResponse(BaseModel):
    id: int
    name: str
    asset: str
    strategy: str
    status: str
    interval: str
    email_alert: bool
    user_id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)