from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, DateTime, Integer, ForeignKey
from sqlalchemy.sql import func
from typing import Optional
from app.db.base import Base


class Signal(Base):
    __tablename__ = "signals"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    asset: Mapped[str] = mapped_column(String, nullable=False)
    rf_signal: Mapped[str] = mapped_column(String, nullable=False)   
    xgb_signal: Mapped[str] = mapped_column(String, nullable=False)  
    final_decision: Mapped[str] = mapped_column(String, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )