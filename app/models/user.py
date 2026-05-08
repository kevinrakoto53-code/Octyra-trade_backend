from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from typing import Optional
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    plan_id: Mapped[int] = mapped_column(ForeignKey("plans.id"), default=1)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    # Relations
    plan: Mapped["Plan"] = relationship("Plan", backref="users")
    bots: Mapped[list["Bot"]] = relationship(
        "Bot", backref="owner", cascade="all, delete-orphan"
    )