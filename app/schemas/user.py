from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class PlanResponse(BaseModel):
    id: int
    name: str
    max_bots: int
    email_alerts: bool
    api_access: bool
    backtesting: bool
    price: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UpdateProfile(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None

class UpdatePassword(BaseModel):
    current_password: str
    new_password: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    avatar: Optional[str] = None
    is_active: bool
    plan_id: int
    created_at: Optional[datetime] = None
    plan: Optional[PlanResponse] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None