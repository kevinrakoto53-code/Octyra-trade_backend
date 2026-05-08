from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey, DateTime, Integer
from sqlalchemy.sql import func
from typing import Optional
from app.db.base import Base


class Bot(Base):
    __tablename__ = "bots"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    asset: Mapped[str] = mapped_column(String, nullable=False)  # BTC, ETH, OR...
    strategy: Mapped[str] = mapped_column(String, default="ensemble")  # rf, xgb, ensemble
    status: Mapped[str] = mapped_column(String, default="stopped")  # active, stopped
    interval: Mapped[str] = mapped_column(String, default="5m")  # 5m, 15m, 1h
    exchange: Mapped[str] = mapped_column(String, default="binance_testnet")
    email_alert: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relations
    trades: Mapped[list["Trade"]] = relationship(
        "Trade", backref="bot", cascade="all, delete-orphan"
    )