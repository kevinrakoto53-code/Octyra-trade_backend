from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, DateTime, Text
from sqlalchemy.sql import func
from typing import Optional
from app.db.base import Base


class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=True)
    url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sentiment: Mapped[str] = mapped_column(String, default="neutral")  # positive, negative, neutral
    impact: Mapped[float] = mapped_column(Float, default=0.0)  # -1.0 à 1.0
    asset_related: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    published_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )